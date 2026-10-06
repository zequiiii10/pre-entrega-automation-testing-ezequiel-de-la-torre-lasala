"""Navegador independiente por test y evidencias automáticas ante fallos."""

import base64
import logging
import re
from datetime import datetime

import pytest
import pytest_html
from selenium import webdriver

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False,
        help="Ejecuta Chrome sin mostrar su ventana.",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Crea las carpetas antes de que se escriban logs, reportes y capturas."""
    (config.rootpath / "reports" / "screenshots").mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="function")
def driver(request):
    """Crea una sesión nueva de Chrome y la cierra incluso si falla el test."""
    opciones = webdriver.ChromeOptions()
    opciones.add_argument("--window-size=1440,1000")
    opciones.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    if request.config.getoption("--headless"):
        opciones.add_argument("--headless=new")

    # Selenium Manager resuelve el driver sin instalar webdriver-manager.
    navegador = webdriver.Chrome(options=opciones)
    try:
        navegador.set_page_load_timeout(30)
        logger.info("Navegador nuevo para %s", request.node.name)
        yield navegador
    finally:
        navegador.quit()
        logger.info("Navegador cerrado para %s", request.node.name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura fallos de setup/call mientras el navegador sigue disponible."""
    resultado = yield
    reporte = resultado.get_result()
    if reporte.when == "call" or reporte.failed:
        logger.info("Resultado de %s (%s): %s", item.name, reporte.when, reporte.outcome)
    if not reporte.failed or reporte.when not in ("setup", "call"):
        return

    navegador = item.funcargs.get("driver")
    if navegador is None:
        logger.error("No hay navegador disponible para capturar el fallo de %s", item.name)
        return

    # Se usan nombres únicos para conservar capturas de distintas ejecuciones.
    nombre_seguro = re.sub(r"[^a-zA-Z0-9_-]", "_", item.nodeid)
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    ruta = item.config.rootpath / "reports" / "screenshots" / f"{nombre_seguro}_{fecha}.png"
    try:
        captura = navegador.get_screenshot_as_png()
        ruta.write_bytes(captura)
        extras = getattr(reporte, "extras", [])
        # Base64 permite visualizar la captura dentro del HTML autocontenido.
        extras.append(pytest_html.extras.png(
            base64.b64encode(captura).decode("ascii"), name="Captura del fallo",
        ))
        extras.append(pytest_html.extras.url(navegador.current_url, name="URL del fallo"))
        reporte.extras = extras
        logger.error("Captura guardada: %s", ruta)
    except Exception:
        # El error de la captura no debe reemplazar el error original del test.
        logger.exception("No se pudo completar la evidencia de %s", item.name)
