from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
from slugify import slugify
from sqlalchemy import insert, select, update, delete

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    stmt = select(Task)  # выборка всех задач
    result = db.execute(stmt).scalars().all()  # Получаем список всех задач
    return result  # Возвращаем список задач


@router.get("/task_id")
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = select(Task).where(Task.id == task_id)  # выборка задачи по task_id
    result = db.execute(stmt).scalar_one_or_none()  # Получаем одну задачу

    if result is not None:
        return result  # Возвращаем задачу, если она найдена

    # Если задача не найдена, выбрасываем исключение
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача не найдена"
    )


@router.post("/create")
def create_task(task_data: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        # Если пользователь не найден, выбрасываем 404 ошибку
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(insert(Task).values(title=task_data.title, content=task_data.content,
                                   priority=task_data.priority, user_id=user_id, slug=slugify(task_data.title)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put("/update")
def update_task(task_id: int, task_data: UpdateTask, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    task.title = task_data.title
    task.content = task_data.content  # Исправлено на корректное поле
    task.priority = task_data.priority  # Обновляем приоритет
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Успешно'}


@router.delete("/delete")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    db.delete(task)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Задача успешно удалена'}