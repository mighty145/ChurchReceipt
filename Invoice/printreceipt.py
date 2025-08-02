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
OnlineChequeNo: None
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
        # Use absolute path to ensure logo is always found
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "logo.jpg")
        logo = Image.open(logo_path)
        # Resize logo to fit appropriately (reduced size to avoid overlap)
        logo_size = (50, 50)
        logo = logo.resize(logo_size, Image.Resampling.LANCZOS)
        # Position logo on the left side
        logo_x = 15
        logo_y = 20
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        img.paste(logo, (logo_x, logo_y), logo)
    except Exception as e:
        print(f"Warning: Could not load logo.jpg: {e}")
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
    
    # Calculate total amount first to get the correct sum in words
    temp_total = 0
    temp_items = [
        invoice_data.get('TitheAmount', ''),
        invoice_data.get('MembershipAmount', ''), 
        invoice_data.get('BirthdayThankOffering', ''),
        invoice_data.get('WeddingAnniversaryThankOffering', ''),
        invoice_data.get('SpecialThanksAmount', ''),
        invoice_data.get('MissionAndEvangelismFund', ''),
        invoice_data.get('CharityFundAmount', ''),
        invoice_data.get('StStephensSocialAidFund', ''),
        invoice_data.get('HarvestAuctionAmount', ''),
        invoice_data.get('DonationAmount', '')
    ]
    
    for amount in temp_items:
        try:
            if isinstance(amount, str):
                amount_value = float(amount) if amount and amount.strip() != '' and amount != 'None' else 0
            elif isinstance(amount, (int, float)):
                amount_value = float(amount) if amount > 0 else 0
            else:
                amount_value = 0
            temp_total += amount_value
        except (ValueError, TypeError):
            temp_total += 0
    
    # Convert total amount to words in bold with underline
    # Safely convert amount to integer for number_to_words
    try:
        amount_int = int(temp_total) if temp_total > 0 else 0
    except (ValueError, TypeError):
        amount_int = 0
        
    if amount_int > 0:
        amount_words = number_to_words(amount_int) + " Only"
        amount_start_x = 160
        draw.text((amount_start_x, y_pos), amount_words, fill=black_color, font=body_bold_font)
        # Draw underline for amount words
        amount_bbox = draw.textbbox((amount_start_x, y_pos), amount_words, font=body_bold_font)
        draw.line([(amount_start_x, amount_bbox[3] + 2), (amount_bbox[2], amount_bbox[3] + 2)], fill=black_color, width=1)
    
    y_pos += 20
    # Use the selected payment method instead of generic text
    payment_method = invoice_data.get('PaymentMethod', 'CASH').lower()
    towards_text = f"by {payment_method} towards"
    draw.text((50, y_pos), towards_text, fill=black_color, font=body_font)
    
    # Calculate position for contribution text right after "towards"
    towards_bbox = draw.textbbox((50, y_pos), towards_text, font=body_font)
    contribution_start_x = towards_bbox[2] + 5  # Add 5 pixels spacing
    
    # Generate dynamic contribution comments based on actual contributions
    def get_contribution_comments(invoice_data):
        """Generate contribution comments based on non-zero amounts"""
        contributions = []
        
        # Check each contribution type and add to list if amount exists
        try:
            if invoice_data.get('TitheAmount') and float(invoice_data.get('TitheAmount', 0) or 0) > 0:
                contributions.append("Tithe")
            if invoice_data.get('MembershipAmount') and float(invoice_data.get('MembershipAmount', 0) or 0) > 0:
                contributions.append("Membership")
            if invoice_data.get('BirthdayThankOffering') and float(invoice_data.get('BirthdayThankOffering', 0) or 0) > 0:
                contributions.append("Birthday Offering")
            if invoice_data.get('WeddingAnniversaryThankOffering') and float(invoice_data.get('WeddingAnniversaryThankOffering', 0) or 0) > 0:
                contributions.append("Anniversary Offering")
            if invoice_data.get('SpecialThanksAmount') and float(invoice_data.get('SpecialThanksAmount', 0) or 0) > 0:
                contributions.append("Special Thanks")
            if invoice_data.get('MissionAndEvangelismFund') and float(invoice_data.get('MissionAndEvangelismFund', 0) or 0) > 0:
                contributions.append("Mission & Evangelism")
            if invoice_data.get('CharityFundAmount') and float(invoice_data.get('CharityFundAmount', 0) or 0) > 0:
                contributions.append("Charity Fund")
            if invoice_data.get('StStephensSocialAidFund') and float(invoice_data.get('StStephensSocialAidFund', 0) or 0) > 0:
                contributions.append("Social Aid")
            if invoice_data.get('HarvestAuctionAmount') and float(invoice_data.get('HarvestAuctionAmount', 0) or 0) > 0:
                contributions.append("Harvest Auction")
            if invoice_data.get('DonationAmount') and float(invoice_data.get('DonationAmount', 0) or 0) > 0:
                contributions.append("Donation")
        except (ValueError, TypeError):
            # If there's any error in conversion, default to generic
            pass
        
        # Format the contributions list
        if len(contributions) == 0:
            return "Contribution"
        elif len(contributions) == 1:
            return contributions[0]
        elif len(contributions) == 2:
            return f"{contributions[0]} & {contributions[1]}"
        elif len(contributions) <= 4:
            return f"{', '.join(contributions[:-1])} & {contributions[-1]}"
        else:
            # If more than 4 contributions, show first 3 and "& Others"
            return f"{', '.join(contributions[:3])} & Others"
    
    contribution_text = get_contribution_comments(invoice_data)
    draw.text((contribution_start_x, y_pos), contribution_text, fill=black_color, font=body_bold_font)
    # Draw underline for contribution text
    contribution_bbox = draw.textbbox((contribution_start_x, y_pos), contribution_text, font=body_bold_font)
    draw.line([(contribution_start_x, contribution_bbox[3] + 2), (contribution_bbox[2], contribution_bbox[3] + 2)], fill=black_color, width=1)
    
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
            # Format amount with 2 decimal places
            if isinstance(amount, (int, float)) and amount > 0:
                amount_text = f"{amount:.2f}"
            else:
                amount_text = str(amount) if amount else ""
            
            amount_bbox = draw.textbbox((0, 0), amount_text, font=body_font)
            amount_width = amount_bbox[2] - amount_bbox[0]
            amount_x = 440 - amount_width  # Right-align within the column
            draw.text((amount_x, y_pos + 5), amount_text, fill=black_color, font=body_font)
            
            # Add to total with proper decimal handling
            try:
                # Convert to float, handling both string and numeric inputs
                if isinstance(amount, str):
                    amount_value = float(amount) if amount and amount.strip() != '' and amount != 'None' else 0
                elif isinstance(amount, (int, float)):
                    amount_value = float(amount) if amount > 0 else 0
                else:
                    amount_value = 0
                total_amount += amount_value
            except (ValueError, TypeError):
                total_amount += 0
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
    total_text = f"{total_amount:.2f}"
    total_bbox = draw.textbbox((0, 0), total_text, font=header_bold_font)
    total_width = total_bbox[2] - total_bbox[0]
    total_x = 440 - total_width  # Right-align within the column
    draw.text((total_x, y_pos + 10), total_text, fill=black_color, font=header_bold_font)
    
    # Online/Cheque number (reduced space) - Dynamic based on payment method
    y_pos += 50
    payment_method = invoice_data.get('PaymentMethod', 'CASH').upper()
    if payment_method == 'CHEQUE':
        number_label = "Cheque No."
    elif payment_method == 'ONLINE':
        number_label = "Online No."
    else:  # CASH or other
        number_label = "Reference No."
    
    draw.text((50, y_pos), number_label, fill=black_color, font=body_font)
    cheque_no = invoice_data.get('OnlineChequeNo', '')
    # Calculate proper position for the value based on label width
    label_bbox = draw.textbbox((0, 0), number_label, font=body_font)
    label_width = label_bbox[2] - label_bbox[0]
    value_x = 50 + label_width + 10  # Label start + label width + small gap
    draw.text((value_x, y_pos), str(cheque_no), fill=black_color, font=body_font)
    
    # Signature
    draw.text((320, y_pos), "Treasurer / Secretary", fill=black_color, font=body_font)
    # Place NameT.jpg image directly below Treasurer/Secretary text
    try:
        # Use absolute path to ensure signature image is always found
        script_dir = os.path.dirname(os.path.abspath(__file__))
        signature_path = os.path.join(script_dir, "NameT.jpg")
        signature = Image.open(signature_path)
        signature_size = (80, 40)
        signature = signature.resize(signature_size, Image.Resampling.LANCZOS)
        signature_x = 330
        signature_y = y_pos + 15
        if signature.mode != 'RGBA':
            signature = signature.convert('RGBA')
        img.paste(signature, (signature_x, signature_y), signature)
    except Exception as e:
        print(f"Warning: Could not load NameT.jpg: {e}")
        # Fallback: Draw a simple signature placeholder
        draw.rectangle([(330, y_pos + 15), (410, y_pos + 55)], outline=black_color, width=1)
        draw.text((340, y_pos + 30), "Signature", fill=black_color, font=body_font)
    
    # Return the image along with receipt details for filename generation
    # Create filename-friendly date format: DD-MMM-YYYY (e.g., 08-Aug-2025)
    date_for_filename = datetime.datetime.strptime(invoice_data['InvoiceDate'], '%Y-%m-%d').strftime('%d-%b-%Y')
    
    receipt_info = {
        'image': img,
        'receipt_no': receipt_no,
        'date': date_formatted,  # Keep original format for display
        'date_filename': date_for_filename,  # New format for filename
        'name': invoice_data.get('Name', 'Unknown').replace(' ', '_').replace('.', '')
    }
    return receipt_info

def number_to_words(num):
    """Convert number to words (simplified for common amounts)"""
    # Handle string inputs - convert to int
    if isinstance(num, str):
        try:
            num = int(float(num))
        except (ValueError, TypeError):
            return "Zero"
    
    # Handle None or other non-numeric types
    if num is None or not isinstance(num, (int, float)):
        return "Zero"
    
    # Convert to int if it's a float
    num = int(num)
    
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
    print(f"DEBUG: Image mode: {image.mode}, Image size: {image.size}")
    
    # Convert RGBA to RGB if necessary for JPG/PDF formats
    if image.mode in ("RGBA", "P"):
        print("DEBUG: Converting image from RGBA/P to RGB")
        rgb_image = Image.new("RGB", image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
        image = rgb_image
        print(f"DEBUG: Converted image mode: {image.mode}")
    
    for format_type in formats:
        format_type = format_type.lower()
        # Create full path to save in "Receipts store" folder
        filename = os.path.join(receipts_dir, f"{base_filename}.{format_type}")
        
        try:
            print(f"DEBUG: Attempting to save {filename}")
            
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
                continue
            
            # Verify file was actually created
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                print(f"DEBUG: File {filename} created successfully ({file_size} bytes)")
            else:
                print(f"ERROR: File {filename} was not created despite no exception!")
                
        except Exception as e:
            print(f"ERROR: Failed to save {filename}: {e}")
            import traceback
            traceback.print_exc()
    
    return saved_files

def edit_invoice_data(invoice_data):
    """Allow user to edit/correct invoice data before generating receipt"""
    print("\n" + "="*60)
    print("RECEIPT DATA EDITOR")
    print("="*60)
    print("Current invoice data:")
    print("-" * 40)
    
    # Display current data
    for key, value in invoice_data.items():
        display_value = value if value is not None else "None"
        print(f"{key}: {display_value}")
    
    print("-" * 40)
    print("\nOptions:")
    print("1. Edit specific field")
    print("2. Generate receipt with current data")
    print("3. Reset all fields to None")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Edit specific field
            print("\nAvailable fields:")
            fields = list(invoice_data.keys())
            for i, field in enumerate(fields, 1):
                current_value = invoice_data[field] if invoice_data[field] is not None else "None"
                print(f"{i:2d}. {field} = {current_value}")
            
            try:
                field_choice = input("\nEnter field number to edit (or 'back' to return): ").strip()
                if field_choice.lower() == 'back':
                    continue
                
                field_index = int(field_choice) - 1
                if 0 <= field_index < len(fields):
                    field_name = fields[field_index]
                    current_value = invoice_data[field_name]
                    
                    print(f"\nEditing: {field_name}")
                    print(f"Current value: {current_value if current_value is not None else 'None'}")
                    
                    new_value = input("Enter new value (or 'none' to set as None, 'keep' to keep current): ").strip()
                    
                    if new_value.lower() == 'none':
                        invoice_data[field_name] = None
                        print(f"✓ {field_name} set to None")
                    elif new_value.lower() == 'keep':
                        print(f"✓ {field_name} kept as current value")
                    elif new_value == '':
                        print(f"✗ Empty value not allowed. {field_name} kept as current value")
                    else:
                        # Convert to appropriate type
                        if field_name in ['TitheAmount', 'MembershipAmount', 'BirthdayThankOffering', 
                                        'WeddingAnniversaryThankOffering', 'HomeMissionPledges', 
                                        'MissionAndEvangelismFund', 'StStephensSocialAidFund',
                                        'SpecialThanksAmount', 'CharityFundAmount', 'DonationAmount',
                                        'HarvestAuctionAmount']:
                            try:
                                invoice_data[field_name] = int(new_value)
                                print(f"✓ {field_name} updated to: {invoice_data[field_name]}")
                            except ValueError:
                                print(f"✗ Invalid number format. {field_name} kept as current value")
                        else:
                            invoice_data[field_name] = new_value
                            print(f"✓ {field_name} updated to: {invoice_data[field_name]}")
                else:
                    print("✗ Invalid field number")
            except ValueError:
                print("✗ Invalid input")
                
        elif choice == "2":
            # Generate receipt
            print("\n✓ Proceeding with receipt generation...")
            return invoice_data
            
        elif choice == "3":
            # Reset all fields
            confirm = input("\nAre you sure you want to reset all fields to None? (y/n): ").strip().lower()
            if confirm == 'y':
                for key in invoice_data.keys():
                    invoice_data[key] = None
                print("✓ All fields reset to None")
            else:
                print("✓ Reset cancelled")
                
        else:
            print("✗ Invalid choice. Please enter 1, 2, or 3.")

# Sample data
invoice_data = {
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

# Generate and save the receipt
if __name__ == "__main__":
    # Uncomment the line below to reset receipt counter to 1
    # reset_receipt_counter()
    
    # Allow user to edit invoice data before generating receipt
    print("Methodist Church Receipt Generator")
    print("=" * 50)
    
    # Edit invoice data
    edited_invoice_data = edit_invoice_data(invoice_data)
    
    # Generate receipt with edited data
    receipt_result = generate_receipt(edited_invoice_data)
    
    # Save in multiple formats (JPG and PDF) with new filename format
    standalone_filename = f"Receipt_No-{receipt_result['receipt_no']}-{receipt_result['date_filename']}-{receipt_result['name']}"
    saved_files = save_receipt_multiple_formats(receipt_result['image'], standalone_filename, ["jpg", "pdf"])
    
    print(f"\n" + "="*50)
    print("RECEIPT GENERATED SUCCESSFULLY")
    print("="*50)
    print(f"Date: {edited_invoice_data['InvoiceDate']}")
    print(f"Name: {edited_invoice_data['Name']}")
    print(f"Tithe Month: {edited_invoice_data['TitheMonth']}")
    print(f"Amount: Rs. {edited_invoice_data['TitheAmount']}")
    print(f"Generated files: {', '.join(saved_files)}")
    
    # Show the image if possible
    try:
        receipt_result['image'].show()
    except:
        print("Receipt saved successfully. Please check the generated files.")