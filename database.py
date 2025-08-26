import sqlite3
from contextlib import contextmanager

# Database connection context manager
@contextmanager
def get_db():
    conn = sqlite3.connect('tasks.db')
    try:
        yield conn
    finally:
        conn.close()

# Initialize the database (create table if not exists)
def init_db():
    with get_db() as conn:
        conn.executescript(open('schema.sql', 'r').read())

# CRUD Operations
def create_task(title, description=None):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (title, description)
        )
        conn.commit()
        return cursor.lastrowid

def get_tasks():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        return cursor.fetchall()

def get_task_by_id(task_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return cursor.fetchone()

def update_task_status(task_id, status):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = ? WHERE id = ? AND status IN ('pending', 'completed')",
            (status, task_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def delete_task(task_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0