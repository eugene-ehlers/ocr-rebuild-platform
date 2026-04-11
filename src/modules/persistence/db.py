"""Persistence bootstrap for System B.

This module defines the SQLAlchemy engine/session baseline only.
No business logic and no schema-specific models are implemented here.
"""

from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "SYSTEM_B_DATABASE_URL",
    "postgresql+psycopg://CHANGE_ME_USER:CHANGE_ME_PASSWORD@CHANGE_ME_HOST:5432/CHANGE_ME_DB",
)

Base = declarative_base()

engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
