from pinecone import Pinecone
from src.config.base_config import PINECONE_API_KEY

def initialize_pinecone():
    """
    Initialize and return the Pinecone client.
    """
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is not set in the configuration.")
    return Pinecone(api_key=PINECONE_API_KEY)
