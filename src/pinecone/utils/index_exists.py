def index_exists(pc, index_name: str) -> bool:
    """
    Check if a Pinecone index exists.
    """
    return index_name in [idx.name for idx in pc.list_indexes()]
