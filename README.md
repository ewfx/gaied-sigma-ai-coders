# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
The project revolves around classification of emails to improve routing to loan system. So as to minimize human intervention and effort.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
A lot of manpower goes into reading and classifying emails based on the type of function they are trying to achieve. So, to have minimal human involvement in this classification by involving LLM's to classify these emails from the data that we have extracted from emails and their attachments.
## ⚙️ What It Does
This project automates email classification for financial service requests. It extracts key fields from email bodies and attachments, identifies the primary request type and subrequests, and assigns them for processing. It uses LLMs for classification, OCR for text extraction, and FAISS for duplicate detection, ensuring accurate and efficient handling of service requests. 

## 🛠️ How We Built It
Backend: 
Flask (Python) – API for processing email files.

AI Model:
Hugging Face's Mistral-7B-Instruct-v0.3 for text classification.

Embeddings & Similarity Search:
FAISS (Facebook AI Similarity Search) to detect duplicate emails.

OCR & Text Extraction:
pdfplumber for extracting text from PDFs.
python-docx for DOCX processing.
pytesseract for OCR-based extraction.

Prompt Engineering:
LangChain to generate structured prompts for classification.


## 🚧 Challenges We Faced

Handling Long Emails & Attachments:

Some emails exceeded LLM token limits, requiring truncation & prioritization strategies.
Multi-Intent Detection:

Ensuring only one primary request type is selected while capturing subrequests.
Duplicate Email Handling:

Emails forwarded or replied multiple times needed FAISS-based similarity detection.


Non-Technical Challenges:

Defining Extraction Rules:

Financial emails contain inconsistent formats, requiring configurable extraction rules.
Balancing Accuracy & Performance:

Optimizing between classification accuracy and processing time, especially for large attachments.


## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/your-repo.git
   ```
2. Install dependencies  
   ```sh
   pip install -r requirements.txt (for Python)
   ** Update the hugging face model api token in the code - llm_calls.py **
   ```
3. Run the project  
   ```sh
   python main.py
   
   ```

## 🏗️ Tech Stack
- 🔹 Backend: Flask
- 🔹 Other: Hugging Face's Mistral-7B-Instruct-v0.3 / FAISS / LangChain

## 👥 Team
- Nalini R
- Viral Bundella Ashwin
- Rahul Srivastava
- Dhirav Choudhary
- Shaik Saheb S
