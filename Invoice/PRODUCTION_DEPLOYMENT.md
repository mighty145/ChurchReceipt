# Production Deployment Guide for Church Invoice Analyzer

## Overview
This guide covers deploying your Flask church invoice analyzer to production for internet access from any device.

## Quick Deployment Options

### Option 1: Azure App Service (Recommended)
**Benefits:** Seamless integration with your existing Azure AI services, automatic HTTPS, easy scaling

**Steps:**
1. Install Azure CLI: `az login`
2. Create resource group: `az group create --name church-app-rg --location "East US"`
3. Create App Service plan: `az appservice plan create --name church-app-plan --resource-group church-app-rg --sku B1 --is-linux`
4. Create web app: `az webapp create --resource-group church-app-rg --plan church-app-plan --name church-invoice-analyzer --runtime "PYTHON|3.9"`
5. Deploy code: `az webapp deployment source config-zip --resource-group church-app-rg --name church-invoice-analyzer --src deployment.zip`

**Environment Variables to Set:**
```bash
az webapp config appsettings set --resource-group church-app-rg --name church-invoice-analyzer --settings \
    FLASK_ENV=production \
    SECRET_KEY="your-secure-secret-key" \
    AZURE_ENDPOINT="https://your-resource-name.cognitiveservices.azure.com/" \
    AZURE_API_KEY="your-api-key"
```

### Option 2: Heroku (Easy & Free Tier Available)
**Benefits:** Simple deployment, free tier available, automatic HTTPS

**Steps:**
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create church-invoice-analyzer`
4. Set environment variables:
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY="your-secure-secret-key"
heroku config:set AZURE_ENDPOINT="https://your-resource-name.cognitiveservices.azure.com/"
heroku config:set AZURE_API_KEY="your-api-key"
```
5. Deploy: `git push heroku main`

### Option 3: Railway (Modern Alternative)
**Benefits:** Simple deployment, automatic HTTPS, good free tier

**Steps:**
1. Connect GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on git push

### Option 4: DigitalOcean App Platform
**Benefits:** Affordable, good performance, automatic scaling

## Security & Production Considerations

### 1. Environment Variables
- Never commit API keys to git
- Use environment variables for all sensitive data
- Generate a strong SECRET_KEY for Flask sessions

### 2. HTTPS & Security Headers
- All platforms provide automatic HTTPS
- Security headers are configured in the production app
- File upload restrictions are enforced

### 3. Error Handling & Logging
- Production app includes proper error handling
- Logging configured for debugging production issues
- User-friendly error messages

### 4. File Management
- Uploaded files are automatically cleaned up
- File size limits enforced (16MB)
- Secure filename handling

## Custom Domain Setup

### For Azure App Service:
```bash
# Add custom domain
az webapp config hostname add --webapp-name church-invoice-analyzer --resource-group church-app-rg --hostname yourdomain.com

# Enable SSL
az webapp config ssl bind --certificate-thumbprint <thumbprint> --ssl-type SNI --name church-invoice-analyzer --resource-group church-app-rg
```

### For Heroku:
```bash
# Add custom domain
heroku domains:add yourdomain.com

# Enable SSL (automatic on paid plans)
heroku certs:auto:enable
```

## Performance Optimization

### 1. Gunicorn Configuration
The production setup uses Gunicorn with:
- 2 worker processes (adjust based on CPU cores)
- 120-second timeout for large file processing
- Proper error handling

### 2. File Storage
Consider upgrading to cloud storage for production:
- Azure Blob Storage
- AWS S3
- Google Cloud Storage

### 3. Database (if needed later)
For storing receipt history:
- PostgreSQL (available on all platforms)
- Azure SQL Database
- MongoDB Atlas

## Mobile Access

### Responsive Design
The mobile interface is already optimized for:
- Phone cameras
- Touch interfaces
- Mobile browsers
- WhatsApp integration

### Progressive Web App (PWA)
Consider adding PWA features:
- Offline capability
- App installation
- Push notifications

## Cost Estimation

### Azure App Service B1:
- ~$13/month
- 1.75 GB RAM, 10 GB storage
- Custom domain, SSL included

### Heroku:
- Free tier: 550-1000 hours/month
- Hobby tier: $7/month
- Professional: $25/month

### Railway:
- Free tier: $5 credit/month
- Pro: $20/month

## Monitoring & Maintenance

### 1. Application Insights (Azure)
- Track usage and performance
- Monitor errors and exceptions
- Set up alerts

### 2. Log Management
- Review application logs regularly
- Set up error notifications
- Monitor file upload patterns

### 3. Backup Strategy
- Regular database backups (if using database)
- Keep receipt generation templates backed up
- Environment variable documentation

## Getting Started

1. **Choose a platform** (Azure recommended for your setup)
2. **Set up environment variables** (copy from .env.example)
3. **Deploy using provided files** (wsgi.py, Procfile, Dockerfile)
4. **Configure custom domain** (optional)
5. **Test from multiple devices**

## Support & Troubleshooting

### Common Issues:
1. **File upload fails**: Check file size limits
2. **Azure AI errors**: Verify API keys and endpoints
3. **Mobile interface issues**: Clear browser cache
4. **Receipt generation fails**: Check font files are included

### Debug Steps:
1. Check application logs
2. Verify environment variables
3. Test with sample files
4. Check network connectivity

## Next Steps

After deployment:
1. Test all features from different devices
2. Set up monitoring and alerts
3. Configure backup procedures
4. Document the production URL for users
5. Consider adding user authentication if needed

Your app will be accessible at:
- Azure: `https://church-invoice-analyzer.azurewebsites.net`
- Heroku: `https://church-invoice-analyzer.herokuapp.com`
- Custom domain: `https://yourdomain.com`
