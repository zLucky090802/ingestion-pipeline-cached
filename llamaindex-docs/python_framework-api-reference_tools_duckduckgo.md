# Duckduckgo
##  DuckDuckGoSearchToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/duckduckgo/#llama_index.tools.duckduckgo.DuckDuckGoSearchToolSpec "Permanent link")
Bases: 
DuckDuckGoSearch tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-duckduckgo/llama_index/tools/duckduckgo/base.py`  
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
```
 | 
```
classDuckDuckGoSearchToolSpec(BaseToolSpec):
"""DuckDuckGoSearch tool spec."""

    spec_functions = ["duckduckgo_instant_search", "duckduckgo_full_search"]

    def__init__(self) -> None:
        if not importlib.util.find_spec("duckduckgo_search"):
            raise ImportError(
                "DuckDuckGoSearchToolSpec requires the duckduckgo_search package to be installed."
            )
        super().__init__()

    defduckduckgo_instant_search(self, query: str) -> List[Dict]:
"""
        Make a query to DuckDuckGo api to receive an instant answer.

        Args:
            query (str): The query to be passed to DuckDuckGo.

        """
        fromduckduckgo_searchimport DDGS

        with DDGS() as ddg:
            return list(ddg.answers(query))

    defduckduckgo_full_search(
        self,
        query: str,
        region: Optional[str] = "wt-wt",
        max_results: Optional[int] = 10,
    ) -> List[Dict]:
"""
        Make a query to DuckDuckGo search to receive a full search results.

        Args:
            query (str): The query to be passed to DuckDuckGo.
            region (Optional[str]): The region to be used for the search in [country-language] convention, ex us-en, uk-en, ru-ru, etc...
            max_results (Optional[int]): The maximum number of results to be returned.

        """
        fromduckduckgo_searchimport DDGS

        params = {
            "keywords": query,
            "region": region,
            "max_results": max_results,
        }

        with DDGS() as ddg:
            return list(ddg.text(**params))

```
 |  
| --- | --- |  
###  duckduckgo_instant_search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/duckduckgo/#llama_index.tools.duckduckgo.DuckDuckGoSearchToolSpec.duckduckgo_instant_search "Permanent link")

```
duckduckgo_instant_search(query: ) -> []

```

Make a query to DuckDuckGo api to receive an instant answer.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to be passed to DuckDuckGo.  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-duckduckgo/llama_index/tools/duckduckgo/base.py`  
| 
```
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
```
 | 
```
defduckduckgo_instant_search(self, query: str) -> List[Dict]:
"""
    Make a query to DuckDuckGo api to receive an instant answer.

    Args:
        query (str): The query to be passed to DuckDuckGo.

    """
    fromduckduckgo_searchimport DDGS

    with DDGS() as ddg:
        return list(ddg.answers(query))

```
 |  
| --- | --- |  
###  duckduckgo_full_search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/duckduckgo/#llama_index.tools.duckduckgo.DuckDuckGoSearchToolSpec.duckduckgo_full_search "Permanent link")

```
duckduckgo_full_search(
    query: ,
    region: Optional[] = "wt-wt",
    max_results: Optional[] = 10,
) -> []

```

Make a query to DuckDuckGo search to receive a full search results.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to be passed to DuckDuckGo.  |  _required_  |  
|  `region`  |  `Optional[str]`  |  The region to be used for the search in [country-language] convention, ex us-en, uk-en, ru-ru, etc...  |  `'wt-wt'`  |  
|  `max_results`  |  `Optional[int]`  |  The maximum number of results to be returned.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-duckduckgo/llama_index/tools/duckduckgo/base.py`  
| 
```
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
```
 | 
```
defduckduckgo_full_search(
    self,
    query: str,
    region: Optional[str] = "wt-wt",
    max_results: Optional[int] = 10,
) -> List[Dict]:
"""
    Make a query to DuckDuckGo search to receive a full search results.

    Args:
        query (str): The query to be passed to DuckDuckGo.
        region (Optional[str]): The region to be used for the search in [country-language] convention, ex us-en, uk-en, ru-ru, etc...
        max_results (Optional[int]): The maximum number of results to be returned.

    """
    fromduckduckgo_searchimport DDGS

    params = {
        "keywords": query,
        "region": region,
        "max_results": max_results,
    }

    with DDGS() as ddg:
        return list(ddg.text(**params))

```
 |  
| --- | --- |  
options: members: - DuckDuckGoSearchToolSpec
