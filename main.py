import time
from scraper import SauceLabsScraper
from database import Database
from utils import setup_logger, generate_report
import argparse
import os


# Set up logger
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
    
    # Initialize scraper and database
    scraper = SauceLabsScraper()
    db = Database()
    
    try:
        # Start driver and log in
        scraper.start_driver()
        scraper.login()
        
        # Extract products
        products = scraper.extract_products()
        logger.info(f"Se extrajeron {len(products)} productos")
        
        # Generate report
        report = generate_report(products, args.report)
        
        # Save report to file
        report_dir = 'reports'
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
            
        extension = 'txt' if args.report == 'text' else args.report
        report_path = f"{report_dir}/productos_{time.strftime('%Y%m%d_%H%M%S')}.{extension}"
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        logger.info(f"Reporte generado y guardado en {report_path}")
        
        # Save to database if requested
        if args.save:
            # Connect to the database
            if db.connect():
                # Save products
                db.save_products(products)
                logger.info("Productos guardados en la base de datos")
            else:
                logger.error("No se pudo conectar a la base de datos")
        
        # Perform checkout if requested
        if args.checkout:
            # Select some products to add to the cart
            products_to_add = [p["id"] for p in products[:2]]  # Add the first 2 products
            
            if scraper.add_to_cart(products_to_add):
                # Customer information
                customer_info = {
                    "first_name": "Test",
                    "last_name": "User",
                    "postal_code": "12345"
                }
                
                # Perform checkout
                checkout_result = scraper.checkout(customer_info)
                
                if checkout_result.get("status") == "completed":
                    logger.info("Checkout completado correctamente")
                    
                    # Save order to the database if connected
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
        # Close browser and database
        scraper.close()
        if args.save:
            db.close()
        
        logger.info("Proceso de web scraping finalizado")

if __name__ == "__main__":
    main()

