from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DECIMAL, Numeric

from app.core.database import Base



class AccountModel(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    balance: Mapped[float] = mapped_column(Numeric(20, 2), default=0.00)

    account_owner: Mapped["UserModel"] = relationship(back_populates="accounts")
    