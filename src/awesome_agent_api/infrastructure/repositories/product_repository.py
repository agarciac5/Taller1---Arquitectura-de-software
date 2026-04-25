from sqlalchemy.orm import Session

from awesome_agent_api.domain.entities import Product
from awesome_agent_api.domain.repositories import IProductRepository
from awesome_agent_api.infrastructure.db.models import ProductModel


class SQLProductRepository(IProductRepository):
    """
    Implementacion de repositorio de productos usando SQLAlchemy.

    Convierte entre modelos ORM y entidades del dominio para mantener las
    capas separadas.
    """

    def __init__(self, db: Session) -> None:
        """Inicializa el repositorio con una sesion de base de datos."""
        self.db = db

    def get_all(self) -> list[Product]:
        """Obtiene todos los productos almacenados."""
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(model) for model in models]

    def get_by_id(self, product_id: int) -> Product | None:
        """Obtiene un producto por ID o retorna None si no existe."""
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if model is None:
            return None
        return self._model_to_entity(model)

    def get_by_brand(self, brand: str) -> list[Product]:
        """Obtiene productos de una marca especifica."""
        models = self.db.query(ProductModel).filter(ProductModel.brand == brand).all()
        return [self._model_to_entity(model) for model in models]

    def get_by_category(self, category: str) -> list[Product]:
        """Obtiene productos de una categoria especifica."""
        models = (
            self.db.query(ProductModel).filter(ProductModel.category == category).all()
        )
        return [self._model_to_entity(model) for model in models]

    def save(self, product: Product) -> Product:
        """Guarda o actualiza un producto y retorna la entidad persistida."""
        if product.id is None:
            model = self._entity_to_model(product)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return self._model_to_entity(model)

        model = self.db.query(ProductModel).filter(ProductModel.id == product.id).first()
        if model is None:
            model = self._entity_to_model(product)
            self.db.add(model)
        else:
            model.name = product.name
            model.brand = product.brand
            model.category = product.category
            model.size = product.size
            model.color = product.color
            model.price = product.price
            model.stock = product.stock
            model.description = product.description

        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def delete(self, product_id: int) -> bool:
        """Elimina un producto por ID y retorna True si existia."""
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if model is None:
            return False

        self.db.delete(model)
        self.db.commit()
        return True

    def _model_to_entity(self, model: ProductModel) -> Product:
        """Convierte un modelo ORM en una entidad del dominio."""
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description,
        )

    def _entity_to_model(self, entity: Product) -> ProductModel:
        """Convierte una entidad del dominio en un modelo ORM."""
        return ProductModel(
            id=entity.id,
            name=entity.name,
            brand=entity.brand,
            category=entity.category,
            size=entity.size,
            color=entity.color,
            price=entity.price,
            stock=entity.stock,
            description=entity.description,
        )
