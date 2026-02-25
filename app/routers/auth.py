from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import db
from app.security import hash_password, verify_password, create_access_token
from app.schemas import UserCreate

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):

    existing = db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = hash_password(user.password)

    new_user = {
    "name": user.name,
    "email": user.email,
    "password": hashed_password,
    "role": "student"  # default role
}

    db.users.insert_one(new_user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    db_user = db.users.find_one({"email": form_data.username})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": db_user["email"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }