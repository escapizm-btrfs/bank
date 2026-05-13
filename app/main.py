from fastapi import FastAPI
from sqlalchemy import text

from app.routers.main_router import main_router
from app.dependencies.Annotated import SessionDep



app = FastAPI()

app.include_router(main_router)


@app.get("/")
async def test_conn(session:SessionDep):
    result = await session.execute(text("SELECT version()"))
    return result.scalars().all()


'''
DB_HOST = localhost
DB_PORT = 5432
DB_NAME = main_db
DB_USER = escapizm
DB_PASSWORD = 321321

SECRET_KEY = 4321NJKLDNFLS8312mkFDSAfFDqnjk012
ACCESS_TOKEN = 30
ALGORITHM = HS256
'''