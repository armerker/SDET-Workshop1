from pydantic import BaseModel
from typing import Optional, List


class AdditionRequest(BaseModel):
    """Дополнительная информация о сущности (запрос)"""
    additional_info: Optional[str] = None
    additional_number: Optional[int] = None


class AdditionResponse(AdditionRequest):
    """Дополнительная информация о сущности (ответ)"""
    id: int


class EntityCreate(BaseModel):
    """Модель для создания сущности"""
    title: str
    verified: Optional[bool] = True
    important_numbers: Optional[List[int]] = None
    addition: Optional[AdditionRequest] = None


class EntityUpdate(BaseModel):
    """Модель для обновления сущности"""
    title: Optional[str] = None
    verified: Optional[bool] = None
    important_numbers: Optional[List[int]] = None
    addition: Optional[AdditionRequest] = None