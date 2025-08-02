# Church Invoice Analyzer

A comprehensive solution for analyzing church payment forms and invoices with support for desktop, web, and mobile interfaces.

## Features

- **Multi-platform Support**: Desktop GUI, Web interface, and Mobile-friendly upload
- **Azure Content Understanding Integration**: Automatic data extraction from payment forms
- **Receipt Generation**: Automatic receipt creation from extracted data
- **Multiple Input Methods**: File picker, drag-and-drop, camera capture, gallery selection
- **Mobile Optimized**: Responsive design for smartphones and tablets

## Installation

### Option 1: Automatic Setup (Windows)
1. Run `setup.bat` (Command Prompt) or `setup.ps1` (PowerShell)
2. The script will install all required dependencies

### Option 2: Manual Installation
```bash
pip install flask werkzeug pillow requests
```

## Usage

### 1. Desktop Application (Command Line)
```bash
python invoiceanalyzer.py
```

Choose from:
- Use default file
- Enter file path manually
- Use file picker (GUI)
- Start web interface

### 2. Web Interface (Recommended for Mobile)
```bash
python web_invoice_app.py
```

Then open your browser to:
- Local: http://localhost:5000
- Network: http://[your-ip]:5000

### 3. Mobile-Only Interface
Open `mobile_upload.html` directly in a mobile browser for a simplified mobile experience.

## File Structure

```
Invoice/
├── invoiceanalyzer.py          # Main analyzer with Azure integration
├── web_invoice_app.py          # Flask web application
├── mobile_upload.html          # Mobile-only interface
├── printreceipt.py            # Receipt generation module
├── templates/                  # Web interface templates
│   ├── upload.html
│   ├── results.html
│   └── receipt_generated.html
├── uploads/                    # Directory for uploaded files
├── requirements.txt            # Python dependencies
├── setup.bat                   # Windows setup script
├── setup.ps1                   # PowerShell setup script
└── README.md                   # This file
```

## Supported File Types

- **Images**: JPG, JPEG, PNG, GIF, BMP, TIFF
- **Documents**: PDF
- **Maximum File Size**: 16MB

## Mobile Features

The mobile interface includes:
- **Camera Capture**: Take photos directly from the camera
- **Gallery Selection**: Choose existing photos from device gallery
- **Touch-Friendly**: Large buttons optimized for mobile devices
- **Progress Indicators**: Visual feedback during upload and processing
- **Responsive Design**: Works on phones and tablets

## API Endpoints

The web application provides REST API endpoints for integration:

### Upload File
```
POST /api/upload
Content-Type: multipart/form-data

Response:
{
  "success": true,
  "filename": "unique_filename",
  "extracted_data": {...},
  "message": "File analyzed successfully"
}
```

## Configuration

### Azure Content Understanding Settings
Update the following in `invoiceanalyzer.py`:
```python
settings = Settings(
    endpoint="your-azure-endpoint",
    api_version="2025-05-01-preview",
    subscription_key="your-subscription-key",
    analyzer_id="invoice-analyzer",
    file_location=file_path,
)
```

## Security Considerations

- **File Validation**: Only approved file types are accepted
- **Size Limits**: Maximum 16MB file size to prevent abuse
- **Secure Filenames**: Uploaded files are renamed with secure random names
- **Input Sanitization**: All user inputs are properly sanitized

## Troubleshooting

### Common Issues

1. **"Import flask could not be resolved"**
   - Run `pip install flask werkzeug`

2. **"tkinter not available"**
   - Install Python with tkinter support or use web interface

3. **"Azure endpoint not responding"**
   - Check your Azure subscription key and endpoint URL
   - Ensure the analyzer is properly deployed

4. **Mobile camera not working**
   - Ensure you're accessing the site via HTTPS on mobile
   - Grant camera permissions when prompted

### File Upload Issues

- **Large files**: Ensure files are under 16MB
- **Unsupported formats**: Use JPG, PNG, or PDF files
- **Network issues**: Check internet connection for Azure API calls

## Development

### Adding New Fields
To extract additional fields from invoices:

1. Add field names to `selected_fields` in `invoiceanalyzer.py`
2. Update the form templates in `templates/results.html`
3. Modify the receipt generation in `printreceipt.py`

### Customizing the Mobile Interface
Edit `mobile_upload.html` to:
- Change styling and colors
- Add new input methods
- Modify the preview functionality

## License

This project is designed for church use and contains Azure AI services integration.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure Azure services are properly configured
