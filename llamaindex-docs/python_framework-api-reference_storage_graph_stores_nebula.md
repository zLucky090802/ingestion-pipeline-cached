# Nebula
##  NebulaGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore "Permanent link")
Bases: 
NebulaGraph graph store.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_graph_store.py`  
| 
```
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
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
```
 | 
```
classNebulaGraphStore(GraphStore):
"""NebulaGraph graph store."""

    def__init__(
        self,
        session_pool: Optional[Any] = None,
        space_name: Optional[str] = None,
        edge_types: Optional[List[str]] = ["relationship"],
        rel_prop_names: Optional[List[str]] = ["relationship,"],
        tags: Optional[List[str]] = ["entity"],
        tag_prop_names: Optional[List[str]] = ["name,"],
        include_vid: bool = True,
        session_pool_kwargs: Optional[Dict[str, Any]] = {},
        **kwargs: Any,
    ) -> None:
"""
        Initialize NebulaGraph graph store.

        Args:
            session_pool: NebulaGraph session pool.
            space_name: NebulaGraph space name.
            edge_types: Edge types.
            rel_prop_names: Relation property names corresponding to edge types.
            tags: Tags.
            tag_prop_names: Tag property names corresponding to tags.
            session_pool_kwargs: Keyword arguments for NebulaGraph session pool.
            **kwargs: Keyword arguments.

        """
        assert space_name is not None, "space_name should be provided."
        self._space_name = space_name
        self._session_pool_kwargs = session_pool_kwargs

        self._session_pool: Any = session_pool
        if self._session_pool is None:
            self.init_session_pool()

        self._vid_type = self._get_vid_type()

        self._tags = tags or ["entity"]
        self._edge_types = edge_types or ["rel"]
        self._rel_prop_names = rel_prop_names or ["predicate,"]
        if len(self._edge_types) != len(self._rel_prop_names):
            raise ValueError(
                "edge_types and rel_prop_names to define relation and relation name"
                "should be provided, yet with same length."
            )
        if len(self._edge_types) == 0:
            raise ValueError("Length of `edge_types` should be greater than 0.")

        if tag_prop_names is None or len(self._tags) != len(tag_prop_names):
            raise ValueError(
                "tag_prop_names to define tag and tag property name should be "
                "provided, yet with same length."
            )

        if len(self._tags) == 0:
            raise ValueError("Length of `tags` should be greater than 0.")

        # for building query
        self._edge_dot_rel = [
            f"`{edge_type}`.`{rel_prop_name}`"
            for edge_type, rel_prop_name in zip(self._edge_types, self._rel_prop_names)
        ]

        self._edge_prop_map = {}
        for edge_type, rel_prop_name in zip(self._edge_types, self._rel_prop_names):
            self._edge_prop_map[edge_type] = [
                prop.strip() for prop in rel_prop_name.split(",")
            ]

        # cypher string like: map{`follow`: "degree", `serve`: "start_year,end_year"}
        self._edge_prop_map_cypher_string = (
            "map{"
            + ", ".join(
                [
                    f'`{edge_type}`: "{",".join(rel_prop_names)}"'  # noqa
                    for edge_type, rel_prop_names in self._edge_prop_map.items()
                ]
            )
            + "}"
        )

        # build tag_prop_names map
        self._tag_prop_names_map = {}
        for tag, prop_names in zip(self._tags, tag_prop_names or []):
            if prop_names is not None:
                self._tag_prop_names_map[tag] = f"`{tag}`.`{prop_names}`"
        self._tag_prop_names: List[str] = list(
            {
                prop_name.strip()
                for prop_names in tag_prop_names or []
                if prop_names is not None
                for prop_name in prop_names.split(",")
            }
        )

        self._include_vid = include_vid

    definit_session_pool(self) -> Any:
"""Return NebulaGraph session pool."""
        # ensure "NEBULA_USER", "NEBULA_PASSWORD", "NEBULA_ADDRESS" are set
        # in environment variables
        if not all(
            key in os.environ
            for key in ["NEBULA_USER", "NEBULA_PASSWORD", "NEBULA_ADDRESS"]
        ):
            raise ValueError(
                "NEBULA_USER, NEBULA_PASSWORD, NEBULA_ADDRESS should be set in "
                "environment variables when NebulaGraph Session Pool is not "
                "directly passed."
            )
        graphd_host, graphd_port = os.environ["NEBULA_ADDRESS"].split(":")
        session_pool = SessionPool(
            os.environ["NEBULA_USER"],
            os.environ["NEBULA_PASSWORD"],
            self._space_name,
            [(graphd_host, int(graphd_port))],
        )

        session_pool_config = SessionPoolConfig()
        session_pool.init(session_pool_config)
        self._session_pool = session_pool
        return self._session_pool

    def_get_vid_type(self) -> str:
"""Get vid type."""
        return (
            self.execute(f"DESCRIBE SPACE {self._space_name}")
            .column_values("Vid Type")[0]
            .cast()
        )

    def__del__(self) -> None:
"""Close NebulaGraph session pool."""
        self._session_pool.close()

    @retry(
        wait=wait_random_exponential(min=WAIT_MIN_SECONDS, max=WAIT_MAX_SECONDS),
        stop=stop_after_attempt(RETRY_TIMES),
    )
    defexecute(self, query: str, param_map: Optional[Dict[str, Any]] = {}) -> Any:
"""
        Execute query.

        Args:
            query: Query.
            param_map: Parameter map.

        Returns:
            Query result.

        """
        # Clean the query string by removing triple backticks
        query = query.replace("```", "").strip()

        try:
            result = self._session_pool.execute_parameter(query, param_map)
            if result is None:
                raise ValueError(f"Query failed. Query: {query}, Param: {param_map}")
            if not result.is_succeeded():
                raise ValueError(
                    f"Query failed. Query: {query}, Param: {param_map}"
                    f"Error message: {result.error_msg()}"
                )
            return result
        except (TTransportException, IOErrorException, RuntimeError) as e:
            logger.error(
                f"Connection issue, try to recreate session pool. Query: {query}, "
                f"Param: {param_map}"
                f"Error: {e}"
            )
            self.init_session_pool()
            logger.info(
                f"Session pool recreated. Query: {query}, Param: {param_map}"
                f"This was due to error: {e}, and now retrying."
            )
            raise

        except ValueError as e:
            # query failed on db side
            logger.error(
                f"Query failed. Query: {query}, Param: {param_map}Error message: {e}"
            )
            raise
        except Exception as e:
            # other exceptions
            logger.error(
                f"Query failed. Query: {query}, Param: {param_map}Error message: {e}"
            )
            raise

    @classmethod
    deffrom_dict(cls, config_dict: Dict[str, Any]) -> "GraphStore":
"""
        Initialize graph store from configuration dictionary.

        Args:
            config_dict: Configuration dictionary.

        Returns:
            Graph store.

        """
        return cls(**config_dict)

    @property
    defclient(self) -> Any:
"""Return NebulaGraph session pool."""
        return self._session_pool

    @property
    defconfig_dict(self) -> dict:
"""Return configuration dictionary."""
        return {
            "session_pool": self._session_pool,
            "space_name": self._space_name,
            "edge_types": self._edge_types,
            "rel_prop_names": self._rel_prop_names,
            "session_pool_kwargs": self._session_pool_kwargs,
        }

    defget(self, subj: str) -> List[List[str]]:
"""
        Get triplets.

        Args:
            subj: Subject.

        Returns:
            Triplets.

        """
        rel_map = self.get_flat_rel_map([subj], depth=1)
        rels = list(rel_map.values())
        if len(rels) == 0:
            return []
        return rels[0]

    defget_flat_rel_map(
        self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
    ) -> Dict[str, List[List[str]]]:
"""Get flat rel map."""
        # The flat means for multi-hop relation path, we could get
        # knowledge like: subj -rel-> obj -rel-> obj <-rel- obj.
        # This type of knowledge is useful for some tasks.
        # +---------------------+---------------------------------------------...-----+
        # | subj                | flattened_rels                              ...     |
        # +---------------------+---------------------------------------------...-----+
        # | "{name:Tony Parker}"| "{name: Tony Parker}-[follow:{degree:95}]-> ...ili}"|
        # | "{name:Tony Parker}"| "{name: Tony Parker}-[follow:{degree:95}]-> ...r}"  |
        # ...
        rel_map: Dict[Any, List[Any]] = {}
        if subjs is None or len(subjs) == 0:
            # unlike simple graph_store, we don't do get_all here
            return rel_map

        # WITH map{`true`: "-[", `false`: "<-["} AS arrow_l,
        #      map{`true`: "]->", `false`: "]-"} AS arrow_r,
        #      map{`follow`: "degree", `serve`: "start_year,end_year"} AS edge_type_map
        # MATCH p=(start)-[e:follow|serve*..2]-()
        #     WHERE id(start) IN ["player100", "player101"]
        #   WITH start, id(start) AS vid, nodes(p) AS nodes, e AS rels,
        #     length(p) AS rel_count, arrow_l, arrow_r, edge_type_map
        #   WITH
        #     REDUCE(s = vid + '{', key IN [key_ in ["name"]
        #       WHERE properties(start)[key_] IS NOT NULL]  | s + key + ': ' +
        #         COALESCE(TOSTRING(properties(start)[key]), 'null') + ', ')
        #         + '}'
        #       AS subj,
        #     [item in [i IN RANGE(0, rel_count - 1) | [nodes[i], nodes[i + 1],
        #         rels[i], typeid(rels[i]) > 0, type(rels[i]) ]] | [
        #      arrow_l[tostring(item[3])] +
        #          item[4] + ':' +
        #          REDUCE(s = '{', key IN SPLIT(edge_type_map[item[4]], ',') |
        #            s + key + ': ' + COALESCE(TOSTRING(properties(item[2])[key]),
        #            'null') + ', ') + '}'
        #           +
        #      arrow_r[tostring(item[3])],
        #      REDUCE(s = id(item[1]) + '{', key IN [key_ in ["name"]
        #           WHERE properties(item[1])[key_] IS NOT NULL]  | s + key + ': ' +
        #           COALESCE(TOSTRING(properties(item[1])[key]), 'null') + ', ') + '}'
        #      ]
        #   ] AS rels
        #   WITH
        #       REPLACE(subj, ', }', '}') AS subj,
        #       REDUCE(acc = collect(NULL), l in rels | acc + l) AS flattened_rels
        #   RETURN
        #     subj,
        #     REPLACE(REDUCE(acc = subj,l in flattened_rels|acc + ' ' + l),
        #       ', }', '}')
        #       AS flattened_rels
        #   LIMIT 30

        # Based on self._include_vid
        # {name: Tim Duncan} or player100{name: Tim Duncan} for entity
        s_prefix = "vid + '{'" if self._include_vid else "'{'"
        s1 = "id(item[1]) + '{'" if self._include_vid else "'{'"

        query = (
            f"WITH map{{`true`: '-[', `false`: '<-['}} AS arrow_l,"
            f"     map{{`true`: ']->', `false`: ']-'}} AS arrow_r,"
            f{self._edge_prop_map_cypher_string} AS edge_type_map "
            f"MATCH p=(start)-[e:`{'`|`'.join(self._edge_types)}`*..{depth}]-() "
            f"  WHERE id(start) IN $subjs "
            f"WITH start, id(start) AS vid, nodes(p) AS nodes, e AS rels,"
            f"  length(p) AS rel_count, arrow_l, arrow_r, edge_type_map "
            f"WITH "
            f"  REDUCE(s = {s_prefix}, key IN [key_ in {self._tag_prop_names!s} "
            f"    WHERE properties(start)[key_] IS NOT NULL]  | s + key + ': ' + "
            f"      COALESCE(TOSTRING(properties(start)[key]), 'null') + ', ')"
            f"      + '}}'"
            f"    AS subj,"
            f"  [item in [i IN RANGE(0, rel_count - 1)|[nodes[i], nodes[i + 1],"
            f"      rels[i], typeid(rels[i]) > 0, type(rels[i]) ]] | ["
            f"    arrow_l[tostring(item[3])] +"
            f"      item[4] + ':' +"
            f"      REDUCE(s = '{{', key IN SPLIT(edge_type_map[item[4]], ',') | "
            f"        s + key + ': ' + COALESCE(TOSTRING(properties(item[2])[key]),"
            f"        'null') + ', ') + '}}'"
            f"      +"
            f"    arrow_r[tostring(item[3])],"
            f"    REDUCE(s = {s1}, key IN [key_ in "
            f{self._tag_prop_names!s} WHERE properties(item[1])[key_] "
            f"        IS NOT NULL]  | s + key + ': ' + "
            f"        COALESCE(TOSTRING(properties(item[1])[key]), 'null') + ', ')"
            f"        + '}}'"
            f"    ]"
            f"  ] AS rels "
            f"WITH "
            f"  REPLACE(subj, ', }}', '}}') AS subj,"
            f"  REDUCE(acc = collect(NULL), l in rels | acc + l) AS flattened_rels "
            f"RETURN "
            f"  subj,"
            f"  REPLACE(REDUCE(acc = subj, l in flattened_rels | acc + ' ' + l), "
            f"    ', }}', '}}') "
            f"    AS flattened_rels"
            f"  LIMIT {limit}"
        )
        subjs_param = prepare_subjs_param(subjs, self._vid_type)
        logger.debug(f"get_flat_rel_map()\nsubjs_param: {subjs},\nquery: {query}")
        if subjs_param == {}:
            # This happens when subjs is None after prepare_subjs_param()
            # Probably because vid type is INT64, but no digit string is provided.
            return rel_map
        result = self.execute(query, subjs_param)
        if result is None:
            return rel_map

        # get raw data
        subjs_ = result.column_values("subj") or []
        rels_ = result.column_values("flattened_rels") or []

        for subj, rel in zip(subjs_, rels_):
            subj_ = subj.cast()
            rel_ = rel.cast()
            if subj_ not in rel_map:
                rel_map[subj_] = []
            rel_map[subj_].append(rel_)
        return rel_map

    defget_rel_map(
        self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
    ) -> Dict[str, List[List[str]]]:
"""Get rel map."""
        # We put rels in a long list for depth>= 1, this is different from
        # SimpleGraphStore.get_rel_map() though.
        # But this makes more sense for multi-hop relation path.

        if subjs is not None:
            subjs = [
                escape_str(subj) for subj in subjs if isinstance(subj, str) and subj
            ]
            if len(subjs) == 0:
                return {}

        return self.get_flat_rel_map(subjs, depth, limit)

    defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
        # Note, to enable leveraging existing knowledge graph,
        # the (triplet -- property graph) mapping
        #   makes (n:1) edge_type.prop_name --> triplet.rel
        # thus we have to assume rel to be the first edge_type.prop_name
        # here in upsert_triplet().
        # This applies to the type of entity(tags) with subject and object, too,
        # thus we have to assume subj to be the first entity.tag_name

        # lower case subj, rel, obj
        subj = escape_str(subj)
        rel = escape_str(rel)
        obj = escape_str(obj)
        if self._vid_type == "INT64":
            assert all([subj.isdigit(), obj.isdigit()]), (
                "Subject and object should be digit strings in current graph store."
            )
            subj_field = subj
            obj_field = obj
        else:
            subj_field = f"{QUOTE}{subj}{QUOTE}"
            obj_field = f"{QUOTE}{obj}{QUOTE}"
        edge_field = f"{subj_field}->{obj_field}"

        edge_type = self._edge_types[0]
        rel_prop_name = self._rel_prop_names[0]
        entity_type = self._tags[0]
        rel_hash = hash_string_to_rank(rel)
        dml_query = (
            f"INSERT VERTEX `{entity_type}`(name) "
            f"  VALUES {subj_field}:({QUOTE}{subj}{QUOTE});"
            f"INSERT VERTEX `{entity_type}`(name) "
            f"  VALUES {obj_field}:({QUOTE}{obj}{QUOTE});"
            f"INSERT EDGE `{edge_type}`(`{rel_prop_name}`) "
            f"  VALUES "
            f"{edge_field}"
            f"@{rel_hash}:({QUOTE}{rel}{QUOTE});"
        )
        logger.debug(f"upsert_triplet()\nDML query: {dml_query}")
        result = self.execute(dml_query)
        assert result and result.is_succeeded(), (
            f"Failed to upsert triplet: {subj}{rel}{obj}, query: {dml_query}"
        )

    defdelete(self, subj: str, rel: str, obj: str) -> None:
"""
        Delete triplet.
        1. Similar to upsert_triplet(),
           we have to assume rel to be the first edge_type.prop_name.
        2. After edge being deleted, we need to check if the subj or
           obj are isolated vertices,
           if so, delete them, too.
        """
        # lower case subj, rel, obj
        subj = escape_str(subj)
        rel = escape_str(rel)
        obj = escape_str(obj)

        if self._vid_type == "INT64":
            assert all([subj.isdigit(), obj.isdigit()]), (
                "Subject and object should be digit strings in current graph store."
            )
            subj_field = subj
            obj_field = obj
        else:
            subj_field = f"{QUOTE}{subj}{QUOTE}"
            obj_field = f"{QUOTE}{obj}{QUOTE}"
        edge_field = f"{subj_field}->{obj_field}"

        # DELETE EDGE serve "player100" -> "team204"@7696463696635583936;
        edge_type = self._edge_types[0]
        # rel_prop_name = self._rel_prop_names[0]
        rel_hash = hash_string_to_rank(rel)
        dml_query = f"DELETE EDGE `{edge_type}{edge_field}@{rel_hash};"
        logger.debug(f"delete()\nDML query: {dml_query}")
        result = self.execute(dml_query)
        assert result and result.is_succeeded(), (
            f"Failed to delete triplet: {subj}{rel}{obj}, query: {dml_query}"
        )
        # Get isolated vertices to be deleted
        # MATCH (s) WHERE id(s) IN ["player700"] AND NOT (s)-[]-()
        # RETURN id(s) AS isolated
        query = (
            f"MATCH (s) "
            f"  WHERE id(s) IN [{subj_field}, {obj_field}] "
            f"  AND NOT (s)-[]-() "
            f"RETURN id(s) AS isolated"
        )
        result = self.execute(query)
        isolated = result.column_values("isolated")
        if not isolated:
            return
        # DELETE VERTEX "player700" or DELETE VERTEX 700
        quote_field = QUOTE if self._vid_type != "INT64" else ""
        vertex_ids = ",".join(
            [f"{quote_field}{v.cast()}{quote_field}" for v in isolated]
        )
        dml_query = f"DELETE VERTEX {vertex_ids};"

        result = self.execute(dml_query)
        assert result and result.is_succeeded(), (
            f"Failed to delete isolated vertices: {isolated}, query: {dml_query}"
        )

    defrefresh_schema(self) -> None:
"""
        Refreshes the NebulaGraph Store Schema.
        """
        tags_schema, edge_types_schema, relationships = [], [], []
        for tag in self.execute("SHOW TAGS").column_values("Name"):
            tag_name = tag.cast()
            tag_schema = {"tag": tag_name, "properties": []}
            r = self.execute(f"DESCRIBE TAG `{tag_name}`")
            props, types, comments = (
                r.column_values("Field"),
                r.column_values("Type"),
                r.column_values("Comment"),
            )
            for i in range(r.row_size()):
                # back compatible with old version of nebula-python
                property_defination = (
                    (props[i].cast(), types[i].cast())
                    if comments[i].is_empty()
                    else (props[i].cast(), types[i].cast(), comments[i].cast())
                )
                tag_schema["properties"].append(property_defination)
            tags_schema.append(tag_schema)
        for edge_type in self.execute("SHOW EDGES").column_values("Name"):
            edge_type_name = edge_type.cast()
            edge_schema = {"edge": edge_type_name, "properties": []}
            r = self.execute(f"DESCRIBE EDGE `{edge_type_name}`")
            props, types, comments = (
                r.column_values("Field"),
                r.column_values("Type"),
                r.column_values("Comment"),
            )
            for i in range(r.row_size()):
                # back compatible with old version of nebula-python
                property_defination = (
                    (props[i].cast(), types[i].cast())
                    if comments[i].is_empty()
                    else (props[i].cast(), types[i].cast(), comments[i].cast())
                )
                edge_schema["properties"].append(property_defination)
            edge_types_schema.append(edge_schema)

            # build relationships types
            sample_edge = self.execute(
                rel_query_sample_edge.substitute(edge_type=edge_type_name)
            ).column_values("sample_edge")
            if len(sample_edge) == 0:
                continue
            src_id, dst_id = sample_edge[0].cast()
            r = self.execute(
                rel_query_edge_type.substitute(
                    edge_type=edge_type_name,
                    src_id=src_id,
                    dst_id=dst_id,
                    quote="" if self._vid_type == "INT64" else QUOTE,
                )
            ).column_values("rels")
            if len(r)  0:
                relationships.append(r[0].cast())

        self.schema = (
            f"Node properties: {tags_schema}\n"
            f"Edge properties: {edge_types_schema}\n"
            f"Relationships: {relationships}\n"
        )

    defget_schema(self, refresh: bool = False) -> str:
"""Get the schema of the NebulaGraph store."""
        if self.schema and not refresh:
            return self.schema
        self.refresh_schema()
        logger.debug(f"get_schema()\nschema: {self.schema}")
        return self.schema

    defquery(self, query: str, param_map: Optional[Dict[str, Any]] = {}) -> Any:
        result = self.execute(query, param_map)
        columns = result.keys()
        d: Dict[str, list] = {}
        for col_num in range(result.col_size()):
            col_name = columns[col_num]
            col_list = result.column_values(col_name)
            d[col_name] = [x.cast() for x in col_list]
        return d

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore.client "Permanent link")

```
client: 

```

Return NebulaGraph session pool.
###  config_dict `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore.config_dict "Permanent link")

```
config_dict: 

```

Return configuration dictionary.
###  init_session_pool [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore.init_session_pool "Permanent link")

```
init_session_pool() -> 

```

Return NebulaGraph session pool.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_graph_store.py`  
| 
```
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
```
 | 
```
definit_session_pool(self) -> Any:
"""Return NebulaGraph session pool."""
    # ensure "NEBULA_USER", "NEBULA_PASSWORD", "NEBULA_ADDRESS" are set
    # in environment variables
    if not all(
        key in os.environ
        for key in ["NEBULA_USER", "NEBULA_PASSWORD", "NEBULA_ADDRESS"]
    ):
        raise ValueError(
            "NEBULA_USER, NEBULA_PASSWORD, NEBULA_ADDRESS should be set in "
            "environment variables when NebulaGraph Session Pool is not "
            "directly passed."
        )
    graphd_host, graphd_port = os.environ["NEBULA_ADDRESS"].split(":")
    session_pool = SessionPool(
        os.environ["NEBULA_USER"],
        os.environ["NEBULA_PASSWORD"],
        self._space_name,
        [(graphd_host, int(graphd_port))],
    )

    session_pool_config = SessionPoolConfig()
    session_pool.init(session_pool_config)
    self._session_pool = session_pool
    return self._session_pool

```
 |  
| --- | --- |  
###  execute [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore.execute "Permanent link")

```
execute(
    query: , param_map: Optional[[, ]] = {}
) -> 

```

Execute query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query.  |  _required_  |  
|  `param_map`  |  `Optional[Dict[str, Any]]`  |  Parameter map.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  Query result.  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_graph_store.py`  
| 
```
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
```
 | 
```
@retry(
    wait=wait_random_exponential(min=WAIT_MIN_SECONDS, max=WAIT_MAX_SECONDS),
    stop=stop_after_attempt(RETRY_TIMES),
)
defexecute(self, query: str, param_map: Optional[Dict[str, Any]] = {}) -> Any:
"""
    Execute query.

    Args:
        query: Query.
        param_map: Parameter map.

    Returns:
        Query result.

    """
    # Clean the query string by removing triple backticks
    query = query.replace("```", "").strip()

    try:
        result = self._session_pool.execute_parameter(query, param_map)
        if result is None:
            raise ValueError(f"Query failed. Query: {query}, Param: {param_map}")
        if not result.is_succeeded():
            raise ValueError(
                f"Query failed. Query: {query}, Param: {param_map}"
                f"Error message: {result.error_msg()}"
            )
        return result
    except (TTransportException, IOErrorException, RuntimeError) as e:
        logger.error(
            f"Connection issue, try to recreate session pool. Query: {query}, "
            f"Param: {param_map}"
            f"Error: {e}"
        )
        self.init_session_pool()
        logger.info(
            f"Session pool recreated. Query: {query}, Param: {param_map}"
            f"This was due to error: {e}, and now retrying."
        )
        raise

    except ValueError as e:
        # query failed on db side
        logger.error(
            f"Query failed. Query: {query}, Param: {param_map}Error message: {e}"
        )
        raise
    except Exception as e:
        # other exceptions
        logger.error(
            f"Query failed. Query: {query}, Param: {param_map}Error message: {e}"
        )
        raise

```
 |  
| --- | --- |  
###  from_dict `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore.from_dict "Permanent link")

```
from_dict(config_dict: [, ]) -> 

```

Initialize graph store from configuration dictionary.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `config_dict`  |  `Dict[str, Any]`  |  Configuration dictionary.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  Graph store.  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_graph_store.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_dict(cls, config_dict: Dict[str, Any]) -> "GraphStore":
"""
    Initialize graph store from configuration dictionary.

    Args:
        config_dict: Configuration dictionary.

    Returns:
        Graph store.

    """
    return cls(**config_dict)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore.get "Permanent link")

```
get(subj: ) -> [[]]

```

Get triplets.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `subj`  |  Subject.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[List[str]]`  |  Triplets.  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_graph_store.py`  
| 
```
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
```
 | 
```
defget(self, subj: str) -> List[List[str]]:
"""
    Get triplets.

    Args:
        subj: Subject.

    Returns:
        Triplets.

    """
    rel_map = self.get_flat_rel_map([subj], depth=1)
    rels = list(rel_map.values())
    if len(rels) == 0:
        return []
    return rels[0]

```
 |  
| --- | --- |  
###  get_flat_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore.get_flat_rel_map "Permanent link")

```
get_flat_rel_map(
    subjs: Optional[[]] = None,
    depth:  = 2,
    limit:  = 30,
) -> [, [[]]]

```

Get flat rel map.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_graph_store.py`  
| 
```
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
```
 | 
```
defget_flat_rel_map(
    self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
) -> Dict[str, List[List[str]]]:
"""Get flat rel map."""
    # The flat means for multi-hop relation path, we could get
    # knowledge like: subj -rel-> obj -rel-> obj <-rel- obj.
    # This type of knowledge is useful for some tasks.
    # +---------------------+---------------------------------------------...-----+
    # | subj                | flattened_rels                              ...     |
    # +---------------------+---------------------------------------------...-----+
    # | "{name:Tony Parker}"| "{name: Tony Parker}-[follow:{degree:95}]-> ...ili}"|
    # | "{name:Tony Parker}"| "{name: Tony Parker}-[follow:{degree:95}]-> ...r}"  |
    # ...
    rel_map: Dict[Any, List[Any]] = {}
    if subjs is None or len(subjs) == 0:
        # unlike simple graph_store, we don't do get_all here
        return rel_map

    # WITH map{`true`: "-[", `false`: "<-["} AS arrow_l,
    #      map{`true`: "]->", `false`: "]-"} AS arrow_r,
    #      map{`follow`: "degree", `serve`: "start_year,end_year"} AS edge_type_map
    # MATCH p=(start)-[e:follow|serve*..2]-()
    #     WHERE id(start) IN ["player100", "player101"]
    #   WITH start, id(start) AS vid, nodes(p) AS nodes, e AS rels,
    #     length(p) AS rel_count, arrow_l, arrow_r, edge_type_map
    #   WITH
    #     REDUCE(s = vid + '{', key IN [key_ in ["name"]
    #       WHERE properties(start)[key_] IS NOT NULL]  | s + key + ': ' +
    #         COALESCE(TOSTRING(properties(start)[key]), 'null') + ', ')
    #         + '}'
    #       AS subj,
    #     [item in [i IN RANGE(0, rel_count - 1) | [nodes[i], nodes[i + 1],
    #         rels[i], typeid(rels[i]) > 0, type(rels[i]) ]] | [
    #      arrow_l[tostring(item[3])] +
    #          item[4] + ':' +
    #          REDUCE(s = '{', key IN SPLIT(edge_type_map[item[4]], ',') |
    #            s + key + ': ' + COALESCE(TOSTRING(properties(item[2])[key]),
    #            'null') + ', ') + '}'
    #           +
    #      arrow_r[tostring(item[3])],
    #      REDUCE(s = id(item[1]) + '{', key IN [key_ in ["name"]
    #           WHERE properties(item[1])[key_] IS NOT NULL]  | s + key + ': ' +
    #           COALESCE(TOSTRING(properties(item[1])[key]), 'null') + ', ') + '}'
    #      ]
    #   ] AS rels
    #   WITH
    #       REPLACE(subj, ', }', '}') AS subj,
    #       REDUCE(acc = collect(NULL), l in rels | acc + l) AS flattened_rels
    #   RETURN
    #     subj,
    #     REPLACE(REDUCE(acc = subj,l in flattened_rels|acc + ' ' + l),
    #       ', }', '}')
    #       AS flattened_rels
    #   LIMIT 30

    # Based on self._include_vid
    # {name: Tim Duncan} or player100{name: Tim Duncan} for entity
    s_prefix = "vid + '{'" if self._include_vid else "'{'"
    s1 = "id(item[1]) + '{'" if self._include_vid else "'{'"

    query = (
        f"WITH map{{`true`: '-[', `false`: '<-['}} AS arrow_l,"
        f"     map{{`true`: ']->', `false`: ']-'}} AS arrow_r,"
        f{self._edge_prop_map_cypher_string} AS edge_type_map "
        f"MATCH p=(start)-[e:`{'`|`'.join(self._edge_types)}`*..{depth}]-() "
        f"  WHERE id(start) IN $subjs "
        f"WITH start, id(start) AS vid, nodes(p) AS nodes, e AS rels,"
        f"  length(p) AS rel_count, arrow_l, arrow_r, edge_type_map "
        f"WITH "
        f"  REDUCE(s = {s_prefix}, key IN [key_ in {self._tag_prop_names!s} "
        f"    WHERE properties(start)[key_] IS NOT NULL]  | s + key + ': ' + "
        f"      COALESCE(TOSTRING(properties(start)[key]), 'null') + ', ')"
        f"      + '}}'"
        f"    AS subj,"
        f"  [item in [i IN RANGE(0, rel_count - 1)|[nodes[i], nodes[i + 1],"
        f"      rels[i], typeid(rels[i]) > 0, type(rels[i]) ]] | ["
        f"    arrow_l[tostring(item[3])] +"
        f"      item[4] + ':' +"
        f"      REDUCE(s = '{{', key IN SPLIT(edge_type_map[item[4]], ',') | "
        f"        s + key + ': ' + COALESCE(TOSTRING(properties(item[2])[key]),"
        f"        'null') + ', ') + '}}'"
        f"      +"
        f"    arrow_r[tostring(item[3])],"
        f"    REDUCE(s = {s1}, key IN [key_ in "
        f{self._tag_prop_names!s} WHERE properties(item[1])[key_] "
        f"        IS NOT NULL]  | s + key + ': ' + "
        f"        COALESCE(TOSTRING(properties(item[1])[key]), 'null') + ', ')"
        f"        + '}}'"
        f"    ]"
        f"  ] AS rels "
        f"WITH "
        f"  REPLACE(subj, ', }}', '}}') AS subj,"
        f"  REDUCE(acc = collect(NULL), l in rels | acc + l) AS flattened_rels "
        f"RETURN "
        f"  subj,"
        f"  REPLACE(REDUCE(acc = subj, l in flattened_rels | acc + ' ' + l), "
        f"    ', }}', '}}') "
        f"    AS flattened_rels"
        f"  LIMIT {limit}"
    )
    subjs_param = prepare_subjs_param(subjs, self._vid_type)
    logger.debug(f"get_flat_rel_map()\nsubjs_param: {subjs},\nquery: {query}")
    if subjs_param == {}:
        # This happens when subjs is None after prepare_subjs_param()
        # Probably because vid type is INT64, but no digit string is provided.
        return rel_map
    result = self.execute(query, subjs_param)
    if result is None:
        return rel_map

    # get raw data
    subjs_ = result.column_values("subj") or []
    rels_ = result.column_values("flattened_rels") or []

    for subj, rel in zip(subjs_, rels_):
        subj_ = subj.cast()
        rel_ = rel.cast()
        if subj_ not in rel_map:
            rel_map[subj_] = []
        rel_map[subj_].append(rel_)
    return rel_map

```
 |  
| --- | --- |  
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    subjs: Optional[[]] = None,
    depth:  = 2,
    limit:  = 30,
) -> [, [[]]]

```

Get rel map.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_graph_store.py`  
| 
```
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
```
 | 
```
defget_rel_map(
    self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
) -> Dict[str, List[List[str]]]:
"""Get rel map."""
    # We put rels in a long list for depth>= 1, this is different from
    # SimpleGraphStore.get_rel_map() though.
    # But this makes more sense for multi-hop relation path.

    if subjs is not None:
        subjs = [
            escape_str(subj) for subj in subjs if isinstance(subj, str) and subj
        ]
        if len(subjs) == 0:
            return {}

    return self.get_flat_rel_map(subjs, depth, limit)

```
 |  
| --- | --- |  
###  upsert_triplet [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore.upsert_triplet "Permanent link")

```
upsert_triplet(subj: , rel: , obj: ) -> None

```

Add triplet.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_graph_store.py`  
| 
```
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
```
 | 
```
defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
    # Note, to enable leveraging existing knowledge graph,
    # the (triplet -- property graph) mapping
    #   makes (n:1) edge_type.prop_name --> triplet.rel
    # thus we have to assume rel to be the first edge_type.prop_name
    # here in upsert_triplet().
    # This applies to the type of entity(tags) with subject and object, too,
    # thus we have to assume subj to be the first entity.tag_name

    # lower case subj, rel, obj
    subj = escape_str(subj)
    rel = escape_str(rel)
    obj = escape_str(obj)
    if self._vid_type == "INT64":
        assert all([subj.isdigit(), obj.isdigit()]), (
            "Subject and object should be digit strings in current graph store."
        )
        subj_field = subj
        obj_field = obj
    else:
        subj_field = f"{QUOTE}{subj}{QUOTE}"
        obj_field = f"{QUOTE}{obj}{QUOTE}"
    edge_field = f"{subj_field}->{obj_field}"

    edge_type = self._edge_types[0]
    rel_prop_name = self._rel_prop_names[0]
    entity_type = self._tags[0]
    rel_hash = hash_string_to_rank(rel)
    dml_query = (
        f"INSERT VERTEX `{entity_type}`(name) "
        f"  VALUES {subj_field}:({QUOTE}{subj}{QUOTE});"
        f"INSERT VERTEX `{entity_type}`(name) "
        f"  VALUES {obj_field}:({QUOTE}{obj}{QUOTE});"
        f"INSERT EDGE `{edge_type}`(`{rel_prop_name}`) "
        f"  VALUES "
        f"{edge_field}"
        f"@{rel_hash}:({QUOTE}{rel}{QUOTE});"
    )
    logger.debug(f"upsert_triplet()\nDML query: {dml_query}")
    result = self.execute(dml_query)
    assert result and result.is_succeeded(), (
        f"Failed to upsert triplet: {subj}{rel}{obj}, query: {dml_query}"
    )

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore.delete "Permanent link")

```
delete(subj: , rel: , obj: ) -> None

```

Delete triplet. 1. Similar to upsert_triplet(), we have to assume rel to be the first edge_type.prop_name. 2. After edge being deleted, we need to check if the subj or obj are isolated vertices, if so, delete them, too.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_graph_store.py`  
| 
```
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
```
 | 
```
defdelete(self, subj: str, rel: str, obj: str) -> None:
"""
    Delete triplet.
    1. Similar to upsert_triplet(),
       we have to assume rel to be the first edge_type.prop_name.
    2. After edge being deleted, we need to check if the subj or
       obj are isolated vertices,
       if so, delete them, too.
    """
    # lower case subj, rel, obj
    subj = escape_str(subj)
    rel = escape_str(rel)
    obj = escape_str(obj)

    if self._vid_type == "INT64":
        assert all([subj.isdigit(), obj.isdigit()]), (
            "Subject and object should be digit strings in current graph store."
        )
        subj_field = subj
        obj_field = obj
    else:
        subj_field = f"{QUOTE}{subj}{QUOTE}"
        obj_field = f"{QUOTE}{obj}{QUOTE}"
    edge_field = f"{subj_field}->{obj_field}"

    # DELETE EDGE serve "player100" -> "team204"@7696463696635583936;
    edge_type = self._edge_types[0]
    # rel_prop_name = self._rel_prop_names[0]
    rel_hash = hash_string_to_rank(rel)
    dml_query = f"DELETE EDGE `{edge_type}{edge_field}@{rel_hash};"
    logger.debug(f"delete()\nDML query: {dml_query}")
    result = self.execute(dml_query)
    assert result and result.is_succeeded(), (
        f"Failed to delete triplet: {subj}{rel}{obj}, query: {dml_query}"
    )
    # Get isolated vertices to be deleted
    # MATCH (s) WHERE id(s) IN ["player700"] AND NOT (s)-[]-()
    # RETURN id(s) AS isolated
    query = (
        f"MATCH (s) "
        f"  WHERE id(s) IN [{subj_field}, {obj_field}] "
        f"  AND NOT (s)-[]-() "
        f"RETURN id(s) AS isolated"
    )
    result = self.execute(query)
    isolated = result.column_values("isolated")
    if not isolated:
        return
    # DELETE VERTEX "player700" or DELETE VERTEX 700
    quote_field = QUOTE if self._vid_type != "INT64" else ""
    vertex_ids = ",".join(
        [f"{quote_field}{v.cast()}{quote_field}" for v in isolated]
    )
    dml_query = f"DELETE VERTEX {vertex_ids};"

    result = self.execute(dml_query)
    assert result and result.is_succeeded(), (
        f"Failed to delete isolated vertices: {isolated}, query: {dml_query}"
    )

```
 |  
| --- | --- |  
###  refresh_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore.refresh_schema "Permanent link")

```
refresh_schema() -> None

```

Refreshes the NebulaGraph Store Schema.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_graph_store.py`  
| 
```
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
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
```
 | 
```
defrefresh_schema(self) -> None:
"""
    Refreshes the NebulaGraph Store Schema.
    """
    tags_schema, edge_types_schema, relationships = [], [], []
    for tag in self.execute("SHOW TAGS").column_values("Name"):
        tag_name = tag.cast()
        tag_schema = {"tag": tag_name, "properties": []}
        r = self.execute(f"DESCRIBE TAG `{tag_name}`")
        props, types, comments = (
            r.column_values("Field"),
            r.column_values("Type"),
            r.column_values("Comment"),
        )
        for i in range(r.row_size()):
            # back compatible with old version of nebula-python
            property_defination = (
                (props[i].cast(), types[i].cast())
                if comments[i].is_empty()
                else (props[i].cast(), types[i].cast(), comments[i].cast())
            )
            tag_schema["properties"].append(property_defination)
        tags_schema.append(tag_schema)
    for edge_type in self.execute("SHOW EDGES").column_values("Name"):
        edge_type_name = edge_type.cast()
        edge_schema = {"edge": edge_type_name, "properties": []}
        r = self.execute(f"DESCRIBE EDGE `{edge_type_name}`")
        props, types, comments = (
            r.column_values("Field"),
            r.column_values("Type"),
            r.column_values("Comment"),
        )
        for i in range(r.row_size()):
            # back compatible with old version of nebula-python
            property_defination = (
                (props[i].cast(), types[i].cast())
                if comments[i].is_empty()
                else (props[i].cast(), types[i].cast(), comments[i].cast())
            )
            edge_schema["properties"].append(property_defination)
        edge_types_schema.append(edge_schema)

        # build relationships types
        sample_edge = self.execute(
            rel_query_sample_edge.substitute(edge_type=edge_type_name)
        ).column_values("sample_edge")
        if len(sample_edge) == 0:
            continue
        src_id, dst_id = sample_edge[0].cast()
        r = self.execute(
            rel_query_edge_type.substitute(
                edge_type=edge_type_name,
                src_id=src_id,
                dst_id=dst_id,
                quote="" if self._vid_type == "INT64" else QUOTE,
            )
        ).column_values("rels")
        if len(r)  0:
            relationships.append(r[0].cast())

    self.schema = (
        f"Node properties: {tags_schema}\n"
        f"Edge properties: {edge_types_schema}\n"
        f"Relationships: {relationships}\n"
    )

```
 |  
| --- | --- |  
###  get_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaGraphStore.get_schema "Permanent link")

```
get_schema(refresh:  = False) -> 

```

Get the schema of the NebulaGraph store.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_graph_store.py`  
| 
```
658
659
660
661
662
663
664
```
 | 
```
defget_schema(self, refresh: bool = False) -> str:
"""Get the schema of the NebulaGraph store."""
    if self.schema and not refresh:
        return self.schema
    self.refresh_schema()
    logger.debug(f"get_schema()\nschema: {self.schema}")
    return self.schema

```
 |  
| --- | --- |  
##  NebulaPropertyGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaPropertyGraphStore "Permanent link")
Bases: 
NebulaGraph Property Graph Store.
This class implements a NebulaGraph property graph store.
You could go with NebulaGraph-lite freely on Google Colab. - https://github.com/nebula-contrib/nebulagraph-lite Or Install with Docker Extension(search in the Docker Extension marketplace) on your local machine.
Examples:
`pip install llama-index-graph-stores-nebula` `pip install jupyter-nebulagraph`
Create a new NebulaGraph Space with Basic Schema:

```
%load_ext ngql
%ngql --address 127.0.0.1 --port 9669 --user root --password nebula
%ngql CREATE SPACE IF NOT EXISTS llamaindex_nebula_property_graph(vid_type=FIXED_STRING(256));

```

Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_property_graph.py`  
| 
```
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
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
```
 | 
```
classNebulaPropertyGraphStore(PropertyGraphStore):
"""
    NebulaGraph Property Graph Store.

    This class implements a NebulaGraph property graph store.

    You could go with NebulaGraph-lite freely on Google Colab.
    - https://github.com/nebula-contrib/nebulagraph-lite
    Or Install with Docker Extension(search in the Docker Extension marketplace) on your local machine.

    Examples:
        `pip install llama-index-graph-stores-nebula`
        `pip install jupyter-nebulagraph`

        Create a new NebulaGraph Space with Basic Schema:

        ```jupyter
        %load_ext ngql
        %ngql --address 127.0.0.1 --port 9669 --user root --password nebula
        %ngql CREATE SPACE IF NOT EXISTS llamaindex_nebula_property_graph(vid_type=FIXED_STRING(256));
        ```

    """

    _space: str
    _client: BaseExecutor
    sanitize_query_output: bool
    enhanced_schema: bool

    def__init__(
        self,
        space: str,
        client: Optional[BaseExecutor] = None,
        username: str = "root",
        password: str = "nebula",
        url: str = "nebula://localhost:9669",
        overwrite: bool = False,
        props_schema: str = DEFAULT_PROPS_SCHEMA,
        refresh_schema: bool = True,
        sanitize_query_output: bool = False,  # We don't put Embedding-Like values as Properties
        enhanced_schema: bool = False,
    ) -> None:
        self.sanitize_query_output = sanitize_query_output
        self.enhanced_schema = enhanced_schema

        self._space = space
        if client:
            self._client = client
        else:
            session_pool = SessionPool(
                username,
                password,
                self._space,
                [url_scheme_parse(url)],
            )
            session_pool.init()
            self._client = session_pool
        self._client.execute(DDL.render(props_schema=props_schema))
        self._client.execute(INDEX_DDL)
        if overwrite:
            self._client.execute(f"CLEAR SPACE {self._space};")

        self.structured_schema = {}
        if refresh_schema:
            try:
                self.refresh_schema()
            except Exception:
                # fails to refresh for the first time
                pass

        self.supports_structured_queries = True

    @property
    defclient(self):
"""Client of NebulaGraph."""
        return self._client

    def_execute(self, query: str) -> ResultSet:
        return self._client.execute(query)

    defrefresh_schema(self) -> None:
"""
        Refresh schema.

        Example data of self.structured_schema

            "node_props": {
                "Person": [
                    {"property": "name", "type": "STRING", "comment": "The name of the person"},
                    {"property": "age", "type": "INTEGER", "comment": "The age of the person"},
                    {"property": "dob", "type": "DATE", "comment": "The date of birth of the person"}

                "Company": [
                    {"property": "name", "type": "STRING", "comment": "The name of the company"},
                    {"property": "founded", "type": "DATE", "comment": "The date of foundation of the company"}


            "rel_props": {
                "WORKS_AT": [
                    {"property": "since", "type": "DATE", "comment": "The date when the person started working at the company"}

                "MANAGES": [
                    {"property": "since", "type": "DATE", "comment": "The date when the person started managing the company"}


            "relationships": [
                {"start": "Person", "type": "WORKS_AT", "end": "Company"},
                {"start": "Person", "type": "MANAGES", "end": "Company"}


        """
        tags_schema = {}
        edge_types_schema = {}
        relationships = []

        for node_label in self.structured_query(
            "MATCH ()-[node_label:`__meta__node_label__`]->() "
            "RETURN node_label.label AS name, "
            "JSON_EXTRACT(node_label.props_json) AS props"
        ):
            tags_schema[node_label["name"]] = []
            # TODO: add properties to tags_schema

        for rel_label in self.structured_query(
            "MATCH ()-[rel_label:`__meta__rel_label__`]->() "
            "RETURN rel_label.label AS name, "
            "src(rel_label) AS src, dst(rel_label) AS dst, "
            "JSON_EXTRACT(rel_label.props_json) AS props"
        ):
            edge_types_schema[rel_label["name"]] = []
            # TODO: add properties to edge_types_schema
            relationships.append(
                {
                    "start": rel_label["src"],
                    "type": rel_label["name"],
                    "end": rel_label["dst"],
                }
            )

        self.structured_schema = {
            "node_props": tags_schema,
            "rel_props": edge_types_schema,
            "relationships": relationships,
            # TODO: need to check necessarity of meta data here
        }

    defupsert_nodes(self, nodes: List[LabelledNode]) -> None:
        # meta tag Entity__ is used to store the entity name
        # meta tag Chunk__ is used to store the chunk text
        # other labels are used to store the entity properties
        # which must be created before upserting the nodes

        # Lists to hold separated types
        entity_list: List[EntityNode] = []
        chunk_list: List[ChunkNode] = []
        other_list: List[LabelledNode] = []

        # Sort by type
        for item in nodes:
            if isinstance(item, EntityNode):
                entity_list.append(item)
            elif isinstance(item, ChunkNode):
                chunk_list.append(item)
            else:
                other_list.append(item)

        if chunk_list:
            # TODO: need to double check other properties if any(it seems for now only text is there)
            # model chunk as tag and perform upsert
            # i.e. INSERT VERTEX `Chunk__` (`text`) VALUES "foo":("hello world"), "baz":("lorem ipsum");
            insert_query = "INSERT VERTEX `Chunk__` (`text`) VALUES "
            for i, chunk in enumerate(chunk_list):
                insert_query += f'"{chunk.id}":($chunk_{i}),'
            insert_query = insert_query[:-1]  # Remove trailing comma
            self.structured_query(
                insert_query,
                param_map={
                    f"chunk_{i}": chunk.text for i, chunk in enumerate(chunk_list)
                },
            )

        if entity_list:
            # model with tag Entity__ and other tags(label) if applicable
            # need to add properties as well, for extractors like SchemaLLMPathExtractor there is no properties
            # NebulaGraph is Schema-Full, so we need to be strong schema mindset to abstract this.
            # i.e.
            # INSERT VERTEX Entity__ (name) VALUES "foo":("bar"), "baz":("qux");
            # INSERT VERTEX Person (name) VALUES "foo":("bar"), "baz":("qux");

            # The meta tag Entity__ is used to store the entity name
            insert_query = "INSERT VERTEX `Entity__` (`name`) VALUES "
            for i, entity in enumerate(entity_list):
                insert_query += f'"{entity.id}":($entity_{i}),'
            insert_query = insert_query[:-1]  # Remove trailing comma
            self.structured_query(
                insert_query,
                param_map={
                    f"entity_{i}": entity.name for i, entity in enumerate(entity_list)
                },
            )
            mention_list = []  # Use a fresh variable name to be safe
            for entity in entity_list:
                if "triplet_source_id" in entity.properties:
                    chunk_id = entity.properties["triplet_source_id"]
                    mention_list.append(f'"{chunk_id}"->"{entity.id}"')  # Just the IDs

            if mention_list:  # Check if empty!
                values_str = ",".join(
                    [f"{pair}:()" for pair in mention_list]
                )  # Add the :() here
                edge_query = f"INSERT EDGE `MENTIONS` () VALUES {values_str}"
                self.structured_query(edge_query)

        # Create tags for each LabelledNode
        # This could be revisited, if we don't have any properties for labels, mapping labels to
        # Properties of tag: Entity__ is also feasible.
        schema_ensurence_cache = set()
        for i, entity in enumerate(nodes):
            keys, values_k, values_params = self._construct_property_query(
                entity.properties
            )
            stmt = f'INSERT VERTEX Props__ ({keys}) VALUES "{entity.id}":({values_k});'
            self.structured_query(
                stmt,
                param_map=values_params,
            )
            stmt = (
                f'INSERT VERTEX Node__ (label) VALUES "{entity.id}":("{entity.label}");'
            )
            # if entity.label not in schema_ensurence_cache:
            #     if ensure_node_meta_schema(
            #         entity.label, self.structured_schema, self.client, entity.properties
            #     ):
            #         self.refresh_schema()
            #         schema_ensurence_cache.add(entity.label)
            self.structured_query(stmt)

    def_construct_property_query(self, properties: Dict[str, Any]):
        keys = ",".join([f"`{k}`" for k in properties])
        values_k = ""
        values_params: Dict[Any] = {}
        for idx, v in enumerate(properties.values()):
            values_k += f"$kv_{idx},"
            values_params[f"kv_{idx}"] = v
        values_k = values_k[:-1]
        return keys, values_k, values_params

    defupsert_relations(self, relations: List[Relation]) -> None:
"""Add relations."""
        schema_ensurence_cache = set()
        for relation in relations:
            keys, values_k, values_params = self._construct_property_query(
                relation.properties
            )
            stmt = f'INSERT EDGE `Relation__` (`label`,{keys}) VALUES "{relation.source_id}"->"{relation.target_id}":("{relation.label}",{values_k});'
            # if relation.label not in schema_ensurence_cache:
            #     if ensure_relation_meta_schema(
            #         relation.source_id,
            #         relation.target_id,
            #         relation.label,
            #         self.structured_schema,
            #         self.client,
            #         relation.properties,
            #     ):
            #         self.refresh_schema()
            #         schema_ensurence_cache.add(relation.label)
            self.structured_query(stmt, param_map=values_params)

    defget(
        self,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[LabelledNode]:
"""Get nodes."""
        if not (properties or ids):
            return []
        else:
            return self._get(properties, ids)

    def_get(
        self,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[LabelledNode]:
"""Get nodes."""
        cypher_statement = "MATCH (e:Node__) "
        if properties or ids:
            cypher_statement += "WHERE "
        params = {}

        if ids:
            cypher_statement += f"id(e) in $all_id "
            params[f"all_id"] = ids
        if properties:
            for i, prop in enumerate(properties):
                cypher_statement += f"e.Props__.`{prop}` == $property_{i} AND "
                params[f"property_{i}"] = properties[prop]
            cypher_statement = cypher_statement[:-5]  # Remove trailing AND

        return_statement = """
        RETURN id(e) AS name,
               e.Node__.label AS type,
               properties(e.Props__) AS properties,
               properties(e) AS all_props
        """
        cypher_statement += return_statement
        cypher_statement = cypher_statement.replace("\n", " ")

        response = self.structured_query(cypher_statement, param_map=params)

        nodes = []
        for record in response:
            if "text" in record["all_props"]:
                node = ChunkNode(
                    id_=record["name"],
                    label=record["type"],
                    text=record["all_props"]["text"],
                    properties=remove_empty_values(record["properties"]),
                )
            elif "name" in record["all_props"]:
                node = EntityNode(
                    id_=record["name"],
                    label=record["type"],
                    name=record["all_props"]["name"],
                    properties=remove_empty_values(record["properties"]),
                )
            else:
                node = EntityNode(
                    name=record["name"],
                    type=record["type"],
                    properties=remove_empty_values(record["properties"]),
                )
            nodes.append(node)
        return nodes

    defget_all_nodes(self) -> List[LabelledNode]:
        return self._get()

    defget_triplets(
        self,
        entity_names: Optional[List[str]] = None,
        relation_names: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[Triplet]:
        cypher_statement = "MATCH (e:`Entity__`)-[r:`Relation__`]->(t:`Entity__`) "
        if not (entity_names or relation_names or properties or ids):
            return []
        else:
            cypher_statement += "WHERE "
        params = {}

        if entity_names:
            cypher_statement += (
                f"e.Entity__.name in $entities OR t.Entity__.name in $entities"
            )
            params[f"entities"] = entity_names
        if relation_names:
            cypher_statement += f"r.label in $relations "
            params[f"relations"] = relation_names
        if properties:
            pass
        if ids:
            cypher_statement += f"id(e) in $all_id OR id(t) in $all_id"
            params[f"all_id"] = ids
        if properties:
            v0_matching = ""
            v1_matching = ""
            edge_matching = ""
            for i, prop in enumerate(properties):
                v0_matching += f"e.Props__.`{prop}` == $property_{i} AND "
                v1_matching += f"t.Props__.`{prop}` == $property_{i} AND "
                edge_matching += f"r.`{prop}` == $property_{i} AND "
                params[f"property_{i}"] = properties[prop]
            v0_matching = v0_matching[:-5]  # Remove trailing AND
            v1_matching = v1_matching[:-5]  # Remove trailing AND
            edge_matching = edge_matching[:-5]  # Remove trailing AND
            cypher_statement += (
                f"({v0_matching}) OR ({edge_matching}) OR ({v1_matching})"
            )

        return_statement = f"""
        RETURN id(e) AS source_id, e.Node__.label AS source_type,
                properties(e.Props__) AS source_properties,
                r.label AS type,
                properties(r) AS rel_properties,
                id(t) AS target_id, t.Node__.label AS target_type,
                properties(t.Props__) AS target_properties
        """
        cypher_statement += return_statement
        cypher_statement = cypher_statement.replace("\n", " ")

        data = self.structured_query(cypher_statement, param_map=params)

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
            rel_properties = remove_empty_values(record["rel_properties"])
            rel_properties.pop("label")
            rel = Relation(
                source_id=record["source_id"],
                target_id=record["target_id"],
                label=record["type"],
                properties=rel_properties,
            )
            triples.append((source, rel, target))
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
            MATCH (e:`Entity__`)
            WHERE id(e) in $ids
            MATCH p=(e)-[r*1..{depth}]-(other)
            WHERE ALL(rel in relationships(p) WHERE rel.`label` <> 'MENTIONS')
            UNWIND relationships(p) AS rel
            WITH distinct rel
            WITH startNode(rel) AS source,
                rel.`label` AS type,
                endNode(rel) AS endNode
            MATCH (v) WHERE id(v)==id(source) WITH v AS source, type, endNode
            MATCH (v) WHERE id(v)==id(endNode) WITH source, type, v AS endNode
            RETURN id(source) AS source_id, source.`Node__`.`label` AS source_type,
                    properties(source.`Props__`) AS source_properties,
                    type,
                    id(endNode) AS target_id, endNode.`Node__`.`label` AS target_type,
                    properties(endNode.`Props__`) AS target_properties
            LIMIT {limit}
,
            param_map={"ids": ids},
        )

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
        if not param_map:
            result = self._client.execute(query)
        else:
            result = self._client.execute_parameter(query, build_param_map(param_map))
        if not result.is_succeeded():
            raise Exception(
                "NebulaGraph query failed:",
                result.error_msg(),
                "Statement:",
                query,
                "Params:",
                param_map,
            )
        full_result = [
            {
                key: result.row_values(row_index)[i].cast_primitive()
                for i, key in enumerate(result.keys())
            }
            for row_index in range(result.row_size())
        ]
        if self.sanitize_query_output:
            # Not applicable for NebulaGraph for now though
            return value_sanitize(full_result)

        return full_result

    defdelete(
        self,
        entity_names: Optional[List[str]] = None,
        relation_names: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
"""Delete matching data."""
        ans_ids: List[str] = []
        if entity_names:
            trips = self.get_triplets(
                entity_names=entity_names,
            )
            for trip in trips:
                if isinstance(trip[0], EntityNode) and trip[0].name in entity_names:
                    ans_ids.append(trip[0].id)
                if isinstance(trip[2], EntityNode) and trip[2].name in entity_names:
                    ans_ids.append(trip[2].id)
        if relation_names:
            trips = self.get_triplets(
                relation_names=relation_names,
            )
            for trip in trips:
                ans_ids += [trip[0].id, trip[2].id, trip[1].source_id]
        if properties:
            nodes = self.get(properties=properties)
            ans_ids += [node.id for node in nodes]
        if ids:
            nodes = self.get(ids=ids)
            ans_ids += [node.id for node in nodes]
        ans_ids = list(set(ans_ids))
        for id in ans_ids or []:
            self.structured_query(f'DELETE VERTEX "{id}" WITH EDGE;')

    def_enhanced_schema_cypher(
        self,
        label_or_type: str,
        properties: List[Dict[str, Any]],
        exhaustive: bool,
        is_relationship: bool = False,
    ) -> str:
"""Get enhanced schema information."""

    defget_schema(self, refresh: bool = False) -> Any:
        if refresh:
            self.refresh_schema()

        return self.structured_schema

    defget_schema_str(self, refresh: bool = False) -> str:
        schema = self.get_schema(refresh=refresh)

        formatted_node_props = []
        formatted_rel_props = []

        if self.enhanced_schema:
            # Enhanced formatting for nodes
            for node_type, properties in schema["node_props"].items():
                formatted_node_props.append(f"- **{node_type}**")
                for prop in properties:
                    example = ""
                    if prop["type"] == "string" and prop.get("values"):
                        if prop.get("distinct_count", 11)  DISTINCT_VALUE_LIMIT:
                            example = (
                                f'Example: "{clean_string_values(prop["values"][0])}"'
                                if prop["values"]
                                else ""
                            )
                        else:  # If less than 10 possible values return all
                            example = (
                                (
                                    "Available options: "
                                    f"{[clean_string_values(el)forelinprop['values']]}"
                                )
                                if prop["values"]
                                else ""
                            )

                    elif prop["type"] in [
                        # TODO: Add all numeric types
                        "int64",
                        "int32",
                        "int16",
                        "int8",
                        "uint64",
                        "uint32",
                        "uint16",
                        "uint8",
                        "date",
                        "datetime",
                        "timestamp",
                        "float",
                        "double",
                    ]:
                        if prop.get("min") is not None:
                            example = f"Min: {prop['min']}, Max: {prop['max']}"
                        else:
                            example = (
                                f'Example: "{prop["values"][0]}"'
                                if prop.get("values")
                                else ""
                            )
                    formatted_node_props.append(
                        f"  - `{prop['property']}`: {prop['type']}{example}"
                    )

            # Enhanced formatting for relationships
            for rel_type, properties in schema["rel_props"].items():
                formatted_rel_props.append(f"- **{rel_type}**")
                for prop in properties:
                    example = ""
                    if prop["type"] == "string":
                        if prop.get("distinct_count", 11)  DISTINCT_VALUE_LIMIT:
                            example = (
                                f'Example: "{clean_string_values(prop["values"][0])}"'
                                if prop.get("values")
                                else ""
                            )
                        else:  # If less than 10 possible values return all
                            example = (
                                (
                                    "Available options: "
                                    f"{[clean_string_values(el)forelinprop['values']]}"
                                )
                                if prop.get("values")
                                else ""
                            )
                    elif prop["type"] in [
                        "int",
                        "int64",
                        "int32",
                        "int16",
                        "int8",
                        "uint64",
                        "uint32",
                        "uint16",
                        "uint8",
                        "float",
                        "double",
                        "date",
                        "datetime",
                        "timestamp",
                    ]:
                        if prop.get("min"):  # If we have min/max
                            example = f"Min: {prop['min']}, Max:  {prop['max']}"
                        else:  # return a single value
                            example = (
                                f'Example: "{prop["values"][0]}"'
                                if prop.get("values")
                                else ""
                            )
                    elif prop["type"] == "LIST":
                        # Skip embeddings
                        if prop["min_size"]  LIST_LIMIT:
                            continue
                        example = f"Min Size: {prop['min_size']}, Max Size: {prop['max_size']}"
                    formatted_rel_props.append(
                        f"  - `{prop['property']}: {prop['type']}` {example}"
                    )
        else:
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

    defvector_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> Tuple[List[LabelledNode], List[float]]:
        raise NotImplementedError(
            "Vector query not implemented for NebulaPropertyGraphStore."
        )

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaPropertyGraphStore.client "Permanent link")

```
client

```

Client of NebulaGraph.
###  refresh_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaPropertyGraphStore.refresh_schema "Permanent link")

```
refresh_schema() -> None

```

Refresh schema.
Example data of self.structured_schema { "node_props": { "Person": [ {"property": "name", "type": "STRING", "comment": "The name of the person"}, {"property": "age", "type": "INTEGER", "comment": "The age of the person"}, {"property": "dob", "type": "DATE", "comment": "The date of birth of the person"} ], "Company": [ {"property": "name", "type": "STRING", "comment": "The name of the company"}, {"property": "founded", "type": "DATE", "comment": "The date of foundation of the company"} ] }, "rel_props": { "WORKS_AT": [ {"property": "since", "type": "DATE", "comment": "The date when the person started working at the company"} ], "MANAGES": [ {"property": "since", "type": "DATE", "comment": "The date when the person started managing the company"} ] }, "relationships": [ {"start": "Person", "type": "WORKS_AT", "end": "Company"}, {"start": "Person", "type": "MANAGES", "end": "Company"} ] }
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_property_graph.py`  
| 
```
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
```
 | 
```
defrefresh_schema(self) -> None:
"""
    Refresh schema.

    Example data of self.structured_schema

        "node_props": {
            "Person": [
                {"property": "name", "type": "STRING", "comment": "The name of the person"},
                {"property": "age", "type": "INTEGER", "comment": "The age of the person"},
                {"property": "dob", "type": "DATE", "comment": "The date of birth of the person"}

            "Company": [
                {"property": "name", "type": "STRING", "comment": "The name of the company"},
                {"property": "founded", "type": "DATE", "comment": "The date of foundation of the company"}


        "rel_props": {
            "WORKS_AT": [
                {"property": "since", "type": "DATE", "comment": "The date when the person started working at the company"}

            "MANAGES": [
                {"property": "since", "type": "DATE", "comment": "The date when the person started managing the company"}


        "relationships": [
            {"start": "Person", "type": "WORKS_AT", "end": "Company"},
            {"start": "Person", "type": "MANAGES", "end": "Company"}


    """
    tags_schema = {}
    edge_types_schema = {}
    relationships = []

    for node_label in self.structured_query(
        "MATCH ()-[node_label:`__meta__node_label__`]->() "
        "RETURN node_label.label AS name, "
        "JSON_EXTRACT(node_label.props_json) AS props"
    ):
        tags_schema[node_label["name"]] = []
        # TODO: add properties to tags_schema

    for rel_label in self.structured_query(
        "MATCH ()-[rel_label:`__meta__rel_label__`]->() "
        "RETURN rel_label.label AS name, "
        "src(rel_label) AS src, dst(rel_label) AS dst, "
        "JSON_EXTRACT(rel_label.props_json) AS props"
    ):
        edge_types_schema[rel_label["name"]] = []
        # TODO: add properties to edge_types_schema
        relationships.append(
            {
                "start": rel_label["src"],
                "type": rel_label["name"],
                "end": rel_label["dst"],
            }
        )

    self.structured_schema = {
        "node_props": tags_schema,
        "rel_props": edge_types_schema,
        "relationships": relationships,
        # TODO: need to check necessarity of meta data here
    }

```
 |  
| --- | --- |  
###  upsert_relations [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaPropertyGraphStore.upsert_relations "Permanent link")

```
upsert_relations(relations: []) -> None

```

Add relations.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_property_graph.py`  
| 
```
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
```
 | 
```
defupsert_relations(self, relations: List[Relation]) -> None:
"""Add relations."""
    schema_ensurence_cache = set()
    for relation in relations:
        keys, values_k, values_params = self._construct_property_query(
            relation.properties
        )
        stmt = f'INSERT EDGE `Relation__` (`label`,{keys}) VALUES "{relation.source_id}"->"{relation.target_id}":("{relation.label}",{values_k});'
        # if relation.label not in schema_ensurence_cache:
        #     if ensure_relation_meta_schema(
        #         relation.source_id,
        #         relation.target_id,
        #         relation.label,
        #         self.structured_schema,
        #         self.client,
        #         relation.properties,
        #     ):
        #         self.refresh_schema()
        #         schema_ensurence_cache.add(relation.label)
        self.structured_query(stmt, param_map=values_params)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaPropertyGraphStore.get "Permanent link")

```
get(
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> []

```

Get nodes.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_property_graph.py`  
| 
```
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
```
 | 
```
defget(
    self,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> List[LabelledNode]:
"""Get nodes."""
    if not (properties or ids):
        return []
    else:
        return self._get(properties, ids)

```
 |  
| --- | --- |  
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaPropertyGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    graph_nodes: [],
    depth:  = 2,
    limit:  = 30,
    ignore_rels: Optional[[]] = None,
) -> [Triplet]

```

Get depth-aware rel map.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_property_graph.py`  
| 
```
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
        MATCH (e:`Entity__`)
        WHERE id(e) in $ids
        MATCH p=(e)-[r*1..{depth}]-(other)
        WHERE ALL(rel in relationships(p) WHERE rel.`label` <> 'MENTIONS')
        UNWIND relationships(p) AS rel
        WITH distinct rel
        WITH startNode(rel) AS source,
            rel.`label` AS type,
            endNode(rel) AS endNode
        MATCH (v) WHERE id(v)==id(source) WITH v AS source, type, endNode
        MATCH (v) WHERE id(v)==id(endNode) WITH source, type, v AS endNode
        RETURN id(source) AS source_id, source.`Node__`.`label` AS source_type,
                properties(source.`Props__`) AS source_properties,
                type,
                id(endNode) AS target_id, endNode.`Node__`.`label` AS target_type,
                properties(endNode.`Props__`) AS target_properties
        LIMIT {limit}
        """,
        param_map={"ids": ids},
    )

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
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/nebula/#llama_index.graph_stores.nebula.NebulaPropertyGraphStore.delete "Permanent link")

```
delete(
    entity_names: Optional[[]] = None,
    relation_names: Optional[[]] = None,
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> None

```

Delete matching data.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-nebula/llama_index/graph_stores/nebula/nebula_property_graph.py`  
| 
```
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
    ans_ids: List[str] = []
    if entity_names:
        trips = self.get_triplets(
            entity_names=entity_names,
        )
        for trip in trips:
            if isinstance(trip[0], EntityNode) and trip[0].name in entity_names:
                ans_ids.append(trip[0].id)
            if isinstance(trip[2], EntityNode) and trip[2].name in entity_names:
                ans_ids.append(trip[2].id)
    if relation_names:
        trips = self.get_triplets(
            relation_names=relation_names,
        )
        for trip in trips:
            ans_ids += [trip[0].id, trip[2].id, trip[1].source_id]
    if properties:
        nodes = self.get(properties=properties)
        ans_ids += [node.id for node in nodes]
    if ids:
        nodes = self.get(ids=ids)
        ans_ids += [node.id for node in nodes]
    ans_ids = list(set(ans_ids))
    for id in ans_ids or []:
        self.structured_query(f'DELETE VERTEX "{id}" WITH EDGE;')

```
 |  
| --- | --- |  
options: members: - NebulaGraphStore - NebulaPropertyGraphStore
