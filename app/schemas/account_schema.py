from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy import Numeric



class AccountCreateSchema(BaseModel):
    balance: float

