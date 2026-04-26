"""Servicio de aplicacion para casos de uso relacionados con productos."""

from awesome_agent_api.application.dtos import ProductDTO
from awesome_agent_api.domain.entities import Product
from awesome_agent_api.domain.exceptions import (
    InvalidProductDataError,
    ProductNotFoundError,
)
from awesome_agent_api.domain.repositories import IProductRepository


class ProductService:
    """Orquesta operaciones de productos usando un repositorio inyectado"""

    def __init__(self, product_repository: IProductRepository) -> None:
        """Inicializa el servicio con un repositorio de productos."""
        self.product_repository = product_repository

    def get_all_products(self) -> list[ProductDTO]:
        """Obtiene todos los productos y los transforma a DTOs"""
        products = self.product_repository.get_all()
        return [ProductDTO.model_validate(product) for product in products]

    def get_product_by_id(self, product_id: int) -> ProductDTO:
        """Obtiene un producto por id o lanza ProductNotFoundError."""
        product = self.product_repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return ProductDTO.model_validate(product)

    def search_products(self, filters: dict[str, str]) -> list[ProductDTO]:
        """Busca productos usando filtros simples como marca o categoria"""
        if "brand" in filters and filters["brand"]:
            products = self.product_repository.get_by_brand(filters["brand"])
        elif "category" in filters and filters["category"]:
            products = self.product_repository.get_by_category(filters["category"])
        else:
            products = self.product_repository.get_all()

        return [ProductDTO.model_validate(product) for product in products]

    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """Crea un producto nuevo a partir de un DTO ya validado."""
        product = self._build_product_from_dto(product_dto)

        try:
            saved_product = self.product_repository.save(product)
        except ValueError as error:
            raise InvalidProductDataError(str(error)) from error

        return ProductDTO.model_validate(saved_product)

    def update_product(self, product_id: int, product_dto: ProductDTO) -> ProductDTO:
        """Actualiza un producto existente usando el id recibido"""
        existing_product = self.product_repository.get_by_id(product_id)
        if existing_product is None:
            raise ProductNotFoundError(product_id)

        product = self._build_product_from_dto(product_dto, product_id=product_id)

        try:
            saved_product = self.product_repository.save(product)
        except ValueError as error:
            raise InvalidProductDataError(str(error)) from error

        return ProductDTO.model_validate(saved_product)

    def delete_product(self, product_id: int) -> bool:
        """Elimina un producto existente"""
        product = self.product_repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return self.product_repository.delete(product_id)

    def get_available_products(self) -> list[ProductDTO]:
        """Obtiene solo los productos que todavia tienen stock."""
        products = self.product_repository.get_all()
        available_products = [product for product in products if product.is_available()]
        return [ProductDTO.model_validate(product) for product in available_products]

    def _build_product_from_dto(
        self, product_dto: ProductDTO, product_id: int | None = None
    ) -> Product:
        """Convierte un ProductDTO en una entidad Product"""
        try:
            return Product(
                id=product_id if product_id is not None else product_dto.id,
                name=product_dto.name,
                brand=product_dto.brand,
                category=product_dto.category,
                size=product_dto.size,
                color=product_dto.color,
                price=product_dto.price,
                stock=product_dto.stock,
                description=product_dto.description,
            )
        except ValueError as error:
            raise InvalidProductDataError(str(error)) from error
