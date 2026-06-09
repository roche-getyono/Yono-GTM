import os
import base64
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

TOKEN_PATH = r'c:\Users\danie\OneDrive\Desktop\Yono Daily Update\token_compose.json'

def search_f2_threads():
    if not os.path.exists(TOKEN_PATH):
        print(f"Error: Token not found at {TOKEN_PATH}")
        return

    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    service = build('gmail', 'v1', credentials=creds)

    query = 'f2vc.com OR "Roi Elad" OR "F2"'
    results = service.users().threads().list(userId='me', q=query).execute()
    threads = results.get('threads', [])

    if not threads:
        print("No threads found for F2.")
        return

    for t in threads[:5]:
        thread = service.users().threads().get(userId='me', id=t['id']).execute()
        messages = thread.get('messages', [])
        print(f"\nThread ID: {t['id']}")
        for msg in messages:
            payload = msg.get('payload')
            headers = payload.get('headers')
            sender = [h['value'] for h in headers if h['name'] == 'From'][0]
            date = [h['value'] for h in headers if h['name'] == 'Date'][0]
            subject = [h['value'] for h in headers if h['name'] == 'Subject'][0]
            
            print(f"From: {sender} | Date: {date} | Subject: {subject}")
            
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
                print(f"Snippet: {body[:1000]}...")
        print("-" * 40)

if __name__ == "__main__":
    search_f2_threads()
