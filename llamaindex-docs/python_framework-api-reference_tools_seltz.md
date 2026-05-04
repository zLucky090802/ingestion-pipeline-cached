# Seltz
##  SeltzToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/seltz/#llama_index.tools.seltz.SeltzToolSpec "Permanent link")
Bases: 
Seltz web knowledge tool spec.
Seltz provides fast, up-to-date web data with context-engineered web content and sources for real-time AI reasoning.
Source code in `llama-index-integrations/tools/llama-index-tools-seltz/llama_index/tools/seltz/base.py`  
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
```
 | 
```
classSeltzToolSpec(BaseToolSpec):
"""
    Seltz web knowledge tool spec.

    Seltz provides fast, up-to-date web data with context-engineered
    web content and sources for real-time AI reasoning.
    """

    spec_functions = ["search"]

    def__init__(self, api_key: str) -> None:
"""
        Initialize with parameters.

        Args:
            api_key: Seltz API key. Obtain one at https://www.seltz.ai/

        """
        self.client = Seltz(api_key=api_key)

    defsearch(
        self,
        query: str,
        max_documents: Optional[int] = 10,
        context: Optional[str] = None,
        profile: Optional[str] = None,
    ) -> List[Document]:
"""
        Search the web using Seltz and return relevant documents with sources.

        Args:
            query: The search query text.
            max_documents: Maximum number of documents to return (default: 10).
            context: Optional context to refine search results.
            profile: Optional profile to customize search behavior.

        Returns:
            A list of Document objects containing web content and source URLs.

        """
        includes = Includes(max_documents=max_documents) if max_documents else None
        response = self.client.search(
            query, includes=includes, context=context, profile=profile
        )
        return [
            Document(text=doc.content or "", metadata={"url": doc.url or ""})
            for doc in response.documents
        ]

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/seltz/#llama_index.tools.seltz.SeltzToolSpec.search "Permanent link")

```
search(
    query: ,
    max_documents: Optional[] = 10,
    context: Optional[] = None,
    profile: Optional[] = None,
) -> []

```

Search the web using Seltz and return relevant documents with sources.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The search query text.  |  _required_  |  
|  `max_documents`  |  `Optional[int]`  |  Maximum number of documents to return (default: 10).  |  
|  `context`  |  `Optional[str]`  |  Optional context to refine search results.  |  `None`  |  
|  `profile`  |  `Optional[str]`  |  Optional profile to customize search behavior.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  A list of Document objects containing web content and source URLs.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-seltz/llama_index/tools/seltz/base.py`  
| 
```
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
```
 | 
```
defsearch(
    self,
    query: str,
    max_documents: Optional[int] = 10,
    context: Optional[str] = None,
    profile: Optional[str] = None,
) -> List[Document]:
"""
    Search the web using Seltz and return relevant documents with sources.

    Args:
        query: The search query text.
        max_documents: Maximum number of documents to return (default: 10).
        context: Optional context to refine search results.
        profile: Optional profile to customize search behavior.

    Returns:
        A list of Document objects containing web content and source URLs.

    """
    includes = Includes(max_documents=max_documents) if max_documents else None
    response = self.client.search(
        query, includes=includes, context=context, profile=profile
    )
    return [
        Document(text=doc.content or "", metadata={"url": doc.url or ""})
        for doc in response.documents
    ]

```
 |  
| --- | --- |  
options: members: - SeltzToolSpec
