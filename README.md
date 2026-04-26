E-commerce con Chat IA

Descripcion
Este proyecto es una API REST de una tienda de zapatos con chat inteligente. Permite consultar productos y enviar mensajes a un asistente para recibir recomendaciones.

Arquitectura
El proyecto esta dividido en 3 capas:
domain: entidades, reglas de negocio, interfaces y excepciones
application: servicios y DTOs
infrastructure: FastAPI, base de datos, repositorios y Gemini

Caracteristicas
Lista productos
Busca productos por id
Permite enviar mensajes al chat
Muestra historial por sesion
Permite eliminar historial
Usa SQLite
Tiene pruebas unitarias
Tiene Docker

Instalacion
Clonar el repositorio:
git clone <url-del-repo>
cd Taller1

Crear entorno virtual:
python -m venv venv

Activarlo en Windows:
venv\Scripts\activate

Instalar dependencias:
pip install -r requirements.txt

Configuracion
Crear un archivo .env con esto:
GEMINI_API_KEY=AIzaSyD41e2powSs7I4p1jixbFrWL_3p1wm76FM
DATABASE_URL=sqlite:///./data/ecommerce_chat.db
ENVIRONMENT=development

Uso
Para correr el proyecto sin Docker:
uvicorn awesome_agent_api.infrastructure.api.main:app --reload

Luego puedes entrar a:
http://localhost:8000
http://localhost:8000/docs
http://localhost:8000/redoc

Endpoints
GET /
GET /products
GET /products/{product_id}
POST /chat
GET /chat/history/{session_id}
DELETE /chat/history/{session_id}
GET /health

Testing
Para correr las pruebas:
pytest

Si usas el entorno virtual en Windows:
.\venv\Scripts\python.exe -m pytest

Docker
Para levantar el proyecto con Docker:
docker-compose up --build

Tecnologias
Python
FastAPI
SQLAlchemy
SQLite
Pydantic
Google Gemini
Pytest
Docker

Estructura
Taller1/
src/
awesome_agent_api/
domain/
application/
infrastructure/
tests/
data/
Dockerfile
docker-compose.yml
requirements.txt
pyproject.toml

Nota
Para que el endpoint de chat funcione bien, debes tener una API key valida de Gemini en el archivo .env.
