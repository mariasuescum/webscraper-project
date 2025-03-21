# utils.py - Funciones de utilidad
import logging
import os
from datetime import datetime

def setup_logger(name):
    """Configura y devuelve un logger personalizado"""
    # Crear directorio de logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evitar duplicación de handlers
    if not logger.handlers:
        # Crear formato
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Handler para archivo
        file_handler = logging.FileHandler(f'logs/{name}_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        
        # Agregar handlers al logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

def generate_report(products, format='text'):
    """Genera un reporte con los productos extraídos"""
    if format == 'text':
        report = "=== REPORTE DE PRODUCTOS ===\n\n"
        for product in products:
            report += f"ID: {product['id']}\n"
            report += f"Nombre: {product['name']}\n"
            report += f"Descripción: {product['description']}\n"
            report += f"Precio: ${product['price']}\n"
            report += f"URL de imagen: {product['img_url']}\n"
            report += "----------------------------\n"
        
        return report
    elif format == 'csv':
        import csv
        import io
        
        output = io.StringIO()
        fieldnames = ['id', 'name', 'description', 'price', 'img_url']
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for product in products:
            writer.writerow(product)
        
        return output.getvalue()
    else:
        return "Formato no soportado"