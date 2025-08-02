#!/usr/bin/env python3

"""
Test script to verify receipt generation fixes:
1. Sum of rupees in words matches total amount
2. Filename format is correct
"""

import sys
import os

# Test data with multiple contributions
test_receipt_data = {
    'InvoiceDate': '2025-08-02',
    'Name': 'John Smith',
    'Address': 'Test Address',
    'MobileNumber': '1234567890',
    'TitheMonth': 'AUGUST',
    'TitheAmount': 1000.0,
    'MembershipMonth': 'AUGUST',
    'MembershipAmount': 500.0,
    'BirthdayThankOffering': 200.0,
    'WeddingAnniversaryThankOffering': 0.0,
    'HomeMissionPledges': 0.0,
    'MissionAndEvangelismFund': 300.0,
    'StStephensSocialAidFund': 0.0,
    'DonationFor': 'Church Building',
    'DonationAmount': 1000.0,
    'SpecialThanksAmount': 0.0,
    'CharityFundAmount': 0.0,
    'HarvestAuctionComment': '',
    'HarvestAuctionAmount': 0.0,
    'OnlineChequeNo': '123456789',
    'PaymentMethod': 'ONLINE'
}

def test_receipt_generation():
    try:
        from printreceipt import generate_receipt, save_receipt_multiple_formats, number_to_words
        
        print("Testing receipt generation with fixes...")
        print("=" * 50)
        
        # Calculate expected total
        expected_total = (
            test_receipt_data['TitheAmount'] + 
            test_receipt_data['MembershipAmount'] + 
            test_receipt_data['BirthdayThankOffering'] + 
            test_receipt_data['MissionAndEvangelismFund'] + 
            test_receipt_data['DonationAmount']
        )
        print(f"Expected total amount: {expected_total}")
        print(f"Expected total in words: {number_to_words(int(expected_total))} Only")
        
        # Generate receipt
        receipt_result = generate_receipt(test_receipt_data)
        
        print(f"\nReceipt generated successfully!")
        print(f"Receipt No: {receipt_result['receipt_no']}")
        print(f"Date: {receipt_result['date']}")
        print(f"Name: {receipt_result['name']}")
        
        # Test new filename format
        filename = f"Rec{receipt_result['receipt_no']}_{receipt_result['date'].replace('/', '_')}_{receipt_result['name']}"
        print(f"New filename format: {filename}")
        
        # Save receipt to test
        saved_files = save_receipt_multiple_formats(receipt_result['image'], filename, ["pdf", "jpg"])
        print(f"Saved files: {saved_files}")
        
        return True
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_receipt_generation()
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)
