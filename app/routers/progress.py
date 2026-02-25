from fastapi import APIRouter, Depends
from app.database import db
from app.security import get_current_user

router = APIRouter()

@router.post("/courses/{course_id}/progress")
def update_progress(course_id: str, completed_lessons: int, current_user: dict = Depends(get_current_user)):

    db.progress.update_one(
        {
            "course_id": course_id,
            "student_email": current_user["email"]
        },
        {
            "$set": {"completed_lessons": completed_lessons}
        },
        upsert=True
    )

    return {"message": "Progress updated"}