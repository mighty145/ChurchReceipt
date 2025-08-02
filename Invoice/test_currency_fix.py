#!/usr/bin/env python3

"""
Test script to verify currency and contribution comments fixes
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from printreceipt import generate_receipt, save_receipt_multiple_formats

def test_currency_and_comments():
    """Test the receipt generation with multiple contributions"""
    
    # Test data with multiple contribution types
    test_data = {
        'InvoiceDate': '2025-08-02',
        'Name': 'Test User Multiple Contributions',
        'Address': 'Test Address, Test City',
        'MobileNumber': '9876543210',
        'TitheMonth': 'AUGUST',
        'TitheAmount': 1500.00,
        'MembershipMonth': 'AUGUST', 
        'MembershipAmount': 500.00,
        'BirthdayThankOffering': 250.00,
        'WeddingAnniversaryThankOffering': 0,
        'HomeMissionPledges': 0,
        'MissionAndEvangelismFund': 300.00,
        'StStephensSocialAidFund': 200.00,
        'SpecialThanksAmount': 100.00,
        'CharityFundAmount': 150.00,
        'DonationFor': 'Church Building',
        'DonationAmount': 1000.00,
        'HarvestAuctionComment': 'Special Items',
        'HarvestAuctionAmount': 750.00,
        'OnlineChequeNo': 'TEST123456',
        'PaymentMethod': 'ONLINE'
    }
    
    print("Testing receipt generation with multiple contributions...")
    print(f"Test data: {test_data['Name']}")
    print(f"Total expected contributions: Tithe, Membership, Birthday Offering, Mission & Evangelism, Social Aid, Special Thanks, Charity Fund, Donation, Harvest Auction")
    
    try:
        # Generate receipt
        receipt_result = generate_receipt(test_data)
        
        print(f"Receipt generated successfully!")
        print(f"Receipt No: {receipt_result['receipt_no']}")
        print(f"Date: {receipt_result['date']}")
        print(f"Name: {receipt_result['name']}")
        
        # Save as both JPG and PDF for verification
        filename = f"test_currency_fix_receipt_{receipt_result['receipt_no']}"
        saved_files = save_receipt_multiple_formats(receipt_result['image'], filename, ["jpg", "pdf"])
        
        print(f"Saved files: {saved_files}")
        print("\nPlease check the generated receipt to verify:")
        print("1. The contribution comments show all contribution types (not just 'Tithe')")
        print("2. All amounts are displayed with ₹ (Rupee) symbol, not $ (Dollar)")
        print("3. The summary total uses ₹ (Rupee) symbol")
        
        return True
        
    except Exception as e:
        print(f"Error generating receipt: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_single_contribution():
    """Test with only tithe contribution"""
    
    test_data = {
        'InvoiceDate': '2025-08-02',
        'Name': 'Test User Single Contribution', 
        'Address': 'Test Address, Test City',
        'MobileNumber': '9876543210',
        'TitheMonth': 'AUGUST',
        'TitheAmount': 2000.00,
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
        'OnlineChequeNo': 'TEST789012',
        'PaymentMethod': 'CASH'
    }
    
    print("\nTesting receipt generation with single contribution...")
    print(f"Test data: {test_data['Name']}")
    print(f"Expected contribution comment: Tithe")
    
    try:
        receipt_result = generate_receipt(test_data)
        
        filename = f"test_single_contribution_receipt_{receipt_result['receipt_no']}"
        saved_files = save_receipt_multiple_formats(receipt_result['image'], filename, ["jpg", "pdf"])
        
        print(f"Saved files: {saved_files}")
        print("Please verify the contribution comment shows only 'Tithe'")
        
        return True
        
    except Exception as e:
        print(f"Error generating receipt: {e}")
        return False

if __name__ == "__main__":
    print("Currency and Comments Fix Test")
    print("=" * 50)
    
    # Test multiple contributions
    success1 = test_currency_and_comments()
    
    # Test single contribution  
    success2 = test_single_contribution()
    
    if success1 and success2:
        print("\n✅ All tests completed successfully!")
        print("Please check the generated receipt files to verify the fixes.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
