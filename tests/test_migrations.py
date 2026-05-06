from pathlib import Path


def test_alembic_config_exists():
    """Test alembic.ini exists."""
    config_file = Path("alembic.ini")
    assert config_file.exists(), "alembic.ini should exist"


def test_migrations_directory_structure():
    """Test migrations directory has proper structure."""
    migrations_dir = Path("migrations")
    assert migrations_dir.exists(), "migrations/ should exist"

    # Check for versions directory
    versions_dir = migrations_dir / "versions"
    assert versions_dir.exists(), "migrations/versions/ should exist"

    # Check for env.py
    env_file = migrations_dir / "env.py"
    assert env_file.exists(), "migrations/env.py should exist"

    # Check for script.py.mako
    script_mako = migrations_dir / "script.py.mako"
    assert script_mako.exists(), "migrations/script.py.mako should exist"


def test_env_py_has_async_support():
    """Test env.py is configured for async SQLAlchemy."""
    env_file = Path("migrations/env.py")
    content = env_file.read_text(encoding="utf-8")

    # Check for async engine configuration
    assert (
        "asyncio" in content.lower() or "async_engine" in content
    ), "env.py should have async support"
    assert (
        "AsyncSession" in content or "asyncio" in content
    ), "env.py should use async session"
