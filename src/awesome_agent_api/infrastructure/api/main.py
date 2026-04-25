from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from awesome_agent_api.application.chat_service import ChatService
from awesome_agent_api.application.dtos import (
    ChatHistoryDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ProductDTO,
)
from awesome_agent_api.application.product_service import ProductService
from awesome_agent_api.domain.exceptions import ChatServiceError, ProductNotFoundError
from awesome_agent_api.infrastructure.db.database import get_db, init_db
from awesome_agent_api.infrastructure.llm_providers.gemini_service import GeminiService
from awesome_agent_api.infrastructure.repositories.chat_repository import SQLChatRepository
from awesome_agent_api.infrastructure.repositories.product_repository import (
    SQLProductRepository,
)

app = FastAPI(
    title="E-commerce con Chat IA",
    description="API REST de e-commerce de zapatos con chat inteligente.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Inicializa la base de datos al arrancar la aplicación."""
    init_db()


@app.get("/")
def read_root() -> dict[str, object]:
    """Retorna información básica de la API y sus endpoints principales."""
    return {
        "name": "E-commerce con Chat IA",
        "version": "0.1.0",
        "description": "API REST para productos y chat inteligente de zapatos.",
        "endpoints": [
            "/",
            "/products",
            "/products/{product_id}",
            "/chat",
            "/chat/history/{session_id}",
            "/health",
        ],
    }


@app.get("/products", response_model=list[ProductDTO])
def list_products(db: Session = Depends(get_db)) -> list[ProductDTO]:
    """Lista todos los productos disponibles en la base de datos."""
    product_repository = SQLProductRepository(db)
    product_service = ProductService(product_repository)
    return product_service.get_all_products()


@app.get("/products/{product_id}", response_model=ProductDTO)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductDTO:
    """Obtiene un producto por su identificador."""
    product_repository = SQLProductRepository(db)
    product_service = ProductService(product_repository)

    try:
        return product_service.get_product_by_id(product_id)
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@app.post("/chat", response_model=ChatMessageResponseDTO)
async def send_chat_message(
    request: ChatMessageRequestDTO, db: Session = Depends(get_db)
) -> ChatMessageResponseDTO:
    """Procesa un mensaje del usuario y retorna una respuesta del asistente."""
    product_repository = SQLProductRepository(db)
    chat_repository = SQLChatRepository(db)

    try:
        ai_service = GeminiService()
        chat_service = ChatService(product_repository, chat_repository, ai_service)
        return await chat_service.process_message(request)
    except ChatServiceError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno procesando el chat: {error}",
        ) from error


@app.get("/chat/history/{session_id}", response_model=list[ChatHistoryDTO])
def get_chat_history(
    session_id: str,
    limit: int = Query(default=10, ge=1),
    db: Session = Depends(get_db),
) -> list[ChatHistoryDTO]:
    """Obtiene el historial de una sesión con un límite de mensajes."""
    product_repository = SQLProductRepository(db)
    chat_repository = SQLChatRepository(db)
    chat_service = ChatService(product_repository, chat_repository, ai_service=None)
    return chat_service.get_session_history(session_id, limit=limit)


@app.delete("/chat/history/{session_id}")
def delete_chat_history(
    session_id: str, db: Session = Depends(get_db)
) -> dict[str, object]:
    """Elimina el historial de una sesión y retorna la cantidad borrada."""
    product_repository = SQLProductRepository(db)
    chat_repository = SQLChatRepository(db)
    chat_service = ChatService(product_repository, chat_repository, ai_service=None)
    deleted_count = chat_service.clear_session_history(session_id)
    return {
        "session_id": session_id,
        "deleted_messages": deleted_count,
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Retorna el estado de salud básico de la aplicación."""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
    }
