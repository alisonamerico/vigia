from pathlib import Path

import pytest
from geoalchemy2.functions import ST_IsValid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.region import Region
from scripts.seed_regions import load_geojson, seed_database


def test_seed_script_exists():
    """Test seed_regions.py script exists."""
    script_path = Path('scripts/seed_regions.py')
    assert script_path.exists(), 'scripts/seed_regions.py should exist'


def test_seed_script_has_load_geojson_function():
    """Test seed script has load_geojson function."""
    assert callable(load_geojson), 'load_geojson should be a function'


def test_seed_script_has_seed_database_function():
    """Test seed script has seed_database function."""
    assert callable(seed_database), 'seed_database should be a function'


@pytest.mark.skipif(
    condition=True,
    reason='Requires PostgreSQL + PostGIS running via Docker Compose',
)
@pytest.mark.asyncio
async def test_seed_regions_creates_records():
    """Test seeding regions creates database records."""
    await seed_database()
    engine = create_async_engine(settings.database_url)
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Region))
        regions = result.scalars().all()
        assert len(regions) > 0, 'Should have created region records'
    await engine.dispose()


@pytest.mark.skipif(
    condition=True,
    reason='Requires PostgreSQL + PostGIS running via Docker Compose',
)
@pytest.mark.asyncio
async def test_seeded_region_has_geometry():
    """Test seeded region has valid PostGIS geometry."""
    await seed_database()
    engine = create_async_engine(settings.database_url)
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Region).limit(1))
        region = result.scalar_one()
        assert region.geom is not None, 'Region should have geometry'
        is_valid = await session.execute(select(ST_IsValid(region.geom)))
        assert is_valid.scalar(), 'Geometry should be valid PostGIS geometry'
    await engine.dispose()
