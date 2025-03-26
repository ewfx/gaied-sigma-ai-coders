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
        
app = Flask(__name__)

@app.route("/process-email", methods=["POST"])
def process_email():
    data = request.get_json()

    file_name = data.get("file_name")
    if not file_name:
        return jsonify({"error": "Email file name is required"}), 400

    file_path = os.path.join("data", file_name)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    email_text, attachment_text = extract_email_text_and_attachment_text(file_path)
    
    # Check for duplicates using FAISS
    add_existing_emails()
    similarity_score = check_emailSimilarity(file_path, email_text, attachment_text)
    
    if similarity_score > 0.6:
        return jsonify({"message": "Duplicate detected", "similarity_score": similarity_score})
    else:        
        classification_result = classify_email(email_text, attachment_text)
        json_part=classification_result[classification_result.index("["):]
        return f"Not a duplicate Similarity_Score: {similarity_score})"+"\n"+json_part
        # print(json_part)

        # try:
        #     json_data = json.loads(json_part)  # Convert to Python dict
        #     return json_data
        # except (SyntaxError, ValueError) as e:
        #     return jsonify({"Error parsing JSON": e})
   
       


if __name__ == "__main__":
    app.run(debug=True)

