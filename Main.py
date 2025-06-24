import os
import email
import openai
from email import policy
from pathlib import Path
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---- CONFIG ----
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY
email_dir =  "C:\\Users\\ASUS\\Desktop\\All projects\\Email  extraction\\emails"

CREDENTIALS_FILE = "credentials.json"  # <-- Use your actual credentials file name
GOOGLE_SHEET_NAME = 'Stanza Email Extract'

# ---- FUNCTION: PARSE EML ----
def parse_eml(file_path):
    with open(file_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
    sender = msg.get('From')
    date = msg.get('Date')
    subject = msg.get('Subject')
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body += part.get_content()
    else:
        body = msg.get_content()
    return sender, date, subject, body

# ---- FUNCTION: EXTRACT SHIPPING INFO WITH GPT ----
def extract_shipping_info(email_body):
    prompt = f"""
You are an AI logistics assistant. Extract the following from the email below:
1. Sender Email ID
2. Date
3. Shipping Line(s)
4. Origin Port(s)
5. Destination Port(s)
6. Price(s) with container type and currency (if mentioned)

EMAIL CONTENT:
{email_body}
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# ---- MAIN EXECUTION ----
results = []

for eml_file in Path(email_dir).glob("*.eml"):
    sender, date, subject, body = parse_eml(eml_file)
    extracted = extract_shipping_info(body)
    results.append({
        "Filename": eml_file.name,
        "Sender Email": sender,
        "Date": date,
        "Extracted Info": extracted
    })

# ---- OUTPUT TO CSV ----
df = pd.DataFrame(results)
df.to_csv("parsed_shipping_quotes.csv", index=False)
print("Extracted data saved to parsed_shipping_quotes.csv")

# ---- UPLOAD TO GOOGLE SHEETS ----
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# Clear existing data and upload new data
sheet.clear()
headers = list(df.columns)
sheet.append_row(headers)
for _, row in df.iterrows():
    sheet.append_row(row.astype(str).tolist())

print("Data uploaded to Google Sheet successfully!")
