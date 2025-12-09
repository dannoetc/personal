# app/db_models.py

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    password_hash = Column(String, nullable=True)
    auth_provider = Column(String, nullable=False)
    google_sub = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    # NEW: user timezone (IANA name, e.g. "America/Denver")
    timezone = Column(String, nullable=False, default="UTC")

    # IMPORTANT: backref used by Session.user
    sessions = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, nullable=False, unique=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="sessions")

    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)

    target_minutes_per_question = Column(Float, nullable=True)

    current_question_index = Column(Integer, nullable=True)
    current_question_started_at = Column(DateTime, nullable=True)

    pause_accumulated_seconds = Column(Float, nullable=False, default=0.0)
    is_paused = Column(Boolean, nullable=False, default=False)
    pause_started_at = Column(DateTime, nullable=True)

    events = relationship(
        "Event",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    questions = relationship(
        "Question",
        back_populates="session",
        cascade="all, delete-orphan",
    )


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    type = Column(String, nullable=False)  # "NEXT", "PAUSE", "EXIT", "UNDO", etc.
    timestamp = Column(DateTime, nullable=False)

    session = relationship("Session", back_populates="events")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)

    # Per-session question number
    index = Column(Integer, nullable=False)

    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=False)

    raw_seconds = Column(Float, nullable=False)
    active_seconds = Column(Float, nullable=False)

    session = relationship("Session", back_populates="questions")
