from fastapi import FastAPI

app = FastAPI(
    title='Vigia',
    description='Monitoramento de riscos climáticos para Pernambuco',
    version='0.1.0',
)


@app.get('/health')
async def health_check():
    return {'status': 'ok'}
