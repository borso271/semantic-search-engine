from src.postgres.client import get_postgres_connection
from psycopg2.extras import RealDictCursor

def fetch_articles(limit=500):
    """
    Fetch articles from the `pedia_article` table.
    Optionally limit the number of rows.
    """
    query = """
        SELECT 
            id, 
            topic, 
            description, 
            age_group, 
            image_url
        FROM pedia_article
    """
    if limit:
        query += f" LIMIT {limit}"
    
    conn = get_postgres_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query)
        articles = cursor.fetchall()
        print(f"Fetched {len(articles)} articles from the database.")
        return articles

def fetch_articles_by_ids(ids): # not useful anymore
    """
    Fetch articles from PostgreSQL based on Pinecone result IDs.
    """
    # Convert IDs to integers
    int_ids = [int(id) for id in ids]

    conn = get_postgres_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT id, topic AS title, description
            FROM pedia_article
            WHERE id = ANY(%s)

            """,
            (int_ids,)
        )
        results = cursor.fetchall()

    # Log missing IDs for debugging
    fetched_ids = {article['id'] for article in results}
    missing_ids = set(int_ids) - fetched_ids
    if missing_ids:
        print(f"Warning: Missing IDs in database: {missing_ids}")

    return results




def fetch_all_article_by_ids(ids):
    """
    Fetch articles from PostgreSQL based on Pinecone result IDs.
    """
    # Convert IDs to integers
    int_ids = [int(id) for id in ids]

    conn = get_postgres_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT *
            FROM pedia_article
            WHERE id = ANY(%s)

            """,
            (int_ids,)
        )
        results = cursor.fetchall()

    # Log missing IDs for debugging
    fetched_ids = {article['id'] for article in results}
    missing_ids = set(int_ids) - fetched_ids
    if missing_ids:
        print(f"Warning: Missing IDs in database: {missing_ids}")

    return results


#print(fetch_all_article_by_ids([28274]))