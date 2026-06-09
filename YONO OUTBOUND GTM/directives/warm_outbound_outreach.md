# Directive: LinkedIn Warm Outreach

## Goal
Convert warm LinkedIn connections into Design Partner discovery calls by sending personalized, high-context messages that highlight Yono's unique reliability and speed.

## Inputs
- `3_output/Phase1_Warm_Targets.csv`: The list of qualified connections.
- `2_config/yono_master_context.md`: The product value proposition and tone guidelines.

## Messaging Strategy
1. **Peer-to-Peer:** Message must come from Daniel (Founder) to another Founder/C-Suite/VP.
2. **The "Anti-Hype" Hook:** Acknowledge the AI noise but offer a "Reliable Context Layer" that bypasses hallucinations and long dev cycles.
3. **The Offer:** A quick 15-minute sync to show how Yono would handle *their* specific product logic overnight.

## Process
1. Use `execution/generate_outbound_messages.py` to draft messages for a batch of contacts.
2. The script should pull the First Name, Company, and Position to create a natural-sounding outreach.
3. Prioritize targets with "Founder", "CEO", or "VP Product" titles.

## Output
- `4_final_outputs/LinkedIn_Outbound_Worklist.csv`: A unified tracking sheet for all outreach efforts.
