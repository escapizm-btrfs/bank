from pydantic import BaseModel, EmailStr, ConfigDict
from decimal import Decimal



class AccountCreateSchema(BaseModel):
    balance: Decimal
    

class AccountPublicReadSchema(BaseModel):
    email : str
    account_number : str

    model_config = ConfigDict(from_attributes=True)

class AccountMyReadSchema(BaseModel):
    balance: Decimal
    account_number: str

    model_config = ConfigDict(from_attributes=True)