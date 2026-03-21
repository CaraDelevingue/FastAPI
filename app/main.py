from fastapi import FastAPI
from app.routers import user
from app.core.database import Base, engine
from app.models import user, task

app = FastAPI(title="Backend Service")

#创建所有表
Base.metadata.create_all(bind=engine)

#注册路由
app.include_router(user.router)

@app.get("ping")
def ping():
    return {"message":"pong"}