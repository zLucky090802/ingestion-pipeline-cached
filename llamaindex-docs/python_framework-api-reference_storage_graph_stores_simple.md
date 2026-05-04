# Simple
Simple graph store index.
##  SimpleGraphStoreData `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStoreData "Permanent link")
Bases: `DataClassJsonMixin`
Simple Graph Store Data container.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `graph_dict`  |  `Dict[str, List[List[str]]]`  |  dict mapping subject to  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/graph_stores/simple.py`  
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
```
 | 
```
@dataclass
classSimpleGraphStoreData(DataClassJsonMixin):
"""
    Simple Graph Store Data container.

    Args:
        graph_dict (Optional[dict]): dict mapping subject to

    """

    graph_dict: Dict[str, List[List[str]]] = field(default_factory=dict)

    defget_rel_map(
        self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
    ) -> Dict[str, List[List[str]]]:
"""Get subjects' rel map in max depth."""
        if subjs is None:
            subjs = list(self.graph_dict.keys())
        rel_map = {}
        for subj in subjs:
            rel_map[subj] = self._get_rel_map(subj, depth=depth, limit=limit)
        # TBD, truncate the rel_map in a spread way, now just truncate based
        # on iteration order
        rel_count = 0
        return_map = {}
        for subj in rel_map:
            if rel_count + len(rel_map[subj])  limit:
                return_map[subj] = rel_map[subj][: limit - rel_count]
                break
            else:
                return_map[subj] = rel_map[subj]
                rel_count += len(rel_map[subj])
        return return_map

    def_get_rel_map(
        self, subj: str, depth: int = 2, limit: int = 30
    ) -> List[List[str]]:
"""Get one subect's rel map in max depth."""
        if depth == 0:
            return []
        rel_map = []
        rel_count = 0
        if subj in self.graph_dict:
            for rel, obj in self.graph_dict[subj]:
                if rel_count >= limit:
                    break
                rel_map.append([subj, rel, obj])
                rel_map += self._get_rel_map(obj, depth=depth - 1)
                rel_count += 1
        return rel_map

```
 |  
| --- | --- |  
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStoreData.get_rel_map "Permanent link")

```
get_rel_map(
    subjs: Optional[[]] = None,
    depth:  = 2,
    limit:  = 30,
) -> [, [[]]]

```

Get subjects' rel map in max depth.
Source code in `llama-index-core/llama_index/core/graph_stores/simple.py`  
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
48
49
50
51
52
```
 | 
```
defget_rel_map(
    self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
) -> Dict[str, List[List[str]]]:
"""Get subjects' rel map in max depth."""
    if subjs is None:
        subjs = list(self.graph_dict.keys())
    rel_map = {}
    for subj in subjs:
        rel_map[subj] = self._get_rel_map(subj, depth=depth, limit=limit)
    # TBD, truncate the rel_map in a spread way, now just truncate based
    # on iteration order
    rel_count = 0
    return_map = {}
    for subj in rel_map:
        if rel_count + len(rel_map[subj])  limit:
            return_map[subj] = rel_map[subj][: limit - rel_count]
            break
        else:
            return_map[subj] = rel_map[subj]
            rel_count += len(rel_map[subj])
    return return_map

```
 |  
| --- | --- |  
##  SimpleGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStore "Permanent link")
Bases: 
Simple Graph Store.
In this graph store, triplets are stored within a simple, in-memory dictionary.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `simple_graph_store_data_dict`  |  `Optional[dict]`  |  data dict containing the triplets. See SimpleGraphStoreData for more details.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/graph_stores/simple.py`  
| 
```
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
```
 | 
```
classSimpleGraphStore(GraphStore):
"""
    Simple Graph Store.

    In this graph store, triplets are stored within a simple, in-memory dictionary.

    Args:
        simple_graph_store_data_dict (Optional[dict]): data dict
            containing the triplets. See SimpleGraphStoreData
            for more details.

    """

    def__init__(
        self,
        data: Optional[SimpleGraphStoreData] = None,
        fs: Optional[fsspec.AbstractFileSystem] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._data = data or SimpleGraphStoreData()
        self._fs = fs or fsspec.filesystem("file")

    @classmethod
    deffrom_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "SimpleGraphStore":
"""Load from persist dir."""
        persist_path = os.path.join(persist_dir, DEFAULT_PERSIST_FNAME)
        return cls.from_persist_path(persist_path, fs=fs)

    @property
    defclient(self) -> None:
"""
        Get client.
        Not applicable for this store.
        """
        return

    defget(self, subj: str) -> List[List[str]]:
"""Get triplets."""
        return self._data.graph_dict.get(subj, [])

    defget_rel_map(
        self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
    ) -> Dict[str, List[List[str]]]:
"""Get depth-aware rel map."""
        return self._data.get_rel_map(subjs=subjs, depth=depth, limit=limit)

    defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
        if subj not in self._data.graph_dict:
            self._data.graph_dict[subj] = []
        existing = self._data.graph_dict[subj]
        if (rel, obj) not in map(tuple, existing):
            existing.append([rel, obj])

    defdelete(self, subj: str, rel: str, obj: str) -> None:
"""Delete triplet."""
        if subj in self._data.graph_dict:
            if (rel, obj) in self._data.graph_dict[subj]:
                self._data.graph_dict[subj].remove([rel, obj])
                if len(self._data.graph_dict[subj]) == 0:
                    del self._data.graph_dict[subj]

    defpersist(
        self,
        persist_path: str = os.path.join(DEFAULT_PERSIST_DIR, DEFAULT_PERSIST_FNAME),
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> None:
"""Persist the SimpleGraphStore to a directory."""
        fs = fs or self._fs
        dirpath = os.path.dirname(persist_path)
        if not fs.exists(dirpath):
            fs.makedirs(dirpath)

        with fs.open(persist_path, "w") as f:
            json.dump(self._data.to_dict(), f)

    defget_schema(self, refresh: bool = False) -> str:
"""Get the schema of the Simple Graph store."""
        raise NotImplementedError("SimpleGraphStore does not support get_schema")

    defquery(self, query: str, param_map: Optional[Dict[str, Any]] = {}) -> Any:
"""Query the Simple Graph store."""
        raise NotImplementedError("SimpleGraphStore does not support query")

    @classmethod
    deffrom_persist_path(
        cls, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
    ) -> "SimpleGraphStore":
"""Create a SimpleGraphStore from a persist directory."""
        fs = fs or fsspec.filesystem("file")
        if not fs.exists(persist_path):
            logger.warning(
                f"No existing {__name__} found at {persist_path}. "
                "Initializing a new graph_store from scratch. "
            )
            return cls()

        logger.debug(f"Loading {__name__} from {persist_path}.")
        with fs.open(persist_path, "rb") as f:
            data_dict = json.load(f)
            data = SimpleGraphStoreData.from_dict(data_dict)
        return cls(data)

    @classmethod
    deffrom_dict(cls, save_dict: dict) -> "SimpleGraphStore":
        data = SimpleGraphStoreData.from_dict(save_dict)
        return cls(data)

    defto_dict(self) -> dict:
        return self._data.to_dict()

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStore.client "Permanent link")

```
client: None

```

Get client. Not applicable for this store.
###  from_persist_dir `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStore.from_persist_dir "Permanent link")

```
from_persist_dir(
    persist_dir:  = DEFAULT_PERSIST_DIR,
    fs: Optional[AbstractFileSystem] = None,
) -> 

```

Load from persist dir.
Source code in `llama-index-core/llama_index/core/graph_stores/simple.py`  
| 
```
 95
 96
 97
 98
 99
100
101
102
103
```
 | 
```
@classmethod
deffrom_persist_dir(
    cls,
    persist_dir: str = DEFAULT_PERSIST_DIR,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> "SimpleGraphStore":
"""Load from persist dir."""
    persist_path = os.path.join(persist_dir, DEFAULT_PERSIST_FNAME)
    return cls.from_persist_path(persist_path, fs=fs)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStore.get "Permanent link")

```
get(subj: ) -> [[]]

```

Get triplets.
Source code in `llama-index-core/llama_index/core/graph_stores/simple.py`  
| 
```
113
114
115
```
 | 
```
defget(self, subj: str) -> List[List[str]]:
"""Get triplets."""
    return self._data.graph_dict.get(subj, [])

```
 |  
| --- | --- |  
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    subjs: Optional[[]] = None,
    depth:  = 2,
    limit:  = 30,
) -> [, [[]]]

```

Get depth-aware rel map.
Source code in `llama-index-core/llama_index/core/graph_stores/simple.py`  
| 
```
117
118
119
120
121
```
 | 
```
defget_rel_map(
    self, subjs: Optional[List[str]] = None, depth: int = 2, limit: int = 30
) -> Dict[str, List[List[str]]]:
"""Get depth-aware rel map."""
    return self._data.get_rel_map(subjs=subjs, depth=depth, limit=limit)

```
 |  
| --- | --- |  
###  upsert_triplet [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStore.upsert_triplet "Permanent link")

```
upsert_triplet(subj: , rel: , obj: ) -> None

```

Add triplet.
Source code in `llama-index-core/llama_index/core/graph_stores/simple.py`  
| 
```
123
124
125
126
127
128
129
```
 | 
```
defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
    if subj not in self._data.graph_dict:
        self._data.graph_dict[subj] = []
    existing = self._data.graph_dict[subj]
    if (rel, obj) not in map(tuple, existing):
        existing.append([rel, obj])

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStore.delete "Permanent link")

```
delete(subj: , rel: , obj: ) -> None

```

Delete triplet.
Source code in `llama-index-core/llama_index/core/graph_stores/simple.py`  
| 
```
131
132
133
134
135
136
137
```
 | 
```
defdelete(self, subj: str, rel: str, obj: str) -> None:
"""Delete triplet."""
    if subj in self._data.graph_dict:
        if (rel, obj) in self._data.graph_dict[subj]:
            self._data.graph_dict[subj].remove([rel, obj])
            if len(self._data.graph_dict[subj]) == 0:
                del self._data.graph_dict[subj]

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStore.persist "Permanent link")

```
persist(
    persist_path:  = (
        DEFAULT_PERSIST_DIR, DEFAULT_PERSIST_FNAME
    ),
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persist the SimpleGraphStore to a directory.
Source code in `llama-index-core/llama_index/core/graph_stores/simple.py`  
| 
```
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
defpersist(
    self,
    persist_path: str = os.path.join(DEFAULT_PERSIST_DIR, DEFAULT_PERSIST_FNAME),
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> None:
"""Persist the SimpleGraphStore to a directory."""
    fs = fs or self._fs
    dirpath = os.path.dirname(persist_path)
    if not fs.exists(dirpath):
        fs.makedirs(dirpath)

    with fs.open(persist_path, "w") as f:
        json.dump(self._data.to_dict(), f)

```
 |  
| --- | --- |  
###  get_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStore.get_schema "Permanent link")

```
get_schema(refresh:  = False) -> 

```

Get the schema of the Simple Graph store.
Source code in `llama-index-core/llama_index/core/graph_stores/simple.py`  
| 
```
153
154
155
```
 | 
```
defget_schema(self, refresh: bool = False) -> str:
"""Get the schema of the Simple Graph store."""
    raise NotImplementedError("SimpleGraphStore does not support get_schema")

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStore.query "Permanent link")

```
query(
    query: , param_map: Optional[[, ]] = {}
) -> 

```

Query the Simple Graph store.
Source code in `llama-index-core/llama_index/core/graph_stores/simple.py`  
| 
```
157
158
159
```
 | 
```
defquery(self, query: str, param_map: Optional[Dict[str, Any]] = {}) -> Any:
"""Query the Simple Graph store."""
    raise NotImplementedError("SimpleGraphStore does not support query")

```
 |  
| --- | --- |  
###  from_persist_path `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/simple/#llama_index.core.graph_stores.simple.SimpleGraphStore.from_persist_path "Permanent link")

```
from_persist_path(
    persist_path: ,
    fs: Optional[AbstractFileSystem] = None,
) -> 

```

Create a SimpleGraphStore from a persist directory.
Source code in `llama-index-core/llama_index/core/graph_stores/simple.py`  
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
177
178
```
 | 
```
@classmethod
deffrom_persist_path(
    cls, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
) -> "SimpleGraphStore":
"""Create a SimpleGraphStore from a persist directory."""
    fs = fs or fsspec.filesystem("file")
    if not fs.exists(persist_path):
        logger.warning(
            f"No existing {__name__} found at {persist_path}. "
            "Initializing a new graph_store from scratch. "
        )
        return cls()

    logger.debug(f"Loading {__name__} from {persist_path}.")
    with fs.open(persist_path, "rb") as f:
        data_dict = json.load(f)
        data = SimpleGraphStoreData.from_dict(data_dict)
    return cls(data)

```
 |  
| --- | --- |  
options: members: - SimpleGraphStore - SimplePropertyGraphStore
