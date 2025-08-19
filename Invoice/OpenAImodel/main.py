import os
import json
import base64
import sys
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load .env from the current directory (OpenAImodel)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    image_path = "Invoice/OpenAImodel/Full_Input_sample.jpg"

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
subscription_key = os.getenv("AZURE_OPENAI_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
model_name = deployment  # or set separately if needed

# Load schema from Input.json
with open("Invoice/OpenAImodel/Input.json", "r", encoding="utf-8") as f:
    schema_json = json.load(f)
schema = json.dumps(schema_json["schema"], indent=2)

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

with open(image_path, "rb") as image_file:
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": (
                "You are an AI that extracts structured data from church donation receipts.\n"
                "Return strict JSON that matches the provided schema without any additional comments or explanations like (```json). Ensure all amounts are numbers, dates are in YYYY-MM-DD format, and currency is INR.\n\n"
                "Extract data from the attached church receipt and return it as JSON according to this schema and don't put comment line at begining and end of the JSON:\n"
                f"{schema}"
            ),
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64," + image_base64,
                    }
                }
            ]
        }
    ],
    max_tokens=4096,
    temperature=0,
    top_p=1.0,
    model=deployment
)

output_content = response.choices[0].message.content

# Write output to output.json 
with open("Invoice/OpenAImodel/output.json", "w", encoding="utf-8") as out_file:
    out_file.write(output_content)

# Extract and print all fields from the JSON output
try:
    output_data = json.loads(output_content)
    #print("Extracted fields from output.json:")
    #for key, value in output_data.items():
    #    print(f"{key}: {value}")
            
    # Initialize variables for mapping
    tithe_month = ""
    tithe_amount = ""
    membership_month = ""
    membership_amount = ""
    birthday_thank_offering = ""
    wedding_anniversary_thank_offering = ""
    home_mission_pledges = ""
    mission_and_evangelism_fund = ""
    st_stephens_social_aid_fund = ""
    donation_amount = ""
    donation_purpose = ""

    for item in output_data.get("line_items", []):
        category = item.get("category", "").lower()
        if category == "tithe":
            tithe_month = item.get("month", "")
            tithe_amount = item.get("amount", "")
        elif category == "membership":
            membership_month = item.get("month", "")
            membership_amount = item.get("amount", "")
        elif category == "birthday thank offering":
            birthday_thank_offering = item.get("amount", "")
        elif category == "wedding anniversary thank offering":
            wedding_anniversary_thank_offering = item.get("amount", "")
        elif category == "home mission pledges":
            home_mission_pledges = item.get("amount", "")
        elif category == "mission & evangelism fund":
            mission_and_evangelism_fund = item.get("amount", "")
        elif category == "st. stephen’s social aid fund":
            st_stephens_social_aid_fund = item.get("amount", "")
        elif category == "donation":
            donation_purpose = item.get("purpose", "")
            donation_amount = item.get("amount", "")

    # Map fields as requested
    mapped_fields = {
        "InvoiceDate": output_data.get("date", ""),
        "Name": output_data.get("donor_name", ""),
        "Address": output_data.get("address", ""),
        "TitheMonth": tithe_month,
        "TitheAmount": tithe_amount,
        "MembershipMonth": membership_month,
        "MembershipAmount": membership_amount,
        "BirthdayThankOffering": birthday_thank_offering,
        "WeddingAnniversaryThankOffering": wedding_anniversary_thank_offering,
        "HomeMissionPledges": home_mission_pledges,
        "MissionAndEvangelismFund": mission_and_evangelism_fund,
        "StStephensSocialAidFund": st_stephens_social_aid_fund,
        "DonationAmount": donation_amount,
        "DonationFor": donation_purpose,
        "TotalAmount": output_data.get("total_amount", ""),
        "Currency": output_data.get("currency", "")
    }
    
    print(json.dumps(mapped_fields))
    
except Exception as e:
        print(f"Error parsing output JSON: {e}")
