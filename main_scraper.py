import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales del archivo .env
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

def main():
    # Configuración del driver
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    options.add_argument("--window-size=1440")

    # Inicializar Chrome correctamente
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.saucedemo.com/")

    # LOGIN 
    driver.find_element(By.ID, "user-name").send_keys(USER)
    driver.find_element(By.ID, 'password').send_keys(PASSWORD)

    driver.find_element(By.ID, 'login-button').click()
    time.sleep(2)

    # EXTRAER PRODUCTOS Y PRECIOS
    print("\n📌 Productos disponibles en la tienda:")
    products = driver.find_elements(By.CLASS_NAME, "inventory_item")

    for product in products:
        name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
        price = product.find_element(By.CLASS_NAME, "inventory_item_price").text
        print(f"{name}: {price}")

    time.sleep(2)

    # COMPRAS 
    driver.find_element(By.ID, 'add-to-cart-sauce-labs-bolt-t-shirt').click()
    driver.find_element(By.ID, 'add-to-cart-test.allthethings()-t-shirt-(red)').click()
    time.sleep(2)

    # CARRITO
    driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[1]/div[3]/a').click()
    driver.find_element(By.ID, 'checkout').click()
    time.sleep(2)

    # PAGAR
    driver.find_element(By.ID, 'first-name').send_keys('Test')
    driver.find_element(By.ID, 'last-name').send_keys('Test')
    driver.find_element(By.ID, 'postal-code').send_keys('12345')
    time.sleep(2)
    driver.find_element(By.ID, 'continue').click()
    time.sleep(4)

    driver.find_element(By.ID, 'finish').click()
    time.sleep(10)

    # Cerrar el navegador
    driver.quit()



if __name__ == "__main__":
    main()