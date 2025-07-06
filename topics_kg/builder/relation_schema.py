from pydantic import BaseModel, Field, field_validator
from typing import Literal, List

from topics_kg.builder.config import ALLOWED_RELATION_TYPES


class TopicRelation(BaseModel):
    """
    Schema for structured output representing relationships between LeetCode topics.
    """
    source: str = Field(..., description="Name of the source topic (lowercase, snake_case)")
    relations: List[Literal[*ALLOWED_RELATION_TYPES]] = Field(
        ..., description="List of valid conceptual relationships from source to target"
    )
    target: str = Field(..., description="Name of the target topic (lowercase, snake_case)")

    @field_validator("source", "target")
    def must_be_snake_case(cls, v):
        assert v == v.lower().replace(" ", "_"), "Must be lowercase and snake_case"
        return v