# Simple
##  SimpleDocumentStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.SimpleDocumentStore "Permanent link")
Bases: `KVDocumentStore`
Simple Document (Node) store.
An in-memory store for Document and Node objects.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `simple_kvstore`  |   |  simple key-value store  |  `None`  |  
|  `namespace`  |  namespace for the docstore  |  `None`  |  
Source code in `llama-index-core/llama_index/core/storage/docstore/simple_docstore.py`  
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
```
 | 
```
classSimpleDocumentStore(KVDocumentStore):
"""
    Simple Document (Node) store.

    An in-memory store for Document and Node objects.

    Args:
        simple_kvstore (SimpleKVStore): simple key-value store
        namespace (str): namespace for the docstore

    """

    def__init__(
        self,
        simple_kvstore: Optional[SimpleKVStore] = None,
        namespace: Optional[str] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""Init a SimpleDocumentStore."""
        simple_kvstore = simple_kvstore or SimpleKVStore()
        super().__init__(simple_kvstore, namespace=namespace, batch_size=batch_size)

    @classmethod
    deffrom_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        namespace: Optional[str] = None,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "SimpleDocumentStore":
"""
        Create a SimpleDocumentStore from a persist directory.

        Args:
            persist_dir (str): directory to persist the store
            namespace (Optional[str]): namespace for the docstore
            fs (Optional[fsspec.AbstractFileSystem]): filesystem to use

        """
        if fs is not None:
            persist_path = concat_dirs(persist_dir, DEFAULT_PERSIST_FNAME)
        else:
            persist_path = os.path.join(persist_dir, DEFAULT_PERSIST_FNAME)
        return cls.from_persist_path(persist_path, namespace=namespace, fs=fs)

    @classmethod
    deffrom_persist_path(
        cls,
        persist_path: str,
        namespace: Optional[str] = None,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "SimpleDocumentStore":
"""
        Create a SimpleDocumentStore from a persist path.

        Args:
            persist_path (str): Path to persist the store
            namespace (Optional[str]): namespace for the docstore
            fs (
            Optional[fsspec.AbstractFileSystem]): filesystem to use

        """
        simple_kvstore = SimpleKVStore.from_persist_path(persist_path, fs=fs)
        return cls(simple_kvstore, namespace)

    defpersist(
        self,
        persist_path: str = DEFAULT_PERSIST_PATH,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> None:
"""Persist the store."""
        if isinstance(self._kvstore, (MutableMappingKVStore, BaseInMemoryKVStore)):
            self._kvstore.persist(persist_path, fs=fs)

    @classmethod
    deffrom_dict(
        cls, save_dict: dict, namespace: Optional[str] = None
    ) -> "SimpleDocumentStore":
        simple_kvstore = SimpleKVStore.from_dict(save_dict)
        return cls(simple_kvstore, namespace)

    defto_dict(self) -> dict:
        assert isinstance(self._kvstore, SimpleKVStore)
        return self._kvstore.to_dict()

```
 |  
| --- | --- |  
###  from_persist_dir `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.SimpleDocumentStore.from_persist_dir "Permanent link")

```
from_persist_dir(
    persist_dir:  = DEFAULT_PERSIST_DIR,
    namespace: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> 

```

Create a SimpleDocumentStore from a persist directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `persist_dir`  |  directory to persist the store  |  `DEFAULT_PERSIST_DIR`  |  
|  `namespace`  |  `Optional[str]`  |  namespace for the docstore  |  `None`  |  
|  `Optional[AbstractFileSystem]`  |  filesystem to use  |  `None`  |  
Source code in `llama-index-core/llama_index/core/storage/docstore/simple_docstore.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_persist_dir(
    cls,
    persist_dir: str = DEFAULT_PERSIST_DIR,
    namespace: Optional[str] = None,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> "SimpleDocumentStore":
"""
    Create a SimpleDocumentStore from a persist directory.

    Args:
        persist_dir (str): directory to persist the store
        namespace (Optional[str]): namespace for the docstore
        fs (Optional[fsspec.AbstractFileSystem]): filesystem to use

    """
    if fs is not None:
        persist_path = concat_dirs(persist_dir, DEFAULT_PERSIST_FNAME)
    else:
        persist_path = os.path.join(persist_dir, DEFAULT_PERSIST_FNAME)
    return cls.from_persist_path(persist_path, namespace=namespace, fs=fs)

```
 |  
| --- | --- |  
###  from_persist_path `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.SimpleDocumentStore.from_persist_path "Permanent link")

```
from_persist_path(
    persist_path: ,
    namespace: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> 

```

Create a SimpleDocumentStore from a persist path.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `persist_path`  |  Path to persist the store  |  _required_  |  
|  `namespace`  |  `Optional[str]`  |  namespace for the docstore  |  `None`  |  
|  `Optional[fsspec.AbstractFileSystem])`  |  filesystem to use  |  _required_  |  
Source code in `llama-index-core/llama_index/core/storage/docstore/simple_docstore.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_persist_path(
    cls,
    persist_path: str,
    namespace: Optional[str] = None,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> "SimpleDocumentStore":
"""
    Create a SimpleDocumentStore from a persist path.

    Args:
        persist_path (str): Path to persist the store
        namespace (Optional[str]): namespace for the docstore
        fs (
        Optional[fsspec.AbstractFileSystem]): filesystem to use

    """
    simple_kvstore = SimpleKVStore.from_persist_path(persist_path, fs=fs)
    return cls(simple_kvstore, namespace)

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.SimpleDocumentStore.persist "Permanent link")

```
persist(
    persist_path:  = DEFAULT_PERSIST_PATH,
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persist the store.
Source code in `llama-index-core/llama_index/core/storage/docstore/simple_docstore.py`  
| 
```
84
85
86
87
88
89
90
91
```
 | 
```
defpersist(
    self,
    persist_path: str = DEFAULT_PERSIST_PATH,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> None:
"""Persist the store."""
    if isinstance(self._kvstore, (MutableMappingKVStore, BaseInMemoryKVStore)):
        self._kvstore.persist(persist_path, fs=fs)

```
 |  
| --- | --- |  
##  BaseDocumentStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
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
```
 | 
```
classBaseDocumentStore(ABC):
    # ===== Save/load =====
    defpersist(
        self,
        persist_path: str = DEFAULT_PERSIST_PATH,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> None:
"""Persist the docstore to a file."""

    # ===== Main interface =====
    @property
    @abstractmethod
    defdocs(self) -> Dict[str, BaseNode]: ...

    @abstractmethod
    defadd_documents(
        self,
        docs: Sequence[BaseNode],
        allow_update: bool = True,
        batch_size: int = DEFAULT_BATCH_SIZE,
        store_text: bool = True,
    ) -> None: ...

    @abstractmethod
    async defasync_add_documents(
        self,
        docs: Sequence[BaseNode],
        allow_update: bool = True,
        batch_size: int = DEFAULT_BATCH_SIZE,
        store_text: bool = True,
    ) -> None: ...

    @abstractmethod
    defget_document(
        self, doc_id: str, raise_error: bool = True
    ) -> Optional[BaseNode]: ...

    @abstractmethod
    async defaget_document(
        self, doc_id: str, raise_error: bool = True
    ) -> Optional[BaseNode]: ...

    @abstractmethod
    defdelete_document(self, doc_id: str, raise_error: bool = True) -> None:
"""Delete a document from the store."""
        ...

    @abstractmethod
    async defadelete_document(self, doc_id: str, raise_error: bool = True) -> None:
"""Delete a document from the store."""
        ...

    @abstractmethod
    defdocument_exists(self, doc_id: str) -> bool: ...

    @abstractmethod
    async defadocument_exists(self, doc_id: str) -> bool: ...

    # ===== Hash =====
    @abstractmethod
    defset_document_hash(self, doc_id: str, doc_hash: str) -> None: ...

    @abstractmethod
    async defaset_document_hash(self, doc_id: str, doc_hash: str) -> None: ...

    @abstractmethod
    defset_document_hashes(self, doc_hashes: Dict[str, str]) -> None: ...

    @abstractmethod
    async defaset_document_hashes(self, doc_hashes: Dict[str, str]) -> None: ...

    @abstractmethod
    defget_document_hash(self, doc_id: str) -> Optional[str]: ...

    @abstractmethod
    async defaget_document_hash(self, doc_id: str) -> Optional[str]: ...

    @abstractmethod
    defget_all_document_hashes(self) -> Dict[str, str]: ...

    @abstractmethod
    async defaget_all_document_hashes(self) -> Dict[str, str]: ...

    # ==== Ref Docs =====
    @abstractmethod
    defget_all_ref_doc_info(self) -> Optional[Dict[str, RefDocInfo]]:
"""Get a mapping of ref_doc_id -> RefDocInfo for all ingested documents."""

    @abstractmethod
    async defaget_all_ref_doc_info(self) -> Optional[Dict[str, RefDocInfo]]:
"""Get a mapping of ref_doc_id -> RefDocInfo for all ingested documents."""

    @abstractmethod
    defget_ref_doc_info(self, ref_doc_id: str) -> Optional[RefDocInfo]:
"""Get the RefDocInfo for a given ref_doc_id."""

    @abstractmethod
    async defaget_ref_doc_info(self, ref_doc_id: str) -> Optional[RefDocInfo]:
"""Get the RefDocInfo for a given ref_doc_id."""

    @abstractmethod
    defdelete_ref_doc(self, ref_doc_id: str, raise_error: bool = True) -> None:
"""Delete a ref_doc and all it's associated nodes."""

    @abstractmethod
    async defadelete_ref_doc(self, ref_doc_id: str, raise_error: bool = True) -> None:
"""Delete a ref_doc and all it's associated nodes."""

    # ===== Nodes =====
    defget_nodes(
        self, node_ids: List[str], raise_error: bool = True
    ) -> List[BaseNode]:
"""
        Get nodes from docstore.

        Args:
            node_ids (List[str]): node ids
            raise_error (bool): raise error if node_id not found

        """
        nodes: list[BaseNode] = []

        for node_id in node_ids:
            # if needed for type checking
            if not raise_error:
                if node := self.get_node(node_id=node_id, raise_error=False):
                    nodes.append(node)
                continue

            nodes.append(self.get_node(node_id=node_id, raise_error=True))

        return nodes

    async defaget_nodes(
        self, node_ids: List[str], raise_error: bool = True
    ) -> List[BaseNode]:
"""
        Get nodes from docstore.

        Args:
            node_ids (List[str]): node ids
            raise_error (bool): raise error if node_id not found

        """
        nodes: list[BaseNode] = []

        for node_id in node_ids:
            # if needed for type checking
            if not raise_error:
                if node := await self.aget_node(node_id=node_id, raise_error=False):
                    nodes.append(node)
                continue

            nodes.append(await self.aget_node(node_id=node_id, raise_error=True))

        return nodes

    @overload
    defget_node(self, node_id: str, raise_error: Literal[True] = True) -> BaseNode: ...

    @overload
    defget_node(
        self, node_id: str, raise_error: Literal[False] = False
    ) -> Optional[BaseNode]: ...

    defget_node(self, node_id: str, raise_error: bool = True) -> Optional[BaseNode]:
"""
        Get node from docstore.

        Args:
            node_id (str): node id
            raise_error (bool): raise error if node_id not found

        """
        doc = self.get_document(node_id, raise_error=raise_error)

        if doc is None:
            # The doc store should have raised an error if the node_id is not found, but it didn't
            # so we raise an error here
            if raise_error:
                raise ValueError(f"Node {node_id} not found")
            return None

        # The document should always be a BaseNode, but we check to be safe
        if not isinstance(doc, BaseNode):
            raise ValueError(f"Document {node_id} is not a Node.")

        return doc

    @overload
    async defaget_node(
        self, node_id: str, raise_error: Literal[True] = True
    ) -> BaseNode: ...

    @overload
    async defaget_node(
        self, node_id: str, raise_error: Literal[False] = False
    ) -> Optional[BaseNode]: ...

    async defaget_node(
        self, node_id: str, raise_error: bool = True
    ) -> Optional[BaseNode]:
"""
        Get node from docstore.

        Args:
            node_id (str): node id
            raise_error (bool): raise error if node_id not found

        """
        doc = await self.aget_document(node_id, raise_error=raise_error)

        if doc is None:
            # The doc store should have raised an error if the node_id is not found, but it didn't
            # so we raise an error here
            if raise_error:
                raise ValueError(f"Node {node_id} not found")
            return None

        # The document should always be a BaseNode, but we check to be safe
        if not isinstance(doc, BaseNode):
            raise ValueError(f"Document {node_id} is not a Node.")

        return doc

    defget_node_dict(self, node_id_dict: Dict[int, str]) -> Dict[int, BaseNode]:
"""
        Get node dict from docstore given a mapping of index to node ids.

        Args:
            node_id_dict (Dict[int, str]): mapping of index to node ids

        """
        return {
            index: self.get_node(node_id) for index, node_id in node_id_dict.items()
        }

    async defaget_node_dict(self, node_id_dict: Dict[int, str]) -> Dict[int, BaseNode]:
"""
        Get node dict from docstore given a mapping of index to node ids.

        Args:
            node_id_dict (Dict[int, str]): mapping of index to node ids

        """
        return {
            index: await self.aget_node(node_id)
            for index, node_id in node_id_dict.items()
        }

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.persist "Permanent link")

```
persist(
    persist_path:  = DEFAULT_PERSIST_PATH,
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persist the docstore to a file.
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
26
27
28
29
30
31
```
 | 
```
defpersist(
    self,
    persist_path: str = DEFAULT_PERSIST_PATH,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> None:
"""Persist the docstore to a file."""

```
 |  
| --- | --- |  
###  delete_document `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.delete_document "Permanent link")

```
delete_document(
    doc_id: , raise_error:  = True
) -> None

```

Delete a document from the store.
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
66
67
68
69
```
 | 
```
@abstractmethod
defdelete_document(self, doc_id: str, raise_error: bool = True) -> None:
"""Delete a document from the store."""
    ...

```
 |  
| --- | --- |  
###  adelete_document `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.adelete_document "Permanent link")

```
adelete_document(
    doc_id: , raise_error:  = True
) -> None

```

Delete a document from the store.
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
71
72
73
74
```
 | 
```
@abstractmethod
async defadelete_document(self, doc_id: str, raise_error: bool = True) -> None:
"""Delete a document from the store."""
    ...

```
 |  
| --- | --- |  
###  get_all_ref_doc_info `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.get_all_ref_doc_info "Permanent link")

```
get_all_ref_doc_info() -> Optional[[, ]]

```

Get a mapping of ref_doc_id -> RefDocInfo for all ingested documents.
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
108
109
110
```
 | 
```
@abstractmethod
defget_all_ref_doc_info(self) -> Optional[Dict[str, RefDocInfo]]:
"""Get a mapping of ref_doc_id -> RefDocInfo for all ingested documents."""

```
 |  
| --- | --- |  
###  aget_all_ref_doc_info `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.aget_all_ref_doc_info "Permanent link")

```
aget_all_ref_doc_info() -> Optional[[, ]]

```

Get a mapping of ref_doc_id -> RefDocInfo for all ingested documents.
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
112
113
114
```
 | 
```
@abstractmethod
async defaget_all_ref_doc_info(self) -> Optional[Dict[str, RefDocInfo]]:
"""Get a mapping of ref_doc_id -> RefDocInfo for all ingested documents."""

```
 |  
| --- | --- |  
###  get_ref_doc_info `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.get_ref_doc_info "Permanent link")

```
get_ref_doc_info(ref_doc_id: ) -> Optional[]

```

Get the RefDocInfo for a given ref_doc_id.
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
116
117
118
```
 | 
```
@abstractmethod
defget_ref_doc_info(self, ref_doc_id: str) -> Optional[RefDocInfo]:
"""Get the RefDocInfo for a given ref_doc_id."""

```
 |  
| --- | --- |  
###  aget_ref_doc_info `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.aget_ref_doc_info "Permanent link")

```
aget_ref_doc_info(ref_doc_id: ) -> Optional[]

```

Get the RefDocInfo for a given ref_doc_id.
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
120
121
122
```
 | 
```
@abstractmethod
async defaget_ref_doc_info(self, ref_doc_id: str) -> Optional[RefDocInfo]:
"""Get the RefDocInfo for a given ref_doc_id."""

```
 |  
| --- | --- |  
###  delete_ref_doc `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.delete_ref_doc "Permanent link")

```
delete_ref_doc(
    ref_doc_id: , raise_error:  = True
) -> None

```

Delete a ref_doc and all it's associated nodes.
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
124
125
126
```
 | 
```
@abstractmethod
defdelete_ref_doc(self, ref_doc_id: str, raise_error: bool = True) -> None:
"""Delete a ref_doc and all it's associated nodes."""

```
 |  
| --- | --- |  
###  adelete_ref_doc `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.adelete_ref_doc "Permanent link")

```
adelete_ref_doc(
    ref_doc_id: , raise_error:  = True
) -> None

```

Delete a ref_doc and all it's associated nodes.
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
128
129
130
```
 | 
```
@abstractmethod
async defadelete_ref_doc(self, ref_doc_id: str, raise_error: bool = True) -> None:
"""Delete a ref_doc and all it's associated nodes."""

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: [], raise_error:  = True
) -> []

```

Get nodes from docstore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `List[str]`  |  node ids  |  _required_  |  
|  `raise_error`  |  `bool`  |  raise error if node_id not found  |  `True`  |  
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
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
```
 | 
```
defget_nodes(
    self, node_ids: List[str], raise_error: bool = True
) -> List[BaseNode]:
"""
    Get nodes from docstore.

    Args:
        node_ids (List[str]): node ids
        raise_error (bool): raise error if node_id not found

    """
    nodes: list[BaseNode] = []

    for node_id in node_ids:
        # if needed for type checking
        if not raise_error:
            if node := self.get_node(node_id=node_id, raise_error=False):
                nodes.append(node)
            continue

        nodes.append(self.get_node(node_id=node_id, raise_error=True))

    return nodes

```
 |  
| --- | --- |  
###  aget_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.aget_nodes "Permanent link")

```
aget_nodes(
    node_ids: [], raise_error:  = True
) -> []

```

Get nodes from docstore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `List[str]`  |  node ids  |  _required_  |  
|  `raise_error`  |  `bool`  |  raise error if node_id not found  |  `True`  |  
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
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
```
 | 
```
async defaget_nodes(
    self, node_ids: List[str], raise_error: bool = True
) -> List[BaseNode]:
"""
    Get nodes from docstore.

    Args:
        node_ids (List[str]): node ids
        raise_error (bool): raise error if node_id not found

    """
    nodes: list[BaseNode] = []

    for node_id in node_ids:
        # if needed for type checking
        if not raise_error:
            if node := await self.aget_node(node_id=node_id, raise_error=False):
                nodes.append(node)
            continue

        nodes.append(await self.aget_node(node_id=node_id, raise_error=True))

    return nodes

```
 |  
| --- | --- |  
###  get_node [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.get_node "Permanent link")

```
get_node(
    node_id: , raise_error: Literal[True] = True
) -> 

```


```
get_node(
    node_id: , raise_error: Literal[False] = False
) -> Optional[]

```


```
get_node(
    node_id: , raise_error:  = True
) -> Optional[]

```

Get node from docstore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_id`  |  node id  |  _required_  |  
|  `raise_error`  |  `bool`  |  raise error if node_id not found  |  `True`  |  
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
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
208
209
210
211
```
 | 
```
defget_node(self, node_id: str, raise_error: bool = True) -> Optional[BaseNode]:
"""
    Get node from docstore.

    Args:
        node_id (str): node id
        raise_error (bool): raise error if node_id not found

    """
    doc = self.get_document(node_id, raise_error=raise_error)

    if doc is None:
        # The doc store should have raised an error if the node_id is not found, but it didn't
        # so we raise an error here
        if raise_error:
            raise ValueError(f"Node {node_id} not found")
        return None

    # The document should always be a BaseNode, but we check to be safe
    if not isinstance(doc, BaseNode):
        raise ValueError(f"Document {node_id} is not a Node.")

    return doc

```
 |  
| --- | --- |  
###  aget_node [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.aget_node "Permanent link")

```
aget_node(
    node_id: , raise_error: Literal[True] = True
) -> 

```


```
aget_node(
    node_id: , raise_error: Literal[False] = False
) -> Optional[]

```


```
aget_node(
    node_id: , raise_error:  = True
) -> Optional[]

```

Get node from docstore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_id`  |  node id  |  _required_  |  
|  `raise_error`  |  `bool`  |  raise error if node_id not found  |  `True`  |  
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
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
```
 | 
```
async defaget_node(
    self, node_id: str, raise_error: bool = True
) -> Optional[BaseNode]:
"""
    Get node from docstore.

    Args:
        node_id (str): node id
        raise_error (bool): raise error if node_id not found

    """
    doc = await self.aget_document(node_id, raise_error=raise_error)

    if doc is None:
        # The doc store should have raised an error if the node_id is not found, but it didn't
        # so we raise an error here
        if raise_error:
            raise ValueError(f"Node {node_id} not found")
        return None

    # The document should always be a BaseNode, but we check to be safe
    if not isinstance(doc, BaseNode):
        raise ValueError(f"Document {node_id} is not a Node.")

    return doc

```
 |  
| --- | --- |  
###  get_node_dict [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.get_node_dict "Permanent link")

```
get_node_dict(
    node_id_dict: [, ]
) -> [, ]

```

Get node dict from docstore given a mapping of index to node ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_id_dict`  |  `Dict[int, str]`  |  mapping of index to node ids  |  _required_  |  
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
| 
```
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
```
 | 
```
defget_node_dict(self, node_id_dict: Dict[int, str]) -> Dict[int, BaseNode]:
"""
    Get node dict from docstore given a mapping of index to node ids.

    Args:
        node_id_dict (Dict[int, str]): mapping of index to node ids

    """
    return {
        index: self.get_node(node_id) for index, node_id in node_id_dict.items()
    }

```
 |  
| --- | --- |  
###  aget_node_dict [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore.aget_node_dict "Permanent link")

```
aget_node_dict(
    node_id_dict: [, ]
) -> [, ]

```

Get node dict from docstore given a mapping of index to node ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_id_dict`  |  `Dict[int, str]`  |  mapping of index to node ids  |  _required_  |  
Source code in `llama-index-core/llama_index/core/storage/docstore/types.py`  
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
```
 | 
```
async defaget_node_dict(self, node_id_dict: Dict[int, str]) -> Dict[int, BaseNode]:
"""
    Get node dict from docstore given a mapping of index to node ids.

    Args:
        node_id_dict (Dict[int, str]): mapping of index to node ids

    """
    return {
        index: await self.aget_node(node_id)
        for index, node_id in node_id_dict.items()
    }

```
 |  
| --- | --- |  
options: members: - SimpleDocumentStore
