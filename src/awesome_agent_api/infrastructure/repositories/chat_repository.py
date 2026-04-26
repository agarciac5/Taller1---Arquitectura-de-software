"""Repositorio SQLAlchemy para persistencia del historial de chat."""

from sqlalchemy.orm import Session

from awesome_agent_api.domain.entities import ChatMessage
from awesome_agent_api.domain.repositories import IChatRepository
from awesome_agent_api.infrastructure.db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    """Implementacion concreta del repositorio de chat usando SQLAlchemy."""

    def __init__(self, db: Session) -> None:
        """Inicializa el repositorio con una sesion de base de datos"""
        self.db = db

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Guarda un mensaje y retorna la entidad persistida."""
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(
        self, session_id: str, limit: int | None = None
    ) -> list[ChatMessage]:
        """Obtiene el historial de una sesion en orden cronologico"""
        if limit is not None:
            models = (
                self.db.query(ChatMemoryModel)
                .filter(ChatMemoryModel.session_id == session_id)
                .order_by(ChatMemoryModel.timestamp.desc())
                .limit(limit)
                .all()
            )
            models.reverse()
        else:
            models = (
                self.db.query(ChatMemoryModel)
                .filter(ChatMemoryModel.session_id == session_id)
                .order_by(ChatMemoryModel.timestamp.asc())
                .all()
            )

        return [self._model_to_entity(model) for model in models]

    def delete_session_history(self, session_id: str) -> int:
        """Elimina todo el historial de una sesion y retorna la cantidad borrada."""
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .all()
        )
        deleted_count = len(models)

        for model in models:
            self.db.delete(model)

        self.db.commit()
        return deleted_count

    def get_recent_messages(self, session_id: str, count: int) -> list[ChatMessage]:
        """Obtiene los ultimos mensajes de una sesion"""
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(count)
            .all()
        )
        models.reverse()
        return [self._model_to_entity(model) for model in models]

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """Convierte un modelo ORM en una entidad de dominio."""
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp,
        )

    def _entity_to_model(self, entity: ChatMessage) -> ChatMemoryModel:
        """Convierte una entidad de dominio en un modelo ORM"""
        return ChatMemoryModel(
            id=entity.id,
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp,
        )
