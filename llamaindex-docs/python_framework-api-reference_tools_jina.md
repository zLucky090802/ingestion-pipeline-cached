# Jina
##  JinaToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jina/#llama_index.tools.jina.JinaToolSpec "Permanent link")
Bases: 
Jina tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-jina/llama_index/tools/jina/base.py`  
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
```
 | 
```
classJinaToolSpec(BaseToolSpec):
"""
    Jina tool spec.
    """

    spec_functions = ["jina_search"]

    def_make_request(self, params: Dict) -> requests.Response:
"""
        Make a request to the Jina Search API.

        Args:
            params (dict): The parameters to be passed to the API.

        Returns:
            requests.Response: The response from the API.

        """
        headers = {
            "Accept": "application/json",
        }
        url = str(URL(JINA_SEARCH_URL_ENDPOINT + params.get("query")))
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    defjina_search(self, query: str) -> List[Document]:
"""
        Make a query to the Jina Search engine to receive a list of results.

        Args:
            query (str): The query to be passed to Jina Search.

        Returns:
            [Document]: A list of documents containing search results.

        """
        search_params = {
            "query": query,
        }
        response = self._make_request(search_params)
        return [
            Document(
                text=result["content"],
                extra_info={
                    "url": result["url"],
                    "title": result["title"],
                    "description": result["description"],
                },
            )
            for result in response["data"]
        ]

```
 |  
| --- | --- |  
###  jina_search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jina/#llama_index.tools.jina.JinaToolSpec.jina_search "Permanent link")

```
jina_search(query: ) -> []

```

Make a query to the Jina Search engine to receive a list of results.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to be passed to Jina Search.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  [Document]: A list of documents containing search results.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-jina/llama_index/tools/jina/base.py`  
| 
```
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
```
 | 
```
defjina_search(self, query: str) -> List[Document]:
"""
    Make a query to the Jina Search engine to receive a list of results.

    Args:
        query (str): The query to be passed to Jina Search.

    Returns:
        [Document]: A list of documents containing search results.

    """
    search_params = {
        "query": query,
    }
    response = self._make_request(search_params)
    return [
        Document(
            text=result["content"],
            extra_info={
                "url": result["url"],
                "title": result["title"],
                "description": result["description"],
            },
        )
        for result in response["data"]
    ]

```
 |  
| --- | --- |  
options: members: - JinaToolSpec
