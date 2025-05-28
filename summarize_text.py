import os
import requests
from huggingface_hub import InferenceClient

# Setup
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise EnvironmentError("HF_API_KEY environment variable not set.")

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def summarize_text(text, lang='en'):
    client = InferenceClient(token=HF_API_KEY)

    # Truncate if needed
    if len(text) > 3000:
        text = text[:3000]

    prompt = f"""
Summarize the following YouTube transcript in {lang}.

Provide:
- A concise summary (1–2 lines).
- Key takeaways in bullet points.

Transcript:
{text}
"""

    payload = {"inputs": prompt}
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        
        result = response.json()
        if isinstance(result, list) and 'summary_text' in result[0]:
            return result[0]['summary_text'].strip()
        else:
            return f"Unexpected response format: {result}"
    except Exception as e:
        return f"Exception occurred: {e}"
