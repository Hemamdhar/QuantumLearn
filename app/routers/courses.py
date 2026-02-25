from fastapi import APIRouter, HTTPException, Depends
from app.database import db
from app.schemas import CourseCreate, CourseResponse
from app.security import admin_required
from typing import List

from bson import ObjectId

router = APIRouter()

@router.post("/courses")
def create_course(course: CourseCreate, admin: dict = Depends(admin_required)):

    new_course = {
        "title": course.title,
        "description": course.description,
        "price": course.price
    }

    result = db.courses.insert_one(new_course)

    return {
        "message": "Course created",
        "course_id": str(result.inserted_id)
    }


@router.get("/courses", response_model=List[CourseResponse])
def get_courses():

    courses = list(db.courses.find())

    result = []
    for course in courses:
        result.append({
            "id": str(course["_id"]),
            "title": course["title"],
            "description": course["description"],
            "price": course["price"]
        })

    return result