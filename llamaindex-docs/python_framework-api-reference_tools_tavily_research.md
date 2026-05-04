# Tavily research
##  TavilyToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/tavily_research/#llama_index.tools.tavily_research.TavilyToolSpec "Permanent link")
Bases: 
Tavily tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-tavily-research/llama_index/tools/tavily_research/base.py`  
| 
```
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
```
 | 
```
classTavilyToolSpec(BaseToolSpec):
"""Tavily tool spec."""

    spec_functions = [
        "search",
        "extract",
    ]

    def__init__(self, api_key: str) -> None:
"""Initialize with parameters."""
        fromtavilyimport TavilyClient

        self.client = TavilyClient(api_key=api_key)

    defsearch(self, query: str, max_results: Optional[int] = 6) -> List[Document]:
"""
        Run query through Tavily Search and return metadata.

        Args:
            query: The query to search for.
            max_results: The maximum number of results to return.

        Returns:
            results: A list of dictionaries containing the results:
                url: The url of the result.
                content: The content of the result.

        """
        response = self.client.search(
            query, max_results=max_results, search_depth="advanced"
        )
        return [
            Document(text=result["content"], extra_info={"url": result["url"]})
            for result in response["results"]
        ]

    defextract(
        self,
        urls: List[str],
        include_images: bool = False,
        include_favicon: bool = False,
        extract_depth: str = "basic",
        format: str = "markdown",
    ) -> List[Document]:
"""
        Extract raw content from a URL using Tavily Extract API.

        Args:
            urls: The URL(s) to extract content from.
            include_images: Whether to include images in the response.
            include_favicon: Whether to include the favicon in the response.
            extract_depth: 'basic' or 'advanced' (default: 'basic').
            format: 'markdown' or 'text' (default: 'markdown').

        Returns:
            A list of Document objects containing the extracted content and metadata,
            or an empty list if no results were returned.

        """
        response = self.client.extract(
            urls,
            include_images=include_images,
            include_favicon=include_favicon,
            extract_depth=extract_depth,
            format=format,
        )

        results = response.get("results", [])

        if not results:
            return []

        return [
            Document(
                text=result.get("raw_content", ""),
                extra_info={
                    "url": result.get("url"),
                    "favicon": result.get("favicon"),
                    "images": result.get("images"),
                },
            )
            for result in results
        ]

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/tavily_research/#llama_index.tools.tavily_research.TavilyToolSpec.search "Permanent link")

```
search(
    query: , max_results: Optional[] = 6
) -> []

```

Run query through Tavily Search and return metadata.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to search for.  |  _required_  |  
|  `max_results`  |  `Optional[int]`  |  The maximum number of results to return.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `results`  |   |  A list of dictionaries containing the results: url: The url of the result. content: The content of the result.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-tavily-research/llama_index/tools/tavily_research/base.py`  
| 
```
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
```
 | 
```
defsearch(self, query: str, max_results: Optional[int] = 6) -> List[Document]:
"""
    Run query through Tavily Search and return metadata.

    Args:
        query: The query to search for.
        max_results: The maximum number of results to return.

    Returns:
        results: A list of dictionaries containing the results:
            url: The url of the result.
            content: The content of the result.

    """
    response = self.client.search(
        query, max_results=max_results, search_depth="advanced"
    )
    return [
        Document(text=result["content"], extra_info={"url": result["url"]})
        for result in response["results"]
    ]

```
 |  
| --- | --- |  
###  extract [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/tavily_research/#llama_index.tools.tavily_research.TavilyToolSpec.extract "Permanent link")

```
extract(
    urls: [],
    include_images:  = False,
    include_favicon:  = False,
    extract_depth:  = "basic",
    format:  = "markdown",
) -> []

```

Extract raw content from a URL using Tavily Extract API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  The URL(s) to extract content from.  |  _required_  |  
|  `include_images`  |  `bool`  |  Whether to include images in the response.  |  `False`  |  
|  `include_favicon`  |  `bool`  |  Whether to include the favicon in the response.  |  `False`  |  
|  `extract_depth`  |  'basic' or 'advanced' (default: 'basic').  |  `'basic'`  |  
|  `format`  |  'markdown' or 'text' (default: 'markdown').  |  `'markdown'`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  A list of Document objects containing the extracted content and metadata,  |  
|   |  or an empty list if no results were returned.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-tavily-research/llama_index/tools/tavily_research/base.py`  
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
```
 | 
```
defextract(
    self,
    urls: List[str],
    include_images: bool = False,
    include_favicon: bool = False,
    extract_depth: str = "basic",
    format: str = "markdown",
) -> List[Document]:
"""
    Extract raw content from a URL using Tavily Extract API.

    Args:
        urls: The URL(s) to extract content from.
        include_images: Whether to include images in the response.
        include_favicon: Whether to include the favicon in the response.
        extract_depth: 'basic' or 'advanced' (default: 'basic').
        format: 'markdown' or 'text' (default: 'markdown').

    Returns:
        A list of Document objects containing the extracted content and metadata,
        or an empty list if no results were returned.

    """
    response = self.client.extract(
        urls,
        include_images=include_images,
        include_favicon=include_favicon,
        extract_depth=extract_depth,
        format=format,
    )

    results = response.get("results", [])

    if not results:
        return []

    return [
        Document(
            text=result.get("raw_content", ""),
            extra_info={
                "url": result.get("url"),
                "favicon": result.get("favicon"),
                "images": result.get("images"),
            },
        )
        for result in results
    ]

```
 |  
| --- | --- |  
options: members: - TavilyToolSpec
