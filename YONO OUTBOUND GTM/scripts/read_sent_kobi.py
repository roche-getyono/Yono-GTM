
import os
import base64
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

TOKEN_PATH = r'c:\Users\danie\OneDrive\Desktop\Yono Daily Update\token_compose.json'

def get_sent_message():
    if not os.path.exists(TOKEN_PATH):
        print(f"Error: Token not found at {TOKEN_PATH}")
        return

    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    service = build('gmail', 'v1', credentials=creds)

    # Search for sent messages to Kobi
    query = 'to:kobi@glilotcapital.com'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No sent messages found for Kobi.")
        return

    # Get the latest message
    msg_id = messages[0]['id']
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    
    payload = message.get('payload')
    headers = payload.get('headers')
    subject = [h['value'] for h in headers if h['name'] == 'Subject'][0]
    date = [h['value'] for h in headers if h['name'] == 'Date'][0]
    
    print(f"Subject: {subject}")
    print(f"Date: {date}")
    print("-" * 20)

    parts = payload.get('parts')
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    text = base64.urlsafe_b64decode(data).decode()
                    print(text)
    else:
        data = payload.get('body').get('data')
        if data:
            text = base64.urlsafe_b64decode(data).decode()
            print(text)

if __name__ == "__main__":
    get_sent_message()
