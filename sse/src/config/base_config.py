import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")
load_dotenv(dotenv_path=dotenv_path)

# Shared configurations
POSTGRES_DATABASE_NAME = os.getenv("POSTGRES_DATABASE_NAME")
POSTGRES_DATABASE_USER = os.getenv("POSTGRES_DATABASE_USER")
POSTGRES_DATABASE_PASSWORD = os.getenv("POSTGRES_DATABASE_PASSWORD")
POSTGRES_DATABASE_HOST = os.getenv("POSTGRES_DATABASE_HOST")
POSTGRES_DATABASE_PORT = os.getenv("POSTGRES_DATABASE_PORT")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")