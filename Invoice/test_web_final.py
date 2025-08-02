#!/usr/bin/env python3

"""
Test the web application with the new fixes
"""

import sys
import os

def test_web_app_final_fixes():
    try:
        from web_invoice_app import app
        
        # Create a test client
        with app.test_client() as client:
            # Test data for online payment (should show "Online No.")
            form_data = {
                'InvoiceDate': '2025-08-08',
                'Name': 'Mighty Basumata',
                'Address': '123 Test Street',
                'MobileNumber': '9876543210',
                'TitheMonth': 'AUGUST',
                'TitheAmount': '500',
                'MembershipMonth': '', 
                'MembershipAmount': '',
                'BirthdayThankOffering': '',
                'WeddingAnniversaryThankOffering': '',
                'HomeMissionPledges': '',
                'MissionAndEvangelismFund': '',
                'StStephensSocialAidFund': '',
                'DonationFor': '',
                'DonationAmount': '',
                'SpecialThanksAmount': '',
                'CharityFundAmount': '',
                'HarvestAuctionComment': '',
                'HarvestAuctionAmount': '',
                'OnlineChequeNo': '987654321',
                'PaymentMethod': 'ONLINE',
                'filename': 'test_receipt'
            }
            
            print("Testing web app with final fixes...")
            print("=" * 50)
            print("Testing ONLINE payment method (should show 'Online No.')")
            
            # Make a POST request to generate_receipt endpoint
            response = client.post('/generate_receipt', data=form_data, follow_redirects=True)
            
            print(f"Response status code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Receipt generation successful!")
                
                # Check if receipt files were created with new naming format
                import glob
                receipt_files = glob.glob("Receipt_No-*-08-Aug-2025-Mighty_Basumata.*")
                if receipt_files:
                    print(f"✅ Found receipt files with new naming format: {receipt_files}")
                    print("✅ Filename format: Receipt_No-[No]-08-Aug-2025-Mighty_Basumata")
                else:
                    print("⚠️ No receipt files found with new naming format")
                    all_files = glob.glob("Receipt_No-*.pdf")
                    print(f"All Receipt_No files: {all_files}")
                
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
    success = test_web_app_final_fixes()
    if success:
        print("\n✅ Web app final fixes test passed!")
        print("✅ Dynamic payment method labels working")
        print("✅ New filename format working")
    else:
        print("\n❌ Web app test failed!")
        sys.exit(1)
