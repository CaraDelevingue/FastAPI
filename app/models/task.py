import enum
from enum import Enum 
from app.core.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_process = "in_process"
    done = "done"

class Task(Base):
        __tablename__  = "tasks"

        id = Column(Integer, primary_key=True, index=True)
        title = Column(String(255),nullable=False)
        description = Column(String(1024),nullable=True)
        owner_id = Column(Integer, ForeignKey("users.id"),nullable=False)
        status = Column(Enum(TaskStatus),default=TaskStatus.todo)

        owner = relationship("User",backref="tasks")