import pytest
from scraper import SauceLabsScraper
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import SauceLabsScraper  

@pytest.fixture
def scraper():
    scraper = SauceLabsScraper()
    scraper.start_driver()
    yield scraper
    scraper.close()

def test_login(scraper):
    """Prueba que el login se realice correctamente"""
    try:
        scraper.login()
        assert "inventory.html" in scraper.driver.current_url
    except Exception as e:
        pytest.fail(f"Error en login: {e}")

def test_extract_products(scraper):
    """Prueba la extracción de productos"""
    scraper.login()
    products = scraper.extract_products()
    assert isinstance(products, list)
    assert len(products) > 0
    assert "id" in products[0]
