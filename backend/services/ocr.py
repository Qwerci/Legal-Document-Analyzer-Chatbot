from pdf2image import convert_from_path
import pytesseract


def extract_text_from_pdf(pdf_path: str) -> str :
    try:
        images = convert_from_path(pdf_path)
        text = "\n".join([pytesseract.image_to_string(img) for img in images])
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""