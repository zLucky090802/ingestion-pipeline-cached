# Index
##  LabelledNode [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledNode "Permanent link")
Bases: `BaseModel`
An entity in a graph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `label`  |  The label of the node.  |  `'node'`  |  
|  `embedding`  |  `List[float] | None`  |  The embeddings of the node.  |  `None`  |  
|  `properties`  |  `Dict[str, Any]`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
```
 | 
```
classLabelledNode(BaseModel):
"""An entity in a graph."""

    label: str = Field(default="node", description="The label of the node.")
    embedding: Optional[List[float]] = Field(
        default=None, description="The embeddings of the node."
    )
    properties: Dict[str, Any] = Field(default_factory=dict)

    @abstractmethod
    def__str__(self) -> str:
"""Return the string representation of the node."""
        ...

    @property
    @abstractmethod
    defid(self) -> str:
"""Get the node id."""
        ...

```
 |  
| --- | --- |  
###  id `abstractmethod` `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledNode.id "Permanent link")

```
id: 

```

Get the node id.
##  EntityNode [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.EntityNode "Permanent link")
Bases: 
An entity in a graph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `label`  |  The label of the node.  |  `'entity'`  |  
|  `properties`  |  `Dict[str, Any]`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
|  `name`  |  The name of the entity.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
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
```
 | 
```
classEntityNode(LabelledNode):
"""An entity in a graph."""

    name: str = Field(description="The name of the entity.")
    label: str = Field(default="entity", description="The label of the node.")
    properties: Dict[str, Any] = Field(default_factory=dict)

    def__str__(self) -> str:
"""Return the string representation of the node."""
        if self.properties:
            return f"{self.name} ({self.properties})"
        return self.name

    @property
    defid(self) -> str:
"""Get the node id."""
        return self.name.replace('"', " ")

```
 |  
| --- | --- |  
###  id `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.EntityNode.id "Permanent link")

```
id: 

```

Get the node id.
##  ChunkNode [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.ChunkNode "Permanent link")
Bases: 
A text chunk in a graph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `label`  |  The label of the node.  |  `'text_chunk'`  |  
|  `properties`  |  `Dict[str, Any]`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
|  `text`  |  The text content of the chunk.  |  _required_  |  
|  `id_`  |  `str | None`  |  The id of the node. Defaults to a hash of the text.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
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
```
 | 
```
classChunkNode(LabelledNode):
"""A text chunk in a graph."""

    text: str = Field(description="The text content of the chunk.")
    id_: Optional[str] = Field(
        default=None, description="The id of the node. Defaults to a hash of the text."
    )
    label: str = Field(default="text_chunk", description="The label of the node.")
    properties: Dict[str, Any] = Field(default_factory=dict)

    def__str__(self) -> str:
"""Return the string representation of the node."""
        return self.text

    @property
    defid(self) -> str:
"""Get the node id."""
        return str(hash(self.text)) if self.id_ is None else self.id_

```
 |  
| --- | --- |  
###  id `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.ChunkNode.id "Permanent link")

```
id: 

```

Get the node id.
##  Relation [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.Relation "Permanent link")
Bases: `BaseModel`
A relation connecting two entities in a graph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `label`  |  _required_  |  
|  `source_id`  |  _required_  |  
|  `target_id`  |  _required_  |  
|  `properties`  |  `Dict[str, Any]`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
```
 | 
```
classRelation(BaseModel):
"""A relation connecting two entities in a graph."""

    label: str
    source_id: str
    target_id: str
    properties: Dict[str, Any] = Field(default_factory=dict)

    def__str__(self) -> str:
"""Return the string representation of the relation."""
        if self.properties:
            return f"{self.label} ({self.properties})"
        return self.label

    @property
    defid(self) -> str:
"""Get the relation id."""
        return self.label

```
 |  
| --- | --- |  
###  id `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.Relation.id "Permanent link")

```
id: 

```

Get the relation id.
##  LabelledPropertyGraph [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledPropertyGraph "Permanent link")
Bases: `BaseModel`
In memory labelled property graph containing entities and relations.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Dict[str, LabelledNode[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledNode "LabelledNode \(llama_index.core.graph_stores.types.LabelledNode\)")]`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
|  `relations`  |  `Dict[str, Relation[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.Relation "Relation \(llama_index.core.graph_stores.types.Relation\)")]`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
|  `triplets`  |  `Set[Tuple[str, str, str]]`  |  List of triplets (subject, relation, object).  |  `<dynamic>`  |  
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
```
 | 
```
classLabelledPropertyGraph(BaseModel):
"""In memory labelled property graph containing entities and relations."""

    nodes: SerializeAsAny[Dict[str, LabelledNode]] = Field(default_factory=dict)
    relations: SerializeAsAny[Dict[str, Relation]] = Field(default_factory=dict)
    triplets: Set[Tuple[str, str, str]] = Field(
        default_factory=set, description="List of triplets (subject, relation, object)."
    )

    def_get_relation_key(
        self,
        relation: Optional[Relation] = None,
        subj_id: Optional[str] = None,
        obj_id: Optional[str] = None,
        rel_id: Optional[str] = None,
    ) -> str:
"""Get relation id."""
        if relation:
            return f"{relation.source_id}_{relation.label}_{relation.target_id}"
        return f"{subj_id}_{rel_id}_{obj_id}"

    defget_all_nodes(self) -> List[LabelledNode]:
"""Get all entities."""
        return list(self.nodes.values())

    defget_all_relations(self) -> List[Relation]:
"""Get all relations."""
        return list(self.relations.values())

    defget_triplets(self) -> List[Triplet]:
"""Get all triplets."""
        return [
            (
                self.nodes[subj],
                self.relations[
                    self._get_relation_key(obj_id=obj, subj_id=subj, rel_id=rel)
                ],
                self.nodes[obj],
            )
            for subj, rel, obj in self.triplets
        ]

    defadd_triplet(self, triplet: Triplet) -> None:
"""Add a triplet."""
        subj, rel, obj = triplet
        if (subj.id, rel.id, obj.id) in self.triplets:
            return

        self.triplets.add((subj.id, rel.id, obj.id))
        self.nodes[subj.id] = subj
        self.nodes[obj.id] = obj
        self.relations[self._get_relation_key(relation=rel)] = rel

    defadd_node(self, node: LabelledNode) -> None:
"""Add a node."""
        self.nodes[node.id] = node

    defadd_relation(self, relation: Relation) -> None:
"""Add a relation."""
        if relation.source_id not in self.nodes:
            self.nodes[relation.source_id] = EntityNode(name=relation.source_id)
        if relation.target_id not in self.nodes:
            self.nodes[relation.target_id] = EntityNode(name=relation.target_id)

        self.add_triplet(
            (self.nodes[relation.source_id], relation, self.nodes[relation.target_id])
        )

    defdelete_triplet(self, triplet: Triplet) -> None:
"""Delete a triplet."""
        subj, rel, obj = triplet
        if (subj.id, rel.id, obj.id) not in self.triplets:
            return

        self.triplets.remove((subj.id, rel.id, obj.id))
        if subj.id in self.nodes:
            del self.nodes[subj.id]
        if obj.id in self.nodes:
            del self.nodes[obj.id]

        rel_key = self._get_relation_key(relation=rel)
        if rel_key in self.relations:
            del self.relations[rel_key]

    defdelete_node(self, node: LabelledNode) -> None:
"""Delete a node."""
        if node.id in self.nodes:
            del self.nodes[node.id]

    defdelete_relation(self, relation: Relation) -> None:
"""Delete a relation."""
        rel_key = self._get_relation_key(relation=relation)
        if rel_key in self.relations:
            del self.relations[rel_key]

```
 |  
| --- | --- |  
###  get_all_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledPropertyGraph.get_all_nodes "Permanent link")

```
get_all_nodes() -> []

```

Get all entities.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
140
141
142
```
 | 
```
defget_all_nodes(self) -> List[LabelledNode]:
"""Get all entities."""
    return list(self.nodes.values())

```
 |  
| --- | --- |  
###  get_all_relations [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledPropertyGraph.get_all_relations "Permanent link")

```
get_all_relations() -> []

```

Get all relations.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
144
145
146
```
 | 
```
defget_all_relations(self) -> List[Relation]:
"""Get all relations."""
    return list(self.relations.values())

```
 |  
| --- | --- |  
###  get_triplets [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledPropertyGraph.get_triplets "Permanent link")

```
get_triplets() -> [Triplet]

```

Get all triplets.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
defget_triplets(self) -> List[Triplet]:
"""Get all triplets."""
    return [
        (
            self.nodes[subj],
            self.relations[
                self._get_relation_key(obj_id=obj, subj_id=subj, rel_id=rel)
            ],
            self.nodes[obj],
        )
        for subj, rel, obj in self.triplets
    ]

```
 |  
| --- | --- |  
###  add_triplet [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledPropertyGraph.add_triplet "Permanent link")

```
add_triplet(triplet: Triplet) -> None

```

Add a triplet.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
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
```
 | 
```
defadd_triplet(self, triplet: Triplet) -> None:
"""Add a triplet."""
    subj, rel, obj = triplet
    if (subj.id, rel.id, obj.id) in self.triplets:
        return

    self.triplets.add((subj.id, rel.id, obj.id))
    self.nodes[subj.id] = subj
    self.nodes[obj.id] = obj
    self.relations[self._get_relation_key(relation=rel)] = rel

```
 |  
| --- | --- |  
###  add_node [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledPropertyGraph.add_node "Permanent link")

```
add_node(node: ) -> None

```

Add a node.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
172
173
174
```
 | 
```
defadd_node(self, node: LabelledNode) -> None:
"""Add a node."""
    self.nodes[node.id] = node

```
 |  
| --- | --- |  
###  add_relation [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledPropertyGraph.add_relation "Permanent link")

```
add_relation(relation: ) -> None

```

Add a relation.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
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
```
 | 
```
defadd_relation(self, relation: Relation) -> None:
"""Add a relation."""
    if relation.source_id not in self.nodes:
        self.nodes[relation.source_id] = EntityNode(name=relation.source_id)
    if relation.target_id not in self.nodes:
        self.nodes[relation.target_id] = EntityNode(name=relation.target_id)

    self.add_triplet(
        (self.nodes[relation.source_id], relation, self.nodes[relation.target_id])
    )

```
 |  
| --- | --- |  
###  delete_triplet [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledPropertyGraph.delete_triplet "Permanent link")

```
delete_triplet(triplet: Triplet) -> None

```

Delete a triplet.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
```
 | 
```
defdelete_triplet(self, triplet: Triplet) -> None:
"""Delete a triplet."""
    subj, rel, obj = triplet
    if (subj.id, rel.id, obj.id) not in self.triplets:
        return

    self.triplets.remove((subj.id, rel.id, obj.id))
    if subj.id in self.nodes:
        del self.nodes[subj.id]
    if obj.id in self.nodes:
        del self.nodes[obj.id]

    rel_key = self._get_relation_key(relation=rel)
    if rel_key in self.relations:
        del self.relations[rel_key]

```
 |  
| --- | --- |  
###  delete_node [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledPropertyGraph.delete_node "Permanent link")

```
delete_node(node: ) -> None

```

Delete a node.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
203
204
205
206
```
 | 
```
defdelete_node(self, node: LabelledNode) -> None:
"""Delete a node."""
    if node.id in self.nodes:
        del self.nodes[node.id]

```
 |  
| --- | --- |  
###  delete_relation [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledPropertyGraph.delete_relation "Permanent link")

```
delete_relation(relation: ) -> None

```

Delete a relation.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
208
209
210
211
212
```
 | 
```
defdelete_relation(self, relation: Relation) -> None:
"""Delete a relation."""
    rel_key = self._get_relation_key(relation=relation)
    if rel_key in self.relations:
        del self.relations[rel_key]

```
 |  
| --- | --- |  
##  GraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore "Permanent link")
Bases: `Protocol`
Abstract graph store protocol.
This protocol defines the interface for a graph store, which is responsible for storing and retrieving knowledge graph data.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
|   |  Any: The client used to connect to the graph store.  |  
|  `List[List[str]]`  |  Callable[[str], List[List[str]]]: Get triplets for a given subject.  |  
|   |  `Dict[str, List[List[str]]]`  |  Callable[[Optional[List[str]], int], Dict[str, List[List[str]]]]: Get subjects' rel map in max depth.  |  
|   |  `None`  |  Callable[[str, str, str], None]: Upsert a triplet.  |  
|   |  `None`  |  Callable[[str, str, str], None]: Delete a triplet.  |  
|   |  `None`  |  Callable[[str, Optional[fsspec.AbstractFileSystem]], None]: Persist the graph store to a file.  |  
|   |  Callable[[bool], str]: Get the schema of the graph store.  |  
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
```
 | 
```
@runtime_checkable
classGraphStore(Protocol):
"""
    Abstract graph store protocol.

    This protocol defines the interface for a graph store, which is responsible
    for storing and retrieving knowledge graph data.

    Attributes:
        client: Any: The client used to connect to the graph store.
        get: Callable[[str], List[List[str]]]: Get triplets for a given subject.
        get_rel_map: Callable[[Optional[List[str]], int], Dict[str, List[List[str]]]]:
            Get subjects' rel map in max depth.
        upsert_triplet: Callable[[str, str, str], None]: Upsert a triplet.
        delete: Callable[[str, str, str], None]: Delete a triplet.
        persist: Callable[[str, Optional[fsspec.AbstractFileSystem]], None]:
            Persist the graph store to a file.
        get_schema: Callable[[bool], str]: Get the schema of the graph store.

    """

    schema: str = ""

    @property
    defclient(self) -> Any:
"""Get client."""
        ...

    defget(self, subj: str) -> List[List[str]]:
"""Get triplets."""
        ...

    defget_rel_map(
        self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
    ) -> Dict[str, List[List[str]]]:
"""Get depth-aware rel map."""
        ...

    defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
        ...

    defdelete(self, subj: str, rel: str, obj: str) -> None:
"""Delete triplet."""
        ...

    defpersist(
        self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
    ) -> None:
"""Persist the graph store to a file."""
        return

    defget_schema(self, refresh: bool = False) -> str:
"""Get the schema of the graph store."""
        ...

    defquery(self, query: str, param_map: Optional[Dict[str, Any]] = {}) -> Any:
"""Query the graph store with statement and parameters."""
        ...

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore.client "Permanent link")

```
client: 

```

Get client.
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore.get "Permanent link")

```
get(subj: ) -> [[]]

```

Get triplets.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
243
244
245
```
 | 
```
defget(self, subj: str) -> List[List[str]]:
"""Get triplets."""
    ...

```
 |  
| --- | --- |  
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    subjs: Optional[[]] = None,
    depth:  = 2,
    limit:  = 30,
) -> [, [[]]]

```

Get depth-aware rel map.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
247
248
249
250
251
```
 | 
```
defget_rel_map(
    self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
) -> Dict[str, List[List[str]]]:
"""Get depth-aware rel map."""
    ...

```
 |  
| --- | --- |  
###  upsert_triplet [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore.upsert_triplet "Permanent link")

```
upsert_triplet(subj: , rel: , obj: ) -> None

```

Add triplet.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
253
254
255
```
 | 
```
defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
    ...

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore.delete "Permanent link")

```
delete(subj: , rel: , obj: ) -> None

```

Delete triplet.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
257
258
259
```
 | 
```
defdelete(self, subj: str, rel: str, obj: str) -> None:
"""Delete triplet."""
    ...

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore.persist "Permanent link")

```
persist(
    persist_path: ,
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persist the graph store to a file.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
261
262
263
264
265
```
 | 
```
defpersist(
    self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
) -> None:
"""Persist the graph store to a file."""
    return

```
 |  
| --- | --- |  
###  get_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore.get_schema "Permanent link")

```
get_schema(refresh:  = False) -> 

```

Get the schema of the graph store.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
267
268
269
```
 | 
```
defget_schema(self, refresh: bool = False) -> str:
"""Get the schema of the graph store."""
    ...

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore.query "Permanent link")

```
query(
    query: , param_map: Optional[[, ]] = {}
) -> 

```

Query the graph store with statement and parameters.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
271
272
273
```
 | 
```
defquery(self, query: str, param_map: Optional[Dict[str, Any]] = {}) -> Any:
"""Query the graph store with statement and parameters."""
    ...

```
 |  
| --- | --- |  
##  PropertyGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore "Permanent link")
Bases: 
Abstract labelled graph store protocol.
This protocol defines the interface for a graph store, which is responsible for storing and retrieving knowledge graph data.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
|   |  Any: The client used to connect to the graph store.  |  
|  `List[LabelledNode[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.LabelledNode "LabelledNode \(llama_index.core.graph_stores.types.LabelledNode\)")]`  |  Callable[[str], List[List[str]]]: Get triplets for a given subject.  |  
|   |  `List[Triplet]`  |  Callable[[Optional[List[str]], int], Dict[str, List[List[str]]]]: Get subjects' rel map in max depth.  |  
| `upsert_triplet`  |  `List[Triplet]`  |  Callable[[str, str, str], None]: Upsert a triplet.  |  
|   |  `None`  |  Callable[[str, str, str], None]: Delete a triplet.  |  
|   |  `None`  |  Callable[[str, Optional[fsspec.AbstractFileSystem]], None]: Persist the graph store to a file.  |  
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
```
 | 
```
classPropertyGraphStore(ABC):
"""
    Abstract labelled graph store protocol.

    This protocol defines the interface for a graph store, which is responsible
    for storing and retrieving knowledge graph data.

    Attributes:
        client: Any: The client used to connect to the graph store.
        get: Callable[[str], List[List[str]]]: Get triplets for a given subject.
        get_rel_map: Callable[[Optional[List[str]], int], Dict[str, List[List[str]]]]:
            Get subjects' rel map in max depth.
        upsert_triplet: Callable[[str, str, str], None]: Upsert a triplet.
        delete: Callable[[str, str, str], None]: Delete a triplet.
        persist: Callable[[str, Optional[fsspec.AbstractFileSystem]], None]:
            Persist the graph store to a file.

    """

    supports_structured_queries: bool = False
    supports_vector_queries: bool = False
    text_to_cypher_template: PromptTemplate = DEFAULT_CYPHER_TEMPALTE

    @property
    defclient(self) -> Any:
"""Get client."""

    @abstractmethod
    defget(
        self,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[LabelledNode]:
"""Get nodes with matching values."""
        ...

    @abstractmethod
    defget_triplets(
        self,
        entity_names: Optional[List[str]] = None,
        relation_names: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[Triplet]:
"""Get triplets with matching values."""
        ...

    @abstractmethod
    defget_rel_map(
        self,
        graph_nodes: List[LabelledNode],
        depth: int = 2,
        limit: int = 30,
        ignore_rels: Optional[List[str]] = None,
    ) -> List[Triplet]:
"""Get depth-aware rel map."""
        ...

    defget_llama_nodes(self, node_ids: List[str]) -> List[BaseNode]:
"""Get llama-index nodes."""
        nodes = self.get(ids=node_ids)
        converted_nodes = []
        for node in nodes:
            try:
                converted_nodes.append(metadata_dict_to_node(node.properties))
                converted_nodes[-1].set_content(node.text)  # type: ignore
            except Exception:
                continue

        return converted_nodes

    @abstractmethod
    defupsert_nodes(self, nodes: Sequence[LabelledNode]) -> None:
"""Upsert nodes."""
        ...

    @abstractmethod
    defupsert_relations(self, relations: List[Relation]) -> None:
"""Upsert relations."""
        ...

    defupsert_llama_nodes(self, llama_nodes: List[BaseNode]) -> None:
"""Add llama-index nodes."""
        converted_nodes = []
        for llama_node in llama_nodes:
            metadata_dict = node_to_metadata_dict(llama_node, remove_text=True)
            converted_nodes.append(
                ChunkNode(
                    text=llama_node.get_content(metadata_mode=MetadataMode.NONE),
                    id_=llama_node.id_,
                    properties=metadata_dict,
                    embedding=llama_node.embedding,
                )
            )
        self.upsert_nodes(converted_nodes)

    @abstractmethod
    defdelete(
        self,
        entity_names: Optional[List[str]] = None,
        relation_names: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
"""Delete matching data."""
        ...

    defdelete_llama_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        ref_doc_ids: Optional[List[str]] = None,
    ) -> None:
"""
        Delete llama-index nodes.

        Intended to delete any nodes in the graph store associated
        with the given llama-index node_ids or ref_doc_ids.
        """
        nodes = []

        node_ids = node_ids or []
        for id_ in node_ids:
            nodes.extend(self.get(properties={TRIPLET_SOURCE_KEY: id_}))

        if len(node_ids)  0:
            nodes.extend(self.get(ids=node_ids))

        ref_doc_ids = ref_doc_ids or []
        for id_ in ref_doc_ids:
            nodes.extend(self.get(properties={"ref_doc_id": id_}))

        if len(ref_doc_ids)  0:
            nodes.extend(self.get(ids=ref_doc_ids))

        self.delete(ids=[node.id for node in nodes])

    @abstractmethod
    defstructured_query(
        self, query: str, param_map: Optional[Dict[str, Any]] = None
    ) -> Any:
"""Query the graph store with statement and parameters."""
        ...

    @abstractmethod
    defvector_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> Tuple[List[LabelledNode], List[float]]:
"""Query the graph store with a vector store query."""
        ...

    defpersist(
        self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
    ) -> None:
"""Persist the graph store to a file."""
        return

    defget_schema(self, refresh: bool = False) -> Any:
"""Get the schema of the graph store."""
        return None

    defget_schema_str(self, refresh: bool = False) -> str:
"""Get the schema of the graph store as a string."""
        return str(self.get_schema(refresh=refresh))

    ### ----- Async Methods ----- ###

    async defaget(
        self,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[LabelledNode]:
"""Asynchronously get nodes with matching values."""
        return self.get(properties, ids)

    async defaget_triplets(
        self,
        entity_names: Optional[List[str]] = None,
        relation_names: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[Triplet]:
"""Asynchronously get triplets with matching values."""
        return self.get_triplets(entity_names, relation_names, properties, ids)

    async defaget_rel_map(
        self,
        graph_nodes: List[LabelledNode],
        depth: int = 2,
        limit: int = 30,
        ignore_rels: Optional[List[str]] = None,
    ) -> List[Triplet]:
"""Asynchronously get depth-aware rel map."""
        return self.get_rel_map(graph_nodes, depth, limit, ignore_rels)

    async defaget_llama_nodes(self, node_ids: List[str]) -> List[BaseNode]:
"""Asynchronously get nodes."""
        nodes = await self.aget(ids=node_ids)
        converted_nodes = []
        for node in nodes:
            try:
                converted_nodes.append(metadata_dict_to_node(node.properties))
                converted_nodes[-1].set_content(node.text)  # type: ignore
            except Exception:
                continue

        return converted_nodes

    async defaupsert_nodes(self, nodes: List[LabelledNode]) -> None:
"""Asynchronously add nodes."""
        return self.upsert_nodes(nodes)

    async defaupsert_relations(self, relations: List[Relation]) -> None:
"""Asynchronously add relations."""
        return self.upsert_relations(relations)

    async defadelete(
        self,
        entity_names: Optional[List[str]] = None,
        relation_names: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
"""Asynchronously delete matching data."""
        return self.delete(entity_names, relation_names, properties, ids)

    async defadelete_llama_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        ref_doc_ids: Optional[List[str]] = None,
    ) -> None:
"""Asynchronously delete llama-index nodes."""
        return self.delete_llama_nodes(node_ids, ref_doc_ids)

    async defastructured_query(
        self, query: str, param_map: Optional[Dict[str, Any]] = {}
    ) -> Any:
"""Asynchronously query the graph store with statement and parameters."""
        return self.structured_query(query, param_map)

    async defavector_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> Tuple[List[LabelledNode], List[float]]:
"""Asynchronously query the graph store with a vector store query."""
        return self.vector_query(query, **kwargs)

    async defaget_schema(self, refresh: bool = False) -> str:
"""Asynchronously get the schema of the graph store."""
        return self.get_schema(refresh=refresh)

    async defaget_schema_str(self, refresh: bool = False) -> str:
"""Asynchronously get the schema of the graph store as a string."""
        return str(await self.aget_schema(refresh=refresh))

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.client "Permanent link")

```
client: 

```

Get client.
###  get `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.get "Permanent link")

```
get(
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> []

```

Get nodes with matching values.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
303
304
305
306
307
308
309
310
```
 | 
```
@abstractmethod
defget(
    self,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> List[LabelledNode]:
"""Get nodes with matching values."""
    ...

```
 |  
| --- | --- |  
###  get_triplets `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.get_triplets "Permanent link")

```
get_triplets(
    entity_names: Optional[[]] = None,
    relation_names: Optional[[]] = None,
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> [Triplet]

```

Get triplets with matching values.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
```
 | 
```
@abstractmethod
defget_triplets(
    self,
    entity_names: Optional[List[str]] = None,
    relation_names: Optional[List[str]] = None,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> List[Triplet]:
"""Get triplets with matching values."""
    ...

```
 |  
| --- | --- |  
###  get_rel_map `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    graph_nodes: [],
    depth:  = 2,
    limit:  = 30,
    ignore_rels: Optional[[]] = None,
) -> [Triplet]

```

Get depth-aware rel map.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
```
 | 
```
@abstractmethod
defget_rel_map(
    self,
    graph_nodes: List[LabelledNode],
    depth: int = 2,
    limit: int = 30,
    ignore_rels: Optional[List[str]] = None,
) -> List[Triplet]:
"""Get depth-aware rel map."""
    ...

```
 |  
| --- | --- |  
###  get_llama_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.get_llama_nodes "Permanent link")

```
get_llama_nodes(node_ids: []) -> []

```

Get llama-index nodes.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
defget_llama_nodes(self, node_ids: List[str]) -> List[BaseNode]:
"""Get llama-index nodes."""
    nodes = self.get(ids=node_ids)
    converted_nodes = []
    for node in nodes:
        try:
            converted_nodes.append(metadata_dict_to_node(node.properties))
            converted_nodes[-1].set_content(node.text)  # type: ignore
        except Exception:
            continue

    return converted_nodes

```
 |  
| --- | --- |  
###  upsert_nodes `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.upsert_nodes "Permanent link")

```
upsert_nodes(nodes: Sequence[]) -> None

```

Upsert nodes.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
347
348
349
350
```
 | 
```
@abstractmethod
defupsert_nodes(self, nodes: Sequence[LabelledNode]) -> None:
"""Upsert nodes."""
    ...

```
 |  
| --- | --- |  
###  upsert_relations `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.upsert_relations "Permanent link")

```
upsert_relations(relations: []) -> None

```

Upsert relations.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
352
353
354
355
```
 | 
```
@abstractmethod
defupsert_relations(self, relations: List[Relation]) -> None:
"""Upsert relations."""
    ...

```
 |  
| --- | --- |  
###  upsert_llama_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.upsert_llama_nodes "Permanent link")

```
upsert_llama_nodes(llama_nodes: []) -> None

```

Add llama-index nodes.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
```
 | 
```
defupsert_llama_nodes(self, llama_nodes: List[BaseNode]) -> None:
"""Add llama-index nodes."""
    converted_nodes = []
    for llama_node in llama_nodes:
        metadata_dict = node_to_metadata_dict(llama_node, remove_text=True)
        converted_nodes.append(
            ChunkNode(
                text=llama_node.get_content(metadata_mode=MetadataMode.NONE),
                id_=llama_node.id_,
                properties=metadata_dict,
                embedding=llama_node.embedding,
            )
        )
    self.upsert_nodes(converted_nodes)

```
 |  
| --- | --- |  
###  delete `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.delete "Permanent link")

```
delete(
    entity_names: Optional[[]] = None,
    relation_names: Optional[[]] = None,
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> None

```

Delete matching data.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
```
 | 
```
@abstractmethod
defdelete(
    self,
    entity_names: Optional[List[str]] = None,
    relation_names: Optional[List[str]] = None,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> None:
"""Delete matching data."""
    ...

```
 |  
| --- | --- |  
###  delete_llama_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.delete_llama_nodes "Permanent link")

```
delete_llama_nodes(
    node_ids: Optional[[]] = None,
    ref_doc_ids: Optional[[]] = None,
) -> None

```

Delete llama-index nodes.
Intended to delete any nodes in the graph store associated with the given llama-index node_ids or ref_doc_ids.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
```
 | 
```
defdelete_llama_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    ref_doc_ids: Optional[List[str]] = None,
) -> None:
"""
    Delete llama-index nodes.

    Intended to delete any nodes in the graph store associated
    with the given llama-index node_ids or ref_doc_ids.
    """
    nodes = []

    node_ids = node_ids or []
    for id_ in node_ids:
        nodes.extend(self.get(properties={TRIPLET_SOURCE_KEY: id_}))

    if len(node_ids)  0:
        nodes.extend(self.get(ids=node_ids))

    ref_doc_ids = ref_doc_ids or []
    for id_ in ref_doc_ids:
        nodes.extend(self.get(properties={"ref_doc_id": id_}))

    if len(ref_doc_ids)  0:
        nodes.extend(self.get(ids=ref_doc_ids))

    self.delete(ids=[node.id for node in nodes])

```
 |  
| --- | --- |  
###  structured_query `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.structured_query "Permanent link")

```
structured_query(
    query: , param_map: Optional[[, ]] = None
) -> 

```

Query the graph store with statement and parameters.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
412
413
414
415
416
417
```
 | 
```
@abstractmethod
defstructured_query(
    self, query: str, param_map: Optional[Dict[str, Any]] = None
) -> Any:
"""Query the graph store with statement and parameters."""
    ...

```
 |  
| --- | --- |  
###  vector_query `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.vector_query "Permanent link")

```
vector_query(
    query: , **kwargs: 
) -> Tuple[[], [float]]

```

Query the graph store with a vector store query.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
419
420
421
422
423
424
```
 | 
```
@abstractmethod
defvector_query(
    self, query: VectorStoreQuery, **kwargs: Any
) -> Tuple[List[LabelledNode], List[float]]:
"""Query the graph store with a vector store query."""
    ...

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.persist "Permanent link")

```
persist(
    persist_path: ,
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persist the graph store to a file.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
426
427
428
429
430
```
 | 
```
defpersist(
    self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
) -> None:
"""Persist the graph store to a file."""
    return

```
 |  
| --- | --- |  
###  get_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.get_schema "Permanent link")

```
get_schema(refresh:  = False) -> 

```

Get the schema of the graph store.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
432
433
434
```
 | 
```
defget_schema(self, refresh: bool = False) -> Any:
"""Get the schema of the graph store."""
    return None

```
 |  
| --- | --- |  
###  get_schema_str [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.get_schema_str "Permanent link")

```
get_schema_str(refresh:  = False) -> 

```

Get the schema of the graph store as a string.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
436
437
438
```
 | 
```
defget_schema_str(self, refresh: bool = False) -> str:
"""Get the schema of the graph store as a string."""
    return str(self.get_schema(refresh=refresh))

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.aget "Permanent link")

```
aget(
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> []

```

Asynchronously get nodes with matching values.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
442
443
444
445
446
447
448
```
 | 
```
async defaget(
    self,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> List[LabelledNode]:
"""Asynchronously get nodes with matching values."""
    return self.get(properties, ids)

```
 |  
| --- | --- |  
###  aget_triplets [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.aget_triplets "Permanent link")

```
aget_triplets(
    entity_names: Optional[[]] = None,
    relation_names: Optional[[]] = None,
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> [Triplet]

```

Asynchronously get triplets with matching values.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
450
451
452
453
454
455
456
457
458
```
 | 
```
async defaget_triplets(
    self,
    entity_names: Optional[List[str]] = None,
    relation_names: Optional[List[str]] = None,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> List[Triplet]:
"""Asynchronously get triplets with matching values."""
    return self.get_triplets(entity_names, relation_names, properties, ids)

```
 |  
| --- | --- |  
###  aget_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.aget_rel_map "Permanent link")

```
aget_rel_map(
    graph_nodes: [],
    depth:  = 2,
    limit:  = 30,
    ignore_rels: Optional[[]] = None,
) -> [Triplet]

```

Asynchronously get depth-aware rel map.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
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
async defaget_rel_map(
    self,
    graph_nodes: List[LabelledNode],
    depth: int = 2,
    limit: int = 30,
    ignore_rels: Optional[List[str]] = None,
) -> List[Triplet]:
"""Asynchronously get depth-aware rel map."""
    return self.get_rel_map(graph_nodes, depth, limit, ignore_rels)

```
 |  
| --- | --- |  
###  aget_llama_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.aget_llama_nodes "Permanent link")

```
aget_llama_nodes(node_ids: []) -> []

```

Asynchronously get nodes.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
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
```
 | 
```
async defaget_llama_nodes(self, node_ids: List[str]) -> List[BaseNode]:
"""Asynchronously get nodes."""
    nodes = await self.aget(ids=node_ids)
    converted_nodes = []
    for node in nodes:
        try:
            converted_nodes.append(metadata_dict_to_node(node.properties))
            converted_nodes[-1].set_content(node.text)  # type: ignore
        except Exception:
            continue

    return converted_nodes

```
 |  
| --- | --- |  
###  aupsert_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.aupsert_nodes "Permanent link")

```
aupsert_nodes(nodes: []) -> None

```

Asynchronously add nodes.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
483
484
485
```
 | 
```
async defaupsert_nodes(self, nodes: List[LabelledNode]) -> None:
"""Asynchronously add nodes."""
    return self.upsert_nodes(nodes)

```
 |  
| --- | --- |  
###  aupsert_relations [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.aupsert_relations "Permanent link")

```
aupsert_relations(relations: []) -> None

```

Asynchronously add relations.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
487
488
489
```
 | 
```
async defaupsert_relations(self, relations: List[Relation]) -> None:
"""Asynchronously add relations."""
    return self.upsert_relations(relations)

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.adelete "Permanent link")

```
adelete(
    entity_names: Optional[[]] = None,
    relation_names: Optional[[]] = None,
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> None

```

Asynchronously delete matching data.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
491
492
493
494
495
496
497
498
499
```
 | 
```
async defadelete(
    self,
    entity_names: Optional[List[str]] = None,
    relation_names: Optional[List[str]] = None,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> None:
"""Asynchronously delete matching data."""
    return self.delete(entity_names, relation_names, properties, ids)

```
 |  
| --- | --- |  
###  adelete_llama_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.adelete_llama_nodes "Permanent link")

```
adelete_llama_nodes(
    node_ids: Optional[[]] = None,
    ref_doc_ids: Optional[[]] = None,
) -> None

```

Asynchronously delete llama-index nodes.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
501
502
503
504
505
506
507
```
 | 
```
async defadelete_llama_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    ref_doc_ids: Optional[List[str]] = None,
) -> None:
"""Asynchronously delete llama-index nodes."""
    return self.delete_llama_nodes(node_ids, ref_doc_ids)

```
 |  
| --- | --- |  
###  astructured_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.astructured_query "Permanent link")

```
astructured_query(
    query: , param_map: Optional[[, ]] = {}
) -> 

```

Asynchronously query the graph store with statement and parameters.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
509
510
511
512
513
```
 | 
```
async defastructured_query(
    self, query: str, param_map: Optional[Dict[str, Any]] = {}
) -> Any:
"""Asynchronously query the graph store with statement and parameters."""
    return self.structured_query(query, param_map)

```
 |  
| --- | --- |  
###  avector_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.avector_query "Permanent link")

```
avector_query(
    query: , **kwargs: 
) -> Tuple[[], [float]]

```

Asynchronously query the graph store with a vector store query.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
515
516
517
518
519
```
 | 
```
async defavector_query(
    self, query: VectorStoreQuery, **kwargs: Any
) -> Tuple[List[LabelledNode], List[float]]:
"""Asynchronously query the graph store with a vector store query."""
    return self.vector_query(query, **kwargs)

```
 |  
| --- | --- |  
###  aget_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.aget_schema "Permanent link")

```
aget_schema(refresh:  = False) -> 

```

Asynchronously get the schema of the graph store.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
521
522
523
```
 | 
```
async defaget_schema(self, refresh: bool = False) -> str:
"""Asynchronously get the schema of the graph store."""
    return self.get_schema(refresh=refresh)

```
 |  
| --- | --- |  
###  aget_schema_str [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore.aget_schema_str "Permanent link")

```
aget_schema_str(refresh:  = False) -> 

```

Asynchronously get the schema of the graph store as a string.
Source code in `llama-index-core/llama_index/core/graph_stores/types.py`  
| 
```
525
526
527
```
 | 
```
async defaget_schema_str(self, refresh: bool = False) -> str:
"""Asynchronously get the schema of the graph store as a string."""
    return str(await self.aget_schema(refresh=refresh))

```
 |  
| --- | --- |  
options: members: - GraphStore - PropertyGraphStore - DEFAULT_PERSIST_DIR - DEFAULT_PERSIST_FNAME
