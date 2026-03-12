from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#hash加密用户密码
def hash_password(password:str)->str:
    return pwd_context.hash(password)

#校验密码
def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)