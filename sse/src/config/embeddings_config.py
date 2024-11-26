from .base_config import OPENAI_API_KEY

# Embedding model to use
EMBEDDING_MODEL = "text-embedding-ada-002"
MAX_INPUT_TOKENS = 1024  # Define a reasonable limit
RETRY_LIMIT = 3  # Maximum number of retries for API calls
BACKOFF = 2  # Exponential backoff base

# Validate OpenAI API Key
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set or is invalid.")
