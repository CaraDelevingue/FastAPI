from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user
from app.core.database import SessionLocal

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