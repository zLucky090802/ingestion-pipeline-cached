# Bing search
##  BingSearchToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/bing_search/#llama_index.tools.bing_search.BingSearchToolSpec "Permanent link")
Bases: 
Bing Search tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-bing-search/llama_index/tools/bing_search/base.py`  
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
```
 | 
```
classBingSearchToolSpec(BaseToolSpec):
"""Bing Search tool spec."""

    spec_functions = ["bing_news_search", "bing_image_search", "bing_video_search"]

    def__init__(
        self, api_key: str, lang: Optional[str] = "en-US", results: Optional[int] = 3
    ) -> None:
"""Initialize with parameters."""
        self.api_key = api_key
        self.lang = lang
        self.results = results

    def_bing_request(self, endpoint: str, query: str, keys: List[str]):
        response = requests.get(
            ENDPOINT_BASE_URL + endpoint,
            headers={"Ocp-Apim-Subscription-Key": self.api_key},
            params={"q": query, "mkt": self.lang, "count": self.results},
        )
        response_json = response.json()
        return [[result[key] for key in keys] for result in response_json["value"]]

    defbing_news_search(self, query: str):
"""
        Make a query to bing news search. Useful for finding news on a query.

        Args:
            query (str): The query to be passed to bing.

        """
        return self._bing_request("news/search", query, ["name", "description", "url"])

    defbing_image_search(self, query: str):
"""
        Make a query to bing images search. Useful for finding an image of a query.

        Args:
            query (str): The query to be passed to bing.

        returns a url of the images found

        """
        return self._bing_request("images/search", query, ["name", "contentUrl"])

    defbing_video_search(self, query: str):
"""
        Make a query to bing video search. Useful for finding a video related to a query.

        Args:
            query (str): The query to be passed to bing.

        """
        return self._bing_request("videos/search", query, ["name", "contentUrl"])

```
 |  
| --- | --- |  
###  bing_news_search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/bing_search/#llama_index.tools.bing_search.BingSearchToolSpec.bing_news_search "Permanent link")

```
bing_news_search(query: )

```

Make a query to bing news search. Useful for finding news on a query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to be passed to bing.  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-bing-search/llama_index/tools/bing_search/base.py`  
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
```
 | 
```
defbing_news_search(self, query: str):
"""
    Make a query to bing news search. Useful for finding news on a query.

    Args:
        query (str): The query to be passed to bing.

    """
    return self._bing_request("news/search", query, ["name", "description", "url"])

```
 |  
| --- | --- |  
###  bing_image_search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/bing_search/#llama_index.tools.bing_search.BingSearchToolSpec.bing_image_search "Permanent link")

```
bing_image_search(query: )

```

Make a query to bing images search. Useful for finding an image of a query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to be passed to bing.  |  _required_  |  
returns a url of the images found
Source code in `llama-index-integrations/tools/llama-index-tools-bing-search/llama_index/tools/bing_search/base.py`  
| 
```
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
```
 | 
```
defbing_image_search(self, query: str):
"""
    Make a query to bing images search. Useful for finding an image of a query.

    Args:
        query (str): The query to be passed to bing.

    returns a url of the images found

    """
    return self._bing_request("images/search", query, ["name", "contentUrl"])

```
 |  
| --- | --- |  
###  bing_video_search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/bing_search/#llama_index.tools.bing_search.BingSearchToolSpec.bing_video_search "Permanent link")

```
bing_video_search(query: )

```

Make a query to bing video search. Useful for finding a video related to a query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to be passed to bing.  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-bing-search/llama_index/tools/bing_search/base.py`  
| 
```
55
56
57
58
59
60
61
62
63
```
 | 
```
defbing_video_search(self, query: str):
"""
    Make a query to bing video search. Useful for finding a video related to a query.

    Args:
        query (str): The query to be passed to bing.

    """
    return self._bing_request("videos/search", query, ["name", "contentUrl"])

```
 |  
| --- | --- |  
options: members: - BingSearchToolSpec
