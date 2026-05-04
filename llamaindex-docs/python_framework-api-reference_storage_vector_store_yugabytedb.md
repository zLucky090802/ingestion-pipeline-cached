# Yugabytedb
##  YBVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/yugabytedb/#llama_index.vector_stores.yugabytedb.YBVectorStore "Permanent link")
Bases: 
Yugabytedb Vector Store.
Examples:
`pip install llama-index-vector-stores-yugabytedb`

```
fromllama_index.vector_stores.yugabytedbimport YBVectorStore

# Create YBVectorStore instance
vector_store = YBVectorStore.from_params(
    database="vector_db",
    host="localhost",
    password="password",
    port=5432,
    user="yugabytedb",
    table_name="paul_graham_essay",
    embed_dim=1536  # openai embedding dimension
    use_halfvec=True  # Enable half precision
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-yugabytedb/llama_index/vector_stores/yugabytedb/base.py`  
| 
```
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
 936
 937
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
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
```
 | 
```
classYBVectorStore(BasePydanticVectorStore):
"""
    Yugabytedb Vector Store.

    Examples:
        `pip install llama-index-vector-stores-yugabytedb`

        ```python
        from llama_index.vector_stores.yugabytedb import YBVectorStore

        # Create YBVectorStore instance
        vector_store = YBVectorStore.from_params(
            database="vector_db",
            host="localhost",
            password="password",
            port=5432,
            user="yugabytedb",
            table_name="paul_graham_essay",
            embed_dim=1536  # openai embedding dimension
            use_halfvec=True  # Enable half precision

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    connection_string: str
    table_name: str
    schema_name: str
    embed_dim: int
    hybrid_search: bool
    text_search_config: str
    cache_ok: bool
    perform_setup: bool
    debug: bool
    use_jsonb: bool
    create_engine_kwargs: Dict
    initialization_fail_on_error: bool = False
    indexed_metadata_keys: Optional[Set[Tuple[str, PGType]]] = None

    hnsw_kwargs: Optional[Dict[str, Any]]

    use_halfvec: bool = False

    _base: Any = PrivateAttr()
    _table_class: Any = PrivateAttr()
    _engine: Optional[sqlalchemy.engine.Engine] = PrivateAttr(default=None)
    _session: sqlalchemy.orm.Session = PrivateAttr()
    _is_initialized: bool = PrivateAttr(default=False)

    def__init__(
        self,
        connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
        table_name: Optional[str] = None,
        schema_name: Optional[str] = None,
        hybrid_search: bool = False,
        text_search_config: str = "english",
        embed_dim: int = 1536,
        cache_ok: bool = False,
        perform_setup: bool = True,
        debug: bool = False,
        use_jsonb: bool = False,
        hnsw_kwargs: Optional[Dict[str, Any]] = None,
        create_engine_kwargs: Optional[Dict[str, Any]] = None,
        initialization_fail_on_error: bool = False,
        use_halfvec: bool = False,
        engine: Optional[sqlalchemy.engine.Engine] = None,
        indexed_metadata_keys: Optional[Set[Tuple[str, PGType]]] = None,
    ) -> None:
"""
        Constructor.

        Args:
            connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to yugabytedb db.
            table_name (str): Table name.
            schema_name (str): Schema name.
            hybrid_search (bool, optional): Enable hybrid search. Defaults to False.
            text_search_config (str, optional): Text search configuration. Defaults to "english".
            embed_dim (int, optional): Embedding dimensions. Defaults to 1536.
            cache_ok (bool, optional): Enable cache. Defaults to False.
            perform_setup (bool, optional): If db should be set up. Defaults to True.
            debug (bool, optional): Debug mode. Defaults to False.
            use_jsonb (bool, optional): Use JSONB instead of JSON. Defaults to False.
            hnsw_kwargs (Optional[Dict[str, Any]], optional): HNSW kwargs, a dict that
                contains "hnsw_ef_construction", "hnsw_ef_search", "hnsw_m", and optionally "hnsw_dist_method". Defaults to None,
                which turns off HNSW search.
            create_engine_kwargs (Optional[Dict[str, Any]], optional): Engine parameters to pass to create_engine. Defaults to None.
            use_halfvec (bool, optional): If `True`, use half-precision vectors. Defaults to False.
            engine (Optional[sqlalchemy.engine.Engine], optional): SQLAlchemy engine instance to use. Defaults to None.
            indexed_metadata_keys (Optional[List[Tuple[str, str]]], optional): Set of metadata keys with their type to index. Defaults to None.

        """
        table_name = table_name.lower() if table_name else "llamaindex"
        schema_name = schema_name.lower() if schema_name else "public"

        if hybrid_search and text_search_config is None:
            raise ValueError(
                "Sparse vector index creation requires "
                "a text search configuration specification."
            )

        fromsqlalchemy.ormimport declarative_base

        super().__init__(
            connection_string=str(connection_string),
            table_name=table_name,
            schema_name=schema_name,
            hybrid_search=hybrid_search,
            text_search_config=text_search_config,
            embed_dim=embed_dim,
            cache_ok=cache_ok,
            perform_setup=perform_setup,
            debug=debug,
            use_jsonb=use_jsonb,
            hnsw_kwargs=hnsw_kwargs,
            create_engine_kwargs=create_engine_kwargs or {},
            initialization_fail_on_error=initialization_fail_on_error,
            use_halfvec=use_halfvec,
            indexed_metadata_keys=indexed_metadata_keys,
        )

        # sqlalchemy model
        self._base = declarative_base()
        self._table_class = get_data_model(
            self._base,
            table_name,
            schema_name,
            hybrid_search,
            text_search_config,
            cache_ok,
            embed_dim=embed_dim,
            use_jsonb=use_jsonb,
            use_halfvec=use_halfvec,
            indexed_metadata_keys=indexed_metadata_keys,
        )

        if engine is not None:
            self._engine = engine

    async defclose(self) -> None:
        if not self._is_initialized:
            return

        if self._engine:
            self._engine.dispose()

    @classmethod
    defclass_name(cls) -> str:
        return "YBVectorStore"

    @classmethod
    deffrom_params(
        cls,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        load_balance: Optional[bool] = False,
        topology: Optional[str] = None,
        yb_servers_refresh_interval: Optional[int] = 300,
        fallback_to_topology_keys_only: Optional[bool] = False,
        failed_host_ttl_seconds: Optional[int] = 5,
        table_name: str = "llamaindex",
        schema_name: str = "public",
        connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
        hybrid_search: bool = False,
        text_search_config: str = "english",
        embed_dim: int = 1536,
        cache_ok: bool = False,
        perform_setup: bool = True,
        debug: bool = False,
        use_jsonb: bool = False,
        hnsw_kwargs: Optional[Dict[str, Any]] = None,
        create_engine_kwargs: Optional[Dict[str, Any]] = None,
        use_halfvec: bool = False,
        indexed_metadata_keys: Optional[Set[Tuple[str, PGType]]] = None,
    ) -> "YBVectorStore":
"""
        Construct from params.

        Args:
            load_balance:
            host (Optional[str], optional): Host of yugabytedb connection. Defaults to None.
            port (Optional[str], optional): Port of yugabytedb connection. Defaults to None.
            database (Optional[str], optional): Postgres DB name. Defaults to None.
            user (Optional[str], optional): Postgres username. Defaults to None.
            password (Optional[str], optional): Postgres password. Defaults to None.
            table_name (str): Table name. Defaults to "llamaindex".
            schema_name (str): Schema name. Defaults to "public".
            connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to yugabytedb db
            hybrid_search (bool, optional): Enable hybrid search. Defaults to False.
            text_search_config (str, optional): Text search configuration. Defaults to "english".
            embed_dim (int, optional): Embedding dimensions. Defaults to 1536.
            cache_ok (bool, optional): Enable cache. Defaults to False.
            perform_setup (bool, optional): If db should be set up. Defaults to True.
            debug (bool, optional): Debug mode. Defaults to False.
            use_jsonb (bool, optional): Use JSONB instead of JSON. Defaults to False.
            hnsw_kwargs (Optional[Dict[str, Any]], optional): HNSW kwargs, a dict that
                contains "hnsw_ef_construction", "hnsw_ef_search", "hnsw_m", and optionally "hnsw_dist_method". Defaults to None,
                which turns off HNSW search.
            create_engine_kwargs (Optional[Dict[str, Any]], optional): Engine parameters to pass to create_engine. Defaults to None.
            use_halfvec (bool, optional): If `True`, use half-precision vectors. Defaults to False.
            indexed_metadata_keys (Optional[Set[Tuple[str, str]]], optional): Set of metadata keys to index. Defaults to None.

        Returns:
            YBVectorStore: Instance of YBVectorStore constructed from params.

        """
        fromurllib.parseimport urlencode

        query_params = {"load_balance": str(load_balance)}

        if topology is not None:
            query_params["topology_keys"] = topology
        if yb_servers_refresh_interval is not None:
            query_params["yb_servers_refresh_interval"] = yb_servers_refresh_interval
        if fallback_to_topology_keys_only:
            query_params["fallback_to_topology_keys_only"] = (
                fallback_to_topology_keys_only
            )
        if failed_host_ttl_seconds is not None:
            query_params["failed_host_ttl_seconds"] = failed_host_ttl_seconds

        query_str = urlencode(query_params)

        conn_str = (
            connection_string
            or f"yugabytedb+psycopg2://{user}:{password}@{host}:{port}/{database}?{query_str}"
        )
        return cls(
            connection_string=conn_str,
            table_name=table_name,
            schema_name=schema_name,
            hybrid_search=hybrid_search,
            text_search_config=text_search_config,
            embed_dim=embed_dim,
            cache_ok=cache_ok,
            perform_setup=perform_setup,
            debug=debug,
            use_jsonb=use_jsonb,
            hnsw_kwargs=hnsw_kwargs,
            create_engine_kwargs=create_engine_kwargs,
            use_halfvec=use_halfvec,
            indexed_metadata_keys=indexed_metadata_keys,
        )

    @property
    defclient(self) -> Any:
        if not self._is_initialized:
            return None
        return self._engine

    def_connect(self) -> Any:
        fromsqlalchemyimport create_engine
        fromsqlalchemy.ormimport sessionmaker

        self._engine = self._engine or create_engine(
            self.connection_string, echo=self.debug, **self.create_engine_kwargs
        )
        self._session = sessionmaker(self._engine)

    def_create_schema_if_not_exists(self) -> bool:
"""
        Create the schema if it does not exist.
        Returns True if the schema was created, False if it already existed.
        """
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", self.schema_name):
            raise ValueError(f"Invalid schema_name: {self.schema_name}")
        with self._session() as session, session.begin():
            # Check if the specified schema exists with "CREATE" statement
            check_schema_statement = sqlalchemy.text(
                f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema_name"
            ).bindparams(schema_name=self.schema_name)
            result = session.execute(check_schema_statement).fetchone()

            # If the schema does not exist, then create it
            schema_doesnt_exist = result is None
            if schema_doesnt_exist:
                create_schema_statement = sqlalchemy.text(
                    # DDL won't tolerate quoted string literal here for schema_name,
                    # so use a format string to embed the schema_name directly, instead of a param.
                    f"CREATE SCHEMA IF NOT EXISTS {self.schema_name}"
                )
                session.execute(create_schema_statement)

            session.commit()
            return schema_doesnt_exist

    def_create_tables_if_not_exists(self) -> None:
        with self._session() as session, session.begin():
            self._base.metadata.create_all(session.connection())

    def_create_extension(self) -> None:
        importsqlalchemy

        with self._session() as session, session.begin():
            statement = sqlalchemy.text("CREATE EXTENSION IF NOT EXISTS vector")
            session.execute(statement)
            session.commit()

    def_create_hnsw_index(self) -> None:
        importsqlalchemy

        if (
            "hnsw_ef_construction" not in self.hnsw_kwargs
            or "hnsw_m" not in self.hnsw_kwargs
        ):
            raise ValueError(
                "Make sure hnsw_ef_search, hnsw_ef_construction, and hnsw_m are in hnsw_kwargs."
            )

        hnsw_ef_construction = self.hnsw_kwargs.pop("hnsw_ef_construction")
        hnsw_m = self.hnsw_kwargs.pop("hnsw_m")

        # If user didn’t specify an operator, pick a default based on whether halfvec is used
        if "hnsw_dist_method" in self.hnsw_kwargs:
            hnsw_dist_method = self.hnsw_kwargs.pop("hnsw_dist_method")
        else:
            if self.use_halfvec:
                hnsw_dist_method = "halfvec_l2_ops"
            else:
                # Default to vector_cosine_ops
                hnsw_dist_method = "vector_cosine_ops"

        index_name = f"{self._table_class.__tablename__}_embedding_idx"

        with self._session() as session, session.begin():
            statement = sqlalchemy.text(
                f"CREATE INDEX IF NOT EXISTS {index_name} "
                f"ON {self.schema_name}.{self._table_class.__tablename__} "
                f"USING ybhnsw (embedding {hnsw_dist_method}) "
                f"WITH (m = {hnsw_m}, ef_construction = {hnsw_ef_construction})"
            )
            session.execute(statement)
            session.commit()

    def_initialize(self) -> None:
        fail_on_error = self.initialization_fail_on_error
        if not self._is_initialized:
            self._connect()
            if self.perform_setup:
                try:
                    self._create_schema_if_not_exists()
                except Exception as e:
                    _logger.warning(f"PG Setup: Error creating schema: {e}")
                    if fail_on_error:
                        raise
                try:
                    self._create_extension()
                except Exception as e:
                    _logger.warning(f"PG Setup: Error creating extension: {e}")
                    if fail_on_error:
                        raise
                try:
                    self._create_tables_if_not_exists()
                except Exception as e:
                    _logger.warning(f"PG Setup: Error creating tables: {e}")
                    if fail_on_error:
                        raise
                if self.hnsw_kwargs is not None:
                    try:
                        self._create_hnsw_index()
                    except Exception as e:
                        _logger.warning(f"PG Setup: Error creating HNSW index: {e}")
                        if fail_on_error:
                            raise
            self._is_initialized = True

    def_node_to_table_row(self, node: BaseNode) -> Any:
        return self._table_class(
            node_id=node.node_id,
            embedding=node.get_embedding(),
            text=node.get_content(metadata_mode=MetadataMode.NONE),
            metadata_=node_to_metadata_dict(
                node,
                remove_text=True,
                flat_metadata=self.flat_metadata,
            ),
        )

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
        self._initialize()
        ids = []
        with self._session() as session, session.begin():
            for node in nodes:
                ids.append(node.node_id)
                item = self._node_to_table_row(node)
                session.add(item)
            session.commit()
        return ids

    def_to_postgres_operator(self, operator: FilterOperator) -> str:
        if operator == FilterOperator.EQ:
            return "="
        elif operator == FilterOperator.GT:
            return ">"
        elif operator == FilterOperator.LT:
            return "<"
        elif operator == FilterOperator.NE:
            return "!="
        elif operator == FilterOperator.GTE:
            return ">="
        elif operator == FilterOperator.LTE:
            return "<="
        elif operator == FilterOperator.IN:
            return "IN"
        elif operator == FilterOperator.NIN:
            return "NOT IN"
        elif operator == FilterOperator.CONTAINS:
            return "@>"
        elif operator == FilterOperator.TEXT_MATCH:
            return "LIKE"
        elif operator == FilterOperator.TEXT_MATCH_INSENSITIVE:
            return "ILIKE"
        elif operator == FilterOperator.IS_EMPTY:
            return "IS NULL"
        else:
            _logger.warning(f"Unknown operator: {operator}, fallback to '='")
            return "="

    def_build_filter_clause(self, filter_: MetadataFilter) -> Any:
        fromsqlalchemyimport text

        if filter_.operator in [FilterOperator.IN, FilterOperator.NIN]:
            # Expects a single value in the metadata, and a list to compare

            # In Python, to create a tuple with a single element, you need to include a comma after the element
            # This code will correctly format the IN clause whether there is one element or multiple elements in the list:
            filter_value = ", ".join(f"'{e}'" for e in filter_.value)

            return text(
                f"metadata_->>'{filter_.key}' "
                f"{self._to_postgres_operator(filter_.operator)} "
                f"({filter_value})"
            )
        elif filter_.operator == FilterOperator.CONTAINS:
            # Expects a list stored in the metadata, and a single value to compare
            return text(
                f"metadata_::jsonb->'{filter_.key}' "
                f"{self._to_postgres_operator(filter_.operator)} "
                f"'[\"{filter_.value}\"]'"
            )
        elif (
            filter_.operator == FilterOperator.TEXT_MATCH
            or filter_.operator == FilterOperator.TEXT_MATCH_INSENSITIVE
        ):
            # Where the operator is text_match or ilike, we need to wrap the filter in '%' characters
            return text(
                f"metadata_->>'{filter_.key}' "
                f"{self._to_postgres_operator(filter_.operator)} "
                f"'%{filter_.value}%'"
            )
        elif filter_.operator == FilterOperator.IS_EMPTY:
            # Where the operator is is_empty, we need to check if the metadata is null
            return text(
                f"metadata_->>'{filter_.key}' "
                f"{self._to_postgres_operator(filter_.operator)}"
            )
        else:
            # Check if value is a number. If so, cast the metadata value to a float
            # This is necessary because the metadata is stored as a string
            try:
                return text(
                    f"(metadata_->>'{filter_.key}')::float "
                    f"{self._to_postgres_operator(filter_.operator)} "
                    f"{float(filter_.value)}"
                )
            except ValueError:
                # If not a number, then treat it as a string
                return text(
                    f"metadata_->>'{filter_.key}' "
                    f"{self._to_postgres_operator(filter_.operator)} "
                    f"'{filter_.value}'"
                )

    def_recursively_apply_filters(self, filters: List[MetadataFilters]) -> Any:
"""
        Returns a sqlalchemy where clause.
        """
        importsqlalchemy

        sqlalchemy_conditions = {
            "or": sqlalchemy.sql.or_,
            "and": sqlalchemy.sql.and_,
        }

        if filters.condition not in sqlalchemy_conditions:
            raise ValueError(
                f"Invalid condition: {filters.condition}. "
                f"Must be one of {list(sqlalchemy_conditions.keys())}"
            )

        return sqlalchemy_conditions[filters.condition](
            *(
                (
                    self._build_filter_clause(filter_)
                    if not isinstance(filter_, MetadataFilters)
                    else self._recursively_apply_filters(filter_)
                )
                for filter_ in filters.filters
            )
        )

    def_apply_filters_and_limit(
        self,
        stmt: "Select",
        limit: int,
        metadata_filters: Optional[MetadataFilters] = None,
    ) -> Any:
        if metadata_filters:
            stmt = stmt.where(  # type: ignore
                self._recursively_apply_filters(metadata_filters)
            )
        return stmt.limit(limit)  # type: ignore

    def_build_query(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
    ) -> Any:
        fromsqlalchemyimport select, text

        stmt = select(  # type: ignore
            self._table_class.id,
            self._table_class.node_id,
            self._table_class.text,
            self._table_class.metadata_,
            self._table_class.embedding.cosine_distance(embedding).label("distance"),
        ).order_by(text("distance asc"))

        return self._apply_filters_and_limit(stmt, limit, metadata_filters)

    def_query_with_score(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> List[DBEmbeddingRow]:
        stmt = self._build_query(embedding, limit, metadata_filters)
        with self._session() as session, session.begin():
            res = session.execute(
                stmt,
            )
            return [
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=item.metadata_,
                    similarity=(1 - item.distance) if item.distance is not None else 0,
                )
                for item in res.all()
            ]

    def_build_sparse_query(
        self,
        query_str: Optional[str],
        limit: int,
        metadata_filters: Optional[MetadataFilters] = None,
    ) -> Any:
        fromsqlalchemyimport select, type_coerce
        fromsqlalchemy.sqlimport func, text
        fromsqlalchemy.typesimport UserDefinedType

        classREGCONFIG(UserDefinedType):
            # The TypeDecorator.cache_ok class-level flag indicates if this custom TypeDecorator is safe to be used as part of a cache key.
            # If the TypeDecorator is not guaranteed to produce the same bind/result behavior and SQL generation every time,
            # this flag should be set to False; otherwise if the class produces the same behavior each time, it may be set to True.
            cache_ok = True

            defget_col_spec(self, **kw: Any) -> str:
                return "regconfig"

        if query_str is None:
            raise ValueError("query_str must be specified for a sparse vector query.")

        # Replace '&' with '|' to perform an OR search for higher recall
        config_type_coerce = type_coerce(self.text_search_config, REGCONFIG)
        ts_query = func.to_tsquery(
            config_type_coerce,
            func.replace(
                func.text(func.plainto_tsquery(config_type_coerce, query_str)),
                "&",
                "|",
            ),
        )
        stmt = (
            select(  # type: ignore
                self._table_class.id,
                self._table_class.node_id,
                self._table_class.text,
                self._table_class.metadata_,
                func.ts_rank(self._table_class.text_search_tsv, ts_query).label("rank"),
            )
            .where(self._table_class.text_search_tsv.op("@@")(ts_query))
            .order_by(text("rank desc"))
        )

        # type: ignore
        return self._apply_filters_and_limit(stmt, limit, metadata_filters)

    def_sparse_query_with_rank(
        self,
        query_str: Optional[str] = None,
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
    ) -> List[DBEmbeddingRow]:
        stmt = self._build_sparse_query(query_str, limit, metadata_filters)
        with self._session() as session, session.begin():
            res = session.execute(stmt)
            return [
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=item.metadata_,
                    similarity=item.rank,
                )
                for item in res.all()
            ]

    def_hybrid_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> List[DBEmbeddingRow]:
        if query.alpha is not None:
            _logger.warning(
                "yugabytedb hybrid search does not support alpha parameter."
            )

        sparse_top_k = query.sparse_top_k or query.similarity_top_k

        dense_results = self._query_with_score(
            query.query_embedding,
            query.similarity_top_k,
            query.filters,
            **kwargs,
        )

        sparse_results = self._sparse_query_with_rank(
            query.query_str, sparse_top_k, query.filters
        )

        all_results = dense_results + sparse_results
        return _dedup_results(all_results)

    def_db_rows_to_query_result(
        self, rows: List[DBEmbeddingRow]
    ) -> VectorStoreQueryResult:
        nodes = []
        similarities = []
        ids = []
        for db_embedding_row in rows:
            try:
                node = metadata_dict_to_node(db_embedding_row.metadata)
                node.set_content(str(db_embedding_row.text))
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                node = TextNode(
                    id_=db_embedding_row.node_id,
                    text=db_embedding_row.text,
                    metadata=db_embedding_row.metadata,
                )
            similarities.append(db_embedding_row.similarity)
            ids.append(db_embedding_row.node_id)
            nodes.append(node)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities,
            ids=ids,
        )

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        self._initialize()
        if query.mode == VectorStoreQueryMode.HYBRID:
            results = self._hybrid_query(query, **kwargs)
        elif query.mode in [
            VectorStoreQueryMode.SPARSE,
            VectorStoreQueryMode.TEXT_SEARCH,
        ]:
            sparse_top_k = query.sparse_top_k or query.similarity_top_k
            results = self._sparse_query_with_rank(
                query.query_str, sparse_top_k, query.filters
            )
        elif query.mode == VectorStoreQueryMode.DEFAULT:
            results = self._query_with_score(
                query.query_embedding,
                query.similarity_top_k,
                query.filters,
                **kwargs,
            )
        else:
            raise ValueError(f"Invalid query mode: {query.mode}")

        return self._db_rows_to_query_result(results)

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        fromsqlalchemyimport delete

        self._initialize()
        with self._session() as session, session.begin():
            stmt = delete(self._table_class).where(
                self._table_class.metadata_["doc_id"].astext == ref_doc_id
            )

            session.execute(stmt)
            session.commit()

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Deletes nodes.

        Args:
            node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
            filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

        """
        if not node_ids and not filters:
            return

        fromsqlalchemyimport delete

        self._initialize()
        with self._session() as session, session.begin():
            stmt = delete(self._table_class)

            if node_ids:
                stmt = stmt.where(self._table_class.node_id.in_(node_ids))

            if filters:
                stmt = stmt.where(self._recursively_apply_filters(filters))

            session.execute(stmt)
            session.commit()

    defclear(self) -> None:
"""Clears table."""
        fromsqlalchemyimport delete

        self._initialize()
        with self._session() as session, session.begin():
            stmt = delete(self._table_class)

            session.execute(stmt)
            session.commit()

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""Get nodes from vector store."""
        assert node_ids is not None or filters is not None, (
            "Either node_ids or filters must be provided"
        )

        self._initialize()
        fromsqlalchemyimport select

        stmt = select(
            self._table_class.node_id,
            self._table_class.text,
            self._table_class.metadata_,
            self._table_class.embedding,
        )

        if node_ids:
            stmt = stmt.where(self._table_class.node_id.in_(node_ids))

        if filters:
            filter_clause = self._recursively_apply_filters(filters)
            stmt = stmt.where(filter_clause)

        nodes: List[BaseNode] = []

        with self._session() as session, session.begin():
            res = session.execute(stmt).fetchall()
            for item in res:
                node_id = item.node_id
                text = item.text
                metadata = item.metadata_
                embedding = item.embedding

                try:
                    node = metadata_dict_to_node(metadata)
                    node.set_content(str(text))
                    node.embedding = embedding
                except Exception:
                    node = TextNode(
                        id_=node_id,
                        text=text,
                        metadata=metadata,
                        embedding=embedding,
                    )
                nodes.append(node)

        return nodes

```
 |  
| --- | --- |  
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/yugabytedb/#llama_index.vector_stores.yugabytedb.YBVectorStore.from_params "Permanent link")

```
from_params(
    host: Optional[] = None,
    port: Optional[] = None,
    database: Optional[] = None,
    user: Optional[] = None,
    password: Optional[] = None,
    load_balance: Optional[] = False,
    topology: Optional[] = None,
    yb_servers_refresh_interval: Optional[] = 300,
    fallback_to_topology_keys_only: Optional[] = False,
    failed_host_ttl_seconds: Optional[] = 5,
    table_name:  = "llamaindex",
    schema_name:  = "public",
    connection_string: Optional[Union[, ]] = None,
    hybrid_search:  = False,
    text_search_config:  = "english",
    embed_dim:  = 1536,
    cache_ok:  = False,
    perform_setup:  = True,
    debug:  = False,
    use_jsonb:  = False,
    hnsw_kwargs: Optional[[, ]] = None,
    create_engine_kwargs: Optional[[, ]] = None,
    use_halfvec:  = False,
    indexed_metadata_keys: Optional[
        [Tuple[, PGType]]
    ] = None,
) -> 

```

Construct from params.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `load_balance`  |  `Optional[bool]`  |  `False`  |  
|  `host`  |  `Optional[str]`  |  Host of yugabytedb connection. Defaults to None.  |  `None`  |  
|  `port`  |  `Optional[str]`  |  Port of yugabytedb connection. Defaults to None.  |  `None`  |  
|  `database`  |  `Optional[str]`  |  Postgres DB name. Defaults to None.  |  `None`  |  
|  `user`  |  `Optional[str]`  |  Postgres username. Defaults to None.  |  `None`  |  
|  `password`  |  `Optional[str]`  |  Postgres password. Defaults to None.  |  `None`  |  
|  `table_name`  |  Table name. Defaults to "llamaindex".  |  `'llamaindex'`  |  
|  `schema_name`  |  Schema name. Defaults to "public".  |  `'public'`  |  
|  `connection_string`  |  `Union[str, URL]`  |  Connection string to yugabytedb db  |  `None`  |  
|  `hybrid_search`  |  `bool`  |  Enable hybrid search. Defaults to False.  |  `False`  |  
|  `text_search_config`  |  Text search configuration. Defaults to "english".  |  `'english'`  |  
|  `embed_dim`  |  Embedding dimensions. Defaults to 1536.  |  `1536`  |  
|  `cache_ok`  |  `bool`  |  Enable cache. Defaults to False.  |  `False`  |  
|  `perform_setup`  |  `bool`  |  If db should be set up. Defaults to True.  |  `True`  |  
|  `debug`  |  `bool`  |  Debug mode. Defaults to False.  |  `False`  |  
|  `use_jsonb`  |  `bool`  |  Use JSONB instead of JSON. Defaults to False.  |  `False`  |  
|  `hnsw_kwargs`  |  `Optional[Dict[str, Any]]`  |  HNSW kwargs, a dict that contains "hnsw_ef_construction", "hnsw_ef_search", "hnsw_m", and optionally "hnsw_dist_method". Defaults to None, which turns off HNSW search.  |  `None`  |  
|  `create_engine_kwargs`  |  `Optional[Dict[str, Any]]`  |  Engine parameters to pass to create_engine. Defaults to None.  |  `None`  |  
|  `use_halfvec`  |  `bool`  |  If `True`, use half-precision vectors. Defaults to False.  |  `False`  |  
|  `indexed_metadata_keys`  |  `Optional[Set[Tuple[str, str]]]`  |  Set of metadata keys to index. Defaults to None.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `YBVectorStore`  |   |  Instance of YBVectorStore constructed from params.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-yugabytedb/llama_index/vector_stores/yugabytedb/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_params(
    cls,
    host: Optional[str] = None,
    port: Optional[str] = None,
    database: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    load_balance: Optional[bool] = False,
    topology: Optional[str] = None,
    yb_servers_refresh_interval: Optional[int] = 300,
    fallback_to_topology_keys_only: Optional[bool] = False,
    failed_host_ttl_seconds: Optional[int] = 5,
    table_name: str = "llamaindex",
    schema_name: str = "public",
    connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
    hybrid_search: bool = False,
    text_search_config: str = "english",
    embed_dim: int = 1536,
    cache_ok: bool = False,
    perform_setup: bool = True,
    debug: bool = False,
    use_jsonb: bool = False,
    hnsw_kwargs: Optional[Dict[str, Any]] = None,
    create_engine_kwargs: Optional[Dict[str, Any]] = None,
    use_halfvec: bool = False,
    indexed_metadata_keys: Optional[Set[Tuple[str, PGType]]] = None,
) -> "YBVectorStore":
"""
    Construct from params.

    Args:
        load_balance:
        host (Optional[str], optional): Host of yugabytedb connection. Defaults to None.
        port (Optional[str], optional): Port of yugabytedb connection. Defaults to None.
        database (Optional[str], optional): Postgres DB name. Defaults to None.
        user (Optional[str], optional): Postgres username. Defaults to None.
        password (Optional[str], optional): Postgres password. Defaults to None.
        table_name (str): Table name. Defaults to "llamaindex".
        schema_name (str): Schema name. Defaults to "public".
        connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to yugabytedb db
        hybrid_search (bool, optional): Enable hybrid search. Defaults to False.
        text_search_config (str, optional): Text search configuration. Defaults to "english".
        embed_dim (int, optional): Embedding dimensions. Defaults to 1536.
        cache_ok (bool, optional): Enable cache. Defaults to False.
        perform_setup (bool, optional): If db should be set up. Defaults to True.
        debug (bool, optional): Debug mode. Defaults to False.
        use_jsonb (bool, optional): Use JSONB instead of JSON. Defaults to False.
        hnsw_kwargs (Optional[Dict[str, Any]], optional): HNSW kwargs, a dict that
            contains "hnsw_ef_construction", "hnsw_ef_search", "hnsw_m", and optionally "hnsw_dist_method". Defaults to None,
            which turns off HNSW search.
        create_engine_kwargs (Optional[Dict[str, Any]], optional): Engine parameters to pass to create_engine. Defaults to None.
        use_halfvec (bool, optional): If `True`, use half-precision vectors. Defaults to False.
        indexed_metadata_keys (Optional[Set[Tuple[str, str]]], optional): Set of metadata keys to index. Defaults to None.

    Returns:
        YBVectorStore: Instance of YBVectorStore constructed from params.

    """
    fromurllib.parseimport urlencode

    query_params = {"load_balance": str(load_balance)}

    if topology is not None:
        query_params["topology_keys"] = topology
    if yb_servers_refresh_interval is not None:
        query_params["yb_servers_refresh_interval"] = yb_servers_refresh_interval
    if fallback_to_topology_keys_only:
        query_params["fallback_to_topology_keys_only"] = (
            fallback_to_topology_keys_only
        )
    if failed_host_ttl_seconds is not None:
        query_params["failed_host_ttl_seconds"] = failed_host_ttl_seconds

    query_str = urlencode(query_params)

    conn_str = (
        connection_string
        or f"yugabytedb+psycopg2://{user}:{password}@{host}:{port}/{database}?{query_str}"
    )
    return cls(
        connection_string=conn_str,
        table_name=table_name,
        schema_name=schema_name,
        hybrid_search=hybrid_search,
        text_search_config=text_search_config,
        embed_dim=embed_dim,
        cache_ok=cache_ok,
        perform_setup=perform_setup,
        debug=debug,
        use_jsonb=use_jsonb,
        hnsw_kwargs=hnsw_kwargs,
        create_engine_kwargs=create_engine_kwargs,
        use_halfvec=use_halfvec,
        indexed_metadata_keys=indexed_metadata_keys,
    )

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/yugabytedb/#llama_index.vector_stores.yugabytedb.YBVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Deletes nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  IDs of nodes to delete. Defaults to None.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters. Defaults to None.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-yugabytedb/llama_index/vector_stores/yugabytedb/base.py`  
| 
```
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
936
937
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
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Deletes nodes.

    Args:
        node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
        filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

    """
    if not node_ids and not filters:
        return

    fromsqlalchemyimport delete

    self._initialize()
    with self._session() as session, session.begin():
        stmt = delete(self._table_class)

        if node_ids:
            stmt = stmt.where(self._table_class.node_id.in_(node_ids))

        if filters:
            stmt = stmt.where(self._recursively_apply_filters(filters))

        session.execute(stmt)
        session.commit()

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/yugabytedb/#llama_index.vector_stores.yugabytedb.YBVectorStore.clear "Permanent link")

```
clear() -> None

```

Clears table.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-yugabytedb/llama_index/vector_stores/yugabytedb/base.py`  
| 
```
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
```
 | 
```
defclear(self) -> None:
"""Clears table."""
    fromsqlalchemyimport delete

    self._initialize()
    with self._session() as session, session.begin():
        stmt = delete(self._table_class)

        session.execute(stmt)
        session.commit()

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/yugabytedb/#llama_index.vector_stores.yugabytedb.YBVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes from vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-yugabytedb/llama_index/vector_stores/yugabytedb/base.py`  
| 
```
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
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""Get nodes from vector store."""
    assert node_ids is not None or filters is not None, (
        "Either node_ids or filters must be provided"
    )

    self._initialize()
    fromsqlalchemyimport select

    stmt = select(
        self._table_class.node_id,
        self._table_class.text,
        self._table_class.metadata_,
        self._table_class.embedding,
    )

    if node_ids:
        stmt = stmt.where(self._table_class.node_id.in_(node_ids))

    if filters:
        filter_clause = self._recursively_apply_filters(filters)
        stmt = stmt.where(filter_clause)

    nodes: List[BaseNode] = []

    with self._session() as session, session.begin():
        res = session.execute(stmt).fetchall()
        for item in res:
            node_id = item.node_id
            text = item.text
            metadata = item.metadata_
            embedding = item.embedding

            try:
                node = metadata_dict_to_node(metadata)
                node.set_content(str(text))
                node.embedding = embedding
            except Exception:
                node = TextNode(
                    id_=node_id,
                    text=text,
                    metadata=metadata,
                    embedding=embedding,
                )
            nodes.append(node)

    return nodes

```
 |  
| --- | --- |  
options: members: - YBVectorStore
