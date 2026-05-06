from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_app_directory_exists():
    """Verify app directory exists."""
    app_dir = PROJECT_ROOT / 'app'
    assert app_dir.exists(), 'app directory should exist'
    assert app_dir.is_dir(), 'app should be a directory'


def test_app_init_file_exists():
    """Verify app/__init__.py exists."""
    init_file = PROJECT_ROOT / 'app' / '__init__.py'
    assert init_file.exists(), 'app/__init__.py should exist'


def test_pyproject_toml_exists():
    """Verify pyproject.toml exists."""
    pyproject = PROJECT_ROOT / 'pyproject.toml'
    assert pyproject.exists(), 'pyproject.toml should exist'


def test_docker_compose_exists():
    """Verify docker-compose.yml exists."""
    docker_compose = PROJECT_ROOT / 'docker-compose.yml'
    assert docker_compose.exists(), 'docker-compose.yml should exist'


def test_app_subdirectories_exist():
    """Verify all required app subdirectories exist."""
    required_dirs = [
        'models',
        'schemas',
        'routers',
        'collectors',
        'analyzers',
        'workers',
        'kafka',
        'notifiers',
        'bot',
        'services',
    ]
    for dirname in required_dirs:
        dir_path = PROJECT_ROOT / 'app' / dirname
        assert dir_path.exists(), f'app/{dirname} directory should exist'
        assert dir_path.is_dir(), f'app/{dirname} should be a directory'


def test_migrations_directory_exists():
    """Verify migrations directory exists."""
    migrations_dir = PROJECT_ROOT / 'migrations'
    assert migrations_dir.exists(), 'migrations directory should exist'


def test_tests_directory_exists():
    """Verify tests directory exists."""
    tests_dir = PROJECT_ROOT / 'tests'
    assert tests_dir.exists(), 'tests directory should exist'


def test_scripts_directory_exists():
    """Verify scripts directory exists."""
    scripts_dir = PROJECT_ROOT / 'scripts'
    assert scripts_dir.exists(), 'scripts directory should exist'


def test_data_directory_exists():
    """Verify data directory exists."""
    data_dir = PROJECT_ROOT / 'data'
    assert data_dir.exists(), 'data directory should exist'
