from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.routers import auth, courses, enrollment, payments, progress, admin
import subprocess
import tempfile
import os

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

# Request model for code execution
class CodeRequest(BaseModel):
    code: str
    framework: str

@app.get("/")
def home():
    return {"message": "QuantumLearn Backend Running 🚀"}

@app.post("/run")
async def run_code(request: CodeRequest):
    try:
        # Framework validation
        if request.framework not in ["qiskit", "cirq"]:
            return {"output": "Invalid framework selected"}

        # Create temp python file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
            temp.write(request.code.encode())
            temp_path = temp.name

        # Execute file
        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=10000
        )

        # Remove temp file
        os.remove(temp_path)

        output = result.stdout if result.stdout else result.stderr

        return {"output": output}

    except subprocess.TimeoutExpired:
        return {"output": "Execution timed out (10 seconds limit)"}

    except Exception as e:
        return {"output": str(e)}

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(enrollment.router)
app.include_router(payments.router)
app.include_router(progress.router)
app.include_router(admin.router)