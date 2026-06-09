
import csv

network_path = r"c:\Users\danie\OneDrive\Desktop\YONO FUNDRAISE\VC_Network.csv"
targets = ["Lightspeed", "Vertex", "Angular", "Emerge", "Viola", "Battery", "Pitango", "Amiti", "Glilot", "NFX", "Team8", "Entree", "Entrée"]

matches = []

with open(network_path, mode='r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company = row.get('Company', '')
        for t in targets:
            if t.lower() in company.lower():
                matches.append({
                    'Name': f"{row['First Name']} {row['Last Name']}",
                    'Company': company,
                    'Position': row['Position'],
                    'Match': t
                })
                break

for m in matches:
    print(f"Match: {m['Match']} | {m['Name']} ({m['Position']}) at {m['Company']}")
