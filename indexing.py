from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    Settings
)
from embed import get_embedding_model
from llama_index.core.node_parser import SentenceSplitter
from qdb import get_vector_store
from logger import logger
from rag_eng import load_index_from_storage, get_rag_engine
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from config import DATA_DIR, STORAGE_DIR, QDRANT_COLLECTION
import os
import config
from qdb import get_vector_store
from utils.file_hash import compute_file_hash
from qdb import create_collection_if_not_exists


# Chunking Configuration
Settings.node_parser = SentenceSplitter(chunk_size=512,chunk_overlap=51)

# def build_index(data_dir: str):
#     logger.info(f"Loading documents from {data_dir}")
    
#     documents = SimpleDirectoryReader(data_dir,recursive=True).load_data()
    
#      # add metadta
#     for doc in documents:
#         doc.metadata["source"] = os.path.basename(doc.metadata.get("file_path", "unknown"))
#         doc.metadata["file_path"] = doc.metadata.get("file_path", "unknown")
#     logger.info(f"Loaded {len(documents)} documents.")
    
#     vector_store = get_vector_store()


#     #embed_model = get_embedding_model() #-- useful for only similarity and simentic search.
#     #logger.info(f"Using embedding model: {embed_model}")
    
#     #vector_store = get_vector_store()

#     storage_context = StorageContext.from_defaults(vector_store=vector_store)

#     logger.info("Building vector index")
#     index = VectorStoreIndex.from_documents(documents=documents,storage_context=storage_context,embed_model=get_embedding_model())
#     #logger.info(f"--- Index built with {len(documents)} documents. && {vector_store.num_entities} vectors. && {vector_store.num_collections} collections. && embedding model: {get_embedding_model()}. ---")
#     logger.info(f"Index built successfully with {len(documents)} documents "f"using embedding model: {config.EMBED_MODEL_NAME}")

#     # Persist docstore + index
#     index.storage_context.persist(persist_dir="./storage")

#     return index


# def file_hash(file_bytes):
#     return hashlib.sha256(file_bytes).hexdigest()


# def compute_file_hash(file_path: str) -> str:
#     hasher = hashlib.sha256()
#     with open(file_path, "rb") as f:
#         while chunk := f.read(8192):
#             hasher.update(chunk)
#     return hasher.hexdigest()


def build_index(data_dir):
    
    create_collection_if_not_exists()
    os.makedirs(data_dir, exist_ok=True) #create data_dir if not exists
    
    if not os.listdir(data_dir):
        raise RuntimeError("No documents found. Please upload documents before indexing.")
    
    documents = SimpleDirectoryReader(data_dir, recursive=True).load_data()

    if not documents:
        raise RuntimeError("No documents found to index.")
    
    # for document in documents:
    #     #document.metadata["file_name"] = os.path.basename(document.metadata.get("file_path", "unknown"))
    #     #document.metadata["file_path"] = document.metadata.get("file_path", "unknown")
    #     # Add page label if available (assuming it's part of the metadata)
    #     #document.metadata["page_label"] = document.metadata.get("page_label", "N/A")
    #     metadata = {
    #         "file_name": [document.name],
    #         #"file_hash": file_hash(file.getbuffer())
    #         "file_hash": [file_hash(document.get_content().encode('utf-8'))]
    #     }
    #     document.metadata.update(metadata)
        
    #client = QdrantClient(path=STORAGE_DIR)
    #client = QdrantClient(host=QDRANT_HOST,port=QDRANT_PORT)

    #vector_store = QdrantVectorStore(client=client,collection_name=COLLECTION_NAME)
    vector_store = get_vector_store()

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )

    index.storage_context.persist(persist_dir=STORAGE_DIR)
    #return index
    
# client = QdrantClient(
#     url="YOUR_QDRANT_URL",
#     api_key="YOUR_QDRANT_API_KEY"
# )

#def build_index(file_path: str, file_name: str, file_bytes: bytes):
# def build_index(data_dir: str):
#     file_name: str = os.path.basename(data_dir)
#     file_bytes: bytes = open(data_dir, "rb").read()
    
#     documents = SimpleDirectoryReader(data_dir).load_data()

#     file_hash = compute_file_hash(file_bytes)

#     if is_file_hash_present(client, file_hash):
#         print(f"[SKIPPED] {file_name} already indexed.")
#         return
    
#     documents = SimpleDirectoryReader(data_dir).load_data()

#     if not documents:
#         raise RuntimeError("No documents found to index.")
    
#     vector_store = get_vector_store()

#     storage_context = StorageContext.from_defaults(vector_store=vector_store)

#     index = VectorStoreIndex.from_documents(
#         documents,
#         storage_context=storage_context,
#     )

#     index.storage_context.persist(persist_dir=STORAGE_DIR)

#     # --- proceed with chunking + embedding ---
#     # documents = load_and_chunk(file_path)

#     # for i, doc in enumerate(documents):
#     #     embedding = embed_text(doc.text)

#     #     client.upsert(
#     #         collection_name=QDRANT_COLLECTION,
#     #         points=[
#     #             {
#     #                 "id": f"{file_hash}_{i}",
#     #                 "vector": embedding,
#     #                 "payload": {
#     #                     "file_name": file_name,
#     #                     "file_hash": file_hash,
#     #                     "chunk_id": i,
#     #                     "text": doc.text
#     #                 }
#     #             }
#     #         ]
#     #     )

#     # print(f"[INDEXED] {file_name}")



