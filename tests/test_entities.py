from datetime import datetime

import pytest

from awesome_agent_api.domain.entities import ChatContext, ChatMessage, Product


def test_product_validations_raise_error_for_invalid_data() -> None:
    with pytest.raises(ValueError):
        Product(
            id=None,
            name="",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=5,
            description="Zapato de prueba",
        )

    with pytest.raises(ValueError):
        Product(
            id=None,
            name="Pegasus",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=0,
            stock=5,
            description="Zapato de prueba",
        )

    with pytest.raises(ValueError):
        Product(
            id=None,
            name="Pegasus",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=-1,
            description="Zapato de prueba",
        )


def test_product_availability_and_reduce_stock() -> None:
    product = Product(
        id=1,
        name="Pegasus",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=120.0,
        stock=5,
        description="Zapato de prueba",
    )

    assert product.is_available() is True

    product.reduce_stock(2)
    assert product.stock == 3

    with pytest.raises(ValueError):
        product.reduce_stock(0)

    with pytest.raises(ValueError):
        product.reduce_stock(10)


def test_chat_message_validations() -> None:
    now = datetime.utcnow()

    with pytest.raises(ValueError):
        ChatMessage(
            id=None,
            session_id="",
            role="user",
            message="Hola",
            timestamp=now,
        )

    with pytest.raises(ValueError):
        ChatMessage(
            id=None,
            session_id="session-1",
            role="admin",
            message="Hola",
            timestamp=now,
        )

    with pytest.raises(ValueError):
        ChatMessage(
            id=None,
            session_id="session-1",
            role="assistant",
            message="",
            timestamp=now,
        )


def test_chat_context_format_for_prompt() -> None:
    now = datetime.utcnow()
    messages = [
        ChatMessage(
            id=1,
            session_id="session-1",
            role="user",
            message="Busco zapatos para correr",
            timestamp=now,
        ),
        ChatMessage(
            id=2,
            session_id="session-1",
            role="assistant",
            message="Tengo varias opciones disponibles",
            timestamp=now,
        ),
    ]

    context = ChatContext(messages=messages)

    assert context.format_for_prompt() == (
        "Usuario: Busco zapatos para correr\n"
        "Asistente: Tengo varias opciones disponibles"
    )
