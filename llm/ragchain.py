import dotenv
import os 
dotenv.load_dotenv()

# open-source models 
from transformers import AutoModel, AutoTokenizer, pipeline

# langchain
from langchain import hub
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# openai & langchain integration 
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# google genmini
from langchain_google_genai import ChatGoogleGenerativeAI


# vector store
from langchain_community.vectorstores import Chroma
import chromadb 



class ragchain: 

    def from_google(self, embedding_function=None, collection_name='langchain', k=2):

        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.embedding_function = embedding_function if embedding_function else OpenAIEmbeddings() 
        self.collection_name = collection_name 
        self.retriever = self.set_chromadb( k=k, collection_name=collection_name)

        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        self.prompt = hub.pull("rlm/rag-prompt")

        self.rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        return self.rag_chain


    def from_openai(self, embedding_function=None, collection_name='langchain', k=2):
        self.embedding_function = embedding_function if embedding_function else OpenAIEmbeddings() 
        self.collection_name = collection_name 
        self.retriever = self.set_chromadb( k=k, collection_name=self.collection_name)

        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.prompt = hub.pull("rlm/rag-prompt")

        self.rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        return self.rag_chain

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)


    def from_model_id(self, model_name, model_type, embedding_function, host='localhost', port='8000', k=4, chain_type='refine', path=None, **kwargs):
        self.model_name = model_name 
        self.model_type = model_type 
        self.embedding_function = embedding_function
        self.chain_type = chain_type 

        self.retriever = self.set_chromadb(path=path, host=host, port=port, k=k)

        self.llm_pipe = pipeline(model_type, model=model_name, tokenizer=model_name, return_tensors='pt')
        
        if not self.model_type == 'question-answering': 
            self.llm = HuggingFacePipeline(
                pipeline=self.llm_pipe,
                model_kwargs={"temperature": 0.7, "max_new_tokens": 256, "max_length": 256},
            )

        self.model = RetrievalQA.from_chain_type(llm=self.llm, chain_type="refine", retriever=self.retriever, return_source_documents=False)

        return self
    
    def set_embedding_function(self, embedding_function): 
        self.embedding_function = embedding_function

    def set_chromadb(self, path=None, host='localhost', port='8000', k=4, collection_name='langchain'): 
        if path: 
            self.client = chromadb.PersistentClient(path=path)
        else: 
            self.client = chromadb.HttpClient(host=host, port=port)   

        self.k = k 
        self.collection_name = collection_name
        self.retriever = Chroma( 
            client=self.client,
            collection_name=collection_name,
            embedding_function=self.embedding_function,
        ).as_retriever(search_kwargs={'k': k}) 
                
        return self.retriever

    def set_llm(self, model_name, model_type, model_kwargs=None):

        if not model_kwargs:
            model_kwargs = {"temperature": 0.7, "max_new_tokens": 512}
        
        self.llm_pipe = pipeline(model_type, model=model_name, tokenizer=model_name)
        
        if not self.model_type == 'questions-answering': 
            self.llm = HuggingFacePipeline(
                pipeline=self.llm_pipe,
                model_kwargs=model_kwargs
            )
        
        self.model = RetrievalQA.from_chain_type(llm=self.llm, chain_type="refine", retriever=self.retriever, return_source_documents=False)

        return self.llm_pipe, self.llm
    
    def set_openai(self):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.prompt = hub.pull("rlm/rag-prompt")

        return 


    def generate(self, question):
        
        if self.model_type == 'question-answering':
            docs = self.retriever.get_relevant_documents(question)
            prompt = {"question": question, "context": '\n'.join([d.page_content for d in docs])}
            res = self.llm(prompt)

        else: 
            res = self.model.invoke({"query": question})
            res = res['result']
        return res


