from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate,TaskUpdate
from app.models.user import User
from fastapi import HTTPException

#创建任务
def create_task(db: Session, task_in: TaskCreate, current_user: User):
    task = Task(
        title = task_in.title,
        description = task_in.description,
        owner_id = current_user.id #绑定任务归属用户
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

#根据ID获取任务
def get_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404,detail="Task not found")
    return task

#更新任务
def update_task(db: Session, task: Task, task_in: TaskUpdate):
    for field,value in task_in.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

#删除任务
def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
    return {"detail":"Task deleted"}

#获取用户任务列表
def list_tasks(db: Session, current_user: User, admin_view: bool = False):
    if admin_view and current_user.role == "admin":
        return db.query(Task).all() #Admin 查看所有任务
    return db.query(Task).filter(Task.owner_id == current_user.id).all()