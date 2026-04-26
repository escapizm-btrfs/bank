from sqlalchemy import select


from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreateSchema
from app.schemas.user_schema import UserReadSchema
from app.dependencies.sessiondep import SessionDep



async def create_user(session:SessionDep, user:UserCreateSchema):
    new_user = UserModel (
        email = user.email,
        name = user.name,
        password = user.password
        )
    session.add(new_user)
    await session.commit()
    return {"message" : "user_created"}

async def get_user(session: SessionDep, email: str):
    body_query = select(UserModel).where(UserModel.email == email)
    query = await session.execute(body_query)

    result = query.scalar_one_or_none()
    return result


async def get_user(session: SessionDep, id:int):
    body_query = select(UserModel).where(UserModel.id == id)
    query = await session.execute(query)

    result = query.scalar_one_or_none()
    return result

    
    
    
