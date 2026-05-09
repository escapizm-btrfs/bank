from pydantic import BaseModel, EmailStr, ConfigDict
from decimal import Decimal



class AccountCreateSchema(BaseModel):
    balance: Decimal
    

class AccountPublicReadSchema(BaseModel):
    account_number : str
    email : str

class AccountMyReadSchema(BaseModel):
    balance: Decimal
    account_number: str