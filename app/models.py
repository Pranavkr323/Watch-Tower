from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy import ForeignKey, Enum, DECIMAL
from app.enums import Status, Role
from datetime import datetime, timezone
from decimal import Decimal

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] =  mapped_column(primary_key = True)
    username: Mapped[str] = mapped_column(nullable=False, unique= True)
    email: Mapped[str] = mapped_column(nullable=False, unique= True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default= lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default= lambda: datetime.now(timezone.utc),
                                                 onupdate= lambda: datetime.now(timezone.utc))
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False, default=Role.USER)

class Monitor(Base):
    __tablename__ = "monitors"

    monitor_id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    threshold: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    product_link: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default= lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default= lambda: datetime.now(timezone.utc),
                                                 onupdate= lambda: datetime.now(timezone.utc))
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False, default= Status.ACTIVE)
