import csv
import json
import os

def filter_contacts():
    # Paths
    config_path = os.path.join('2_config', 'icp_filters.json')
    input_path = os.path.join('1_input', 'Connections.csv')
    output_path = os.path.join('3_output', 'Phase1_Qualified_Warm_Leads.csv')

    # Load config
    with open(config_path, 'r') as f:
        config = json.load(f)

    target_titles = [t.lower() for t in config.get('target_titles', [])]
    target_industries = [i.lower() for i in config.get('target_industries', [])]
    exclude_keywords = [e.lower() for e in config.get('exclude_keywords', [])]

    title_matches = 0
    excluded_count = 0
    qualified_leads = []

    # Read CSV
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(input_path, 'r', encoding='utf-16') as f:
            lines = f.readlines()

    csv_start = 0
    for i, line in enumerate(lines):
        if 'First Name,' in line:
            csv_start = i
            break
    
    # Process lines from csv_start
    header = lines[csv_start].strip().split(',')
    reader = csv.DictReader(lines[csv_start:])
    
    row_count = 0
    for row in reader:
        row_count += 1
        
        # Combine first and last name
        name = f"{row.get('First Name', '')} {row.get('Last Name', '')}".strip()
        company = row.get('Company', '')
        position = row.get('Position', '')
        industry = row.get('Industry', '') # Might be None

        pos_lower = position.lower() if position else ""
        comp_lower = company.lower() if company else ""
        ind_lower = industry.lower() if industry else ""

        # Check for title match (at least one target title in position)
        title_match = False
        for tt in target_titles:
            if tt in pos_lower:
                title_match = True
                break
        
        if not title_match:
            continue
        
        title_matches += 1

        # Check for exclusions
        excluded = False
        for kw in exclude_keywords:
            if kw in pos_lower or kw in comp_lower:
                excluded = True
                break
        if excluded:
            excluded_count += 1
            continue

        # Check for industry match (REMOVED as per user request)
        # industry_match = False
        # ...
        
        # If we got here, it's a qualified lead
        qualified_leads.append({
            'Name': name,
            'Company': company,
            'Position': position
        })

    # Write output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Name', 'Company', 'Position'])
        writer.writeheader()
        writer.writerows(qualified_leads)

    print(f"Total rows processed: {row_count}")
    print(f"Rows matching titles: {title_matches}")
    print(f"Rows excluded: {excluded_count}")
    print(f"Total qualified leads found: {len(qualified_leads)}")
    for i, lead in enumerate(qualified_leads[:3]):
        print(f"Lead {i+1} Company: {lead['Company']}")

if __name__ == "__main__":
    filter_contacts()
