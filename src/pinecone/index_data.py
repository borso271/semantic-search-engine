import time
from src.postgres.query_operations import fetch_articles
from src.embeddings.generate_article_embedding import generate_embedding
from src.pinecone.utils.drop_and_recreate_index import drop_and_recreate_index
from src.pinecone.upsert_embeddings import upsert_embeddings

import time

from src.config.pinecone_config import MAX_TIME_PER_ARTICLE, PERCENTAGE_OF_DATABASE_TO_INDEX, DIMENSION


def validate_indexing(index, indexed_ids):
    """
    Validate that the number of indexed vectors matches the expected number of input entries.
    :param index: Pinecone index object.
    :param indexed_ids: List of IDs that were attempted to be indexed.
    """
    try:
        # Fetch the number of vectors currently indexed in Pinecone
        index_stats = index.describe_index_stats()
        indexed_count = index_stats.get("total_vector_count", 0)
        expected_count = len(indexed_ids)

        if indexed_count != expected_count:
            print(f"Warning: Mismatch in vector count. Indexed in Pinecone: {indexed_count}, Expected: {expected_count}")

            # Retrieve all IDs from Pinecone in batches
            retrieved_ids = set()
            for batch in range(0, len(indexed_ids), 100):  # Adjust batch size as needed
                batch_ids = indexed_ids[batch:batch + 100]
                results = index.fetch(ids=batch_ids).get("vectors", {})
                retrieved_ids.update(results.keys())

            missing_ids = set(indexed_ids) - retrieved_ids
            print(f"Missing IDs: {missing_ids}")
        else:
            print(f"Validation successful. Indexed vectors match input entries ({indexed_count}/{expected_count}).")
    except Exception as e:
        print(f"Error validating index: {e}")



def index_data(content_type="pedia_article", max_time_per_article=MAX_TIME_PER_ARTICLE, percentage=PERCENTAGE_OF_DATABASE_TO_INDEX):
    """
    Fetch data from PostgreSQL, generate embeddings, and index them in Pinecone.
    :param content_type: Type of content being indexed (default: "pedia_article").
    :param max_time_per_article: Maximum time in seconds allowed to process an article. Defaults to 1 second.
    """
    # Set up the Pinecone index
    index = drop_and_recreate_index()

    # Fetch all articles to calculate total
    total_articles = fetch_articles(limit=None)
    print(f"Total articles in database: {len(total_articles)}")

    # Calculate limit based on percentage
    limit = max(1, int(len(total_articles) * percentage))
    articles = fetch_articles(limit)

    # Track successfully indexed articles
    successfully_indexed_ids = []

    for i, article in enumerate(articles, start=1):
        try:
            print(f"Processing article ID: {article['id']} (#{i})")
            start_time = time.time()

            # Generate embedding
            embedding = generate_embedding(article)

            # Check processing time
            processing_time = time.time() - start_time
            if processing_time > max_time_per_article:
                print(f"Skipping article ID {article['id']} due to timeout ({processing_time:.2f} seconds).")
                continue
           
            # Prepare metadata
            metadata = {
                "id": article["id"],
                "topic": article["topic"],
                "description": article.get("description", ""),
                "ageGroup": article.get("age_group", ""),
                "imageUrl": article.get("image_url", ""),
                "type": content_type
            }
            
            # Upsert into Pinecone
            upsert_embeddings(index, str(article["id"]), embedding, metadata)
            successfully_indexed_ids.append(article["id"])  # Track successfully indexed IDs

            print(f"Article ID {article['id']} indexed successfully.")
            print(f"Time taken: {processing_time:.2f} seconds")

        except Exception as e:
            print(f"Error indexing article ID {article['id']}: {e}")

    # Validate that all articles were indexed
    validate_indexing(index, successfully_indexed_ids)

    print(f"Indexed {len(successfully_indexed_ids)} articles out of {len(articles)}.")

if __name__ == "__main__":
    index_data()
