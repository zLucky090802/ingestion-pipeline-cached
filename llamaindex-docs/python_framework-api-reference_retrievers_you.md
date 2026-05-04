# You
##  YouRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/you/#llama_index.retrievers.you.YouRetriever "Permanent link")
Bases: 
Retriever for You.com's Search API (unified web and news search).
[API reference](https://docs.you.com/api-reference/search/v1-search)
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  `Optional[str]`  |  You.com API key, if `YDC_API_KEY` is not set in the environment  |  `None`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  Callback manager for instrumentation  |  `None`  |  
|  `count`  |  `Optional[int]`  |  Maximum number of search results to return per section (web/news), range 1-100, defaults to 10  |  `None`  |  
|  `safesearch`  |  `Optional[Literal['off', 'moderate', 'strict']]`  |  Safesearch settings, one of "off", "moderate", "strict"  |  `None`  |  
|  `country`  |  `Optional[str]`  |  Country code (ISO 3166-2), ex: 'US' for United States  |  `None`  |  
|  `language`  |  `Optional[str]`  |  Language of results in BCP 47 format, ex: 'en' for English, defaults to 'EN'  |  `None`  |  
|  `freshness`  |  `Optional[str]`  |  Recency of results - "day", "week", "month", "year", or custom range "YYYY-MM-DDtoYYYY-MM-DD"  |  `None`  |  
|  `offset`  |  `Optional[int]`  |  Offset for pagination (in multiples of count), range 0-9  |  `None`  |  
|  `livecrawl`  |  `Optional[Literal['web', 'news', 'all']]`  |  Which section(s) to live crawl - "web", "news", or "all"  |  `None`  |  
|  `livecrawl_formats`  |  `Optional[Literal['html', 'markdown']]`  |  Format of live-crawled content - "html" or "markdown"  |  `None`  |  
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-you/llama_index/retrievers/you/base.py`  
| 
```
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
176
177
178
179
180
181
182
```
 | 
```
classYouRetriever(BaseRetriever):
"""
    Retriever for You.com's Search API (unified web and news search).

    [API reference](https://docs.you.com/api-reference/search/v1-search)

    Args:
        api_key: You.com API key, if `YDC_API_KEY` is not set in the environment
        callback_manager: Callback manager for instrumentation
        count: Maximum number of search results to return per section (web/news), range 1-100, defaults to 10
        safesearch: Safesearch settings, one of "off", "moderate", "strict"
        country: Country code (ISO 3166-2), ex: 'US' for United States
        language: Language of results in BCP 47 format, ex: 'en' for English, defaults to 'EN'
        freshness: Recency of results - "day", "week", "month", "year", or custom range "YYYY-MM-DDtoYYYY-MM-DD"
        offset: Offset for pagination (in multiples of count), range 0-9
        livecrawl: Which section(s) to live crawl - "web", "news", or "all"
        livecrawl_formats: Format of live-crawled content - "html" or "markdown"

    """

    _api_key: str
    count: Optional[int]
    safesearch: Optional[Literal["off", "moderate", "strict"]]
    country: Optional[str]
    language: Optional[str]
    freshness: Optional[str]
    offset: Optional[int]
    livecrawl: Optional[Literal["web", "news", "all"]]
    livecrawl_formats: Optional[Literal["html", "markdown"]]

    def__init__(
        self,
        api_key: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        count: Optional[int] = None,
        safesearch: Optional[Literal["off", "moderate", "strict"]] = None,
        country: Optional[str] = None,
        language: Optional[str] = None,
        freshness: Optional[str] = None,
        offset: Optional[int] = None,
        livecrawl: Optional[Literal["web", "news", "all"]] = None,
        livecrawl_formats: Optional[Literal["html", "markdown"]] = None,
    ) -> None:
"""Initialize YouRetriever with API key and search parameters."""
        self._api_key = api_key or os.getenv("YDC_API_KEY") or ""
        if not self._api_key:
            raise ValueError(
                "You.com API key is required. Please provide it as an argument "
                "or set the YDC_API_KEY environment variable."
            )
        super().__init__(callback_manager)

        self.count = count
        self.safesearch = safesearch
        self.country = country
        self.language = language
        self.freshness = freshness
        self.offset = offset
        self.livecrawl = livecrawl
        self.livecrawl_formats = livecrawl_formats

    def_generate_params(self, query: str) -> Dict[str, Union[str, int]]:
"""Generate query parameters for the API request."""
        params: Dict[str, Any] = {
            "query": query,
            "count": self.count,
            "safesearch": self.safesearch,
            "country": self.country,
            "language": self.language,
            "freshness": self.freshness,
            "offset": self.offset,
            "livecrawl": self.livecrawl,
            "livecrawl_formats": self.livecrawl_formats,
        }

        # Remove `None` values
        return {k: v for k, v in params.items() if v is not None}

    def_process_result(self, result: Dict[str, Any], source_type: str) -> TextNode:
"""Process a single search result into a TextNode."""
        # Use snippets if available, fall back to description
        snippets = result.get("snippets", [])
        text = "\n".join(snippets) if snippets else result.get("description", "")

        metadata: Dict[str, Any] = {
            "url": result.get("url"),
            "title": result.get("title"),
            "description": result.get("description"),
            "page_age": result.get("page_age"),
            "thumbnail_url": result.get("thumbnail_url"),
            "favicon_url": result.get("favicon_url"),
            "authors": result.get("authors"),
            "source_type": source_type,
        }

        # Livecrawl content is additional full-page content when requested
        contents = result.get("contents") or {}
        if contents.get("markdown"):
            metadata["content_markdown"] = contents["markdown"]
        if contents.get("html"):
            metadata["content_html"] = contents["html"]

        return TextNode(
            text=text,
            metadata={k: v for k, v in metadata.items() if v is not None},
        )

    def_process_response(self, data: Dict[str, Any]) -> List[NodeWithScore]:
"""Process API response data into NodeWithScore list."""
        results = data.get("results", {})
        nodes: List[TextNode] = []

        # Process web results if present
        for hit in results.get("web", []):
            nodes.append(self._process_result(hit, "web"))

        # Process news results if present
        for article in results.get("news", []):
            nodes.append(self._process_result(article, "news"))

        return [NodeWithScore(node=node, score=1.0) for node in nodes]

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve nodes from You.com Search API."""
        headers = {"X-API-Key": self._api_key, "Accept": "application/json"}
        params = self._generate_params(query_bundle.query_str)

        try:
            with httpx.Client(timeout=_DEFAULT_TIMEOUT) as client:
                response = client.get(
                    _SEARCH_ENDPOINT,
                    params=params,
                    headers=headers,
                )
                response.raise_for_status()
                data = response.json()
        except httpx.TimeoutException as e:
            raise ValueError(f"You.com API request timed out: {e}") frome
        except httpx.HTTPStatusError as e:
            raise ValueError(f"You.com API request failed: {e}") frome
        except Exception as e:
            raise ValueError(f"You.com API request failed: {e}") frome

        return self._process_response(data)

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve nodes from You.com Search API asynchronously."""
        headers = {"X-API-Key": self._api_key, "Accept": "application/json"}
        params = self._generate_params(query_bundle.query_str)

        try:
            async with httpx.AsyncClient(timeout=_DEFAULT_TIMEOUT) as client:
                response = await client.get(
                    _SEARCH_ENDPOINT,
                    params=params,
                    headers=headers,
                )
                response.raise_for_status()
                data = response.json()
        except httpx.TimeoutException as e:
            raise ValueError(f"You.com API request timed out: {e}") frome
        except httpx.HTTPStatusError as e:
            raise ValueError(f"You.com API request failed: {e}") frome
        except Exception as e:
            raise ValueError(f"You.com API request failed: {e}") frome

        return self._process_response(data)

```
 |  
| --- | --- |  
options: members: - YouRetriever
