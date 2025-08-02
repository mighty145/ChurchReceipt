#!/usr/bin/env python3
"""
Test script to verify receipt generation works independently
"""

import os
import sys

def test_receipt_generation():
    print("Testing receipt generation independently...")
    
    # Test data
    test_data = {
        'InvoiceDate': '2025-07-06',
        'Name': 'Test User',
        'Address': 'Test Address',
        'TitheMonth': 'JULY',
        'TitheAmount': 1000,
        'MembershipMonth': None,
        'MembershipAmount': None,
        'BirthdayThankOffering': None,
        'WeddingAnniversaryThankOffering': None,
        'HomeMissionPledges': None,
        'MissionAndEvangelismFund': None,
        'StStephensSocialAidFund': None,
        'SpecialThanksAmount': None,
        'CharityFundAmount': None,
        'DonationFor': None,
        'DonationAmount': None,
        'HarvestAuctionComment': None,
        'HarvestAuctionAmount': None,
        'OnlineChequeNo': '12345'
    }
    
    try:
        # Import receipt generation functions
        from printreceipt import generate_receipt, save_receipt_multiple_formats
        
        print("✓ Successfully imported printreceipt functions")
        
        # Generate receipt
        print("Generating receipt...")
        receipt_image = generate_receipt(test_data)
        print("✓ Receipt image generated")
        
        # Save files
        print("Saving files...")
        saved_files = save_receipt_multiple_formats(receipt_image, "test_independent", ["jpg", "pdf"])
        
        # Verify files
        print("\nFile verification:")
        for filename in saved_files:
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"✓ {filename} - {size} bytes")
            else:
                print(f"✗ {filename} - NOT FOUND")
        
        print("\n✓ Test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_receipt_generation()
    if success:
        print("\nReceipt generation is working correctly!")
    else:
        print("\nReceipt generation has issues that need to be fixed.")
