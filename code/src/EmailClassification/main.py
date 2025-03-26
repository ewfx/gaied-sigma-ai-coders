# ## main.py (Entry Point)
# import os
# from utils.email_processing import extract_email_text_and_attachment_text
# from utils.faiss_index import add_existing_emails, check_emailSimilarity
# from utils.llm_calls import classify_email

# def main():
#     # Load and process a sample file
#     file_path = "data/sample.pdf"  # Change this to process other file types

#     email_text, attachment_text = extract_email_text_and_attachment_text(file_path)
    
#     # Check for duplicates using FAISS
#     add_existing_emails()

#     similarity_score=check_emailSimilarity(file_path,email_text, attachment_text)
#     if similarity_score<0.5:
#         classify_email(email_text,attachment_text)


# if __name__ == "__main__":
#     main()
## main.py (Entry Point)
import os
from flask import Flask, request, jsonify
from utils.email_processing import extract_email_text_and_attachment_text
from utils.faiss_index import add_existing_emails, check_emailSimilarity
from utils.llm_calls import classify_email
import json
def extract_json_from_text(text):
    """Extracts JSON data from text using string parsing."""
    try:
        # Find the starting and ending point of the JSON block
        json_start = text.find("```json") + len("```json")
        json_end = text.rfind("```")

        if json_start == -1 or json_end == -1:
            raise ValueError("No JSON found in text")

        json_data = text[json_start:json_end].strip()
        return json.loads(json_data)  # Convert string to dictionary
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return {"error": "Invalid JSON format extracted"}
    
app = Flask(__name__)

@app.route("/process-email", methods=["POST"])
def process_email():
    data = request.get_json()
    pdf_name = data.get("pdf_name")
    if not pdf_name:
        return jsonify({"error": "PDF name is required"}), 400

    file_path = os.path.join("data", pdf_name)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    email_text, attachment_text = extract_email_text_and_attachment_text(file_path)
    
    # Check for duplicates using FAISS
    add_existing_emails()
    similarity_score = check_emailSimilarity(file_path, email_text, attachment_text)
    
    if similarity_score > 0.8:
        return jsonify({"message": "Duplicate detected", "similarity_score": similarity_score})
    else:        
        classification_result = classify_email(email_text, attachment_text)
        extracted_json = extract_json_from_text(classification_result["text"])

        return jsonify({
            "classification": extracted_json,  # Parsed JSON output
            "raw_text": classification_result["text"],  # Full raw model output
            "email_text": classification_result["email"],  # Original email body
            "attachment_text": classification_result["attachment"]  # Extracted attachment text
        })
   
       


if __name__ == "__main__":
    app.run(debug=True)

