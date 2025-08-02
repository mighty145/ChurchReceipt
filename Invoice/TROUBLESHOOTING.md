# TROUBLESHOOTING GUIDE - Church Invoice Analyzer

## ❌ Error: "setup.ps1 is not recognized"

### **Problem**
PowerShell execution policy or incorrect path/syntax.

### **Solutions**

#### **Option 1: Use Batch File (Recommended)**
```cmd
cd "C:\Users\might\Projects\ChruchProject\Invoice"
.\setup.bat
```

#### **Option 2: Fix PowerShell Script**
```powershell
# Navigate to correct directory first
cd "C:\Users\might\Projects\ChruchProject\Invoice"

# Then run with proper syntax
.\setup.ps1

# If execution policy error, temporarily allow scripts:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
# Restore policy after:
Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser
```

#### **Option 3: Run Commands Directly**
```powershell
cd "C:\Users\might\Projects\ChruchProject\Invoice"
powershell -ExecutionPolicy Bypass -File setup.ps1
```

---

## ❌ Error: "pip is not recognized" or "python is not recognized"

### **Problem**
Python is not installed or not added to system PATH.

### **Solutions**

#### **Step 1: Install Python**
1. Download Python from: https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Choose "Install for all users" if you have admin rights

#### **Step 2: Verify Installation**
```cmd
python --version
# or try:
py --version
```

#### **Step 3: Manual PATH Setup (if needed)**
1. Open System Properties → Advanced → Environment Variables
2. Add Python installation directory to PATH:
   - `C:\Users\[username]\AppData\Local\Programs\Python\Python311\`
   - `C:\Users\[username]\AppData\Local\Programs\Python\Python311\Scripts\`

#### **Step 4: Use Python Environment Checker**
```cmd
python check_environment.py
```

---

## ❌ Error: "Import flask could not be resolved"

### **Solutions**

#### **Option 1: Install with Python Module**
```cmd
python -m pip install flask werkzeug pillow requests
```

#### **Option 2: Use py launcher**
```cmd
py -m pip install flask werkzeug pillow requests
```

#### **Option 3: Manual Installation**
```cmd
# Install each package individually
python -m pip install flask
python -m pip install werkzeug
python -m pip install pillow
python -m pip install requests
```

---

## ❌ Error: "tkinter not available"

### **Problem**
GUI file picker won't work without tkinter.

### **Solutions**
- **Windows**: tkinter usually comes with Python
- **If missing**: Reinstall Python with "tcl/tk and IDLE" option checked
- **Alternative**: Use web interface instead of GUI picker

---

## ✅ **Quick Setup Commands (Copy & Paste)**

### **For Command Prompt:**
```cmd
cd "C:\Users\might\Projects\ChruchProject\Invoice"
python -m pip install flask werkzeug pillow requests
python invoiceanalyzer.py
```

### **For PowerShell:**
```powershell
cd "C:\Users\might\Projects\ChruchProject\Invoice"
python -m pip install flask werkzeug pillow requests
python invoiceanalyzer.py
```

---

## 🚀 **Running the Application**

### **Method 1: Desktop Application**
```cmd
cd "C:\Users\might\Projects\ChruchProject\Invoice"
python invoiceanalyzer.py
```

### **Method 2: Web Interface**
```cmd
cd "C:\Users\might\Projects\ChruchProject\Invoice"
python web_invoice_app.py
```
Then open: http://localhost:5000

### **Method 3: Mobile Interface**
Open `mobile_upload.html` directly in any web browser.

---

## 🔍 **Testing Your Setup**

Run this command to test everything:
```cmd
python check_environment.py
```

---

## 📱 **Mobile Access**

1. Start web interface: `python web_invoice_app.py`
2. Find your computer's IP address: `ipconfig`
3. On mobile, go to: `http://[your-ip]:5000`

---

## 🆘 **Still Having Issues?**

1. **Check Python Installation**:
   ```cmd
   python --version
   pip --version
   ```

2. **Check Current Directory**:
   ```cmd
   dir setup.*
   ```

3. **Manual Package Check**:
   ```cmd
   python -c "import flask; print('Flask OK')"
   python -c "import requests; print('Requests OK')"
   ```

4. **Alternative Python Commands to Try**:
   - `python3` instead of `python`
   - `py` instead of `python`
   - `pip3` instead of `pip`

---

## 📞 **Contact Information**

If you continue to have issues, please provide:
1. Your Windows version
2. Python version (`python --version`)
3. Exact error message
4. Steps you tried from this guide
