
from typing import Optional, List, Dict
from elasticsearch import Elasticsearch

from app.utils.embeddings import embed_text  

ES_INDEX = "documents"


def get_es_client() -> Elasticsearch:
    client = Elasticsearch(
        "https://localhost:9200",
        basic_auth=("elastic", "WI7-9MSUqJ_sbuXrAT=2"),  
        verify_certs=False,
        ssl_show_warn=False,
    )
    return client


def index_document(
    doc_id: int,
    user_id: int,
    source_id: int,
    title: str,
    content: str,
    url: Optional[str] = None,
) -> None:
    client = get_es_client()

    full_text = (title or "") + "\n" + (content or "")
    embedding = embed_text(full_text)

    body = {
        "doc_id": doc_id,
        "user_id": user_id,
        "source_id": source_id,
        "title": title,
        "content": content,
        "url": url,
        "embedding": embedding,
    }

    client.index(index=ES_INDEX, id=doc_id, document=body)



def search_documents(query: str, user_id: int, size: int = 5) -> List[Dict]:
    client = get_es_client()

    resp = client.search(
        index=ES_INDEX,
        body={
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["title^2", "content"],
                            }
                        }
                    ],
                    "filter": [
                        {"term": {"user_id": user_id}}
                    ],
                }
            },
            "size": size,
        },
    )

    hits = resp.get("hits", {}).get("hits", [])
    return [
        {
            "id": hit["_id"],
            "score": hit["_score"],
            **hit["_source"],
        }
        for hit in hits
    ]
def semantic_search_documents(
    question: str,
    user_id: int,
    source_id: Optional[int] = None,   
    size: int = 5,
) -> List[Dict]:
    client = get_es_client()
    query_vector = embed_text(question)

  
    filter_clauses: List[Dict] = [
        {"term": {"user_id": user_id}}
    ]
    if source_id is not None:
        
        filter_clauses.append({"term": {"source_id": source_id}})

    body = {
        "size": size,
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                        "filter": filter_clauses
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {
                        "query_vector": query_vector,
                    },
                },
            }
        },
    }

    resp = client.search(index=ES_INDEX, body=body)
    hits = resp.get("hits", {}).get("hits", [])
    return [
        {
            "id": hit["_id"],
            "score": hit["_score"],
            **hit["_source"],
        }
        for hit in hits
    ]