#!/bin/bash

# Script to clean Git history and remove secrets
# This will create a fresh commit without the secret-containing history

echo "Creating backup of current repository..."
cd ..
cp -r Chruchreceipt Chruchreceipt_backup

echo "Cleaning Git history to remove secrets..."
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

echo "Git history cleaned successfully!"
echo ""
echo "Next steps:"
echo "1. Add your GitHub remote: git remote add origin https://github.com/mighty145/ChurchReceipt.git"
echo "2. Force push the clean history: git push -f origin main"
echo ""
echo "Note: This will completely replace your GitHub repository history."
echo "The backup is saved in ../Chruchreceipt_backup/"
