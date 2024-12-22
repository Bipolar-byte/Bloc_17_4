from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from app.models.task import Task
from app.schemas import CreateTask, UpdateTask

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Session = Depends(get_db)):
    return db.query(...).all()


@router.get('/{task_id}')
async def task_by_id(task_id: int, db: Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post('/create')
async def create_task(task: CreateTask, db: Depends(get_db)):
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    return {'status_code': 201, 'transaction': 'Task created successfully'}


@router.put('/update/{task_id}')
async def update_task(task_id: int, task: UpdateTask, db: Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    return {'status_code': 200, 'transaction': 'Task updated successfully'}


@router.delete('/delete/{task_id}')
async def delete_task(task_id: int, db: Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {'status_code': 200, 'transaction': 'Task deleted successfully'}
