# ApertureDB
##  ApertureDBGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/ApertureDB/#llama_index.graph_stores.ApertureDB.ApertureDBGraphStore "Permanent link")
Bases: 
ApertureDB graph store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `config`  |  `dict`  |  Configuration for the graph store.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-ApertureDB/llama_index/graph_stores/ApertureDB/property_graph.py`  
| 
```
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
```
 | 
```
classApertureDBGraphStore(PropertyGraphStore):
"""
    ApertureDB graph store.

    Args:
        config (dict): Configuration for the graph store.
        **kwargs: Additional keyword arguments.

    """

    flat_metadata: bool = True

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._client

    def__init__(self, *args, **kwargs) -> None:
        try:
            fromaperturedb.CommonLibraryimport create_connector, execute_query
            fromaperturedb.Queryimport QueryBuilder
        except ImportError:
            raise ImportError(
                "ApertureDB is not installed. Please install it using "
                "'pip install --upgrade aperturedb'"
            )

        self._client = create_connector()
        global query_executor
        query_executor = execute_query
        global query_builder
        query_builder = QueryBuilder

    defget_rel_map(
        self,
        subjs: List[LabelledNode],
        depth: int = 2,
        limit: int = 30,
        ignore_rels: Optional[List[str]] = None,
    ) -> List[Triplet]:
"""Get depth-aware rel map."""
        if subjs is None or len(subjs) == 0:
            return []
        if depth <= 0:
            return []
        rel_map = []
        ignore_rels = ignore_rels or []
        for s in subjs:
            query = [
                query_builder.find_command(
                    oclass=s.label,
                    params={
                        "_ref": 1,
                        "constraints": {UNIQUEID_PROPERTY: ["==", s.id]},
                        "results": {"all_properties": True, "limit": limit},
                    },
                )
            ]
            for i in range(1, 2):
                query.extend(
                    [
                        {
                            "FindEntity": {
                                "_ref": i + 1,
                                "is_connected_to": {"ref": i, "direction": "out"},
                                "results": {"all_properties": True, "limit": limit},
                            }
                        },
                        {
                            "FindConnection": {
                                "src": i,
                                "results": {"all_properties": True, "limit": limit},
                            }
                        },
                    ]
                )
            result, response, _ = query_executor(
                self._client,
                query,
            )
            assert result == 0, response

            adjacent_nodes = []
            if "entities" in response[0]["FindEntity"]:
                for entity in response[0]["FindEntity"]["entities"]:
                    for c, ce in zip(
                        response[1]["FindEntity"]["entities"],
                        response[2]["FindConnection"]["connections"],
                    ):
                        if ce[UNIQUEID_PROPERTY] in ignore_rels:
                            continue
                        source = EntityNode(
                            name=entity[UNIQUEID_PROPERTY],
                            label=entity["label"],
                            properties=entity,
                        )

                        target = EntityNode(
                            name=c[UNIQUEID_PROPERTY],
                            label=c["label"],
                            properties=c,
                        )

                        relation = Relation(
                            source_id=c[UNIQUEID_PROPERTY],
                            target_id=c[UNIQUEID_PROPERTY],
                            label=ce[UNIQUEID_PROPERTY],
                        )
                        adjacent_nodes.append(target)
                        rel_map.append([source, relation, target])
                    rel_map.extend(self.get_rel_map(adjacent_nodes, depth - 1))
        return rel_map

    defdelete(
        self,
        entity_names: Optional[List[str]] = None,
        relation_names: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
"""Delete nodes."""
        if ids and len(ids)  0:
            query = query_for_ids("DeleteEntity", [id.capitalize() for id in ids])
            result, response, _ = query_executor(
                self._client,
                query,
            )
            assert result == 0, response
        if properties and len(properties)  0:
            query = query_for_properties("DeleteEntity", properties)
            result, response, _ = query_executor(
                self._client,
                query,
            )
            assert result == 0, response
        if entity_names and len(entity_names)  0:
            for name in entity_names:
                query = [
                    {
                        "DeleteEntity": {
                            "with_class": name,
                            "constraints": {"_uniqueid": ["!=", "0.0.0"]},
                        }
                    }
                ]
                result, response, _ = query_executor(
                    self._client,
                    query,
                )
                assert result == 0, response
        if relation_names and len(relation_names)  0:
            for relation_name in set(relation_names):
                query = [
                    {
                        "DeleteConnection": {
                            "with_class": relation_name,
                            "constraints": {"_uniqueid": ["!=", "0.0.0"]},
                        }
                    }
                ]
                result, response, _ = query_executor(
                    self._client,
                    query,
                )
                assert result == 0, response

    defget(
        self, properties: Optional[dict] = None, ids: Optional[List[str]] = None
    ) -> List[LabelledNode]:
        entities = []
        if ids and len(ids)  0:
            query = query_for_ids("FindEntity", ids)
            result, response, _ = query_executor(
                self._client,
                query,
            )
            assert result == 0, response
            entities.extend(response[0]["FindEntity"].get("entities", []))

        elif properties and len(properties)  0:
            query = query_for_properties("FindEntity", properties)
            result, response, _ = query_executor(
                self._client,
                query,
            )
            assert result == 0, response
            entities.extend(response[0]["FindEntity"].get("entities", []))

        else:
            query = [
                {
                    "FindEntity": {
                        "results": {"all_properties": True, "limit": BATCHSIZE}
                    }
                }
            ]
            result, response, _ = query_executor(
                self._client,
                query,
            )
            assert result == 0, response
            entities.extend(response[0]["FindEntity"].get("entities", []))

        response = []
        if len(entities)  0:
            for e in entities:
                if e["label"] == "text_chunk":
                    node = ChunkNode(
                        properties={
                            "_node_content": e["node_content"],
                            "_node_type": e["node_type"],
                        },
                        text=e["text"],
                        id=e[UNIQUEID_PROPERTY],
                    )
                else:
                    node = EntityNode(
                        label=e["label"], properties=e, name=e[UNIQUEID_PROPERTY]
                    )
                response.append(node)

        return response

    defget_triplets(
        self, entity_names=None, relation_names=None, properties=None, ids=None
    ):
        raise NotImplementedError("get_triplets is not implemented")

    defstructured_query(
        self, query: str, param_map: Optional[Dict[str, Any]] = None
    ) -> Any:
        query = [{query: param_map}]
        blobs = []
        result, response, _ = query_executor(self._client, query, blobs)
        assert result == 0, response
        return response

    defupsert_nodes(self, nodes: List[EntityNode]) -> List[str]:
        ids = []
        data = []

        for node in nodes:
            # TODO: nodes can be of type EntityNode or ChunkNode
            properties = node.properties
            id = node.id.capitalize()
            if isinstance(node, ChunkNode):
                sane_props = {
                    "text": node.text,
                }
                for k, v in node.properties.items():
                    if k.startswith("_"):
                        sane_props[k[1:]] = v
                properties = sane_props

            entity = get_entity(self._client, node.label, id)
            combined_properties = properties | {
                UNIQUEID_PROPERTY: id,
                "label": node.label,
            }

            command = None
            if entity is None:
                command = {
                    "AddEntity": {
                        "class": node.label,
                        "if_not_found": {UNIQUEID_PROPERTY: ["==", id]},
                        "properties": combined_properties,
                    }
                }
            else:
                to_update, to_delete = changed(entity, combined_properties)
                if len(to_update)  0 or len(to_delete)  0:
                    command = {
                        "UpdateEntity": {
                            "constraints": {UNIQUEID_PROPERTY: ["==", id]},
                            "properties": to_update,
                            "remove_props": to_delete,
                        }
                    }

            if command is not None:
                query = [command]
                blobs = []
                result, response, _ = query_executor(self._client, query, blobs)
                assert result == 0, response
                data.append((query, blobs))
                ids.append(id)

        return ids

    defupsert_relations(self, relations: List[Relation]) -> None:
"""Upsert relations."""
        ids = []
        for i, r in enumerate(relations):
            query = [
                {
                    "FindEntity": {
                        "constraints": {
                            UNIQUEID_PROPERTY: ["==", r.source_id.capitalize()]
                        },
                        "_ref": 1,
                    }
                },
                {
                    "FindEntity": {
                        "constraints": {
                            UNIQUEID_PROPERTY: ["==", r.target_id.capitalize()]
                        },
                        "_ref": 2,
                    }
                },
                {
                    "AddConnection": {
                        "class": r.label,
                        "src": 1,
                        "dst": 2,
                        "properties": r.properties
                        | {
                            UNIQUEID_PROPERTY: f"{r.id}",
                            "src_id": r.source_id.capitalize(),
                            "dst_id": r.target_id.capitalize(),
                        },
                        "if_not_found": {
                            UNIQUEID_PROPERTY: ["==", f"{r.id}"],
                            "src_id": ["==", r.source_id.capitalize()],
                            "dst_id": ["==", r.target_id.capitalize()],
                        },
                    }
                },
            ]
            result, response, _ = query_executor(
                self._client, query, success_statuses=[0, 2]
            )
            assert result == 0, response
            ids.append(r.id)
        return ids

    defvector_query(self, query, **kwargs):
        raise NotImplementedError("vector_query is not implemented")

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/ApertureDB/#llama_index.graph_stores.ApertureDB.ApertureDBGraphStore.client "Permanent link")

```
client: 

```

Get client.
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/ApertureDB/#llama_index.graph_stores.ApertureDB.ApertureDBGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    subjs: [],
    depth:  = 2,
    limit:  = 30,
    ignore_rels: Optional[[]] = None,
) -> [Triplet]

```

Get depth-aware rel map.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-ApertureDB/llama_index/graph_stores/ApertureDB/property_graph.py`  
| 
```
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
```
 | 
```
defget_rel_map(
    self,
    subjs: List[LabelledNode],
    depth: int = 2,
    limit: int = 30,
    ignore_rels: Optional[List[str]] = None,
) -> List[Triplet]:
"""Get depth-aware rel map."""
    if subjs is None or len(subjs) == 0:
        return []
    if depth <= 0:
        return []
    rel_map = []
    ignore_rels = ignore_rels or []
    for s in subjs:
        query = [
            query_builder.find_command(
                oclass=s.label,
                params={
                    "_ref": 1,
                    "constraints": {UNIQUEID_PROPERTY: ["==", s.id]},
                    "results": {"all_properties": True, "limit": limit},
                },
            )
        ]
        for i in range(1, 2):
            query.extend(
                [
                    {
                        "FindEntity": {
                            "_ref": i + 1,
                            "is_connected_to": {"ref": i, "direction": "out"},
                            "results": {"all_properties": True, "limit": limit},
                        }
                    },
                    {
                        "FindConnection": {
                            "src": i,
                            "results": {"all_properties": True, "limit": limit},
                        }
                    },
                ]
            )
        result, response, _ = query_executor(
            self._client,
            query,
        )
        assert result == 0, response

        adjacent_nodes = []
        if "entities" in response[0]["FindEntity"]:
            for entity in response[0]["FindEntity"]["entities"]:
                for c, ce in zip(
                    response[1]["FindEntity"]["entities"],
                    response[2]["FindConnection"]["connections"],
                ):
                    if ce[UNIQUEID_PROPERTY] in ignore_rels:
                        continue
                    source = EntityNode(
                        name=entity[UNIQUEID_PROPERTY],
                        label=entity["label"],
                        properties=entity,
                    )

                    target = EntityNode(
                        name=c[UNIQUEID_PROPERTY],
                        label=c["label"],
                        properties=c,
                    )

                    relation = Relation(
                        source_id=c[UNIQUEID_PROPERTY],
                        target_id=c[UNIQUEID_PROPERTY],
                        label=ce[UNIQUEID_PROPERTY],
                    )
                    adjacent_nodes.append(target)
                    rel_map.append([source, relation, target])
                rel_map.extend(self.get_rel_map(adjacent_nodes, depth - 1))
    return rel_map

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/ApertureDB/#llama_index.graph_stores.ApertureDB.ApertureDBGraphStore.delete "Permanent link")

```
delete(
    entity_names: Optional[[]] = None,
    relation_names: Optional[[]] = None,
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> None

```

Delete nodes.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-ApertureDB/llama_index/graph_stores/ApertureDB/property_graph.py`  
| 
```
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
"""Delete nodes."""
    if ids and len(ids)  0:
        query = query_for_ids("DeleteEntity", [id.capitalize() for id in ids])
        result, response, _ = query_executor(
            self._client,
            query,
        )
        assert result == 0, response
    if properties and len(properties)  0:
        query = query_for_properties("DeleteEntity", properties)
        result, response, _ = query_executor(
            self._client,
            query,
        )
        assert result == 0, response
    if entity_names and len(entity_names)  0:
        for name in entity_names:
            query = [
                {
                    "DeleteEntity": {
                        "with_class": name,
                        "constraints": {"_uniqueid": ["!=", "0.0.0"]},
                    }
                }
            ]
            result, response, _ = query_executor(
                self._client,
                query,
            )
            assert result == 0, response
    if relation_names and len(relation_names)  0:
        for relation_name in set(relation_names):
            query = [
                {
                    "DeleteConnection": {
                        "with_class": relation_name,
                        "constraints": {"_uniqueid": ["!=", "0.0.0"]},
                    }
                }
            ]
            result, response, _ = query_executor(
                self._client,
                query,
            )
            assert result == 0, response

```
 |  
| --- | --- |  
###  upsert_relations [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/ApertureDB/#llama_index.graph_stores.ApertureDB.ApertureDBGraphStore.upsert_relations "Permanent link")

```
upsert_relations(relations: []) -> None

```

Upsert relations.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-ApertureDB/llama_index/graph_stores/ApertureDB/property_graph.py`  
| 
```
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
```
 | 
```
defupsert_relations(self, relations: List[Relation]) -> None:
"""Upsert relations."""
    ids = []
    for i, r in enumerate(relations):
        query = [
            {
                "FindEntity": {
                    "constraints": {
                        UNIQUEID_PROPERTY: ["==", r.source_id.capitalize()]
                    },
                    "_ref": 1,
                }
            },
            {
                "FindEntity": {
                    "constraints": {
                        UNIQUEID_PROPERTY: ["==", r.target_id.capitalize()]
                    },
                    "_ref": 2,
                }
            },
            {
                "AddConnection": {
                    "class": r.label,
                    "src": 1,
                    "dst": 2,
                    "properties": r.properties
                    | {
                        UNIQUEID_PROPERTY: f"{r.id}",
                        "src_id": r.source_id.capitalize(),
                        "dst_id": r.target_id.capitalize(),
                    },
                    "if_not_found": {
                        UNIQUEID_PROPERTY: ["==", f"{r.id}"],
                        "src_id": ["==", r.source_id.capitalize()],
                        "dst_id": ["==", r.target_id.capitalize()],
                    },
                }
            },
        ]
        result, response, _ = query_executor(
            self._client, query, success_statuses=[0, 2]
        )
        assert result == 0, response
        ids.append(r.id)
    return ids

```
 |  
| --- | --- |  
options: members: - ApertureDBPropertyGraphStore
