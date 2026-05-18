from app.dependencies.Annotated import SessionDep
from sqlalchemy import select,delete
import asyncio

from app.models.account_model import AccountModel
from app.models.user_model import UserModel
from app.core.database import AsyncSessionLocal
from app.models.transaction_model import TransactionModel

async def delete_all_tables():
    async with AsyncSessionLocal() as session:
        # Сначала находим все ID тестовых пользователей, чтобы узнать, какие транзакции удалять
        user_ids_query = await session.execute(
            select(UserModel.id).where(UserModel.name.in_(["test_reg", "test_login"]))
        )
        all_user_ids = user_ids_query.scalars().all()

        if all_user_ids:
            # Находим номера аккаунтов этих пользователей
            acc_query = await session.execute(
                select(AccountModel.account_number).where(AccountModel.user_id.in_(all_user_ids))
            )
            all_account_numbers = acc_query.scalars().all()

            # Очищаем связанные транзакции, чтобы избежать ForeignKeyViolationError
            if all_account_numbers:
                await session.execute(
                    delete(TransactionModel).where(
                        TransactionModel.from_account_number.in_(all_account_numbers)
                    )
                )

        all_transactions = await session.execute(
            select(TransactionModel)
        )

        #все пользователи с name == test_reg
        user_id_reg_query = await session.execute(
            select(UserModel.id).where(UserModel.name == "test_reg")
        )
        user_ids_reg = user_id_reg_query.scalars().all() 

        #удалятся аккаунты
        if user_ids_reg:  #если список пуст
            await session.execute(
                delete(AccountModel).where(AccountModel.user_id.in_(user_ids_reg))
            )

        # --- ОБРАБОТКА TEST_LOGIN ---
        #id пользователей с name == test_login
        user_id_login_query = await session.execute(
            select(UserModel.id).where(UserModel.name == "test_login")
        )
        user_ids_login = user_id_login_query.scalars().all()

        #удаляется аккаунты через .in_
        if user_ids_login:
            await session.execute(
                delete(AccountModel).where(AccountModel.user_id.in_(user_ids_login))
            )

    
        #удаление пользователей с name test_reg
        await session.execute(
            delete(UserModel).where(UserModel.name == "test_reg")
        )
        
        #удаление пользователя с name test_login
        await session.execute(
            delete(UserModel).where(UserModel.name == "test_login")
        )


        await session.commit()
        print("ddd")

asyncio.run(delete_all_tables())