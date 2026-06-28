from celery import shared_task
from datetime import datetime
import csv
import os


@shared_task
def send_enrollment_email(user_email, course_title, username):
    print(f"Sending enrollment email to {user_email} for {course_title}")

    return {
        "task": "send_enrollment_email",
        "status": "success",
        "email": user_email,
        "course": course_title,
        "username": username,
        "timestamp": str(datetime.utcnow())
    }


@shared_task
def generate_certificate(username, course_title):
    print(f"Generating certificate for {username} - {course_title}")

    return {
        "task": "generate_certificate",
        "status": "success",
        "username": username,
        "course": course_title,
        "timestamp": str(datetime.utcnow())
    }


@shared_task
def update_course_statistics():
    from lms.models import Course, Enrollment

    course_count = Course.objects.count()
    enrollment_count = Enrollment.objects.count()

    print(
        f"[Statistics Updated] Courses={course_count}, Enrollments={enrollment_count}"
    )

    return {
        "task": "update_course_statistics",
        "status": "success",
        "courses": course_count,
        "enrollments": enrollment_count,
        "timestamp": str(datetime.utcnow())
    }


@shared_task
def export_course_report(course_id):
    from lms.models import Course

    try:
        course = Course.objects.get(id=course_id)

        os.makedirs("reports", exist_ok=True)

        file_path = f"reports/course_{course_id}_report.csv"

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Course ID",
                "Course Title",
                "Enrollment Count"
            ])

            writer.writerow([
                course.id,
                course.title,
                course.enrollments.count()
            ])

        print(f"Report exported: {file_path}")

        return {
            "task": "export_course_report",
            "status": "success",
            "file": file_path,
            "timestamp": str(datetime.utcnow())
        }

    except Exception as e:
        return {
            "task": "export_course_report",
            "status": "failed",
            "error": str(e),
            "timestamp": str(datetime.utcnow())
        }
