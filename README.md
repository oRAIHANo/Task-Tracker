Task Tracker API
A REST API to manage tasks using FastAPI and SQLite.
Setup

Install Dependencies:
pip install -r requirements.txt


Initialize Database:

Run schema.sql using SQLite (e.g., sqlite3 tasks.db < schema.sql).


Run the App:
uvicorn main:app --reload


Test Endpoints:

Access Swagger UI at http://127.0.0.1:8000/docs to test all endpoints.



Endpoints

POST /tasks/: Create a task
GET /tasks/: List all tasks
GET /tasks/{id}: Get task by ID
PUT /tasks/{id}/status: Update task status
DELETE /tasks/{id}: Delete task
