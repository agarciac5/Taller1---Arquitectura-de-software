"""Interfaces del dominio para productos e historial de chat."""

from abc import ABC, abstractmethod
from typing import Optional

from awesome_agent_api.domain.entities import ChatMessage, Product


class IProductRepository(ABC):
    """Contrato abstracto para operaciones de persistencia de productos"""

    @abstractmethod
    def get_all(self) -> list[Product]:
        """Obtiene todos los productos registrados."""
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Busca un producto por id y retorna None si no existe"""
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> list[Product]:
        """Obtiene productos filtrados por marca"""
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> list[Product]:
        """Obtiene productos filtrados por categoria."""
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """Guarda o actualiza un producto y retorna la entidad persistida"""
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """Elimina un producto por id"""
        pass


class IChatRepository(ABC):
    """Contrato abstracto para persistir el historial conversacional."""

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Guarda un mensaje en el historial"""
        pass

    @abstractmethod
    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> list[ChatMessage]:
        """Obtiene el historial de una sesion en orden cronologico"""
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """Elimina todos los mensajes de una sesion."""
        pass

    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> list[ChatMessage]:
        """Obtiene los ultimos mensajes de una sesion"""
        pass
