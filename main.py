from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import init_db, create_task, get_tasks, get_task_by_id, update_task_status, delete_task

app = FastAPI()

# Pydantic models for validation
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    status: str

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# 1. Create Task
@app.post("/tasks/")
async def create_task_endpoint(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title must not be empty")
    task_id = create_task(task.title, task.description)
    return {"id": task_id, "title": task.title, "description": task.description, "status": "pending", "created_at": "2025-08-26 21:45:00"}

# 2. List All Tasks
@app.get("/tasks/")
async def list_tasks():
    tasks = get_tasks()
    return [{"id": task[0], "title": task[1], "description": task[2], "status": task[3], "created_at": task[4]} for task in tasks]

# 3. Get Task by ID
@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task[0], "title": task[1], "description": task[2], "status": task[3], "created_at": task[4]}

# 4. Update Task Status
@app.put("/tasks/{task_id}/status")
async def update_task_status_endpoint(task_id: int, task: TaskUpdate):
    if task.status not in ["pending", "completed"]:
        raise HTTPException(status_code=400, detail="Status must be 'pending' or 'completed'")
    if update_task_status(task_id, task.status):
        updated_task = get_task_by_id(task_id)
        return {"id": updated_task[0], "title": updated_task[1], "description": updated_task[2], "status": updated_task[3], "created_at": updated_task[4]}
    raise HTTPException(status_code=404, detail="Task not found")

# 5. Delete Task
@app.delete("/tasks/{task_id}")
async def delete_task_endpoint(task_id: int):
    if delete_task(task_id):
        return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")