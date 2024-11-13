from langchain_core.tools import tool
from langchain_ollama import ChatOllama
import yfinance as yf 
from langchain.agents import AgentType, initialize_agent
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool

llm = ChatOllama(
	base_url = "http://100.125.116.26:11434",
	model = "llama3.2",
	temperature = 0.8,
	num_predict = 256,
)



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

@tool
def get_stock_news(symbol: str) -> str: 
	"""Get news about the stock"""
	ticker = yf.Ticker(symbol) 
	

	return 



tools = [add, multiply, get_current_price, get_stock_info]

llm_with_tools = llm.bind_tools(tools)

messages = [
	("system", "You are a helpful Stock analyst. Help summarize the information user. with also simple math"),
	("human", "What is the current price of Nvidia?")
]
ai_msg = llm_with_tools.invoke(messages)

print(ai_msg.tool_calls)

messages.append(ai_msg)

for tool_call in ai_msg.tool_calls:
	selected_tool = {"add": add, "multiply": multiply, "get_current_price": get_current_price, 'get_stock_info': get_stock_info}[tool_call["name"].lower()]
	tool_msg = selected_tool.invoke(tool_call)
	messages.append(tool_msg)

print(messages[-1])
output = llm_with_tools.invoke(messages)

print()
print(output.content)

