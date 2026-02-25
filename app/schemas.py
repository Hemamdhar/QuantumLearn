from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "student"  # default to student if not provided

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class CourseCreate(BaseModel):
    title: str
    description: str
    price: float

class CourseResponse(BaseModel):
    id: str
    title: str
    description: str
    price: float
    instructor_email: str

class CourseResponse(BaseModel):
    id: str
    title: str
    description: str
    price: float


class AdminStatsResponse(BaseModel):
    total_users: int
    total_students: int
    total_admins: int
    total_courses: int
    total_enrollments: int