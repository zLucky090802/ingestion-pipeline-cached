# Postgres
##  PGVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/postgres/#llama_index.vector_stores.postgres.PGVectorStore "Permanent link")
Bases: 
Postgres Vector Store.
Examples:
`pip install llama-index-vector-stores-postgres`

```
fromllama_index.vector_stores.postgresimport PGVectorStore

# Create PGVectorStore instance
vector_store = PGVectorStore.from_params(
    database="vector_db",
    host="localhost",
    password="password",
    port=5432,
    user="postgres",
    table_name="paul_graham_essay",
    embed_dim=1536  # openai embedding dimension
    use_halfvec=True  # Enable half precision
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-postgres/llama_index/vector_stores/postgres/base.py`  
| 
```
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
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
1263
1264
1265
1266
1267
1268
1269
1270
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
1282
1283
1284
1285
1286
1287
1288
1289
1290
1291
1292
1293
1294
1295
1296
1297
1298
1299
1300
1301
1302
1303
1304
1305
1306
1307
1308
1309
1310
1311
1312
1313
1314
1315
1316
1317
1318
1319
1320
1321
1322
1323
1324
1325
1326
1327
1328
1329
1330
1331
1332
1333
1334
1335
1336
1337
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
1352
1353
1354
1355
1356
1357
1358
1359
1360
1361
1362
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
1379
1380
1381
1382
1383
1384
1385
1386
1387
1388
1389
1390
1391
1392
1393
1394
1395
1396
1397
1398
1399
1400
1401
1402
1403
1404
1405
1406
1407
1408
1409
1410
1411
1412
1413
1414
1415
1416
1417
1418
1419
1420
1421
1422
1423
1424
1425
1426
1427
1428
1429
1430
1431
1432
1433
1434
1435
1436
1437
1438
1439
1440
1441
1442
1443
1444
1445
1446
1447
1448
1449
1450
1451
1452
1453
1454
1455
1456
1457
1458
1459
1460
1461
1462
1463
1464
1465
1466
1467
1468
1469
1470
1471
1472
1473
1474
1475
1476
1477
1478
1479
1480
1481
1482
1483
1484
1485
1486
1487
1488
1489
1490
1491
1492
1493
1494
1495
1496
1497
1498
1499
1500
1501
1502
1503
1504
1505
1506
1507
1508
1509
1510
1511
1512
1513
1514
1515
1516
1517
1518
1519
1520
1521
1522
1523
1524
1525
1526
1527
1528
1529
1530
1531
1532
1533
1534
1535
1536
1537
1538
1539
1540
1541
1542
1543
1544
1545
1546
1547
1548
1549
1550
1551
1552
1553
1554
1555
1556
1557
1558
1559
1560
1561
1562
1563
1564
1565
1566
1567
1568
1569
1570
1571
1572
1573
1574
1575
1576
1577
1578
1579
1580
1581
1582
1583
1584
1585
1586
1587
1588
1589
1590
1591
1592
1593
1594
1595
1596
1597
1598
1599
1600
1601
1602
1603
1604
1605
1606
1607
1608
1609
1610
1611
1612
1613
1614
1615
1616
1617
1618
1619
1620
1621
1622
1623
1624
1625
1626
1627
1628
1629
1630
1631
1632
1633
1634
1635
1636
1637
1638
1639
1640
1641
1642
1643
1644
1645
1646
1647
1648
1649
1650
1651
1652
1653
1654
1655
1656
1657
1658
1659
1660
1661
1662
1663
1664
1665
1666
1667
1668
1669
1670
1671
1672
1673
1674
1675
1676
1677
1678
1679
1680
1681
1682
1683
1684
1685
1686
1687
1688
```
 | 
```
classPGVectorStore(BasePydanticVectorStore):
"""
    Postgres Vector Store.

    Examples:
        `pip install llama-index-vector-stores-postgres`

        ```python
        from llama_index.vector_stores.postgres import PGVectorStore

        # Create PGVectorStore instance
        vector_store = PGVectorStore.from_params(
            database="vector_db",
            host="localhost",
            password="password",
            port=5432,
            user="postgres",
            table_name="paul_graham_essay",
            embed_dim=1536  # openai embedding dimension
            use_halfvec=True  # Enable half precision

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    connection_string: str
    async_connection_string: str
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
    _async_engine: Optional[sqlalchemy.ext.asyncio.AsyncEngine] = PrivateAttr(
        default=None
    )
    _async_session: sqlalchemy.ext.asyncio.AsyncSession = PrivateAttr()
    _is_initialized: bool = PrivateAttr(default=False)
    _customize_query_fn: Optional[Callable[[Select, Any, Any], Select]] = PrivateAttr(
        default=None
    )

    def__init__(
        self,
        connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
        async_connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
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
        async_engine: Optional[sqlalchemy.ext.asyncio.AsyncEngine] = None,
        indexed_metadata_keys: Optional[Set[Tuple[str, PGType]]] = None,
        customize_query_fn: Optional[Callable[[Select, Any, Any], Select]] = None,
    ) -> None:
"""
        Constructor.

        Args:
            connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to postgres db.
            async_connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to async pg db.
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
            async_engine (Optional[sqlalchemy.ext.asyncio.AsyncEngine], optional): SQLAlchemy async engine instance to use. Defaults to None.
            indexed_metadata_keys (Optional[List[Tuple[str, str]]], optional): Set of metadata keys with their type to index. Defaults to None.
            customize_query_fn (Optional[Callable[[Select, Any, Any], Select]], optional): Function used to customize PostgreSQL queries. Defaults to None.

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
            async_connection_string=str(async_connection_string),
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

        # both engine and async_engine must be provided, or both must be None
        if engine is not None and async_engine is not None:
            self._engine = engine
            self._async_engine = async_engine
        elif engine is None and async_engine is None:
            pass
        else:
            raise ValueError(
                "Both engine and async_engine must be provided, or both must be None"
            )

        self._customize_query_fn = customize_query_fn

    async defclose(self) -> None:
        if not self._is_initialized:
            return

        if self._engine:
            self._engine.dispose()
        if self._async_engine:
            await self._async_engine.dispose()

    @classmethod
    defclass_name(cls) -> str:
        return "PGVectorStore"

    @classmethod
    deffrom_params(
        cls,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        table_name: str = "llamaindex",
        schema_name: str = "public",
        connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
        async_connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
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
        customize_query_fn: Optional[Callable[[Select, Any, Any], Select]] = None,
    ) -> "PGVectorStore":
"""
        Construct from params.

        Args:
            host (Optional[str], optional): Host of postgres connection. Defaults to None.
            port (Optional[str], optional): Port of postgres connection. Defaults to None.
            database (Optional[str], optional): Postgres DB name. Defaults to None.
            user (Optional[str], optional): Postgres username. Defaults to None.
            password (Optional[str], optional): Postgres password. Defaults to None.
            table_name (str): Table name. Defaults to "llamaindex".
            schema_name (str): Schema name. Defaults to "public".
            connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to postgres db
            async_connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to async pg db
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
            customize_query_fn (Optional[Callable[[Select, Any, Any], Select]], optional): Function used to customize PostgreSQL queries. Defaults to None.

        Returns:
            PGVectorStore: Instance of PGVectorStore constructed from params.

        """
        conn_str = (
            connection_string
            or f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )
        async_conn_str = async_connection_string or (
            f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
        )
        return cls(
            connection_string=conn_str,
            async_connection_string=async_conn_str,
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
            customize_query_fn=customize_query_fn,
        )

    @property
    defclient(self) -> Any:
        if not self._is_initialized:
            return None
        return self._engine

    def_connect(self) -> Any:
        fromsqlalchemyimport create_engine
        fromsqlalchemy.ext.asyncioimport AsyncSession, create_async_engine
        fromsqlalchemy.ormimport sessionmaker

        self._engine = self._engine or create_engine(
            self.connection_string, echo=self.debug, **self.create_engine_kwargs
        )
        self._session = sessionmaker(self._engine)

        self._async_engine = self._async_engine or create_async_engine(
            self.async_connection_string, **self.create_engine_kwargs
        )
        self._async_session = sessionmaker(self._async_engine, class_=AsyncSession)  # type: ignore

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
            self._table_class.__table__.create(session.connection(), checkfirst=True)

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
                f"USING hnsw (embedding {hnsw_dist_method}) "
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

    async defasync_add(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
        self._initialize()
        ids = []
        async with self._async_session() as session, session.begin():
            for node in nodes:
                ids.append(node.node_id)
                item = self._node_to_table_row(node)
                session.add(item)
            await session.commit()
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
        elif operator == FilterOperator.ANY:
            return "?|"
        elif operator == FilterOperator.ALL:
            return "?&"
        else:
            _logger.warning(f"Unknown operator: {operator}, fallback to '='")
            return "="

    def_build_filter_clause(self, filter_: MetadataFilter) -> Any:
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
        elif filter_.operator in [FilterOperator.ANY, FilterOperator.ALL]:
            # Expects a text array stored in the metadata, and a list of values to compare
            # Works with text[] arrays using PostgreSQL ?| (ANY) and ?& (ALL) operators
            # Example: metadata_::jsonb->'tags' ?| array['AI', 'ML']
            filter_value = ", ".join(f"'{e}'" for e in filter_.value)

            return text(
                f"metadata_::jsonb->'{filter_.key}' "
                f"{self._to_postgres_operator(filter_.operator)} "
                f"array[{filter_value}]"
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
        **kwargs: Any,
    ) -> Any:
        stmt = select(  # type: ignore
            self._table_class.id,
            self._table_class.node_id,
            self._table_class.text,
            self._table_class.metadata_,
            self._table_class.embedding.cosine_distance(embedding).label("distance"),
        ).order_by(text("distance asc"))

        if self._customize_query_fn is not None:
            stmt = self._customize_query_fn(stmt, self._table_class, **kwargs)

        return self._apply_filters_and_limit(stmt, limit, metadata_filters)

    def_get_query_session_settings(self, **kwargs: Any) -> List[Tuple[str, dict]]:
"""Build list of (SQL, params) for index-specific session settings."""
        settings: List[Tuple[str, dict]] = []
        needs_bitmapscan_off = False
        if kwargs.get("ivfflat_probes"):
            settings.append(
                (
                    "SET ivfflat.probes = :ivfflat_probes",
                    {"ivfflat_probes": int(kwargs["ivfflat_probes"])},
                )
            )
            needs_bitmapscan_off = True
        if self.hnsw_kwargs:
            hnsw_ef_search = (
                kwargs.get("hnsw_ef_search") or self.hnsw_kwargs["hnsw_ef_search"]
            )
            settings.append(
                (
                    "SET hnsw.ef_search = :hnsw_ef_search",
                    {"hnsw_ef_search": int(hnsw_ef_search)},
                )
            )
            needs_bitmapscan_off = True
        if needs_bitmapscan_off:
            settings.append(("SET LOCAL enable_bitmapscan = off", {}))
        return settings

    def_query_with_score(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> List[DBEmbeddingRow]:
        stmt = self._build_query(embedding, limit, metadata_filters, **kwargs)
        with self._session() as session, session.begin():
            if kwargs.get("ivfflat_probes"):
                ivfflat_probes = kwargs.get("ivfflat_probes")
                session.execute(
                    text(f"SET ivfflat.probes = :ivfflat_probes"),
                    {"ivfflat_probes": ivfflat_probes},
                )
                session.execute(text("SET LOCAL enable_bitmapscan = off"))
            if self.hnsw_kwargs:
                hnsw_ef_search = (
                    kwargs.get("hnsw_ef_search") or self.hnsw_kwargs["hnsw_ef_search"]
                )
                session.execute(
                    text(f"SET hnsw.ef_search = :hnsw_ef_search"),
                    {"hnsw_ef_search": hnsw_ef_search},
                )
                session.execute(text("SET LOCAL enable_bitmapscan = off"))

            res = session.execute(
                stmt,
            )
            return [
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=item.metadata_,
                    custom_fields={
                        key: val
                        for key, val in item._asdict().items()
                        if key not in ["id", "node_id", "text", "metadata_", "distance"]
                    },
                    similarity=(1 - item.distance) if item.distance is not None else 0,
                )
                for item in res.all()
            ]

    async def_aquery_with_score(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> List[DBEmbeddingRow]:
        stmt = self._build_query(embedding, limit, metadata_filters, **kwargs)
        async with self._async_session() as async_session, async_session.begin():
            if self.hnsw_kwargs:
                hnsw_ef_search = (
                    kwargs.get("hnsw_ef_search") or self.hnsw_kwargs["hnsw_ef_search"]
                )
                await async_session.execute(
                    text(f"SET hnsw.ef_search = {hnsw_ef_search}"),
                )
                await async_session.execute(text("SET LOCAL enable_bitmapscan = off"))
            if kwargs.get("ivfflat_probes"):
                ivfflat_probes = kwargs.get("ivfflat_probes")
                await async_session.execute(
                    text(f"SET ivfflat.probes = :ivfflat_probes"),
                    {"ivfflat_probes": ivfflat_probes},
                )
                await async_session.execute(text("SET LOCAL enable_bitmapscan = off"))

            res = await async_session.execute(stmt)
            return [
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=item.metadata_,
                    custom_fields={
                        key: val
                        for key, val in item._asdict().items()
                        if key not in ["id", "node_id", "text", "metadata_", "distance"]
                    },
                    similarity=(1 - item.distance) if item.distance is not None else 0,
                )
                for item in res.all()
            ]

    def_build_sparse_query(
        self,
        query_str: Optional[str],
        limit: int,
        metadata_filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> Any:
        fromsqlalchemyimport type_coerce
        fromsqlalchemy.sqlimport func, text, select
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

        # Remove special characters used by ts_query (essentially, all punctuation except single periods within words)
        # and collapse multiple spaces
        query_str = re.sub(r"(?!\b\.\b)\W+", " ", query_str).strip()

        # Replace space with "|" to perform an OR search for higher recall
        query_str = query_str.replace(" ", "|")

        ts_query = func.to_tsquery(
            type_coerce(self.text_search_config, REGCONFIG),
            query_str,
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

        if self._customize_query_fn is not None:
            stmt = self._customize_query_fn(stmt, self._table_class, **kwargs)

        # type: ignore
        return self._apply_filters_and_limit(stmt, limit, metadata_filters)

    async def_async_sparse_query_with_rank(
        self,
        query_str: Optional[str] = None,
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
    ) -> List[DBEmbeddingRow]:
        stmt = self._build_sparse_query(query_str, limit, metadata_filters)
        async with self._async_session() as async_session, async_session.begin():
            res = await async_session.execute(stmt)
            return [
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=item.metadata_,
                    custom_fields={
                        key: val
                        for key, val in item._asdict().items()
                        if key not in ["id", "node_id", "text", "metadata_", "rank"]
                    },
                    similarity=item.rank,
                )
                for item in res.all()
            ]

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
                    custom_fields={
                        key: val
                        for key, val in item._asdict().items()
                        if key not in ["id", "node_id", "text", "metadata_", "rank"]
                    },
                    similarity=item.rank,
                )
                for item in res.all()
            ]

    async def_async_hybrid_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> List[DBEmbeddingRow]:
        importasyncio

        if query.alpha is not None:
            _logger.warning("postgres hybrid search does not support alpha parameter.")

        sparse_top_k = query.sparse_top_k or query.similarity_top_k

        results = await asyncio.gather(
            self._aquery_with_score(
                query.query_embedding,
                query.similarity_top_k,
                query.filters,
                **kwargs,
            ),
            self._async_sparse_query_with_rank(
                query.query_str, sparse_top_k, query.filters
            ),
        )

        dense_results, sparse_results = results
        all_results = dense_results + sparse_results
        return _dedup_results(all_results)

    def_hybrid_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> List[DBEmbeddingRow]:
        if query.alpha is not None:
            _logger.warning("postgres hybrid search does not support alpha parameter.")

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

    def_build_query_with_embedding(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> Any:
"""Build a query that also returns embeddings (needed for MMR)."""
        stmt = select(
            self._table_class.id,
            self._table_class.node_id,
            self._table_class.text,
            self._table_class.metadata_,
            self._table_class.embedding,
            self._table_class.embedding.cosine_distance(embedding).label("distance"),
        ).order_by(text("distance asc"))

        if self._customize_query_fn is not None:
            stmt = self._customize_query_fn(stmt, self._table_class, **kwargs)

        return self._apply_filters_and_limit(stmt, limit, metadata_filters)

    def_query_with_embedding(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> List[Tuple[DBEmbeddingRow, List[float]]]:
"""Query and return results with their embeddings."""
        stmt = self._build_query_with_embedding(
            embedding, limit, metadata_filters, **kwargs
        )
        with self._session() as session, session.begin():
            for sql, params in self._get_query_session_settings(**kwargs):
                session.execute(text(sql), params)

            res = session.execute(stmt)
            return [
                (
                    DBEmbeddingRow(
                        node_id=item.node_id,
                        text=item.text,
                        metadata=item.metadata_,
                        custom_fields={
                            key: val
                            for key, val in item._asdict().items()
                            if key
                            not in [
                                "id",
                                "node_id",
                                "text",
                                "metadata_",
                                "distance",
                                "embedding",
                            ]
                        },
                        similarity=(1 - item.distance)
                        if item.distance is not None
                        else 0,
                    ),
                    list(item.embedding) if item.embedding is not None else [],
                )
                for item in res.all()
            ]

    async def_async_query_with_embedding(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> List[Tuple[DBEmbeddingRow, List[float]]]:
"""Async query and return results with their embeddings."""
        stmt = self._build_query_with_embedding(
            embedding, limit, metadata_filters, **kwargs
        )
        async with self._async_session() as async_session, async_session.begin():
            for sql, params in self._get_query_session_settings(**kwargs):
                await async_session.execute(text(sql), params)

            res = await async_session.execute(stmt)
            return [
                (
                    DBEmbeddingRow(
                        node_id=item.node_id,
                        text=item.text,
                        metadata=item.metadata_,
                        custom_fields={
                            key: val
                            for key, val in item._asdict().items()
                            if key
                            not in [
                                "id",
                                "node_id",
                                "text",
                                "metadata_",
                                "distance",
                                "embedding",
                            ]
                        },
                        similarity=(1 - item.distance)
                        if item.distance is not None
                        else 0,
                    ),
                    list(item.embedding) if item.embedding is not None else [],
                )
                for item in res.all()
            ]

    def_prepare_mmr_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> Tuple[int, Optional[float]]:
"""Validate MMR parameters and compute prefetch_k and mmr_threshold."""
        if query.query_embedding is None:
            raise ValueError("MMR query requires query_embedding")

        if (
            kwargs.get("mmr_prefetch_factor") is not None
            and kwargs.get("mmr_prefetch_k") is not None
        ):
            raise ValueError(
                "'mmr_prefetch_factor' and 'mmr_prefetch_k' "
                "cannot coexist in a call to query()"
            )

        mmr_prefetch_k = kwargs.get("mmr_prefetch_k")
        if mmr_prefetch_k is not None:
            prefetch_k = int(mmr_prefetch_k)
        else:
            prefetch_k = int(
                query.similarity_top_k
                * kwargs.get("mmr_prefetch_factor", DEFAULT_MMR_PREFETCH_FACTOR)
            )
        prefetch_k = max(prefetch_k, query.similarity_top_k)

        mmr_threshold = (
            query.mmr_threshold
            if query.mmr_threshold is not None
            else kwargs.get("mmr_threshold")
        )
        if mmr_threshold is not None and not (0 <= mmr_threshold <= 1):
            raise ValueError(
                f"mmr_threshold must be between 0 and 1, got {mmr_threshold}"
            )

        _logger.debug(
            f"MMR search: prefetching {prefetch_k} candidates for "
            f"{query.similarity_top_k} final results"
        )

        return prefetch_k, mmr_threshold

    def_mmr_rerank_results(
        self,
        query: VectorStoreQuery,
        results_with_embeddings: List[Tuple[DBEmbeddingRow, List[float]]],
        mmr_threshold: Optional[float],
    ) -> Optional[VectorStoreQueryResult]:
"""
        Apply MMR algorithm to prefetched results.

        Returns VectorStoreQueryResult on success, or None if fallback to
        regular search is needed (insufficient valid embeddings).
        """
        if not results_with_embeddings:
            _logger.debug("MMR search: no results found during prefetch")
            return VectorStoreQueryResult(nodes=[], similarities=[], ids=[])

        embeddings = [emb for _, emb in results_with_embeddings]
        node_ids = [row.node_id for row, _ in results_with_embeddings]

        valid_indices = [i for i, emb in enumerate(embeddings) if emb]
        if not valid_indices:
            _logger.debug("MMR search: no valid embeddings found")
            return VectorStoreQueryResult(nodes=[], similarities=[], ids=[])

        valid_embeddings = [embeddings[i] for i in valid_indices]
        valid_node_ids = [node_ids[i] for i in valid_indices]

        if len(valid_embeddings)  query.similarity_top_k:
            _logger.warning(
                f"Not enough valid embeddings for MMR: "
                f"{len(valid_embeddings)}{query.similarity_top_k}. "
                f"Falling back to regular search."
            )
            return None  # Signal caller to fall back

        mmr_similarities, mmr_ids = get_top_k_mmr_embeddings(
            query_embedding=query.query_embedding,
            embeddings=valid_embeddings,
            similarity_top_k=query.similarity_top_k,
            embedding_ids=valid_node_ids,
            mmr_threshold=mmr_threshold,
        )

        result_map = {row.node_id: row for row, _ in results_with_embeddings}
        ordered_rows = []
        for mmr_sim, node_id in zip(mmr_similarities, mmr_ids):
            if node_id in result_map:
                row = result_map[node_id]
                ordered_rows.append(
                    DBEmbeddingRow(
                        node_id=row.node_id,
                        text=row.text,
                        metadata=row.metadata,
                        custom_fields=row.custom_fields,
                        similarity=mmr_sim,
                    )
                )

        _logger.debug(
            f"MMR search completed: {len(ordered_rows)} results selected from "
            f"{len(results_with_embeddings)} candidates"
        )

        return self._db_rows_to_query_result(ordered_rows)

    def_mmr_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Perform MMR (Maximal Marginal Relevance) query.

        MMR balances relevance and diversity by iteratively selecting documents
        that are both similar to the query and dissimilar to already selected documents.

        Args:
            query: VectorStoreQuery with mode set to MMR
            **kwargs: Additional arguments including:
                - mmr_threshold: Float between 0 and 1. Higher values favor relevance,
                  lower values favor diversity. Default is 0.5.
                - mmr_prefetch_factor: Multiplier for prefetch count. Default is 4.
                - mmr_prefetch_k: Explicit prefetch count (overrides mmr_prefetch_factor).

        Returns:
            VectorStoreQueryResult with nodes reranked by MMR algorithm.

        """
        prefetch_k, mmr_threshold = self._prepare_mmr_query(query, **kwargs)

        db_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k not in ("mmr_prefetch_factor", "mmr_prefetch_k", "mmr_threshold")
        }

        results_with_embeddings = self._query_with_embedding(
            query.query_embedding, prefetch_k, query.filters, **db_kwargs
        )

        result = self._mmr_rerank_results(query, results_with_embeddings, mmr_threshold)
        if result is not None:
            return result

        # Fallback to regular search
        rows = self._query_with_score(
            query.query_embedding,
            query.similarity_top_k,
            query.filters,
            **db_kwargs,
        )
        return self._db_rows_to_query_result(rows)

    async def_async_mmr_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Perform async MMR (Maximal Marginal Relevance) query.

        MMR balances relevance and diversity by iteratively selecting documents
        that are both similar to the query and dissimilar to already selected documents.

        Args:
            query: VectorStoreQuery with mode set to MMR
            **kwargs: Additional arguments including:
                - mmr_threshold: Float between 0 and 1. Higher values favor relevance,
                  lower values favor diversity. Default is 0.5.
                - mmr_prefetch_factor: Multiplier for prefetch count. Default is 4.
                - mmr_prefetch_k: Explicit prefetch count (overrides mmr_prefetch_factor).

        Returns:
            VectorStoreQueryResult with nodes reranked by MMR algorithm.

        """
        prefetch_k, mmr_threshold = self._prepare_mmr_query(query, **kwargs)

        db_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k not in ("mmr_prefetch_factor", "mmr_prefetch_k", "mmr_threshold")
        }

        results_with_embeddings = await self._async_query_with_embedding(
            query.query_embedding, prefetch_k, query.filters, **db_kwargs
        )

        result = self._mmr_rerank_results(query, results_with_embeddings, mmr_threshold)
        if result is not None:
            return result

        # Fallback to regular search
        rows = await self._aquery_with_score(
            query.query_embedding,
            query.similarity_top_k,
            query.filters,
            **db_kwargs,
        )
        return self._db_rows_to_query_result(rows)

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
            if db_embedding_row.custom_fields:
                node.metadata["custom_fields"] = db_embedding_row.custom_fields
            similarities.append(db_embedding_row.similarity)
            ids.append(db_embedding_row.node_id)
            nodes.append(node)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities,
            ids=ids,
        )

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
        self._initialize()
        if query.mode == VectorStoreQueryMode.HYBRID:
            results = await self._async_hybrid_query(query, **kwargs)
        elif query.mode in [
            VectorStoreQueryMode.SPARSE,
            VectorStoreQueryMode.TEXT_SEARCH,
        ]:
            sparse_top_k = query.sparse_top_k or query.similarity_top_k
            results = await self._async_sparse_query_with_rank(
                query.query_str, sparse_top_k, query.filters
            )
        elif query.mode == VectorStoreQueryMode.MMR:
            return await self._async_mmr_query(query, **kwargs)
        elif query.mode == VectorStoreQueryMode.DEFAULT:
            results = await self._aquery_with_score(
                query.query_embedding,
                query.similarity_top_k,
                query.filters,
                **kwargs,
            )
        else:
            raise ValueError(f"Invalid query mode: {query.mode}")

        return self._db_rows_to_query_result(results)

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
        elif query.mode == VectorStoreQueryMode.MMR:
            return self._mmr_query(query, **kwargs)
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
                self._table_class.metadata_["ref_doc_id"].astext == ref_doc_id
            )

            session.execute(stmt)
            session.commit()

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        fromsqlalchemyimport delete

        self._initialize()
        async with self._async_session() as session, session.begin():
            stmt = delete(self._table_class).where(
                self._table_class.metadata_["ref_doc_id"].astext == ref_doc_id
            )

            await session.execute(stmt)
            await session.commit()

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

    async defadelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Deletes nodes asynchronously.

        Args:
            node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
            filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

        """
        if not node_ids and not filters:
            return

        fromsqlalchemyimport delete

        self._initialize()
        async with self._async_session() as async_session, async_session.begin():
            stmt = delete(self._table_class)

            if node_ids:
                stmt = stmt.where(self._table_class.node_id.in_(node_ids))

            if filters:
                stmt = stmt.where(self._recursively_apply_filters(filters))

            await async_session.execute(stmt)
            await async_session.commit()

    defclear(self) -> None:
"""Clears table."""
        fromsqlalchemyimport delete

        self._initialize()
        with self._session() as session, session.begin():
            stmt = delete(self._table_class)

            session.execute(stmt)
            session.commit()

    async defaclear(self) -> None:
"""Asynchronously clears table."""
        fromsqlalchemyimport delete

        self._initialize()
        async with self._async_session() as async_session, async_session.begin():
            stmt = delete(self._table_class)

            await async_session.execute(stmt)
            await async_session.commit()

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
                custom_fields = {
                    key: val
                    for key, val in item._asdict().items()
                    if key not in ["id", "node_id", "text", "metadata_"]
                }

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

    async defaget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""Get nodes asynchronously from vector store."""
        assert node_ids is not None or filters is not None, (
            "Either node_ids or filters must be provided"
        )

        self._initialize()

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

        async with self._async_session() as session, session.begin():
            res = (await session.execute(stmt)).fetchall()
            for item in res:
                node_id = item.node_id
                text = item.text
                metadata = item.metadata_
                embedding = item.embedding
                custom_fields = {
                    key: val
                    for key, val in item._asdict().items()
                    if key not in ["id", "node_id", "text", "metadata_"]
                }

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
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/postgres/#llama_index.vector_stores.postgres.PGVectorStore.from_params "Permanent link")

```
from_params(
    host: Optional[] = None,
    port: Optional[] = None,
    database: Optional[] = None,
    user: Optional[] = None,
    password: Optional[] = None,
    table_name:  = "llamaindex",
    schema_name:  = "public",
    connection_string: Optional[Union[, ]] = None,
    async_connection_string: Optional[
        Union[, ]
    ] = None,
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
    customize_query_fn: Optional[
        Callable[[Select, , ], Select]
    ] = None,
) -> 

```

Construct from params.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  `Optional[str]`  |  Host of postgres connection. Defaults to None.  |  `None`  |  
|  `port`  |  `Optional[str]`  |  Port of postgres connection. Defaults to None.  |  `None`  |  
|  `database`  |  `Optional[str]`  |  Postgres DB name. Defaults to None.  |  `None`  |  
|  `user`  |  `Optional[str]`  |  Postgres username. Defaults to None.  |  `None`  |  
|  `password`  |  `Optional[str]`  |  Postgres password. Defaults to None.  |  `None`  |  
|  `table_name`  |  Table name. Defaults to "llamaindex".  |  `'llamaindex'`  |  
|  `schema_name`  |  Schema name. Defaults to "public".  |  `'public'`  |  
|  `connection_string`  |  `Union[str, URL]`  |  Connection string to postgres db  |  `None`  |  
|  `async_connection_string`  |  `Union[str, URL]`  |  Connection string to async pg db  |  `None`  |  
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
|  `customize_query_fn`  |  `Optional[Callable[[Select, Any, Any], Select]]`  |  Function used to customize PostgreSQL queries. Defaults to None.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `PGVectorStore`  |   |  Instance of PGVectorStore constructed from params.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-postgres/llama_index/vector_stores/postgres/base.py`  
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
    table_name: str = "llamaindex",
    schema_name: str = "public",
    connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
    async_connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
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
    customize_query_fn: Optional[Callable[[Select, Any, Any], Select]] = None,
) -> "PGVectorStore":
"""
    Construct from params.

    Args:
        host (Optional[str], optional): Host of postgres connection. Defaults to None.
        port (Optional[str], optional): Port of postgres connection. Defaults to None.
        database (Optional[str], optional): Postgres DB name. Defaults to None.
        user (Optional[str], optional): Postgres username. Defaults to None.
        password (Optional[str], optional): Postgres password. Defaults to None.
        table_name (str): Table name. Defaults to "llamaindex".
        schema_name (str): Schema name. Defaults to "public".
        connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to postgres db
        async_connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to async pg db
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
        customize_query_fn (Optional[Callable[[Select, Any, Any], Select]], optional): Function used to customize PostgreSQL queries. Defaults to None.

    Returns:
        PGVectorStore: Instance of PGVectorStore constructed from params.

    """
    conn_str = (
        connection_string
        or f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )
    async_conn_str = async_connection_string or (
        f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    )
    return cls(
        connection_string=conn_str,
        async_connection_string=async_conn_str,
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
        customize_query_fn=customize_query_fn,
    )

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/postgres/#llama_index.vector_stores.postgres.PGVectorStore.delete_nodes "Permanent link")

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
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-postgres/llama_index/vector_stores/postgres/base.py`  
| 
```
1492
1493
1494
1495
1496
1497
1498
1499
1500
1501
1502
1503
1504
1505
1506
1507
1508
1509
1510
1511
1512
1513
1514
1515
1516
1517
1518
1519
1520
1521
1522
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
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/postgres/#llama_index.vector_stores.postgres.PGVectorStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Deletes nodes asynchronously.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  IDs of nodes to delete. Defaults to None.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters. Defaults to None.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-postgres/llama_index/vector_stores/postgres/base.py`  
| 
```
1524
1525
1526
1527
1528
1529
1530
1531
1532
1533
1534
1535
1536
1537
1538
1539
1540
1541
1542
1543
1544
1545
1546
1547
1548
1549
1550
1551
1552
1553
1554
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Deletes nodes asynchronously.

    Args:
        node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
        filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

    """
    if not node_ids and not filters:
        return

    fromsqlalchemyimport delete

    self._initialize()
    async with self._async_session() as async_session, async_session.begin():
        stmt = delete(self._table_class)

        if node_ids:
            stmt = stmt.where(self._table_class.node_id.in_(node_ids))

        if filters:
            stmt = stmt.where(self._recursively_apply_filters(filters))

        await async_session.execute(stmt)
        await async_session.commit()

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/postgres/#llama_index.vector_stores.postgres.PGVectorStore.clear "Permanent link")

```
clear() -> None

```

Clears table.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-postgres/llama_index/vector_stores/postgres/base.py`  
| 
```
1556
1557
1558
1559
1560
1561
1562
1563
1564
1565
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
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/postgres/#llama_index.vector_stores.postgres.PGVectorStore.aclear "Permanent link")

```
aclear() -> None

```

Asynchronously clears table.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-postgres/llama_index/vector_stores/postgres/base.py`  
| 
```
1567
1568
1569
1570
1571
1572
1573
1574
1575
1576
```
 | 
```
async defaclear(self) -> None:
"""Asynchronously clears table."""
    fromsqlalchemyimport delete

    self._initialize()
    async with self._async_session() as async_session, async_session.begin():
        stmt = delete(self._table_class)

        await async_session.execute(stmt)
        await async_session.commit()

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/postgres/#llama_index.vector_stores.postgres.PGVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes from vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-postgres/llama_index/vector_stores/postgres/base.py`  
| 
```
1578
1579
1580
1581
1582
1583
1584
1585
1586
1587
1588
1589
1590
1591
1592
1593
1594
1595
1596
1597
1598
1599
1600
1601
1602
1603
1604
1605
1606
1607
1608
1609
1610
1611
1612
1613
1614
1615
1616
1617
1618
1619
1620
1621
1622
1623
1624
1625
1626
1627
1628
1629
1630
1631
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
            custom_fields = {
                key: val
                for key, val in item._asdict().items()
                if key not in ["id", "node_id", "text", "metadata_"]
            }

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
###  aget_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/postgres/#llama_index.vector_stores.postgres.PGVectorStore.aget_nodes "Permanent link")

```
aget_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes asynchronously from vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-postgres/llama_index/vector_stores/postgres/base.py`  
| 
```
1633
1634
1635
1636
1637
1638
1639
1640
1641
1642
1643
1644
1645
1646
1647
1648
1649
1650
1651
1652
1653
1654
1655
1656
1657
1658
1659
1660
1661
1662
1663
1664
1665
1666
1667
1668
1669
1670
1671
1672
1673
1674
1675
1676
1677
1678
1679
1680
1681
1682
1683
1684
1685
1686
1687
1688
```
 | 
```
async defaget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""Get nodes asynchronously from vector store."""
    assert node_ids is not None or filters is not None, (
        "Either node_ids or filters must be provided"
    )

    self._initialize()

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

    async with self._async_session() as session, session.begin():
        res = (await session.execute(stmt)).fetchall()
        for item in res:
            node_id = item.node_id
            text = item.text
            metadata = item.metadata_
            embedding = item.embedding
            custom_fields = {
                key: val
                for key, val in item._asdict().items()
                if key not in ["id", "node_id", "text", "metadata_"]
            }

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
options: members: - PGVectorStore
