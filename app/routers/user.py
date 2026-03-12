from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserUpdate,UserLogin
from app.services.user_service import create_user,get_user_by_id,get_users,update_user,delete_user,authenticate_user
from app.core.database import SessionLocal
from app.core.jwt import create_access_token
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users",tags=["users"])

#依赖注入数据库 Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/",response_model=UserResponse)
def create_user_api(user_in: UserCreate, db:Session=Depends(get_db)):
    try:
        user = create_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

#创建受保护的接口
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}",response_model=UserResponse)
def get_user_api(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/",response_model=list[UserResponse])
def list_users_api(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    users = get_users(db,skip=skip,limit=limit)
    return users

@router.put("/{user_id}",response_model=UserResponse)
def update_user_api(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db)
):
    user = update_user(db, user_id, user_in)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.delete("/{user_id}")
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db,user_id)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message":"User deleted successfully"}

@router.post("/login")
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db)
    ):
    user = authenticate_user(db,user_in.username, user_in.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"user_id":user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


