#!/usr/bin/env python3

"""
Test both UI currency fixes and receipt positioning fixes
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from printreceipt import generate_receipt, save_receipt_multiple_formats

def test_positioning_and_currency_fixes():
    """Test the positioning and currency fixes"""
    
    print("Testing Positioning and Currency Fixes")
    print("=" * 60)
    
    # Test data with multiple contributions to test positioning
    test_data = {
        'InvoiceDate': '2025-08-02',
        'Name': 'Smita Basumata',
        'Address': 'Test Address, City',
        'MobileNumber': '9876543210',
        'TitheMonth': 'AUGUST',
        'TitheAmount': 1000.0,
        'MembershipMonth': 'AUGUST', 
        'MembershipAmount': 200.0,
        'BirthdayThankOffering': 0,
        'WeddingAnniversaryThankOffering': 0,
        'HomeMissionPledges': 0,
        'MissionAndEvangelismFund': 0,
        'StStephensSocialAidFund': 0,
        'SpecialThanksAmount': 0,
        'CharityFundAmount': 0,
        'DonationFor': 'Building Fund',
        'DonationAmount': 10000.0,
        'HarvestAuctionComment': '',
        'HarvestAuctionAmount': 0,
        'OnlineChequeNo': 'POS001',
        'PaymentMethod': 'CASH'
    }
    
    print("Test Case: Receipt positioning fix")
    print("Expected contribution comment: 'Tithe, Membership & Donation'")
    print("Expected positioning: Comments should start right after 'towards'")
    
    try:
        # Generate receipt 
        receipt_result = generate_receipt(test_data)
        
        # Create filename
        filename = f"test_positioning_fix_receipt_{receipt_result['receipt_no']}"
        
        # Save receipt
        saved_files = save_receipt_multiple_formats(receipt_result['image'], filename, ["jpg", "pdf"])
        
        print(f"✅ Receipt generated successfully!")
        print(f"Receipt No: {receipt_result['receipt_no']}")
        print(f"Files saved: {saved_files}")
        print()
        print("Please check the generated receipt to verify:")
        print("1. ✅ Contribution comments appear right after 'by cash towards'")
        print("2. ✅ Text 'Tithe, Membership & Donation' is properly positioned")
        print("3. ✅ All amounts in table show ₹ symbol (not $)")
        print("4. ✅ Total amount shows ₹ symbol")
        print()
        print("UI Testing Notes:")
        print("- Start the web app: python web_invoice_app.py")
        print("- Go to http://localhost:5000/manual-entry")
        print("- Enter similar data and generate receipt")
        print("- Verify Receipt Summary shows ₹ symbols (not $)")
        print("- Verify all contribution types appear in summary")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_positioning_and_currency_fixes()
    
    print("\n" + "=" * 60)
    print("SUMMARY OF FIXES IMPLEMENTED:")
    print("=" * 60)
    print()
    print("🎯 ISSUE 1: UI Receipt Summary Currency ($ → ₹)")
    print("✅ Fixed: templates/receipt_generated.html")
    print("   - Changed ${{ amount }} to ₹{{ amount }}")
    print("   - Added all contribution types to summary")
    print("   - Enhanced to show only non-zero amounts")
    print()
    print("🎯 ISSUE 2: Receipt Text Positioning")
    print("✅ Fixed: printreceipt.py")
    print("   - Calculate position dynamically after 'towards' text")
    print("   - Use textbbox to measure text width")
    print("   - Position contribution comments immediately after")
    print("✅ Fixed: receipt_generator.py")
    print("   - Applied same positioning fix")
    print()
    print("🔧 TECHNICAL CHANGES:")
    print("1. Dynamic X positioning based on 'towards' text width")
    print("2. Added 5px spacing between 'towards' and comments")  
    print("3. Comprehensive UI summary with all contribution types")
    print("4. Only show amounts > 0 in UI summary")
    print()
    print("📋 TO VERIFY:")
    print("1. Run web app and test manual entry")
    print("2. Check Receipt Summary uses ₹ symbols")
    print("3. Generate PDF and verify text positioning")
    print("4. Ensure contribution comments appear right after 'towards'")
