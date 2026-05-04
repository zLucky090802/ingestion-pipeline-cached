# Arxiv
##  ArxivToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/arxiv/#llama_index.tools.arxiv.ArxivToolSpec "Permanent link")
Bases: 
arXiv tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-arxiv/llama_index/tools/arxiv/base.py`  
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
```
 | 
```
classArxivToolSpec(BaseToolSpec):
"""arXiv tool spec."""

    spec_functions = ["arxiv_query"]

    def__init__(self, max_results: Optional[int] = 3):
        self.max_results = max_results

    defarxiv_query(self, query: str, sort_by: Optional[str] = "relevance"):
"""
        A tool to query arxiv.org
        ArXiv contains a variety of papers that are useful for answering
        mathematic and scientific questions.

        Args:
            query (str): The query to be passed to arXiv.
            sort_by (str): Either 'relevance' (default) or 'recent'

        """
        importarxiv

        sort = arxiv.SortCriterion.Relevance
        if sort_by == "recent":
            sort = arxiv.SortCriterion.SubmittedDate
        search = arxiv.Search(query, max_results=self.max_results, sort_by=sort)
        results = []
        for result in search.results():
            results.append(
                Document(text=f"{result.pdf_url}: {result.title}\n{result.summary}")
            )
        return results

```
 |  
| --- | --- |  
###  arxiv_query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/arxiv/#llama_index.tools.arxiv.ArxivToolSpec.arxiv_query "Permanent link")

```
arxiv_query(
    query: , sort_by: Optional[] = "relevance"
)

```

A tool to query arxiv.org ArXiv contains a variety of papers that are useful for answering mathematic and scientific questions.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to be passed to arXiv.  |  _required_  |  
|  `sort_by`  |  Either 'relevance' (default) or 'recent'  |  `'relevance'`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-arxiv/llama_index/tools/arxiv/base.py`  
| 
```
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
```
 | 
```
defarxiv_query(self, query: str, sort_by: Optional[str] = "relevance"):
"""
    A tool to query arxiv.org
    ArXiv contains a variety of papers that are useful for answering
    mathematic and scientific questions.

    Args:
        query (str): The query to be passed to arXiv.
        sort_by (str): Either 'relevance' (default) or 'recent'

    """
    importarxiv

    sort = arxiv.SortCriterion.Relevance
    if sort_by == "recent":
        sort = arxiv.SortCriterion.SubmittedDate
    search = arxiv.Search(query, max_results=self.max_results, sort_by=sort)
    results = []
    for result in search.results():
        results.append(
            Document(text=f"{result.pdf_url}: {result.title}\n{result.summary}")
        )
    return results

```
 |  
| --- | --- |  
options: members: - ArxivToolSpec
