# webscraper-project
# 🚀 Automatización con Selenium - Demo SauceDemo

## 📌 Descripción
Este proyecto automatiza el proceso de inicio de sesión, selección de productos y pago en el sitio web [SauceDemo](https://www.saucedemo.com/). Se utiliza **Selenium** para interactuar con la interfaz del usuario y extraer información sobre los productos disponibles.

---

## 🛠 Tecnologías y herramientas
- **Python**
- **Selenium**
- **WebDriver Manager**
- **Google Chrome**

---

## 📥 Instalación
Antes de ejecutar el script, asegúrate de tener **Python** instalado en tu sistema.

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```
2. Crear y activar un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Mac/Linux
   venv\Scripts\activate     # En Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuración
Este script utiliza credenciales de prueba predefinidas. Si deseas modificar las credenciales, edita las siguientes variables en el archivo `main.py`:

```python
USER = "standard_user"
PASSWORD = "secret_sauce"
```

---

## ▶️ Ejecución
Para ejecutar el script, simplemente corre:
```bash
python main.py
```
Esto abrirá un navegador, iniciará sesión en SauceDemo, extraerá información de los productos y completará el proceso de compra.

---

## 🔧 Posibles mejoras futuras
- Implementar pruebas automatizadas con **pytest**.
- Añadir soporte para otros navegadores como Firefox.
- Manejo de credenciales con variables de entorno.
- Generación de reportes de ejecución automatizados.

---

##  🏆 Gestión del proyecto con Scrum y Trello

Se ha desarrollado siguiendo la metodología ágil Scrum, organizando tareas  y priorizando funcionalidades en un tablero de Trello. Esto nos ha permitido mejorar la productividad y la planificación del proyecto de manera eficiente.

puedes revisar nuestro tablero de Trello en el siguiente enlace: [Enlace a Trello.](https://trello.com/b/lULZYm1B/scrapingproject). 

## 📄 Licencia
Este proyecto está bajo la licencia MIT.

---

### ✨ Autor
**Andreina** 🚀

