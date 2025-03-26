import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from utils.email_processing import extract_email_text_and_attachment_text

# Load a sentence embedding model (Hugging Face MiniLM)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize FAISS index
embedding_dim = 384  # Dimension of embeddings
index = faiss.IndexFlatL2(embedding_dim)  # L2 similarity search

# Track email filenames and embeddings
email_filenames = []
email_embeddings = []  

# Directory containing PDFs, DOCX, and EML files
FOLDER = "data/datastore"

### 1️⃣ Add existing emails to FAISS ###
def add_existing_emails():
    """Indexes all existing emails before performing duplicate checks."""
    global email_filenames, index, email_embeddings  

    for file in os.listdir(FOLDER):
        file_path = os.path.join(FOLDER, file)

        if file.endswith((".pdf", ".docx", ".eml")):
            email_text, attachment_text = extract_email_text_and_attachment_text(file_path)
            text = email_text + attachment_text

            if text:
                embedding = model.encode(text, convert_to_numpy=True)
                email_embeddings.append(embedding)
                email_filenames.append(file)

    # Convert embeddings to NumPy and add to FAISS
    if email_embeddings:  
        email_embeddings_np = np.array(email_embeddings, dtype=np.float32)
        index.add(email_embeddings_np)

### 2️⃣ Check similarity of a new email ###
def check_duplicate(file_path, email_text, attachment_text, threshold=0.6):
    """Check if a new email is similar to existing emails in FAISS."""
    new_text = email_text + attachment_text
    new_embedding = model.encode(new_text, convert_to_numpy=True).reshape(1, -1)

    if index.ntotal == 0:
        return False, None, 0  # No previous emails stored yet

    # Search for the 2 closest matches
    D, I = index.search(new_embedding, k=2)

    if len(I[0]) > 1 and I[0][1] != -1:  # Ensure valid match
        second_best_match_idx = I[0][1]
        similarity_score = 1 - (D[0][1] / 2)  # Normalize similarity (1 = identical)

        if similarity_score >= threshold:
            return True, email_filenames[second_best_match_idx], round(similarity_score, 2)

    return False, None, round(1 - (D[0][0] / 2), 2)  # Return highest similarity

### 3️⃣ Process new email (Check & Add if Unique) ###
def check_emailSimilarity(file_path, email_text, attachment_text):
    """Checks for duplicates and adds the email to FAISS if unique."""
    is_dup, matched_file, similarity = check_duplicate(file_path, email_text, attachment_text)

    print(f"\nProcessing: {file_path}")
    if is_dup or similarity >= 1.0:
        print(f"🚨 Duplicate detected! Similar to: {matched_file} (Score: {similarity})")
    else:
        print(f"✅ No duplicates found. Adding to database. (Score: {similarity})")
        text = email_text + attachment_text
        embedding = model.encode(text, convert_to_numpy=True).reshape(1, -1)
        index.add(embedding)
        email_filenames.append(os.path.basename(file_path))
    
    return similarity
