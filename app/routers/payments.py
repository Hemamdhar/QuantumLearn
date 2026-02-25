from fastapi import APIRouter, Depends, HTTPException
from app.database import db
from app.security import get_current_user
from bson import ObjectId

router = APIRouter()

@router.post("/courses/{course_id}/pay")
def simulate_payment(course_id: str, current_user: dict = Depends(get_current_user)):

    course = db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.payments.insert_one({
        "course_id": course_id,
        "student_email": current_user["email"],
        "amount": course["price"],
        "status": "paid"
    })

    return {"message": "Payment successful"}