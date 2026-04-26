FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH=/app/src

CMD ["uvicorn", "awesome_agent_api.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
