from pdf2image import convert_from_path
import easyocr
import numpy as np
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        # Debug statement to print the PDF file path
        print(f"PDF file path: {pdf_path}")
        
        # Specify the path to the Poppler bin directory
        poppler_path = r"C:\Program Files\poppler-24.08.0\Library\bin"
        print(f"Poppler path: {poppler_path}")
        
        # Convert PDF pages to images using pdf2image
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        print(f"Converted {len(images)} images from PDF.")
        
        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'])  # Specify the languages you want to support
        
        # Extract text from each image using EasyOCR
        text = ""
        for i, img in enumerate(images):
            try:
                # Convert PIL image to NumPy array
                img_array = np.array(img)
                
                # Use EasyOCR to extract text
                result = reader.readtext(img_array)
                
                # Join the extracted text from all bounding boxes
                extracted_text = " ".join([res[1] for res in result])
                text += extracted_text + "\n"
                
                # Print the first 500 characters of the extracted text for debugging
                print(f"Extracted text from image {i + 1}: {extracted_text[:500]}")
            except Exception as e:
                print(f"Error extracting text from image {i + 1}: {e}")
        
        # Print the first 500 characters of the total extracted text
        print(f"Total extracted text: {text[:500]}")
        
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""