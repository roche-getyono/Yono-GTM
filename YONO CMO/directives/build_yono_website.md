# Directive: Build Yono Landing Page

## Goal
Create a production-grade, visually stunning landing page for Yono that embodies the "Code & Chaos" brand identity and the "Reliable Context Layer" mission.

## Inputs
- `yono_master_context.md`: Synthesized messaging from Pitch Deck & GTM.
- `Yono Deck.pdf`: For specific ROI metrics and problem framing.
- `Pilot_VC_Outreach.md`: For ICP and "V2" messaging.
- `skills/yono-brand-guidelines/SKILL.md`: For the color palette and typography.
- `SKILLDES.md` & `ui-designer.md`: For UI/UX best practices.

## Tools/Scripts
- `execution/extract_deck_text.py`: Python script for PDF extraction.
- `execution/generate_hero_image.py`: (Optional) Script to use `generate_image` for the hero section.

## Outputs
- `index.html`: The main landing page (V2 - Enriched Context).
- `index.css`: The custom "Code & Chaos" design system.
- `assets/`: Generated images and icons.

## Instructions
1. **Analyze Messaging**: Focus on "Reliability vs. Hype". Use the Grey Jedi manifesto. [COMPLETED: Integrated Deck/GTM Stats]
2. **Design System**: 
   - Background: Terminal Black (#161618).
   - Accents: Chaos Lavender (#6E56CF).
   - Fonts: JetBrains Mono (Headers), Inter (Body).
3. **Sections**:
   - Hero: "Code is the Only Source of Truth". High-impact visual.
   - The Problem: "Empire of Hype" (Vaporware Orange #E54D2E warnings).
   - The Solution: "Reliable Context Layer".
   - Feature Grid: Bento grid style with Grey Jedi (#232326) cards.
4. **Interactions**:
   - Subtle terminal-style typing effects.
   - Glitch hover effects on Chaos Lavender buttons.
   - Staggered entry animations for cards.
5. **SEO**: Follow best practices from `web_application_development`.
