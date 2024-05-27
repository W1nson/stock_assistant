# stock_assistant


## To-Do
- [ ] setup LangChain to connect with OllamaAPI
- [ ] study which API provides the best output (**Cleaner Data the Better Performance/Efficient**)
- [ ] Do we need vectorDB(RAG) at all for the Question-Answering(QA)? How would that slow down our process? or How can we speed up the process using other approach? 




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