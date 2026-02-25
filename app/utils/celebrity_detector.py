import os
import base64
import requests
import logging

logger = logging.getLogger(__name__)

class CelebrityDetector:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct"

    def identify(self, image_bytes):
        encoded_image = base64.b64encode(image_bytes).decode()

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        prompt = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """You are a celebrity recognition expert AI.
Identify the person in the image. If known, respond EXACTLY in this format with no extra text:

- **Full Name**: <name>
- **Profession**: <profession>
- **Nationality**: <nationality>
- **Famous For**: <short description>
- **Top Achievements**:
- <achievement 1>
- <achievement 2>
- <achievement 3>
- <achievement 4>
- <achievement 5>

Important: Each achievement must be on its own line starting with '- '.
If the person is unknown, return only: Unknown."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.3,
            "max_tokens": 1024
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=prompt, timeout=30)

            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                name = self.extract_name(result)
                return result, name
            else:
                logger.error(f"Celebrity API error {response.status_code}: {response.text}")
                return None, ""

        except requests.exceptions.Timeout:
            logger.error("Celebrity API request timed out")
            return None, ""
        except Exception as e:
            logger.error(f"Celebrity API unexpected error: {e}")
            return None, ""

    def extract_name(self, content):
        for line in content.splitlines():
            if line.lower().startswith("- **full name**:"):
                return line.split(":", 1)[-1].strip()
        return "Unknown"
