from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy import ForeignKey, Enum, DECIMAL
from app.enums import Status
from datetime import datetime
from decimal import Decimal

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] =  mapped_column(primary_key = True)
    username: Mapped[str] = mapped_column(nullable=False, unique= True)
    email: Mapped[str] = mapped_column(nullable=False, unique= True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)

class Monitor(Base):
    __tablename__ = "monitors"

    monitor_id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    threshold: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    product_link: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)
