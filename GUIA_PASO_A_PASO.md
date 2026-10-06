# Guía para ejecutar y entregar el proyecto

## 1. Preparar la carpeta

1. Descargar y extraer el ZIP. No trabajar dentro del archivo comprimido.
2. Abrir en VS Code la carpeta `pre-entrega-automation-testing-ezequiel-de-la-torre-lasala`.
3. Confirmar que `README.md`, `pytest.ini` y `conftest.py` estén en la raíz.
4. Tener Python 3.10 o superior, Google Chrome y Git instalados.

## 2. Abrir una terminal CMD en VS Code

En **Terminal → Nueva terminal**, elegir **Command Prompt / Símbolo del sistema**
en el selector de perfiles. Los comandos de activación de esta guía usan CMD.

Comprobar las herramientas:

```bat
py --version
git --version
```

Si `py` no se reconoce pero `python --version` funciona, usar `python` en lugar
de `py` en el comando de creación del entorno virtual.

Crear el entorno e instalar:

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## 3. Ejecutar en tu PC

```bat
python -m pytest
```

Se abrirá y cerrará Chrome para cada test. Esperar a que termine: no cerrar las
ventanas mientras se ejecuta. Una ejecución satisfactoria debe mostrar
**3 passed**. Si hay fallos, conservar el error y revisar las evidencias.

Abrir el reporte:

```bat
start reports\reporte.html
```

El reporte adjunto al ZIP documenta la verificación indicada en
`reports/VERIFICACION.md`. Tu ejecución vuelve a generar el reporte y el log
con los resultados de tu PC; esos son los que conviene entregar.

## 4. Crear los commits

Este ZIP no contiene un historial Git previo. Los siguientes commits registran
de forma transparente las partes del proyecto que incorporás al repositorio.
No cambies fechas ni simules un historial de desarrollo anterior. A partir de
ahora, cada corrección o mejora debe tener su propio commit descriptivo.

Primero, inicializar:

```bat
git init
git branch -M main
```

Si Git solicita tu identidad, configurar tus datos reales. Usar el email de
GitHub o el correo privado `noreply` que GitHub muestre en tu configuración:

```bat
git config user.name "TU NOMBRE"
git config user.email "TU EMAIL"
```

Reemplazar esos dos valores antes de ejecutar. Si Git ya tiene tu identidad
correcta, no hace falta configurarlos otra vez.

Incorporar los archivos por partes:

```bat
git add .gitignore requirements.txt pytest.ini utils/__init__.py reports/screenshots/.gitkeep
git commit -m "Crear estructura y configurar dependencias de QA"

git add conftest.py utils/saucedemo_utils.py
git commit -m "Agregar navegador independiente, funciones auxiliares y capturas de fallos"

git add tests/test_saucedemo.py
git commit -m "Agregar pruebas de login, catalogo y carrito"

git add README.md GUIA_PASO_A_PASO.md
git commit -m "Documentar instalacion, ejecucion y entrega"
```

Para conservar evidencias completas después de probar casos individuales,
ejecutar de nuevo la suite y luego registrar sus resultados:

```bat
python -m pytest
git add reports
git commit -m "Guardar reporte HTML y logs de la ejecucion completa"
git status
git log --oneline
```

Si hubo fallos, resolverlos y repetir antes de entregar. El reporte debe
reflejar una ejecución real; no editarlo para modificar los resultados.

## 5. Crear el repositorio público en GitHub

1. Iniciar sesión en tu cuenta de GitHub.
2. Ir a **New repository**.
3. Nombre: `pre-entrega-automation-testing-ezequiel-de-la-torre-lasala`.
4. Seleccionar **Public**, como pide la consigna.
5. Dejar sin marcar las opciones de crear README, `.gitignore` o licencia:
   los archivos ya están preparados localmente.
6. Crear el repositorio y copiar su URL HTTPS.

En la terminal, reemplazar `TU_USUARIO` por tu usuario de GitHub:

```bat
git remote add origin https://github.com/TU_USUARIO/pre-entrega-automation-testing-ezequiel-de-la-torre-lasala.git
git push -u origin main
```

Completar el inicio de sesión que Git solicite. Si aparece un error,
compartir el texto del error para revisarlo.

## 6. Revisar antes de entregar

- El repositorio es público y se puede abrir sin iniciar sesión.
- Se ven `tests/`, `utils/`, `conftest.py`, `requirements.txt`, `pytest.ini` y README.
- Se ve `reports/reporte.html` y `reports/ejecucion.log` de la suite completa.
- El reporte muestra los tres tests aprobados.
- Se ven los commits descriptivos.
- No se subieron `.venv/` ni cachés.
- Compartir el enlace al repositorio, no solamente el ZIP ni el enlace al reporte.

GitHub muestra el HTML como código; para visualizar el reporte se descarga y
se abre con un navegador.

## Cómo explicar el código

- `tests/test_saucedemo.py` define qué comportamientos se validan con `assert`.
- `utils/saucedemo_utils.py` reúne las operaciones repetidas con Selenium.
- `conftest.py` administra el navegador mediante un fixture con `yield`:
  la parte anterior prepara el navegador y el bloque `finally` lo cierra.
- El hook `pytest_runtest_makereport` recibe el resultado de cada etapa del
  test y genera una captura si ocurre un fallo con un navegador disponible.
- `pytest.ini` activa los logs y el HTML; por eso `python -m pytest` ya genera
  ambos archivos.
- `WebDriverWait` espera una condición concreta hasta un máximo de 10 segundos.
- El primer producto se obtiene de su contenedor; el test no depende de que
  su nombre o precio sean siempre los mismos.
- Cada test recibe un Chrome nuevo e inicia sesión por sí mismo: puede
  ejecutarse solo o en cualquier orden.
