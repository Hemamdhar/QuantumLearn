from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.database import db
from app.security import get_current_user
from app.schemas import CourseResponse
from typing import List
from datetime import datetime

router = APIRouter()

# ✅ Enroll in course (Students only)
@router.post("/enroll/{course_id}")
def enroll_course(course_id: str, current_user: dict = Depends(get_current_user)):

    # 1️⃣ Only students allowed
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can enroll")

    # 2️⃣ Check course exists
    course = db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # 3️⃣ Prevent duplicate enrollment
    existing = db.enrollments.find_one({
        "student_email": current_user["email"],
        "course_id": course_id
    })

    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")

    # 4️⃣ Insert enrollment
    db.enrollments.insert_one({
        "student_email": current_user["email"],
        "course_id": course_id
    })

    return {"message": "Enrollment successful"}


@router.get("/my-courses", response_model=List[CourseResponse])
def get_my_courses(current_user: dict = Depends(get_current_user)):

    enrollments = list(db.enrollments.find({
        "student_email": current_user["email"]
    }))

    course_ids = [ObjectId(e["course_id"]) for e in enrollments]

    courses = list(db.courses.find({
        "_id": {"$in": course_ids}
    }))

    result = []
    for course in courses:
        result.append({
            "id": str(course["_id"]),
            "title": course["title"],
            "description": course["description"],
            "price": course["price"]
        })

    return result
@router.get("/enrolled-courses")
async def get_enrolled_courses(current_user: dict = Depends(get_current_user)):

    # Get user email from token
    user_email = current_user["sub"]

    # Find all enrollments for this user
    enrollments = await db.enrollments.find({
        "user_email": user_email
    }).to_list(100)

    course_ids = [enrollment["course_id"] for enrollment in enrollments]

    # Fetch full course details
    courses = await db.courses.find({
        "_id": {"$in": course_ids}
    }).to_list(100)

    # Convert ObjectId to string
    for course in courses:
        course["_id"] = str(course["_id"])

    return courses