# Oracledb
##  OraLlamaVS [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/oracledb/#llama_index.vector_stores.oracledb.OraLlamaVS "Permanent link")
Bases: 
`OraLlamaVS` vector store.
To use, you should have both: - the `oracledb` python package installed - a connection string associated with a OracleVS having deployed an Search index
Example
.. code-block:: python

```
from llama-index.core.vectorstores import OracleVS
from oracledb import oracledb

with oracledb.connect(user = user, passwd = pwd, dsn = dsn) as connection:
    print ("Database version:", connection.version)

```
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-oracledb/llama_index/vector_stores/oracledb/base.py`  
| 
```
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
```
 | 
```
classOraLlamaVS(BasePydanticVectorStore):
"""
    `OraLlamaVS` vector store.

    To use, you should have both:
    - the ``oracledb`` python package installed
    - a connection string associated with a OracleVS having deployed an
       Search index

    Example:
        .. code-block:: python

            from llama-index.core.vectorstores import OracleVS
            from oracledb import oracledb

            with oracledb.connect(user = user, passwd = pwd, dsn = dsn) as connection:
                print ("Database version:", connection.version)

    """

    AMPLIFY_RATIO_LE5: ClassVar[int] = 100
    AMPLIFY_RATIO_GT5: ClassVar[int] = 20
    AMPLIFY_RATIO_GT50: ClassVar[int] = 10
    metadata_column: str = "metadata"
    stores_text: bool = True
    _client: Connection = PrivateAttr()
    table_name: str
    distance_strategy: DistanceStrategy
    batch_size: Optional[int]
    params: Optional[dict[str, Any]]

    def__init__(
        self,
        _client: Connection,
        table_name: str,
        distance_strategy: DistanceStrategy = DistanceStrategy.EUCLIDEAN_DISTANCE,
        batch_size: Optional[int] = 32,
        params: Optional[dict[str, Any]] = None,
    ):
        try:
            importoracledb
        except ImportError as e:
            raise ImportError(
                "Unable to import oracledb, please install with "
                "`pip install -U oracledb`."
            ) frome

        try:
"""Initialize with necessary components."""
            super().__init__(
                table_name=table_name,
                distance_strategy=distance_strategy,
                batch_size=batch_size,
                params=params,
            )
            connection = _get_connection(_client)
            # Assign _client to PrivateAttr after the Pydantic initialization
            object.__setattr__(self, "_client", _client)
            _create_table(connection, table_name)

        except oracledb.DatabaseError as db_err:
            logger.exception(f"Database error occurred while create table: {db_err}")
            raise RuntimeError(
                "Failed to create table due to a database error."
            ) fromdb_err
        except ValueError as val_err:
            logger.exception(f"Validation error: {val_err}")
            raise RuntimeError(
                "Failed to create table due to a validation error."
            ) fromval_err
        except Exception as ex:
            logger.exception("An unexpected error occurred while creating the index.")
            raise RuntimeError(
                "Failed to create table due to an unexpected error."
            ) fromex

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._client

    @classmethod
    defclass_name(cls) -> str:
        return "OraLlamaVS"

    def_convert_oper_to_sql(
        self,
        oper: FilterOperator,
        metadata_column: str,
        filter_key: str,
        value_bind: str,
    ) -> str:
        if oper == FilterOperator.IS_EMPTY:
            return f"NOT JSON_EXISTS({metadata_column}, '$.{filter_key}') OR JSON_EQUAL(JSON_QUERY({metadata_column}, '$.{filter_key}'), '[]') OR JSON_EQUAL(JSON_QUERY({metadata_column}, '$.{filter_key}'), 'null')"
        elif oper == FilterOperator.CONTAINS:
            return f"JSON_EXISTS({metadata_column}, '$.{filter_key}[*]?(@ == $val)' PASSING {value_bind} AS \"val\")"
        else:
            oper_map = {
                FilterOperator.EQ: "{0}{1}",  # default operator (string, int, float)
                FilterOperator.GT: "{0}{1}",  # greater than (int, float)
                FilterOperator.LT: "{0}{1}",  # less than (int, float)
                FilterOperator.NE: "{0} != {1}",  # not equal to (string, int, float)
                FilterOperator.GTE: "{0} >= {1}",  # greater than or equal to (int, float)
                FilterOperator.LTE: "{0} <= {1}",  # less than or equal to (int, float)
                FilterOperator.IN: "{0} IN ({1})",  # In array (string or number)
                FilterOperator.NIN: "{0} NOT IN ({1})",  # Not in array (string or number)
                FilterOperator.TEXT_MATCH: "{0} LIKE '%' || {1} || '%'",  # full text match (allows you to search for a specific substring, token or phrase within the text field)
            }

            if oper not in oper_map:
                raise ValueError(
                    f"FilterOperation {oper} cannot be used with this vector store."
                )

            operation_f = oper_map.get(oper)

            return operation_f.format(
                f"JSON_VALUE({metadata_column}, '$.{filter_key}')", value_bind
            )

    def_get_filter_string(
        self, filter: MetadataFilters | MetadataFilter, bind_variables: list
    ) -> str:
        if isinstance(filter, MetadataFilter):
            if not re.match(r"^[a-zA-Z0-9_]+$", filter.key):
                raise ValueError(f"Invalid metadata key format: {filter.key}")

            value_bind = f""
            if filter.operator == FilterOperator.IS_EMPTY:
                # No values needed
                pass
            elif isinstance(filter.value, List):
                # Needs multiple binds for a list https://python-oracledb.readthedocs.io/en/latest/user_guide/bind.html#binding-multiple-values-to-a-sql-where-in-clause
                value_binds = []
                for val in filter.value:
                    value_binds.append(f":value{len(bind_variables)}")
                    bind_variables.append(val)
                value_bind = ",".join(value_binds)
            else:
                value_bind = f":value{len(bind_variables)}"
                bind_variables.append(filter.value)

            return self._convert_oper_to_sql(
                filter.operator, self.metadata_column, filter.key, value_bind
            )

        # Combine all sub filters
        filter_strings = [
            self._get_filter_string(f_, bind_variables) for f_ in filter.filters
        ]

        return f" {filter.condition.value.upper()} ".join(filter_strings)

    def_append_meta_filter_condition(
        self, where_str: Optional[str], filters: Optional[MetadataFilters]
    ) -> Tuple[str, list]:
        bind_variables = []

        filter_str = self._get_filter_string(filters, bind_variables)

        # Convert filter conditions to a single string
        if where_str is None:
            where_str = filter_str
        else:
            where_str += " AND " + filter_str

        return where_str, bind_variables

    def_build_insert(self, values: List[BaseNode]) -> Tuple[str, List[tuple]]:
        _data = []
        for item in values:
            item_values = tuple(
                column["extract_func"](item) for column in column_config.values()
            )
            _data.append(item_values)

        dml = f"""
           INSERT INTO {self.table_name} ({", ".join(column_config.keys())})
           VALUES ({", ".join([":"+str(i+1)foriinrange(len(column_config))])})
        """
        return dml, _data

    def_build_query(
        self, distance_function: str, k: int, where_str: Optional[str] = None
    ) -> str:
        where_clause = f"WHERE {where_str}" if where_str else ""

        return f"""
            SELECT id,
                doc_id,
                text,
                node_info,
                metadata,
                vector_distance(embedding, :embedding, {distance_function}) AS distance
            FROM {self.table_name}
{where_clause}
            ORDER BY distance
            FETCH APPROX FIRST {k} ROWS ONLY
        """

    def_build_hybrid_query(
        self, sub_query: str, query_str: str, similarity_top_k: int
    ) -> str:
        terms_pattern = [f"(?i){x}" for x in query_str.split(" ")]
        column_keys = column_config.keys()
        return (
            f"SELECT {','.join(filter(lambdak:k!='embedding',column_keys))}, "
            f"distance FROM ({sub_query}) temp_table "
            f"ORDER BY length(multiMatchAllIndices(text, {terms_pattern})) "
            f"AS distance1 DESC, "
            f"log(1 + countMatches(text, '(?i)({query_str.replace(' ','|')})')) "
            f"AS distance2 DESC limit {similarity_top_k}"
        )

    @_handle_exceptions
    defadd(self, nodes: list[BaseNode], **kwargs: Any) -> list[str]:
        if not nodes:
            return []

        connection = _get_connection(self._client)

        for result_batch in iter_batch(nodes, self.batch_size):
            dml, bind_values = self._build_insert(values=result_batch)

            with connection.cursor() as cursor:
                # Use executemany to insert the batch
                cursor.executemany(dml, bind_values)
                connection.commit()

        return [node.node_id for node in nodes]

    @_handle_exceptions
    defdelete(self, ref_doc_id: str, **kwargs: Any) -> None:
        connection = _get_connection(self._client)
        with connection.cursor() as cursor:
            ddl = f"DELETE FROM {self.table_name} WHERE doc_id = :ref_doc_id"
            cursor.execute(ddl, [ref_doc_id])
            connection.commit()

    @_handle_exceptions
    def_get_clob_value(self, result: Any) -> str:
        try:
            importoracledb
        except ImportError as e:
            raise ImportError(
                "Unable to import oracledb, please install with "
                "`pip install -U oracledb`."
            ) frome

        clob_value = ""
        if result:
            if isinstance(result, oracledb.LOB):
                raw_data = result.read()
                if isinstance(raw_data, bytes):
                    clob_value = raw_data.decode(
                        "utf-8"
                    )  # Specify the correct encoding
                else:
                    clob_value = raw_data
            elif isinstance(result, str):
                clob_value = result
            else:
                raise Exception("Unexpected type:", type(result))
        return clob_value

    @_handle_exceptions
    defdrop(self) -> None:
        drop_table_purge(self._client, self.table_name)

    @_handle_exceptions
    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        distance_function = _get_distance_function(self.distance_strategy)
        where_str = None
        params = {}
        if query.doc_ids:
            placeholders = ", ".join([f":doc_id{i}" for i in range(len(query.doc_ids))])
            where_str = f"doc_id in ({placeholders})"
            for i, doc_id in enumerate(query.doc_ids):
                params[f"doc_id{i}"] = doc_id

        bind_vars = []
        if query.filters is not None:
            where_str, bind_vars = self._append_meta_filter_condition(
                where_str, query.filters
            )

        # build query sql
        query_sql = self._build_query(
            distance_function, query.similarity_top_k, where_str
        )
"""
        if query.mode == VectorStoreQueryMode.HYBRID and query.query_str is not None:
            amplify_ratio = self.AMPLIFY_RATIO_LE5
            if 5 < query.similarity_top_k < 50:
                amplify_ratio = self.AMPLIFY_RATIO_GT5
            if query.similarity_top_k > 50:
                amplify_ratio = self.AMPLIFY_RATIO_GT50
            query_sql = self._build_hybrid_query(
                self._build_query(
                    query_embed=query.query_embedding,
                    k=query.similarity_top_k,
                    where_str=where_str,
                    limit=query.similarity_top_k * amplify_ratio,

                query.query_str,
                query.similarity_top_k,

            logger.debug(f"hybrid query_statement={query_statement}")
        """
        embedding = array.array("f", query.query_embedding)
        params = {"embedding": embedding}
        for i, value in enumerate(bind_vars):
            params[f"value{i}"] = value

        connection = _get_connection(self._client)
        with connection.cursor() as cursor:
            cursor.execute(query_sql, **params)
            results = cursor.fetchall()

            similarities = []
            ids = []
            nodes = []
            for result in results:
                doc_id = result[1]
                text = self._get_clob_value(result[2])
                node_info = (
                    json.loads(result[3]) if isinstance(result[3], str) else result[3]
                )
                metadata = (
                    json.loads(result[4]) if isinstance(result[4], str) else result[4]
                )

                if query.node_ids:
                    if result[0] not in query.node_ids:
                        continue

                if isinstance(node_info, dict):
                    start_char_idx = node_info.get("start", None)
                    end_char_idx = node_info.get("end", None)
                try:
                    node = metadata_dict_to_node(metadata)
                    node.set_content(text)
                except Exception:
                    # Note: deprecated legacy logic for backward compatibility

                    node = TextNode(
                        id_=result[0],
                        text=text,
                        metadata=metadata,
                        start_char_idx=start_char_idx,
                        end_char_idx=end_char_idx,
                        relationships={
                            NodeRelationship.SOURCE: RelatedNodeInfo(node_id=doc_id)
                        },
                    )

                nodes.append(node)
                similarities.append(1.0 - math.exp(-result[5]))
                ids.append(result[0])
            return VectorStoreQueryResult(
                nodes=nodes, similarities=similarities, ids=ids
            )

    @classmethod
    @_handle_exceptions
    deffrom_documents(
        cls: Type[OraLlamaVS],
        docs: List[TextNode],
        table_name: str = "llama_index",
        **kwargs: Any,
    ) -> OraLlamaVS:
"""Return VectorStore initialized from texts and embeddings."""
        _client = kwargs.get("client")
        if _client is None:
            raise ValueError("client parameter is required...")
        params = kwargs.get("params")
        distance_strategy = kwargs.get("distance_strategy")
        drop_table_purge(_client, table_name)

        vss = cls(
            _client=_client,
            table_name=table_name,
            params=params,
            distance_strategy=distance_strategy,
        )
        vss.add(nodes=docs)
        return vss

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/oracledb/#llama_index.vector_stores.oracledb.OraLlamaVS.client "Permanent link")

```
client: 

```

Get client.
###  from_documents `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/oracledb/#llama_index.vector_stores.oracledb.OraLlamaVS.from_documents "Permanent link")

```
from_documents(
    docs: [],
    table_name:  = "llama_index",
    **kwargs: 
) -> 

```

Return VectorStore initialized from texts and embeddings.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-oracledb/llama_index/vector_stores/oracledb/base.py`  
| 
```
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
```
 | 
```
@classmethod
@_handle_exceptions
deffrom_documents(
    cls: Type[OraLlamaVS],
    docs: List[TextNode],
    table_name: str = "llama_index",
    **kwargs: Any,
) -> OraLlamaVS:
"""Return VectorStore initialized from texts and embeddings."""
    _client = kwargs.get("client")
    if _client is None:
        raise ValueError("client parameter is required...")
    params = kwargs.get("params")
    distance_strategy = kwargs.get("distance_strategy")
    drop_table_purge(_client, table_name)

    vss = cls(
        _client=_client,
        table_name=table_name,
        params=params,
        distance_strategy=distance_strategy,
    )
    vss.add(nodes=docs)
    return vss

```
 |  
| --- | --- |  
options: members: - OraLlamaVS
