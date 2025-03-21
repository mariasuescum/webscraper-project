import time
from scraper import SauceLabsScraper
from database import Database
from utils import setup_logger, generate_report
import argparse
import os


# Configurar logger
logger = setup_logger('main')

def parse_arguments():
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description='Web Scraping para SauceLabs Demo')
    parser.add_argument('--headless', action='store_true', help='Ejecutar en modo headless')
    parser.add_argument('--report', choices=['text', 'csv'], default='text', help='Formato del reporte')
    parser.add_argument('--save', action='store_true', help='Guardar datos en la base de datos')
    parser.add_argument('--checkout', action='store_true', help='Realizar proceso de checkout')
    
    return parser.parse_args()

def main():
    """Función principal del programa"""
    # Parsear argumentos
    args = parse_arguments()
    
    logger.info("Iniciando proceso de web scraping")
    
    # Inicializar scraper y base de datos
    scraper = SauceLabsScraper()
    db = Database()
    
    try:
        # Iniciar driver y hacer login
        scraper.start_driver()
        scraper.login()
        
        # Extraer productos
        products = scraper.extract_products()
        logger.info(f"Se extrajeron {len(products)} productos")
        
        # Generar reporte
        report = generate_report(products, args.report)
        
        # Guardar reporte en archivo
        report_dir = 'reports'
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
            
        extension = 'txt' if args.report == 'text' else args.report
        report_path = f"{report_dir}/productos_{time.strftime('%Y%m%d_%H%M%S')}.{extension}"
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        logger.info(f"Reporte generado y guardado en {report_path}")
        
        # Guardar en base de datos si se solicita
        if args.save:
            # Conectar a la base de datos
            if db.connect():
                # Guardar productos
                db.save_products(products)
                logger.info("Productos guardados en la base de datos")
            else:
                logger.error("No se pudo conectar a la base de datos")
        
        # Realizar checkout si se solicita
        if args.checkout:
            # Elegir algunos productos para añadir al carrito
            products_to_add = [p["id"] for p in products[:2]]  # Añadir los primeros 2 productos
            
            if scraper.add_to_cart(products_to_add):
                # Información del cliente
                customer_info = {
                    "first_name": "Test",
                    "last_name": "User",
                    "postal_code": "12345"
                }
                
                # Realizar checkout
                checkout_result = scraper.checkout(customer_info)
                
                if checkout_result.get("status") == "completed":
                    logger.info("Checkout completado correctamente")
                    
                    # Guardar orden en base de datos si está conectada
                    if args.save and db.connection:
                        order_id = db.save_order(customer_info, products_to_add, checkout_result)
                        if order_id:
                            logger.info(f"Orden guardada con ID: {order_id}")
                else:
                    logger.error("El checkout no se completó correctamente")
            else:
                logger.error("No se pudieron añadir productos al carrito")
        
    except Exception as e:
        logger.error(f"Error en el proceso principal: {e}")
    finally:
        # Cerrar navegador y base de datos
        scraper.close()
        if args.save:
            db.close()
        
        logger.info("Proceso de web scraping finalizado")

if __name__ == "__main__":
    main()

