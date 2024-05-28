import requests
import json
import os 
from dotenv import load_dotenv

load_dotenv()

class API_Base: 
	def __init__(self, name, key, domain=None): 
		self.name = name
		self.key = key 
		self.domain = domain 

	def __repr__(self) -> str:
		return f'API({self.name}, {self.domain})'
	

class News(API_Base): 
	def __init__(self, key, domain=None):
		super().__init__('News', key, domain)
		
		self.args = {
			'apiKey': key
		}
		# Read documnetation: https://newsapi.org/docs/endpoints/everything
		# example: 
		# params = { 
		# 	'q': "bitcoin", 
		# 	'searchIn': "title", 
		# 	"sources": "",
		# 	"domains": "techcrunch.com,thenextweb.com", 
		#   ... etc
		# }

	def get_everything(self, q, **kwargs):

		self.args['q'] = q
		self.args.update(kwargs)
		url = os.path.join(self.domain, 'everything?')
		for i, kv in enumerate(self.args.items()): 
			if i == 0: 
				url += f"{kv[0]}={kv[1]}"
			else: 
				url += f"&{kv[0]}={kv[1]}"

		
		print(url)
		res = requests.get(url)
		res = res.json()
		self.out = res
		if res['status'] != 'ok': 
			print("Error:", res['code'])
			print(res['message'])
			return res

		print(f"Successfully Retrieve {res['totalResults']} articles")
		
		return res['articles']

	# def to_json(self, name): 
	# 	with open(name, 'w') as file: 
	# 		json.dump(self.out, file)
		
def main(): 
	api = News(os.getenv('NEWS_API_KEY'), 'https://newsapi.org/v2/')

	params = { 
		"from": "2024-04-28",
		"sortBy": "popularity",

	}
	res = api.get_everything('TSLA', **params)

class FMP(API_Base): 
	def __init__(self, key, domain):
		super().__init__('FMP', key, domain)

	def get_balance_sheet(self, symbol, period='', limit=''): 
		assert period in ['', 'annual', 'quarter'], f'period parameter must be annual, quarter, or none. Error: period={period}'

		url = os.path.join(self.domain,'balance-sheet-statement',symbol)
		print(url)
		params = {'apikey': self.key}
		params['period'] = period 
		params['limit'] = limit
		res = requests.get(url, params)
		print(res.url)

		return res.json()

if __name__ == '__main__': 
	main()