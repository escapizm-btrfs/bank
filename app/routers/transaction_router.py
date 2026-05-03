from fastapi import APIRouter


from app.dependencies.Annotated import SessionDep, CurrentUserDep
from app.schemas.transaction_schema import TransactionCreateSchema
from app.services.transaction import transaction



router = APIRouter()

@router.post("/transactions")
async def transaction_router(session:SessionDep, whoami_user:CurrentUserDep, transaction_schema:TransactionCreateSchema):
    return await transaction(session, whoami_user, transaction_schema)