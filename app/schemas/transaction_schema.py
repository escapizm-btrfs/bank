from pydantic import BaseModel
from decimal import Decimal



class TransactionCreateSchema(BaseModel):
    from_account_number: str
    to_account_number: str
    amount: Decimal

