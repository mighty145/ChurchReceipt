import json
import logging
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast
from dataclasses import dataclass
from unittest import result
import subprocess
import os
import csv
from datetime import datetime

import requests


def calculate_total_amount(receipt_data):
    """Calculate total amount from all numeric fields"""
    numeric_fields = [
        'TitheAmount', 'MembershipAmount', 'BirthdayThankOffering',
        'WeddingAnniversaryThankOffering', 'HomeMissionPledges',
        'MissionAndEvangelismFund', 'StStephensSocialAidFund',
        'SpecialThanksAmount', 'CharityFundAmount', 'DonationAmount',
        'HarvestAuctionAmount'
    ]
    
    total = 0
    for field in numeric_fields:
        value = receipt_data.get(field)
        if value:
            try:
                total += float(value)
            except (ValueError, TypeError):
                continue
    return total


def generate_description(receipt_data):
    """Generate a description based on the contributions"""
    contributions = []
    
    # Map fields to readable descriptions
    field_descriptions = {
        'TitheAmount': f"Tithe for {receipt_data.get('TitheMonth', '')}",
        'MembershipAmount': f"Membership for {receipt_data.get('MembershipMonth', '')}",
        'BirthdayThankOffering': 'Birthday Thank Offering',
        'WeddingAnniversaryThankOffering': 'Wedding Anniversary Thank Offering',
        'HomeMissionPledges': 'Home Mission Pledges',
        'MissionAndEvangelismFund': 'Mission and Evangelism Fund',
        'StStephensSocialAidFund': 'St Stephens Social Aid Fund',
        'SpecialThanksAmount': 'Special Thanks',
        'CharityFundAmount': 'Charity Fund',
        'DonationAmount': f"Donation for {receipt_data.get('DonationFor', 'General')}",
        'HarvestAuctionAmount': f"Harvest Auction - {receipt_data.get('HarvestAuctionComment', '')}"
    }
    
    for field, description in field_descriptions.items():
        value = receipt_data.get(field)
        if value:
            try:
                amount = float(value)
                if amount > 0:
                    contributions.append(f"{description} (₹{amount:.2f})")
            except (ValueError, TypeError):
                continue
    
    return "; ".join(contributions) if contributions else "No contributions"


def export_to_csv(receipt_data, csv_filename="Extract.csv"):
    """Export receipt data to CSV file, appending if file exists"""
    
    # Calculate total and description
    total_amount = calculate_total_amount(receipt_data)
    description = generate_description(receipt_data)
    
    # Add calculated fields to receipt data
    enhanced_data = receipt_data.copy()
    enhanced_data['Total'] = total_amount
    enhanced_data['Description'] = description
    enhanced_data['ProcessedDateTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Define CSV headers in the order we want them
    csv_headers = [
        'ProcessedDateTime', 'InvoiceDate', 'Name', 'Address', 'OnlineChequeNo',
        'TitheMonth', 'TitheAmount', 'MembershipMonth', 'MembershipAmount',
        'BirthdayThankOffering', 'WeddingAnniversaryThankOffering', 'HomeMissionPledges',
        'MissionAndEvangelismFund', 'StStephensSocialAidFund', 'SpecialThanksAmount',
        'CharityFundAmount', 'DonationFor', 'DonationAmount', 'HarvestAuctionComment',
        'HarvestAuctionAmount', 'Total', 'Description'
    ]
    
    # Check if file exists
    file_exists = os.path.exists(csv_filename)
    
    try:
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            
            # Write header only if file is new
            if not file_exists:
                writer.writeheader()
                print(f"Created new CSV file: {csv_filename}")
            
            # Write the data row
            writer.writerow({field: enhanced_data.get(field, '') for field in csv_headers})
            print(f"Data appended to: {csv_filename}")
            print(f"Total Amount: ₹{total_amount:.2f}")
            print(f"Description: {description}")
            
    except Exception as e:
        print(f"Error writing to CSV file: {e}")


def select_file_gui():
    """Open a file dialog to select a file"""
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        file_path = filedialog.askopenfilename(
            title="Select Invoice/Payment Form",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )
        
        root.destroy()
        return file_path
        
    except ImportError:
        print("tkinter not available. Please install it or use manual file path entry.")
        return None


def start_web_interface():
    """Start the web interface for mobile uploads"""
    try:
        # Check if Flask is available
        import flask
        
        print("Starting web interface...")
        print("The web interface will be available at:")
        print("- Local: http://localhost:5000")
        print("- Network: http://[your-ip]:5000")
        print("\nPress Ctrl+C to stop the server")
        
        # Import and run the web app
        web_app_path = Path(__file__).parent / "web_invoice_app.py"
        
        if web_app_path.exists():
            subprocess.run([sys.executable, str(web_app_path)], check=True)
        else:
            print("Error: web_invoice_app.py not found in the same directory")
            
    except ImportError:
        print("Flask not installed. To use the web interface, install Flask:")
        print("pip install flask werkzeug")
    except subprocess.CalledProcessError as e:
        print(f"Error starting web interface: {e}")
    except KeyboardInterrupt:
        print("\nWeb interface stopped.")


def upload_from_mobile_url(mobile_url):
    """Handle file upload from mobile app via URL"""
    if mobile_url.startswith(('http://', 'https://')):
        return mobile_url
    else:
        print("Invalid URL provided")
        return None


def main(file_location=None):
    # Allow file location to be passed as parameter or prompt user
    if file_location is None:
        print("Choose file input method:")
        print("1. Use default file (Payment_form_Church.JPG)")
        print("2. Enter file path manually")
        print("3. Use file picker (GUI)")
        print("4. Start web interface for mobile uploads")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            file_location = r"c:\Users\might\Projects\ChruchProject\Invoice\Payment_form_Church.JPG"
        elif choice == "2":
            file_location = input("Enter the full path to your file: ").strip()
        elif choice == "3":
            file_location = select_file_gui()
            if not file_location:
                print("No file selected. Exiting.")
                return
        elif choice == "4":
            print("Starting web interface...")
            start_web_interface()
            return
        else:
            print("Invalid choice. Using default file.")
            file_location = r"c:\Users\might\Projects\ChruchProject\Invoice\Payment_form_Church.JPG"
    
    # Validate file exists
    if not Path(file_location).exists() and not file_location.startswith(('http://', 'https://')):
        print(f"Error: File not found: {file_location}")
        return
    
    print(f"Processing file: {file_location}")
    
    # Load configuration from environment
    import os
    azure_endpoint = os.getenv('AZURE_ENDPOINT')
    azure_api_key = os.getenv('AZURE_API_KEY')
    
    if not azure_endpoint or not azure_api_key:
        print("Error: Azure credentials not configured. Please set AZURE_ENDPOINT and AZURE_API_KEY environment variables.")
        return
    
    settings = Settings(
        endpoint=azure_endpoint,
        api_version="2025-05-01-preview",
        # Either subscription_key or aad_token must be provided. Subscription Key is more prioritized.
        subscription_key=azure_api_key,
        aad_token=None,
        # Insert the analyzer name.
        analyzer_id="invoice-analyzer",
        # Insert the supported file types of the analyzer.
        file_location=file_location,
        
    )
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast
from dataclasses import dataclass
from unittest import result

import requests


def main():
    # Load configuration from environment
    import os
    azure_endpoint = os.getenv('AZURE_ENDPOINT')
    azure_api_key = os.getenv('AZURE_API_KEY')
    
    if not azure_endpoint or not azure_api_key:
        print("Error: Azure credentials not configured. Please set AZURE_ENDPOINT and AZURE_API_KEY environment variables.")
        return
    
    settings = Settings(
        endpoint=azure_endpoint,
        api_version="2025-05-01-preview",
        # Either subscription_key or aad_token must be provided. Subscription Key is more prioritized.
        subscription_key=azure_api_key,
        aad_token=None,
        # Insert the analyzer name.
        analyzer_id="invoice-analyzer",
        # Insert the supported file types of the analyzer.
        #file_location="https://raw.githubusercontent.com/Azure/azure-sdk-for-python/main/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/receipt/contoso-receipt.png",
        file_location=r"c:\Users\might\Projects\ChruchProject\Invoice\Payment_form_Church.JPG",
        
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
    
        # After you get the result:
    contents = result.get("result", {}).get("contents", [])
    if contents and "fields" in contents[0]:
        fields = contents[0]["fields"]
        
        selected_fields = [
            "InvoiceDate", "Name", "Address", "TitheMonth", "TitheAmount",
            "MembershipMonth", "MembershipAmount", "BirthdayThankOffering",
            "WeddingAnniversaryThankOffering", "HomeMissionPledges",
            "MissionAndEvangelismFund", "StStephensSocialAidFund",
            "DonationFor", "DonationAmount", "SpecialThanksAmount", 
            "CharityFundAmount", "HarvestAuctionComment", "HarvestAuctionAmount",
            "OnlineChequeNo"
        ]
        
        # Extract field values and map to printreceipt format
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
            print(f"{field}: {value}")
        
        # Import and call printreceipt module
        try:
            from printreceipt import edit_invoice_data, generate_receipt, save_receipt_multiple_formats
            
            print("\n" + "="*60)
            print("INVOKING RECEIPT GENERATOR WITH EXTRACTED DATA")
            print("="*60)
            
            # Use extracted data as initial values for printreceipt
            receipt_data = {
                'InvoiceDate': extracted_data.get('InvoiceDate') or '2025-07-06',
                'Name': extracted_data.get('Name') or 'N/A',
                'Address': extracted_data.get('Address') or 'N/A',
                'TitheMonth': extracted_data.get('TitheMonth'),
                'TitheAmount': extracted_data.get('TitheAmount'),
                'MembershipMonth': extracted_data.get('MembershipMonth'),
                'MembershipAmount': extracted_data.get('MembershipAmount'),
                'BirthdayThankOffering': extracted_data.get('BirthdayThankOffering'),
                'WeddingAnniversaryThankOffering': extracted_data.get('WeddingAnniversaryThankOffering'),
                'HomeMissionPledges': extracted_data.get('HomeMissionPledges'),
                'MissionAndEvangelismFund': extracted_data.get('MissionAndEvangelismFund'),
                'StStephensSocialAidFund': extracted_data.get('StStephensSocialAidFund'),
                'SpecialThanksAmount': extracted_data.get('SpecialThanksAmount'),
                'CharityFundAmount': extracted_data.get('CharityFundAmount'),
                'DonationFor': extracted_data.get('DonationFor'),
                'DonationAmount': extracted_data.get('DonationAmount'),
                'HarvestAuctionComment': extracted_data.get('HarvestAuctionComment'),
                'HarvestAuctionAmount': extracted_data.get('HarvestAuctionAmount'),
                'OnlineChequeNo': extracted_data.get('OnlineChequeNo') or ''
            }
            
            # Export to CSV
            print("\n" + "="*60)
            print("EXPORTING DATA TO CSV")
            print("="*60)
            export_to_csv(receipt_data)
            
            # Call the interactive editor with extracted data
            print("Do you want to edit the extracted data before generating receipt?")
            print("1. Yes, edit the data")
            print("2. No, generate receipt with extracted data")
            
            choice = input("Enter your choice (1 or 2): ").strip()
            
            if choice == "1":
                edited_data = edit_invoice_data(receipt_data)
            else:
                print("Using extracted data as-is...")
                edited_data = receipt_data
            
            # Generate and save the receipt
            print("Generating receipt image...")
            try:
                receipt_image = generate_receipt(edited_data)
                print("Receipt image generated successfully")
                
                print("Saving receipt files...")
                saved_files = save_receipt_multiple_formats(receipt_image, "generated_receipt_from_analyzer", ["jpg", "pdf"])
                
                # Verify files were actually created
                actual_files = []
                for filename in saved_files:
                    if os.path.exists(filename):
                        file_size = os.path.getsize(filename)
                        actual_files.append(f"{filename} ({file_size} bytes)")
                        print(f"✓ File created: {filename} ({file_size} bytes)")
                    else:
                        print(f"✗ File NOT created: {filename}")
                
                print(f"\n" + "="*60)
                print("RECEIPT GENERATED FROM ANALYZER DATA")
                print("="*60)
                if actual_files:
                    print(f"Successfully created files: {', '.join(actual_files)}")
                else:
                    print("ERROR: No files were actually created!")
                    
            except Exception as e:
                print(f"Error during receipt generation: {e}")
                import traceback
                traceback.print_exc()
            
        except ImportError as e:
            print(f"Error importing printreceipt module: {e}")
            print("Make sure printreceipt.py is in the same directory.")
        except Exception as e:
            print(f"Error generating receipt: {e}")
    else:
        print("No fields found in result.")
        
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2) 


@dataclass(frozen=True, kw_only=True)
class Settings:
    endpoint: str
    api_version: str
    subscription_key: str | None = None
    aad_token: str | None = None
    analyzer_id: str
    file_location: str

    def __post_init__(self):
        key_not_provided = (
            not self.subscription_key
            or self.subscription_key == "AZURE_CONTENT_UNDERSTANDING_SUBSCRIPTION_KEY"
        )
        token_not_provided = (
            not self.aad_token
            or self.aad_token == "AZURE_CONTENT_UNDERSTANDING_AAD_TOKEN"
        )
        if key_not_provided and token_not_provided:
            raise ValueError(
                "Either 'subscription_key' or 'aad_token' must be provided"
            )

    @property
    def token_provider(self) -> Callable[[], str] | None:
        aad_token = self.aad_token
        if aad_token is None:
            return None

        return lambda: aad_token


class AzureContentUnderstandingClient:
    def __init__(
        self,
        endpoint: str,
        api_version: str,
        subscription_key: str | None = None,
        token_provider: Callable[[], str] | None = None,
        x_ms_useragent: str = "cu-sample-code",
    ) -> None:
        if not subscription_key and token_provider is None:
            raise ValueError(
                "Either subscription key or token provider must be provided"
            )
        if not api_version:
            raise ValueError("API version must be provided")
        if not endpoint:
            raise ValueError("Endpoint must be provided")

        self._endpoint: str = endpoint.rstrip("/")
        self._api_version: str = api_version
        self._logger: logging.Logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)
        self._headers: dict[str, str] = self._get_headers(
            subscription_key, token_provider and token_provider(), x_ms_useragent
        )

    def begin_analyze(self, analyzer_id: str, file_location: str):
        """
        Begins the analysis of a file or URL using the specified analyzer.

        Args:
            analyzer_id (str): The ID of the analyzer to use.
            file_location (str): The path to the file or the URL to analyze.

        Returns:
            Response: The response from the analysis request.

        Raises:
            ValueError: If the file location is not a valid path or URL.
            HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        if Path(file_location).exists():
            with open(file_location, "rb") as file:
                data = file.read()
            headers = {"Content-Type": "application/octet-stream"}
        elif "https://" in file_location or "http://" in file_location:
            data = {"url": file_location}
            headers = {"Content-Type": "application/json"}
        else:
            raise ValueError("File location must be a valid path or URL.")

        headers.update(self._headers)
        if isinstance(data, dict):
            response = requests.post(
                url=self._get_analyze_url(
                    self._endpoint, self._api_version, analyzer_id
                ),
                headers=headers,
                json=data,
            )
        else:
            response = requests.post(
                url=self._get_analyze_url(
                    self._endpoint, self._api_version, analyzer_id
                ),
                headers=headers,
                data=data,
            )

        response.raise_for_status()
        self._logger.info(
            f"Analyzing file {file_location} with analyzer: {analyzer_id}"
        )
        return response

    def poll_result(
        self,
        response: requests.Response,
        timeout_seconds: int = 120,
        polling_interval_seconds: int = 2,
    ) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
        """
        Polls the result of an asynchronous operation until it completes or times out.

        Args:
            response (Response): The initial response object containing the operation location.
            timeout_seconds (int, optional): The maximum number of seconds to wait for the operation to complete. Defaults to 120.
            polling_interval_seconds (int, optional): The number of seconds to wait between polling attempts. Defaults to 2.

        Raises:
            ValueError: If the operation location is not found in the response headers.
            TimeoutError: If the operation does not complete within the specified timeout.
            RuntimeError: If the operation fails.

        Returns:
            dict: The JSON response of the completed operation if it succeeds.
        """
        operation_location = response.headers.get("operation-location", "")
        if not operation_location:
            raise ValueError("Operation location not found in response headers.")

        headers = {"Content-Type": "application/json"}
        headers.update(self._headers)

        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            self._logger.info(
                "Waiting for service response", extra={"elapsed": elapsed_time}
            )
            if elapsed_time > timeout_seconds:
                raise TimeoutError(
                    f"Operation timed out after {timeout_seconds:.2f} seconds."
                )

            response = requests.get(operation_location, headers=self._headers)
            response.raise_for_status()
            result = cast(dict[str, str], response.json())
            status = result.get("status", "").lower()
            if status == "succeeded":
                self._logger.info(
                    f"Request result is ready after {elapsed_time:.2f} seconds."
                )
                return response.json()  # pyright: ignore[reportAny]
            elif status == "failed":
                self._logger.error(f"Request failed. Reason: {response.json()}")
                raise RuntimeError("Request failed.")
            else:
                self._logger.info(
                    f"Request {operation_location.split('/')[-1].split('?')[0]} in progress ..."
                )
            time.sleep(polling_interval_seconds)

    def _get_analyze_url(self, endpoint: str, api_version: str, analyzer_id: str):
        return f"{endpoint}/contentunderstanding/analyzers/{analyzer_id}:analyze?api-version={api_version}&stringEncoding=utf16"

    def _get_headers(
        self, subscription_key: str | None, api_token: str | None, x_ms_useragent: str
    ) -> dict[str, str]:
        """Returns the headers for the HTTP requests.
        Args:
            subscription_key (str): The subscription key for the service.
            api_token (str): The API token for the service.
            enable_face_identification (bool): A flag to enable face identification.
        Returns:
            dict: A dictionary containing the headers for the HTTP requests.
        """
        headers = (
            {"Ocp-Apim-Subscription-Key": subscription_key}
            if subscription_key
            else {"Authorization": f"Bearer {api_token}"}
        )
        headers["x-ms-useragent"] = x_ms_useragent
        return headers


if __name__ == "__main__":
    main()
