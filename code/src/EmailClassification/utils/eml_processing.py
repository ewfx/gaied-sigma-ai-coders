import os
import io
import re
import fitz  # PyMuPDF for PDFs
from PIL import Image
import docx2txt
import pytesseract
from email import policy
from email.parser import BytesParser
from email import message_from_bytes
from docx import Document

pytesseract.pytesseract.tesseract_cmd = r"D:\project\tesseract.exe"

def process_eml(file_path):
    """Extracts text from EML files, including email body, PDFs, DOCX, and images."""
    extracted_data = {"email_body": "", "attachments": []}
    
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    # Extract email body (text & HTML)
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = part.get("Content-Disposition", "")
            
            # Extract plain text or HTML content
            if content_type == "text/plain":
                extracted_data["email_body"] += part.get_payload(decode=True).decode(errors="ignore") + "\n"
            elif content_type == "text/html":
                extracted_data["email_body"] += part.get_payload(decode=True).decode(errors="ignore") + "\n"
            
            # Process attachments
            if part.get_filename():
                file_data = part.get_payload(decode=True)
                file_name = part.get_filename()
                
                if file_name.lower().endswith(".pdf"):
                    text_from_pdf = extract_text_from_pdf(file_data)
                    text_from_images = extract_text_from_images(file_data)
                    text_from_embedded_pdfs = extract_text_from_embedded_pdfs(file_data)
                    extracted_text = f"📄 Text from PDF:\n{text_from_pdf}\n🖼️ Text from Images:\n{text_from_images}\n📎 Text from Embedded PDFs:\n{text_from_embedded_pdfs}"
                
                elif file_name.lower().endswith(".docx"):
                    extracted_text = extract_text_from_docx(file_data)
                
                elif file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                    image = Image.open(io.BytesIO(file_data))
                    # Extract text using Tesseract OCR
                    extracted_text = pytesseract.image_to_string(image).strip()
                
                else:
                    extracted_text = f"[Unsupported File: {file_name}]"

                extracted_data["attachments"].append({"filename": file_name, "content": extracted_text})
    
    return extracted_data

# Test with an EML file
# eml_file_path = "/content/Message_.eml"
# result = process_eml(eml_file_path)

# # Print extracted content
# print("📩 Email Body:\n", result["email_body"])
# for attachment in result["attachments"]:
#     print(f"\n📎 Attachment ({attachment['filename']}):\n{attachment['content']}")
