from app.config import Settings


def test_settings_defaults():
    """Test Settings loads default values."""
    s = Settings()
    assert (
        s.database_url
        == 'postgresql+asyncpg://vigia:vigia@localhost:5432/vigia'
    )
    assert s.redis_url == 'redis://localhost:6379/0'
    assert s.llm_provider == 'ollama'
    assert (
        s.test_database_url
        == 'postgresql+asyncpg://vigia:vigia@localhost:5432/vigia_test'
    )


def test_settings_env_override(monkeypatch):
    """Test Settings reads from environment variables."""
    monkeypatch.setenv(
        'DATABASE_URL', 'postgresql+asyncpg://custom:pass@host:5432/db'
    )
    monkeypatch.setenv('LLM_PROVIDER', 'groq')
    s = Settings()
    assert s.database_url == 'postgresql+asyncpg://custom:pass@host:5432/db'
    assert s.llm_provider == 'groq'
