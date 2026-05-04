# Raptor
##  RaptorPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raptor/#llama_index.packs.raptor.RaptorPack "Permanent link")
Bases: 
Raptor pack.
Source code in `llama-index-packs/llama-index-packs-raptor/llama_index/packs/raptor/base.py`  
| 
```
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
```
 | 
```
classRaptorPack(BaseLlamaPack):
"""Raptor pack."""

    def__init__(
        self,
        documents: List[BaseNode],
        llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        vector_store: Optional[BasePydanticVectorStore] = None,
        similarity_top_k: int = 2,
        mode: QueryModes = "collapsed",
        verbose: bool = True,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        self.retriever = RaptorRetriever(
            documents,
            embed_model=embed_model,
            llm=llm,
            similarity_top_k=similarity_top_k,
            vector_store=vector_store,
            mode=mode,
            verbose=verbose,
            **kwargs,
        )

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "retriever": self.retriever,
        }

    defrun(
        self,
        query: str,
        mode: Optional[QueryModes] = None,
    ) -> Any:
"""Run the pipeline."""
        return self.retriever.retrieve(query, mode=mode)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raptor/#llama_index.packs.raptor.RaptorPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-raptor/llama_index/packs/raptor/base.py`  
| 
```
375
376
377
378
379
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "retriever": self.retriever,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raptor/#llama_index.packs.raptor.RaptorPack.run "Permanent link")

```
run(query: , mode: Optional[QueryModes] = None) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-raptor/llama_index/packs/raptor/base.py`  
| 
```
381
382
383
384
385
386
387
```
 | 
```
defrun(
    self,
    query: str,
    mode: Optional[QueryModes] = None,
) -> Any:
"""Run the pipeline."""
    return self.retriever.retrieve(query, mode=mode)

```
 |  
| --- | --- |  
##  RaptorRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raptor/#llama_index.packs.raptor.RaptorRetriever "Permanent link")
Bases: 
Raptor indexing retriever.
Source code in `llama-index-packs/llama-index-packs-raptor/llama_index/packs/raptor/base.py`  
| 
```
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
```
 | 
```
classRaptorRetriever(BaseRetriever):
"""Raptor indexing retriever."""

    def__init__(
        self,
        documents: List[BaseNode],
        tree_depth: int = 3,
        similarity_top_k: int = 2,
        llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        vector_store: Optional[BasePydanticVectorStore] = None,
        transformations: Optional[List[TransformComponent]] = None,
        summary_module: Optional[SummaryModule] = None,
        existing_index: Optional[VectorStoreIndex] = None,
        mode: QueryModes = "collapsed",
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__(
            **kwargs,
        )

        self.mode = mode
        self.summary_module = summary_module or SummaryModule(llm=llm)
        self.index = existing_index or VectorStoreIndex(
            nodes=[],
            storage_context=StorageContext.from_defaults(vector_store=vector_store),
            embed_model=embed_model,
            transformations=transformations,
        )
        self.tree_depth = tree_depth
        self.similarity_top_k = similarity_top_k

        if len(documents)  0:
            asyncio.run(self.insert(documents))

    def_get_embeddings_per_level(self, level: int = 0) -> List[float]:
"""
        Retrieve embeddings per level in the abstraction tree.

        Args:
            level (int, optional): Target level. Defaults to 0 which stands for leaf nodes.

        Returns:
            List[float]: List of embeddings

        """
        filters = MetadataFilters(filters=[MetadataFilter("level", level)])

        # kind of janky, but should work with any vector index
        source_nodes = self.index.as_retriever(
            similarity_top_k=10000, filters=filters
        ).retrieve("retrieve")

        return [x.node for x in source_nodes]

    async definsert(self, documents: List[BaseNode]) -> None:
"""
        Given a set of documents, this function inserts higher level of abstractions within the index.

        For later retrieval

        Args:
            documents (List[BaseNode]): List of Documents

        """
        embed_model = self.index._embed_model
        transformations = self.index._transformations

        cur_nodes = run_transformations(documents, transformations, in_place=False)
        for level in range(self.tree_depth):
            # get the embeddings for the current documents

            if self._verbose:
                print(f"Generating embeddings for level {level}.")

            embeddings = await embed_model.aget_text_embedding_batch(
                [node.get_content(metadata_mode="embed") for node in cur_nodes]
            )
            assert len(embeddings) == len(cur_nodes)
            id_to_embedding = {
                node.id_: embedding for node, embedding in zip(cur_nodes, embeddings)
            }

            if self._verbose:
                print(f"Performing clustering for level {level}.")

            # cluster the documents
            nodes_per_cluster = get_clusters(cur_nodes, id_to_embedding)

            if self._verbose:
                print(
                    f"Generating summaries for level {level} with {len(nodes_per_cluster)} clusters."
                )
            summaries_per_cluster = await self.summary_module.generate_summaries(
                nodes_per_cluster
            )

            if self._verbose:
                print(
                    f"Level {level} created summaries/clusters: {len(nodes_per_cluster)}"
                )

            # replace the current nodes with their summaries
            new_nodes = [
                TextNode(
                    text=summary,
                    metadata={"level": level},
                    excluded_embed_metadata_keys=["level"],
                    excluded_llm_metadata_keys=["level"],
                )
                for summary in summaries_per_cluster
            ]

            # insert the nodes with their embeddings and parent_id
            nodes_with_embeddings = []
            for cluster, summary_doc in zip(nodes_per_cluster, new_nodes):
                for node in cluster:
                    node.metadata["parent_id"] = summary_doc.id_
                    node.excluded_embed_metadata_keys.append("parent_id")
                    node.excluded_llm_metadata_keys.append("parent_id")
                    node.embedding = id_to_embedding[node.id_]
                    nodes_with_embeddings.append(node)

            self.index.insert_nodes(nodes_with_embeddings)

            # set the current nodes to the new nodes
            cur_nodes = new_nodes

        self.index.insert_nodes(cur_nodes)

    async defcollapsed_retrieval(self, query_str: str) -> Response:
"""Query the index as a collapsed tree -- i.e. a single pool of nodes."""
        return await self.index.as_retriever(
            similarity_top_k=self.similarity_top_k
        ).aretrieve(query_str)

    async deftree_traversal_retrieval(self, query_str: str) -> Response:
"""Query the index as a tree, traversing the tree from the top down."""
        # get top k nodes for each level, starting with the top
        parent_ids = None
        selected_node_ids = set()
        selected_nodes = []
        level = self.tree_depth - 1
        while level >= 0:
            # retrieve nodes at the current level
            if parent_ids is None:
                nodes = await self.index.as_retriever(
                    similarity_top_k=self.similarity_top_k,
                    filters=MetadataFilters(
                        filters=[MetadataFilter(key="level", value=level)]
                    ),
                ).aretrieve(query_str)

                for node in nodes:
                    if node.id_ not in selected_node_ids:
                        selected_nodes.append(node)
                        selected_node_ids.add(node.id_)

                parent_ids = [node.id_ for node in nodes]
                if self._verbose:
                    print(f"Retrieved parent IDs from level {level}: {parent_ids!s}")
            # retrieve nodes that are children of the nodes at the previous level
            elif parent_ids is not None and len(parent_ids)  0:
                nested_nodes = await asyncio.gather(
                    *[
                        self.index.as_retriever(
                            similarity_top_k=self.similarity_top_k,
                            filters=MetadataFilters(
                                filters=[MetadataFilter(key="parent_id", value=id_)]
                            ),
                        ).aretrieve(query_str)
                        for id_ in parent_ids
                    ]
                )

                nodes = [node for nested in nested_nodes for node in nested]
                for node in nodes:
                    if node.id_ not in selected_node_ids:
                        selected_nodes.append(node)
                        selected_node_ids.add(node.id_)

                if self._verbose:
                    print(f"Retrieved {len(nodes)} from parents at level {level}.")

                level -= 1
                parent_ids = None

        return selected_nodes

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve nodes given query and mode."""
        # not used, needed for type checking

    defretrieve(
        self, query_str_or_bundle: QueryType, mode: Optional[QueryModes] = None
    ) -> List[NodeWithScore]:
"""Retrieve nodes given query and mode."""
        if isinstance(query_str_or_bundle, QueryBundle):
            query_str = query_str_or_bundle.query_str
        else:
            query_str = query_str_or_bundle

        return asyncio.run(self.aretrieve(query_str, mode or self.mode))

    async defaretrieve(
        self, query_str_or_bundle: QueryType, mode: Optional[QueryModes] = None
    ) -> List[NodeWithScore]:
"""Retrieve nodes given query and mode."""
        if isinstance(query_str_or_bundle, QueryBundle):
            query_str = query_str_or_bundle.query_str
        else:
            query_str = query_str_or_bundle

        mode = mode or self.mode
        if mode == "tree_traversal":
            return await self.tree_traversal_retrieval(query_str)
        elif mode == "collapsed":
            return await self.collapsed_retrieval(query_str)
        else:
            raise ValueError(f"Invalid mode: {mode}")

    defpersist(self, persist_dir: str) -> None:
        self.index.storage_context.persist(persist_dir=persist_dir)

    @classmethod
    deffrom_persist_dir(
        cls: "RaptorRetriever",
        persist_dir: str,
        embed_model: Optional[BaseEmbedding] = None,
        **kwargs: Any,
    ) -> "RaptorRetriever":
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        return cls(
            [],
            existing_index=load_index_from_storage(
                storage_context, embed_model=embed_model
            ),
            **kwargs,
        )

```
 |  
| --- | --- |  
###  insert [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raptor/#llama_index.packs.raptor.RaptorRetriever.insert "Permanent link")

```
insert(documents: []) -> None

```

Given a set of documents, this function inserts higher level of abstractions within the index.
For later retrieval
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `documents`  |   |  List of Documents  |  _required_  |  
Source code in `llama-index-packs/llama-index-packs-raptor/llama_index/packs/raptor/base.py`  
| 
```
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
```
 | 
```
async definsert(self, documents: List[BaseNode]) -> None:
"""
    Given a set of documents, this function inserts higher level of abstractions within the index.

    For later retrieval

    Args:
        documents (List[BaseNode]): List of Documents

    """
    embed_model = self.index._embed_model
    transformations = self.index._transformations

    cur_nodes = run_transformations(documents, transformations, in_place=False)
    for level in range(self.tree_depth):
        # get the embeddings for the current documents

        if self._verbose:
            print(f"Generating embeddings for level {level}.")

        embeddings = await embed_model.aget_text_embedding_batch(
            [node.get_content(metadata_mode="embed") for node in cur_nodes]
        )
        assert len(embeddings) == len(cur_nodes)
        id_to_embedding = {
            node.id_: embedding for node, embedding in zip(cur_nodes, embeddings)
        }

        if self._verbose:
            print(f"Performing clustering for level {level}.")

        # cluster the documents
        nodes_per_cluster = get_clusters(cur_nodes, id_to_embedding)

        if self._verbose:
            print(
                f"Generating summaries for level {level} with {len(nodes_per_cluster)} clusters."
            )
        summaries_per_cluster = await self.summary_module.generate_summaries(
            nodes_per_cluster
        )

        if self._verbose:
            print(
                f"Level {level} created summaries/clusters: {len(nodes_per_cluster)}"
            )

        # replace the current nodes with their summaries
        new_nodes = [
            TextNode(
                text=summary,
                metadata={"level": level},
                excluded_embed_metadata_keys=["level"],
                excluded_llm_metadata_keys=["level"],
            )
            for summary in summaries_per_cluster
        ]

        # insert the nodes with their embeddings and parent_id
        nodes_with_embeddings = []
        for cluster, summary_doc in zip(nodes_per_cluster, new_nodes):
            for node in cluster:
                node.metadata["parent_id"] = summary_doc.id_
                node.excluded_embed_metadata_keys.append("parent_id")
                node.excluded_llm_metadata_keys.append("parent_id")
                node.embedding = id_to_embedding[node.id_]
                nodes_with_embeddings.append(node)

        self.index.insert_nodes(nodes_with_embeddings)

        # set the current nodes to the new nodes
        cur_nodes = new_nodes

    self.index.insert_nodes(cur_nodes)

```
 |  
| --- | --- |  
###  collapsed_retrieval [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raptor/#llama_index.packs.raptor.RaptorRetriever.collapsed_retrieval "Permanent link")

```
collapsed_retrieval(query_str: ) -> 

```

Query the index as a collapsed tree -- i.e. a single pool of nodes.
Source code in `llama-index-packs/llama-index-packs-raptor/llama_index/packs/raptor/base.py`  
| 
```
238
239
240
241
242
```
 | 
```
async defcollapsed_retrieval(self, query_str: str) -> Response:
"""Query the index as a collapsed tree -- i.e. a single pool of nodes."""
    return await self.index.as_retriever(
        similarity_top_k=self.similarity_top_k
    ).aretrieve(query_str)

```
 |  
| --- | --- |  
###  tree_traversal_retrieval [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raptor/#llama_index.packs.raptor.RaptorRetriever.tree_traversal_retrieval "Permanent link")

```
tree_traversal_retrieval(query_str: ) -> 

```

Query the index as a tree, traversing the tree from the top down.
Source code in `llama-index-packs/llama-index-packs-raptor/llama_index/packs/raptor/base.py`  
| 
```
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
```
 | 
```
async deftree_traversal_retrieval(self, query_str: str) -> Response:
"""Query the index as a tree, traversing the tree from the top down."""
    # get top k nodes for each level, starting with the top
    parent_ids = None
    selected_node_ids = set()
    selected_nodes = []
    level = self.tree_depth - 1
    while level >= 0:
        # retrieve nodes at the current level
        if parent_ids is None:
            nodes = await self.index.as_retriever(
                similarity_top_k=self.similarity_top_k,
                filters=MetadataFilters(
                    filters=[MetadataFilter(key="level", value=level)]
                ),
            ).aretrieve(query_str)

            for node in nodes:
                if node.id_ not in selected_node_ids:
                    selected_nodes.append(node)
                    selected_node_ids.add(node.id_)

            parent_ids = [node.id_ for node in nodes]
            if self._verbose:
                print(f"Retrieved parent IDs from level {level}: {parent_ids!s}")
        # retrieve nodes that are children of the nodes at the previous level
        elif parent_ids is not None and len(parent_ids)  0:
            nested_nodes = await asyncio.gather(
                *[
                    self.index.as_retriever(
                        similarity_top_k=self.similarity_top_k,
                        filters=MetadataFilters(
                            filters=[MetadataFilter(key="parent_id", value=id_)]
                        ),
                    ).aretrieve(query_str)
                    for id_ in parent_ids
                ]
            )

            nodes = [node for nested in nested_nodes for node in nested]
            for node in nodes:
                if node.id_ not in selected_node_ids:
                    selected_nodes.append(node)
                    selected_node_ids.add(node.id_)

            if self._verbose:
                print(f"Retrieved {len(nodes)} from parents at level {level}.")

            level -= 1
            parent_ids = None

    return selected_nodes

```
 |  
| --- | --- |  
###  retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raptor/#llama_index.packs.raptor.RaptorRetriever.retrieve "Permanent link")

```
retrieve(
    query_str_or_bundle: QueryType,
    mode: Optional[QueryModes] = None,
) -> []

```

Retrieve nodes given query and mode.
Source code in `llama-index-packs/llama-index-packs-raptor/llama_index/packs/raptor/base.py`  
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
```
 | 
```
defretrieve(
    self, query_str_or_bundle: QueryType, mode: Optional[QueryModes] = None
) -> List[NodeWithScore]:
"""Retrieve nodes given query and mode."""
    if isinstance(query_str_or_bundle, QueryBundle):
        query_str = query_str_or_bundle.query_str
    else:
        query_str = query_str_or_bundle

    return asyncio.run(self.aretrieve(query_str, mode or self.mode))

```
 |  
| --- | --- |  
###  aretrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raptor/#llama_index.packs.raptor.RaptorRetriever.aretrieve "Permanent link")

```
aretrieve(
    query_str_or_bundle: QueryType,
    mode: Optional[QueryModes] = None,
) -> []

```

Retrieve nodes given query and mode.
Source code in `llama-index-packs/llama-index-packs-raptor/llama_index/packs/raptor/base.py`  
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
322
323
324
325
326
327
```
 | 
```
async defaretrieve(
    self, query_str_or_bundle: QueryType, mode: Optional[QueryModes] = None
) -> List[NodeWithScore]:
"""Retrieve nodes given query and mode."""
    if isinstance(query_str_or_bundle, QueryBundle):
        query_str = query_str_or_bundle.query_str
    else:
        query_str = query_str_or_bundle

    mode = mode or self.mode
    if mode == "tree_traversal":
        return await self.tree_traversal_retrieval(query_str)
    elif mode == "collapsed":
        return await self.collapsed_retrieval(query_str)
    else:
        raise ValueError(f"Invalid mode: {mode}")

```
 |  
| --- | --- |  
options: members: - RaptorPack
