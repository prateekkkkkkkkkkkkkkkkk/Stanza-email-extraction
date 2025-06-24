
# Logistics Email Quotation Extractor & Google Sheets Integration

##  Overview

This project automates extraction of shipping price quotations from `.eml` email samples and updates them into a structured **Google Sheet** using AI tools.

---

##  Features

- Extracts from `.eml`:
  - Sender Email
  - Date/Time Received
  - Subject
  - Shipping Line (via AI)
  - Origin & Destination Ports (via AI)
  - 20GP and 40HC Pricing (via AI)
- Auto-formatted output to CSV and Google Sheets.

 

## Folder Structure

```
project/
├── eml_samples/                 # Place all .eml email files here
├── extracted_shipping_data.csv  # Output file (sample)
├── extract_emails.py            # Main script
└── README.md
```

---

##  Setup Instructions

### 1. Clone Repository and Install Dependencies

```bash
pip install openai pandas gspread oauth2client
```

### 2. Setup Google Sheets Access

- Go to [Google Developers Console](https://console.developers.google.com/)
- Create project → Enable Sheets API
- Create credentials → Download `credentials.json`
- Share your Google Sheet with the service account email.

---

### 3. Run the Extraction Script

```bash
python extract_emails.py
```

The extracted results will:
- Save into `extracted_shipping_data.csv`
- Update the provided Google Sheet (if ID is configured)

---

##  AI Processing

The script uses AI parsing (e.g., via OpenAI GPT) to extract:
- Ports
- Prices (20GP/40HC)
- Carrier details

Use prompt-based extraction with `openai.ChatCompletion.create()`.

---

##  Example Output

| Sender              | Date               | Origin Port | Destination Port | 20GP Price | 40HC Price |
|---------------------|--------------------|-------------|------------------|------------|------------|
| nate@cimclogistics.vn | 19 Jun 2025 | HO CHI MINH | NHAVA SHEVA | 1550 | 1850 |

---

##  Support

For help, contact `support@stanzalogistics.com`
