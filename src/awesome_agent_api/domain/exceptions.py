"""Excepciones de dominio para productos y flujo de chat."""


class ProductNotFoundError(Exception):
    """Se lanza cuando se intenta consultar un producto que no existe"""

    def __init__(self, product_id: int | None = None) -> None:
        """Construye la excepcion con un mensaje simple o con el id"""
        if product_id is None:
            message = "Producto no encontrado"
        else:
            message = f"Producto con ID {product_id} no encontrado"
        super().__init__(message)


class InvalidProductDataError(Exception):
    """Se usa cuando los datos de un producto no pasan validacion."""

    def __init__(self, message: str = "Datos de producto invalidos") -> None:
        """Crea la excepcion con un mensaje personalizado"""
        super().__init__(message)


class ChatServiceError(Exception):
    """Error relacionado con el servicio de chat"""

    def __init__(self, message: str = "Error en el servicio de chat") -> None:
        """Crea la excepcion con el mensaje recibido o el mensaje por defecto."""
        super().__init__(message)
