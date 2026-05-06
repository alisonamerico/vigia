from pydantic import BaseModel, ConfigDict


class RegionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    geom: str
    threshold_green: float = 30.0
    threshold_yellow: float = 50.0
    threshold_orange: float = 100.0
    threshold_red: float = 150.0


class RegionCreate(RegionBase):
    pass


class RegionSchema(RegionBase):
    id: int
