#!/usr/bin/env python3

"""
Test the web application's generate_receipt functionality with the new fixes
"""

import sys
import os

def test_web_app_receipt_generation():
    try:
        from web_invoice_app import app
        
        # Create a test client
        with app.test_client() as client:
            # Simulate form data for receipt generation
            form_data = {
                'InvoiceDate': '2025-08-02',
                'Name': 'Test User Web',
                'Address': '123 Test Street',
                'MobileNumber': '9876543210',
                'TitheMonth': 'AUGUST',
                'TitheAmount': '500',
                'MembershipMonth': 'AUGUST', 
                'MembershipAmount': '200',
                'BirthdayThankOffering': '100',
                'WeddingAnniversaryThankOffering': '',
                'HomeMissionPledges': '',
                'MissionAndEvangelismFund': '150',
                'StStephensSocialAidFund': '',
                'DonationFor': 'Test Donation',
                'DonationAmount': '250',
                'SpecialThanksAmount': '',
                'CharityFundAmount': '',
                'HarvestAuctionComment': '',
                'HarvestAuctionAmount': '',
                'OnlineChequeNo': '987654321',
                'PaymentMethod': 'ONLINE',
                'filename': 'test_receipt'
            }
            
            print("Testing web app receipt generation...")
            print("=" * 50)
            
            # Calculate expected total
            expected_total = 500 + 200 + 100 + 150 + 250  # 1200
            print(f"Expected total: {expected_total}")
            
            # Make a POST request to generate_receipt endpoint
            response = client.post('/generate_receipt', data=form_data, follow_redirects=True)
            
            print(f"Response status code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Receipt generation successful!")
                # Check if receipt files were created with new naming format
                import glob
                receipt_files = glob.glob("Rec*_*_*_Test_User_Web.*")
                if receipt_files:
                    print(f"✅ Found receipt files with new naming format: {receipt_files}")
                else:
                    print("⚠️ No receipt files found with new naming format")
                    all_files = glob.glob("*.pdf")
                    print(f"All PDF files: {all_files}")
                return True
            else:
                print(f"❌ Receipt generation failed with status {response.status_code}")
                print(f"Response: {response.get_data(as_text=True)}")
                return False
                
    except Exception as e:
        print(f"Error during web app test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_web_app_receipt_generation()
    if success:
        print("\n✅ Web app test passed!")
    else:
        print("\n❌ Web app test failed!")
        sys.exit(1)
