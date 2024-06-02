from ragchain import ragchain 

from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.embeddings import OllamaEmbeddings

# choose your embedding models 
# embedding_function = OllamaEmbeddings(model="nomic-embed-text")

if __name__ == "__main__": 
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")

    # model = RAGModel().from_model_id(model_name="gpt2-medium", model_type='text-generation', embedding_function=embedding_function)

    model = ragchain().from_ollama('phi3', embedding_function=embedding_function, collection_name='temp', k=3)

    q = input("Enter your question: ")
    print(q)
    for chunk in model.stream(q):
        print(chunk, end="", flush=True)
