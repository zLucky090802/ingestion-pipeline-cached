# Tidb
##  TiDBGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBGraphStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/graph.py`  
| 
```
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
```
 | 
```
classTiDBGraphStore(GraphStore):
    def__init__(
        self,
        db_connection_string: str,
        entity_table_name: str = "entities",
        relation_table_name: str = "relations",
    ) -> None:
        # TiDB Serverless clusters have a limitation: if there are no active connections for 5 minutes,
        # they will shut down, which closes all connections, so we need to recycle the connections
        self._engine = create_engine(db_connection_string, pool_recycle=300)
        check_db_availability(self._engine)

        self._entity_table_name = entity_table_name
        self._relation_table_name = relation_table_name
        self._entity_model, self._rel_model = self.init_schema()

    definit_schema(self) -> Tuple[Any, Any]:
"""Initialize schema."""
        Base = declarative_base()

        classEntityModel(Base):
            __tablename__ = self._entity_table_name

            id = Column(Integer, primary_key=True)
            name = Column(String(512), nullable=False)
            created_at = Column(DateTime, nullable=False, server_default=sql.func.now())
            updated_at = Column(
                DateTime,
                nullable=False,
                server_default=sql.func.now(),
                onupdate=sql.func.now(),
            )

        classRelationshipModel(Base):
            __tablename__ = self._relation_table_name

            id = Column(Integer, primary_key=True)
            description = Column(Text, nullable=False)
            subject_id = Column(Integer, ForeignKey(f"{self._entity_table_name}.id"))
            object_id = Column(Integer, ForeignKey(f"{self._entity_table_name}.id"))
            created_at = Column(DateTime, nullable=False, server_default=sql.func.now())
            updated_at = Column(
                DateTime,
                nullable=False,
                server_default=sql.func.now(),
                onupdate=sql.func.now(),
            )

            subject = relationship("EntityModel", foreign_keys=[subject_id])
            object = relationship("EntityModel", foreign_keys=[object_id])

        Base.metadata.create_all(self._engine)
        return EntityModel, RelationshipModel

    @property
    defget_client(self) -> Any:
"""Get client."""
        return self._engine

    defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
        with Session(self._engine) as session:
            subj_instance, _ = get_or_create(session, self._entity_model, name=subj)
            obj_instance, _ = get_or_create(session, self._entity_model, name=obj)
            get_or_create(
                session,
                self._rel_model,
                description=rel,
                subject=subj_instance,
                object=obj_instance,
            )

    defget(self, subj: str) -> List[List[str]]:
"""Get triplets."""
        with Session(self._engine) as session:
            rels = (
                session.query(self._rel_model)
                .options(
                    joinedload(self._rel_model.subject),
                    joinedload(self._rel_model.object),
                )
                .filter(self._rel_model.subject.has(name=subj))
                .all()
            )
            return [[rel.description, rel.object.name] for rel in rels]

    defget_rel_map(
        self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
    ) -> Dict[str, List[List[str]]]:
"""Get depth-aware rel map."""
        rel_map: Dict[str, List[List[str]]] = defaultdict(list)
        with Session(self._engine) as session:
            # `raw_rels`` is a list of tuples (depth, subject, description, object), ordered by depth
            # Example:
            # +-------+------------------+------------------+------------------+
            # | depth | subject          | description      | object           |
            # +-------+------------------+------------------+------------------+
            # |     1 | Software         | Mention in       | Footnotes        |
            # |     1 | Viaweb           | Started by       | Paul graham      |
            # |     2 | Paul graham      | Invited to       | Lisp conference  |
            # |     2 | Paul graham      | Coded            | Bel              |
            # +-------+------------------+------------------+------------------+
            raw_rels = session.execute(
                sql.text(
                    rel_depth_query.format(
                        relation_table=self._relation_table_name,
                        entity_table=self._entity_table_name,
                    )
                ),
                {
                    "subjs": subjs,
                    "depth": depth,
                    "limit": limit,
                },
            ).fetchall()
            # `obj_reverse_map` is a dict of sets, where the key is a tuple (object, depth)
            # and the value is a set of subjects that have the object at the previous depth
            obj_reverse_map = defaultdict(set)
            for depth, subj, rel, obj in raw_rels:
                if depth == 1:
                    rel_map[subj].append([subj, rel, obj])
                    obj_reverse_map[(obj, depth)].update([subj])
                else:
                    for _subj in obj_reverse_map[(subj, depth - 1)]:
                        rel_map[_subj].append([subj, rel, obj])
                        obj_reverse_map[(obj, depth)].update([_subj])
            return dict(rel_map)

    defdelete(self, subj: str, rel: str, obj: str) -> None:
"""Delete triplet."""
        with Session(self._engine) as session:
            stmt = delete(self._rel_model).where(
                self._rel_model.subject.has(name=subj),
                self._rel_model.description == rel,
                self._rel_model.object.has(name=obj),
            )
            result = session.execute(stmt)
            session.commit()
            # no rows affected, do not need to delete entities
            if result.rowcount == 0:
                return

            defdelete_entity(entity_name: str):
                stmt = delete(self._entity_model).where(
                    self._entity_model.name == entity_name
                )
                session.execute(stmt)
                session.commit()

            defentity_was_referenced(entity_name: str):
                return (
                    session.query(self._rel_model)
                    .filter(
                        self._rel_model.subject.has(name=entity_name)
                        | self._rel_model.object.has(name=entity_name)
                    )
                    .one_or_none()
                )

            if not entity_was_referenced(subj):
                delete_entity(subj)
            if not entity_was_referenced(obj):
                delete_entity(obj)

    defquery(self, query: str, param_map: Optional[Dict[str, Any]] = {}) -> Any:
"""Query the graph store with statement and parameters."""
        with Session(self._engine) as session:
            return session.execute(query, param_map).fetchall()

```
 |  
| --- | --- |  
###  get_client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBGraphStore.get_client "Permanent link")

```
get_client: 

```

Get client.
###  init_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBGraphStore.init_schema "Permanent link")

```
init_schema() -> Tuple[, ]

```

Initialize schema.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/graph.py`  
| 
```
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
```
 | 
```
definit_schema(self) -> Tuple[Any, Any]:
"""Initialize schema."""
    Base = declarative_base()

    classEntityModel(Base):
        __tablename__ = self._entity_table_name

        id = Column(Integer, primary_key=True)
        name = Column(String(512), nullable=False)
        created_at = Column(DateTime, nullable=False, server_default=sql.func.now())
        updated_at = Column(
            DateTime,
            nullable=False,
            server_default=sql.func.now(),
            onupdate=sql.func.now(),
        )

    classRelationshipModel(Base):
        __tablename__ = self._relation_table_name

        id = Column(Integer, primary_key=True)
        description = Column(Text, nullable=False)
        subject_id = Column(Integer, ForeignKey(f"{self._entity_table_name}.id"))
        object_id = Column(Integer, ForeignKey(f"{self._entity_table_name}.id"))
        created_at = Column(DateTime, nullable=False, server_default=sql.func.now())
        updated_at = Column(
            DateTime,
            nullable=False,
            server_default=sql.func.now(),
            onupdate=sql.func.now(),
        )

        subject = relationship("EntityModel", foreign_keys=[subject_id])
        object = relationship("EntityModel", foreign_keys=[object_id])

    Base.metadata.create_all(self._engine)
    return EntityModel, RelationshipModel

```
 |  
| --- | --- |  
###  upsert_triplet [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBGraphStore.upsert_triplet "Permanent link")

```
upsert_triplet(subj: , rel: , obj: ) -> None

```

Add triplet.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/graph.py`  
| 
```
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
    with Session(self._engine) as session:
        subj_instance, _ = get_or_create(session, self._entity_model, name=subj)
        obj_instance, _ = get_or_create(session, self._entity_model, name=obj)
        get_or_create(
            session,
            self._rel_model,
            description=rel,
            subject=subj_instance,
            object=obj_instance,
        )

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBGraphStore.get "Permanent link")

```
get(subj: ) -> [[]]

```

Get triplets.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/graph.py`  
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
```
 | 
```
defget(self, subj: str) -> List[List[str]]:
"""Get triplets."""
    with Session(self._engine) as session:
        rels = (
            session.query(self._rel_model)
            .options(
                joinedload(self._rel_model.subject),
                joinedload(self._rel_model.object),
            )
            .filter(self._rel_model.subject.has(name=subj))
            .all()
        )
        return [[rel.description, rel.object.name] for rel in rels]

```
 |  
| --- | --- |  
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    subjs: Optional[[]] = None,
    depth:  = 2,
    limit:  = 30,
) -> [, [[]]]

```

Get depth-aware rel map.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/graph.py`  
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
```
 | 
```
defget_rel_map(
    self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
) -> Dict[str, List[List[str]]]:
"""Get depth-aware rel map."""
    rel_map: Dict[str, List[List[str]]] = defaultdict(list)
    with Session(self._engine) as session:
        # `raw_rels`` is a list of tuples (depth, subject, description, object), ordered by depth
        # Example:
        # +-------+------------------+------------------+------------------+
        # | depth | subject          | description      | object           |
        # +-------+------------------+------------------+------------------+
        # |     1 | Software         | Mention in       | Footnotes        |
        # |     1 | Viaweb           | Started by       | Paul graham      |
        # |     2 | Paul graham      | Invited to       | Lisp conference  |
        # |     2 | Paul graham      | Coded            | Bel              |
        # +-------+------------------+------------------+------------------+
        raw_rels = session.execute(
            sql.text(
                rel_depth_query.format(
                    relation_table=self._relation_table_name,
                    entity_table=self._entity_table_name,
                )
            ),
            {
                "subjs": subjs,
                "depth": depth,
                "limit": limit,
            },
        ).fetchall()
        # `obj_reverse_map` is a dict of sets, where the key is a tuple (object, depth)
        # and the value is a set of subjects that have the object at the previous depth
        obj_reverse_map = defaultdict(set)
        for depth, subj, rel, obj in raw_rels:
            if depth == 1:
                rel_map[subj].append([subj, rel, obj])
                obj_reverse_map[(obj, depth)].update([subj])
            else:
                for _subj in obj_reverse_map[(subj, depth - 1)]:
                    rel_map[_subj].append([subj, rel, obj])
                    obj_reverse_map[(obj, depth)].update([_subj])
        return dict(rel_map)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBGraphStore.delete "Permanent link")

```
delete(subj: , rel: , obj: ) -> None

```

Delete triplet.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/graph.py`  
| 
```
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
```
 | 
```
defdelete(self, subj: str, rel: str, obj: str) -> None:
"""Delete triplet."""
    with Session(self._engine) as session:
        stmt = delete(self._rel_model).where(
            self._rel_model.subject.has(name=subj),
            self._rel_model.description == rel,
            self._rel_model.object.has(name=obj),
        )
        result = session.execute(stmt)
        session.commit()
        # no rows affected, do not need to delete entities
        if result.rowcount == 0:
            return

        defdelete_entity(entity_name: str):
            stmt = delete(self._entity_model).where(
                self._entity_model.name == entity_name
            )
            session.execute(stmt)
            session.commit()

        defentity_was_referenced(entity_name: str):
            return (
                session.query(self._rel_model)
                .filter(
                    self._rel_model.subject.has(name=entity_name)
                    | self._rel_model.object.has(name=entity_name)
                )
                .one_or_none()
            )

        if not entity_was_referenced(subj):
            delete_entity(subj)
        if not entity_was_referenced(obj):
            delete_entity(obj)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBGraphStore.query "Permanent link")

```
query(
    query: , param_map: Optional[[, ]] = {}
) -> 

```

Query the graph store with statement and parameters.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/graph.py`  
| 
```
221
222
223
224
```
 | 
```
defquery(self, query: str, param_map: Optional[Dict[str, Any]] = {}) -> Any:
"""Query the graph store with statement and parameters."""
    with Session(self._engine) as session:
        return session.execute(query, param_map).fetchall()

```
 |  
| --- | --- |  
##  TiDBPropertyGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBPropertyGraphStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/property_graph.py`  
| 
```
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
```
 | 
```
classTiDBPropertyGraphStore(PropertyGraphStore):
    # TiDB does not support graph cypher queries
    supports_structured_queries: bool = False
    supports_vector_queries: bool = True

    def__init__(
        self,
        db_connection_string: str,
        embedding_dim: int = 1536,
        node_table_name: str = "pg_nodes",
        relation_table_name: str = "pg_relations",
        drop_existing_table: bool = False,
        echo_queries: bool = False,
    ) -> None:
        # TiDB Serverless clusters have a limitation: if there are no active connections for 5 minutes,
        # they will shut down, which closes all connections, so we need to recycle the connections
        self._engine = create_engine(
            db_connection_string, pool_recycle=300, echo=echo_queries
        )
        check_db_availability(self._engine, check_vector=True)

        self._embedding_dim = embedding_dim
        self._node_table_name = node_table_name
        self._relation_table_name = relation_table_name
        self._drop_existing_table = drop_existing_table
        self._node_model, self._relation_model = self.init_schema()

    definit_schema(self) -> Tuple:
"""Initialize schema."""
        Base = declarative_base()

        classBaseMixin:
            created_at = Column(DateTime, nullable=False, server_default=sql.func.now())
            updated_at = Column(
                DateTime,
                nullable=False,
                server_default=sql.func.now(),
                onupdate=sql.func.now(),
            )

        classNodeModel(BaseMixin, Base):
            __tablename__ = self._node_table_name
            id = Column(String(512), primary_key=True)
            text = Column(TEXT, nullable=True)
            name = Column(String(512), nullable=True)
            label = Column(String(512), nullable=False, default="node")
            properties = Column(JSON, default={})
            embedding = Column(
                VectorType(self._embedding_dim), comment="hnsw(distance=cosine)"
            )

        classRelationModel(BaseMixin, Base):
            __tablename__ = self._relation_table_name
            id = Column(Integer, primary_key=True)
            label = Column(String(512), nullable=False)
            source_id = Column(String(512), ForeignKey(f"{self._node_table_name}.id"))
            target_id = Column(String(512), ForeignKey(f"{self._node_table_name}.id"))
            properties = Column(JSON, default={})

            source = relationship("NodeModel", foreign_keys=[source_id])
            target = relationship("NodeModel", foreign_keys=[target_id])

        if self._drop_existing_table:
            Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        return NodeModel, RelationModel

    defget(
        self,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[LabelledNode]:
"""Get nodes."""
        with Session(self._engine) as session:
            query = session.query(self._node_model)
            if properties:
                for key, value in properties.items():
                    query = query.filter(self._node_model.properties[key] == value)
            if ids:
                query = query.filter(self._node_model.id.in_(ids))

            nodes = []
            for n in query.all():
                if n.text and n.name is None:
                    nodes.append(
                        ChunkNode(
                            id=n.id,
                            text=n.text,
                            label=n.label,
                            properties=remove_empty_values(n.properties),
                        )
                    )
                else:
                    nodes.append(
                        EntityNode(
                            name=n.name,
                            label=n.label,
                            properties=remove_empty_values(n.properties),
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
"""Get triplets."""
        # if nothing is passed, return empty list
        if not ids and not properties and not entity_names and not relation_names:
            return []

        with Session(self._engine) as session:
            query = session.query(self._relation_model).options(
                joinedload(self._relation_model.source),
                joinedload(self._relation_model.target),
            )
            if ids:
                query = query.filter(
                    self._relation_model.source_id.in_(ids)
                    | self._relation_model.target_id.in_(ids)
                )
            if properties:
                for key, value in properties.items():
                    query = query.filter(
                        (self._relation_model.properties[key] == value)
                        | self._relation_model.source.has(
                            self._node_model.properties[key] == value
                        )
                        | self._relation_model.target.has(
                            self._node_model.properties[key] == value
                        )
                    )
            if entity_names:
                query = query.filter(
                    self._relation_model.source.has(
                        self._node_model.name.in_(entity_names)
                    )
                    | self._relation_model.target.has(
                        self._node_model.name.in_(entity_names)
                    )
                )
            if relation_names:
                query = query.filter(self._relation_model.label.in_(relation_names))

            triplets = []
            for r in query.all():
                source = EntityNode(
                    name=r.source.name,
                    label=r.source.label,
                    properties=remove_empty_values(r.source.properties),
                )
                target = EntityNode(
                    name=r.target.name,
                    label=r.target.label,
                    properties=remove_empty_values(r.target.properties),
                )
                relation = Relation(
                    label=r.label,
                    source_id=source.id,
                    target_id=target.id,
                    properties=remove_empty_values(r.properties),
                )
                triplets.append([source, relation, target])
            return triplets

    defget_rel_map(
        self,
        graph_nodes: List[LabelledNode],
        depth: int = 2,
        limit: int = 30,
        ignore_rels: Optional[List[str]] = None,
    ) -> List[Triplet]:
"""Get depth-aware rel map."""
        triplets = []
        ids = [node.id for node in graph_nodes]

        if not ids:
            return []

        with Session(self._engine) as session:
            result = session.execute(
                sql.text(
                    rel_depth_query.format(
                        relation_table=self._relation_table_name,
                        node_table=self._node_table_name,
                    )
                ),
                {
                    "ids": ids,
                    "depth": depth,
                    "limit": limit,
                },
            )

            keys = result.keys()
            raw_rels = [dict(zip(keys, row)) for row in result.fetchall()]

            ignore_rels = ignore_rels or []
            for row in raw_rels:
                if row["rel_label"] in ignore_rels:
                    continue

                source = EntityNode(
                    id=row["e1_id"],
                    name=row["e1_name"],
                    label=row["e1_label"],
                    properties=json.loads(row["e1_properties"]),
                )
                target = EntityNode(
                    id=row["e2_id"],
                    name=row["e2_name"],
                    label=row["e2_label"],
                    properties=json.loads(row["e2_properties"]),
                )
                relation = Relation(
                    label=row["rel_label"],
                    source_id=source.id,
                    target_id=target.id,
                    properties=json.loads(row["rel_properties"]),
                )
                triplets.append([source, relation, target])
        return triplets

    defupsert_nodes(self, nodes: List[LabelledNode]) -> None:
"""Upsert nodes."""
        entity_list: List[EntityNode] = []
        chunk_list: List[ChunkNode] = []
        other_list: List[LabelledNode] = []

        for item in nodes:
            if isinstance(item, EntityNode):
                entity_list.append(item)
            elif isinstance(item, ChunkNode):
                chunk_list.append(item)
            else:
                other_list.append(item)

        with Session(self._engine) as session:
            # TODO: use upsert instead of get_or_create
            for entity in entity_list:
                entity_instance, _ = get_or_create(
                    session, self._node_model, id=entity.id
                )
                entity_instance.name = entity.name
                entity_instance.label = entity.label
                entity_instance.properties = entity.properties
                entity_instance.embedding = entity.embedding
                session.add(entity_instance)

            for chunk in chunk_list:
                chunk_instance, _ = get_or_create(
                    session, self._node_model, id=chunk.id
                )
                chunk_instance.text = chunk.text
                chunk_instance.label = chunk.label
                chunk_instance.properties = chunk.properties
                chunk_instance.embedding = chunk.embedding
                session.add(chunk_instance)
            session.commit()

    defupsert_relations(self, relations: List[Relation]) -> None:
"""Upsert relations."""
        with Session(self._engine) as session:
            for r in relations:
                get_or_create(
                    session,
                    self._node_model,
                    id=r.source_id,
                )
                get_or_create(
                    session,
                    self._node_model,
                    id=r.target_id,
                )
                relation_instance, _ = get_or_create(
                    session,
                    self._relation_model,
                    label=r.label,
                    source_id=r.source_id,
                    target_id=r.target_id,
                )
                relation_instance.properties = r.properties
                session.add(relation_instance)
                session.commit()

    defdelete(
        self,
        entity_names: Optional[List[str]] = None,
        relation_names: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
"""Delete matching data."""
        with Session(self._engine) as session:
            # 1. Delete relations
            relation_stmt = delete(self._relation_model)
            if ids:
                relation_stmt = relation_stmt.filter(
                    self._relation_model.source_id.in_(ids)
                    | self._relation_model.target_id.in_(ids)
                )
            if entity_names:
                relation_stmt = relation_stmt.filter(
                    self._relation_model.source.has(name=entity_names)
                    | self._relation_model.target.has(name=entity_names)
                )
            if relation_names:
                relation_stmt = relation_stmt.filter(
                    self._relation_model.label.in_(relation_names)
                )
            if properties:
                for key, value in properties.items():
                    relation_stmt = relation_stmt.filter(
                        self._relation_model.source.has(
                            self._node_model.properties[key] == value
                        )
                        | self._relation_model.target.has(
                            self._node_model.properties[key] == value
                        )
                    )
            session.execute(relation_stmt)

            # 2. Delete nodes
            entity_stmt = delete(self._node_model)
            if ids:
                entity_stmt = entity_stmt.filter(self._node_model.id.in_(ids))
            if entity_names:
                entity_stmt = entity_stmt.filter(
                    self._node_model.name.in_(entity_names)
                )
            if properties:
                for key, value in properties.items():
                    entity_stmt = entity_stmt.filter(
                        self._node_model.properties[key] == value
                    )
            session.execute(entity_stmt)
            session.commit()

    defstructured_query(
        self, query: str, param_map: Optional[Dict[str, Any]] = None
    ) -> Any:
"""Query the graph store with statement and parameters."""
        raise NotImplementedError("TiDB does not support cypher queries.")

    defvector_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> Tuple[List[LabelledNode], List[float]]:
"""Query the graph store with a vector store query."""
        with Session(self._engine) as session:
            result = (
                session.query(
                    self._node_model,
                    self._node_model.embedding.cosine_distance(
                        query.query_embedding
                    ).label("embedding_distance"),
                )
                .filter(self._node_model.name.is_not(None))
                .order_by(sql.asc("embedding_distance"))
                .limit(query.similarity_top_k)
                .all()
            )

            nodes = []
            scores = []
            for node, score in result:
                nodes.append(
                    EntityNode(
                        name=node.name,
                        label=node.label,
                        properties=remove_empty_values(node.properties),
                    )
                )
                scores.append(score)
            return nodes, scores

```
 |  
| --- | --- |  
###  init_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBPropertyGraphStore.init_schema "Permanent link")

```
init_schema() -> Tuple

```

Initialize schema.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/property_graph.py`  
| 
```
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
```
 | 
```
definit_schema(self) -> Tuple:
"""Initialize schema."""
    Base = declarative_base()

    classBaseMixin:
        created_at = Column(DateTime, nullable=False, server_default=sql.func.now())
        updated_at = Column(
            DateTime,
            nullable=False,
            server_default=sql.func.now(),
            onupdate=sql.func.now(),
        )

    classNodeModel(BaseMixin, Base):
        __tablename__ = self._node_table_name
        id = Column(String(512), primary_key=True)
        text = Column(TEXT, nullable=True)
        name = Column(String(512), nullable=True)
        label = Column(String(512), nullable=False, default="node")
        properties = Column(JSON, default={})
        embedding = Column(
            VectorType(self._embedding_dim), comment="hnsw(distance=cosine)"
        )

    classRelationModel(BaseMixin, Base):
        __tablename__ = self._relation_table_name
        id = Column(Integer, primary_key=True)
        label = Column(String(512), nullable=False)
        source_id = Column(String(512), ForeignKey(f"{self._node_table_name}.id"))
        target_id = Column(String(512), ForeignKey(f"{self._node_table_name}.id"))
        properties = Column(JSON, default={})

        source = relationship("NodeModel", foreign_keys=[source_id])
        target = relationship("NodeModel", foreign_keys=[target_id])

    if self._drop_existing_table:
        Base.metadata.drop_all(self._engine)
    Base.metadata.create_all(self._engine)
    return NodeModel, RelationModel

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBPropertyGraphStore.get "Permanent link")

```
get(
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> []

```

Get nodes.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/property_graph.py`  
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
```
 | 
```
defget(
    self,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> List[LabelledNode]:
"""Get nodes."""
    with Session(self._engine) as session:
        query = session.query(self._node_model)
        if properties:
            for key, value in properties.items():
                query = query.filter(self._node_model.properties[key] == value)
        if ids:
            query = query.filter(self._node_model.id.in_(ids))

        nodes = []
        for n in query.all():
            if n.text and n.name is None:
                nodes.append(
                    ChunkNode(
                        id=n.id,
                        text=n.text,
                        label=n.label,
                        properties=remove_empty_values(n.properties),
                    )
                )
            else:
                nodes.append(
                    EntityNode(
                        name=n.name,
                        label=n.label,
                        properties=remove_empty_values(n.properties),
                    )
                )
        return nodes

```
 |  
| --- | --- |  
###  get_triplets [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBPropertyGraphStore.get_triplets "Permanent link")

```
get_triplets(
    entity_names: Optional[[]] = None,
    relation_names: Optional[[]] = None,
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> [Triplet]

```

Get triplets.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/property_graph.py`  
| 
```
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
```
 | 
```
defget_triplets(
    self,
    entity_names: Optional[List[str]] = None,
    relation_names: Optional[List[str]] = None,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> List[Triplet]:
"""Get triplets."""
    # if nothing is passed, return empty list
    if not ids and not properties and not entity_names and not relation_names:
        return []

    with Session(self._engine) as session:
        query = session.query(self._relation_model).options(
            joinedload(self._relation_model.source),
            joinedload(self._relation_model.target),
        )
        if ids:
            query = query.filter(
                self._relation_model.source_id.in_(ids)
                | self._relation_model.target_id.in_(ids)
            )
        if properties:
            for key, value in properties.items():
                query = query.filter(
                    (self._relation_model.properties[key] == value)
                    | self._relation_model.source.has(
                        self._node_model.properties[key] == value
                    )
                    | self._relation_model.target.has(
                        self._node_model.properties[key] == value
                    )
                )
        if entity_names:
            query = query.filter(
                self._relation_model.source.has(
                    self._node_model.name.in_(entity_names)
                )
                | self._relation_model.target.has(
                    self._node_model.name.in_(entity_names)
                )
            )
        if relation_names:
            query = query.filter(self._relation_model.label.in_(relation_names))

        triplets = []
        for r in query.all():
            source = EntityNode(
                name=r.source.name,
                label=r.source.label,
                properties=remove_empty_values(r.source.properties),
            )
            target = EntityNode(
                name=r.target.name,
                label=r.target.label,
                properties=remove_empty_values(r.target.properties),
            )
            relation = Relation(
                label=r.label,
                source_id=source.id,
                target_id=target.id,
                properties=remove_empty_values(r.properties),
            )
            triplets.append([source, relation, target])
        return triplets

```
 |  
| --- | --- |  
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBPropertyGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    graph_nodes: [],
    depth:  = 2,
    limit:  = 30,
    ignore_rels: Optional[[]] = None,
) -> [Triplet]

```

Get depth-aware rel map.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/property_graph.py`  
| 
```
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
    triplets = []
    ids = [node.id for node in graph_nodes]

    if not ids:
        return []

    with Session(self._engine) as session:
        result = session.execute(
            sql.text(
                rel_depth_query.format(
                    relation_table=self._relation_table_name,
                    node_table=self._node_table_name,
                )
            ),
            {
                "ids": ids,
                "depth": depth,
                "limit": limit,
            },
        )

        keys = result.keys()
        raw_rels = [dict(zip(keys, row)) for row in result.fetchall()]

        ignore_rels = ignore_rels or []
        for row in raw_rels:
            if row["rel_label"] in ignore_rels:
                continue

            source = EntityNode(
                id=row["e1_id"],
                name=row["e1_name"],
                label=row["e1_label"],
                properties=json.loads(row["e1_properties"]),
            )
            target = EntityNode(
                id=row["e2_id"],
                name=row["e2_name"],
                label=row["e2_label"],
                properties=json.loads(row["e2_properties"]),
            )
            relation = Relation(
                label=row["rel_label"],
                source_id=source.id,
                target_id=target.id,
                properties=json.loads(row["rel_properties"]),
            )
            triplets.append([source, relation, target])
    return triplets

```
 |  
| --- | --- |  
###  upsert_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBPropertyGraphStore.upsert_nodes "Permanent link")

```
upsert_nodes(nodes: []) -> None

```

Upsert nodes.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/property_graph.py`  
| 
```
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
```
 | 
```
defupsert_nodes(self, nodes: List[LabelledNode]) -> None:
"""Upsert nodes."""
    entity_list: List[EntityNode] = []
    chunk_list: List[ChunkNode] = []
    other_list: List[LabelledNode] = []

    for item in nodes:
        if isinstance(item, EntityNode):
            entity_list.append(item)
        elif isinstance(item, ChunkNode):
            chunk_list.append(item)
        else:
            other_list.append(item)

    with Session(self._engine) as session:
        # TODO: use upsert instead of get_or_create
        for entity in entity_list:
            entity_instance, _ = get_or_create(
                session, self._node_model, id=entity.id
            )
            entity_instance.name = entity.name
            entity_instance.label = entity.label
            entity_instance.properties = entity.properties
            entity_instance.embedding = entity.embedding
            session.add(entity_instance)

        for chunk in chunk_list:
            chunk_instance, _ = get_or_create(
                session, self._node_model, id=chunk.id
            )
            chunk_instance.text = chunk.text
            chunk_instance.label = chunk.label
            chunk_instance.properties = chunk.properties
            chunk_instance.embedding = chunk.embedding
            session.add(chunk_instance)
        session.commit()

```
 |  
| --- | --- |  
###  upsert_relations [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBPropertyGraphStore.upsert_relations "Permanent link")

```
upsert_relations(relations: []) -> None

```

Upsert relations.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/property_graph.py`  
| 
```
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
```
 | 
```
defupsert_relations(self, relations: List[Relation]) -> None:
"""Upsert relations."""
    with Session(self._engine) as session:
        for r in relations:
            get_or_create(
                session,
                self._node_model,
                id=r.source_id,
            )
            get_or_create(
                session,
                self._node_model,
                id=r.target_id,
            )
            relation_instance, _ = get_or_create(
                session,
                self._relation_model,
                label=r.label,
                source_id=r.source_id,
                target_id=r.target_id,
            )
            relation_instance.properties = r.properties
            session.add(relation_instance)
            session.commit()

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBPropertyGraphStore.delete "Permanent link")

```
delete(
    entity_names: Optional[[]] = None,
    relation_names: Optional[[]] = None,
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> None

```

Delete matching data.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/property_graph.py`  
| 
```
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
    with Session(self._engine) as session:
        # 1. Delete relations
        relation_stmt = delete(self._relation_model)
        if ids:
            relation_stmt = relation_stmt.filter(
                self._relation_model.source_id.in_(ids)
                | self._relation_model.target_id.in_(ids)
            )
        if entity_names:
            relation_stmt = relation_stmt.filter(
                self._relation_model.source.has(name=entity_names)
                | self._relation_model.target.has(name=entity_names)
            )
        if relation_names:
            relation_stmt = relation_stmt.filter(
                self._relation_model.label.in_(relation_names)
            )
        if properties:
            for key, value in properties.items():
                relation_stmt = relation_stmt.filter(
                    self._relation_model.source.has(
                        self._node_model.properties[key] == value
                    )
                    | self._relation_model.target.has(
                        self._node_model.properties[key] == value
                    )
                )
        session.execute(relation_stmt)

        # 2. Delete nodes
        entity_stmt = delete(self._node_model)
        if ids:
            entity_stmt = entity_stmt.filter(self._node_model.id.in_(ids))
        if entity_names:
            entity_stmt = entity_stmt.filter(
                self._node_model.name.in_(entity_names)
            )
        if properties:
            for key, value in properties.items():
                entity_stmt = entity_stmt.filter(
                    self._node_model.properties[key] == value
                )
        session.execute(entity_stmt)
        session.commit()

```
 |  
| --- | --- |  
###  structured_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBPropertyGraphStore.structured_query "Permanent link")

```
structured_query(
    query: , param_map: Optional[[, ]] = None
) -> 

```

Query the graph store with statement and parameters.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/property_graph.py`  
| 
```
417
418
419
420
421
```
 | 
```
defstructured_query(
    self, query: str, param_map: Optional[Dict[str, Any]] = None
) -> Any:
"""Query the graph store with statement and parameters."""
    raise NotImplementedError("TiDB does not support cypher queries.")

```
 |  
| --- | --- |  
###  vector_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/tidb/#llama_index.graph_stores.tidb.TiDBPropertyGraphStore.vector_query "Permanent link")

```
vector_query(
    query: , **kwargs: 
) -> Tuple[[], [float]]

```

Query the graph store with a vector store query.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-tidb/llama_index/graph_stores/tidb/property_graph.py`  
| 
```
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
```
 | 
```
defvector_query(
    self, query: VectorStoreQuery, **kwargs: Any
) -> Tuple[List[LabelledNode], List[float]]:
"""Query the graph store with a vector store query."""
    with Session(self._engine) as session:
        result = (
            session.query(
                self._node_model,
                self._node_model.embedding.cosine_distance(
                    query.query_embedding
                ).label("embedding_distance"),
            )
            .filter(self._node_model.name.is_not(None))
            .order_by(sql.asc("embedding_distance"))
            .limit(query.similarity_top_k)
            .all()
        )

        nodes = []
        scores = []
        for node, score in result:
            nodes.append(
                EntityNode(
                    name=node.name,
                    label=node.label,
                    properties=remove_empty_values(node.properties),
                )
            )
            scores.append(score)
        return nodes, scores

```
 |  
| --- | --- |  
options: members: - TiDBGraphStore - TiDBPropertyGraphStore
