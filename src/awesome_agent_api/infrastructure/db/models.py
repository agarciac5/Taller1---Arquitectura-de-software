from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from awesome_agent_api.infrastructure.db.database import Base


class ProductModel(Base):
    """Modelo ORM para la tabla de productos."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    brand: Mapped[str] = mapped_column(String(100), index=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    size: Mapped[str] = mapped_column(String(20))
    color: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)


class ChatMemoryModel(Base):
    """Modelo ORM para la tabla de memoria conversacional."""

    __tablename__ = "chat_memory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100), index=True)
    role: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
