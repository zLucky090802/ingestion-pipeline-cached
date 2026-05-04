# Upstash
##  UpstashVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/upstash/#llama_index.vector_stores.upstash.UpstashVectorStore "Permanent link")
Bases: 
Upstash Vector Store.
Examples:
`pip install llama-index-vector-stores-upstash`

```
fromllama_index.vector_stores.upstashimport UpstashVectorStore

# Create Upstash vector store
upstash_vector_store = UpstashVectorStore(
    url="your_upstash_vector_url",
    token="your_upstash_vector_token",
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-upstash/llama_index/vector_stores/upstash/base.py`  
| 
```
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
```
 | 
```
classUpstashVectorStore(BasePydanticVectorStore):
"""
    Upstash Vector Store.

    Examples:
        `pip install llama-index-vector-stores-upstash`

        ```python
        from llama_index.vector_stores.upstash import UpstashVectorStore

        # Create Upstash vector store
        upstash_vector_store = UpstashVectorStore(
            url="your_upstash_vector_url",
            token="your_upstash_vector_token",

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    namespace: str = ""

    batch_size: int
    _index: Index = PrivateAttr()

    @classmethod
    defclass_name(cls) -> str:
        return "UpstashVectorStore"

    @property
    defclient(self) -> Any:
"""Return the Upstash client."""
        return self._index

    def__init__(
        self,
        url: str,
        token: str,
        batch_size: int = DEFAULT_BATCH_SIZE,
        # Upstash uses ("") as the default namespace, if not provided
        namespace: str = "",
    ) -> None:
"""
        Create a UpstashVectorStore. The index can be created using the Upstash console.

        Args:
            url (String): URL of the Upstash Vector instance, found in the Upstash console.
            token (String): Token for the Upstash Vector Index, found in the Upstash console.
            batch_size (Optional[int]): Batch size for adding nodes to the vector store.

        Raises:
            ImportError: If the upstash-vector python package is not installed.

        """
        super().__init__(batch_size=batch_size, namespace=namespace)
        self._index = Index(url=url, token=token)

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes to the vector store.

        Args:
            nodes: List of nodes to add to the vector store.
            add_kwargs: Additional arguments to pass to the add method.

        Returns:
            List of ids of the added nodes.

        """
        ids = []
        vectors = []
        for node_batch in iter_batch(nodes, self.batch_size):
            for node in node_batch:
                metadata_dict = node_to_metadata_dict(node)
                ids.append(node.node_id)
                vectors.append((node.node_id, node.embedding, metadata_dict))

            self.client.upsert(vectors=vectors, namespace=self.namespace)

        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete node from the vector store.

        Args:
            ref_doc_id: Reference doc id of the node to delete.
            delete_kwargs: Additional arguments to pass to the delete method.

        """
        raise NotImplementedError(
            "Delete is not currently supported, but will be in the future."
        )

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query the vector store.

        Args:
            query: Query to run against the vector store.
            kwargs: Additional arguments to pass to the query method.

        Returns:
            Query result.

        """
        if query.mode != VectorStoreQueryMode.DEFAULT:
            raise ValueError(f"Query mode {query.mode} not supported")

        # if query.filters:
        #     raise ValueError("Metadata filtering not supported")

        res = self.client.query(
            vector=query.query_embedding,
            top_k=query.similarity_top_k,
            include_vectors=True,
            include_metadata=True,
            filter=_to_upstash_filters(query.filters),
            namespace=self.namespace,
        )

        top_k_nodes = []
        top_k_ids = []
        top_k_scores = []
        for vector in res:
            node = metadata_dict_to_node(vector.metadata)
            node.embedding = vector.vector
            top_k_nodes.append(node)
            top_k_ids.append(vector.id)
            top_k_scores.append(vector.score)

        return VectorStoreQueryResult(
            nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
        )

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/upstash/#llama_index.vector_stores.upstash.UpstashVectorStore.client "Permanent link")

```
client: 

```

Return the Upstash client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/upstash/#llama_index.vector_stores.upstash.UpstashVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to the vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes to add to the vector store.  |  _required_  |  
|  `add_kwargs`  |  Additional arguments to pass to the add method.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List of ids of the added nodes.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-upstash/llama_index/vector_stores/upstash/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes to the vector store.

    Args:
        nodes: List of nodes to add to the vector store.
        add_kwargs: Additional arguments to pass to the add method.

    Returns:
        List of ids of the added nodes.

    """
    ids = []
    vectors = []
    for node_batch in iter_batch(nodes, self.batch_size):
        for node in node_batch:
            metadata_dict = node_to_metadata_dict(node)
            ids.append(node.node_id)
            vectors.append((node.node_id, node.embedding, metadata_dict))

        self.client.upsert(vectors=vectors, namespace=self.namespace)

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/upstash/#llama_index.vector_stores.upstash.UpstashVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete node from the vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  Reference doc id of the node to delete.  |  _required_  |  
|  `delete_kwargs`  |  Additional arguments to pass to the delete method.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-upstash/llama_index/vector_stores/upstash/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete node from the vector store.

    Args:
        ref_doc_id: Reference doc id of the node to delete.
        delete_kwargs: Additional arguments to pass to the delete method.

    """
    raise NotImplementedError(
        "Delete is not currently supported, but will be in the future."
    )

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/upstash/#llama_index.vector_stores.upstash.UpstashVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query the vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Query to run against the vector store.  |  _required_  |  
|  `kwargs`  |  Additional arguments to pass to the query method.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  Query result.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-upstash/llama_index/vector_stores/upstash/base.py`  
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
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query the vector store.

    Args:
        query: Query to run against the vector store.
        kwargs: Additional arguments to pass to the query method.

    Returns:
        Query result.

    """
    if query.mode != VectorStoreQueryMode.DEFAULT:
        raise ValueError(f"Query mode {query.mode} not supported")

    # if query.filters:
    #     raise ValueError("Metadata filtering not supported")

    res = self.client.query(
        vector=query.query_embedding,
        top_k=query.similarity_top_k,
        include_vectors=True,
        include_metadata=True,
        filter=_to_upstash_filters(query.filters),
        namespace=self.namespace,
    )

    top_k_nodes = []
    top_k_ids = []
    top_k_scores = []
    for vector in res:
        node = metadata_dict_to_node(vector.metadata)
        node.embedding = vector.vector
        top_k_nodes.append(node)
        top_k_ids.append(vector.id)
        top_k_scores.append(vector.score)

    return VectorStoreQueryResult(
        nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
    )

```
 |  
| --- | --- |  
options: members: - UpstashVectorStore
