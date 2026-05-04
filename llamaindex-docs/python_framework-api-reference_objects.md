# Index
LlamaIndex objects.
##  ObjectIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.ObjectIndex "Permanent link")
Bases: `Generic[OT]`
Object index.
Source code in `llama-index-core/llama_index/core/objects/base.py`  
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
```
 | 
```
classObjectIndex(Generic[OT]):
"""Object index."""

    def__init__(
        self, index: BaseIndex, object_node_mapping: BaseObjectNodeMapping
    ) -> None:
        self._index = index
        self._object_node_mapping = object_node_mapping

    @property
    defindex(self) -> BaseIndex:
"""Index."""
        return self._index

    @property
    defobject_node_mapping(self) -> BaseObjectNodeMapping:
"""Object node mapping."""
        return self._object_node_mapping

    @classmethod
    deffrom_objects(
        cls,
        objects: Sequence[OT],
        object_mapping: Optional[BaseObjectNodeMapping] = None,
        from_node_fn: Optional[Callable[[BaseNode], OT]] = None,
        to_node_fn: Optional[Callable[[OT], BaseNode]] = None,
        index_cls: Type[BaseIndex] = VectorStoreIndex,
        **index_kwargs: Any,
    ) -> "ObjectIndex":
        fromllama_index.core.objects.utilsimport get_object_mapping

        # pick the best mapping if not provided
        if object_mapping is None:
            object_mapping = get_object_mapping(
                objects,
                from_node_fn=from_node_fn,
                to_node_fn=to_node_fn,
            )

        nodes = object_mapping.to_nodes(objects)
        index = index_cls(nodes, **index_kwargs)
        return cls(index, object_mapping)

    @classmethod
    deffrom_objects_and_index(
        cls,
        objects: Sequence[OT],
        index: BaseIndex,
        object_mapping: Optional[BaseObjectNodeMapping] = None,
        from_node_fn: Optional[Callable[[BaseNode], OT]] = None,
        to_node_fn: Optional[Callable[[OT], BaseNode]] = None,
    ) -> "ObjectIndex":
        fromllama_index.core.objects.utilsimport get_object_mapping

        # pick the best mapping if not provided
        if object_mapping is None:
            object_mapping = get_object_mapping(
                objects,
                from_node_fn=from_node_fn,
                to_node_fn=to_node_fn,
            )

        return cls(index, object_mapping)

    definsert_object(self, obj: Any) -> None:
        self._object_node_mapping.add_object(obj)
        node = self._object_node_mapping.to_node(obj)
        self._index.insert_nodes([node])

    defas_retriever(
        self,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        **kwargs: Any,
    ) -> ObjectRetriever:
        return ObjectRetriever(
            retriever=self._index.as_retriever(**kwargs),
            object_node_mapping=self._object_node_mapping,
            node_postprocessors=node_postprocessors,
        )

    defas_node_retriever(self, **kwargs: Any) -> BaseRetriever:
        return self._index.as_retriever(**kwargs)

    defpersist(
        self,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        obj_node_mapping_fname: str = DEFAULT_PERSIST_FNAME,
    ) -> None:
        # try to persist object node mapping
        try:
            self._object_node_mapping.persist(
                persist_dir=persist_dir, obj_node_mapping_fname=obj_node_mapping_fname
            )
        except (NotImplementedError, pickle.PickleError) as err:
            warnings.warn(
                (
                    "Unable to persist ObjectNodeMapping. You will need to "
                    "reconstruct the same object node mapping to build this ObjectIndex"
                ),
                stacklevel=2,
            )
        self._index._storage_context.persist(persist_dir=persist_dir)

    @classmethod
    deffrom_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        object_node_mapping: Optional[BaseObjectNodeMapping] = None,
    ) -> "ObjectIndex":
        fromllama_index.core.indicesimport load_index_from_storage

        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        index = load_index_from_storage(storage_context)
        if object_node_mapping:
            return cls(index=index, object_node_mapping=object_node_mapping)
        else:
            # try to load object_node_mapping
            # assume SimpleObjectNodeMapping for simplicity as its only subclass
            # that supports this method
            try:
                object_node_mapping = SimpleObjectNodeMapping.from_persist_dir(
                    persist_dir=persist_dir
                )
            except Exception as err:
                raise Exception(
                    "Unable to load from persist dir. The object_node_mapping cannot be loaded."
                ) fromerr
            else:
                return cls(index=index, object_node_mapping=object_node_mapping)

```
 |  
| --- | --- |  
###  index `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.ObjectIndex.index "Permanent link")

```
index: 

```

Index.
###  object_node_mapping `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.ObjectIndex.object_node_mapping "Permanent link")

```
object_node_mapping: BaseObjectNodeMapping

```

Object node mapping.
##  ObjectRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.ObjectRetriever "Permanent link")
Bases: `Generic[OT]`
Object retriever.
Source code in `llama-index-core/llama_index/core/objects/base.py`  
| 
```
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
```
 | 
```
classObjectRetriever(Generic[OT]):
"""Object retriever."""

    def__init__(
        self,
        retriever: BaseRetriever,
        object_node_mapping: BaseObjectNodeMapping[OT],
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
    ):
        self._retriever = retriever
        self._object_node_mapping = object_node_mapping
        self._node_postprocessors = node_postprocessors or []

    @property
    defretriever(self) -> BaseRetriever:
"""Retriever."""
        return self._retriever

    @property
    defobject_node_mapping(self) -> BaseObjectNodeMapping[OT]:
"""Object node mapping."""
        return self._object_node_mapping

    @property
    defnode_postprocessors(self) -> List[BaseNodePostprocessor]:
"""Node postprocessors."""
        return self._node_postprocessors

    defretrieve(self, str_or_query_bundle: QueryType) -> List[OT]:
        if isinstance(str_or_query_bundle, str):
            query_bundle = QueryBundle(query_str=str_or_query_bundle)
        else:
            query_bundle = str_or_query_bundle

        nodes = self._retriever.retrieve(query_bundle)
        for node_postprocessor in self._node_postprocessors:
            nodes = node_postprocessor.postprocess_nodes(
                nodes, query_bundle=query_bundle
            )

        return [self._object_node_mapping.from_node(node.node) for node in nodes]

    async defaretrieve(self, str_or_query_bundle: QueryType) -> List[OT]:
        if isinstance(str_or_query_bundle, str):
            query_bundle = QueryBundle(query_str=str_or_query_bundle)
        else:
            query_bundle = str_or_query_bundle

        nodes = await self._retriever.aretrieve(query_bundle)
        for node_postprocessor in self._node_postprocessors:
            nodes = node_postprocessor.postprocess_nodes(
                nodes, query_bundle=query_bundle
            )

        return [self._object_node_mapping.from_node(node.node) for node in nodes]

```
 |  
| --- | --- |  
###  retriever `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.ObjectRetriever.retriever "Permanent link")

```
retriever: 

```

Retriever.
###  object_node_mapping `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.ObjectRetriever.object_node_mapping "Permanent link")

```
object_node_mapping: BaseObjectNodeMapping[]

```

Object node mapping.
###  node_postprocessors `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.ObjectRetriever.node_postprocessors "Permanent link")

```
node_postprocessors: []

```

Node postprocessors.
##  SimpleObjectNodeMapping [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SimpleObjectNodeMapping "Permanent link")
Bases: `BaseObjectNodeMapping[Any]`
General node mapping that works for any obj.
More specifically, any object with a meaningful string representation.
Source code in `llama-index-core/llama_index/core/objects/base_node_mapping.py`  
| 
```
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
```
 | 
```
classSimpleObjectNodeMapping(BaseObjectNodeMapping[Any]):
"""
    General node mapping that works for any obj.

    More specifically, any object with a meaningful string representation.

    """

    def__init__(self, objs: Optional[Sequence[Any]] = None) -> None:
        objs = objs or []
        for obj in objs:
            self.validate_object(obj)
        self._objs = {hash(str(obj)): obj for obj in objs}

    @classmethod
    deffrom_objects(
        cls, objs: Sequence[Any], *args: Any, **kwargs: Any
    ) -> "SimpleObjectNodeMapping":
        return cls(objs)

    @property
    defobj_node_mapping(self) -> Dict[int, Any]:
        return self._objs

    @obj_node_mapping.setter
    defobj_node_mapping(self, mapping: Dict[int, Any]) -> None:
        self._objs = mapping

    def_add_object(self, obj: Any) -> None:
        self._objs[hash(str(obj))] = obj

    defto_node(self, obj: Any) -> TextNode:
        return TextNode(id_=str(hash(str(obj))), text=str(obj))

    def_from_node(self, node: BaseNode) -> Any:
        return self._objs[hash(node.get_content(metadata_mode=MetadataMode.NONE))]

    defpersist(
        self,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        obj_node_mapping_fname: str = DEFAULT_PERSIST_FNAME,
    ) -> None:
"""
        Persist object node mapping.

        NOTE: This may fail depending on whether the object types are
        pickle-able.
        """
        if not os.path.exists(persist_dir):
            os.makedirs(persist_dir)
        obj_node_mapping_path = concat_dirs(persist_dir, obj_node_mapping_fname)
        try:
            with open(obj_node_mapping_path, "wb") as f:
                pickle.dump(self, f)
        except pickle.PickleError as err:
            raise ValueError("Objs is not pickleable") fromerr

    @classmethod
    deffrom_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        obj_node_mapping_fname: str = DEFAULT_PERSIST_FNAME,
    ) -> "SimpleObjectNodeMapping":
        obj_node_mapping_path = concat_dirs(persist_dir, obj_node_mapping_fname)
        try:
            with open(obj_node_mapping_path, "rb") as f:
                simple_object_node_mapping = _RestrictedUnpickler(f).load()
        except pickle.PickleError as err:
            raise ValueError("Objs cannot be loaded.") fromerr
        return simple_object_node_mapping

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SimpleObjectNodeMapping.persist "Permanent link")

```
persist(
    persist_dir:  = DEFAULT_PERSIST_DIR,
    obj_node_mapping_fname:  = DEFAULT_PERSIST_FNAME,
) -> None

```

Persist object node mapping.
NOTE: This may fail depending on whether the object types are pickle-able.
Source code in `llama-index-core/llama_index/core/objects/base_node_mapping.py`  
| 
```
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
```
 | 
```
defpersist(
    self,
    persist_dir: str = DEFAULT_PERSIST_DIR,
    obj_node_mapping_fname: str = DEFAULT_PERSIST_FNAME,
) -> None:
"""
    Persist object node mapping.

    NOTE: This may fail depending on whether the object types are
    pickle-able.
    """
    if not os.path.exists(persist_dir):
        os.makedirs(persist_dir)
    obj_node_mapping_path = concat_dirs(persist_dir, obj_node_mapping_fname)
    try:
        with open(obj_node_mapping_path, "wb") as f:
            pickle.dump(self, f)
    except pickle.PickleError as err:
        raise ValueError("Objs is not pickleable") fromerr

```
 |  
| --- | --- |  
##  SQLTableNodeMapping [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SQLTableNodeMapping "Permanent link")
Bases: `BaseObjectNodeMapping[SQLTableSchema[](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SQLTableSchema "SQLTableSchema \(llama_index.core.objects.table_node_mapping.SQLTableSchema\)")]`
SQL Table node mapping.
Source code in `llama-index-core/llama_index/core/objects/table_node_mapping.py`  
| 
```
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
```
 | 
```
classSQLTableNodeMapping(BaseObjectNodeMapping[SQLTableSchema]):
"""SQL Table node mapping."""

    def__init__(self, sql_database: SQLDatabase) -> None:
        self._sql_database = sql_database

    @classmethod
    deffrom_objects(
        cls,
        objs: Sequence[SQLTableSchema],
        *args: Any,
        sql_database: Optional[SQLDatabase] = None,
        **kwargs: Any,
    ) -> "BaseObjectNodeMapping":
"""Initialize node mapping."""
        if sql_database is None:
            raise ValueError("Must provide sql_database")
        # ignore objs, since we are building from sql_database
        return cls(sql_database)

    def_add_object(self, obj: SQLTableSchema) -> None:
        raise NotImplementedError

    defto_node(self, obj: SQLTableSchema) -> TextNode:
"""To node."""
        # taken from existing schema logic
        table_text = (
            f"Schema of table {obj.table_name}:\n"
            f"{self._sql_database.get_single_table_info(obj.table_name)}\n"
        )

        metadata = {"name": obj.table_name}

        if obj.context_str is not None:
            table_text += f"Context of table {obj.table_name}:\n"
            table_text += obj.context_str
            metadata["context"] = obj.context_str

        table_identity = f"{obj.table_name}{obj.context_str}"

        return TextNode(
            id_=str(uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name=table_identity)),
            text=table_text,
            metadata=metadata,
            excluded_embed_metadata_keys=["name", "context"],
            excluded_llm_metadata_keys=["name", "context"],
        )

    def_from_node(self, node: BaseNode) -> SQLTableSchema:
"""From node."""
        if node.metadata is None:
            raise ValueError("Metadata must be set")
        return SQLTableSchema(
            table_name=node.metadata["name"], context_str=node.metadata.get("context")
        )

    @property
    defobj_node_mapping(self) -> Dict[int, Any]:
"""The mapping data structure between node and object."""
        raise NotImplementedError("Subclasses should implement this!")

    defpersist(
        self, persist_dir: str = ..., obj_node_mapping_fname: str = ...
    ) -> None:
"""Persist objs."""
        raise NotImplementedError("Subclasses should implement this!")

    @classmethod
    deffrom_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        obj_node_mapping_fname: str = DEFAULT_PERSIST_FNAME,
    ) -> "SQLTableNodeMapping":
        raise NotImplementedError(
            "This object node mapping does not support persist method."
        )

```
 |  
| --- | --- |  
###  obj_node_mapping `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SQLTableNodeMapping.obj_node_mapping "Permanent link")

```
obj_node_mapping: [, ]

```

The mapping data structure between node and object.
###  from_objects `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SQLTableNodeMapping.from_objects "Permanent link")

```
from_objects(
    objs: Sequence[],
    *args: ,
    sql_database: Optional[] = None,
    **kwargs: 
) -> BaseObjectNodeMapping

```

Initialize node mapping.
Source code in `llama-index-core/llama_index/core/objects/table_node_mapping.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_objects(
    cls,
    objs: Sequence[SQLTableSchema],
    *args: Any,
    sql_database: Optional[SQLDatabase] = None,
    **kwargs: Any,
) -> "BaseObjectNodeMapping":
"""Initialize node mapping."""
    if sql_database is None:
        raise ValueError("Must provide sql_database")
    # ignore objs, since we are building from sql_database
    return cls(sql_database)

```
 |  
| --- | --- |  
###  to_node [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SQLTableNodeMapping.to_node "Permanent link")

```
to_node(obj: ) -> 

```

To node.
Source code in `llama-index-core/llama_index/core/objects/table_node_mapping.py`  
| 
```
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
```
 | 
```
defto_node(self, obj: SQLTableSchema) -> TextNode:
"""To node."""
    # taken from existing schema logic
    table_text = (
        f"Schema of table {obj.table_name}:\n"
        f"{self._sql_database.get_single_table_info(obj.table_name)}\n"
    )

    metadata = {"name": obj.table_name}

    if obj.context_str is not None:
        table_text += f"Context of table {obj.table_name}:\n"
        table_text += obj.context_str
        metadata["context"] = obj.context_str

    table_identity = f"{obj.table_name}{obj.context_str}"

    return TextNode(
        id_=str(uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name=table_identity)),
        text=table_text,
        metadata=metadata,
        excluded_embed_metadata_keys=["name", "context"],
        excluded_llm_metadata_keys=["name", "context"],
    )

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SQLTableNodeMapping.persist "Permanent link")

```
persist(
    persist_dir:  = ...,
    obj_node_mapping_fname:  = ...,
) -> None

```

Persist objs.
Source code in `llama-index-core/llama_index/core/objects/table_node_mapping.py`  
| 
```
84
85
86
87
88
```
 | 
```
defpersist(
    self, persist_dir: str = ..., obj_node_mapping_fname: str = ...
) -> None:
"""Persist objs."""
    raise NotImplementedError("Subclasses should implement this!")

```
 |  
| --- | --- |  
##  SQLTableSchema [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SQLTableSchema "Permanent link")
Bases: `BaseModel`
Lightweight representation of a SQL table.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `table_name`  |  _required_  |  
|  `context_str`  |  `str | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/objects/table_node_mapping.py`  
| 
```
16
17
18
19
20
```
 | 
```
classSQLTableSchema(BaseModel):
"""Lightweight representation of a SQL table."""

    table_name: str
    context_str: Optional[str] = None

```
 |  
| --- | --- |  
##  SimpleQueryToolNodeMapping [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SimpleQueryToolNodeMapping "Permanent link")
Bases: `BaseQueryToolNodeMapping`
Simple query tool mapping.
Source code in `llama-index-core/llama_index/core/objects/tool_node_mapping.py`  
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
```
 | 
```
classSimpleQueryToolNodeMapping(BaseQueryToolNodeMapping):
"""Simple query tool mapping."""

    def__init__(self, objs: Optional[Sequence[QueryEngineTool]] = None) -> None:
        objs = objs or []
        self._tools = {tool.metadata.name: tool for tool in objs}

    defvalidate_object(self, obj: QueryEngineTool) -> None:
        if not isinstance(obj, QueryEngineTool):
            raise ValueError(f"Object must be of type {QueryEngineTool}")

    @classmethod
    deffrom_objects(
        cls, objs: Sequence[QueryEngineTool], *args: Any, **kwargs: Any
    ) -> "BaseObjectNodeMapping":
        return cls(objs)

    def_add_object(self, tool: QueryEngineTool) -> None:
        if tool.metadata.name is None:
            raise ValueError("Tool name must be set")
        self._tools[tool.metadata.name] = tool

    defto_node(self, obj: QueryEngineTool) -> TextNode:
"""To node."""
        return convert_tool_to_node(obj)

    def_from_node(self, node: BaseNode) -> QueryEngineTool:
"""From node."""
        if node.metadata is None:
            raise ValueError("Metadata must be set")
        return self._tools[node.metadata["name"]]

```
 |  
| --- | --- |  
###  to_node [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SimpleQueryToolNodeMapping.to_node "Permanent link")

```
to_node(obj: ) -> 

```

To node.
Source code in `llama-index-core/llama_index/core/objects/tool_node_mapping.py`  
| 
```
146
147
148
```
 | 
```
defto_node(self, obj: QueryEngineTool) -> TextNode:
"""To node."""
    return convert_tool_to_node(obj)

```
 |  
| --- | --- |  
##  SimpleToolNodeMapping [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SimpleToolNodeMapping "Permanent link")
Bases: `BaseToolNodeMapping`
Simple Tool mapping.
In this setup, we assume that the tool name is unique, and that the list of all tools are stored in memory.
Source code in `llama-index-core/llama_index/core/objects/tool_node_mapping.py`  
| 
```
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
```
 | 
```
classSimpleToolNodeMapping(BaseToolNodeMapping):
"""
    Simple Tool mapping.

    In this setup, we assume that the tool name is unique, and
    that the list of all tools are stored in memory.

    """

    def__init__(self, objs: Optional[Sequence[BaseTool]] = None) -> None:
        objs = objs or []
        self._tools = {tool.metadata.name: tool for tool in objs}

    @classmethod
    deffrom_objects(
        cls, objs: Sequence[BaseTool], *args: Any, **kwargs: Any
    ) -> "BaseObjectNodeMapping":
        return cls(objs)

    def_add_object(self, tool: BaseTool) -> None:
        self._tools[tool.metadata.name] = tool

    defto_node(self, tool: BaseTool) -> TextNode:
"""To node."""
        return convert_tool_to_node(tool)

    def_from_node(self, node: BaseNode) -> BaseTool:
"""From node."""
        if node.metadata is None:
            raise ValueError("Metadata must be set")
        return self._tools[node.metadata["name"]]

```
 |  
| --- | --- |  
###  to_node [#](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SimpleToolNodeMapping.to_node "Permanent link")

```
to_node(tool: ) -> 

```

To node.
Source code in `llama-index-core/llama_index/core/objects/tool_node_mapping.py`  
| 
```
88
89
90
```
 | 
```
defto_node(self, tool: BaseTool) -> TextNode:
"""To node."""
    return convert_tool_to_node(tool)

```
 |  
| --- | --- |
