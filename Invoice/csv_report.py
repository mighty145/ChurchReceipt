"""
CSV Report Generator as alternative to Excel
"""

import csv
import os
from datetime import datetime
from offertory_report import OffertoryReportGenerator

class CSVReportGenerator(OffertoryReportGenerator):
    """Extended report generator that can create CSV reports"""
    
    def __init__(self, template_path=None):
        super().__init__(template_path)
        # Override output directory for CSV files
        self.csv_output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Receipts store", "CSV_Reports")
        os.makedirs(self.csv_output_dir, exist_ok=True)
    
    def generate_csv_offertory_report(self, service_date=None, service_type="Worship Service"):
        """Generate CSV version of offertory report"""
        if service_date is None:
            service_date = datetime.date.today().strftime("%Y-%m-%d")
        
        # Collect receipt data for the specified date
        receipts_data = self.collect_receipt_data(service_date)
        
        # Generate filename
        report_filename = f"Offertory_Report_{service_date}_{service_type.replace(' ', '_')}.csv"
        report_path = os.path.join(self.csv_output_dir, report_filename)
        
        # Create CSV report
        with open(report_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header information
            writer.writerow(['METHODIST ENGLISH CHURCH, KIRKEE'])
            writer.writerow(['Offertory (Cash and Cheque) Collection Record'])
            writer.writerow([f'Sunday - {service_type}'])
            writer.writerow([f'Date: {service_date}'])
            writer.writerow([])
            
            # Section A - Bag Offertory Collection
            writer.writerow(['A. Bag Offertory Collection - Cash'])
            writer.writerow(['Denomination', '1000x', '500x', '200x', '100x', '50x', '20x', '10x', 'Coins', 'Total'])
            
            # Calculate totals for cash contributions
            total_cash = 0
            for receipt in receipts_data:
                payment_method = receipt.get('PaymentMethod', 'CASH')
                if payment_method.upper() == 'CASH':
                    for field in ['TitheAmount', 'MembershipAmount', 'BirthdayThankOffering',
                                 'WeddingAnniversaryThankOffering', 'SpecialThanksAmount',
                                 'MissionAndEvangelismFund', 'CharityFundAmount',
                                 'StStephensSocialAidFund', 'HarvestAuctionAmount',
                                 'DonationAmount']:
                        amount = receipt.get(field, 0)
                        if amount:
                            try:
                                total_cash += float(amount)
                            except (ValueError, TypeError):
                                continue
            
            # Placeholder for manual cash breakdown (would need to be filled manually)
            writer.writerow(['1st Off', '-', '-', '-', '-', '-', '-', '-', '-', ''])
            writer.writerow(['Amount', '-', '-', '-', '-', '-', '-', '-', '-', total_cash])
            writer.writerow(['2nd Off', '-', '-', '-', '-', '-', '-', '-', '-', ''])
            writer.writerow(['Amount', '-', '-', '-', '-', '-', '-', '-', '-', ''])
            writer.writerow(['', '', '', '', '', '', '', '', 'TOTAL CASH - A', total_cash])
            writer.writerow([])
            
            # Section B - Special Offertory
            writer.writerow(['B. Special Offertory - Cash(B1) & Cheque(B1)'])
            writer.writerow(['No.', 'Name', 'Amount', 'Details'])
            
            sr_no = 1
            total_special = 0
            
            for receipt in receipts_data:
                name = receipt.get('Name', 'Unknown')
                if not name or name == 'Unknown':
                    continue
                
                # Calculate total amount for this person
                person_total = 0
                contributions = []
                
                # Check all contribution types
                contribution_types = {
                    'TitheAmount': 'Tithe',
                    'MembershipAmount': 'Membership',
                    'BirthdayThankOffering': 'Birthday Offering',
                    'WeddingAnniversaryThankOffering': 'Anniversary Offering',
                    'SpecialThanksAmount': 'Special Thanks',
                    'MissionAndEvangelismFund': 'Mission & Evangelism',
                    'CharityFundAmount': 'Charity Fund',
                    'StStephensSocialAidFund': 'Social Aid',
                    'HarvestAuctionAmount': 'Harvest Auction',
                    'DonationAmount': 'Donation'
                }
                
                for field, description in contribution_types.items():
                    amount = receipt.get(field, 0)
                    if amount:
                        try:
                            amount_val = float(amount)
                            if amount_val > 0:
                                person_total += amount_val
                                
                                # Add specific details
                                if field == 'TitheAmount' and receipt.get('TitheMonth'):
                                    contributions.append(f"{description} ({receipt.get('TitheMonth')})")
                                elif field == 'MembershipAmount' and receipt.get('MembershipMonth'):
                                    contributions.append(f"{description} ({receipt.get('MembershipMonth')})")
                                elif field == 'DonationAmount' and receipt.get('DonationFor'):
                                    contributions.append(f"{description} ({receipt.get('DonationFor')})")
                                elif field == 'HarvestAuctionAmount' and receipt.get('HarvestAuctionComment'):
                                    contributions.append(f"{description} ({receipt.get('HarvestAuctionComment')})")
                                else:
                                    contributions.append(description)
                        except (ValueError, TypeError):
                            continue
                
                if person_total > 0 and contributions:
                    writer.writerow([sr_no, name, person_total, "; ".join(contributions)])
                    total_special += person_total
                    sr_no += 1
            
            writer.writerow([])
            writer.writerow(['GRAND TOTAL CASH (A)', total_cash])
            writer.writerow(['GRAND TOTAL CHEQUE', ''])  # Would need cheque data
            writer.writerow(['GRAND TOTAL', 'A+B(I)', total_cash + total_special])
            writer.writerow([])
            
            # Summary information
            writer.writerow(['Report Summary'])
            writer.writerow(['Generated on:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow(['Total Individual Contributors:', sr_no - 1])
            writer.writerow(['Total Amount Collected:', total_cash + total_special])
            
        return report_path
    
    def generate_csv_summary_report(self, start_date=None, end_date=None):
        """Generate CSV summary report for date range"""
        summary = self.generate_summary_report(start_date, end_date)
        
        # Generate filename
        report_filename = f"Summary_Report_{summary['start_date']}_to_{summary['end_date']}.csv"
        report_path = os.path.join(self.csv_output_dir, report_filename)
        
        # Create CSV report
        with open(report_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header
            writer.writerow(['Church Receipt Summary Report'])
            writer.writerow([f"Date Range: {summary['start_date']} to {summary['end_date']}"])
            writer.writerow([f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
            writer.writerow([])
            
            # Summary statistics
            writer.writerow(['Summary Statistics'])
            writer.writerow(['Total Receipts', summary['total_receipts']])
            writer.writerow(['Total Amount', f"₹{summary['total_amount']:.2f}"])
            writer.writerow(['Service Days', len(summary['by_date'])])
            avg_per_receipt = summary['total_amount'] / summary['total_receipts'] if summary['total_receipts'] > 0 else 0
            writer.writerow(['Average per Receipt', f"₹{avg_per_receipt:.2f}"])
            writer.writerow([])
            
            # Daily breakdown
            writer.writerow(['Daily Breakdown'])
            writer.writerow(['Date', 'Number of Receipts', 'Total Amount', 'Average per Receipt'])
            
            for date, data in summary['by_date'].items():
                avg = data['amount'] / data['count'] if data['count'] > 0 else 0
                writer.writerow([date, data['count'], f"₹{data['amount']:.2f}", f"₹{avg:.2f}"])
        
        return report_path

def create_csv_offertory_report(service_date=None, service_type="Worship Service"):
    """Convenience function to generate CSV offertory report"""
    generator = CSVReportGenerator()
    return generator.generate_csv_offertory_report(service_date, service_type)

def create_csv_summary_report(start_date=None, end_date=None):
    """Convenience function to generate CSV summary report"""
    generator = CSVReportGenerator()
    return generator.generate_csv_summary_report(start_date, end_date)
