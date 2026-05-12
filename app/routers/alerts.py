from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.alert import AlertSchema

router = APIRouter()


@router.get('/', response_model=List[AlertSchema])
async def get_alerts(region: str = None, db: AsyncSession = Depends(get_db)):
    """Get all alerts or filter by region."""
    return []


@router.get('/{region}', response_model=List[AlertSchema])
async def get_alerts_by_region(
    region: str, db: AsyncSession = Depends(get_db)
):
    """Get alerts for a specific region."""
    return []
