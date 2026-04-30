from pydantic import BaseModel
from decimal import Decimal



class TransactionCreateSchema(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: Decimal

