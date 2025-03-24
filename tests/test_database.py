import pytest
from database import Database

@pytest.fixture
def db():
    database = Database()
    database.connect()
    yield database
    database.close()

def test_connection(db):
    """Prueba la conexión a la base de datos"""
    assert db.connection is not None
    assert db.cursor is not None

def test_save_products(db):
    """Prueba que los productos se guarden correctamente"""
    sample_product = [{
        "id": "test123",
        "name": "Producto Test",
        "description": "Descripción de prueba",
        "price": 9.99,
        "img_url": "http://example.com/image.jpg"
    }]
    result = db.save_products(sample_product)
    assert result is True
