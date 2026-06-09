import os
import base64
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

TOKEN_PATH = r'c:\Users\danie\OneDrive\Desktop\Yono Daily Update\token_compose.json'

def get_full_thread():
    if not os.path.exists(TOKEN_PATH):
        print(f"Error: Token not found at {TOKEN_PATH}")
        return

    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    service = build('gmail', 'v1', credentials=creds)

    thread_id = '19c4380946dab96b'
    thread = service.users().threads().get(userId='me', id=thread_id).execute()
    messages = thread.get('messages', [])

    print(f"Thread: {thread_id} - {len(messages)} messages")

    for msg in messages:
        payload = msg.get('payload')
        headers = payload.get('headers')
        sender = [h['value'] for h in headers if h['name'] == 'From'][0]
        date = [h['value'] for h in headers if h['name'] == 'Date'][0]
        print(f"\nFrom: {sender} | Date: {date}")
        
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
        
        print(f"Body: {body}")
        print("-" * 40)

if __name__ == "__main__":
    get_full_thread()
