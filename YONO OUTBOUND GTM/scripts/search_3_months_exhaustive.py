import os
import base64
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

TOKEN_PATH = r'c:\Users\danie\OneDrive\Desktop\Yono Daily Update\token_compose.json'

def search_3_months_all():
    if not os.path.exists(TOKEN_PATH):
        print(f"Error: Token not found at {TOKEN_PATH}")
        return

    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    service = build('gmail', 'v1', credentials=creds)

    query = '"3 months"'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    print(f"Found {len(messages)} messages with '3 months'. Analyzing first 20...")

    for m in messages[:20]:
        msg = service.users().messages().get(userId='me', id=m['id'], format='full').execute()
        payload = msg.get('payload')
        headers = payload.get('headers')
        sender = [h['value'] for h in headers if h['name'] == 'From'][0]
        subject = [h['value'] for h in headers if h['name'] == 'Subject'][0]
        
        # Check if sender is from Hetz or names are mentioned
        if 'hetz' in sender.lower() or 'pavel' in sender.lower() or 'itamar' in sender.lower():
             print(f"\n[MATCH] From: {sender} | Subject: {subject}")
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
             print(f"Body: {body[:1500]}...")
             print("-" * 40)
        else:
             print(f"Skipping: {sender} | {subject}")

if __name__ == "__main__":
    search_3_months_all()
