from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DECIMAL, Numeric, func

from datetime import datetime

from app.core.database import Base



class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    from_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    to_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    amount:Mapped[float] = mapped_column(Numeric(20, 2))   
    
    created_at:Mapped[datetime] = mapped_column(server_default=func.now())