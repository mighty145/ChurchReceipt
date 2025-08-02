#!/usr/bin/env python3
"""
Simple test without user interaction
"""

def test_simple():
    try:
        from printreceipt import generate_receipt, save_receipt_multiple_formats
        
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
        
        print("Generating receipt...")
        receipt_image = generate_receipt(test_data)
        print("Receipt generated, saving files...")
        
        saved_files = save_receipt_multiple_formats(receipt_image, "simple_test", ["jpg"])
        print(f"Saved files: {saved_files}")
        
        # Check if file exists
        import os
        for file in saved_files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"File {file} exists: {size} bytes")
            else:
                print(f"File {file} does NOT exist")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()
