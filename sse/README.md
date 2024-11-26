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
1. data indexing into pinecone occurs in index_data.py. I added a drop_and_recreate_index() for testing reasons. I use  parameters MAX_TIME_PER_ARTICLE, PERCENTAGE_OF_DATABASE_TO_INDEX. MAX_TIME_PER_ARTICLE hopefully temporary, used because indexing some specific articles was taking much longer than the others.
2. embeddings are dynamically generated using opeanai API
3. metadata is dynamically generated and indexed along with the embedding, to be used both for filters, and as diplay datawhen search results are sent to the frontend.

SEARCH:
1. User insert search query, and select age group / or use default
2. Search query is sent to http://127.0.0.1:8000/api/search
3. query content is validated, and response is created: response = fetch_search_results_with_metadata(), passing also filters like type and age_group
4. embedding for query is created: query_embedding = generate_embedding(), using opeanai API
5. results are fetched using query_embeddings(), with approapriate filtes 
6. filtered results are returned, using pinecone's entries metadata to display back to the frontend