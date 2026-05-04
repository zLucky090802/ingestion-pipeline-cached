# Firestore
##  FirestoreVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/firestore/#llama_index.vector_stores.firestore.FirestoreVectorStore "Permanent link")
Bases: 
Firestore Vector Store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-firestore/llama_index/vector_stores/firestore/base.py`  
| 
```
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
```
 | 
```
classFirestoreVectorStore(BasePydanticVectorStore):
"""Firestore Vector Store."""

    stores_text: bool = True
    flat_metadata: bool = True

    collection_name: str
    batch_size: Optional[int] = DEFAULT_BATCH_SIZE
    embedding_key: str = "embedding"
    text_key: str = "text"
    metadata_key: str = "metadata"
    distance_strategy: DistanceMeasure = DistanceMeasure.COSINE

    _client: Client

    def__init__(
        self,
        client: Optional[Client] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        super().__init__(**kwargs)
        object.__setattr__(self, "_client", client_with_user_agent(client))

    @classmethod
    defclass_name(cls) -> str:
        return "FirestoreVectorStore"

    @property
    defclient(self) -> Any:
        return self._client

    defadd(
        self,
        nodes: List[BaseNode],
    ) -> List[str]:
"""Add nodes to vector store."""
        ids = []
        entries = []
        for node in nodes:
            node_id = node.node_id
            metadata = node_to_metadata_dict(
                node,
                remove_text=not self.stores_text,
                flat_metadata=self.flat_metadata,
            )
            entry = {
                self.embedding_key: node.get_embedding(),
                self.metadata_key: metadata,
            }
            ids.append(node_id)
            entries.append(entry)
        self._upsert_batch(entries, ids)
        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Delete nodes using with ref_doc_id."""
        docs = (
            self._client.collection(self.collection_name)
            .where("metadata.ref_doc_id", "==", ref_doc_id)
            .stream()
        )

        self._delete_batch([doc.id for doc in docs])

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query vector store."""
        if query.query_embedding is None:
            raise ValueError("Query embedding is required.")

        filters = _to_firestore_filter(query.filters) if query.filters else None

        results = self._similarity_search(
            query.query_embedding, query.similarity_top_k, filters=filters, **kwargs
        )

        top_k_ids = []
        top_k_nodes = []
        top_k_similarities = []

        LOGGER.debug(f"Found {len(results)} results.")

        for result in results:
            # Convert the Firestore document to dict
            result_dict = result.to_dict() or {}
            metadata = result_dict.get(self.metadata_key) or {}
            fir_vec: Optional[Vector] = result_dict.get(self.embedding_key)
            if fir_vec is None:
                raise ValueError(
                    "Embedding is missing in Firestore document.", result.id
                )
            embedding = list(fir_vec.to_map_value()["value"])

            # Convert metadata to node, and add text if available
            node = metadata_dict_to_node(metadata, text=result_dict.get(self.text_key))

            # Keep track of the top k ids and nodes
            top_k_ids.append(result.id)
            top_k_nodes.append(node)
            top_k_similarities.append(
                similarity(
                    query.query_embedding,
                    embedding,
                    self._distance_to_similarity_mode(self.distance_strategy),
                )
            )

        return VectorStoreQueryResult(
            nodes=top_k_nodes, ids=top_k_ids, similarities=top_k_similarities
        )

    def_distance_to_similarity_mode(self, distance: DistanceMeasure) -> SimilarityMode:
"""Convert Firestore's distance measure to similarity mode."""
        return {
            DistanceMeasure.COSINE: SimilarityMode.DEFAULT,
            DistanceMeasure.EUCLIDEAN: SimilarityMode.EUCLIDEAN,
            DistanceMeasure.DOT_PRODUCT: SimilarityMode.DOT_PRODUCT,
        }.get(distance, SimilarityMode.DEFAULT)

    def_delete_batch(self, ids: List[str]) -> None:
"""Delete batch of vectors from Firestore."""
        db_batch = self._client.batch()
        for batch in more_itertools.chunked(ids, DEFAULT_BATCH_SIZE):
            for doc_id in batch:
                doc = self._client.collection(self.collection_name).document(doc_id)
                db_batch.delete(doc)
            db_batch.commit()

    def_upsert_batch(self, entries: List[dict], ids: Optional[List[str]]) -> None:
"""Upsert batch of vectors to Firestore."""
        if ids and len(ids) != len(entries):
            raise ValueError("Length of ids and entries should be the same.")

        db_batch = self._client.batch()

        for batch in more_itertools.chunked(entries, DEFAULT_BATCH_SIZE):
            for i, entry in enumerate(batch):
                # Convert the embedding array to a Firestore Vector
                entry[self.embedding_key] = Vector(entry[self.embedding_key])
                doc = self._client.collection(self.collection_name).document(
                    ids[i] if ids else None
                )
                db_batch.set(doc, entry, merge=True)
            db_batch.commit()

    def_similarity_search(
        self,
        query: List[float],
        k: int,
        filters: Union[BaseFilter, BaseCompositeFilter, None] = None,
    ) -> List[DocumentSnapshot]:
        wfilters = None
        collection = self._client.collection(self.collection_name)

        if filters:
            wfilters = collection.where(filter=filters)

        results = (wfilters or collection).find_nearest(
            vector_field=self.embedding_key,
            query_vector=Vector(query),
            distance_measure=self.distance_strategy,
            limit=k,
        )

        return results.get()

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/firestore/#llama_index.vector_stores.firestore.FirestoreVectorStore.add "Permanent link")

```
add(nodes: []) -> []

```

Add nodes to vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-firestore/llama_index/vector_stores/firestore/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
) -> List[str]:
"""Add nodes to vector store."""
    ids = []
    entries = []
    for node in nodes:
        node_id = node.node_id
        metadata = node_to_metadata_dict(
            node,
            remove_text=not self.stores_text,
            flat_metadata=self.flat_metadata,
        )
        entry = {
            self.embedding_key: node.get_embedding(),
            self.metadata_key: metadata,
        }
        ids.append(node_id)
        entries.append(entry)
    self._upsert_batch(entries, ids)
    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/firestore/#llama_index.vector_stores.firestore.FirestoreVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-firestore/llama_index/vector_stores/firestore/base.py`  
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Delete nodes using with ref_doc_id."""
    docs = (
        self._client.collection(self.collection_name)
        .where("metadata.ref_doc_id", "==", ref_doc_id)
        .stream()
    )

    self._delete_batch([doc.id for doc in docs])

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/firestore/#llama_index.vector_stores.firestore.FirestoreVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-firestore/llama_index/vector_stores/firestore/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query vector store."""
    if query.query_embedding is None:
        raise ValueError("Query embedding is required.")

    filters = _to_firestore_filter(query.filters) if query.filters else None

    results = self._similarity_search(
        query.query_embedding, query.similarity_top_k, filters=filters, **kwargs
    )

    top_k_ids = []
    top_k_nodes = []
    top_k_similarities = []

    LOGGER.debug(f"Found {len(results)} results.")

    for result in results:
        # Convert the Firestore document to dict
        result_dict = result.to_dict() or {}
        metadata = result_dict.get(self.metadata_key) or {}
        fir_vec: Optional[Vector] = result_dict.get(self.embedding_key)
        if fir_vec is None:
            raise ValueError(
                "Embedding is missing in Firestore document.", result.id
            )
        embedding = list(fir_vec.to_map_value()["value"])

        # Convert metadata to node, and add text if available
        node = metadata_dict_to_node(metadata, text=result_dict.get(self.text_key))

        # Keep track of the top k ids and nodes
        top_k_ids.append(result.id)
        top_k_nodes.append(node)
        top_k_similarities.append(
            similarity(
                query.query_embedding,
                embedding,
                self._distance_to_similarity_mode(self.distance_strategy),
            )
        )

    return VectorStoreQueryResult(
        nodes=top_k_nodes, ids=top_k_ids, similarities=top_k_similarities
    )

```
 |  
| --- | --- |  
options: members: - FirestoreVectorStore
