# Supabase
##  SupabaseVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/supabase/#llama_index.vector_stores.supabase.SupabaseVectorStore "Permanent link")
Bases: 
Supbabase Vector.
In this vector store, embeddings are stored in Postgres table using pgvector.
During query time, the index uses pgvector/Supabase to query for the top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `postgres_connection_string`  |  postgres connection string  |  _required_  |  
|  `collection_name`  |  name of the collection to store the embeddings in  |  _required_  |  
|  `dimension`  |  dimension of the embeddings. Defaults to 1536.  |  `DEFAULT_EMBEDDING_DIM`  |  
Examples:
`pip install llama-index-vector-stores-supabase`

```
fromllama_index.vector_stores.supabaseimport SupabaseVectorStore

# Set up SupabaseVectorStore
vector_store = SupabaseVectorStore(
    postgres_connection_string="postgresql://<user>:<password>@<host>:<port>/<db_name>",
    collection_name="base_demo",
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-supabase/llama_index/vector_stores/supabase/base.py`  
| 
```
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
```
 | 
```
classSupabaseVectorStore(BasePydanticVectorStore):
"""
    Supbabase Vector.

    In this vector store, embeddings are stored in Postgres table using pgvector.

    During query time, the index uses pgvector/Supabase to query for the top
    k most similar nodes.

    Args:
        postgres_connection_string (str):
            postgres connection string
        collection_name (str):
            name of the collection to store the embeddings in
        dimension (int, optional):
            dimension of the embeddings. Defaults to 1536.

    Examples:
        `pip install llama-index-vector-stores-supabase`

        ```python
        from llama_index.vector_stores.supabase import SupabaseVectorStore

        # Set up SupabaseVectorStore
        vector_store = SupabaseVectorStore(
            postgres_connection_string="postgresql://<user>:<password>@<host>:<port>/<db_name>",
            collection_name="base_demo",

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False
    _client: Optional[Any] = PrivateAttr()
    _collection: Optional[Collection] = PrivateAttr()

    def__init__(
        self,
        postgres_connection_string: str,
        collection_name: str,
        dimension: int = DEFAULT_EMBEDDING_DIM,
        **kwargs: Any,
    ) -> None:
        super().__init__()
        self._client = vecs.create_client(postgres_connection_string)

        try:
            self._collection = self._client.get_collection(name=collection_name)
        except CollectionNotFound:
            logger.info(
                f"Collection {collection_name} does not exist, "
                f"try creating one with dimension={dimension}"
            )
            self._collection = self._client.create_collection(
                name=collection_name, dimension=dimension
            )

    def__del__(self) -> None:
"""Close the client when the object is deleted."""
        try:  # try-catch in case the attribute is not present
            self._client.disconnect()
        except AttributeError:
            pass

    @property
    defclient(self) -> None:
"""Get client."""
        return

    def_to_vecs_filters(self, filters: MetadataFilters) -> Any:
"""Convert llama filters to vecs filters. $eq is the only supported operator."""
        vecs_filter = defaultdict(list)
        filter_cond = f"${filters.condition.value}"

        for f in filters.legacy_filters():
            sub_filter = {}
            sub_filter[f.key] = {"$eq": f.value}
            vecs_filter[filter_cond].append(sub_filter)
        return vecs_filter

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        if self._collection is None:
            raise ValueError("Collection not initialized")

        data = []
        ids = []

        for node in nodes:
            # NOTE: keep text in metadata dict since there's no special field in
            #       Supabase Vector.
            metadata_dict = node_to_metadata_dict(
                node, remove_text=False, flat_metadata=self.flat_metadata
            )

            data.append((node.node_id, node.get_embedding(), metadata_dict))
            ids.append(node.node_id)

        self._collection.upsert(records=data)

        return ids

    defget_by_id(self, doc_id: str, **kwargs: Any) -> list:
"""
        Get row ids by doc id.

        Args:
            doc_id (str): document id

        """
        filters = {"doc_id": {"$eq": doc_id}}

        return self._collection.query(
            data=None,
            filters=filters,
            include_value=False,
            include_metadata=False,
            **kwargs,
        )

        # NOTE: list of row ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete doc.

        Args:
            :param ref_doc_id (str): document id

        """
        row_ids = self.get_by_id(ref_doc_id)

        if len(row_ids)  0:
            self._collection.delete(row_ids)

    defquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query (List[float]): query embedding

        """
        filters = None
        if query.filters is not None:
            filters = self._to_vecs_filters(query.filters)

        results = self._collection.query(
            data=query.query_embedding,
            limit=query.similarity_top_k,
            filters=filters,
            include_value=True,
            include_metadata=True,
        )

        similarities = []
        ids = []
        nodes = []
        for id_, distance, metadata in results:
"""shape of the result is [(vector, distance, metadata)]"""
            text = metadata.pop("text", None)

            try:
                node = metadata_dict_to_node(metadata)
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                metadata, node_info, relationships = legacy_metadata_dict_to_node(
                    metadata
                )
                node = TextNode(
                    id_=id_,
                    text=text,
                    metadata=metadata,
                    start_char_idx=node_info.get("start", None),
                    end_char_idx=node_info.get("end", None),
                    relationships=relationships,
                )

            nodes.append(node)
            similarities.append(1.0 - math.exp(-distance))
            ids.append(id_)

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/supabase/#llama_index.vector_stores.supabase.SupabaseVectorStore.client "Permanent link")

```
client: None

```

Get client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/supabase/#llama_index.vector_stores.supabase.SupabaseVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-supabase/llama_index/vector_stores/supabase/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    """
    if self._collection is None:
        raise ValueError("Collection not initialized")

    data = []
    ids = []

    for node in nodes:
        # NOTE: keep text in metadata dict since there's no special field in
        #       Supabase Vector.
        metadata_dict = node_to_metadata_dict(
            node, remove_text=False, flat_metadata=self.flat_metadata
        )

        data.append((node.node_id, node.get_embedding(), metadata_dict))
        ids.append(node.node_id)

    self._collection.upsert(records=data)

    return ids

```
 |  
| --- | --- |  
###  get_by_id [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/supabase/#llama_index.vector_stores.supabase.SupabaseVectorStore.get_by_id "Permanent link")

```
get_by_id(doc_id: , **kwargs: ) -> 

```

Get row ids by doc id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `doc_id`  |  document id  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-supabase/llama_index/vector_stores/supabase/base.py`  
| 
```
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
```
 | 
```
defget_by_id(self, doc_id: str, **kwargs: Any) -> list:
"""
    Get row ids by doc id.

    Args:
        doc_id (str): document id

    """
    filters = {"doc_id": {"$eq": doc_id}}

    return self._collection.query(
        data=None,
        filters=filters,
        include_value=False,
        include_metadata=False,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/supabase/#llama_index.vector_stores.supabase.SupabaseVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete doc.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  param ref_doc_id (str): document id  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-supabase/llama_index/vector_stores/supabase/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete doc.

    Args:
        :param ref_doc_id (str): document id

    """
    row_ids = self.get_by_id(ref_doc_id)

    if len(row_ids)  0:
        self._collection.delete(row_ids)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/supabase/#llama_index.vector_stores.supabase.SupabaseVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  `List[float]`  |  query embedding  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-supabase/llama_index/vector_stores/supabase/base.py`  
| 
```
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
```
 | 
```
defquery(
    self,
    query: VectorStoreQuery,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query (List[float]): query embedding

    """
    filters = None
    if query.filters is not None:
        filters = self._to_vecs_filters(query.filters)

    results = self._collection.query(
        data=query.query_embedding,
        limit=query.similarity_top_k,
        filters=filters,
        include_value=True,
        include_metadata=True,
    )

    similarities = []
    ids = []
    nodes = []
    for id_, distance, metadata in results:
"""shape of the result is [(vector, distance, metadata)]"""
        text = metadata.pop("text", None)

        try:
            node = metadata_dict_to_node(metadata)
        except Exception:
            # NOTE: deprecated legacy logic for backward compatibility
            metadata, node_info, relationships = legacy_metadata_dict_to_node(
                metadata
            )
            node = TextNode(
                id_=id_,
                text=text,
                metadata=metadata,
                start_char_idx=node_info.get("start", None),
                end_char_idx=node_info.get("end", None),
                relationships=relationships,
            )

        nodes.append(node)
        similarities.append(1.0 - math.exp(-distance))
        ids.append(id_)

    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
options: members: - SupabaseVectorStore
