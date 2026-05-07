from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DECIMAL, Numeric

import uuid
from decimal import Decimal

from app.core.database import Base



class AccountModel(Base):
    __tablename__ = "accounts"

    #id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    balance: Mapped[Numeric] = mapped_column(Numeric(20, 2), default=0.00)
    account_number: Mapped[str] = mapped_column(unique=True, nullable=True)

    account_owner: Mapped["UserModel"] = relationship(back_populates="accounts")
    