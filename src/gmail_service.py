import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# These scopes define what our app is allowed to do.
# We need to read emails and also mark them as read after processing.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets"
]


# Path where Google OAuth client details are stored
CREDENTIALS_PATH = "credentials/credentials.json"

# Path where Google will store the login token after first successful login
# This avoids asking the user to log in again and again
TOKEN_PATH = "credentials/token.json"


def get_gmail_service():
    """
    This function handles authentication with Google and returns
    a Gmail API service object that we can use to access emails.
    """
    creds = None

    # If a token already exists, load it so the user does not have to login again
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # If token does not exist or is invalid, we run the OAuth login flow
    if not creds or not creds.valid:
        # If token has expired but can be refreshed, refresh it
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Otherwise, start a new login flow using credentials.json
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the new token so that next time login is not required
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    # Create and return the Gmail API service object
    return build("gmail", "v1", credentials=creds)


def fetch_unread_emails(service):
    """
    Fetches all unread emails from the user's Gmail inbox.
    Returns a list of message IDs.
    """
    result = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"]
    ).execute()

    return result.get("messages", [])


def get_email_raw(service, message_id):
    """
    Given a message ID, this function fetches the complete email
    in raw format so that it can be parsed later.
    """
    return service.users().messages().get(
        userId="me",
        id=message_id,
        format="raw"
    ).execute()


def mark_as_read(service, message_id):
    """
    After we have processed an email and stored it in Google Sheets,
    we mark it as READ so it does not get processed again.
    """
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()
