# Verificación del proyecto

## Ejecución funcional

- **Fecha:** 06/10/2026, de 01:00 a 01:01 (Argentina, UTC-3).
- **Sistema operativo:** Windows 11.
- **Python:** 3.13.15.
- **Selenium:** 4.50.0.
- **Pytest:** 9.1.1.
- **pytest-html:** 4.2.0.
- **Navegador:** Google Chrome.
- **Sitio:** https://www.saucedemo.com/.
- **Resultado:** 3 pruebas aprobadas en 27,59 segundos.

Comando ejecutado desde PowerShell, sin activar el entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Casos verificados

| Caso | Resultado | Validaciones |
| --- | --- | --- |
| Login exitoso | Aprobado | Credenciales válidas, ruta `/inventory.html`, título y cabeceras del inventario. |
| Catálogo de productos | Aprobado | Producto visible, nombre y precio del primero, menú, filtro y acceso al carrito. |
| Agregar producto al carrito | Aprobado | Carrito inicialmente vacío, contador 1, producto con nombre y precio coincidentes y cantidad 1. |

El primer producto fue **Sauce Labs Backpack**, con precio **$29.99**.
Los logs registran una sesión nueva y el cierre del navegador para cada caso.

## Evidencias

- `reporte.html`: reporte HTML de los tres casos aprobados.
- `ejecucion.log`: registro de la misma ejecución.
- `screenshots/`: carpeta destinada a capturas automáticas ante fallos. La
  ejecución funcional aprobada no produjo capturas de error.

El mecanismo de capturas se comprobó por separado con un navegador simulado:
se verificaron la generación del PNG, la incorporación de la imagen al HTML
y el cierre del navegador tras el fallo. Esa comprobación técnica no forma
parte de los tres casos funcionales ni de su reporte.

Selenium Manager emitió una advertencia al enviar estadísticas a Plausible.
La advertencia no impidió abrir Chrome ni ejecutar los tres tests.

## Estado

La ejecución funcional en Windows fue satisfactoria. El reporte y el log
publicados corresponden a esa ejecución y reemplazan las evidencias del
intento inicial realizado en otro entorno.
