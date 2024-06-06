import chromadb 
from typing import Optional 
from langchain_community.vectorstores import Chroma
import chromadb.utils.embedding_functions as embedding_functions
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter


from api_test import News
import os 
from dotenv import load_dotenv

load_dotenv()


class APItoVDB: 

	def __init__(self, host='localhost', port='8000'):
		self.host = host 
		self.port = port 

		self.client = chromadb.HttpClient(host=self.host, port=self.port) 
		self.id = 0 
		self.name = None

	def create(self, name, emb_fn=None, metadata:Optional[dict]=None): 
		try: 
			self.emb_fn = emb_fn
			self.name = name
			self.collection = self.client.create_collection(name=name, metadata=metadata)
			print(f"{self.name} is Created")

			return 
		except: 
			print(f"{name} failed to create")
			return 

	def delete(self, name=None): 
		try:
			if not name: 
				self.client.delete_collection(name=self.name) 
				print(f"{self.name} is Deleted")
			else: 
				self.client.delete_collection(name=name) 
				print(f"{name} is Deleted")
		except: 
			print(f"{self.name} failed to delete")
		return 

	def load(self, content, metadata): 
		# embedding_functions
		docs = self.preprocess(content, metadata)
		self.db = Chroma.from_documents(docs, self.emb_fn, client=self.client, collection_name=self.name)
		return self.db 

	def preprocess(self, content, metadata): 
		text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
		documents = text_splitter.create_documents([content], metadatas=[metadata])
		# print(documents)
		docs = text_splitter.split_documents(documents)
		return docs 
	
	def query(self, q): 
		return self.db.similarity_search(q) 
	


