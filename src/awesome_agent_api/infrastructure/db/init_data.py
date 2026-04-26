"""Carga de datos iniciales para poblar la base de datos."""

from sqlalchemy.orm import Session

from awesome_agent_api.infrastructure.db.database import SessionLocal
from awesome_agent_api.infrastructure.db.models import ProductModel


def load_initial_data() -> None:
    """Inserta productos de ejemplo si la base de datos esta vacia"""
    session: Session = SessionLocal()

    try:
        product_count = session.query(ProductModel).count()
        if product_count > 0:
            return

        products = [
            ProductModel(
                name="Air Zoom Pegasus",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=120.0,
                stock=5,
                description="Zapato de running con buena amortiguacion.",
            ),
            ProductModel(
                name="Ultraboost 21",
                brand="Adidas",
                category="Running",
                size="41",
                color="Blanco",
                price=150.0,
                stock=3,
                description="Zapato comodo para correr largas distancias.",
            ),
            ProductModel(
                name="Suede Classic",
                brand="Puma",
                category="Casual",
                size="40",
                color="Azul",
                price=80.0,
                stock=10,
                description="Zapato casual clasico para uso diario.",
            ),
            ProductModel(
                name="Classic Leather",
                brand="Reebok",
                category="Casual",
                size="39",
                color="Blanco",
                price=75.0,
                stock=8,
                description="Zapato casual de cuero con estilo tradicional.",
            ),
            ProductModel(
                name="RS-X",
                brand="Puma",
                category="Casual",
                size="43",
                color="Gris",
                price=95.0,
                stock=6,
                description="Zapato urbano con diseno moderno.",
            ),
            ProductModel(
                name="Gel-Kayano",
                brand="Asics",
                category="Running",
                size="42",
                color="Rojo",
                price=165.0,
                stock=4,
                description="Zapato de running con soporte y estabilidad.",
            ),
            ProductModel(
                name="Oxford Executive",
                brand="Bata",
                category="Formal",
                size="41",
                color="Cafe",
                price=110.0,
                stock=7,
                description="Zapato formal elegante para ocasiones especiales.",
            ),
            ProductModel(
                name="Derby Prime",
                brand="Velez",
                category="Formal",
                size="42",
                color="Negro",
                price=135.0,
                stock=5,
                description="Zapato formal en cuero con acabado premium.",
            ),
            ProductModel(
                name="Court Vision",
                brand="Nike",
                category="Casual",
                size="40",
                color="Blanco",
                price=90.0,
                stock=9,
                description="Zapato casual inspirado en estilo deportivo.",
            ),
            ProductModel(
                name="Grand Court",
                brand="Adidas",
                category="Casual",
                size="44",
                color="Negro",
                price=85.0,
                stock=12,
                description="Zapato versatil para uso diario y caminatas.",
            ),
        ]

        session.add_all(products)
        session.commit()
    finally:
        session.close()
