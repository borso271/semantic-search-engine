### Running Tests
Run all tests with:
```bash
pytest tests/

├── README.md
├── frontend
│   ├── index.html
│   ├── index.js
│   └── style.css
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   └── __init__.cpython-312.pyc
│   ├── api
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── app.cpython-310.pyc
│   │   │   └── app.cpython-312.pyc
│   │   ├── app.py
│   │   └── routes
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-310.pyc
│   │       │   └── search_routes.cpython-310.pyc
│   │       └── search_routes.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── base_config.cpython-310.pyc
│   │   │   ├── base_config.cpython-312.pyc
│   │   │   ├── embeddings_config.cpython-310.pyc
│   │   │   ├── embeddings_config.cpython-312.pyc
│   │   │   ├── pinecone_config.cpython-310.pyc
│   │   │   └── pinecone_config.cpython-312.pyc
│   │   ├── base_config.py
│   │   ├── embeddings_config.py
│   │   ├── pinecone_config.py
│   │   └── postgres_config.py
│   ├── embeddings
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── client.cpython-310.pyc
│   │   │   ├── client.cpython-312.pyc
│   │   │   ├── generate.cpython-310.pyc
│   │   │   └── generate.cpython-312.pyc
│   │   ├── client.py
│   │   └── generate.py
│   ├── pinecone
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── client.cpython-310.pyc
│   │   │   ├── client.cpython-312.pyc
│   │   │   ├── drop_and_recreate_index.cpython-312.pyc
│   │   │   ├── get_index.cpython-310.pyc
│   │   │   ├── query_embeddings.cpython-310.pyc
│   │   │   ├── setup_index.cpython-310.pyc
│   │   │   └── upsert_embeddings.cpython-312.pyc
│   │   ├── client.py
│   │   ├── get_index.py
│   │   ├── index_data.py
│   │   ├── query_embeddings.py
│   │   ├── upsert_embeddings.py
│   │   └── utils
│   │       ├── __pycache__
│   │       │   ├── drop_and_recreate_index.cpython-312.pyc
│   │       │   ├── index_exists.cpython-310.pyc
│   │       │   ├── index_exists.cpython-312.pyc
│   │       │   └── validation.cpython-312.pyc
│   │       ├── drop_and_recreate_index.py
│   │       ├── index_exists.py
│   │       └── validation.py
│   ├── postgres
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── client.cpython-310.pyc
│   │   │   ├── client.cpython-312.pyc
│   │   │   ├── query_operations.cpython-310.pyc
│   │   │   └── query_operations.cpython-312.pyc
│   │   ├── client.py
│   │   └── query_operations.py
│   └── utils
└── tests

INDEXING:
1. Data Indexing: The script `index_data.py` handles the indexing process. For testing purposes, a function `drop_and_recreate_index()` has been included. The indexing process is controlled by parameters such as `MAX_TIME_PER_ARTICLE` and `PERCENTAGE_OF_DATABASE_TO_INDEX`. The `MAX_TIME_PER_ARTICLE` parameter, which is likely temporary, helps manage cases where some articles take significantly longer to index than others.

2. Embeddings: Embeddings are generated dynamically using an external API.

3. Metadata: Metadata is created dynamically alongside the embeddings and is indexed together with them. This metadata serves two purposes: it is used as a filter during searches and is displayed when search results are sent to the frontend.

SEARCH:
1. User Input: The user provides a search query and optionally selects an age group, or the default age group is applied.

2. API Request: The query is sent to the backend search API.

3. Validation and Response Creation: The query content is validated, and a response is prepared using the function `fetch_search_results_with_metadata()`. This step incorporates filters such as type and age group.

4. Query Embedding: An embedding for the query is generated dynamically using the external API.

5. Result Fetching: Results are retrieved using the query embedding and the specified filters.

6. Returning Results: Filtered results, along with metadata from the indexed entries, are sent back to the frontend for display.
