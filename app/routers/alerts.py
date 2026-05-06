from typing import List

from fastapi import APIRouter

from app.schemas.alert import AlertSchema

router = APIRouter()


@router.get("/", response_model=List[AlertSchema])
async def get_alerts(region: str = None):
    """Get all alerts or filter by region."""
    return []


@router.get("/{region}", response_model=List[AlertSchema])
async def get_alerts_by_region(region: str):
    """Get alerts for a specific region."""
    return []
