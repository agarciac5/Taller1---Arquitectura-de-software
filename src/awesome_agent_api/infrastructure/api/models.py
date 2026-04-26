from datetime import datetime

from pydantic import BaseModel, Field


class ProductDTO(BaseModel):
    id: int
    name: str
    brand: str
    category: str
    size: int
    color: str
    price: float
    stock: int


class ChatMessageRequestDTO(BaseModel):
    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class ChatMessageResponseDTO(BaseModel):
    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    session_id: str
    role: str
    message: str
    timestamp: datetime
