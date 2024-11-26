
from src.embeddings.client import initialize_openai_client


# Initialize the OpenAI client
client = initialize_openai_client()
from typing import List
import time
from openai import OpenAIError

EMBEDDING_MODEL = "text-embedding-ada-002"


def generate_query_embedding(query: str) -> List[float]:
    """
    Generate an embedding for a user query using OpenAI's API.
    :param query: The input query string.
    :return: A list of floats representing the query embedding.
    """
    try:
        # Ensure the query is stripped of excess whitespace
        cleaned_query = query.strip()

        # Generate embedding using OpenAI's API
        response = client.embeddings.create(
            input=cleaned_query,
            model=EMBEDDING_MODEL  # Use the model specified in the config
        )

        # Extract the embedding vector from the response
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating query embedding: {e}")
        raise RuntimeError(f"Error generating query embedding: {e}")