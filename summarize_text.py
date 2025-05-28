import os
import requests


#only added hugging facehub and client lines two lines
from huggingface_hub import InferenceClient
# Choose your preferred model (BART, Pegasus, T5, etc.)


API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise EnvironmentError("HF_API_KEY environment variable not set.")

headers = {
    "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"  # Your Hugging Face token
}

def summarize_text(text, lang='en'):
    client = InferenceClient(token=os.getenv("HF_API_KEY"))
    # Truncate long text to avoid API limit issues (optional enhancement: chunking)
    if len(text) > 3000:
        text = text[:3000]

    prompt = f"""
    Summarize the following YouTube transcript in {lang}. Provide:
    Summary:
    (short summary)

    Key Takeaways:
    - (bullet points)
    
    Transcript:
    {text}
    """

    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"

    try:
        summary_text = response.json()[0]['summary_text']
        return summary_text
    except:
        return f"Unexpected error. Response: {response.text}"
