# Vector db
##  VectorDBToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/vector_db/#llama_index.tools.vector_db.VectorDBToolSpec "Permanent link")
Bases: 
Vector DB tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-vector-db/llama_index/tools/vector_db/base.py`  
| 
```
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
classVectorDBToolSpec(BaseToolSpec):
"""Vector DB tool spec."""

    spec_functions = ["auto_retrieve_fn"]

    def__init__(
        self,
        index: BaseIndex,  # TODO typing
    ) -> None:
"""Initialize with parameters."""
        self._index = index

    defauto_retrieve_fn(
        self,
        query: str,
        top_k: int,
        filter_key_list: List[str],
        filter_value_list: List[str],
    ) -> str:
"""
        Auto retrieval function.

        Performs auto-retrieval from a vector database, and then applies a set of filters.

        Args:
            query (str): The query to search
            top_k (int): The number of results to retrieve
            filter_key_list (List[str]): The list of filter keys
            filter_value_list (List[str]): The list of filter values

        """
        exact_match_filters = [
            ExactMatchFilter(key=k, value=v)
            for k, v in zip(filter_key_list, filter_value_list)
        ]
        retriever = VectorIndexRetriever(
            self._index,
            filters=MetadataFilters(filters=exact_match_filters),
            top_k=top_k,
        )
        query_engine = RetrieverQueryEngine.from_args(retriever)

        response = query_engine.query(query)
        return str(response)

```
 |  
| --- | --- |  
###  auto_retrieve_fn [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/vector_db/#llama_index.tools.vector_db.VectorDBToolSpec.auto_retrieve_fn "Permanent link")

```
auto_retrieve_fn(
    query: ,
    top_k: ,
    filter_key_list: [],
    filter_value_list: [],
) -> 

```

Auto retrieval function.
Performs auto-retrieval from a vector database, and then applies a set of filters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to search  |  _required_  |  
|  `top_k`  |  The number of results to retrieve  |  _required_  |  
|  `filter_key_list`  |  `List[str]`  |  The list of filter keys  |  _required_  |  
|  `filter_value_list`  |  `List[str]`  |  The list of filter values  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-vector-db/llama_index/tools/vector_db/base.py`  
| 
```
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
defauto_retrieve_fn(
    self,
    query: str,
    top_k: int,
    filter_key_list: List[str],
    filter_value_list: List[str],
) -> str:
"""
    Auto retrieval function.

    Performs auto-retrieval from a vector database, and then applies a set of filters.

    Args:
        query (str): The query to search
        top_k (int): The number of results to retrieve
        filter_key_list (List[str]): The list of filter keys
        filter_value_list (List[str]): The list of filter values

    """
    exact_match_filters = [
        ExactMatchFilter(key=k, value=v)
        for k, v in zip(filter_key_list, filter_value_list)
    ]
    retriever = VectorIndexRetriever(
        self._index,
        filters=MetadataFilters(filters=exact_match_filters),
        top_k=top_k,
    )
    query_engine = RetrieverQueryEngine.from_args(retriever)

    response = query_engine.query(query)
    return str(response)

```
 |  
| --- | --- |  
options: members: - VectorDBToolSpec
