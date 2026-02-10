from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core import StorageContext, load_index_from_storage,Settings
from llama_index.core.node_parser import SentenceSplitter
from embed import get_embedding_model
from qdb import get_vector_store
from llm import get_llm
from config import TOP_K, SEARCH_MODE, STORAGE_DIR, DATA_DIR, QDRANT_COLLECTION, TEMPERATURE 
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import QueryFusionRetriever
#from llama_index.core.response_synthesizers import ResponseSynthesizer
from rag_eng import load_index_from_storage, get_rag_engine,load_index
import config
import os
from llama_index.core.retrievers import QueryFusionRetriever
import streamlit as st
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.core.query_engine import RetrieverQueryEngine

#from rag_eng import load_index


Settings.llm = get_llm()
Settings.embed_model = get_embedding_model()
Settings.node_parser = SentenceSplitter(chunk_size=512,chunk_overlap=51)

#if "memory" not in st.session_state:
    #st.session_state.memory = ChatMemoryBuffer.from_defaults(token_limit=2006)
    
#from llama_index.core.memory import ChatMemoryBuffer

#memory = ChatMemoryBuffer.from_defaults(token_limit=1500)



# def load_index():
#     storage_context = StorageContext.from_defaults(persist_dir="./storage")
#     return load_index_from_storage(storage_context)

# def get_query_engine(search_mode=SEARCH_MODE):
#     #embed_model = get_embedding_model()
#     #llm = get_llm()
#     #vector_store = get_vector_store()
#     #best for semintic search.
#     #index = VectorStoreIndex.from_vector_store(vector_store=vector_store,embed_model=embed_model)
#     #index = load_index()
#     embed_model = Settings.embed_model
#     llm = Settings.llm
#     vector_store = get_vector_store()
#     storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
#     index = load_index()
    
#     if index.docstore is None or len(index.docstore.docs) == 0:
#         raise RuntimeError("No documents available for keyword or hybrid search.")


#     # --- Vector (Semantic) Search ---
#     vector_retriever = VectorIndexRetriever(index=index,similarity_top_k=TOP_K)

#     # --- Keyword Search ---
#     bm25_retriever = BM25Retriever.from_defaults(index=index,similarity_top_k=TOP_K)

#     # --- Choose Mode ---
#     if search_mode == "vector":
#         retriever = vector_retriever

#     elif search_mode == "keyword":
#         retriever = bm25_retriever

#     elif search_mode == "hybrid":
#         retriever = [vector_retriever, bm25_retriever]

#     else:
#         raise ValueError("Invalid search mode")

#     response_synthesizer = ResponseSynthesizer.from_args(llm=llm,response_mode="compact")

#     query_engine = RetrieverQueryEngine(retriever=retriever,response_synthesizer=response_synthesizer)

#     #return RetrieverQueryEngine(retriever=retriever,response_synthesizer=response_synthesizer)
#     return query_engine
# def load_index():
#     qdrant_store = get_vector_store()

#     storage_context = StorageContext.from_defaults(
#         persist_dir="./storage",
#         vector_stores={
#             "default": qdrant_store
#         }
#     )

#     index = load_index_from_storage(storage_context)
#     return index

#-- form documentation --
from llama_index.core import SimpleDirectoryReader

#docs = SimpleDirectoryReader(DATA_DIR).load_data()

from llama_index.core.storage.docstore import SimpleDocumentStore

#docstore = SimpleDocumentStore()
#docstore.add_documents(docs)
#-- --

# for more information visit : https://developers.llamaindex.ai/python/examples/retrievers/bm25_retriever/ for BM25Retriever

def get_query_engine(search_mode=SEARCH_MODE):
    
        
    index = load_index()
    if index is None:
        return None
    
    docs = SimpleDirectoryReader(DATA_DIR).load_data()
    docstore = SimpleDocumentStore()
    docstore.add_documents(docs)
    
    storage_context = StorageContext.from_defaults(persist_dir="./storage", docstore=docstore)
    # index = load_index_from_storage(storage_context)
    
    # if index.docstore is None or len(index.docstore.docs) == 0:
    #     raise RuntimeError("No documents available. Please index first.")
    
    if not os.path.exists(os.path.join(STORAGE_DIR, "docstore.json")):
        raise RuntimeError("No index found. Please click 'Index Documents' first.")


    vector_retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=TOP_K
    )

    bm25_retriever = BM25Retriever.from_defaults(
        #index=index,
        #index = docs,
        docstore= docstore,
        similarity_top_k=TOP_K
    )

    if search_mode == "vector":
        retriever = vector_retriever

    elif search_mode == "keyword":
        retriever = bm25_retriever

    elif search_mode == "hybrid":
        # retriever = QueryFusionRetriever(
        #     retrievers=[vector_retriever, bm25_retriever],
        #     #retrievers= vector_retriever & bm25_retriever,
        #     similarity_top_k=TOP_K,
        #     num_queries=1
        # )
        # from docs > https://developers.llamaindex.ai/python/examples/retrievers/simple_fusion/
        fusion = QueryFusionRetriever(
            retrievers=[vector_retriever, bm25_retriever],
            similarity_top_k=TOP_K,
            num_queries=1,
            use_async=True
            #memory=st.session_state.memory
        )
        response_synthesizer = get_response_synthesizer(
            llm=Settings.llm,
            response_mode="compact"
        ) #, num_queries=1 -- u can add this param if needed
        # return RetrieverQueryEngine(
            #     retriever=retriever,
            #     response_synthesizer=response_synthesizer
            #     memory=st.session_state.memory
        # )
        

        be1 = RetrieverQueryEngine.from_args(fusion,response_synthesizer=response_synthesizer) #memory=memory,llm=Settings.llm,response_mode="compact") #llm and response_model i copy here from the base_engine below
        #just user seer logic for solving the issue name "'RetrieverQueryEngine' object has no attribute 'chat'", do some copy past from below code.
        return ContextChatEngine.from_defaults(
        query_engine=be1,
        retriever=fusion,
        #memory=st.session_state.memory,
        #memory=memory,
        chat_mode="context",
        #query = query_engine.query,
        #query = query_engine
        query = be1.query
        #query = base_engine
    )
        #return RetrieverQueryEngine.from_args(fusion)


    else:
        raise ValueError("Invalid search mode")

    # response_synthesizer = get_response_synthesizer(
    #     llm=Settings.llm,
    #     response_mode="compact"
    # ) #, num_queries=1 -- u can add this param if needed

    # return RetrieverQueryEngine(
    #     retriever=retriever,
    #     response_synthesizer=response_synthesizer
    #     memory=st.session_state.memory
    # )

    # Build base query engine
    base_engine = RetrieverQueryEngine.from_args(
    #RetrieverQueryEngine.from_args(
        retriever=retriever,
        llm=Settings.llm,
        response_mode="compact"
        #use_async=False
    )

    # Wrap it with chat engine (THIS enables memory + follow-ups)
    # use https://developers.llamaindex.ai/python/examples/chat_engine/chat_engine_context/ for more information
    #chat_engine = ContextChatEngine.from_defaults(
    return ContextChatEngine.from_defaults(
        query_engine=base_engine,
        retriever=retriever,
        #memory=st.session_state.memory,
        #memory=memory,
        chat_mode="context",
        #query = query_engine.query,
        #query = query_engine
        query = base_engine.query
        #query = base_engine
    )

    #return chat_engine