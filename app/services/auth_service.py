from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from datetime import datetime, timedelta

from app.schemas.user_schema import UserCreateSchema
from app.models.user_model import UserModel
from app.dependencies.sessiondep import SessionDep
from app.core.security import hash_password, verify_password
from app.core.auth import create_access_token, get_current_user



router = APIRouter

@router.post("/registration")
async def registration(session:SessionDep, user: UserCreateSchema):
    new_user = UserModel(
        name = user.name,
        email = user.email,
        hashed_pswd = hash_password(user.password)
    )

    session.add(new_user)
    await session.commit()    
    return {"success":True}
    

@router.post("/login")
async def login(session:SessionDep, email:str, password:str):
    body_query = (select(UserModel).where(UserModel.email == email))
    query = await session.execute(body_query)
    user = query.scalar_one_or_none()
    if not verify_password(password, user.hashed_pswd):
        raise HTTPException(status_code=401, detail="not currectly passw or email")
    token = create_access_token({"sub":str(user.id), "exp":datetime.now() + timedelta(minutes=30)})
    return {"access_token": token}
