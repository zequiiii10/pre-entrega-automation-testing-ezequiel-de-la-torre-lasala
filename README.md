# Pre-entrega Automation Testing — SauceDemo

Proyecto del curso de automatización QA. Automatiza flujos básicos de
[SauceDemo](https://www.saucedemo.com/) mediante Python, Selenium WebDriver y
Pytest: inicio de sesión, verificación del catálogo y agregado de un producto
al carrito.

## Tecnologías y requisitos

- Python 3.10 o superior (validación del proyecto con Python 3.12).
- Google Chrome instalado y conexión a Internet.
- Selenium WebDriver 4.50.0.
- Pytest 9.1.1 y pytest-html 4.2.0.
- Git y GitHub para el control de versiones y la entrega.

Selenium Manager administra el ChromeDriver compatible. No se requiere
instalar `webdriver-manager` ni descargar el driver manualmente. La primera
ejecución puede demorar más mientras se descarga el driver.

## Estructura

| Ruta | Función |
| --- | --- |
| `tests/test_saucedemo.py` | Tres casos de prueba independientes. |
| `utils/saucedemo_utils.py` | Login, esperas explícitas y operaciones de productos. |
| `utils/__init__.py` | Identifica el paquete de funciones auxiliares. |
| `conftest.py` | Fixture de Chrome, opción headless y captura automática de fallos. |
| `pytest.ini` | Descubrimiento de tests, markers, logs y reporte HTML. |
| `requirements.txt` | Versiones de las dependencias principales. |
| `reports/reporte.html` | Resultados de la última ejecución completa. |
| `reports/ejecucion.log` | Registro de la última ejecución. |
| `reports/screenshots/` | Capturas PNG ante fallos, si los hubo. |
| `GUIA_PASO_A_PASO.md` | Instrucciones para preparar la PC y publicar en GitHub. |

No se utiliza una carpeta `datos/`: las credenciales públicas de práctica
están definidas en las funciones auxiliares y no se necesitan archivos externos.

## Instalación en Windows

Abrir una terminal **CMD** en la carpeta raíz del proyecto:

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

En PowerShell, activar con `.\.venv\Scripts\Activate.ps1`. También se puede
evitar la activación usando `.\.venv\Scripts\python.exe` en lugar de `python`.

En Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecución de las pruebas

Ejecutar desde la raíz del proyecto, donde se encuentra `pytest.ini`:

```bash
python -m pytest
```

La configuración genera automáticamente un reporte HTML autocontenido y un
log. El comando equivalente con las opciones expresas es:

```bash
python -m pytest tests/test_saucedemo.py -v --html=reports/reporte.html --self-contained-html
```

Para ejecutar sin mostrar la ventana del navegador:

```bash
python -m pytest --headless
```

Para comprobar la independencia ejecutando un único caso:

```bash
python -m pytest tests/test_saucedemo.py::test_agregar_producto_al_carrito
```

También se puede filtrar por marker:

```bash
python -m pytest -m login
python -m pytest -m catalogo
python -m pytest -m carrito
```

Cada ejecución sobrescribe `reporte.html` y `ejecucion.log`. Antes de entregar,
ejecutar la suite completa para que las evidencias incluyan los tres casos.

## Casos de prueba

| ID | Caso | Validaciones |
| --- | --- | --- |
| TC01 | Login exitoso | Credenciales válidas; ruta `/inventory.html`; título `Swag Labs`; cabeceras `Products` y `Swag Labs`. |
| TC02 | Catálogo de productos | Título correcto; producto visible; nombre no vacío y precio con formato monetario; registro del nombre/precio del primero; menú, filtro con opciones y acceso al carrito presentes. |
| TC03 | Agregar producto al carrito | Carrito inicialmente vacío; agregado del primer producto; contador exactamente 1; ruta `/cart.html`; producto con el mismo nombre/precio; cantidad 1. |

Las credenciales públicas utilizadas son `standard_user` y `secret_sauce`.

## Organización y sincronización

El fixture `driver` tiene alcance de función: crea una sesión nueva de Chrome
para cada caso y cierra el navegador al terminar, incluso ante fallos. Cada
test inicia sesión por su cuenta, sin depender del resultado de otro.

Las esperas explícitas usan `WebDriverWait` y condiciones de visibilidad,
elementos habilitados, cambio de ruta y actualización del contador. No se
utiliza `time.sleep()` ni se mezclan esperas implícitas y explícitas.

Los localizadores utilizan IDs, clases y atributos `data-test`. Los elementos
del producto se buscan dentro de su contenedor para asociar correctamente
nombre, precio y botón.

## Reportes y evidencias

- Abrir `reports/reporte.html` con el navegador para consultar los resultados.
- Revisar `reports/ejecucion.log` para ver los pasos, el primer nombre/precio y
  los resultados de los tests.
- Si un test falla durante su preparación o ejecución y el navegador está
  disponible, se guarda un PNG en `reports/screenshots/` y se incorpora su
  imagen al reporte HTML. El nombre contiene el caso y la fecha/hora.
- Si Chrome no llega a abrirse, no puede generarse una captura; el error queda
  registrado en el resultado de Pytest. Tampoco se captura un fallo posterior
  al cierre del navegador.
- Las capturas de diferentes ejecuciones se conservan. Si todos los tests
  pasan, no se esperan capturas nuevas.

Los reportes, logs y capturas se incluyen en Git porque forman parte de la
consigna. El entorno virtual y las cachés se excluyen mediante `.gitignore`.

## Entrega

Publicar el código en un repositorio público llamado:

`pre-entrega-automation-testing-ezequiel-de-la-torre-lasala`

Incluir el reporte y el log generados con la suite completa. Compartir el
enlace del repositorio en el espacio de entrega del curso. La guía adjunta
explica cómo crear los commits y subirlo.

## Referencias

- [Esperas explícitas de Selenium](https://www.selenium.dev/documentation/webdriver/waits/).
- [Selenium Manager](https://www.selenium.dev/documentation/selenium_manager/).
- [Reportes y extras de pytest-html](https://pytest-html.readthedocs.io/en/latest/user_guide.html).
- [Logs de Pytest](https://docs.pytest.org/en/stable/how-to/logging.html).

## Autor

Ezequiel de la Torre Lasala.
