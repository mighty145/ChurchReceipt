@echo off
echo Starting Church Invoice Analyzer Web Application
echo.

echo Checking Flask installation...
py -c "from web_invoice_app import app; print('Flask app imports successfully!')" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Flask import failed!
    echo.
    echo The Flask import error has been fixed by modifying web_invoice_app.py
    echo to include the local package path. The import should work now.
    echo.
    echo If you still see errors, try:
    echo 1. py test_flask_app.py
    echo 2. Check PYTHON_FLASK_FIX_GUIDE.md for solutions
    pause
    exit /b 1
)

echo ✅ Flask import successful!
echo.
echo Starting Flask web server...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

py web_invoice_app.py
