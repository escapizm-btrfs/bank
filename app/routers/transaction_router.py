from fastapi import APIRouter


from app.dependencies.Annotated import SessionDep, CurrentUserDep
from app.schemas.transaction_schema import TransactionCreateSchema
from app.services.transaction import transaction, get_transactions_list



router = APIRouter()

@router.post("/transactions")
async def transaction_router(session:SessionDep, whoami_user:CurrentUserDep, transaction_schema:TransactionCreateSchema):
    return await transaction(session, whoami_user, transaction_schema)

@router.get("/transactions")
async def get_transactions_list_router(session:SessionDep, user:CurrentUserDep):
    return await get_transactions_list(session, user)