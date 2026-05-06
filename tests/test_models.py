from app.models.alert import Alert
from app.models.reading import Reading
from app.models.region import Region
from app.models.user import User


def test_region_model_exists():
    """Test Region model can be imported."""
    assert Region is not None


def test_region_model_fields():
    """Test Region model has required fields."""
    # Check table name
    assert hasattr(Region, "__tablename__")
    assert Region.__tablename__ == "regions"

    # Check required columns exist
    assert hasattr(Region, "id")
    assert hasattr(Region, "nome")
    assert hasattr(Region, "geom")
    assert hasattr(Region, "threshold_green")
    assert hasattr(Region, "threshold_yellow")
    assert hasattr(Region, "threshold_orange")
    assert hasattr(Region, "threshold_red")


def test_reading_model_exists():
    """Test Reading model can be imported."""
    assert Reading is not None


def test_reading_model_fields():
    """Test Reading model has required fields."""
    assert hasattr(Reading, "__tablename__")
    assert Reading.__tablename__ == "readings"

    assert hasattr(Reading, "id")
    assert hasattr(Reading, "source")
    assert hasattr(Reading, "region")
    assert hasattr(Reading, "rain_mm")
    assert hasattr(Reading, "timestamp")


def test_alert_model_exists():
    """Test Alert model can be imported."""
    assert Alert is not None


def test_alert_model_fields():
    """Test Alert model has required fields."""
    assert hasattr(Alert, "__tablename__")
    assert Alert.__tablename__ == "alerts"

    assert hasattr(Alert, "id")
    assert hasattr(Alert, "region")
    assert hasattr(Alert, "level")
    assert hasattr(Alert, "rain_mm")
    assert hasattr(Alert, "river")
    assert hasattr(Alert, "timestamp")


def test_user_model_exists():
    """Test User model can be imported."""
    assert User is not None


def test_user_model_fields():
    """Test User model has required fields."""
    assert hasattr(User, "__tablename__")
    assert User.__tablename__ == "users"

    assert hasattr(User, "id")
    assert hasattr(User, "telegram_id")
    assert hasattr(User, "nome")
    assert hasattr(User, "cidade")
    assert hasattr(User, "bairro")
    assert hasattr(User, "active")
