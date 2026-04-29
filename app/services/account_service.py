from fastapi import APIRouter, Depends


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
