from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime



class TransactionCreateSchema(BaseModel):
    from_account_number: str
    to_account_number: str
    amount: Decimal

class TransactionReadSchema(BaseModel):
    from_account_number: str
    to_account_number: str
    amount: Decimal
    created_at: datetime