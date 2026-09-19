import fitz


def load_pdf(pdf_path):
    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text()

        if text.strip():
            pages.append({
                "page_number": page_number + 1,
                "text": text
            })

    document.close()

    return pages