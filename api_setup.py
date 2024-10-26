import openai
import os

def setup_openai_api():
    # Set your OpenAI API key securely
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure this environment variable is set