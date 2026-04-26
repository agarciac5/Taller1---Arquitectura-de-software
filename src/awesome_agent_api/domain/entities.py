"""Entidades principales del dominio para productos y conversaciones de chat."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    """
    Entidad que representa un producto del e-commerce

    Contiene la informacion principal de un zapato y reglas basicas
    de negocio relacionadas con precio, stock y disponibilidad.
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
        """Valida los datos del producto al momento de crearlo"""
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
        """
        Reduce el stock del producto

        Args:
            quantity (int): cantidad que se quiere descontar

        Raises:
            ValueError: Si la cantidad no es valida o supera el stock actual.
        """
        if quantity <= 0:
            raise ValueError("La cantidad a reducir debe ser mayor a 0.")
        if quantity > self.stock:
            raise ValueError("No hay suficiente stock para reducir.")
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """Aumenta el stock del producto segun la cantidad enviada"""
        if quantity <= 0:
            raise ValueError("La cantidad a aumentar debe ser mayor a 0.")
        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje dentro del chat.

    Sirve para guardar quien envio el mensaje, el contenido
    y la sesion a la que pertenece
    """

    id: Optional[int]
    session_id: str
    role: str
    message: str
    timestamp: datetime

    def __post_init__(self) -> None:
        """Valida session_id, role y message"""
        if not self.session_id.strip():
            raise ValueError("El identificador de sesion no puede estar vacio.")
        if self.role not in ("user", "assistant"):
            raise ValueError("El rol debe ser 'user' o 'assistant'.")
        if not self.message.strip():
            raise ValueError("El mensaje no puede estar vacio.")

    def is_from_user(self) -> bool:
        """Retorna True si el mensaje viene del usuario"""
        return self.role == "user"

    def is_from_assistant(self) -> bool:
        """Retorna True si el mensaje viene del asistente."""
        return self.role == "assistant"


@dataclass
class ChatContext:
    """
    contexto conversacional de una sesion

    Mantiene los mensajes recientes para poder construir
    mejor el prompt antes de consultar la IA.
    """

    messages: list[ChatMessage]
    max_messages: int = 6

    def get_recent_messages(self) -> list[ChatMessage]:
        """Obtiene los ultimos mensajes segun el limite configurado"""
        return self.messages[-self.max_messages :]

    def format_for_prompt(self) -> str:
        """
        Convierte el historial reciente a texto legible para el prompt

        Returns:
            str: Texto armado con etiquetas de Usuario y Asistente
        """
        formatted_messages = []

        for message in self.get_recent_messages():
            speaker = "Usuario" if message.is_from_user() else "Asistente"
            formatted_messages.append(f"{speaker}: {message.message}")

        return "\n".join(formatted_messages)
