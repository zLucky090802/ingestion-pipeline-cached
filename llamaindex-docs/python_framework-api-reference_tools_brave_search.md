# Brave search
##  BraveSearchToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/brave_search/#llama_index.tools.brave_search.BraveSearchToolSpec "Permanent link")
Bases: 
Brave Search tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-brave-search/llama_index/tools/brave_search/base.py`  
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
```
 | 
```
classBraveSearchToolSpec(BaseToolSpec):
"""
    Brave Search tool spec.
    """

    spec_functions = ["brave_search"]

    def__init__(self, api_key: str) -> None:
"""
        Initialize with parameters.
        """
        self.api_key = api_key

    def_make_request(self, params: Dict) -> requests.Response:
"""
        Make a request to the Brave Search API.

        Args:
            params (dict): The parameters to be passed to the API.

        Returns:
            requests.Response: The response from the API.

        """
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key,
        }
        url = SEARCH_URL_TMPL.format(params=urllib.parse.urlencode(params))

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response

    defbrave_search(
        self, query: str, search_lang: str = "en", num_results: int = 5
    ) -> [Document]:
"""
        Make a query to the Brave Search engine to receive a list of results.

        Args:
            query (str): The query to be passed to Brave Search.
            search_lang (str): The search language preference (ISO 639-1), default is "en".
            num_results (int): The number of search results returned in response, default is 5.

        Returns:
            [Document]: A list of documents containing search results.

        """
        search_params = {
            "q": query,
            "search_lang": search_lang,
            "count": num_results,
        }

        response = self._make_request(search_params)
        return [Document(text=response.text)]

```
 |  
| --- | --- |  
###  brave_search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/brave_search/#llama_index.tools.brave_search.BraveSearchToolSpec.brave_search "Permanent link")

```
brave_search(
    query: ,
    search_lang:  = "en",
    num_results:  = 5,
) -> []

```

Make a query to the Brave Search engine to receive a list of results.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to be passed to Brave Search.  |  _required_  |  
|  `search_lang`  |  The search language preference (ISO 639-1), default is "en".  |  `'en'`  |  
|  `num_results`  |  The number of search results returned in response, default is 5.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  [Document]: A list of documents containing search results.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-brave-search/llama_index/tools/brave_search/base.py`  
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
defbrave_search(
    self, query: str, search_lang: str = "en", num_results: int = 5
) -> [Document]:
"""
    Make a query to the Brave Search engine to receive a list of results.

    Args:
        query (str): The query to be passed to Brave Search.
        search_lang (str): The search language preference (ISO 639-1), default is "en".
        num_results (int): The number of search results returned in response, default is 5.

    Returns:
        [Document]: A list of documents containing search results.

    """
    search_params = {
        "q": query,
        "search_lang": search_lang,
        "count": num_results,
    }

    response = self._make_request(search_params)
    return [Document(text=response.text)]

```
 |  
| --- | --- |  
options: members: - BraveSearchToolSpec
