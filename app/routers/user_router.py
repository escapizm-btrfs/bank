from fastapi import APIRouter

from app.schemas.user_schema import UserCreateSchema
from app.schemas.user_schema import UserReadSchema

from app.models.user_model import UserModel
from app.models.account_model import AccountModel

from app.services.user_service import create_user, get_user

from app.dependencies.sessiondep import SessionDep



router = APIRouter()

@router.post("/users")
async def create_user_router(session: SessionDep, user:UserCreateSchema):
    result = await create_user(session, user)
    return result

@router.get("/users/{email}", response_model=UserReadSchema)
async def get_user_router(session:SessionDep, email:str):
    result = await get_user(session, email)
    return result
    