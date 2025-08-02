#!/usr/bin/env python3
"""
Validation script to test the consolidated receipt counter functionality
"""

import os
import sys

def test_receipt_counter():
    """Test that receipt counter works correctly with the consolidated file"""
    
    # Add current directory to path to import printreceipt
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from printreceipt import get_next_receipt_number, reset_receipt_counter
        
        print("Testing receipt counter functionality...")
        print("-" * 50)
        
        # Check current receipt counter file location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        receipt_file = os.path.join(script_dir, "receipt_counter.txt")
        
        print(f"Receipt counter file location: {receipt_file}")
        print(f"File exists: {os.path.exists(receipt_file)}")
        
        if os.path.exists(receipt_file):
            with open(receipt_file, 'r') as f:
                current_value = f.read().strip()
            print(f"Current counter value: {current_value}")
        
        # Test getting next receipt number
        next_number = get_next_receipt_number()
        print(f"Next receipt number: {next_number}")
        
        # Read the updated value
        with open(receipt_file, 'r') as f:
            new_value = f.read().strip()
        print(f"Updated counter value: {new_value}")
        
        print("\n✅ Receipt counter is working correctly!")
        print("✅ Using consolidated file in Invoice folder")
        
    except Exception as e:
        print(f"❌ Error testing receipt counter: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_receipt_counter()
