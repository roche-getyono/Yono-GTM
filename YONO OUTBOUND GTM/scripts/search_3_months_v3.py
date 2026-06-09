import os
import base64
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

TOKEN_PATH = r'c:\Users\danie\OneDrive\Desktop\Yono Daily Update\token_compose.json'

def search_3_months_v3():
    if not os.path.exists(TOKEN_PATH):
        print(f"Error: Token not found at {TOKEN_PATH}")
        return

    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    service = build('gmail', 'v1', credentials=creds)

    # Search for "3 months" or "three months"
    query = '"3 months" OR "three months"'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    print(f"Found {len(messages)} messages. Analyzing...")

    for m in messages:
        msg = service.users().messages().get(userId='me', id=m['id'], format='full').execute()
        payload = msg.get('payload')
        headers = payload.get('headers')
        sender = [h['value'] for h in headers if h['name'] == 'From'][0]
        subject = [h['value'] for h in headers if h['name'] == 'Subject'][0]
        
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
        
        if body:
            # Check for Hetz, Pavel, Itamar in body
            low_body = body.lower()
            if 'hetz' in low_body or 'pavel' in low_body or 'itamar' in low_body:
                print(f"\n[MATCH] From: {sender} | Subject: {subject}")
                print(f"Snippet: {body[:1500]}...")
                print("-" * 40)

if __name__ == "__main__":
    search_3_months_v3()
