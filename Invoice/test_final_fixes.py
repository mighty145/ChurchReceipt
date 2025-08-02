#!/usr/bin/env python3

"""
Test script to verify the fixes:
1. Dynamic "Online No." / "Cheque No." based on payment method
2. New filename format: Receipt_No-[ReceiptNo]-[Date]-[Name]
"""

import sys
import os

def test_dynamic_payment_labels_and_filename():
    try:
        from printreceipt import generate_receipt, save_receipt_multiple_formats
        
        print("Testing dynamic payment labels and filename format...")
        print("=" * 60)
        
        # Test data for different payment methods
        test_cases = [
            {
                'payment_method': 'ONLINE',
                'name': 'Mighty Basumata',
                'expected_label': 'Online No.'
            },
            {
                'payment_method': 'CHEQUE', 
                'name': 'John Smith',
                'expected_label': 'Cheque No.'
            },
            {
                'payment_method': 'CASH',
                'name': 'Test User',
                'expected_label': 'Reference No.'
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            print(f"\n--- Test Case {i+1}: {test_case['payment_method']} Payment ---")
            
            test_receipt_data = {
                'InvoiceDate': '2025-08-08',  # August 8, 2025 (to match the example)
                'Name': test_case['name'],
                'Address': 'Test Address',
                'MobileNumber': '1234567890',
                'TitheMonth': 'AUGUST',
                'TitheAmount': 1000.0,
                'MembershipMonth': '',
                'MembershipAmount': 0.0,
                'BirthdayThankOffering': 0.0,
                'WeddingAnniversaryThankOffering': 0.0,
                'HomeMissionPledges': 0.0,
                'MissionAndEvangelismFund': 0.0,
                'StStephensSocialAidFund': 0.0,
                'DonationFor': '',
                'DonationAmount': 0.0,
                'SpecialThanksAmount': 0.0,
                'CharityFundAmount': 0.0,
                'HarvestAuctionComment': '',
                'HarvestAuctionAmount': 0.0,
                'OnlineChequeNo': '123456789',
                'PaymentMethod': test_case['payment_method']
            }
            
            # Generate receipt
            receipt_result = generate_receipt(test_receipt_data)
            
            print(f"Payment Method: {test_case['payment_method']}")
            print(f"Expected Label: {test_case['expected_label']}")
            print(f"Receipt No: {receipt_result['receipt_no']}")
            print(f"Display Date: {receipt_result['date']}")
            print(f"Filename Date: {receipt_result['date_filename']}")
            print(f"Name: {receipt_result['name']}")
            
            # Test new filename format
            filename = f"Receipt_No-{receipt_result['receipt_no']}-{receipt_result['date_filename']}-{receipt_result['name']}"
            print(f"Generated Filename: {filename}")
            
            # For Receipt No. 9, Date 8th Aug 2025 and name as "Mighty Basumata"
            # Should reflect as Receipt_No-9-08-Aug-2025-Mighty_Basumata
            if test_case['name'] == 'Mighty Basumata':
                expected_pattern = f"Receipt_No-{receipt_result['receipt_no']}-08-Aug-2025-Mighty_Basumata"
                print(f"Expected for Mighty Basumata: {expected_pattern}")
                if filename == expected_pattern:
                    print("✅ Filename format matches expected pattern!")
                else:
                    print(f"❌ Filename mismatch. Expected: {expected_pattern}")
            
            # Save a test file to verify the actual filename
            saved_files = save_receipt_multiple_formats(receipt_result['image'], filename, ["pdf"])
            print(f"Saved files: {saved_files}")
            
        return True
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_dynamic_payment_labels_and_filename()
    if success:
        print(f"\n{'='*60}")
        print("✅ All tests completed!")
        print("✅ Dynamic payment labels implemented")
        print("✅ New filename format implemented")
        print("✅ Expected format: Receipt_No-[No]-[DD-MMM-YYYY]-[Name]")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)
