import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.message import EmailMessage

# Added .compose scope
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.compose'
]

TOKEN_PATH = r'c:\Users\danie\OneDrive\Desktop\Yono Daily Update\token_business.json'
CREDS_PATH = 'credentials.json' # Assumes this is in the CWD or Yono Daily Update folder

def get_creds():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Need to find credentials.json. Let's look in the Daily Update folder first.
            daily_update_creds = r'c:\Users\danie\OneDrive\Desktop\Yono Daily Update\credentials.json'
            if os.path.exists(daily_update_creds):
                flow = InstalledAppFlow.from_client_secrets_file(daily_update_creds, SCOPES)
                creds = flow.run_local_server(port=0)
            else:
                print("Error: credentials.json not found in Yono Daily Update folder.")
                return None
        
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    return creds

def create_draft():
    creds = get_creds()
    if not creds:
        return

    service = build('gmail', 'v1', credentials=creds)
    
    message = EmailMessage()
    message.set_content("""Kobi,

It's been a few weeks since we last spoke, and our execution velocity has shifted dramatically. I wanted to share two major milestones:

1. Commercial Momentum: We signed an SF-based client to an LOI and successfully onboarded them for a live pilot this week. 
2. Product Velocity: We’ve compressed our GTM roadmap from 9 months down to 2 months. Our architecture is now proven to handle high UI complexity without the "hallucination risk" that usually stalls these builds.

Since we last spoke, we’ve also sharpened our focus into a two-phase roadmap designed to solve the specific "resource-pull" and technical debt issues we've seen in the market:

* Phase 1 (Current): Focusing on CEOs and Product Leaders at hypergrowth startups (Series A–D). They need natural language interfaces now but either lack the resources to build them internally or aren't sure how to build them properly. Yono is their "overnight" solution.
* Phase 2: Scaling to Engineering and AI Leaders at larger enterprises. We've found that even companies that did build an initial internal solution are seeing it pull massive resources away from their core product. We are already in early discussions with OnCloud to address this "maintenance debt" for their enterprise stack.

I'd love to share the data from the SF pilot and the OnCloud conversation with you. Are you free for 15 minutes later this week?

Best,
Daniel""")

    message['To'] = 'kobi@glilotcapital.com'
    message['Subject'] = 'Yono Update: Commercial Momentum & SF Pilot Live'

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'message': {'raw': encoded_message}}

    draft = service.users().drafts().create(userId='me', body=create_message).execute()
    print(f'Draft id: {draft["id"]} created successfully.')

if __name__ == "__main__":
    create_draft()
