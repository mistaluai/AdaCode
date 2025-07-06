from pydantic import BaseModel, Field, field_validator
from typing import List, Literal

from topics_kg.builder.config import ALLOWED_RELATION_TYPES


class RelationDetail(BaseModel):
    """
    Represents a single relation between two topics with its type and a human-readable description.
    """
    type: Literal[*ALLOWED_RELATION_TYPES] = Field(
        ..., description="Type of conceptual relationship from source to target"
    )
    description: str = Field(
        ..., description="Explanation of what the relationship means in the context of the topics"
    )


class TopicRelation(BaseModel):
    """
    Schema for structured output representing relationships between LeetCode topics.
    """
    source: str = Field(..., description="Name of the source topic (lowercase, snake_case)")
    relations: List[RelationDetail] = Field(
        ..., description="List of relation objects describing connections from source to target"
    )
    target: str = Field(..., description="Name of the target topic (lowercase, snake_case)")

    @field_validator("source", "target")
    def must_be_snake_case(cls, v):
        assert v == v.lower().replace(" ", "_"), "Must be lowercase and snake_case"
        return v