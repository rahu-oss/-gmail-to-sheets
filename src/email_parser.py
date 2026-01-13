import base64
import email
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime


def parse_email(raw_message):
    """
    Converts raw Gmail API email into clean structured data.
    Extracts:
    - From
    - Subject
    - Date
    - Plain text body
    """

    # Step 1: Decode Base64 Gmail message
    raw_data = base64.urlsafe_b64decode(raw_message["raw"].encode("ASCII"))

    # Step 2: Convert bytes into email object
    message = email.message_from_bytes(raw_data)

    # Step 3: Extract headers
    sender = message.get("From", "")
    subject = message.get("Subject", "")
    date = message.get("Date", "")

    # Step 4: Extract email body
    body = ""

    # Most emails are multipart (HTML + attachments + text)
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()

            # We only care about the readable content
            if content_type in ["text/plain", "text/html"]:
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors="ignore")
                    break
    else:
        payload = message.get_payload(decode=True)
        if payload:
            body = payload.decode(errors="ignore")

    # Step 5: Convert HTML email to plain text
    if "<html" in body.lower():
        soup = BeautifulSoup(body, "html.parser")
        body = soup.get_text()

    # Step 6: Convert date to readable format
    try:
        parsed_date = parsedate_to_datetime(date)
        date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
    except:
        pass

    return {
        "from": sender,
        "subject": subject,
        "date": date,
        "body": body.strip()
    }
