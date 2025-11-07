from pydantic import BaseModel
from typing import Optional, List

class AdditionRequest(BaseModel):
    """Дополнительная информация о сущности"""
    additional_info: Optional[str] = None
    additional_number: Optional[int] = None

class EntityCreate(BaseModel):
    """Модель для создания сущности"""
    title: str
    verified: Optional[bool] = True
    important_numbers: Optional[List[int]] = None
    addition: Optional[AdditionRequest] = None

class AdditionResponse(AdditionRequest):
    id: int

class EntityResponse(BaseModel):
    """Модель ответа API для сущности"""
    id: int
    title: str
    verified: Optional[bool] = None
    important_numbers: Optional[List[int]] = None
    addition: Optional[AdditionResponse] = None