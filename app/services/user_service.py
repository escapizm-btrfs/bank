from sqlalchemy import select


from app.models.user_model import UserModel
from app.models.account_model import AccountModel

from app.schemas.user_schema import UserCreateSchema
from app.schemas.user_schema import UserReadSchema

from app.core.security import hash_password

from app.dependencies.sessiondep import SessionDep



async def create_user(session:SessionDep, user:UserCreateSchema):
    new_user = UserModel (
        email = user.email,
        name = user.name,
        hashed_pswd = hash_password(user.password)
        )
    
    session.add(new_user)
    await session.commit()
    return {"message" : "user_created"}

async def get_user(session: SessionDep, email: str):
    body_query = select(UserModel).where(UserModel.email == email)
    query = await session.execute(body_query)

    result = query.scalar_one_or_none()
    return result




    
    
    
