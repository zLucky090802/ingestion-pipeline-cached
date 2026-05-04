# Volcengine mysql
##  VolcengineMySQLVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore "Permanent link")
Bases: 
Volcengine RDS MySQL Vector Store.
LlamaIndex vector store implementation backed by Volcengine RDS MySQL with native vector index support (`VECTOR(N)` + HNSW ANN).
Capabilities ~~~~~~~~~~~~ - Vector column: `VECTOR(embed_dim)`. - Vector index: `VECTOR INDEX (embedding) USING HNSW` or a vector index with `SECONDARY_ENGINE_ATTRIBUTE` specifying algorithm, `M`, and distance metric, for example::

```
SECONDARY_ENGINE_ATTRIBUTE='{"algorithm": "hnsw", "M": "16", "distance": "l2"}'

```

  * Distance functions:
  * `L2_DISTANCE(embedding, TO_VECTOR('[...]'))`
  * `COSINE_DISTANCE(embedding, TO_VECTOR('[...]'))`
  * Server parameters (depending on configuration):
  * `loose_vector_index_enabled`
  * `loose_hnsw_ef_search` and other HNSW-related options.


Differences from :class:`MariaDBVectorStore` ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ - Uses MySQL `VECTOR` columns and `TO_VECTOR`/`L2_DISTANCE` functions instead of MariaDB's `VECTOR(...)` together with `VEC_FromText`/`VEC_DISTANCE_COSINE`. - Uses `JSON_EXTRACT` / `JSON_UNQUOTE` to filter on the metadata JSON column. - Optionally uses `loose_hnsw_ef_search` to control ANN search breadth.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
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
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
```
 | 
```
classVolcengineMySQLVectorStore(BasePydanticVectorStore):
"""
    Volcengine RDS MySQL Vector Store.

    LlamaIndex vector store implementation backed by Volcengine RDS
    MySQL with native vector index support (``VECTOR(N)`` + HNSW ANN).

    Capabilities
    ~~~~~~~~~~~~
    - Vector column: ``VECTOR(embed_dim)``.
    - Vector index: ``VECTOR INDEX (embedding) USING HNSW`` or a vector
      index with ``SECONDARY_ENGINE_ATTRIBUTE`` specifying algorithm,
      ``M``, and distance metric, for example::

        SECONDARY_ENGINE_ATTRIBUTE='{"algorithm": "hnsw", "M": "16", "distance": "l2"}'

    - Distance functions:
      - ``L2_DISTANCE(embedding, TO_VECTOR('[...]'))``
      - ``COSINE_DISTANCE(embedding, TO_VECTOR('[...]'))``
    - Server parameters (depending on configuration):
      - ``loose_vector_index_enabled``
      - ``loose_hnsw_ef_search`` and other HNSW-related options.

    Differences from :class:`MariaDBVectorStore`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    - Uses MySQL ``VECTOR`` columns and ``TO_VECTOR``/``L2_DISTANCE``
      functions instead of MariaDB's ``VECTOR(...)`` together with
      ``VEC_FromText``/``VEC_DISTANCE_COSINE``.
    - Uses ``JSON_EXTRACT`` / ``JSON_UNQUOTE`` to filter on the metadata
      JSON column.
    - Optionally uses ``loose_hnsw_ef_search`` to control ANN search
      breadth.
    """

    # LlamaIndex protocol flags
    stores_text: bool = True
    flat_metadata: bool = False

    # Pydantic model fields ( persisted configuration )
    connection_string: str
    connection_args: Dict[str, Any]
    table_name: str
    database: str
    embed_dim: int
    ann_index_algorithm: str
    ann_index_distance: str
    ann_m: int
    ef_search: int
    perform_setup: bool
    debug: bool

    # Runtime-only attributes
    _engine: Any = PrivateAttr()
    _aengine: Any = PrivateAttr()
    _is_initialized: bool = PrivateAttr(default=False)

    def__init__(
        self,
        connection_string: Union[str, sqlalchemy.engine.URL],
        connection_args: Optional[Dict[str, Any]] = None,
        table_name: str = "llamaindex",
        database: Optional[str] = None,
        embed_dim: int = 1536,
        ann_index_algorithm: str = "hnsw",
        ann_index_distance: str = "l2",
        ann_m: int = 16,
        ef_search: int = 20,
        perform_setup: bool = True,
        debug: bool = False,
    ) -> None:
"""
        Constructor.

        Args:
            connection_string: SQLAlchemy/MySQL connection string, for
                example ``mysql+pymysql://user:pwd@host:3306/database``.
            connection_args: Extra connection arguments passed to
                SQLAlchemy. For Volcengine RDS MySQL this typically
                includes SSL options and read timeouts.
            table_name: Name of the table used to store vectors. Defaults
                to ``"llamaindex"``.
            database: Name of the database/schema (for bookkeeping only;
                the actual target is taken from the connection string).
            embed_dim: Embedding dimension. Must match the upstream
                embedding model dimension.
            ann_index_algorithm: Vector index algorithm. RDS MySQL
                currently supports ``"hnsw"``.
            ann_index_distance: Distance metric, ``"l2"`` or
                ``"cosine"``.
            ann_m: HNSW parameter ``M`` (maximum number of neighbors per
                node). Affects recall and performance.
            ef_search: HNSW ``ef_search`` parameter controlling search
                breadth at query time.
            perform_setup: If ``True``, perform basic capability checks
                and create the table/index on initialization.
            debug: If ``True``, enable SQLAlchemy SQL logging.

        """
        super().__init__(
            connection_string=str(connection_string),
            connection_args=connection_args
            or {
                "ssl": {"ssl_mode": "PREFERRED"},
                "read_timeout": 30,
            },
            table_name=table_name,
            database=database or "",
            embed_dim=embed_dim,
            ann_index_algorithm=ann_index_algorithm.lower(),
            ann_index_distance=ann_index_distance.lower(),
            ann_m=ann_m,
            ef_search=ef_search,
            perform_setup=perform_setup,
            debug=debug,
        )

        # Private attrs
        self._engine = None
        self._aengine = None
        self._is_initialized = False

    # ------------------------------------------------------------------
    # LlamaIndex base metadata
    # ------------------------------------------------------------------

    @classmethod
    defclass_name(cls) -> str:
"""Return the vector store type name used by LlamaIndex."""
        return "VolcengineMySQLVectorStore"

    @property
    defclient(self) -> Any:  # type: ignore[override]
"""Return the underlying SQLAlchemy engine (if initialized)."""
        if not self._is_initialized:
            return None
        return self._engine

    @property
    defaclient(self) -> Any:  # type: ignore[override]
"""Return the underlying Async SQLAlchemy engine (if initialized)."""
        if not self._is_initialized:
            return None
        return self._aengine

    defclose(self) -> None:
"""Dispose the underlying SQLAlchemy engine."""
        if not self._is_initialized:
            return

        assert self._engine is not None
        self._engine.dispose()
        self._is_initialized = False

    async defaclose(self) -> None:
"""Dispose the underlying Async SQLAlchemy engine."""
        if self._aengine is not None:
            await self._aengine.dispose()
            self._aengine = None

    # ------------------------------------------------------------------
    # Factory construction
    # ------------------------------------------------------------------

    @classmethod
    deffrom_params(
        cls,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        table_name: str = "llamaindex",
        connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
        connection_args: Optional[Dict[str, Any]] = None,
        embed_dim: int = 1536,
        ann_index_algorithm: str = "hnsw",
        ann_index_distance: str = "l2",
        ann_m: int = 16,
        ef_search: int = 20,
        perform_setup: bool = True,
        debug: bool = False,
    ) -> "VolcengineMySQLVectorStore":
"""
        Construct a vector store from basic connection parameters.

        Args:
            host: Hostname of the Volcengine RDS MySQL instance.
            port: Port of the MySQL instance (typically 3306).
            database: Database/schema name.
            user: Database username.
            password: Database password.
            table_name: Name of the table used to store vectors.
            connection_string: Optional full SQLAlchemy connection string.
                If provided, it takes precedence over ``host``/``user``/
                ``password``/``database``.
            connection_args: Optional dict of extra SQLAlchemy connection
                arguments.
            embed_dim: Embedding dimension.
            ann_index_algorithm: Vector index algorithm, typically
                ``"hnsw"``.
            ann_index_distance: Distance metric, ``"l2"`` or
                ``"cosine"``.
            ann_m: HNSW ``M`` parameter.
            ef_search: HNSW ``ef_search`` parameter.
            perform_setup: Whether to create the table/index and validate
                configuration on initialization.
            debug: Whether to emit SQL debug logs.

        """
        if connection_string is None:
            if not all([host, port, database, user]):
                raise ValueError(
                    "host/port/database/user must all be provided, or pass a full connection_string instead."
                )
            password_safe = quote_plus(password or "")
            connection_string = (
                f"mysql+pymysql://{user}:{password_safe}@{host}:{port}/{database}"
            )

        return cls(
            connection_string=connection_string,
            connection_args=connection_args,
            table_name=table_name,
            database=database,
            embed_dim=embed_dim,
            ann_index_algorithm=ann_index_algorithm,
            ann_index_distance=ann_index_distance,
            ann_m=ann_m,
            ef_search=ef_search,
            perform_setup=perform_setup,
            debug=debug,
        )

    # ------------------------------------------------------------------
    # Internal initialization & DDL
    # ------------------------------------------------------------------

    def_connect(self) -> None:
"""Create SQLAlchemy engine."""
        self._engine = sqlalchemy.create_engine(
            self.connection_string,
            connect_args=self.connection_args,
            echo=self.debug,
        )

    def_aconnect(self) -> None:
"""Create Async SQLAlchemy engine."""
        if self._aengine is not None:
            return

        # Prepare async connection string
        # We replace 'pymysql' with 'aiomysql' if present
        async_conn_str = self.connection_string.replace("pymysql", "aiomysql")

        # aiomysql does not support 'read_timeout' which is commonly used in pymysql
        # Filter out incompatible args
        filtered_args = {
            k: v for k, v in self.connection_args.items() if k != "read_timeout"
        }

        self._aengine = create_async_engine(
            async_conn_str,
            connect_args=filtered_args,
            echo=self.debug,
        )

    def_validate_server_capability(self) -> None:
"""
        Validate that the MySQL server supports Volcengine vector index.

        The current implementation performs only a basic check:

        - Run ``SHOW VARIABLES LIKE 'loose_vector_index_enabled'`` and
          verify that the value is ``ON``.
        - If the variable is missing or disabled, raise an error and ask
          the user to enable it in the RDS console or parameter template.

        This method can be extended to also inspect ``SELECT VERSION()``
        and enforce a minimum server version if needed.
        """
        assert self._engine is not None

        with self._engine.connect() as connection:
            # Check loose_vector_index_enabled
            result = connection.execute(
                sqlalchemy.text("SHOW VARIABLES LIKE :var"),
                {"var": "loose_vector_index_enabled"},
            )
            row = result.fetchone()
            if not row or str(row[1]).upper() != "ON":
                raise ValueError(
                    "Volcengine MySQL vector index is not enabled: please set loose_vector_index_enabled to ON."
                )

    def_create_table_if_not_exists(self) -> None:
"""
        Create table with a VECTOR column and HNSW vector index if needed.

        Example schema::

            CREATE TABLE IF NOT EXISTS `table_name` (
                id BIGINT PRIMARY KEY AUTO_INCREMENT,
                node_id VARCHAR(255) NOT NULL,
                text LONGTEXT,
                metadata JSON,
                embedding VECTOR(1536) NOT NULL,
                INDEX idx_node_id (node_id),
                VECTOR INDEX idx_embedding (embedding)
                  SECONDARY_ENGINE_ATTRIBUTE='{"algorithm": "hnsw", "M": "16", "distance": "l2"}'
            ) ENGINE = InnoDB;

        Notes
        -----
        - Vector indexes can typically only be created on empty tables.
          It is therefore recommended to let this class create the table
          *before* any data is written.
        - If a user has already created the table without a vector
          index, this method will **not** attempt to run
          ``ALTER TABLE ... ADD VECTOR INDEX`` on existing data in order
          to avoid long locks or failures. In that case, please migrate
          the data manually or create the correct schema ahead of time.

        """
        assert self._engine is not None

        sec_attr = (
            "{"  # Build JSON string for SECONDARY_ENGINE_ATTRIBUTE
            f'"algorithm": "{self.ann_index_algorithm}", '
            f'"M": "{self.ann_m}", '
            f'"distance": "{self.ann_index_distance}"'
            "}"
        )

        create_stmt = f"""
        CREATE TABLE IF NOT EXISTS `{self.table_name}` (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            node_id VARCHAR(255) NOT NULL,
            text LONGTEXT,
            metadata JSON,
            embedding VECTOR({self.embed_dim}) NOT NULL,
            INDEX idx_node_id (node_id),
            VECTOR INDEX idx_embedding (embedding)
              SECONDARY_ENGINE_ATTRIBUTE='{sec_attr}'
        ) ENGINE = InnoDB
        """

        with self._engine.connect() as connection:
            connection.execute(sqlalchemy.text(create_stmt))
            connection.commit()

    def_initialize(self) -> None:
"""Ensure engine is created and table is ready."""
        if self._engine is None:
            self._connect()

        if self._is_initialized:
            return

        if self.perform_setup:
            self._validate_server_capability()
            self._create_table_if_not_exists()

        self._is_initialized = True

    async def_ainitialize(self) -> None:
"""Ensure async engine is created and table is ready."""
        if self._aengine is None:
            self._aconnect()

        if self._is_initialized:
            return

        if self.perform_setup:
            await self._avalidate_server_capability()
            await self._acreate_table_if_not_exists()

        self._is_initialized = True

    async def_avalidate_server_capability(self) -> None:
"""Async version of _validate_server_capability."""
        assert self._aengine is not None

        async with self._aengine.connect() as connection:
            result = await connection.execute(
                sqlalchemy.text("SHOW VARIABLES LIKE :var"),
                {"var": "loose_vector_index_enabled"},
            )
            row = result.fetchone()
            if not row or str(row[1]).upper() != "ON":
                raise ValueError(
                    "Volcengine MySQL vector index is not enabled: please set loose_vector_index_enabled to ON."
                )

    async def_acreate_table_if_not_exists(self) -> None:
"""Async version of _create_table_if_not_exists."""
        assert self._aengine is not None

        sec_attr = (
            "{"  # Build JSON string for SECONDARY_ENGINE_ATTRIBUTE
            f'"algorithm": "{self.ann_index_algorithm}", '
            f'"M": "{self.ann_m}", '
            f'"distance": "{self.ann_index_distance}"'
            "}"
        )

        create_stmt = f"""
        CREATE TABLE IF NOT EXISTS `{self.table_name}` (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            node_id VARCHAR(255) NOT NULL,
            text LONGTEXT,
            metadata JSON,
            embedding VECTOR({self.embed_dim}) NOT NULL,
            INDEX idx_node_id (node_id),
            VECTOR INDEX idx_embedding (embedding)
              SECONDARY_ENGINE_ATTRIBUTE='{sec_attr}'
        ) ENGINE = InnoDB
        """

        async with self._aengine.connect() as connection:
            await connection.execute(sqlalchemy.text(create_stmt))
            await connection.commit()

    # ------------------------------------------------------------------
    # Helpers for (de)serializing nodes and filters
    # ------------------------------------------------------------------

    def_node_to_table_row(self, node: BaseNode) -> Dict[str, Any]:
"""Convert a BaseNode into a plain row dict ready for insertion."""
        return {
            "node_id": node.node_id,
            "text": node.get_content(metadata_mode=MetadataMode.NONE),
            "embedding": node.get_embedding(),
            "metadata": node_to_metadata_dict(
                node,
                remove_text=True,
                flat_metadata=self.flat_metadata,
            ),
        }

    def_to_mysql_operator(self, operator: FilterOperator) -> str:
"""Map LlamaIndex FilterOperator to SQL operator string."""
        if operator == FilterOperator.EQ:
            return "="
        if operator == FilterOperator.GT:
            return ">"
        if operator == FilterOperator.LT:
            return "<"
        if operator == FilterOperator.NE:
            return "!="
        if operator == FilterOperator.GTE:
            return ">="
        if operator == FilterOperator.LTE:
            return "<="
        if operator == FilterOperator.IN:
            return "IN"
        if operator == FilterOperator.NIN:
            return "NOT IN"

        _logger.warning("Unsupported operator: %s, fallback to '='", operator)
        return "="

    def_build_filter_clause(
        self,
        filter_: MetadataFilter,
        params: Dict[str, Any],
        param_counter: List[int],
    ) -> str:
"""
        Build a single metadata filter expression for the JSON column.

        Rules:
        - For string values use ``JSON_UNQUOTE(JSON_EXTRACT(...))`` in
          comparisons.
        - For numeric values compare the result of ``JSON_EXTRACT(...)``
          directly.
        - For ``IN``/``NIN`` operators build a ``(v1, v2, ...)`` value
          list.
        """
        key_expr = f"JSON_EXTRACT(metadata, '$.{filter_.key}')"
        value = filter_.value

        if filter_.operator in [FilterOperator.IN, FilterOperator.NIN]:
            assert isinstance(value, list), (
                "The value for an IN/NIN filter must be a list"
            )
            param_keys: List[str] = []
            for v in value:
                param_name = f"filter_param_{param_counter[0]}"
                param_counter[0] += 1

                # For IN/NIN, we always compare as strings after JSON_UNQUOTE
                if isinstance(v, str):
                    params[param_name] = v
                else:
                    params[param_name] = str(v)

                param_keys.append(f":{param_name}")

            filter_value = f"({', '.join(param_keys)})"
            return f"JSON_UNQUOTE({key_expr}) {self._to_mysql_operator(filter_.operator)}{filter_value}"

        # Scalar comparison
        param_name = f"filter_param_{param_counter[0]}"
        param_counter[0] += 1
        params[param_name] = value

        if isinstance(value, str):
            expr = f"JSON_UNQUOTE({key_expr}) {self._to_mysql_operator(filter_.operator)} :{param_name}"
        else:
            # For numeric or other non-string values, compare the JSON_EXTRACT
            # result directly.
            expr = (
                f"{key_expr}{self._to_mysql_operator(filter_.operator)} :{param_name}"
            )

        return expr

    def_filters_to_where_clause(
        self,
        filters: MetadataFilters,
        params: Dict[str, Any],
        param_counter: List[int],
    ) -> str:
"""Convert MetadataFilters tree into a SQL WHERE clause (without 'WHERE')."""
        conditions_map = {
            FilterCondition.OR: "OR",
            FilterCondition.AND: "AND",
        }

        if filters.condition not in conditions_map:
            raise ValueError(
                f"Unsupported condition: {filters.condition}. "
                f"Must be one of {list(conditions_map.keys())}"
            )

        clauses: List[str] = []
        for f in filters.filters:
            if isinstance(f, MetadataFilter):
                clauses.append(self._build_filter_clause(f, params, param_counter))
            elif isinstance(f, MetadataFilters):
                sub = self._filters_to_where_clause(f, params, param_counter)
                if sub:
                    clauses.append(f"({sub})")
            else:
                raise ValueError(
                    "Unsupported filter type: {type(f)}. Must be one of "
                    f"MetadataFilter, MetadataFilters"
                )

        return f" {conditions_map[filters.condition]} ".join(clauses)

    def_db_rows_to_query_result(
        self, rows: List[DBEmbeddingRow]
    ) -> VectorStoreQueryResult:
"""Convert internal DB rows to LlamaIndex VectorStoreQueryResult."""
        nodes: List[BaseNode] = []
        similarities: List[float] = []
        ids: List[str] = []

        for r in rows:
            metadata = r.metadata or {}

            # If the metadata contains the special fields used by
            # `metadata_dict_to_node`, reconstruct the original node.
            # Otherwise, fall back to a plain TextNode so that we can still
            # return meaningful results when only custom metadata is stored.
            if isinstance(metadata, dict) and metadata.get("_node_content") is not None:
                node = metadata_dict_to_node(metadata)
                node.set_content(str(r.text))
            else:
                node = TextNode(text=str(r.text), id_=r.node_id, metadata=metadata)
            nodes.append(node)
            ids.append(r.node_id)
            similarities.append(r.similarity)

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    # ------------------------------------------------------------------
    # Public API: get_nodes / add / delete / query
    # ------------------------------------------------------------------

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:  # type: ignore[override]
"""
        Get nodes by ``node_ids``.

        Note:
            The current implementation only supports exact lookup by
            ``node_ids`` and ignores the ``filters`` argument.

        """
        self._initialize()

        if not node_ids:
            return []

        # Use bind parameters for the IN clause
        stmt_str = (
            f"SELECT text, metadata FROM `{self.table_name}` WHERE node_id IN :node_ids"
        )
        stmt = sqlalchemy.text(stmt_str).bindparams(
            sqlalchemy.bindparam("node_ids", expanding=True)
        )

        assert self._engine is not None
        with self._engine.connect() as connection:
            result = connection.execute(stmt, {"node_ids": node_ids})

        nodes: List[BaseNode] = []
        for item in result:
            raw_meta = item.metadata
            metadata = json.loads(raw_meta) if isinstance(raw_meta, str) else raw_meta

            if isinstance(metadata, dict) and metadata.get("_node_content") is not None:
                node = metadata_dict_to_node(metadata)
                node.set_content(str(item.text))
            else:
                node = TextNode(text=str(item.text), metadata=metadata or {})

            nodes.append(node)

        return nodes

    defadd(
        self,
        nodes: Sequence[BaseNode],
        **kwargs: Any,
    ) -> List[str]:  # type: ignore[override]
"""
        Add nodes with embeddings into the MySQL vector store.

        Expectations:
        - Each :class:`BaseNode` in ``nodes`` must already contain an
          ``embedding`` (normally computed by the index or embedding
          model upstream).
        - The embedding is serialized as a JSON array string and passed
          to ``TO_VECTOR(:embedding)`` when inserting into the
          ``VECTOR`` column.
        - Rows are inserted in batch using ``executemany`` semantics to
          reduce round trips.
        """
        self._initialize()

        if not nodes:
            return []

        ids: List[str] = []
        rows: List[Dict[str, Any]] = []

        for node in nodes:
            ids.append(node.node_id)
            item = self._node_to_table_row(node)
            rows.append(
                {
                    "node_id": item["node_id"],
                    "text": item["text"],
                    # TO_VECTOR expects a string like "[1.0,2.0,...]"
                    "embedding": json.dumps(item["embedding"]),
                    "metadata": json.dumps(item["metadata"]),
                }
            )

        insert_stmt = sqlalchemy.text(
            f"""
            INSERT INTO `{self.table_name}` (node_id, text, embedding, metadata)
            VALUES (:node_id, :text, TO_VECTOR(:embedding), :metadata)

        )

        assert self._engine is not None
        with self._engine.connect() as connection:
            connection.execute(insert_stmt, rows)
            connection.commit()

        return ids

    async defasync_add(  # type: ignore[override]
        self,
        nodes: Sequence[BaseNode],
        **kwargs: Any,
    ) -> List[str]:
"""
        Add nodes with embeddings into the MySQL vector store asynchronously.
        """
        await self._ainitialize()

        if not nodes:
            return []

        ids: List[str] = []
        rows: List[Dict[str, Any]] = []

        for node in nodes:
            ids.append(node.node_id)
            item = self._node_to_table_row(node)
            rows.append(
                {
                    "node_id": item["node_id"],
                    "text": item["text"],
                    # TO_VECTOR expects a string like "[1.0,2.0,...]"
                    "embedding": json.dumps(item["embedding"]),
                    "metadata": json.dumps(item["metadata"]),
                }
            )

        insert_stmt = sqlalchemy.text(
            f"""
            INSERT INTO `{self.table_name}` (node_id, text, embedding, metadata)
            VALUES (:node_id, :text, TO_VECTOR(:embedding), :metadata)

        )

        async with self._aengine.connect() as connection:
            await connection.execute(insert_stmt, rows)
            await connection.commit()

        return ids

    defdelete(
        self,
        ref_doc_id: str,
        **delete_kwargs: Any,
    ) -> None:  # type: ignore[override]
"""Delete all nodes whose metadata.ref_doc_id equals the given value."""
        self._initialize()

        if not ref_doc_id:
            return

        stmt = sqlalchemy.text(
            f"""
            DELETE FROM `{self.table_name}`
            WHERE JSON_EXTRACT(metadata, '$.ref_doc_id') = :doc_id

        )

        assert self._engine is not None
        with self._engine.connect() as connection:
            connection.execute(stmt, {"doc_id": ref_doc_id})
            connection.commit()

    async defadelete(  # type: ignore[override]
        self,
        ref_doc_id: str,
        **delete_kwargs: Any,
    ) -> None:
"""Async wrapper around :meth:`delete`."""
        await self._ainitialize()

        if not ref_doc_id:
            return

        stmt = sqlalchemy.text(
            f"""
            DELETE FROM `{self.table_name}`
            WHERE JSON_EXTRACT(metadata, '$.ref_doc_id') = :doc_id

        )

        async with self._aengine.connect() as connection:
            await connection.execute(stmt, {"doc_id": ref_doc_id})
            await connection.commit()

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:  # type: ignore[override]
"""
        Delete nodes by ``node_ids``.

        Note:
            The current implementation only supports deletion by
            ``node_ids`` and ignores ``filters``.

        """
        self._initialize()

        if not node_ids:
            return

        stmt_str = f"DELETE FROM `{self.table_name}` WHERE node_id IN :node_ids"
        stmt = sqlalchemy.text(stmt_str).bindparams(
            sqlalchemy.bindparam("node_ids", expanding=True)
        )

        assert self._engine is not None
        with self._engine.connect() as connection:
            connection.execute(stmt, {"node_ids": node_ids})
            connection.commit()

    async defadelete_nodes(  # type: ignore[override]
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""Async wrapper around :meth:`delete_nodes`."""
        await self._ainitialize()

        if not node_ids:
            return

        stmt_str = f"DELETE FROM `{self.table_name}` WHERE node_id IN :node_ids"
        stmt = sqlalchemy.text(stmt_str).bindparams(
            sqlalchemy.bindparam("node_ids", expanding=True)
        )

        async with self._aengine.connect() as connection:
            await connection.execute(stmt, {"node_ids": node_ids})
            await connection.commit()

    defcount(self) -> int:
"""Return total number of rows in the table."""
        self._initialize()

        stmt = sqlalchemy.text(f"SELECT COUNT(*) FROM `{self.table_name}`")

        assert self._engine is not None
        with self._engine.connect() as connection:
            result = connection.execute(stmt)
            value = result.scalar()

        return int(value or 0)

    defdrop(self) -> None:
"""Drop the underlying table and dispose the engine."""
        self._initialize()

        stmt = sqlalchemy.text(f"DROP TABLE IF EXISTS `{self.table_name}`")

        assert self._engine is not None
        with self._engine.connect() as connection:
            connection.execute(stmt)
            connection.commit()

        self.close()

    defclear(self) -> None:  # type: ignore[override]
"""Delete all rows from the table (keep schema & indexes)."""
        self._initialize()

        stmt = sqlalchemy.text(f"DELETE FROM `{self.table_name}`")

        assert self._engine is not None
        with self._engine.connect() as connection:
            connection.execute(stmt)
            connection.commit()

    async defaclear(self) -> None:  # type: ignore[override]
"""Async wrapper around :meth:`clear`."""
        await self._ainitialize()

        stmt = sqlalchemy.text(f"DELETE FROM `{self.table_name}`")

        async with self._aengine.connect() as connection:
            await connection.execute(stmt)
            await connection.commit()

    def_build_distance_expression(self) -> str:
"""
        Return the SQL distance expression template used in ORDER BY.

        The returned string uses a named bind parameter ``:query_embedding``
        (serialized JSON array string) and the ``embedding`` column.
        """
        if self.ann_index_distance == "cosine":
            func_name = "COSINE_DISTANCE"
        else:
            # Default to L2 distance
            func_name = "L2_DISTANCE"

        return f"{func_name}(embedding, TO_VECTOR(:query_embedding))"

    defquery(  # type: ignore[override]
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Execute a vector similarity search on Volcengine RDS MySQL.

        - Only ``VectorStoreQueryMode.DEFAULT`` is supported.
        - The database-side vector index and distance functions are used
          to perform ANN/KNN search.
        - :class:`MetadataFilters` are translated into a ``WHERE``
          clause over the JSON ``metadata`` column.
        - Returned similarities are computed as ``1 / (1 + distance)``.
        """
        if query.mode != VectorStoreQueryMode.DEFAULT:
            raise NotImplementedError(f"Query mode {query.mode} not available.")

        if query.query_embedding is None:
            raise ValueError(
                "VolcengineMySQLVectorStore only supports embedding-based queries; query_embedding must be provided"
            )

        self._initialize()

        distance_expr = self._build_distance_expression()

        base_stmt = f"""
        SELECT
            node_id,
            text,
            metadata,
{distance_expr} AS distance
        FROM `{self.table_name}`
        """

        # Metadata filters
        params = {
            "query_embedding": json.dumps(query.query_embedding),
            "limit": int(query.similarity_top_k),
        }

        if query.filters is not None:
            param_counter = [0]
            where_clause = self._filters_to_where_clause(
                query.filters, params, param_counter
            )
            if where_clause:
                base_stmt += f" WHERE {where_clause}"

        base_stmt += " ORDER BY distance LIMIT :limit"

        rows: List[DBEmbeddingRow] = []

        assert self._engine is not None
        with self._engine.connect() as connection:
            # Optionally set ef_search, which affects recall and latency
            if self.ef_search:
                try:
                    connection.execute(
                        sqlalchemy.text(
                            "SET SESSION loose_hnsw_ef_search = :ef_search"
                        ),
                        {"ef_search": int(self.ef_search)},
                    )
                except Exception:  # pragma: no cover - tolerate cases where the parameter does not exist
                    _logger.warning(
                        "Failed to set loose_hnsw_ef_search, continue without it.",
                        exc_info=True,
                    )

            result = connection.execute(sqlalchemy.text(base_stmt), params)

            for item in result:
                raw_meta = item.metadata
                metadata = (
                    json.loads(raw_meta) if isinstance(raw_meta, str) else raw_meta
                )
                distance = float(item.distance) if item.distance is not None else 0.0
                similarity = 1.0 / (1.0 + distance)

                rows.append(
                    DBEmbeddingRow(
                        node_id=item.node_id,
                        text=item.text,
                        metadata=metadata,
                        similarity=similarity,
                    )
                )

        return self._db_rows_to_query_result(rows)

    async defaquery(  # type: ignore[override]
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""Async wrapper around :meth:`query`."""
        if query.mode != VectorStoreQueryMode.DEFAULT:
            raise NotImplementedError(f"Query mode {query.mode} not available.")

        if query.query_embedding is None:
            raise ValueError(
                "VolcengineMySQLVectorStore only supports embedding-based queries; query_embedding must be provided"
            )

        await self._ainitialize()

        distance_expr = self._build_distance_expression()

        base_stmt = f"""
        SELECT
            node_id,
            text,
            metadata,
{distance_expr} AS distance
        FROM `{self.table_name}`
        """

        # Metadata filters
        params = {
            "query_embedding": json.dumps(query.query_embedding),
            "limit": int(query.similarity_top_k),
        }

        if query.filters is not None:
            param_counter = [0]
            where_clause = self._filters_to_where_clause(
                query.filters, params, param_counter
            )
            if where_clause:
                base_stmt += f" WHERE {where_clause}"

        base_stmt += " ORDER BY distance LIMIT :limit"

        rows: List[DBEmbeddingRow] = []

        async with self._aengine.connect() as connection:
            # Optionally set ef_search, which affects recall and latency
            if self.ef_search:
                try:
                    await connection.execute(
                        sqlalchemy.text(
                            "SET SESSION loose_hnsw_ef_search = :ef_search"
                        ),
                        {"ef_search": int(self.ef_search)},
                    )
                except Exception:
                    _logger.warning(
                        "Failed to set loose_hnsw_ef_search, continue without it.",
                        exc_info=True,
                    )

            result = await connection.execute(sqlalchemy.text(base_stmt), params)

            for item in result:
                raw_meta = item.metadata
                metadata = (
                    json.loads(raw_meta) if isinstance(raw_meta, str) else raw_meta
                )
                distance = float(item.distance) if item.distance is not None else 0.0
                similarity = 1.0 / (1.0 + distance)

                rows.append(
                    DBEmbeddingRow(
                        node_id=item.node_id,
                        text=item.text,
                        metadata=metadata,
                        similarity=similarity,
                    )
                )

        return self._db_rows_to_query_result(rows)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.client "Permanent link")

```
client: 

```

Return the underlying SQLAlchemy engine (if initialized).
###  aclient `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.aclient "Permanent link")

```
aclient: 

```

Return the underlying Async SQLAlchemy engine (if initialized).
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.class_name "Permanent link")

```
class_name() -> 

```

Return the vector store type name used by LlamaIndex.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
173
174
175
176
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Return the vector store type name used by LlamaIndex."""
    return "VolcengineMySQLVectorStore"

```
 |  
| --- | --- |  
###  close [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.close "Permanent link")

```
close() -> None

```

Dispose the underlying SQLAlchemy engine.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
192
193
194
195
196
197
198
199
```
 | 
```
defclose(self) -> None:
"""Dispose the underlying SQLAlchemy engine."""
    if not self._is_initialized:
        return

    assert self._engine is not None
    self._engine.dispose()
    self._is_initialized = False

```
 |  
| --- | --- |  
###  aclose [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.aclose "Permanent link")

```
aclose() -> None

```

Dispose the underlying Async SQLAlchemy engine.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
201
202
203
204
205
```
 | 
```
async defaclose(self) -> None:
"""Dispose the underlying Async SQLAlchemy engine."""
    if self._aengine is not None:
        await self._aengine.dispose()
        self._aengine = None

```
 |  
| --- | --- |  
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.from_params "Permanent link")

```
from_params(
    host: Optional[] = None,
    port: Optional[] = None,
    database: Optional[] = None,
    user: Optional[] = None,
    password: Optional[] = None,
    table_name:  = "llamaindex",
    connection_string: Optional[Union[, ]] = None,
    connection_args: Optional[[, ]] = None,
    embed_dim:  = 1536,
    ann_index_algorithm:  = "hnsw",
    ann_index_distance:  = "l2",
    ann_m:  = 16,
    ef_search:  = 20,
    perform_setup:  = True,
    debug:  = False,
) -> "VolcengineMySQLVectorStore"

```

Construct a vector store from basic connection parameters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  `Optional[str]`  |  Hostname of the Volcengine RDS MySQL instance.  |  `None`  |  
|  `port`  |  `Optional[int]`  |  Port of the MySQL instance (typically 3306).  |  `None`  |  
|  `database`  |  `Optional[str]`  |  Database/schema name.  |  `None`  |  
|  `user`  |  `Optional[str]`  |  Database username.  |  `None`  |  
|  `password`  |  `Optional[str]`  |  Database password.  |  `None`  |  
|  `table_name`  |  Name of the table used to store vectors.  |  `'llamaindex'`  |  
|  `connection_string`  |  `Optional[Union[str, URL]]`  |  Optional full SQLAlchemy connection string. If provided, it takes precedence over `host`/`user`/ `password`/`database`.  |  `None`  |  
|  `connection_args`  |  `Optional[Dict[str, Any]]`  |  Optional dict of extra SQLAlchemy connection arguments.  |  `None`  |  
|  `embed_dim`  |  Embedding dimension.  |  `1536`  |  
|  `ann_index_algorithm`  |  Vector index algorithm, typically `"hnsw"`.  |  `'hnsw'`  |  
|  `ann_index_distance`  |  Distance metric, `"l2"` or `"cosine"`.  |  `'l2'`  |  
|  `ann_m`  |  HNSW `M` parameter.  |  
|  `ef_search`  |  HNSW `ef_search` parameter.  |  
|  `perform_setup`  |  `bool`  |  Whether to create the table/index and validate configuration on initialization.  |  `True`  |  
|  `debug`  |  `bool`  |  Whether to emit SQL debug logs.  |  `False`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_params(
    cls,
    host: Optional[str] = None,
    port: Optional[int] = None,
    database: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    table_name: str = "llamaindex",
    connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
    connection_args: Optional[Dict[str, Any]] = None,
    embed_dim: int = 1536,
    ann_index_algorithm: str = "hnsw",
    ann_index_distance: str = "l2",
    ann_m: int = 16,
    ef_search: int = 20,
    perform_setup: bool = True,
    debug: bool = False,
) -> "VolcengineMySQLVectorStore":
"""
    Construct a vector store from basic connection parameters.

    Args:
        host: Hostname of the Volcengine RDS MySQL instance.
        port: Port of the MySQL instance (typically 3306).
        database: Database/schema name.
        user: Database username.
        password: Database password.
        table_name: Name of the table used to store vectors.
        connection_string: Optional full SQLAlchemy connection string.
            If provided, it takes precedence over ``host``/``user``/
            ``password``/``database``.
        connection_args: Optional dict of extra SQLAlchemy connection
            arguments.
        embed_dim: Embedding dimension.
        ann_index_algorithm: Vector index algorithm, typically
            ``"hnsw"``.
        ann_index_distance: Distance metric, ``"l2"`` or
            ``"cosine"``.
        ann_m: HNSW ``M`` parameter.
        ef_search: HNSW ``ef_search`` parameter.
        perform_setup: Whether to create the table/index and validate
            configuration on initialization.
        debug: Whether to emit SQL debug logs.

    """
    if connection_string is None:
        if not all([host, port, database, user]):
            raise ValueError(
                "host/port/database/user must all be provided, or pass a full connection_string instead."
            )
        password_safe = quote_plus(password or "")
        connection_string = (
            f"mysql+pymysql://{user}:{password_safe}@{host}:{port}/{database}"
        )

    return cls(
        connection_string=connection_string,
        connection_args=connection_args,
        table_name=table_name,
        database=database,
        embed_dim=embed_dim,
        ann_index_algorithm=ann_index_algorithm,
        ann_index_distance=ann_index_distance,
        ann_m=ann_m,
        ef_search=ef_search,
        perform_setup=perform_setup,
        debug=debug,
    )

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes by `node_ids`.
Note
The current implementation only supports exact lookup by `node_ids` and ignores the `filters` argument.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:  # type: ignore[override]
"""
    Get nodes by ``node_ids``.

    Note:
        The current implementation only supports exact lookup by
        ``node_ids`` and ignores the ``filters`` argument.

    """
    self._initialize()

    if not node_ids:
        return []

    # Use bind parameters for the IN clause
    stmt_str = (
        f"SELECT text, metadata FROM `{self.table_name}` WHERE node_id IN :node_ids"
    )
    stmt = sqlalchemy.text(stmt_str).bindparams(
        sqlalchemy.bindparam("node_ids", expanding=True)
    )

    assert self._engine is not None
    with self._engine.connect() as connection:
        result = connection.execute(stmt, {"node_ids": node_ids})

    nodes: List[BaseNode] = []
    for item in result:
        raw_meta = item.metadata
        metadata = json.loads(raw_meta) if isinstance(raw_meta, str) else raw_meta

        if isinstance(metadata, dict) and metadata.get("_node_content") is not None:
            node = metadata_dict_to_node(metadata)
            node.set_content(str(item.text))
        else:
            node = TextNode(text=str(item.text), metadata=metadata or {})

        nodes.append(node)

    return nodes

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.add "Permanent link")

```
add(nodes: Sequence[], **kwargs: ) -> []

```

Add nodes with embeddings into the MySQL vector store.
Expectations: - Each :class:`BaseNode` in `nodes` must already contain an `embedding` (normally computed by the index or embedding model upstream). - The embedding is serialized as a JSON array string and passed to `TO_VECTOR(:embedding)` when inserting into the `VECTOR` column. - Rows are inserted in batch using `executemany` semantics to reduce round trips.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: Sequence[BaseNode],
    **kwargs: Any,
) -> List[str]:  # type: ignore[override]
"""
    Add nodes with embeddings into the MySQL vector store.

    Expectations:
    - Each :class:`BaseNode` in ``nodes`` must already contain an
      ``embedding`` (normally computed by the index or embedding
      model upstream).
    - The embedding is serialized as a JSON array string and passed
      to ``TO_VECTOR(:embedding)`` when inserting into the
      ``VECTOR`` column.
    - Rows are inserted in batch using ``executemany`` semantics to
      reduce round trips.
    """
    self._initialize()

    if not nodes:
        return []

    ids: List[str] = []
    rows: List[Dict[str, Any]] = []

    for node in nodes:
        ids.append(node.node_id)
        item = self._node_to_table_row(node)
        rows.append(
            {
                "node_id": item["node_id"],
                "text": item["text"],
                # TO_VECTOR expects a string like "[1.0,2.0,...]"
                "embedding": json.dumps(item["embedding"]),
                "metadata": json.dumps(item["metadata"]),
            }
        )

    insert_stmt = sqlalchemy.text(
        f"""
        INSERT INTO `{self.table_name}` (node_id, text, embedding, metadata)
        VALUES (:node_id, :text, TO_VECTOR(:embedding), :metadata)
        """
    )

    assert self._engine is not None
    with self._engine.connect() as connection:
        connection.execute(insert_stmt, rows)
        connection.commit()

    return ids

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.async_add "Permanent link")

```
async_add(
    nodes: Sequence[], **kwargs: 
) -> []

```

Add nodes with embeddings into the MySQL vector store asynchronously.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
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
```
 | 
```
async defasync_add(  # type: ignore[override]
    self,
    nodes: Sequence[BaseNode],
    **kwargs: Any,
) -> List[str]:
"""
    Add nodes with embeddings into the MySQL vector store asynchronously.
    """
    await self._ainitialize()

    if not nodes:
        return []

    ids: List[str] = []
    rows: List[Dict[str, Any]] = []

    for node in nodes:
        ids.append(node.node_id)
        item = self._node_to_table_row(node)
        rows.append(
            {
                "node_id": item["node_id"],
                "text": item["text"],
                # TO_VECTOR expects a string like "[1.0,2.0,...]"
                "embedding": json.dumps(item["embedding"]),
                "metadata": json.dumps(item["metadata"]),
            }
        )

    insert_stmt = sqlalchemy.text(
        f"""
        INSERT INTO `{self.table_name}` (node_id, text, embedding, metadata)
        VALUES (:node_id, :text, TO_VECTOR(:embedding), :metadata)
        """
    )

    async with self._aengine.connect() as connection:
        await connection.execute(insert_stmt, rows)
        await connection.commit()

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete all nodes whose metadata.ref_doc_id equals the given value.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
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
```
 | 
```
defdelete(
    self,
    ref_doc_id: str,
    **delete_kwargs: Any,
) -> None:  # type: ignore[override]
"""Delete all nodes whose metadata.ref_doc_id equals the given value."""
    self._initialize()

    if not ref_doc_id:
        return

    stmt = sqlalchemy.text(
        f"""
        DELETE FROM `{self.table_name}`
        WHERE JSON_EXTRACT(metadata, '$.ref_doc_id') = :doc_id
        """
    )

    assert self._engine is not None
    with self._engine.connect() as connection:
        connection.execute(stmt, {"doc_id": ref_doc_id})
        connection.commit()

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Async wrapper around :meth:`delete`.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
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
```
 | 
```
async defadelete(  # type: ignore[override]
    self,
    ref_doc_id: str,
    **delete_kwargs: Any,
) -> None:
"""Async wrapper around :meth:`delete`."""
    await self._ainitialize()

    if not ref_doc_id:
        return

    stmt = sqlalchemy.text(
        f"""
        DELETE FROM `{self.table_name}`
        WHERE JSON_EXTRACT(metadata, '$.ref_doc_id') = :doc_id
        """
    )

    async with self._aengine.connect() as connection:
        await connection.execute(stmt, {"doc_id": ref_doc_id})
        await connection.commit()

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes by `node_ids`.
Note
The current implementation only supports deletion by `node_ids` and ignores `filters`.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
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
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:  # type: ignore[override]
"""
    Delete nodes by ``node_ids``.

    Note:
        The current implementation only supports deletion by
        ``node_ids`` and ignores ``filters``.

    """
    self._initialize()

    if not node_ids:
        return

    stmt_str = f"DELETE FROM `{self.table_name}` WHERE node_id IN :node_ids"
    stmt = sqlalchemy.text(stmt_str).bindparams(
        sqlalchemy.bindparam("node_ids", expanding=True)
    )

    assert self._engine is not None
    with self._engine.connect() as connection:
        connection.execute(stmt, {"node_ids": node_ids})
        connection.commit()

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Async wrapper around :meth:`delete_nodes`.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
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
```
 | 
```
async defadelete_nodes(  # type: ignore[override]
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""Async wrapper around :meth:`delete_nodes`."""
    await self._ainitialize()

    if not node_ids:
        return

    stmt_str = f"DELETE FROM `{self.table_name}` WHERE node_id IN :node_ids"
    stmt = sqlalchemy.text(stmt_str).bindparams(
        sqlalchemy.bindparam("node_ids", expanding=True)
    )

    async with self._aengine.connect() as connection:
        await connection.execute(stmt, {"node_ids": node_ids})
        await connection.commit()

```
 |  
| --- | --- |  
###  count [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.count "Permanent link")

```
count() -> 

```

Return total number of rows in the table.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
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
```
 | 
```
defcount(self) -> int:
"""Return total number of rows in the table."""
    self._initialize()

    stmt = sqlalchemy.text(f"SELECT COUNT(*) FROM `{self.table_name}`")

    assert self._engine is not None
    with self._engine.connect() as connection:
        result = connection.execute(stmt)
        value = result.scalar()

    return int(value or 0)

```
 |  
| --- | --- |  
###  drop [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.drop "Permanent link")

```
drop() -> None

```

Drop the underlying table and dispose the engine.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
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
```
 | 
```
defdrop(self) -> None:
"""Drop the underlying table and dispose the engine."""
    self._initialize()

    stmt = sqlalchemy.text(f"DROP TABLE IF EXISTS `{self.table_name}`")

    assert self._engine is not None
    with self._engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()

    self.close()

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.clear "Permanent link")

```
clear() -> None

```

Delete all rows from the table (keep schema & indexes).
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
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
```
 | 
```
defclear(self) -> None:  # type: ignore[override]
"""Delete all rows from the table (keep schema & indexes)."""
    self._initialize()

    stmt = sqlalchemy.text(f"DELETE FROM `{self.table_name}`")

    assert self._engine is not None
    with self._engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.aclear "Permanent link")

```
aclear() -> None

```

Async wrapper around :meth:`clear`.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
901
902
903
904
905
906
907
908
909
```
 | 
```
async defaclear(self) -> None:  # type: ignore[override]
"""Async wrapper around :meth:`clear`."""
    await self._ainitialize()

    stmt = sqlalchemy.text(f"DELETE FROM `{self.table_name}`")

    async with self._aengine.connect() as connection:
        await connection.execute(stmt)
        await connection.commit()

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Execute a vector similarity search on Volcengine RDS MySQL.
  * Only `VectorStoreQueryMode.DEFAULT` is supported.
  * The database-side vector index and distance functions are used to perform ANN/KNN search.
  * :class:`MetadataFilters` are translated into a `WHERE` clause over the JSON `metadata` column.
  * Returned similarities are computed as `1 / (1 + distance)`.

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
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
1011
1012
1013
1014
1015
1016
```
 | 
```
defquery(  # type: ignore[override]
    self,
    query: VectorStoreQuery,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""
    Execute a vector similarity search on Volcengine RDS MySQL.

    - Only ``VectorStoreQueryMode.DEFAULT`` is supported.
    - The database-side vector index and distance functions are used
      to perform ANN/KNN search.
    - :class:`MetadataFilters` are translated into a ``WHERE``
      clause over the JSON ``metadata`` column.
    - Returned similarities are computed as ``1 / (1 + distance)``.
    """
    if query.mode != VectorStoreQueryMode.DEFAULT:
        raise NotImplementedError(f"Query mode {query.mode} not available.")

    if query.query_embedding is None:
        raise ValueError(
            "VolcengineMySQLVectorStore only supports embedding-based queries; query_embedding must be provided"
        )

    self._initialize()

    distance_expr = self._build_distance_expression()

    base_stmt = f"""
    SELECT
        node_id,
        text,
        metadata,
{distance_expr} AS distance
    FROM `{self.table_name}`
    """

    # Metadata filters
    params = {
        "query_embedding": json.dumps(query.query_embedding),
        "limit": int(query.similarity_top_k),
    }

    if query.filters is not None:
        param_counter = [0]
        where_clause = self._filters_to_where_clause(
            query.filters, params, param_counter
        )
        if where_clause:
            base_stmt += f" WHERE {where_clause}"

    base_stmt += " ORDER BY distance LIMIT :limit"

    rows: List[DBEmbeddingRow] = []

    assert self._engine is not None
    with self._engine.connect() as connection:
        # Optionally set ef_search, which affects recall and latency
        if self.ef_search:
            try:
                connection.execute(
                    sqlalchemy.text(
                        "SET SESSION loose_hnsw_ef_search = :ef_search"
                    ),
                    {"ef_search": int(self.ef_search)},
                )
            except Exception:  # pragma: no cover - tolerate cases where the parameter does not exist
                _logger.warning(
                    "Failed to set loose_hnsw_ef_search, continue without it.",
                    exc_info=True,
                )

        result = connection.execute(sqlalchemy.text(base_stmt), params)

        for item in result:
            raw_meta = item.metadata
            metadata = (
                json.loads(raw_meta) if isinstance(raw_meta, str) else raw_meta
            )
            distance = float(item.distance) if item.distance is not None else 0.0
            similarity = 1.0 / (1.0 + distance)

            rows.append(
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=metadata,
                    similarity=similarity,
                )
            )

    return self._db_rows_to_query_result(rows)

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/volcengine_mysql/#llama_index.vector_stores.volcengine_mysql.VolcengineMySQLVectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Async wrapper around :meth:`query`.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-volcenginemysql/llama_index/vector_stores/volcengine_mysql/base.py`  
| 
```
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
```
 | 
```
async defaquery(  # type: ignore[override]
    self,
    query: VectorStoreQuery,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""Async wrapper around :meth:`query`."""
    if query.mode != VectorStoreQueryMode.DEFAULT:
        raise NotImplementedError(f"Query mode {query.mode} not available.")

    if query.query_embedding is None:
        raise ValueError(
            "VolcengineMySQLVectorStore only supports embedding-based queries; query_embedding must be provided"
        )

    await self._ainitialize()

    distance_expr = self._build_distance_expression()

    base_stmt = f"""
    SELECT
        node_id,
        text,
        metadata,
{distance_expr} AS distance
    FROM `{self.table_name}`
    """

    # Metadata filters
    params = {
        "query_embedding": json.dumps(query.query_embedding),
        "limit": int(query.similarity_top_k),
    }

    if query.filters is not None:
        param_counter = [0]
        where_clause = self._filters_to_where_clause(
            query.filters, params, param_counter
        )
        if where_clause:
            base_stmt += f" WHERE {where_clause}"

    base_stmt += " ORDER BY distance LIMIT :limit"

    rows: List[DBEmbeddingRow] = []

    async with self._aengine.connect() as connection:
        # Optionally set ef_search, which affects recall and latency
        if self.ef_search:
            try:
                await connection.execute(
                    sqlalchemy.text(
                        "SET SESSION loose_hnsw_ef_search = :ef_search"
                    ),
                    {"ef_search": int(self.ef_search)},
                )
            except Exception:
                _logger.warning(
                    "Failed to set loose_hnsw_ef_search, continue without it.",
                    exc_info=True,
                )

        result = await connection.execute(sqlalchemy.text(base_stmt), params)

        for item in result:
            raw_meta = item.metadata
            metadata = (
                json.loads(raw_meta) if isinstance(raw_meta, str) else raw_meta
            )
            distance = float(item.distance) if item.distance is not None else 0.0
            similarity = 1.0 / (1.0 + distance)

            rows.append(
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=metadata,
                    similarity=similarity,
                )
            )

    return self._db_rows_to_query_result(rows)

```
 |  
| --- | --- |  
options: members: - VolcengineMySQLVectorStore
