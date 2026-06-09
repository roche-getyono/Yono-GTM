import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Force stdout to use UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

TOKEN_PATH = r'c:\Users\danie\OneDrive\Desktop\Yono Daily Update\token_business.json'

def search_kobi_persona():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    service = build('gmail', 'v1', credentials=creds)
    
    # Search for Kobi AND persona
    query = 'from:kobi@glilotcapital.com persona OR "Kobi Samboursky" persona'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    
    if not messages:
        # Broaden search to just Kobi and scan for the word persona
        query = 'from:kobi@glilotcapital.com OR "Kobi Samboursky"'
        results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
        messages = results.get('messages', [])
        
    if not messages:
        print("No messages found from Kobi.")
        return

    for msg_info in messages:
        msg = service.users().messages().get(userId='me', id=msg_info['id']).execute()
        snippet = msg.get('snippet', '')
        if 'persona' in snippet.lower() or 'target' in snippet.lower():
            print(f"Message ID: {msg_info['id']}")
            print(f"Snippet: {snippet}")
            # Get full body if possible
            parts = msg.get('payload', {}).get('parts', [])
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    import base64
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    print(f"Body snippet: {body[:500]}...")

if __name__ == "__main__":
    search_kobi_persona()
