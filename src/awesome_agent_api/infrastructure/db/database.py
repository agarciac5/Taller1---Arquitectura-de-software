"""Configuracion de SQLAlchemy para conexion, sesiones e inicializacion."""

import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/ecommerce_chat.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Provee una sesion de base de datos para FastAPI

    Yields:
        Session: sesion activa de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Inicializa la base de datos creando tablas y cargando datos iniciales"""
    from awesome_agent_api.infrastructure.db import models

    Base.metadata.create_all(bind=engine)

    try:
        from awesome_agent_api.infrastructure.db.init_data import load_initial_data

        load_initial_data()
    except ImportError:
        pass
