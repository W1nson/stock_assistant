from api_test import News, Perigon
from APItoVDB import APItoVDB
import os 

from langchain_community.embeddings import OllamaEmbeddings

from dotenv import load_dotenv 
load_dotenv()


def main(): 
	# News data
	api = Perigon(os.getenv('PERIGON_API_KEY'), 'https://api.goperigon.com/v1/')
	params = { 
		"category": "Business",
		"sourceGroup": "top100",
		"showReprints": "false"
	}
	res = api.all('TSLA', **params)

	# vector DB 
	db = APItoVDB()
	# choose your embedding models 
	embedding_function = OllamaEmbeddings(model="nomic-embed-text")
	
	
	# try: 
	db.create('temp', emb_fn=embedding_function)

	for article in res[:5]:
		print(article['content'])
		db.load(article['content']) 


	print(db.query("TSLA"))

	# debug
	db.delete('temp')
	# except: 
	# 	db.delete('temp')


if __name__ == "__main__": 
	main()
