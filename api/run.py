from api_test import News
from APItoVDB import APItoVDB
import os 

from langchain_community.embeddings import OllamaEmbeddings

from dotenv import load_dotenv 
load_dotenv()


def main(): 
	# News data
	api = News(os.getenv('NEWS_API_KEY'), 'https://newsapi.org/v2/')

	params = { 
		"from": "2024-04-28",
		"sortBy": "popularity",

	}
	res = api.get_everything('TSLA', **params)

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
