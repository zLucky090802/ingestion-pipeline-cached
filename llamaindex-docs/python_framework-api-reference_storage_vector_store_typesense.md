# Typesense
##  TypesenseVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/typesense/#llama_index.vector_stores.typesense.TypesenseVectorStore "Permanent link")
Bases: 
Typesense Vector Store.
In this vector store, embeddings and docs are stored within a Typesense index.
During query time, the index uses Typesense to query for the top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `client`  |  Typesense client  |  _required_  |  
|  `tokenizer`  |  `Optional[Callable[[str], List]]`  |  tokenizer function.  |  `None`  |  
Examples:
`pip install llama-index-vector-stores-typesense`

```
fromllama_index.vector_stores.typesenseimport TypesenseVectorStore
fromtypesenseimport Client

# Sign up for Typesense and get your API key
typesense_client = Client(
    {
        "api_key": "your_api_key_here",
        "nodes": [{"host": "localhost", "port": "8108", "protocol": "http"}],
        "connection_timeout_seconds": 2,
    }
)

# Create an instance of TypesenseVectorStore
vector_store = TypesenseVectorStore(typesense_client)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-typesense/llama_index/vector_stores/typesense/base.py`  
| 
```
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
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
```
 | 
```
classTypesenseVectorStore(BasePydanticVectorStore):
"""
    Typesense Vector Store.

    In this vector store, embeddings and docs are stored within a
    Typesense index.

    During query time, the index uses Typesense to query for the top
    k most similar nodes.

    Args:
        client (Any): Typesense client
        tokenizer (Optional[Callable[[str], List]]): tokenizer function.

    Examples:
        `pip install llama-index-vector-stores-typesense`

        ```python
        from llama_index.vector_stores.typesense import TypesenseVectorStore
        from typesense import Client

        # Sign up for Typesense and get your API key
        typesense_client = Client(

                "api_key": "your_api_key_here",
                "nodes": [{"host": "localhost", "port": "8108", "protocol": "http"}],
                "connection_timeout_seconds": 2,



        # Create an instance of TypesenseVectorStore
        vector_store = TypesenseVectorStore(typesense_client)
        ```

    """

    stores_text: bool = True
    is_embedding_query: bool = False
    flat_metadata: bool = False

    _tokenizer: Callable[[str], List] = PrivateAttr()
    _text_key: str = PrivateAttr()
    _collection_name: str = PrivateAttr()
    _collection: Any = PrivateAttr()
    _batch_size: int = PrivateAttr()
    _metadata_key: str = PrivateAttr()
    _client: typesense.Client = PrivateAttr()

    def__init__(
        self,
        client: Any,
        tokenizer: Optional[Callable[[str], List]] = None,
        text_key: str = DEFAULT_TEXT_KEY,
        collection_name: str = DEFAULT_COLLECTION_NAME,
        batch_size: int = DEFAULT_BATCH_SIZE,
        metadata_key: str = DEFAULT_METADATA_KEY,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        super().__init__()

        if client is not None:
            if not isinstance(client, typesense.Client):
                raise ValueError(
                    f"client should be an instance of typesense.Client, "
                    f"got {type(client)}"
                )
            self._client = cast(typesense.Client, client)
        self._tokenizer = tokenizer or get_tokenizer()
        self._text_key = text_key
        self._collection_name = collection_name
        self._collection = self._client.collections[self._collection_name]
        self._batch_size = batch_size
        self._metadata_key = metadata_key

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "TypesenseVectorStore"

    @property
    defclient(self) -> Any:
"""Return Typesense client."""
        return self._client

    @property
    defcollection(self) -> Any:
"""Return Typesense collection."""
        return self._collection

    def_create_collection(self, num_dim: int) -> None:
        fields = [
            {"name": "vec", "type": "float[]", "num_dim": num_dim},
            {"name": f"{self._text_key}", "type": "string"},
            {"name": ".*", "type": "auto"},
        ]
        self._client.collections.create(
            {"name": self._collection_name, "fields": fields}
        )

    def_create_upsert_docs(self, nodes: List[BaseNode]) -> List[dict]:
        upsert_docs = []
        for node in nodes:
            doc = {
                "id": node.node_id,
                "vec": node.get_embedding(),
                f"{self._text_key}": node.get_content(metadata_mode=MetadataMode.NONE),
                "ref_doc_id": node.ref_doc_id,
                f"{self._metadata_key}": node_to_metadata_dict(
                    node, remove_text=True, flat_metadata=self.flat_metadata
                ),
            }
            upsert_docs.append(doc)

        return upsert_docs

    @staticmethod
    def_to_typesense_filter(standard_filters: MetadataFilters) -> str:
"""Convert from standard dataclass to typesense filter dict."""
        for filter in standard_filters.legacy_filters():
            if filter.key == "filter_by":
                return str(filter.value)

        return ""

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        docs = self._create_upsert_docs(nodes)

        try:
            collection = cast(Collection, self.collection)
            collection.documents.import_(
                docs, {"action": "upsert"}, batch_size=self._batch_size
            )
        except ObjectNotFound:
            # Create the collection if it doesn't already exist
            num_dim = len(nodes[0].get_embedding())
            self._create_collection(num_dim)
            collection.documents.import_(
                docs, {"action": "upsert"}, batch_size=self._batch_size
            )

        return [node.node_id for node in nodes]

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        collection = cast(Collection, self.collection)
        collection.documents.delete({"filter_by": f"ref_doc_id:={ref_doc_id}"})

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query Typesense index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): Vector store query object.

        """
        if query.filters:
            typesense_filter = self._to_typesense_filter(query.filters)
        else:
            typesense_filter = ""

        if query.mode is not VectorStoreQueryMode.TEXT_SEARCH:
            if query.query_embedding:
                embedded_query = [str(x) for x in query.query_embedding]
                search_requests = {
                    "searches": [
                        {
                            "collection": self._collection_name,
                            "q": "*",
                            "vector_query": f"vec:([{','.join(embedded_query)}],"
                            + f"k:{query.similarity_top_k})",
                            "filter_by": typesense_filter,
                        }
                    ]
                }
            else:
                raise ValueError("Vector search requires a query embedding")
        if query.mode is VectorStoreQueryMode.TEXT_SEARCH:
            if query.query_str:
                search_requests = {
                    "searches": [
                        {
                            "collection": self._collection_name,
                            "q": query.query_str,
                            "query_by": self._text_key,
                            "filter_by": typesense_filter,
                        }
                    ]
                }
            else:
                raise ValueError("Text search requires a query string")
        response = self._client.multi_search.perform(search_requests, {})

        top_k_nodes = []
        top_k_ids = []
        top_k_scores = None
        if query.mode is not VectorStoreQueryMode.TEXT_SEARCH:
            top_k_scores = []

        for hit in response["results"][0]["hits"]:
            document = hit["document"]
            id = document["id"]
            text = document[self._text_key]

            # Note that typesense distances range from 0 to 2, \
            # where 0 is most similar and 2 is most dissimilar
            if query.mode is not VectorStoreQueryMode.TEXT_SEARCH:
                score = hit["vector_distance"]

            try:
                node = metadata_dict_to_node(document[self._metadata_key])
                node.text = text
            except Exception:
                extra_info, node_info, relationships = legacy_metadata_dict_to_node(
                    document[self._metadata_key], text_key=self._text_key
                )
                node = TextNode(
                    text=text,
                    id_=id,
                    metadata=extra_info,
                    start_chart_idx=node_info.get("start", None),
                    end_chart_idx=node_info.get("end", None),
                    relationships=relationships,
                )

            top_k_ids.append(id)
            top_k_nodes.append(node)
            if query.mode is not VectorStoreQueryMode.TEXT_SEARCH:
                top_k_scores.append(score)

        return VectorStoreQueryResult(
            nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
        )

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/typesense/#llama_index.vector_stores.typesense.TypesenseVectorStore.client "Permanent link")

```
client: 

```

Return Typesense client.
###  collection `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/typesense/#llama_index.vector_stores.typesense.TypesenseVectorStore.collection "Permanent link")

```
collection: 

```

Return Typesense collection.
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/typesense/#llama_index.vector_stores.typesense.TypesenseVectorStore.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-typesense/llama_index/vector_stores/typesense/base.py`  
| 
```
114
115
116
117
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "TypesenseVectorStore"

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/typesense/#llama_index.vector_stores.typesense.TypesenseVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-typesense/llama_index/vector_stores/typesense/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    """
    docs = self._create_upsert_docs(nodes)

    try:
        collection = cast(Collection, self.collection)
        collection.documents.import_(
            docs, {"action": "upsert"}, batch_size=self._batch_size
        )
    except ObjectNotFound:
        # Create the collection if it doesn't already exist
        num_dim = len(nodes[0].get_embedding())
        self._create_collection(num_dim)
        collection.documents.import_(
            docs, {"action": "upsert"}, batch_size=self._batch_size
        )

    return [node.node_id for node in nodes]

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/typesense/#llama_index.vector_stores.typesense.TypesenseVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-typesense/llama_index/vector_stores/typesense/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    collection = cast(Collection, self.collection)
    collection.documents.delete({"filter_by": f"ref_doc_id:={ref_doc_id}"})

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/typesense/#llama_index.vector_stores.typesense.TypesenseVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query Typesense index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Vector store query object.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-typesense/llama_index/vector_stores/typesense/base.py`  
| 
```
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
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query Typesense index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): Vector store query object.

    """
    if query.filters:
        typesense_filter = self._to_typesense_filter(query.filters)
    else:
        typesense_filter = ""

    if query.mode is not VectorStoreQueryMode.TEXT_SEARCH:
        if query.query_embedding:
            embedded_query = [str(x) for x in query.query_embedding]
            search_requests = {
                "searches": [
                    {
                        "collection": self._collection_name,
                        "q": "*",
                        "vector_query": f"vec:([{','.join(embedded_query)}],"
                        + f"k:{query.similarity_top_k})",
                        "filter_by": typesense_filter,
                    }
                ]
            }
        else:
            raise ValueError("Vector search requires a query embedding")
    if query.mode is VectorStoreQueryMode.TEXT_SEARCH:
        if query.query_str:
            search_requests = {
                "searches": [
                    {
                        "collection": self._collection_name,
                        "q": query.query_str,
                        "query_by": self._text_key,
                        "filter_by": typesense_filter,
                    }
                ]
            }
        else:
            raise ValueError("Text search requires a query string")
    response = self._client.multi_search.perform(search_requests, {})

    top_k_nodes = []
    top_k_ids = []
    top_k_scores = None
    if query.mode is not VectorStoreQueryMode.TEXT_SEARCH:
        top_k_scores = []

    for hit in response["results"][0]["hits"]:
        document = hit["document"]
        id = document["id"]
        text = document[self._text_key]

        # Note that typesense distances range from 0 to 2, \
        # where 0 is most similar and 2 is most dissimilar
        if query.mode is not VectorStoreQueryMode.TEXT_SEARCH:
            score = hit["vector_distance"]

        try:
            node = metadata_dict_to_node(document[self._metadata_key])
            node.text = text
        except Exception:
            extra_info, node_info, relationships = legacy_metadata_dict_to_node(
                document[self._metadata_key], text_key=self._text_key
            )
            node = TextNode(
                text=text,
                id_=id,
                metadata=extra_info,
                start_chart_idx=node_info.get("start", None),
                end_chart_idx=node_info.get("end", None),
                relationships=relationships,
            )

        top_k_ids.append(id)
        top_k_nodes.append(node)
        if query.mode is not VectorStoreQueryMode.TEXT_SEARCH:
            top_k_scores.append(score)

    return VectorStoreQueryResult(
        nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
    )

```
 |  
| --- | --- |  
options: members: - TypesenseVectorStore
