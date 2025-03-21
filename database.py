import mysql.connector
from config import DB_CONFIG
import logging
from utils import setup_logger

# Configurar logger
logger = setup_logger('database')

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establece conexión con la base de datos MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=DB_CONFIG["host"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"]
            )
            self.cursor = self.connection.cursor()
            logger.info("Conexión a MySQL establecida")
            
            # Crear base de datos si no existe
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            self.cursor.execute(f"USE {DB_CONFIG['database']}")
            logger.info(f"Base de datos {DB_CONFIG['database']} seleccionada")
            
            # Crear tablas necesarias
            self._create_tables()
            
            return True
        except Exception as e:
            logger.error(f"Error al conectar con la base de datos: {e}")
            return False
    
    def _create_tables(self):
        """Crea las tablas necesarias en la base de datos"""
        try:
            # Tabla de productos
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id VARCHAR(100) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    price DECIMAL(10, 2) NOT NULL,
                    img_url TEXT,
                    date_scraped TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de órdenes/compras
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    postal_code VARCHAR(20),
                    total DECIMAL(10, 2),
                    status VARCHAR(50),
                    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de relación entre órdenes y productos
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_products (
                    order_id INT,
                    product_id VARCHAR(100),
                    PRIMARY KEY (order_id, product_id),
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            ''')
            
            self.connection.commit()
            logger.info("Tablas creadas correctamente")
        except Exception as e:
            logger.error(f"Error al crear tablas: {e}")
            raise
    
    def save_products(self, products):
        """Guarda los productos extraídos en la base de datos"""
        try:
            for product in products:
                # Verificar si el producto ya existe
                self.cursor.execute(
                    "SELECT id FROM products WHERE id = %s",
                    (product["id"],)
                )
                result = self.cursor.fetchone()
                
                if result:
                    # Actualizar producto existente
                    self.cursor.execute(
                        """
                        UPDATE products 
                        SET name = %s, description = %s, price = %s, img_url = %s
                        WHERE id = %s
                        """,
                        (
                            product["name"],
                            product["description"],
                            product["price"],
                            product["img_url"],
                            product["id"]
                        )
                    )
                    logger.info(f"Producto {product['id']} actualizado")
                else:
                    # Insertar nuevo producto
                    self.cursor.execute(
                        """
                        INSERT INTO products (id, name, description, price, img_url)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            product["id"],
                            product["name"],
                            product["description"],
                            product["price"],
                            product["img_url"]
                        )
                    )
                    logger.info(f"Producto {product['id']} insertado")
            
            self.connection.commit()
            logger.info(f"Se guardaron {len(products)} productos en la base de datos")
            return True
        except Exception as e:
            logger.error(f"Error al guardar productos: {e}")
            self.connection.rollback()
            return False
    
    def save_order(self, customer_info, product_ids, checkout_info):
        """Guarda la información de una orden en la base de datos"""
        try:
            # Extraer el total como número
            total = checkout_info.get("total", "0").replace("Total: $", "")
            
            # Insertar orden
            self.cursor.execute(
                """
                INSERT INTO orders (first_name, last_name, postal_code, total, status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    customer_info["first_name"],
                    customer_info["last_name"],
                    customer_info["postal_code"],
                    float(total),
                    checkout_info.get("status", "unknown")
                )
            )
            
            # Obtener ID de la orden insertada
            order_id = self.cursor.lastrowid
            
            # Insertar relaciones entre orden y productos
            for product_id in product_ids:
                self.cursor.execute(
                    """
                    INSERT INTO order_products (order_id, product_id)
                    VALUES (%s, %s)
                    """,
                    (order_id, product_id)
                )
            
            self.connection.commit()
            logger.info(f"Orden {order_id} guardada correctamente")
            return order_id
        except Exception as e:
            logger.error(f"Error al guardar orden: {e}")
            self.connection.rollback()
            return None
    
    def get_all_products(self):
        """Obtiene todos los productos de la base de datos"""
        try:
            self.cursor.execute("SELECT * FROM products")
            products = self.cursor.fetchall()
            
            # Convertir a lista de diccionarios
            columns = [col[0] for col in self.cursor.description]
            product_list = []
            
            for product in products:
                product_dict = dict(zip(columns, product))
                product_list.append(product_dict)
            
            return product_list
        except Exception as e:
            logger.error(f"Error al obtener productos: {e}")
            return []
    
    def close(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            logger.info("Conexión a la base de datos cerrada")
