class ProductNotFoundError(Exception):
    """
    Se lanza cuando se busca un producto que no existe.

    Permite indicar opcionalmente el ID del producto no encontrado.
    """

    def __init__(self, product_id: int | None = None) -> None:
        """Crea la excepcion con un mensaje descriptivo."""
        if product_id is None:
            message = "Producto no encontrado"
        else:
            message = f"Producto con ID {product_id} no encontrado"
        super().__init__(message)


class InvalidProductDataError(Exception):
    """
    Se lanza cuando los datos de un producto son invalidos.

    Permite usar un mensaje personalizado o un mensaje por defecto.
    """

    def __init__(self, message: str = "Datos de producto invalidos") -> None:
        """Crea la excepcion con el mensaje indicado."""
        super().__init__(message)


class ChatServiceError(Exception):
    """
    Se lanza cuando ocurre un error en el servicio de chat.

    Representa errores de negocio relacionados con el flujo conversacional.
    """

    def __init__(self, message: str = "Error en el servicio de chat") -> None:
        """Crea la excepcion con el mensaje indicado."""
        super().__init__(message)
