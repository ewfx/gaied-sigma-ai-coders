# 🚀 Gen AI-based Email Classification And OCR
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
Provided automation for email classification of commercial loan bank transaction types and extracted vital information from the email content for the generation of the service loan workflow.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
Manual intervention by an email gatekeeper to scan loan email types and feed those details into a loan service workflow would be a tedious and lengthy process, also prone to human error. We identified an opportunity in this problem to reduce manual interventions and process more loan types than regular human intervention allows.

## ⚙️ What It Does
Email similarity check using Faiss index.
Email extraction using Tesseract OCR and PDFPlumber.
Prompt template to identify loan service request types and subtypes, extracting relevant information about the deal from the loan request type.
LLM classifies the email context and extracts key details of the deal from the email content and attachments.

## 🛠️ How We Built It
We used Python Flask API to provide enpoints API, tesseract OCR to extract details from image, pdf plumber to extract content details from email pdf ,LLM Langhchain Hugging face to provide RAG based responses.
## 🚧 Challenges We Faced
Setting up the infrastructure , most of times teams members encounter TokenLimitException which hinder the development completion.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/your-repo.git](https://github.com/ewfx/gaied-sigma-ai-coders.git
   ```
2. Install dependencies  
    pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   python main.py
   ```

## 🏗️ Tech Stack
- 🔹 Backend: Flask API/Python , LLM Langchain
- 

## 👥 Team

- **SIGMA-AI-CODERS** - [GitHub](#) | [LinkedIn](#)
- Nalini R
- Saheb Sheikh
- Dhirav Choudhary
- Viral Bundella
- Rahul Srivastava
 
