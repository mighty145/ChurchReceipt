#!/usr/bin/env python3

# Test script to verify the receipt generation with editing capability
import sys
sys.path.append('.')
from printreceipt import generate_receipt, save_receipt_multiple_formats

# Test data
test_invoice_data = {
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
    'OnlineChequeNo': '45435345'
}

print("Testing receipt generation...")
receipt_image = generate_receipt(test_invoice_data)
saved_files = save_receipt_multiple_formats(receipt_image, "test_receipt", ["jpg", "pdf"])
print(f"Test completed. Generated files: {', '.join(saved_files)}")
