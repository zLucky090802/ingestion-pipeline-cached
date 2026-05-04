# Singlestoredb
##  SingleStoreVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/singlestoredb/#llama_index.vector_stores.singlestoredb.SingleStoreVectorStore "Permanent link")
Bases: 
SingleStore vector store.
This vector store stores embeddings within a SingleStore database table.
During query time, the index uses SingleStore to query for the top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `table_name`  |  Specifies the name of the table in use. Defaults to "embeddings".  |  `'embeddings'`  |  
|  `content_field`  |  Specifies the field to store the content. Defaults to "content".  |  `'content'`  |  
|  `metadata_field`  |  Specifies the field to store metadata. Defaults to "metadata".  |  `'metadata'`  |  
|  `vector_field`  |  Specifies the field to store the vector. Defaults to "vector".  |  `'vector'`  |  
|  `Following arguments pertain to the connection pool`  |  _required_  |  
|  `pool_size`  |  Determines the number of active connections in the pool. Defaults to 5.  |  
|  `max_overflow`  |  Determines the maximum number of connections allowed beyond the pool_size. Defaults to 10.  |  
|  `timeout`  |  `float`  |  Specifies the maximum wait time in seconds for establishing a connection. Defaults to 30.  |  
|  `Following arguments pertain to the connection`  |  _required_  |  
|  `host`  |  Specifies the hostname, IP address, or URL for the database connection. The default scheme is "mysql".  |  _required_  |  
|  `user`  |  Database username.  |  _required_  |  
|  `password`  |  Database password.  |  _required_  |  
|  `port`  |  Database port. Defaults to 3306 for non-HTTP connections, 80 for HTTP connections, and 443 for HTTPS connections.  |  _required_  |  
|  `database`  |  Database name.  |  _required_  |  
Examples:
`pip install llama-index-vector-stores-singlestoredb`

```
fromllama_index.vector_stores.singlestoredbimport SingleStoreVectorStore
importos

# can set the singlestore db url in env
# or pass it in as an argument to the SingleStoreVectorStore constructor
os.environ["SINGLESTOREDB_URL"] = "PLACEHOLDER URL"
vector_store = SingleStoreVectorStore(
    table_name="embeddings",
    content_field="content",
    metadata_field="metadata",
    vector_field="vector",
    timeout=30,
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-singlestoredb/llama_index/vector_stores/singlestoredb/base.py`  
| 
```
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
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
```
 | 
```
classSingleStoreVectorStore(BasePydanticVectorStore):
"""
    SingleStore vector store.

    This vector store stores embeddings within a SingleStore database table.

    During query time, the index uses SingleStore to query for the top
    k most similar nodes.

    Args:
        table_name (str, optional): Specifies the name of the table in use.
                Defaults to "embeddings".
        content_field (str, optional): Specifies the field to store the content.
            Defaults to "content".
        metadata_field (str, optional): Specifies the field to store metadata.
            Defaults to "metadata".
        vector_field (str, optional): Specifies the field to store the vector.
            Defaults to "vector".

        Following arguments pertain to the connection pool:

        pool_size (int, optional): Determines the number of active connections in
            the pool. Defaults to 5.
        max_overflow (int, optional): Determines the maximum number of connections
            allowed beyond the pool_size. Defaults to 10.
        timeout (float, optional): Specifies the maximum wait time in seconds for
            establishing a connection. Defaults to 30.

        Following arguments pertain to the connection:

        host (str, optional): Specifies the hostname, IP address, or URL for the
                database connection. The default scheme is "mysql".
        user (str, optional): Database username.
        password (str, optional): Database password.
        port (int, optional): Database port. Defaults to 3306 for non-HTTP
            connections, 80 for HTTP connections, and 443 for HTTPS connections.
        database (str, optional): Database name.

    Examples:
        `pip install llama-index-vector-stores-singlestoredb`

        ```python
        from llama_index.vector_stores.singlestoredb import SingleStoreVectorStore
        import os

        # can set the singlestore db url in env
        # or pass it in as an argument to the SingleStoreVectorStore constructor
        os.environ["SINGLESTOREDB_URL"] = "PLACEHOLDER URL"
        vector_store = SingleStoreVectorStore(
            table_name="embeddings",
            content_field="content",
            metadata_field="metadata",
            vector_field="vector",
            timeout=30,

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = True

    table_name: str
    content_field: str
    metadata_field: str
    vector_field: str
    pool_size: int
    max_overflow: int
    timeout: float
    connection_kwargs: dict
    connection_pool: QueuePool

    def__init__(
        self,
        table_name: str = "embeddings",
        content_field: str = "content",
        metadata_field: str = "metadata",
        vector_field: str = "vector",
        pool_size: int = 5,
        max_overflow: int = 10,
        timeout: float = 30,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__(
            table_name=table_name,
            content_field=content_field,
            metadata_field=metadata_field,
            vector_field=vector_field,
            pool_size=pool_size,
            max_overflow=max_overflow,
            timeout=timeout,
            connection_kwargs=kwargs,
            connection_pool=QueuePool(
                self._get_connection,
                pool_size=pool_size,
                max_overflow=max_overflow,
                timeout=timeout,
            ),
            stores_text=True,
        )

        self._create_table()

    @property
    defclient(self) -> Any:
"""Return SingleStoreDB client."""
        return self._get_connection()

    @classmethod
    defclass_name(cls) -> str:
        return "SingleStoreVectorStore"

    def_get_connection(self) -> Any:
        return s2.connect(**self.connection_kwargs)

    def_create_table(self) -> None:
        VALID_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")
        if not VALID_NAME_PATTERN.match(self.table_name):
            raise ValueError(
                f"Invalid table name: {self.table_name}. Table names can only contain alphanumeric characters and underscores."
            )

        if not VALID_NAME_PATTERN.match(self.content_field):
            raise ValueError(
                f"Invalid content_field: {self.content_field}. Field names can only contain alphanumeric characters and underscores."
            )

        if not VALID_NAME_PATTERN.match(self.vector_field):
            raise ValueError(
                f"Invalid vector_field: {self.vector_field}. Field names can only contain alphanumeric characters and underscores."
            )

        if not VALID_NAME_PATTERN.match(self.metadata_field):
            raise ValueError(
                f"Invalid metadata_field: {self.metadata_field}. Field names can only contain alphanumeric characters and underscores."
            )
        conn = self.connection_pool.connect()
        try:
            cur = conn.cursor()
            try:
                cur.execute(
                    f"""CREATE TABLE IF NOT EXISTS {self.table_name}
{self.content_field} TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
{self.vector_field} BLOB, {self.metadata_field} JSON);"""
                )
            finally:
                cur.close()
        finally:
            conn.close()

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        insert_query = (
            f"INSERT INTO {self.table_name} VALUES (%s, JSON_ARRAY_PACK(%s), %s)"
        )

        conn = self.connection_pool.connect()
        try:
            cursor = conn.cursor()
            try:
                for node in nodes:
                    embedding = node.get_embedding()
                    metadata = node_to_metadata_dict(
                        node, remove_text=True, flat_metadata=self.flat_metadata
                    )
                    # Use parameterized query for all data values
                    cursor.execute(
                        insert_query,
                        (
                            node.get_content(metadata_mode=MetadataMode.NONE) or "",
                            "[{}]".format(",".join(map(str, embedding))),
                            json.dumps(metadata),
                        ),
                    )
            finally:
                cursor.close()
        finally:
            conn.close()

        return [node.node_id for node in nodes]

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        delete_query = f"DELETE FROM {self.table_name} WHERE JSON_EXTRACT_JSON({self.metadata_field}, 'ref_doc_id') = %s"
        conn = self.connection_pool.connect()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(delete_query, (json.dumps(ref_doc_id),))
            finally:
                cursor.close()
        finally:
            conn.close()

    defquery(
        self, query: VectorStoreQuery, filter: Optional[dict] = None, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): Contains query_embedding and similarity_top_k attributes.
            filter (Optional[dict]): A dictionary of metadata fields and values to filter by. Defaults to None.

        Returns:
            VectorStoreQueryResult: Contains nodes, similarities, and ids attributes.

        """
        query_embedding = query.query_embedding
        similarity_top_k = query.similarity_top_k
        if not isinstance(similarity_top_k, int) or similarity_top_k <= 0:
            raise ValueError(
                f"similarity_top_k must be a positive integer, got {similarity_top_k}"
            )
        conn = self.connection_pool.connect()
        where_clause: str = ""
        where_clause_values: List[Any] = []

        if filter:
            where_clause = "WHERE "
            arguments = []

            defbuild_where_clause(
                where_clause_values: List[Any],
                sub_filter: dict,
                prefix_args: Optional[List[str]] = None,
            ) -> None:
                prefix_args = prefix_args or []
                for key in sub_filter:
                    if isinstance(sub_filter[key], dict):
                        build_where_clause(
                            where_clause_values, sub_filter[key], [*prefix_args, key]
                        )
                    else:
                        arguments.append(
                            f"JSON_EXTRACT({self.metadata_field}, {', '.join(['%s']*(len(prefix_args)+1))}) = %s"
                        )
                        where_clause_values += [*prefix_args, key]
                        where_clause_values.append(json.dumps(sub_filter[key]))

            build_where_clause(where_clause_values, filter)
            where_clause += " AND ".join(arguments)

        results: Sequence[Any] = []
        if query_embedding:
            try:
                cur = conn.cursor()
                formatted_vector = "[{}]".format(",".join(map(str, query_embedding)))
                try:
                    logger.debug("vector field: %s", formatted_vector)
                    logger.debug("similarity_top_k: %s", similarity_top_k)
                    query = (
                        f"SELECT {self.content_field}, {self.metadata_field}, "
                        f"DOT_PRODUCT({self.vector_field}, "
                        "JSON_ARRAY_PACK(%s)) as similarity_score "
                        f"FROM {self.table_name}{where_clause} "
                        "ORDER BY similarity_score DESC LIMIT %s"
                    )
                    cur.execute(
                        query,
                        (
                            formatted_vector,
                            *tuple(where_clause_values),
                            similarity_top_k,
                        ),
                    )
                    results = cur.fetchall()
                finally:
                    cur.close()
            finally:
                conn.close()

        nodes = []
        similarities = []
        ids = []
        for result in results:
            text, metadata, similarity_score = result
            node = metadata_dict_to_node(metadata)
            node.set_content(text)
            nodes.append(node)
            similarities.append(similarity_score)
            ids.append(node.node_id)

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/singlestoredb/#llama_index.vector_stores.singlestoredb.SingleStoreVectorStore.client "Permanent link")

```
client: 

```

Return SingleStoreDB client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/singlestoredb/#llama_index.vector_stores.singlestoredb.SingleStoreVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-singlestoredb/llama_index/vector_stores/singlestoredb/base.py`  
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    """
    insert_query = (
        f"INSERT INTO {self.table_name} VALUES (%s, JSON_ARRAY_PACK(%s), %s)"
    )

    conn = self.connection_pool.connect()
    try:
        cursor = conn.cursor()
        try:
            for node in nodes:
                embedding = node.get_embedding()
                metadata = node_to_metadata_dict(
                    node, remove_text=True, flat_metadata=self.flat_metadata
                )
                # Use parameterized query for all data values
                cursor.execute(
                    insert_query,
                    (
                        node.get_content(metadata_mode=MetadataMode.NONE) or "",
                        "[{}]".format(",".join(map(str, embedding))),
                        json.dumps(metadata),
                    ),
                )
        finally:
            cursor.close()
    finally:
        conn.close()

    return [node.node_id for node in nodes]

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/singlestoredb/#llama_index.vector_stores.singlestoredb.SingleStoreVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-singlestoredb/llama_index/vector_stores/singlestoredb/base.py`  
| 
```
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
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    delete_query = f"DELETE FROM {self.table_name} WHERE JSON_EXTRACT_JSON({self.metadata_field}, 'ref_doc_id') = %s"
    conn = self.connection_pool.connect()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(delete_query, (json.dumps(ref_doc_id),))
        finally:
            cursor.close()
    finally:
        conn.close()

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/singlestoredb/#llama_index.vector_stores.singlestoredb.SingleStoreVectorStore.query "Permanent link")

```
query(
    query: ,
    filter: Optional[] = None,
    **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Contains query_embedding and similarity_top_k attributes.  |  _required_  |  
|  `filter`  |  `Optional[dict]`  |  A dictionary of metadata fields and values to filter by. Defaults to None.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  Contains nodes, similarities, and ids attributes.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-singlestoredb/llama_index/vector_stores/singlestoredb/base.py`  
| 
```
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
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
```
 | 
```
defquery(
    self, query: VectorStoreQuery, filter: Optional[dict] = None, **kwargs: Any
) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): Contains query_embedding and similarity_top_k attributes.
        filter (Optional[dict]): A dictionary of metadata fields and values to filter by. Defaults to None.

    Returns:
        VectorStoreQueryResult: Contains nodes, similarities, and ids attributes.

    """
    query_embedding = query.query_embedding
    similarity_top_k = query.similarity_top_k
    if not isinstance(similarity_top_k, int) or similarity_top_k <= 0:
        raise ValueError(
            f"similarity_top_k must be a positive integer, got {similarity_top_k}"
        )
    conn = self.connection_pool.connect()
    where_clause: str = ""
    where_clause_values: List[Any] = []

    if filter:
        where_clause = "WHERE "
        arguments = []

        defbuild_where_clause(
            where_clause_values: List[Any],
            sub_filter: dict,
            prefix_args: Optional[List[str]] = None,
        ) -> None:
            prefix_args = prefix_args or []
            for key in sub_filter:
                if isinstance(sub_filter[key], dict):
                    build_where_clause(
                        where_clause_values, sub_filter[key], [*prefix_args, key]
                    )
                else:
                    arguments.append(
                        f"JSON_EXTRACT({self.metadata_field}, {', '.join(['%s']*(len(prefix_args)+1))}) = %s"
                    )
                    where_clause_values += [*prefix_args, key]
                    where_clause_values.append(json.dumps(sub_filter[key]))

        build_where_clause(where_clause_values, filter)
        where_clause += " AND ".join(arguments)

    results: Sequence[Any] = []
    if query_embedding:
        try:
            cur = conn.cursor()
            formatted_vector = "[{}]".format(",".join(map(str, query_embedding)))
            try:
                logger.debug("vector field: %s", formatted_vector)
                logger.debug("similarity_top_k: %s", similarity_top_k)
                query = (
                    f"SELECT {self.content_field}, {self.metadata_field}, "
                    f"DOT_PRODUCT({self.vector_field}, "
                    "JSON_ARRAY_PACK(%s)) as similarity_score "
                    f"FROM {self.table_name}{where_clause} "
                    "ORDER BY similarity_score DESC LIMIT %s"
                )
                cur.execute(
                    query,
                    (
                        formatted_vector,
                        *tuple(where_clause_values),
                        similarity_top_k,
                    ),
                )
                results = cur.fetchall()
            finally:
                cur.close()
        finally:
            conn.close()

    nodes = []
    similarities = []
    ids = []
    for result in results:
        text, metadata, similarity_score = result
        node = metadata_dict_to_node(metadata)
        node.set_content(text)
        nodes.append(node)
        similarities.append(similarity_score)
        ids.append(node.node_id)

    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
options: members: - SingleStoreVectorStore
