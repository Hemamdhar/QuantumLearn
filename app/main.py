from fastapi import FastAPI
from app.routers import auth, courses, enrollment, payments, progress, admin

app = FastAPI()

@app.get("/")
def home():
    return {"message": "QuantumLearn Backend Running 🚀"}

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(enrollment.router)
app.include_router(payments.router)
app.include_router(progress.router)
app.include_router(admin.router)