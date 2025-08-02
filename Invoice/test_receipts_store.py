#!/usr/bin/env python3
"""
Test script to verify the new Receipts store functionality
"""

import os
import datetime
from printreceipt import generate_receipt, save_receipt_multiple_formats

def test_receipts_store():
    """Test receipt generation in the new Receipts store folder"""
    print("=" * 60)
    print("TESTING RECEIPTS STORE FUNCTIONALITY")
    print("=" * 60)
    
    # Test data
    test_data = {
        'InvoiceDate': '2025-08-02',
        'Name': 'Test User Receipts Store',
        'Address': 'Test Address, Pune',
        'TitheMonth': 'AUGUST',
        'TitheAmount': 1000,
        'MembershipAmount': 500,
        'PaymentMethod': 'CASH'
    }
    
    print("1. Generating test receipt...")
    receipt_result = generate_receipt(test_data)
    
    print("2. Saving receipt to Receipts store folder...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Test_Receipt_Store_{timestamp}"
    saved_files = save_receipt_multiple_formats(receipt_result['image'], filename, ['pdf', 'jpg'])
    
    print("3. Verifying files were saved...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    receipts_dir = os.path.join(script_dir, "Receipts store")
    
    print(f"   Receipts directory: {receipts_dir}")
    print(f"   Directory exists: {os.path.exists(receipts_dir)}")
    
    if os.path.exists(receipts_dir):
        print("   Files in Receipts store:")
        for file in os.listdir(receipts_dir):
            file_path = os.path.join(receipts_dir, file)
            file_size = os.path.getsize(file_path)
            print(f"   - {file} ({file_size} bytes)")
    
    print("4. Receipt information:")
    print(f"   Receipt No: {receipt_result['receipt_no']}")
    print(f"   Date: {receipt_result['date']}")
    print(f"   Name: {receipt_result['name']}")
    print(f"   Saved files: {saved_files}")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETED - Check the 'Receipts store' folder for generated files")
    print("=" * 60)

if __name__ == "__main__":
    test_receipts_store()
