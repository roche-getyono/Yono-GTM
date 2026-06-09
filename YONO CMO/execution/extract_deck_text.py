from pypdf import PdfReader
import json

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text_content = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        text_content.append({
            "page": i + 1,
            "content": text
        })
    return text_content

if __name__ == "__main__":
    pdf_path = "Yono Deck.pdf"
    content = extract_text(pdf_path)
    with open(".tmp/deck_text.json", "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4)
    print("Extracted text to .tmp/deck_text.json")
