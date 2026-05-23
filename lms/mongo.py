from datetime import datetime
from pymongo import MongoClient
from django.conf import settings


client = MongoClient(settings.MONGO_URI)
db = client["lms_activity"]

activity_logs = db["activity_logs"]
learning_analytics = db["learning_analytics"]


def log_activity(username, action, course_id=None, details=None):
    activity_logs.insert_one({
        "username": username,
        "action": action,
        "course_id": course_id,
        "details": details or {},
        "timestamp": datetime.utcnow(),
    })


def log_learning_analytics(username, course_id, lesson_id=None, event="activity"):
    learning_analytics.insert_one({
        "username": username,
        "course_id": course_id,
        "lesson_id": lesson_id,
        "event": event,
        "timestamp": datetime.utcnow(),
    })
