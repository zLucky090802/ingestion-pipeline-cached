# Mariadb
##  MariaDBVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mariadb/#llama_index.vector_stores.mariadb.MariaDBVectorStore "Permanent link")
Bases: 
MariaDB Vector Store.
Examples:
`pip install llama-index-vector-stores-mariadb`

```
fromllama_index.vector_stores.mariadbimport MariaDBVectorStore

# Create MariaDBVectorStore instance
vector_store = MariaDBVectorStore.from_params(
    host="localhost",
    port=3306,
    user="llamaindex",
    password="password",
    database="vectordb",
    table_name="llama_index_vectorstore",
    default_m=6,
    ef_search=20,
    embed_dim=1536  # OpenAI embedding dimension
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mariadb/llama_index/vector_stores/mariadb/base.py`  
| 
```
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
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
```
 | 
```
classMariaDBVectorStore(BasePydanticVectorStore):
"""
    MariaDB Vector Store.

    Examples:
        `pip install llama-index-vector-stores-mariadb`

        ```python
        from llama_index.vector_stores.mariadb import MariaDBVectorStore

        # Create MariaDBVectorStore instance
        vector_store = MariaDBVectorStore.from_params(
            host="localhost",
            port=3306,
            user="llamaindex",
            password="password",
            database="vectordb",
            table_name="llama_index_vectorstore",
            default_m=6,
            ef_search=20,
            embed_dim=1536  # OpenAI embedding dimension

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    connection_string: str
    connection_args: Dict[str, Any]
    table_name: str
    schema_name: str
    embed_dim: int
    default_m: int
    ef_search: int
    perform_setup: bool
    debug: bool

    _engine: Any = PrivateAttr()
    _is_initialized: bool = PrivateAttr(default=False)

    def__init__(
        self,
        connection_string: Union[str, sqlalchemy.engine.URL],
        connection_args: Dict[str, Any],
        table_name: str,
        schema_name: str,
        embed_dim: int = 1536,
        default_m: int = 6,
        ef_search: int = 20,
        perform_setup: bool = True,
        debug: bool = False,
    ) -> None:
"""
        Constructor.

        Args:
            connection_string (Union[str, sqlalchemy.engine.URL]): Connection string for the MariaDB server.
            connection_args (Dict[str, Any]): A dictionary of connection options.
            table_name (str): Table name.
            schema_name (str): Schema name.
            embed_dim (int, optional): Embedding dimensions. Defaults to 1536.
            default_m (int, optional): Default M value for the vector index. Defaults to 6.
            ef_search (int, optional): EF search value for the vector index. Defaults to 20.
            perform_setup (bool, optional): If DB should be set up. Defaults to True.
            debug (bool, optional): Debug mode. Defaults to False.

        """
        super().__init__(
            connection_string=connection_string,
            connection_args=connection_args,
            table_name=table_name,
            schema_name=schema_name,
            embed_dim=embed_dim,
            default_m=default_m,
            ef_search=ef_search,
            perform_setup=perform_setup,
            debug=debug,
        )

        self._initialize()

    defclose(self) -> None:
        if not self._is_initialized:
            return

        self._engine.dispose()
        self._is_initialized = False

    @classmethod
    defclass_name(cls) -> str:
        return "MariaDBVectorStore"

    @classmethod
    deffrom_params(
        cls,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        table_name: str = "llamaindex",
        schema_name: str = "public",
        connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
        connection_args: Optional[Dict[str, Any]] = None,
        embed_dim: int = 1536,
        default_m: int = 6,
        ef_search: int = 20,
        perform_setup: bool = True,
        debug: bool = False,
    ) -> "MariaDBVectorStore":
"""
        Construct from params.

        Args:
            host (Optional[str], optional): Host of MariaDB connection. Defaults to None.
            port (Optional[str], optional): Port of MariaDB connection. Defaults to None.
            database (Optional[str], optional): MariaDB DB name. Defaults to None.
            user (Optional[str], optional): MariaDB username. Defaults to None.
            password (Optional[str], optional): MariaDB password. Defaults to None.
            table_name (str): Table name. Defaults to "llamaindex".
            schema_name (str): Schema name. Defaults to "public".
            connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to MariaDB DB.
            connection_args (Dict[str, Any], optional): A dictionary of connection options.
            embed_dim (int, optional): Embedding dimensions. Defaults to 1536.
            default_m (int, optional): Default M value for the vector index. Defaults to 6.
            ef_search (int, optional): EF search value for the vector index. Defaults to 20.
            perform_setup (bool, optional): If DB should be set up. Defaults to True.
            debug (bool, optional): Debug mode. Defaults to False.

        Returns:
            MariaDBVectorStore: Instance of MariaDBVectorStore constructed from params.

        """
        conn_str = (
            connection_string
            or f"mysql+pymysql://{user}:{quote_plus(password)}@{host}:{port}/{database}"
        )
        conn_args = connection_args or {
            "ssl": {"ssl_mode": "PREFERRED"},
            "read_timeout": 30,
        }

        return cls(
            connection_string=conn_str,
            connection_args=conn_args,
            table_name=table_name,
            schema_name=schema_name,
            embed_dim=embed_dim,
            default_m=default_m,
            ef_search=ef_search,
            perform_setup=perform_setup,
            debug=debug,
        )

    @property
    defclient(self) -> Any:
        if not self._is_initialized:
            return None
        return self._engine

    def_connect(self) -> Any:
        self._engine = sqlalchemy.create_engine(
            self.connection_string, connect_args=self.connection_args, echo=self.debug
        )

    def_validate_server_version(self) -> None:
"""Validate that the MariaDB server version is supported."""
        with self._engine.connect() as connection:
            result = connection.execute(sqlalchemy.text("SELECT VERSION()"))
            version = result.fetchone()[0]

            if not _meets_min_server_version(version, "11.7.1"):
                raise ValueError(
                    f"MariaDB version 11.7.1 or later is required, found version: {version}."
                )

    def_create_table_if_not_exists(self) -> None:
        with self._engine.connect() as connection:
            # Note that we define the vector index with DISTANCE=cosine, because we use VEC_DISTANCE_COSINE.
            # This is because searches using a different distance function do not use the vector index.
            # Reference: https://mariadb.com/kb/en/create-table-with-vectors/
            stmt = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                id SERIAL PRIMARY KEY,
                node_id VARCHAR(255) NOT NULL,
                text TEXT,
                metadata JSON,
                embedding VECTOR({self.embed_dim}) NOT NULL,
                INDEX (`node_id`),
                VECTOR INDEX (embedding) M={self.default_m} DISTANCE=cosine


            connection.execute(sqlalchemy.text(stmt))

            connection.commit()

    def_initialize(self) -> None:
        if not self._is_initialized:
            self._connect()
            if self.perform_setup:
                self._validate_server_version()
                self._create_table_if_not_exists()
            self._is_initialized = True

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""Get nodes from vector store."""
        self._initialize()

        stmt = f"""SELECT text, metadata FROM `{self.table_name}` WHERE node_id IN :node_ids"""

        with self._engine.connect() as connection:
            result = connection.execute(sqlalchemy.text(stmt), {"node_ids": node_ids})

        nodes: List[BaseNode] = []
        for item in result:
            node = metadata_dict_to_node(json.loads(item.metadata))
            node.set_content(str(item.text))
            nodes.append(node)

        return nodes

    def_node_to_table_row(self, node: BaseNode) -> Dict[str, Any]:
        return {
            "node_id": node.node_id,
            "text": node.get_content(metadata_mode=MetadataMode.NONE),
            "embedding": node.get_embedding(),
            "metadata": node_to_metadata_dict(
                node,
                remove_text=True,
                flat_metadata=self.flat_metadata,
            ),
        }

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
        self._initialize()

        ids = []
        with self._engine.connect() as connection:
            for node in nodes:
                ids.append(node.node_id)
                item = self._node_to_table_row(node)
                stmt = sqlalchemy.text(
                    f"""
                INSERT INTO `{self.table_name}` (node_id, text, embedding, metadata)
                VALUES (
                    :node_id,
                    :text,
                    VEC_FromText(:embedding),
                    :metadata


                )
                connection.execute(
                    stmt,
                    {
                        "node_id": item["node_id"],
                        "text": item["text"],
                        "embedding": json.dumps(item["embedding"]),
                        "metadata": json.dumps(item["metadata"]),
                    },
                )

            connection.commit()

        return ids

    def_to_mariadb_operator(self, operator: FilterOperator) -> str:
        if operator == FilterOperator.EQ:
            return "="
        elif operator == FilterOperator.GT:
            return ">"
        elif operator == FilterOperator.LT:
            return "<"
        elif operator == FilterOperator.NE:
            return "!="
        elif operator == FilterOperator.GTE:
            return ">="
        elif operator == FilterOperator.LTE:
            return "<="
        elif operator == FilterOperator.IN:
            return "IN"
        elif operator == FilterOperator.NIN:
            return "NOT IN"
        else:
            _logger.warning("Unsupported operator: %s, fallback to '='", operator)
            return "="

    def_build_filter_clause(self, filter_: MetadataFilter) -> str:
        filter_value = filter_.value
        if filter_.operator in [FilterOperator.IN, FilterOperator.NIN]:
            values = []
            for v in filter_.value:
                if isinstance(v, str):
                    value = f"'{v}'"

                values.append(value)
            filter_value = ", ".join(values)
            filter_value = f"({filter_value})"
        elif isinstance(filter_.value, str):
            filter_value = f"'{filter_.value}'"

        return f"JSON_VALUE(metadata, '$.{filter_.key}') {self._to_mariadb_operator(filter_.operator)}{filter_value}"

    def_filters_to_where_clause(self, filters: MetadataFilters) -> str:
        conditions = {
            FilterCondition.OR: "OR",
            FilterCondition.AND: "AND",
        }
        if filters.condition not in conditions:
            raise ValueError(
                f"Unsupported condition: {filters.condition}. "
                f"Must be one of {list(conditions.keys())}"
            )

        clauses: List[str] = []
        for filter_ in filters.filters:
            if isinstance(filter_, MetadataFilter):
                clauses.append(self._build_filter_clause(filter_))
                continue

            if isinstance(filter_, MetadataFilters):
                subfilters = self._filters_to_where_clause(filter_)
                if subfilters:
                    clauses.append(f"({subfilters})")
                continue

            raise ValueError(
                f"Unsupported filter type: {type(filter_)}. Must be one of {MetadataFilter}, {MetadataFilters}"
            )
        return f" {conditions[filters.condition]} ".join(clauses)

    def_db_rows_to_query_result(
        self, rows: List[DBEmbeddingRow]
    ) -> VectorStoreQueryResult:
        nodes = []
        similarities = []
        ids = []
        for db_embedding_row in rows:
            node = metadata_dict_to_node(db_embedding_row.metadata)
            node.set_content(str(db_embedding_row.text))

            similarities.append(db_embedding_row.similarity)
            ids.append(db_embedding_row.node_id)
            nodes.append(node)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities,
            ids=ids,
        )

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        if query.mode != VectorStoreQueryMode.DEFAULT:
            raise NotImplementedError(f"Query mode {query.mode} not available.")

        self._initialize()

        stmt = f"""
        SET STATEMENT mhnsw_ef_search={self.ef_search} FOR
        SELECT
            node_id,
            text,
            embedding,
            metadata,
            VEC_DISTANCE_COSINE(embedding, VEC_FromText('{query.query_embedding}')) AS distance
        FROM `{self.table_name}`"""

        if query.filters:
            stmt += f"""
        WHERE {self._filters_to_where_clause(query.filters)}"""

        stmt += f"""
        ORDER BY distance
        LIMIT {query.similarity_top_k}
        """

        with self._engine.connect() as connection:
            result = connection.execute(sqlalchemy.text(stmt))

        results = []
        for item in result:
            results.append(
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=json.loads(item.metadata),
                    similarity=(1 - item.distance) if item.distance is not None else 0,
                )
            )

        return self._db_rows_to_query_result(results)

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        self._initialize()

        with self._engine.connect() as connection:
            # Should we create an index on ref_doc_id?
            stmt = f"""DELETE FROM `{self.table_name}` WHERE JSON_EXTRACT(metadata, '$.ref_doc_id') = :doc_id"""
            connection.execute(sqlalchemy.text(stmt), {"doc_id": ref_doc_id})

            connection.commit()

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
        self._initialize()

        with self._engine.connect() as connection:
            stmt = f"""DELETE FROM `{self.table_name}` WHERE node_id IN :node_ids"""
            connection.execute(sqlalchemy.text(stmt), {"node_ids": node_ids})

            connection.commit()

    defcount(self) -> int:
        self._initialize()

        with self._engine.connect() as connection:
            stmt = f"""SELECT COUNT(*) FROM `{self.table_name}`"""
            result = connection.execute(sqlalchemy.text(stmt))

        return result.scalar() or 0

    defdrop(self) -> None:
        self._initialize()

        with self._engine.connect() as connection:
            stmt = f"""DROP TABLE IF EXISTS `{self.table_name}`"""
            connection.execute(sqlalchemy.text(stmt))

            connection.commit()

        self.close()

    defclear(self) -> None:
        self._initialize()

        with self._engine.connect() as connection:
            stmt = f"""DELETE FROM `{self.table_name}`"""
            connection.execute(sqlalchemy.text(stmt))

            connection.commit()

```
 |  
| --- | --- |  
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mariadb/#llama_index.vector_stores.mariadb.MariaDBVectorStore.from_params "Permanent link")

```
from_params(
    host: Optional[] = None,
    port: Optional[] = None,
    database: Optional[] = None,
    user: Optional[] = None,
    password: Optional[] = None,
    table_name:  = "llamaindex",
    schema_name:  = "public",
    connection_string: Optional[Union[, ]] = None,
    connection_args: Optional[[, ]] = None,
    embed_dim:  = 1536,
    default_m:  = 6,
    ef_search:  = 20,
    perform_setup:  = True,
    debug:  = False,
) -> 

```

Construct from params.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  `Optional[str]`  |  Host of MariaDB connection. Defaults to None.  |  `None`  |  
|  `port`  |  `Optional[str]`  |  Port of MariaDB connection. Defaults to None.  |  `None`  |  
|  `database`  |  `Optional[str]`  |  MariaDB DB name. Defaults to None.  |  `None`  |  
|  `user`  |  `Optional[str]`  |  MariaDB username. Defaults to None.  |  `None`  |  
|  `password`  |  `Optional[str]`  |  MariaDB password. Defaults to None.  |  `None`  |  
|  `table_name`  |  Table name. Defaults to "llamaindex".  |  `'llamaindex'`  |  
|  `schema_name`  |  Schema name. Defaults to "public".  |  `'public'`  |  
|  `connection_string`  |  `Union[str, URL]`  |  Connection string to MariaDB DB.  |  `None`  |  
|  `connection_args`  |  `Dict[str, Any]`  |  A dictionary of connection options.  |  `None`  |  
|  `embed_dim`  |  Embedding dimensions. Defaults to 1536.  |  `1536`  |  
|  `default_m`  |  Default M value for the vector index. Defaults to 6.  |  
|  `ef_search`  |  EF search value for the vector index. Defaults to 20.  |  
|  `perform_setup`  |  `bool`  |  If DB should be set up. Defaults to True.  |  `True`  |  
|  `debug`  |  `bool`  |  Debug mode. Defaults to False.  |  `False`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `MariaDBVectorStore`  |   |  Instance of MariaDBVectorStore constructed from params.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mariadb/llama_index/vector_stores/mariadb/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_params(
    cls,
    host: Optional[str] = None,
    port: Optional[str] = None,
    database: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    table_name: str = "llamaindex",
    schema_name: str = "public",
    connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
    connection_args: Optional[Dict[str, Any]] = None,
    embed_dim: int = 1536,
    default_m: int = 6,
    ef_search: int = 20,
    perform_setup: bool = True,
    debug: bool = False,
) -> "MariaDBVectorStore":
"""
    Construct from params.

    Args:
        host (Optional[str], optional): Host of MariaDB connection. Defaults to None.
        port (Optional[str], optional): Port of MariaDB connection. Defaults to None.
        database (Optional[str], optional): MariaDB DB name. Defaults to None.
        user (Optional[str], optional): MariaDB username. Defaults to None.
        password (Optional[str], optional): MariaDB password. Defaults to None.
        table_name (str): Table name. Defaults to "llamaindex".
        schema_name (str): Schema name. Defaults to "public".
        connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to MariaDB DB.
        connection_args (Dict[str, Any], optional): A dictionary of connection options.
        embed_dim (int, optional): Embedding dimensions. Defaults to 1536.
        default_m (int, optional): Default M value for the vector index. Defaults to 6.
        ef_search (int, optional): EF search value for the vector index. Defaults to 20.
        perform_setup (bool, optional): If DB should be set up. Defaults to True.
        debug (bool, optional): Debug mode. Defaults to False.

    Returns:
        MariaDBVectorStore: Instance of MariaDBVectorStore constructed from params.

    """
    conn_str = (
        connection_string
        or f"mysql+pymysql://{user}:{quote_plus(password)}@{host}:{port}/{database}"
    )
    conn_args = connection_args or {
        "ssl": {"ssl_mode": "PREFERRED"},
        "read_timeout": 30,
    }

    return cls(
        connection_string=conn_str,
        connection_args=conn_args,
        table_name=table_name,
        schema_name=schema_name,
        embed_dim=embed_dim,
        default_m=default_m,
        ef_search=ef_search,
        perform_setup=perform_setup,
        debug=debug,
    )

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mariadb/#llama_index.vector_stores.mariadb.MariaDBVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes from vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mariadb/llama_index/vector_stores/mariadb/base.py`  
| 
```
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""Get nodes from vector store."""
    self._initialize()

    stmt = f"""SELECT text, metadata FROM `{self.table_name}` WHERE node_id IN :node_ids"""

    with self._engine.connect() as connection:
        result = connection.execute(sqlalchemy.text(stmt), {"node_ids": node_ids})

    nodes: List[BaseNode] = []
    for item in result:
        node = metadata_dict_to_node(json.loads(item.metadata))
        node.set_content(str(item.text))
        nodes.append(node)

    return nodes

```
 |  
| --- | --- |  
options: members: - MariaDBVectorStore
