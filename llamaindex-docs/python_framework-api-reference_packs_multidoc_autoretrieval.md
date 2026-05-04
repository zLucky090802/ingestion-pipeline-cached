# Multidoc autoretrieval
##  MultiDocAutoRetrieverPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/multidoc_autoretrieval/#llama_index.packs.multidoc_autoretrieval.MultiDocAutoRetrieverPack "Permanent link")
Bases: 
Multi-doc auto-retriever pack.
Uses weaviate as the underlying storage.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `docs`  |   |  A list of documents to index.  |  _required_  |  
|  `**kwargs`  |  Keyword arguments to pass to the underlying index.  |  _required_  |  
Source code in `llama-index-packs/llama-index-packs-multidoc-autoretrieval/llama_index/packs/multidoc_autoretrieval/base.py`  
| 
```
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
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
```
 | 
```
classMultiDocAutoRetrieverPack(BaseLlamaPack):
"""
    Multi-doc auto-retriever pack.

    Uses weaviate as the underlying storage.

    Args:
        docs (List[Document]): A list of documents to index.
        **kwargs: Keyword arguments to pass to the underlying index.

    """

    def__init__(
        self,
        weaviate_client: Any,
        doc_metadata_index_name: str,
        doc_chunks_index_name: str,
        metadata_nodes: List[BaseNode],
        docs: List[Document],
        doc_metadata_schema: VectorStoreInfo,
        auto_retriever_kwargs: Optional[Dict[str, Any]] = None,
        verbose: bool = False,
    ) -> None:
"""Init params."""
        importweaviate

        # do some validation
        if len(docs) != len(metadata_nodes):
            raise ValueError(
                "The number of metadata nodes must match the number of documents."
            )

        # authenticate
        client = cast(weaviate.Client, weaviate_client)
        # auth_config = weaviate.AuthApiKey(api_key="")
        # client = weaviate.Client(
        #     "https://<weaviate-cluster>.weaviate.network",
        #     auth_client_secret=auth_config,
        # )

        # initialize two vector store classes corresponding to the two index names
        metadata_store = WeaviateVectorStore(
            weaviate_client=client, index_name=doc_metadata_index_name
        )
        metadata_sc = StorageContext.from_defaults(vector_store=metadata_store)
        # index VectorStoreIndex
        # Since "new_docs" are concise summaries, we can directly feed them as nodes into VectorStoreIndex
        index = VectorStoreIndex(metadata_nodes, storage_context=metadata_sc)
        if verbose:
            print("Indexed metadata nodes.")

        # construct separate Weaviate Index with original docs. Define a separate query engine with query engine mapping to each doc id.
        chunks_store = WeaviateVectorStore(
            weaviate_client=client, index_name=doc_chunks_index_name
        )
        chunks_sc = StorageContext.from_defaults(vector_store=chunks_store)
        doc_index = VectorStoreIndex.from_documents(docs, storage_context=chunks_sc)
        if verbose:
            print("Indexed source document nodes.")

        # setup auto retriever
        auto_retriever = VectorIndexAutoRetriever(
            index,
            vector_store_info=doc_metadata_schema,
            **(auto_retriever_kwargs or {}),
        )
        self.index_auto_retriever = IndexAutoRetriever(retriever=auto_retriever)
        if verbose:
            print("Setup autoretriever over metadata.")

        # define per-document retriever
        self.retriever_dict = {}
        for doc in docs:
            index_id = doc.metadata["index_id"]
            # filter for the specific doc id
            filters = MetadataFilters(
                filters=[
                    MetadataFilter(
                        key="index_id", operator=FilterOperator.EQ, value=index_id
                    ),
                ]
            )
            retriever = doc_index.as_retriever(filters=filters)

            self.retriever_dict[index_id] = retriever

        if verbose:
            print("Setup per-document retriever.")

        # setup recursive retriever
        self.recursive_retriever = RecursiveRetriever(
            "vector",
            retriever_dict={"vector": self.index_auto_retriever, **self.retriever_dict},
            verbose=True,
        )
        if verbose:
            print("Setup recursive retriever.")

        # plug into query engine
        llm = OpenAI(model="gpt-3.5-turbo")
        self.query_engine = RetrieverQueryEngine.from_args(
            self.recursive_retriever, llm=llm
        )

    defget_modules(self) -> Dict[str, Any]:
"""
        Returns a dictionary containing the internals of the LlamaPack.

        Returns:
            Dict[str, Any]: A dictionary containing the internals of the
            LlamaPack.

        """
        return {
            "index_auto_retriever": self.index_auto_retriever,
            "retriever_dict": self.retriever_dict,
            "recursive_retriever": self.recursive_retriever,
            "query_engine": self.query_engine,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""
        Runs queries against the index.

        Returns:
            Any: A response from the query engine.

        """
        return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/multidoc_autoretrieval/#llama_index.packs.multidoc_autoretrieval.MultiDocAutoRetrieverPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Returns a dictionary containing the internals of the LlamaPack.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: A dictionary containing the internals of the  |  
|  `Dict[str, Any]`  |  LlamaPack.  |  
Source code in `llama-index-packs/llama-index-packs-multidoc-autoretrieval/llama_index/packs/multidoc_autoretrieval/base.py`  
| 
```
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
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
        "index_auto_retriever": self.index_auto_retriever,
        "retriever_dict": self.retriever_dict,
        "recursive_retriever": self.recursive_retriever,
        "query_engine": self.query_engine,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/multidoc_autoretrieval/#llama_index.packs.multidoc_autoretrieval.MultiDocAutoRetrieverPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Runs queries against the index.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Any`  |  A response from the query engine.  |  
Source code in `llama-index-packs/llama-index-packs-multidoc-autoretrieval/llama_index/packs/multidoc_autoretrieval/base.py`  
| 
```
174
175
176
177
178
179
180
181
182
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""
    Runs queries against the index.

    Returns:
        Any: A response from the query engine.

    """
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - MultiDocAutoRetrieverPack
