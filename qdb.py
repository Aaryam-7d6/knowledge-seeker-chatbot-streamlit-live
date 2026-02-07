from qdrant_client import QdrantClient,AsyncQdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from config import QDRANT_HOST,QDRANT_PORT, QDRANT_API,QDRANT_COLLECTION,HASH_FIELD_NAME,EMBEDDING_DIM
from llama_index.core.storage.storage_context import StorageContext
from qdrant_client.models import VectorParams, Distance

# def ensure_collection(client, collection_name, vector_size):
#     if not client.collection_exists(collection_name):
#         client.create_collection(
#             collection_name=collection_name,
#             vectors_config=VectorParams(
#                 size=vector_size,
#                 distance=Distance.COSINE
#             )
#         )

def get_qdrant_client():
    return QdrantClient(
        url= QDRANT_HOST,
        api_key= QDRANT_API,
    )

def create_collection_if_not_exists():
    client = get_qdrant_client()
    collection_name = QDRANT_COLLECTION

    existing_collections = [
        c.name for c in client.get_collections().collections
    ]

    if collection_name in existing_collections:
        print(f"Qdrant collection '{collection_name}' already exists")
        return

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size= EMBEDDING_DIM,
            distance=Distance.COSINE,
        ),
    )

    print(f"Created Qdrant collection: {collection_name}")



# def is_file_hash_present(client: QdrantClient, file_hash: str) -> bool:
#     """
#     Check if file hash already exists in Qdrant collection.
#     """
#     result, _ = client.scroll(
#         collection_name=QDRANT_COLLECTION,
#         scroll_filter={
#             "must": [
#                 {
#                     "key": HASH_FIELD_NAME,
#                     "match": {"value": file_hash}
#                 }
#             ]
#         },
#         limit=1
#     )
#     return len(result) > 0



def get_vector_store():
    client = QdrantClient(url=QDRANT_HOST,port=QDRANT_PORT,api_key=QDRANT_API) #add url = QDRANT_HOST here insted of host=QDRANT_HOST because AsyncQdrantClient uses url parameter instead of host and port.
    aclient = AsyncQdrantClient(url=QDRANT_HOST, port=QDRANT_PORT,api_key=QDRANT_API) #add url = QDRANT_HOST here insted of host=QDRANT_HOST because AsyncQdrantClient uses url parameter instead of host and port.
    #payload = {"file_name": file_name,"file_hash": file_hash,"chunk_id": chunk_id}


    return QdrantVectorStore(client=client,aclient = aclient,collection_name=QDRANT_COLLECTION)