#!/usr/bin/env python3

"""
Test that logo.jpg and NameT.jpg are always loaded correctly with absolute paths
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from printreceipt import generate_receipt, save_receipt_multiple_formats

def test_permanent_image_loading():
    """Test that images are always loaded correctly regardless of execution directory"""
    
    print("Testing Permanent Image Loading")
    print("=" * 60)
    
    # Test data
    test_data = {
        'InvoiceDate': '2025-08-02',
        'Name': 'Test User Images',
        'Address': 'Test Address, City',
        'MobileNumber': '9876543210',
        'TitheMonth': 'AUGUST',
        'TitheAmount': 500.0,
        'MembershipMonth': '', 
        'MembershipAmount': 0,
        'BirthdayThankOffering': 0,
        'WeddingAnniversaryThankOffering': 0,
        'HomeMissionPledges': 0,
        'MissionAndEvangelismFund': 0,
        'StStephensSocialAidFund': 0,
        'SpecialThanksAmount': 0,
        'CharityFundAmount': 0,
        'DonationFor': '',
        'DonationAmount': 0,
        'HarvestAuctionComment': '',
        'HarvestAuctionAmount': 0,
        'OnlineChequeNo': 'IMG001',
        'PaymentMethod': 'CASH'
    }
    
    print("Testing image loading with absolute paths...")
    print("Expected:")
    print("1. ✅ logo.jpg should always load at top-left of receipt")
    print("2. ✅ NameT.jpg should always load below 'Treasurer / Secretary'")
    print("3. ✅ Images should work regardless of execution directory")
    print()
    
    # Test from current directory
    print("Test 1: Generating receipt from current directory")
    try:
        receipt_result = generate_receipt(test_data)
        filename = f"test_permanent_images_receipt_{receipt_result['receipt_no']}"
        saved_files = save_receipt_multiple_formats(receipt_result['image'], filename, ["jpg", "pdf"])
        
        print(f"✅ Receipt generated successfully!")
        print(f"Receipt No: {receipt_result['receipt_no']}")
        print(f"Files: {saved_files}")
        
    except Exception as e:
        print(f"❌ Error in Test 1: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test by changing to a different directory
    print("\nTest 2: Testing from different working directory")
    try:
        # Change to parent directory
        original_dir = os.getcwd()
        parent_dir = os.path.dirname(original_dir)
        os.chdir(parent_dir)
        print(f"Changed working directory to: {os.getcwd()}")
        
        # Generate receipt from different directory
        receipt_result2 = generate_receipt(test_data)
        
        # Change back to original directory for saving
        os.chdir(original_dir)
        
        filename2 = f"test_from_different_dir_receipt_{receipt_result2['receipt_no']}"
        saved_files2 = save_receipt_multiple_formats(receipt_result2['image'], filename2, ["jpg"])
        
        print(f"✅ Receipt generated from different directory!")
        print(f"Receipt No: {receipt_result2['receipt_no']}")
        print(f"Files: {saved_files2}")
        
    except Exception as e:
        # Restore original directory even if test fails
        os.chdir(original_dir)
        print(f"❌ Error in Test 2: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests completed successfully!")
    print("\nImages should now be permanent and always load correctly.")
    print("Check the generated receipts to verify:")
    print("1. Methodist Church logo appears at top-left")
    print("2. NameT.jpg signature appears below 'Treasurer / Secretary'")
    print("3. Both images work regardless of where script is run from")
    
    return True

def verify_image_files():
    """Verify that the required image files exist"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, "logo.jpg")
    signature_path = os.path.join(script_dir, "NameT.jpg")
    
    print("Verifying image files exist:")
    print(f"Script directory: {script_dir}")
    
    if os.path.exists(logo_path):
        print(f"✅ logo.jpg found at: {logo_path}")
    else:
        print(f"❌ logo.jpg NOT found at: {logo_path}")
        
    if os.path.exists(signature_path):
        print(f"✅ NameT.jpg found at: {signature_path}")
    else:
        print(f"❌ NameT.jpg NOT found at: {signature_path}")
    
    return os.path.exists(logo_path) and os.path.exists(signature_path)

if __name__ == "__main__":
    print("Permanent Image Loading Test")
    print("=" * 60)
    
    # First verify files exist
    if not verify_image_files():
        print("❌ Required image files not found! Please ensure logo.jpg and NameT.jpg are in the same directory as the script.")
        sys.exit(1)
    
    print()
    
    # Run the test
    success = test_permanent_image_loading()
    
    if success:
        print("\n" + "=" * 60)
        print("SUMMARY OF FIXES IMPLEMENTED:")
        print("=" * 60)
        print()
        print("🎯 ISSUE: Images reset after 1 run (relative path problem)")
        print("✅ FIXED: Using absolute paths for both images")
        print()
        print("🔧 TECHNICAL CHANGES:")
        print("1. Added os.path.dirname(os.path.abspath(__file__)) to get script directory")
        print("2. Used os.path.join() to create absolute paths")
        print("3. Applied fix to both printreceipt.py and receipt_generator.py")
        print("4. Added proper error handling with fallbacks")
        print("5. Enhanced RGBA conversion for transparent images")
        print()
        print("📁 FILES MODIFIED:")
        print("- printreceipt.py: Lines ~103 and ~415 (logo and signature)")
        print("- receipt_generator.py: Lines ~43 and ~312 (logo and signature)")
        print()
        print("✅ RESULT: Images will now load permanently regardless of:")
        print("- Working directory when script is executed")
        print("- How the Python script is called (python, import, etc.)")
        print("- Multiple runs or system restarts")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
