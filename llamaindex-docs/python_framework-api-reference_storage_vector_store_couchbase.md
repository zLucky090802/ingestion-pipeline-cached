# Couchbase
Couchbase vector stores.
##  CouchbaseVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.CouchbaseVectorStore "Permanent link")
Bases: 
Couchbase Vector Store (deprecated).
This class is deprecated, please use CouchbaseSearchVectorStore instead.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-couchbase/llama_index/vector_stores/couchbase/base.py`  
| 
```
938
939
940
941
942
943
944
945
946
947
948
949
950
951
952
953
954
955
956
957
958
959
960
961
962
963
964
965
966
967
968
969
970
971
972
973
974
975
976
977
```
 | 
```
classCouchbaseVectorStore(CouchbaseSearchVectorStore):
"""
    Couchbase Vector Store (deprecated).

    This class is deprecated, please use CouchbaseSearchVectorStore instead.
    """

    def__init__(
        self,
        cluster: Any,
        bucket_name: str,
        scope_name: str,
        collection_name: str,
        index_name: str,
        text_key: Optional[str] = "text",
        embedding_key: Optional[str] = "embedding",
        metadata_key: Optional[str] = "metadata",
        scoped_index: bool = True,
    ) -> None:
"""
        Initializes a connection to a Couchbase Vector Store.

        This class is deprecated, please use CouchbaseSearchVectorStore instead.
        """
        warnings.warn(
            "CouchbaseVectorStore is deprecated, please use CouchbaseSearchVectorStore instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(
            cluster,
            bucket_name,
            scope_name,
            collection_name,
            index_name,
            text_key,
            embedding_key,
            metadata_key,
            scoped_index,
        )

```
 |  
| --- | --- |  
##  CouchbaseSearchVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.CouchbaseSearchVectorStore "Permanent link")
Bases: 
Couchbase Vector Store using Search Vector Indexes (FTS-based).
This implementation uses Couchbase's Search Vector Indexes, which combine Full-Text Search (FTS) with vector search capabilities. Ideal for hybrid searches combining vector similarity, full-text search, and geospatial queries.
Supports datasets up to tens of millions of documents. Requires Couchbase Server 7.6 or later.
To use, you should have the `couchbase` python package installed.
For more information, see: https://docs.couchbase.com/server/current/vector-index/use-vector-indexes.html
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-couchbase/llama_index/vector_stores/couchbase/base.py`  
| 
```
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
```
 | 
```
classCouchbaseSearchVectorStore(CouchbaseVectorStoreBase):
"""
    Couchbase Vector Store using Search Vector Indexes (FTS-based).

    This implementation uses Couchbase's Search Vector Indexes, which combine
    Full-Text Search (FTS) with vector search capabilities. Ideal for hybrid
    searches combining vector similarity, full-text search, and geospatial queries.

    Supports datasets up to tens of millions of documents.
    Requires Couchbase Server 7.6 or later.

    To use, you should have the ``couchbase`` python package installed.

    For more information, see:
    https://docs.couchbase.com/server/current/vector-index/use-vector-indexes.html
    """

    _index_name: str = PrivateAttr()
    _scoped_index: bool = PrivateAttr()

    def__init__(
        self,
        cluster: Any,
        bucket_name: str,
        scope_name: str,
        collection_name: str,
        index_name: str,
        text_key: Optional[str] = "text",
        embedding_key: Optional[str] = "embedding",
        metadata_key: Optional[str] = "metadata",
        scoped_index: bool = True,
        query_options: Optional[QueryOptions] = None,
    ) -> None:
"""
        Initializes a connection to a Couchbase Vector Store using FTS.

        Args:
            cluster (Cluster): Couchbase cluster object with active connection.
            bucket_name (str): Name of bucket to store documents in.
            scope_name (str): Name of scope in the bucket to store documents in.
            collection_name (str): Name of collection in the scope to store documents in.
            index_name (str): Name of the Search index.
            text_key (Optional[str], optional): The field for the document text.
                Defaults to "text".
            embedding_key (Optional[str], optional): The field for the document embedding.
                Defaults to "embedding".
            metadata_key (Optional[str], optional): The field for the document metadata.
                Defaults to "metadata".
            scoped_index (Optional[bool]): specify whether the index is a scoped index.
                Set to True by default.
            query_options (Optional[QueryOptions]): Query options for SQL++ queries.
                Defaults to None.

        Returns:
            None

        """
        super().__init__(
            cluster=cluster,
            bucket_name=bucket_name,
            scope_name=scope_name,
            collection_name=collection_name,
            text_key=text_key,
            embedding_key=embedding_key,
            metadata_key=metadata_key,
            query_options=query_options,
        )

        if not index_name:
            raise ValueError("index_name must be provided.")

        self._index_name = index_name
        self._scoped_index = scoped_index

        # Check if the index exists. Throws ValueError if it doesn't
        try:
            self._check_index_exists()
        except Exception as e:
            raise

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Executes a query in the vector store and returns the result.

        Args:
            query (VectorStoreQuery): The query object containing the search parameters.
            **kwargs (Any): Additional keyword arguments.
                cb_search_options (Dict): Search options to pass to Couchbase Search

        Returns:
            VectorStoreQueryResult: The result of the query containing the top-k nodes, similarities, and ids.

        """
        fields = query.output_fields

        if not fields:
            fields = ["*"]

        # Document text field needs to be returned from the search
        if self._text_key not in fields and fields != ["*"]:
            fields.append(self._text_key)

        logger.debug("Output Fields: ", fields)

        k = query.similarity_top_k

        # Get the search options
        search_options = kwargs.get("cb_search_options", {})

        if search_options and query.filters:
            raise ValueError("Cannot use both filters and cb_search_options")
        elif query.filters:
            couchbase_options = _to_couchbase_filter(query.filters)
            logger.debug(f"Filters transformed to Couchbase: {couchbase_options}")
            search_options = couchbase_options

        logger.debug(f"Filters: {search_options}")

        # Create Search Request
        search_req = search.SearchRequest.create(
            VectorSearch.from_vector_query(
                VectorQuery(
                    self._embedding_key,
                    query.query_embedding,
                    k,
                )
            )
        )

        try:
            logger.debug("Querying Couchbase")
            if self._scoped_index:
                search_iter = self._scope.search(
                    self._index_name,
                    search_req,
                    SearchOptions(limit=k, fields=fields, raw=search_options),
                )

            else:
                search_iter = self._cluster.search(
                    self._index_name,
                    search_req,
                    SearchOptions(limit=k, fields=fields, raw=search_options),
                )
        except Exception as e:
            logger.debug(f"Search failed with error {e}")
            raise ValueError(f"Search failed with error: {e}")

        top_k_nodes = []
        top_k_scores = []
        top_k_ids = []

        # Parse the results
        for result in search_iter.rows():
            text = result.fields.pop(self._text_key, "")

            score = result.score

            # Format the metadata into a dictionary
            metadata_dict = self._format_metadata(result.fields)

            id = result.id

            try:
                node = metadata_dict_to_node(metadata_dict, text)
            except Exception:
                # Deprecated legacy logic for backwards compatibility
                node = TextNode(
                    text=text,
                    id_=id,
                    score=score,
                    metadata=metadata_dict,
                )

            top_k_nodes.append(node)
            top_k_scores.append(score)
            top_k_ids.append(id)

        return VectorStoreQueryResult(
            nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
        )

    def_check_index_exists(self) -> bool:
"""
        Check if the Search index exists in the linked Couchbase cluster
        Returns:
            bool: True if the index exists, False otherwise.
            Raises a ValueError if the index does not exist.
        """
        if self._scoped_index:
            all_indexes = [
                index.name for index in self._scope.search_indexes().get_all_indexes()
            ]
            if self._index_name not in all_indexes:
                raise ValueError(
                    f"Index {self._index_name} does not exist. "
                    " Please create the index before searching."
                )
        else:
            all_indexes = [
                index.name for index in self._cluster.search_indexes().get_all_indexes()
            ]
            if self._index_name not in all_indexes:
                raise ValueError(
                    f"Index {self._index_name} does not exist. "
                    " Please create the index before searching."
                )

        return True

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.CouchbaseSearchVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Executes a query in the vector store and returns the result.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  The query object containing the search parameters.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments. cb_search_options (Dict): Search options to pass to Couchbase Search  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  The result of the query containing the top-k nodes, similarities, and ids.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-couchbase/llama_index/vector_stores/couchbase/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Executes a query in the vector store and returns the result.

    Args:
        query (VectorStoreQuery): The query object containing the search parameters.
        **kwargs (Any): Additional keyword arguments.
            cb_search_options (Dict): Search options to pass to Couchbase Search

    Returns:
        VectorStoreQueryResult: The result of the query containing the top-k nodes, similarities, and ids.

    """
    fields = query.output_fields

    if not fields:
        fields = ["*"]

    # Document text field needs to be returned from the search
    if self._text_key not in fields and fields != ["*"]:
        fields.append(self._text_key)

    logger.debug("Output Fields: ", fields)

    k = query.similarity_top_k

    # Get the search options
    search_options = kwargs.get("cb_search_options", {})

    if search_options and query.filters:
        raise ValueError("Cannot use both filters and cb_search_options")
    elif query.filters:
        couchbase_options = _to_couchbase_filter(query.filters)
        logger.debug(f"Filters transformed to Couchbase: {couchbase_options}")
        search_options = couchbase_options

    logger.debug(f"Filters: {search_options}")

    # Create Search Request
    search_req = search.SearchRequest.create(
        VectorSearch.from_vector_query(
            VectorQuery(
                self._embedding_key,
                query.query_embedding,
                k,
            )
        )
    )

    try:
        logger.debug("Querying Couchbase")
        if self._scoped_index:
            search_iter = self._scope.search(
                self._index_name,
                search_req,
                SearchOptions(limit=k, fields=fields, raw=search_options),
            )

        else:
            search_iter = self._cluster.search(
                self._index_name,
                search_req,
                SearchOptions(limit=k, fields=fields, raw=search_options),
            )
    except Exception as e:
        logger.debug(f"Search failed with error {e}")
        raise ValueError(f"Search failed with error: {e}")

    top_k_nodes = []
    top_k_scores = []
    top_k_ids = []

    # Parse the results
    for result in search_iter.rows():
        text = result.fields.pop(self._text_key, "")

        score = result.score

        # Format the metadata into a dictionary
        metadata_dict = self._format_metadata(result.fields)

        id = result.id

        try:
            node = metadata_dict_to_node(metadata_dict, text)
        except Exception:
            # Deprecated legacy logic for backwards compatibility
            node = TextNode(
                text=text,
                id_=id,
                score=score,
                metadata=metadata_dict,
            )

        top_k_nodes.append(node)
        top_k_scores.append(score)
        top_k_ids.append(id)

    return VectorStoreQueryResult(
        nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
    )

```
 |  
| --- | --- |  
##  CouchbaseQueryVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.CouchbaseQueryVectorStore "Permanent link")
Bases: 
Couchbase Vector Store using Query Service with vector search capabilities.
This implementation supports both Hyperscale Vector Indexes and Composite Vector Indexes, which use the Couchbase Query Service with SQL++ and vector search functions.
Hyperscale Vector Indexes: - Purpose-built for pure vector searches at massive scale - Lowest memory footprint (most index data on disk) - Higher accuracy at lower quantizations - Best for content discovery, RAG workflows, image search, anomaly detection
Composite Vector Indexes: - Combine Global Secondary Index (GSI) with vector search functions - Scalar filters applied BEFORE vector search (reduces vectors to compare) - Best for searches combining vector similarity with scalar filters - Useful for compliance requirements (can exclude results based on scalars)
Key features: - Supports both ANN (Approximate) and KNN (Exact) nearest neighbor searches - Can scale to billions of documents - Various similarity metrics (COSINE, DOT, L2/EUCLIDEAN, L2_SQUARED)
Requires Couchbase Server 8.0 or later.
For more information, see: https://docs.couchbase.com/server/current/vector-index/use-vector-indexes.html
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-couchbase/llama_index/vector_stores/couchbase/base.py`  
| 
```
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
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
921
922
923
924
925
926
927
928
929
930
931
932
933
934
935
```
 | 
```
classCouchbaseQueryVectorStore(CouchbaseVectorStoreBase):
"""
    Couchbase Vector Store using Query Service with vector search capabilities.

    This implementation supports both Hyperscale Vector Indexes and Composite Vector
    Indexes, which use the Couchbase Query Service with SQL++ and vector search functions.

    Hyperscale Vector Indexes:
    - Purpose-built for pure vector searches at massive scale
    - Lowest memory footprint (most index data on disk)
    - Higher accuracy at lower quantizations
    - Best for content discovery, RAG workflows, image search, anomaly detection

    Composite Vector Indexes:
    - Combine Global Secondary Index (GSI) with vector search functions
    - Scalar filters applied BEFORE vector search (reduces vectors to compare)
    - Best for searches combining vector similarity with scalar filters
    - Useful for compliance requirements (can exclude results based on scalars)

    Key features:
    - Supports both ANN (Approximate) and KNN (Exact) nearest neighbor searches
    - Can scale to billions of documents
    - Various similarity metrics (COSINE, DOT, L2/EUCLIDEAN, L2_SQUARED)

    Requires Couchbase Server 8.0 or later.

    For more information, see:
    https://docs.couchbase.com/server/current/vector-index/use-vector-indexes.html
    """

    _search_type: QueryVectorSearchType = PrivateAttr()
    _similarity: str = PrivateAttr()
    _query_timeout: timedelta = PrivateAttr()

    def__init__(
        self,
        cluster: Any,
        bucket_name: str,
        scope_name: str,
        collection_name: str,
        search_type: Union[QueryVectorSearchType, str],
        similarity: Union[QueryVectorSearchSimilarity, str],
        nprobes: Optional[int] = None,
        text_key: Optional[str] = "text",
        embedding_key: Optional[str] = "embedding",
        metadata_key: Optional[str] = "metadata",
        query_options: Optional[QueryOptions] = None,
    ) -> None:
"""
        Initializes a connection to a Couchbase Vector Store using GSI.

        Args:
            cluster (Cluster): Couchbase cluster object with active connection.
            bucket_name (str): Name of bucket to store documents in.
            scope_name (str): Name of scope in the bucket to store documents in.
            collection_name (str): Name of collection in the scope to store documents in.
            search_type (Union[QueryVectorSearchType, str]): Type of vector search (ANN or KNN).
                Defaults to ANN.
            similarity (str): Similarity metric to use (cosine, euclidean, dot_product).
                Defaults to "cosine".
            nprobes (Optional[int], optional): Number of probes for the ANN search.
                Defaults to None, uses the value set at index creation time.
            text_key (Optional[str], optional): The field for the document text.
                Defaults to "text".
            embedding_key (Optional[str], optional): The field for the document embedding.
                Defaults to "embedding".
            metadata_key (Optional[str], optional): The field for the document metadata.
                Defaults to "metadata".
            query_options (Optional[QueryOptions]): Query options for SQL++ queries.
                Defaults to 60 seconds.

        Returns:
            None

        """
        super().__init__(
            cluster=cluster,
            bucket_name=bucket_name,
            scope_name=scope_name,
            collection_name=collection_name,
            text_key=text_key,
            embedding_key=embedding_key,
            metadata_key=metadata_key,
            query_options=query_options,
        )

        if isinstance(search_type, str):
            search_type = QueryVectorSearchType(search_type)

        self._search_type = search_type
        self._similarity = (
            similarity.upper()
            if isinstance(similarity, str)
            else (
                similarity.value
                if isinstance(similarity, QueryVectorSearchSimilarity)
                else None
            )
        )
        self._nprobes = nprobes

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Executes a vector similarity query using GSI.

        Args:
            query (VectorStoreQuery): The query object containing the search parameters.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            VectorStoreQueryResult: The result of the query containing the top-k nodes, similarities, and ids.

        """
        if not query.query_embedding:
            raise ValueError("Query embedding must not be empty")

        k = query.similarity_top_k
        query_context = (
            f"`{self._bucket_name}`.`{self._scope_name}`.`{self._collection_name}`"
        )

        # Convert embedding to string representation for query
        query_vector_str = str(query.query_embedding)

        # Handle filters if provided
        where_clause = ""
        if query.filters:
            try:
                # Convert LlamaIndex filters to SQL++ conditions
                filter_sql = _convert_llamaindex_filters_to_sql(
                    query.filters, self._metadata_key
                )
                if filter_sql:
                    where_clause = f"WHERE {filter_sql}"
            except Exception as e:
                logger.warning(f"Failed to process filters: {e}")

        if query.output_fields:
            fields = query.output_fields.join(",")
        else:
            fields = "d.*, meta().id as id"

        nprobes = self._nprobes
        if kwargs.get("nprobes"):
            nprobes = kwargs.get("nprobes")

        # Determine the appropriate distance function based on search type
        if self._search_type == QueryVectorSearchType.ANN:
            nprobes_exp = f", {nprobes}" if nprobes else ""
            distance_function_exp = f"APPROX_VECTOR_DISTANCE(d.{self._embedding_key}, {query_vector_str}, '{self._similarity}'{nprobes_exp})"
        else:
            distance_function_exp = f"VECTOR_DISTANCE(d.{self._embedding_key}, {query_vector_str}, '{self._similarity}')"

        # Build the SQL++ query
        query_str = f"""
        SELECT {fields}, {distance_function_exp} as score
        FROM {query_context} d
{where_clause}
        ORDER BY score
        LIMIT {k}
        """

        try:
            # Execute the query
            result = self._cluster.query(query_str, self._query_options)

            top_k_nodes = []
            top_k_scores = []
            top_k_ids = []

            # Process results
            for row in result.rows():
                doc_id = row.get("id", "")
                text = row.get(self._text_key, "")
                score = row.get("score")

                # Extract metadata
                metadata_dict = {}
                if self._metadata_key in row:
                    metadata_dict = row[self._metadata_key]
                try:
                    node = metadata_dict_to_node(metadata_dict, text)
                    node.node_id = doc_id
                except Exception:
                    # Fallback for backwards compatibility
                    node = TextNode(
                        text=text,
                        id_=doc_id,
                        score=score,
                        metadata=metadata_dict,
                    )

                top_k_nodes.append(node)
                top_k_scores.append(score)
                top_k_ids.append(doc_id)

            return VectorStoreQueryResult(
                nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
            )

        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            raise ValueError(f"Vector search failed with error: {e}")

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.CouchbaseQueryVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Executes a vector similarity query using GSI.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  The query object containing the search parameters.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  The result of the query containing the top-k nodes, similarities, and ids.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-couchbase/llama_index/vector_stores/couchbase/base.py`  
| 
```
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
921
922
923
924
925
926
927
928
929
930
931
932
933
934
935
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Executes a vector similarity query using GSI.

    Args:
        query (VectorStoreQuery): The query object containing the search parameters.
        **kwargs (Any): Additional keyword arguments.

    Returns:
        VectorStoreQueryResult: The result of the query containing the top-k nodes, similarities, and ids.

    """
    if not query.query_embedding:
        raise ValueError("Query embedding must not be empty")

    k = query.similarity_top_k
    query_context = (
        f"`{self._bucket_name}`.`{self._scope_name}`.`{self._collection_name}`"
    )

    # Convert embedding to string representation for query
    query_vector_str = str(query.query_embedding)

    # Handle filters if provided
    where_clause = ""
    if query.filters:
        try:
            # Convert LlamaIndex filters to SQL++ conditions
            filter_sql = _convert_llamaindex_filters_to_sql(
                query.filters, self._metadata_key
            )
            if filter_sql:
                where_clause = f"WHERE {filter_sql}"
        except Exception as e:
            logger.warning(f"Failed to process filters: {e}")

    if query.output_fields:
        fields = query.output_fields.join(",")
    else:
        fields = "d.*, meta().id as id"

    nprobes = self._nprobes
    if kwargs.get("nprobes"):
        nprobes = kwargs.get("nprobes")

    # Determine the appropriate distance function based on search type
    if self._search_type == QueryVectorSearchType.ANN:
        nprobes_exp = f", {nprobes}" if nprobes else ""
        distance_function_exp = f"APPROX_VECTOR_DISTANCE(d.{self._embedding_key}, {query_vector_str}, '{self._similarity}'{nprobes_exp})"
    else:
        distance_function_exp = f"VECTOR_DISTANCE(d.{self._embedding_key}, {query_vector_str}, '{self._similarity}')"

    # Build the SQL++ query
    query_str = f"""
    SELECT {fields}, {distance_function_exp} as score
    FROM {query_context} d
{where_clause}
    ORDER BY score
    LIMIT {k}
    """

    try:
        # Execute the query
        result = self._cluster.query(query_str, self._query_options)

        top_k_nodes = []
        top_k_scores = []
        top_k_ids = []

        # Process results
        for row in result.rows():
            doc_id = row.get("id", "")
            text = row.get(self._text_key, "")
            score = row.get("score")

            # Extract metadata
            metadata_dict = {}
            if self._metadata_key in row:
                metadata_dict = row[self._metadata_key]
            try:
                node = metadata_dict_to_node(metadata_dict, text)
                node.node_id = doc_id
            except Exception:
                # Fallback for backwards compatibility
                node = TextNode(
                    text=text,
                    id_=doc_id,
                    score=score,
                    metadata=metadata_dict,
                )

            top_k_nodes.append(node)
            top_k_scores.append(score)
            top_k_ids.append(doc_id)

        return VectorStoreQueryResult(
            nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
        )

    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        raise ValueError(f"Vector search failed with error: {e}")

```
 |  
| --- | --- |  
##  CouchbaseVectorStoreBase [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.CouchbaseVectorStoreBase "Permanent link")
Bases: 
Base class for Couchbase Vector Stores providing common database operations.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-couchbase/llama_index/vector_stores/couchbase/base.py`  
| 
```
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
```
 | 
```
classCouchbaseVectorStoreBase(BasePydanticVectorStore):
"""
    Base class for Couchbase Vector Stores providing common database operations.
    """

    stores_text: bool = True
    flat_metadata: bool = True
    # Default batch size
    DEFAULT_BATCH_SIZE: int = 100

    _cluster: Cluster = PrivateAttr()
    _bucket: Bucket = PrivateAttr()
    _scope: Scope = PrivateAttr()
    _collection: Collection = PrivateAttr()
    _bucket_name: str = PrivateAttr()
    _scope_name: str = PrivateAttr()
    _collection_name: str = PrivateAttr()
    _text_key: str = PrivateAttr()
    _embedding_key: str = PrivateAttr()
    _metadata_key: str = PrivateAttr()
    _query_options: QueryOptions = PrivateAttr()

    def__init__(
        self,
        cluster: Any,
        bucket_name: str,
        scope_name: str,
        collection_name: str,
        text_key: Optional[str] = "text",
        embedding_key: Optional[str] = "embedding",
        metadata_key: Optional[str] = "metadata",
        query_options: Optional[QueryOptions] = None,
    ) -> None:
"""
        Base initialization for Couchbase Vector Stores.

        Args:
            cluster (Cluster): Couchbase cluster object with active connection.
            bucket_name (str): Name of bucket to store documents in.
            scope_name (str): Name of scope in the bucket to store documents in.
            collection_name (str): Name of collection in the scope to store documents in.
            text_key (Optional[str], optional): The field for the document text.
                Defaults to "text".
            embedding_key (Optional[str], optional): The field for the document embedding.
                Defaults to "embedding".
            metadata_key (Optional[str], optional): The field for the document metadata.
                Defaults to "metadata".
            query_options (Optional[QueryOptions]): Query options for SQL++ queries.
                Defaults to None.

        Returns:
            None

        """
        try:
            fromcouchbase.clusterimport Cluster
        except ImportError as e:
            raise ImportError(
                "Could not import couchbase python package. "
                "Please install couchbase SDK  with `pip install couchbase`."
            )

        if not isinstance(cluster, Cluster):
            raise ValueError(
                f"cluster should be an instance of couchbase.Cluster, "
                f"got {type(cluster)}"
            )

        super().__init__()
        self._cluster = cluster

        if not bucket_name:
            raise ValueError("bucket_name must be provided.")

        if not scope_name:
            raise ValueError("scope_name must be provided.")

        if not collection_name:
            raise ValueError("collection_name must be provided.")

        self._bucket_name = bucket_name
        self._scope_name = scope_name
        self._collection_name = collection_name
        self._text_key = text_key
        self._embedding_key = embedding_key
        self._metadata_key = metadata_key
        self._query_options = query_options
        # Check if the bucket exists
        if not self._check_bucket_exists():
            raise ValueError(
                f"Bucket {self._bucket_name} does not exist. "
                " Please create the bucket before searching."
            )

        try:
            self._bucket = self._cluster.bucket(self._bucket_name)
            self._scope = self._bucket.scope(self._scope_name)
            self._collection = self._scope.collection(self._collection_name)
        except Exception as e:
            raise ValueError(
                "Error connecting to couchbase. "
                "Please check the connection and credentials."
            ) frome

        # Check if the scope and collection exists. Throws ValueError if they don't
        try:
            self._check_scope_and_collection_exists()
        except Exception as e:
            raise

    defadd(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
"""
        Add nodes to the collection and return their document IDs.

        Args:
            nodes (List[BaseNode]): List of nodes to add.
            **kwargs (Any): Additional keyword arguments.
                batch_size (int): Size of the batch for batch insert.

        Returns:
            List[str]: List of document IDs for the added nodes.

        """
        fromcouchbase.exceptionsimport DocumentExistsException

        batch_size = kwargs.get("batch_size", self.DEFAULT_BATCH_SIZE)
        documents_to_insert = []
        doc_ids = []

        for node in nodes:
            metadata = node_to_metadata_dict(
                node,
                remove_text=True,
                text_field=self._text_key,
                flat_metadata=self.flat_metadata,
            )
            doc_id: str = node.node_id

            doc = {
                self._text_key: node.get_content(metadata_mode=MetadataMode.NONE),
                self._embedding_key: node.embedding,
                self._metadata_key: metadata,
            }

            documents_to_insert.append({doc_id: doc})

        for i in range(0, len(documents_to_insert), batch_size):
            batch = documents_to_insert[i : i + batch_size]
            try:
                # convert the list of dicts to a single dict for batch insert
                insert_batch = {}
                for doc in batch:
                    insert_batch.update(doc)

                logger.debug("Inserting batch of documents to Couchbase", insert_batch)

                # upsert the batch of documents into the collection
                result = self._collection.upsert_multi(insert_batch)

                logger.debug(f"Insert result: {result.all_ok}")
                if result.all_ok:
                    doc_ids.extend(insert_batch.keys())

            except DocumentExistsException as e:
                logger.debug(f"Document already exists: {e}")

            logger.debug("Inserted batch of documents to Couchbase")
        return doc_ids

    defdelete(self, ref_doc_id: str, **kwargs: Any) -> None:
"""
        Delete a document by its reference document ID.

        Args:
            ref_doc_id: The reference document ID to be deleted.

        Returns:
            None

        """
        try:
            document_field = f"`{self._metadata_key}`.`ref_doc_id`"
            query = f"DELETE FROM `{self._collection_name}` WHERE {document_field} = $ref_doc_id"
            query_options = (
                self._query_options.copy() if self._query_options else QueryOptions()
            )
            query_options["named_parameters"] = {"ref_doc_id": ref_doc_id}
            self._scope.query(query, query_options).execute()
            logger.debug(f"Deleted document {ref_doc_id}")
        except Exception:
            logger.error(f"Error deleting document {ref_doc_id}")
            raise

    @property
    defclient(self) -> Any:
"""
        Property function to access the client attribute.
        """
        return self._cluster

    @property
    defbucket(self) -> Any:
"""
        Property function to access the bucket attribute.
        """
        return self._bucket

    @property
    defscope(self) -> Any:
"""
        Property function to access the scope attribute.
        """
        return self._scope

    @property
    defcollection(self) -> Any:
"""
        Property function to access the collection attribute.
        """
        return self._collection

    def_check_bucket_exists(self) -> bool:
"""
        Check if the bucket exists in the linked Couchbase cluster.

        Returns:
            True if the bucket exists

        """
        bucket_manager = self._cluster.buckets()
        try:
            bucket_manager.get_bucket(self._bucket_name)
            return True
        except Exception as e:
            logger.debug("Error checking if bucket exists:", e)
            return False

    def_check_scope_and_collection_exists(self) -> bool:
"""
        Check if the scope and collection exists in the linked Couchbase bucket
        Returns:
            True if the scope and collection exist in the bucket
            Raises a ValueError if either is not found.
        """
        scope_collection_map: Dict[str, Any] = {}

        # Get a list of all scopes in the bucket
        for scope in self._bucket.collections().get_all_scopes():
            scope_collection_map[scope.name] = []

            # Get a list of all the collections in the scope
            for collection in scope.collections:
                scope_collection_map[scope.name].append(collection.name)

        # Check if the scope exists
        if self._scope_name not in scope_collection_map:
            raise ValueError(
                f"Scope {self._scope_name} not found in Couchbase "
                f"bucket {self._bucket_name}"
            )

        # Check if the collection exists in the scope
        if self._collection_name not in scope_collection_map[self._scope_name]:
            raise ValueError(
                f"Collection {self._collection_name} not found in scope "
                f"{self._scope_name} in Couchbase bucket {self._bucket_name}"
            )

        return True

    def_format_metadata(self, row_fields: Dict[str, Any]) -> Dict[str, Any]:
"""
        Helper method to format the metadata from the Couchbase Search API.

        Args:
            row_fields (Dict[str, Any]): The fields to format.

        Returns:
            Dict[str, Any]: The formatted metadata.

        """
        metadata = {}
        for key, value in row_fields.items():
            # Couchbase Search returns the metadata key with a prefix
            # `metadata.` We remove it to get the original metadata key
            if key.startswith(self._metadata_key):
                new_key = key.split(self._metadata_key + ".")[-1]
                metadata[new_key] = value
            else:
                metadata[key] = value

        return metadata

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.CouchbaseVectorStoreBase.client "Permanent link")

```
client: 

```

Property function to access the client attribute.
###  bucket `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.CouchbaseVectorStoreBase.bucket "Permanent link")

```
bucket: 

```

Property function to access the bucket attribute.
###  scope `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.CouchbaseVectorStoreBase.scope "Permanent link")

```
scope: 

```

Property function to access the scope attribute.
###  collection `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.CouchbaseVectorStoreBase.collection "Permanent link")

```
collection: 

```

Property function to access the collection attribute.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.CouchbaseVectorStoreBase.add "Permanent link")

```
add(nodes: [], **kwargs: ) -> []

```

Add nodes to the collection and return their document IDs.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes to add.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments. batch_size (int): Size of the batch for batch insert.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: List of document IDs for the added nodes.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-couchbase/llama_index/vector_stores/couchbase/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
"""
    Add nodes to the collection and return their document IDs.

    Args:
        nodes (List[BaseNode]): List of nodes to add.
        **kwargs (Any): Additional keyword arguments.
            batch_size (int): Size of the batch for batch insert.

    Returns:
        List[str]: List of document IDs for the added nodes.

    """
    fromcouchbase.exceptionsimport DocumentExistsException

    batch_size = kwargs.get("batch_size", self.DEFAULT_BATCH_SIZE)
    documents_to_insert = []
    doc_ids = []

    for node in nodes:
        metadata = node_to_metadata_dict(
            node,
            remove_text=True,
            text_field=self._text_key,
            flat_metadata=self.flat_metadata,
        )
        doc_id: str = node.node_id

        doc = {
            self._text_key: node.get_content(metadata_mode=MetadataMode.NONE),
            self._embedding_key: node.embedding,
            self._metadata_key: metadata,
        }

        documents_to_insert.append({doc_id: doc})

    for i in range(0, len(documents_to_insert), batch_size):
        batch = documents_to_insert[i : i + batch_size]
        try:
            # convert the list of dicts to a single dict for batch insert
            insert_batch = {}
            for doc in batch:
                insert_batch.update(doc)

            logger.debug("Inserting batch of documents to Couchbase", insert_batch)

            # upsert the batch of documents into the collection
            result = self._collection.upsert_multi(insert_batch)

            logger.debug(f"Insert result: {result.all_ok}")
            if result.all_ok:
                doc_ids.extend(insert_batch.keys())

        except DocumentExistsException as e:
            logger.debug(f"Document already exists: {e}")

        logger.debug("Inserted batch of documents to Couchbase")
    return doc_ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.CouchbaseVectorStoreBase.delete "Permanent link")

```
delete(ref_doc_id: , **kwargs: ) -> None

```

Delete a document by its reference document ID.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The reference document ID to be deleted.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `None`  |  None  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-couchbase/llama_index/vector_stores/couchbase/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **kwargs: Any) -> None:
"""
    Delete a document by its reference document ID.

    Args:
        ref_doc_id: The reference document ID to be deleted.

    Returns:
        None

    """
    try:
        document_field = f"`{self._metadata_key}`.`ref_doc_id`"
        query = f"DELETE FROM `{self._collection_name}` WHERE {document_field} = $ref_doc_id"
        query_options = (
            self._query_options.copy() if self._query_options else QueryOptions()
        )
        query_options["named_parameters"] = {"ref_doc_id": ref_doc_id}
        self._scope.query(query, query_options).execute()
        logger.debug(f"Deleted document {ref_doc_id}")
    except Exception:
        logger.error(f"Error deleting document {ref_doc_id}")
        raise

```
 |  
| --- | --- |  
##  QueryVectorSearchType [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.QueryVectorSearchType "Permanent link")
Bases: `str`, `Enum`
Enum for search types supported by Couchbase GSI.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-couchbase/llama_index/vector_stores/couchbase/base.py`  
| 
```
37
38
39
40
41
```
 | 
```
classQueryVectorSearchType(str, Enum):
"""Enum for search types supported by Couchbase GSI."""

    ANN = "ANN"
    KNN = "KNN"

```
 |  
| --- | --- |  
##  QueryVectorSearchSimilarity [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/couchbase/#llama_index.vector_stores.couchbase.QueryVectorSearchSimilarity "Permanent link")
Bases: `str`, `Enum`
Enum for similarity metrics supported by Couchbase GSI.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-couchbase/llama_index/vector_stores/couchbase/base.py`  
| 
```
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
classQueryVectorSearchSimilarity(str, Enum):
"""Enum for similarity metrics supported by Couchbase GSI."""

    COSINE = "COSINE"
    DOT = "DOT"
    L2 = "L2"
    EUCLIDEAN = "EUCLIDEAN"
    L2_SQUARED = "L2_SQUARED"
    EUCLIDEAN_SQUARED = "EUCLIDEAN_SQUARED"

```
 |  
| --- | --- |  
options: members: - CouchbaseVectorStore - CouchbaseSearchVectorStore
