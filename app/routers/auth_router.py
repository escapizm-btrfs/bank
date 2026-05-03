from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.Annotated import SessionDep
from app.services.auth_service import registration, login
from app.schemas.user_schema import UserCreateSchema



#router = APIRouter()

#@router.post("/auth/registration")
#async def registration_router(session:SessionDep, user:UserCreateSchema):
#    return await registration(session, user)

#@router.post("/auth/login")
#async def login_router(session:SessionDep, form:OAuth2PasswordRequestForm):
#    return await login(session, form)