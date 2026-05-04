# Ray
##  RayIngestionPipeline [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/ray/#llama_index.ingestion.ray.RayIngestionPipeline "Permanent link")
Bases: 
An ingestion pipeline that can be applied to data using a Ray cluster.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  Unique name of the ingestion pipeline. Defaults to DEFAULT_PIPELINE_NAME.  |  `DEFAULT_PIPELINE_NAME`  |  
|  `project_name`  |  Unique name of the project. Defaults to DEFAULT_PROJECT_NAME.  |  `DEFAULT_PROJECT_NAME`  |  
|  `transformations`  |  `List[RayTransformComponent[](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/ray/#llama_index.ingestion.ray.RayTransformComponent "RayTransformComponent \(llama_index.ingestion.ray.transform.RayTransformComponent\)")]`  |  Ray transformations to apply to the data. Defaults to None.  |  `None`  |  
|  `documents`  |  `Optional[Sequence[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]]`  |  Documents to ingest. Defaults to None.  |  `None`  |  
|  `readers`  |  `Optional[List[ReaderConfig[](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ReaderConfig "ReaderConfig \(llama_index.core.readers.base.ReaderConfig\)")]]`  |  Reader to use to read the data. Defaults to None.  |  `None`  |  
|  `vector_store`  |  `Optional[BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)")]`  |  Vector store to use to store the data. Defaults to None.  |  `None`  |  
|  `docstore`  |  `Optional[BaseDocumentStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore "BaseDocumentStore \(llama_index.core.storage.docstore.BaseDocumentStore\)")]`  |  Document store to use for de-duping with a vector store. Defaults to None.  |  `None`  |  
|  `docstore_strategy`  |   |  Document de-dup strategy. Defaults to DocstoreStrategy.UPSERTS.  |  `UPSERTS`  |  
Examples:

```
importray
fromllama_index.coreimport Document
fromllama_index.embeddings.openaiimport OpenAIEmbedding
fromllama_index.core.extractorsimport TitleExtractor
fromllama_index.ingestion.rayimport RayIngestionPipeline, RayTransformComponent

# Start a new cluster (or connect to an existing one)
ray.init()

# Create transformations
transformations=[
    RayTransformComponent(
        transform_class=TitleExtractor,
        map_batches_kwargs={
            "batch_size": 10,  # Define the batch size
        },
    ),
    RayTransformComponent(
        transform_class=OpenAIEmbedding,
        map_batches_kwargs={
            "batch_size": 10,
        },
    ),
]

# Create the Ray ingestion pipeline
pipeline = RayIngestionPipeline(
    transformations=transformations
)

# Run the pipeline with many documents
nodes = pipeline.run(documents=[Document.example()] * 100)

```

Source code in `llama-index-integrations/ingestion/llama-index-ingestion-ray/llama_index/ingestion/ray/base.py`  
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
```
 | 
```
classRayIngestionPipeline(IngestionPipeline):
"""
    An ingestion pipeline that can be applied to data using a Ray cluster.

    Args:
        name (str, optional):
            Unique name of the ingestion pipeline. Defaults to DEFAULT_PIPELINE_NAME.
        project_name (str, optional):
            Unique name of the project. Defaults to DEFAULT_PROJECT_NAME.
        transformations (List[RayTransformComponent], optional):
            Ray transformations to apply to the data. Defaults to None.
        documents (Optional[Sequence[Document]], optional):
            Documents to ingest. Defaults to None.
        readers (Optional[List[ReaderConfig]], optional):
            Reader to use to read the data. Defaults to None.
        vector_store (Optional[BasePydanticVectorStore], optional):
            Vector store to use to store the data. Defaults to None.
        docstore (Optional[BaseDocumentStore], optional):
            Document store to use for de-duping with a vector store. Defaults to None.
        docstore_strategy (DocstoreStrategy, optional):
            Document de-dup strategy. Defaults to DocstoreStrategy.UPSERTS.

    Examples:
        ```python
        import ray
        from llama_index.core import Document
        from llama_index.embeddings.openai import OpenAIEmbedding
        from llama_index.core.extractors import TitleExtractor
        from llama_index.ingestion.ray import RayIngestionPipeline, RayTransformComponent

        # Start a new cluster (or connect to an existing one)
        ray.init()

        # Create transformations
        transformations=[
            RayTransformComponent(
                transform_class=TitleExtractor,
                map_batches_kwargs={
                    "batch_size": 10,  # Define the batch size


            RayTransformComponent(
                transform_class=OpenAIEmbedding,
                map_batches_kwargs={
                    "batch_size": 10,




        # Create the Ray ingestion pipeline
        pipeline = RayIngestionPipeline(
            transformations=transformations


        # Run the pipeline with many documents
        nodes = pipeline.run(documents=[Document.example()] * 100)
        ```

    """

    transformations: List[RayTransformComponent] = Field(
        description="Transformations to apply to the data with Ray"
    )

    def__init__(
        self,
        name: str = DEFAULT_PIPELINE_NAME,
        project_name: str = DEFAULT_PROJECT_NAME,
        transformations: Optional[List[RayTransformComponent]] = None,
        readers: Optional[List[ReaderConfig]] = None,
        documents: Optional[Sequence[Document]] = None,
        vector_store: Optional[BasePydanticVectorStore] = None,
        docstore: Optional[BaseDocumentStore] = None,
        docstore_strategy: DocstoreStrategy = DocstoreStrategy.UPSERTS,
    ) -> None:
        BaseModel.__init__(
            self,
            name=name,
            project_name=project_name,
            transformations=transformations,
            readers=readers,
            documents=documents,
            vector_store=vector_store,
            cache=IngestionCache(),
            docstore=docstore,
            docstore_strategy=docstore_strategy,
            disable_cache=True,  # Caching is disabled as Ray processes transformations lazily
        )

    @dispatcher.span
    defrun(
        self,
        show_progress: bool = False,
        documents: Optional[List[Document]] = None,
        nodes: Optional[Sequence[BaseNode]] = None,
        store_doc_text: bool = True,
        **kwargs: Any,
    ) -> Sequence[BaseNode]:
"""
        Run a series of transformations on a set of nodes.

        If a vector store is provided, nodes with embeddings will be added to the vector store.

        If a vector store + docstore are provided, the docstore will be used to de-duplicate documents.

        Args:
            show_progress (bool, optional): Shows execution progress bar(s). Defaults to False.
            documents (Optional[List[Document]], optional): Set of documents to be transformed. Defaults to None.
            nodes (Optional[Sequence[BaseNode]], optional): Set of nodes to be transformed. Defaults to None.
            store_doc_text (bool, optional): Whether to store the document texts. Defaults to True.

        Returns:
            Sequence[BaseNode]: The set of transformed Nodes/Documents

        """
        input_nodes = self._prepare_inputs(documents, nodes)

        # check if we need to dedup
        if self.docstore is not None and self.vector_store is not None:
            if self.docstore_strategy in (
                DocstoreStrategy.UPSERTS,
                DocstoreStrategy.UPSERTS_AND_DELETE,
            ):
                nodes_to_run = self._handle_upserts(input_nodes)
            elif self.docstore_strategy == DocstoreStrategy.DUPLICATES_ONLY:
                nodes_to_run = self._handle_duplicates(input_nodes)
            else:
                raise ValueError(f"Invalid docstore strategy: {self.docstore_strategy}")
        elif self.docstore is not None and self.vector_store is None:
            if self.docstore_strategy == DocstoreStrategy.UPSERTS:
                logger.info(
                    "Docstore strategy set to upserts, but no vector store. "
                    "Switching to duplicates_only strategy."
                )
                self.docstore_strategy = DocstoreStrategy.DUPLICATES_ONLY
            elif self.docstore_strategy == DocstoreStrategy.UPSERTS_AND_DELETE:
                logger.info(
                    "Docstore strategy set to upserts and delete, but no vector store. "
                    "Switching to duplicates_only strategy."
                )
                self.docstore_strategy = DocstoreStrategy.DUPLICATES_ONLY
            nodes_to_run = self._handle_duplicates(input_nodes)
        else:
            nodes_to_run = input_nodes

        nodes = run_transformations(
            nodes_to_run,
            self.transformations,
            show_progress=show_progress,
            **kwargs,
        )

        if self.vector_store is not None:
            nodes_with_embeddings = [n for n in nodes if n.embedding is not None]
            if nodes_with_embeddings:
                self.vector_store.add(nodes_with_embeddings)

        if self.docstore is not None:
            self._update_docstore(nodes_to_run, store_doc_text=store_doc_text)

        return nodes

    @dispatcher.span
    async defarun(
        self,
        show_progress: bool = False,
        documents: Optional[List[Document]] = None,
        nodes: Optional[Sequence[BaseNode]] = None,
        store_doc_text: bool = True,
        **kwargs: Any,
    ) -> Sequence[BaseNode]:
"""
        Run a series of transformations on a set of nodes.

        If a vector store is provided, nodes with embeddings will be added to the vector store.

        If a vector store + docstore are provided, the docstore will be used to de-duplicate documents.

        Args:
            show_progress (bool, optional): Shows execution progress bar(s). Defaults to False.
            documents (Optional[List[Document]], optional): Set of documents to be transformed. Defaults to None.
            nodes (Optional[Sequence[BaseNode]], optional): Set of nodes to be transformed. Defaults to None.
            store_doc_text (bool, optional): Whether to store the document texts. Defaults to True.

        Returns:
            Sequence[BaseNode]: The set of transformed Nodes/Documents

        """
        input_nodes = self._prepare_inputs(documents, nodes)

        # check if we need to dedup
        if self.docstore is not None and self.vector_store is not None:
            if self.docstore_strategy in (
                DocstoreStrategy.UPSERTS,
                DocstoreStrategy.UPSERTS_AND_DELETE,
            ):
                nodes_to_run = await self._ahandle_upserts(
                    input_nodes, store_doc_text=store_doc_text
                )
            elif self.docstore_strategy == DocstoreStrategy.DUPLICATES_ONLY:
                nodes_to_run = await self._ahandle_duplicates(
                    input_nodes, store_doc_text=store_doc_text
                )
            else:
                raise ValueError(f"Invalid docstore strategy: {self.docstore_strategy}")
        elif self.docstore is not None and self.vector_store is None:
            if self.docstore_strategy == DocstoreStrategy.UPSERTS:
                logger.info(
                    "Docstore strategy set to upserts, but no vector store. "
                    "Switching to duplicates_only strategy."
                )
                self.docstore_strategy = DocstoreStrategy.DUPLICATES_ONLY
            elif self.docstore_strategy == DocstoreStrategy.UPSERTS_AND_DELETE:
                logger.info(
                    "Docstore strategy set to upserts and delete, but no vector store. "
                    "Switching to duplicates_only strategy."
                )
                self.docstore_strategy = DocstoreStrategy.DUPLICATES_ONLY
            nodes_to_run = await self._ahandle_duplicates(
                input_nodes, store_doc_text=store_doc_text
            )

        else:
            nodes_to_run = input_nodes

        nodes = await arun_transformations(  # type: ignore
            nodes_to_run,
            self.transformations,
            show_progress=show_progress,
            **kwargs,
        )

        if self.vector_store is not None:
            nodes_with_embeddings = [n for n in nodes if n.embedding is not None]
            if nodes_with_embeddings:
                await self.vector_store.async_add(nodes_with_embeddings)

        if self.docstore is not None:
            await self._aupdate_docstore(nodes_to_run, store_doc_text=store_doc_text)

        return nodes

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/ray/#llama_index.ingestion.ray.RayIngestionPipeline.run "Permanent link")

```
run(
    show_progress:  = False,
    documents: Optional[[]] = None,
    nodes: Optional[Sequence[]] = None,
    store_doc_text:  = True,
    **kwargs: 
) -> Sequence[]

```

Run a series of transformations on a set of nodes.
If a vector store is provided, nodes with embeddings will be added to the vector store.
If a vector store + docstore are provided, the docstore will be used to de-duplicate documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `show_progress`  |  `bool`  |  Shows execution progress bar(s). Defaults to False.  |  `False`  |  
|  `documents`  |  `Optional[List[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]]`  |  Set of documents to be transformed. Defaults to None.  |  `None`  |  
|  `nodes`  |  `Optional[Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]]`  |  Set of nodes to be transformed. Defaults to None.  |  `None`  |  
|  `store_doc_text`  |  `bool`  |  Whether to store the document texts. Defaults to True.  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]`  |  Sequence[BaseNode]: The set of transformed Nodes/Documents  |  
Source code in `llama-index-integrations/ingestion/llama-index-ingestion-ray/llama_index/ingestion/ray/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defrun(
    self,
    show_progress: bool = False,
    documents: Optional[List[Document]] = None,
    nodes: Optional[Sequence[BaseNode]] = None,
    store_doc_text: bool = True,
    **kwargs: Any,
) -> Sequence[BaseNode]:
"""
    Run a series of transformations on a set of nodes.

    If a vector store is provided, nodes with embeddings will be added to the vector store.

    If a vector store + docstore are provided, the docstore will be used to de-duplicate documents.

    Args:
        show_progress (bool, optional): Shows execution progress bar(s). Defaults to False.
        documents (Optional[List[Document]], optional): Set of documents to be transformed. Defaults to None.
        nodes (Optional[Sequence[BaseNode]], optional): Set of nodes to be transformed. Defaults to None.
        store_doc_text (bool, optional): Whether to store the document texts. Defaults to True.

    Returns:
        Sequence[BaseNode]: The set of transformed Nodes/Documents

    """
    input_nodes = self._prepare_inputs(documents, nodes)

    # check if we need to dedup
    if self.docstore is not None and self.vector_store is not None:
        if self.docstore_strategy in (
            DocstoreStrategy.UPSERTS,
            DocstoreStrategy.UPSERTS_AND_DELETE,
        ):
            nodes_to_run = self._handle_upserts(input_nodes)
        elif self.docstore_strategy == DocstoreStrategy.DUPLICATES_ONLY:
            nodes_to_run = self._handle_duplicates(input_nodes)
        else:
            raise ValueError(f"Invalid docstore strategy: {self.docstore_strategy}")
    elif self.docstore is not None and self.vector_store is None:
        if self.docstore_strategy == DocstoreStrategy.UPSERTS:
            logger.info(
                "Docstore strategy set to upserts, but no vector store. "
                "Switching to duplicates_only strategy."
            )
            self.docstore_strategy = DocstoreStrategy.DUPLICATES_ONLY
        elif self.docstore_strategy == DocstoreStrategy.UPSERTS_AND_DELETE:
            logger.info(
                "Docstore strategy set to upserts and delete, but no vector store. "
                "Switching to duplicates_only strategy."
            )
            self.docstore_strategy = DocstoreStrategy.DUPLICATES_ONLY
        nodes_to_run = self._handle_duplicates(input_nodes)
    else:
        nodes_to_run = input_nodes

    nodes = run_transformations(
        nodes_to_run,
        self.transformations,
        show_progress=show_progress,
        **kwargs,
    )

    if self.vector_store is not None:
        nodes_with_embeddings = [n for n in nodes if n.embedding is not None]
        if nodes_with_embeddings:
            self.vector_store.add(nodes_with_embeddings)

    if self.docstore is not None:
        self._update_docstore(nodes_to_run, store_doc_text=store_doc_text)

    return nodes

```
 |  
| --- | --- |  
###  arun [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/ray/#llama_index.ingestion.ray.RayIngestionPipeline.arun "Permanent link")

```
arun(
    show_progress:  = False,
    documents: Optional[[]] = None,
    nodes: Optional[Sequence[]] = None,
    store_doc_text:  = True,
    **kwargs: 
) -> Sequence[]

```

Run a series of transformations on a set of nodes.
If a vector store is provided, nodes with embeddings will be added to the vector store.
If a vector store + docstore are provided, the docstore will be used to de-duplicate documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `show_progress`  |  `bool`  |  Shows execution progress bar(s). Defaults to False.  |  `False`  |  
|  `documents`  |  `Optional[List[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]]`  |  Set of documents to be transformed. Defaults to None.  |  `None`  |  
|  `nodes`  |  `Optional[Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]]`  |  Set of nodes to be transformed. Defaults to None.  |  `None`  |  
|  `store_doc_text`  |  `bool`  |  Whether to store the document texts. Defaults to True.  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]`  |  Sequence[BaseNode]: The set of transformed Nodes/Documents  |  
Source code in `llama-index-integrations/ingestion/llama-index-ingestion-ray/llama_index/ingestion/ray/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
async defarun(
    self,
    show_progress: bool = False,
    documents: Optional[List[Document]] = None,
    nodes: Optional[Sequence[BaseNode]] = None,
    store_doc_text: bool = True,
    **kwargs: Any,
) -> Sequence[BaseNode]:
"""
    Run a series of transformations on a set of nodes.

    If a vector store is provided, nodes with embeddings will be added to the vector store.

    If a vector store + docstore are provided, the docstore will be used to de-duplicate documents.

    Args:
        show_progress (bool, optional): Shows execution progress bar(s). Defaults to False.
        documents (Optional[List[Document]], optional): Set of documents to be transformed. Defaults to None.
        nodes (Optional[Sequence[BaseNode]], optional): Set of nodes to be transformed. Defaults to None.
        store_doc_text (bool, optional): Whether to store the document texts. Defaults to True.

    Returns:
        Sequence[BaseNode]: The set of transformed Nodes/Documents

    """
    input_nodes = self._prepare_inputs(documents, nodes)

    # check if we need to dedup
    if self.docstore is not None and self.vector_store is not None:
        if self.docstore_strategy in (
            DocstoreStrategy.UPSERTS,
            DocstoreStrategy.UPSERTS_AND_DELETE,
        ):
            nodes_to_run = await self._ahandle_upserts(
                input_nodes, store_doc_text=store_doc_text
            )
        elif self.docstore_strategy == DocstoreStrategy.DUPLICATES_ONLY:
            nodes_to_run = await self._ahandle_duplicates(
                input_nodes, store_doc_text=store_doc_text
            )
        else:
            raise ValueError(f"Invalid docstore strategy: {self.docstore_strategy}")
    elif self.docstore is not None and self.vector_store is None:
        if self.docstore_strategy == DocstoreStrategy.UPSERTS:
            logger.info(
                "Docstore strategy set to upserts, but no vector store. "
                "Switching to duplicates_only strategy."
            )
            self.docstore_strategy = DocstoreStrategy.DUPLICATES_ONLY
        elif self.docstore_strategy == DocstoreStrategy.UPSERTS_AND_DELETE:
            logger.info(
                "Docstore strategy set to upserts and delete, but no vector store. "
                "Switching to duplicates_only strategy."
            )
            self.docstore_strategy = DocstoreStrategy.DUPLICATES_ONLY
        nodes_to_run = await self._ahandle_duplicates(
            input_nodes, store_doc_text=store_doc_text
        )

    else:
        nodes_to_run = input_nodes

    nodes = await arun_transformations(  # type: ignore
        nodes_to_run,
        self.transformations,
        show_progress=show_progress,
        **kwargs,
    )

    if self.vector_store is not None:
        nodes_with_embeddings = [n for n in nodes if n.embedding is not None]
        if nodes_with_embeddings:
            await self.vector_store.async_add(nodes_with_embeddings)

    if self.docstore is not None:
        await self._aupdate_docstore(nodes_to_run, store_doc_text=store_doc_text)

    return nodes

```
 |  
| --- | --- |  
##  RayTransformComponent [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/ray/#llama_index.ingestion.ray.RayTransformComponent "Permanent link")
Bases: `BaseModel`
A wrapper around transformations that enables execution in Ray.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `transform_class`  |  `Type[TransformComponent[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TransformComponent "TransformComponent \(llama_index.core.schema.TransformComponent\)")]`  |  The transformation class to wrap.  |  _required_  |  
|  `transform_kwargs`  |  `Optional[Dict[str, Any]]`  |  The keyword arguments to pass to the transformation **init** function.  |  `None`  |  
|  `map_batches_kwargs`  |  `Optional[Dict[str, Any]]`  |  The keyword arguments to pass to ray.data.Dataset.map_batches (see https://docs.ray.io/en/latest/data/api/doc/ray.data.Dataset.map_batches.html for details)  |  `None`  |  
Source code in `llama-index-integrations/ingestion/llama-index-ingestion-ray/llama_index/ingestion/ray/transform.py`  
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
74
75
76
```
 | 
```
classRayTransformComponent(BaseModel):
"""
    A wrapper around transformations that enables execution in Ray.

    Args:
        transform_class (Type[TransformComponent]): The transformation class to wrap.
        transform_kwargs (Optional[Dict[str, Any]], optional): The keyword arguments to pass to the transformation __init__ function.
        map_batches_kwargs (Optional[Dict[str, Any]], optional): The keyword arguments to pass to ray.data.Dataset.map_batches (see https://docs.ray.io/en/latest/data/api/doc/ray.data.Dataset.map_batches.html for details)

    """

    transform_class: Type[TransformComponent]
    transform_kwargs: Dict[str, Any]
    map_batches_kwargs: Dict[str, Any]

    def__init__(
        self,
        transform_class: Type[TransformComponent],
        map_batches_kwargs: Optional[Dict[str, Any]] = None,
        transform_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            transform_class=transform_class,
            transform_kwargs=transform_kwargs or kwargs,
            map_batches_kwargs=map_batches_kwargs or {},
        )

    def__call__(self, dataset: ray.data.Dataset, **kwargs) -> ray.data.Dataset:
"""Run the transformation on the given ray dataset."""
        return dataset.map_batches(
            TransformActor,
            fn_constructor_kwargs={
                "transform_class": self.transform_class,
                "transform_kwargs": self.transform_kwargs,
            },
            fn_kwargs=kwargs,
            batch_format="pyarrow",
            **self.map_batches_kwargs,
        )

```
 |  
| --- | --- |  
options: members: - RayIngestionPipeline
