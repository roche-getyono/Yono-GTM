import os
import base64
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

TOKEN_PATH = r'c:\Users\danie\OneDrive\Desktop\Yono Daily Update\token_compose.json'

def get_sent_hetz():
    if not os.path.exists(TOKEN_PATH):
        print(f"Error: Token not found at {TOKEN_PATH}")
        return

    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    service = build('gmail', 'v1', credentials=creds)

    # Search for sent messages to Hetz
    query = 'to:plivshiz@hetz.vc OR to:itamar@hetz.vc OR "Hetz"'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No sent messages found for Hetz.")
        return

    # Get the latest sent message
    # We filter for messages with 'SENT' label
    sent_msgs = []
    for m in messages[:10]:
        msg = service.users().messages().get(userId='me', id=m['id'], format='full').execute()
        if 'SENT' in msg.get('labelIds', []):
            sent_msgs.append(msg)
            break # Get the latest one

    if not sent_msgs:
        print("No messages with SENT label found for Hetz query.")
        return

    message = sent_msgs[0]
    payload = message.get('payload')
    headers = payload.get('headers')
    subject = [h['value'] for h in headers if h['name'] == 'Subject'][0]
    date = [h['value'] for h in headers if h['name'] == 'Date'][0]
    
    print(f"Subject: {subject}")
    print(f"Date: {date}")
    print("-" * 20)

    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode()
    else:
        data = payload.get('body').get('data')
        if data:
            body = base64.urlsafe_b64decode(data).decode()
    
    print(body)

if __name__ == "__main__":
    get_sent_hetz()
