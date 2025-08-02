@echo off
echo Installing required packages for Church Invoice Analyzer...
echo.

echo Checking Python installation...

rem First try py launcher (Windows Python Launcher)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python found via py launcher!
    set PYTHON_CMD=py
    set PIP_CMD=py -m pip
    goto :python_found
)

rem Then try python command
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python found via python command!
    set PYTHON_CMD=python
    set PIP_CMD=python -m pip
    goto :python_found
)

rem If neither works, show error
echo ERROR: Python is not installed or not accessible!
echo.
echo You have two options:
echo 1. Add Python to PATH manually:
echo    - Add: C:\Users\might\AppData\Local\Programs\Python\Python313
echo    - Add: C:\Users\might\AppData\Local\Programs\Python\Python313\Scripts
echo 2. Or continue with 'py' command (recommended)
echo.
echo Testing 'py' command...
py --version
if %errorlevel% equ 0 (
    echo 'py' command works! Continuing with setup...
    set PYTHON_CMD=py
    set PIP_CMD=py -m pip
    goto :python_found
)
echo.
echo Please install Python from: https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
pause
exit /b 1

:python_found

echo Python found! Installing packages...
echo.

echo Installing Flask and dependencies...
%PIP_CMD% install flask werkzeug

echo.
echo Installing image processing libraries...
%PIP_CMD% install pillow

echo.
echo Installing requests library...
%PIP_CMD% install requests

echo.
echo Setup complete!
echo.
echo To use the application:
echo 1. For desktop GUI: %PYTHON_CMD% invoiceanalyzer.py
echo 2. For web interface: %PYTHON_CMD% web_invoice_app.py
echo 3. For mobile: Open mobile_upload.html in a browser
echo.
echo If you get import errors, you may need to install additional packages:
echo %PIP_CMD% install tkinter (for GUI file picker)
echo.
pause
