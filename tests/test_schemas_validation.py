import pytest
from pydantic import ValidationError

from app.schemas.alert import AlertCreate, AlertSchema
from app.schemas.region import RegionCreate, RegionSchema
from app.schemas.user import UserCreate, UserSchema


def test_alert_schema_requires_region():
    """Test AlertSchema requires region field."""
    with pytest.raises(ValidationError):
        AlertSchema(level='RED', timestamp='2026-01-01T00:00:00')


def test_alert_schema_requires_level():
    """Test AlertSchema requires level field."""
    with pytest.raises(ValidationError):
        AlertSchema(region='Recife', timestamp='2026-01-01T00:00:00')


def test_alert_create_optional_timestamp():
    """Test AlertCreate allows omitting timestamp."""
    alert = AlertCreate(region='Recife', level='YELLOW')
    assert alert.region == 'Recife'
    assert alert.level == 'YELLOW'


def test_region_schema_requires_nome():
    """Test RegionSchema requires nome."""
    with pytest.raises(ValidationError):
        RegionSchema(geom='POINT(0 0)')


GREEN_DEFAULT = 30.0
YELLOW_DEFAULT = 50.0
ORANGE_DEFAULT = 100.0
RED_DEFAULT = 150.0


def test_region_create_default_thresholds():
    """Test RegionCreate applies default thresholds."""
    region = RegionCreate(nome='Test', geom='POINT(0 0)')
    assert region.threshold_green == GREEN_DEFAULT
    assert region.threshold_yellow == YELLOW_DEFAULT
    assert region.threshold_orange == ORANGE_DEFAULT
    assert region.threshold_red == RED_DEFAULT


def test_user_schema_requires_telegram_id():
    """Test UserSchema requires telegram_id."""
    with pytest.raises(ValidationError):
        UserSchema(nome='Test', cidade='Recife')


def test_user_create_optional_bairro():
    """Test UserCreate allows omitting bairro."""
    user = UserCreate(telegram_id=123, nome='Test', cidade='Recife')
    assert user.bairro is None


def test_user_schema_default_active():
    """Test UserSchema default active is True."""
    user = UserSchema(id=1, telegram_id=123, nome='Test', cidade='Recife')
    assert user.active is True
