from fastapi import APIRouter

from app.dependencies.Annotated import SessionDep, CurrentUserDep
from app.services.account_service import create_account
from app.schemas.account_schema import AccountCreateSchema



router = APIRouter()

@router.post("/account")
async def create_account_router(session:SessionDep, account: AccountCreateSchema,user:CurrentUserDep):
    return await create_account(session, account, user)
    