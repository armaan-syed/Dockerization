from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Dict

app = FastAPI(
    title="Student Performance Analyzer",
    description="REST API for analyzing student academic performance",
    version="1.0.0"
)

# Pydantic Models
class StudentInput(BaseModel):
    name: str = Field(..., min_length=1, description="Student name")
    marks: Dict[str, float] = Field(..., description="Subject-wise marks")
    
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @field_validator('marks')
    @classmethod
    def validate_marks(cls, v):
        if not v:
            raise ValueError('At least one subject must be provided')
        for subject, mark in v.items():
            if mark < 0 or mark > 100:
                raise ValueError(f'Marks for {subject} must be between 0 and 100')
        return v


class PerformanceResult(BaseModel):
    name: str
    total_marks: float
    max_marks: float
    average: float
    percentage: float
    grade: str
    result: str


class StudentSummary(BaseModel):
    name: str
    percentage: float
    grade: str
    result: str


# In-memory storage for sample students
sample_students = [
    {
        "name": "Armaan",
        "marks": {
            "Mathematics": 85,
            "Computer Networks": 78,
            "Cloud Computing": 91,
            "Machine Learning": 88,
            "Cyber Security": 82
        }
    },
    {
        "name": "Priya",
        "marks": {
            "Mathematics": 92,
            "Computer Networks": 88,
            "Cloud Computing": 95,
            "Machine Learning": 90,
            "Cyber Security": 89
        }
    },
    {
        "name": "Rahul",
        "marks": {
            "Mathematics": 76,
            "Computer Networks": 72,
            "Cloud Computing": 80,
            "Machine Learning": 75,
            "Cyber Security": 78
        }
    },
    {
        "name": "Sneha",
        "marks": {
            "Mathematics": 68,
            "Computer Networks": 65,
            "Cloud Computing": 70,
            "Machine Learning": 72,
            "Cyber Security": 69
        }
    }
]


# Helper function to calculate grade
def calculate_grade(percentage: float) -> str:
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    elif percentage >= 40:
        return "E"
    else:
        return "F"


# Helper function to analyze performance
def analyze_performance(name: str, marks: Dict[str, float]) -> PerformanceResult:
    total_marks = sum(marks.values())
    num_subjects = len(marks)
    max_marks = num_subjects * 100
    average = total_marks / num_subjects
    percentage = (total_marks / max_marks) * 100
    grade = calculate_grade(percentage)
    result = "PASS" if average >= 40 else "FAIL"
    
    return PerformanceResult(
        name=name,
        total_marks=total_marks,
        max_marks=max_marks,
        average=round(average, 2),
        percentage=round(percentage, 2),
        grade=grade,
        result=result
    )


# API Endpoints
@app.get("/")
async def root():
    return {
        "application": "Student Performance Analyzer",
        "version": "1.0.0",
        "description": "REST API for analyzing student academic performance",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/analyze", response_model=PerformanceResult)
async def analyze_student(student: StudentInput):
    try:
        result = analyze_performance(student.name, student.marks)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/students", response_model=list[StudentSummary])
async def get_students():
    students_summary = []
    for student in sample_students:
        performance = analyze_performance(student["name"], student["marks"])
        students_summary.append(StudentSummary(
            name=performance.name,
            percentage=performance.percentage,
            grade=performance.grade,
            result=performance.result
        ))
    return students_summary


@app.get("/students/topper", response_model=StudentSummary)
async def get_topper():
    if not sample_students:
        raise HTTPException(status_code=404, detail="No students found")
    
    topper = None
    max_percentage = 0
    
    for student in sample_students:
        performance = analyze_performance(student["name"], student["marks"])
        if performance.percentage > max_percentage:
            max_percentage = performance.percentage
            topper = StudentSummary(
                name=performance.name,
                percentage=performance.percentage,
                grade=performance.grade,
                result=performance.result
            )
    
    return topper
