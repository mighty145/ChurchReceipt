@echo off
echo Adding Python to PATH for current session...
echo.

echo Current Python installation detected at:
for /f "tokens=*" %%i in ('py -c "import sys; print(sys.executable)"') do set PYTHON_PATH=%%i
echo %PYTHON_PATH%

echo.
echo Adding Python directory to PATH...
for %%i in ("%PYTHON_PATH%") do set PYTHON_DIR=%%~dpi
set PATH=%PYTHON_DIR%;%PATH%

echo Testing python command...
python --version
if %errorlevel% equ 0 (
    echo ✅ SUCCESS: 'python' command now works!
    echo.
    echo To make this permanent:
    echo 1. Open System Properties ^> Advanced ^> Environment Variables
    echo 2. Add this path to your PATH variable: %PYTHON_DIR%
    echo.
) else (
    echo ❌ Still having issues. Use 'py' command instead.
)

echo.
echo Testing the Church Invoice Analyzer...
echo.
python invoiceanalyzer.py
pause
