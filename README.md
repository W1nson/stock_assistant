# stock_assistant


## To-Do
- [x] setup LangChain to connect with OllamaAPI
- [ ] study which API provides the best output (**Cleaner Data the Better Performance/Efficient**)
- [ ] (Alec) Need to think about how to pick the useful data from the API? Do we need to include title? descriptions? or just content? 
- [ ] Do we need vectorDB(RAG) at all for the Question-Answering(QA)? How would that slow down our process? or How can we speed up the process using other approach? 

## Getting Started 

Setup a virtual environment to run have the same setup as the development: 

```
git clone https://github.com/W1nson/stock_assistant.git
cd stock_assistant
```

Setup your conda environment: 
```
conda activate nlp 
pip install -r requirements.txt 
```


To run the Ollama Model locally with RAG: 

First you need to run Chromadb Docker: 
```
docker run --rm -it -p 8000:8000 --mount type=volume,src=langchain,target=/chroma/chroma chromadb/chroma
``` 

Then run 
```
cd llm 
python3 run.py 
```


## News API study: 
Please use the `new_api_demo.ipynb` to try out the API wrapper. 
Let me know if there is anything that can be improved. 

## Frontend: 
- using openwebUI as frontend?

## Ollama resources: 
- setting ollama as a restful api to call the API which would allow for other LLM Hosting API uses for future 
- [Ollama API endpoint documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- We should use ollama-python to test out the function calling 
	- We might need to work on prompt engineering to give an example or few-shot prompting or chain-of-thought techniques to enchance the accuracy of function calling json format

## [LangChain](https://github.com/langchain-ai/langchain): 
- using langchain as a wrapper to connect the RAG (LLM + VectorDB)


## VectorDB: 
- [ChromaDB](https://docs.trychroma.com/)
	- Running ChromaDB as Docker Container for hosting (Currently 05/24/2024)
	- Create a volume and connect to the container, saving the load in volume

		```docker run --rm -it -p 8000:8000 --mount type=volume,src=langchain,target=/chroma/chroma chromadb/chroma```

## API options: 

- [NEWS API](https://newsapi.org/): 100 requests/day, articles with 24 hr delay, [...etc](https://newsapi.org/pricing)
	- [Docs](https://newsapi.org/docs)

- [TheNewsAPI](https://www.thenewsapi.com/): 100 requests/day, real time data, [...etc](https://www.thenewsapi.com/pricing)
	- [Docs](https://www.thenewsapi.com/documentation)

- [MarketStack](https://marketstack.com/): 100 requests/month, [...etc](https://marketstack.com/product)
	- [Docs](https://marketstack.com/documentation)

- [FMP](https://site.financialmodelingprep.com/): 250 requests/day, 5 year historical data, [..etc](https://site.financialmodelingprep.com/developer/docs/pricing)
	- [Docs](https://site.financialmodelingprep.com/developer/docs)