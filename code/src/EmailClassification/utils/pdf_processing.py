import pdfplumber
import pytesseract
from PIL import Image, UnidentifiedImageError
import fitz  # PyMuPDF for extracting embedded PDFs
import io
import re

pytesseract.pytesseract.tesseract_cmd = r"D:\project\tesseract.exe"


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file (excluding images and attachments)."""
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def extract_text_from_images(pdf_path):
    """Extracts text from images inside a PDF using OCR (Tesseract)."""
    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if not page.images:  # ✅ Skip pages without images
                continue

            for img_index, img in enumerate(page.images):
                try:
                    image_data = img["stream"].get_data()
                    image = Image.open(io.BytesIO(image_data))

                    # Convert image to text using OCR
                    text = pytesseract.image_to_string(image)
                    text = re.sub(r'\n+', '\n', text)  # Remove multiple newlines
                    extracted_text += text + "\n"

                except UnidentifiedImageError:
                    print(f"⚠️ Skipping invalid image on Page {i+1}, Image {img_index+1}")

    return extracted_text.strip()

def extract_text_from_embedded_pdfs(pdf_path):
    """Extracts text from embedded PDFs inside a PDF."""
    doc = fitz.open(pdf_path)
    extracted_text = ""

    for file in doc.embfile_names():  # Get all embedded file names
        try:
            file_data = doc.embfile_get(file)["file"]  # Get binary data
            pdf_stream = io.BytesIO(file_data)  # Convert to a file-like object

            # Read and extract text from the embedded PDF
            with pdfplumber.open(pdf_stream) as embedded_pdf:
                for page in embedded_pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"

        except Exception as e:
            print(f"⚠️ Error extracting embedded PDF '{file}': {e}")

    return extracted_text.strip()

# PDF path
# pdf_path = "/content/textdocimage.pdf"  # Replace with your actual file path

# # Extract different types of content
# text_from_pdf = extract_text_from_pdf(pdf_path)
# text_from_images = extract_text_from_images(pdf_path)
# text_from_attachments = extract_text_from_embedded_pdfs(pdf_path)

# # Print results
# print("📄 Extracted Text from PDF Pages:\n", text_from_pdf)
# print("\n🖼️ Extracted Text from Images:\n", text_from_images)
# print("\n📎 Extracted Text from Embedded PDFs:\n", text_from_attachments)
