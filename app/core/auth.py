from datetime import datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt



SECRET_KEY = "4321NJKLDNFLS8312mkFDSAfFDqnjk012"
ALGORITHM = "HS256"
ACCES_TOKEN_EXP = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login") # Утилита для автоматического поиска JWT внутри заголовка

def create_access_token(payload:dict):
    encoded_jwt = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def get_current_user(token : str = Depends(oauth2_scheme)): # В парамиетр передается токен из ручки и функция возвращает id пользователя из cookie
    try: # отлов ошибки
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None: # Проверка на существ. токен
            raise HTTPException(status_code=401, detail="NonAuthorized")
    except JWTError:
        raise HTTPException(status_code=401, detail="NonAuthorized")
    return int(sub)
    

# email ami@gmail.com name escapism psswd 321321