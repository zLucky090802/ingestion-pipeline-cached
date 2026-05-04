# Serpex
SERPEX tool for LlamaIndex.
##  SerpexToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/serpex/#llama_index.tools.serpex.SerpexToolSpec "Permanent link")
Bases: 
SERPEX tool spec for web search.
This tool allows you to search the web using the SERPEX API and get real-time search results from multiple search engines including Google, Bing, DuckDuckGo, Brave, Yahoo, and Yandex.
SERPEX provides fast, reliable search results via API, perfect for AI applications, RAG systems, and data analytics.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  `Optional[str]`  |  SERPEX API key. If not provided, will look for SERPEX_API_KEY environment variable.  |  `None`  |  
|  `engine`  |  Default search engine to use. Options: 'auto' (default), 'google', 'bing', 'duckduckgo', 'brave', 'yahoo', 'yandex'.  |  `'auto'`  |  
Examples:

```
>>> fromllama_index.tools.serpeximport SerpexToolSpec
>>> tool = SerpexToolSpec(api_key="your_api_key")
>>> results = tool.search("latest AI news")
>>> for doc in results:
...     print(doc.text)

```

Source code in `llama-index-integrations/tools/llama-index-tools-serpex/llama_index/tools/serpex/base.py`  
| 
```
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
classSerpexToolSpec(BaseToolSpec):
"""
    SERPEX tool spec for web search.

    This tool allows you to search the web using the SERPEX API and get
    real-time search results from multiple search engines including Google,
    Bing, DuckDuckGo, Brave, Yahoo, and Yandex.

    SERPEX provides fast, reliable search results via API, perfect for
    AI applications, RAG systems, and data analytics.

    Args:
        api_key (Optional[str]): SERPEX API key. If not provided, will look
            for SERPEX_API_KEY environment variable.
        engine (str): Default search engine to use. Options: 'auto' (default),
            'google', 'bing', 'duckduckgo', 'brave', 'yahoo', 'yandex'.

    Examples:
        >>> from llama_index.tools.serpex import SerpexToolSpec
        >>> tool = SerpexToolSpec(api_key="your_api_key")
        >>> results = tool.search("latest AI news")
        >>> for doc in results:
        ...     print(doc.text)
    """

    spec_functions = ["search"]

    def__init__(
        self,
        api_key: Optional[str] = None,
        engine: str = "auto",
    ) -> None:
"""
        Initialize SERPEX tool.

        Args:
            api_key: SERPEX API key. If not provided, reads from
                SERPEX_API_KEY environment variable.
            engine: Default search engine ('auto', 'google', 'bing', etc.).

        Raises:
            ValueError: If API key is not provided and not found in environment.
        """
        self.api_key = api_key or os.environ.get("SERPEX_API_KEY")

        if not self.api_key:
            raise ValueError(
                "SERPEX_API_KEY not found. Please set it as an environment "
                "variable or pass it as an argument. "
                "Get your API key at: https://serpex.dev/dashboard"
            )

        self.base_url = "https://api.serpex.dev/api/search"
        self.engine = engine

    defsearch(
        self,
        query: str,
        num_results: int = 10,
        engine: Optional[str] = None,
        time_range: Optional[str] = None,
    ) -> List[Document]:
"""
        Search the web using SERPEX API.

        This function queries the specified search engine and returns structured
        results containing titles, URLs, and snippets.

        Args:
            query: Search query string.
            num_results: Number of results to return (default: 10, max: 100).
            engine: Override default search engine. Options: 'auto', 'google',
                'bing', 'duckduckgo', 'brave', 'yahoo', 'yandex'.
            time_range: Filter results by time. Options: 'day', 'week',
                'month', 'year'.

        Returns:
            List of Document objects, one per search result.
            Each document contains the title, URL, and snippet in its text,
            with metadata including search details.

        Examples:
            >>> tool = SerpexToolSpec(api_key="your_key")
            >>> results = tool.search("LlamaIndex tutorial", num_results=5)
            >>> for doc in results:
            ...     print(f"Title: {doc.metadata['title']}")
            ...     print(f"URL: {doc.metadata['url']}")
            ...     print(doc.text)

            >>> # Search with specific engine
            >>> results = tool.search(
            ...     "privacy focused browser",
            ...     engine="duckduckgo",
            ...     num_results=5
            ... )

            >>> # Search with time filter
            >>> results = tool.search(
            ...     "AI news",
            ...     time_range="day",
            ...     num_results=10
            ... )
        """
        params: Dict[str, Any] = {
            "q": query,
            "engine": engine or self.engine,
            "category": "web",
        }

        if num_results:
            params["num"] = min(num_results, 100)  # Cap at 100

        if time_range:
            params["time_range"] = time_range

        try:
            response = requests.get(
                self.base_url,
                params=params,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                },
                timeout=30,
            )
            response.raise_for_status()

            data = response.json()

            # Extract results from the response
            results_list = data.get("results", [])

            if not results_list:
                return []

            # Get metadata
            api_metadata = data.get("metadata", {})
            num_results_total = api_metadata.get("number_of_results", 0)
            response_time = api_metadata.get("response_time", 0)

            # Create documents for each result
            documents = []
            for result in results_list[:num_results]:
                title = result.get("title", "No title")
                url = result.get("url", "")
                snippet = result.get("snippet", "No description available")

                text = f"{title}\nURL: {url}\n{snippet}"

                metadata = {
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                    "number_of_results": num_results_total,
                    "response_time": response_time,
                    "query": query,
                    "engine": engine or self.engine,
                }

                documents.append(Document(text=text, metadata=metadata))

            return documents

        except requests.exceptions.RequestException as e:
            raise e

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/serpex/#llama_index.tools.serpex.SerpexToolSpec.search "Permanent link")

```
search(
    query: ,
    num_results:  = 10,
    engine: Optional[] = None,
    time_range: Optional[] = None,
) -> []

```

Search the web using SERPEX API.
This function queries the specified search engine and returns structured results containing titles, URLs, and snippets.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Search query string.  |  _required_  |  
|  `num_results`  |  Number of results to return (default: 10, max: 100).  |  
|  `engine`  |  `Optional[str]`  |  Override default search engine. Options: 'auto', 'google', 'bing', 'duckduckgo', 'brave', 'yahoo', 'yandex'.  |  `None`  |  
|  `time_range`  |  `Optional[str]`  |  Filter results by time. Options: 'day', 'week', 'month', 'year'.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List of Document objects, one per search result.  |  
|   |  Each document contains the title, URL, and snippet in its text,  |  
|   |  with metadata including search details.  |  
Examples:

```
>>> tool = SerpexToolSpec(api_key="your_key")
>>> results = tool.search("LlamaIndex tutorial", num_results=5)
>>> for doc in results:
...     print(f"Title: {doc.metadata['title']}")
...     print(f"URL: {doc.metadata['url']}")
...     print(doc.text)

```


```
>>> # Search with specific engine
>>> results = tool.search(
...     "privacy focused browser",
...     engine="duckduckgo",
...     num_results=5
... )

```


```
>>> # Search with time filter
>>> results = tool.search(
...     "AI news",
...     time_range="day",
...     num_results=10
... )

```

Source code in `llama-index-integrations/tools/llama-index-tools-serpex/llama_index/tools/serpex/base.py`  
| 
```
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
defsearch(
    self,
    query: str,
    num_results: int = 10,
    engine: Optional[str] = None,
    time_range: Optional[str] = None,
) -> List[Document]:
"""
    Search the web using SERPEX API.

    This function queries the specified search engine and returns structured
    results containing titles, URLs, and snippets.

    Args:
        query: Search query string.
        num_results: Number of results to return (default: 10, max: 100).
        engine: Override default search engine. Options: 'auto', 'google',
            'bing', 'duckduckgo', 'brave', 'yahoo', 'yandex'.
        time_range: Filter results by time. Options: 'day', 'week',
            'month', 'year'.

    Returns:
        List of Document objects, one per search result.
        Each document contains the title, URL, and snippet in its text,
        with metadata including search details.

    Examples:
        >>> tool = SerpexToolSpec(api_key="your_key")
        >>> results = tool.search("LlamaIndex tutorial", num_results=5)
        >>> for doc in results:
        ...     print(f"Title: {doc.metadata['title']}")
        ...     print(f"URL: {doc.metadata['url']}")
        ...     print(doc.text)

        >>> # Search with specific engine
        >>> results = tool.search(
        ...     "privacy focused browser",
        ...     engine="duckduckgo",
        ...     num_results=5
        ... )

        >>> # Search with time filter
        >>> results = tool.search(
        ...     "AI news",
        ...     time_range="day",
        ...     num_results=10
        ... )
    """
    params: Dict[str, Any] = {
        "q": query,
        "engine": engine or self.engine,
        "category": "web",
    }

    if num_results:
        params["num"] = min(num_results, 100)  # Cap at 100

    if time_range:
        params["time_range"] = time_range

    try:
        response = requests.get(
            self.base_url,
            params=params,
            headers={
                "Authorization": f"Bearer {self.api_key}",
            },
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()

        # Extract results from the response
        results_list = data.get("results", [])

        if not results_list:
            return []

        # Get metadata
        api_metadata = data.get("metadata", {})
        num_results_total = api_metadata.get("number_of_results", 0)
        response_time = api_metadata.get("response_time", 0)

        # Create documents for each result
        documents = []
        for result in results_list[:num_results]:
            title = result.get("title", "No title")
            url = result.get("url", "")
            snippet = result.get("snippet", "No description available")

            text = f"{title}\nURL: {url}\n{snippet}"

            metadata = {
                "title": title,
                "url": url,
                "snippet": snippet,
                "number_of_results": num_results_total,
                "response_time": response_time,
                "query": query,
                "engine": engine or self.engine,
            }

            documents.append(Document(text=text, metadata=metadata))

        return documents

    except requests.exceptions.RequestException as e:
        raise e

```
 |  
| --- | --- |  
options: members: - SerpexToolSpec
