#!/usr/bin/env python3

"""
Edge case tests for the currency and contribution comments fixes
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from printreceipt import generate_receipt, save_receipt_multiple_formats

def test_edge_cases():
    """Test edge cases for the contribution comments"""
    
    test_cases = [
        {
            'name': 'Empty/Zero Amounts',
            'data': {
                'InvoiceDate': '2025-08-02',
                'Name': 'Test Zero Amounts',
                'Address': 'Test Address',
                'MobileNumber': '9876543210',
                'TitheMonth': '',
                'TitheAmount': 0,
                'MembershipMonth': '', 
                'MembershipAmount': '',
                'BirthdayThankOffering': 0.00,
                'WeddingAnniversaryThankOffering': '',
                'HomeMissionPledges': None,
                'MissionAndEvangelismFund': 0,
                'StStephensSocialAidFund': '',
                'SpecialThanksAmount': None,
                'CharityFundAmount': 0.00,
                'DonationFor': '',
                'DonationAmount': '',
                'HarvestAuctionComment': '',
                'HarvestAuctionAmount': 0,
                'OnlineChequeNo': 'EMPTY001',
                'PaymentMethod': 'CASH'
            },
            'expected_comment': 'Contribution'
        },
        {
            'name': 'Only Donation',
            'data': {
                'InvoiceDate': '2025-08-02',
                'Name': 'Test Only Donation',
                'Address': 'Test Address',
                'MobileNumber': '9876543210',
                'TitheMonth': '',
                'TitheAmount': 0,
                'MembershipMonth': '', 
                'MembershipAmount': 0,
                'BirthdayThankOffering': 0,
                'WeddingAnniversaryThankOffering': 0,
                'HomeMissionPledges': 0,
                'MissionAndEvangelismFund': 0,
                'StStephensSocialAidFund': 0,
                'SpecialThanksAmount': 0,
                'CharityFundAmount': 0,
                'DonationFor': 'Building Fund',
                'DonationAmount': 500.00,
                'HarvestAuctionComment': '',
                'HarvestAuctionAmount': 0,
                'OnlineChequeNo': 'DONATION001',
                'PaymentMethod': 'ONLINE'
            },
            'expected_comment': 'Donation'
        },
        {
            'name': 'Two Contributions',
            'data': {
                'InvoiceDate': '2025-08-02',
                'Name': 'Test Two Contributions',
                'Address': 'Test Address',
                'MobileNumber': '9876543210',
                'TitheMonth': 'AUGUST',
                'TitheAmount': 1000.00,
                'MembershipMonth': 'AUGUST', 
                'MembershipAmount': 200.00,
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
                'OnlineChequeNo': 'TWO001',
                'PaymentMethod': 'CHEQUE'
            },
            'expected_comment': 'Tithe & Membership'
        }
    ]
    
    print("Testing edge cases for contribution comments...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Expected comment: {test_case['expected_comment']}")
        
        try:
            receipt_result = generate_receipt(test_case['data'])
            
            filename = f"test_edge_case_{i}_{test_case['name'].replace(' ', '_').replace('/', '_').lower()}_receipt_{receipt_result['receipt_no']}"
            saved_files = save_receipt_multiple_formats(receipt_result['image'], filename, ["jpg"])
            
            print(f"✅ Receipt generated: {saved_files[0]}")
            print(f"Receipt No: {receipt_result['receipt_no']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Edge case testing completed!")
    print("Please check the generated receipts to verify:")
    print("1. Empty amounts show 'Contribution' as comment")
    print("2. Single contributions show the specific type")
    print("3. Two contributions show 'Type1 & Type2' format")
    print("4. All amounts display with ₹ (Rupee) symbol")

if __name__ == "__main__":
    test_edge_cases()
