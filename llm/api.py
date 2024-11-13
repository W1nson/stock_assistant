import re
from pathlib import Path
from typing import Callable, Union
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_ollama import ChatOllama
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder 
from langchain_core.messages import HumanMessage
# from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents.react.agent import create_react_agent
# from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import yfinance as yf

from langserve import add_routes

import os
from dotenv import load_dotenv 
load_dotenv()

def _is_valid_identifier(value: str) -> bool:
    """Check if the session ID is in a valid format."""
    # Use a regular expression to match the allowed characters
    valid_characters = re.compile(r"^[a-zA-Z0-9-_]+$")
    return bool(valid_characters.match(value))

def create_session_factory(
    base_dir: Union[str, Path],
) -> Callable[[str], BaseChatMessageHistory]:
    """Create a session ID factory that creates session IDs from a base dir.

    Args:
        base_dir: Base directory to use for storing the chat histories.

    Returns:
        A session ID factory that creates session IDs from a base path.
    """
    base_dir_ = Path(base_dir) if isinstance(base_dir, str) else base_dir
    if not base_dir_.exists():
        base_dir_.mkdir(parents=True)

    def get_chat_history(session_id: str) -> FileChatMessageHistory:
        """Get a chat history from a session ID."""
        if not _is_valid_identifier(session_id):
            raise HTTPException(
                status_code=400,
                detail=f"Session ID `{session_id}` is not in a valid format. "
                "Session ID must only contain alphanumeric characters, "
                "hyphens, and underscores.",
            )
        file_path = base_dir_ / f"{session_id}.json"
        return FileChatMessageHistory(str(file_path))

    return get_chat_history


model = ChatOllama(
	base_url = "http://100.125.116.26:11434",
	model = "llama3.2",
	temperature = 0.8,
	num_predict = 256,
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're an assistant who can gather stock information and news to help user evaluate the potential of the stock. Help them make decision on whether or not it's a good time to buy or sell. You shouldn't give direct advice on any financial decision."),
		MessagesPlaceholder(variable_name="history"),      
		("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
@tool 
def get_current_price(symbol: str) -> float:
	"""Get current price of the stock """
	ticker = yf.Ticker(symbol)
	todays_data = ticker.history(period='1d')
	return todays_data['Close'][0]


tools = [YahooFinanceNewsTool(), get_current_price]
# llm_with_tools = model.bind_tools(tools)
agent = create_react_agent(llm=model, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)


class InputChat(BaseModel):
    """Input for the chat endpoint."""

    # The field extra defines a chat widget.
    # As of 2024-02-05, this chat widget is not fully supported.
    # It's included in documentation to show how it should be specified, but
    # will not work until the widget is fully supported for history persistence
    # on the backend.
    human_input: str = Field(
        ...,
        description="The human input to the chat system.",
        extra={"widget": {"type": "chat", "input": "human_input"}},
    )


chain_with_history = RunnableWithMessageHistory(
    agent_executor,
    create_session_factory("chat_histories"),
    input_messages_key="human_input",
    history_messages_key="history",
).with_types(input_type=InputChat)


add_routes(
    app,
    chain_with_history,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)