# -------------------------------
# Google Sheet Configuration
# -------------------------------

# Paste your Google Sheet ID here
SPREADSHEET_ID = "1e5QeAP4f494bdMTfJi0v0U2feKXI9EsAQ_08D0O2dvI"


# -------------------------------
# Email Filtering (Optional)
# -------------------------------

# If you want to process only certain emails
# Example: "Invoice", "Application", "Payment"
EMAIL_SUBJECT_FILTER = ""   # leave empty to allow all emails


# -------------------------------
# State Management
# -------------------------------

# This value stores the Gmail message ID of the last processed email
# It is updated automatically by the script after every successful run
# This prevents duplicate rows in Google Sheets
LAST_PROCESSED_MESSAGE_ID = "19b507e4e90680ad"
