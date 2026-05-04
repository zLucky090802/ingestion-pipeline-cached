# Azure postgres
Common utilities and models for Azure Database for PostgreSQL operations.
##  AzurePGVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azure_postgres/#llama_index.vector_stores.azure_postgres.AzurePGVectorStore "Permanent link")
Bases: , `BaseAzurePGVectorStore`
Azure PostgreSQL vector store for LlamaIndex.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurepostgresql/llama_index/vector_stores/azure_postgres/base.py`  
| 
```
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
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
```
 | 
```
classAzurePGVectorStore(BasePydanticVectorStore, BaseAzurePGVectorStore):
"""Azure PostgreSQL vector store for LlamaIndex."""

    stores_text: bool = True
    metadata_columns: str | None = "metadata"

    @classmethod
    defclass_name(cls) -> str:
"""Return the class name for this vector store."""
        return "AzurePGVectorStore"

    @property
    defclient(self) -> None:
"""Return the client property (not used for AzurePGVectorStore)."""
        return

    @override
    @classmethod
    deffrom_params(
        cls,
        connection_pool: AzurePGConnectionPool,
        schema_name: str = "public",
        table_name: str = "llamaindex_vectors",
        embed_dim: int = 1536,
        embedding_index: Algorithm | None = None,
    ) -> "AzurePGVectorStore":
"""Create an AzurePGVectorStore from connection and configuration parameters."""
        return cls(
            connection_pool=connection_pool,
            schema_name=schema_name,
            table_name=table_name,
            embed_dim=embed_dim,
            embedding_index=embedding_index,
        )

    def_table_row_to_node(self, row: dict[str, Any]) -> BaseNode:
"""Convert a table row dictionary to a BaseNode object."""
        metadata = row.get("metadata")
        if metadata is None:
            raise ValueError("Metadata not found in row data.")

        node = metadata_dict_to_node(metadata, text=row.get("content"))
        # Convert UUID to string if needed
        node_id = row.get("id")
        if node_id is not None:
            node.node_id = str(node_id)
        embedding = row.get("embedding")

        if isinstance(embedding, str):
            embedding = row.get("embedding").strip("[]").split(",")
            node.embedding = list(map(float, embedding))
        elif embedding is not None:
            node.embedding = embedding
        else:
            raise ValueError("Missing embedding value")

        return node

    def_get_insert_sql_dict(
        self, node: BaseNode, on_conflict_update: bool
    ) -> tuple[sql.SQL, dict[str, Any]]:
"""Get the SQL command and dictionary for inserting a node."""
        if on_conflict_update:
            update = sql.SQL(
"""
                UPDATE SET
                    {content_col} = EXCLUDED.{content_col},
                    {embedding_col} = EXCLUDED.{embedding_col},
                    {metadata_col} = EXCLUDED.{metadata_col}

            ).format(
                id_col=sql.Identifier(self.id_column),
                content_col=sql.Identifier(self.content_column),
                embedding_col=sql.Identifier(self.embedding_column),
                metadata_col=sql.Identifier(self.metadata_columns),
            )
        else:
            update = sql.SQL("nothing")
        insert_sql = sql.SQL(
"""
            INSERT INTO {schema}.{table} ({id_col}, {content_col}, {embedding_col}, {metadata_col})
            VALUES (%(id)s, %(content)s, %(embedding)s, %(metadata)s)
            ON CONFLICT ({id_col}) DO {update}
        """
        ).format(
            schema=sql.Identifier(self.schema_name),
            table=sql.Identifier(self.table_name),
            id_col=sql.Identifier(self.id_column),
            content_col=sql.Identifier(self.content_column),
            embedding_col=sql.Identifier(self.embedding_column),
            metadata_col=sql.Identifier(self.metadata_columns),
            update=update,
        )

        return (
            insert_sql,
            {
                "id": node.node_id,
                "content": node.get_content(metadata_mode=MetadataMode.NONE),
                "embedding": np.array(node.get_embedding(), dtype=np.float32),
                "metadata": Jsonb(node_to_metadata_dict(node)),
            },
        )

    @override
    defadd(self, nodes: list[BaseNode], **add_kwargs: Any) -> list[str]:
"""Add a list of BaseNode objects to the vector store.

        Args:
            nodes: List of BaseNode objects to add.
            **add_kwargs: Additional keyword arguments.

        Returns:
            List of node IDs added.
        """
        ids = []
        on_conflict_update = bool(add_kwargs.pop("on_conflict_update", None))
        with self.connection_pool.connection() as conn:
            register_vector(conn)
            with conn.cursor(row_factory=dict_row) as cursor:
                for node in nodes:
                    ids.append(node.node_id)
                    insert_sql, insert_dict = self._get_insert_sql_dict(
                        node, on_conflict_update
                    )
                    cursor.execute(insert_sql, insert_dict)
        return ids

    @override
    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Perform a similarity search using the provided query.

        Args:
            query: VectorStoreQuery object containing the query embedding and parameters.
            **kwargs: Additional keyword arguments.

        Returns:
            VectorStoreQueryResult containing the search results.
        """
        results = self._similarity_search_by_vector_with_distance(
            embedding=query.query_embedding,
            k=query.similarity_top_k,
            filter_expression=metadata_filters_to_sql(query.filters),
            **kwargs,
        )
        if query.mode == VectorStoreQueryMode.HYBRID:
            text_results = self._full_text_search(
                query_str=query.query_str,
                **kwargs,
            )
            results = self._dedup_results(results + text_results)

        nodes = []
        similarities = []
        ids = []
        for row in results:
            node = metadata_dict_to_node(row[0]["metadata"], text=row[0]["content"])
            nodes.append(node)
            similarities.append(row[1])
            ids.append(row[0]["id"])

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities,
            ids=ids,
        )

    @override
    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Delete a node from the vector store by reference document ID.

        Args:
            ref_doc_id: The reference document ID to delete.
            **delete_kwargs: Additional keyword arguments.
        """
        with self.connection_pool.connection() as conn:
            register_vector(conn)
            with conn.cursor(row_factory=dict_row) as cursor:
                delete_sql = sql.SQL(
                    "DELETE FROM {table} WHERE metadata ->> 'doc_id' = %s"
                ).format(table=sql.Identifier(self.schema_name, self.table_name))
                cursor.execute(delete_sql, (ref_doc_id,))

    @override
    defdelete_nodes(
        self,
        node_ids: list[str] | None = None,
        filters: MetadataFilters | None = None,
        **delete_kwargs: Any,
    ) -> None:
"""Delete nodes from the vector store by node IDs or filters.

        Args:
            node_ids: Optional list of node IDs to delete.
            filters: Optional MetadataFilters to filter nodes for deletion.
            **delete_kwargs: Additional keyword arguments.
        """
        if not node_ids:
            return

        self._delete_rows_from_table(
            ids=node_ids, filters=metadata_filters_to_sql(filters), **delete_kwargs
        )

    @override
    defclear(self) -> None:
"""Clear all data from the vector store table."""
        with self.connection_pool.connection() as conn:
            register_vector(conn)
            with conn.cursor(row_factory=dict_row) as cursor:
                stmt = sql.SQL("TRUNCATE TABLE {schema}.{table}").format(
                    schema=sql.Identifier(self.schema_name),
                    table=sql.Identifier(self.table_name),
                )
                cursor.execute(stmt)
                conn.commit()

    @override
    defget_nodes(
        self,
        node_ids: list[str] | None = None,
        filters: MetadataFilters | None = None,
        **kwargs: Any,
    ) -> list[BaseNode]:
"""Retrieve nodes by IDs or filters.

        Args:
            node_ids: Optional list of node IDs to retrieve.
            filters: Optional MetadataFilters to filter nodes.
            **kwargs: Additional keyword arguments.

        Returns:
            List of BaseNode objects matching the criteria.
        """
        # TODO: Implement filter handling
        documents = self._get_by_ids(node_ids)
        nodes = []
        for doc in documents:
            node = self._table_row_to_node(doc)
            nodes.append(node)

        return nodes

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azure_postgres/#llama_index.vector_stores.azure_postgres.AzurePGVectorStore.client "Permanent link")

```
client: None

```

Return the client property (not used for AzurePGVectorStore).
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azure_postgres/#llama_index.vector_stores.azure_postgres.AzurePGVectorStore.class_name "Permanent link")

```
class_name() -> 

```

Return the class name for this vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurepostgresql/llama_index/vector_stores/azure_postgres/base.py`  
| 
```
149
150
151
152
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Return the class name for this vector store."""
    return "AzurePGVectorStore"

```
 |  
| --- | --- |  
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azure_postgres/#llama_index.vector_stores.azure_postgres.AzurePGVectorStore.from_params "Permanent link")

```
from_params(
    connection_pool: AzurePGConnectionPool,
    schema_name:  = "public",
    table_name:  = "llamaindex_vectors",
    embed_dim:  = 1536,
    embedding_index: Algorithm | None = None,
) -> 

```

Create an AzurePGVectorStore from connection and configuration parameters.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurepostgresql/llama_index/vector_stores/azure_postgres/base.py`  
| 
```
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
```
 | 
```
@override
@classmethod
deffrom_params(
    cls,
    connection_pool: AzurePGConnectionPool,
    schema_name: str = "public",
    table_name: str = "llamaindex_vectors",
    embed_dim: int = 1536,
    embedding_index: Algorithm | None = None,
) -> "AzurePGVectorStore":
"""Create an AzurePGVectorStore from connection and configuration parameters."""
    return cls(
        connection_pool=connection_pool,
        schema_name=schema_name,
        table_name=table_name,
        embed_dim=embed_dim,
        embedding_index=embedding_index,
    )

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azure_postgres/#llama_index.vector_stores.azure_postgres.AzurePGVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add a list of BaseNode objects to the vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of BaseNode objects to add.  |  _required_  |  
|  `**add_kwargs`  |  Additional keyword arguments.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `list[str]`  |  List of node IDs added.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurepostgresql/llama_index/vector_stores/azure_postgres/base.py`  
| 
```
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
```
 | 
```
@override
defadd(self, nodes: list[BaseNode], **add_kwargs: Any) -> list[str]:
"""Add a list of BaseNode objects to the vector store.

    Args:
        nodes: List of BaseNode objects to add.
        **add_kwargs: Additional keyword arguments.

    Returns:
        List of node IDs added.
    """
    ids = []
    on_conflict_update = bool(add_kwargs.pop("on_conflict_update", None))
    with self.connection_pool.connection() as conn:
        register_vector(conn)
        with conn.cursor(row_factory=dict_row) as cursor:
            for node in nodes:
                ids.append(node.node_id)
                insert_sql, insert_dict = self._get_insert_sql_dict(
                    node, on_conflict_update
                )
                cursor.execute(insert_sql, insert_dict)
    return ids

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azure_postgres/#llama_index.vector_stores.azure_postgres.AzurePGVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Perform a similarity search using the provided query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  VectorStoreQuery object containing the query embedding and parameters.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  VectorStoreQueryResult containing the search results.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurepostgresql/llama_index/vector_stores/azure_postgres/base.py`  
| 
```
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
```
 | 
```
@override
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Perform a similarity search using the provided query.

    Args:
        query: VectorStoreQuery object containing the query embedding and parameters.
        **kwargs: Additional keyword arguments.

    Returns:
        VectorStoreQueryResult containing the search results.
    """
    results = self._similarity_search_by_vector_with_distance(
        embedding=query.query_embedding,
        k=query.similarity_top_k,
        filter_expression=metadata_filters_to_sql(query.filters),
        **kwargs,
    )
    if query.mode == VectorStoreQueryMode.HYBRID:
        text_results = self._full_text_search(
            query_str=query.query_str,
            **kwargs,
        )
        results = self._dedup_results(results + text_results)

    nodes = []
    similarities = []
    ids = []
    for row in results:
        node = metadata_dict_to_node(row[0]["metadata"], text=row[0]["content"])
        nodes.append(node)
        similarities.append(row[1])
        ids.append(row[0]["id"])

    return VectorStoreQueryResult(
        nodes=nodes,
        similarities=similarities,
        ids=ids,
    )

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azure_postgres/#llama_index.vector_stores.azure_postgres.AzurePGVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete a node from the vector store by reference document ID.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The reference document ID to delete.  |  _required_  |  
|  `**delete_kwargs`  |  Additional keyword arguments.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurepostgresql/llama_index/vector_stores/azure_postgres/base.py`  
| 
```
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
320
321
322
323
324
```
 | 
```
@override
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Delete a node from the vector store by reference document ID.

    Args:
        ref_doc_id: The reference document ID to delete.
        **delete_kwargs: Additional keyword arguments.
    """
    with self.connection_pool.connection() as conn:
        register_vector(conn)
        with conn.cursor(row_factory=dict_row) as cursor:
            delete_sql = sql.SQL(
                "DELETE FROM {table} WHERE metadata ->> 'doc_id' = %s"
            ).format(table=sql.Identifier(self.schema_name, self.table_name))
            cursor.execute(delete_sql, (ref_doc_id,))

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azure_postgres/#llama_index.vector_stores.azure_postgres.AzurePGVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: [] | None = None,
    filters:  | None = None,
    **delete_kwargs: 
) -> None

```

Delete nodes from the vector store by node IDs or filters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `list[str] | None`  |  Optional list of node IDs to delete.  |  `None`  |  
|  `filters`  |  `MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)") | None`  |  Optional MetadataFilters to filter nodes for deletion.  |  `None`  |  
|  `**delete_kwargs`  |  Additional keyword arguments.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurepostgresql/llama_index/vector_stores/azure_postgres/base.py`  
| 
```
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
```
 | 
```
@override
defdelete_nodes(
    self,
    node_ids: list[str] | None = None,
    filters: MetadataFilters | None = None,
    **delete_kwargs: Any,
) -> None:
"""Delete nodes from the vector store by node IDs or filters.

    Args:
        node_ids: Optional list of node IDs to delete.
        filters: Optional MetadataFilters to filter nodes for deletion.
        **delete_kwargs: Additional keyword arguments.
    """
    if not node_ids:
        return

    self._delete_rows_from_table(
        ids=node_ids, filters=metadata_filters_to_sql(filters), **delete_kwargs
    )

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azure_postgres/#llama_index.vector_stores.azure_postgres.AzurePGVectorStore.clear "Permanent link")

```
clear() -> None

```

Clear all data from the vector store table.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurepostgresql/llama_index/vector_stores/azure_postgres/base.py`  
| 
```
347
348
349
350
351
352
353
354
355
356
357
358
```
 | 
```
@override
defclear(self) -> None:
"""Clear all data from the vector store table."""
    with self.connection_pool.connection() as conn:
        register_vector(conn)
        with conn.cursor(row_factory=dict_row) as cursor:
            stmt = sql.SQL("TRUNCATE TABLE {schema}.{table}").format(
                schema=sql.Identifier(self.schema_name),
                table=sql.Identifier(self.table_name),
            )
            cursor.execute(stmt)
            conn.commit()

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azure_postgres/#llama_index.vector_stores.azure_postgres.AzurePGVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: [] | None = None,
    filters:  | None = None,
    **kwargs: 
) -> []

```

Retrieve nodes by IDs or filters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `list[str] | None`  |  Optional list of node IDs to retrieve.  |  `None`  |  
|  `filters`  |  `MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)") | None`  |  Optional MetadataFilters to filter nodes.  |  `None`  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List of BaseNode objects matching the criteria.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurepostgresql/llama_index/vector_stores/azure_postgres/base.py`  
| 
```
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
```
 | 
```
@override
defget_nodes(
    self,
    node_ids: list[str] | None = None,
    filters: MetadataFilters | None = None,
    **kwargs: Any,
) -> list[BaseNode]:
"""Retrieve nodes by IDs or filters.

    Args:
        node_ids: Optional list of node IDs to retrieve.
        filters: Optional MetadataFilters to filter nodes.
        **kwargs: Additional keyword arguments.

    Returns:
        List of BaseNode objects matching the criteria.
    """
    # TODO: Implement filter handling
    documents = self._get_by_ids(node_ids)
    nodes = []
    for doc in documents:
        node = self._table_row_to_node(doc)
        nodes.append(node)

    return nodes

```
 |  
| --- | --- |  
options: members: - AzurePostgreSQLVectorStore
