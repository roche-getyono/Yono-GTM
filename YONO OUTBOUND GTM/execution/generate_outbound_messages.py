import pandas as pd
import os
import re

# Paths
INPUT_CSV = r'c:\Users\danie\OneDrive\Desktop\YONO OUTBOUND GTM\3_output\Phase1_Warm_Targets.csv'
OUTPUT_CSV = r'c:\Users\danie\OneDrive\Desktop\YONO OUTBOUND GTM\4_final_outputs\LinkedIn_Outbound_Worklist.csv'

# Self-Exclusion
EXCLUDE_NAMES = ['Daniel Roche', 'Daniel Blokh']

def clean_name(name):
    """Remove emojis and extra whitespace from names."""
    if not isinstance(name, str):
        return ""
    # Remove emojis (non-ascii)
    name = name.encode('ascii', 'ignore').decode('ascii')
    # Remove special chars but keep space and hyphen
    name = re.sub(r'[^\w\s-]', '', name)
    return name.strip()

def generate_message(first_name, company, position):
    """Draft a concise, peer-to-peer message for SaaS targets."""
    first_name = clean_name(first_name)
    company = clean_name(company)
    
    # Logic to adjust the "light touch" opening
    pos_low = position.lower()
    if any(word in pos_low for word in ['founder', 'ceo']):
        opening = f"Hey {first_name}, saw you're building {company} - congrats on the progress."
    elif any(word in pos_low for word in ['product', 'cpo']):
        opening = f"Hey {first_name}, saw what you're building at {company} - very cool."
    else:
        opening = f"Hey {first_name}, noticed you're at {company}."

    # Updated Template: Much shorter, less wordy, "Tech CEO" tone.
    message = (
        f"{opening}\n\n"
        f"I'm building Yono. We turn complex UIs into natural language execution interfaces overnight. "
        f"Since {company} has a lot of surface area, I'd love to show you how we'd handle it.\n\n"
        f"Free for 15 mins later this week?"
    )
    return message

def main():
    if not os.path.exists(INPUT_CSV):
        print(f"Error: {INPUT_CSV} not found.")
        return

    df = pd.read_csv(INPUT_CSV)
    
    # Filter for SaaS Targets
    targets = df[df['Category'] == 'SaaS Target'].copy()
    
    # Apply exclusions
    targets['Full Name'] = targets['First Name'] + ' ' + targets['Last Name']
    targets = targets[~targets['Full Name'].isin(EXCLUDE_NAMES)]

    # Take first 20 for initial batch
    batch = targets.head(20)

    new_rows = []
    for _, row in batch.iterrows():
        draft = generate_message(row['First Name'], row['Company'], row['Position'])
        
        new_rows.append({
            'Name': f"{row['First Name']} {row['Last Name']}",
            'Company': row['Company'],
            'Position': row['Position'],
            'URL': row['URL'],
            'Draft Message': draft,
            'Status': 'Pending',
            'Connected On': row['Connected On'],
            'Notes': ''
        })

    if new_rows:
        new_df = pd.DataFrame(new_rows)
        # Overwrite the worklist with refined drafts
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
        new_df.to_csv(OUTPUT_CSV, index=False)
        print(f"Successfully generated {len(new_rows)} ultra-concise refined messages in {OUTPUT_CSV}")
    else:
        print("No targets to process.")

if __name__ == "__main__":
    main()
