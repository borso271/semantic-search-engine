import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.embeddings.generate_query_embedding import generate_query_embedding
from src.pinecone.query_embeddings import query_embeddings
from src.postgres.query_operations import fetch_articles_by_ids
from src.pinecone.get_index import get_index  # Import the index setup function
from src.config.pinecone_config import DEFAULT_TOP_K, DEFAULT_MIN_RELEVANCY

# Initialize the Pinecone index globally
index = get_index()

logger = logging.getLogger(__name__)
router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    age_group: Optional[str] = None  # Filter for age group (e.g., "6-8")
    content_type: Optional[str] = None  # Filter for content type (e.g., "article" or "video")

def process_query(query: str):
    query = query.strip()
    if not query or len(query) < 2:
        raise ValueError("Query must be at least 2 characters long.")
    return query

def fetch_search_results_with_metadata(query: str, index, age_group: Optional[str], content_type: Optional[str]):
    """
    Fetch search results directly from Pinecone metadata.
    """
    # Generate query embedding
    query_embedding = generate_query_embedding(query)

    # Construct Pinecone filters
    pinecone_filter = {}
    
    if age_group:
      
        pinecone_filter["ageGroup"] = age_group
    if content_type:
        pinecone_filter["type"] = content_type

    # Query Pinecone
    results = query_embeddings(
        index=index,
        query_vector=query_embedding,
        top_k=DEFAULT_TOP_K,
        min_relevancy=DEFAULT_MIN_RELEVANCY,
        filters=pinecone_filter
    )
 
    # Construct the response directly from Pinecone metadata

    response = [
        {
            "id": match["id"],
            "title": match["metadata"].get("topic", "Unknown Title"),
            "description": match["metadata"].get("description", "No Description Available"),
            "score": match["score"],
            "type": match["metadata"].get("type", "Unknown"),
            "age_group": match["metadata"].get("ageGroup", "Unknown"),
            "image_url": match["metadata"].get("imageUrl", "")
        }
        for match in results
    ]
  
    # Sort the response by score in descending order
    return sorted(response, key=lambda x: x["score"], reverse=True)

@router.post("/api/search")
async def search(request: SearchRequest):
    """
    Search endpoint using Pinecone metadata for response construction.
    """
    try:
        # Process query and filters
      
        query = process_query(request.query)
        ageGroup = request.age_group
        contentType = request.content_type

        # Fetch search results with metadata
        response = fetch_search_results_with_metadata(query, index, ageGroup, contentType)

        return {"query": query, "results": response}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        logger.error(f"RuntimeError during search: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during search: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")














"""
OLD VERSION QUERYING THE POSTGRES AFTER PINECONE RETURNS IDS RATHER THAN USING PINECONE STORED METADATA TO CONSTRUCT RESPONSE

class SearchRequest(BaseModel):
    query: str
    age_group: Optional[str] = None  # Filter for age group (e.g., "6-8")
    content_type: Optional[str] = None  # Filter for content type (e.g., "article" or "video")

def process_query(query: str):
    query = query.strip()
    if not query or len(query) < 2:
        raise ValueError("Query must be at least 2 characters long.")
    return query

def fetch_search_results(query: str, index, age_group: Optional[str], content_type: Optional[str]):
    # Generate query embedding
    query_embedding = generate_embedding(query)

    # Query Pinecone with filters
    pinecone_filter = {}
    if age_group:
        pinecone_filter["ageGroup"] = age_group
    if content_type:
        pinecone_filter["type"] = content_type

    results = query_embeddings(
        index, query_embedding, top_k=DEFAULT_TOP_K, min_relevancy=DEFAULT_MIN_RELEVANCY, filters=pinecone_filter
    )

    # Retrieve matching IDs and scores
    ids_and_scores = [(match["id"], match["score"]) for match in results]

    # Fetch data from the database
    fetched_articles = fetch_articles_by_ids([item[0] for item in ids_and_scores])

    return construct_response(fetched_articles, ids_and_scores)

def construct_response(fetched_articles, ids_and_scores):
    return sorted(
        [
            {
                "id": article["id"],
                "title": article["title"],
                "description": article["description"],
                "score": score,
                "type": article.get("type", "unknown"),  # Default to "unknown" if not present
                "age_group": article.get("age_group", "unknown")  # Default to "unknown" if not present
            }
            for article, (_, score) in zip(fetched_articles, ids_and_scores)
        ],
        key=lambda x: x["score"],
        reverse=True
    )

@router.post("/api/search")
async def search(request: SearchRequest):
    try:
        # Process query and filters
        query = process_query(request.query)
        age_group = request.age_group
        content_type = request.content_type

        # Fetch search results with filters
        response = fetch_search_results(query, index, age_group, content_type)

        return {"query": query, "results": response}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        logger.error(f"RuntimeError during search: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during search: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
"""