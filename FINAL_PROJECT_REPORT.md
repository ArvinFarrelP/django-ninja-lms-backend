# FINAL PROJECT REPORT

## Student Information

| Information | Details                                                  |
| ----------- | -------------------------------------------------------- |
| Name        | Arvin Farrel Pramuditya                                  |
| NIM         | A11.2023.15062                                           |
| Class       | _(A11.4618)_                                             |
| Course      | Server-Side Programming                                  |
| Repository  | https://github.com/ArvinFarrelP/django-ninja-lms-backend |

---

# Project Description

This project is a production-like Learning Management System (LMS) backend built using Django Ninja REST API.

The system supports authentication, role-based access control, course management, student enrollment, lesson progress tracking, Redis caching, MongoDB analytics, asynchronous task processing using Celery and RabbitMQ, task monitoring with Flower, and containerized deployment using Docker Compose.

---

# Core Features

The following core LMS features have been successfully implemented.

- JWT Authentication
- Refresh Token
- Role-Based Access Control (Admin, Instructor, Student)
- Course CRUD
- Enrollment System
- Lesson Progress Tracking
- Course Export API
- Swagger API Documentation
- Django Admin

---

# Additional Features

| No  | Feature                               | Category                          | Points |  Status   |
| --- | ------------------------------------- | --------------------------------- | -----: | :-------: |
| 1   | Redis Caching for Course              | Redis, Caching and Performance    |     12 | Completed |
| 2   | Cache Invalidation Strategy           | Redis, Caching and Performance    |     12 | Completed |
| 3   | MongoDB Activity Logging              | MongoDB & Analytics               |     15 | Completed |
| 4   | Learning Analytics Collection         | MongoDB & Analytics               |     15 | Completed |
| 5   | Async Email Notification              | Celery, RabbitMQ & Async          |     12 | Completed |
| 6   | Async Certificate & Report Generation | Celery, RabbitMQ & Async          |     18 | Completed |
| 7   | Scheduled Task (Celery Beat)          | Celery, RabbitMQ & Async          |     15 | Completed |
| 8   | Flower Monitoring                     | Celery, RabbitMQ & Async          |      8 | Completed |
| 9   | Production-like Docker Compose        | Deployment & Production Readiness |     12 | Completed |

**Total Implemented Points : 119**

**Maximum Counted Points : 50**

---

# Implementation Summary

The project integrates several backend technologies.

- PostgreSQL as the primary relational database.
- Redis for API caching.
- MongoDB for activity logging and learning analytics.
- RabbitMQ as the message broker.
- Celery Worker for asynchronous background processing.
- Celery Beat for scheduled tasks.
- Flower for monitoring Celery workers and tasks.
- Docker Compose for container orchestration.

---

# How to Run

Clone the repository.

```bash
git clone https://github.com/ArvinFarrelP/django-ninja-lms-backend.git

cd django-ninja-lms-backend
```

Start the application.

```bash
docker compose up --build
```

Run migrations.

```bash
docker compose exec web python manage.py migrate
```

Load demo data.

```bash
docker compose exec web python manage.py loaddata fixtures.json
```

Open Swagger.

```
http://localhost:8000/api/docs
```

---

# Demo Accounts

## Admin

Username

```
admin
```

Password

```
password123
```

## Instructor

Username

```
arvin
```

Password

```
password123
```

## Student

Username

```
student1
```

Password

```
password123
```

---

# Important API Endpoints

Authentication

```
POST /api/auth/login
```

Courses

```
GET /api/courses
POST /api/courses
PATCH /api/courses/{id}
DELETE /api/courses/{id}
```

Enrollment

```
POST /api/enrollments
```

Lesson Progress

```
POST /api/enrollments/{enroll_id}/progress
```

Course Report

```
POST /api/courses/{id}/export
```

---

# Testing Evidence

All implemented features have been tested and documented.

Testing screenshots are available inside the following folders.

```
img/

1_Redis_Cache/

2_Cache_Invalidation/

3_MongoDB_Activity/

4_Learning_Analytics/

5_Async_Email_Notification/

6_Async_Report/

7_Async_Certificate/

8_Scheduled_Task/

9_Flower_Monitoring/

10_Docker_Compose/
```

---

# Challenges and Solutions

| Challenge                                         | Solution                                                          |
| ------------------------------------------------- | ----------------------------------------------------------------- |
| Redis cache was not refreshed after course update | Implemented cache invalidation using `cache.clear()`              |
| Unauthorized API requests                         | Implemented JWT Bearer Authentication                             |
| Background task execution                         | Configured RabbitMQ and Celery Worker                             |
| Scheduled tasks                                   | Configured Celery Beat                                            |
| Task monitoring                                   | Implemented Flower dashboard                                      |
| Analytics storage                                 | Used MongoDB collections for activity logs and learning analytics |

---

# Conclusion

This project successfully implements a production-like Learning Management System backend using Django Ninja and modern backend technologies.

The project integrates PostgreSQL, Redis, MongoDB, RabbitMQ, Celery Worker, Celery Beat, Flower, and Docker Compose to build a scalable backend system.

All required core features and selected additional features have been implemented, tested, documented, and demonstrated through screenshots included in the repository.

The project satisfies the requirements of the Server-Side Programming Final Project while demonstrating practical backend engineering concepts including REST API development, caching, asynchronous processing, monitoring, analytics, and containerized deployment.
