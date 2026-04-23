from abc import ABC, abstractmethod
from typing import Optional

from awesome_agent_api.domain.entities import ChatMessage, Product


class IProductRepository(ABC):
    """
    Interface que define el contrato para acceder a productos.

    Las implementaciones concretas deben vivir en la capa de infraestructura.
    """

    @abstractmethod
    def get_all(self) -> list[Product]:
        """Obtiene todos los productos registrados."""
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto por ID o retorna None si no existe."""
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> list[Product]:
        """Obtiene productos de una marca especifica."""
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> list[Product]:
        """Obtiene productos de una categoria especifica."""
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """Guarda o actualiza un producto y retorna el producto persistido."""
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """Elimina un producto por ID y retorna True si fue eliminado."""
        pass


class IChatRepository(ABC):
    """
    Interface que define el contrato para gestionar el historial de chat.

    Permite guardar, consultar y eliminar mensajes sin depender de una base de
    datos concreta.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Guarda un mensaje en el historial y retorna el mensaje persistido."""
        pass

    @abstractmethod
    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> list[ChatMessage]:
        """Obtiene el historial de una sesion en orden cronologico."""
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """Elimina el historial de una sesion y retorna la cantidad eliminada."""
        pass

    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> list[ChatMessage]:
        """Obtiene los ultimos mensajes de una sesion en orden cronologico."""
        pass
