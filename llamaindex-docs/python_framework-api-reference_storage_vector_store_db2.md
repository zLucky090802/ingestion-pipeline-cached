# Db2
##  DB2LlamaVS [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/db2/#llama_index.vector_stores.db2.DB2LlamaVS "Permanent link")
Bases: 
`DB2LlamaVS` vector store.
To use, you should have both: - the `ibm_db` python package installed - a connection to db2 database with vector store feature (v12.1.2+)
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-db2/llama_index/vector_stores/db2/base.py`  
| 
```
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
```
 | 
```
classDB2LlamaVS(BasePydanticVectorStore):
"""
    `DB2LlamaVS` vector store.

    To use, you should have both:
    - the ``ibm_db`` python package installed
    - a connection to db2 database with vector store feature (v12.1.2+)
    """

    metadata_column: str = "metadata"
    stores_text: bool = True
    _client: Connection = PrivateAttr()
    table_name: str
    distance_strategy: DistanceStrategy
    batch_size: Optional[int]
    params: Optional[dict[str, Any]]
    embed_dim: int

    def__init__(
        self,
        _client: Connection,
        table_name: str,
        distance_strategy: DistanceStrategy = DistanceStrategy.EUCLIDEAN_DISTANCE,
        batch_size: Optional[int] = 32,
        embed_dim: int = 1536,
        params: Optional[dict[str, Any]] = None,
    ):
        try:
            importibm_db_dbi
        except ImportError as e:
            raise ImportError(
                "Unable to import ibm_db_dbi, please install with "
                "`pip install -U ibm_db`."
            ) frome

        try:
"""Initialize with necessary components."""
            super().__init__(
                table_name=table_name,
                distance_strategy=distance_strategy,
                batch_size=batch_size,
                embed_dim=embed_dim,
                params=params,
            )
            # Assign _client to PrivateAttr after the Pydantic initialization
            object.__setattr__(self, "_client", _client)
            create_table(_client, table_name, embed_dim)

        except ibm_db_dbi.DatabaseError as db_err:
            logger.exception(f"Database error occurred while create table: {db_err}")
            raise RuntimeError(
                "Failed to create table due to a database error."
            ) fromdb_err
        except ValueError as val_err:
            logger.exception(f"Validation error: {val_err}")
            raise RuntimeError(
                "Failed to create table due to a validation error."
            ) fromval_err
        except Exception as ex:
            logger.exception("An unexpected error occurred while creating the index.")
            raise RuntimeError(
                "Failed to create table due to an unexpected error."
            ) fromex

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._client

    @classmethod
    defclass_name(cls) -> str:
        return "DB2LlamaVS"

    def_append_meta_filter_condition(
        self, where_str: Optional[str], exact_match_filter: list
    ) -> str:
        filter_str = " AND ".join(
            f"JSON_VALUE({self.metadata_column}, '$.{filter_item.key}') = '{filter_item.value}'"
            for filter_item in exact_match_filter
        )
        if where_str is None:
            where_str = filter_str
        else:
            where_str += " AND " + filter_str
        return where_str

    def_build_insert(self, values: List[BaseNode]) -> List[tuple]:
        _data = []
        for item in values:
            item_values = tuple(
                column["extract_func"](item) for column in column_config.values()
            )
            _data.append(item_values)

        return _data

    def_build_query(
        self, distance_function: str, k: int, where_str: Optional[str] = None
    ) -> str:
        where_clause = f"WHERE {where_str}" if where_str else ""

        return f"""
            SELECT id,
                doc_id,
                text,
                SYSTOOLS.BSON2JSON(node_info),
                SYSTOOLS.BSON2JSON(metadata),
                vector_distance(embedding, VECTOR(?, {self.embed_dim}, FLOAT32), {distance_function}) AS distance
            FROM {self.table_name}
{where_clause}
            ORDER BY distance
            FETCH FIRST {k} ROWS ONLY
        """

    @_handle_exceptions
    defadd(self, nodes: list[BaseNode], **kwargs: Any) -> list[str]:
        if not nodes:
            return []

        for result_batch in iter_batch(nodes, self.batch_size):
            bind_values = self._build_insert(values=result_batch)

        dml = f"""
           INSERT INTO {self.table_name} ({", ".join(column_config.keys())})
           VALUES (?, ?, VECTOR(?, {self.embed_dim}, FLOAT32), SYSTOOLS.JSON2BSON(?), SYSTOOLS.JSON2BSON(?), ?)
        """

        cursor = self.client.cursor()
        try:
            # Use executemany to insert the batch
            cursor.executemany(dml, bind_values)
            cursor.execute("COMMIT")
        finally:
            cursor.close()

        return [node.node_id for node in nodes]

    @_handle_exceptions
    defdelete(self, ref_doc_id: str, **kwargs: Any) -> None:
        ddl = f"DELETE FROM {self.table_name} WHERE doc_id = '{ref_doc_id}'"
        cursor = self._client.cursor()
        try:
            cursor.execute(ddl)
            cursor.execute("COMMIT")
        finally:
            cursor.close()

    @_handle_exceptions
    defdrop(self) -> None:
        drop_table(self._client, self.table_name)

    @_handle_exceptions
    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        distance_function = _get_distance_function(self.distance_strategy)
        where_str = (
            f"doc_id in {_stringify_list(query.doc_ids)}" if query.doc_ids else None
        )

        if query.filters is not None:
            where_str = self._append_meta_filter_condition(
                where_str, query.filters.filters
            )

        # build query sql
        query_sql = self._build_query(
            distance_function, query.similarity_top_k, where_str
        )

        embedding = f"{query.query_embedding}"
        cursor = self._client.cursor()
        try:
            cursor.execute(query_sql, [embedding])
            results = cursor.fetchall()
        finally:
            cursor.close()

        similarities = []
        ids = []
        nodes = []
        for result in results:
            doc_id = result[1]
            text = result[2] if result[2] is not None else ""
            node_info = json.loads(result[3] if result[3] is not None else "{}")
            metadata = json.loads(result[4] if result[4] is not None else "{}")

            if query.node_ids:
                if result[0] not in query.node_ids:
                    continue

            if isinstance(node_info, dict):
                start_char_idx = node_info.get("start", None)
                end_char_idx = node_info.get("end", None)
            try:
                node = metadata_dict_to_node(metadata)
                node.set_content(text)
            except Exception:
                # Note: deprecated legacy logic for backward compatibility

                node = TextNode(
                    id_=result[0],
                    text=text,
                    metadata=metadata,
                    start_char_idx=start_char_idx,
                    end_char_idx=end_char_idx,
                    relationships={
                        NodeRelationship.SOURCE: RelatedNodeInfo(node_id=doc_id)
                    },
                )

            nodes.append(node)
            similarities.append(1.0 - math.exp(-result[5]))
            ids.append(result[0])
        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    @classmethod
    @_handle_exceptions
    deffrom_documents(
        cls: Type[DB2LlamaVS],
        docs: List[BaseNode],
        table_name: str = "llama_index",
        **kwargs: Any,
    ) -> DB2LlamaVS:
"""Return VectorStore initialized from texts and embeddings."""
        _client = kwargs.get("client")
        if _client is None:
            raise ValueError("client parameter is required...")
        params = kwargs.get("params")
        distance_strategy = kwargs.get("distance_strategy")
        drop_table(_client, table_name)
        embed_dim = kwargs.get("embed_dim")

        vss = cls(
            _client=_client,
            table_name=table_name,
            params=params,
            distance_strategy=distance_strategy,
            embed_dim=embed_dim,
        )
        vss.add(nodes=docs)
        return vss

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/db2/#llama_index.vector_stores.db2.DB2LlamaVS.client "Permanent link")

```
client: 

```

Get client.
###  from_documents `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/db2/#llama_index.vector_stores.db2.DB2LlamaVS.from_documents "Permanent link")

```
from_documents(
    docs: [],
    table_name:  = "llama_index",
    **kwargs: 
) -> 

```

Return VectorStore initialized from texts and embeddings.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-db2/llama_index/vector_stores/db2/base.py`  
| 
```
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
```
 | 
```
@classmethod
@_handle_exceptions
deffrom_documents(
    cls: Type[DB2LlamaVS],
    docs: List[BaseNode],
    table_name: str = "llama_index",
    **kwargs: Any,
) -> DB2LlamaVS:
"""Return VectorStore initialized from texts and embeddings."""
    _client = kwargs.get("client")
    if _client is None:
        raise ValueError("client parameter is required...")
    params = kwargs.get("params")
    distance_strategy = kwargs.get("distance_strategy")
    drop_table(_client, table_name)
    embed_dim = kwargs.get("embed_dim")

    vss = cls(
        _client=_client,
        table_name=table_name,
        params=params,
        distance_strategy=distance_strategy,
        embed_dim=embed_dim,
    )
    vss.add(nodes=docs)
    return vss

```
 |  
| --- | --- |  
options: members: - OraLlamaVS
