from pydantic import BaseModel
from typing import Optional, List

class EntityCreate(BaseModel):
    title: str
    description: Optional[str] = None
    value: Optional[int] = None
    verified: Optional[bool] = True

class EntityResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    value: Optional[int] = None
    verified: Optional[bool] = None

class EntityList(BaseModel):
    entity: List[EntityResponse]