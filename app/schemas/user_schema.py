from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreateSchema(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserReadSchema(BaseModel):
    email: str
    name: str

    model_config = ConfigDict(from_attributes=True)
