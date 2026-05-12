import json
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.region import Region


DATA_PATH = Path("data/regions_pe.geojson")


async def load_geojson():
    """Load GeoJSON file and return features."""
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data["features"]


async def seed_database():
    """Seed regions from GeoJSON into database."""
    engine = create_async_engine(settings.database_url)
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        features = await load_geojson()
        for feature in features:
            nome = feature["properties"]["nome"]
            geom_json = json.dumps(feature["geometry"])
            stmt = text("""
                INSERT INTO regions (nome, geom)
                VALUES (:nome, ST_SetSRID(ST_GeomFromGeoJSON(:geom), 4326))
            """)
            await session.execute(stmt, {"nome": nome, "geom": geom_json})
        await session.commit()
    await engine.dispose()


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_database())
