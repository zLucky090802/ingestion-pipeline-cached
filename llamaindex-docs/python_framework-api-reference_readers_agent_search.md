# Agent search
##  AgentSearchReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/agent_search/#llama_index.readers.agent_search.AgentSearchReader "Permanent link")
Bases: 
AgentSearch reader.
Source code in `llama-index-integrations/readers/llama-index-readers-agent-search/llama_index/readers/agent_search/base.py`  
| 
```
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
```
 | 
```
classAgentSearchReader(BaseReader):
"""AgentSearch reader."""

    def__init__(
        self,
        api_base: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
"""Initialize with parameters."""
        import_err_msg = (
            "`agent-search` package not found, please run `pip install agent-search`"
        )
        try:
            importagent_search  # noqa: F401
        except ImportError:
            raise ImportError(import_err_msg)

        fromagent_searchimport SciPhi

        self._client = SciPhi(api_base=api_base, api_key=api_key)

    defload_data(
        self,
        query: str,
        search_provider: str = "bing",
        llm_model: str = "SciPhi/Sensei-7B-V1",
    ) -> List[Document]:
"""
        Load data from AgentSearch, hosted by SciPhi.

        Args:
            collection_name (str): Name of the Milvus collection.
            query_vector (List[float]): Query vector.
            limit (int): Number of results to return.

        Returns:
            List[Document]: A list of documents.

        """
        rag_response = self._client.get_search_rag_response(
            query=query, search_provider=search_provider, llm_model=llm_model
        )
        return [Document(text=rag_response.pop("response"), metadata=rag_response)]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/agent_search/#llama_index.readers.agent_search.AgentSearchReader.load_data "Permanent link")

```
load_data(
    query: ,
    search_provider:  = "bing",
    llm_model:  = "SciPhi/Sensei-7B-V1",
) -> []

```

Load data from AgentSearch, hosted by SciPhi.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_name`  |  Name of the Milvus collection.  |  _required_  |  
|  `query_vector`  |  `List[float]`  |  Query vector.  |  _required_  |  
|  `limit`  |  Number of results to return.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-agent-search/llama_index/readers/agent_search/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    query: str,
    search_provider: str = "bing",
    llm_model: str = "SciPhi/Sensei-7B-V1",
) -> List[Document]:
"""
    Load data from AgentSearch, hosted by SciPhi.

    Args:
        collection_name (str): Name of the Milvus collection.
        query_vector (List[float]): Query vector.
        limit (int): Number of results to return.

    Returns:
        List[Document]: A list of documents.

    """
    rag_response = self._client.get_search_rag_response(
        query=query, search_provider=search_provider, llm_model=llm_model
    )
    return [Document(text=rag_response.pop("response"), metadata=rag_response)]

```
 |  
| --- | --- |  
options: members: - AgentSearchReader
