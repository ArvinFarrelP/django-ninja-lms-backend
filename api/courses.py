from ninja import Router
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from lms.models import Course, Category
from lms.mongo import log_activity
from .jwt_utils import decode_token
from .permissions import get_user_from_token

router = Router()


@router.get("/", auth=None)
def list_courses(request, limit: int = 10, offset: int = 0):
    cache_key = f"course_list_{limit}_{offset}"

    cached_data = cache.get(cache_key)
    if cached_data:
        return {
            "source": "redis cache",
            **cached_data
        }

    qs = Course.objects.for_listing().all()
    total = qs.count()
    courses = qs[offset:offset + limit]

    data = []
    for c in courses:
        data.append({
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "instructor": c.instructor.username,
            "category": c.category.name if c.category else None,
        })

    result = {
        "count": total,
        "results": data
    }

    cache.set(cache_key, result, timeout=60)

    user = get_user_from_token(request, decode_token)
    if user:
        log_activity(user.username, "list_courses")

    return {
        "source": "database",
        **result
    }


@router.get("/{course_id}", auth=None)
def course_detail(request, course_id: int):
    cache_key = f"course_detail_{course_id}"

    cached_data = cache.get(cache_key)
    if cached_data:
        return {
            "source": "redis cache",
            "data": cached_data
        }

    course = get_object_or_404(Course.objects.for_listing(), id=course_id)

    data = {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "instructor": course.instructor.username,
        "category": course.category.name if course.category else None,
    }

    cache.set(cache_key, data, timeout=60)

    user = get_user_from_token(request, decode_token)
    if user:
        log_activity(user.username, "view_course_detail", course_id=course.id)

    return {
        "source": "database",
        "data": data
    }


@router.post("/")
def create_course(request, title: str, description: str, category_id: int = None):
    user = get_user_from_token(request, decode_token)

    if not user:
        return {"error": "Unauthorized"}

    if user.role != "instructor":
        return {"error": "Only instructor"}

    category = None
    if category_id:
        category = get_object_or_404(Category, id=category_id)

    course = Course.objects.create(
        title=title,
        description=description,
        instructor=user,
        category=category
    )

    cache.clear()

    log_activity(user.username, "create_course", course_id=course.id, details={
        "title": course.title
    })

    return {
        "id": course.id,
        "title": course.title,
        "message": "Course created"
    }


@router.patch("/{course_id}")
def update_course(request, course_id: int, title: str = None, description: str = None, category_id: int = None):
    user = get_user_from_token(request, decode_token)

    if not user:
        return {"error": "Unauthorized"}

    course = get_object_or_404(Course, id=course_id)

    if course.instructor != user and user.role != "admin":
        return {"error": "Not allowed"}

    if title is not None:
        course.title = title

    if description is not None:
        course.description = description

    if category_id is not None:
        course.category = get_object_or_404(Category, id=category_id)

    course.save()

    cache.clear()

    log_activity(user.username, "update_course", course_id=course.id)

    return {"message": "Course updated"}


@router.delete("/{course_id}")
def delete_course(request, course_id: int):
    user = get_user_from_token(request, decode_token)

    if not user:
        return {"error": "Unauthorized"}

    if user.role != "admin":
        return {"error": "Only admin"}

    course = get_object_or_404(Course, id=course_id)
    title = course.title
    course.delete()

    cache.clear()

    log_activity(user.username, "delete_course", course_id=course_id, details={
        "title": title
    })

    return {"message": "deleted"}
