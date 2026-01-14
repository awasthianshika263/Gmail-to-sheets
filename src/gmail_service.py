import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import SCOPES, STATE_FILE

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def get_gmail_service():
    token_path = os.path.join(BASE_DIR, 'token.json')
    cred_path = os.path.join(BASE_DIR, 'credentials', 'credentials.json')

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service, creds


def fetch_unread_messages(service):
    message_ids = []
    request = service.users().messages().list(
        userId='me',
        q='is:unread in:inbox'
    )

    while request:
        response = request.execute()
        message_ids.extend(
            [msg['id'] for msg in response.get('messages', [])]
        )
        request = service.users().messages().list_next(request, response)

    return message_ids


def mark_as_read(service, msg_id):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()


def load_processed_ids():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return set(json.load(f))
    return set()


def save_processed_ids(ids_set):
    with open(STATE_FILE, 'w') as f:
        json.dump(list(ids_set), f)
