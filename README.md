# Intern Activity Tracker

A Python-based Intern Activity Tracker developed progressively from a console application to a FastAPI web application.

The project was completed in three stages:

- Day 1: Single Intern Prototype
- Day 2: Multi-Intern Console System
- Day 3: FastAPI Web Application with Async File Operations

---

## Project Overview

The Intern Activity Tracker allows intern information and daily work activities to be recorded and stored using JSON.

The project demonstrates the progression from basic Python programming to a REST API using FastAPI.

The application supports:

- Intern registration
- Unique intern ID generation
- Intern status tracking
- Daily activity logging
- Total and average working hours
- Individual intern summaries
- Overall statistics
- Top performer identification
- JSON-based data persistence
- REST API endpoints
- Pydantic request validation
- Asynchronous file operations

---

# Day 1 - Single Intern Prototype

## Objective

The goal of Day 1 was to build a basic console-based application for managing the activities of a single intern.

## Concepts Covered

- Python syntax and execution flow
- User input
- Input validation
- Lists
- Dictionaries
- Object-Oriented Programming
- Classes and objects
- Functions
- try/except error handling
- JSON file operations
- String manipulation and formatting

## Implementation

An `Intern` class was created with the following attributes:

- `name`
- `role`
- `daily_hours`
- `daily_tasks`

The application:

1. Takes the intern's name and role as input.
2. Cleans the input using `strip()` and `title()`.
3. Creates an `Intern` object.
4. Asks how many days of activity should be recorded.
5. Accepts hours worked and task descriptions for each day.
6. Validates that working hours are numeric and non-negative.
7. Calculates total working hours.
8. Calculates average working hours.
9. Generates a formatted intern summary.
10. Converts the intern object into a dictionary.
11. Saves the data to `intern.json`.
12. Reads the JSON file back for verification.

## Day 1 Output

The application displays:

- Intern name
- Intern role
- Total working hours
- Average working hours
- Task history
- Hours worked for each day

---

# Day 2 - Multi-Intern Console System

## Objective

Day 2 extended the single-intern application into a multi-intern tracking system with status management.

## Concepts Covered

- Multi-record data management
- Lists of dictionaries
- Menu-driven applications
- Unique ID generation
- Status-based workflow
- Data aggregation
- Performance ranking

## Implementation

The `Intern` class was enhanced with:

- `intern_id`
- `name`
- `role`
- `status`
- `daily_hours`
- `daily_tasks`

New interns receive the default status:

```text
Active
```

Unique IDs are generated automatically, such as:

```text
INT001
INT002
INT003
```

Intern records are stored in a list and persisted to:

```text
interns.json
```

## Main Features

### 1. Add Intern

The application accepts:

- Intern name
- Intern role

A unique intern ID is generated automatically.

The intern is initially assigned:

```text
Active
```

The information is then saved to the JSON file.

### 2. Add Daily Activity

The user enters an intern ID.

The system checks whether the intern exists.

Activity can only be added when the intern's status is:

```text
Active
```

Activities cannot be added when the intern is:

```text
Inactive
```

or:

```text
Completed
```

### 3. Update Intern Status

The status can be changed using the menu:

```text
1. Active
2. Inactive
3. Completed
```

The updated status is immediately saved to JSON.

### 4. View Intern Summary

The application displays:

- Intern ID
- Name
- Role
- Current status
- Total hours
- Average hours
- Complete task history
- Most recent activity

### 5. Overall Statistics

The application calculates:

- Total number of interns
- Number of active interns
- Average working hours
- Top performer based on total hours worked

### 6. Menu-Driven Interface

The main menu provides the following options:

```text
1. Add Intern
2. Add Daily Activity
3. Update Intern Status
4. View Intern Summary
5. Overall Statistics
6. Exit
```

---

# Day 3 - FastAPI Web Application

## Objective

Day 3 converted the console-based Intern Activity Tracker into a web-based REST API using FastAPI.

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pydantic
- aiofiles
- JSON

## Concepts Covered

- FastAPI application architecture
- REST API design
- HTTP methods
- API endpoints
- Path parameters
- Request bodies
- Pydantic models
- Async/await
- Asynchronous file operations
- Uvicorn server
- Swagger UI
- JSON responses

---

## FastAPI Application

The FastAPI application is initialized using:

```python
app = FastAPI(title="Intern Activity Tracker")
```

The application is run using Uvicorn.

For the current file name `d3_fastapi.py`, the application can be started with:

```powershell
python -m uvicorn d3_fastapi:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```

---

# Pydantic Models

Pydantic is used to validate incoming API request data.

## InternInput

```python
class InternInput(BaseModel):
    name: str
    role: str
```

This model expects:

- `name` as a string
- `role` as a string

Example request:

```json
{
    "name": "Harsh",
    "role": "Python Intern"
}
```

## ActivityInput

```python
class ActivityInput(BaseModel):
    hours: float
    task: str
```

This model expects:

- `hours` as a number
- `task` as a string

Example request:

```json
{
    "hours": 6,
    "task": "Worked on FastAPI"
}
```

---

# Async File Operations

The application uses `aiofiles` for asynchronous JSON file operations.

The data is read using:

```python
async def read_data():
```

and:

```python
data = await file.read()
```

Data is written using:

```python
async def write_data(data):
```

and:

```python
await file.write(...)
```

Using `async` and `await` allows file I/O operations to be handled asynchronously so that the server does not unnecessarily block while waiting for file operations.

---

# API Endpoints

## 1. Home

### GET `/`

Checks whether the API is running.

Response:

```json
{
    "message": "Intern Activity Tracker API is running"
}
```

---

## 2. Add Intern

### POST `/interns`

Creates a new intern.

### Request Body

```json
{
    "name": "Harsh",
    "role": "Python Intern"
}
```

### Response

```json
{
    "message": "Intern added successfully",
    "intern_id": "INT001"
}
```

A new intern is created with:

```text
status = Active
```

---

## 3. Add Daily Activity

### POST `/interns/{intern_id}/activity`

Adds a daily activity for a specific intern.

Example:

```text
/interns/INT001/activity
```

### Request Body

```json
{
    "hours": 6,
    "task": "Worked on FastAPI"
}
```

The API checks:

1. Whether the intern exists.
2. Whether the intern is Active.
3. Whether the number of hours is non-negative.

---

## 4. View Intern Summary

### GET `/interns/{intern_id}`

Returns the details and activity summary of a specific intern.

Example:

```text
/interns/INT001
```

The response includes:

- Intern ID
- Name
- Role
- Status
- Daily hours
- Daily tasks
- Total hours
- Average hours

---

## 5. Overall Statistics

### GET `/statistics`

Returns overall statistics for all interns.

The response includes:

- Total number of interns
- Average hours
- Top performer

Example:

```json
{
    "total_interns": 2,
    "average_hours": 6.5,
    "top_performer": {
        "intern_id": "INT001",
        "name": "Harsh",
        "total_hours": 12
    }
}
```

---

# Project Structure

```text
Intern Activity Tracker/
│
├── d3_fastapi.py
├── interns.json
├── README.md
└── ...
```

`d3_fastapi.py` contains the FastAPI application.

`interns.json` stores intern information and activity data.

`README.md` documents the project and its progression from Day 1 to Day 3.

---

# How to Run the Project

## 1. Open the project directory

```powershell
cd "C:\Users\HarshPawar\Desktop\Capstone\Intern Activity Tracker"
```

## 2. Install dependencies

```powershell
python -m pip install fastapi uvicorn aiofiles
```

## 3. Start the FastAPI server

```powershell
python -m uvicorn d3_fastapi:app --reload
```

## 4. Open the API

```text
http://127.0.0.1:8000
```

## 5. Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all available API endpoints.

---

# Day 1 to Day 3 Progression

The project progressed through three stages:

```text
Day 1
Single Intern
     ↓
Python Classes + Lists + Functions + JSON
     ↓
Day 2
Multi-Intern System
     ↓
IDs + Status Tracking + Statistics + Menu
     ↓
Day 3
FastAPI Web Application
     ↓
REST API + Pydantic + Async/Await + Swagger UI
```

This progression demonstrates how a simple Python console application can be gradually developed into a web-based API application.

---

# Learning Outcome

By completing the three stages, the project demonstrates practical understanding of:

- Python programming
- Object-Oriented Programming
- Input validation
- Error handling
- JSON persistence
- Multi-record data management
- REST API development
- FastAPI
- Pydantic
- Async/await
- Asynchronous file operations
- Uvicorn
- Swagger UI
- API testing