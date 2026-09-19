from app.pdf_loader import load_pdf


pages = load_pdf("data/sample.pdf")

for page in pages:
    print(f"\n--- Page {page['page_number']} ---")
    print(page["text"][:500])