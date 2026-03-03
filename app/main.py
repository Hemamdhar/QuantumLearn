from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, courses, enrollment, payments, progress, admin

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://quantumlearn-frontend.vercel.app",  # future production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "QuantumLearn Backend Running 🚀"}

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(enrollment.router)
app.include_router(payments.router)
app.include_router(progress.router)
app.include_router(admin.router)