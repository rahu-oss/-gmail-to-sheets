# Gmail to Google Sheets Automation System

## High-Level Architecture Diagram
(User can include a hand-drawn diagram showing: Gmail -> Python Script -> Google Sheets)

Gmail API ---> gmail_service.py ---> email_parser.py ---> main.py ---> sheets_service.py ---> Google Sheets

---

## Step-by-Step Setup Instructions

1. Install dependencies:
pip install -r requirements.txt

2. Place credentials.json inside the credentials/ folder.

3. Open config.py and paste your Google Sheet ID.

4. In your Google Sheet, manually add headers:
From | Subject | Date | Content

5. Run the project:
python -m src.main

---

## OAuth Flow Used

This project uses Google OAuth 2.0 Desktop Application flow.  
On the first run, a browser window opens asking the user to log in and give permission for Gmail and Google Sheets.  
Google then provides a token that is stored in credentials/token.json so the user does not need to log in again.

---

## Duplicate Prevention Logic

The system stores the last processed Gmail message ID inside config.py.  
On every run, emails with IDs less than or equal to this value are skipped.  
This ensures the same email is never added twice.

---

## State Persistence Method

State is stored in config.py using LAST_PROCESSED_MESSAGE_ID.  
This value is updated after every successful run and survives program restarts.

---

## Challenge Faced

The main challenge was Google OAuth scope mismatch, which caused 403 permission errors.  
This was solved by ensuring Gmail and Google Sheets scopes were included in the same OAuth token and regenerating the token.

---

## Limitations

- The script must be run manually  
- Only unread emails are processed  
- Requires Google OAuth setup  

---

This project demonstrates real-world API integration, secure authentication, and automated data handling.
