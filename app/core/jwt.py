from datetime import datetime, timedelta
from jose import JWTError,jwt

SECRET_KEY = "superscretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_code = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_code.update({"exp":expire})
    return jwt.encode(to_code, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        return payload
    except JWTError:
        return None
