import enum
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.ai_taskflow.core.database import Base


class TaskStatus(str, enum.Enum):
    """Representa a máquina de estados (lifecycle) da tarefa de IA."""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Task(Base):
    """Entidade de domínio que mapeia a tabela 'tasks' no PostgreSQL."""

    __tablename__ = "tasks"

    # UUIDv4 como chave primária nativa do banco
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Payload enviado pelo cliente (o texto bruto da transcrição, log, etc.)
    content: Mapped[str] = mapped_column(String, nullable=False)

    # O tipo de análise requisitada (ex: "summarize", "bug_hunt")
    task_type: Mapped[str] = mapped_column(String(50), nullable=False)

    # Estado atual da tarefa
    status: Mapped[TaskStatus] = mapped_column(
        String(20), default=TaskStatus.PENDING, nullable=False
    )

    # Resultado estruturado da IA (Mapeado como JSONB no Postgres)
    # Usamos dict[str, Any] para que o MyPy consiga fazer checagem estática livre
    result: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Auditoria Temporal (Data com timezone UTC fixo)
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
