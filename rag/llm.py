import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "[router.huggingface.co](https://router.huggingface.co/models/google/flan-t5-base)"



def call_llm(prompt):
    if not HF_TOKEN:
        return {"error": "HF_TOKEN missing"}

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

        result = response.json()

        # handle HF response format
        if isinstance(result, list):
            return {"answer": result[0]["generated_text"]}

        return result

    except Exception as e:
        return {"error": str(e)}