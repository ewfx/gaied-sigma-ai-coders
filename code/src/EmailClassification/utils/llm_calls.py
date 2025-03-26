from langchain_huggingface import HuggingFaceEndpoint
from langchain import PromptTemplate, LLMChain
from utils.prompt_templates import email_prompt_template
import json
import os

def classify_email(email_text,attachment_text):
    sec_key=""
    print(sec_key)
    os.environ["HUGGINGFACEHUB_API_TOKEN"]=sec_key

    repo_id="mistralai/Mistral-7B-Instruct-v0.3"
    llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=1000,temperature=0.7,token=sec_key)

    llm_chain = LLMChain(llm=llm, prompt=email_prompt_template)

    # Invoke Model
    response = llm_chain.invoke({"email": email_text,"attachment":attachment_text})

    # Extract text response
    text_response = response["text"]
    print(response)
    print("Text Output:\n", text_response)

    # Extract JSON response using regex
    # json_match = re.search(r"```json\n(.*?)\n```", text_response, re.DOTALL)
    # if json_match:
    #     json_output = json.loads(json_match.group(1))
    #     print("\nJSON Output:\n", json.dumps(json_output, indent=2))
    # else:
    #     print("\nJSON Output: Could not parse JSON.")
