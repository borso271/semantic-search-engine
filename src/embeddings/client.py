from openai import OpenAI
from src.config.embeddings_config import OPENAI_API_KEY

def initialize_openai_client():
    """
    Initialize and return the OpenAI client.
    """
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        print("OpenAI client initialized successfully.")
        return client
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        raise RuntimeError(f"Error initializing OpenAI client: {e}")
