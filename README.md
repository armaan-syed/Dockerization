# Student Performance Analyzer API

A REST API built with FastAPI for analyzing student academic performance. This application calculates total marks, averages, percentages, grades, and pass/fail status based on student marks input.

## Features

- Calculate student performance metrics (total, average, percentage, grade)
- Determine pass/fail status based on performance
- View all sample students and their performance
- Identify the topper (highest-performing student)
- Input validation using Pydantic models
- Interactive API documentation with Swagger UI
- Health check endpoint for monitoring

## Tech Stack

- **Python** 3.11+
- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **Pydantic** - Data validation using Python type annotations

## Project Structure

```
student-performance-api/
│
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Git ignore rules
```

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Steps

1. **Clone or download this project**

2. **Navigate to the project directory**
   ```bash
   cd student-performance-api
   ```

3. **Create a virtual environment**
   
   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

**Note**: The application listens on `0.0.0.0` to ensure it works properly when containerized with Docker later.

## API Endpoints

### 1. Root Endpoint
- **GET** `/`
- Returns application information

### 2. Health Check
- **GET** `/health`
- Returns server health status

### 3. Analyze Student Performance
- **POST** `/analyze`
- Accepts student data and calculates performance metrics

**Request Body:**
```json
{
  "name": "Armaan",
  "marks": {
    "Mathematics": 85,
    "Computer Networks": 78,
    "Cloud Computing": 91,
    "Machine Learning": 88,
    "Cyber Security": 82
  }
}
```

**Response:**
```json
{
  "name": "Armaan",
  "total_marks": 424,
  "max_marks": 500,
  "average": 84.8,
  "percentage": 84.8,
  "grade": "A",
  "result": "PASS"
}
```

### 4. Get All Students
- **GET** `/students`
- Returns performance summary of all sample students

### 5. Get Topper
- **GET** `/students/topper`
- Returns the student with highest percentage

## Grading System

- **A+**: 90-100%
- **A**: 80-89%
- **B**: 70-79%
- **C**: 60-69%
- **D**: 50-59%
- **E**: 40-49%
- **F**: Below 40%

**Pass/Fail**: Students with average marks ≥ 40 pass, otherwise fail.

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Use Swagger UI to test all endpoints interactively through a web interface.

## Validation Rules

- Student name cannot be empty
- Marks must be between 0 and 100
- At least one subject must be provided
- Invalid input returns appropriate HTTP error responses

## Example Usage

### Using curl

```bash
# Check if server is running
curl http://localhost:8000/health

# Analyze a student
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Armaan",
    "marks": {
      "Mathematics": 85,
      "Computer Networks": 78,
      "Cloud Computing": 91,
      "Machine Learning": 88,
      "Cyber Security": 82
    }
  }'

# Get all students
curl http://localhost:8000/students

# Get topper
curl http://localhost:8000/students/topper
```

### Using Python requests

```python
import requests

# Analyze student
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "name": "Armaan",
        "marks": {
            "Mathematics": 85,
            "Computer Networks": 78,
            "Cloud Computing": 91,
            "Machine Learning": 88,
            "Cyber Security": 82
        }
    }
)
print(response.json())
```

## Development

To stop the server, press `Ctrl+C` in the terminal.

To deactivate the virtual environment:
```bash
deactivate
```

## Next Steps

This application is ready for:
- Dockerization
- Container registry deployment
- Cloud deployment
- CI/CD pipeline integration

---

**Built for College Practical: Experiment 9 - Dockerization and Deployment**
