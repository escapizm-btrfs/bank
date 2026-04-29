from fastapi import FastAPI
from sqlalchemy import text

from app.routers.routes import main_router
from app.dependencies.Annotated import SessionDep



app = FastAPI()

app.include_router(main_router)


@app.get("/")
async def test_conn(session:SessionDep):
    result = await session.execute(text("SELECT version()"))
    return result.scalars().all()
