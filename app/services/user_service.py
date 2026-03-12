from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate,UserUpdate
from app.core.security import hash_password,verify_password

#用户创建
def create_user(db:Session,user_in:UserCreate)-> User:
    #检查用户名是否存在
    existing = db.query(User).filter(User.username == user_in.username).first()
    if existing:
        raise ValueError("Username aleady exists")
    
    #创建对象并加密密码
    new_user = User(
        username = user_in.username,
        password = hash_password(user_in.password)
    )

    #入库
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#查询单个用户
def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

#通过页查询用户
def get_users(db: Session, skip:int = 0, limit:int = 10):
    return db.query(User).offset(skip).limit(limit).all()

#用户数据更新
def update_user(db:Session, user_id: int, user_in: UserUpdate) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None
    
    #更新usrname
    if user_in.username is not None:
        user.username = user_in.username

    #更新密码
    if user_in.password is not None:
        user.password = hash_password(user_in.password)

    db.commit()
    db.refresh(user)

    return user

def delete_user(db:Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    
    db.delete(user)
    db.commit()

    return True

def authenticate_user(db:Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return None
    
    if not verify_password(password,user.password):
        return None
    
    return user