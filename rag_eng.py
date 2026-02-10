from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.response_synthesizers import get_response_synthesizer
from embed import get_embedding_model
from qdb import get_vector_store
from llm import get_llm
from config import TOP_K,TEMPERATURE,PERSIST_DIR
#import google.generativeai as genai
#import llm_model as llmm
import config
Settings.llm = get_llm()
Settings.embed_model = get_embedding_model()
Settings.node_parser = SentenceSplitter(chunk_size=512,chunk_overlap=51)


# def get_rag_engine():
#     #embed_model = get_embedding_model()
#     #llm = get_llm()
    
#     embed_model = Settings.embed_model
#     llm = Settings.llm
#     vector_store = get_vector_store()
#     storage_context = StorageContext.from_defaults(vector_store=vector_store) #add it here

#     index = VectorStoreIndex.from_vector_store(vector_store=vector_store,embed_model=embed_model,storage_context=storage_context) #add storage_context here

#     retriever = VectorIndexRetriever(index=index,similarity_top_k=TOP_K)

#     response_synthesizer = get_response_synthesizer(llm=llm,response_mode="compact")

#     query_engine = RetrieverQueryEngine(retriever=retriever,response_synthesizer=response_synthesizer)

#     return query_engine



# index = VectorStoreIndex.from_documents(
#     documents,
#     storage_context=storage_context,
#     embed_model=get_embedding_model()
# )

#index.storage_context.persist(persist_dir="./storage")

from llama_index.core import StorageContext, load_index_from_storage
from qdb import get_vector_store
import os

def index_exists():
    return os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR)

def load_index():
    if not index_exists():
        return None
    
    qdrant_store = get_vector_store()

    storage_context = StorageContext.from_defaults(
        persist_dir="./storage",
        vector_stores={
            "default": qdrant_store
        }
    )
    

    index = load_index_from_storage(storage_context)
    return index


def get_rag_engine():
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    #index = load_index_from_storage(storage_context)
    # if hash_exists_in_db(file_hash):
    #     #st.info("Document already indexed, skipping.")

    index = load_index()

    retriever = VectorIndexRetriever(index=index, similarity_top_k=TOP_K)

    response_synthesizer = get_response_synthesizer(
        llm=Settings.llm,
        response_mode="compact"
    )

    return RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer
    )

