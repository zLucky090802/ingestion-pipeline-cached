# Index
##  DocstoreStrategy [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/#llama_index.core.ingestion.pipeline.DocstoreStrategy "Permanent link")
Bases: `str`, `Enum`
Document de-duplication de-deduplication strategies work by comparing the hashes or ids stored in the document store. They require a document store to be set which must be persisted across pipeline runs.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `UPSERTS`  |  ('upserts') Use upserts to handle duplicates. Checks if the a document is already in the doc store based on its id. If it is not, or if the hash of the document is updated, it will update the document in the doc store and run the transformations.  |  
| `DUPLICATES_ONLY`  |  ('duplicates_only') Only handle duplicates. Checks if the hash of a document is already in the doc store. Only then it will add the document to the doc store and run the transformations  |  
| `UPSERTS_AND_DELETE`  |  ('upserts_and_delete') Use upserts and delete to handle duplicates. Like the upsert strategy but it will also delete non-existing documents from the doc store  |  
Source code in `llama-index-core/llama_index/core/ingestion/pipeline.py`  
| 
```
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
```
 | 
```
classDocstoreStrategy(str, Enum):
"""
    Document de-duplication de-deduplication strategies work by comparing the hashes or ids stored in the document store.
       They require a document store to be set which must be persisted across pipeline runs.

    Attributes:
        UPSERTS:
            ('upserts') Use upserts to handle duplicates. Checks if the a document is already in the doc store based on its id. If it is not, or if the hash of the document is updated, it will update the document in the doc store and run the transformations.
        DUPLICATES_ONLY:
            ('duplicates_only') Only handle duplicates. Checks if the hash of a document is already in the doc store. Only then it will add the document to the doc store and run the transformations
        UPSERTS_AND_DELETE:
            ('upserts_and_delete') Use upserts and delete to handle duplicates. Like the upsert strategy but it will also delete non-existing documents from the doc store

    """

    UPSERTS = "upserts"
    DUPLICATES_ONLY = "duplicates_only"
    UPSERTS_AND_DELETE = "upserts_and_delete"

```
 |  
| --- | --- |  
##  IngestionPipeline [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/#llama_index.core.ingestion.pipeline.IngestionPipeline "Permanent link")
Bases: `BaseModel`
An ingestion pipeline that can be applied to data.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  Unique name of the ingestion pipeline. Defaults to DEFAULT_PIPELINE_NAME.  |  `DEFAULT_PIPELINE_NAME`  |  
|  `project_name`  |  Unique name of the project. Defaults to DEFAULT_PROJECT_NAME.  |  `DEFAULT_PROJECT_NAME`  |  
|  `transformations`  |  `List[TransformComponent[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TransformComponent "TransformComponent \(llama_index.core.schema.TransformComponent\)")]`  |  Transformations to apply to the data. Defaults to None.  |  `None`  |  
|  `documents`  |  `Sequence[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")] | None`  |  Documents to ingest. Defaults to None.  |  `None`  |  
|  `readers`  |  `List[ReaderConfig[](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ReaderConfig "ReaderConfig \(llama_index.core.readers.base.ReaderConfig\)")] | None`  |  Reader to use to read the data. Defaults to None.  |  `None`  |  
|  `vector_store`  |  `BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)") | None`  |  Vector store to use to store the data. Defaults to None.  |  `None`  |  
|  `cache`  |  `IngestionCache`  |  Cache to use to store the data. Defaults to None.  |  `None`  |  
|  `docstore`  |  `BaseDocumentStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/simple/#llama_index.core.storage.docstore.BaseDocumentStore "BaseDocumentStore \(llama_index.core.storage.docstore.BaseDocumentStore\)") | None`  |  Document store to use for de-duping with a vector store. Defaults to None.  |  `None`  |  
|  `docstore_strategy`  |   |  Document de-dup strategy. Defaults to DocstoreStrategy.UPSERTS.  |  `UPSERTS`  |  
|  `disable_cache`  |  `bool`  |  Disable the cache. Defaults to False.  |  `False`  |  
|  `base_url`  |  Base URL for the LlamaCloud API. Defaults to DEFAULT_BASE_URL.  |  _required_  |  
|  `app_url`  |  Base URL for the LlamaCloud app. Defaults to DEFAULT_APP_URL.  |  _required_  |  
|  `api_key`  |  `Optional[str]`  |  LlamaCloud API key. Defaults to None.  |  _required_  |  
Examples:

```
fromllama_index.core.ingestionimport IngestionPipeline
fromllama_index.core.node_parserimport SentenceSplitter
fromllama_index.embeddings.openaiimport OpenAIEmbedding

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512, chunk_overlap=20),
        OpenAIEmbedding(),
    ],
)

nodes = pipeline.run(documents=documents)

```

Source code in `llama-index-core/llama_index/core/ingestion/pipeline.py`  
| 
```
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
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
```
 | 
```
classIngestionPipeline(BaseModel):
"""
    An ingestion pipeline that can be applied to data.

    Args:
        name (str, optional):
            Unique name of the ingestion pipeline. Defaults to DEFAULT_PIPELINE_NAME.
        project_name (str, optional):
            Unique name of the project. Defaults to DEFAULT_PROJECT_NAME.
        transformations (List[TransformComponent], optional):
            Transformations to apply to the data. Defaults to None.
        documents (Optional[Sequence[Document]], optional):
            Documents to ingest. Defaults to None.
        readers (Optional[List[ReaderConfig]], optional):
            Reader to use to read the data. Defaults to None.
        vector_store (Optional[BasePydanticVectorStore], optional):
            Vector store to use to store the data. Defaults to None.
        cache (Optional[IngestionCache], optional):
            Cache to use to store the data. Defaults to None.
        docstore (Optional[BaseDocumentStore], optional):
            Document store to use for de-duping with a vector store. Defaults to None.
        docstore_strategy (DocstoreStrategy, optional):
            Document de-dup strategy. Defaults to DocstoreStrategy.UPSERTS.
        disable_cache (bool, optional):
            Disable the cache. Defaults to False.
        base_url (str, optional):
            Base URL for the LlamaCloud API. Defaults to DEFAULT_BASE_URL.
        app_url (str, optional):
            Base URL for the LlamaCloud app. Defaults to DEFAULT_APP_URL.
        api_key (Optional[str], optional):
            LlamaCloud API key. Defaults to None.

    Examples:
        ```python
        from llama_index.core.ingestion import IngestionPipeline
        from llama_index.core.node_parser import SentenceSplitter
        from llama_index.embeddings.openai import OpenAIEmbedding

        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=512, chunk_overlap=20),
                OpenAIEmbedding(),



        nodes = pipeline.run(documents=documents)
        ```

    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str = Field(
        default=DEFAULT_PIPELINE_NAME,
        description="Unique name of the ingestion pipeline",
    )
    project_name: str = Field(
        default=DEFAULT_PROJECT_NAME, description="Unique name of the project"
    )

    transformations: List[TransformComponent] = Field(
        description="Transformations to apply to the data"
    )

    documents: Optional[Sequence[Document]] = Field(description="Documents to ingest")
    readers: Optional[List[ReaderConfig]] = Field(
        description="Reader to use to read the data"
    )
    vector_store: Optional[BasePydanticVectorStore] = Field(
        description="Vector store to use to store the data"
    )
    cache: IngestionCache = Field(
        default_factory=IngestionCache,
        description="Cache to use to store the data",
    )
    docstore: Optional[BaseDocumentStore] = Field(
        default=None,
        description="Document store to use for de-duping with a vector store.",
    )
    docstore_strategy: DocstoreStrategy = Field(
        default=DocstoreStrategy.UPSERTS, description="Document de-dup strategy."
    )
    disable_cache: bool = Field(default=False, description="Disable the cache")

    def__init__(
        self,
        name: str = DEFAULT_PIPELINE_NAME,
        project_name: str = DEFAULT_PROJECT_NAME,
        transformations: Optional[List[TransformComponent]] = None,
        readers: Optional[List[ReaderConfig]] = None,
        documents: Optional[Sequence[Document]] = None,
        vector_store: Optional[BasePydanticVectorStore] = None,
        cache: Optional[IngestionCache] = None,
        docstore: Optional[BaseDocumentStore] = None,
        docstore_strategy: DocstoreStrategy = DocstoreStrategy.UPSERTS,
        disable_cache: bool = False,
    ) -> None:
        if transformations is None:
            transformations = self._get_default_transformations()

        super().__init__(
            name=name,
            project_name=project_name,
            transformations=transformations,
            readers=readers,
            documents=documents,
            vector_store=vector_store,
            cache=cache or IngestionCache(),
            docstore=docstore,
            docstore_strategy=docstore_strategy,
            disable_cache=disable_cache,
        )

    defpersist(
        self,
        persist_dir: str = "./pipeline_storage",
        fs: Optional[AbstractFileSystem] = None,
        cache_name: str = DEFAULT_CACHE_NAME,
        docstore_name: str = DOCSTORE_FNAME,
    ) -> None:
"""Persist the pipeline to disk."""
        if fs is not None:
            persist_dir = str(persist_dir)  # NOTE: doesn't support Windows here
            docstore_path = concat_dirs(persist_dir, docstore_name)
            cache_path = concat_dirs(persist_dir, cache_name)

        else:
            persist_path = Path(persist_dir)
            docstore_path = str(persist_path / docstore_name)
            cache_path = str(persist_path / cache_name)

        self.cache.persist(cache_path, fs=fs)
        if self.docstore is not None:
            self.docstore.persist(docstore_path, fs=fs)

    defload(
        self,
        persist_dir: str = "./pipeline_storage",
        fs: Optional[AbstractFileSystem] = None,
        cache_name: str = DEFAULT_CACHE_NAME,
        docstore_name: str = DOCSTORE_FNAME,
    ) -> None:
"""Load the pipeline from disk."""
        if fs is not None:
            self.cache = IngestionCache.from_persist_path(
                concat_dirs(persist_dir, cache_name), fs=fs
            )
            persist_docstore_path = concat_dirs(persist_dir, docstore_name)
            if fs.exists(persist_docstore_path):
                self.docstore = SimpleDocumentStore.from_persist_path(
                    concat_dirs(persist_dir, docstore_name), fs=fs
                )
        else:
            self.cache = IngestionCache.from_persist_path(
                str(Path(persist_dir) / cache_name)
            )
            persist_docstore_path = str(Path(persist_dir) / docstore_name)
            if os.path.exists(persist_docstore_path):
                self.docstore = SimpleDocumentStore.from_persist_path(
                    str(Path(persist_dir) / docstore_name)
                )

    def_get_default_transformations(self) -> List[TransformComponent]:
        return [
            SentenceSplitter(),
            Settings.embed_model,
        ]

    def_prepare_inputs(
        self,
        documents: Optional[Sequence[Document]],
        nodes: Optional[Sequence[BaseNode]],
    ) -> Sequence[BaseNode]:
        input_nodes: Sequence[BaseNode] = []

        if documents is not None:
            input_nodes += documents  # type: ignore

        if nodes is not None:
            input_nodes += nodes  # type: ignore

        if self.documents is not None:
            input_nodes += self.documents  # type: ignore

        if self.readers is not None:
            for reader in self.readers:
                input_nodes += reader.read()  # type: ignore

        return input_nodes

    def_handle_duplicates(
        self,
        nodes: Sequence[BaseNode],
    ) -> Sequence[BaseNode]:
"""Handle docstore duplicates by checking all hashes."""
        assert self.docstore is not None

        existing_hashes = self.docstore.get_all_document_hashes()
        current_hashes = []
        nodes_to_run = []
        for node in nodes:
            if node.hash not in existing_hashes and node.hash not in current_hashes:
                self.docstore.set_document_hash(node.id_, node.hash)
                nodes_to_run.append(node)
                current_hashes.append(node.hash)

        return nodes_to_run

    def_handle_upserts(
        self,
        nodes: Sequence[BaseNode],
    ) -> Sequence[BaseNode]:
"""Handle docstore upserts by checking hashes and ids."""
        assert self.docstore is not None

        doc_ids_from_nodes = set()
        deduped_nodes_to_run = {}
        for node in nodes:
            ref_doc_id = node.ref_doc_id if node.ref_doc_id else node.id_
            doc_ids_from_nodes.add(ref_doc_id)
            existing_hash = self.docstore.get_document_hash(ref_doc_id)
            if not existing_hash:
                # document doesn't exist, so add it
                deduped_nodes_to_run[ref_doc_id] = node
            elif existing_hash and existing_hash != node.hash:
                self.docstore.delete_ref_doc(ref_doc_id, raise_error=False)

                if self.vector_store is not None:
                    self.vector_store.delete(ref_doc_id)

                deduped_nodes_to_run[ref_doc_id] = node
            else:
                continue  # document exists and is unchanged, so skip it

        if self.docstore_strategy == DocstoreStrategy.UPSERTS_AND_DELETE:
            # Identify missing docs and delete them from docstore and vector store
            existing_doc_ids_before = set(
                self.docstore.get_all_document_hashes().values()
            )
            doc_ids_to_delete = existing_doc_ids_before - doc_ids_from_nodes
            for ref_doc_id in doc_ids_to_delete:
                self.docstore.delete_document(ref_doc_id)

                if self.vector_store is not None:
                    self.vector_store.delete(ref_doc_id)

        return list(deduped_nodes_to_run.values())

    @staticmethod
    def_node_batcher(
        num_batches: int, nodes: Union[Sequence[BaseNode], List[Document]]
    ) -> Generator[Union[Sequence[BaseNode], List[Document]], Any, Any]:
"""Yield successive n-sized chunks from lst."""
        batch_size = max(1, int(len(nodes) / num_batches))
        for i in range(0, len(nodes), batch_size):
            yield nodes[i : i + batch_size]

    def_update_docstore(
        self,
        nodes: Sequence[BaseNode],
        effective_strategy: DocstoreStrategy,
        store_doc_text: bool = True,
    ) -> None:
"""Update the document store with the given nodes."""
        assert self.docstore is not None

        if effective_strategy in (
            DocstoreStrategy.UPSERTS,
            DocstoreStrategy.UPSERTS_AND_DELETE,
        ):
            self.docstore.set_document_hashes({n.id_: n.hash for n in nodes})
            self.docstore.add_documents(nodes, store_text=store_doc_text)
        elif effective_strategy == DocstoreStrategy.DUPLICATES_ONLY:
            self.docstore.add_documents(nodes, store_text=store_doc_text)
        else:
            raise ValueError(f"Invalid docstore strategy: {effective_strategy}")

    @dispatcher.span
    defrun(
        self,
        show_progress: bool = False,
        documents: Optional[List[Document]] = None,
        nodes: Optional[Sequence[BaseNode]] = None,
        cache_collection: Optional[str] = None,
        in_place: bool = True,
        store_doc_text: bool = True,
        num_workers: Optional[int] = None,
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
            cache_collection (Optional[str], optional): Cache for transformations. Defaults to None.
            in_place (bool, optional): Whether transformations creates a new list for transformed nodes or modifies the
                array passed to `run_transformations`. Defaults to True.
            store_doc_text (bool, optional): Whether to store the document texts. Defaults to True.
            num_workers (Optional[int], optional): The number of parallel processes to use.
                If set to None, then sequential compute is used. Defaults to None.

        Returns:
            Sequence[BaseNode]: The set of transformed Nodes/Documents

        """
        input_nodes = self._prepare_inputs(documents, nodes)

        effective_strategy = self.docstore_strategy
        if (
            self.docstore is not None
            and self.vector_store is None
            and self.docstore_strategy
            in (DocstoreStrategy.UPSERTS, DocstoreStrategy.UPSERTS_AND_DELETE)
        ):
            warnings.warn(
                f"docstore_strategy='{self.docstore_strategy.value}' requires a vector store "
                "to apply upsert/delete semantics; falling back to 'duplicates_only' for this run. "
                "pipeline.docstore_strategy is unchanged.",
                UserWarning,
                stacklevel=3,
            )
            effective_strategy = DocstoreStrategy.DUPLICATES_ONLY

        # check if we need to dedup
        if self.docstore is not None and self.vector_store is not None:
            if effective_strategy in (
                DocstoreStrategy.UPSERTS,
                DocstoreStrategy.UPSERTS_AND_DELETE,
            ):
                nodes_to_run = self._handle_upserts(input_nodes)
            elif effective_strategy == DocstoreStrategy.DUPLICATES_ONLY:
                nodes_to_run = self._handle_duplicates(input_nodes)
            else:
                raise ValueError(f"Invalid docstore strategy: {effective_strategy}")
        elif self.docstore is not None and self.vector_store is None:
            nodes_to_run = self._handle_duplicates(input_nodes)
        else:
            nodes_to_run = input_nodes

        if num_workers and num_workers  1:
            num_cpus = multiprocessing.cpu_count()
            if num_workers  num_cpus:
                warnings.warn(
                    "Specified num_workers exceed number of CPUs in the system. "
                    "Setting `num_workers` down to the maximum CPU count.",
                    stacklevel=2,
                )
                num_workers = num_cpus

            with multiprocessing.get_context("spawn").Pool(num_workers) as p:
                node_batches = self._node_batcher(
                    num_batches=num_workers, nodes=nodes_to_run
                )
                nodes_parallel = p.starmap(
                    run_transformations,
                    zip(
                        node_batches,
                        repeat(self.transformations),
                        repeat(in_place),
                        repeat(self.cache if not self.disable_cache else None),
                        repeat(cache_collection),
                    ),
                )
                nodes = reduce(lambda x, y: x + y, nodes_parallel, [])  # type: ignore
        else:
            nodes = run_transformations(
                nodes_to_run,
                self.transformations,
                show_progress=show_progress,
                cache=self.cache if not self.disable_cache else None,
                cache_collection=cache_collection,
                in_place=in_place,
                **kwargs,
            )

        nodes = nodes or []

        if self.vector_store is not None:
            nodes_with_embeddings = [n for n in nodes if n.embedding is not None]
            if nodes_with_embeddings:
                self.vector_store.add(nodes_with_embeddings)

        if self.docstore is not None:
            self._update_docstore(
                nodes_to_run,
                effective_strategy=effective_strategy,
                store_doc_text=store_doc_text,
            )

        return nodes

    # ------ async methods ------
    async def_aupdate_docstore(
        self,
        nodes: Sequence[BaseNode],
        effective_strategy: DocstoreStrategy,
        store_doc_text: bool = True,
    ) -> None:
"""Update the document store with the given nodes."""
        assert self.docstore is not None

        if effective_strategy in (
            DocstoreStrategy.UPSERTS,
            DocstoreStrategy.UPSERTS_AND_DELETE,
        ):
            await self.docstore.aset_document_hashes({n.id_: n.hash for n in nodes})
            await self.docstore.async_add_documents(nodes, store_text=store_doc_text)
        elif effective_strategy == DocstoreStrategy.DUPLICATES_ONLY:
            await self.docstore.async_add_documents(nodes, store_text=store_doc_text)
        else:
            raise ValueError(f"Invalid docstore strategy: {effective_strategy}")

    async def_ahandle_duplicates(
        self,
        nodes: Sequence[BaseNode],
        store_doc_text: bool = True,
    ) -> Sequence[BaseNode]:
"""Handle docstore duplicates by checking all hashes."""
        assert self.docstore is not None

        existing_hashes = await self.docstore.aget_all_document_hashes()
        current_hashes = []
        nodes_to_run = []
        for node in nodes:
            if node.hash not in existing_hashes and node.hash not in current_hashes:
                await self.docstore.aset_document_hash(node.id_, node.hash)
                nodes_to_run.append(node)
                current_hashes.append(node.hash)

        return nodes_to_run

    async def_ahandle_upserts(
        self,
        nodes: Sequence[BaseNode],
        store_doc_text: bool = True,
    ) -> Sequence[BaseNode]:
"""Handle docstore upserts by checking hashes and ids."""
        assert self.docstore is not None

        doc_ids_from_nodes = set()
        deduped_nodes_to_run = {}
        for node in nodes:
            ref_doc_id = node.ref_doc_id if node.ref_doc_id else node.id_
            doc_ids_from_nodes.add(ref_doc_id)
            existing_hash = await self.docstore.aget_document_hash(ref_doc_id)
            if not existing_hash:
                # document doesn't exist, so add it
                deduped_nodes_to_run[ref_doc_id] = node
            elif existing_hash and existing_hash != node.hash:
                await self.docstore.adelete_ref_doc(ref_doc_id, raise_error=False)

                if self.vector_store is not None:
                    await self.vector_store.adelete(ref_doc_id)

                deduped_nodes_to_run[ref_doc_id] = node
            else:
                continue  # document exists and is unchanged, so skip it

        if self.docstore_strategy == DocstoreStrategy.UPSERTS_AND_DELETE:
            # Identify missing docs and delete them from docstore and vector store
            existing_doc_ids_before = set(
                (await self.docstore.aget_all_document_hashes()).values()
            )
            doc_ids_to_delete = existing_doc_ids_before - doc_ids_from_nodes
            for ref_doc_id in doc_ids_to_delete:
                await self.docstore.adelete_document(ref_doc_id)

                if self.vector_store is not None:
                    await self.vector_store.adelete(ref_doc_id)

        return list(deduped_nodes_to_run.values())

    @dispatcher.span
    async defarun(
        self,
        show_progress: bool = False,
        documents: Optional[List[Document]] = None,
        nodes: Optional[Sequence[BaseNode]] = None,
        cache_collection: Optional[str] = None,
        in_place: bool = True,
        store_doc_text: bool = True,
        num_workers: Optional[int] = None,
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
            cache_collection (Optional[str], optional): Cache for transformations. Defaults to None.
            in_place (bool, optional): Whether transformations creates a new list for transformed nodes or modifies the
                array passed to `run_transformations`. Defaults to True.
            store_doc_text (bool, optional): Whether to store the document texts. Defaults to True.
            num_workers (Optional[int], optional): The number of parallel processes to use.
                If set to None, then sequential compute is used. Defaults to None.

        Returns:
            Sequence[BaseNode]: The set of transformed Nodes/Documents

        """
        input_nodes = self._prepare_inputs(documents, nodes)

        effective_strategy = self.docstore_strategy
        if (
            self.docstore is not None
            and self.vector_store is None
            and self.docstore_strategy
            in (DocstoreStrategy.UPSERTS, DocstoreStrategy.UPSERTS_AND_DELETE)
        ):
            warnings.warn(
                f"docstore_strategy='{self.docstore_strategy.value}' requires a vector store "
                "to apply upsert/delete semantics; falling back to 'duplicates_only' for this run. "
                "pipeline.docstore_strategy is unchanged.",
                UserWarning,
                stacklevel=3,
            )
            effective_strategy = DocstoreStrategy.DUPLICATES_ONLY

        # check if we need to dedup
        if self.docstore is not None and self.vector_store is not None:
            if effective_strategy in (
                DocstoreStrategy.UPSERTS,
                DocstoreStrategy.UPSERTS_AND_DELETE,
            ):
                nodes_to_run = await self._ahandle_upserts(
                    input_nodes, store_doc_text=store_doc_text
                )
            elif effective_strategy == DocstoreStrategy.DUPLICATES_ONLY:
                nodes_to_run = await self._ahandle_duplicates(
                    input_nodes, store_doc_text=store_doc_text
                )
            else:
                raise ValueError(f"Invalid docstore strategy: {effective_strategy}")
        elif self.docstore is not None and self.vector_store is None:
            nodes_to_run = await self._ahandle_duplicates(
                input_nodes, store_doc_text=store_doc_text
            )
        else:
            nodes_to_run = input_nodes

        if num_workers and num_workers  1:
            num_cpus = multiprocessing.cpu_count()
            if num_workers  num_cpus:
                warnings.warn(
                    "Specified num_workers exceed number of CPUs in the system. "
                    "Setting `num_workers` down to the maximum CPU count.",
                    stacklevel=2,
                )
                num_workers = num_cpus

            loop = asyncio.get_event_loop()
            with ProcessPoolExecutor(max_workers=num_workers) as p:
                node_batches = self._node_batcher(
                    num_batches=num_workers, nodes=nodes_to_run
                )
                tasks = [
                    loop.run_in_executor(
                        p,
                        partial(
                            arun_transformations_wrapper,
                            transformations=self.transformations,
                            in_place=in_place,
                            cache=self.cache if not self.disable_cache else None,
                            cache_collection=cache_collection,
                        ),
                        batch,
                    )
                    for batch in node_batches
                ]
                result: Sequence[Sequence[BaseNode]] = await asyncio.gather(*tasks)
                nodes: Sequence[BaseNode] = reduce(lambda x, y: x + y, result, [])  # type: ignore
        else:
            nodes = await arun_transformations(  # type: ignore
                nodes_to_run,
                self.transformations,
                show_progress=show_progress,
                cache=self.cache if not self.disable_cache else None,
                cache_collection=cache_collection,
                in_place=in_place,
                **kwargs,
            )
            nodes = nodes

        nodes = nodes or []

        if self.vector_store is not None:
            nodes_with_embeddings = [n for n in nodes if n.embedding is not None]
            if nodes_with_embeddings:
                await self.vector_store.async_add(nodes_with_embeddings)

        if self.docstore is not None:
            await self._aupdate_docstore(
                nodes_to_run,
                effective_strategy=effective_strategy,
                store_doc_text=store_doc_text,
            )

        return nodes

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/#llama_index.core.ingestion.pipeline.IngestionPipeline.persist "Permanent link")

```
persist(
    persist_dir:  = "./pipeline_storage",
    fs: Optional[AbstractFileSystem] = None,
    cache_name:  = DEFAULT_CACHE_NAME,
    docstore_name:  = DOCSTORE_FNAME,
) -> None

```

Persist the pipeline to disk.
Source code in `llama-index-core/llama_index/core/ingestion/pipeline.py`  
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
334
335
336
337
```
 | 
```
defpersist(
    self,
    persist_dir: str = "./pipeline_storage",
    fs: Optional[AbstractFileSystem] = None,
    cache_name: str = DEFAULT_CACHE_NAME,
    docstore_name: str = DOCSTORE_FNAME,
) -> None:
"""Persist the pipeline to disk."""
    if fs is not None:
        persist_dir = str(persist_dir)  # NOTE: doesn't support Windows here
        docstore_path = concat_dirs(persist_dir, docstore_name)
        cache_path = concat_dirs(persist_dir, cache_name)

    else:
        persist_path = Path(persist_dir)
        docstore_path = str(persist_path / docstore_name)
        cache_path = str(persist_path / cache_name)

    self.cache.persist(cache_path, fs=fs)
    if self.docstore is not None:
        self.docstore.persist(docstore_path, fs=fs)

```
 |  
| --- | --- |  
###  load [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/#llama_index.core.ingestion.pipeline.IngestionPipeline.load "Permanent link")

```
load(
    persist_dir:  = "./pipeline_storage",
    fs: Optional[AbstractFileSystem] = None,
    cache_name:  = DEFAULT_CACHE_NAME,
    docstore_name:  = DOCSTORE_FNAME,
) -> None

```

Load the pipeline from disk.
Source code in `llama-index-core/llama_index/core/ingestion/pipeline.py`  
| 
```
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
```
 | 
```
defload(
    self,
    persist_dir: str = "./pipeline_storage",
    fs: Optional[AbstractFileSystem] = None,
    cache_name: str = DEFAULT_CACHE_NAME,
    docstore_name: str = DOCSTORE_FNAME,
) -> None:
"""Load the pipeline from disk."""
    if fs is not None:
        self.cache = IngestionCache.from_persist_path(
            concat_dirs(persist_dir, cache_name), fs=fs
        )
        persist_docstore_path = concat_dirs(persist_dir, docstore_name)
        if fs.exists(persist_docstore_path):
            self.docstore = SimpleDocumentStore.from_persist_path(
                concat_dirs(persist_dir, docstore_name), fs=fs
            )
    else:
        self.cache = IngestionCache.from_persist_path(
            str(Path(persist_dir) / cache_name)
        )
        persist_docstore_path = str(Path(persist_dir) / docstore_name)
        if os.path.exists(persist_docstore_path):
            self.docstore = SimpleDocumentStore.from_persist_path(
                str(Path(persist_dir) / docstore_name)
            )

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/#llama_index.core.ingestion.pipeline.IngestionPipeline.run "Permanent link")

```
run(
    show_progress:  = False,
    documents: Optional[[]] = None,
    nodes: Optional[Sequence[]] = None,
    cache_collection: Optional[] = None,
    in_place:  = True,
    store_doc_text:  = True,
    num_workers: Optional[] = None,
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
|  `cache_collection`  |  `Optional[str]`  |  Cache for transformations. Defaults to None.  |  `None`  |  
|  `in_place`  |  `bool`  |  Whether transformations creates a new list for transformed nodes or modifies the array passed to `run_transformations`. Defaults to True.  |  `True`  |  
|  `store_doc_text`  |  `bool`  |  Whether to store the document texts. Defaults to True.  |  `True`  |  
|  `num_workers`  |  `Optional[int]`  |  The number of parallel processes to use. If set to None, then sequential compute is used. Defaults to None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]`  |  Sequence[BaseNode]: The set of transformed Nodes/Documents  |  
Source code in `llama-index-core/llama_index/core/ingestion/pipeline.py`  
| 
```
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
592
593
594
595
596
597
598
599
```
 | 
```
@dispatcher.span
defrun(
    self,
    show_progress: bool = False,
    documents: Optional[List[Document]] = None,
    nodes: Optional[Sequence[BaseNode]] = None,
    cache_collection: Optional[str] = None,
    in_place: bool = True,
    store_doc_text: bool = True,
    num_workers: Optional[int] = None,
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
        cache_collection (Optional[str], optional): Cache for transformations. Defaults to None.
        in_place (bool, optional): Whether transformations creates a new list for transformed nodes or modifies the
            array passed to `run_transformations`. Defaults to True.
        store_doc_text (bool, optional): Whether to store the document texts. Defaults to True.
        num_workers (Optional[int], optional): The number of parallel processes to use.
            If set to None, then sequential compute is used. Defaults to None.

    Returns:
        Sequence[BaseNode]: The set of transformed Nodes/Documents

    """
    input_nodes = self._prepare_inputs(documents, nodes)

    effective_strategy = self.docstore_strategy
    if (
        self.docstore is not None
        and self.vector_store is None
        and self.docstore_strategy
        in (DocstoreStrategy.UPSERTS, DocstoreStrategy.UPSERTS_AND_DELETE)
    ):
        warnings.warn(
            f"docstore_strategy='{self.docstore_strategy.value}' requires a vector store "
            "to apply upsert/delete semantics; falling back to 'duplicates_only' for this run. "
            "pipeline.docstore_strategy is unchanged.",
            UserWarning,
            stacklevel=3,
        )
        effective_strategy = DocstoreStrategy.DUPLICATES_ONLY

    # check if we need to dedup
    if self.docstore is not None and self.vector_store is not None:
        if effective_strategy in (
            DocstoreStrategy.UPSERTS,
            DocstoreStrategy.UPSERTS_AND_DELETE,
        ):
            nodes_to_run = self._handle_upserts(input_nodes)
        elif effective_strategy == DocstoreStrategy.DUPLICATES_ONLY:
            nodes_to_run = self._handle_duplicates(input_nodes)
        else:
            raise ValueError(f"Invalid docstore strategy: {effective_strategy}")
    elif self.docstore is not None and self.vector_store is None:
        nodes_to_run = self._handle_duplicates(input_nodes)
    else:
        nodes_to_run = input_nodes

    if num_workers and num_workers  1:
        num_cpus = multiprocessing.cpu_count()
        if num_workers  num_cpus:
            warnings.warn(
                "Specified num_workers exceed number of CPUs in the system. "
                "Setting `num_workers` down to the maximum CPU count.",
                stacklevel=2,
            )
            num_workers = num_cpus

        with multiprocessing.get_context("spawn").Pool(num_workers) as p:
            node_batches = self._node_batcher(
                num_batches=num_workers, nodes=nodes_to_run
            )
            nodes_parallel = p.starmap(
                run_transformations,
                zip(
                    node_batches,
                    repeat(self.transformations),
                    repeat(in_place),
                    repeat(self.cache if not self.disable_cache else None),
                    repeat(cache_collection),
                ),
            )
            nodes = reduce(lambda x, y: x + y, nodes_parallel, [])  # type: ignore
    else:
        nodes = run_transformations(
            nodes_to_run,
            self.transformations,
            show_progress=show_progress,
            cache=self.cache if not self.disable_cache else None,
            cache_collection=cache_collection,
            in_place=in_place,
            **kwargs,
        )

    nodes = nodes or []

    if self.vector_store is not None:
        nodes_with_embeddings = [n for n in nodes if n.embedding is not None]
        if nodes_with_embeddings:
            self.vector_store.add(nodes_with_embeddings)

    if self.docstore is not None:
        self._update_docstore(
            nodes_to_run,
            effective_strategy=effective_strategy,
            store_doc_text=store_doc_text,
        )

    return nodes

```
 |  
| --- | --- |  
###  arun [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/#llama_index.core.ingestion.pipeline.IngestionPipeline.arun "Permanent link")

```
arun(
    show_progress:  = False,
    documents: Optional[[]] = None,
    nodes: Optional[Sequence[]] = None,
    cache_collection: Optional[] = None,
    in_place:  = True,
    store_doc_text:  = True,
    num_workers: Optional[] = None,
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
|  `cache_collection`  |  `Optional[str]`  |  Cache for transformations. Defaults to None.  |  `None`  |  
|  `in_place`  |  `bool`  |  Whether transformations creates a new list for transformed nodes or modifies the array passed to `run_transformations`. Defaults to True.  |  `True`  |  
|  `store_doc_text`  |  `bool`  |  Whether to store the document texts. Defaults to True.  |  `True`  |  
|  `num_workers`  |  `Optional[int]`  |  The number of parallel processes to use. If set to None, then sequential compute is used. Defaults to None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]`  |  Sequence[BaseNode]: The set of transformed Nodes/Documents  |  
Source code in `llama-index-core/llama_index/core/ingestion/pipeline.py`  
| 
```
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
```
 | 
```
@dispatcher.span
async defarun(
    self,
    show_progress: bool = False,
    documents: Optional[List[Document]] = None,
    nodes: Optional[Sequence[BaseNode]] = None,
    cache_collection: Optional[str] = None,
    in_place: bool = True,
    store_doc_text: bool = True,
    num_workers: Optional[int] = None,
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
        cache_collection (Optional[str], optional): Cache for transformations. Defaults to None.
        in_place (bool, optional): Whether transformations creates a new list for transformed nodes or modifies the
            array passed to `run_transformations`. Defaults to True.
        store_doc_text (bool, optional): Whether to store the document texts. Defaults to True.
        num_workers (Optional[int], optional): The number of parallel processes to use.
            If set to None, then sequential compute is used. Defaults to None.

    Returns:
        Sequence[BaseNode]: The set of transformed Nodes/Documents

    """
    input_nodes = self._prepare_inputs(documents, nodes)

    effective_strategy = self.docstore_strategy
    if (
        self.docstore is not None
        and self.vector_store is None
        and self.docstore_strategy
        in (DocstoreStrategy.UPSERTS, DocstoreStrategy.UPSERTS_AND_DELETE)
    ):
        warnings.warn(
            f"docstore_strategy='{self.docstore_strategy.value}' requires a vector store "
            "to apply upsert/delete semantics; falling back to 'duplicates_only' for this run. "
            "pipeline.docstore_strategy is unchanged.",
            UserWarning,
            stacklevel=3,
        )
        effective_strategy = DocstoreStrategy.DUPLICATES_ONLY

    # check if we need to dedup
    if self.docstore is not None and self.vector_store is not None:
        if effective_strategy in (
            DocstoreStrategy.UPSERTS,
            DocstoreStrategy.UPSERTS_AND_DELETE,
        ):
            nodes_to_run = await self._ahandle_upserts(
                input_nodes, store_doc_text=store_doc_text
            )
        elif effective_strategy == DocstoreStrategy.DUPLICATES_ONLY:
            nodes_to_run = await self._ahandle_duplicates(
                input_nodes, store_doc_text=store_doc_text
            )
        else:
            raise ValueError(f"Invalid docstore strategy: {effective_strategy}")
    elif self.docstore is not None and self.vector_store is None:
        nodes_to_run = await self._ahandle_duplicates(
            input_nodes, store_doc_text=store_doc_text
        )
    else:
        nodes_to_run = input_nodes

    if num_workers and num_workers  1:
        num_cpus = multiprocessing.cpu_count()
        if num_workers  num_cpus:
            warnings.warn(
                "Specified num_workers exceed number of CPUs in the system. "
                "Setting `num_workers` down to the maximum CPU count.",
                stacklevel=2,
            )
            num_workers = num_cpus

        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor(max_workers=num_workers) as p:
            node_batches = self._node_batcher(
                num_batches=num_workers, nodes=nodes_to_run
            )
            tasks = [
                loop.run_in_executor(
                    p,
                    partial(
                        arun_transformations_wrapper,
                        transformations=self.transformations,
                        in_place=in_place,
                        cache=self.cache if not self.disable_cache else None,
                        cache_collection=cache_collection,
                    ),
                    batch,
                )
                for batch in node_batches
            ]
            result: Sequence[Sequence[BaseNode]] = await asyncio.gather(*tasks)
            nodes: Sequence[BaseNode] = reduce(lambda x, y: x + y, result, [])  # type: ignore
    else:
        nodes = await arun_transformations(  # type: ignore
            nodes_to_run,
            self.transformations,
            show_progress=show_progress,
            cache=self.cache if not self.disable_cache else None,
            cache_collection=cache_collection,
            in_place=in_place,
            **kwargs,
        )
        nodes = nodes

    nodes = nodes or []

    if self.vector_store is not None:
        nodes_with_embeddings = [n for n in nodes if n.embedding is not None]
        if nodes_with_embeddings:
            await self.vector_store.async_add(nodes_with_embeddings)

    if self.docstore is not None:
        await self._aupdate_docstore(
            nodes_to_run,
            effective_strategy=effective_strategy,
            store_doc_text=store_doc_text,
        )

    return nodes

```
 |  
| --- | --- |  
##  remove_unstable_values [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/#llama_index.core.ingestion.pipeline.remove_unstable_values "Permanent link")

```
remove_unstable_values(s: ) -> 

```

Remove unstable key/value pairs.
Examples include: - <**main**.Test object at 0x7fb9f3793f50> - 
Source code in `llama-index-core/llama_index/core/ingestion/pipeline.py`  
| 
```
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
defremove_unstable_values(s: str) -> str:
"""
    Remove unstable key/value pairs.

    Examples include:
    - <__main__.Test object at 0x7fb9f3793f50>
    - <function test_fn at 0x7fb9f37a8900>
    """
    pattern = r"<[\w\s_\. ]+ at 0x[a-z0-9]+>"
    return re.sub(pattern, "", s)

```
 |  
| --- | --- |  
##  get_transformation_hash [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/#llama_index.core.ingestion.pipeline.get_transformation_hash "Permanent link")

```
get_transformation_hash(
    nodes: Sequence[],
    transformation: ,
) -> 

```

Get the hash of a transformation.
Source code in `llama-index-core/llama_index/core/ingestion/pipeline.py`  
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
```
 | 
```
defget_transformation_hash(
    nodes: Sequence[BaseNode], transformation: TransformComponent
) -> str:
"""Get the hash of a transformation."""
    nodes_str = "".join(
        [str(node.get_content(metadata_mode=MetadataMode.ALL)) for node in nodes]
    )

    transformation_dict = transformation.to_dict()
    transform_string = remove_unstable_values(str(transformation_dict))

    return sha256((nodes_str + transform_string).encode("utf-8")).hexdigest()

```
 |  
| --- | --- |  
##  run_transformations [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/#llama_index.core.ingestion.pipeline.run_transformations "Permanent link")

```
run_transformations(
    nodes: Sequence[],
    transformations: Sequence[],
    in_place:  = True,
    cache: Optional[IngestionCache] = None,
    cache_collection: Optional[] = None,
    show_progress:  = False,
    **kwargs: 
) -> Sequence[]

```

Run a series of transformations on a set of nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]`  |  The nodes to transform.  |  _required_  |  
|  `transformations`  |  `Sequence[TransformComponent[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TransformComponent "TransformComponent \(llama_index.core.schema.TransformComponent\)")]`  |  The transformations to apply to the nodes.  |  _required_  |  
|  `show_progress`  |  `bool`  |  Whether to show progress bar for transformations.  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]`  |  The transformed nodes.  |  
Source code in `llama-index-core/llama_index/core/ingestion/pipeline.py`  
| 
```
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
```
 | 
```
defrun_transformations(
    nodes: Sequence[BaseNode],
    transformations: Sequence[TransformComponent],
    in_place: bool = True,
    cache: Optional[IngestionCache] = None,
    cache_collection: Optional[str] = None,
    show_progress: bool = False,
    **kwargs: Any,
) -> Sequence[BaseNode]:
"""
    Run a series of transformations on a set of nodes.

    Args:
        nodes: The nodes to transform.
        transformations: The transformations to apply to the nodes.
        show_progress: Whether to show progress bar for transformations.

    Returns:
        The transformed nodes.

    """
    if not in_place:
        nodes = list(nodes)

    transformations_with_progress = get_tqdm_iterable(
        transformations, show_progress, "Applying transformations"
    )

    for transform in transformations_with_progress:
        if cache is not None:
            hash = get_transformation_hash(nodes, transform)
            cached_nodes = cache.get(hash, collection=cache_collection)
            if cached_nodes is not None:
                nodes = cached_nodes
            else:
                nodes = transform(nodes, **kwargs)
                cache.put(hash, nodes, collection=cache_collection)
        else:
            nodes = transform(nodes, **kwargs)

    return nodes

```
 |  
| --- | --- |  
##  arun_transformations [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/#llama_index.core.ingestion.pipeline.arun_transformations "Permanent link")

```
arun_transformations(
    nodes: Sequence[],
    transformations: Sequence[],
    in_place:  = True,
    cache: Optional[IngestionCache] = None,
    cache_collection: Optional[] = None,
    show_progress:  = False,
    **kwargs: 
) -> Sequence[]

```

Run a series of transformations on a set of nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]`  |  The nodes to transform.  |  _required_  |  
|  `transformations`  |  `Sequence[TransformComponent[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TransformComponent "TransformComponent \(llama_index.core.schema.TransformComponent\)")]`  |  The transformations to apply to the nodes.  |  _required_  |  
|  `show_progress`  |  `bool`  |  Whether to show progress bar for transformations.  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]`  |  The transformed nodes.  |  
Source code in `llama-index-core/llama_index/core/ingestion/pipeline.py`  
| 
```
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
```
 | 
```
async defarun_transformations(
    nodes: Sequence[BaseNode],
    transformations: Sequence[TransformComponent],
    in_place: bool = True,
    cache: Optional[IngestionCache] = None,
    cache_collection: Optional[str] = None,
    show_progress: bool = False,
    **kwargs: Any,
) -> Sequence[BaseNode]:
"""
    Run a series of transformations on a set of nodes.

    Args:
        nodes: The nodes to transform.
        transformations: The transformations to apply to the nodes.
        show_progress: Whether to show progress bar for transformations.

    Returns:
        The transformed nodes.

    """
    if not in_place:
        nodes = list(nodes)

    transformations_with_progress = get_tqdm_iterable(
        transformations, show_progress, "Applying transformations"
    )

    for transform in transformations_with_progress:
        if cache is not None:
            hash = get_transformation_hash(nodes, transform)

            cached_nodes = cache.get(hash, collection=cache_collection)
            if cached_nodes is not None:
                nodes = cached_nodes
            else:
                nodes = await transform.acall(nodes, **kwargs)
                cache.put(hash, nodes, collection=cache_collection)
        else:
            nodes = await transform.acall(nodes, **kwargs)

    return nodes

```
 |  
| --- | --- |  
##  arun_transformations_wrapper [#](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/#llama_index.core.ingestion.pipeline.arun_transformations_wrapper "Permanent link")

```
arun_transformations_wrapper(
    nodes: Sequence[],
    transformations: Sequence[],
    in_place:  = True,
    cache: Optional[IngestionCache] = None,
    cache_collection: Optional[] = None,
    **kwargs: 
) -> Sequence[]

```

Wrapper for async run_transformation. To be used in loop.run_in_executor within a ProcessPoolExecutor.
Source code in `llama-index-core/llama_index/core/ingestion/pipeline.py`  
| 
```
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
```
 | 
```
defarun_transformations_wrapper(
    nodes: Sequence[BaseNode],
    transformations: Sequence[TransformComponent],
    in_place: bool = True,
    cache: Optional[IngestionCache] = None,
    cache_collection: Optional[str] = None,
    **kwargs: Any,
) -> Sequence[BaseNode]:
"""
    Wrapper for async run_transformation. To be used in loop.run_in_executor
    within a ProcessPoolExecutor.
    """
    loop = asyncio.new_event_loop()
    nodes = loop.run_until_complete(
        arun_transformations(
            nodes=nodes,
            transformations=transformations,
            in_place=in_place,
            cache=cache,
            cache_collection=cache_collection,
            **kwargs,
        )
    )
    loop.close()
    return nodes

```
 |  
| --- | --- |  
options: members: - IngestionPipeline - DocstoreStrategy
