from app.elastic_client import index_document
from app.elastic_client import semantic_search_documents

def main():
    index_document(
        doc_id=1,
        user_id=1,
        source_id=1,
        title="בדיקת אלסטיק",
        content="זה טקסט בדיקה שנשמר בתוך אלסטיק.",
        url="https://example.com",  
    )
    print("Document inserted!")

results = semantic_search_documents(
    question="What is Wikipedia?",
    user_id=1,
    size=3,
)

for r in results:
    print(r["score"], r["title"])


if __name__ == "__main__":
    main()
    print(results)
