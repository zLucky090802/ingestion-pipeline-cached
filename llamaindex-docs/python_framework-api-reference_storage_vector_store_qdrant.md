# Qdrant
##  QdrantVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore "Permanent link")
Bases: 
Qdrant Vector Store.
In this vector store, embeddings and docs are stored within a Qdrant collection.
During query time, the index uses Qdrant to query for the top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_name`  |  (str): name of the Qdrant collection  |  _required_  |  
|  `client`  |  `Optional[QdrantClient]`  |  QdrantClient instance from `qdrant-client` package  |  `None`  |  
|  `aclient`  |  `Optional[AsyncQdrantClient]`  |  AsyncQdrantClient instance from `qdrant-client` package  |  `None`  |  
|  `url`  |  `Optional[str]`  |  url of the Qdrant instance  |  `None`  |  
|  `api_key`  |  `Optional[str]`  |  API key for authenticating with Qdrant  |  `None`  |  
|  `batch_size`  |  number of points to upload in a single request to Qdrant. Defaults to 64  |  
|  `parallel`  |  number of parallel processes to use during upload. Defaults to 1  |  
|  `max_retries`  |  maximum number of retries in case of a failure. Defaults to 3  |  
|  `client_kwargs`  |  `Optional[dict]`  |  additional kwargs for QdrantClient and AsyncQdrantClient  |  `None`  |  
|  `enable_hybrid`  |  `bool`  |  whether to enable hybrid search using dense and sparse vectors  |  `False`  |  
|  `fastembed_sparse_model`  |  `Optional[str]`  |  name of the FastEmbed sparse model to use, if any  |  `None`  |  
|  `sparse_doc_fn`  |  `Optional[SparseEncoderCallable]`  |  function to encode sparse vectors  |  `None`  |  
|  `sparse_query_fn`  |  `Optional[SparseEncoderCallable]`  |  function to encode sparse queries  |  `None`  |  
|  `hybrid_fusion_fn`  |  `Optional[HybridFusionCallable]`  |  function to fuse hybrid search results  |  `None`  |  
|  `index_doc_id`  |  `bool`  |  whether to create a payload index for the document ID. Defaults to True  |  `True`  |  
|  `text_key`  |  Name of the field holding the text information, Defaults to 'text'  |  `'text'`  |  
|  `dense_vector_name`  |  `Optional[str]`  |  Custom name for the dense vector field. Defaults to 'text-dense'  |  `None`  |  
|  `sparse_vector_name`  |  `Optional[str]`  |  Custom name for the sparse vector field. Defaults to 'text-sparse-new'  |  `None`  |  
|  `shard_number`  |  `Optional[int]`  |  Shard number for sharding the collection  |  `None`  |  
|  `sharding_method`  |  `Optional[ShardingMethod]`  |  Sharding method for the collection  |  `None`  |  
|  `replication_factor`  |  `Optional[int]`  |  Replication factor for the collection  |  `None`  |  
|  `write_consistency_factor`  |  `Optional[int]`  |  Write consistency factor for the collection  |  `None`  |  
|  `shard_key_selector_fn`  |  `Optional[Callable[..., ShardKeySelector]]`  |  Function to select shard keys  |  `None`  |  
|  `shard_keys`  |  `Optional[list[ShardKey]]`  |  List of shard keys  |  `None`  |  
|  `payload_indexes`  |  `Optional[list[dict[str, PayloadSchemaType]]]`  |  Optional[list[dict[str, rest.PayloadSchemaType]]]: List of payload field indexes  |  `None`  |  
Notes
For backward compatibility, the vector store will automatically detect the vector format of existing collections and adapt accordingly: - For collections created with older versions using unnamed vectors (empty string ""), the vector store will use the legacy format for queries. - For collections with named vectors, it will use the existing vector names. - For new collections, it will use the vector names provided or the defaults.
Examples:
`pip install llama-index-vector-stores-qdrant`

```
importqdrant_client
fromllama_index.vector_stores.qdrantimport QdrantVectorStore

client = qdrant_client.QdrantClient()

vector_store = QdrantVectorStore(
    collection_name="example_collection", client=client
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
1689
1690
1691
1692
1693
1694
1695
1696
1697
1698
1699
1700
1701
1702
1703
1704
1705
1706
1707
1708
1709
1710
1711
1712
1713
1714
1715
1716
1717
1718
1719
1720
1721
1722
1723
1724
1725
1726
```
 | 
```
classQdrantVectorStore(BasePydanticVectorStore):
"""
    Qdrant Vector Store.

    In this vector store, embeddings and docs are stored within a
    Qdrant collection.

    During query time, the index uses Qdrant to query for the top
    k most similar nodes.

    Args:
        collection_name: (str): name of the Qdrant collection
        client (Optional[QdrantClient]): QdrantClient instance from `qdrant-client` package
        aclient (Optional[AsyncQdrantClient]): AsyncQdrantClient instance from `qdrant-client` package
        url (Optional[str]): url of the Qdrant instance
        api_key (Optional[str]): API key for authenticating with Qdrant
        batch_size (int): number of points to upload in a single request to Qdrant. Defaults to 64
        parallel (int): number of parallel processes to use during upload. Defaults to 1
        max_retries (int): maximum number of retries in case of a failure. Defaults to 3
        client_kwargs (Optional[dict]): additional kwargs for QdrantClient and AsyncQdrantClient
        enable_hybrid (bool): whether to enable hybrid search using dense and sparse vectors
        fastembed_sparse_model (Optional[str]): name of the FastEmbed sparse model to use, if any
        sparse_doc_fn (Optional[SparseEncoderCallable]): function to encode sparse vectors
        sparse_query_fn (Optional[SparseEncoderCallable]): function to encode sparse queries
        hybrid_fusion_fn (Optional[HybridFusionCallable]): function to fuse hybrid search results
        index_doc_id (bool): whether to create a payload index for the document ID. Defaults to True
        text_key (str): Name of the field holding the text information, Defaults to 'text'
        dense_vector_name (Optional[str]): Custom name for the dense vector field. Defaults to 'text-dense'
        sparse_vector_name (Optional[str]): Custom name for the sparse vector field. Defaults to 'text-sparse-new'
        shard_number (Optional[int]): Shard number for sharding the collection
        sharding_method (Optional[rest.ShardingMethod]): Sharding method for the collection
        replication_factor (Optional[int]): Replication factor for the collection
        write_consistency_factor (Optional[int]): Write consistency factor for the collection
        shard_key_selector_fn (Optional[Callable[..., rest.ShardKeySelector]]): Function to select shard keys
        shard_keys (Optional[list[rest.ShardKey]]): List of shard keys
        payload_indexes: Optional[list[dict[str, rest.PayloadSchemaType]]]: List of payload field indexes

    Notes:
        For backward compatibility, the vector store will automatically detect the vector format
        of existing collections and adapt accordingly:
        - For collections created with older versions using unnamed vectors (empty string ""),
          the vector store will use the legacy format for queries.
        - For collections with named vectors, it will use the existing vector names.
        - For new collections, it will use the vector names provided or the defaults.

    Examples:
        `pip install llama-index-vector-stores-qdrant`

        ```python
        import qdrant_client
        from llama_index.vector_stores.qdrant import QdrantVectorStore

        client = qdrant_client.QdrantClient()

        vector_store = QdrantVectorStore(
            collection_name="example_collection", client=client

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    collection_name: str
    url: Optional[str]
    api_key: Optional[str]
    batch_size: int
    parallel: int
    max_retries: int
    client_kwargs: dict = Field(default_factory=dict)
    enable_hybrid: bool
    index_doc_id: bool
    fastembed_sparse_model: Optional[str]
    text_key: Optional[str]
    dense_vector_name: str
    sparse_vector_name: str

    _client: QdrantClient = PrivateAttr()
    _aclient: AsyncQdrantClient = PrivateAttr()
    _collection_initialized: bool = PrivateAttr()
    _sparse_doc_fn: Optional[SparseEncoderCallable] = PrivateAttr()
    _sparse_query_fn: Optional[SparseEncoderCallable] = PrivateAttr()
    _hybrid_fusion_fn: Optional[HybridFusionCallable] = PrivateAttr()
    _dense_config: Optional[rest.VectorParams] = PrivateAttr()
    _sparse_config: Optional[rest.SparseVectorParams] = PrivateAttr()
    _quantization_config: Optional[QuantizationConfig] = PrivateAttr()
    _legacy_vector_format: Optional[bool] = PrivateAttr()
    _shard_key_selector_fn: Optional[Callable[..., rest.ShardKeySelector]] = (
        PrivateAttr()
    )
    _shard_keys: Optional[list[rest.ShardKey]] = PrivateAttr()
    _shard_number: Optional[int] = PrivateAttr()
    _sharding_method: Optional[rest.ShardingMethod] = PrivateAttr()
    _replication_factor: Optional[int] = PrivateAttr()
    _write_consistency_factor: Optional[int] = PrivateAttr()
    _payload_indexes: Optional[list[dict[str, rest.PayloadSchemaType]]] = PrivateAttr()

    def__init__(
        self,
        collection_name: str,
        client: Optional[QdrantClient] = None,
        aclient: Optional[AsyncQdrantClient] = None,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        batch_size: int = 64,
        parallel: int = 1,
        max_retries: int = 3,
        client_kwargs: Optional[dict] = None,
        dense_config: Optional[rest.VectorParams] = None,
        sparse_config: Optional[rest.SparseVectorParams] = None,
        quantization_config: Optional[QuantizationConfig] = None,
        enable_hybrid: bool = False,
        fastembed_sparse_model: Optional[str] = None,
        sparse_doc_fn: Optional[SparseEncoderCallable] = None,
        sparse_query_fn: Optional[SparseEncoderCallable] = None,
        hybrid_fusion_fn: Optional[HybridFusionCallable] = None,
        index_doc_id: bool = True,
        text_key: Optional[str] = "text",
        dense_vector_name: Optional[str] = None,
        sparse_vector_name: Optional[str] = None,
        shard_number: Optional[int] = None,
        sharding_method: Optional[rest.ShardingMethod] = None,
        shard_key_selector_fn: Optional[Callable[..., rest.ShardKeySelector]] = None,
        shard_keys: Optional[list[rest.ShardKey]] = None,
        replication_factor: Optional[int] = None,
        write_consistency_factor: Optional[int] = None,
        payload_indexes: Optional[list[dict[str, rest.PayloadSchemaType]]] = None,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        # Set default vector names if not provided
        dense_vector_name = dense_vector_name or DEFAULT_DENSE_VECTOR_NAME
        sparse_vector_name = sparse_vector_name or DEFAULT_SPARSE_VECTOR_NAME

        super().__init__(
            collection_name=collection_name,
            url=url,
            api_key=api_key,
            batch_size=batch_size,
            parallel=parallel,
            max_retries=max_retries,
            client_kwargs=client_kwargs or {},
            enable_hybrid=enable_hybrid,
            index_doc_id=index_doc_id,
            fastembed_sparse_model=fastembed_sparse_model,
            text_key=text_key,
            dense_vector_name=dense_vector_name,
            sparse_vector_name=sparse_vector_name,
        )
        # Track if the user provided their own sparse functions. This is to prevent
        # them from being overwritten by the lazy-init correction for async clients.
        self._user_provided_sparse_doc_fn = sparse_doc_fn is not None
        self._user_provided_sparse_query_fn = sparse_query_fn is not None

        if (
            client is None
            and aclient is None
            and (url is None or api_key is None or collection_name is None)
        ):
            raise ValueError(
                "Must provide either a QdrantClient instance or a url and api_key."
            )

        if client is None and aclient is None:
            client_kwargs = client_kwargs or {}
            self._client = qdrant_client.QdrantClient(
                url=url, api_key=api_key, **client_kwargs
            )
            self._aclient = qdrant_client.AsyncQdrantClient(
                url=url, api_key=api_key, **client_kwargs
            )
        else:
            if client is not None and aclient is not None:
                possible_local_clients = [
                    getattr(client, "_client", None),
                    getattr(aclient, "_client", None),
                ]
                if any(
                    isinstance(client, QdrantLocal) for client in possible_local_clients
                ):
                    logger.warning(
                        "Both client and aclient are provided. If using `:memory:` "
                        "mode, the data between clients is not synced."
                    )

            self._client = client
            self._aclient = aclient

        self._payload_indexes = payload_indexes

        # Check if collection exists and detect vector format
        self._legacy_vector_format = None
        if self._client is not None:
            self._collection_initialized = self._collection_exists(collection_name)
            if self._collection_initialized:
                self._detect_vector_format(collection_name)
                if self._payload_indexes:
                    self._create_payload_indexes()
        else:
            # Need to do lazy init for async clients
            self._collection_initialized = False

        # Setup hybrid search if enabled
        if enable_hybrid or fastembed_sparse_model is not None:
            enable_hybrid = True
            self._sparse_doc_fn = sparse_doc_fn or self.get_default_sparse_doc_encoder(
                collection_name,
                fastembed_sparse_model=fastembed_sparse_model,
            )
            self._sparse_query_fn = (
                sparse_query_fn
                or self.get_default_sparse_query_encoder(
                    collection_name,
                    fastembed_sparse_model=fastembed_sparse_model,
                )
            )
            self._hybrid_fusion_fn = hybrid_fusion_fn or cast(
                HybridFusionCallable, relative_score_fusion
            )

        self._sparse_config = sparse_config
        self._dense_config = dense_config
        self._quantization_config = quantization_config

        self._shard_number = shard_number
        self._sharding_method = sharding_method
        self._shard_key_selector_fn = shard_key_selector_fn
        self._shard_keys = shard_keys
        self._replication_factor = replication_factor
        self._write_consistency_factor = write_consistency_factor

        if self._sharding_method == rest.ShardingMethod.CUSTOM:
            self._validate_custom_sharding()

    @classmethod
    defclass_name(cls) -> str:
        return "QdrantVectorStore"

    defset_query_functions(
        self,
        sparse_doc_fn: Optional[SparseEncoderCallable] = None,
        sparse_query_fn: Optional[SparseEncoderCallable] = None,
        hybrid_fusion_fn: Optional[HybridFusionCallable] = None,
    ):
        self._sparse_doc_fn = sparse_doc_fn
        self._sparse_query_fn = sparse_query_fn
        self._hybrid_fusion_fn = hybrid_fusion_fn

    def_build_points(
        self, nodes: List[BaseNode], sparse_vector_name: str
    ) -> Tuple[List[Any], List[str]]:
        ids = []
        points = []

        for node_batch in iter_batch(nodes, self.batch_size):
            node_ids = []
            vectors: List[Any] = []
            sparse_vectors: List[List[float]] = []
            sparse_indices: List[List[int]] = []
            payloads = []

            if self.enable_hybrid and self._sparse_doc_fn is not None:
                sparse_indices, sparse_vectors = self._sparse_doc_fn(
                    [
                        node.get_content(metadata_mode=MetadataMode.EMBED)
                        for node in node_batch
                    ],
                )

            for i, node in enumerate(node_batch):
                assert isinstance(node, BaseNode)
                node_ids.append(node.node_id)

                if self.enable_hybrid:
                    if (
                        len(sparse_vectors)  0
                        and len(sparse_indices)  0
                        and len(sparse_vectors) == len(sparse_indices)
                    ):
                        vectors.append(
                            {
                                # Dynamically switch between the old and new sparse vector name
                                sparse_vector_name: rest.SparseVector(
                                    indices=sparse_indices[i],
                                    values=sparse_vectors[i],
                                ),
                                self.dense_vector_name: node.get_embedding(),
                            }
                        )
                    else:
                        vectors.append(
                            {
                                self.dense_vector_name: node.get_embedding(),
                            }
                        )
                else:
                    vectors.append({self.dense_vector_name: node.get_embedding()})

                metadata = node_to_metadata_dict(
                    node, remove_text=False, flat_metadata=self.flat_metadata
                )

                payloads.append(metadata)

            points.extend(
                [
                    rest.PointStruct(id=node_id, payload=payload, vector=vector)
                    for node_id, payload, vector in zip(node_ids, payloads, vectors)
                ]
            )

            ids.extend(node_ids)

        return points, ids

    def_ensure_async_client(self) -> None:
        if self._aclient is None:
            raise ValueError(
                "Async client is not initialized!\nPlease pass in `aclient` to the constructor: "
                "`QdrantVectorStore(..., aclient=AsyncQdrantClient(...))`"
            )

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        limit: Optional[int] = None,
        shard_identifier: Optional[Any] = None,
    ) -> List[BaseNode]:
"""
        Get nodes from the index.

        Args:
            node_ids (Optional[List[str]]): List of node IDs to retrieve.
            filters (Optional[MetadataFilters]): Metadata filters to apply.
            limit (Optional[int]): Maximum number of nodes to retrieve.
            shard_identifier (Optional[Any]): Shard identifier for the query.

        Returns:
            List[BaseNode]: List of nodes retrieved from the index.

        """
        should = []
        if node_ids is not None:
            should = [
                HasIdCondition(
                    has_id=node_ids,
                )
            ]
            # If we pass a node_ids list,
            # we can limit the search to only those nodes
            # or less if limit is provided
            limit = len(node_ids) if limit is None else min(len(node_ids), limit)

        if filters is not None:
            filter = self._build_subfilter(filters)
            if filter.should is None:
                filter.should = should
            else:
                filter.should.extend(should)
        else:
            filter = Filter(should=should)

        # If we pass an empty list, Qdrant will not return any results
        filter.must = filter.must if filter.must and len(filter.must)  0 else None
        filter.should = (
            filter.should if filter.should and len(filter.should)  0 else None
        )
        filter.must_not = (
            filter.must_not if filter.must_not and len(filter.must_not)  0 else None
        )

        shard_key_selector = (
            self._generate_shard_key_selector(shard_identifier)
            if shard_identifier is not None
            else None
        )

        response = self._client.scroll(
            collection_name=self.collection_name,
            limit=limit or 9999,
            scroll_filter=filter,
            with_vectors=True,
            shard_key_selector=shard_key_selector,
        )

        return self.parse_to_query_result(response[0]).nodes

    async defaget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        limit: Optional[int] = None,
        shard_identifier: Optional[Any] = None,
    ) -> List[BaseNode]:
"""
        Asynchronous method to get nodes from the index.

        Args:
            node_ids (Optional[List[str]]): List of node IDs to retrieve.
            filters (Optional[MetadataFilters]): Metadata filters to apply.
            limit (Optional[int]): Maximum number of nodes to retrieve.
            shard_identifier (Optional[Any]): Shard identifier for the query.

        Returns:
            List[BaseNode]: List of nodes retrieved from the index.

        """
        self._ensure_async_client()

        should = []
        if node_ids is not None:
            should = [
                HasIdCondition(
                    has_id=node_ids,
                )
            ]
            # If we pass a node_ids list,
            # we can limit the search to only those nodes
            # or less if limit is provided
            limit = len(node_ids) if limit is None else min(len(node_ids), limit)

        if filters is not None:
            filter = self._build_subfilter(filters)
            if filter.should is None:
                filter.should = should
            else:
                filter.should.extend(should)
        else:
            filter = Filter(should=should)

        shard_key_selector = (
            self._generate_shard_key_selector(shard_identifier)
            if shard_identifier is not None
            else None
        )

        response = await self._aclient.scroll(
            collection_name=self.collection_name,
            limit=limit or 9999,
            scroll_filter=filter,
            with_vectors=True,
            shard_key_selector=shard_key_selector,
        )

        return self.parse_to_query_result(response[0]).nodes

    defadd(
        self,
        nodes: List[BaseNode],
        shard_identifier: Optional[Any] = None,
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings
            shard_identifier (Optional[Any]): Shard identifier for the nodes

        """
        if len(nodes)  0 and not self._collection_initialized:
            self._create_collection(
                collection_name=self.collection_name,
                vector_size=len(nodes[0].get_embedding()),
            )

        if self._collection_initialized and self._legacy_vector_format is None:
            self._detect_vector_format(self.collection_name)

        points, ids = self._build_points(nodes, self.sparse_vector_name)

        shard_key_selector = (
            self._generate_shard_key_selector(shard_identifier)
            if shard_identifier is not None
            else None
        )

        self._client.upload_points(
            collection_name=self.collection_name,
            points=points,
            batch_size=self.batch_size,
            parallel=self.parallel,
            max_retries=self.max_retries,
            wait=True,
            shard_key_selector=shard_key_selector,
        )

        return ids

    async defasync_add(
        self,
        nodes: List[BaseNode],
        shard_identifier: Optional[Any] = None,
        **kwargs: Any,
    ) -> List[str]:
"""
        Asynchronous method to add nodes to Qdrant index.

        Args:
            nodes: List[BaseNode]: List of nodes with embeddings.
            shard_identifier: Optional[Any]: Shard identifier for the nodes.

        Returns:
            List of node IDs that were added to the index.

        Raises:
            ValueError: If trying to using async methods without aclient

        """
        self._ensure_async_client()

        collection_initialized = await self._acollection_exists(self.collection_name)

        if len(nodes)  0 and not collection_initialized:
            await self._acreate_collection(
                collection_name=self.collection_name,
                vector_size=len(nodes[0].get_embedding()),
            )
            collection_initialized = True

        if collection_initialized and self._legacy_vector_format is None:
            # If collection exists but we haven't detected the vector format yet
            await self._adetect_vector_format(self.collection_name)

        points, ids = self._build_points(nodes, self.sparse_vector_name)

        shard_key_selector = (
            self._generate_shard_key_selector(shard_identifier)
            if shard_identifier is not None
            else None
        )

        for batch in iter_batch(points, self.batch_size):
            retries = 0
            while retries  self.max_retries:
                try:
                    await self._aclient.upsert(
                        collection_name=self.collection_name,
                        points=batch,
                        shard_key_selector=shard_key_selector,
                    )
                    break
                except (RpcError, UnexpectedResponse) as exc:
                    retries += 1
                    if retries >= self.max_retries:
                        raise exc  # noqa: TRY201

        return ids

    defdelete(
        self,
        ref_doc_id: str,
        shard_identifier: Optional[Any] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.
            shard_identifier (Optional[Any]): Shard identifier for the nodes.

        """
        shard_key_selector = (
            self._generate_shard_key_selector(shard_identifier)
            if shard_identifier is not None
            else None
        )
        self._client.delete(
            collection_name=self.collection_name,
            points_selector=rest.Filter(
                must=[
                    rest.FieldCondition(
                        key=DOCUMENT_ID_KEY,
                        match=rest.MatchValue(value=ref_doc_id),
                    )
                ]
            ),
            shard_key_selector=shard_key_selector,
        )

    async defadelete(
        self,
        ref_doc_id: str,
        shard_identifier: Optional[Any] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Asynchronous method to delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.
            shard_identifier (Optional[Any]): Shard identifier for the nodes.

        """
        self._ensure_async_client()

        shard_key_selector = (
            self._generate_shard_key_selector(shard_identifier)
            if shard_identifier is not None
            else None
        )

        await self._aclient.delete(
            collection_name=self.collection_name,
            points_selector=rest.Filter(
                must=[
                    rest.FieldCondition(
                        key=DOCUMENT_ID_KEY,
                        match=rest.MatchValue(value=ref_doc_id),
                    )
                ]
            ),
            shard_key_selector=shard_key_selector,
        )

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        shard_identifier: Optional[Any] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete nodes using with node_ids.

        Args:
            node_ids (Optional[List[str]): List of node IDs to delete.
            filters (Optional[MetadataFilters]): Metadata filters to apply.
            shard_identifier (Optional[Any]): Shard identifier for the nodes.

        """
        should = []
        if node_ids is not None:
            should = [
                HasIdCondition(
                    has_id=node_ids,
                )
            ]

        if filters is not None:
            filter = self._build_subfilter(filters)
            if filter.should is None:
                filter.should = should
            else:
                filter.should.extend(should)
        else:
            filter = Filter(should=should)

        shard_key_selector = (
            self._generate_shard_key_selector(shard_identifier)
            if shard_identifier is not None
            else None
        )

        self._client.delete(
            collection_name=self.collection_name,
            points_selector=filter,
            shard_key_selector=shard_key_selector,
        )

    async defadelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        shard_identifier: Optional[Any] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Asynchronous method to delete nodes using with node_ids.

        Args:
            node_ids (Optional[List[str]): List of node IDs to delete.
            filters (Optional[MetadataFilters]): Metadata filters to apply.
            shard_identifier (Optional[Any]): Shard identifier for the nodes.

        """
        self._ensure_async_client()

        should = []
        if node_ids is not None:
            should = [
                HasIdCondition(
                    has_id=node_ids,
                )
            ]

        if filters is not None:
            filter = self._build_subfilter(filters)
            if filter.should is None:
                filter.should = should
            else:
                filter.should.extend(should)
        else:
            filter = Filter(should=should)

        shard_key_selector = (
            self._generate_shard_key_selector(shard_identifier)
            if shard_identifier is not None
            else None
        )

        await self._aclient.delete(
            collection_name=self.collection_name,
            points_selector=filter,
            shard_key_selector=shard_key_selector,
        )

    defclear(self) -> None:
"""
        Clear the index.
        """
        self._client.delete_collection(collection_name=self.collection_name)
        self._collection_initialized = False

    async defaclear(self) -> None:
"""
        Asynchronous method to clear the index.
        """
        self._ensure_async_client()

        await self._aclient.delete_collection(collection_name=self.collection_name)
        self._collection_initialized = False

    @property
    defclient(self) -> Any:
"""Return the Qdrant client."""
        return self._client

    def_create_collection(self, collection_name: str, vector_size: int) -> None:
"""Create a Qdrant collection."""
        dense_config = self._dense_config or rest.VectorParams(
            size=vector_size,
            distance=rest.Distance.COSINE,
        )

        sparse_config = self._sparse_config or rest.SparseVectorParams(
            index=rest.SparseIndexParams(),
            modifier=(
                rest.Modifier.IDF
                if self.fastembed_sparse_model in IDF_EMBEDDING_MODELS
                else None
            ),
        )

        try:
            if self.enable_hybrid:
                self._client.create_collection(
                    collection_name=collection_name,
                    vectors_config={
                        self.dense_vector_name: dense_config,
                    },
                    # Newly created collection will have the new sparse vector name
                    sparse_vectors_config={self.sparse_vector_name: sparse_config},
                    quantization_config=self._quantization_config,
                    shard_number=self._shard_number,
                    replication_factor=self._replication_factor,
                    sharding_method=self._sharding_method,
                    write_consistency_factor=self._write_consistency_factor,
                )
            else:
                self._client.create_collection(
                    collection_name=collection_name,
                    vectors_config=dense_config,
                    quantization_config=self._quantization_config,
                    shard_number=self._shard_number,
                    replication_factor=self._replication_factor,
                    sharding_method=self._sharding_method,
                    write_consistency_factor=self._write_consistency_factor,
                )

            if self._shard_keys:
                self._create_shard_keys()

            # To improve search performance Qdrant recommends setting up
            # a payload index for fields used in filters.
            # https://qdrant.tech/documentation/concepts/indexing
            if self.index_doc_id:
                self._client.create_payload_index(
                    collection_name=collection_name,
                    field_name=DOCUMENT_ID_KEY,
                    field_schema=rest.PayloadSchemaType.KEYWORD,
                )

            if self._payload_indexes:
                self._create_payload_indexes()
        except (RpcError, ValueError, UnexpectedResponse) as exc:
            if "already exists" not in str(exc):
                raise exc  # noqa: TRY201
            logger.warning(
                "Collection %s already exists, skipping collection creation.",
                collection_name,
            )

            if self._shard_keys:
                self._create_shard_keys()

            if self._payload_indexes:
                self._create_payload_indexes()

        self._collection_initialized = True

    async def_acreate_collection(self, collection_name: str, vector_size: int) -> None:
"""Asynchronous method to create a Qdrant collection."""
        dense_config = self._dense_config or rest.VectorParams(
            size=vector_size,
            distance=rest.Distance.COSINE,
        )

        sparse_config = self._sparse_config or rest.SparseVectorParams(
            index=rest.SparseIndexParams(),
            modifier=(
                rest.Modifier.IDF
                if self.fastembed_sparse_model in IDF_EMBEDDING_MODELS
                else None
            ),
        )

        try:
            if self.enable_hybrid:
                await self._aclient.create_collection(
                    collection_name=collection_name,
                    vectors_config={self.dense_vector_name: dense_config},
                    sparse_vectors_config={self.sparse_vector_name: sparse_config},
                    quantization_config=self._quantization_config,
                    shard_number=self._shard_number,
                    replication_factor=self._replication_factor,
                    sharding_method=self._sharding_method,
                    write_consistency_factor=self._write_consistency_factor,
                )
            else:
                await self._aclient.create_collection(
                    collection_name=collection_name,
                    vectors_config=dense_config,
                    quantization_config=self._quantization_config,
                    shard_number=self._shard_number,
                    replication_factor=self._replication_factor,
                    sharding_method=self._sharding_method,
                    write_consistency_factor=self._write_consistency_factor,
                )

            if self._shard_keys:
                await self._acreate_shard_keys()

            # To improve search performance Qdrant recommends setting up
            # a payload index for fields used in filters.
            # https://qdrant.tech/documentation/concepts/indexing
            if self.index_doc_id:
                await self._aclient.create_payload_index(
                    collection_name=collection_name,
                    field_name=DOCUMENT_ID_KEY,
                    field_schema=rest.PayloadSchemaType.KEYWORD,
                )

            if self._payload_indexes:
                await self._acreate_payload_indexes()
        except (RpcError, ValueError, UnexpectedResponse) as exc:
            if "already exists" not in str(exc):
                raise exc  # noqa: TRY201
            logger.warning(
                "Collection %s already exists, skipping collection creation.",
                collection_name,
            )

            if self._shard_keys:
                await self._acreate_shard_keys()

            if self._payload_indexes:
                await self._acreate_payload_indexes()

        self._collection_initialized = True

    def_collection_exists(self, collection_name: str) -> bool:
"""Check if a collection exists."""
        return self._client.collection_exists(collection_name)

    async def_acollection_exists(self, collection_name: str) -> bool:
"""Asynchronous method to check if a collection exists."""
        return await self._aclient.collection_exists(collection_name)

    def_create_shard_keys(self) -> None:
"""Create shard keys in Qdrant collection."""
        if not self._shard_keys:
            return

        for shard_key in self._shard_keys:
            try:
                self._client.create_shard_key(
                    collection_name=self.collection_name,
                    shard_key=shard_key,
                )
            except (RpcError, ValueError, UnexpectedResponse) as exc:
                if "already exists" not in str(exc):
                    raise exc  # noqa: TRY201
                logger.warning(
                    "Shard key %s already exists, skipping creation.",
                    shard_key,
                )
                continue

    async def_acreate_shard_keys(self) -> None:
"""Asynchronous method to create shard keys in Qdrant collection."""
        if not self._shard_keys:
            return

        for shard_key in self._shard_keys:
            try:
                await self._aclient.create_shard_key(
                    collection_name=self.collection_name,
                    shard_key=shard_key,
                )
            except (RpcError, ValueError, UnexpectedResponse) as exc:
                if "already exists" not in str(exc):
                    raise exc  # noqa: TRY201
                logger.warning(
                    "Shard key %s already exists, skipping creation.",
                    shard_key,
                )
                continue

    def_create_payload_indexes(self) -> None:
"""Create payload indexes in Qdrant collection."""
        if not self._payload_indexes:
            return
        for payload_index in self._payload_indexes:
            self._client.create_payload_index(
                collection_name=self.collection_name,
                field_name=payload_index["field_name"],
                field_schema=payload_index["field_schema"],
            )

    async def_acreate_payload_indexes(self) -> None:
"""Create payload indexes in Qdrant collection."""
        if not self._payload_indexes:
            return
        for payload_index in self._payload_indexes:
            await self._aclient.create_payload_index(
                collection_name=self.collection_name,
                field_name=payload_index["field_name"],
                field_schema=payload_index["field_schema"],
            )

    defquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): query

        """
        query_embedding = cast(List[float], query.query_embedding)
        #  NOTE: users can pass in qdrant_filters (nested/complicated filters) to override the default MetadataFilters
        qdrant_filters = kwargs.get("qdrant_filters")
        if qdrant_filters is not None:
            query_filter = qdrant_filters
        else:
            query_filter = cast(Filter, self._build_query_filter(query))

        shard_identifier = kwargs.get("shard_identifier")
        shard_key = (
            self._generate_shard_key_selector(shard_identifier)
            if shard_identifier is not None
            else None
        )

        search_params = kwargs.get("search_params")
        if search_params is not None and isinstance(search_params, dict):
            search_params = rest.SearchParams(**search_params)
        search_params = cast(Optional[rest.SearchParams], search_params)

        if query.mode == VectorStoreQueryMode.HYBRID and not self.enable_hybrid:
            raise ValueError(
                "Hybrid search is not enabled. Please build the query with "
                "`enable_hybrid=True` in the constructor."
            )
        elif (
            query.mode == VectorStoreQueryMode.HYBRID
            and self.enable_hybrid
            and self._sparse_query_fn is not None
            and query.query_str is not None
        ):
            sparse_indices, sparse_embedding = self._sparse_query_fn(
                [query.query_str],
            )
            sparse_top_k = query.sparse_top_k or query.similarity_top_k

            sparse_response = self._client.query_batch_points(
                collection_name=self.collection_name,
                requests=[
                    rest.QueryRequest(
                        query=query_embedding,
                        using=self.dense_vector_name,
                        limit=query.similarity_top_k,
                        filter=query_filter,
                        with_payload=True,
                        shard_key=shard_key,
                        params=search_params,
                    ),
                    rest.QueryRequest(
                        query=rest.SparseVector(
                            indices=sparse_indices[0],
                            values=sparse_embedding[0],
                        ),
                        using=self.sparse_vector_name,
                        limit=sparse_top_k,
                        filter=query_filter,
                        with_payload=True,
                        shard_key=shard_key,
                        params=search_params,
                    ),
                ],
            )

            # sanity check
            assert len(sparse_response) == 2
            assert self._hybrid_fusion_fn is not None

            # flatten the response
            return self._hybrid_fusion_fn(
                self.parse_to_query_result(sparse_response[0].points),
                self.parse_to_query_result(sparse_response[1].points),
                # NOTE: only for hybrid search (0 for sparse search, 1 for dense search)
                alpha=query.alpha if query.alpha is not None else 0.5,
                # NOTE: use hybrid_top_k if provided, otherwise use similarity_top_k
                top_k=query.hybrid_top_k or query.similarity_top_k,
            )
        elif (
            query.mode == VectorStoreQueryMode.SPARSE
            and self.enable_hybrid
            and self._sparse_query_fn is not None
            and query.query_str is not None
        ):
            sparse_indices, sparse_embedding = self._sparse_query_fn(
                [query.query_str],
            )
            sparse_top_k = query.sparse_top_k or query.similarity_top_k

            sparse_response = self._client.query_batch_points(
                collection_name=self.collection_name,
                requests=[
                    rest.QueryRequest(
                        query=rest.SparseVector(
                            indices=sparse_indices[0],
                            values=sparse_embedding[0],
                        ),
                        using=self.sparse_vector_name,
                        limit=sparse_top_k,
                        filter=query_filter,
                        with_payload=True,
                        shard_key=shard_key,
                        params=search_params,
                    ),
                ],
            )

            return self.parse_to_query_result(sparse_response[0].points)
        elif self.enable_hybrid:
            # search for dense vectors only
            response = self._client.query_batch_points(
                collection_name=self.collection_name,
                requests=[
                    rest.QueryRequest(
                        query=query_embedding,
                        using=self.dense_vector_name,
                        limit=query.similarity_top_k,
                        filter=query_filter,
                        with_payload=True,
                        shard_key=shard_key,
                        params=search_params,
                    ),
                ],
            )

            return self.parse_to_query_result(response[0].points)
        else:
            # Regular non-hybrid search
            response = self._client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                using=self.dense_vector_name,
                limit=query.similarity_top_k,
                query_filter=query_filter,
                shard_key_selector=shard_key,
                search_params=search_params,
            )
            return self.parse_to_query_result(response.points)

    async defaquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Asynchronous method to query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): query

        """
        self._ensure_async_client()

        query_embedding = cast(List[float], query.query_embedding)

        #  NOTE: users can pass in qdrant_filters (nested/complicated filters) to override the default MetadataFilters
        qdrant_filters = kwargs.get("qdrant_filters")
        if qdrant_filters is not None:
            query_filter = qdrant_filters
        else:
            # build metadata filters
            query_filter = cast(Filter, self._build_query_filter(query))

        # Check if we need to detect vector format
        if self._legacy_vector_format is None:
            await self._adetect_vector_format(self.collection_name)

        # Get shard_identifier if provided
        shard_identifier = kwargs.get("shard_identifier")
        shard_key = (
            self._generate_shard_key_selector(shard_identifier)
            if shard_identifier
            else None
        )

        search_params = kwargs.get("search_params")
        if search_params is not None and isinstance(search_params, dict):
            search_params = rest.SearchParams(**search_params)
        search_params = cast(Optional[rest.SearchParams], search_params)

        if query.mode == VectorStoreQueryMode.HYBRID and not self.enable_hybrid:
            raise ValueError(
                "Hybrid search is not enabled. Please build the query with "
                "`enable_hybrid=True` in the constructor."
            )
        elif (
            query.mode == VectorStoreQueryMode.HYBRID
            and self.enable_hybrid
            and self._sparse_query_fn is not None
            and query.query_str is not None
        ):
            sparse_indices, sparse_embedding = self._sparse_query_fn(
                [query.query_str],
            )
            sparse_top_k = query.sparse_top_k or query.similarity_top_k

            sparse_response = await self._aclient.query_batch_points(
                collection_name=self.collection_name,
                requests=[
                    rest.QueryRequest(
                        query=query_embedding,
                        using=self.dense_vector_name,
                        limit=query.similarity_top_k,
                        filter=query_filter,
                        with_payload=True,
                        shard_key=shard_key,
                        params=search_params,
                    ),
                    rest.QueryRequest(
                        query=rest.SparseVector(
                            indices=sparse_indices[0],
                            values=sparse_embedding[0],
                        ),
                        using=self.sparse_vector_name,
                        limit=sparse_top_k,
                        filter=query_filter,
                        with_payload=True,
                        shard_key=shard_key,
                        params=search_params,
                    ),
                ],
            )

            # sanity check
            assert len(sparse_response) == 2
            assert self._hybrid_fusion_fn is not None

            # flatten the response
            return self._hybrid_fusion_fn(
                self.parse_to_query_result(sparse_response[0].points),
                self.parse_to_query_result(sparse_response[1].points),
                alpha=query.alpha or 0.5,
                # NOTE: use hybrid_top_k if provided, otherwise use similarity_top_k
                top_k=query.hybrid_top_k or query.similarity_top_k,
            )
        elif (
            query.mode == VectorStoreQueryMode.SPARSE
            and self.enable_hybrid
            and self._sparse_query_fn is not None
            and query.query_str is not None
        ):
            sparse_indices, sparse_embedding = self._sparse_query_fn(
                [query.query_str],
            )
            sparse_top_k = query.sparse_top_k or query.similarity_top_k

            sparse_response = await self._aclient.query_batch_points(
                collection_name=self.collection_name,
                requests=[
                    rest.QueryRequest(
                        query=rest.SparseVector(
                            indices=sparse_indices[0],
                            values=sparse_embedding[0],
                        ),
                        using=self.sparse_vector_name,
                        limit=sparse_top_k,
                        filter=query_filter,
                        with_payload=True,
                        shard_key=shard_key,
                        params=search_params,
                    ),
                ],
            )
            return self.parse_to_query_result(sparse_response[0].points)
        elif self.enable_hybrid:
            # search for dense vectors only
            response = await self._aclient.query_batch_points(
                collection_name=self.collection_name,
                requests=[
                    rest.QueryRequest(
                        query=query_embedding,
                        using=self.dense_vector_name,
                        limit=query.similarity_top_k,
                        filter=query_filter,
                        with_payload=True,
                        shard_key=shard_key,
                        params=search_params,
                    ),
                ],
            )

            return self.parse_to_query_result(response[0].points)
        else:
            response = await self._aclient.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                using=self.dense_vector_name,
                limit=query.similarity_top_k,
                query_filter=query_filter,
                shard_key_selector=shard_key,
                search_params=search_params,
            )

            return self.parse_to_query_result(response.points)

    defparse_to_query_result(self, response: List[Any]) -> VectorStoreQueryResult:
"""
        Convert vector store response to VectorStoreQueryResult.

        Args:
            response: List[Any]: List of results returned from the vector store.

        """
        nodes = []
        similarities = []
        ids = []

        for point in response:
            payload = cast(Payload, point.payload)
            vector = point.vector
            embedding = None

            if isinstance(vector, dict):
                embedding = vector.get(self.dense_vector_name, vector.get("", None))
            elif isinstance(vector, list):
                embedding = vector

            try:
                node = metadata_dict_to_node(payload)

                if embedding and node.embedding is None:
                    node.embedding = embedding
            except Exception:
                metadata, node_info, relationships = legacy_metadata_dict_to_node(
                    payload
                )

                node = TextNode(
                    id_=str(point.id),
                    text=payload.get(self.text_key),
                    metadata=metadata,
                    start_char_idx=node_info.get("start", None),
                    end_char_idx=node_info.get("end", None),
                    relationships=relationships,
                    embedding=embedding,
                )
            nodes.append(node)
            ids.append(str(point.id))
            try:
                similarities.append(point.score)
            except AttributeError:
                # certain requests do not return a score
                similarities.append(1.0)

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    def_build_subfilter(self, filters: MetadataFilters) -> Filter:
        conditions = []
        for subfilter in filters.filters:
            # Handle nested MetadataFilters
            if isinstance(subfilter, MetadataFilters):
                if len(subfilter.filters)  0:
                    conditions.append(self._build_subfilter(subfilter))
                # Skip empty MetadataFilters
                continue

            # Handle MetadataFilter with operators
            if not subfilter.operator or subfilter.operator == FilterOperator.EQ:
                if isinstance(subfilter.value, float):
                    conditions.append(
                        FieldCondition(
                            key=subfilter.key,
                            range=Range(
                                gte=subfilter.value,
                                lte=subfilter.value,
                            ),
                        )
                    )
                else:
                    conditions.append(
                        FieldCondition(
                            key=subfilter.key,
                            match=MatchValue(value=subfilter.value),
                        )
                    )
            elif subfilter.operator == FilterOperator.LT:
                conditions.append(
                    FieldCondition(
                        key=subfilter.key,
                        range=Range(lt=subfilter.value),
                    )
                )
            elif subfilter.operator == FilterOperator.GT:
                conditions.append(
                    FieldCondition(
                        key=subfilter.key,
                        range=Range(gt=subfilter.value),
                    )
                )
            elif subfilter.operator == FilterOperator.GTE:
                conditions.append(
                    FieldCondition(
                        key=subfilter.key,
                        range=Range(gte=subfilter.value),
                    )
                )
            elif subfilter.operator == FilterOperator.LTE:
                conditions.append(
                    FieldCondition(
                        key=subfilter.key,
                        range=Range(lte=subfilter.value),
                    )
                )
            elif (
                subfilter.operator == FilterOperator.TEXT_MATCH
                or subfilter.operator == FilterOperator.TEXT_MATCH_INSENSITIVE
            ):
                conditions.append(
                    FieldCondition(
                        key=subfilter.key,
                        match=MatchText(text=subfilter.value),
                    )
                )
            elif subfilter.operator == FilterOperator.NE:
                conditions.append(
                    FieldCondition(
                        key=subfilter.key,
                        match=MatchExcept(**{"except": [subfilter.value]}),
                    )
                )
            elif subfilter.operator == FilterOperator.IN:
                # match any of the values
                # https://qdrant.tech/documentation/concepts/filtering/#match-any
                if isinstance(subfilter.value, List):
                    values = subfilter.value
                else:
                    values = str(subfilter.value).split(",")

                conditions.append(
                    FieldCondition(
                        key=subfilter.key,
                        match=MatchAny(any=values),
                    )
                )
            elif subfilter.operator == FilterOperator.NIN:
                # match none of the values
                # https://qdrant.tech/documentation/concepts/filtering/#match-except
                if isinstance(subfilter.value, List):
                    values = subfilter.value
                else:
                    values = str(subfilter.value).split(",")
                conditions.append(
                    FieldCondition(
                        key=subfilter.key,
                        match=MatchExcept(**{"except": values}),
                    )
                )
            elif subfilter.operator == FilterOperator.IS_EMPTY:
                # This condition will match all records where the field reports either does not exist, or has null or [] value.
                # https://qdrant.tech/documentation/concepts/filtering/#is-empty
                conditions.append(
                    IsEmptyCondition(is_empty=PayloadField(key=subfilter.key))
                )
            else:
                # Unsupported filter operator
                raise NotImplementedError(
                    f"Filter operator {subfilter.operator} is not supported by Qdrant vector store. "
                    f"Supported operators: EQ, NE, GT, GTE, LT, LTE, IN, NIN, TEXT_MATCH, "
                    f"TEXT_MATCH_INSENSITIVE, IS_EMPTY"
                )

        filter = Filter()
        if filters.condition == FilterCondition.AND:
            filter.must = conditions
        elif filters.condition == FilterCondition.OR:
            filter.should = conditions
        elif filters.condition == FilterCondition.NOT:
            filter.must_not = conditions
        return filter

    def_build_query_filter(self, query: VectorStoreQuery) -> Optional[Any]:
        must_conditions = []

        if query.doc_ids:
            must_conditions.append(
                FieldCondition(
                    key=DOCUMENT_ID_KEY,
                    match=MatchAny(any=query.doc_ids),
                )
            )

        # Point id is a "service" id, it is not stored in payload. There is 'HasId' condition to filter by point id
        # https://qdrant.tech/documentation/concepts/filtering/#has-id
        if query.node_ids:
            must_conditions.append(
                HasIdCondition(has_id=query.node_ids),
            )

        # Qdrant does not use the query.query_str property for the filtering. Full-text
        # filtering cannot handle longer queries and can effectively filter our all the
        # nodes. See: https://github.com/jerryjliu/llama_index/pull/1181

        if query.filters and query.filters.filters:
            must_conditions.append(self._build_subfilter(query.filters))

        if len(must_conditions) == 0:
            return None

        return Filter(must=must_conditions)

    defuse_old_sparse_encoder(self, collection_name: str) -> bool:
"""
        Check if the collection uses the old sparse encoder format.
        This is used during initialization to determine which sparse vector name to use.
        """
        collection_exists = self._collection_exists(collection_name)
        if collection_exists:
            cur_collection = self.client.get_collection(collection_name)
            return DEFAULT_SPARSE_VECTOR_NAME_OLD in (
                cur_collection.config.params.sparse_vectors or {}
            )

        return False

    async defause_old_sparse_encoder(self, collection_name: str) -> bool:
"""
        Asynchronous method to check if the collection uses the old sparse encoder format.
        """
        collection_exists = await self._acollection_exists(collection_name)
        if collection_exists:
            cur_collection = await self._aclient.get_collection(collection_name)
            return DEFAULT_SPARSE_VECTOR_NAME_OLD in (
                cur_collection.config.params.sparse_vectors or {}
            )

        return False

    defget_default_sparse_doc_encoder(
        self,
        collection_name: str,
        fastembed_sparse_model: Optional[str] = None,
    ) -> SparseEncoderCallable:
"""
        Get the default sparse document encoder.
        For async-only clients, assumes new format initially.
        Will be auto-corrected on first async operation if collection uses old format.
        """
        if self._client is not None:
            if self.use_old_sparse_encoder(collection_name):
                self.sparse_vector_name = DEFAULT_SPARSE_VECTOR_NAME_OLD
                return default_sparse_encoder("naver/efficient-splade-VI-BT-large-doc")

        if fastembed_sparse_model is not None:
            return fastembed_sparse_encoder(model_name=fastembed_sparse_model)

        return fastembed_sparse_encoder()

    defget_default_sparse_query_encoder(
        self,
        collection_name: str,
        fastembed_sparse_model: Optional[str] = None,
    ) -> SparseEncoderCallable:
"""
        Get the default sparse query encoder.
        For async-only clients, assumes new format initially.
        Will be auto-corrected on first async operation if collection uses old format.
        """
        if self._client is not None:
            if self.use_old_sparse_encoder(collection_name):
                # Update the sparse vector name to use the old format
                self.sparse_vector_name = DEFAULT_SPARSE_VECTOR_NAME_OLD
                return default_sparse_encoder(
                    "naver/efficient-splade-VI-BT-large-query"
                )

        if fastembed_sparse_model is not None:
            return fastembed_sparse_encoder(model_name=fastembed_sparse_model)

        return fastembed_sparse_encoder()

    def_detect_vector_format(self, collection_name: str) -> None:
"""
        Detect and handle old vector formats from existing collections.
        - named vs non-named vectors
        - new sparse vector field name vs old sparse vector field name
        """
        try:
            old_sparse_name = self.sparse_vector_name  # Store state before detection

            collection_info = self._client.get_collection(collection_name)
            vectors_config = collection_info.config.params.vectors
            sparse_vectors = collection_info.config.params.sparse_vectors or {}

            # Check if we have an unnamed vector format (where name is empty string)
            if isinstance(vectors_config, dict):
                # Using named vectors format
                if LEGACY_UNNAMED_VECTOR in vectors_config:
                    self._legacy_vector_format = True
                    self.dense_vector_name = LEGACY_UNNAMED_VECTOR
            else:
                # Using unnamed vector format from earlier versions
                self._legacy_vector_format = True
                self.dense_vector_name = LEGACY_UNNAMED_VECTOR

            # Detect sparse vector name if any sparse vectors configured
            if isinstance(sparse_vectors, dict) and len(sparse_vectors)  0:
                if self.sparse_vector_name in sparse_vectors:
                    pass
                elif DEFAULT_SPARSE_VECTOR_NAME_OLD in sparse_vectors:
                    self.sparse_vector_name = DEFAULT_SPARSE_VECTOR_NAME_OLD

            # If the name changed, our initial assumption was wrong. Correct it.
            if self.enable_hybrid and old_sparse_name != self.sparse_vector_name:
                self._reinitialize_sparse_encoders()

        except Exception as e:
            logger.warning(
                f"Could not detect vector format for collection {collection_name}: {e}"
            )

    async def_adetect_vector_format(self, collection_name: str) -> None:
"""
        Asynchronous method to detect and handle old vector formats from existing collections.
        """
        try:
            old_sparse_name = self.sparse_vector_name  # Store state before detection

            collection_info = await self._aclient.get_collection(collection_name)
            vectors_config = collection_info.config.params.vectors
            sparse_vectors = collection_info.config.params.sparse_vectors or {}

            # Check if we have an unnamed vector format (where name is empty string)
            if isinstance(vectors_config, dict):
                # Using named vectors format
                if LEGACY_UNNAMED_VECTOR in vectors_config:
                    self._legacy_vector_format = True
                    self.dense_vector_name = LEGACY_UNNAMED_VECTOR
            else:
                # Using unnamed vector format from earlier versions
                self._legacy_vector_format = True
                self.dense_vector_name = LEGACY_UNNAMED_VECTOR

            # Detect sparse vector name and correct if necessary
            if isinstance(sparse_vectors, dict) and len(sparse_vectors)  0:
                if self.sparse_vector_name in sparse_vectors:
                    pass
                elif DEFAULT_SPARSE_VECTOR_NAME_OLD in sparse_vectors:
                    self.sparse_vector_name = DEFAULT_SPARSE_VECTOR_NAME_OLD

            # If the name changed, our initial assumption was wrong. Correct it.
            if self.enable_hybrid and old_sparse_name != self.sparse_vector_name:
                self._reinitialize_sparse_encoders()

        except Exception as e:
            logger.warning(
                f"Could not detect vector format for collection {collection_name}: {e}"
            )

    def_reinitialize_sparse_encoders(self) -> None:
"""Recreate default sparse encoders after vector format detection, respecting user-provided functions."""
        if not self.enable_hybrid:
            return

        # Only override the doc function if the user did NOT provide one
        if not self._user_provided_sparse_doc_fn:
            if self.sparse_vector_name == DEFAULT_SPARSE_VECTOR_NAME_OLD:
                self._sparse_doc_fn = default_sparse_encoder(
                    "naver/efficient-splade-VI-BT-large-doc"
                )
            else:
                self._sparse_doc_fn = fastembed_sparse_encoder(
                    model_name=self.fastembed_sparse_model
                )

        # Only override the query function if the user did NOT provide one
        if not self._user_provided_sparse_query_fn:
            if self.sparse_vector_name == DEFAULT_SPARSE_VECTOR_NAME_OLD:
                self._sparse_query_fn = default_sparse_encoder(
                    "naver/efficient-splade-VI-BT-large-query"
                )
            else:
                self._sparse_query_fn = fastembed_sparse_encoder(
                    model_name=self.fastembed_sparse_model
                )

    def_validate_custom_sharding(
        self,
    ):
"""
        Validate custom sharding configuration.
        """
        if not self._shard_key_selector_fn:
            raise ValueError(
                "Must provide a shard_key_selector_fn for custom sharding."
            )
        if not self._shard_keys:
            raise ValueError("Must provide shard_keys for custom sharding.")

    def_generate_shard_key_selector(
        self, shard_identifier: Any
    ) -> Union[rest.ShardKeySelector, None]:
"""
        Generate a shard key selector based on the shard identifier.
        """
        if (
            self._shard_key_selector_fn is not None
            and self._sharding_method == rest.ShardingMethod.CUSTOM
        ):
            return self._shard_key_selector_fn(shard_identifier)

        return None

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.client "Permanent link")

```
client: 

```

Return the Qdrant client.
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    limit: Optional[] = None,
    shard_identifier: Optional[] = None,
) -> []

```

Get nodes from the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  List of node IDs to retrieve.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to apply.  |  `None`  |  
|  `limit`  |  `Optional[int]`  |  Maximum number of nodes to retrieve.  |  `None`  |  
|  `shard_identifier`  |  `Optional[Any]`  |  Shard identifier for the query.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[BaseNode]: List of nodes retrieved from the index.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    limit: Optional[int] = None,
    shard_identifier: Optional[Any] = None,
) -> List[BaseNode]:
"""
    Get nodes from the index.

    Args:
        node_ids (Optional[List[str]]): List of node IDs to retrieve.
        filters (Optional[MetadataFilters]): Metadata filters to apply.
        limit (Optional[int]): Maximum number of nodes to retrieve.
        shard_identifier (Optional[Any]): Shard identifier for the query.

    Returns:
        List[BaseNode]: List of nodes retrieved from the index.

    """
    should = []
    if node_ids is not None:
        should = [
            HasIdCondition(
                has_id=node_ids,
            )
        ]
        # If we pass a node_ids list,
        # we can limit the search to only those nodes
        # or less if limit is provided
        limit = len(node_ids) if limit is None else min(len(node_ids), limit)

    if filters is not None:
        filter = self._build_subfilter(filters)
        if filter.should is None:
            filter.should = should
        else:
            filter.should.extend(should)
    else:
        filter = Filter(should=should)

    # If we pass an empty list, Qdrant will not return any results
    filter.must = filter.must if filter.must and len(filter.must)  0 else None
    filter.should = (
        filter.should if filter.should and len(filter.should)  0 else None
    )
    filter.must_not = (
        filter.must_not if filter.must_not and len(filter.must_not)  0 else None
    )

    shard_key_selector = (
        self._generate_shard_key_selector(shard_identifier)
        if shard_identifier is not None
        else None
    )

    response = self._client.scroll(
        collection_name=self.collection_name,
        limit=limit or 9999,
        scroll_filter=filter,
        with_vectors=True,
        shard_key_selector=shard_key_selector,
    )

    return self.parse_to_query_result(response[0]).nodes

```
 |  
| --- | --- |  
###  aget_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.aget_nodes "Permanent link")

```
aget_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    limit: Optional[] = None,
    shard_identifier: Optional[] = None,
) -> []

```

Asynchronous method to get nodes from the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  List of node IDs to retrieve.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to apply.  |  `None`  |  
|  `limit`  |  `Optional[int]`  |  Maximum number of nodes to retrieve.  |  `None`  |  
|  `shard_identifier`  |  `Optional[Any]`  |  Shard identifier for the query.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[BaseNode]: List of nodes retrieved from the index.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
async defaget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    limit: Optional[int] = None,
    shard_identifier: Optional[Any] = None,
) -> List[BaseNode]:
"""
    Asynchronous method to get nodes from the index.

    Args:
        node_ids (Optional[List[str]]): List of node IDs to retrieve.
        filters (Optional[MetadataFilters]): Metadata filters to apply.
        limit (Optional[int]): Maximum number of nodes to retrieve.
        shard_identifier (Optional[Any]): Shard identifier for the query.

    Returns:
        List[BaseNode]: List of nodes retrieved from the index.

    """
    self._ensure_async_client()

    should = []
    if node_ids is not None:
        should = [
            HasIdCondition(
                has_id=node_ids,
            )
        ]
        # If we pass a node_ids list,
        # we can limit the search to only those nodes
        # or less if limit is provided
        limit = len(node_ids) if limit is None else min(len(node_ids), limit)

    if filters is not None:
        filter = self._build_subfilter(filters)
        if filter.should is None:
            filter.should = should
        else:
            filter.should.extend(should)
    else:
        filter = Filter(should=should)

    shard_key_selector = (
        self._generate_shard_key_selector(shard_identifier)
        if shard_identifier is not None
        else None
    )

    response = await self._aclient.scroll(
        collection_name=self.collection_name,
        limit=limit or 9999,
        scroll_filter=filter,
        with_vectors=True,
        shard_key_selector=shard_key_selector,
    )

    return self.parse_to_query_result(response[0]).nodes

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.add "Permanent link")

```
add(
    nodes: [],
    shard_identifier: Optional[] = None,
    **add_kwargs: 
) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
|  `shard_identifier`  |  `Optional[Any]`  |  Shard identifier for the nodes  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    shard_identifier: Optional[Any] = None,
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings
        shard_identifier (Optional[Any]): Shard identifier for the nodes

    """
    if len(nodes)  0 and not self._collection_initialized:
        self._create_collection(
            collection_name=self.collection_name,
            vector_size=len(nodes[0].get_embedding()),
        )

    if self._collection_initialized and self._legacy_vector_format is None:
        self._detect_vector_format(self.collection_name)

    points, ids = self._build_points(nodes, self.sparse_vector_name)

    shard_key_selector = (
        self._generate_shard_key_selector(shard_identifier)
        if shard_identifier is not None
        else None
    )

    self._client.upload_points(
        collection_name=self.collection_name,
        points=points,
        batch_size=self.batch_size,
        parallel=self.parallel,
        max_retries=self.max_retries,
        wait=True,
        shard_key_selector=shard_key_selector,
    )

    return ids

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.async_add "Permanent link")

```
async_add(
    nodes: [],
    shard_identifier: Optional[] = None,
    **kwargs: 
) -> []

```

Asynchronous method to add nodes to Qdrant index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: List of nodes with embeddings.  |  _required_  |  
|  `shard_identifier`  |  `Optional[Any]`  |  Optional[Any]: Shard identifier for the nodes.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List of node IDs that were added to the index.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If trying to using async methods without aclient  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
async defasync_add(
    self,
    nodes: List[BaseNode],
    shard_identifier: Optional[Any] = None,
    **kwargs: Any,
) -> List[str]:
"""
    Asynchronous method to add nodes to Qdrant index.

    Args:
        nodes: List[BaseNode]: List of nodes with embeddings.
        shard_identifier: Optional[Any]: Shard identifier for the nodes.

    Returns:
        List of node IDs that were added to the index.

    Raises:
        ValueError: If trying to using async methods without aclient

    """
    self._ensure_async_client()

    collection_initialized = await self._acollection_exists(self.collection_name)

    if len(nodes)  0 and not collection_initialized:
        await self._acreate_collection(
            collection_name=self.collection_name,
            vector_size=len(nodes[0].get_embedding()),
        )
        collection_initialized = True

    if collection_initialized and self._legacy_vector_format is None:
        # If collection exists but we haven't detected the vector format yet
        await self._adetect_vector_format(self.collection_name)

    points, ids = self._build_points(nodes, self.sparse_vector_name)

    shard_key_selector = (
        self._generate_shard_key_selector(shard_identifier)
        if shard_identifier is not None
        else None
    )

    for batch in iter_batch(points, self.batch_size):
        retries = 0
        while retries  self.max_retries:
            try:
                await self._aclient.upsert(
                    collection_name=self.collection_name,
                    points=batch,
                    shard_key_selector=shard_key_selector,
                )
                break
            except (RpcError, UnexpectedResponse) as exc:
                retries += 1
                if retries >= self.max_retries:
                    raise exc  # noqa: TRY201

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.delete "Permanent link")

```
delete(
    ref_doc_id: ,
    shard_identifier: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
|  `shard_identifier`  |  `Optional[Any]`  |  Shard identifier for the nodes.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
defdelete(
    self,
    ref_doc_id: str,
    shard_identifier: Optional[Any] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.
        shard_identifier (Optional[Any]): Shard identifier for the nodes.

    """
    shard_key_selector = (
        self._generate_shard_key_selector(shard_identifier)
        if shard_identifier is not None
        else None
    )
    self._client.delete(
        collection_name=self.collection_name,
        points_selector=rest.Filter(
            must=[
                rest.FieldCondition(
                    key=DOCUMENT_ID_KEY,
                    match=rest.MatchValue(value=ref_doc_id),
                )
            ]
        ),
        shard_key_selector=shard_key_selector,
    )

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.adelete "Permanent link")

```
adelete(
    ref_doc_id: ,
    shard_identifier: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Asynchronous method to delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
|  `shard_identifier`  |  `Optional[Any]`  |  Shard identifier for the nodes.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
async defadelete(
    self,
    ref_doc_id: str,
    shard_identifier: Optional[Any] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Asynchronous method to delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.
        shard_identifier (Optional[Any]): Shard identifier for the nodes.

    """
    self._ensure_async_client()

    shard_key_selector = (
        self._generate_shard_key_selector(shard_identifier)
        if shard_identifier is not None
        else None
    )

    await self._aclient.delete(
        collection_name=self.collection_name,
        points_selector=rest.Filter(
            must=[
                rest.FieldCondition(
                    key=DOCUMENT_ID_KEY,
                    match=rest.MatchValue(value=ref_doc_id),
                )
            ]
        ),
        shard_key_selector=shard_key_selector,
    )

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    shard_identifier: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes using with node_ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]`  |  List of node IDs to delete.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to apply.  |  `None`  |  
|  `shard_identifier`  |  `Optional[Any]`  |  Shard identifier for the nodes.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    shard_identifier: Optional[Any] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Delete nodes using with node_ids.

    Args:
        node_ids (Optional[List[str]): List of node IDs to delete.
        filters (Optional[MetadataFilters]): Metadata filters to apply.
        shard_identifier (Optional[Any]): Shard identifier for the nodes.

    """
    should = []
    if node_ids is not None:
        should = [
            HasIdCondition(
                has_id=node_ids,
            )
        ]

    if filters is not None:
        filter = self._build_subfilter(filters)
        if filter.should is None:
            filter.should = should
        else:
            filter.should.extend(should)
    else:
        filter = Filter(should=should)

    shard_key_selector = (
        self._generate_shard_key_selector(shard_identifier)
        if shard_identifier is not None
        else None
    )

    self._client.delete(
        collection_name=self.collection_name,
        points_selector=filter,
        shard_key_selector=shard_key_selector,
    )

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    shard_identifier: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Asynchronous method to delete nodes using with node_ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]`  |  List of node IDs to delete.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to apply.  |  `None`  |  
|  `shard_identifier`  |  `Optional[Any]`  |  Shard identifier for the nodes.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    shard_identifier: Optional[Any] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Asynchronous method to delete nodes using with node_ids.

    Args:
        node_ids (Optional[List[str]): List of node IDs to delete.
        filters (Optional[MetadataFilters]): Metadata filters to apply.
        shard_identifier (Optional[Any]): Shard identifier for the nodes.

    """
    self._ensure_async_client()

    should = []
    if node_ids is not None:
        should = [
            HasIdCondition(
                has_id=node_ids,
            )
        ]

    if filters is not None:
        filter = self._build_subfilter(filters)
        if filter.should is None:
            filter.should = should
        else:
            filter.should.extend(should)
    else:
        filter = Filter(should=should)

    shard_key_selector = (
        self._generate_shard_key_selector(shard_identifier)
        if shard_identifier is not None
        else None
    )

    await self._aclient.delete(
        collection_name=self.collection_name,
        points_selector=filter,
        shard_key_selector=shard_key_selector,
    )

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.clear "Permanent link")

```
clear() -> None

```

Clear the index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
782
783
784
785
786
787
```
 | 
```
defclear(self) -> None:
"""
    Clear the index.
    """
    self._client.delete_collection(collection_name=self.collection_name)
    self._collection_initialized = False

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.aclear "Permanent link")

```
aclear() -> None

```

Asynchronous method to clear the index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
789
790
791
792
793
794
795
796
```
 | 
```
async defaclear(self) -> None:
"""
    Asynchronous method to clear the index.
    """
    self._ensure_async_client()

    await self._aclient.delete_collection(collection_name=self.collection_name)
    self._collection_initialized = False

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  query  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
defquery(
    self,
    query: VectorStoreQuery,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): query

    """
    query_embedding = cast(List[float], query.query_embedding)
    #  NOTE: users can pass in qdrant_filters (nested/complicated filters) to override the default MetadataFilters
    qdrant_filters = kwargs.get("qdrant_filters")
    if qdrant_filters is not None:
        query_filter = qdrant_filters
    else:
        query_filter = cast(Filter, self._build_query_filter(query))

    shard_identifier = kwargs.get("shard_identifier")
    shard_key = (
        self._generate_shard_key_selector(shard_identifier)
        if shard_identifier is not None
        else None
    )

    search_params = kwargs.get("search_params")
    if search_params is not None and isinstance(search_params, dict):
        search_params = rest.SearchParams(**search_params)
    search_params = cast(Optional[rest.SearchParams], search_params)

    if query.mode == VectorStoreQueryMode.HYBRID and not self.enable_hybrid:
        raise ValueError(
            "Hybrid search is not enabled. Please build the query with "
            "`enable_hybrid=True` in the constructor."
        )
    elif (
        query.mode == VectorStoreQueryMode.HYBRID
        and self.enable_hybrid
        and self._sparse_query_fn is not None
        and query.query_str is not None
    ):
        sparse_indices, sparse_embedding = self._sparse_query_fn(
            [query.query_str],
        )
        sparse_top_k = query.sparse_top_k or query.similarity_top_k

        sparse_response = self._client.query_batch_points(
            collection_name=self.collection_name,
            requests=[
                rest.QueryRequest(
                    query=query_embedding,
                    using=self.dense_vector_name,
                    limit=query.similarity_top_k,
                    filter=query_filter,
                    with_payload=True,
                    shard_key=shard_key,
                    params=search_params,
                ),
                rest.QueryRequest(
                    query=rest.SparseVector(
                        indices=sparse_indices[0],
                        values=sparse_embedding[0],
                    ),
                    using=self.sparse_vector_name,
                    limit=sparse_top_k,
                    filter=query_filter,
                    with_payload=True,
                    shard_key=shard_key,
                    params=search_params,
                ),
            ],
        )

        # sanity check
        assert len(sparse_response) == 2
        assert self._hybrid_fusion_fn is not None

        # flatten the response
        return self._hybrid_fusion_fn(
            self.parse_to_query_result(sparse_response[0].points),
            self.parse_to_query_result(sparse_response[1].points),
            # NOTE: only for hybrid search (0 for sparse search, 1 for dense search)
            alpha=query.alpha if query.alpha is not None else 0.5,
            # NOTE: use hybrid_top_k if provided, otherwise use similarity_top_k
            top_k=query.hybrid_top_k or query.similarity_top_k,
        )
    elif (
        query.mode == VectorStoreQueryMode.SPARSE
        and self.enable_hybrid
        and self._sparse_query_fn is not None
        and query.query_str is not None
    ):
        sparse_indices, sparse_embedding = self._sparse_query_fn(
            [query.query_str],
        )
        sparse_top_k = query.sparse_top_k or query.similarity_top_k

        sparse_response = self._client.query_batch_points(
            collection_name=self.collection_name,
            requests=[
                rest.QueryRequest(
                    query=rest.SparseVector(
                        indices=sparse_indices[0],
                        values=sparse_embedding[0],
                    ),
                    using=self.sparse_vector_name,
                    limit=sparse_top_k,
                    filter=query_filter,
                    with_payload=True,
                    shard_key=shard_key,
                    params=search_params,
                ),
            ],
        )

        return self.parse_to_query_result(sparse_response[0].points)
    elif self.enable_hybrid:
        # search for dense vectors only
        response = self._client.query_batch_points(
            collection_name=self.collection_name,
            requests=[
                rest.QueryRequest(
                    query=query_embedding,
                    using=self.dense_vector_name,
                    limit=query.similarity_top_k,
                    filter=query_filter,
                    with_payload=True,
                    shard_key=shard_key,
                    params=search_params,
                ),
            ],
        )

        return self.parse_to_query_result(response[0].points)
    else:
        # Regular non-hybrid search
        response = self._client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            using=self.dense_vector_name,
            limit=query.similarity_top_k,
            query_filter=query_filter,
            shard_key_selector=shard_key,
            search_params=search_params,
        )
        return self.parse_to_query_result(response.points)

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Asynchronous method to query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  query  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
async defaquery(
    self,
    query: VectorStoreQuery,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""
    Asynchronous method to query index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): query

    """
    self._ensure_async_client()

    query_embedding = cast(List[float], query.query_embedding)

    #  NOTE: users can pass in qdrant_filters (nested/complicated filters) to override the default MetadataFilters
    qdrant_filters = kwargs.get("qdrant_filters")
    if qdrant_filters is not None:
        query_filter = qdrant_filters
    else:
        # build metadata filters
        query_filter = cast(Filter, self._build_query_filter(query))

    # Check if we need to detect vector format
    if self._legacy_vector_format is None:
        await self._adetect_vector_format(self.collection_name)

    # Get shard_identifier if provided
    shard_identifier = kwargs.get("shard_identifier")
    shard_key = (
        self._generate_shard_key_selector(shard_identifier)
        if shard_identifier
        else None
    )

    search_params = kwargs.get("search_params")
    if search_params is not None and isinstance(search_params, dict):
        search_params = rest.SearchParams(**search_params)
    search_params = cast(Optional[rest.SearchParams], search_params)

    if query.mode == VectorStoreQueryMode.HYBRID and not self.enable_hybrid:
        raise ValueError(
            "Hybrid search is not enabled. Please build the query with "
            "`enable_hybrid=True` in the constructor."
        )
    elif (
        query.mode == VectorStoreQueryMode.HYBRID
        and self.enable_hybrid
        and self._sparse_query_fn is not None
        and query.query_str is not None
    ):
        sparse_indices, sparse_embedding = self._sparse_query_fn(
            [query.query_str],
        )
        sparse_top_k = query.sparse_top_k or query.similarity_top_k

        sparse_response = await self._aclient.query_batch_points(
            collection_name=self.collection_name,
            requests=[
                rest.QueryRequest(
                    query=query_embedding,
                    using=self.dense_vector_name,
                    limit=query.similarity_top_k,
                    filter=query_filter,
                    with_payload=True,
                    shard_key=shard_key,
                    params=search_params,
                ),
                rest.QueryRequest(
                    query=rest.SparseVector(
                        indices=sparse_indices[0],
                        values=sparse_embedding[0],
                    ),
                    using=self.sparse_vector_name,
                    limit=sparse_top_k,
                    filter=query_filter,
                    with_payload=True,
                    shard_key=shard_key,
                    params=search_params,
                ),
            ],
        )

        # sanity check
        assert len(sparse_response) == 2
        assert self._hybrid_fusion_fn is not None

        # flatten the response
        return self._hybrid_fusion_fn(
            self.parse_to_query_result(sparse_response[0].points),
            self.parse_to_query_result(sparse_response[1].points),
            alpha=query.alpha or 0.5,
            # NOTE: use hybrid_top_k if provided, otherwise use similarity_top_k
            top_k=query.hybrid_top_k or query.similarity_top_k,
        )
    elif (
        query.mode == VectorStoreQueryMode.SPARSE
        and self.enable_hybrid
        and self._sparse_query_fn is not None
        and query.query_str is not None
    ):
        sparse_indices, sparse_embedding = self._sparse_query_fn(
            [query.query_str],
        )
        sparse_top_k = query.sparse_top_k or query.similarity_top_k

        sparse_response = await self._aclient.query_batch_points(
            collection_name=self.collection_name,
            requests=[
                rest.QueryRequest(
                    query=rest.SparseVector(
                        indices=sparse_indices[0],
                        values=sparse_embedding[0],
                    ),
                    using=self.sparse_vector_name,
                    limit=sparse_top_k,
                    filter=query_filter,
                    with_payload=True,
                    shard_key=shard_key,
                    params=search_params,
                ),
            ],
        )
        return self.parse_to_query_result(sparse_response[0].points)
    elif self.enable_hybrid:
        # search for dense vectors only
        response = await self._aclient.query_batch_points(
            collection_name=self.collection_name,
            requests=[
                rest.QueryRequest(
                    query=query_embedding,
                    using=self.dense_vector_name,
                    limit=query.similarity_top_k,
                    filter=query_filter,
                    with_payload=True,
                    shard_key=shard_key,
                    params=search_params,
                ),
            ],
        )

        return self.parse_to_query_result(response[0].points)
    else:
        response = await self._aclient.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            using=self.dense_vector_name,
            limit=query.similarity_top_k,
            query_filter=query_filter,
            shard_key_selector=shard_key,
            search_params=search_params,
        )

        return self.parse_to_query_result(response.points)

```
 |  
| --- | --- |  
###  parse_to_query_result [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.parse_to_query_result "Permanent link")

```
parse_to_query_result(
    response: [],
) -> 

```

Convert vector store response to VectorStoreQueryResult.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `response`  |  `List[Any]`  |  List[Any]: List of results returned from the vector store.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
defparse_to_query_result(self, response: List[Any]) -> VectorStoreQueryResult:
"""
    Convert vector store response to VectorStoreQueryResult.

    Args:
        response: List[Any]: List of results returned from the vector store.

    """
    nodes = []
    similarities = []
    ids = []

    for point in response:
        payload = cast(Payload, point.payload)
        vector = point.vector
        embedding = None

        if isinstance(vector, dict):
            embedding = vector.get(self.dense_vector_name, vector.get("", None))
        elif isinstance(vector, list):
            embedding = vector

        try:
            node = metadata_dict_to_node(payload)

            if embedding and node.embedding is None:
                node.embedding = embedding
        except Exception:
            metadata, node_info, relationships = legacy_metadata_dict_to_node(
                payload
            )

            node = TextNode(
                id_=str(point.id),
                text=payload.get(self.text_key),
                metadata=metadata,
                start_char_idx=node_info.get("start", None),
                end_char_idx=node_info.get("end", None),
                relationships=relationships,
                embedding=embedding,
            )
        nodes.append(node)
        ids.append(str(point.id))
        try:
            similarities.append(point.score)
        except AttributeError:
            # certain requests do not return a score
            similarities.append(1.0)

    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
###  use_old_sparse_encoder [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.use_old_sparse_encoder "Permanent link")

```
use_old_sparse_encoder(collection_name: ) -> 

```

Check if the collection uses the old sparse encoder format. This is used during initialization to determine which sparse vector name to use.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
defuse_old_sparse_encoder(self, collection_name: str) -> bool:
"""
    Check if the collection uses the old sparse encoder format.
    This is used during initialization to determine which sparse vector name to use.
    """
    collection_exists = self._collection_exists(collection_name)
    if collection_exists:
        cur_collection = self.client.get_collection(collection_name)
        return DEFAULT_SPARSE_VECTOR_NAME_OLD in (
            cur_collection.config.params.sparse_vectors or {}
        )

    return False

```
 |  
| --- | --- |  
###  ause_old_sparse_encoder [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.ause_old_sparse_encoder "Permanent link")

```
ause_old_sparse_encoder(collection_name: ) -> 

```

Asynchronous method to check if the collection uses the old sparse encoder format.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
async defause_old_sparse_encoder(self, collection_name: str) -> bool:
"""
    Asynchronous method to check if the collection uses the old sparse encoder format.
    """
    collection_exists = await self._acollection_exists(collection_name)
    if collection_exists:
        cur_collection = await self._aclient.get_collection(collection_name)
        return DEFAULT_SPARSE_VECTOR_NAME_OLD in (
            cur_collection.config.params.sparse_vectors or {}
        )

    return False

```
 |  
| --- | --- |  
###  get_default_sparse_doc_encoder [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.get_default_sparse_doc_encoder "Permanent link")

```
get_default_sparse_doc_encoder(
    collection_name: ,
    fastembed_sparse_model: Optional[] = None,
) -> SparseEncoderCallable

```

Get the default sparse document encoder. For async-only clients, assumes new format initially. Will be auto-corrected on first async operation if collection uses old format.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
defget_default_sparse_doc_encoder(
    self,
    collection_name: str,
    fastembed_sparse_model: Optional[str] = None,
) -> SparseEncoderCallable:
"""
    Get the default sparse document encoder.
    For async-only clients, assumes new format initially.
    Will be auto-corrected on first async operation if collection uses old format.
    """
    if self._client is not None:
        if self.use_old_sparse_encoder(collection_name):
            self.sparse_vector_name = DEFAULT_SPARSE_VECTOR_NAME_OLD
            return default_sparse_encoder("naver/efficient-splade-VI-BT-large-doc")

    if fastembed_sparse_model is not None:
        return fastembed_sparse_encoder(model_name=fastembed_sparse_model)

    return fastembed_sparse_encoder()

```
 |  
| --- | --- |  
###  get_default_sparse_query_encoder [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/qdrant/#llama_index.vector_stores.qdrant.QdrantVectorStore.get_default_sparse_query_encoder "Permanent link")

```
get_default_sparse_query_encoder(
    collection_name: ,
    fastembed_sparse_model: Optional[] = None,
) -> SparseEncoderCallable

```

Get the default sparse query encoder. For async-only clients, assumes new format initially. Will be auto-corrected on first async operation if collection uses old format.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-qdrant/llama_index/vector_stores/qdrant/base.py`  
| 
```
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
```
 | 
```
defget_default_sparse_query_encoder(
    self,
    collection_name: str,
    fastembed_sparse_model: Optional[str] = None,
) -> SparseEncoderCallable:
"""
    Get the default sparse query encoder.
    For async-only clients, assumes new format initially.
    Will be auto-corrected on first async operation if collection uses old format.
    """
    if self._client is not None:
        if self.use_old_sparse_encoder(collection_name):
            # Update the sparse vector name to use the old format
            self.sparse_vector_name = DEFAULT_SPARSE_VECTOR_NAME_OLD
            return default_sparse_encoder(
                "naver/efficient-splade-VI-BT-large-query"
            )

    if fastembed_sparse_model is not None:
        return fastembed_sparse_encoder(model_name=fastembed_sparse_model)

    return fastembed_sparse_encoder()

```
 |  
| --- | --- |  
options: members: - QdrantVectorStore
