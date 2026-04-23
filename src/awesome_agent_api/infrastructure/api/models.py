from datetime import datetime

from pydantic import BaseModel, Field


class ProductDTO(BaseModel):
    """Representa la información pública de un producto de la tienda."""

    id: int
    name: str
    brand: str
    category: str
    size: int
    color: str
    price: float
    stock: int


class ChatMessageRequestDTO(BaseModel):
    """Representa el mensaje enviado por un usuario al chat."""

    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class ChatMessageResponseDTO(BaseModel):
    """Representa la respuesta generada por el asistente de chat."""

    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    """Representa un mensaje almacenado en el historial de chat."""

    session_id: str
    role: str
    message: str
    timestamp: datetime
