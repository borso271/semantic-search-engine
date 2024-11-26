from .base_config import PINECONE_API_KEY, PINECONE_ENVIRONMENT

# Validate Pinecone configuration
if not PINECONE_API_KEY:
    raise RuntimeError("PINECONE_API_KEY is not set in the environment variables.")
if not PINECONE_ENVIRONMENT:
    raise RuntimeError("PINECONE_ENVIRONMENT is not set in the environment variables.")

# Pinecone-specific configurations
INDEX_NAME = "semantic-search"
DIMENSION = 1536  # Embedding vector size
METRIC = "cosine"  # Similarity metric, Text and Semantic Similarity, alternatives: 
REGION = "us-east-1"  # Default region for Pinecone (my free user)
CLOUD = "aws"

# Query parameters
DEFAULT_TOP_K = 5  # Number of results to return
DEFAULT_MIN_RELEVANCY = 0.7  # Minimum similarity score for a result

MAX_TIME_PER_ARTICLE = 1.0
PERCENTAGE_OF_DATABASE_TO_INDEX = 0.001