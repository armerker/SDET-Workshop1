from pydantic import BaseModel
from typing import Optional, List
from .entity_models import AdditionResponse


class EntityResponse(BaseModel):
    """Модель ответа API для сущности"""
    id: int
    title: str
    verified: Optional[bool] = None
    important_numbers: Optional[List[int]] = None
    addition: Optional[AdditionResponse] = None


class EntityListResponse(BaseModel):
    """Модель ответа для списка сущностей"""
    entity: List[EntityResponse]


class CreateEntityResponse(BaseModel):
    """Модель ответа при создании сущности (только ID)"""
    id: int