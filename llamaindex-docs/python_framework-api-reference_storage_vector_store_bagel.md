# Bagel
##  BagelVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bagel/#llama_index.vector_stores.bagel.BagelVectorStore "Permanent link")
Bases: 
Vector store for Bagel.
Examples:
`pip install llama-index-vector-stores-bagel`

```
fromllama_index.coreimport VectorStoreIndex, StorageContext
fromllama_index.vector_stores.bagelimport BagelVectorStore

importbagel
frombagelimport Settings

server_settings = Settings(
    bagel_api_impl="rest", bagel_server_host="api.bageldb.ai"
)

client = bagel.Client(server_settings)

collection = client.get_or_create_cluster("testing_embeddings")
vector_store = BagelVectorStore(collection=collection)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-bagel/llama_index/vector_stores/bagel/base.py`  
| 
```
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
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
```
 | 
```
classBagelVectorStore(BasePydanticVectorStore):
"""
    Vector store for Bagel.

    Examples:
        `pip install llama-index-vector-stores-bagel`

        ```python
        from llama_index.core import VectorStoreIndex, StorageContext
        from llama_index.vector_stores.bagel import BagelVectorStore

        import bagel
        from bagel import Settings

        server_settings = Settings(
            bagel_api_impl="rest", bagel_server_host="api.bageldb.ai"


        client = bagel.Client(server_settings)

        collection = client.get_or_create_cluster("testing_embeddings")
        vector_store = BagelVectorStore(collection=collection)
        ```

    """

    # support for Bagel specific parameters
    stores_text: bool = True
    flat_metadata: bool = True

    _collection: Any = PrivateAttr()

    def__init__(self, collection: Any, **kwargs: Any) -> None:
"""
        Initialize BagelVectorStore.

        Args:
            collection: Bagel collection.
            **kwargs: Additional arguments.

        """
        super().__init__()

        try:
            frombagel.api.Clusterimport Cluster
        except ImportError:
            raise ImportError("Bagel is not installed. Please install bagel.")

        if not isinstance(collection, Cluster):
            raise ValueError("Collection must be a bagel Cluster.")

        self._collection = collection

    @classmethod
    defclass_name(cls) -> str:
        return "BagelVectorStore"

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add a list of nodes with embeddings to the vector store.

        Args:
            nodes: List of nodes with embeddings.
            kwargs: Additional arguments.

        Returns:
            List of document ids.

        """
        if not self._collection:
            raise ValueError("collection not set")

        ids = []
        embeddings = []
        metadatas = []
        documents = []

        for node in nodes:
            ids.append(node.node_id)
            embeddings.append(node.get_embedding())
            metadatas.append(
                node_to_metadata_dict(
                    node,
                    remove_text=True,
                    flat_metadata=self.flat_metadata,
                )
            )
            documents.append(node.get_content(metadata_mode=MetadataMode.NONE) or "")

        self._collection.add(
            ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents
        )

        return ids

    defdelete(self, ref_doc_id: str, **kwargs: Any) -> None:
"""
        Delete a document from the vector store.

        Args:
            ref_doc_id: Reference document id.
            kwargs: Additional arguments.

        """
        if not self._collection:
            raise ValueError("collection not set")

        results = self._collection.get(where={"doc_id": ref_doc_id})
        if results and "ids" in results:
            self._collection.delete(ids=results["ids"])

    @property
    defclient(self) -> Any:
"""
        Get the Bagel cluster.
        """
        return self._collection

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query the vector store.

        Args:
            query: Query to run.
            kwargs: Additional arguments.

        Returns:
            Query result.

        """
        if not self._collection:
            raise ValueError("collection not set")

        if query.filters is not None:
            if "where" in kwargs:
                raise ValueError("Cannot specify both filters and where")
            where = _to_bagel_filter(query.filters)
        else:
            where = kwargs.get("where", {})

        results = self._collection.find(
            query_embeddings=query.query_embedding,
            where=where,
            n_results=query.similarity_top_k,
            **kwargs,
        )

        logger.debug(f"query results: {results}")

        nodes = []
        similarities = []
        ids = []

        for node_id, text, metadata, distance in zip(
            results["ids"][0],
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            try:
                node = metadata_dict_to_node(metadata)
                node.set_content(text)
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                metadata, node_info, relationships = legacy_metadata_dict_to_node(
                    metadata
                )

                node = TextNode(
                    text=text,
                    id_=node_id,
                    metadata=metadata,
                    start_char_idx=node_info.get("start", None),
                    end_char_idx=node_info.get("end", None),
                    relationships=relationships,
                )

            nodes.append(node)
            similarities.append(1.0 - math.exp(-distance))
            ids.append(node_id)

            logger.debug(f"node: {node}")
            logger.debug(f"similarity: {1.0-math.exp(-distance)}")
            logger.debug(f"id: {node_id}")

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bagel/#llama_index.vector_stores.bagel.BagelVectorStore.client "Permanent link")

```
client: 

```

Get the Bagel cluster.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bagel/#llama_index.vector_stores.bagel.BagelVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add a list of nodes with embeddings to the vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings.  |  _required_  |  
|  `kwargs`  |  Additional arguments.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List of document ids.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-bagel/llama_index/vector_stores/bagel/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add a list of nodes with embeddings to the vector store.

    Args:
        nodes: List of nodes with embeddings.
        kwargs: Additional arguments.

    Returns:
        List of document ids.

    """
    if not self._collection:
        raise ValueError("collection not set")

    ids = []
    embeddings = []
    metadatas = []
    documents = []

    for node in nodes:
        ids.append(node.node_id)
        embeddings.append(node.get_embedding())
        metadatas.append(
            node_to_metadata_dict(
                node,
                remove_text=True,
                flat_metadata=self.flat_metadata,
            )
        )
        documents.append(node.get_content(metadata_mode=MetadataMode.NONE) or "")

    self._collection.add(
        ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents
    )

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bagel/#llama_index.vector_stores.bagel.BagelVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **kwargs: ) -> None

```

Delete a document from the vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  Reference document id.  |  _required_  |  
|  `kwargs`  |  Additional arguments.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-bagel/llama_index/vector_stores/bagel/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **kwargs: Any) -> None:
"""
    Delete a document from the vector store.

    Args:
        ref_doc_id: Reference document id.
        kwargs: Additional arguments.

    """
    if not self._collection:
        raise ValueError("collection not set")

    results = self._collection.get(where={"doc_id": ref_doc_id})
    if results and "ids" in results:
        self._collection.delete(ids=results["ids"])

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bagel/#llama_index.vector_stores.bagel.BagelVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query the vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Query to run.  |  _required_  |  
|  `kwargs`  |  Additional arguments.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  Query result.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-bagel/llama_index/vector_stores/bagel/base.py`  
| 
```
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
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query the vector store.

    Args:
        query: Query to run.
        kwargs: Additional arguments.

    Returns:
        Query result.

    """
    if not self._collection:
        raise ValueError("collection not set")

    if query.filters is not None:
        if "where" in kwargs:
            raise ValueError("Cannot specify both filters and where")
        where = _to_bagel_filter(query.filters)
    else:
        where = kwargs.get("where", {})

    results = self._collection.find(
        query_embeddings=query.query_embedding,
        where=where,
        n_results=query.similarity_top_k,
        **kwargs,
    )

    logger.debug(f"query results: {results}")

    nodes = []
    similarities = []
    ids = []

    for node_id, text, metadata, distance in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        try:
            node = metadata_dict_to_node(metadata)
            node.set_content(text)
        except Exception:
            # NOTE: deprecated legacy logic for backward compatibility
            metadata, node_info, relationships = legacy_metadata_dict_to_node(
                metadata
            )

            node = TextNode(
                text=text,
                id_=node_id,
                metadata=metadata,
                start_char_idx=node_info.get("start", None),
                end_char_idx=node_info.get("end", None),
                relationships=relationships,
            )

        nodes.append(node)
        similarities.append(1.0 - math.exp(-distance))
        ids.append(node_id)

        logger.debug(f"node: {node}")
        logger.debug(f"similarity: {1.0-math.exp(-distance)}")
        logger.debug(f"id: {node_id}")

    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
options: members: - BagelVectorStore
