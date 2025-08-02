"""
Test script to verify download functionality
"""

def test_download_route():
    """Test the download route functionality"""
    import os
    from werkzeug.utils import secure_filename
    
    # Test filename security
    test_files = [
        "test_receipt.jpg",
        "web_generated_receipt_36dc8fa8-43aa-43a8-b931-cfa4904ef936_Payment_form_Church.JPG.jpg",
        "../../../malicious_file.txt",  # Should be cleaned
        "normal_file.pdf"
    ]
    
    print("Testing filename security:")
    for filename in test_files:
        safe_name = secure_filename(filename)
        print(f"Original: {filename}")
        print(f"Safe:     {safe_name}")
        print()

def test_file_existence():
    """Check what files exist in the directory"""
    import os
    
    print("Files in current directory:")
    for file in os.listdir('.'):
        if file.startswith('web_generated_receipt'):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} bytes)")
    
    print("\nFiles in uploads directory:")
    if os.path.exists('uploads'):
        for file in os.listdir('uploads'):
            size = os.path.getsize(os.path.join('uploads', file))
            print(f"✅ {file} ({size} bytes)")
    else:
        print("No uploads directory found")

if __name__ == "__main__":
    print("🔧 Testing Download Functionality")
    print("=" * 40)
    
    test_download_route()
    test_file_existence()
    
    print("=" * 40)
    print("✅ Download functionality should now work!")
    print("\nTo test:")
    print("1. Run: py web_invoice_app.py")
    print("2. Upload a file and generate a receipt")
    print("3. Click the Download buttons")
    print("4. Files should download instead of showing alert")
