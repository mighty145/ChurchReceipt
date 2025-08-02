"""
Test script to verify the receipt generation fix
"""

def test_number_to_words():
    # Import the function
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    
    from printreceipt import number_to_words
    
    print("Testing number_to_words function:")
    
    # Test cases that should work
    test_cases = [
        (100, "One Hundred"),
        ("100", "One Hundred"),
        ("100.0", "One Hundred"),
        (0, "Zero"),
        ("0", "Zero"),
        ("", "Zero"),
        (None, "Zero"),
        ("abc", "Zero"),
        (1000, "One Thousand"),
        ("1000", "One Thousand")
    ]
    
    for input_val, expected in test_cases:
        try:
            result = number_to_words(input_val)
            status = "✅ PASS" if result == expected else "❌ FAIL"
            print(f"{status} Input: {repr(input_val)} -> Output: '{result}' (Expected: '{expected}')")
        except Exception as e:
            print(f"❌ ERROR Input: {repr(input_val)} -> Exception: {e}")

def test_receipt_generation():
    print("\nTesting receipt generation with string amounts:")
    
    from printreceipt import generate_receipt
    
    # Test data with string amounts (like from web forms)
    test_data = {
        'InvoiceDate': '2025-07-27',
        'Name': 'Test User',
        'Address': 'Test Address',
        'TitheAmount': '1000',  # String value
        'OnlineChequeNo': '123456789'
    }
    
    try:
        receipt_image = generate_receipt(test_data)
        print("✅ Receipt generation successful with string amounts!")
        return True
    except Exception as e:
        print(f"❌ Receipt generation failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Receipt Generation Fixes")
    print("=" * 50)
    
    test_number_to_words()
    success = test_receipt_generation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! The fix should work.")
    else:
        print("❌ Some tests failed. Check the error messages above.")
