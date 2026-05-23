from ninja import Router
from django.shortcuts import get_object_or_404

from lms.models import Course, Enrollment, Progress, Lesson
from lms.mongo import log_activity, log_learning_analytics
from lms.tasks import send_enrollment_email, generate_certificate
from .jwt_utils import decode_token
from .permissions import get_user_from_token

router = Router()


@router.post("/")
def enroll(request, course_id: int):
    user = get_user_from_token(request, decode_token)

    if not user:
        return {"error": "Unauthorized"}

    if user.role != "student":
        return {"error": "Only student can enroll"}

    course = get_object_or_404(Course, id=course_id)

    enrollment, created = Enrollment.objects.get_or_create(
        student=user,
        course=course
    )

    if not created:
        return {"error": "Already enrolled"}

    send_enrollment_email.delay(
        user.email or "student@example.com", course.title, user.username)

    log_activity(user.username, "enroll_course", course_id=course.id)
    log_learning_analytics(user.username, course.id, event="enroll")

    return {
        "message": "enrolled",
        "course": course.title,
        "email_task": "queued"
    }


@router.get("/my-courses")
def my_courses(request):
    user = get_user_from_token(request, decode_token)

    if not user:
        return {"error": "Unauthorized"}

    enrollments = Enrollment.objects.for_student_dashboard().filter(student=user)

    return [
        {
            "course_id": e.course.id,
            "course": e.course.title,
            "lesson_count": e.course.lessons.count(),
        }
        for e in enrollments
    ]


@router.post("/{enroll_id}/progress")
def mark_progress(request, enroll_id: int, lesson_id: int):
    user = get_user_from_token(request, decode_token)

    if not user:
        return {"error": "Unauthorized"}

    enrollment = get_object_or_404(Enrollment, id=enroll_id, student=user)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if lesson.course != enrollment.course:
        return {"error": "Lesson not part of enrolled course"}

    progress, created = Progress.objects.get_or_create(
        student=user,
        lesson=lesson
    )

    progress.completed = True
    progress.save()

    log_activity(user.username, "complete_lesson", course_id=enrollment.course.id, details={
        "lesson_id": lesson.id,
        "lesson_title": lesson.title
    })
    log_learning_analytics(user.username, enrollment.course.id,
                           lesson_id=lesson.id, event="lesson_completed")

    total_lessons = enrollment.course.lessons.count()
    completed_lessons = Progress.objects.filter(
        student=user,
        lesson__course=enrollment.course,
        completed=True
    ).count()

    if total_lessons > 0 and completed_lessons == total_lessons:
        generate_certificate.delay(user.username, enrollment.course.title)

    return {
        "message": "Progress updated",
        "lesson": lesson.title,
        "completed": progress.completed,
        "course_completed": total_lessons == completed_lessons
    }
