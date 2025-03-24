from utils import setup_logger
import os

def test_setup_logger():
    """Prueba la creación del logger"""
    logger = setup_logger("test_logger")
    assert logger is not None
    assert os.path.exists("logs")
