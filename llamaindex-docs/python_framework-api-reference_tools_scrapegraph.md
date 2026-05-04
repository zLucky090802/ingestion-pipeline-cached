# Scrapegraph
##  ScrapegraphToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/scrapegraph/#llama_index.tools.scrapegraph.ScrapegraphToolSpec "Permanent link")
Bases: 
ScrapeGraph tool specification for web scraping operations.
This tool provides access to ScrapeGraph AI's web scraping capabilities, including smart scraping, content conversion to markdown, search functionality, and basic HTML scraping with various options.
Source code in `llama-index-integrations/tools/llama-index-tools-scrapegraph/llama_index/tools/scrapegraph/base.py`  
| 
```
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
```
 | 
```
classScrapegraphToolSpec(BaseToolSpec):
"""
    ScrapeGraph tool specification for web scraping operations.

    This tool provides access to ScrapeGraph AI's web scraping capabilities,
    including smart scraping, content conversion to markdown, search functionality,
    and basic HTML scraping with various options.
    """

    spec_functions = [
        "scrapegraph_smartscraper",
        "scrapegraph_markdownify",
        "scrapegraph_search",
        "scrapegraph_scrape",
        "scrapegraph_agentic_scraper",
    ]

    def__init__(self, api_key: Optional[str] = None) -> None:
"""
        Initialize the ScrapeGraph tool specification.

        Args:
            api_key (Optional[str]): ScrapeGraph API key. If not provided,
                                   will attempt to load from environment variable SGAI_API_KEY.

        """
        if api_key:
            self.client = Client(api_key=api_key)
        else:
            self.client = Client.from_env()

    defscrapegraph_smartscraper(
        self,
        prompt: str,
        url: str,
        schema: Optional[Union[List[BaseModel], Dict[str, Any]]] = None,
        **kwargs,
    ) -> Union[List[Dict], Dict]:
"""
        Perform intelligent web scraping using ScrapeGraph's SmartScraper.

        Args:
            prompt (str): User prompt describing what data to extract from the webpage
            url (str): Target website URL to scrape
            schema (Optional[Union[List[BaseModel], Dict]]): Pydantic models or dict defining output structure
            **kwargs: Additional parameters for the SmartScraper

        Returns:
            Union[List[Dict], Dict]: Scraped data matching the provided schema or prompt requirements

        """
        try:
            return self.client.smartscraper(
                website_url=url, user_prompt=prompt, output_schema=schema, **kwargs
            )
        except Exception as e:
            return {"error": f"SmartScraper failed: {e!s}"}

    defscrapegraph_markdownify(self, url: str, **kwargs) -> str:
"""
        Convert webpage content to markdown format using ScrapeGraph.

        Args:
            url (str): Target website URL to convert to markdown
            **kwargs: Additional parameters for the markdownify operation

        Returns:
            str: Markdown representation of the webpage content

        """
        try:
            return self.client.markdownify(website_url=url, **kwargs)
        except Exception as e:
            return f"Markdownify failed: {e!s}"

    defscrapegraph_search(
        self, query: str, max_results: Optional[int] = None, **kwargs
    ) -> str:
"""
        Perform a search query using ScrapeGraph's search functionality.

        Args:
            query (str): Search query to execute
            max_results (Optional[int]): Maximum number of search results to return
            **kwargs: Additional parameters for the search operation

        Returns:
            str: Search results from ScrapeGraph

        """
        try:
            search_params = {"query": query}
            if max_results:
                search_params["max_results"] = max_results
            search_params.update(kwargs)

            return self.client.search(**search_params)
        except Exception as e:
            return f"Search failed: {e!s}"

    defscrapegraph_scrape(
        self,
        url: str,
        render_heavy_js: bool = False,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
"""
        Perform basic HTML scraping using ScrapeGraph's scrape functionality.

        Args:
            url (str): Target website URL to scrape
            render_heavy_js (bool): Whether to enable JavaScript rendering for dynamic content
            headers (Optional[Dict[str, str]]): Custom HTTP headers to include in the request
            **kwargs: Additional parameters for the scrape operation

        Returns:
            Dict[str, Any]: Dictionary containing scraped HTML content and metadata

        """
        try:
            scrape_params = {"website_url": url, "render_heavy_js": render_heavy_js}
            if headers:
                scrape_params["headers"] = headers
            scrape_params.update(kwargs)

            return self.client.scrape(**scrape_params)
        except Exception as e:
            return {"error": f"Scrape failed: {e!s}"}

    defscrapegraph_agentic_scraper(
        self,
        prompt: str,
        url: str,
        schema: Optional[Union[List[BaseModel], Dict[str, Any]]] = None,
        **kwargs,
    ) -> Union[List[Dict], Dict]:
"""
        Perform agentic web scraping that can navigate and interact with websites.

        Args:
            prompt (str): User prompt describing the scraping task and navigation requirements
            url (str): Target website URL to start scraping from
            schema (Optional[Union[List[BaseModel], Dict]]): Pydantic models or dict defining output structure
            **kwargs: Additional parameters for the agentic scraper

        Returns:
            Union[List[Dict], Dict]: Scraped data from the agentic navigation and extraction

        """
        try:
            return self.client.agentic_scraper(
                website_url=url, user_prompt=prompt, output_schema=schema, **kwargs
            )
        except Exception as e:
            return {"error": f"Agentic scraper failed: {e!s}"}

```
 |  
| --- | --- |  
###  scrapegraph_smartscraper [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/scrapegraph/#llama_index.tools.scrapegraph.ScrapegraphToolSpec.scrapegraph_smartscraper "Permanent link")

```
scrapegraph_smartscraper(
    prompt: ,
    url: ,
    schema: Optional[
        Union[[BaseModel], [, ]]
    ] = None,
    **kwargs
) -> Union[[], ]

```

Perform intelligent web scraping using ScrapeGraph's SmartScraper.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  User prompt describing what data to extract from the webpage  |  _required_  |  
|  `url`  |  Target website URL to scrape  |  _required_  |  
|  `schema`  |  `Optional[Union[List[BaseModel], Dict]]`  |  Pydantic models or dict defining output structure  |  `None`  |  
|  `**kwargs`  |  Additional parameters for the SmartScraper  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Union[List[Dict], Dict]`  |  Union[List[Dict], Dict]: Scraped data matching the provided schema or prompt requirements  |  
Source code in `llama-index-integrations/tools/llama-index-tools-scrapegraph/llama_index/tools/scrapegraph/base.py`  
| 
```
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
```
 | 
```
defscrapegraph_smartscraper(
    self,
    prompt: str,
    url: str,
    schema: Optional[Union[List[BaseModel], Dict[str, Any]]] = None,
    **kwargs,
) -> Union[List[Dict], Dict]:
"""
    Perform intelligent web scraping using ScrapeGraph's SmartScraper.

    Args:
        prompt (str): User prompt describing what data to extract from the webpage
        url (str): Target website URL to scrape
        schema (Optional[Union[List[BaseModel], Dict]]): Pydantic models or dict defining output structure
        **kwargs: Additional parameters for the SmartScraper

    Returns:
        Union[List[Dict], Dict]: Scraped data matching the provided schema or prompt requirements

    """
    try:
        return self.client.smartscraper(
            website_url=url, user_prompt=prompt, output_schema=schema, **kwargs
        )
    except Exception as e:
        return {"error": f"SmartScraper failed: {e!s}"}

```
 |  
| --- | --- |  
###  scrapegraph_markdownify [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/scrapegraph/#llama_index.tools.scrapegraph.ScrapegraphToolSpec.scrapegraph_markdownify "Permanent link")

```
scrapegraph_markdownify(url: , **kwargs) -> 

```

Convert webpage content to markdown format using ScrapeGraph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  Target website URL to convert to markdown  |  _required_  |  
|  `**kwargs`  |  Additional parameters for the markdownify operation  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Markdown representation of the webpage content  |  
Source code in `llama-index-integrations/tools/llama-index-tools-scrapegraph/llama_index/tools/scrapegraph/base.py`  
| 
```
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
```
 | 
```
defscrapegraph_markdownify(self, url: str, **kwargs) -> str:
"""
    Convert webpage content to markdown format using ScrapeGraph.

    Args:
        url (str): Target website URL to convert to markdown
        **kwargs: Additional parameters for the markdownify operation

    Returns:
        str: Markdown representation of the webpage content

    """
    try:
        return self.client.markdownify(website_url=url, **kwargs)
    except Exception as e:
        return f"Markdownify failed: {e!s}"

```
 |  
| --- | --- |  
###  scrapegraph_search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/scrapegraph/#llama_index.tools.scrapegraph.ScrapegraphToolSpec.scrapegraph_search "Permanent link")

```
scrapegraph_search(
    query: , max_results: Optional[] = None, **kwargs
) -> 

```

Perform a search query using ScrapeGraph's search functionality.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Search query to execute  |  _required_  |  
|  `max_results`  |  `Optional[int]`  |  Maximum number of search results to return  |  `None`  |  
|  `**kwargs`  |  Additional parameters for the search operation  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Search results from ScrapeGraph  |  
Source code in `llama-index-integrations/tools/llama-index-tools-scrapegraph/llama_index/tools/scrapegraph/base.py`  
| 
```
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
```
 | 
```
defscrapegraph_search(
    self, query: str, max_results: Optional[int] = None, **kwargs
) -> str:
"""
    Perform a search query using ScrapeGraph's search functionality.

    Args:
        query (str): Search query to execute
        max_results (Optional[int]): Maximum number of search results to return
        **kwargs: Additional parameters for the search operation

    Returns:
        str: Search results from ScrapeGraph

    """
    try:
        search_params = {"query": query}
        if max_results:
            search_params["max_results"] = max_results
        search_params.update(kwargs)

        return self.client.search(**search_params)
    except Exception as e:
        return f"Search failed: {e!s}"

```
 |  
| --- | --- |  
###  scrapegraph_scrape [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/scrapegraph/#llama_index.tools.scrapegraph.ScrapegraphToolSpec.scrapegraph_scrape "Permanent link")

```
scrapegraph_scrape(
    url: ,
    render_heavy_js:  = False,
    headers: Optional[[, ]] = None,
    **kwargs
) -> [, ]

```

Perform basic HTML scraping using ScrapeGraph's scrape functionality.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  Target website URL to scrape  |  _required_  |  
|  `render_heavy_js`  |  `bool`  |  Whether to enable JavaScript rendering for dynamic content  |  `False`  |  
|  `headers`  |  `Optional[Dict[str, str]]`  |  Custom HTTP headers to include in the request  |  `None`  |  
|  `**kwargs`  |  Additional parameters for the scrape operation  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: Dictionary containing scraped HTML content and metadata  |  
Source code in `llama-index-integrations/tools/llama-index-tools-scrapegraph/llama_index/tools/scrapegraph/base.py`  
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
```
 | 
```
defscrapegraph_scrape(
    self,
    url: str,
    render_heavy_js: bool = False,
    headers: Optional[Dict[str, str]] = None,
    **kwargs,
) -> Dict[str, Any]:
"""
    Perform basic HTML scraping using ScrapeGraph's scrape functionality.

    Args:
        url (str): Target website URL to scrape
        render_heavy_js (bool): Whether to enable JavaScript rendering for dynamic content
        headers (Optional[Dict[str, str]]): Custom HTTP headers to include in the request
        **kwargs: Additional parameters for the scrape operation

    Returns:
        Dict[str, Any]: Dictionary containing scraped HTML content and metadata

    """
    try:
        scrape_params = {"website_url": url, "render_heavy_js": render_heavy_js}
        if headers:
            scrape_params["headers"] = headers
        scrape_params.update(kwargs)

        return self.client.scrape(**scrape_params)
    except Exception as e:
        return {"error": f"Scrape failed: {e!s}"}

```
 |  
| --- | --- |  
###  scrapegraph_agentic_scraper [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/scrapegraph/#llama_index.tools.scrapegraph.ScrapegraphToolSpec.scrapegraph_agentic_scraper "Permanent link")

```
scrapegraph_agentic_scraper(
    prompt: ,
    url: ,
    schema: Optional[
        Union[[BaseModel], [, ]]
    ] = None,
    **kwargs
) -> Union[[], ]

```

Perform agentic web scraping that can navigate and interact with websites.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  User prompt describing the scraping task and navigation requirements  |  _required_  |  
|  `url`  |  Target website URL to start scraping from  |  _required_  |  
|  `schema`  |  `Optional[Union[List[BaseModel], Dict]]`  |  Pydantic models or dict defining output structure  |  `None`  |  
|  `**kwargs`  |  Additional parameters for the agentic scraper  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Union[List[Dict], Dict]`  |  Union[List[Dict], Dict]: Scraped data from the agentic navigation and extraction  |  
Source code in `llama-index-integrations/tools/llama-index-tools-scrapegraph/llama_index/tools/scrapegraph/base.py`  
| 
```
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
```
 | 
```
defscrapegraph_agentic_scraper(
    self,
    prompt: str,
    url: str,
    schema: Optional[Union[List[BaseModel], Dict[str, Any]]] = None,
    **kwargs,
) -> Union[List[Dict], Dict]:
"""
    Perform agentic web scraping that can navigate and interact with websites.

    Args:
        prompt (str): User prompt describing the scraping task and navigation requirements
        url (str): Target website URL to start scraping from
        schema (Optional[Union[List[BaseModel], Dict]]): Pydantic models or dict defining output structure
        **kwargs: Additional parameters for the agentic scraper

    Returns:
        Union[List[Dict], Dict]: Scraped data from the agentic navigation and extraction

    """
    try:
        return self.client.agentic_scraper(
            website_url=url, user_prompt=prompt, output_schema=schema, **kwargs
        )
    except Exception as e:
        return {"error": f"Agentic scraper failed: {e!s}"}

```
 |  
| --- | --- |  
options: members: - ScrapegraphToolSpec
