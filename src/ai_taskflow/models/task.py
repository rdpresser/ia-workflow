import enum
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.ai_taskflow.core.database import Base


class TaskStatus(str, enum.Enum):
    """Represents the AI task lifecycle state machine."""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Task(Base):
    """Domain entity mapped to the 'tasks' table in PostgreSQL."""

    __tablename__ = "tasks"

    # UUIDv4 as native primary key.
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Payload submitted by the client (raw transcript text, logs, etc.).
    content: Mapped[str] = mapped_column(String, nullable=False)

    # Requested analysis type (for example: "summarize", "bug_hunt").
    task_type: Mapped[str] = mapped_column(String(50), nullable=False)

    # Current task state.
    status: Mapped[TaskStatus] = mapped_column(
        String(20), default=TaskStatus.PENDING, nullable=False
    )

    # Structured AI output (mapped as JSON/JSONB depending on backend).
    # Keep dict[str, Any] for static typing compatibility with MyPy.
    result: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Timestamp audit fields with fixed UTC timezone.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Task id={self.id} status={self.status} type={self.task_type}>"
