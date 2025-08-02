# Church Receipt System

A Flask web application that uses Azure AI Services to analyze church payment forms and automatically generate receipts.

## ⚠️ Important Security Notice

This application requires Azure AI Services credentials. **Never commit your actual API keys to Git!**

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/mighty145/ChurchReceipt.git
cd ChurchReceipt/Invoice
```

### 2. Set Up Environment Variables
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file and add your actual Azure credentials:
   ```bash
   # Replace with your actual Azure AI Services credentials
   AZURE_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
   AZURE_API_KEY=your-actual-azure-api-key-here
   
   # Set a secure secret key for Flask sessions
   SECRET_KEY=your-secure-secret-key-here
   ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python web_invoice_app.py
```

The application will be available at `http://localhost:5000`

## Features

- **File Upload**: Upload images or PDFs of church payment forms
- **AI Analysis**: Automatically extract payment information using Azure AI
- **Manual Entry**: Create receipts manually without uploading files
- **Receipt Generation**: Generate professional PDF receipts
- **Mobile Friendly**: Responsive design for mobile devices
- **PWA Support**: Install as a Progressive Web App

## API Endpoints

- `GET /` - Main upload page
- `POST /upload` - Upload and analyze files
- `GET /manual-entry` - Manual receipt entry form
- `POST /generate_receipt` - Generate receipt from data
- `GET /mobile` - Mobile-optimized interface
- `POST /api/upload` - API endpoint for mobile apps
- `GET /api/health` - Health check endpoint

## Security Features

- Environment variable configuration for credentials
- File type validation
- File size limits (16MB max)
- Secure filename handling
- CORS support for mobile apps

## Deployment

See `PRODUCTION_DEPLOYMENT.md` for detailed deployment instructions for:
- Azure App Service
- Heroku
- Railway
- DigitalOcean

## Project Structure

```
Invoice/
├── web_invoice_app.py          # Main Flask application
├── invoiceanalyzer.py          # Azure AI integration
├── printreceipt.py             # Receipt generation
├── config.py                   # Configuration management
├── templates/                  # HTML templates
├── static/                     # Static files (CSS, JS, images)
├── uploads/                    # File upload directory
└── Receipts store/             # Generated receipts storage
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_ENDPOINT` | Azure AI Services endpoint URL | Yes |
| `AZURE_API_KEY` | Azure AI Services subscription key | Yes |
| `SECRET_KEY` | Flask session secret key | Yes |
| `FLASK_ENV` | Environment (development/production) | No |
| `UPLOAD_FOLDER` | Upload directory path | No |
| `MAX_FILE_SIZE` | Maximum file size in bytes | No |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please create an issue on GitHub.
