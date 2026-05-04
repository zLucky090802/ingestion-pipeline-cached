# Neptune
##  NeptuneAnalyticsGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneAnalyticsGraphStore "Permanent link")
Bases: `NeptuneBaseGraphStore`
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/analytics.py`  
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
```
 | 
```
classNeptuneAnalyticsGraphStore(NeptuneBaseGraphStore):
    def__init__(
        self,
        graph_identifier: str,
        client: Any = None,
        credentials_profile_name: Optional[str] = None,
        region_name: Optional[str] = None,
        node_label: str = "Entity",
        **kwargs: Any,
    ) -> None:
"""Create a new Neptune Analytics graph wrapper instance."""
        self.node_label = node_label
        self._client = create_neptune_analytics_client(
            graph_identifier, client, credentials_profile_name, region_name
        )
        self.graph_identifier = graph_identifier

    defquery(self, query: str, params: dict = {}) -> Dict[str, Any]:
"""Query Neptune Analytics graph."""
        try:
            logger.debug(f"query() query: {query} parameters: {json.dumps(params)}")
            resp = self.client.execute_query(
                graphIdentifier=self.graph_identifier,
                queryString=query,
                parameters=params,
                language="OPEN_CYPHER",
            )
            return json.loads(resp["payload"].read().decode("UTF-8"))["results"]
        except Exception as e:
            raise NeptuneQueryException(
                {
                    "message": "An error occurred while executing the query.",
                    "details": str(e),
                    "query": query,
                    "parameters": str(params),
                }
            )

    def_get_summary(self) -> Dict:
        try:
            response = self.client.get_graph_summary(
                graphIdentifier=self.graph_identifier, mode="detailed"
            )
        except Exception as e:
            raise NeptuneQueryException(
                {
                    "message": ("Summary API error occurred on Neptune Analytics"),
                    "details": str(e),
                }
            )

        try:
            summary = response["graphSummary"]
        except Exception:
            raise NeptuneQueryException(
                {
                    "message": "Summary API did not return a valid response.",
                    "details": response.content.decode(),
                }
            )
        else:
            return summary

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneAnalyticsGraphStore.query "Permanent link")

```
query(query: , params:  = {}) -> [, ]

```

Query Neptune Analytics graph.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/analytics.py`  
| 
```
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
```
 | 
```
defquery(self, query: str, params: dict = {}) -> Dict[str, Any]:
"""Query Neptune Analytics graph."""
    try:
        logger.debug(f"query() query: {query} parameters: {json.dumps(params)}")
        resp = self.client.execute_query(
            graphIdentifier=self.graph_identifier,
            queryString=query,
            parameters=params,
            language="OPEN_CYPHER",
        )
        return json.loads(resp["payload"].read().decode("UTF-8"))["results"]
    except Exception as e:
        raise NeptuneQueryException(
            {
                "message": "An error occurred while executing the query.",
                "details": str(e),
                "query": query,
                "parameters": str(params),
            }
        )

```
 |  
| --- | --- |  
##  NeptuneDatabaseGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneDatabaseGraphStore "Permanent link")
Bases: `NeptuneBaseGraphStore`
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/database.py`  
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
```
 | 
```
classNeptuneDatabaseGraphStore(NeptuneBaseGraphStore):
    def__init__(
        self,
        host: str,
        port: int = 8182,
        use_https: bool = True,
        client: Any = None,
        credentials_profile_name: Optional[str] = None,
        region_name: Optional[str] = None,
        sign: bool = True,
        node_label: str = "Entity",
        **kwargs: Any,
    ) -> None:
"""Create a new Neptune Database graph wrapper instance."""
        self.node_label = node_label
        self._client = create_neptune_database_client(
            host, port, client, credentials_profile_name, region_name, sign, use_https
        )

    defquery(self, query: str, params: dict = {}) -> Dict[str, Any]:
"""Query Neptune database."""
        try:
            logger.debug(f"query() query: {query} parameters: {json.dumps(params)}")
            return self.client.execute_open_cypher_query(
                openCypherQuery=query, parameters=json.dumps(params)
            )["results"]
        except Exception as e:
            raise NeptuneQueryException(
                {
                    "message": "An error occurred while executing the query.",
                    "details": str(e),
                    "query": query,
                    "parameters": str(params),
                }
            )

    def_get_summary(self) -> Dict:
        try:
            response = self.client.get_propertygraph_summary()
        except Exception as e:
            raise NeptuneQueryException(
                {
                    "message": (
                        "Summary API is not available for this instance of Neptune,"
                        "ensure the engine version is >=1.2.1.0"
                    ),
                    "details": str(e),
                }
            )

        try:
            summary = response["payload"]["graphSummary"]
        except Exception:
            raise NeptuneQueryException(
                {
                    "message": "Summary API did not return a valid response.",
                    "details": response.content.decode(),
                }
            )
        else:
            return summary

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneDatabaseGraphStore.query "Permanent link")

```
query(query: , params:  = {}) -> [, ]

```

Query Neptune database.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/database.py`  
| 
```
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
```
 | 
```
defquery(self, query: str, params: dict = {}) -> Dict[str, Any]:
"""Query Neptune database."""
    try:
        logger.debug(f"query() query: {query} parameters: {json.dumps(params)}")
        return self.client.execute_open_cypher_query(
            openCypherQuery=query, parameters=json.dumps(params)
        )["results"]
    except Exception as e:
        raise NeptuneQueryException(
            {
                "message": "An error occurred while executing the query.",
                "details": str(e),
                "query": query,
                "parameters": str(params),
            }
        )

```
 |  
| --- | --- |  
##  NeptuneAnalyticsPropertyGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneAnalyticsPropertyGraphStore "Permanent link")
Bases: `NeptuneBasePropertyGraph`
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/analytics_property_graph.py`  
| 
```
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
```
 | 
```
classNeptuneAnalyticsPropertyGraphStore(NeptuneBasePropertyGraph):
    supports_vector_queries: bool = True

    def__init__(
        self,
        graph_identifier: str,
        client: Any = None,
        credentials_profile_name: Optional[str] = None,
        region_name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
"""Create a new Neptune Analytics graph wrapper instance."""
        self._client = create_neptune_analytics_client(
            graph_identifier, client, credentials_profile_name, region_name
        )
        self.graph_identifier = graph_identifier

    defstructured_query(self, query: str, param_map: Dict[str, Any] = None) -> Any:
"""
        Run the structured query.

        Args:
            query (str): The query to run
            param_map (Dict[str, Any] | None, optional): A dictionary of query parameters. Defaults to None.

        Raises:
            NeptuneQueryException: An exception from Neptune with details

        Returns:
            Any: The results of the query

        """
        param_map = param_map or {}

        try:
            logger.debug(
                f"structured_query() query: {query} parameters: {json.dumps(param_map)}"
            )
            resp = self.client.execute_query(
                graphIdentifier=self.graph_identifier,
                queryString=query,
                parameters=param_map,
                language="OPEN_CYPHER",
            )
            return json.loads(resp["payload"].read().decode("UTF-8"))["results"]
        except Exception as e:
            raise NeptuneQueryException(
                {
                    "message": "An error occurred while executing the query.",
                    "details": str(e),
                    "query": query,
                    "parameters": str(param_map),
                }
            )

    defvector_query(self, query: VectorStoreQuery, **kwargs: Any) -> Tuple[List[Any]]:
"""
        Query the graph store with a vector store query.

        Returns:
            (nodes, score): The nodes and their associated score

        """
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
            f"""MATCH (e:`{BASE_ENTITY_LABEL}`)
            WHERE ({filters})
            CALL neptune.algo.vectors.get(e)
            YIELD embedding
            WHERE embedding IS NOT NULL
            CALL neptune.algo.vectors.topKByNode(e)
            YIELD node, score
            WITH e, score
            ORDER BY score DESC LIMIT $limit
            RETURN e.id AS name,
                [l in labels(e) WHERE l <> '{BASE_ENTITY_LABEL}' | l][0] AS type,
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

    defupsert_nodes(self, nodes: List[LabelledNode]) -> None:
"""
        Upsert the nodes in the graph.

        Args:
            nodes (List[LabelledNode]): The list of nodes to upsert

        """
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
            for d in chunk_dicts:
                self.structured_query(
"""
                    WITH $data AS row
                    MERGE (c:Chunk {id: row.id})
                    SET c.text = row.text
                    SET c += removeKeyFromMap(row.properties, '')
                    WITH c, row.embedding as e
                    WHERE e IS NOT NULL
                    CALL neptune.algo.vectors.upsert(c, e)
                    RETURN count(*)
,
                    param_map={"data": d},
                )

        if entity_dicts:
            for d in entity_dicts:
                self.structured_query(
                    f"""
                    WITH $data AS row
                    MERGE (e:`{BASE_NODE_LABEL}` {{id: row.id}})
                    SET e += removeKeyFromMap(row.properties, '')
                    SET e.name = row.name, e:`{BASE_ENTITY_LABEL}`
                    SET e:`{d["label"]}`
                    WITH e, row
                    WHERE removeKeyFromMap(row.properties, '').triplet_source_id IS NOT NULL
                    MERGE (c:Chunk {{id: removeKeyFromMap(row.properties, '').triplet_source_id}})
                    MERGE (e)<-[:MENTIONS]-(c)
                    WITH e, row.embedding as em
                    CALL neptune.algo.vectors.upsert(e, em)
                    RETURN count(*) as count
,
                    param_map={"data": d},
                )

    def_get_summary(self) -> Dict:
"""
        Get the Summary of the graph topology.

        Returns:
            Dict: The graph summary

        """
        try:
            response = self.client.get_graph_summary(
                graphIdentifier=self.graph_identifier, mode="detailed"
            )
        except Exception as e:
            raise NeptuneQueryException(
                {
                    "message": ("Summary API error occurred on Neptune Analytics"),
                    "details": str(e),
                }
            )

        try:
            summary = response["graphSummary"]
        except Exception:
            raise NeptuneQueryException(
                {
                    "message": "Summary API did not return a valid response.",
                    "details": response.content.decode(),
                }
            )
        else:
            return summary

```
 |  
| --- | --- |  
###  structured_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneAnalyticsPropertyGraphStore.structured_query "Permanent link")

```
structured_query(
    query: , param_map: [, ] = None
) -> 

```

Run the structured query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to run  |  _required_  |  
|  `param_map`  |  `Dict[str, Any] | None`  |  A dictionary of query parameters. Defaults to None.  |  `None`  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|   |  An exception from Neptune with details  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Any`  |  The results of the query  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/analytics_property_graph.py`  
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
```
 | 
```
defstructured_query(self, query: str, param_map: Dict[str, Any] = None) -> Any:
"""
    Run the structured query.

    Args:
        query (str): The query to run
        param_map (Dict[str, Any] | None, optional): A dictionary of query parameters. Defaults to None.

    Raises:
        NeptuneQueryException: An exception from Neptune with details

    Returns:
        Any: The results of the query

    """
    param_map = param_map or {}

    try:
        logger.debug(
            f"structured_query() query: {query} parameters: {json.dumps(param_map)}"
        )
        resp = self.client.execute_query(
            graphIdentifier=self.graph_identifier,
            queryString=query,
            parameters=param_map,
            language="OPEN_CYPHER",
        )
        return json.loads(resp["payload"].read().decode("UTF-8"))["results"]
    except Exception as e:
        raise NeptuneQueryException(
            {
                "message": "An error occurred while executing the query.",
                "details": str(e),
                "query": query,
                "parameters": str(param_map),
            }
        )

```
 |  
| --- | --- |  
###  vector_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneAnalyticsPropertyGraphStore.vector_query "Permanent link")

```
vector_query(
    query: , **kwargs: 
) -> Tuple[[]]

```

Query the graph store with a vector store query.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `(nodes, score)`  |  The nodes and their associated score  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/analytics_property_graph.py`  
| 
```
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
```
 | 
```
defvector_query(self, query: VectorStoreQuery, **kwargs: Any) -> Tuple[List[Any]]:
"""
    Query the graph store with a vector store query.

    Returns:
        (nodes, score): The nodes and their associated score

    """
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
        f"""MATCH (e:`{BASE_ENTITY_LABEL}`)
        WHERE ({filters})
        CALL neptune.algo.vectors.get(e)
        YIELD embedding
        WHERE embedding IS NOT NULL
        CALL neptune.algo.vectors.topKByNode(e)
        YIELD node, score
        WITH e, score
        ORDER BY score DESC LIMIT $limit
        RETURN e.id AS name,
            [l in labels(e) WHERE l <> '{BASE_ENTITY_LABEL}' | l][0] AS type,
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
###  upsert_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneAnalyticsPropertyGraphStore.upsert_nodes "Permanent link")

```
upsert_nodes(nodes: []) -> None

```

Upsert the nodes in the graph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `List[LabelledNode[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledNode "LabelledNode \(llama_index.core.graph_stores.types.LabelledNode\)")]`  |  The list of nodes to upsert  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/analytics_property_graph.py`  
| 
```
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
```
 | 
```
defupsert_nodes(self, nodes: List[LabelledNode]) -> None:
"""
    Upsert the nodes in the graph.

    Args:
        nodes (List[LabelledNode]): The list of nodes to upsert

    """
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
        for d in chunk_dicts:
            self.structured_query(
"""
                WITH $data AS row
                MERGE (c:Chunk {id: row.id})
                SET c.text = row.text
                SET c += removeKeyFromMap(row.properties, '')
                WITH c, row.embedding as e
                WHERE e IS NOT NULL
                CALL neptune.algo.vectors.upsert(c, e)
                RETURN count(*)
,
                param_map={"data": d},
            )

    if entity_dicts:
        for d in entity_dicts:
            self.structured_query(
                f"""
                WITH $data AS row
                MERGE (e:`{BASE_NODE_LABEL}` {{id: row.id}})
                SET e += removeKeyFromMap(row.properties, '')
                SET e.name = row.name, e:`{BASE_ENTITY_LABEL}`
                SET e:`{d["label"]}`
                WITH e, row
                WHERE removeKeyFromMap(row.properties, '').triplet_source_id IS NOT NULL
                MERGE (c:Chunk {{id: removeKeyFromMap(row.properties, '').triplet_source_id}})
                MERGE (e)<-[:MENTIONS]-(c)
                WITH e, row.embedding as em
                CALL neptune.algo.vectors.upsert(e, em)
                RETURN count(*) as count
,
                param_map={"data": d},
            )

```
 |  
| --- | --- |  
##  NeptuneDatabasePropertyGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneDatabasePropertyGraphStore "Permanent link")
Bases: `NeptuneBasePropertyGraph`
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/database_property_graph.py`  
| 
```
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
```
 | 
```
classNeptuneDatabasePropertyGraphStore(NeptuneBasePropertyGraph):
    supports_vector_queries: bool = False

    def__init__(
        self,
        host: str,
        port: int = 8182,
        client: Any = None,
        credentials_profile_name: Optional[str] = None,
        region_name: Optional[str] = None,
        sign: bool = True,
        use_https: bool = True,
        **kwargs: Any,
    ) -> None:
"""
        Init.

        Args:
            host (str): The host endpoint
            port (int, optional): The port. Defaults to 8182.
            client (Any, optional): If provided, this is the client that will be used. Defaults to None.
            credentials_profile_name (Optional[str], optional): If provided this is the credentials profile that will be used. Defaults to None.
            region_name (Optional[str], optional): The region to use. Defaults to None.
            sign (bool, optional): True will SigV4 sign all requests, False will not. Defaults to True.
            use_https (bool, optional): True to use https, False to use http. Defaults to True.

        """
        self._client = create_neptune_database_client(
            host, port, client, credentials_profile_name, region_name, sign, use_https
        )

    defstructured_query(self, query: str, param_map: Dict[str, Any] = None) -> Any:
"""
        Run the structured query.

        Args:
            query (str): The query to run
            param_map (Dict[str, Any] | None, optional): A dictionary of query parameters. Defaults to None.

        Raises:
            NeptuneQueryException: An exception from Neptune with details

        Returns:
            Any: The results of the query

        """
        param_map = param_map or {}

        try:
            logger.debug(
                f"structured_query() query: {query} parameters: {json.dumps(param_map)}"
            )

            return self.client.execute_open_cypher_query(
                openCypherQuery=query, parameters=json.dumps(param_map)
            )["results"]
        except Exception as e:
            raise NeptuneQueryException(
                {
                    "message": "An error occurred while executing the query.",
                    "details": str(e),
                    "query": query,
                    "parameters": str(param_map),
                }
            )

    defvector_query(self, query: VectorStoreQuery, **kwargs: Any) -> Tuple[List[Any]]:
"""
        NOT SUPPORTED.

        Args:
            query (VectorStoreQuery): _description_

        Raises:
            NotImplementedError: _description_

        Returns:
            Tuple[List[LabelledNode] | List[float]]: _description_

        """
        raise NotImplementedError

    defupsert_nodes(self, nodes: List[LabelledNode]) -> None:
"""
        Upsert the nodes in the graph.

        Args:
            nodes (List[LabelledNode]): The list of nodes to upsert

        """
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
            for d in chunk_dicts:
                self.structured_query(
"""
                    WITH $data AS row
                    MERGE (c:Chunk {id: row.id})
                    SET c.text = row.text
                    SET c += removeKeyFromMap(row.properties, '')
                    RETURN count(*)
,
                    param_map={"data": d},
                )

        if entity_dicts:
            for d in entity_dicts:
                self.structured_query(
                    f"""
                    WITH $data AS row
                    MERGE (e:`{BASE_NODE_LABEL}` {{id: row.id}})
                    SET e += removeKeyFromMap(row.properties, '')
                    SET e.name = row.name, e:`{BASE_ENTITY_LABEL}`
                    SET e:`{d["label"]}`
                    WITH e, row
                    WHERE removeKeyFromMap(row.properties, '').triplet_source_id IS NOT NULL
                    MERGE (c:Chunk {{id: removeKeyFromMap(row.properties, '').triplet_source_id}})
                    MERGE (e)<-[:MENTIONS]-(c)
                    RETURN count(*) as count
,
                    param_map={"data": d},
                )

    def_get_summary(self) -> Dict:
"""
        Get the Summary of the graph schema.

        Returns:
            Dict: The graph summary

        """
        try:
            response = self.client.get_propertygraph_summary()
        except Exception as e:
            raise NeptuneQueryException(
                {
                    "message": (
                        "Summary API is not available for this instance of Neptune,"
                        "ensure the engine version is >=1.2.1.0"
                    ),
                    "details": str(e),
                }
            )

        try:
            summary = response["payload"]["graphSummary"]
        except Exception:
            raise NeptuneQueryException(
                {
                    "message": "Summary API did not return a valid response.",
                    "details": response.content.decode(),
                }
            )
        else:
            return summary

```
 |  
| --- | --- |  
###  structured_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneDatabasePropertyGraphStore.structured_query "Permanent link")

```
structured_query(
    query: , param_map: [, ] = None
) -> 

```

Run the structured query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to run  |  _required_  |  
|  `param_map`  |  `Dict[str, Any] | None`  |  A dictionary of query parameters. Defaults to None.  |  `None`  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|   |  An exception from Neptune with details  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Any`  |  The results of the query  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/database_property_graph.py`  
| 
```
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
```
 | 
```
defstructured_query(self, query: str, param_map: Dict[str, Any] = None) -> Any:
"""
    Run the structured query.

    Args:
        query (str): The query to run
        param_map (Dict[str, Any] | None, optional): A dictionary of query parameters. Defaults to None.

    Raises:
        NeptuneQueryException: An exception from Neptune with details

    Returns:
        Any: The results of the query

    """
    param_map = param_map or {}

    try:
        logger.debug(
            f"structured_query() query: {query} parameters: {json.dumps(param_map)}"
        )

        return self.client.execute_open_cypher_query(
            openCypherQuery=query, parameters=json.dumps(param_map)
        )["results"]
    except Exception as e:
        raise NeptuneQueryException(
            {
                "message": "An error occurred while executing the query.",
                "details": str(e),
                "query": query,
                "parameters": str(param_map),
            }
        )

```
 |  
| --- | --- |  
###  vector_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneDatabasePropertyGraphStore.vector_query "Permanent link")

```
vector_query(
    query: , **kwargs: 
) -> Tuple[[]]

```

NOT SUPPORTED.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  _description_  |  _required_  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `NotImplementedError`  |  _description_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Tuple[List[Any]]`  |  Tuple[List[LabelledNode] | List[float]]: _description_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/database_property_graph.py`  
| 
```
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
```
 | 
```
defvector_query(self, query: VectorStoreQuery, **kwargs: Any) -> Tuple[List[Any]]:
"""
    NOT SUPPORTED.

    Args:
        query (VectorStoreQuery): _description_

    Raises:
        NotImplementedError: _description_

    Returns:
        Tuple[List[LabelledNode] | List[float]]: _description_

    """
    raise NotImplementedError

```
 |  
| --- | --- |  
###  upsert_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneDatabasePropertyGraphStore.upsert_nodes "Permanent link")

```
upsert_nodes(nodes: []) -> None

```

Upsert the nodes in the graph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `List[LabelledNode[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledNode "LabelledNode \(llama_index.core.graph_stores.types.LabelledNode\)")]`  |  The list of nodes to upsert  |  _required_  |  
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/database_property_graph.py`  
| 
```
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
```
 | 
```
defupsert_nodes(self, nodes: List[LabelledNode]) -> None:
"""
    Upsert the nodes in the graph.

    Args:
        nodes (List[LabelledNode]): The list of nodes to upsert

    """
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
        for d in chunk_dicts:
            self.structured_query(
"""
                WITH $data AS row
                MERGE (c:Chunk {id: row.id})
                SET c.text = row.text
                SET c += removeKeyFromMap(row.properties, '')
                RETURN count(*)
,
                param_map={"data": d},
            )

    if entity_dicts:
        for d in entity_dicts:
            self.structured_query(
                f"""
                WITH $data AS row
                MERGE (e:`{BASE_NODE_LABEL}` {{id: row.id}})
                SET e += removeKeyFromMap(row.properties, '')
                SET e.name = row.name, e:`{BASE_ENTITY_LABEL}`
                SET e:`{d["label"]}`
                WITH e, row
                WHERE removeKeyFromMap(row.properties, '').triplet_source_id IS NOT NULL
                MERGE (c:Chunk {{id: removeKeyFromMap(row.properties, '').triplet_source_id}})
                MERGE (e)<-[:MENTIONS]-(c)
                RETURN count(*) as count
,
                param_map={"data": d},
            )

```
 |  
| --- | --- |  
##  NeptuneQueryException [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/neptune/#llama_index.graph_stores.neptune.NeptuneQueryException "Permanent link")
Bases: `Exception`
Exception for the Neptune queries.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-neptune/llama_index/graph_stores/neptune/neptune.py`  
| 
```
 8
 9
10
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
```
 | 
```
classNeptuneQueryException(Exception):
"""Exception for the Neptune queries."""

    def__init__(self, exception: Union[str, Dict]):
        if isinstance(exception, dict):
            self.message = exception["message"] if "message" in exception else "unknown"
            self.details = exception["details"] if "details" in exception else "unknown"
        else:
            self.message = exception
            self.details = "unknown"

    defget_message(self) -> str:
        return self.message

    defget_details(self) -> Any:
        return self.details

```
 |  
| --- | --- |  
options: members: - NeptuneAnalyticsGraphStore - NeptuneAnalyticsPropertyGraphStore - NeptuneDatabaseGraphStore - NeptuneDatabasePropertyGraphStore
