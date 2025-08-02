#!/usr/bin/env python3
"""
Quick test to verify the os import fix
"""

def test_receipt_generation():
    """Test receipt generation to ensure os import issue is fixed"""
    try:
        print("Testing receipt generation after os import fix...")
        
        # Import the modules
        from printreceipt import generate_receipt, save_receipt_multiple_formats
        
        # Test data
        test_data = {
            'InvoiceDate': '2025-08-02',
            'Name': 'Test User Fix',
            'Address': 'Test Address',
            'TitheMonth': 'AUGUST',
            'TitheAmount': 1000,
            'PaymentMethod': 'CASH'
        }
        
        print("1. Generating receipt...")
        receipt_result = generate_receipt(test_data)
        
        print("2. Saving receipt (this should not fail with os import error)...")
        filename = f"Fix_Test_Receipt_{receipt_result['receipt_no']}"
        saved_files = save_receipt_multiple_formats(receipt_result['image'], filename, ['pdf'])
        
        print("3. Success! Receipt generated and saved:")
        for file_path in saved_files:
            print(f"   - {file_path}")
        
        print("\n✅ Fix successful - no os import error!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_receipt_generation()
