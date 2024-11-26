from src.pinecone.client import initialize_pinecone
from src.config.pinecone_config import INDEX_NAME
from src.pinecone.utils.index_exists import index_exists

def get_index():
    """
    Return the Pinecone index for use. If the index doesn't exist, raise an error.
    """
    pc = initialize_pinecone()
    if not index_exists(pc, INDEX_NAME):
        raise ValueError(f"Index {INDEX_NAME} does not exist. Please create it first.")
    return pc.Index(INDEX_NAME)
