from datetime import datetime

from awesome_agent_api.application.dtos import (
    ChatHistoryDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
)
from awesome_agent_api.domain.entities import ChatContext, ChatMessage
from awesome_agent_api.domain.exceptions import ChatServiceError
from awesome_agent_api.domain.repositories import IChatRepository, IProductRepository


class ChatService:
    """
    Servicio de aplicación para gestionar conversaciones con IA.

    Orquesta productos, historial conversacional y el servicio externo de IA
    para generar respuestas coherentes para el usuario.
    """

    def __init__(
        self,
        product_repository: IProductRepository,
        chat_repository: IChatRepository,
        ai_service,
    ) -> None:
        """Inicializa el servicio con sus dependencias principales."""
        self.product_repository = product_repository
        self.chat_repository = chat_repository
        self.ai_service = ai_service

    async def process_message(
        self, request: ChatMessageRequestDTO
    ) -> ChatMessageResponseDTO:
        """Procesa un mensaje del usuario y retorna la respuesta del asistente."""
        try:
            products = self.product_repository.get_all()
            recent_messages = self.chat_repository.get_recent_messages(
                request.session_id, count=6
            )
            context = ChatContext(messages=recent_messages)

            assistant_message = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=context,
            )

            timestamp = datetime.utcnow()
            user_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="user",
                message=request.message,
                timestamp=timestamp,
            )
            assistant_response = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="assistant",
                message=assistant_message,
                timestamp=timestamp,
            )

            self.chat_repository.save_message(user_message)
            self.chat_repository.save_message(assistant_response)

            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=assistant_message,
                timestamp=timestamp,
            )
        except ChatServiceError:
            raise
        except Exception as error:
            raise ChatServiceError(f"Error procesando el mensaje del chat: {error}") from error

    def get_session_history(
        self, session_id: str, limit: int = 10
    ) -> list[ChatHistoryDTO]:
        """Obtiene el historial de una sesión y lo transforma a DTOs."""
        messages = self.chat_repository.get_session_history(session_id, limit=limit)
        return [
            ChatHistoryDTO(
                id=message.id or 0,
                role=message.role,
                message=message.message,
                timestamp=message.timestamp,
            )
            for message in messages
        ]

    def clear_session_history(self, session_id: str) -> int:
        """Elimina el historial de una sesión y retorna la cantidad eliminada."""
        return self.chat_repository.delete_session_history(session_id)
