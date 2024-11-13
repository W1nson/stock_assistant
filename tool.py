from langchain_core.tools import tool
import yfinance as yf 


@tool
def add(a: int, b: int) -> int:
	"""Adds a and b."""
	return a + b


@tool
def multiply(a: int, b: int) -> int:
	"""Multiplies a and b."""
	return a * b

@tool 
def get_current_price(symbol: str) -> float:
	"""Get current price of the stock """
	ticker = yf.Ticker(symbol)
	todays_data = ticker.history(period='1d')
	return todays_data['Close'][0]

@tool 
def get_stock_info(symbol: str) -> str: 
	"""Get general information about the stock"""
	ticker = yf.Ticker(symbol)
	return ticker.info

# @tool
# def get_stock_news(symbol: str) -> str: 
# 	"""Get news about the stock"""
# 	ticker = yf.Ticker(symbol) 
	
# 	return 