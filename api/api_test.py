import requests
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

	def get(self, )
		



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
	
		
		
# import requests

# params = {
#   'access_key': '941c85f9caebb38b4a757ef1ba6f1be1'
# }

# api_result = requests.get('https://api.marketstack.com/v1/tickers/aapl/eod', params)

# api_response = api_result.json()
