import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_intent(query: str) -> str:
    prompt = f"""
Classify this user query into one of the following categories:
- lead_qualification
- sales
- customer_support
- general_info
- out_of_scope

Query: {query}

Return only the category name.
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()
