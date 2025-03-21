from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CREDENTIALS, URLS
import time
import logging
from utils import setup_logger

# Configurar logger
logger = setup_logger('scraper')

class SauceLabsScraper:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--window-size=1440")
        self.options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
        self.service = Service(ChromeDriverManager().install())
        self.driver = None
        self.products = []
    
    def start_driver(self):
        """Inicializa el driver de Chrome"""
        try:
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
            logger.info("Driver de Chrome iniciado correctamente")
        except Exception as e:
            logger.error(f"Error al iniciar el driver: {e}")
            raise
    
    def login(self):
        """Realiza el login en el sitio web"""
        try:
            self.driver.get(URLS["base_url"])
            
            # Esperar a que los elementos estén disponibles
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "user-name"))
            )
            
            # Completar credenciales
            self.driver.find_element(By.ID, "user-name").send_keys(CREDENTIALS["user"])
            self.driver.find_element(By.ID, "password").send_keys(CREDENTIALS["password"])
            self.driver.find_element(By.ID, "login-button").click()
            
            # Verificar login exitoso
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
            )
            logger.info("Login exitoso")
        except Exception as e:
            logger.error(f"Error durante el login: {e}")
            raise
    
    def extract_products(self):
        """Extrae información de los productos"""
        try:
            # Esperar a que los productos se carguen
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
            )
            
            # Obtener todos los productos
            product_elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
            logger.info(f"Se encontraron {len(product_elements)} productos")
            
            # Extraer información de cada producto
            for product in product_elements:
                try:
                    product_id = product.find_element(By.CLASS_NAME, "inventory_item_description").find_element(By.CSS_SELECTOR, "button").get_attribute("id")
                    # Extraer el ID limpio del formato "add-to-cart-{id}"
                    product_id = product_id.replace("add-to-cart-", "")
                    
                    name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
                    description = product.find_element(By.CLASS_NAME, "inventory_item_desc").text
                    price = product.find_element(By.CLASS_NAME, "inventory_item_price").text.replace("$", "")
                    
                    # Obtener URL de la imagen
                    img_element = product.find_element(By.CLASS_NAME, "inventory_item_img").find_element(By.TAG_NAME, "img")
                    img_url = img_element.get_attribute("src")
                    
                    # Crear diccionario con la información del producto
                    product_info = {
                        "id": product_id,
                        "name": name,
                        "description": description,
                        "price": float(price),
                        "img_url": img_url
                    }
                    
                    self.products.append(product_info)
                    
                except Exception as e:
                    logger.warning(f"Error al extraer información de un producto: {e}")
                    continue
            
            logger.info(f"Se extrajeron datos de {len(self.products)} productos correctamente")
            return self.products
            
        except Exception as e:
            logger.error(f"Error durante la extracción de productos: {e}")
            raise
    
    def add_to_cart(self, product_ids):
        """Añade productos al carrito"""
        try:
            for product_id in product_ids:
                self.driver.find_element(By.ID, f"add-to-cart-{product_id}").click()
                logger.info(f"Producto {product_id} añadido al carrito")
            
            return True
        except Exception as e:
            logger.error(f"Error al añadir productos al carrito: {e}")
            return False
    
    def checkout(self, customer_info):
        """Realiza el proceso de checkout"""
        try:
            # Ir al carrito
            self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
            
            # Checkout
            self.driver.find_element(By.ID, "checkout").click()
            
            # Completar información del cliente
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "first-name"))
            )
            
            self.driver.find_element(By.ID, "first-name").send_keys(customer_info["first_name"])
            self.driver.find_element(By.ID, "last-name").send_keys(customer_info["last_name"])
            self.driver.find_element(By.ID, "postal-code").send_keys(customer_info["postal_code"])
            
            self.driver.find_element(By.ID, "continue").click()
            
            # Finalizar compra
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "finish"))
            )
            
            # Extraer información del resumen de compra
            total = self.driver.find_element(By.CLASS_NAME, "summary_total_label").text
            
            self.driver.find_element(By.ID, "finish").click()
            
            # Verificar compra exitosa
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
            )
            
            confirmation_message = self.driver.find_element(By.CLASS_NAME, "complete-header").text
            
            checkout_info = {
                "total": total,
                "confirmation": confirmation_message,
                "status": "completed"
            }
            
            logger.info(f"Checkout completado: {confirmation_message}")
            return checkout_info
            
        except Exception as e:
            logger.error(f"Error durante el checkout: {e}")
            return {"status": "failed", "error": str(e)}
    
    def close(self):
        """Cierra el navegador"""
        if self.driver:
            self.driver.quit()
            logger.info("Driver cerrado correctamente")