import psycopg2
from psycopg2.extras import RealDictCursor
from src.config.base_config import POSTGRES_DATABASE_NAME, POSTGRES_DATABASE_USER, POSTGRES_DATABASE_PASSWORD, POSTGRES_DATABASE_HOST, POSTGRES_DATABASE_PORT

def get_postgres_connection():
    """
    Create and return a PostgreSQL database connection.
    """
    return psycopg2.connect(
        dbname=POSTGRES_DATABASE_NAME,
        user=POSTGRES_DATABASE_USER,
        password=POSTGRES_DATABASE_PASSWORD,
        host=POSTGRES_DATABASE_HOST,
        port=POSTGRES_DATABASE_PORT
    )
