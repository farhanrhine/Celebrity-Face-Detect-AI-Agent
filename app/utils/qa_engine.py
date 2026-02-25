import os
import requests
import logging

logger = logging.getLogger(__name__)

class QAEngine:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct"

    def ask_about_celebrity(self, name, question):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        prompt = f"""You are an AI assistant that knows a lot about celebrities.
Answer the following question about {name} concisely and accurately.
Question: {question}"""

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": 512
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                logger.error(f"QA API error {response.status_code}: {response.text}")
                return "Sorry, I couldn't get an answer right now. Please try again."

        except requests.exceptions.Timeout:
            logger.error("QA API request timed out")
            return "Request timed out. Please try again."
        except Exception as e:
            logger.error(f"QA API unexpected error: {e}")
            return "An unexpected error occurred. Please try again."
