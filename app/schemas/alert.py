from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class AlertBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    region: str
    level: str
    rain_mm: Optional[float] = None
    river: Optional[str] = None
    river_level_m: Optional[float] = None
    sources: Optional[List[str]] = None


class AlertCreate(AlertBase):
    timestamp: Optional[str] = None


class AlertSchema(AlertBase):
    id: int
    timestamp: Optional[str] = None
