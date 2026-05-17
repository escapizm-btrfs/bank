from app.dependencies.Annotated import SessionDep
from sqlalchemy import select,delete
import asyncio

from app.models.account_model import AccountModel
from app.models.user_model import UserModel
from app.core.database import AsyncSessionLocal

async def delete_all_tables():
    async with AsyncSessionLocal() as session:
        #Выбирает пользователя с именем test_reg и достает его id 
        user_id_reg_query = await session.execute(
            select(UserModel.id).where(UserModel.name == "test_reg")
        )
        user_id_reg = user_id_reg_query.scalar_one_or_none()
        #Удаляет аккаунты с user_id == user_id_reg
        await session.execute(
            delete(AccountModel).where(AccountModel.user_id == user_id_reg)
        )
        #Выбирает пользователя с именем test_login и достает его id 
        user_id_login_query = await session.execute(
            select(UserModel.id).where(UserModel.name == "test_login")
        )
        user_id_login = user_id_login_query.scalar_one_or_none()

        #Удаляет аккаунты c user_id == user_id_log
        await session.execute(
            delete(AccountModel).where(AccountModel.user_id == user_id_login)
        )






        '''await session.execute(
            delete(AccountModel).where(AccountModel)
        )'''

        #Удаление пользователей с name test_reg
        await session.execute(
            delete(UserModel).where(UserModel.name == "test_reg")
        )

        
        #удалени пользовтеля с name test_login
        await session.execute(
            delete(UserModel).where(UserModel.name == "test_login")
        )
        await session.execute(
            delete(UserModel)
        )

        print("ddd")

        await session.commit()

asyncio.run(delete_all_tables())