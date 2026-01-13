import sys
import os

# Allow main.py to access config.py from root folder
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import config

from src.gmail_service import (
    get_gmail_service,
    fetch_unread_emails,
    get_email_raw,
    mark_as_read
)
from src.sheets_service import get_sheets_service, append_to_sheet
from src.email_parser import parse_email


def main():
    print("Starting Gmail → Google Sheets automation...")

    # Step 1: Connect to Gmail
    gmail_service = get_gmail_service()

    # Step 2: Fetch all unread emails
    unread_messages = fetch_unread_emails(gmail_service)

    if not unread_messages:
        print("No unread emails found.")
        return

    # Step 3: Connect to Google Sheets
    sheets_service = get_sheets_service()

    last_processed = config.LAST_PROCESSED_MESSAGE_ID
    new_last_processed = last_processed

    # Step 4: Process each unread email
    for msg in unread_messages:
        message_id = msg["id"]

        # Step 5: Skip already processed emails (duplicate prevention)
        if last_processed and message_id <= last_processed:
            continue

        # Step 6: Get full raw email from Gmail
        raw_email = get_email_raw(gmail_service, message_id)

        # Step 7: Parse raw email into clean fields
        email_data = parse_email(raw_email)

        # Step 8: Apply subject filter (if configured)
        if config.EMAIL_SUBJECT_FILTER:
            if config.EMAIL_SUBJECT_FILTER.lower() not in email_data["subject"].lower():
                continue

        # Step 9: Prepare row for Google Sheets
        row = [
            email_data["from"],
            email_data["subject"],
            email_data["date"],
            email_data["body"]
        ]

        # Step 10: Append to Google Sheet
        append_to_sheet(sheets_service, config.SPREADSHEET_ID, row)

        # Step 11: Mark email as read in Gmail
        mark_as_read(gmail_service, message_id)

        print("Processed:", email_data["subject"])

        # Step 12: Update last processed message ID
        new_last_processed = message_id

    # Step 13: Save state so next run does not duplicate
    if new_last_processed and new_last_processed != last_processed:
        update_last_processed_id(new_last_processed)

    print("Automation completed successfully.")


def update_last_processed_id(message_id):
    """
    Saves the last processed Gmail message ID into config.py
    This is used to prevent duplicate rows in Google Sheets.
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.py")

    with open(config_path, "r") as file:
        lines = file.readlines()

    with open(config_path, "w") as file:
        for line in lines:
            if line.startswith("LAST_PROCESSED_MESSAGE_ID"):
                file.write(f'LAST_PROCESSED_MESSAGE_ID = "{message_id}"\n')
            else:
                file.write(line)


if __name__ == "__main__":
    main()

