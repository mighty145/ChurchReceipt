@echo off
REM iOS Testing Setup Script for Invoice Analyzer Web App
REM ====================================================

echo =========================================
echo iOS Mobile Testing Setup
echo =========================================
echo.

REM Get local IP address
echo Finding your computer's IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set IP=%%a
    goto :found
)
:found
set IP=%IP: =%
echo Your IP Address: %IP%
echo.

REM Check if Python is available
echo Checking Python installation...
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Python is available
) else (
    echo ✗ Python not found. Please install Python first.
    pause
    exit /b 1
)
echo.

REM Check if required packages are installed
echo Checking required packages...
py -c "import flask" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Flask is installed
) else (
    echo Installing Flask...
    py -m pip install flask
)

py -c "import PIL" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ PIL is installed
) else (
    echo Installing Pillow...
    py -m pip install Pillow
)

py -c "import requests" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Requests is installed
) else (
    echo Installing Requests...
    py -m pip install requests
)
echo.

REM Create uploads directory if it doesn't exist
if not exist "uploads" (
    echo Creating uploads directory...
    mkdir uploads
    echo ✓ Uploads directory created
)
echo.

REM Check firewall status
echo Checking Windows Firewall...
netsh advfirewall show allprofiles | findstr "State" | findstr "ON" >nul
if %errorlevel% equ 0 (
    echo ⚠ Windows Firewall is ON
    echo   You may need to allow Python/Flask through the firewall
    echo   or temporarily disable it for testing
) else (
    echo ✓ Windows Firewall appears to be OFF
)
echo.

echo =========================================
echo Setup Complete! Ready for iOS Testing
echo =========================================
echo.
echo TESTING INSTRUCTIONS:
echo 1. Make sure your iOS device is on the same WiFi network
echo 2. Open Safari on your iOS device
echo 3. Go to: http://%IP%:5000
echo 4. For mobile-optimized interface: http://%IP%:5000/mobile
echo.
echo Starting Flask application...
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask application
py web_invoice_app.py
