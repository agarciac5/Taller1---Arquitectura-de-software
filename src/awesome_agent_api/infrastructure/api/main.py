from datetime import datetime

from fastapi import FastAPI

from awesome_agent_api.infrastructure.api.models import (
    ChatHistoryDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ProductDTO,
)


app = FastAPI(
    title="E-commerce con Chat IA",
    description="API REST básica para el taller de e-commerce de zapatos con chat inteligente.",
    version="0.1.0",
)

PRODUCTS = [
    ProductDTO(
        id=1,
        name="Air Zoom Pegasus",
        brand="Nike",
        category="Running",
        size=42,
        color="Negro",
        price=120.0,
        stock=5,
    ),
    ProductDTO(
        id=2,
        name="Ultraboost 21",
        brand="Adidas",
        category="Running",
        size=41,
        color="Blanco",
        price=150.0,
        stock=3,
    ),
]

CHAT_HISTORY: list[ChatHistoryDTO] = []


@app.get("/")
def read_root() -> dict[str, str]:
    """Retorna información básica de la API."""
    return {
        "name": "E-commerce con Chat IA",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/products", response_model=list[ProductDTO])
def list_products() -> list[ProductDTO]:
    """Lista los productos disponibles en la tienda."""
    return PRODUCTS


@app.get("/products/{product_id}", response_model=ProductDTO)
def get_product(product_id: int) -> ProductDTO | None:
    """Obtiene un producto por su identificador."""
    for product in PRODUCTS:
        if product.id == product_id:
            return product
    return None


@app.post("/chat", response_model=ChatMessageResponseDTO)
def send_chat_message(request: ChatMessageRequestDTO) -> ChatMessageResponseDTO:
    """Procesa un mensaje de chat y retorna una respuesta básica."""
    now = datetime.now()
    assistant_message = "Hola, soy el asistente de la tienda. Puedo ayudarte a encontrar zapatos."

    CHAT_HISTORY.append(
        ChatHistoryDTO(
            session_id=request.session_id,
            role="user",
            message=request.message,
            timestamp=now,
        )
    )
    CHAT_HISTORY.append(
        ChatHistoryDTO(
            session_id=request.session_id,
            role="assistant",
            message=assistant_message,
            timestamp=now,
        )
    )

    return ChatMessageResponseDTO(
        session_id=request.session_id,
        user_message=request.message,
        assistant_message=assistant_message,
        timestamp=now,
    )


@app.get("/chat/history/{session_id}", response_model=list[ChatHistoryDTO])
def get_chat_history(session_id: str, limit: int = 10) -> list[ChatHistoryDTO]:
    """Obtiene los últimos mensajes del historial de una sesión."""
    session_messages = [
        message for message in CHAT_HISTORY if message.session_id == session_id
    ]
    return session_messages[-limit:]
