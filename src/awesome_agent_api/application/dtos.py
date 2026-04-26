"""DTOs de la capa de aplicacion para productos y chat."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class ProductDTO(BaseModel):
    """DTO para transportar datos de productos entre capas"""

    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    @validator("price")
    def price_must_be_positive(cls, value: float) -> float:
        """Valida que el precio sea mayor a cero."""
        if value <= 0:
            raise ValueError("El precio debe ser mayor a 0.")
        return value

    @validator("stock")
    def stock_must_be_non_negative(cls, value: int) -> int:
        """Valida que el stock no sea negativo"""
        if value < 0:
            raise ValueError("El stock no puede ser negativo.")
        return value

    class Config:
        from_attributes = True


class ChatMessageRequestDTO(BaseModel):
    """DTO para recibir mensajes enviados por el usuario."""

    session_id: str
    message: str

    @validator("message")
    def message_not_empty(cls, value: str) -> str:
        """Valida que el mensaje no este vacio"""
        if not value.strip():
            raise ValueError("El mensaje no puede estar vacio.")
        return value

    @validator("session_id")
    def session_id_not_empty(cls, value: str) -> str:
        """Valida que el identificador de sesion no este vacio."""
        if not value.strip():
            raise ValueError("El session_id no puede estar vacio.")
        return value


class ChatMessageResponseDTO(BaseModel):
    """DTO para devolver respuestas del asistente"""

    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    """DTO para retornar mensajes del historial conversacional."""

    id: int
    role: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True
