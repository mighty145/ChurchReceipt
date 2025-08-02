#!/usr/bin/env python3

# Test script to verify invoiceanalyzer integration with printreceipt
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_integration():
    """Test the integration between invoiceanalyzer and printreceipt"""
    
    # Simulate extracted data from invoice analyzer
    simulated_extracted_data = {
        'InvoiceDate': '2025-07-06',
        'Name': 'Diana Moses More',
        'Address': 'B-305 Cassiopeia Classic, Baner, Pune.',
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
        'OnlineChequeNo': ''
    }
    
    print("Testing integration between invoiceanalyzer and printreceipt...")
    print("Simulated extracted data:")
    for key, value in simulated_extracted_data.items():
        print(f"  {key}: {value}")
    
    try:
        # Import printreceipt functions
        from printreceipt import generate_receipt, save_receipt_multiple_formats
        
        print("\n✓ Successfully imported printreceipt functions")
        
        # Generate receipt directly with simulated data (skip interactive editor for test)
        print("Generating receipt with simulated data...")
        receipt_image = generate_receipt(simulated_extracted_data)
        
        # Save receipt
        saved_files = save_receipt_multiple_formats(receipt_image, "test_integration_receipt", ["jpg", "pdf"])
        
        print(f"\n✓ Integration test successful!")
        print(f"Generated files: {', '.join(saved_files)}")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error during integration: {e}")
        return False

if __name__ == "__main__":
    success = test_integration()
    if success:
        print("\n" + "="*50)
        print("INTEGRATION TEST PASSED")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("INTEGRATION TEST FAILED")
        print("="*50)
