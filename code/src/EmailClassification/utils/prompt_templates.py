from langchain import PromptTemplate

email_prompt_template = PromptTemplate(
    template="""
    You are an AI that extracts structured fields and detects request types from emails related to financial transactions.
    Extract the expected fields for each request. Determine the primary intent based on the sender's main ask.
    Identify the primary request based on the primary intent of the email.

    **Priority Extraction Rules:**
    1. Identify request types **only from the email content**.
    2. Extract all fields from the **email first**.
    3. If numerical fields (e.g., amounts, balances, ABA numbers) are **missing in the email**, extract them from the **attachment**.
    4. Combine extracted data while maintaining priority.


    **Email Content:**
    {email}

    **Attachment Content (if available):**
    {attachment}

    **JSON Output Format:**
    ```json
    {{
        "primary_request": {{
            "request_type": "[Detected primary request type]",
            "fields": {{
                "deal_name": "[Value or null]",
                "deal_CUSIP": "[Value or null]",
                "facility_CUSIP": "[Priority: Email → Attachment]",
                "lender_share_amount": "[Priority: Email → Attachment]",
                "new_lender_share_balance": "[Priority: Email → Attachment]",
                "previous_global_principal_balance": "[Priority: Email → Attachment]",
                "new_global_principal_balance": "[Priority: Email → Attachment]",
                "payment_effective_date": "[Value or null]",
                "borrower": "[Value or null]",
                "ABA_number": "[Priority: Email → Attachment]",
                "account_number": "[Priority: Email → Attachment]",
                "reference_details": "[Value or null]"
            }}
        }},
        "subrequests": [
            {{
                "request_type": "[Detected subrequest type]",
                "fields": {{
                    "deal_name": "[Value or null]",
                    "deal_CUSIP": "[Value or null]",
                    "facility_CUSIP": "[Priority: Email → Attachment]",
                    "lender_share_amount": "[Priority: Email → Attachment]",
                    "new_lender_share_balance": "[Priority: Email → Attachment]",
                    "previous_global_principal_balance": "[Priority: Email → Attachment]",
                    "new_global_principal_balance": "[Priority: Email → Attachment]",
                    "payment_effective_date": "[Value or null]",
                    "borrower": "[Value or null]",
                    "ABA_number": "[Priority: Email → Attachment]",
                    "account_number": "[Priority: Email → Attachment]",
                    "reference_details": "[Value or null]"
                }}
            }}
        ]
    }}
    ```
    """,
    input_variables=["email", "attachment"]
)
