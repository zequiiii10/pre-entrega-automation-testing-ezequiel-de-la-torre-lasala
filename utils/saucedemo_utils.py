"""Operaciones reutilizables con esperas explícitas y localizadores estables."""

import logging
from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL_BASE = "https://www.saucedemo.com/"
USUARIO_VALIDO = "standard_user"
CONTRASENA_VALIDA = "secret_sauce"  # Credencial pública del sitio de práctica.
TIEMPO_ESPERA = 10
logger = logging.getLogger(__name__)


def esperar_visible(driver, localizador):
    """Espera hasta que el elemento esté visible, como máximo 10 segundos."""
    return WebDriverWait(driver, TIEMPO_ESPERA).until(
        EC.visibility_of_element_located(localizador),
        message=f"No se encontró un elemento visible: {localizador}",
    )


def esperar_clickable(driver, localizador):
    """Espera hasta que el elemento esté visible y habilitado para hacer clic."""
    return WebDriverWait(driver, TIEMPO_ESPERA).until(
        EC.element_to_be_clickable(localizador),
        message=f"El elemento no está disponible para hacer clic: {localizador}",
    )


def esperar_ruta(driver, ruta):
    """Espera la ruta exacta, sin confundirla con parámetros de la URL."""
    WebDriverWait(driver, TIEMPO_ESPERA).until(
        lambda navegador: urlparse(navegador.current_url).path == ruta,
        message=f"No se llegó a {ruta}. Revisar la redirección o el login.",
    )


def realizar_login(driver, usuario=USUARIO_VALIDO, contrasena=CONTRASENA_VALIDA):
    """Abre el sitio e inicia sesión. Cada test realiza su propio login."""
    logger.info("Abrir SauceDemo e iniciar sesión con %s", usuario)
    driver.get(URL_BASE)
    campo_usuario = esperar_visible(driver, (By.ID, "user-name"))
    campo_contrasena = esperar_visible(driver, (By.ID, "password"))
    campo_usuario.clear()
    campo_usuario.send_keys(usuario)
    campo_contrasena.clear()
    campo_contrasena.send_keys(contrasena)
    esperar_clickable(driver, (By.ID, "login-button")).click()
    esperar_ruta(driver, "/inventory.html")
    esperar_visible(driver, (By.CSS_SELECTOR, '[data-test="title"]'))
    logger.info("Login realizado. URL actual: %s", driver.current_url)


def obtener_primer_producto(driver):
    """Devuelve el primer producto visible para consultar datos o interactuar."""
    productos = WebDriverWait(driver, TIEMPO_ESPERA).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "inventory_item")),
        message="No hay productos visibles en el inventario.",
    )
    return productos[0]


def obtener_datos_producto(producto):
    """Obtiene el nombre y el precio dentro del producto seleccionado."""
    return {
        "nombre": producto.find_element(By.CLASS_NAME, "inventory_item_name").text,
        "precio": producto.find_element(By.CLASS_NAME, "inventory_item_price").text,
    }


def agregar_primer_producto(driver):
    """Guarda los datos del primer producto y lo agrega al carrito."""
    producto = obtener_primer_producto(driver)
    datos = obtener_datos_producto(producto)
    boton = WebDriverWait(driver, TIEMPO_ESPERA).until(
        EC.element_to_be_clickable(producto.find_element(By.TAG_NAME, "button"))
    )
    assert boton.text == "Add to cart", "El primer producto ya estaba agregado."
    boton.click()
    logger.info("Producto agregado: %s | Precio: %s", datos["nombre"], datos["precio"])
    return datos
