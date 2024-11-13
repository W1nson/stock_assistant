from flask import Flask, render_template, request, Response

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
import yfinance as yf 
import os
from dotenv import load_dotenv

system_prompt = "" 

app = Flask(__name__) 

llm = ChatOllama(
	base_url = "http://100.125.116.26:11434",
	model = "llama3.2",
	temperature = 0.8,
	num_predict = 128,
)

messages = [
	("system", "You are a helpful Stock analyst. Help summarize the information user. with also simple math"),
	("human", "What is the current price of Nvidia?")
]
ai_msg = llm_with_tools.invoke(messages)

def stream(input_text):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": "You're an assistant."},
            {"role": "user", "content": f"{prompt(input_text)}"},
        ], stream=True, max_tokens=500, temperature=0)
        for line in completion:
            if 'content' in line['choices'][0]['delta']:
                yield line['choices'][0]['delta']['content']




@app.route('/completion', methods=['GET', 'POST'])
def completion_api():
    if request.method == "POST":
        data = request.form
        input_text = data['input_text']
        return Response(stream(input_text), mimetype='text/event-stream')
    else:
        return Response(None, mimetype='text/event-stream')