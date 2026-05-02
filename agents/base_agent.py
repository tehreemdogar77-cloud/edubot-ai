import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        self.system_prompt = "You are a helpful AI assistant."

    def call_llm(self, user_message: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def run(self, state: dict) -> dict:
        raise NotImplementedError("Each agent must have its own run() method")