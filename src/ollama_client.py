import requests
import json

class OllamaClient:
    def __init__(self, model="llama3.2"):
        self.base_url = "http://localhost:11434/api"
        self.model = model

    def generate_response(self, prompt, system_prompt=None):
        """
        Generate a response from the Ollama API
        """
        url = f"{self.base_url}/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to Ollama API: {str(e)}")

    def get_context(self):
        """
        Get the current context of the conversation
        """
        try:
            response = requests.get(f"{self.base_url}/context")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to get context: {str(e)}")