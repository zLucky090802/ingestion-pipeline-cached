# Awadb
##  AwaDBVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/awadb/#llama_index.vector_stores.awadb.AwaDBVectorStore "Permanent link")
Bases: 
AwaDB vector store.
In this vector store, embeddings are stored within a AwaDB table.
During query time, the index uses AwaDB to query for the top k most similar nodes.
Examples:
`pip install llama-index-vector-stores-awadb`

```
fromllama_index.vector_stores.awadbimport AwaDBVectorStore

vector_store = AwaDBVectorStore(table_name="llamaindex")

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-awadb/llama_index/vector_stores/awadb/base.py`  
| 
```
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
221
222
223
224
225
226
227
228
```
 | 
```
classAwaDBVectorStore(BasePydanticVectorStore):
"""
    AwaDB vector store.

    In this vector store, embeddings are stored within a AwaDB table.

    During query time, the index uses AwaDB to query for the top
    k most similar nodes.

    Examples:
        `pip install llama-index-vector-stores-awadb`

        ```python
        from llama_index.vector_stores.awadb import AwaDBVectorStore

        vector_store = AwaDBVectorStore(table_name="llamaindex")
        ```

    """

    flat_metadata: bool = True
    stores_text: bool = True
    DEFAULT_TABLE_NAME: str = "llamaindex_awadb"

    _awadb_client: Any = PrivateAttr()

    @property
    defclient(self) -> Any:
"""Get AwaDB client."""
        return self._awadb_client

    def__init__(
        self,
        table_name: str = DEFAULT_TABLE_NAME,
        log_and_data_dir: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
"""
        Initialize with AwaDB client.
           If table_name is not specified,
           a random table name of `DEFAULT_TABLE_NAME + last segment of uuid`
           would be created automatically.

        Args:
            table_name: Name of the table created, default DEFAULT_TABLE_NAME.
            log_and_data_dir: Optional the root directory of log and data.
            kwargs: Any possible extend parameters in the future.

        Returns:
            None.

        """
        super().__init__()

        import_err_msg = "`awadb` package not found, please run `pip install awadb`"
        try:
            importawadb
        except ImportError:
            raise ImportError(import_err_msg)
        if log_and_data_dir is not None:
            self._awadb_client = awadb.Client(log_and_data_dir)
        else:
            self._awadb_client = awadb.Client()

        if table_name == self.DEFAULT_TABLE_NAME:
            table_name += "_"
            table_name += str(uuid.uuid4()).split("-")[-1]

        self._awadb_client.Create(table_name)

    @classmethod
    defclass_name(cls) -> str:
        return "AwaDBVectorStore"

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to AwaDB.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        Returns:
            Added node ids

        """
        if not self._awadb_client:
            raise ValueError("AwaDB client not initialized")

        embeddings = []
        metadatas = []
        ids = []
        texts = []
        for node in nodes:
            embeddings.append(node.get_embedding())
            metadatas.append(
                node_to_metadata_dict(
                    node, remove_text=True, flat_metadata=self.flat_metadata
                )
            )
            ids.append(node.node_id)
            texts.append(node.get_content(metadata_mode=MetadataMode.NONE) or "")

        self._awadb_client.AddTexts(
            "embedding_text",
            "text_embedding",
            texts,
            embeddings,
            metadatas,
            is_duplicate_texts=False,
            ids=ids,
        )

        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        Returns:
            None

        """
        if len(ref_doc_id) == 0:
            return
        ids: List[str] = []
        ids.append(ref_doc_id)
        self._awadb_client.Delete(ids)

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query : vector store query

        Returns:
            VectorStoreQueryResult: Query results

        """
        meta_filters = {}
        if query.filters is not None:
            for filter in query.filters.legacy_filters():
                meta_filters[filter.key] = filter.value

        not_include_fields: Set[str] = {"text_embedding"}
        results = self._awadb_client.Search(
            query=query.query_embedding,
            topn=query.similarity_top_k,
            meta_filter=meta_filters,
            not_include_fields=not_include_fields,
        )

        nodes = []
        similarities = []
        ids = []

        for item_detail in results[0]["ResultItems"]:
            content = ""
            meta_data = {}
            node_id = ""
            for item_key in item_detail:
                if item_key == "embedding_text":
                    content = item_detail[item_key]
                    continue
                elif item_key == "_id":
                    node_id = item_detail[item_key]
                    ids.append(node_id)
                    continue
                elif item_key == "score":
                    similarities.append(item_detail[item_key])
                    continue
                meta_data[item_key] = item_detail[item_key]

            try:
                node = metadata_dict_to_node(meta_data)
                node.set_content(content)
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                metadata, node_info, relationships = legacy_metadata_dict_to_node(
                    meta_data
                )

                node = TextNode(
                    text=content,
                    id_=node_id,
                    metadata=metadata,
                    start_char_idx=node_info.get("start", None),
                    end_char_idx=node_info.get("end", None),
                    relationships=relationships,
                )

            nodes.append(node)

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/awadb/#llama_index.vector_stores.awadb.AwaDBVectorStore.client "Permanent link")

```
client: 

```

Get AwaDB client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/awadb/#llama_index.vector_stores.awadb.AwaDBVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to AwaDB.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  Added node ids  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-awadb/llama_index/vector_stores/awadb/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to AwaDB.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    Returns:
        Added node ids

    """
    if not self._awadb_client:
        raise ValueError("AwaDB client not initialized")

    embeddings = []
    metadatas = []
    ids = []
    texts = []
    for node in nodes:
        embeddings.append(node.get_embedding())
        metadatas.append(
            node_to_metadata_dict(
                node, remove_text=True, flat_metadata=self.flat_metadata
            )
        )
        ids.append(node.node_id)
        texts.append(node.get_content(metadata_mode=MetadataMode.NONE) or "")

    self._awadb_client.AddTexts(
        "embedding_text",
        "text_embedding",
        texts,
        embeddings,
        metadatas,
        is_duplicate_texts=False,
        ids=ids,
    )

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/awadb/#llama_index.vector_stores.awadb.AwaDBVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `None`  |  None  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-awadb/llama_index/vector_stores/awadb/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    Returns:
        None

    """
    if len(ref_doc_id) == 0:
        return
    ids: List[str] = []
    ids.append(ref_doc_id)
    self._awadb_client.Delete(ids)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/awadb/#llama_index.vector_stores.awadb.AwaDBVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query `  |  vector store query  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  Query results  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-awadb/llama_index/vector_stores/awadb/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query : vector store query

    Returns:
        VectorStoreQueryResult: Query results

    """
    meta_filters = {}
    if query.filters is not None:
        for filter in query.filters.legacy_filters():
            meta_filters[filter.key] = filter.value

    not_include_fields: Set[str] = {"text_embedding"}
    results = self._awadb_client.Search(
        query=query.query_embedding,
        topn=query.similarity_top_k,
        meta_filter=meta_filters,
        not_include_fields=not_include_fields,
    )

    nodes = []
    similarities = []
    ids = []

    for item_detail in results[0]["ResultItems"]:
        content = ""
        meta_data = {}
        node_id = ""
        for item_key in item_detail:
            if item_key == "embedding_text":
                content = item_detail[item_key]
                continue
            elif item_key == "_id":
                node_id = item_detail[item_key]
                ids.append(node_id)
                continue
            elif item_key == "score":
                similarities.append(item_detail[item_key])
                continue
            meta_data[item_key] = item_detail[item_key]

        try:
            node = metadata_dict_to_node(meta_data)
            node.set_content(content)
        except Exception:
            # NOTE: deprecated legacy logic for backward compatibility
            metadata, node_info, relationships = legacy_metadata_dict_to_node(
                meta_data
            )

            node = TextNode(
                text=content,
                id_=node_id,
                metadata=metadata,
                start_char_idx=node_info.get("start", None),
                end_char_idx=node_info.get("end", None),
                relationships=relationships,
            )

        nodes.append(node)

    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
options: members: - AwaDBVectorStore
