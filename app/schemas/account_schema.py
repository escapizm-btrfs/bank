from pydantic import BaseModel, EmailStr, ConfigDict
from decimal import Decimal



class AccountCreateSchema(BaseModel):
    balance: Decimal
    

