# Estado de la verificación del proyecto

## Qué se verificó

- Se instalaron las versiones indicadas en `requirements.txt`.
- `pip check` no detectó incompatibilidades de dependencias.
- Pytest importó y descubrió los tres casos de SauceDemo.
- Se confirmaron los IDs del formulario real de login: `user-name`, `password`
  y `login-button`.
- Una comprobación técnica separada, con un navegador simulado, confirmó que
  un fallo genera un PNG, que el HTML incorpora su imagen y que el fixture
  crea sesiones distintas y cierra ambas, incluso tras el fallo.

La comprobación con navegador simulado verifica el mecanismo de evidencias;
no demuestra que los flujos de SauceDemo hayan pasado. Sus archivos
temporales no forman parte de la entrega.

## Resultado del reporte adjunto

Se intentó ejecutar la suite con Python 3.12.14, Chrome for Testing
154.0.8037.92, Selenium 4.50.0, Pytest 9.1.1 y pytest-html 4.2.0 en Linux.
Para ese intento se adaptaron únicamente la ruta del navegador/driver y las
opciones de inicio requeridas por este entorno; el código de los tests se
mantuvo igual.

**Resultado: 3 errores de preparación del navegador.** Chrome no pudo abrirse
por una restricción del entorno al crear un socket. Selenium informó
`SessionNotCreatedException`. Ninguno de los tres flujos llegó a ejecutarse.

`reporte.html` y `ejecucion.log` documentan ese intento real. No constituyen una
validación funcional aprobada ni el reporte final para entregar al curso. No
hay capturas reales porque el navegador no llegó a estar disponible.

## Verificación pendiente en la PC del autor

Desde la raíz del proyecto, con las dependencias instaladas y Google Chrome
disponible:

```bash
python -m pytest
```

Confirmar **3 passed**. Esa ejecución reemplaza el reporte y el log adjuntos.
Antes de entregar, revisar los archivos generados y agregar aquí la fecha, el
resultado y el entorno de tu verificación local. Si hay fallos, conservarlos
para diagnosticar y corregir; no editar el HTML para cambiar resultados.

También se puede verificar un test aislado:

```bash
python -m pytest tests/test_saucedemo.py::test_agregar_producto_al_carrito
```

Después del test aislado, volver a ejecutar la suite completa para que el
reporte final incluya los tres casos.
