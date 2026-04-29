from fastapi import APIRouter

from app.dependencies.Annotated import SessionDep, CurrentUserDep
from app.schemas.account_schema import AccountCreateSchema

from app.services.account_service import create_account, get_account




router = APIRouter()

@router.post("/account")
async def create_account_router(session:SessionDep, account: AccountCreateSchema,user:CurrentUserDep):
    return await create_account(session, account, user)

@router.get("/account")
async def get_account_router(session:SessionDep, user:CurrentUserDep):
    return await get_account(session, user)
    