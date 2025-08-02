import os
import json
import logging
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
import tempfile
from config import config
from invoiceanalyzer import AzureContentUnderstandingClient, Settings

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Configure logging for production
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
        app.logger.setLevel(logging.INFO)
    
    # Security headers for production
    @app.after_request
    def after_request(response):
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Force HTTPS in production
        if not app.debug:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'pdf'}

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def analyze_uploaded_file(file_path):
        """Analyze the uploaded file using Azure Content Understanding"""
        try:
            # Use environment variables for production
            endpoint = app.config.get('AZURE_ENDPOINT')
            api_key = app.config.get('AZURE_API_KEY')
            
            if not endpoint or not api_key:
                raise ValueError("Azure credentials not configured properly")
            
            settings = Settings(
                endpoint=endpoint,
                api_version="2025-05-01-preview",
                subscription_key=api_key,
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
            app.logger.error(f"Error analyzing file: {e}")
            return {}, {"error": str(e)}

    @app.route('/')
    def index():
        return render_template('upload.html')

    @app.route('/mobile')
    def mobile_interface():
        """Serve the mobile-optimized interface"""
        try:
            with open('mobile_upload.html', 'r', encoding='utf-8') as f:
                mobile_content = f.read()
            # Replace any localhost references with current host
            mobile_content = mobile_content.replace('http://localhost:5000', request.host_url.rstrip('/'))
            return mobile_content
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
                    app.logger.error(f"Error processing file: {e}")
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
                'OnlineChequeNo': request.form.get('OnlineChequeNo', '')
            }
            
            # Import and use printreceipt module
            from printreceipt import generate_receipt, save_receipt_multiple_formats
            
            # Generate receipt
            receipt_image = generate_receipt(receipt_data)
            
            # Save receipt files
            receipt_filename = f"web_generated_receipt_{request.form.get('filename', 'unknown')}"
            saved_files = save_receipt_multiple_formats(receipt_image, receipt_filename, ["jpg", "pdf"])
            
            flash('Receipt generated successfully!')
            return render_template('receipt_generated.html', 
                                 saved_files=saved_files,
                                 receipt_data=receipt_data)
            
        except Exception as e:
            app.logger.error(f"Error generating receipt: {e}")
            flash(f'Error generating receipt: {str(e)}')
            return redirect(url_for('index'))

    @app.route('/api/upload', methods=['POST'])
    def api_upload():
        """API endpoint for mobile app uploads"""
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400
            
            file = request.files['file']
            
            if file.filename == '' or not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file'}), 400
            
            filename = secure_filename(file.filename)
            import uuid
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            file.save(file_path)
            
            # Analyze the file
            extracted_data, full_result = analyze_uploaded_file(file_path)
            
            return jsonify({
                'success': True,
                'filename': unique_filename,
                'extracted_data': extracted_data,
                'message': 'File analyzed successfully'
            })
            
        except Exception as e:
            app.logger.error(f"API upload error: {e}")
            return jsonify({'error': str(e)}), 500

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
            app.logger.error(f"Download error: {e}")
            flash(f'Error downloading file: {str(e)}')
            return redirect(url_for('index'))

    @app.errorhandler(413)
    def too_large(e):
        return "File is too large", 413

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Server Error: {error}")
        return "Internal server error", 500

    return app

# For production deployment
app = create_app()

if __name__ == '__main__':
    import os
    # Development server
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
