"""
Client for communicating with Ollama API
"""
import requests
import json
from typing import Optional, Dict, Any
from .utils.text_formatter import TextFormatter as Fmt

class OllamaClient:
    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.context = None  # Store conversation context
        self._test_connection()

    def _test_connection(self):
        """Test connection to Ollama server"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(Fmt.failure_text("Failed to connect to Ollama server!"))
            print(Fmt.system_message("Make sure Ollama is running and accessible."))
            raise ConnectionError(f"Ollama server connection failed: {str(e)}")

    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from the Ollama API

        Args:
            prompt (str): The user's prompt
            system_prompt (str, optional): System prompt to guide the model's behavior

        Returns:
            str: The generated response
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "context": self.context
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

            # Update context for conversation continuity
            if 'context' in data:
                self.context = data['context']

            return data["response"]

        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to generate response: {str(e)}"
            print(Fmt.failure_text(error_msg))
            return "I apologize, but I'm having trouble connecting to my thinking apparatus. Please try again."

    def reset_context(self):
        """Reset the conversation context"""
        self.context = None

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        try:
            response = requests.get(f"{self.base_url}/api/show", params={"name": self.model})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return {}

    def _format_prompt(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Format the prompt with optional system prompt"""
        if system_prompt:
            return f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
        return f"User: {prompt}\nAssistant:"