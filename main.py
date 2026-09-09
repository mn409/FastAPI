from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory storage
todos = {}
next_id = 1


# Request model (NO id here)
class Todo(BaseModel):
    title: str
    completed: bool = False


# CREATE
@app.post("/todos")
def create_todo(todo: Todo):
    global next_id

    new_todo = {
        "id": next_id,
        "title": todo.title,
        "completed": todo.completed
    }

    todos[next_id] = new_todo
    next_id += 1

    return new_todo


# GET ALL
@app.get("/todos")
def get_todos():
    return list(todos.values())


# GET ONE
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todos[todo_id]


# UPDATE
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated: Todo):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")

    todos[todo_id]["title"] = updated.title
    todos[todo_id]["completed"] = updated.completed

    return todos[todo_id]


# DELETE
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")

    deleted = todos.pop(todo_id)

    return {"message": "Deleted successfully", "data": deleted}