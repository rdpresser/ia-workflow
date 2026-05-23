import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.ai_taskflow.models.task import TaskStatus


class TaskBase(BaseModel):
    """Base contract with fields shared across task schemas."""

    # Field metadata improves OpenAPI docs and adds extra validation rules.
    task_type: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description=("Analysis type the AI should execute (for example: summarize, bug_hunt)"),
        examples=["summarize"],
    )
    content: str = Field(
        ...,
        min_length=5,
        description="Raw text content sent for AI processing",
    )


class TaskCreate(TaskBase):
    """Inbound DTO used to create new tasks.

    Inherits common fields from TaskBase and represents the POST payload.
    """

    pass


class TaskResponse(TaskBase):
    """Outbound DTO used for API responses.

    Defines the exact data returned by the API while avoiding unnecessary
    infrastructure details.
    """

    # Pydantic v2 config for attribute-based ORM object parsing.
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: TaskStatus
    result: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime
