import docx2txt
import pytesseract
from PIL import Image, UnidentifiedImageError
import fitz  # PyMuPDF for extracting embedded PDFs
import zipfile
import io
import os
import re

pytesseract.pytesseract.tesseract_cmd = r"D:\project\tesseract.exe"

def extract_text_from_docx(docx_path):
    """Extracts plain text from a DOCX file."""
    return docx2txt.process(docx_path)

def extract_text_from_images_in_docx(docx_path):
    """Extracts text from images inside a DOCX file using OCR (Tesseract)."""
    extracted_text = ""

    with zipfile.ZipFile(docx_path, "r") as docx_zip:
        image_files = [f for f in docx_zip.namelist() if f.startswith("word/media/") and f.endswith((".png", ".jpg", ".jpeg"))]

        for img_file in image_files:
            try:
                with docx_zip.open(img_file) as img_data:
                    image = Image.open(io.BytesIO(img_data.read()))

                    # Convert image to text using OCR
                    text = pytesseract.image_to_string(image)
                    text = re.sub(r'\n+', '\n', text)  # Remove multiple newlines
                    extracted_text += text + "\n"

            except UnidentifiedImageError:
                print(f"⚠️ Skipping invalid image: {img_file}")

    return extracted_text.strip()

def extract_text_from_embedded_pdfs_in_docx(docx_path):
    """Extracts text from embedded PDFs inside a DOCX file."""
    extracted_text = ""

    with zipfile.ZipFile(docx_path, "r") as docx_zip:
        pdf_files = [f for f in docx_zip.namelist() if f.endswith(".pdf")]

        for pdf_file in pdf_files:
            try:
                with docx_zip.open(pdf_file) as pdf_data:
                    pdf_stream = io.BytesIO(pdf_data.read())  # Convert to file-like object

                    # Open and extract text from the embedded PDF
                    doc = fitz.open(pdf_stream)
                    for page in doc:
                        text = page.get_text()
                        if text:
                            extracted_text += text + "\n"

            except Exception as e:
                print(f"⚠️ Error extracting embedded PDF '{pdf_file}': {e}")

    return extracted_text.strip()

# DOCX path
# docx_path = "/content/test.docx"  # Replace with your actual file path

# # Extract different types of content
# text_from_docx = extract_text_from_docx(docx_path)
# text_from_images = extract_text_from_images_in_docx(docx_path)
# text_from_attachments = extract_text_from_embedded_pdfs_in_docx(docx_path)

# # Print results
# print("📄 Extracted Text from DOCX:\n", text_from_docx)
# print("\n🖼️ Extracted Text from Images in DOCX:\n", text_from_images)
# print("\n📎 Extracted Text from Embedded PDFs in DOCX:\n", text_from_attachments)
