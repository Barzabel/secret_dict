from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

from app.database import Base


class Secrets(Base):
    __tablename__ = "secrets"

    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str]
    body: Mapped[str]
    url: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
