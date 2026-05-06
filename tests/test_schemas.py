from app.schemas.alert import AlertCreate, AlertSchema
from app.schemas.region import RegionCreate, RegionSchema
from app.schemas.user import UserCreate, UserSchema

ALERT_RAIN_MM = 87.5


def test_alert_schema_creation():
    """Test AlertSchema can be created with valid data."""
    alert = AlertSchema(
        id=1,
        region='Recife',
        level='RED',
        rain_mm=ALERT_RAIN_MM,
        river='Rio Capibaribe',
        river_level_m=4.2,
        sources=['CEMADEN', 'APAC'],
        timestamp='2026-05-06T14:00:00-03:00',
    )
    assert alert.region == 'Recife'
    assert alert.level == 'RED'
    assert alert.rain_mm == ALERT_RAIN_MM


def test_alert_create_schema():
    """Test AlertCreate schema for API input."""
    alert_create = AlertCreate(
        region='Jaboatão dos Guararapes',
        level='ORANGE',
        rain_mm=65.0,
        river='Rio Jaboatão',
        river_level_m=3.1,
        sources=['CEMADEN'],
    )
    assert alert_create.region == 'Jaboatão dos Guararapes'
    assert alert_create.level == 'ORANGE'


USER_TELEGRAM_ID = 123456789


def test_user_schema_creation():
    """Test UserSchema can be created with valid data."""
    user = UserSchema(
        id=1,
        telegram_id=USER_TELEGRAM_ID,
        nome='Alison',
        cidade='Recife',
        bairro='Boa Viagem',
        active=True,
    )
    assert user.telegram_id == USER_TELEGRAM_ID
    assert user.cidade == 'Recife'
    assert user.bairro == 'Boa Viagem'


def test_user_create_schema():
    """Test UserCreate schema for registration."""
    user_create = UserCreate(
        telegram_id=987654321,
        nome='Maria',
        cidade='Olinda',
        bairro='Casa Forte',
    )
    assert user_create.cidade == 'Olinda'
    assert user_create.bairro == 'Casa Forte'


THRESHOLD_GREEN = 30.0

GEOM_RECIFE = (
    "SRID=4326;"
    "POLYGON((-34.9 -8.1, -34.8 -8.1, -34.8 -8.0, -34.9 -8.0, -34.9 -8.1))"
)

GEOM_JABOAO = (
    "SRID=4326;"
    "POLYGON((-34.9 -8.1, -34.8 -8.1, -34.8 -8.0, -34.9 -8.0, -34.9 -8.1))"
)


def test_region_schema_creation():
    """Test RegionSchema can be created with valid data."""
    region = RegionSchema(
        id=1,
        nome="Recife",
        geom=GEOM_RECIFE,
        threshold_green=THRESHOLD_GREEN,
        threshold_yellow=50.0,
        threshold_orange=100.0,
        threshold_red=150.0,
    )
    assert region.nome == "Recife"
    assert region.threshold_green == THRESHOLD_GREEN


def test_region_create_schema():
    """Test RegionCreate schema for API input."""
    region_create = RegionCreate(
        nome='Jaboatão dos Guararapes',
        geom=GEOM_JABOAO,
        threshold_green=THRESHOLD_GREEN,
        threshold_yellow=50.0,
        threshold_orange=100.0,
        threshold_red=150.0,
    )
    assert region_create.nome == 'Jaboatão dos Guararapes'
