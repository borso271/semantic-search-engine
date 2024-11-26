def query_embeddings(index, query_vector: list, top_k: int = 5, min_relevancy: float = 0.7, filters: dict = None):
    """
    Queries the Pinecone index for similar embeddings with optional filters and a relevancy threshold.
    :param index: Pinecone index object.
    :param query_vector: Query vector for similarity search.
    :param top_k: Number of top results to return.
    :param min_relevancy: Minimum relevancy score to include a result.
    :param filters: Optional metadata filters to apply.
    :return: Filtered list of matches.
    """
    try:
        # Perform the Pinecone query
        query_params = {
            "vector": query_vector,
            "top_k": top_k,
            "include_metadata": True,
        }
        
        if filters:
            query_params["filter"] = filters

        results = index.query(**query_params)
    


        if "matches" in results and isinstance(results["matches"], list):
            # Filter results based on relevancy threshold
            filtered_results = [
                match for match in results["matches"] if match["score"] >= min_relevancy
            ]
            print(f"Filtered results (min_relevancy={min_relevancy}): {filtered_results}")
            return filtered_results
        else:
            print("Unexpected query result structure:", results)
            return []
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return []
