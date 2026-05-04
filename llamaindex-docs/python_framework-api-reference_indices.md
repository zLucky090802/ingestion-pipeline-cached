# Index
Base index classes.
##  BaseIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "Permanent link")
Bases: `Generic[IS]`, 
Base LlamaIndex.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `List[Node]`  |  List of nodes to index  |  `None`  |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/base.py`  
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
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
```
 | 
```
classBaseIndex(Generic[IS], ABC):
"""
    Base LlamaIndex.

    Args:
        nodes (List[Node]): List of nodes to index
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.

    """

    index_struct_cls: Type[IS]

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[IS] = None,
        storage_context: Optional[StorageContext] = None,
        callback_manager: Optional[CallbackManager] = None,
        transformations: Optional[List[TransformComponent]] = None,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize with parameters."""
        if index_struct is None and nodes is None and objects is None:
            raise ValueError("One of nodes, objects, or index_struct must be provided.")
        if index_struct is not None and nodes is not None and len(nodes) >= 1:
            raise ValueError("Only one of nodes or index_struct can be provided.")
        # This is to explicitly make sure that the old UX is not used
        if nodes is not None and len(nodes) >= 1 and not isinstance(nodes[0], BaseNode):
            if isinstance(nodes[0], Document):
                raise ValueError(
                    "The constructor now takes in a list of Node objects. "
                    "Since you are passing in a list of Document objects, "
                    "please use `from_documents` instead."
                )
            else:
                raise ValueError("nodes must be a list of Node objects.")

        self._storage_context = storage_context or StorageContext.from_defaults()
        self._docstore = self._storage_context.docstore
        self._show_progress = show_progress
        self._vector_store = self._storage_context.vector_store
        self._graph_store = self._storage_context.graph_store
        self._callback_manager = callback_manager or Settings.callback_manager

        objects = objects or []
        self._object_map = {obj.index_id: obj.obj for obj in objects}
        for obj in objects:
            obj.obj = None  # clear the object to avoid serialization issues

        with self._callback_manager.as_trace("index_construction"):
            if index_struct is None:
                nodes = nodes or []
                index_struct = self.build_index_from_nodes(
                    nodes + objects,  # type: ignore
                    **kwargs,  # type: ignore
                )
            self._index_struct = index_struct
            self._storage_context.index_store.add_index_struct(self._index_struct)

        self._transformations = transformations or Settings.transformations

    @classmethod
    deffrom_documents(
        cls: Type[IndexType],
        documents: Sequence[Document],
        storage_context: Optional[StorageContext] = None,
        show_progress: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        transformations: Optional[List[TransformComponent]] = None,
        **kwargs: Any,
    ) -> IndexType:
"""
        Create index from documents.

        Args:
            documents (Sequence[Document]]): List of documents to
                build the index from.

        """
        storage_context = storage_context or StorageContext.from_defaults()
        docstore = storage_context.docstore
        callback_manager = callback_manager or Settings.callback_manager
        transformations = transformations or Settings.transformations

        with callback_manager.as_trace("index_construction"):
            for doc in documents:
                docstore.set_document_hash(doc.id_, doc.hash)

            nodes = run_transformations(
                documents,  # type: ignore
                transformations,
                show_progress=show_progress,
                **kwargs,
            )

            return cls(
                nodes=nodes,
                storage_context=storage_context,
                callback_manager=callback_manager,
                show_progress=show_progress,
                transformations=transformations,
                **kwargs,
            )

    @property
    defindex_struct(self) -> IS:
"""Get the index struct."""
        return self._index_struct

    @property
    defindex_id(self) -> str:
"""Get the index struct."""
        return self._index_struct.index_id

    defset_index_id(self, index_id: str) -> None:
"""
        Set the index id.

        NOTE: if you decide to set the index_id on the index_struct manually,
        you will need to explicitly call `add_index_struct` on the `index_store`
        to update the index store.

        Args:
            index_id (str): Index id to set.

        """
        # delete the old index struct
        old_id = self._index_struct.index_id
        self._storage_context.index_store.delete_index_struct(old_id)
        # add the new index struct
        self._index_struct.index_id = index_id
        self._storage_context.index_store.add_index_struct(self._index_struct)

    @property
    defdocstore(self) -> BaseDocumentStore:
"""Get the docstore corresponding to the index."""
        return self._docstore

    @property
    defstorage_context(self) -> StorageContext:
        return self._storage_context

    @property
    defsummary(self) -> str:
        return str(self._index_struct.summary)

    @summary.setter
    defsummary(self, new_summary: str) -> None:
        self._index_struct.summary = new_summary
        self._storage_context.index_store.add_index_struct(self._index_struct)

    @abstractmethod
    def_build_index_from_nodes(
        self, nodes: Sequence[BaseNode], **build_kwargs: Any
    ) -> IS:
"""Build the index from nodes."""

    defbuild_index_from_nodes(
        self, nodes: Sequence[BaseNode], **build_kwargs: Any
    ) -> IS:
"""Build the index from nodes."""
        self._docstore.add_documents(nodes, allow_update=True)
        return self._build_index_from_nodes(nodes, **build_kwargs)

    @abstractmethod
    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Index-specific logic for inserting nodes to the index struct."""

    definsert_nodes(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert nodes."""
        for node in nodes:
            if isinstance(node, IndexNode):
                try:
                    node.dict()
                except ValueError:
                    self._object_map[node.index_id] = node.obj
                    node.obj = None

        with self._callback_manager.as_trace("insert_nodes"):
            self.docstore.add_documents(nodes, allow_update=True)
            self._insert(nodes, **insert_kwargs)
            self._storage_context.index_store.add_index_struct(self._index_struct)

    async defainsert_nodes(
        self, nodes: Sequence[BaseNode], **insert_kwargs: Any
    ) -> None:
"""Asynchronously insert nodes."""
        for node in nodes:
            if isinstance(node, IndexNode):
                try:
                    node.dict()
                except ValueError:
                    self._object_map[node.index_id] = node.obj
                    node.obj = None

        with self._callback_manager.as_trace("ainsert_nodes"):
            await self.docstore.async_add_documents(nodes, allow_update=True)
            self._insert(nodes=nodes)
            await self._storage_context.index_store.async_add_index_struct(
                self._index_struct
            )

    definsert(self, document: Document, **insert_kwargs: Any) -> None:
"""Insert a document."""
        with self._callback_manager.as_trace("insert"):
            nodes = run_transformations(
                [document],
                self._transformations,
                show_progress=self._show_progress,
                **insert_kwargs,
            )

            self.insert_nodes(nodes, **insert_kwargs)
            self.docstore.set_document_hash(document.id_, document.hash)

    async defainsert(self, document: Document, **insert_kwargs: Any) -> None:
"""Asynchronously insert a document."""
        with self._callback_manager.as_trace("ainsert"):
            nodes = await arun_transformations(
                [document],
                self._transformations,
                show_progress=self._show_progress,
                **insert_kwargs,
            )

            await self.ainsert_nodes(nodes, **insert_kwargs)
            await self.docstore.aset_document_hash(document.id_, document.hash)

    @abstractmethod
    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
"""Delete a node."""

    defdelete_nodes(
        self,
        node_ids: List[str],
        delete_from_docstore: bool = False,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete a list of nodes from the index.

        Args:
            doc_ids (List[str]): A list of doc_ids from the nodes to delete

        """
        for node_id in node_ids:
            self._delete_node(node_id, **delete_kwargs)
            if delete_from_docstore:
                self.docstore.delete_document(node_id, raise_error=False)

        self._storage_context.index_store.add_index_struct(self._index_struct)

    async defadelete_nodes(
        self,
        node_ids: List[str],
        delete_from_docstore: bool = False,
        **delete_kwargs: Any,
    ) -> None:
"""
        Asynchronously delete a list of nodes from the index.

        Args:
            doc_ids (List[str]): A list of doc_ids from the nodes to delete

        """
        for node_id in node_ids:
            self._delete_node(node_id, **delete_kwargs)
            if delete_from_docstore:
                await self.docstore.adelete_document(node_id, raise_error=False)

        await self._storage_context.index_store.async_add_index_struct(
            self._index_struct
        )

    defdelete(self, doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete a document from the index.
        All nodes in the index related to the index will be deleted.

        Args:
            doc_id (str): A doc_id of the ingested document

        """
        logger.warning(
            "delete() is now deprecated, please refer to delete_ref_doc() to delete "
            "ingested documents+nodes or delete_nodes to delete a list of nodes."
            "Use adelete_ref_docs() for an asynchronous implementation"
        )
        self.delete_ref_doc(doc_id)

    defdelete_ref_doc(
        self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
    ) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
        ref_doc_info = self.docstore.get_ref_doc_info(ref_doc_id)
        if ref_doc_info is None:
            logger.warning(f"ref_doc_id {ref_doc_id} not found, nothing deleted.")
            return

        self.delete_nodes(
            ref_doc_info.node_ids,
            delete_from_docstore=delete_from_docstore,
            **delete_kwargs,
        )

        if delete_from_docstore:
            self.docstore.delete_ref_doc(ref_doc_id, raise_error=False)

    async defadelete_ref_doc(
        self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
    ) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
        ref_doc_info = await self.docstore.aget_ref_doc_info(ref_doc_id)
        if ref_doc_info is None:
            logger.warning(f"ref_doc_id {ref_doc_id} not found, nothing deleted.")
            return

        await self.adelete_nodes(
            ref_doc_info.node_ids,
            delete_from_docstore=delete_from_docstore,
            **delete_kwargs,
        )

        if delete_from_docstore:
            await self.docstore.adelete_ref_doc(ref_doc_id, raise_error=False)

    defupdate(self, document: Document, **update_kwargs: Any) -> None:
"""
        Update a document and it's corresponding nodes.

        This is equivalent to deleting the document and then inserting it again.

        Args:
            document (Union[BaseDocument, BaseIndex]): document to update
            insert_kwargs (Dict): kwargs to pass to insert
            delete_kwargs (Dict): kwargs to pass to delete

        """
        logger.warning(
            "update() is now deprecated, please refer to update_ref_doc() to update "
            "ingested documents+nodes."
            "Use aupdate_ref_docs() for an asynchronous implementation"
        )
        self.update_ref_doc(document, **update_kwargs)

    defupdate_ref_doc(self, document: Document, **update_kwargs: Any) -> None:
"""
        Update a document and it's corresponding nodes.

        This is equivalent to deleting the document and then inserting it again.

        Args:
            document (Union[BaseDocument, BaseIndex]): document to update
            insert_kwargs (Dict): kwargs to pass to insert
            delete_kwargs (Dict): kwargs to pass to delete

        """
        with self._callback_manager.as_trace("update_ref_doc"):
            self.delete_ref_doc(
                document.id_,
                delete_from_docstore=True,
                **update_kwargs.pop("delete_kwargs", {}),
            )
            self.insert(document, **update_kwargs.pop("insert_kwargs", {}))

    async defaupdate_ref_doc(self, document: Document, **update_kwargs: Any) -> None:
"""
        Asynchronously update a document and it's corresponding nodes.

        This is equivalent to deleting the document and then inserting it again.

        Args:
            document (Union[BaseDocument, BaseIndex]): document to update
            insert_kwargs (Dict): kwargs to pass to insert
            delete_kwargs (Dict): kwargs to pass to delete

        """
        with self._callback_manager.as_trace("aupdate_ref_doc"):
            await self.adelete_ref_doc(
                document.id_,
                delete_from_docstore=True,
                **update_kwargs.pop("delete_kwargs", {}),
            )
            await self.ainsert(document, **update_kwargs.pop("insert_kwargs", {}))

    defrefresh(
        self, documents: Sequence[Document], **update_kwargs: Any
    ) -> List[bool]:
"""
        Refresh an index with documents that have changed.

        This allows users to save LLM and Embedding model calls, while only
        updating documents that have any changes in text or metadata. It
        will also insert any documents that previously were not stored.
        """
        logger.warning(
            "refresh() is now deprecated, please refer to refresh_ref_docs() to "
            "refresh ingested documents+nodes with an updated list of documents."
            "Use arefresh_ref_docs() for an asynchronous implementation"
        )
        return self.refresh_ref_docs(documents, **update_kwargs)

    defrefresh_ref_docs(
        self, documents: Sequence[Document], **update_kwargs: Any
    ) -> List[bool]:
"""
        Refresh an index with documents that have changed.

        This allows users to save LLM and Embedding model calls, while only
        updating documents that have any changes in text or metadata. It
        will also insert any documents that previously were not stored.
        """
        with self._callback_manager.as_trace("refresh_ref_docs"):
            refreshed_documents = [False] * len(documents)
            for i, document in enumerate(documents):
                existing_doc_hash = self._docstore.get_document_hash(document.id_)
                if existing_doc_hash is None:
                    self.insert(document, **update_kwargs.pop("insert_kwargs", {}))
                    refreshed_documents[i] = True
                elif existing_doc_hash != document.hash:
                    self.update_ref_doc(
                        document, **update_kwargs.pop("update_kwargs", {})
                    )
                    refreshed_documents[i] = True

            return refreshed_documents

    async defarefresh_ref_docs(
        self, documents: Sequence[Document], **update_kwargs: Any
    ) -> List[bool]:
"""
        Asynchronously refresh an index with documents that have changed.

        This allows users to save LLM and Embedding model calls, while only
        updating documents that have any changes in text or metadata. It
        will also insert any documents that previously were not stored.
        """
        with self._callback_manager.as_trace("arefresh_ref_docs"):
            refreshed_documents = [False] * len(documents)
            for i, document in enumerate(documents):
                existing_doc_hash = await self._docstore.aget_document_hash(
                    document.id_
                )
                if existing_doc_hash is None:
                    await self.ainsert(
                        document, **update_kwargs.pop("insert_kwargs", {})
                    )
                    refreshed_documents[i] = True
                elif existing_doc_hash != document.hash:
                    await self.aupdate_ref_doc(
                        document, **update_kwargs.pop("update_kwargs", {})
                    )
                    refreshed_documents[i] = True
            return refreshed_documents

    @property
    @abstractmethod
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        ...

    @abstractmethod
    defas_retriever(self, **kwargs: Any) -> BaseRetriever: ...

    defas_query_engine(
        self, llm: Optional[LLMType] = None, **kwargs: Any
    ) -> BaseQueryEngine:
"""
        Convert the index to a query engine.

        Calls `index.as_retriever(**kwargs)` to get the retriever and then wraps it in a
        `RetrieverQueryEngine.from_args(retriever, **kwrags)` call.
        """
        # NOTE: lazy import
        fromllama_index.core.query_engine.retriever_query_engineimport (
            RetrieverQueryEngine,
        )

        retriever = self.as_retriever(**kwargs)
        llm = (
            resolve_llm(llm, callback_manager=self._callback_manager)
            if llm
            else Settings.llm
        )

        return RetrieverQueryEngine.from_args(
            retriever,
            llm=llm,
            **kwargs,
        )

    defas_chat_engine(
        self,
        chat_mode: ChatMode = ChatMode.BEST,
        llm: Optional[LLMType] = None,
        **kwargs: Any,
    ) -> BaseChatEngine:
"""
        Convert the index to a chat engine.

        Calls `index.as_query_engine(llm=llm, **kwargs)` to get the query engine and then
        wraps it in a chat engine based on the chat mode.

        Chat modes:
            - `ChatMode.BEST` (default): Chat engine that uses an agent (react or openai) with a query engine tool
            - `ChatMode.CONTEXT`: Chat engine that uses a retriever to get context
            - `ChatMode.CONDENSE_QUESTION`: Chat engine that condenses questions
            - `ChatMode.CONDENSE_PLUS_CONTEXT`: Chat engine that condenses questions and uses a retriever to get context
            - `ChatMode.SIMPLE`: Simple chat engine that uses the LLM directly
            - `ChatMode.REACT`: Chat engine that uses a react agent with a query engine tool
            - `ChatMode.OPENAI`: Chat engine that uses an openai agent with a query engine tool
        """
        llm = (
            resolve_llm(llm, callback_manager=self._callback_manager)
            if llm
            else Settings.llm
        )

        query_engine = self.as_query_engine(llm=llm, **kwargs)

        # resolve chat mode
        if chat_mode in [ChatMode.REACT, ChatMode.OPENAI]:
            raise ValueError(
                "ChatMode.REACT and ChatMode.OPENAI are now deprecated and removed. "
                "Please use the ReActAgent or FunctionAgent classes from llama_index.core.agent.workflow "
                "to create an agent with a query engine tool."
            )

        if chat_mode == ChatMode.CONDENSE_QUESTION:
            # NOTE: lazy import
            fromllama_index.core.chat_engineimport CondenseQuestionChatEngine

            return CondenseQuestionChatEngine.from_defaults(
                query_engine=query_engine,
                llm=llm,
                **kwargs,
            )

        elif chat_mode == ChatMode.CONTEXT:
            fromllama_index.core.chat_engineimport ContextChatEngine

            return ContextChatEngine.from_defaults(
                retriever=self.as_retriever(**kwargs),
                llm=llm,
                **kwargs,
            )

        elif chat_mode in [ChatMode.CONDENSE_PLUS_CONTEXT, ChatMode.BEST]:
            fromllama_index.core.chat_engineimport CondensePlusContextChatEngine

            return CondensePlusContextChatEngine.from_defaults(
                retriever=self.as_retriever(**kwargs),
                llm=llm,
                **kwargs,
            )

        elif chat_mode == ChatMode.SIMPLE:
            fromllama_index.core.chat_engineimport SimpleChatEngine

            return SimpleChatEngine.from_defaults(
                llm=llm,
                **kwargs,
            )
        else:
            raise ValueError(f"Unknown chat mode: {chat_mode}")

```
 |  
| --- | --- |  
###  index_struct `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.index_struct "Permanent link")

```
index_struct: 

```

Get the index struct.
###  index_id `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.index_id "Permanent link")

```
index_id: 

```

Get the index struct.
###  docstore `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.docstore "Permanent link")

```
docstore: 

```

Get the docstore corresponding to the index.
###  ref_doc_info `abstractmethod` `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
###  from_documents `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.from_documents "Permanent link")

```
from_documents(
    documents: Sequence[],
    storage_context: Optional[] = None,
    show_progress:  = False,
    callback_manager: Optional[] = None,
    transformations: Optional[
        []
    ] = None,
    **kwargs: 
) -> IndexType

```

Create index from documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `documents`  |  `Sequence[Document]]`  |  List of documents to build the index from.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/base.py`  
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
```
 | 
```
@classmethod
deffrom_documents(
    cls: Type[IndexType],
    documents: Sequence[Document],
    storage_context: Optional[StorageContext] = None,
    show_progress: bool = False,
    callback_manager: Optional[CallbackManager] = None,
    transformations: Optional[List[TransformComponent]] = None,
    **kwargs: Any,
) -> IndexType:
"""
    Create index from documents.

    Args:
        documents (Sequence[Document]]): List of documents to
            build the index from.

    """
    storage_context = storage_context or StorageContext.from_defaults()
    docstore = storage_context.docstore
    callback_manager = callback_manager or Settings.callback_manager
    transformations = transformations or Settings.transformations

    with callback_manager.as_trace("index_construction"):
        for doc in documents:
            docstore.set_document_hash(doc.id_, doc.hash)

        nodes = run_transformations(
            documents,  # type: ignore
            transformations,
            show_progress=show_progress,
            **kwargs,
        )

        return cls(
            nodes=nodes,
            storage_context=storage_context,
            callback_manager=callback_manager,
            show_progress=show_progress,
            transformations=transformations,
            **kwargs,
        )

```
 |  
| --- | --- |  
###  set_index_id [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.set_index_id "Permanent link")

```
set_index_id(index_id: ) -> None

```

Set the index id.
NOTE: if you decide to set the index_id on the index_struct manually, you will need to explicitly call `add_index_struct` on the `index_store` to update the index store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index_id`  |  Index id to set.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
defset_index_id(self, index_id: str) -> None:
"""
    Set the index id.

    NOTE: if you decide to set the index_id on the index_struct manually,
    you will need to explicitly call `add_index_struct` on the `index_store`
    to update the index store.

    Args:
        index_id (str): Index id to set.

    """
    # delete the old index struct
    old_id = self._index_struct.index_id
    self._storage_context.index_store.delete_index_struct(old_id)
    # add the new index struct
    self._index_struct.index_id = index_id
    self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  build_index_from_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.build_index_from_nodes "Permanent link")

```
build_index_from_nodes(
    nodes: Sequence[], **build_kwargs: 
) -> 

```

Build the index from nodes.
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
184
185
186
187
188
189
```
 | 
```
defbuild_index_from_nodes(
    self, nodes: Sequence[BaseNode], **build_kwargs: Any
) -> IS:
"""Build the index from nodes."""
    self._docstore.add_documents(nodes, allow_update=True)
    return self._build_index_from_nodes(nodes, **build_kwargs)

```
 |  
| --- | --- |  
###  insert_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.insert_nodes "Permanent link")

```
insert_nodes(
    nodes: Sequence[], **insert_kwargs: 
) -> None

```

Insert nodes.
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
definsert_nodes(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert nodes."""
    for node in nodes:
        if isinstance(node, IndexNode):
            try:
                node.dict()
            except ValueError:
                self._object_map[node.index_id] = node.obj
                node.obj = None

    with self._callback_manager.as_trace("insert_nodes"):
        self.docstore.add_documents(nodes, allow_update=True)
        self._insert(nodes, **insert_kwargs)
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  ainsert_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.ainsert_nodes "Permanent link")

```
ainsert_nodes(
    nodes: Sequence[], **insert_kwargs: 
) -> None

```

Asynchronously insert nodes.
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
async defainsert_nodes(
    self, nodes: Sequence[BaseNode], **insert_kwargs: Any
) -> None:
"""Asynchronously insert nodes."""
    for node in nodes:
        if isinstance(node, IndexNode):
            try:
                node.dict()
            except ValueError:
                self._object_map[node.index_id] = node.obj
                node.obj = None

    with self._callback_manager.as_trace("ainsert_nodes"):
        await self.docstore.async_add_documents(nodes, allow_update=True)
        self._insert(nodes=nodes)
        await self._storage_context.index_store.async_add_index_struct(
            self._index_struct
        )

```
 |  
| --- | --- |  
###  insert [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.insert "Permanent link")

```
insert(document: , **insert_kwargs: ) -> None

```

Insert a document.
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
definsert(self, document: Document, **insert_kwargs: Any) -> None:
"""Insert a document."""
    with self._callback_manager.as_trace("insert"):
        nodes = run_transformations(
            [document],
            self._transformations,
            show_progress=self._show_progress,
            **insert_kwargs,
        )

        self.insert_nodes(nodes, **insert_kwargs)
        self.docstore.set_document_hash(document.id_, document.hash)

```
 |  
| --- | --- |  
###  ainsert [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.ainsert "Permanent link")

```
ainsert(document: , **insert_kwargs: ) -> None

```

Asynchronously insert a document.
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
async defainsert(self, document: Document, **insert_kwargs: Any) -> None:
"""Asynchronously insert a document."""
    with self._callback_manager.as_trace("ainsert"):
        nodes = await arun_transformations(
            [document],
            self._transformations,
            show_progress=self._show_progress,
            **insert_kwargs,
        )

        await self.ainsert_nodes(nodes, **insert_kwargs)
        await self.docstore.aset_document_hash(document.id_, document.hash)

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: [],
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a list of nodes from the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `doc_ids`  |  `List[str]`  |  A list of doc_ids from the nodes to delete  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
defdelete_nodes(
    self,
    node_ids: List[str],
    delete_from_docstore: bool = False,
    **delete_kwargs: Any,
) -> None:
"""
    Delete a list of nodes from the index.

    Args:
        doc_ids (List[str]): A list of doc_ids from the nodes to delete

    """
    for node_id in node_ids:
        self._delete_node(node_id, **delete_kwargs)
        if delete_from_docstore:
            self.docstore.delete_document(node_id, raise_error=False)

    self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: [],
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Asynchronously delete a list of nodes from the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `doc_ids`  |  `List[str]`  |  A list of doc_ids from the nodes to delete  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: List[str],
    delete_from_docstore: bool = False,
    **delete_kwargs: Any,
) -> None:
"""
    Asynchronously delete a list of nodes from the index.

    Args:
        doc_ids (List[str]): A list of doc_ids from the nodes to delete

    """
    for node_id in node_ids:
        self._delete_node(node_id, **delete_kwargs)
        if delete_from_docstore:
            await self.docstore.adelete_document(node_id, raise_error=False)

    await self._storage_context.index_store.async_add_index_struct(
        self._index_struct
    )

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.delete "Permanent link")

```
delete(doc_id: , **delete_kwargs: ) -> None

```

Delete a document from the index. All nodes in the index related to the index will be deleted.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `doc_id`  |  A doc_id of the ingested document  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/base.py`  
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
311
312
313
314
315
```
 | 
```
defdelete(self, doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete a document from the index.
    All nodes in the index related to the index will be deleted.

    Args:
        doc_id (str): A doc_id of the ingested document

    """
    logger.warning(
        "delete() is now deprecated, please refer to delete_ref_doc() to delete "
        "ingested documents+nodes or delete_nodes to delete a list of nodes."
        "Use adelete_ref_docs() for an asynchronous implementation"
    )
    self.delete_ref_doc(doc_id)

```
 |  
| --- | --- |  
###  delete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.delete_ref_doc "Permanent link")

```
delete_ref_doc(
    ref_doc_id: ,
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a document and it's nodes by using ref_doc_id.
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
defdelete_ref_doc(
    self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
    ref_doc_info = self.docstore.get_ref_doc_info(ref_doc_id)
    if ref_doc_info is None:
        logger.warning(f"ref_doc_id {ref_doc_id} not found, nothing deleted.")
        return

    self.delete_nodes(
        ref_doc_info.node_ids,
        delete_from_docstore=delete_from_docstore,
        **delete_kwargs,
    )

    if delete_from_docstore:
        self.docstore.delete_ref_doc(ref_doc_id, raise_error=False)

```
 |  
| --- | --- |  
###  adelete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.adelete_ref_doc "Permanent link")

```
adelete_ref_doc(
    ref_doc_id: ,
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a document and it's nodes by using ref_doc_id.
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
async defadelete_ref_doc(
    self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
    ref_doc_info = await self.docstore.aget_ref_doc_info(ref_doc_id)
    if ref_doc_info is None:
        logger.warning(f"ref_doc_id {ref_doc_id} not found, nothing deleted.")
        return

    await self.adelete_nodes(
        ref_doc_info.node_ids,
        delete_from_docstore=delete_from_docstore,
        **delete_kwargs,
    )

    if delete_from_docstore:
        await self.docstore.adelete_ref_doc(ref_doc_id, raise_error=False)

```
 |  
| --- | --- |  
###  update [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.update "Permanent link")

```
update(document: , **update_kwargs: ) -> None

```

Update a document and it's corresponding nodes.
This is equivalent to deleting the document and then inserting it again.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `document`  |  `Union[BaseDocument, BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")]`  |  document to update  |  _required_  |  
|  `insert_kwargs`  |  `Dict`  |  kwargs to pass to insert  |  _required_  |  
|  `delete_kwargs`  |  `Dict`  |  kwargs to pass to delete  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
defupdate(self, document: Document, **update_kwargs: Any) -> None:
"""
    Update a document and it's corresponding nodes.

    This is equivalent to deleting the document and then inserting it again.

    Args:
        document (Union[BaseDocument, BaseIndex]): document to update
        insert_kwargs (Dict): kwargs to pass to insert
        delete_kwargs (Dict): kwargs to pass to delete

    """
    logger.warning(
        "update() is now deprecated, please refer to update_ref_doc() to update "
        "ingested documents+nodes."
        "Use aupdate_ref_docs() for an asynchronous implementation"
    )
    self.update_ref_doc(document, **update_kwargs)

```
 |  
| --- | --- |  
###  update_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.update_ref_doc "Permanent link")

```
update_ref_doc(
    document: , **update_kwargs: 
) -> None

```

Update a document and it's corresponding nodes.
This is equivalent to deleting the document and then inserting it again.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `document`  |  `Union[BaseDocument, BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")]`  |  document to update  |  _required_  |  
|  `insert_kwargs`  |  `Dict`  |  kwargs to pass to insert  |  _required_  |  
|  `delete_kwargs`  |  `Dict`  |  kwargs to pass to delete  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/base.py`  
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
382
383
384
385
386
387
388
389
390
```
 | 
```
defupdate_ref_doc(self, document: Document, **update_kwargs: Any) -> None:
"""
    Update a document and it's corresponding nodes.

    This is equivalent to deleting the document and then inserting it again.

    Args:
        document (Union[BaseDocument, BaseIndex]): document to update
        insert_kwargs (Dict): kwargs to pass to insert
        delete_kwargs (Dict): kwargs to pass to delete

    """
    with self._callback_manager.as_trace("update_ref_doc"):
        self.delete_ref_doc(
            document.id_,
            delete_from_docstore=True,
            **update_kwargs.pop("delete_kwargs", {}),
        )
        self.insert(document, **update_kwargs.pop("insert_kwargs", {}))

```
 |  
| --- | --- |  
###  aupdate_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.aupdate_ref_doc "Permanent link")

```
aupdate_ref_doc(
    document: , **update_kwargs: 
) -> None

```

Asynchronously update a document and it's corresponding nodes.
This is equivalent to deleting the document and then inserting it again.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `document`  |  `Union[BaseDocument, BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")]`  |  document to update  |  _required_  |  
|  `insert_kwargs`  |  `Dict`  |  kwargs to pass to insert  |  _required_  |  
|  `delete_kwargs`  |  `Dict`  |  kwargs to pass to delete  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
async defaupdate_ref_doc(self, document: Document, **update_kwargs: Any) -> None:
"""
    Asynchronously update a document and it's corresponding nodes.

    This is equivalent to deleting the document and then inserting it again.

    Args:
        document (Union[BaseDocument, BaseIndex]): document to update
        insert_kwargs (Dict): kwargs to pass to insert
        delete_kwargs (Dict): kwargs to pass to delete

    """
    with self._callback_manager.as_trace("aupdate_ref_doc"):
        await self.adelete_ref_doc(
            document.id_,
            delete_from_docstore=True,
            **update_kwargs.pop("delete_kwargs", {}),
        )
        await self.ainsert(document, **update_kwargs.pop("insert_kwargs", {}))

```
 |  
| --- | --- |  
###  refresh [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.refresh "Permanent link")

```
refresh(
    documents: Sequence[], **update_kwargs: 
) -> []

```

Refresh an index with documents that have changed.
This allows users to save LLM and Embedding model calls, while only updating documents that have any changes in text or metadata. It will also insert any documents that previously were not stored.
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
defrefresh(
    self, documents: Sequence[Document], **update_kwargs: Any
) -> List[bool]:
"""
    Refresh an index with documents that have changed.

    This allows users to save LLM and Embedding model calls, while only
    updating documents that have any changes in text or metadata. It
    will also insert any documents that previously were not stored.
    """
    logger.warning(
        "refresh() is now deprecated, please refer to refresh_ref_docs() to "
        "refresh ingested documents+nodes with an updated list of documents."
        "Use arefresh_ref_docs() for an asynchronous implementation"
    )
    return self.refresh_ref_docs(documents, **update_kwargs)

```
 |  
| --- | --- |  
###  refresh_ref_docs [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.refresh_ref_docs "Permanent link")

```
refresh_ref_docs(
    documents: Sequence[], **update_kwargs: 
) -> []

```

Refresh an index with documents that have changed.
This allows users to save LLM and Embedding model calls, while only updating documents that have any changes in text or metadata. It will also insert any documents that previously were not stored.
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
defrefresh_ref_docs(
    self, documents: Sequence[Document], **update_kwargs: Any
) -> List[bool]:
"""
    Refresh an index with documents that have changed.

    This allows users to save LLM and Embedding model calls, while only
    updating documents that have any changes in text or metadata. It
    will also insert any documents that previously were not stored.
    """
    with self._callback_manager.as_trace("refresh_ref_docs"):
        refreshed_documents = [False] * len(documents)
        for i, document in enumerate(documents):
            existing_doc_hash = self._docstore.get_document_hash(document.id_)
            if existing_doc_hash is None:
                self.insert(document, **update_kwargs.pop("insert_kwargs", {}))
                refreshed_documents[i] = True
            elif existing_doc_hash != document.hash:
                self.update_ref_doc(
                    document, **update_kwargs.pop("update_kwargs", {})
                )
                refreshed_documents[i] = True

        return refreshed_documents

```
 |  
| --- | --- |  
###  arefresh_ref_docs [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.arefresh_ref_docs "Permanent link")

```
arefresh_ref_docs(
    documents: Sequence[], **update_kwargs: 
) -> []

```

Asynchronously refresh an index with documents that have changed.
This allows users to save LLM and Embedding model calls, while only updating documents that have any changes in text or metadata. It will also insert any documents that previously were not stored.
Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
```
 | 
```
async defarefresh_ref_docs(
    self, documents: Sequence[Document], **update_kwargs: Any
) -> List[bool]:
"""
    Asynchronously refresh an index with documents that have changed.

    This allows users to save LLM and Embedding model calls, while only
    updating documents that have any changes in text or metadata. It
    will also insert any documents that previously were not stored.
    """
    with self._callback_manager.as_trace("arefresh_ref_docs"):
        refreshed_documents = [False] * len(documents)
        for i, document in enumerate(documents):
            existing_doc_hash = await self._docstore.aget_document_hash(
                document.id_
            )
            if existing_doc_hash is None:
                await self.ainsert(
                    document, **update_kwargs.pop("insert_kwargs", {})
                )
                refreshed_documents[i] = True
            elif existing_doc_hash != document.hash:
                await self.aupdate_ref_doc(
                    document, **update_kwargs.pop("update_kwargs", {})
                )
                refreshed_documents[i] = True
        return refreshed_documents

```
 |  
| --- | --- |  
###  as_query_engine [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.as_query_engine "Permanent link")

```
as_query_engine(
    llm: Optional[LLMType] = None, **kwargs: 
) -> 

```

Convert the index to a query engine.
Calls `index.as_retriever(**kwargs)` to get the retriever and then wraps it in a `RetrieverQueryEngine.from_args(retriever, **kwrags)` call.
Source code in `llama-index-core/llama_index/core/indices/base.py`  
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
```
 | 
```
defas_query_engine(
    self, llm: Optional[LLMType] = None, **kwargs: Any
) -> BaseQueryEngine:
"""
    Convert the index to a query engine.

    Calls `index.as_retriever(**kwargs)` to get the retriever and then wraps it in a
    `RetrieverQueryEngine.from_args(retriever, **kwrags)` call.
    """
    # NOTE: lazy import
    fromllama_index.core.query_engine.retriever_query_engineimport (
        RetrieverQueryEngine,
    )

    retriever = self.as_retriever(**kwargs)
    llm = (
        resolve_llm(llm, callback_manager=self._callback_manager)
        if llm
        else Settings.llm
    )

    return RetrieverQueryEngine.from_args(
        retriever,
        llm=llm,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  as_chat_engine [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex.as_chat_engine "Permanent link")

```
as_chat_engine(
    chat_mode:  = ,
    llm: Optional[LLMType] = None,
    **kwargs: 
) -> 

```

Convert the index to a chat engine.
Calls `index.as_query_engine(llm=llm, **kwargs)` to get the query engine and then wraps it in a chat engine based on the chat mode.
Chat modes
  * `ChatMode.BEST` (default): Chat engine that uses an agent (react or openai) with a query engine tool
  * `ChatMode.CONTEXT`: Chat engine that uses a retriever to get context
  * `ChatMode.CONDENSE_QUESTION`: Chat engine that condenses questions
  * `ChatMode.CONDENSE_PLUS_CONTEXT`: Chat engine that condenses questions and uses a retriever to get context
  * `ChatMode.SIMPLE`: Simple chat engine that uses the LLM directly
  * `ChatMode.REACT`: Chat engine that uses a react agent with a query engine tool
  * `ChatMode.OPENAI`: Chat engine that uses an openai agent with a query engine tool

Source code in `llama-index-core/llama_index/core/indices/base.py`  
| 
```
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
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
```
 | 
```
defas_chat_engine(
    self,
    chat_mode: ChatMode = ChatMode.BEST,
    llm: Optional[LLMType] = None,
    **kwargs: Any,
) -> BaseChatEngine:
"""
    Convert the index to a chat engine.

    Calls `index.as_query_engine(llm=llm, **kwargs)` to get the query engine and then
    wraps it in a chat engine based on the chat mode.

    Chat modes:
        - `ChatMode.BEST` (default): Chat engine that uses an agent (react or openai) with a query engine tool
        - `ChatMode.CONTEXT`: Chat engine that uses a retriever to get context
        - `ChatMode.CONDENSE_QUESTION`: Chat engine that condenses questions
        - `ChatMode.CONDENSE_PLUS_CONTEXT`: Chat engine that condenses questions and uses a retriever to get context
        - `ChatMode.SIMPLE`: Simple chat engine that uses the LLM directly
        - `ChatMode.REACT`: Chat engine that uses a react agent with a query engine tool
        - `ChatMode.OPENAI`: Chat engine that uses an openai agent with a query engine tool
    """
    llm = (
        resolve_llm(llm, callback_manager=self._callback_manager)
        if llm
        else Settings.llm
    )

    query_engine = self.as_query_engine(llm=llm, **kwargs)

    # resolve chat mode
    if chat_mode in [ChatMode.REACT, ChatMode.OPENAI]:
        raise ValueError(
            "ChatMode.REACT and ChatMode.OPENAI are now deprecated and removed. "
            "Please use the ReActAgent or FunctionAgent classes from llama_index.core.agent.workflow "
            "to create an agent with a query engine tool."
        )

    if chat_mode == ChatMode.CONDENSE_QUESTION:
        # NOTE: lazy import
        fromllama_index.core.chat_engineimport CondenseQuestionChatEngine

        return CondenseQuestionChatEngine.from_defaults(
            query_engine=query_engine,
            llm=llm,
            **kwargs,
        )

    elif chat_mode == ChatMode.CONTEXT:
        fromllama_index.core.chat_engineimport ContextChatEngine

        return ContextChatEngine.from_defaults(
            retriever=self.as_retriever(**kwargs),
            llm=llm,
            **kwargs,
        )

    elif chat_mode in [ChatMode.CONDENSE_PLUS_CONTEXT, ChatMode.BEST]:
        fromllama_index.core.chat_engineimport CondensePlusContextChatEngine

        return CondensePlusContextChatEngine.from_defaults(
            retriever=self.as_retriever(**kwargs),
            llm=llm,
            **kwargs,
        )

    elif chat_mode == ChatMode.SIMPLE:
        fromllama_index.core.chat_engineimport SimpleChatEngine

        return SimpleChatEngine.from_defaults(
            llm=llm,
            **kwargs,
        )
    else:
        raise ValueError(f"Unknown chat mode: {chat_mode}")

```
 |  
| --- | --- |  
options: members: - BaseIndex
