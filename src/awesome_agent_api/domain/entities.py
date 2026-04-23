from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    """
    Entidad que representa un producto en el e-commerce.

    Contiene los datos principales de un zapato y las reglas de negocio
    relacionadas con precio, stock y disponibilidad.
    """

    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self) -> None:
        """Valida los datos del producto despues de crear la instancia."""
        if not self.name.strip():
            raise ValueError("El nombre del producto no puede estar vacio.")
        if self.price <= 0:
            raise ValueError("El precio del producto debe ser mayor a 0.")
        if self.stock < 0:
            raise ValueError("El stock del producto no puede ser negativo.")

    def is_available(self) -> bool:
        """Retorna True si el producto tiene stock disponible."""
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """Reduce el stock del producto si la cantidad solicitada es valida."""
        if quantity <= 0:
            raise ValueError("La cantidad a reducir debe ser mayor a 0.")
        if quantity > self.stock:
            raise ValueError("No hay suficiente stock para reducir.")
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """Aumenta el stock del producto si la cantidad es valida."""
        if quantity <= 0:
            raise ValueError("La cantidad a aumentar debe ser mayor a 0.")
        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en una conversacion de chat.

    Permite diferenciar si el mensaje fue enviado por el usuario o por el
    asistente de IA.
    """

    id: Optional[int]
    session_id: str
    role: str
    message: str
    timestamp: datetime

    def __post_init__(self) -> None:
        """Valida los datos del mensaje despues de crear la instancia."""
        if not self.session_id.strip():
            raise ValueError("El identificador de sesion no puede estar vacio.")
        if self.role not in ("user", "assistant"):
            raise ValueError("El rol debe ser 'user' o 'assistant'.")
        if not self.message.strip():
            raise ValueError("El mensaje no puede estar vacio.")

    def is_from_user(self) -> bool:
        """Retorna True si el mensaje fue enviado por el usuario."""
        return self.role == "user"

    def is_from_assistant(self) -> bool:
        """Retorna True si el mensaje fue enviado por el asistente."""
        return self.role == "assistant"


@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversacion.

    Mantiene los mensajes recientes para que el asistente pueda responder con
    coherencia segun el historial.
    """

    messages: list[ChatMessage]
    max_messages: int = 6

    def get_recent_messages(self) -> list[ChatMessage]:
        """Retorna los ultimos mensajes segun el limite configurado."""
        return self.messages[-self.max_messages :]

    def format_for_prompt(self) -> str:
        """Formatea el historial reciente para incluirlo en un prompt de IA."""
        formatted_messages = []

        for message in self.get_recent_messages():
            speaker = "Usuario" if message.is_from_user() else "Asistente"
            formatted_messages.append(f"{speaker}: {message.message}")

        return "\n".join(formatted_messages)
