# Neo4j
##  Neo4jGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jGraphStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/base.py`  
| 
```
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
```
 | 
```
classNeo4jGraphStore(GraphStore):
    def__init__(
        self,
        username: str,
        password: str,
        url: str,
        database: str = "neo4j",
        node_label: str = "Entity",
        refresh_schema: bool = True,
        timeout: Optional[float] = None,
        user_agent: str = "LLAMAINDEX-GRAPH",
        apoc_sample: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        self.node_label = node_label
        self._apoc_meta_config = (
            {"sample": apoc_sample} if apoc_sample is not None else {}
        )
        self._driver = neo4j.GraphDatabase.driver(
            url, auth=(username, password), user_agent=user_agent
        )
        self._database = database
        self._timeout = timeout
        self.schema = ""
        self.structured_schema: Dict[str, Any] = {}
        # Verify connection
        try:
            with self._driver as driver:
                driver.verify_connectivity()
        except neo4j.exceptions.ServiceUnavailable:
            raise ValueError(
                "Could not connect to Neo4j database. "
                "Please ensure that the url is correct"
            )
        except neo4j.exceptions.AuthError:
            raise ValueError(
                "Could not connect to Neo4j database. "
                "Please ensure that the username and password are correct"
            )
        # Set schema
        self.schema = ""
        self.structured_schema = {}
        if refresh_schema:
            try:
                self.refresh_schema()
            except neo4j.exceptions.ClientError:
                raise ValueError(
                    "Could not use APOC procedures. "
                    "Please ensure the APOC plugin is installed in Neo4j and that "
                    "'apoc.meta.data()' is allowed in Neo4j configuration "
                )
        # Create constraint for faster insert and retrieval
        try:  # Using Neo4j 5
            self.query(
"""
                CREATE CONSTRAINT IF NOT EXISTS FOR (n:%s) REQUIRE n.id IS UNIQUE;

                % (self.node_label)
            )
        except Exception:  # Using Neo4j <5
            self.query(
"""
                CREATE CONSTRAINT IF NOT EXISTS ON (n:%s) ASSERT n.id IS UNIQUE;

                % (self.node_label)
            )

    @property
    defclient(self) -> Any:
        return self._driver

    defget(self, subj: str) -> List[List[str]]:
"""Get triplets."""
        query = """
            MATCH (n1:%s)-[r]->(n2:%s)
            WHERE n1.id = $subj
            RETURN type(r), n2.id;
        """

        prepared_statement = query % (self.node_label, self.node_label)

        with self._driver.session(database=self._database) as session:
            data = session.run(prepared_statement, {"subj": subj})
            return [record.values() for record in data]

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

        query = (
            f"""MATCH p=(n1:{self.node_label})-[*1..{depth}]->() """
            f"""WHERE toLower(n1.id) IN {[subj.lower()forsubjinsubjs]ifsubjselse[]}"""
            "UNWIND relationships(p) AS rel "
            "WITH n1.id AS subj, p, apoc.coll.flatten(apoc.coll.toSet("
            "collect([type(rel), endNode(rel).id]))) AS flattened_rels "
            f"RETURN subj, collect(flattened_rels) AS flattened_rels LIMIT {limit}"
        )

        data = list(self.query(query, {"subjs": subjs}))
        if not data:
            return rel_map

        for record in data:
            rel_map[record["subj"]] = record["flattened_rels"]
        return rel_map

    defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
        query = """
            MERGE (n1:`%s` {id:$subj})
            MERGE (n2:`%s` {id:$obj})
            MERGE (n1)-[:`%s`]->(n2)
        """

        prepared_statement = query % (
            self.node_label,
            self.node_label,
            rel.replace(" ", "_").upper(),
        )

        with self._driver.session(database=self._database) as session:
            session.run(prepared_statement, {"subj": subj, "obj": obj})

    defdelete(self, subj: str, rel: str, obj: str) -> None:
"""Delete triplet."""

        defdelete_rel(subj: str, obj: str, rel: str) -> None:
            with self._driver.session(database=self._database) as session:
                session.run(
                    (
                        "MATCH (n1:{})-[r:{}]->(n2:{}) WHERE n1.id = $subj AND n2.id"
                        " = $obj DELETE r"
                    ).format(self.node_label, rel, self.node_label),
                    {"subj": subj, "obj": obj},
                )

        defdelete_entity(entity: str) -> None:
            with self._driver.session(database=self._database) as session:
                session.run(
                    "MATCH (n:%s) WHERE n.id = $entity DELETE n" % self.node_label,
                    {"entity": entity},
                )

        defcheck_edges(entity: str) -> bool:
            with self._driver.session(database=self._database) as session:
                is_exists_result = session.run(
                    "MATCH (n1:%s)--() WHERE n1.id = $entity RETURN count(*)"
                    % (self.node_label),
                    {"entity": entity},
                )
                return bool(list(is_exists_result))

        delete_rel(subj, obj, rel)
        if not check_edges(subj):
            delete_entity(subj)
        if not check_edges(obj):
            delete_entity(obj)

    defrefresh_schema(self) -> None:
"""
        Refreshes the Neo4j graph schema information.
        """
        config = {"config": self._apoc_meta_config}
        node_properties = [
            el["output"] for el in self.query(node_properties_query, param_map=config)
        ]
        rel_properties = [
            el["output"] for el in self.query(rel_properties_query, param_map=config)
        ]
        relationships = [el["output"] for el in self.query(rel_query, param_map=config)]

        self.structured_schema = {
            "node_props": {el["labels"]: el["properties"] for el in node_properties},
            "rel_props": {el["type"]: el["properties"] for el in rel_properties},
            "relationships": relationships,
        }

        # Format node properties
        formatted_node_props = []
        for el in node_properties:
            props_str = ", ".join(
                [f"{prop['property']}: {prop['type']}" for prop in el["properties"]]
            )
            formatted_node_props.append(f"{el['labels']}{{{props_str}}}")

        # Format relationship properties
        formatted_rel_props = []
        for el in rel_properties:
            props_str = ", ".join(
                [f"{prop['property']}: {prop['type']}" for prop in el["properties"]]
            )
            formatted_rel_props.append(f"{el['type']}{{{props_str}}}")

        # Format relationships
        formatted_rels = [
            f"(:{el['start']})-[:{el['type']}]->(:{el['end']})" for el in relationships
        ]

        self.schema = "\n".join(
            [
                "Node properties are the following:",
                ",".join(formatted_node_props),
                "Relationship properties are the following:",
                ",".join(formatted_rel_props),
                "The relationships are the following:",
                ",".join(formatted_rels),
            ]
        )

    defget_schema(self, refresh: bool = False) -> str:
"""Get the schema of the Neo4jGraph store."""
        if self.schema and not refresh:
            return self.schema
        self.refresh_schema()
        logger.debug(f"get_schema() schema:\n{self.schema}")
        return self.schema

    defquery(self, query: str, param_map: Optional[Dict[str, Any]] = None) -> Any:
        param_map = param_map or {}
        try:
            data, _, _ = self._driver.execute_query(
                neo4j.Query(text=query, timeout=self._timeout),
                database_=self._database,
                parameters_=param_map,
            )
            return [r.data() for r in data]
        except neo4j.exceptions.Neo4jError as e:
            if not (
                (
                    (  # isCallInTransactionError
                        e.code == "Neo.DatabaseError.Statement.ExecutionFailed"
                        or e.code
                        == "Neo.DatabaseError.Transaction.TransactionStartFailed"
                    )
                    and "in an implicit transaction" in e.message
                )
                or (  # isPeriodicCommitError
                    e.code == "Neo.ClientError.Statement.SemanticError"
                    and (
                        "in an open transaction is not possible" in e.message
                        or "tried to execute in an explicit transaction" in e.message
                    )
                )
            ):
                raise
        # Fallback to allow implicit transactions
        with self._driver.session(database=self._database) as session:
            data = session.run(
                neo4j.Query(text=query, timeout=self._timeout), param_map
            )
            return [r.data() for r in data]

    defclose(self) -> None:
"""
        Explicitly close the Neo4j driver connection.

        Delegates connection management to the Neo4j driver.
        """
        if hasattr(self, "_driver"):
            self._driver.close()
            # Remove the driver attribute to indicate closure
            delattr(self, "_driver")

    def__enter__(self) -> "Neo4jGraphStore":
"""
        Enter the runtime context for the Neo4j graph connection.

        Enables use of the graph connection with the 'with' statement.
        This method allows for automatic resource management and ensures
        that the connection is properly handled.

        Returns:
            Neo4jPropertyGraphStore: The current graph connection instance

        """
        return self

    def__exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
"""
        Exit the runtime context for the Neo4j graph connection.

        This method is automatically called when exiting a 'with' statement.
        It ensures that the database connection is closed, regardless of
        whether an exception occurred during the context's execution.

        Args:
            exc_type: The type of exception that caused the context to exit
                      (None if no exception occurred)
            exc_val: The exception instance that caused the context to exit
                     (None if no exception occurred)
            exc_tb: The traceback for the exception (None if no exception occurred)

        Note:
            Any exception is re-raised after the connection is closed.

        """
        self.close()

    def__del__(self) -> None:
"""
        Destructor for the Neo4j graph connection.

        This method is called during garbage collection to ensure that
        database resources are released if not explicitly closed.

        Caution:
            - Do not rely on this method for deterministic resource cleanup
            - Always prefer explicit .close() or context manager

        Best practices:
            1. Use context manager:
               with Neo4jGraph(...) as graph:

            2. Explicitly close:
               graph = Neo4jGraph(...)
               try:

               finally:
                   graph.close()

        """
        try:
            self.close()
        except Exception:
            # Suppress any exceptions during garbage collection
            pass

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jGraphStore.get "Permanent link")

```
get(subj: ) -> [[]]

```

Get triplets.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/base.py`  
| 
```
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
```
 | 
```
defget(self, subj: str) -> List[List[str]]:
"""Get triplets."""
    query = """
        MATCH (n1:%s)-[r]->(n2:%s)
        WHERE n1.id = $subj
        RETURN type(r), n2.id;
    """

    prepared_statement = query % (self.node_label, self.node_label)

    with self._driver.session(database=self._database) as session:
        data = session.run(prepared_statement, {"subj": subj})
        return [record.values() for record in data]

```
 |  
| --- | --- |  
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    subjs: Optional[[]] = None,
    depth:  = 2,
    limit:  = 30,
) -> [, [[]]]

```

Get flat rel map.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/base.py`  
| 
```
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

    query = (
        f"""MATCH p=(n1:{self.node_label})-[*1..{depth}]->() """
        f"""WHERE toLower(n1.id) IN {[subj.lower()forsubjinsubjs]ifsubjselse[]}"""
        "UNWIND relationships(p) AS rel "
        "WITH n1.id AS subj, p, apoc.coll.flatten(apoc.coll.toSet("
        "collect([type(rel), endNode(rel).id]))) AS flattened_rels "
        f"RETURN subj, collect(flattened_rels) AS flattened_rels LIMIT {limit}"
    )

    data = list(self.query(query, {"subjs": subjs}))
    if not data:
        return rel_map

    for record in data:
        rel_map[record["subj"]] = record["flattened_rels"]
    return rel_map

```
 |  
| --- | --- |  
###  upsert_triplet [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jGraphStore.upsert_triplet "Permanent link")

```
upsert_triplet(subj: , rel: , obj: ) -> None

```

Add triplet.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/base.py`  
| 
```
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
defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
    query = """
        MERGE (n1:`%s` {id:$subj})
        MERGE (n2:`%s` {id:$obj})
        MERGE (n1)-[:`%s`]->(n2)
    """

    prepared_statement = query % (
        self.node_label,
        self.node_label,
        rel.replace(" ", "_").upper(),
    )

    with self._driver.session(database=self._database) as session:
        session.run(prepared_statement, {"subj": subj, "obj": obj})

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jGraphStore.delete "Permanent link")

```
delete(subj: , rel: , obj: ) -> None

```

Delete triplet.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/base.py`  
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
```
 | 
```
defdelete(self, subj: str, rel: str, obj: str) -> None:
"""Delete triplet."""

    defdelete_rel(subj: str, obj: str, rel: str) -> None:
        with self._driver.session(database=self._database) as session:
            session.run(
                (
                    "MATCH (n1:{})-[r:{}]->(n2:{}) WHERE n1.id = $subj AND n2.id"
                    " = $obj DELETE r"
                ).format(self.node_label, rel, self.node_label),
                {"subj": subj, "obj": obj},
            )

    defdelete_entity(entity: str) -> None:
        with self._driver.session(database=self._database) as session:
            session.run(
                "MATCH (n:%s) WHERE n.id = $entity DELETE n" % self.node_label,
                {"entity": entity},
            )

    defcheck_edges(entity: str) -> bool:
        with self._driver.session(database=self._database) as session:
            is_exists_result = session.run(
                "MATCH (n1:%s)--() WHERE n1.id = $entity RETURN count(*)"
                % (self.node_label),
                {"entity": entity},
            )
            return bool(list(is_exists_result))

    delete_rel(subj, obj, rel)
    if not check_edges(subj):
        delete_entity(subj)
    if not check_edges(obj):
        delete_entity(obj)

```
 |  
| --- | --- |  
###  refresh_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jGraphStore.refresh_schema "Permanent link")

```
refresh_schema() -> None

```

Refreshes the Neo4j graph schema information.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/base.py`  
| 
```
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
```
 | 
```
defrefresh_schema(self) -> None:
"""
    Refreshes the Neo4j graph schema information.
    """
    config = {"config": self._apoc_meta_config}
    node_properties = [
        el["output"] for el in self.query(node_properties_query, param_map=config)
    ]
    rel_properties = [
        el["output"] for el in self.query(rel_properties_query, param_map=config)
    ]
    relationships = [el["output"] for el in self.query(rel_query, param_map=config)]

    self.structured_schema = {
        "node_props": {el["labels"]: el["properties"] for el in node_properties},
        "rel_props": {el["type"]: el["properties"] for el in rel_properties},
        "relationships": relationships,
    }

    # Format node properties
    formatted_node_props = []
    for el in node_properties:
        props_str = ", ".join(
            [f"{prop['property']}: {prop['type']}" for prop in el["properties"]]
        )
        formatted_node_props.append(f"{el['labels']}{{{props_str}}}")

    # Format relationship properties
    formatted_rel_props = []
    for el in rel_properties:
        props_str = ", ".join(
            [f"{prop['property']}: {prop['type']}" for prop in el["properties"]]
        )
        formatted_rel_props.append(f"{el['type']}{{{props_str}}}")

    # Format relationships
    formatted_rels = [
        f"(:{el['start']})-[:{el['type']}]->(:{el['end']})" for el in relationships
    ]

    self.schema = "\n".join(
        [
            "Node properties are the following:",
            ",".join(formatted_node_props),
            "Relationship properties are the following:",
            ",".join(formatted_rel_props),
            "The relationships are the following:",
            ",".join(formatted_rels),
        ]
    )

```
 |  
| --- | --- |  
###  get_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jGraphStore.get_schema "Permanent link")

```
get_schema(refresh:  = False) -> 

```

Get the schema of the Neo4jGraph store.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/base.py`  
| 
```
264
265
266
267
268
269
270
```
 | 
```
defget_schema(self, refresh: bool = False) -> str:
"""Get the schema of the Neo4jGraph store."""
    if self.schema and not refresh:
        return self.schema
    self.refresh_schema()
    logger.debug(f"get_schema() schema:\n{self.schema}")
    return self.schema

```
 |  
| --- | --- |  
###  close [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jGraphStore.close "Permanent link")

```
close() -> None

```

Explicitly close the Neo4j driver connection.
Delegates connection management to the Neo4j driver.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/base.py`  
| 
```
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
```
 | 
```
defclose(self) -> None:
"""
    Explicitly close the Neo4j driver connection.

    Delegates connection management to the Neo4j driver.
    """
    if hasattr(self, "_driver"):
        self._driver.close()
        # Remove the driver attribute to indicate closure
        delattr(self, "_driver")

```
 |  
| --- | --- |  
##  CypherQueryCorrector [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.CypherQueryCorrector "Permanent link")
Used to correct relationship direction in generated Cypher statements.
This code is copied from the winner's submission to the Cypher competition: https://github.com/sakusaku-rich/cypher-direction-competition
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/cypher_corrector.py`  
| 
```
 11
 12
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
```
 | 
```
classCypherQueryCorrector:
"""
    Used to correct relationship direction in generated Cypher statements.

    This code is copied from the winner's submission to the Cypher competition:
    https://github.com/sakusaku-rich/cypher-direction-competition
    """

    property_pattern = re.compile(r"\{.+?\}")
    node_pattern = re.compile(r"\(.+?\)")
    path_pattern = re.compile(
        r"(\([^\,\(\)]*?(\{.+\})?[^\,\(\)]*?\))(<?-)(\[.*?\])?(->?)(\([^\,\(\)]*?(\{.+\})?[^\,\(\)]*?\))"
    )
    node_relation_node_pattern = re.compile(
        r"(\()+(?P<left_node>[^()]*?)\)(?P<relation>.*?)\((?P<right_node>[^()]*?)(\))+"
    )
    relation_type_pattern = re.compile(r":(?P<relation_type>.+?)?(\{.+\})?]")

    def__init__(self, schemas: List[Schema]):
"""
        Init function.

        Args:
            schemas: list of schemas

        """
        self.schemas = schemas

    defclean_node(self, node: str) -> str:
"""
        Strip node of parenthesis.

        Args:
            node: node in string format

        """
        return (
            re.sub(self.property_pattern, "", node)
            .replace("(", "")
            .replace(")", "")
            .strip()
        )

    defdetect_node_variables(self, query: str) -> Dict[str, List[str]]:
"""
        Detect node variables.

        Args:
            query: cypher query

        """
        nodes = [self.clean_node(node) for node in re.findall(self.node_pattern, query)]
        res: Dict[str, Any] = {}
        for node in nodes:
            parts = node.split(":")
            if parts == "":
                continue
            variable = parts[0]
            if variable not in res:
                res[variable] = []
            res[variable] += parts[1:]
        return res

    defextract_paths(self, query: str) -> "List[str]":
"""
        Extract paths.

        Args:
            query: cypher query

        """
        paths = []
        idx = 0
        while matched := self.path_pattern.findall(query[idx:]):
            matched = matched[0]
            matched = [
                m for i, m in enumerate(matched) if i not in [1, len(matched) - 1]
            ]
            path = "".join(matched)
            idx = query.find(path) + len(path) - len(matched[-1])
            paths.append(path)
        return paths

    defjudge_direction(self, relation: str) -> str:
"""
        Judge direction.

        Args:
            relation: relation in string format

        """
        direction = "BIDIRECTIONAL"
        if relation[0] == "<":
            direction = "INCOMING"
        if relation[-1] == ">":
            direction = "OUTGOING"
        return direction

    defextract_node_variable(self, part: str) -> Optional[str]:
"""
        Extract node variable.

        Args:
            part: node in string format

        """
        part = part.lstrip("(").rstrip(")")
        idx = part.find(":")
        if idx != -1:
            part = part[:idx]
        return None if part == "" else part

    defdetect_labels(
        self, str_node: str, node_variable_dict: Dict[str, Any]
    ) -> List[str]:
"""
        Detect node labels.

        Args:
            str_node: node in string format
            node_variable_dict: dictionary of node variables

        """
        splitted_node = str_node.split(":")
        variable = splitted_node[0]
        labels = []
        if variable in node_variable_dict:
            labels = node_variable_dict[variable]
        elif variable == "" and len(splitted_node)  1:
            labels = splitted_node[1:]
        return labels

    defverify_schema(
        self,
        from_node_labels: List[str],
        relation_types: List[str],
        to_node_labels: List[str],
    ) -> bool:
"""
        Verify schema.

        Args:
            from_node_labels: labels of the from node
            relation_type: type of the relation
            to_node_labels: labels of the to node

        """
        valid_schemas = self.schemas
        if from_node_labels != []:
            from_node_labels = [label.strip("`") for label in from_node_labels]
            valid_schemas = [
                schema for schema in valid_schemas if schema[0] in from_node_labels
            ]
        if to_node_labels != []:
            to_node_labels = [label.strip("`") for label in to_node_labels]
            valid_schemas = [
                schema for schema in valid_schemas if schema[2] in to_node_labels
            ]
        if relation_types != []:
            relation_types = [type.strip("`") for type in relation_types]
            valid_schemas = [
                schema for schema in valid_schemas if schema[1] in relation_types
            ]
        return valid_schemas != []

    defdetect_relation_types(self, str_relation: str) -> Tuple[str, List[str]]:
"""
        Detect relation types.

        Args:
            str_relation: relation in string format

        """
        relation_direction = self.judge_direction(str_relation)
        relation_type = self.relation_type_pattern.search(str_relation)
        if relation_type is None or relation_type.group("relation_type") is None:
            return relation_direction, []
        relation_types = [
            t.strip().strip("!")
            for t in relation_type.group("relation_type").split("|")
        ]
        return relation_direction, relation_types

    defcorrect_query(self, query: str) -> str:
"""
        Correct query.

        Args:
            query: cypher query

        """
        node_variable_dict = self.detect_node_variables(query)
        paths = self.extract_paths(query)
        for path in paths:
            original_path = path
            start_idx = 0
            while start_idx  len(path):
                match_res = re.match(self.node_relation_node_pattern, path[start_idx:])
                if match_res is None:
                    break
                start_idx += match_res.start()
                match_dict = match_res.groupdict()
                left_node_labels = self.detect_labels(
                    match_dict["left_node"], node_variable_dict
                )
                right_node_labels = self.detect_labels(
                    match_dict["right_node"], node_variable_dict
                )
                end_idx = (
                    start_idx
                    + 4
                    + len(match_dict["left_node"])
                    + len(match_dict["relation"])
                    + len(match_dict["right_node"])
                )
                original_partial_path = original_path[start_idx : end_idx + 1]
                relation_direction, relation_types = self.detect_relation_types(
                    match_dict["relation"]
                )

                if relation_types != [] and "".join(relation_types).find("*") != -1:
                    start_idx += (
                        len(match_dict["left_node"]) + len(match_dict["relation"]) + 2
                    )
                    continue

                if relation_direction == "OUTGOING":
                    is_legal = self.verify_schema(
                        left_node_labels, relation_types, right_node_labels
                    )
                    if not is_legal:
                        is_legal = self.verify_schema(
                            right_node_labels, relation_types, left_node_labels
                        )
                        if is_legal:
                            corrected_relation = "<" + match_dict["relation"][:-1]
                            corrected_partial_path = original_partial_path.replace(
                                match_dict["relation"], corrected_relation
                            )
                            query = query.replace(
                                original_partial_path, corrected_partial_path
                            )
                        else:
                            return ""
                elif relation_direction == "INCOMING":
                    is_legal = self.verify_schema(
                        right_node_labels, relation_types, left_node_labels
                    )
                    if not is_legal:
                        is_legal = self.verify_schema(
                            left_node_labels, relation_types, right_node_labels
                        )
                        if is_legal:
                            corrected_relation = match_dict["relation"][1:] + ">"
                            corrected_partial_path = original_partial_path.replace(
                                match_dict["relation"], corrected_relation
                            )
                            query = query.replace(
                                original_partial_path, corrected_partial_path
                            )
                        else:
                            return ""
                else:
                    is_legal = self.verify_schema(
                        left_node_labels, relation_types, right_node_labels
                    )
                    is_legal |= self.verify_schema(
                        right_node_labels, relation_types, left_node_labels
                    )
                    if not is_legal:
                        return ""

                start_idx += (
                    len(match_dict["left_node"]) + len(match_dict["relation"]) + 2
                )
        return query

    def__call__(self, query: str) -> str:
"""
        Correct the query to make it valid.

        Args:
            query: cypher query

        """
        return self.correct_query(query)

```
 |  
| --- | --- |  
###  clean_node [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.CypherQueryCorrector.clean_node "Permanent link")

```
clean_node(node: ) -> 

```

Strip node of parenthesis.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node`  |  node in string format  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/cypher_corrector.py`  
| 
```
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
```
 | 
```
defclean_node(self, node: str) -> str:
"""
    Strip node of parenthesis.

    Args:
        node: node in string format

    """
    return (
        re.sub(self.property_pattern, "", node)
        .replace("(", "")
        .replace(")", "")
        .strip()
    )

```
 |  
| --- | --- |  
###  detect_node_variables [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.CypherQueryCorrector.detect_node_variables "Permanent link")

```
detect_node_variables(query: ) -> [, []]

```

Detect node variables.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  cypher query  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/cypher_corrector.py`  
| 
```
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
```
 | 
```
defdetect_node_variables(self, query: str) -> Dict[str, List[str]]:
"""
    Detect node variables.

    Args:
        query: cypher query

    """
    nodes = [self.clean_node(node) for node in re.findall(self.node_pattern, query)]
    res: Dict[str, Any] = {}
    for node in nodes:
        parts = node.split(":")
        if parts == "":
            continue
        variable = parts[0]
        if variable not in res:
            res[variable] = []
        res[variable] += parts[1:]
    return res

```
 |  
| --- | --- |  
###  extract_paths [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.CypherQueryCorrector.extract_paths "Permanent link")

```
extract_paths(query: ) -> []

```

Extract paths.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  cypher query  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/cypher_corrector.py`  
| 
```
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
```
 | 
```
defextract_paths(self, query: str) -> "List[str]":
"""
    Extract paths.

    Args:
        query: cypher query

    """
    paths = []
    idx = 0
    while matched := self.path_pattern.findall(query[idx:]):
        matched = matched[0]
        matched = [
            m for i, m in enumerate(matched) if i not in [1, len(matched) - 1]
        ]
        path = "".join(matched)
        idx = query.find(path) + len(path) - len(matched[-1])
        paths.append(path)
    return paths

```
 |  
| --- | --- |  
###  judge_direction [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.CypherQueryCorrector.judge_direction "Permanent link")

```
judge_direction(relation: ) -> 

```

Judge direction.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `relation`  |  relation in string format  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/cypher_corrector.py`  
| 
```
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
```
 | 
```
defjudge_direction(self, relation: str) -> str:
"""
    Judge direction.

    Args:
        relation: relation in string format

    """
    direction = "BIDIRECTIONAL"
    if relation[0] == "<":
        direction = "INCOMING"
    if relation[-1] == ">":
        direction = "OUTGOING"
    return direction

```
 |  
| --- | --- |  
###  extract_node_variable [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.CypherQueryCorrector.extract_node_variable "Permanent link")

```
extract_node_variable(part: ) -> Optional[]

```

Extract node variable.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `part`  |  node in string format  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/cypher_corrector.py`  
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
```
 | 
```
defextract_node_variable(self, part: str) -> Optional[str]:
"""
    Extract node variable.

    Args:
        part: node in string format

    """
    part = part.lstrip("(").rstrip(")")
    idx = part.find(":")
    if idx != -1:
        part = part[:idx]
    return None if part == "" else part

```
 |  
| --- | --- |  
###  detect_labels [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.CypherQueryCorrector.detect_labels "Permanent link")

```
detect_labels(
    str_node: , node_variable_dict: [, ]
) -> []

```

Detect node labels.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `str_node`  |  node in string format  |  _required_  |  
|  `node_variable_dict`  |  `Dict[str, Any]`  |  dictionary of node variables  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/cypher_corrector.py`  
| 
```
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
defdetect_labels(
    self, str_node: str, node_variable_dict: Dict[str, Any]
) -> List[str]:
"""
    Detect node labels.

    Args:
        str_node: node in string format
        node_variable_dict: dictionary of node variables

    """
    splitted_node = str_node.split(":")
    variable = splitted_node[0]
    labels = []
    if variable in node_variable_dict:
        labels = node_variable_dict[variable]
    elif variable == "" and len(splitted_node)  1:
        labels = splitted_node[1:]
    return labels

```
 |  
| --- | --- |  
###  verify_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.CypherQueryCorrector.verify_schema "Permanent link")

```
verify_schema(
    from_node_labels: [],
    relation_types: [],
    to_node_labels: [],
) -> 

```

Verify schema.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `from_node_labels`  |  `List[str]`  |  labels of the from node  |  _required_  |  
|  `relation_type`  |  type of the relation  |  _required_  |  
|  `to_node_labels`  |  `List[str]`  |  labels of the to node  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/cypher_corrector.py`  
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
```
 | 
```
defverify_schema(
    self,
    from_node_labels: List[str],
    relation_types: List[str],
    to_node_labels: List[str],
) -> bool:
"""
    Verify schema.

    Args:
        from_node_labels: labels of the from node
        relation_type: type of the relation
        to_node_labels: labels of the to node

    """
    valid_schemas = self.schemas
    if from_node_labels != []:
        from_node_labels = [label.strip("`") for label in from_node_labels]
        valid_schemas = [
            schema for schema in valid_schemas if schema[0] in from_node_labels
        ]
    if to_node_labels != []:
        to_node_labels = [label.strip("`") for label in to_node_labels]
        valid_schemas = [
            schema for schema in valid_schemas if schema[2] in to_node_labels
        ]
    if relation_types != []:
        relation_types = [type.strip("`") for type in relation_types]
        valid_schemas = [
            schema for schema in valid_schemas if schema[1] in relation_types
        ]
    return valid_schemas != []

```
 |  
| --- | --- |  
###  detect_relation_types [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.CypherQueryCorrector.detect_relation_types "Permanent link")

```
detect_relation_types(
    str_relation: ,
) -> Tuple[, []]

```

Detect relation types.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `str_relation`  |  relation in string format  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/cypher_corrector.py`  
| 
```
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
```
 | 
```
defdetect_relation_types(self, str_relation: str) -> Tuple[str, List[str]]:
"""
    Detect relation types.

    Args:
        str_relation: relation in string format

    """
    relation_direction = self.judge_direction(str_relation)
    relation_type = self.relation_type_pattern.search(str_relation)
    if relation_type is None or relation_type.group("relation_type") is None:
        return relation_direction, []
    relation_types = [
        t.strip().strip("!")
        for t in relation_type.group("relation_type").split("|")
    ]
    return relation_direction, relation_types

```
 |  
| --- | --- |  
###  correct_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.CypherQueryCorrector.correct_query "Permanent link")

```
correct_query(query: ) -> 

```

Correct query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  cypher query  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/cypher_corrector.py`  
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
```
 | 
```
defcorrect_query(self, query: str) -> str:
"""
    Correct query.

    Args:
        query: cypher query

    """
    node_variable_dict = self.detect_node_variables(query)
    paths = self.extract_paths(query)
    for path in paths:
        original_path = path
        start_idx = 0
        while start_idx  len(path):
            match_res = re.match(self.node_relation_node_pattern, path[start_idx:])
            if match_res is None:
                break
            start_idx += match_res.start()
            match_dict = match_res.groupdict()
            left_node_labels = self.detect_labels(
                match_dict["left_node"], node_variable_dict
            )
            right_node_labels = self.detect_labels(
                match_dict["right_node"], node_variable_dict
            )
            end_idx = (
                start_idx
                + 4
                + len(match_dict["left_node"])
                + len(match_dict["relation"])
                + len(match_dict["right_node"])
            )
            original_partial_path = original_path[start_idx : end_idx + 1]
            relation_direction, relation_types = self.detect_relation_types(
                match_dict["relation"]
            )

            if relation_types != [] and "".join(relation_types).find("*") != -1:
                start_idx += (
                    len(match_dict["left_node"]) + len(match_dict["relation"]) + 2
                )
                continue

            if relation_direction == "OUTGOING":
                is_legal = self.verify_schema(
                    left_node_labels, relation_types, right_node_labels
                )
                if not is_legal:
                    is_legal = self.verify_schema(
                        right_node_labels, relation_types, left_node_labels
                    )
                    if is_legal:
                        corrected_relation = "<" + match_dict["relation"][:-1]
                        corrected_partial_path = original_partial_path.replace(
                            match_dict["relation"], corrected_relation
                        )
                        query = query.replace(
                            original_partial_path, corrected_partial_path
                        )
                    else:
                        return ""
            elif relation_direction == "INCOMING":
                is_legal = self.verify_schema(
                    right_node_labels, relation_types, left_node_labels
                )
                if not is_legal:
                    is_legal = self.verify_schema(
                        left_node_labels, relation_types, right_node_labels
                    )
                    if is_legal:
                        corrected_relation = match_dict["relation"][1:] + ">"
                        corrected_partial_path = original_partial_path.replace(
                            match_dict["relation"], corrected_relation
                        )
                        query = query.replace(
                            original_partial_path, corrected_partial_path
                        )
                    else:
                        return ""
            else:
                is_legal = self.verify_schema(
                    left_node_labels, relation_types, right_node_labels
                )
                is_legal |= self.verify_schema(
                    right_node_labels, relation_types, left_node_labels
                )
                if not is_legal:
                    return ""

            start_idx += (
                len(match_dict["left_node"]) + len(match_dict["relation"]) + 2
            )
    return query

```
 |  
| --- | --- |  
##  Neo4jPropertyGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jPropertyGraphStore "Permanent link")
Bases: 
Neo4j Property Graph Store.
This class implements a Neo4j property graph store.
If you are using local Neo4j instead of aura, here's a helpful command for launching the docker container:

```
dockerrun\
-p7474:7474-p7687:7687\
-v$PWD/data:/data-v$PWD/plugins:/plugins\
--nameneo4j-apoc\
-eNEO4J_apoc_export_file_enabled=true\
-eNEO4J_apoc_import_file_enabled=true\
-eNEO4J_apoc_import_file_use__neo4j__config=true\
-eNEO4JLABS_PLUGINS=\\[\"apoc\"\\]\
neo4j:latest

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `username`  |  The username for the Neo4j database.  |  _required_  |  
|  `password`  |  The password for the Neo4j database.  |  _required_  |  
|  `url`  |  The URL for the Neo4j database.  |  _required_  |  
|  `database`  |  `Optional[str]`  |  The name of the database to connect to. Defaults to "neo4j".  |  `'neo4j'`  |  
|  `timeout`  |  `Optional[float]`  |  The timeout for transactions in seconds.  |  `None`  |  
|  `apoc_sample`  |  `Optional[int]`  |  The number of nodes/rels to sample when calling  |  `None`  |  
Examples:
`pip install llama-index-graph-stores-neo4j`

```
fromllama_index.core.indices.property_graphimport PropertyGraphIndex
fromllama_index.graph_stores.neo4jimport Neo4jPropertyGraphStore

# Create a Neo4jPropertyGraphStore instance
graph_store = Neo4jPropertyGraphStore(
    username="neo4j",
    password="neo4j",
    url="bolt://localhost:7687",
    database="neo4j"
)

# create the index
index = PropertyGraphIndex.from_documents(
    documents,
    property_graph_store=graph_store,
)

# Close the neo4j connection explicitly.
graph_store.close()

```

Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/neo4j_property_graph.py`  
| 
```
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
 784
 785
 786
 787
 788
 789
 790
 791
 792
 793
 794
 795
 796
 797
 798
 799
 800
 801
 802
 803
 804
 805
 806
 807
 808
 809
 810
 811
 812
 813
 814
 815
 816
 817
 818
 819
 820
 821
 822
 823
 824
 825
 826
 827
 828
 829
 830
 831
 832
 833
 834
 835
 836
 837
 838
 839
 840
 841
 842
 843
 844
 845
 846
 847
 848
 849
 850
 851
 852
 853
 854
 855
 856
 857
 858
 859
 860
 861
 862
 863
 864
 865
 866
 867
 868
 869
 870
 871
 872
 873
 874
 875
 876
 877
 878
 879
 880
 881
 882
 883
 884
 885
 886
 887
 888
 889
 890
 891
 892
 893
 894
 895
 896
 897
 898
 899
 900
 901
 902
 903
 904
 905
 906
 907
 908
 909
 910
 911
 912
 913
 914
 915
 916
 917
 918
 919
 920
 921
 922
 923
 924
 925
 926
 927
 928
 929
 930
 931
 932
 933
 934
 935
 936
 937
 938
 939
 940
 941
 942
 943
 944
 945
 946
 947
 948
 949
 950
 951
 952
 953
 954
 955
 956
 957
 958
 959
 960
 961
 962
 963
 964
 965
 966
 967
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
```
 | 
```
classNeo4jPropertyGraphStore(PropertyGraphStore):
r"""
    Neo4j Property Graph Store.

    This class implements a Neo4j property graph store.

    If you are using local Neo4j instead of aura, here's a helpful
    command for launching the docker container:

    ```bash
    docker run \
        -p 7474:7474 -p 7687:7687 \
        -v $PWD/data:/data -v $PWD/plugins:/plugins \
        --name neo4j-apoc \
        -e NEO4J_apoc_export_file_enabled=true \
        -e NEO4J_apoc_import_file_enabled=true \
        -e NEO4J_apoc_import_file_use__neo4j__config=true \
        -e NEO4JLABS_PLUGINS=\\[\"apoc\"\\] \
        neo4j:latest
    ```

    Args:
        username (str): The username for the Neo4j database.
        password (str): The password for the Neo4j database.
        url (str): The URL for the Neo4j database.
        database (Optional[str]): The name of the database to connect to. Defaults to "neo4j".
        timeout (Optional[float]): The timeout for transactions in seconds.
        Useful for terminating long-running queries.
        By default, there is no timeout set.
        apoc_sample (Optional[int]): The number of nodes/rels to sample when calling
        apoc.meta.data(). Useful for large databases where schema introspection
        is slow. When None (default), no sampling config is passed.

    Examples:
        `pip install llama-index-graph-stores-neo4j`

        ```python
        from llama_index.core.indices.property_graph import PropertyGraphIndex
        from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

        # Create a Neo4jPropertyGraphStore instance
        graph_store = Neo4jPropertyGraphStore(
            username="neo4j",
            password="neo4j",
            url="bolt://localhost:7687",
            database="neo4j"


        # create the index
        index = PropertyGraphIndex.from_documents(
            documents,
            property_graph_store=graph_store,


        # Close the neo4j connection explicitly.
        graph_store.close()
        ```

    """

    supports_structured_queries: bool = True
    supports_vector_queries: bool = True
    text_to_cypher_template: PromptTemplate = DEFAULT_CYPHER_TEMPALTE

    def__init__(
        self,
        username: str,
        password: str,
        url: str,
        database: Optional[str] = "neo4j",
        refresh_schema: bool = True,
        sanitize_query_output: bool = True,
        enhanced_schema: bool = False,
        create_indexes: bool = True,
        timeout: Optional[float] = None,
        user_agent: str = "LLAMAINDEX-PROPERTYGRAPH",
        apoc_sample: Optional[int] = None,
        **neo4j_kwargs: Any,
    ) -> None:
        self.sanitize_query_output = sanitize_query_output
        self.enhanced_schema = enhanced_schema
        self._apoc_meta_config = (
            {"sample": apoc_sample} if apoc_sample is not None else {}
        )
        self._driver = neo4j.GraphDatabase.driver(
            url,
            auth=(username, password),
            notifications_min_severity="OFF",
            user_agent=user_agent,
            **neo4j_kwargs,
        )
        self._async_driver = neo4j.AsyncGraphDatabase.driver(
            url,
            auth=(username, password),
            notifications_min_severity="OFF",
            user_agent=user_agent,
            **neo4j_kwargs,
        )
        self._database = database
        self._timeout = timeout
        self.structured_schema = {}
        if refresh_schema:
            self.refresh_schema()
        # Verify version to check if we can use vector index
        self.verify_version()
        # Create index for faster imports and retrieval
        if create_indexes:
            self.structured_query(
                f"""CREATE CONSTRAINT IF NOT EXISTS FOR (n:`{BASE_NODE_LABEL}`)
                REQUIRE n.id IS UNIQUE;"""
            )
            self.structured_query(
                f"""CREATE CONSTRAINT IF NOT EXISTS FOR (n:`{BASE_ENTITY_LABEL}`)
                REQUIRE n.id IS UNIQUE;"""
            )

            if self._supports_vector_index:
                self.structured_query(
                    f"CREATE VECTOR INDEX {VECTOR_INDEX_NAME} IF NOT EXISTS "
                    "FOR (m:__Entity__) ON m.embedding"
                )

    @property
    defclient(self):
        return self._driver

    defclose(self) -> None:
        self._driver.close()

    defrefresh_schema(self) -> None:
"""Refresh the schema."""
        node_query_results = self.structured_query(
            node_properties_query,
            param_map={
                "EXCLUDED_LABELS": [
                    *EXCLUDED_LABELS,
                    BASE_ENTITY_LABEL,
                    BASE_NODE_LABEL,
                ],
                "config": self._apoc_meta_config,
            },
        )
        node_properties = (
            [el["output"] for el in node_query_results] if node_query_results else []
        )

        rels_query_result = self.structured_query(
            rel_properties_query,
            param_map={
                "EXCLUDED_LABELS": EXCLUDED_RELS,
                "config": self._apoc_meta_config,
            },
        )
        rel_properties = (
            [el["output"] for el in rels_query_result] if rels_query_result else []
        )

        rel_objs_query_result = self.structured_query(
            rel_query,
            param_map={
                "EXCLUDED_LABELS": [
                    *EXCLUDED_LABELS,
                    BASE_ENTITY_LABEL,
                    BASE_NODE_LABEL,
                ],
                "config": self._apoc_meta_config,
            },
        )
        relationships = (
            [el["output"] for el in rel_objs_query_result]
            if rel_objs_query_result
            else []
        )

        # Get constraints & indexes
        try:
            constraint = self.structured_query("SHOW CONSTRAINTS")
            index = self.structured_query(
                "CALL apoc.schema.nodes() YIELD label, properties, type, size, "
                "valuesSelectivity WHERE type = 'RANGE' RETURN *, "
                "size * valuesSelectivity as distinctValues"
            )
        except (
            neo4j.exceptions.ClientError
        ):  # Read-only user might not have access to schema information
            constraint = []
            index = []

        self.structured_schema = {
            "node_props": {el["labels"]: el["properties"] for el in node_properties},
            "rel_props": {el["type"]: el["properties"] for el in rel_properties},
            "relationships": relationships,
            "metadata": {"constraint": constraint, "index": index},
        }
        schema_counts = self.structured_query(
            "CALL apoc.meta.subGraph({}) YIELD nodes, relationships "
            "RETURN nodes, [rel in relationships | {name:apoc.any.property"
            "(rel, 'type'), count: apoc.any.property(rel, 'count')}]"
            " AS relationships"
        )
        # Update node info
        for node in schema_counts[0].get("nodes", []):
            # Skip bloom labels
            if node["name"] in EXCLUDED_LABELS:
                continue
            node_props = self.structured_schema["node_props"].get(node["name"])
            if not node_props:  # The node has no properties
                continue
            enhanced_cypher = self._enhanced_schema_cypher(
                node["name"], node_props, node["count"]  EXHAUSTIVE_SEARCH_LIMIT
            )
            enhanced_info = self.structured_query(enhanced_cypher)[0]["output"]
            for prop in node_props:
                # Map to custom types
                # Text
                if prop["type"] == "STRING" and any(
                    len(value) >= LONG_TEXT_THRESHOLD
                    for value in enhanced_info[prop["property"]]["values"]
                ):
                    enhanced_info[prop["property"]]["type"] = "TEXT"
                # Embedding
                if (
                    prop["type"] == "LIST"
                    and enhanced_info[prop["property"]]["max_size"]  LIST_LIMIT
                ):
                    enhanced_info[prop["property"]]["type"] = "EMBEDDING"
                if prop["property"] in enhanced_info:
                    prop.update(enhanced_info[prop["property"]])
        # Update rel info
        for rel in schema_counts[0].get("relationships", []):
            # Skip bloom labels
            if rel["name"] in EXCLUDED_RELS:
                continue
            rel_props = self.structured_schema["rel_props"].get(rel["name"])
            if not rel_props:  # The rel has no properties
                continue
            enhanced_cypher = self._enhanced_schema_cypher(
                rel["name"],
                rel_props,
                rel["count"]  EXHAUSTIVE_SEARCH_LIMIT,
                is_relationship=True,
            )
            try:
                enhanced_info = self.structured_query(enhanced_cypher)[0]["output"]
                for prop in rel_props:
                    if prop["property"] in enhanced_info:
                        prop.update(enhanced_info[prop["property"]])
            except neo4j.exceptions.ClientError:
                # Sometimes the types are not consistent in the db
                pass

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
            for index in range(0, len(chunk_dicts), CHUNK_SIZE):
                chunked_params = chunk_dicts[index : index + CHUNK_SIZE]
                self.structured_query(
                    f"""
                    UNWIND $data AS row
                    MERGE (c:{BASE_NODE_LABEL}{{id: row.id}})
                    SET c.text = row.text, c:Chunk
                    WITH c, row
                    SET c += row.properties
                    WITH c, row.embedding AS embedding
                    WHERE embedding IS NOT NULL
                    CALL db.create.setNodeVectorProperty(c, 'embedding', embedding)
                    RETURN count(*)
,
                    param_map={"data": chunked_params},
                )

        if entity_dicts:
            for index in range(0, len(entity_dicts), CHUNK_SIZE):
                chunked_params = entity_dicts[index : index + CHUNK_SIZE]
                self.structured_query(
                    f"""
                    UNWIND $data AS row
                    MERGE (e:{BASE_NODE_LABEL}{{id: row.id}})
                    SET e += apoc.map.clean(row.properties, [], [])
                    SET e.name = row.name, e:`{BASE_ENTITY_LABEL}`
                    WITH e, row
                    CALL apoc.create.addLabels(e, [row.label])
                    YIELD node
                    WITH e, row
                    CALL (e, row) {{
                        WITH e, row
                        WHERE row.embedding IS NOT NULL
                        CALL db.create.setNodeVectorProperty(e, 'embedding', row.embedding)
                        RETURN count(*) AS count
}}
                    WITH e, row WHERE row.properties.triplet_source_id IS NOT NULL
                    MERGE (c:{BASE_NODE_LABEL}{{id: row.properties.triplet_source_id}})
                    MERGE (e)<-[:MENTIONS]-(c)
,
                    param_map={"data": chunked_params},
                )

    defupsert_relations(self, relations: List[Relation]) -> None:
"""Add relations."""
        params = [r.dict() for r in relations]
        for index in range(0, len(params), CHUNK_SIZE):
            chunked_params = params[index : index + CHUNK_SIZE]

            self.structured_query(
                f"""
                UNWIND $data AS row
                MERGE (source: {BASE_NODE_LABEL}{{id: row.source_id}})
                ON CREATE SET source:Chunk
                MERGE (target: {BASE_NODE_LABEL}{{id: row.target_id}})
                ON CREATE SET target:Chunk
                WITH source, target, row
                CALL apoc.merge.relationship(source, row.label, {{}}, row.properties, target) YIELD rel
                RETURN count(*)
,
                param_map={"data": chunked_params},
            )

    defget(
        self,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[LabelledNode]:
"""Get nodes."""
        cypher_statement = f"MATCH (e: {BASE_NODE_LABEL}) "

        params = {}
        cypher_statement += "WHERE e.id IS NOT NULL "

        if ids:
            cypher_statement += "AND e.id in $ids "
            params["ids"] = ids

        if properties:
            prop_list = []
            for i, prop in enumerate(properties):
                prop_list.append(f"e.`{prop}` = $property_{i}")
                params[f"property_{i}"] = properties[prop]
            cypher_statement += " AND " + " AND ".join(prop_list)

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
        cypher_statement = f"MATCH (e:`{BASE_ENTITY_LABEL}`) "

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
        CALL (e) {{
            WITH e
            MATCH (e)-[r{":`"+"`|`".join(relation_names)+"`"ifrelation_nameselse""}]->(t:`{BASE_ENTITY_LABEL}`)
            RETURN e.name AS source_id, [l in labels(e) WHERE NOT l IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}'] | l][0] AS source_type,
{{.* , embedding: Null, name: Null}} AS source_properties,
                   type(r) AS type,
{{.*}} AS rel_properties,
                   t.name AS target_id, [l in labels(t) WHERE NOT l IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}'] | l][0] AS target_type,
{{.* , embedding: Null, name: Null}} AS target_properties
            UNION ALL
            WITH e
            MATCH (e)<-[r{":`"+"`|`".join(relation_names)+"`"ifrelation_nameselse""}]-(t:`{BASE_ENTITY_LABEL}`)
            RETURN t.name AS source_id, [l in labels(t) WHERE NOT l IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}'] | l][0] AS source_type,
{{.* , embedding: Null, name: Null}} AS source_properties,
                   type(r) AS type,
{{.*}} AS rel_properties,
                   e.name AS target_id, [l in labels(e) WHERE NOT l IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}'] | l][0] AS target_type,
{{.* , embedding: Null, name: Null}} AS target_properties
}}
        RETURN source_id, source_type, type, rel_properties, target_id, target_type, source_properties, target_properties"""
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
                properties=remove_empty_values(record["rel_properties"]),
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
            MATCH (e:`{BASE_ENTITY_LABEL}`)
            WHERE e.id = id_list[idx]
            MATCH p=(e)-[r*1..{depth}]-(other)
            WHERE ALL(rel in relationships(p) WHERE type(rel) <> 'MENTIONS')
            UNWIND relationships(p) AS rel
            WITH distinct rel, idx
            WITH startNode(rel) AS source,
                type(rel) AS type,
{{.*}} AS rel_properties,
                endNode(rel) AS endNode,

            LIMIT toInteger($limit)
            RETURN source.id AS source_id, [l in labels(source)
                   WHERE NOT l IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}'] | l][0] AS source_type,
                source{{.* , embedding: Null, id: Null}} AS source_properties,
                type,
                rel_properties,
                endNode.id AS target_id, [l in labels(endNode)
                   WHERE NOT l IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}'] | l][0] AS target_type,
                endNode{{.* , embedding: Null, id: Null}} AS target_properties,

            ORDER BY idx
            LIMIT toInteger($limit)
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
                properties=remove_empty_values(record["rel_properties"]),
            )
            triples.append([source, rel, target])

        return triples

    defstructured_query(
        self,
        query: str,
        param_map: Optional[Dict[str, Any]] = None,
    ) -> Any:
        param_map = param_map or {}
        try:
            data, _, _ = self._driver.execute_query(
                neo4j.Query(text=query, timeout=self._timeout),
                database_=self._database,
                parameters_=param_map,
            )
            full_result = [d.data() for d in data]

            if self.sanitize_query_output:
                return [value_sanitize(el) for el in full_result]
            return full_result
        except neo4j.exceptions.Neo4jError as e:
            if not (
                (
                    (  # isCallInTransactionError
                        e.code == "Neo.DatabaseError.Statement.ExecutionFailed"
                        or e.code
                        == "Neo.DatabaseError.Transaction.TransactionStartFailed"
                    )
                    and "in an implicit transaction" in e.message
                )
                or (  # isPeriodicCommitError
                    e.code == "Neo.ClientError.Statement.SemanticError"
                    and (
                        "in an open transaction is not possible" in e.message
                        or "tried to execute in an explicit transaction" in e.message
                    )
                )
            ):
                raise
        # Fallback to allow implicit transactions
        with self._driver.session(database=self._database) as session:
            data = session.run(
                neo4j.Query(text=query, timeout=self._timeout), param_map
            )
            full_result = [d.data() for d in data]

            if self.sanitize_query_output:
                return [value_sanitize(el) for el in full_result]
            return full_result

    defvector_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> Tuple[List[LabelledNode], List[float]]:
"""Query the graph store with a vector store query."""
        conditions = []
        filter_params = {}
        if query.filters:
            for index, filter in enumerate(query.filters.filters):
                conditions.append(
                    f"{'NOT'iffilter.operator.valuein['nin']else''} e.`{filter.key}` "
                    f"{convert_operator(filter.operator.value)} $param_{index}"
                )
                filter_params[f"param_{index}"] = filter.value
        filters = (
            f" {query.filters.condition.value} ".join(conditions)
            if conditions
            else "1 = 1"
        )
        if not query.filters and self._supports_vector_index:
            data = self.structured_query(
                f"""CALL db.index.vector.queryNodes('{VECTOR_INDEX_NAME}', $limit, $embedding)
                YIELD node, score RETURN node.id AS name,
                [l in labels(node) WHERE NOT l IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}'] | l][0] AS type,
                node{{.* , embedding: Null, name: Null, id: Null}} AS properties,
                score
,
                param_map={
                    "embedding": query.query_embedding,
                    "limit": query.similarity_top_k,
                },
            )
        else:
            data = self.structured_query(
                f"""MATCH (e:`{BASE_ENTITY_LABEL}`)
                WHERE e.embedding IS NOT NULL AND size(e.embedding) = $dimension AND ({filters})
                WITH e, vector.similarity.cosine(e.embedding, $embedding) AS score
                ORDER BY score DESC LIMIT toInteger($limit)
                RETURN e.id AS name,
                [l in labels(e) WHERE NOT l IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}'] | l][0] AS type,
{{.* , embedding: Null, name: Null, id: Null}} AS properties,
                score""",
                param_map={
                    "embedding": query.query_embedding,
                    "dimension": len(query.query_embedding),
                    "limit": query.similarity_top_k,
                    **filter_params,
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

    def_enhanced_schema_cypher(
        self,
        label_or_type: str,
        properties: List[Dict[str, Any]],
        exhaustive: bool,
        is_relationship: bool = False,
    ) -> str:
        if is_relationship:
            match_clause = f"MATCH ()-[n:`{label_or_type}`]->()"
        else:
            match_clause = f"MATCH (n:`{label_or_type}`)"

        with_clauses = []
        return_clauses = []
        output_dict = {}
        if exhaustive:
            for prop in properties:
                prop_name = prop["property"]
                prop_type = prop["type"]
                if prop_type == "STRING":
                    with_clauses.append(
                        f"collect(distinct substring(toString(coalesce(n.`{prop_name}`, '')), 0, {LONG_TEXT_THRESHOLD})) "
                        f"AS `{prop_name}_values`"
                    )
                    return_clauses.append(
                        f"values:`{prop_name}_values`[..{DISTINCT_VALUE_LIMIT}],"
                        f" distinct_count: size(`{prop_name}_values`)"
                    )
                elif prop_type in [
                    "INTEGER",
                    "FLOAT",
                    "DATE",
                    "DATE_TIME",
                    "LOCAL_DATE_TIME",
                ]:
                    with_clauses.append(f"min(n.`{prop_name}`) AS `{prop_name}_min`")
                    with_clauses.append(f"max(n.`{prop_name}`) AS `{prop_name}_max`")
                    with_clauses.append(
                        f"count(distinct n.`{prop_name}`) AS `{prop_name}_distinct`"
                    )
                    return_clauses.append(
                        f"min: toString(`{prop_name}_min`), "
                        f"max: toString(`{prop_name}_max`), "
                        f"distinct_count: `{prop_name}_distinct`"
                    )
                elif prop_type == "LIST":
                    with_clauses.append(
                        f"min(size(coalesce(n.`{prop_name}`, []))) AS `{prop_name}_size_min`, "
                        f"max(size(coalesce(n.`{prop_name}`, []))) AS `{prop_name}_size_max`, "
                        # Get first 3 sub-elements of the first element as sample values
                        f"collect(n.`{prop_name}`)[0][..3] AS `{prop_name}_values`"
                    )
                    return_clauses.append(
                        f"min_size: `{prop_name}_size_min`, "
                        f"max_size: `{prop_name}_size_max`, "
                        f"values:`{prop_name}_values`"
                    )
                elif prop_type in ["BOOLEAN", "POINT", "DURATION"]:
                    continue
                output_dict[prop_name] = "{" + return_clauses.pop() + "}"
        else:
            # Just sample 5 random nodes
            match_clause += " WITH n LIMIT 5"
            for prop in properties:
                prop_name = prop["property"]
                prop_type = prop["type"]

                # Check if indexed property, we can still do exhaustive
                prop_index = [
                    el
                    for el in self.structured_schema["metadata"]["index"]
                    if el["label"] == label_or_type
                    and el["properties"] == [prop_name]
                    and el["type"] == "RANGE"
                ]
                if prop_type == "STRING":
                    if (
                        prop_index
                        and prop_index[0].get("size")  0
                        and prop_index[0].get("distinctValues") <= DISTINCT_VALUE_LIMIT
                    ):
                        distinct_values = self.query(
                            f"CALL apoc.schema.properties.distinct("
                            f"'{label_or_type}', '{prop_name}') YIELD value"
                        )[0]["value"]
                        return_clauses.append(
                            f"values: {distinct_values},"
                            f" distinct_count: {len(distinct_values)}"
                        )
                    else:
                        with_clauses.append(
                            f"collect(distinct substring(toString(n.`{prop_name}`), 0, {LONG_TEXT_THRESHOLD})) "
                            f"AS `{prop_name}_values`"
                        )
                        return_clauses.append(f"values: `{prop_name}_values`")
                elif prop_type in [
                    "INTEGER",
                    "FLOAT",
                    "DATE",
                    "DATE_TIME",
                    "LOCAL_DATE_TIME",
                ]:
                    if not prop_index:
                        with_clauses.append(
                            f"collect(distinct toString(coalesce(n.`{prop_name}`, ''))) "
                            f"AS `{prop_name}_values`"
                        )
                        return_clauses.append(f"values: `{prop_name}_values`")
                    else:
                        with_clauses.append(
                            f"min(n.`{prop_name}`) AS `{prop_name}_min`"
                        )
                        with_clauses.append(
                            f"max(n.`{prop_name}`) AS `{prop_name}_max`"
                        )
                        with_clauses.append(
                            f"count(distinct n.`{prop_name}`) AS `{prop_name}_distinct`"
                        )
                        return_clauses.append(
                            f"min: toString(`{prop_name}_min`), "
                            f"max: toString(`{prop_name}_max`), "
                            f"distinct_count: `{prop_name}_distinct`"
                        )

                elif prop_type == "LIST":
                    with_clauses.append(
                        f"min(size(coalesce(n.`{prop_name}`, []))) AS `{prop_name}_size_min`, "
                        f"max(size(coalesce(n.`{prop_name}`, []))) AS `{prop_name}_size_max`, "
                        # Get first 3 sub-elements of the first element as sample values
                        f"collect(n.`{prop_name}`)[0][..3] AS `{prop_name}_values`"
                    )
                    return_clauses.append(
                        f"min_size: `{prop_name}_size_min`, "
                        f"max_size: `{prop_name}_size_max`, "
                        f"values:`{prop_name}_values`"
                    )
                elif prop_type in ["BOOLEAN", "POINT", "DURATION"]:
                    continue

                output_dict[prop_name] = "{" + return_clauses.pop() + "}"

        with_clause = "WITH " + ",\n.join(with_clauses)
        return_clause = (
            "RETURN {"
            + ", ".join(f"`{k}`: {v}" for k, v in output_dict.items())
            + "} AS output"
        )

        # Combine all parts of the Cypher query
        return f"{match_clause}\n{with_clause}\n{return_clause}"

    defget_schema(self, refresh: bool = False) -> Any:
        if refresh:
            self.refresh_schema()

        return self.structured_schema

    defget_schema_str(
        self,
        refresh: bool = False,
        exclude_types: List[str] = [],
        include_types: List[str] = [],
    ) -> str:
        schema = self.get_schema(refresh=refresh)

        deffilter_func(x: str) -> bool:
            return x in include_types if include_types else x not in exclude_types

        filtered_schema: Dict[str, Any] = {
            "node_props": {
                k: v for k, v in schema.get("node_props", {}).items() if filter_func(k)
            },
            "rel_props": {
                k: v for k, v in schema.get("rel_props", {}).items() if filter_func(k)
            },
            "relationships": [
                r
                for r in schema.get("relationships", [])
                if all(filter_func(r[t]) for t in ["start", "end", "type"])
            ],
        }

        formatted_node_props = []
        formatted_rel_props = []

        if self.enhanced_schema:
            # Enhanced formatting for nodes
            for node_type, properties in filtered_schema["node_props"].items():
                formatted_node_props.append(f"- **{node_type}**")
                for prop in properties:
                    example = ""
                    if prop["type"] == "STRING" and prop.get("values"):
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
                    elif prop["type"] == "TEXT":
                        example = (
                            f'Example: "{clean_string_values(prop["values"][0])}"'
                            if prop["values"]
                            else ""
                        )
                    elif prop["type"] in [
                        "INTEGER",
                        "FLOAT",
                        "DATE",
                        "DATE_TIME",
                        "LOCAL_DATE_TIME",
                    ]:
                        if prop.get("min") is not None:
                            example = f"Min: {prop['min']}, Max: {prop['max']}"
                        else:
                            example = (
                                f'Example: "{prop["values"][0]}"'
                                if prop.get("values")
                                else ""
                            )
                    elif prop["type"] == "LIST":
                        # Skip embeddings
                        # if not prop.get("min_size") or prop["min_size"] > LIST_LIMIT:
                        #    continue
                        example = (
                            f"Min Size: {prop.get('min_size','N/A')}, "
                            f"Max Size: {prop.get('max_size','N/A')}, "
                            + (
                                f"Example: [{prop['values'][0]}]"
                                if prop.get("values") and len(prop["values"])  0
                                else ""
                            )
                        )
                    formatted_node_props.append(
                        f"  - `{prop['property']}`: {prop['type']}{example}"
                    )

            # Enhanced formatting for relationships
            for rel_type, properties in filtered_schema["rel_props"].items():
                formatted_rel_props.append(f"- **{rel_type}**")
                for prop in properties:
                    example = ""
                    if prop["type"] == "STRING":
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
                        "INTEGER",
                        "FLOAT",
                        "DATE",
                        "DATE_TIME",
                        "LOCAL_DATE_TIME",
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
            for label, props in filtered_schema["node_props"].items():
                props_str = ", ".join(
                    [f"{prop['property']}: {prop['type']}" for prop in props]
                )
                formatted_node_props.append(f"{label}{{{props_str}}}")

            # Format relationship properties using structured_schema
            for type, props in filtered_schema["rel_props"].items():
                props_str = ", ".join(
                    [f"{prop['property']}: {prop['type']}" for prop in props]
                )
                formatted_rel_props.append(f"{type}{{{props_str}}}")

        # Format relationships
        formatted_rels = [
            f"(:{el['start']})-[:{el['type']}]->(:{el['end']})"
            for el in filtered_schema["relationships"]
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

    defverify_version(self) -> None:
"""
        Check if the connected Neo4j database version supports vector indexing
        without specifying embedding dimension.

        Queries the Neo4j database to retrieve its version and compares it
        against a target version (5.23.0) that is known to support vector
        indexing. Raises a ValueError if the connected Neo4j version is
        not supported.
        """
        db_data = self.structured_query("CALL dbms.components()")
        version = db_data[0]["versions"][0]
        if "aura" in version:
            version_tuple = (*map(int, version.split("-")[0].split(".")), 0)
        else:
            version_tuple = tuple(map(int, version.split(".")))

        target_version = (5, 23, 0)

        if version_tuple >= target_version:
            self._supports_vector_index = True
        else:
            self._supports_vector_index = False

    defclose(self) -> None:
"""
        Explicitly close the Neo4j driver connection.

        Delegates connection management to the Neo4j driver.
        """
        if hasattr(self, "_driver"):
            self._driver.close()
            # Remove the driver attribute to indicate closure
            delattr(self, "_driver")

    def__enter__(self) -> "Neo4jPropertyGraphStore":
"""
        Enter the runtime context for the Neo4j graph connection.

        Enables use of the graph connection with the 'with' statement.
        This method allows for automatic resource management and ensures
        that the connection is properly handled.

        Returns:
            Neo4jPropertyGraphStore: The current graph connection instance

        """
        return self

    def__exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
"""
        Exit the runtime context for the Neo4j graph connection.

        This method is automatically called when exiting a 'with' statement.
        It ensures that the database connection is closed, regardless of
        whether an exception occurred during the context's execution.

        Args:
            exc_type: The type of exception that caused the context to exit
                      (None if no exception occurred)
            exc_val: The exception instance that caused the context to exit
                     (None if no exception occurred)
            exc_tb: The traceback for the exception (None if no exception occurred)

        Note:
            Any exception is re-raised after the connection is closed.

        """
        self.close()

    def__del__(self) -> None:
"""
        Destructor for the Neo4j graph connection.

        This method is called during garbage collection to ensure that
        database resources are released if not explicitly closed.

        Caution:
            - Do not rely on this method for deterministic resource cleanup
            - Always prefer explicit .close() or context manager

        Best practices:
            1. Use context manager:
               with Neo4jGraph(...) as graph:

            2. Explicitly close:
               graph = Neo4jGraph(...)
               try:

               finally:
                   graph.close()

        """
        try:
            self.close()
        except Exception:
            # Suppress any exceptions during garbage collection
            pass

```
 |  
| --- | --- |  
###  close [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jPropertyGraphStore.close "Permanent link")

```
close() -> None

```

Explicitly close the Neo4j driver connection.
Delegates connection management to the Neo4j driver.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/neo4j_property_graph.py`  
| 
```
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
```
 | 
```
defclose(self) -> None:
"""
    Explicitly close the Neo4j driver connection.

    Delegates connection management to the Neo4j driver.
    """
    if hasattr(self, "_driver"):
        self._driver.close()
        # Remove the driver attribute to indicate closure
        delattr(self, "_driver")

```
 |  
| --- | --- |  
###  refresh_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jPropertyGraphStore.refresh_schema "Permanent link")

```
refresh_schema() -> None

```

Refresh the schema.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/neo4j_property_graph.py`  
| 
```
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
```
 | 
```
defrefresh_schema(self) -> None:
"""Refresh the schema."""
    node_query_results = self.structured_query(
        node_properties_query,
        param_map={
            "EXCLUDED_LABELS": [
                *EXCLUDED_LABELS,
                BASE_ENTITY_LABEL,
                BASE_NODE_LABEL,
            ],
            "config": self._apoc_meta_config,
        },
    )
    node_properties = (
        [el["output"] for el in node_query_results] if node_query_results else []
    )

    rels_query_result = self.structured_query(
        rel_properties_query,
        param_map={
            "EXCLUDED_LABELS": EXCLUDED_RELS,
            "config": self._apoc_meta_config,
        },
    )
    rel_properties = (
        [el["output"] for el in rels_query_result] if rels_query_result else []
    )

    rel_objs_query_result = self.structured_query(
        rel_query,
        param_map={
            "EXCLUDED_LABELS": [
                *EXCLUDED_LABELS,
                BASE_ENTITY_LABEL,
                BASE_NODE_LABEL,
            ],
            "config": self._apoc_meta_config,
        },
    )
    relationships = (
        [el["output"] for el in rel_objs_query_result]
        if rel_objs_query_result
        else []
    )

    # Get constraints & indexes
    try:
        constraint = self.structured_query("SHOW CONSTRAINTS")
        index = self.structured_query(
            "CALL apoc.schema.nodes() YIELD label, properties, type, size, "
            "valuesSelectivity WHERE type = 'RANGE' RETURN *, "
            "size * valuesSelectivity as distinctValues"
        )
    except (
        neo4j.exceptions.ClientError
    ):  # Read-only user might not have access to schema information
        constraint = []
        index = []

    self.structured_schema = {
        "node_props": {el["labels"]: el["properties"] for el in node_properties},
        "rel_props": {el["type"]: el["properties"] for el in rel_properties},
        "relationships": relationships,
        "metadata": {"constraint": constraint, "index": index},
    }
    schema_counts = self.structured_query(
        "CALL apoc.meta.subGraph({}) YIELD nodes, relationships "
        "RETURN nodes, [rel in relationships | {name:apoc.any.property"
        "(rel, 'type'), count: apoc.any.property(rel, 'count')}]"
        " AS relationships"
    )
    # Update node info
    for node in schema_counts[0].get("nodes", []):
        # Skip bloom labels
        if node["name"] in EXCLUDED_LABELS:
            continue
        node_props = self.structured_schema["node_props"].get(node["name"])
        if not node_props:  # The node has no properties
            continue
        enhanced_cypher = self._enhanced_schema_cypher(
            node["name"], node_props, node["count"]  EXHAUSTIVE_SEARCH_LIMIT
        )
        enhanced_info = self.structured_query(enhanced_cypher)[0]["output"]
        for prop in node_props:
            # Map to custom types
            # Text
            if prop["type"] == "STRING" and any(
                len(value) >= LONG_TEXT_THRESHOLD
                for value in enhanced_info[prop["property"]]["values"]
            ):
                enhanced_info[prop["property"]]["type"] = "TEXT"
            # Embedding
            if (
                prop["type"] == "LIST"
                and enhanced_info[prop["property"]]["max_size"]  LIST_LIMIT
            ):
                enhanced_info[prop["property"]]["type"] = "EMBEDDING"
            if prop["property"] in enhanced_info:
                prop.update(enhanced_info[prop["property"]])
    # Update rel info
    for rel in schema_counts[0].get("relationships", []):
        # Skip bloom labels
        if rel["name"] in EXCLUDED_RELS:
            continue
        rel_props = self.structured_schema["rel_props"].get(rel["name"])
        if not rel_props:  # The rel has no properties
            continue
        enhanced_cypher = self._enhanced_schema_cypher(
            rel["name"],
            rel_props,
            rel["count"]  EXHAUSTIVE_SEARCH_LIMIT,
            is_relationship=True,
        )
        try:
            enhanced_info = self.structured_query(enhanced_cypher)[0]["output"]
            for prop in rel_props:
                if prop["property"] in enhanced_info:
                    prop.update(enhanced_info[prop["property"]])
        except neo4j.exceptions.ClientError:
            # Sometimes the types are not consistent in the db
            pass

```
 |  
| --- | --- |  
###  upsert_relations [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jPropertyGraphStore.upsert_relations "Permanent link")

```
upsert_relations(relations: []) -> None

```

Add relations.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/neo4j_property_graph.py`  
| 
```
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
```
 | 
```
defupsert_relations(self, relations: List[Relation]) -> None:
"""Add relations."""
    params = [r.dict() for r in relations]
    for index in range(0, len(params), CHUNK_SIZE):
        chunked_params = params[index : index + CHUNK_SIZE]

        self.structured_query(
            f"""
            UNWIND $data AS row
            MERGE (source: {BASE_NODE_LABEL}{{id: row.source_id}})
            ON CREATE SET source:Chunk
            MERGE (target: {BASE_NODE_LABEL}{{id: row.target_id}})
            ON CREATE SET target:Chunk
            WITH source, target, row
            CALL apoc.merge.relationship(source, row.label, {{}}, row.properties, target) YIELD rel
            RETURN count(*)
,
            param_map={"data": chunked_params},
        )

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jPropertyGraphStore.get "Permanent link")

```
get(
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> []

```

Get nodes.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/neo4j_property_graph.py`  
| 
```
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
```
 | 
```
defget(
    self,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> List[LabelledNode]:
"""Get nodes."""
    cypher_statement = f"MATCH (e: {BASE_NODE_LABEL}) "

    params = {}
    cypher_statement += "WHERE e.id IS NOT NULL "

    if ids:
        cypher_statement += "AND e.id in $ids "
        params["ids"] = ids

    if properties:
        prop_list = []
        for i, prop in enumerate(properties):
            prop_list.append(f"e.`{prop}` = $property_{i}")
            params[f"property_{i}"] = properties[prop]
        cypher_statement += " AND " + " AND ".join(prop_list)

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
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jPropertyGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    graph_nodes: [],
    depth:  = 2,
    limit:  = 30,
    ignore_rels: Optional[[]] = None,
) -> [Triplet]

```

Get depth-aware rel map.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/neo4j_property_graph.py`  
| 
```
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
        MATCH (e:`{BASE_ENTITY_LABEL}`)
        WHERE e.id = id_list[idx]
        MATCH p=(e)-[r*1..{depth}]-(other)
        WHERE ALL(rel in relationships(p) WHERE type(rel) <> 'MENTIONS')
        UNWIND relationships(p) AS rel
        WITH distinct rel, idx
        WITH startNode(rel) AS source,
            type(rel) AS type,
{{.*}} AS rel_properties,
            endNode(rel) AS endNode,

        LIMIT toInteger($limit)
        RETURN source.id AS source_id, [l in labels(source)
               WHERE NOT l IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}'] | l][0] AS source_type,
            source{{.* , embedding: Null, id: Null}} AS source_properties,
            type,
            rel_properties,
            endNode.id AS target_id, [l in labels(endNode)
               WHERE NOT l IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}'] | l][0] AS target_type,
            endNode{{.* , embedding: Null, id: Null}} AS target_properties,

        ORDER BY idx
        LIMIT toInteger($limit)
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
            properties=remove_empty_values(record["rel_properties"]),
        )
        triples.append([source, rel, target])

    return triples

```
 |  
| --- | --- |  
###  vector_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jPropertyGraphStore.vector_query "Permanent link")

```
vector_query(
    query: , **kwargs: 
) -> Tuple[[], [float]]

```

Query the graph store with a vector store query.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/neo4j_property_graph.py`  
| 
```
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
```
 | 
```
defvector_query(
    self, query: VectorStoreQuery, **kwargs: Any
) -> Tuple[List[LabelledNode], List[float]]:
"""Query the graph store with a vector store query."""
    conditions = []
    filter_params = {}
    if query.filters:
        for index, filter in enumerate(query.filters.filters):
            conditions.append(
                f"{'NOT'iffilter.operator.valuein['nin']else''} e.`{filter.key}` "
                f"{convert_operator(filter.operator.value)} $param_{index}"
            )
            filter_params[f"param_{index}"] = filter.value
    filters = (
        f" {query.filters.condition.value} ".join(conditions)
        if conditions
        else "1 = 1"
    )
    if not query.filters and self._supports_vector_index:
        data = self.structured_query(
            f"""CALL db.index.vector.queryNodes('{VECTOR_INDEX_NAME}', $limit, $embedding)
            YIELD node, score RETURN node.id AS name,
            [l in labels(node) WHERE NOT l IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}'] | l][0] AS type,
            node{{.* , embedding: Null, name: Null, id: Null}} AS properties,
            score
,
            param_map={
                "embedding": query.query_embedding,
                "limit": query.similarity_top_k,
            },
        )
    else:
        data = self.structured_query(
            f"""MATCH (e:`{BASE_ENTITY_LABEL}`)
            WHERE e.embedding IS NOT NULL AND size(e.embedding) = $dimension AND ({filters})
            WITH e, vector.similarity.cosine(e.embedding, $embedding) AS score
            ORDER BY score DESC LIMIT toInteger($limit)
            RETURN e.id AS name,
            [l in labels(e) WHERE NOT l IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}'] | l][0] AS type,
{{.* , embedding: Null, name: Null, id: Null}} AS properties,
            score""",
            param_map={
                "embedding": query.query_embedding,
                "dimension": len(query.query_embedding),
                "limit": query.similarity_top_k,
                **filter_params,
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
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jPropertyGraphStore.delete "Permanent link")

```
delete(
    entity_names: Optional[[]] = None,
    relation_names: Optional[[]] = None,
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> None

```

Delete matching data.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/neo4j_property_graph.py`  
| 
```
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
###  verify_version [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neo4j/#llama_index.graph_stores.neo4j.Neo4jPropertyGraphStore.verify_version "Permanent link")

```
verify_version() -> None

```

Check if the connected Neo4j database version supports vector indexing without specifying embedding dimension.
Queries the Neo4j database to retrieve its version and compares it against a target version (5.23.0) that is known to support vector indexing. Raises a ValueError if the connected Neo4j version is not supported.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/llama_index/graph_stores/neo4j/neo4j_property_graph.py`  
| 
```
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
```
 | 
```
defverify_version(self) -> None:
"""
    Check if the connected Neo4j database version supports vector indexing
    without specifying embedding dimension.

    Queries the Neo4j database to retrieve its version and compares it
    against a target version (5.23.0) that is known to support vector
    indexing. Raises a ValueError if the connected Neo4j version is
    not supported.
    """
    db_data = self.structured_query("CALL dbms.components()")
    version = db_data[0]["versions"][0]
    if "aura" in version:
        version_tuple = (*map(int, version.split("-")[0].split(".")), 0)
    else:
        version_tuple = tuple(map(int, version.split(".")))

    target_version = (5, 23, 0)

    if version_tuple >= target_version:
        self._supports_vector_index = True
    else:
        self._supports_vector_index = False

```
 |  
| --- | --- |  
options: members: - Neo4jGraphStore - Neo4jPropertyGraphStore
