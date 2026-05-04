# Finance
##  FinanceAgentToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec "Permanent link")
Bases: 
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```

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
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
```
 | 
```
classFinanceAgentToolSpec(BaseToolSpec):
    spec_functions = [
        "find_similar_companies",
        "get_earnings_history",
        "get_stocks_with_upcoming_earnings",
        "get_current_gainer_stocks",
        "get_current_loser_stocks",
        "get_current_undervalued_growth_stocks",
        "get_current_technology_growth_stocks",
        "get_current_most_traded_stocks",
        "get_current_undervalued_large_cap_stocks",
        "get_current_aggressive_small_cap_stocks",
        "get_trending_finance_news",
        "get_google_trending_searches",
        "get_google_trends_for_query",
        "get_latest_news_for_stock",
        "get_current_stock_price_info",
    ]

    def__init__(
        self,
        polygon_api_key: str,
        finnhub_api_key: str,
        alpha_vantage_api_key: str,
        newsapi_api_key: str,
    ):
        self._api_key = {
            "ALPHA_VANTAGE": alpha_vantage_api_key,
            "POLYGON": polygon_api_key,
            "FINNHUB": finnhub_api_key,
            "NEWSAPI": newsapi_api_key,
        }

    deffind_similar_companies(self, symbol: str) -> List[str]:
"""Given a stock's ticker symbol, returns a list of similar companies."""
        return comparisons.find_similar_companies(self._api_key, symbol)

    defget_earnings_history(self, symbol: str) -> pd.DataFrame:
"""Given a stock's ticker symbol, returns a dataframe storing actual and estimated earnings over past K quarterly reports."""
        return earnings.get_earnings_history(self._api_key, symbol)

    defget_latest_earning_estimate(self, symbol: str) -> float:
"""Given a stock's ticker symbol, returns it's earnings estimate for the upcoming quarterly report."""
        return earnings.get_latest_earning_estimate(symbol)

    defget_stocks_with_upcoming_earnings(
        self, num_days_from_now: int, only_sp500: bool
    ) -> pd.DataFrame:
"""
        Returns a pandas dataframe containing all stocks which are announcing earnings in upcoming days.

        Arguments:
         num_days_from_now: only returns stocks which announcing earnings from today's date to num_days_from_now.
         only_sp500: only returns sp500 stocks.

        """
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(num_days_from_now)).strftime("%Y-%m-%d")
        return earnings.get_upcoming_earnings(
            self._api_key,
            start_date=start_date,
            end_date=end_date,
            country="USD",
            only_sp500=only_sp500,
        )

    defget_current_gainer_stocks(self) -> pd.DataFrame:
"""
        Return US stocks which are classified as day gainers as per Yahoo Finance.

        A US stock is classified as day gainer if %change in price > 3, price >=5, volume > 15_000

        """
        return news.get_current_gainer_stocks()

    defget_current_loser_stocks(self) -> pd.DataFrame:
"""
        Returns US stocks which are classified as day losers as per Yahoo Finance.

        A US stock is classified as day loser if %change in price < -2.5, price >=5, volume > 20_000

        """
        return news.get_current_loser_stocks()

    defget_current_undervalued_growth_stocks(self) -> pd.DataFrame:
"""
        Get list of undervalued growth stocks in US market as per Yahoo Finance.

        A stock with Price to Earnings ratio between 0-20, Price / Earnings to Growth < 1

        """
        return news.get_current_undervalued_growth_stocks()

    defget_current_technology_growth_stocks(self) -> pd.DataFrame:
"""
        Returns a data frame of growth stocks in technology sector in US market.

        If a stocks's quarterly revenue growth YoY% > 25%.

        """
        return news.get_current_technology_growth_stocks()

    defget_current_most_traded_stocks(self) -> pd.DataFrame:
"""
        Returns a dataframe storing stocks which were traded the most in current market.

        Stocks are ordered in decreasing order of activity i.e stock traded the most on top.

        """
        return news.get_current_most_traded_stocks()

    defget_current_undervalued_large_cap_stocks(self) -> pd.DataFrame:
"""Returns a dataframe storing US market large cap stocks with P/E < 20."""
        return news.get_current_undervalued_large_cap_stocks()

    defget_current_aggressive_small_cap_stocks(self) -> pd.DataFrame:
"""Returns a dataframe storing US market small cap stocks with 1 yr % change in earnings per share > 25."""
        return news.get_current_aggressive_small_cap_stocks()

    defget_trending_finance_news(self) -> List[str]:
"""Returns a list of top 10 trending news in financial market as per seekingalpha."""
        trends = news.get_topk_trending_news()
        return [t["title"] for t in trends]

    defget_google_trending_searches(self) -> Optional[pd.DataFrame]:
"""
        Returns trending searches in US as per google trends.

        If unable to find any trends, returns None.

        """
        return news.get_google_trending_searches(region="united_states")

    defget_google_trends_for_query(self, query: str) -> Optional[pd.DataFrame]:
"""
        Finds google search trends for a given query in United States.

        Returns None if unable to find any trends.

        """
        return news.get_google_trends_for_query(query=query, region="united_states")

    defget_latest_news_for_stock(self, stock_id: str) -> List[str]:
"""Given a stock_id representing the name of a company or the stock ticker symbol, Returns a list of news published related to top business articles in US in last 7 days from now."""
        articles = news.get_latest_news_for_stock(self._api_key, stock_id=stock_id)
        return [a["title"] for a in articles]

    defget_current_stock_price_info(
        self, stock_ticker_symbol: str
    ) -> Optional[Dict[str, Any]]:
"""
        Given a stock's ticker symbol, returns current price information of the stock.

        Returns None if the provided stock ticker symbol is invalid.
        """
        price_info = news.get_current_stock_price_info(
            self._api_key, stock_ticker_symbol
        )
        if price_info is not None:
            return {
                "Current Price": price_info["c"],
                "High Price of the day": price_info["h"],
                "Low Price of the day": price_info["l"],
                "Open Price of the day": price_info["o"],
                "Percentage change": price_info["dp"],
            }
        return None

```
 |  
| --- | --- |  
###  find_similar_companies [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.find_similar_companies "Permanent link")

```
find_similar_companies(symbol: ) -> []

```

Given a stock's ticker symbol, returns a list of similar companies.
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
42
43
44
```
 | 
```
deffind_similar_companies(self, symbol: str) -> List[str]:
"""Given a stock's ticker symbol, returns a list of similar companies."""
    return comparisons.find_similar_companies(self._api_key, symbol)

```
 |  
| --- | --- |  
###  get_earnings_history [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_earnings_history "Permanent link")

```
get_earnings_history(symbol: ) -> DataFrame

```

Given a stock's ticker symbol, returns a dataframe storing actual and estimated earnings over past K quarterly reports.
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
46
47
48
```
 | 
```
defget_earnings_history(self, symbol: str) -> pd.DataFrame:
"""Given a stock's ticker symbol, returns a dataframe storing actual and estimated earnings over past K quarterly reports."""
    return earnings.get_earnings_history(self._api_key, symbol)

```
 |  
| --- | --- |  
###  get_latest_earning_estimate [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_latest_earning_estimate "Permanent link")

```
get_latest_earning_estimate(symbol: ) -> float

```

Given a stock's ticker symbol, returns it's earnings estimate for the upcoming quarterly report.
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
50
51
52
```
 | 
```
defget_latest_earning_estimate(self, symbol: str) -> float:
"""Given a stock's ticker symbol, returns it's earnings estimate for the upcoming quarterly report."""
    return earnings.get_latest_earning_estimate(symbol)

```
 |  
| --- | --- |  
###  get_stocks_with_upcoming_earnings [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_stocks_with_upcoming_earnings "Permanent link")

```
get_stocks_with_upcoming_earnings(
    num_days_from_now: , only_sp500: 
) -> DataFrame

```

Returns a pandas dataframe containing all stocks which are announcing earnings in upcoming days.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `num_days_from_now`  |  only returns stocks which announcing earnings from today's date to num_days_from_now.  |  _required_  |  
|  `only_sp500`  |  `bool`  |  only returns sp500 stocks.  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
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
```
 | 
```
defget_stocks_with_upcoming_earnings(
    self, num_days_from_now: int, only_sp500: bool
) -> pd.DataFrame:
"""
    Returns a pandas dataframe containing all stocks which are announcing earnings in upcoming days.

    Arguments:
     num_days_from_now: only returns stocks which announcing earnings from today's date to num_days_from_now.
     only_sp500: only returns sp500 stocks.

    """
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(num_days_from_now)).strftime("%Y-%m-%d")
    return earnings.get_upcoming_earnings(
        self._api_key,
        start_date=start_date,
        end_date=end_date,
        country="USD",
        only_sp500=only_sp500,
    )

```
 |  
| --- | --- |  
###  get_current_gainer_stocks [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_current_gainer_stocks "Permanent link")

```
get_current_gainer_stocks() -> DataFrame

```

Return US stocks which are classified as day gainers as per Yahoo Finance.
A US stock is classified as day gainer if %change in price > 3, price >=5, volume > 15_000
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
75
76
77
78
79
80
81
82
```
 | 
```
defget_current_gainer_stocks(self) -> pd.DataFrame:
"""
    Return US stocks which are classified as day gainers as per Yahoo Finance.

    A US stock is classified as day gainer if %change in price > 3, price >=5, volume > 15_000

    """
    return news.get_current_gainer_stocks()

```
 |  
| --- | --- |  
###  get_current_loser_stocks [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_current_loser_stocks "Permanent link")

```
get_current_loser_stocks() -> DataFrame

```

Returns US stocks which are classified as day losers as per Yahoo Finance.
A US stock is classified as day loser if %change in price < -2.5, price >=5, volume > 20_000
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
84
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
defget_current_loser_stocks(self) -> pd.DataFrame:
"""
    Returns US stocks which are classified as day losers as per Yahoo Finance.

    A US stock is classified as day loser if %change in price < -2.5, price >=5, volume > 20_000

    """
    return news.get_current_loser_stocks()

```
 |  
| --- | --- |  
###  get_current_undervalued_growth_stocks [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_current_undervalued_growth_stocks "Permanent link")

```
get_current_undervalued_growth_stocks() -> DataFrame

```

Get list of undervalued growth stocks in US market as per Yahoo Finance.
A stock with Price to Earnings ratio between 0-20, Price / Earnings to Growth < 1
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
 93
 94
 95
 96
 97
 98
 99
100
```
 | 
```
defget_current_undervalued_growth_stocks(self) -> pd.DataFrame:
"""
    Get list of undervalued growth stocks in US market as per Yahoo Finance.

    A stock with Price to Earnings ratio between 0-20, Price / Earnings to Growth < 1

    """
    return news.get_current_undervalued_growth_stocks()

```
 |  
| --- | --- |  
###  get_current_technology_growth_stocks [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_current_technology_growth_stocks "Permanent link")

```
get_current_technology_growth_stocks() -> DataFrame

```

Returns a data frame of growth stocks in technology sector in US market.
If a stocks's quarterly revenue growth YoY% > 25%.
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
102
103
104
105
106
107
108
109
```
 | 
```
defget_current_technology_growth_stocks(self) -> pd.DataFrame:
"""
    Returns a data frame of growth stocks in technology sector in US market.

    If a stocks's quarterly revenue growth YoY% > 25%.

    """
    return news.get_current_technology_growth_stocks()

```
 |  
| --- | --- |  
###  get_current_most_traded_stocks [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_current_most_traded_stocks "Permanent link")

```
get_current_most_traded_stocks() -> DataFrame

```

Returns a dataframe storing stocks which were traded the most in current market.
Stocks are ordered in decreasing order of activity i.e stock traded the most on top.
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
111
112
113
114
115
116
117
118
```
 | 
```
defget_current_most_traded_stocks(self) -> pd.DataFrame:
"""
    Returns a dataframe storing stocks which were traded the most in current market.

    Stocks are ordered in decreasing order of activity i.e stock traded the most on top.

    """
    return news.get_current_most_traded_stocks()

```
 |  
| --- | --- |  
###  get_current_undervalued_large_cap_stocks [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_current_undervalued_large_cap_stocks "Permanent link")

```
get_current_undervalued_large_cap_stocks() -> DataFrame

```

Returns a dataframe storing US market large cap stocks with P/E < 20.
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
120
121
122
```
 | 
```
defget_current_undervalued_large_cap_stocks(self) -> pd.DataFrame:
"""Returns a dataframe storing US market large cap stocks with P/E < 20."""
    return news.get_current_undervalued_large_cap_stocks()

```
 |  
| --- | --- |  
###  get_current_aggressive_small_cap_stocks [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_current_aggressive_small_cap_stocks "Permanent link")

```
get_current_aggressive_small_cap_stocks() -> DataFrame

```

Returns a dataframe storing US market small cap stocks with 1 yr % change in earnings per share > 25.
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
124
125
126
```
 | 
```
defget_current_aggressive_small_cap_stocks(self) -> pd.DataFrame:
"""Returns a dataframe storing US market small cap stocks with 1 yr % change in earnings per share > 25."""
    return news.get_current_aggressive_small_cap_stocks()

```
 |  
| --- | --- |  
###  get_trending_finance_news [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_trending_finance_news "Permanent link")

```
get_trending_finance_news() -> []

```

Returns a list of top 10 trending news in financial market as per seekingalpha.
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
128
129
130
131
```
 | 
```
defget_trending_finance_news(self) -> List[str]:
"""Returns a list of top 10 trending news in financial market as per seekingalpha."""
    trends = news.get_topk_trending_news()
    return [t["title"] for t in trends]

```
 |  
| --- | --- |  
###  get_google_trending_searches [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_google_trending_searches "Permanent link")

```
get_google_trending_searches() -> Optional[DataFrame]

```

Returns trending searches in US as per google trends.
If unable to find any trends, returns None.
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
133
134
135
136
137
138
139
140
```
 | 
```
defget_google_trending_searches(self) -> Optional[pd.DataFrame]:
"""
    Returns trending searches in US as per google trends.

    If unable to find any trends, returns None.

    """
    return news.get_google_trending_searches(region="united_states")

```
 |  
| --- | --- |  
###  get_google_trends_for_query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_google_trends_for_query "Permanent link")

```
get_google_trends_for_query(
    query: ,
) -> Optional[DataFrame]

```

Finds google search trends for a given query in United States.
Returns None if unable to find any trends.
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
142
143
144
145
146
147
148
149
```
 | 
```
defget_google_trends_for_query(self, query: str) -> Optional[pd.DataFrame]:
"""
    Finds google search trends for a given query in United States.

    Returns None if unable to find any trends.

    """
    return news.get_google_trends_for_query(query=query, region="united_states")

```
 |  
| --- | --- |  
###  get_latest_news_for_stock [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_latest_news_for_stock "Permanent link")

```
get_latest_news_for_stock(stock_id: ) -> []

```

Given a stock_id representing the name of a company or the stock ticker symbol, Returns a list of news published related to top business articles in US in last 7 days from now.
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
151
152
153
154
```
 | 
```
defget_latest_news_for_stock(self, stock_id: str) -> List[str]:
"""Given a stock_id representing the name of a company or the stock ticker symbol, Returns a list of news published related to top business articles in US in last 7 days from now."""
    articles = news.get_latest_news_for_stock(self._api_key, stock_id=stock_id)
    return [a["title"] for a in articles]

```
 |  
| --- | --- |  
###  get_current_stock_price_info [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/finance/#llama_index.tools.finance.FinanceAgentToolSpec.get_current_stock_price_info "Permanent link")

```
get_current_stock_price_info(
    stock_ticker_symbol: ,
) -> Optional[[, ]]

```

Given a stock's ticker symbol, returns current price information of the stock.
Returns None if the provided stock ticker symbol is invalid.
Source code in `llama-index-integrations/tools/llama-index-tools-finance/llama_index/tools/finance/base.py`  
| 
```
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
```
 | 
```
defget_current_stock_price_info(
    self, stock_ticker_symbol: str
) -> Optional[Dict[str, Any]]:
"""
    Given a stock's ticker symbol, returns current price information of the stock.

    Returns None if the provided stock ticker symbol is invalid.
    """
    price_info = news.get_current_stock_price_info(
        self._api_key, stock_ticker_symbol
    )
    if price_info is not None:
        return {
            "Current Price": price_info["c"],
            "High Price of the day": price_info["h"],
            "Low Price of the day": price_info["l"],
            "Open Price of the day": price_info["o"],
            "Percentage change": price_info["dp"],
        }
    return None

```
 |  
| --- | --- |  
options: members: - FinanceAgentToolSpec
