"""
Church Invoice Analyzer - Python Environment Checker
This script helps you set up the Python environment for the application.
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is suitable"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 7:
        print("✅ Python version is suitable")
        return True
    else:
        print("❌ Python 3.7 or higher is required")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} is installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is NOT installed")
        return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ Successfully installed {package_name}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package_name}")
        return False

def main():
    print("🔍 Church Invoice Analyzer - Environment Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        print("\n📥 Please install Python 3.7+ from: https://www.python.org/downloads/")
        print("⚠️  Make sure to check 'Add Python to PATH' during installation")
        input("Press Enter to exit...")
        return
    
    print("\n🔍 Checking required packages...")
    packages_to_check = [
        ("requests", "requests"),
        ("pillow", "PIL"),
        ("flask", "flask"),
        ("werkzeug", "werkzeug")
    ]
    
    missing_packages = []
    for package_name, import_name in packages_to_check:
        if not check_package(package_name, import_name):
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        for package in missing_packages:
            print(f"\n📥 Installing {package}...")
            install_package(package)
    
    print("\n🔍 Final check...")
    all_good = True
    for package_name, import_name in packages_to_check:
        if not check_package(package_name, import_name):
            all_good = False
    
    if all_good:
        print("\n🎉 Setup complete! All packages are installed.")
        print("\n🚀 You can now run:")
        print("   python invoiceanalyzer.py")
        print("   python web_invoice_app.py")
    else:
        print("\n❌ Some packages failed to install.")
        print("📝 Try manual installation:")
        for package in missing_packages:
            print(f"   pip install {package}")
    
    print("\n" + "=" * 50)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
