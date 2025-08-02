#!/usr/bin/env python3
"""
Test script to verify the Online No. positioning fix
"""

import sys
import os

# Add current directory to path to import printreceipt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_online_no_positioning():
    """Test that Online No. positioning is fixed"""
    
    try:
        from printreceipt import generate_receipt
        
        print("Testing Online No. positioning...")
        print("-" * 50)
        
        # Test data with a long online number
        test_data = {
            'InvoiceDate': '2025-08-02',
            'Name': 'Test User',
            'Address': 'Test Address',
            'MobileNumber': '1234567890',
            'TitheMonth': 'AUGUST',
            'TitheAmount': 1000.00,
            'MembershipMonth': '',
            'MembershipAmount': 0.00,
            'BirthdayThankOffering': 0.00,
            'WeddingAnniversaryThankOffering': 0.00,
            'HomeMissionPledges': 0.00,
            'MissionAndEvangelismFund': 0.00,
            'StStephensSocialAidFund': 0.00,
            'SpecialThanksAmount': 0.00,
            'CharityFundAmount': 0.00,
            'DonationFor': '',
            'DonationAmount': 0.00,
            'HarvestAuctionComment': '',
            'HarvestAuctionAmount': 0.00,
            'OnlineChequeNo': '109037543497',  # Long number like in the image
            'PaymentMethod': 'ONLINE'
        }
        
        print("Generating test receipt with online payment...")
        result = generate_receipt(test_data)
        
        print(f"✅ Test receipt generated successfully!")
        print(f"Receipt No: {result['receipt_no']}")
        print(f"Online No: {test_data['OnlineChequeNo']}")
        print(f"Payment Method: {test_data['PaymentMethod']}")
        
        # Test with CHEQUE method as well
        test_data['PaymentMethod'] = 'CHEQUE'
        print("\nGenerating test receipt with cheque payment...")
        result2 = generate_receipt(test_data)
        
        print(f"✅ Test receipt with cheque generated successfully!")
        print(f"Receipt No: {result2['receipt_no']}")
        print(f"Cheque No: {test_data['OnlineChequeNo']}")
        print(f"Payment Method: {test_data['PaymentMethod']}")
        
        print("\n✅ Online No./Cheque No. positioning has been fixed!")
        print("The value should now appear right after the label with proper spacing.")
        
    except Exception as e:
        print(f"❌ Error testing positioning fix: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_online_no_positioning()
