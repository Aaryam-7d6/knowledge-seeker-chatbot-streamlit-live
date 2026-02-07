from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import EMBED_MODEL_NAME

def get_embedding_model():
    return HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)
