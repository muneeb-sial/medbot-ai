from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingsFactory:
    def __init__(self):
        print("🚧 Initializing EmbeddingsFactory...")
        self.embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        print("✅ HuggingFaceEmbeddings initialized.")
        
embedding = EmbeddingsFactory().embedding