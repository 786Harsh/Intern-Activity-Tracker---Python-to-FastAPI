import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiofiles


app = FastAPI(title="Intern Activity Tracker")

FILE_NAME = "interns.json"


class InternInput(BaseModel):
    name: str
    role: str


class ActivityInput(BaseModel):
    hours: float
    task: str


async def read_data():
    if not os.path.exists(FILE_NAME):
        return []

    async with aiofiles.open(FILE_NAME, "r") as file:
        data = await file.read()

    if not data:
        return []

    return json.loads(data)


async def write_data(data):
    async with aiofiles.open(FILE_NAME, "w") as file:
        await file.write(json.dumps(data, indent=4))


def generate_intern_id(interns):
    if not interns:
        return "I001"

    numbers = []

    for intern in interns:
        intern_id = intern["intern_id"]
        numbers.append(int(intern_id[1:]))

    next_number = max(numbers) + 1

    return f"I{next_number:03d}"


@app.get("/")
async def home():
    return {"message": "Intern Activity Tracker API is running"}


@app.post("/interns")
async def add_intern(intern: InternInput):
    interns = await read_data()

    intern_id = generate_intern_id(interns)

    new_intern = {
        "intern_id": intern_id,
        "name": intern.name,
        "role": intern.role,
        "status": "Active",
        "daily_hours": [],
        "daily_tasks": []
    }

    interns.append(new_intern)

    await write_data(interns)

    return {
        "message": "Intern added successfully",
        "intern_id": intern_id
    }


@app.post("/interns/{intern_id}/activity")
async def add_activity(intern_id: str, activity: ActivityInput):
    interns = await read_data()

    intern = None

    for item in interns:
        if item["intern_id"] == intern_id:
            intern = item
            break

    if intern is None:
        raise HTTPException(
            status_code=404,
            detail="Intern not found"
        )

    if intern["status"] != "Active":
        raise HTTPException(
            status_code=400,
            detail="Activity cannot be added for an inactive or completed intern"
        )

    if activity.hours < 0:
        raise HTTPException(
            status_code=400,
            detail="Hours cannot be negative"
        )

    intern["daily_hours"].append(activity.hours)
    intern["daily_tasks"].append(activity.task)

    await write_data(interns)

    return {
        "message": "Daily activity added successfully",
        "intern_id": intern_id
    }


@app.get("/interns/{intern_id}")
async def get_intern_summary(intern_id: str):
    interns = await read_data()

    intern = None

    for item in interns:
        if item["intern_id"] == intern_id:
            intern = item
            break

    if intern is None:
        raise HTTPException(
            status_code=404,
            detail="Intern not found"
        )

    hours = intern["daily_hours"]

    if hours:
        total_hours = sum(hours)
        average_hours = total_hours / len(hours)
    else:
        total_hours = 0
        average_hours = 0

    return {
        "intern_id": intern["intern_id"],
        "name": intern["name"],
        "role": intern["role"],
        "status": intern["status"],
        "daily_hours": intern["daily_hours"],
        "daily_tasks": intern["daily_tasks"],
        "total_hours": total_hours,
        "average_hours": round(average_hours, 2)
    }


@app.get("/statistics")
async def get_statistics():
    interns = await read_data()

    if not interns:
        return {
            "total_interns": 0,
            "average_hours": 0,
            "top_performer": None
        }
        
    total_hours = 0
    total_days = 0

    top_performer = None
    highest_hours = 0

    for intern in interns:
        hours = intern["daily_hours"]

        intern_total = sum(hours)

        total_hours += intern_total
        total_days += len(hours)

        if intern_total > highest_hours:
            highest_hours = intern_total
            top_performer = {
                "intern_id": intern["intern_id"],
                "name": intern["name"],
                "total_hours": intern_total
            }

    if total_days > 0:
        average_hours = total_hours / total_days
    else:
        average_hours = 0

    return {
        "total_interns": len(interns),
        "average_hours": round(average_hours, 2),
        "top_performer": top_performer
    }