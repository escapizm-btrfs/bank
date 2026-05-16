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
            .where(AccountModel.account_number.in_([transaction_schema.from_account_number, transaction_schema.to_account_number]))
            .with_for_update()
        )

        accounts = accounts_query.scalars().all()

        from_acc = None
        to_acc = None
        for acc in accounts:
            if acc.account_number == transaction_schema.from_account_number:
                from_acc = acc
                 
            elif acc.account_number == transaction_schema.to_account_number:
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
            from_account_number = transaction_schema.from_account_number,
            to_account_number = transaction_schema.to_account_number,
            amount = transaction_schema.amount
        )

        session.add(new_transaction)

        return (
            {"success": True},
            new_transaction
        )


async def get_transactions_list(session:SessionDep, user:CurrentUserDep):
    accounts_query = await session.execute(
        select(AccountModel.account_number)
        .where(AccountModel.user_id == user)
    )
    acc = accounts_query.scalars().all()

    body_query = (
        select(TransactionModel)
        .where(
            (TransactionModel.from_account_number.in_(acc)) 
            |
            (TransactionModel.to_account_number.in_(acc))
        )
        .order_by(TransactionModel.created_at.desc()) 
        .limit(10)
#        select(TransactionModel).where(TransactionModel.from_account_number == user)
    )

    query = await session.execute(body_query)
    result = query.scalars().all()
    return result

async def get_received_or_sent_transactions(session:SessionDep, user:CurrentUserDep, transaction_type:str):
    get_account = await session.execute(
        select(AccountModel.account_number)
        .where(AccountModel.user_id == user)
        .order_by(TransactionModel.created_at.desc())
        .limit(10)
    )
    acc = get_account.scalars().all()
    
    if transaction_type == "received":
        #print("received")
        query = await session.execute(
            select(TransactionModel)
            .where(TransactionModel.from_account_number.in_(acc))
            .order_by(TransactionModel.created_at.desc())
            .limit(10)
        )
        
    if transaction_type == "sent":
        #print("sent")
        query = await session.execute(
            select(TransactionModel)
            .where(TransactionModel.to_account_number.in_(acc))
            .order_by(TransactionModel.created_at.desc())
            .limit(10)
        )
    else:
        #print("other")
        query = await session.execute(select(TransactionModel)
                .where(
                    TransactionModel.from_account_number.in_(acc)
                |
                    TransactionModel.to_account_number.in_(acc)
                )
                .order_by(TransactionModel.created_at.desc())
                .limit(10)
                )
    result = query.scalars().all()
    return result
                
