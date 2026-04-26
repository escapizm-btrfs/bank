from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import List

from app.core.database import Base




class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(255))
    
    hashed_pswd: Mapped[str]

    accounts: Mapped[List["AccountModel"]] = relationship(back_populates="account_owner")

