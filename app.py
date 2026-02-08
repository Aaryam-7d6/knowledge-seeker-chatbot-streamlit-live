from llm import get_llm
import streamlit as st
from qdb import get_vector_store
from indexing import build_index
from rag_eng import get_rag_engine
from summary_eng import generate_document_summary
from search import get_query_engine
#from indexing import build_index
#from utils.file_handl import save_uploaded_file
import config
from config import DATA_DIR, STORAGE_DIR,TEMPERATURE, TOP_K, SEARCH_MODE
import os

# def file_hash(file_bytes):
#     return hashlib.sha256(file_bytes).hexdigest()


# def compute_file_hash(file_bytes: bytes) -> str:
#     sha256 = hashlib.sha256()
#     sha256.update(file_bytes)
#     return sha256.hexdigest()
from utils.file_hash import compute_file_hash
from utils.file_registry import load_hashes, save_hashes





#from llama_index.core.memory import ChatMemoryBuffer


# for me information visit: #https://developers.llamaindex.ai/python/examples/agent/memory/chat_memory_buffer/

from llama_index.core.memory import ChatMemoryBuffer

#memory = ChatMemoryBuffer.from_defaults(token_limit=15000)

if "memory" not in st.session_state:
    st.session_state.memory = ChatMemoryBuffer.from_defaults(token_limit = 15000)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="KnowledgeSeeker",layout="wide")

st.title(" KnowledgeSeeker ")
st.caption("A RAG-based conversational AI for knowledge seekers and autodidactic learners.")
st.caption(f"Ask Questions because Questions are Welcomed here :)")


#st.caption("NotebookLM-inspired Document Intelligence System.")


# --- Sidebar ---
st.sidebar.header("User Panel")

with st.sidebar.expander("Upload and indexing", expanded=False):
    
    #st.sidebar.subheader("Upload and Index Documents")
    st.subheader("Upload and Index Documents")
    uploaded_files = st.file_uploader( #remove "sidebar."" after st.
        "Upload PDF, TXT, DOCX, MD files",
        type=["pdf", "txt", "docx", "md"],
        accept_multiple_files=True
        )

    # os.makedirs(DATA_DIR, exist_ok=True)

    # if uploaded_files is not None:
    #     for uploaded_file in uploaded_files:
    #         file_path = os.path.join(DATA_DIR, uploaded_file.name)
    #         with open(file_path, "wb") as f:
    #             f.write(uploaded_file.getbuffer())

    #         st.success(f"Uploaded {uploaded_files.name}")
    
    if uploaded_files:
        
        existing_hashes = load_hashes()
        new_hashes = set(existing_hashes)

        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.getbuffer().tobytes()
            file_hash = compute_file_hash(file_bytes)

            # DUPLICATE CHECK
            if file_hash in existing_hashes:
                st.warning(f"!!! '{uploaded_file.name}' already uploaded. Skipping...")
                continue

            # SAVE FILE
            file_path = os.path.join(config.DATA_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(file_bytes)

            # REGISTER HASH
            new_hashes.add(file_hash)

            st.success(f"✅ Uploaded & registered: {uploaded_file.name}")

        save_hashes(new_hashes)
    # if uploaded_files:
    #     for uploaded_file in uploaded_files:
    #         file_path = os.path.join(config.DATA_DIR, uploaded_file.name)
            
    #         with open(file_path, "wb") as f:
    #             f.write(uploaded_file.getbuffer())
                
    #         #st.success(f"Uploaded {uploaded_file.name}")
    #         st.success(f"Uploaded {uploaded_file.name}")
            # metadata = {
            #     "file_name": uploaded_file.name,
            #     "file_hash": file_hash(uploaded_file.getbuffer())
            # }
            # Here you can also save the metadata to a database if needed
            # file_bytes = uploaded_file.getvalue()
            # file_hash = compute_file_hash(file_bytes)
            # if is_file_already_indexed(file_hash):
            #     st.warning(f"{uploaded_file.name} already uploaded.")
            # else:
            #     save_file_and_index(...)


    

    # if st.sidebar.button("Index Documents"):
    #     if uploaded_files:
    #         for file in uploaded_files:
    #             save_uploaded_file(file)
    #         with st.spinner("Indexing documents..."):
    #             #build_index(data_dir="data/uploads")            
    #             #build_index(data_dir="./storage")  # to index any previously stored docs
    #             st.sidebar.success("Documents indexed successfully!")
    if not uploaded_files:
        #st.sidebar.info("Please upload documents to index.", icon="ℹ️")
        st.subheader("Upload and Index Documents")
    
    # if hash_exists_in_db(file_hash):
    #     st.info("Document already indexed, skipping.")
    # else:
    #     index_document()

    else:
        if st.button("Index Documents"): #remove "sidebar."" after st.
            # if hash_exists_in_db(file_hash):
            #     st.info("Document already indexed, skipping.")
            #else:
                
            with st.spinner("Indexing documents..."):
                build_index(config.DATA_DIR)
            st.success("Indexing completed")
    
    if not os.path.exists(os.path.join(config.STORAGE_DIR, "docstore.json")):
        st.warning("Please upload and index documents first.")
        #st.stop()
        #search_mode = st.selectbox()
        search_mode = "keyword"  # Fallback to keyword search if no index exists

# --- Sidebar Summary ---

#st.sidebar.markdown("---")
with st.sidebar.expander("Summary aka TL;DR", expanded=False):
    st.subheader("Document Summary aka TL;DR") #remove "sidebar."" after st.
    if st.button("Generate Summary"): #remove "sidebar."" after st.
        with st.spinner("Summarizing documents..."):
            summary = generate_document_summary()
            st.sidebar.write(summary) 

#st.sidebar.markdown("---")

# --- Settings Panel ---
with st.sidebar.expander("Settings", expanded=False):
    
    st.header("Settings")
    
    # theme = st.selectbox(
    # "Theme",
    # ["System Default", "Light", "Dark"]
    # )
    # if theme == "System Default":
    #     st.markdown(
    #         """
    #         <style>
    #         :root {
    #             color-scheme: normal;
    #         }
    #         </style>
    #         """,
    #         unsafe_allow_html=True
    #     )
    
    # elif theme == "Light":
    #     st.markdown(
    #         """
    #         <style>
    #         :root {
    #             color-scheme: light;
    #         }
    #         </style>
    #         """,
    #         unsafe_allow_html=True
    #     )
    # else:  # Dark theme
    #     st.markdown(
    #         """
    #         <style>
    #         :root {
    #             color-scheme: dark;
    #         }
    #         </style>
    #         """,
    #         unsafe_allow_html=True
    #     )
        
    # st.session_state.theme = theme
    
    #with st.sidebar:
    st.subheader("LLM Parameters")
    #temperature = st.session_state.get("creativity", 0.5)
    #top_k = st.session_state.get("top_k", 6)

    #temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    st.slider("Adjust Response Creativity aka the Temperature", 0.0,2.0, 0.5, key="creativity")
    st.slider("Adjust the Top-K",5,10,6,key="top_k")
    if creativity := st.session_state.get("creativity"):
        #from config import TEMPERATURE
        TEMPERATURE = creativity
    if top_k := st.session_state.get("top_k"):
        #from config import TOP_K
        TOP_K = top_k
    
    # temperature = st.session_state.get("creativity", 0.5)
    # top_k = st.session_state.get("top_k", 6)

        
    #search_mode = st.selectbox("Search Mode",["hybrid", "vector", "keyword"],index=0)
    search_options = ["hybrid", "vector", "keyword"]
    default_index = search_options.index(config.SEARCH_MODE) if config.SEARCH_MODE in search_options else 0
    search_mode = st.selectbox("Search Mode",search_options,index=default_index)
    
    # assistants = ["Gemini 2.5 Flash","Gemini 2.5 Flash Lite"]
    # default_moldel_index = assistants.index(GEMINI_MODEL_D) # Default to the first model 
    # LLM = st.selectbox("LLM Model",assistants,index=default_moldel_index) 
    # if LLM == default_moldel_index: 
    #     from config import GEMINI_MODEL_D 
    #     st.session_state.llm_model = GEMINI_MODEL_D 
    #     GEMINI_MODEL = GEMINI_MODEL_D 
    # else: 
    #     from config import GEMINI_MODEL_1 
    #     st.session_state.llm_model = GEMINI_MODEL_1 
    #     GEMINI_MODEL = GEMINI_MODEL_1
    assistants = [
        "Gemini 2.5 Flash",
        "Gemini 2.5 Flash Lite"
    ]

    default_model_index = 0

    selected_llm = st.selectbox(
        "LLM Model",
        assistants,
        index=default_model_index
    )

    # Map UI choice → actual Gemini model
    if selected_llm == "Gemini 2.5 Flash":
        st.session_state.llm_model = "models/gemini-2.5-flash"
    else:
        st.session_state.llm_model = "models/gemini-2.5-flash-lite"


    # Map UI choice → actual Gemini model
    if selected_llm == "Gemini 2.5 Flash":
        st.session_state.llm_model = "models/gemini-2.5-flash"
    else:
        st.session_state.llm_model = "models/gemini-2.5-flash-lite"
             
    # Check if index exists; if not, restrict to keyword search    
    
    
    st.session_state.llm_config = {
        #"temperature": temperature,
         "top_p": TEMPERATURE,
         "top_k": TOP_K,
        "search_mode": search_mode,
        "llm": selected_llm
    }

#st.sidebar.markdown("---")

# --- Appearance Panel ---
with st.sidebar.expander("Appearance"):
    st.info("Theme follows system or browser settings. Restart app to apply changes.")

# --- clear button ---
st.sidebar.markdown("---")

if st.sidebar.button("Clear Chat"):
    # Clear UI chat history
    st.session_state.chat_history = []

    # Clear LLM memory (important)
    if "memory" in st.session_state:
        st.session_state.memory.reset()

    # Optional: reset input box
    st.session_state.pop("chat_input", None)

    st.sidebar.success("Chat cleared successfully.")

# --- sliderbar out ---

# --- Main Chat Area ---
#st.subheader(f"Ask Questions because Questions are Welcomed here :)")
st.info("We use Gemini 2.5 Flash LLM model by default. Adjust settings in the sidebar as needed.", icon="💡")
st.info("For best results, upload and index relevant documents first.", icon="ℹ️")
#st.info("In case you face Limit Exceeded error, try reducing the Top-K value or switch to Gemini 2.5 Flash Lite model in LLM Parameters.", icon="⚠️")
st.info(
    "📚 Uploaded & indexed documents are stored persistently. "
    "You can ask questions anytime without re-uploading."
)



# --- Chat History Display ---

# for msg in st.session_state.chat_history:
#      with st.chat_message(msg["role"]):
#         #st.markdown("### Answer")
#          #st.write("#### Sources:")
#          st.markdown(msg["content"])
#          #st.write("### Answer")
#          #st.markdown("### Sources")
#          if msg["role"] == "assistant":
#              st.write("#### Sources:")
#              for node in msg.get("source_nodes", []):
#                  #st.write("#### Sources:")
#                  st.markdown(
#                      f"- **{node.metadata.get('file_name', 'unknown')}** "
#                      f"(score: `{node.score:.3f}`)"
#                  )


# --- Chat Input ---


#query = st.text_input("Ask a question based on uploaded documents:")
#query = st.chat_input("Ask a question based on uploaded documents",placeholder="Type your question here and press Enter...",key="chat_input")
query = st.chat_input("Ask a question based on uploaded documents",key="chat_input")
#query = st.text_input("Ask a question based on uploaded documents",placeholder="Type your question here and press Enter...",key="chat_input")
#query = st.text_input("Ask a question based on uploaded documents",key="chat_input")

if query:
    
    st.session_state.chat_history.append({
        "role": "user",
        "content": query
    })
    
    #with st.chat_message("user"):
        #st.write(query)
        #st.markdown(query)

    #response = query_engine.query(user_query)

# i use "Using Standalone" here, for me information visit: #https://developers.llamaindex.ai/python/examples/agent/memory/chat_memory_buffer/

#query_engine = get_query_engine(search_mode)

#if query:
    #query_engine = get_rag_engine()
    query_engine = get_query_engine(search_mode)
    

    with st.spinner("Thinking..."):
        #response = query_engine.query(query)
        #
        # response = query_engine.retrieve(query)
        #st.write(query_engine)
        #response = query_engine.retrieve(query)
        #response = query_engine.query(query)
        #response = query_engine.chat(query)
        
        try:
            response = query_engine.chat(query)
            #answer = response.response
            # append assistant response to chat history
            st.session_state.chat_history.append({
            "role": "assistant",
            "content": response.response,
            "source_nodes": response.source_nodes
            })
            #st.write(response.response)
            #response = llm.complete(prompt)
        except Exception as e:
            if "quota" in str(e).lower():
                st.warning("Quota exceeded. Switching to Lite model.")
                st.session_state.llm_model = "models/gemini-2.5-flash-lite"
                #llm = get_llm()
                response = query_engine.chat(query)
                #answer = response.response
                #response = llm.complete(prompt)
                st.session_state.chat_history.append({
                    "role": "assistant",
                "content": response.response,
                "source_nodes": response.source_nodes
                })
            else:
                #raise e
                st.error(f"Error: {e}")
                st.warning("Please try again later.")
                st.stop()
                
        with st.expander("Response Metrics"):
            st.write("Chunks used:", len(response.source_nodes))
            st.write("Top similarity score:", response.source_nodes[0].score)

                
                
        #st.markdown(answer)
        # if "quota exceeded" or "Limit exceeded" or "403"  in response.response.lower():
        #     st.warning("Quota exceeded. Switching to Lite model.")
        #     st.session_state.llm_model = "models/gemini-2.5-flash-lite"
        #     llm = get_llm()
        #     response = query_engine.chat(query)
        #     #response = llm.complete(prompt)
        # else:
        #     st.warning("Try Again Later... and report the issue")

        
        #with st.chat_message("assistant"):
            #st.write(response.response)
            #st.markdown("### Answer")
            #st.markdown(response.response)
    #st.write(query_engine)

    #st.markdown("### Sources")
    # for node in response.source_nodes:
    #     st.markdown(
    #         f"- **{node.metadata.get('file_name', 'unknown')}** "
    #         f"(score: `{node.score:.3f}`)"
    #     )
    # Append assistant response to chat history 
    # st.session_state.chat_history.append({
    #     "role": "assistant",
    #     "content": response.response,
    #     "source_nodes": response.source_nodes
    #     })
        
    
# --- Chat History Display ---

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        #st.markdown("### Answer")
        #st.write("#### Sources:")
        st.markdown(msg["content"])
        #st.write("### Answer")
        #st.markdown("### Sources")
        if msg["role"] == "assistant":
            st.write("#### Sources:")
            for node in msg.get("source_nodes", []):
                #st.write("#### Sources:")
                #page = node.metadata.get("page_label", "N/A")
                st.markdown(
                    #f"- **{node.metadata.get('file_name', 'unknown')}** "
                    #st.markdown(f"**{node.metadata.get('file_name')}**")
                    f" - File name: **{node.metadata.get('file_name', 'unknown')}** & Page No: **{node.metadata.get('page_label', 'N/A')}** "                    
                    f"(score: `{node.score:.3f}`)"
                )

# --- auto scroll down ----
st.markdown(
    """
    <script>
    window.scrollTo(0, document.body.scrollHeight);
    </script>
    """,
    unsafe_allow_html=True
)


# from llama_index.core.llms import ChatMessage

# chat_history = [
#     ChatMessage(role="user", content=query),
#     ChatMessage(role="assistant", content=response.response),
# ]

# # put a list of messages
# memory.put_messages(chat_history)

# # put one message at a time
# # memory.put_message(chat_history[0])

# # Get the last X messages that fit into a token limit
# history = memory.get()

# # Get all messages
# all_history = memory.get_all()

# ## clear the memory
# #memory.reset()

# st.markdown("---")
# st.markdown("### Chat History")
# # for msg in all_history:
# #     st.markdown(f"**{msg.role.capitalize()}**: {msg.content}")
# st.write(history)

# st.write("#### Full Chat History:")
# st.write(all_history)


# If want that LLM memory track dialoge:

# from llama_index.core.llms import ChatMessage

# st.session_state.memory.put_messages([
#     ChatMessage(role="user", content=query),
#     ChatMessage(role="assistant", content=response.response)
# ])

# --- Footer ---

#st.markdown("---")
# st.markdown(
#     '<div style="text-align: center; color: #6b7280; font-size: 0.85rem; padding: 1rem 0;">'
#     'Powered by Python, Streamlit, LlamaIndex & QdrantDB • Built for knowledge seekers and autodidactics • Inspired by NotebookLM • Document Intelligence System'
#     '</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     """
#     <hr style="margin-top: 2rem; margin-bottom: 1rem;">

#     <div style="
#         text-align: center;
#         font-size: 0.9rem;
#         color: #6b7280;
#         padding-bottom: 1rem;
#     ">
#         <div style="margin-bottom: 0.5rem;">
#             Created by <strong>Aarya R. Thakar</strong> aka <strong>आर्यम्</strong>
#         </div>

#         <div style="display: flex; justify-content: center; gap: 16px; align-items: center;">
#             <a href="https://www.linkedin.com/in/YOUR_LINKEDIN" target="_blank">
#                 <img src="https://cdn.simpleicons.org/linkedin/0A66C2" width="22"/>
#             </a>
#             <a href="https://github.com/YOUR_GITHUB" target="_blank">
#                 <img src="https://cdn.simpleicons.org/github/181717" width="22"/>
#             </a>
#             <a href="https://twitter.com/YOUR_X" target="_blank">
#                 <img src="https://cdn.simpleicons.org/x/000000" width="22"/>
#             </a>
#             <a href="https://medium.com/@YOUR_MEDIUM" target="_blank">
#                 <img src="https://cdn.simpleicons.org/medium/000000" width="22"/>
#             </a>
#             <a href="https://orcid.org/YOUR_ORCID" target="_blank">
#                 <img src="https://cdn.simpleicons.org/orcid/A6CE39" width="22"/>
#             </a>
#         </div>

#         <div style="margin-top: 0.75rem; font-size: 0.75rem;">
#             Powered by Python, Streamlit, LlamaIndex & QdrantDB • Built for knowledge seekers and autodidactics • Inspired by NotebookLM • Document Intelligence System
#         </div>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown(
#     """
#     <hr style="margin-top: 2rem; margin-bottom: 1rem;">

#     <div style="text-align: center; font-size: 0.9rem; color: #9ca3af;">
#         <div style="margin-bottom: 0.6rem;">
#             Created by <strong>Aarya R. Thakar</strong> aka <strong>आर्यम्</strong>
#         </div>

#         <div style="display: flex; justify-content: center; gap: 18px; align-items: center;">
#             <a href="https://www.linkedin.com/in/YOUR_LINKEDIN" target="_blank">
#                 <img src="https://cdn.simpleicons.org/linkedin/0A66C2" width="22">
#             </a>
#             <a href="https://github.com/YOUR_GITHUB" target="_blank">
#                 <img src="https://cdn.simpleicons.org/github/FFFFFF" width="22">
#             </a>
#             <a href="https://twitter.com/YOUR_X" target="_blank">
#                 <img src="https://cdn.simpleicons.org/x/FFFFFF" width="22">
#             </a>
#             <a href="https://medium.com/@YOUR_MEDIUM" target="_blank">
#                 <img src="https://cdn.simpleicons.org/medium/FFFFFF" width="22">
#             </a>
#             <a href="https://orcid.org/YOUR_ORCID" target="_blank">
#                 <img src="https://cdn.simpleicons.org/orcid/A6CE39" width="22">
#             </a>
#         </div>

#         <div style="margin-top: 0.8rem; font-size: 0.75rem;">
#             Powered by Python • Streamlit • LlamaIndex • QdrantDB
#         </div>
#     </div>
#     """,
#     unsafe_allow_html=True
# )
st.markdown("---")
st.markdown(" <center> Created by <strong>Aarya R. Thakar</strong> aka <strong>आर्यम् </strong> ", unsafe_allow_html=True)
st.markdown(
    """
    <div style="display: flex; justify-content: center; gap: 18px; align-items: center;">
             <a href="https://www.linkedin.com/in/aaryamthakar" target="_blank">
                 <img src="https://www.svgrepo.com/show/157006/linkedin.svg" width="22">
             </a>
             <a href="https://github.com/Aaryam-7d6" target="_blank">
                 <img src="https://cdn.simpleicons.org/github/FFFFFF" width="22">
             </a>
             <a href="https://x.com/Aaryam_Thakar" target="_blank">
                 <img src="https://cdn.iconscout.com/icon/free/png-512/free-twitter-logo-icon-svg-download-png-721979.png?f=webp&w=512" width="22">
             </a>
             <a href="https://medium.com/@aaryamthakar0110" target="_blank">
                 <img src="https://cdn.simpleicons.org/medium/FFFFFF" width="22">
             </a>
             <a href="https://orcid.org/0009-0002-9988-7141" target="_blank">
                 <img src="https://cdn.simpleicons.org/orcid/A6CE39" width="22">
             </a>
         </div>
    """,
    unsafe_allow_html=True
)
st.markdown(""" 
            <div style="margin-top: 0.75rem; font-size: 0.75rem;">
             Powered by Python, Streamlit, LlamaIndex & QdrantDB • Built for knowledge seekers and autodidactics • Inspired by NotebookLM • Document Intelligence System
         </div>
     """, unsafe_allow_html=True
)

# <img src="https://cdn.simpleicons.org/linkedin/0A66C2" width="22">       
# <img src="https://cdn.simpleicons.org/x/FFFFFF" width="22">
# <img sec="https://www.svgrepo.com/show/13677/twitter.svg"width="22">
# https://cdn.iconscout.com/icon/free/png-512/free-twitter-logo-icon-svg-download-png-721979.png?f=webp&w=512
# https://www.svgrepo.com/_next/static/media/dot.6429a523.svg