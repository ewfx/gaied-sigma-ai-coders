import os
from utils.pdf_processing import extract_text_from_pdf, extract_text_from_images, extract_text_from_embedded_pdfs
from utils.docx_processing import extract_text_from_docx, extract_text_from_images_in_docx, extract_text_from_embedded_pdfs_in_docx
from utils.eml_processing import process_eml

def extract_email_text_and_attachment_text(file_path):
    """Extracts text based on file type (PDF or DOCX or eml)."""
    file_extension = os.path.splitext(file_path)[-1].lower()
    
    if file_extension == ".pdf":
        text_pdf = extract_text_from_pdf(file_path)
        text_images = extract_text_from_images(file_path)
        text_embedded = extract_text_from_embedded_pdfs(file_path)
        return text_pdf , text_images + "\n" + text_embedded

    elif file_extension == ".docx":
        text_docx = extract_text_from_docx(file_path)
        text_images = extract_text_from_images_in_docx(file_path)
        text_embedded = extract_text_from_embedded_pdfs_in_docx(file_path)
        return text_docx , text_images + "\n" + text_embedded
    
    elif file_extension == ".eml":
        dict_text= process_eml(file_path)
        dict_text["email_body"]
        attachment_text=''
        for attachment in dict_text["attachments"]:
            attachment_text+= attachment["content"]+"\n"
        return dict_text["email_body"],attachment_text

    else:
        return "Unsupported file type."


# Example Usage
# file_path = "/content/test.docx"  # Change to .docx for DOCX emails
# email_text,attachment_text = extract_email_text_and_attachment_text(file_path)

# print("Extracted Email Text:\n", email_text)
# print("Extracted attachment Text:\n",attachment_text)