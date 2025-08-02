import os
import json
import logging
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
import tempfile
from invoiceanalyzer import AzureContentUnderstandingClient, Settings

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Configure logging
logging.basicConfig(level=logging.INFO)

# CORS support for mobile apps
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for mobile apps"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'mobile_compatible': True,
        'ios_compatible': True,
        'android_compatible': True
    })

@app.route('/manifest.json')
def manifest():
    """Serve PWA manifest for mobile app installation"""
    try:
        with open('static/manifest.json', 'r') as f:
            manifest_data = json.load(f)
        response = jsonify(manifest_data)
        response.headers['Content-Type'] = 'application/manifest+json'
        return response
    except FileNotFoundError:
        return jsonify({'error': 'Manifest not found'}), 404

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files including service worker"""
    try:
        static_path = os.path.join('static', filename)
        if filename == 'sw.js':
            # Serve service worker with correct MIME type
            with open(static_path, 'r') as f:
                content = f.read()
            response = app.response_class(
                response=content,
                status=200,
                mimetype='application/javascript'
            )
            response.headers['Cache-Control'] = 'no-cache'
            return response
        else:
            return send_file(static_path)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_uploaded_file(file_path):
    """Analyze the uploaded file using Azure Content Understanding"""
    try:
        # Load configuration from environment
        from config import Config
        
        azure_endpoint = Config.AZURE_ENDPOINT
        azure_api_key = Config.AZURE_API_KEY
        
        if not azure_endpoint or not azure_api_key:
            raise ValueError("Azure credentials not configured. Please set AZURE_ENDPOINT and AZURE_API_KEY environment variables.")
        
        settings = Settings(
            endpoint=azure_endpoint,
            api_version="2025-05-01-preview",
            subscription_key=azure_api_key,
            aad_token=None,
            analyzer_id="invoice-analyzer",
            file_location=file_path,
        )
        
        client = AzureContentUnderstandingClient(
            settings.endpoint,
            settings.api_version,
            subscription_key=settings.subscription_key,
            token_provider=settings.token_provider,
        )
        
        response = client.begin_analyze(settings.analyzer_id, settings.file_location)
        result = client.poll_result(
            response,
            timeout_seconds=60 * 60,
            polling_interval_seconds=1,
        )
        
        # Extract fields from result
        contents = result.get("result", {}).get("contents", [])
        if contents and "fields" in contents[0]:
            fields = contents[0]["fields"]
            
            selected_fields = [
                "InvoiceDate", "Name", "Address", "MobileNumber", "TitheMonth", "TitheAmount",
                "MembershipMonth", "MembershipAmount", "BirthdayThankOffering",
                "WeddingAnniversaryThankOffering", "HomeMissionPledges",
                "MissionAndEvangelismFund", "StStephensSocialAidFund",
                "DonationFor", "DonationAmount", "SpecialThanksAmount", 
                "CharityFundAmount", "HarvestAuctionComment", "HarvestAuctionAmount",
                "OnlineChequeNo"
            ]
            
            extracted_data = {}
            for field in selected_fields:
                value = (
                    fields.get(field, {}).get("value")
                    or fields.get(field, {}).get("valueDate")
                    or fields.get(field, {}).get("valueString")
                    or fields.get(field, {}).get("valueNumber")
                    or fields.get(field, {}).get("valueInteger")
                )
                extracted_data[field] = value
            
            return extracted_data, result
        else:
            return {}, result
            
    except Exception as e:
        logging.error(f"Error analyzing file: {e}")
        return {}, {"error": str(e)}

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/manual-entry')
def manual_entry():
    """Serve the manual entry form for creating receipts without uploading files"""
    # Create empty data structure matching the expected format
    empty_data = {
        'InvoiceDate': '',
        'Name': '',
        'Address': '',
        'MobileNumber': '',
        'TitheMonth': '',
        'TitheAmount': '',
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
        'OnlineChequeNo': '',
        'PaymentMethod': 'CASH'
    }
    
    return render_template('manual_entry.html', 
                         extracted_data=empty_data, 
                         filename='manual_entry',
                         is_manual=True)

@app.route('/mobile')
def mobile_interface():
    """Serve the mobile-optimized interface"""
    try:
        # Check if it's a mobile device
        user_agent = request.headers.get('User-Agent', '').lower()
        is_mobile = any(device in user_agent for device in [
            'mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone'
        ])
        
        with open('mobile_upload.html', 'r', encoding='utf-8') as f:
            mobile_content = f.read()
        
        # Replace any localhost references with current host
        host_url = request.host_url.rstrip('/')
        mobile_content = mobile_content.replace('http://localhost:5000', host_url)
        
        # Add mobile-specific headers
        response = app.response_class(
            response=mobile_content,
            status=200,
            mimetype='text/html'
        )
        
        # Add PWA and mobile-specific headers
        response.headers['Cache-Control'] = 'no-cache'
        if is_mobile:
            response.headers['X-UA-Compatible'] = 'IE=edge'
            response.headers['X-Mobile-Optimized'] = 'true'
        
        return response
        
    except FileNotFoundError:
        flash('Mobile interface not found')
        return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Create unique filename to avoid conflicts
            import uuid
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            try:
                file.save(file_path)
                
                # Analyze the file
                extracted_data, full_result = analyze_uploaded_file(file_path)
                
                # Save results for potential receipt generation
                result_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_filename}_result.json")
                with open(result_file, 'w', encoding='utf-8') as f:
                    json.dump(full_result, f, indent=2)
                
                return render_template('results.html', 
                                     extracted_data=extracted_data, 
                                     filename=unique_filename,
                                     result_file=result_file)
                
            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload an image or PDF file.')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/generate_receipt', methods=['POST'])
def generate_receipt():
    """Generate receipt from extracted data"""
    try:
        # Helper function to safely convert to float with 2 decimal places
        def safe_float(value):
            if value is None or value == '':
                return 0.00
            try:
                return round(float(value), 2)
            except (ValueError, TypeError):
                return 0.00
        
        # Helper function to safely convert to int for number_to_words (only for whole number fields)
        def safe_int(value):
            if value is None or value == '':
                return 0
            try:
                return int(float(value))
            except (ValueError, TypeError):
                return 0
        
        # Get the form data and convert numeric fields properly
        receipt_data = {
            'InvoiceDate': request.form.get('InvoiceDate', '2025-07-26'),
            'Name': request.form.get('Name', 'N/A'),
            'Address': request.form.get('Address', 'N/A'),
            'MobileNumber': request.form.get('MobileNumber', ''),
            'TitheMonth': request.form.get('TitheMonth'),
            'TitheAmount': safe_float(request.form.get('TitheAmount')),
            'MembershipMonth': request.form.get('MembershipMonth'),
            'MembershipAmount': safe_float(request.form.get('MembershipAmount')),
            'BirthdayThankOffering': safe_float(request.form.get('BirthdayThankOffering')),
            'WeddingAnniversaryThankOffering': safe_float(request.form.get('WeddingAnniversaryThankOffering')),
            'HomeMissionPledges': safe_float(request.form.get('HomeMissionPledges')),
            'MissionAndEvangelismFund': safe_float(request.form.get('MissionAndEvangelismFund')),
            'StStephensSocialAidFund': safe_float(request.form.get('StStephensSocialAidFund')),
            'SpecialThanksAmount': safe_float(request.form.get('SpecialThanksAmount')),
            'CharityFundAmount': safe_float(request.form.get('CharityFundAmount')),
            'DonationFor': request.form.get('DonationFor'),
            'DonationAmount': safe_float(request.form.get('DonationAmount')),
            'HarvestAuctionComment': request.form.get('HarvestAuctionComment'),
            'HarvestAuctionAmount': safe_float(request.form.get('HarvestAuctionAmount')),
            'OnlineChequeNo': request.form.get('OnlineChequeNo', ''),
            'PaymentMethod': request.form.get('PaymentMethod', 'CASH')
        }
        
        # Import and use printreceipt module
        from printreceipt import generate_receipt, save_receipt_multiple_formats
        
        # Generate receipt
        receipt_result = generate_receipt(receipt_data)
        
        # Create filename in format: Receipt_No-[ReceiptNo]-[Date]-[Name]
        # Example: Receipt_No-9-08-Aug-2025-Mighty_Basumata
        receipt_filename = f"Receipt_No-{receipt_result['receipt_no']}-{receipt_result['date_filename']}-{receipt_result['name']}"
        
        # Save receipt files (PDF only)
        saved_files = save_receipt_multiple_formats(receipt_result['image'], receipt_filename, ["pdf"])
        
        flash('Receipt generated successfully!')
        return render_template('receipt_generated.html', 
                             saved_files=saved_files,
                             receipt_data=receipt_data)
        
    except Exception as e:
        flash(f'Error generating receipt: {str(e)}')
        return redirect(url_for('index'))

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """API endpoint for mobile app uploads with enhanced error handling"""
    try:
        # Check for CORS if needed
        origin = request.headers.get('Origin')
        
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file uploaded',
                'code': 'NO_FILE'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'code': 'EMPTY_FILE'
            }), 400
            
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type. Please upload an image or PDF file.',
                'code': 'INVALID_FILE_TYPE',
                'allowed_types': list(ALLOWED_EXTENSIONS)
            }), 400
        
        # Check file size
        if request.content_length and request.content_length > MAX_FILE_SIZE:
            return jsonify({
                'error': 'File too large. Maximum size is 16MB.',
                'code': 'FILE_TOO_LARGE',
                'max_size': MAX_FILE_SIZE
            }), 413
        
        filename = secure_filename(file.filename)
        import uuid
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(file_path)
        
        # Analyze the file
        extracted_data, full_result = analyze_uploaded_file(file_path)
        
        # Enhanced response for mobile
        response_data = {
            'success': True,
            'filename': unique_filename,
            'extracted_data': extracted_data,
            'message': 'File analyzed successfully',
            'timestamp': os.path.getctime(file_path),
            'file_size': os.path.getsize(file_path)
        }
        
        response = jsonify(response_data)
        
        # Add CORS headers for mobile compatibility
        if origin:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        
        return response
        
    except Exception as e:
        app.logger.error(f"API upload error: {str(e)}")
        return jsonify({
            'error': f'Error processing file: {str(e)}',
            'code': 'PROCESSING_ERROR'
        }), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated receipt files"""
    try:
        # Security check - only allow downloading from safe locations
        safe_filename = secure_filename(filename)
        
        # Check if file exists in "Receipts store" directory (primary location for receipts)
        receipts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Receipts store")
        receipts_path = os.path.join(receipts_dir, safe_filename)
        if os.path.exists(receipts_path):
            return send_file(receipts_path, as_attachment=True, download_name=safe_filename)
        
        # Check if file exists in current directory (for backward compatibility)
        current_dir_path = os.path.join(os.getcwd(), safe_filename)
        if os.path.exists(current_dir_path):
            return send_file(current_dir_path, as_attachment=True, download_name=safe_filename)
        
        # Check if file exists in uploads directory
        uploads_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        if os.path.exists(uploads_path):
            return send_file(uploads_path, as_attachment=True, download_name=safe_filename)
        
        # File not found
        flash('File not found')
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'Error downloading file: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
