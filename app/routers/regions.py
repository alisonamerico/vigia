from typing import List

from fastapi import APIRouter

from app.schemas.region import RegionSchema

router = APIRouter()


@router.get("/", response_model=List[RegionSchema])
async def get_regions():
    """Get all monitoring regions."""
    return []
