
from src.embeddings.client import initialize_openai_client


# Initialize the OpenAI client
client = initialize_openai_client()

from src.config.embeddings_config import EMBEDDING_MODEL, MAX_INPUT_TOKENS, BACKOFF, RETRY_LIMIT

import re
import time
from typing import List
from openai import OpenAIError

# Constants


def clean_and_truncate_text(text: str, max_tokens: int = MAX_INPUT_TOKENS) -> str:
    """
    Clean and truncate text to ensure it meets API input limits.
    :param text: The input text to process.
    :param max_tokens: The maximum number of tokens allowed.
    :return: Cleaned and truncated text.
    """
    # Remove non-ASCII characters and collapse multiple spaces
    cleaned_text = re.sub(r"[^\x00-\x7F]+", " ", text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    
    # Truncate text to the maximum token limit
    return cleaned_text[:max_tokens] if len(cleaned_text) > max_tokens else cleaned_text

def generate_embedding(pedia_article: dict) -> List[float]:
    """
    Generate an embedding for a given article using OpenAI's API, combining topic, overview, and description.
    :param pedia_article: The input article containing 'topic', 'article', and 'description'.
    :return: A list of floats representing the text embedding.
    """
    try:
       
        # Extract and weigh components
        topic = pedia_article.get('topic', '')
        overview = pedia_article.get('article', {}).get('Overview', '')
        description = pedia_article.get('description', '')
      
        # Concatenate with weights
        text_to_embed = (
            (topic + " ") * 3 +  # Weight topic by repeating it 3 times
            (overview + " ") * 2 +  # Weight overview by repeating it 2 times
            description  # Include description without extra weight
        ).strip()

        # Clean and truncate text
        text_to_embed = clean_and_truncate_text(text_to_embed, max_tokens=MAX_INPUT_TOKENS)

        # Retry logic for API call
        for attempt in range(RETRY_LIMIT):
            try:
                # Generate embedding using OpenAI's API
                response = client.embeddings.create(
                    input=text_to_embed,
                    model=EMBEDDING_MODEL  # Use the model specified in the config
                )
                # Extract the embedding vector from the response
                return response.data[0].embedding
            except OpenAIError as e:
                print(f"API call failed on attempt {attempt + 1}: {e}")
                if attempt < RETRY_LIMIT - 1:
                    time.sleep(BACKOFF ** attempt)  # Exponential backoff
                else:
                    raise RuntimeError(f"Failed to generate embedding after {RETRY_LIMIT} attempts: {e}")
    except Exception as e:
        print(f"Error generating embedding: {e}")
        raise RuntimeError(f"Error generating embedding: {e}")
