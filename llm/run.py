from ragchain import ragchain 

from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)


if __name__ == "__main__": 
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # model = RAGModel().from_model_id(model_name="gpt2-medium", model_type='text-generation', embedding_function=embedding_function)

    model = ragchain().from_ollama('phi3', embedding_function=embedding_function, k=3)


    # question = "What is the economy in America right now?"
    
    # llm_pipe, llm = model.set_llm(model_name="gpt2-medium", model_type='text-generation')
    # res = llm_pipe(question)
    # print(res)
    
    # res = model.invoke(question)

    for chunk in model.stream("What happened between Russia and Ukraine?"):
        print(chunk, end="", flush=True)

    # print(model.prompt)

    # print(res)