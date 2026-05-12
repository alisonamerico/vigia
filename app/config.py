from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'postgresql+asyncpg://vigia:vigia@localhost:5432/vigia'
    redis_url: str = 'redis://localhost:6379/0'
    kafka_bootstrap_servers: str = 'localhost:9092'
    telegram_bot_token: str = ''
    llm_provider: str = 'ollama'
    ollama_base_url: str = 'http://localhost:11434'
    ollama_model: str = 'llama3.2:3b'
    groq_api_key: str = ''
    test_database_url: str = (
        'postgresql+asyncpg://vigia:vigia@localhost:5432/vigia_test'
    )

    model_config = {'env_file': '.env', 'env_file_encoding': 'utf-8'}


settings = Settings()
