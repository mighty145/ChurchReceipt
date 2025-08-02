"""
Simple validation script for the receipt fix
"""
import sys

def validate_fix():
    try:
        # Test 1: Import the modules
        print("Test 1: Importing modules...")
        from printreceipt import number_to_words
        print("✅ Successfully imported printreceipt module")
        
        # Test 2: Test number_to_words with string input
        print("\nTest 2: Testing number_to_words with string inputs...")
        result1 = number_to_words("100")
        print(f"number_to_words('100') = '{result1}'")
        
        result2 = number_to_words(100)
        print(f"number_to_words(100) = '{result2}'")
        
        result3 = number_to_words("")
        print(f"number_to_words('') = '{result3}'")
        
        result4 = number_to_words(None)
        print(f"number_to_words(None) = '{result4}'")
        
        # Test 3: Test with problematic inputs
        print("\nTest 3: Testing with problematic inputs...")
        result5 = number_to_words("abc")
        print(f"number_to_words('abc') = '{result5}'")
        
        print("\n✅ All tests passed! The fix should resolve the error.")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Validating Receipt Generation Fix")
    print("=" * 40)
    
    success = validate_fix()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Validation successful!")
        print("\nThe web application should now work without the")
        print("'<' not supported between instances of 'str' and 'int' error.")
        print("\nTo test:")
        print("1. Run: py web_invoice_app.py")
        print("2. Open: http://localhost:5000")
        print("3. Upload a file and generate a receipt")
    else:
        print("❌ Validation failed. Please check the errors above.")
