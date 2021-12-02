from typing import Optional
from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title='To Do List',
    version='0.1 beta'
)

today = datetime.today()

@app.get("/tasks/")
async def task(task_id: str, date: Optional[datetime] = None):
    
    if isinstance(date, datetime):
        return {
            "task_id": task_id,
            "date": date
        }
    else:        
        return {
            "task_id": task_id,
            "date": today
        }