from fastapi import FastAPI
from sqlalchemy import text

from app.dependencies.sessiondep import SessionDep



app = FastAPI()

@app.get("/")
async def test_conn(session:SessionDep):
    result = await session.execute(text("SELECT version()"))
    return result.scalars().all()