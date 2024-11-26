from src.pinecone.utils.validation import validate_metadata, prepare_metadata


"""
Metadata to include for query filters:
- type?
- category?

"""
def upsert_embeddings(index, embedding_id: str, embedding_vector: list, metadata: dict):
    """
    Upserts a single embedding into the Pinecone index with enhanced debugging and validation.
    """
    try:
        print(f"Upserting: ID={embedding_id}, Metadata={metadata}, Vector size={len(embedding_vector)}")

        # Prepare and validate metadata
        metadata = prepare_metadata(metadata)
        validate_metadata(metadata)

        # Perform the upsert
        index.upsert(
            vectors=[
                {
                    "id": embedding_id,
                    "values": embedding_vector,
                    "metadata": metadata
                }
            ]
        )
        print(f"Successfully upserted ID={embedding_id}")
    except Exception as e:
        print(f"Error upserting ID={embedding_id}: {e}")
        raise
