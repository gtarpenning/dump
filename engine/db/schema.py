from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, PositiveInt, ValidationError


class Transcription(BaseModel):
    user_id: int
    text: str
    version: PositiveInt  # str?
    created_on: datetime


class Tag(BaseModel):
    user_id: int
    tag: str
    date: List[datetime]


class User(BaseModel):
    user_id: int
    email: str
    created_on: datetime | None
    tags: List[Tag]


def load_model(model: BaseModel, data: Dict[str, Any]) -> Optional[BaseModel]:
    """Convert raw to pydantic model."""
    try:
        return model(**data)
    except ValidationError as e:
        print(e.errors())
        return None
