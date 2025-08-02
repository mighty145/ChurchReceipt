Write-Host "Installing required packages for Church Invoice Analyzer..." -ForegroundColor Green
Write-Host ""

Write-Host "Installing Flask and dependencies..." -ForegroundColor Yellow
pip install flask werkzeug

Write-Host ""
Write-Host "Installing image processing libraries..." -ForegroundColor Yellow
pip install pillow

Write-Host ""
Write-Host "Installing requests library..." -ForegroundColor Yellow
pip install requests

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To use the application:" -ForegroundColor Cyan
Write-Host "1. For desktop GUI: python invoiceanalyzer.py" -ForegroundColor White
Write-Host "2. For web interface: python web_invoice_app.py" -ForegroundColor White
Write-Host "3. For mobile: Open mobile_upload.html in a browser" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to continue"
