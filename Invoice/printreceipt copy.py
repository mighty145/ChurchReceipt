""" Input to be used
InvoiceDate: 2025-07-06
Name: Diana Moses More.
Address: B305 Cassiopeia Classic, Banen, Pune.
TitheMonth: JULY
TitheAmount: 1000
MembershipMonth: None
MembershipAmount: None
BirthdayThankOffering: None
WeddingAnniversaryThankOffering: None
HomeMissionPledges: None
MissionAndEvangelismFund: None
StStephensSocialAidFund: None
SpecialThanksAmount: None
CharityFundAmount: None
DonationFor: None
DonationAmount: None
HarvestAuctionComment: None
HarvestAuctionAmount: None
OnlineChequeNo: 
"""

from PIL import Image, ImageDraw, ImageFont
import datetime
import random
import os

def get_next_receipt_number():
    """Get the next receipt number from file, increment and save"""
    # Use absolute path to ensure we always use the receipt_counter.txt in Invoice folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    receipt_file = os.path.join(script_dir, "receipt_counter.txt")
    try:
        if os.path.exists(receipt_file):
            with open(receipt_file, 'r') as f:
                current_number = int(f.read().strip())
        else:
            current_number = 0
        
        next_number = current_number + 1
        
        # Save the next number
        with open(receipt_file, 'w') as f:
            f.write(str(next_number))
        
        return str(next_number)
    except:
        return "1"

def reset_receipt_counter():
    """Reset receipt counter to 1"""
    # Use absolute path to ensure we always use the receipt_counter.txt in Invoice folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    receipt_file = os.path.join(script_dir, "receipt_counter.txt")
    with open(receipt_file, 'w') as f:
        f.write("0")
    print("Receipt counter reset to 1")

def generate_receipt(invoice_data, output_formats=["jpg", "pdf"]):
    # Receipt dimensions (1/4th of A4 size: A4 is 210x297mm, 1/4th is approximately 210x74mm)
    # At 96 DPI: 210mm = ~794px, 74mm = ~280px, but we need more height for content
    width, height = 500, 700
    
    # Create a white background
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to use different font sizes
    try:
        title_font = ImageFont.truetype("arial.ttf", 22)
        title_bold_font = ImageFont.truetype("arialbd.ttf", 22)  # Bold version
        header_font = ImageFont.truetype("arial.ttf", 14)
        header_bold_font = ImageFont.truetype("arialbd.ttf", 14)  # Bold version
        body_font = ImageFont.truetype("arial.ttf", 12)
        body_bold_font = ImageFont.truetype("arialbd.ttf", 12)  # Bold version
        small_font = ImageFont.truetype("arial.ttf", 10)
        large_num_font = ImageFont.truetype("arial.ttf", 28)
    except:
        # Fallback to default font if arial is not available
        title_font = ImageFont.load_default()
        title_bold_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        header_bold_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        body_bold_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        large_num_font = ImageFont.load_default()
    
    # Colors
    red_color = (220, 20, 60)
    black_color = (0, 0, 0)
    
    # Load and place the Methodist Church Logo
    try:
        logo = Image.open("logo.jpg")
        # Resize logo to fit appropriately (reduced size to avoid overlap)
        logo_size = (50, 50)
        logo = logo.resize(logo_size, Image.Resampling.LANCZOS)
        # Position logo on the left side
        logo_x = 15
        logo_y = 20
        img.paste(logo, (logo_x, logo_y))
    except:
        # Fallback: Draw Methodist Church Logo area (simplified flame/cross symbol)
        # Outer flame shape
        draw.polygon([(30, 40), (45, 25), (60, 40), (65, 60), (60, 80), (50, 95), 
                      (40, 95), (30, 80), (25, 60)], fill=red_color)
        
        # Inner cross
        draw.rectangle([(40, 45), (50, 85)], fill='white', width=2)
        draw.rectangle([(35, 58), (55, 68)], fill='white', width=2)
    
    # Church Title (centered, moved higher, bold)
    title_text = "The Methodist English Church"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_bold_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 25), title_text, fill=black_color, font=title_bold_font)
    
    # Church Address (centered)
    address_text = "39, Elphinstone Road, Kirkee, Pune - 411 003."
    address_bbox = draw.textbbox((0, 0), address_text, font=header_font)
    address_width = address_bbox[2] - address_bbox[0]
    address_x = (width - address_width) // 2
    draw.text((address_x, 55), address_text, fill=black_color, font=header_font)
    
    # Registration info (centered)
    reg_text = "(Bombay Public Trust Act - Regn No. D-36)"
    reg_bbox = draw.textbbox((0, 0), reg_text, font=small_font)
    reg_width = reg_bbox[2] - reg_bbox[0]
    reg_x = (width - reg_width) // 2
    draw.text((reg_x, 75), reg_text, fill=black_color, font=small_font)
    
    # Bible Verse in red (centered) - reduced space from registration line
    verse_text = '"Give and it will be given to you, a good measure, pressed down,'
    verse_text2 = 'shaken together and running over will be given..." Luke 6:38'
    
    # Center first line of Bible verse
    verse1_bbox = draw.textbbox((0, 0), verse_text, font=small_font)
    verse1_width = verse1_bbox[2] - verse1_bbox[0]
    verse1_x = (width - verse1_width) // 2
    draw.text((verse1_x, 95), verse_text, fill=red_color, font=small_font)
    
    # Center second line of Bible verse
    verse2_bbox = draw.textbbox((0, 0), verse_text2, font=small_font)
    verse2_width = verse2_bbox[2] - verse2_bbox[0]
    verse2_x = (width - verse2_width) // 2
    draw.text((verse2_x, 110), verse_text2, fill=red_color, font=small_font)
    
    # Generate receipt number (dynamic)
    receipt_no = invoice_data.get('ReceiptNo', get_next_receipt_number())
    
    # Receipt details header (reduced space after Bible verse)
    y_pos = 135
    draw.text((50, y_pos), "Rec No.", fill=black_color, font=body_font)
    # Align receipt number with "Rec No." text using smaller font
    draw.text((110, y_pos), receipt_no, fill=black_color, font=header_font)
    
    # Date (formatted to match the image format)
    date_formatted = datetime.datetime.strptime(invoice_data['InvoiceDate'], '%Y-%m-%d').strftime('%d/%m/%Y')
    draw.text((320, y_pos), f"Date : {date_formatted}", fill=black_color, font=body_font)
    
    y_pos += 35
    draw.text((50, y_pos), "Received with thanks from", fill=black_color, font=body_font)
    # Name in bold with underline
    name_start_x = 220
    draw.text((name_start_x, y_pos), invoice_data['Name'], fill=black_color, font=body_bold_font)
    # Draw underline for name
    name_bbox = draw.textbbox((name_start_x, y_pos), invoice_data['Name'], font=body_bold_font)
    draw.line([(name_start_x, name_bbox[3] + 2), (name_bbox[2], name_bbox[3] + 2)], fill=black_color, width=1)
    
    y_pos += 20
    draw.text((50, y_pos), "a sum of rupees", fill=black_color, font=body_font)
    
    # Convert amount to words in bold with underline
    amount = invoice_data.get('TitheAmount', 0)
    if amount:
        amount_words = number_to_words(amount) + " Only"
        amount_start_x = 160
        draw.text((amount_start_x, y_pos), amount_words, fill=black_color, font=body_bold_font)
        # Draw underline for amount words
        amount_bbox = draw.textbbox((amount_start_x, y_pos), amount_words, font=body_bold_font)
        draw.line([(amount_start_x, amount_bbox[3] + 2), (amount_bbox[2], amount_bbox[3] + 2)], fill=black_color, width=1)
    
    y_pos += 20
    draw.text((50, y_pos), "by cheque / cash / online towards", fill=black_color, font=body_font)
    tithe_start_x = 280
    draw.text((tithe_start_x, y_pos), "Tithe", fill=black_color, font=body_bold_font)
    # Draw underline for "Tithe"
    tithe_bbox = draw.textbbox((tithe_start_x, y_pos), "Tithe", font=body_bold_font)
    draw.line([(tithe_start_x, tithe_bbox[3] + 2), (tithe_bbox[2], tithe_bbox[3] + 2)], fill=black_color, width=1)
    
    # Draw table (reduced space)
    y_pos += 25
    table_top = y_pos
    
    # Table headers
    draw.rectangle([(50, y_pos), (450, y_pos + 30)], outline=black_color, width=2)
    # Draw vertical line before Rs column (more space)
    draw.line([(340, y_pos), (340, y_pos + 30)], fill=black_color, width=1)
    # Move Amount(₹) header more to the right
    draw.text((375, y_pos + 5), "Amount(₹)", fill=black_color, font=body_font)
    
    # Table rows
    table_items = [
        ("Monthly Tithe for", invoice_data.get('TitheMonth', ''), invoice_data.get('TitheAmount', '')),
        ("Membership Fee for", invoice_data.get('MembershipMonth', ''), invoice_data.get('MembershipAmount', '')),
        ("Birthday Offering", '', invoice_data.get('BirthdayThankOffering', '')),
        ("Wedding Anniversary Offering", '', invoice_data.get('WeddingAnniversaryThankOffering', '')),
        ("Special Thanks Offering", '', invoice_data.get('SpecialThanksAmount', '')),
        ("Mission & Evangelism", '', invoice_data.get('MissionAndEvangelismFund', '')),
        ("Charity Relief Fund", '', invoice_data.get('CharityFundAmount', '')),
        ("St. Stephen's Social aid", '', invoice_data.get('StStephensSocialAidFund', '')),
        ("Harvest Auction", invoice_data.get('HarvestAuctionComment', ''), invoice_data.get('HarvestAuctionAmount', '')),
        ("Donation for", invoice_data.get('DonationFor', ''), invoice_data.get('DonationAmount', ''))
    ]
    
    y_pos += 30
    total_amount = 0
    
    for item, detail, amount in table_items:
        draw.rectangle([(50, y_pos), (450, y_pos + 30)], outline=black_color, width=1)
        
        # Draw vertical line before Rs column (more space)
        draw.line([(340, y_pos), (340, y_pos + 30)], fill=black_color, width=1)
        
        # Check box - tick at the beginning of line if amount exists
        if amount and amount != 'None' and amount != '':
            draw.rectangle([(60, y_pos + 8), (75, y_pos + 23)], outline=black_color, width=2)
            # Better tick mark
            draw.text((63, y_pos + 6), "✓", fill=black_color, font=body_bold_font)
            # Right-align the amount in the Rs column
            amount_text = str(amount)
            amount_bbox = draw.textbbox((0, 0), amount_text, font=body_font)
            amount_width = amount_bbox[2] - amount_bbox[0]
            amount_x = 440 - amount_width  # Right-align within the column
            draw.text((amount_x, y_pos + 5), amount_text, fill=black_color, font=body_font)
            total_amount += int(amount) if str(amount).isdigit() else 0
        else:
            draw.rectangle([(60, y_pos + 8), (75, y_pos + 23)], outline=black_color, width=1)
        
        # Item text
        full_text = f"{item}"
        if detail and detail != 'None':
            # Check if this is TitheMonth, MembershipMonth, HarvestAuctionComment, or DonationFor to make it bold
            if item in ["Monthly Tithe for", "Membership Fee for"] and detail:
                # Draw the item text in regular font
                draw.text((85, y_pos + 5), full_text + " ", fill=black_color, font=body_font)
                # Calculate the width of the item text to position the detail text
                item_bbox = draw.textbbox((0, 0), full_text + " ", font=body_font)
                item_width = item_bbox[2] - item_bbox[0]
                # Draw the detail (month) in bold font
                detail_x = 85 + item_width
                draw.text((detail_x, y_pos + 5), detail, fill=black_color, font=body_bold_font)
                # Draw underline for the detail (month)
                detail_bbox = draw.textbbox((detail_x, y_pos + 5), detail, font=body_bold_font)
                draw.line([(detail_x, detail_bbox[3] + 2), (detail_bbox[2], detail_bbox[3] + 2)], fill=black_color, width=1)
            elif item in ["Harvest Auction", "Donation for"] and detail:
                # Draw the item text in regular font
                draw.text((85, y_pos + 5), full_text + " ", fill=black_color, font=body_font)
                # Calculate the width of the item text to position the detail text
                item_bbox = draw.textbbox((0, 0), full_text + " ", font=body_font)
                item_width = item_bbox[2] - item_bbox[0]
                # Draw the detail (comment/purpose) in bold font
                detail_x = 85 + item_width
                draw.text((detail_x, y_pos + 5), detail, fill=black_color, font=body_bold_font)
                # Draw underline for the detail (comment/purpose)
                detail_bbox = draw.textbbox((detail_x, y_pos + 5), detail, font=body_bold_font)
                draw.line([(detail_x, detail_bbox[3] + 2), (detail_bbox[2], detail_bbox[3] + 2)], fill=black_color, width=1)
            else:
                full_text += f" {detail}"
                draw.text((85, y_pos + 5), full_text, fill=black_color, font=body_font)
        else:
            draw.text((85, y_pos + 5), full_text, fill=black_color, font=body_font)
        
        y_pos += 30
    
    # Total row
    draw.rectangle([(50, y_pos), (450, y_pos + 40)], outline=black_color, width=2)
    # Draw vertical line before Rs column in total row (more space)
    draw.line([(340, y_pos), (340, y_pos + 40)], fill=black_color, width=1)
    draw.text((290, y_pos + 10), "Total", fill=black_color, font=header_font)
    # Right-align the total amount in bold
    total_text = str(total_amount)
    total_bbox = draw.textbbox((0, 0), total_text, font=header_bold_font)
    total_width = total_bbox[2] - total_bbox[0]
    total_x = 440 - total_width  # Right-align within the column
    draw.text((total_x, y_pos + 10), total_text, fill=black_color, font=header_bold_font)
    
    # Online/Cheque number (reduced space)
    y_pos += 50
    draw.text((50, y_pos), "Online / Cheque No.", fill=black_color, font=body_font)
    cheque_no = invoice_data.get('OnlineChequeNo', '')
    # Calculate proper position for the value based on label width
    label_bbox = draw.textbbox((0, 0), "Online / Cheque No.", font=body_font)
    label_width = label_bbox[2] - label_bbox[0]
    value_x = 50 + label_width + 10  # Label start + label width + small gap
    draw.text((value_x, y_pos), str(cheque_no), fill=black_color, font=body_font)
    
    # Signature
    draw.text((320, y_pos), "Treasurer / Secretary", fill=black_color, font=body_font)
    # Load and place signature image - always use NameT.jpg
    try:
        signature = Image.open("NameT.jpg")
        # Resize signature to fit appropriately
        signature_size = (80, 40)  # Slightly larger for better visibility
        signature = signature.resize(signature_size, Image.Resampling.LANCZOS)
        # Position signature below "Treasurer / Secretary"
        signature_x = 330
        signature_y = y_pos + 15
        # Convert signature to RGBA if needed for proper pasting
        if signature.mode != 'RGBA':
            signature = signature.convert('RGBA')
        img.paste(signature, (signature_x, signature_y), signature)
        print("Successfully loaded signature from NameT.jpg")
    except Exception as e:
        print(f"Error loading NameT.jpg: {e}")
        # If NameT.jpg fails, try to load it again or create a placeholder
        try:
            # Try loading NameT.jpg one more time
            signature = Image.open("NameT.jpg")
            signature_size = (80, 40)
            signature = signature.resize(signature_size, Image.Resampling.LANCZOS)
            signature_x = 330
            signature_y = y_pos + 15
            if signature.mode != 'RGBA':
                signature = signature.convert('RGBA')
            img.paste(signature, (signature_x, signature_y), signature)
            print("Successfully loaded signature from NameT.jpg on second attempt")
        except:
            # Only use fallback if absolutely necessary
            print("NameT.jpg not available - using fallback")
            draw.text((350, y_pos + 20), "Signature", fill=black_color, font=body_font)
    
    return img

def number_to_words(num):
    """Convert number to words (simplified for common amounts)"""
    ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
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
        return ones[num // 100] + ' Hundred' + (' ' + number_to_words(num % 100) if num % 100 != 0 else '')
    elif num < 100000:
        return number_to_words(num // 1000) + ' Thousand' + (' ' + number_to_words(num % 1000) if num % 1000 != 0 else '')
    else:
        return str(num)  # Fallback for larger numbers

def save_receipt_multiple_formats(image, base_filename="generated_receipt", formats=["jpg", "pdf"]):
    """Save the receipt image in multiple formats"""
    saved_files = []
    
    # Create "Receipts store" directory if it doesn't exist
    script_dir = os.path.dirname(os.path.abspath(__file__))
    receipts_dir = os.path.join(script_dir, "Receipts store")
    os.makedirs(receipts_dir, exist_ok=True)
    
    print(f"DEBUG: Saving image with base filename: {base_filename}")
    print(f"DEBUG: Receipts will be stored in: {receipts_dir}")
    
    # Convert RGBA to RGB if necessary for JPG/PDF formats
    if image.mode in ("RGBA", "P"):
        rgb_image = Image.new("RGB", image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
        image = rgb_image
    
    for format_type in formats:
        format_type = format_type.lower()
        # Create full path to save in "Receipts store" folder
        filename = os.path.join(receipts_dir, f"{base_filename}.{format_type}")
        
        if format_type == "jpg" or format_type == "jpeg":
            image.save(filename, "JPEG", quality=95)
            saved_files.append(filename)
            print(f"Receipt saved as '{filename}' (JPG format)")
            
        elif format_type == "pdf":
            image.save(filename, "PDF", quality=95)
            saved_files.append(filename)
            print(f"Receipt saved as '{filename}' (PDF format)")
            
        elif format_type == "png":
            image.save(filename, "PNG")
            saved_files.append(filename)
            print(f"Receipt saved as '{filename}' (PNG format)")
            
        else:
            print(f"Warning: Format '{format_type}' not supported. Skipping...")
    
    return saved_files

# Sample data
invoice_data = {
    'InvoiceDate': '2025-07-06',
    'Name': 'Diana Moses More',
    'Address': 'B-305 Cassiopeia Classic, Baner, Pune.',
    'TitheMonth': 'JULY-NOV 2025',
    'TitheAmount': 1000,
    'MembershipMonth': 'AUGUST-2025',
    'MembershipAmount': 500,
    'BirthdayThankOffering': 5000,
    'WeddingAnniversaryThankOffering': 500,
    'HomeMissionPledges': 10000,
    'MissionAndEvangelismFund': 100000,
    'StStephensSocialAidFund': 5000000,
    'SpecialThanksAmount': 1500,
    'CharityFundAmount': 3000,
    'DonationFor': "Ministry & Preaching",
    'DonationAmount': 7500,
    'HarvestAuctionComment': "Christmas Cake Auction",
    'HarvestAuctionAmount': 2500,
    'OnlineChequeNo': '45435345'
}

# Generate and save the receipt
if __name__ == "__main__":
    # Uncomment the line below to reset receipt counter to 1
    # reset_receipt_counter()
    
    receipt_image = generate_receipt(invoice_data)
    
    # Save in multiple formats (JPG and PDF)
    saved_files = save_receipt_multiple_formats(receipt_image, "generated_receipt", ["jpg", "pdf"])
    
    print(f"\nReceipt details:")
    print(f"Date: {invoice_data['InvoiceDate']}")
    print(f"Name: {invoice_data['Name']}")
    print(f"Tithe Month: {invoice_data['TitheMonth']}")
    print(f"Amount: Rs. {invoice_data['TitheAmount']}")
    print(f"Generated files: {', '.join(saved_files)}")
    
    # Show the image if possible
    try:
        receipt_image.show()
    except:
        print("Image saved but cannot display automatically. Please check the generated files.")