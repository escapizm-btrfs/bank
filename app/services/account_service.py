from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.dependencies.Annotated import SessionDep, CurrentUserDep
from app.models.account_model import AccountModel
from app.schemas.account_schema import AccountCreateSchema







async def create_account(session:SessionDep, account:AccountCreateSchema, user:CurrentUserDep):
    new_account = AccountModel(
        user_id = user,
        balance = account.balance
    )
    session.add(new_account)
    await session.commit()
    return {"message": "account_created"}


async def get_account(session:SessionDep, user:CurrentUserDep):
    body_query = select(AccountModel).where(AccountModel.user_id == user)
    query = await session.execute(body_query)
    result = query.scalars().all()
    return result