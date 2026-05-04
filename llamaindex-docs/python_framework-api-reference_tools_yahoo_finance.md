# Yahoo finance
##  YahooFinanceToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/yahoo_finance/#llama_index.tools.yahoo_finance.YahooFinanceToolSpec "Permanent link")
Bases: 
Yahoo Finance tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-yahoo-finance/llama_index/tools/yahoo_finance/base.py`  
| 
```
 6
 7
 8
 9
10
11
12
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
```
 | 
```
classYahooFinanceToolSpec(BaseToolSpec):
"""Yahoo Finance tool spec."""

    spec_functions = [
        "balance_sheet",
        "income_statement",
        "cash_flow",
        "stock_basic_info",
        "stock_analyst_recommendations",
        "stock_news",
    ]

    def__init__(self) -> None:
"""Initialize the Yahoo Finance tool spec."""

    defbalance_sheet(self, ticker: str) -> str:
"""
        Return the balance sheet of the stock.

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
        stock = yf.Ticker(ticker)
        balance_sheet = pd.DataFrame(stock.balance_sheet)
        return "Balance Sheet: \n" + balance_sheet.to_string()

    defincome_statement(self, ticker: str) -> str:
"""
        Return the income statement of the stock.

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
        stock = yf.Ticker(ticker)
        income_statement = pd.DataFrame(stock.income_stmt)
        return "Income Statement: \n" + income_statement.to_string()

    defcash_flow(self, ticker: str) -> str:
"""
        Return the cash flow of the stock.

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
        stock = yf.Ticker(ticker)
        cash_flow = pd.DataFrame(stock.cashflow)
        return "Cash Flow: \n" + cash_flow.to_string()

    defstock_basic_info(self, ticker: str) -> str:
"""
        Return the basic info of the stock. Ex: price, description, name.

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
        stock = yf.Ticker(ticker)
        return "Info: \n" + str(stock.info)

    defstock_analyst_recommendations(self, ticker: str) -> str:
"""
        Get the analyst recommendations for a stock.

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
        stock = yf.Ticker(ticker)
        return "Recommendations: \n" + str(stock.recommendations)

    defstock_news(self, ticker: str) -> str:
"""
        Get the most recent news titles of a stock.

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
        stock = yf.Ticker(ticker)
        news = stock.news
        out = "News: \n"
        for i in news:
            out += i["title"] + "\n"
        return out

```
 |  
| --- | --- |  
###  balance_sheet [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/yahoo_finance/#llama_index.tools.yahoo_finance.YahooFinanceToolSpec.balance_sheet "Permanent link")

```
balance_sheet(ticker: ) -> 

```

Return the balance sheet of the stock.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ticker`  |  the stock ticker to be given to yfinance  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-yahoo-finance/llama_index/tools/yahoo_finance/base.py`  
| 
```
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
```
 | 
```
defbalance_sheet(self, ticker: str) -> str:
"""
    Return the balance sheet of the stock.

    Args:
      ticker (str): the stock ticker to be given to yfinance

    """
    stock = yf.Ticker(ticker)
    balance_sheet = pd.DataFrame(stock.balance_sheet)
    return "Balance Sheet: \n" + balance_sheet.to_string()

```
 |  
| --- | --- |  
###  income_statement [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/yahoo_finance/#llama_index.tools.yahoo_finance.YahooFinanceToolSpec.income_statement "Permanent link")

```
income_statement(ticker: ) -> 

```

Return the income statement of the stock.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ticker`  |  the stock ticker to be given to yfinance  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-yahoo-finance/llama_index/tools/yahoo_finance/base.py`  
| 
```
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
```
 | 
```
defincome_statement(self, ticker: str) -> str:
"""
    Return the income statement of the stock.

    Args:
      ticker (str): the stock ticker to be given to yfinance

    """
    stock = yf.Ticker(ticker)
    income_statement = pd.DataFrame(stock.income_stmt)
    return "Income Statement: \n" + income_statement.to_string()

```
 |  
| --- | --- |  
###  cash_flow [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/yahoo_finance/#llama_index.tools.yahoo_finance.YahooFinanceToolSpec.cash_flow "Permanent link")

```
cash_flow(ticker: ) -> 

```

Return the cash flow of the stock.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ticker`  |  the stock ticker to be given to yfinance  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-yahoo-finance/llama_index/tools/yahoo_finance/base.py`  
| 
```
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
```
 | 
```
defcash_flow(self, ticker: str) -> str:
"""
    Return the cash flow of the stock.

    Args:
      ticker (str): the stock ticker to be given to yfinance

    """
    stock = yf.Ticker(ticker)
    cash_flow = pd.DataFrame(stock.cashflow)
    return "Cash Flow: \n" + cash_flow.to_string()

```
 |  
| --- | --- |  
###  stock_basic_info [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/yahoo_finance/#llama_index.tools.yahoo_finance.YahooFinanceToolSpec.stock_basic_info "Permanent link")

```
stock_basic_info(ticker: ) -> 

```

Return the basic info of the stock. Ex: price, description, name.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ticker`  |  the stock ticker to be given to yfinance  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-yahoo-finance/llama_index/tools/yahoo_finance/base.py`  
| 
```
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
```
 | 
```
defstock_basic_info(self, ticker: str) -> str:
"""
    Return the basic info of the stock. Ex: price, description, name.

    Args:
      ticker (str): the stock ticker to be given to yfinance

    """
    stock = yf.Ticker(ticker)
    return "Info: \n" + str(stock.info)

```
 |  
| --- | --- |  
###  stock_analyst_recommendations [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/yahoo_finance/#llama_index.tools.yahoo_finance.YahooFinanceToolSpec.stock_analyst_recommendations "Permanent link")

```
stock_analyst_recommendations(ticker: ) -> 

```

Get the analyst recommendations for a stock.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ticker`  |  the stock ticker to be given to yfinance  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-yahoo-finance/llama_index/tools/yahoo_finance/base.py`  
| 
```
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
```
 | 
```
defstock_analyst_recommendations(self, ticker: str) -> str:
"""
    Get the analyst recommendations for a stock.

    Args:
      ticker (str): the stock ticker to be given to yfinance

    """
    stock = yf.Ticker(ticker)
    return "Recommendations: \n" + str(stock.recommendations)

```
 |  
| --- | --- |  
###  stock_news [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/yahoo_finance/#llama_index.tools.yahoo_finance.YahooFinanceToolSpec.stock_news "Permanent link")

```
stock_news(ticker: ) -> 

```

Get the most recent news titles of a stock.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ticker`  |  the stock ticker to be given to yfinance  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-yahoo-finance/llama_index/tools/yahoo_finance/base.py`  
| 
```
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
```
 | 
```
defstock_news(self, ticker: str) -> str:
"""
    Get the most recent news titles of a stock.

    Args:
      ticker (str): the stock ticker to be given to yfinance

    """
    stock = yf.Ticker(ticker)
    news = stock.news
    out = "News: \n"
    for i in news:
        out += i["title"] + "\n"
    return out

```
 |  
| --- | --- |  
options: members: - YahooFinanceToolSpec
