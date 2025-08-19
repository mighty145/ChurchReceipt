"""
Direct Flask Download and Setup
Downloads Flask and dependencies directly to project folder
"""

import os
import sys
import urllib.request
import zipfile
import tempfile
import shutil

def download_and_extract_package(package_name, download_url, extract_to):
    """Download and extract a Python package"""
    try:
        # Create temp file
        temp_file = os.path.join(tempfile.gettempdir(), f"{package_name}.zip")
        
        print(f"Downloading {package_name}...")
        urllib.request.urlretrieve(download_url, temp_file)
        
        print(f"Extracting {package_name}...")
        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        # Clean up
        os.remove(temp_file)
        print(f"✓ Successfully installed {package_name}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to install {package_name}: {e}")
        return False

def setup_flask_direct():
    """Set up Flask directly in project directory"""
    print("Direct Flask Setup")
    print("=" * 30)
    
    # Create lib directory in project
    current_dir = os.path.dirname(os.path.abspath(__file__))
    lib_dir = os.path.join(current_dir, 'lib')
    os.makedirs(lib_dir, exist_ok=True)
    
    # Add to Python path
    if lib_dir not in sys.path:
        sys.path.insert(0, lib_dir)
    
    # Package URLs (GitHub releases or PyPI direct downloads)
    packages = {
        'flask': 'https://files.pythonhosted.org/packages/3f/e0/a89e8120fcea040d983423baf2e5af2dea5a0a8e9e7c5bca9b27235b4a73/Flask-2.3.3-py3-none-any.whl',
        'werkzeug': 'https://files.pythonhosted.org/packages/c3/fc/254c3e9b5feb89ff5b9076a23218dafbc99c96ac5941e900b71206e6313b5/werkzeug-2.3.7-py3-none-any.whl',
        'jinja2': 'https://files.pythonhosted.org/packages/bc/c3/f068337a370801f372f2f8f6bad74a5c140f6fda3d9de154052708dd3c65/Jinja2-3.1.2-py3-none-any.whl',
        'click': 'https://files.pythonhosted.org/packages/00/2e/d53fa4befbf2cfa713304affc7ca780ce4fc1fd8710527771b58311a3229/click-8.1.7-py3-none-any.whl',
        'itsdangerous': 'https://files.pythonhosted.org/packages/68/5f/447e04e828f47465eeab35b5d408b7ebaaaee207f48b7136c5a7267a30ae/itsdangerous-2.1.2-py3-none-any.whl',
        'markupsafe': 'https://files.pythonhosted.org/packages/ce/af/2f5c0b3b452c0a1a7ceb2ba2536a96096101a1b8e34db0524c473191b4ca/MarkupSafe-2.1.3-cp313-cp313-win_amd64.whl'
    }
    
    success_count = 0
    for package_name, url in packages.items():
        if download_and_extract_package(package_name, url, lib_dir):
            success_count += 1
    
    print(f"\\nInstalled {success_count}/{len(packages)} packages")
    
    # Test imports
    print("\\nTesting imports...")
    try:
        import flask
        print("✓ Flask imported successfully!")
        return True
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False

def create_simple_test():
    """Create a simple test script"""
    test_code = '''
# Simple Flask test
import sys
import os

# Add lib directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(current_dir, 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

try:
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return '<h1>Flask is working!</h1><p>Church Invoice Analyzer is ready.</p>'
    
    if __name__ == '__main__':
        print("Starting Flask test server...")
        app.run(debug=True, port=5001)
        
except ImportError as e:
    print(f"Flask import failed: {e}")
    print("Please run: python direct_flask_setup.py")
'''
    
    with open('flask_test.py', 'w') as f:
        f.write(test_code)
    
    print("✓ Created flask_test.py")

def main():
    """Main setup function"""
    if setup_flask_direct():
        create_simple_test()
        print("\\n✅ Flask setup complete!")
        print("\\nTest commands:")
        print("1. python flask_test.py")
        print("2. python web_invoice_app.py")
    else:
        print("\\n❌ Flask setup failed")
        print("Please try manual Python reinstallation")

if __name__ == "__main__":
    main()
