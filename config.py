from dotenv import load_dotenv
import os

load_dotenv()


#COLLECTION_NAME = "knowledge_docs" # name 4 minilm-l6 mode
#COLLECTION_NAME = "knowledge_docs_4_search" # name 4 multi-qa-mpnet-base-dot-v1 model
#COLLECTION_NAME = "knowledge_docs_bett_emb" # name 4 all-mpnet-base-v2 model
#COLLECTION_NAME = "knowledge_docs_test_with_metadata_andlogs" # name 4 all-mpnet-base-v2 model with metadata and logs
#COLLECTION_NAME = "knowledge_docs_test_with_ip_path0" # name 4 all-mpnet-base-v2 model with metadata and logs + user ip path #-> #------ -ve failed to do that-----
#COLLECTION_NAME = "knowledge_docs_test_with_chat" # name 4 all-mpnet-base-v2 model with metadata and logs + user ip path #-> #----- note working because collection is not existing -----
QDRANT_COLLECTION = "knowledge_seeker_docs" # final name for collection with all features and best embaddings.

#quedrent connection config

#QDRANT_HOST = "localhost"
QDRANT_API=os.environ.get("QDRANT_API_KEY")
QDRANT_HOST=os.environ.get("QDRANT_URL")
QDRANT_PORT = 6333

#EMBED_MODEL_NAME = "all-MiniLM-L6-v2" # good 4 fast and base line embaddings.
#EMBED_MODEL_NAME = "sentence-transformers/multi-qa-mpnet-base-dot-v1" # better for search use case.
EMBED_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2" # better embaddings but slower.
EMBEDDING_DIM = 768 #dimansion for all-mpnet-base-v2 model


# Retrieval config
TOP_K = 6

# Temperature for LLM responses:
TEMPERATURE = 0.5

#seaech mode default:
SEARCH_MODE = "hybrid"  # Options: "vector", "keyword", "hybrid"

# Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
#GEMINI_MODEL = "models/gemini-1.5-flash" #not working...
#GEMINI_MODEL = "gemini-1.5-flash" #not working..
# GEMINI_MODEL_D = "models/gemini-2.5-flash" # working...
# GEMINI_MODEL_1 = "models/gemini-2.5-flash-lite" # if limit exceed then try this lite version.
# GEMINI_MODEL = GEMINI_MODEL_D # default model

#data dirs:
#PERSIST_DIR = "./storage"
DATA_DIR = "./data"
STORAGE_DIR = PERSIST_DIR = "./storage"

#hasing:
# Hashing
HASH_ALGO = "sha256"
#HASH_FIELD = "file_hash"
HASH_FIELD_NAME = "file_hash"
HASH_REGISTRY_PATH = "storage/file_hashes.json"

