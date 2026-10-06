"""Tres pruebas independientes de login, catálogo y carrito en SauceDemo."""

import logging
import re
from urllib.parse import urlparse

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.saucedemo_utils import (
    TIEMPO_ESPERA,
    agregar_primer_producto,
    esperar_clickable,
    esperar_ruta,
    esperar_visible,
    obtener_datos_producto,
    obtener_primer_producto,
    realizar_login,
)

logger = logging.getLogger(__name__)


@pytest.mark.login
def test_login_exitoso(driver):
    """TC01: credenciales válidas redirigen al inventario de Swag Labs."""
    realizar_login(driver)

    assert urlparse(driver.current_url).path == "/inventory.html", "Ruta de inventario incorrecta."
    assert driver.title == "Swag Labs", "Título del navegador incorrecto."
    titulo = esperar_visible(driver, (By.CSS_SELECTOR, '[data-test="title"]'))
    assert titulo.text == "Products", "No se muestra el título Products."
    logo = esperar_visible(driver, (By.CLASS_NAME, "app_logo"))
    assert logo.text == "Swag Labs", "No se muestra la cabecera Swag Labs."
    logger.info("TC01: ruta, título y cabeceras del inventario correctos.")


@pytest.mark.catalogo
def test_catalogo_productos(driver):
    """TC02: catálogo visible, nombre/precio del primero y controles presentes."""
    realizar_login(driver)

    assert driver.title == "Swag Labs", "Título del navegador incorrecto."
    titulo = esperar_visible(driver, (By.CSS_SELECTOR, '[data-test="title"]'))
    assert titulo.text == "Products", "Título del catálogo incorrecto."

    producto = obtener_primer_producto(driver)
    assert producto.is_displayed(), "El primer producto no está visible."
    datos = obtener_datos_producto(producto)
    assert datos["nombre"].strip(), "El primer producto no tiene nombre."
    assert re.fullmatch(r"\$\d+\.\d{2}", datos["precio"]), "Precio vacío o con formato inesperado."
    logger.info("Primer producto: %s | Precio: %s", datos["nombre"], datos["precio"])

    menu = esperar_clickable(driver, (By.ID, "react-burger-menu-btn"))
    filtro = esperar_visible(driver, (By.CLASS_NAME, "product_sort_container"))
    carrito = esperar_clickable(driver, (By.CLASS_NAME, "shopping_cart_link"))
    assert menu.is_displayed(), "No se muestra el menú."
    assert filtro.is_enabled(), "El filtro está deshabilitado."
    assert filtro.find_elements(By.TAG_NAME, "option"), "El filtro no contiene opciones."
    assert carrito.is_displayed(), "No se muestra el acceso al carrito."
    logger.info("TC02: catálogo, menú, filtro y acceso al carrito disponibles.")


@pytest.mark.carrito
def test_agregar_producto_al_carrito(driver):
    """TC03: el primer producto incrementa el contador y aparece en el carrito."""
    realizar_login(driver)

    # Una sesión nueva debe comenzar sin contador: ningún producto agregado.
    assert not driver.find_elements(By.CLASS_NAME, "shopping_cart_badge"), "El carrito no comenzó vacío."
    producto_agregado = agregar_primer_producto(driver)
    localizador_contador = (By.CLASS_NAME, "shopping_cart_badge")
    esperar_visible(driver, localizador_contador)
    WebDriverWait(driver, TIEMPO_ESPERA).until(
        EC.text_to_be_present_in_element(localizador_contador, "1"),
        message="El contador no se actualizó después de agregar el producto.",
    )
    assert driver.find_element(*localizador_contador).text == "1", "El contador debe ser exactamente 1."

    esperar_clickable(driver, (By.CLASS_NAME, "shopping_cart_link")).click()
    esperar_ruta(driver, "/cart.html")
    assert urlparse(driver.current_url).path == "/cart.html", "No se abrió el carrito."
    titulo = esperar_visible(driver, (By.CSS_SELECTOR, '[data-test="title"]'))
    assert titulo.text == "Your Cart", "Título del carrito incorrecto."

    esperar_visible(driver, (By.CLASS_NAME, "cart_item"))
    productos_carrito = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(productos_carrito) == 1, "Debe haber exactamente un producto en el carrito."
    producto_carrito = productos_carrito[0]
    datos_carrito = obtener_datos_producto(producto_carrito)
    assert datos_carrito["nombre"] == producto_agregado["nombre"], "El producto del carrito no coincide."
    assert datos_carrito["precio"] == producto_agregado["precio"], "El precio del carrito no coincide."
    assert producto_carrito.find_element(By.CLASS_NAME, "cart_quantity").text == "1", "Cantidad incorrecta."
    logger.info("TC03: contador 1 y producto correcto en carrito: %s", datos_carrito)
