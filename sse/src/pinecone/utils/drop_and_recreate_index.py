from src.pinecone.client import initialize_pinecone
from src.config.pinecone_config import INDEX_NAME, DIMENSION, CLOUD, REGION, METRIC
from pinecone import ServerlessSpec
from src.pinecone.utils.index_exists import index_exists

def drop_and_recreate_index():
    """
    Drop the Pinecone index if it exists and recreate it.
    """
    pc = initialize_pinecone()
    if index_exists(pc, INDEX_NAME):
        print(f"Dropping index: {INDEX_NAME}")
        pc.delete_index(INDEX_NAME)
        print(f"Index {INDEX_NAME} dropped.")
    
    print(f"Creating index: {INDEX_NAME}")
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric=METRIC,
        spec=ServerlessSpec(
            cloud=CLOUD,
            region=REGION
        )
    )
    print(f"Index {INDEX_NAME} created.")
    return pc.Index(INDEX_NAME)
