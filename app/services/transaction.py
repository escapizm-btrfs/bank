from fastapi import HTTPException
from sqlalchemy import select

from app.dependencies.Annotated import SessionDep, CurrentUserDep
from app.schemas.transaction_schema import TransactionCreateSchema
from app.models.transaction_model import TransactionModel
from app.models.account_model import AccountModel



async def transaction(session:SessionDep, whoami_user:CurrentUserDep, transaction_schema:TransactionCreateSchema):
    async with session.begin():
        
        accounts_query = await session.execute(
            select(AccountModel)
            .where(AccountModel.id.in_([transaction_schema.from_account_id, transaction_schema.to_account_id]))
            .with_for_update()
        )

        accounts = accounts_query.scalars().all()

        from_acc = None
        to_acc = None
        for acc in accounts:
            if acc.id == transaction_schema.from_account_id:
                from_acc = acc
                 
            elif acc.id == transaction_schema.to_account_id:
                to_acc = acc
                

        # проверка если нет счета
        # проверка если сумма перевода меньше баланса
        # проверка того ли пользователя счет
        if len(accounts) != 2:
            raise HTTPException(status_code=404, detail="account not found")
        if from_acc.user_id != whoami_user:
            raise HTTPException(status_code=400, detail="same account")
        if from_acc.balance < transaction_schema.amount:
            raise HTTPException(status_code=400, detail="enough balance")
        
        from_acc.balance -= transaction_schema.amount
        to_acc.balance += transaction_schema.amount 

        new_transaction = TransactionModel(
            from_account_id = transaction_schema.from_account_id,
            to_account_id = transaction_schema.to_account_id,
            amount = transaction_schema.amount
        )

        session.add(new_transaction)
        await session.commit()

        return {"success": True}
