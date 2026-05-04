# Stock market data query engine
##  StockMarketDataQueryEnginePack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/stock_market_data_query_engine/#llama_index.packs.stock_market_data_query_engine.StockMarketDataQueryEnginePack "Permanent link")
Bases: 
Historical stock market data query engine pack based on yahoo finance.
Source code in `llama-index-packs/llama-index-packs-stock-market-data-query-engine/llama_index/packs/stock_market_data_query_engine/base.py`  
| 
```
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
```
 | 
```
classStockMarketDataQueryEnginePack(BaseLlamaPack):
"""Historical stock market data query engine pack based on yahoo finance."""

    def__init__(
        self,
        tickers: List[str],
        llm: Optional[LLM] = None,
        **kwargs: Any,
    ):
        self.tickers = tickers

        try:
            importyfinanceasyf
        except ImportError:
            raise ImportError("Dependencies missing, run `pip install yfinance`")

        stocks_market_data = []
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            hist = stock.history(**kwargs)

            year = [i.year for i in hist.index]
            hist.insert(0, "year", year)
            month = [i.month for i in hist.index]
            hist.insert(1, "month", month)
            day = [i.day for i in hist.index]
            hist.insert(2, "day", day)
            hist.reset_index(drop=True, inplace=True)
            stocks_market_data.append(hist)
        self.stocks_market_data = stocks_market_data

        Settings.llm = llm or OpenAI(model="gpt-4")

        df_price_query_engines = [
            PandasQueryEngine(stock) for stock in stocks_market_data
        ]

        summaries = [f"{ticker} historical market data" for ticker in tickers]

        df_price_nodes = [
            IndexNode(text=summary, index_id=f"pandas{idx}")
            for idx, summary in enumerate(summaries)
        ]

        df_price_id_query_engine_mapping = {
            f"pandas{idx}": df_engine
            for idx, df_engine in enumerate(df_price_query_engines)
        }

        stock_price_vector_index = VectorStoreIndex(df_price_nodes)
        stock_price_vector_retriever = stock_price_vector_index.as_retriever(
            similarity_top_k=1
        )

        stock_price_recursive_retriever = RecursiveRetriever(
            "vector",
            retriever_dict={"vector": stock_price_vector_retriever},
            query_engine_dict=df_price_id_query_engine_mapping,
            verbose=True,
        )

        stock_price_response_synthesizer = get_response_synthesizer(
            response_mode="compact"
        )

        stock_price_query_engine = RetrieverQueryEngine.from_args(
            stock_price_recursive_retriever,
            response_synthesizer=stock_price_response_synthesizer,
        )

        self.stock_price_query_engine = stock_price_query_engine

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "tickers": self.tickers,
            "stocks market data": self.stocks_market_data,
            "query engine": self.stock_price_query_engine,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run."""
        return self.stock_price_query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/stock_market_data_query_engine/#llama_index.packs.stock_market_data_query_engine.StockMarketDataQueryEnginePack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-stock-market-data-query-engine/llama_index/packs/stock_market_data_query_engine/base.py`  
| 
```
85
86
87
88
89
90
91
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "tickers": self.tickers,
        "stocks market data": self.stocks_market_data,
        "query engine": self.stock_price_query_engine,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/stock_market_data_query_engine/#llama_index.packs.stock_market_data_query_engine.StockMarketDataQueryEnginePack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run.
Source code in `llama-index-packs/llama-index-packs-stock-market-data-query-engine/llama_index/packs/stock_market_data_query_engine/base.py`  
| 
```
93
94
95
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run."""
    return self.stock_price_query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - StockMarketDataQueryEnginePack
