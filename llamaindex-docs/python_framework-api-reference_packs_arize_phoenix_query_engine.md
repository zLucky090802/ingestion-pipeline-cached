# Arize phoenix query engine
##  ArizePhoenixQueryEnginePack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/arize_phoenix_query_engine/#llama_index.packs.arize_phoenix_query_engine.ArizePhoenixQueryEnginePack "Permanent link")
Bases: 
The Arize-Phoenix LlamaPack show how to instrument your LlamaIndex query engine with tracing. It launches Phoenix in the background, builds an index over an input list of nodes, and instantiates and instruments a query engine over that index so that trace data from each query is sent to Phoenix.
Note: Using this LlamaPack requires that your OpenAI API key is set via the OPENAI_API_KEY environment variable.
Source code in `llama-index-packs/llama-index-packs-arize-phoenix-query-engine/llama_index/packs/arize_phoenix_query_engine/base.py`  
| 
```
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
```
 | 
```
classArizePhoenixQueryEnginePack(BaseLlamaPack):
"""
    The Arize-Phoenix LlamaPack show how to instrument your LlamaIndex query
    engine with tracing. It launches Phoenix in the background, builds an index
    over an input list of nodes, and instantiates and instruments a query engine
    over that index so that trace data from each query is sent to Phoenix.

    Note: Using this LlamaPack requires that your OpenAI API key is set via the
    OPENAI_API_KEY environment variable.
    """

    def__init__(
        self,
        nodes: List[TextNode],
        **kwargs: Any,
    ) -> None:
"""
        Initializes a new instance of ArizePhoenixQueryEnginePack.

        Args:
            nodes (List[TextNode]): An input list of nodes over which the index
            will be built.

        """
        try:
            importphoenixaspx
        except ImportError:
            raise ImportError(
                "The arize-phoenix package could not be found. "
                "Please install with `pip install arize-phoenix`."
            )
        self._session: "PhoenixSession" = px.launch_app()
        set_global_handler("arize_phoenix")
        self._index = VectorStoreIndex(nodes, **kwargs)
        self._query_engine = self._index.as_query_engine()

    defget_modules(self) -> Dict[str, Any]:
"""
        Returns a dictionary containing the internals of the LlamaPack.

        Returns:
            Dict[str, Any]: A dictionary containing the internals of the
            LlamaPack.

        """
        return {
            "session": self._session,
            "session_url": self._session.url,
            "index": self._index,
            "query_engine": self._query_engine,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""
        Runs queries against the index.

        Returns:
            Any: A response from the query engine.

        """
        return self._query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/arize_phoenix_query_engine/#llama_index.packs.arize_phoenix_query_engine.ArizePhoenixQueryEnginePack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Returns a dictionary containing the internals of the LlamaPack.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: A dictionary containing the internals of the  |  
|  `Dict[str, Any]`  |  LlamaPack.  |  
Source code in `llama-index-packs/llama-index-packs-arize-phoenix-query-engine/llama_index/packs/arize_phoenix_query_engine/base.py`  
| 
```
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
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""
    Returns a dictionary containing the internals of the LlamaPack.

    Returns:
        Dict[str, Any]: A dictionary containing the internals of the
        LlamaPack.

    """
    return {
        "session": self._session,
        "session_url": self._session.url,
        "index": self._index,
        "query_engine": self._query_engine,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/arize_phoenix_query_engine/#llama_index.packs.arize_phoenix_query_engine.ArizePhoenixQueryEnginePack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Runs queries against the index.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Any`  |  A response from the query engine.  |  
Source code in `llama-index-packs/llama-index-packs-arize-phoenix-query-engine/llama_index/packs/arize_phoenix_query_engine/base.py`  
| 
```
68
69
70
71
72
73
74
75
76
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""
    Runs queries against the index.

    Returns:
        Any: A response from the query engine.

    """
    return self._query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - ArizePhoenixQueryEnginePack
