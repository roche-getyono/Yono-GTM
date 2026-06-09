import os
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime

# Paths
DEALS_PATH = r'c:\Users\danie\OneDrive\Desktop\YONO OUTBOUND GTM\Deals_1777136186.xlsx'
TOKEN_PATH = r'c:\Users\danie\OneDrive\Desktop\Yono Daily Update\token_business.json'

def get_gmail_service():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    return build('gmail', 'v1', credentials=creds)

def search_investor(service, name, contacts):
    query = f'"{name}"'
    if pd.notna(contacts):
        # Extract emails or names from contacts string
        # Assuming contacts might have emails like 'kobi@glilotcapital.com'
        for part in contacts.split(','):
            part = part.strip()
            if '@' in part:
                query += f' OR "{part}"'
            else:
                query += f' OR "{part}"'
    
    # Search last 30 days
    results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
    messages = results.get('messages', [])
    
    if not messages:
        return "No recent conversations found."
    
    # Get the latest message details
    msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
    snippet = msg.get('snippet', '')
    headers = msg.get('payload', {}).get('headers', [])
    subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
    date = next((h['value'] for h in headers if h['name'].lower() == 'date'), 'Unknown Date')
    
    return f"Latest: {subject} ({date})\nSnippet: {snippet}"

def main():
    service = get_gmail_service()
    df = pd.read_excel(DEALS_PATH, header=4)
    df = df.dropna(subset=['Name'])
    
    # Filter for active deals (first section or non-Pass)
    active_df = df[df['Status'] != 'Pass'].head(13) # Taking the first 13 which are the explicit active ones
    
    for _, row in active_df.iterrows():
        name = row['Name']
        contacts = row['Contacts']
        stage = row['Seed Round Stage']
        print(f"\n--- {name} (Stage: {stage}) ---")
        status = search_investor(service, name, contacts)
        print(status)

if __name__ == "__main__":
    main()
