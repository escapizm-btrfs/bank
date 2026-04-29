from fastapi import APIRouter

from app.schemas.user_schema import UserCreateSchema
from app.schemas.user_schema import UserReadSchema

from app.models.user_model import UserModel
from app.models.account_model import AccountModel

 

from app.dependencies.Annotated import SessionDep



router = APIRouter()


    