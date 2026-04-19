@echo off
echo ═══════════════════════════════════════════════════════════════
echo    GREEN HOUSE INMOBILIARIA - Arranque Automatico
echo ═══════════════════════════════════════════════════════════════
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo [1/4] Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual
        echo Asegurate de tener Python instalado
        pause
        exit /b 1
    )
) else (
    echo [✓] Entorno virtual ya existe
)

REM Activar entorno virtual
echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

REM Instalar dependencias
echo [3/4] Instalando dependencias...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

REM Arrancar servidor
echo [4/4] Arrancando servidor Flask...
echo.
echo ═══════════════════════════════════════════════════════════════
echo    ✓ Servidor iniciado correctamente
echo    
echo    Abre tu navegador en:
echo    http://localhost:5000       - Web principal
echo    http://localhost:5000/admin - Panel administracion
echo    
echo    Presiona Ctrl+C para detener el servidor
echo ═══════════════════════════════════════════════════════════════
echo.

python app.py

pause
