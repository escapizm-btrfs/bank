from fastapi import APIRouter

from app.dependencies.Annotated import SessionDep, CurrentUserDep
from app.schemas.account_schema import AccountCreateSchema

from app.services.account_service import create_account, get_my_account, get_accounts_by_email




router = APIRouter()

@router.post("/accounts")
async def create_account_router(session:SessionDep, account: AccountCreateSchema,user:CurrentUserDep):
    return await create_account(session, account, user)

@router.get("/accounts")
async def get_account_router(session:SessionDep, user:CurrentUserDep):
    return await get_my_account(session, user)
    
@router.get("/accounts/{user_email}")
async def get_account_by_email_router(session:SessionDep, user_email:str):
    return await get_accounts_by_email(session, user_email)