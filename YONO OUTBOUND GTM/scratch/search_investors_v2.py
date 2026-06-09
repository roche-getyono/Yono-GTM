import os
import sys
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime

# Force stdout to use UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Paths
DEALS_PATH = r'c:\Users\danie\OneDrive\Desktop\YONO OUTBOUND GTM\Deals_1777136186.xlsx'
TOKEN_PATH = r'c:\Users\danie\OneDrive\Desktop\Yono Daily Update\token_business.json'

def get_gmail_service():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    return build('gmail', 'v1', credentials=creds)

def search_investor(service, name, contacts):
    query = f'"{name}"'
    if pd.notna(contacts):
        for part in str(contacts).split(','):
            part = part.strip()
            if '@' in part:
                query += f' OR "{part}"'
            else:
                query += f' OR "{part}"'
    
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
        messages = results.get('messages', [])
    except Exception as e:
        return f"Error searching: {e}"
    
    if not messages:
        return "No recent conversations found."
    
    try:
        msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
        snippet = msg.get('snippet', '')
        headers = msg.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
        date = next((h['value'] for h in headers if h['name'].lower() == 'date'), 'Unknown Date')
        return f"Latest: {subject} ({date})\nSnippet: {snippet}"
    except Exception as e:
        return f"Error fetching message: {e}"

def main():
    service = get_gmail_service()
    df = pd.read_excel(DEALS_PATH, header=4)
    df = df.dropna(subset=['Name'])
    
    # Filter for active deals (first section or non-Pass)
    active_df = df[df['Status'] != 'Pass'].head(20) 
    
    for _, row in active_df.iterrows():
        name = row['Name']
        contacts = row['Contacts']
        stage = row['Seed Round Stage']
        if pd.isna(stage) or stage == 'Name': continue # Skip header rows or empty stages
        
        print(f"\n--- {name} (Stage: {stage}) ---")
        status = search_investor(service, name, contacts)
        print(status)

if __name__ == "__main__":
    main()
