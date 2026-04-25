import os

from dotenv import load_dotenv
import google.generativeai as genai

from awesome_agent_api.domain.entities import ChatContext, Product
from awesome_agent_api.domain.exceptions import ChatServiceError

load_dotenv()


class GeminiService:
    """
    Servicio de infraestructura para generar respuestas con Google Gemini.

    Se encarga de construir el prompt, invocar el modelo y retornar el texto
    generado para el flujo conversacional del e-commerce.
    """

    def __init__(self) -> None:
        """Configura el cliente de Gemini usando la API key del entorno."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ChatServiceError("No se encontro GEMINI_API_KEY en las variables de entorno.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def generate_response(
        self, user_message: str, products: list[Product], context: ChatContext
    ) -> str:
        """Genera una respuesta usando Gemini con productos y contexto."""
        try:
            products_info = self.format_products_info(products)
            conversation_history = context.format_for_prompt()
            prompt = self._build_prompt(
                user_message=user_message,
                products_info=products_info,
                conversation_history=conversation_history,
            )

            response = await self.model.generate_content_async(prompt)
            generated_text = getattr(response, "text", "").strip()

            if not generated_text:
                raise ChatServiceError("Gemini no retorno contenido util.")

            return generated_text
        except ChatServiceError:
            raise
        except Exception as error:
            raise ChatServiceError(f"Error al generar respuesta con Gemini: {error}") from error

    def format_products_info(self, products: list[Product]) -> str:
        """Convierte la lista de productos a un texto legible para el prompt."""
        if not products:
            return "No hay productos disponibles en este momento."

        lines = []
        for product in products:
            lines.append(
                f"- {product.name} | {product.brand} | ${product.price} | "
                f"Talla {product.size} | Stock {product.stock}"
            )
        return "\n".join(lines)

    def _build_prompt(
        self, user_message: str, products_info: str, conversation_history: str
    ) -> str:
        """Construye el prompt completo para enviar al modelo."""
        history_section = (
            conversation_history if conversation_history else "No hay historial previo."
        )

        return f"""
Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.

PRODUCTOS DISPONIBLES:
{products_info}

INSTRUCCIONES:
- Se amigable y profesional
- Usa el contexto de la conversacion anterior
- Recomienda productos especificos cuando sea apropiado
- Menciona precios, tallas y disponibilidad
- Si no tienes informacion, se honesto

HISTORIAL DE CONVERSACION:
{history_section}

Usuario: {user_message}

Asistente:
""".strip()
