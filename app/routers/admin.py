from fastapi import APIRouter, Depends, HTTPException
from app.database import db
from app.security import get_current_user
from app.schemas import AdminStatsResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats", response_model=AdminStatsResponse)
def get_admin_stats(current_user: dict = Depends(get_current_user)):

    # ✅ Only admin allowed
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    total_users = db.users.count_documents({})
    total_students = db.users.count_documents({"role": "student"})
    total_admins = db.users.count_documents({"role": "admin"})
    total_courses = db.courses.count_documents({})
    total_enrollments = db.enrollments.count_documents({})

    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_admins": total_admins,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments
    }