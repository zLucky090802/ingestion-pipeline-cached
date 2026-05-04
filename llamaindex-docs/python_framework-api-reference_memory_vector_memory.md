# Vector memory
Vector memory.
Memory backed by a vector database.
##  VectorMemory [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/vector_memory/#llama_index.core.memory.vector_memory.VectorMemory "Permanent link")
Bases: 
Deprecated: Please use `llama_index.core.memory.Memory` instead.
Memory backed by a vector index.
NOTE: This class requires the `delete_nodes` method to be implemented by the vector store underlying the vector index. At time of writing (May 2024), Chroma, Qdrant and SimpleVectorStore all support delete_nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `vector_index`  |  _required_  |  
|  `retriever_kwargs`  |  `Dict[str, Any]`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
|  `batch_by_user_message`  |  `bool`  |  `True`  |  
|  `cur_batch_textnode`  |   |  The super node for the current active user-message batch.  |  `TextNode(id_='0e701367-0283-433a-8703-a5e70ea3036c', embedding=None, metadata={'sub_dicts': []}, excluded_embed_metadata_keys=['sub_dicts'], excluded_llm_metadata_keys=['sub_dicts'], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='', mimetype='text/plain', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}')`  |  
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
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
```
 | 
```
classVectorMemory(BaseMemory):
"""
    Deprecated: Please use `llama_index.core.memory.Memory` instead.

    Memory backed by a vector index.

    NOTE: This class requires the `delete_nodes` method to be implemented
    by the vector store underlying the vector index. At time of writing (May 2024),
    Chroma, Qdrant and SimpleVectorStore all support delete_nodes.
    """

    vector_index: Any
    retriever_kwargs: Dict[str, Any] = Field(default_factory=dict)

    # Whether to combine a user message with all subsequent messages
    # until the next user message into a single message
    # This is on by default, ensuring that we always fetch contiguous blocks of user/response pairs.
    # Turning this off may lead to errors in the function calling API of the LLM.
    # If this is on, then any message that's not a user message will be combined with the last user message
    # in the vector store.
    batch_by_user_message: bool = True

    cur_batch_textnode: TextNode = Field(
        default_factory=_get_starter_node_for_new_batch,
        description="The super node for the current active user-message batch.",
    )

    @field_validator("vector_index")
    @classmethod
    defvalidate_vector_index(cls, value: Any) -> Any:
"""Validate vector index."""
        # NOTE: we can't import VectorStoreIndex directly due to circular imports,
        # which is why the type is Any
        fromllama_index.core.indices.vector_storeimport VectorStoreIndex

        if not isinstance(value, VectorStoreIndex):
            raise ValueError(
                f"Expected 'vector_index' to be an instance of VectorStoreIndex, got {type(value)}"
            )
        return value

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "VectorMemory"

    @classmethod
    deffrom_defaults(
        cls,
        vector_store: Optional[BasePydanticVectorStore] = None,
        embed_model: Optional[EmbedType] = None,
        index_kwargs: Optional[Dict] = None,
        retriever_kwargs: Optional[Dict] = None,
        **kwargs: Any,
    ) -> "VectorMemory":
"""
        Create vector memory.

        Args:
            vector_store (Optional[BasePydanticVectorStore]): vector store (note: delete_nodes must
                be implemented. At time of writing (May 2024), Chroma, Qdrant and
                SimpleVectorStore all support delete_nodes.
            embed_model (Optional[EmbedType]): embedding model
            index_kwargs (Optional[Dict]): kwargs for initializing the index
            retriever_kwargs (Optional[Dict]): kwargs for initializing the retriever

        """
        fromllama_index.core.indices.vector_storeimport VectorStoreIndex

        if kwargs:
            raise ValueError(f"Unexpected kwargs: {kwargs}")

        index_kwargs = index_kwargs or {}
        retriever_kwargs = retriever_kwargs or {}

        if vector_store is None:
            # initialize a blank in-memory vector store
            # NOTE: can't easily do that from `from_vector_store` at the moment.
            index = VectorStoreIndex.from_documents(
                [], embed_model=embed_model, **index_kwargs
            )
        else:
            index = VectorStoreIndex.from_vector_store(
                vector_store, embed_model=embed_model, **index_kwargs
            )
        return cls(vector_index=index, retriever_kwargs=retriever_kwargs)

    defget(
        self, input: Optional[str] = None, initial_token_count: int = 0, **kwargs: Any
    ) -> List[ChatMessage]:
"""Get chat history."""
        if input is None:
            return []

        # retrieve from index
        retriever = self.vector_index.as_retriever(**self.retriever_kwargs)
        nodes = retriever.retrieve(input or "")

        # retrieve underlying messages
        return [
            ChatMessage.model_validate(sub_dict)
            for node in nodes
            for sub_dict in node.metadata["sub_dicts"]
        ]

    defget_all(self) -> List[ChatMessage]:
"""Get all chat history."""
        # TODO: while we could implement get_all, would be hacky through metadata filtering
        # since vector stores don't easily support get()
        raise ValueError(
            "Vector memory does not support get_all method, can only retrieve based on input."
        )

    def_commit_node(self, override_last: bool = False) -> None:
"""Commit new node to vector store."""
        if self.cur_batch_textnode.text == "":
            return

        if override_last:
            # delete the last node
            # This is needed since we're updating the last node in the vector
            # index as its being updated. When a new user-message batch starts
            # we already will have the last user message group committed to the
            # vector store index and so we don't need to override_last (i.e. see
            # logic in self.put().)
            self.vector_index.delete_nodes([self.cur_batch_textnode.id_])

        self.vector_index.insert_nodes([self.cur_batch_textnode])

    defput(self, message: ChatMessage) -> None:
"""Put chat history."""
        if not self.batch_by_user_message or message.role in [
            MessageRole.USER,
            MessageRole.SYSTEM,
        ]:
            # if not batching by user message, commit to vector store immediately after adding
            self.cur_batch_textnode = _get_starter_node_for_new_batch()

        # update current batch textnode
        sub_dict = _stringify_chat_message(message)
        if self.cur_batch_textnode.text == "":
            self.cur_batch_textnode.text += sub_dict["content"] or ""
        else:
            self.cur_batch_textnode.text += " " + (sub_dict["content"] or "")
        self.cur_batch_textnode.metadata["sub_dicts"].append(sub_dict)
        self._commit_node(override_last=True)

    defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
        self.reset()
        for message in messages:
            self.put(message)

    defreset(self) -> None:
"""Reset chat history."""
        self.vector_index.vector_store.clear()

```
 |  
| --- | --- |  
###  validate_vector_index `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/vector_memory/#llama_index.core.memory.vector_memory.VectorMemory.validate_vector_index "Permanent link")

```
validate_vector_index(value: ) -> 

```

Validate vector index.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
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
```
 | 
```
@field_validator("vector_index")
@classmethod
defvalidate_vector_index(cls, value: Any) -> Any:
"""Validate vector index."""
    # NOTE: we can't import VectorStoreIndex directly due to circular imports,
    # which is why the type is Any
    fromllama_index.core.indices.vector_storeimport VectorStoreIndex

    if not isinstance(value, VectorStoreIndex):
        raise ValueError(
            f"Expected 'vector_index' to be an instance of VectorStoreIndex, got {type(value)}"
        )
    return value

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/vector_memory/#llama_index.core.memory.vector_memory.VectorMemory.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
89
90
91
92
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "VectorMemory"

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/vector_memory/#llama_index.core.memory.vector_memory.VectorMemory.from_defaults "Permanent link")

```
from_defaults(
    vector_store: Optional[] = None,
    embed_model: Optional[EmbedType] = None,
    index_kwargs: Optional[] = None,
    retriever_kwargs: Optional[] = None,
    **kwargs: 
) -> 

```

Create vector memory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `vector_store`  |  `Optional[BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)")]`  |  vector store (note: delete_nodes must be implemented. At time of writing (May 2024), Chroma, Qdrant and SimpleVectorStore all support delete_nodes.  |  `None`  |  
|  `embed_model`  |  `Optional[EmbedType]`  |  embedding model  |  `None`  |  
|  `index_kwargs`  |  `Optional[Dict]`  |  kwargs for initializing the index  |  `None`  |  
|  `retriever_kwargs`  |  `Optional[Dict]`  |  kwargs for initializing the retriever  |  `None`  |  
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    vector_store: Optional[BasePydanticVectorStore] = None,
    embed_model: Optional[EmbedType] = None,
    index_kwargs: Optional[Dict] = None,
    retriever_kwargs: Optional[Dict] = None,
    **kwargs: Any,
) -> "VectorMemory":
"""
    Create vector memory.

    Args:
        vector_store (Optional[BasePydanticVectorStore]): vector store (note: delete_nodes must
            be implemented. At time of writing (May 2024), Chroma, Qdrant and
            SimpleVectorStore all support delete_nodes.
        embed_model (Optional[EmbedType]): embedding model
        index_kwargs (Optional[Dict]): kwargs for initializing the index
        retriever_kwargs (Optional[Dict]): kwargs for initializing the retriever

    """
    fromllama_index.core.indices.vector_storeimport VectorStoreIndex

    if kwargs:
        raise ValueError(f"Unexpected kwargs: {kwargs}")

    index_kwargs = index_kwargs or {}
    retriever_kwargs = retriever_kwargs or {}

    if vector_store is None:
        # initialize a blank in-memory vector store
        # NOTE: can't easily do that from `from_vector_store` at the moment.
        index = VectorStoreIndex.from_documents(
            [], embed_model=embed_model, **index_kwargs
        )
    else:
        index = VectorStoreIndex.from_vector_store(
            vector_store, embed_model=embed_model, **index_kwargs
        )
    return cls(vector_index=index, retriever_kwargs=retriever_kwargs)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/vector_memory/#llama_index.core.memory.vector_memory.VectorMemory.get "Permanent link")

```
get(
    input: Optional[] = None,
    initial_token_count:  = 0,
    **kwargs: 
) -> []

```

Get chat history.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
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
defget(
    self, input: Optional[str] = None, initial_token_count: int = 0, **kwargs: Any
) -> List[ChatMessage]:
"""Get chat history."""
    if input is None:
        return []

    # retrieve from index
    retriever = self.vector_index.as_retriever(**self.retriever_kwargs)
    nodes = retriever.retrieve(input or "")

    # retrieve underlying messages
    return [
        ChatMessage.model_validate(sub_dict)
        for node in nodes
        for sub_dict in node.metadata["sub_dicts"]
    ]

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/vector_memory/#llama_index.core.memory.vector_memory.VectorMemory.get_all "Permanent link")

```
get_all() -> []

```

Get all chat history.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
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
defget_all(self) -> List[ChatMessage]:
"""Get all chat history."""
    # TODO: while we could implement get_all, would be hacky through metadata filtering
    # since vector stores don't easily support get()
    raise ValueError(
        "Vector memory does not support get_all method, can only retrieve based on input."
    )

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/vector_memory/#llama_index.core.memory.vector_memory.VectorMemory.put "Permanent link")

```
put(message: ) -> None

```

Put chat history.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
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
```
 | 
```
defput(self, message: ChatMessage) -> None:
"""Put chat history."""
    if not self.batch_by_user_message or message.role in [
        MessageRole.USER,
        MessageRole.SYSTEM,
    ]:
        # if not batching by user message, commit to vector store immediately after adding
        self.cur_batch_textnode = _get_starter_node_for_new_batch()

    # update current batch textnode
    sub_dict = _stringify_chat_message(message)
    if self.cur_batch_textnode.text == "":
        self.cur_batch_textnode.text += sub_dict["content"] or ""
    else:
        self.cur_batch_textnode.text += " " + (sub_dict["content"] or "")
    self.cur_batch_textnode.metadata["sub_dicts"].append(sub_dict)
    self._commit_node(override_last=True)

```
 |  
| --- | --- |  
###  set [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/vector_memory/#llama_index.core.memory.vector_memory.VectorMemory.set "Permanent link")

```
set(messages: []) -> None

```

Set chat history.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
195
196
197
198
199
```
 | 
```
defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
    self.reset()
    for message in messages:
        self.put(message)

```
 |  
| --- | --- |  
###  reset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/vector_memory/#llama_index.core.memory.vector_memory.VectorMemory.reset "Permanent link")

```
reset() -> None

```

Reset chat history.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
201
202
203
```
 | 
```
defreset(self) -> None:
"""Reset chat history."""
    self.vector_index.vector_store.clear()

```
 |  
| --- | --- |
