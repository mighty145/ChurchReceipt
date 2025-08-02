# PowerShell script to clean Git history and remove secrets
# This will create a fresh commit without the secret-containing history

Write-Host "Creating backup of current repository..." -ForegroundColor Green
cd ..
Copy-Item -Recurse -Path "Chruchreceipt" -Destination "Chruchreceipt_backup"

Write-Host "Cleaning Git history to remove secrets..." -ForegroundColor Green
cd Chruchreceipt

# Remove the old origin to prevent accidental pushes
git remote remove origin

# Create a new orphan branch (starts with no history)
git checkout --orphan clean-main

# Add all current files (without the secrets)
git add .

# Make the first commit
git commit -m "Initial clean commit: Church Receipt System with secure credential management

Features:
- Flask web application for church receipt generation
- Azure AI Services integration for document analysis
- Mobile-friendly responsive design
- Progressive Web App (PWA) support
- Manual receipt entry functionality
- Secure environment variable configuration
- Professional PDF receipt generation
- File upload with validation and size limits

Security:
- Environment variables for sensitive credentials
- Comprehensive .gitignore for security
- No hardcoded API keys or endpoints
- Secure file handling and validation"

# Delete the old main branch
git branch -D main

# Rename clean-main to main
git branch -m clean-main main

Write-Host "Git history cleaned successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Add your GitHub remote: git remote add origin https://github.com/mighty145/ChurchReceipt.git" -ForegroundColor White
Write-Host "2. Force push the clean history: git push -f origin main" -ForegroundColor White
Write-Host ""
Write-Host "Note: This will completely replace your GitHub repository history." -ForegroundColor Red
Write-Host "The backup is saved in ../Chruchreceipt_backup/" -ForegroundColor Cyan
