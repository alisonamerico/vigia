from fastapi import FastAPI

from app.routers.alerts import router as alerts_router
from app.routers.health import router as health_router
from app.routers.regions import router as regions_router

app = FastAPI(
    title='Vigia',
    description='Monitoramento de riscos climáticos para Pernambuco',
    version='0.1.0',
)

app.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
app.include_router(regions_router, prefix="/regions", tags=["regions"])
app.include_router(health_router, prefix="/health", tags=["health"])


@app.get('/health')
async def health_check():
    return {'status': 'ok'}
