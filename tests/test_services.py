from datetime import datetime

import pytest

from awesome_agent_api.application.chat_service import ChatService
from awesome_agent_api.application.dtos import ChatMessageRequestDTO, ProductDTO
from awesome_agent_api.application.product_service import ProductService
from awesome_agent_api.domain.entities import ChatMessage, Product
from awesome_agent_api.domain.exceptions import ChatServiceError, ProductNotFoundError


class FakeProductRepository:
    def __init__(self, products: list[Product] | None = None) -> None:
        self.products = products or []

    def get_all(self) -> list[Product]:
        return self.products

    def get_by_id(self, product_id: int) -> Product | None:
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def get_by_brand(self, brand: str) -> list[Product]:
        return [product for product in self.products if product.brand == brand]

    def get_by_category(self, category: str) -> list[Product]:
        return [product for product in self.products if product.category == category]

    def save(self, product: Product) -> Product:
        if product.id is None:
            product.id = len(self.products) + 1
            self.products.append(product)
            return product

        for index, existing in enumerate(self.products):
            if existing.id == product.id:
                self.products[index] = product
                return product

        self.products.append(product)
        return product

    def delete(self, product_id: int) -> bool:
        product = self.get_by_id(product_id)
        if product is None:
            return False
        self.products.remove(product)
        return True


class FakeChatRepository:
    def __init__(self, messages: list[ChatMessage] | None = None) -> None:
        self.messages = messages or []

    def save_message(self, message: ChatMessage) -> ChatMessage:
        if message.id is None:
            message.id = len(self.messages) + 1
        self.messages.append(message)
        return message

    def get_session_history(
        self, session_id: str, limit: int | None = None
    ) -> list[ChatMessage]:
        session_messages = [
            message for message in self.messages if message.session_id == session_id
        ]
        if limit is None:
            return session_messages
        return session_messages[-limit:]

    def delete_session_history(self, session_id: str) -> int:
        session_messages = [
            message for message in self.messages if message.session_id == session_id
        ]
        self.messages = [
            message for message in self.messages if message.session_id != session_id
        ]
        return len(session_messages)

    def get_recent_messages(self, session_id: str, count: int) -> list[ChatMessage]:
        return self.get_session_history(session_id, limit=count)


class FakeAIService:
    async def generate_response(self, user_message: str, products, context) -> str:
        return f"Respuesta a: {user_message}"


class FailingAIService:
    async def generate_response(self, user_message: str, products, context) -> str:
        raise RuntimeError("Fallo inesperado")


def build_product(product_id: int = 1, stock: int = 5) -> Product:
    return Product(
        id=product_id,
        name="Pegasus",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=120.0,
        stock=stock,
        description="Zapato de prueba",
    )


def build_chat_message(
    message_id: int, session_id: str, role: str, message: str
) -> ChatMessage:
    return ChatMessage(
        id=message_id,
        session_id=session_id,
        role=role,
        message=message,
        timestamp=datetime.utcnow(),
    )


def test_product_service_returns_all_products() -> None:
    repository = FakeProductRepository(products=[build_product()])
    service = ProductService(repository)

    result = service.get_all_products()

    assert len(result) == 1
    assert result[0].name == "Pegasus"


def test_product_service_raises_when_product_not_found() -> None:
    repository = FakeProductRepository()
    service = ProductService(repository)

    with pytest.raises(ProductNotFoundError):
        service.get_product_by_id(99)


def test_product_service_creates_product() -> None:
    repository = FakeProductRepository()
    service = ProductService(repository)
    dto = ProductDTO(
        name="Ultraboost",
        brand="Adidas",
        category="Running",
        size="41",
        color="Blanco",
        price=150.0,
        stock=3,
        description="Zapato de prueba",
    )

    result = service.create_product(dto)

    assert result.id == 1
    assert len(repository.products) == 1


@pytest.mark.asyncio
async def test_chat_service_process_message_with_mocks() -> None:
    product_repository = FakeProductRepository(products=[build_product()])
    chat_repository = FakeChatRepository()
    ai_service = FakeAIService()
    service = ChatService(product_repository, chat_repository, ai_service)
    request = ChatMessageRequestDTO(session_id="session-1", message="Hola")

    result = await service.process_message(request)

    assert result.session_id == "session-1"
    assert result.user_message == "Hola"
    assert result.assistant_message == "Respuesta a: Hola"
    assert len(chat_repository.messages) == 2


@pytest.mark.asyncio
async def test_chat_service_wraps_unexpected_errors() -> None:
    product_repository = FakeProductRepository(products=[build_product()])
    chat_repository = FakeChatRepository()
    ai_service = FailingAIService()
    service = ChatService(product_repository, chat_repository, ai_service)
    request = ChatMessageRequestDTO(session_id="session-1", message="Hola")

    with pytest.raises(ChatServiceError):
        await service.process_message(request)
