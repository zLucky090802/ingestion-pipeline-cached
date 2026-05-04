# Falkordb
##  FalkorDBGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBGraphStore "Permanent link")
Bases: 
FalkorDB Graph Store.
In this graph store, triplets are stored within FalkorDB.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `simple_graph_store_data_dict`  |  `Optional[dict]`  |  data dict containing the triplets. See FalkorDBGraphStoreData for more details.  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/base.py`  
| 
```
 13
 14
 15
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
```
 | 
```
classFalkorDBGraphStore(GraphStore):
"""
    FalkorDB Graph Store.

    In this graph store, triplets are stored within FalkorDB.

    Args:
        simple_graph_store_data_dict (Optional[dict]): data dict
            containing the triplets. See FalkorDBGraphStoreData
            for more details.

    """

    def__init__(
        self,
        url: str,
        database: str = "falkor",
        node_label: str = "Entity",
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._node_label = node_label

        self._driver = FalkorDB.from_url(url)
        self._graph = self._driver.select_graph(database)

        try:
            self._graph.query(f"CREATE INDEX FOR (n:`{self._node_label}`) ON (n.id)")
        except redis.ResponseError as e:
            # TODO: to find an appropriate way to handle this issue.
            logger.warning("Create index failed: %s", e)

        self._database = database

        self.schema = ""
        self.get_query = f"""
            MATCH (n1:`{self._node_label}`)-[r]->(n2:`{self._node_label}`)
            WHERE n1.id = $subj RETURN type(r), n2.id
        """

    @property
    defclient(self) -> None:
        return self._graph

    defget(self, subj: str) -> List[List[str]]:
"""Get triplets."""
        result = self._graph.query(self.get_query, params={"subj": subj})
        return result.result_set

    defget_rel_map(
        self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
    ) -> Dict[str, List[List[str]]]:
"""Get flat rel map."""
        # The flat means for multi-hop relation path, we could get
        # knowledge like: subj -> rel -> obj -> rel -> obj -> rel -> obj.
        # This type of knowledge is useful for some tasks.
        # +-------------+------------------------------------+
        # | subj        | flattened_rels                     |
        # +-------------+------------------------------------+
        # | "player101" | [95, "player125", 2002, "team204"] |
        # | "player100" | [1997, "team204"]                  |
        # ...
        # +-------------+------------------------------------+

        rel_map: Dict[Any, List[Any]] = {}
        if subjs is None or len(subjs) == 0:
            # unlike simple graph_store, we don't do get_all here
            return rel_map

        query = f"""
            MATCH (n1:{self._node_label})
            WHERE n1.id IN $subjs
            WITH n1
            MATCH p=(n1)-[e*1..{depth}]->(z)
            RETURN p LIMIT {limit}
        """

        data = self.query(query, params={"subjs": subjs})
        if not data:
            return rel_map

        for record in data:
            nodes = record[0].nodes()
            edges = record[0].edges()

            subj_id = nodes[0].properties["id"]
            path = []
            for i, edge in enumerate(edges):
                dest = nodes[i + 1]
                dest_id = dest.properties["id"]
                path.append(edge.relation)
                path.append(dest_id)

            paths = rel_map[subj_id] if subj_id in rel_map else []
            paths.append(path)
            rel_map[subj_id] = paths

        return rel_map

    defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
        query = """
            MERGE (n1:`%s` {id:$subj})
            MERGE (n2:`%s` {id:$obj})
            MERGE (n1)-[:`%s`]->(n2)
        """

        prepared_statement = query % (
            self._node_label,
            self._node_label,
            rel.replace(" ", "_").upper(),
        )

        # Call FalkorDB with prepared statement
        self._graph.query(prepared_statement, params={"subj": subj, "obj": obj})

    defdelete(self, subj: str, rel: str, obj: str) -> None:
"""Delete triplet."""

        defdelete_rel(subj: str, obj: str, rel: str) -> None:
            rel = rel.replace(" ", "_").upper()
            query = f"""
                MATCH (n1:`{self._node_label}`)-[r:`{rel}`]->(n2:`{self._node_label}`)
                WHERE n1.id = $subj AND n2.id = $obj DELETE r


            # Call FalkorDB with prepared statement
            self._graph.query(query, params={"subj": subj, "obj": obj})

        defdelete_entity(entity: str) -> None:
            query = f"MATCH (n:`{self._node_label}`) WHERE n.id = $entity DELETE n"

            # Call FalkorDB with prepared statement
            self._graph.query(query, params={"entity": entity})

        defcheck_edges(entity: str) -> bool:
            query = f"""
                MATCH (n1:`{self._node_label}`)--()
                WHERE n1.id = $entity RETURN count(*)


            # Call FalkorDB with prepared statement
            result = self._graph.query(query, params={"entity": entity})
            return bool(result.result_set)

        delete_rel(subj, obj, rel)
        if not check_edges(subj):
            delete_entity(subj)
        if not check_edges(obj):
            delete_entity(obj)

    defrefresh_schema(self) -> None:
"""
        Refreshes the FalkorDB graph schema information.
        """
        node_properties = self.query("CALL DB.PROPERTYKEYS()")
        relationships = self.query("CALL DB.RELATIONSHIPTYPES()")

        self.schema = f"""
        Properties: {node_properties}
        Relationships: {relationships}
        """

    defget_schema(self, refresh: bool = False) -> str:
"""Get the schema of the FalkorDBGraph store."""
        if self.schema and not refresh:
            return self.schema
        self.refresh_schema()
        logger.debug(f"get_schema() schema:\n{self.schema}")
        return self.schema

    defquery(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        result = self._graph.query(query, params=params)
        return result.result_set

    defswitch_graph(self, graph_name: str) -> None:
"""
        Switch to the given graph name (`graph_name`).

        This method allows users to change the active graph within the same
        database connection.

        Args:
            graph_name (str): The name of the graph to switch to.

        """
        self._graph = self._driver.select_graph(graph_name)

        try:
            self.refresh_schema()
        except Exception as e:
            raise ValueError(f"Could not refresh schema. Error: {e}")

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBGraphStore.get "Permanent link")

```
get(subj: ) -> [[]]

```

Get triplets.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/base.py`  
| 
```
57
58
59
60
```
 | 
```
defget(self, subj: str) -> List[List[str]]:
"""Get triplets."""
    result = self._graph.query(self.get_query, params={"subj": subj})
    return result.result_set

```
 |  
| --- | --- |  
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    subjs: Optional[[]] = None,
    depth:  = 2,
    limit:  = 30,
) -> [, [[]]]

```

Get flat rel map.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/base.py`  
| 
```
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
```
 | 
```
defget_rel_map(
    self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
) -> Dict[str, List[List[str]]]:
"""Get flat rel map."""
    # The flat means for multi-hop relation path, we could get
    # knowledge like: subj -> rel -> obj -> rel -> obj -> rel -> obj.
    # This type of knowledge is useful for some tasks.
    # +-------------+------------------------------------+
    # | subj        | flattened_rels                     |
    # +-------------+------------------------------------+
    # | "player101" | [95, "player125", 2002, "team204"] |
    # | "player100" | [1997, "team204"]                  |
    # ...
    # +-------------+------------------------------------+

    rel_map: Dict[Any, List[Any]] = {}
    if subjs is None or len(subjs) == 0:
        # unlike simple graph_store, we don't do get_all here
        return rel_map

    query = f"""
        MATCH (n1:{self._node_label})
        WHERE n1.id IN $subjs
        WITH n1
        MATCH p=(n1)-[e*1..{depth}]->(z)
        RETURN p LIMIT {limit}
    """

    data = self.query(query, params={"subjs": subjs})
    if not data:
        return rel_map

    for record in data:
        nodes = record[0].nodes()
        edges = record[0].edges()

        subj_id = nodes[0].properties["id"]
        path = []
        for i, edge in enumerate(edges):
            dest = nodes[i + 1]
            dest_id = dest.properties["id"]
            path.append(edge.relation)
            path.append(dest_id)

        paths = rel_map[subj_id] if subj_id in rel_map else []
        paths.append(path)
        rel_map[subj_id] = paths

    return rel_map

```
 |  
| --- | --- |  
###  upsert_triplet [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBGraphStore.upsert_triplet "Permanent link")

```
upsert_triplet(subj: , rel: , obj: ) -> None

```

Add triplet.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/base.py`  
| 
```
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
```
 | 
```
defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
    query = """
        MERGE (n1:`%s` {id:$subj})
        MERGE (n2:`%s` {id:$obj})
        MERGE (n1)-[:`%s`]->(n2)
    """

    prepared_statement = query % (
        self._node_label,
        self._node_label,
        rel.replace(" ", "_").upper(),
    )

    # Call FalkorDB with prepared statement
    self._graph.query(prepared_statement, params={"subj": subj, "obj": obj})

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBGraphStore.delete "Permanent link")

```
delete(subj: , rel: , obj: ) -> None

```

Delete triplet.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/base.py`  
| 
```
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
```
 | 
```
defdelete(self, subj: str, rel: str, obj: str) -> None:
"""Delete triplet."""

    defdelete_rel(subj: str, obj: str, rel: str) -> None:
        rel = rel.replace(" ", "_").upper()
        query = f"""
            MATCH (n1:`{self._node_label}`)-[r:`{rel}`]->(n2:`{self._node_label}`)
            WHERE n1.id = $subj AND n2.id = $obj DELETE r
        """

        # Call FalkorDB with prepared statement
        self._graph.query(query, params={"subj": subj, "obj": obj})

    defdelete_entity(entity: str) -> None:
        query = f"MATCH (n:`{self._node_label}`) WHERE n.id = $entity DELETE n"

        # Call FalkorDB with prepared statement
        self._graph.query(query, params={"entity": entity})

    defcheck_edges(entity: str) -> bool:
        query = f"""
            MATCH (n1:`{self._node_label}`)--()
            WHERE n1.id = $entity RETURN count(*)
        """

        # Call FalkorDB with prepared statement
        result = self._graph.query(query, params={"entity": entity})
        return bool(result.result_set)

    delete_rel(subj, obj, rel)
    if not check_edges(subj):
        delete_entity(subj)
    if not check_edges(obj):
        delete_entity(obj)

```
 |  
| --- | --- |  
###  refresh_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBGraphStore.refresh_schema "Permanent link")

```
refresh_schema() -> None

```

Refreshes the FalkorDB graph schema information.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/base.py`  
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
```
 | 
```
defrefresh_schema(self) -> None:
"""
    Refreshes the FalkorDB graph schema information.
    """
    node_properties = self.query("CALL DB.PROPERTYKEYS()")
    relationships = self.query("CALL DB.RELATIONSHIPTYPES()")

    self.schema = f"""
    Properties: {node_properties}
    Relationships: {relationships}
    """

```
 |  
| --- | --- |  
###  get_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBGraphStore.get_schema "Permanent link")

```
get_schema(refresh:  = False) -> 

```

Get the schema of the FalkorDBGraph store.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/base.py`  
| 
```
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
defget_schema(self, refresh: bool = False) -> str:
"""Get the schema of the FalkorDBGraph store."""
    if self.schema and not refresh:
        return self.schema
    self.refresh_schema()
    logger.debug(f"get_schema() schema:\n{self.schema}")
    return self.schema

```
 |  
| --- | --- |  
###  switch_graph [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBGraphStore.switch_graph "Permanent link")

```
switch_graph(graph_name: ) -> None

```

Switch to the given graph name (`graph_name`).
This method allows users to change the active graph within the same database connection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `graph_name`  |  The name of the graph to switch to.  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/base.py`  
| 
```
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
```
 | 
```
defswitch_graph(self, graph_name: str) -> None:
"""
    Switch to the given graph name (`graph_name`).

    This method allows users to change the active graph within the same
    database connection.

    Args:
        graph_name (str): The name of the graph to switch to.

    """
    self._graph = self._driver.select_graph(graph_name)

    try:
        self.refresh_schema()
    except Exception as e:
        raise ValueError(f"Could not refresh schema. Error: {e}")

```
 |  
| --- | --- |  
##  FalkorDBPropertyGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBPropertyGraphStore "Permanent link")
Bases: 
FalkorDB Property Graph Store.
This class implements a FalkorDB property graph store.
If you are using local FalkorDB instead of FalkorDB Cloud, here's a helpful command for launching the docker container:

```
dockerrun\
-p3000:3000-p6379:6379\
-v$PWD/data:/data\
falkordb/falkordb:latest

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  The URL for the FalkorDB database.  |  _required_  |  
|  `database`  |  `Optional[str]`  |  The name of the database to connect to. Defaults to "falkor".  |  `'falkor'`  |  
Examples:
`pip install llama-index-graph-stores-falkordb`

```
fromllama_index.core.indices.property_graphimport PropertyGraphIndex
fromllama_index.graph_stores.falkordbimport FalkorDBPropertyGraphStore

# Create a FalkorDBPropertyGraphStore instance
graph_store = FalkorDBPropertyGraphStore(
    url="falkordb://localhost:6379",
    database="falkor"
)

# create the index
index = PropertyGraphIndex.from_documents(
    documents,
    property_graph_store=graph_store,
)

```

Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/falkordb_property_graph.py`  
| 
```
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
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
```
 | 
```
classFalkorDBPropertyGraphStore(PropertyGraphStore):
r"""
    FalkorDB Property Graph Store.

    This class implements a FalkorDB property graph store.

    If you are using local FalkorDB instead of FalkorDB Cloud, here's a helpful
    command for launching the docker container:

    ```bash
    docker run \
        -p 3000:3000 -p 6379:6379 \
        -v $PWD/data:/data \
        falkordb/falkordb:latest
    ```

    Args:
        url (str): The URL for the FalkorDB database.
        database (Optional[str]): The name of the database to connect to. Defaults to "falkor".

    Examples:
        `pip install llama-index-graph-stores-falkordb`

        ```python
        from llama_index.core.indices.property_graph import PropertyGraphIndex
        from llama_index.graph_stores.falkordb import FalkorDBPropertyGraphStore

        # Create a FalkorDBPropertyGraphStore instance
        graph_store = FalkorDBPropertyGraphStore(
            url="falkordb://localhost:6379",
            database="falkor"


        # create the index
        index = PropertyGraphIndex.from_documents(
            documents,
            property_graph_store=graph_store,

        ```

    """

    supports_structured_queries: bool = True
    supports_vector_queries: bool = True
    text_to_cypher_template: PromptTemplate = DEFAULT_CYPHER_TEMPALTE

    def__init__(
        self,
        url: str,
        database: str = "falkor",
        refresh_schema: bool = True,
        sanitize_query_output: bool = True,
        **falkordb_kwargs: Any,
    ) -> None:
        self.sanitize_query_output = sanitize_query_output
        self._driver = FalkorDB.from_url(url)
        self._graph = self._driver.select_graph(database)
        self._database = database
        self.structured_schema = {}
        if refresh_schema:
            self.refresh_schema()

    @property
    defclient(self):
        return self._graph

    defrefresh_schema(self) -> None:
"""Refresh the schema."""
        node_query_results = self.structured_query(
            node_properties_query,
            param_map={"EXCLUDED_LABELS": [*EXCLUDED_LABELS, BASE_ENTITY_LABEL]},
        )
        node_properties = (
            [el["output"] for el in node_query_results] if node_query_results else []
        )

        rels_query_result = self.structured_query(
            rel_properties_query, param_map={"EXCLUDED_LABELS": EXCLUDED_RELS}
        )
        rel_properties = (
            [el["output"] for el in rels_query_result] if rels_query_result else []
        )

        rel_objs_query_result = self.structured_query(
            rel_query,
            param_map={"EXCLUDED_LABELS": [*EXCLUDED_LABELS, BASE_ENTITY_LABEL]},
        )
        relationships = (
            [el["output"] for el in rel_objs_query_result]
            if rel_objs_query_result
            else []
        )

        # Get constraints & indexes
        try:
            constraint = self.structured_query("CALL db.constraints()")
            index = self.structured_query(
                "CALL db.indexes() YIELD label, properties, entitytype RETURN *"
            )
        except (
            redis.exceptions.ResponseError
        ):  # Read-only user might not have access to schema information
            constraint = []
            index = []

        self.structured_schema = {
            "node_props": {el["label"]: el["keys"] for el in node_properties},
            "rel_props": {el["type"]: el["keys"] for el in rel_properties},
            "relationships": relationships,
            "metadata": {"constraint": constraint, "index": index},
        }

    defupsert_nodes(self, nodes: List[LabelledNode]) -> None:
        # Lists to hold separated types
        entity_dicts: List[dict] = []
        chunk_dicts: List[dict] = []

        # Sort by type
        for item in nodes:
            if isinstance(item, EntityNode):
                entity_dicts.append({**item.dict(), "id": item.id})
            elif isinstance(item, ChunkNode):
                chunk_dicts.append({**item.dict(), "id": item.id})
            else:
                # Log that we do not support these types of nodes
                # Or raise an error?
                pass

        if chunk_dicts:
            self.structured_query(
"""
                UNWIND $data AS row
                MERGE (c:Chunk {id: row.id})
                SET c.text = row.text
                WITH c, row
                SET c += row.properties
                WITH c, row.embedding AS embedding
                WHERE embedding IS NOT NULL
                SET c.embedding = vecf32(embedding)
                RETURN count(*)
,
                param_map={"data": chunk_dicts},
            )

        if entity_dicts:
            for entity_dict in entity_dicts:
                self.structured_query(
                    f"""
                    MERGE (e:`__Entity__` {{id: $data.id}})
                    SET e += $data.properties
                    SET e.name = $data.name
                    WITH e
                    SET e:{entity_dict["label"]}
                    WITH e
                    CALL {{
                        WITH e
                        WITH e
                        WHERE $data.embedding IS NOT NULL
                        SET e.embedding = vecf32($data.embedding)
                        RETURN count(*) AS count
}}
                    RETURN count(e) AS cnt
,
                    param_map={"data": entity_dict},
                )
                # Create MENTIONS relationship if entity has triplet_source_id
                triplet_source_id = entity_dict.get("properties", {}).get(
                    "triplet_source_id"
                )
                if triplet_source_id:
                    self.structured_query(
"""
                        MATCH (e:`__Entity__` {id: $entity_id})
                        MERGE (c:Chunk {id: $chunk_id})
                        MERGE (e)<-[:MENTIONS]-(c)
,
                        param_map={
                            "entity_id": entity_dict["id"],
                            "chunk_id": triplet_source_id,
                        },
                    )

    defupsert_relations(self, relations: List[Relation]) -> None:
"""Add relations."""
        params = [r.dict() for r in relations]

        for param in params:
            self.structured_query(
                f"""
                MERGE (source {{id: $data.source_id}})
                ON CREATE SET source:Chunk
                MERGE (target {{id: $data.target_id}})
                ON CREATE SET target:Chunk
                WITH source, target
                CREATE (source)-[r:`{param["label"]}`]->(target)
                SET r += $data.properties
                RETURN count(*)
,
                param_map={"data": param},
            )

    defget(
        self,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[LabelledNode]:
"""Get nodes."""
        cypher_statement = "MATCH (e) "

        params = {}
        if properties or ids:
            cypher_statement += "WHERE "

        if ids:
            cypher_statement += "e.id in $ids "
            params["ids"] = ids

        if properties:
            prop_list = []
            for i, prop in enumerate(properties):
                prop_list.append(f"e.`{prop}` = $property_{i}")
                params[f"property_{i}"] = properties[prop]
            cypher_statement += " AND ".join(prop_list)

        return_statement = """
        WITH e
        RETURN e.id AS name,
               [l in labels(e) WHERE l <> '__Entity__' | l][0] AS type,
               e{.* , embedding: Null, id: Null} AS properties
        """
        cypher_statement += return_statement

        response = self.structured_query(cypher_statement, param_map=params)
        response = response if response else []

        nodes = []
        for record in response:
            # text indicates a chunk node
            # none on the type indicates an implicit node, likely a chunk node
            if "text" in record["properties"] or record["type"] is None:
                text = record["properties"].pop("text", "")
                nodes.append(
                    ChunkNode(
                        id_=record["name"],
                        text=text,
                        properties=remove_empty_values(record["properties"]),
                    )
                )
            else:
                nodes.append(
                    EntityNode(
                        name=record["name"],
                        label=record["type"],
                        properties=remove_empty_values(record["properties"]),
                    )
                )

        return nodes

    defget_triplets(
        self,
        entity_names: Optional[List[str]] = None,
        relation_names: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[Triplet]:
        # TODO: handle ids of chunk nodes
        cypher_statement = "MATCH (e:`__Entity__`) "

        params = {}
        if entity_names or properties or ids:
            cypher_statement += "WHERE "

        if entity_names:
            cypher_statement += "e.name in $entity_names "
            params["entity_names"] = entity_names

        if ids:
            cypher_statement += "e.id in $ids "
            params["ids"] = ids

        if properties:
            prop_list = []
            for i, prop in enumerate(properties):
                prop_list.append(f"e.`{prop}` = $property_{i}")
                params[f"property_{i}"] = properties[prop]
            cypher_statement += " AND ".join(prop_list)

        return_statement = f"""
        WITH e
        CALL {{
            WITH e
            MATCH (e)-[r{":`"+"`|`".join(relation_names)+"`"ifrelation_nameselse""}]->(t:__Entity__)
            RETURN e.name AS source_id, [l in labels(e) WHERE l <> '__Entity__' | l][0] AS source_type,
{{.* , embedding: Null, name: Null}} AS source_properties,
                   type(r) AS type,
                   t.name AS target_id, [l in labels(t) WHERE l <> '__Entity__' | l][0] AS target_type,
{{.* , embedding: Null, name: Null}} AS target_properties
            UNION ALL
            WITH e
            MATCH (e)<-[r{":`"+"`|`".join(relation_names)+"`"ifrelation_nameselse""}]-(t:__Entity__)
            RETURN t.name AS source_id, [l in labels(t) WHERE l <> '__Entity__' | l][0] AS source_type,
{{.* , embedding: Null, name: Null}} AS source_properties,
                   type(r) AS type,
                   e.name AS target_id, [l in labels(e) WHERE l <> '__Entity__' | l][0] AS target_type,
{{.* , embedding: Null, name: Null}} AS target_properties
}}
        RETURN source_id, source_type, type, target_id, target_type, source_properties, target_properties"""
        cypher_statement += return_statement

        data = self.structured_query(cypher_statement, param_map=params)
        data = data if data else []

        triples = []
        for record in data:
            source = EntityNode(
                name=record["source_id"],
                label=record["source_type"],
                properties=remove_empty_values(record["source_properties"]),
            )
            target = EntityNode(
                name=record["target_id"],
                label=record["target_type"],
                properties=remove_empty_values(record["target_properties"]),
            )
            rel = Relation(
                source_id=record["source_id"],
                target_id=record["target_id"],
                label=record["type"],
            )
            triples.append([source, rel, target])
        return triples

    defget_rel_map(
        self,
        graph_nodes: List[LabelledNode],
        depth: int = 2,
        limit: int = 30,
        ignore_rels: Optional[List[str]] = None,
    ) -> List[Triplet]:
"""Get depth-aware rel map."""
        triples = []

        ids = [node.id for node in graph_nodes]
        # Needs some optimization
        response = self.structured_query(
            f"""
            WITH $ids AS id_list
            UNWIND range(0, size(id_list) - 1) AS idx
            MATCH (e:`__Entity__`)
            WHERE e.id = id_list[idx]
            MATCH p=(e)-[r*1..{depth}]-(other)
            WHERE ALL(rel in relationships(p) WHERE type(rel) <> 'MENTIONS')
            UNWIND relationships(p) AS rel
            WITH distinct rel, idx
            WITH startNode(rel) AS source,
                type(rel) AS type,
                endNode(rel) AS endNode,

            LIMIT $limit
            RETURN source.id AS source_id, [l in labels(source) WHERE l <> '__Entity__' | l][0] AS source_type,
                source{{.* , embedding: Null, id: Null}} AS source_properties,
                type,
                endNode.id AS target_id, [l in labels(endNode) WHERE l <> '__Entity__' | l][0] AS target_type,
                endNode{{.* , embedding: Null, id: Null}} AS target_properties,

            ORDER BY idx
            LIMIT $limit
,
            param_map={"ids": ids, "limit": limit},
        )
        response = response if response else []

        ignore_rels = ignore_rels or []
        for record in response:
            if record["type"] in ignore_rels:
                continue

            source = EntityNode(
                name=record["source_id"],
                label=record["source_type"],
                properties=remove_empty_values(record["source_properties"]),
            )
            target = EntityNode(
                name=record["target_id"],
                label=record["target_type"],
                properties=remove_empty_values(record["target_properties"]),
            )
            rel = Relation(
                source_id=record["source_id"],
                target_id=record["target_id"],
                label=record["type"],
            )
            triples.append([source, rel, target])

        return triples

    defstructured_query(
        self, query: str, param_map: Optional[Dict[str, Any]] = None
    ) -> Any:
        param_map = param_map or {}

        result = self._graph.query(query, param_map)
        full_result = [
            {h[1]: d[i] for i, h in enumerate(result.header)} for d in result.result_set
        ]

        if self.sanitize_query_output:
            return [value_sanitize(el) for el in full_result]
        return full_result

    defvector_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> Tuple[List[LabelledNode], List[float]]:
"""Query the graph store with a vector store query."""
        conditions = None
        if query.filters:
            conditions = [
                f"e.{filter.key}{filter.operator.value}{filter.value}"
                for filter in query.filters.filters
            ]
        filters = (
            f" {query.filters.condition.value} ".join(conditions).replace("==", "=")
            if conditions is not None
            else "1 = 1"
        )

        data = self.structured_query(
            f"""MATCH (e:`__Entity__`)
            WHERE e.embedding IS NOT NULL AND ({filters})
            WITH e, vec.euclideanDistance(e.embedding, vecf32($embedding)) AS score
            ORDER BY score LIMIT $limit
            RETURN e.id AS name,
               [l in labels(e) WHERE l <> '__Entity__' | l][0] AS type,
{{.* , embedding: Null, name: Null, id: Null}} AS properties,
               score""",
            param_map={
                "embedding": query.query_embedding,
                "dimension": len(query.query_embedding),
                "limit": query.similarity_top_k,
            },
        )
        data = data if data else []

        nodes = []
        scores = []
        for record in data:
            node = EntityNode(
                name=record["name"],
                label=record["type"],
                properties=remove_empty_values(record["properties"]),
            )
            nodes.append(node)
            scores.append(record["score"])

        return (nodes, scores)

    defdelete(
        self,
        entity_names: Optional[List[str]] = None,
        relation_names: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
"""Delete matching data."""
        if entity_names:
            self.structured_query(
                "MATCH (n) WHERE n.name IN $entity_names DETACH DELETE n",
                param_map={"entity_names": entity_names},
            )

        if ids:
            self.structured_query(
                "MATCH (n) WHERE n.id IN $ids DETACH DELETE n",
                param_map={"ids": ids},
            )

        if relation_names:
            for rel in relation_names:
                self.structured_query(f"MATCH ()-[r:`{rel}`]->() DELETE r")

        if properties:
            cypher = "MATCH (e) WHERE "
            prop_list = []
            params = {}
            for i, prop in enumerate(properties):
                prop_list.append(f"e.`{prop}` = $property_{i}")
                params[f"property_{i}"] = properties[prop]
            cypher += " AND ".join(prop_list)
            self.structured_query(cypher + " DETACH DELETE e", param_map=params)

    defget_schema(self, refresh: bool = False) -> Any:
        if refresh:
            self.refresh_schema()

        return self.structured_schema

    defget_schema_str(self, refresh: bool = False) -> str:
        schema = self.get_schema(refresh=refresh)

        formatted_node_props = []
        formatted_rel_props = []

        # Format node properties
        for label, props in schema["node_props"].items():
            props_str = ", ".join(
                [f"{prop['property']}: {prop['type']}" for prop in props]
            )
            formatted_node_props.append(f"{label}{{{props_str}}}")

        # Format relationship properties using structured_schema
        for type, props in schema["rel_props"].items():
            props_str = ", ".join(
                [f"{prop['property']}: {prop['type']}" for prop in props]
            )
            formatted_rel_props.append(f"{type}{{{props_str}}}")

        # Format relationships
        formatted_rels = [
            f"(:{el['start']})-[:{el['type']}]->(:{el['end']})"
            for el in schema["relationships"]
        ]

        return "\n".join(
            [
                "Node properties:",
                "\n".join(formatted_node_props),
                "Relationship properties:",
                "\n".join(formatted_rel_props),
                "The relationships:",
                "\n".join(formatted_rels),
            ]
        )

    defswitch_graph(self, graph_name: str) -> None:
"""
        Switch to the given graph name (`graph_name`).

        This method allows users to change the active graph within the same
        database connection.

        Args:
            graph_name (str): The name of the graph to switch to.

        """
        self._graph = self._driver.select_graph(graph_name)

        try:
            self.refresh_schema()
        except Exception as e:
            raise ValueError(f"Could not refresh schema. Error: {e}")

```
 |  
| --- | --- |  
###  refresh_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBPropertyGraphStore.refresh_schema "Permanent link")

```
refresh_schema() -> None

```

Refresh the schema.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/falkordb_property_graph.py`  
| 
```
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
```
 | 
```
defrefresh_schema(self) -> None:
"""Refresh the schema."""
    node_query_results = self.structured_query(
        node_properties_query,
        param_map={"EXCLUDED_LABELS": [*EXCLUDED_LABELS, BASE_ENTITY_LABEL]},
    )
    node_properties = (
        [el["output"] for el in node_query_results] if node_query_results else []
    )

    rels_query_result = self.structured_query(
        rel_properties_query, param_map={"EXCLUDED_LABELS": EXCLUDED_RELS}
    )
    rel_properties = (
        [el["output"] for el in rels_query_result] if rels_query_result else []
    )

    rel_objs_query_result = self.structured_query(
        rel_query,
        param_map={"EXCLUDED_LABELS": [*EXCLUDED_LABELS, BASE_ENTITY_LABEL]},
    )
    relationships = (
        [el["output"] for el in rel_objs_query_result]
        if rel_objs_query_result
        else []
    )

    # Get constraints & indexes
    try:
        constraint = self.structured_query("CALL db.constraints()")
        index = self.structured_query(
            "CALL db.indexes() YIELD label, properties, entitytype RETURN *"
        )
    except (
        redis.exceptions.ResponseError
    ):  # Read-only user might not have access to schema information
        constraint = []
        index = []

    self.structured_schema = {
        "node_props": {el["label"]: el["keys"] for el in node_properties},
        "rel_props": {el["type"]: el["keys"] for el in rel_properties},
        "relationships": relationships,
        "metadata": {"constraint": constraint, "index": index},
    }

```
 |  
| --- | --- |  
###  upsert_relations [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBPropertyGraphStore.upsert_relations "Permanent link")

```
upsert_relations(relations: []) -> None

```

Add relations.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/falkordb_property_graph.py`  
| 
```
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
```
 | 
```
defupsert_relations(self, relations: List[Relation]) -> None:
"""Add relations."""
    params = [r.dict() for r in relations]

    for param in params:
        self.structured_query(
            f"""
            MERGE (source {{id: $data.source_id}})
            ON CREATE SET source:Chunk
            MERGE (target {{id: $data.target_id}})
            ON CREATE SET target:Chunk
            WITH source, target
            CREATE (source)-[r:`{param["label"]}`]->(target)
            SET r += $data.properties
            RETURN count(*)
,
            param_map={"data": param},
        )

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBPropertyGraphStore.get "Permanent link")

```
get(
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> []

```

Get nodes.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/falkordb_property_graph.py`  
| 
```
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
```
 | 
```
defget(
    self,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> List[LabelledNode]:
"""Get nodes."""
    cypher_statement = "MATCH (e) "

    params = {}
    if properties or ids:
        cypher_statement += "WHERE "

    if ids:
        cypher_statement += "e.id in $ids "
        params["ids"] = ids

    if properties:
        prop_list = []
        for i, prop in enumerate(properties):
            prop_list.append(f"e.`{prop}` = $property_{i}")
            params[f"property_{i}"] = properties[prop]
        cypher_statement += " AND ".join(prop_list)

    return_statement = """
    WITH e
    RETURN e.id AS name,
           [l in labels(e) WHERE l <> '__Entity__' | l][0] AS type,
           e{.* , embedding: Null, id: Null} AS properties
    """
    cypher_statement += return_statement

    response = self.structured_query(cypher_statement, param_map=params)
    response = response if response else []

    nodes = []
    for record in response:
        # text indicates a chunk node
        # none on the type indicates an implicit node, likely a chunk node
        if "text" in record["properties"] or record["type"] is None:
            text = record["properties"].pop("text", "")
            nodes.append(
                ChunkNode(
                    id_=record["name"],
                    text=text,
                    properties=remove_empty_values(record["properties"]),
                )
            )
        else:
            nodes.append(
                EntityNode(
                    name=record["name"],
                    label=record["type"],
                    properties=remove_empty_values(record["properties"]),
                )
            )

    return nodes

```
 |  
| --- | --- |  
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBPropertyGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    graph_nodes: [],
    depth:  = 2,
    limit:  = 30,
    ignore_rels: Optional[[]] = None,
) -> [Triplet]

```

Get depth-aware rel map.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/falkordb_property_graph.py`  
| 
```
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
```
 | 
```
defget_rel_map(
    self,
    graph_nodes: List[LabelledNode],
    depth: int = 2,
    limit: int = 30,
    ignore_rels: Optional[List[str]] = None,
) -> List[Triplet]:
"""Get depth-aware rel map."""
    triples = []

    ids = [node.id for node in graph_nodes]
    # Needs some optimization
    response = self.structured_query(
        f"""
        WITH $ids AS id_list
        UNWIND range(0, size(id_list) - 1) AS idx
        MATCH (e:`__Entity__`)
        WHERE e.id = id_list[idx]
        MATCH p=(e)-[r*1..{depth}]-(other)
        WHERE ALL(rel in relationships(p) WHERE type(rel) <> 'MENTIONS')
        UNWIND relationships(p) AS rel
        WITH distinct rel, idx
        WITH startNode(rel) AS source,
            type(rel) AS type,
            endNode(rel) AS endNode,

        LIMIT $limit
        RETURN source.id AS source_id, [l in labels(source) WHERE l <> '__Entity__' | l][0] AS source_type,
            source{{.* , embedding: Null, id: Null}} AS source_properties,
            type,
            endNode.id AS target_id, [l in labels(endNode) WHERE l <> '__Entity__' | l][0] AS target_type,
            endNode{{.* , embedding: Null, id: Null}} AS target_properties,

        ORDER BY idx
        LIMIT $limit
        """,
        param_map={"ids": ids, "limit": limit},
    )
    response = response if response else []

    ignore_rels = ignore_rels or []
    for record in response:
        if record["type"] in ignore_rels:
            continue

        source = EntityNode(
            name=record["source_id"],
            label=record["source_type"],
            properties=remove_empty_values(record["source_properties"]),
        )
        target = EntityNode(
            name=record["target_id"],
            label=record["target_type"],
            properties=remove_empty_values(record["target_properties"]),
        )
        rel = Relation(
            source_id=record["source_id"],
            target_id=record["target_id"],
            label=record["type"],
        )
        triples.append([source, rel, target])

    return triples

```
 |  
| --- | --- |  
###  vector_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBPropertyGraphStore.vector_query "Permanent link")

```
vector_query(
    query: , **kwargs: 
) -> Tuple[[], [float]]

```

Query the graph store with a vector store query.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/falkordb_property_graph.py`  
| 
```
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
```
 | 
```
defvector_query(
    self, query: VectorStoreQuery, **kwargs: Any
) -> Tuple[List[LabelledNode], List[float]]:
"""Query the graph store with a vector store query."""
    conditions = None
    if query.filters:
        conditions = [
            f"e.{filter.key}{filter.operator.value}{filter.value}"
            for filter in query.filters.filters
        ]
    filters = (
        f" {query.filters.condition.value} ".join(conditions).replace("==", "=")
        if conditions is not None
        else "1 = 1"
    )

    data = self.structured_query(
        f"""MATCH (e:`__Entity__`)
        WHERE e.embedding IS NOT NULL AND ({filters})
        WITH e, vec.euclideanDistance(e.embedding, vecf32($embedding)) AS score
        ORDER BY score LIMIT $limit
        RETURN e.id AS name,
           [l in labels(e) WHERE l <> '__Entity__' | l][0] AS type,
{{.* , embedding: Null, name: Null, id: Null}} AS properties,
           score""",
        param_map={
            "embedding": query.query_embedding,
            "dimension": len(query.query_embedding),
            "limit": query.similarity_top_k,
        },
    )
    data = data if data else []

    nodes = []
    scores = []
    for record in data:
        node = EntityNode(
            name=record["name"],
            label=record["type"],
            properties=remove_empty_values(record["properties"]),
        )
        nodes.append(node)
        scores.append(record["score"])

    return (nodes, scores)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBPropertyGraphStore.delete "Permanent link")

```
delete(
    entity_names: Optional[[]] = None,
    relation_names: Optional[[]] = None,
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> None

```

Delete matching data.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/falkordb_property_graph.py`  
| 
```
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
```
 | 
```
defdelete(
    self,
    entity_names: Optional[List[str]] = None,
    relation_names: Optional[List[str]] = None,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> None:
"""Delete matching data."""
    if entity_names:
        self.structured_query(
            "MATCH (n) WHERE n.name IN $entity_names DETACH DELETE n",
            param_map={"entity_names": entity_names},
        )

    if ids:
        self.structured_query(
            "MATCH (n) WHERE n.id IN $ids DETACH DELETE n",
            param_map={"ids": ids},
        )

    if relation_names:
        for rel in relation_names:
            self.structured_query(f"MATCH ()-[r:`{rel}`]->() DELETE r")

    if properties:
        cypher = "MATCH (e) WHERE "
        prop_list = []
        params = {}
        for i, prop in enumerate(properties):
            prop_list.append(f"e.`{prop}` = $property_{i}")
            params[f"property_{i}"] = properties[prop]
        cypher += " AND ".join(prop_list)
        self.structured_query(cypher + " DETACH DELETE e", param_map=params)

```
 |  
| --- | --- |  
###  switch_graph [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/falkordb/#llama_index.graph_stores.falkordb.FalkorDBPropertyGraphStore.switch_graph "Permanent link")

```
switch_graph(graph_name: ) -> None

```

Switch to the given graph name (`graph_name`).
This method allows users to change the active graph within the same database connection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `graph_name`  |  The name of the graph to switch to.  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-falkordb/llama_index/graph_stores/falkordb/falkordb_property_graph.py`  
| 
```
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
```
 | 
```
defswitch_graph(self, graph_name: str) -> None:
"""
    Switch to the given graph name (`graph_name`).

    This method allows users to change the active graph within the same
    database connection.

    Args:
        graph_name (str): The name of the graph to switch to.

    """
    self._graph = self._driver.select_graph(graph_name)

    try:
        self.refresh_schema()
    except Exception as e:
        raise ValueError(f"Could not refresh schema. Error: {e}")

```
 |  
| --- | --- |  
options: members: - FalkorDBGraphStore - FalkorDBPropertyGraphStore
