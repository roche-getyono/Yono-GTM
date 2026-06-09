
import csv
import re
import openpyxl
import os

csv_path = r"c:\Users\danie\OneDrive\Desktop\YONO OUTBOUND GTM\Israeli Early-Stage VC Landscape - Israeli Early-Stage VC Landscape.csv"
status_path = r"c:\Users\danie\OneDrive\Desktop\YONO FUNDRAISE\context\investor_status.txt"
xlsx_path = r"c:\Users\danie\OneDrive\Desktop\YONO FUNDRAISE\context\investor_tracking.xlsx"

# 1. Read CSV
landscape_vcs = []
with open(csv_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        landscape_vcs.append({
            'name': row['Firm Name'],
            'score': int(row['Weighted FIT Score (1-100)']),
            'gp': row['Key GP/Partner'],
            'rationale': row['Fit Rationale']
        })

# 2. Read Status File
status_vcs = set()
if os.path.exists(status_path):
    with open(status_path, mode='r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        # Find lines like --- Meron Capital (Stage: CTO Meeting) ---
        matches = re.findall(r'--- (.*?) \(Stage:', content)
        for m in matches:
            status_vcs.add(m.strip().lower())

# 3. Read XLSX
tracking_vcs = set()
if os.path.exists(xlsx_path):
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active
    # Assuming the first column (A) contains firm names after the header
    for row in ws.iter_rows(min_row=2, max_col=1, values_only=True):
        if row[0]:
            tracking_vcs.add(str(row[0]).strip().lower())

# 4. Cross Reference
in_contact = []
remaining = []

def normalize(name):
    # Basic normalization to improve matching
    name = name.lower().replace('ventures', '').replace('capital', '').replace('partners', '').replace('israel', '').replace('fund', '').replace('.', '').strip()
    return name

contacted_normalized = {normalize(name) for name in status_vcs.union(tracking_vcs)}

for vc in landscape_vcs:
    norm_name = normalize(vc['name'])
    found = False
    if norm_name in contacted_normalized:
        found = True
    else:
        # Check if any part of the name matches
        for c in contacted_normalized:
            if norm_name in c or c in norm_name:
                found = True
                break
    
    if found:
        in_contact.append(vc)
    else:
        remaining.append(vc)

# Output Results
print("--- IN CONTACT ---")
for vc in in_contact:
    print(f"- {vc['name']} (Score: {vc['score']})")

print("\n--- TOP REMAINING PROSPECTS ---")
# Sort by score descending
remaining.sort(key=lambda x: x['score'], reverse=True)
for vc in remaining[:15]:
    print(f"- {vc['name']} (Score: {vc['score']}) | GP: {vc['gp']}")
    print(f"  Rationale: {vc['rationale']}")
