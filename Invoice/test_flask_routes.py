"""
Quick test to verify the download route exists
"""

def test_flask_routes():
    """Test that all required Flask routes are defined"""
    
    # Read the web_invoice_app.py file and check for routes
    with open('web_invoice_app.py', 'r') as f:
        content = f.read()
    
    required_routes = [
        "@app.route('/')",
        "@app.route('/upload'",
        "@app.route('/generate_receipt'",
        "@app.route('/download/<filename>')",
        "@app.route('/api/upload'"
    ]
    
    print("🔍 Checking Flask routes:")
    for route in required_routes:
        if route in content:
            print(f"✅ Found: {route}")
        else:
            print(f"❌ Missing: {route}")
    
    # Check for send_file import
    if 'send_file' in content:
        print("✅ send_file import found")
    else:
        print("❌ send_file import missing")
    
    print("\n🔍 Checking download_file function:")
    if 'def download_file(filename):' in content:
        print("✅ download_file function exists")
        
        # Check for security features
        if 'secure_filename' in content:
            print("✅ Filename security implemented")
        if 'os.path.exists' in content:
            print("✅ File existence check implemented")
        if 'send_file(' in content:
            print("✅ File sending functionality implemented")
    else:
        print("❌ download_file function missing")

if __name__ == "__main__":
    print("🧪 Testing Flask App Configuration")
    print("=" * 40)
    
    test_flask_routes()
    
    print("\n" + "=" * 40)
    print("🎯 Expected result:")
    print("✅ All routes should be found")
    print("✅ Download functionality should work")
    print("\nTo test the fix:")
    print("1. Run: py web_invoice_app.py")
    print("2. Generate a receipt")
    print("3. Click download - should work without URL build error")
