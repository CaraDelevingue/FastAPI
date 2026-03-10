from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

def create_user(db:Session,user_in:UserCreate)-> User:
    #检查用户名是否存在
    existing = db.query(User).filter(User.username == user_in.username).first()
    if existing:
        raise ValueError("Username aleady exists")
    
    #创建对象
    new_user = User(
        username = user_in.username,
        password = user_in.password
    )

    #入库
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user