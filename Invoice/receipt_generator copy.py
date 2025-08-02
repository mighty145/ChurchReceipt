"""
Methodist Church Receipt Generator
This script generates official receipts for The Methodist English Church donations
"""

from PIL import Image, ImageDraw, ImageFont
import datetime
import random
import os

class ReceiptGenerator:
    def __init__(self):
        self.width = 800
        self.height = 1000
        self.fonts = self._load_fonts()
        self.colors = {
            'red': (220, 20, 60),
            'black': (0, 0, 0),
            'white': (255, 255, 255)
        }
    
    def _load_fonts(self):
        """Load fonts with fallback options"""
        try:
            return {
                'title': ImageFont.truetype("arial.ttf", 22),
                'header': ImageFont.truetype("arial.ttf", 14),
                'body': ImageFont.truetype("arial.ttf", 12),
                'small': ImageFont.truetype("arial.ttf", 10),
                'large_num': ImageFont.truetype("arial.ttf", 28)
            }
        except:
            # Fallback to default fonts
            default_font = ImageFont.load_default()
            return {
                'title': default_font,
                'header': default_font,
                'body': default_font,
                'small': default_font,
                'large_num': default_font
            }
    
    def _draw_church_logo(self, draw):
        """Draw the Methodist Church flame/cross logo"""
        # Outer flame shape
        draw.polygon([(30, 40), (45, 25), (60, 40), (65, 60), (60, 80), (50, 95), 
                      (40, 95), (30, 80), (25, 60)], fill=self.colors['red'])
        
        # Inner cross (white)
        draw.rectangle([(40, 45), (50, 85)], fill=self.colors['white'])
        draw.rectangle([(35, 58), (55, 68)], fill=self.colors['white'])
    
    def _draw_header(self, draw):
        """Draw church header information"""
        # Church Title
        draw.text((120, 35), "The Methodist English Church", 
                 fill=self.colors['black'], font=self.fonts['title'])
        
        # Church Address
        draw.text((120, 65), "39, Elphinstone Road, Kirkee, Pune - 411 003.", 
                 fill=self.colors['black'], font=self.fonts['header'])
        draw.text((120, 85), "(Bombay Public Trust Act - Regn No. D-36)", 
                 fill=self.colors['black'], font=self.fonts['small'])
        
        # Bible Verse in red
        verse1 = '"Give and it will be given to you, a good measure, pressed down,'
        verse2 = 'shaken together and running over will be given..." Luke 6:38'
        draw.text((50, 120), verse1, fill=self.colors['red'], font=self.fonts['small'])
        draw.text((50, 135), verse2, fill=self.colors['red'], font=self.fonts['small'])
    
    def _number_to_words(self, num):
        """Convert number to words"""
        ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 
                'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
        tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
        
        if num == 0:
            return "Zero"
        elif num < 10:
            return ones[num]
        elif num < 20:
            return teens[num - 10]
        elif num < 100:
            return tens[num // 10] + (' ' + ones[num % 10] if num % 10 != 0 else '')
        elif num < 1000:
            return ones[num // 100] + ' Hundred' + (' ' + self._number_to_words(num % 100) if num % 100 != 0 else '')
        elif num < 100000:
            return self._number_to_words(num // 1000) + ' Thousand' + (' ' + self._number_to_words(num % 1000) if num % 1000 != 0 else '')
        else:
            return str(num)  # Fallback for larger numbers
    
    def generate_receipt(self, invoice_data, output_filename="generated_receipt.png"):
        """Generate receipt image based on invoice data"""
        
        # Create white background
        img = Image.new('RGB', (self.width, self.height), self.colors['white'])
        draw = ImageDraw.Draw(img)
        
        # Draw church logo and header
        self._draw_church_logo(draw)
        self._draw_header(draw)
        
        # Receipt number (use provided or generate random)
        receipt_no = invoice_data.get('ReceiptNo', str(random.randint(9000, 9999)))
        
        # Receipt details section
        y_pos = 180
        draw.text((50, y_pos), "Rec No.", fill=self.colors['black'], font=self.fonts['body'])
        draw.text((150, y_pos), receipt_no, fill=self.colors['black'], font=self.fonts['large_num'])
        
        # Date formatting
        try:
            date_obj = datetime.datetime.strptime(invoice_data['InvoiceDate'], '%Y-%m-%d')
            date_formatted = date_obj.strftime('%d/%m/%Y')
        except:
            date_formatted = invoice_data['InvoiceDate']
        
        draw.text((500, y_pos), f"Date : {date_formatted}", 
                 fill=self.colors['black'], font=self.fonts['body'])
        
        # Recipient information
        y_pos += 40
        draw.text((50, y_pos), "Received with thanks from", 
                 fill=self.colors['black'], font=self.fonts['body'])
        name_start_x = 280
        draw.text((name_start_x, y_pos), invoice_data['Name'], 
                 fill=self.colors['black'], font=self.fonts['body'])
        draw.line([(name_start_x, y_pos + 20), (700, y_pos + 20)], 
                 fill=self.colors['black'], width=1)
        
        # Amount in words
        y_pos += 35
        draw.text((50, y_pos), "a sum of rupees", 
                 fill=self.colors['black'], font=self.fonts['body'])
        
        total_amount = self._calculate_total_amount(invoice_data)
        if total_amount > 0:
            amount_words = self._number_to_words(total_amount) + " Only"
            amount_start_x = 200
            draw.text((amount_start_x, y_pos), amount_words, 
                     fill=self.colors['black'], font=self.fonts['body'])
            draw.line([(amount_start_x, y_pos + 20), (700, y_pos + 20)], 
                     fill=self.colors['black'], width=1)
        
        # Payment method
        y_pos += 35
        draw.text((50, y_pos), "by cheque / cash / online towards", 
                 fill=self.colors['black'], font=self.fonts['body'])
        tithe_start_x = 350
        draw.text((tithe_start_x, y_pos), "Tithe", 
                 fill=self.colors['black'], font=self.fonts['body'])
        draw.line([(tithe_start_x, y_pos + 20), (500, y_pos + 20)], 
                 fill=self.colors['black'], width=1)
        
        # Draw donation table
        y_pos = self._draw_donation_table(draw, invoice_data, y_pos + 50)
        
        # Footer information
        self._draw_footer(draw, y_pos)
        
        # Save the image to "Receipts store" folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        receipts_dir = os.path.join(script_dir, "Receipts store")
        os.makedirs(receipts_dir, exist_ok=True)
        
        # Create full path to save in "Receipts store" folder
        full_output_path = os.path.join(receipts_dir, output_filename)
        img.save(full_output_path)
        return img, full_output_path
    
    def _calculate_total_amount(self, invoice_data):
        """Calculate total amount from all donation types"""
        total = 0
        amount_fields = ['TitheAmount', 'MembershipAmount', 'BirthdayThankOffering', 
                        'WeddingAnniversaryThankOffering', 'MissionAndEvangelismFund', 
                        'StStephensSocialAidFund']
        
        for field in amount_fields:
            value = invoice_data.get(field)
            if value and value != 'None' and str(value).isdigit():
                total += int(value)
        
        return total
    
    def _draw_donation_table(self, draw, invoice_data, start_y):
        """Draw the donation items table"""
        y_pos = start_y
        
        # Table header
        draw.rectangle([(50, y_pos), (750, y_pos + 30)], 
                      outline=self.colors['black'], width=2)
        draw.text((680, y_pos + 5), "Rs.", fill=self.colors['black'], font=self.fonts['body'])
        draw.text((720, y_pos + 5), "Ps.", fill=self.colors['black'], font=self.fonts['body'])
        
        # Table items
        table_items = [
            ("Monthly Tithe for", invoice_data.get('TitheMonth', ''), invoice_data.get('TitheAmount', '')),
            ("Membership Fee for", invoice_data.get('MembershipMonth', ''), invoice_data.get('MembershipAmount', '')),
            ("Birthday Offering", '', invoice_data.get('BirthdayThankOffering', '')),
            ("Wedding Anniversary Offering", '', invoice_data.get('WeddingAnniversaryThankOffering', '')),
            ("Special Thanks Offering", '', ''),
            ("Mission & Evangelism", '', invoice_data.get('MissionAndEvangelismFund', '')),
            ("Charity Relief Fund", '', ''),
            ("St. Stephen's Social aid", '', invoice_data.get('StStephensSocialAidFund', '')),
            ("Harvest Auction", '', ''),
            ("Donation for", invoice_data.get('DonationFor', ''), '')
        ]
        
        y_pos += 30
        total_amount = 0
        
        for item, detail, amount in table_items:
            draw.rectangle([(50, y_pos), (750, y_pos + 30)], 
                          outline=self.colors['black'], width=1)
            
            # Checkbox and amount
            if amount and amount != 'None' and amount != '':
                # Checked box
                draw.rectangle([(60, y_pos + 8), (75, y_pos + 23)], 
                              outline=self.colors['black'], width=2)
                draw.text((63, y_pos + 5), "✓", fill=self.colors['black'], font=self.fonts['body'])
                draw.text((680, y_pos + 5), str(amount), 
                         fill=self.colors['black'], font=self.fonts['body'])
                if str(amount).isdigit():
                    total_amount += int(amount)
            else:
                # Empty box
                draw.rectangle([(60, y_pos + 8), (75, y_pos + 23)], 
                              outline=self.colors['black'], width=1)
            
            # Item description
            full_text = item
            if detail and detail != 'None' and detail != '':
                full_text += f" {detail}"
            draw.text((85, y_pos + 5), full_text, 
                     fill=self.colors['black'], font=self.fonts['body'])
            
            y_pos += 30
        
        # Total row
        draw.rectangle([(50, y_pos), (750, y_pos + 40)], 
                      outline=self.colors['black'], width=2)
        draw.text((600, y_pos + 10), "Total", 
                 fill=self.colors['black'], font=self.fonts['header'])
        draw.text((680, y_pos + 10), str(total_amount), 
                 fill=self.colors['black'], font=self.fonts['header'])
        
        return y_pos + 40
    
    def _draw_footer(self, draw, start_y):
        """Draw footer with cheque number and signature"""
        y_pos = start_y + 20
        
        # Cheque/Online number
        draw.text((50, y_pos), "Online / Cheque No.", 
                 fill=self.colors['black'], font=self.fonts['body'])
        cheque_no = f"5185229693{random.randint(10, 99)}"
        draw.text((200, y_pos), cheque_no, 
                 fill=self.colors['black'], font=self.fonts['body'])
        
        # Signature
        draw.text((600, y_pos), "Treasurer / Secretary", 
                 fill=self.colors['black'], font=self.fonts['body'])
        draw.text((650, y_pos + 20), "APS", 
                 fill=self.colors['black'], font=self.fonts['body'])

def create_receipt_from_data(data_dict, output_file="church_receipt.png"):
    """Convenience function to create receipt from data dictionary"""
    generator = ReceiptGenerator()
    image, filename = generator.generate_receipt(data_dict, output_file)
    return image, filename

# Example usage and test data
if __name__ == "__main__":
    # Sample invoice data
    sample_data = {
        'InvoiceDate': '2025-07-06',
        'Name': 'Diana Moses More.',
        'Address': 'B305 Cassiopeia Classic, Banen, Pune.',
        'TitheMonth': 'JULY',
        'TitheAmount': 1000,
        'MembershipMonth': None,
        'MembershipAmount': None,
        'BirthdayThankOffering': None,
        'WeddingAnniversaryThankOffering': None,
        'HomeMissionPledges': None,
        'MissionAndEvangelismFund': None,
        'StStephensSocialAidFund': None,
        'DonationFor': None,
        'ReceiptNo': '9238'  # Optional - will be auto-generated if not provided
    }
    
    # Generate receipt
    generator = ReceiptGenerator()
    receipt_image, filename = generator.generate_receipt(sample_data, "final_receipt.png")
    
    print(f"Receipt generated successfully as '{filename}'")
    print(f"Receipt details:")
    print(f"  Date: {sample_data['InvoiceDate']}")
    print(f"  Name: {sample_data['Name']}")
    print(f"  Tithe Month: {sample_data['TitheMonth']}")
    print(f"  Amount: Rs. {sample_data['TitheAmount']}")
    
    # Try to display the image
    try:
        receipt_image.show()
    except:
        print(f"Image saved but cannot display automatically. Please open '{filename}' to view.")
