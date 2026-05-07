from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Numeric, func

from decimal import Decimal

from datetime import datetime

from app.core.database import Base



class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    from_account_number: Mapped[str] = mapped_column(ForeignKey("accounts.account_number"))
    to_account_number: Mapped[str] = mapped_column(ForeignKey("accounts.account_number"))
    amount:Mapped[Numeric] = mapped_column(Numeric(20, 2))   
    
    created_at:Mapped[datetime] = mapped_column(server_default=func.now())