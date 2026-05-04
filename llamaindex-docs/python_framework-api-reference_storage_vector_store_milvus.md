# Milvus
##  MilvusVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore "Permanent link")
Bases: 
The Milvus Vector Store.
In this vector store we store the text, its embedding and a its metadata in a Milvus collection. This implementation allows the use of an already existing collection. It also supports creating a new one if the collection doesn't exist or if `overwrite` is set to True.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `uri`  |  The URI to connect to, comes in the form of "https://address:port" for Milvus or Zilliz Cloud service, or "path/to/local/milvus.db" for the lite local Milvus. Defaults to "./milvus_llamaindex.db".  |  `'./milvus_llamaindex.db'`  |  
|  `token`  |  The token for log in. Empty if not using rbac, if using rbac it will most likely be "username:password". Defaults to "".  |  
|  `collection_name`  |  The name of the collection where data will be stored. Defaults to "llamalection".  |  `'llamacollection'`  |  
|  `overwrite`  |  `bool`  |  Whether to overwrite existing collection with same name. Defaults to False.  |  `False`  |  
|  `upsert_mode`  |  `bool`  |  Whether to upsert documents into existing collection with same node id. Defaults to False.  |  `False`  |  
|  `doc_id_field`  |  The name of the doc_id field for the collection, defaults to DEFAULT_DOC_ID_KEY.  |  `DEFAULT_DOC_ID_KEY`  |  
|  `text_key`  |  What key text is stored in in the passed collection. Used when bringing your own collection. Defaults to DEFAULT_TEXT_KEY.  |  `DEFAULT_TEXT_KEY`  |  
|  `scalar_field_names`  |  `list`  |  The names of the extra scalar fields to be included in the collection schema.  |  `None`  |  
|  `scalar_field_types`  |  `list`  |  The types of the extra scalar fields.  |  `None`  |  
|  `enable_dense`  |  `bool`  |  A boolean flag to enable or disable dense embedding. Defaults to True.  |  `True`  |  
|  `dim`  |  The dimension of the embedding vectors for the collection. Required when creating a new collection with enable_sparse is False.  |  `None`  |  
|  `embedding_field`  |  The name of the dense embedding field for the collection, defaults to DEFAULT_EMBEDDING_KEY.  |  `DEFAULT_EMBEDDING_KEY`  |  
|  `index_config`  |  `dict`  |  The configuration used for building the dense embedding index. Defaults to None.  |  `None`  |  
|  `search_config`  |  `dict`  |  The configuration used for searching the Milvus dense index. Note that this must be compatible with the index type specified by `index_config`. Defaults to None.  |  `None`  |  
|  `similarity_metric`  |  The similarity metric to use for dense embedding, currently supports IP, COSINE and L2.  |  `'IP'`  |  
|  `enable_sparse`  |  `bool`  |  A boolean flag to enable or disable sparse embedding. Defaults to False.  |  `False`  |  
|  `sparse_embedding_field`  |  The name of sparse embedding field, defaults to DEFAULT_SPARSE_EMBEDDING_KEY.  |  `DEFAULT_SPARSE_EMBEDDING_KEY`  |  
|  `sparse_embedding_function`  |  `Union[BaseSparseEmbeddingFunction, BaseMilvusBuiltInFunction]`  |  If enable_sparse is True, this object should be provided to convert text to a sparse embedding. Defaults to None, which uses BM25 as the default sparse embedding function, or BGEM3 given existing collection without built-in functions.  |  `None`  |  
|  `sparse_index_config`  |  `dict`  |  The configuration used to build the sparse embedding index. Defaults to None.  |  `None`  |  
|  `collection_properties`  |  `dict`  |  The collection properties such as TTL (Time-To-Live) and MMAP (memory mapping). Defaults to None. It could include: - 'collection.ttl.seconds' (int): Once this property is set, data in the current collection expires in the specified time. Expired data in the collection will be cleaned up and will not be involved in searches or queries. - 'mmap.enabled' (bool): Whether to enable memory-mapped storage at the collection level.  |  `None`  |  
|  `index_management`  |   |  Specifies the index management strategy to use. Defaults to "create_if_not_exists".  |  `CREATE_IF_NOT_EXISTS`  |  
|  `batch_size`  |  Configures the number of documents processed in one batch when inserting data into Milvus. Defaults to DEFAULT_BATCH_SIZE.  |  `DEFAULT_BATCH_SIZE`  |  
|  `consistency_level`  |  Which consistency level to use for a newly created collection. Defaults to "Session".  |  `'Session'`  |  
|  `hybrid_ranker`  |  Specifies the type of ranker used in hybrid search queries. Currently only supports ['RRFRanker','WeightedRanker']. Defaults to "RRFRanker".  |  `'RRFRanker'`  |  
|  `hybrid_ranker_params`  |  `dict`  |  Configuration parameters for the hybrid ranker. The structure of this dictionary depends on the specific ranker being used: - For "RRFRanker", it should include: - 'k' (int): A parameter used in Reciprocal Rank Fusion (RRF). This value is used to calculate the rank scores as part of the RRF algorithm, which combines multiple ranking strategies into a single score to improve search relevance. - For "WeightedRanker", it expects: - 'weights' (list of float): A list of exactly two weights: 1. The weight for the dense embedding component. 2. The weight for the sparse embedding component. These weights are used to adjust the importance of the dense and sparse components of the embeddings in the hybrid retrieval process. Defaults to an empty dictionary, implying that the ranker will operate with its predefined default settings.  |  
|  `use_asyc_client`  |  `bool`  |  Whether or not to set the async client. Setting this to `True` outside of asynchronous environments will cause errors.  |  _required_  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ImportError`  |  Unable to import `pymilvus`.  |  
|  `MilvusException`  |  Error communicating with Milvus, more can be found in logging under Debug.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `MilvusVectorstore`  |  Vectorstore that supports add, delete, and query.  |  
Examples:
`pip install llama-index-vector-stores-milvus`

```
fromllama_index.vector_stores.milvusimport MilvusVectorStore

# Setup MilvusVectorStore
vector_store = MilvusVectorStore(
    dim=1536,
    collection_name="your_collection_name",
    uri="http://milvus_address:port",
    token="your_milvus_token_here",
    overwrite=True
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
| 
```
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
```
 | 
```
classMilvusVectorStore(BasePydanticVectorStore):
"""
    The Milvus Vector Store.

    In this vector store we store the text, its embedding and
    a its metadata in a Milvus collection. This implementation
    allows the use of an already existing collection.
    It also supports creating a new one if the collection doesn't
    exist or if `overwrite` is set to True.

    Args:
        uri (str): The URI to connect to, comes in the form of
            "https://address:port" for Milvus or Zilliz Cloud service,
            or "path/to/local/milvus.db" for the lite local Milvus. Defaults to
            "./milvus_llamaindex.db".
        token (str): The token for log in. Empty if not using rbac, if
            using rbac it will most likely be "username:password". Defaults to "".
        collection_name (str): The name of the collection where data will be
            stored. Defaults to "llamalection".
        overwrite (bool, optional): Whether to overwrite existing collection with same
            name. Defaults to False.
        upsert_mode (bool, optional): Whether to upsert documents into existing collection with same node id. Defaults to False.
        doc_id_field (str, optional): The name of the doc_id field for the collection,
            defaults to DEFAULT_DOC_ID_KEY.
        text_key (str, optional): What key text is stored in in the passed collection.
            Used when bringing your own collection. Defaults to DEFAULT_TEXT_KEY.
        scalar_field_names (list, optional): The names of the extra scalar fields to be included in the collection schema.
        scalar_field_types (list, optional): The types of the extra scalar fields.
        enable_dense (bool): A boolean flag to enable or disable dense embedding. Defaults to True.
        dim (int, optional): The dimension of the embedding vectors for the collection.
            Required when creating a new collection with enable_sparse is False.
        embedding_field (str, optional): The name of the dense embedding field for the
            collection, defaults to DEFAULT_EMBEDDING_KEY.
        index_config (dict, optional): The configuration used for building the
            dense embedding index. Defaults to None.
        search_config (dict, optional): The configuration used for searching
            the Milvus dense index. Note that this must be compatible with the index
            type specified by `index_config`. Defaults to None.
        similarity_metric (str, optional): The similarity metric to use for dense embedding,
            currently supports IP, COSINE and L2.
        enable_sparse (bool): A boolean flag to enable or disable sparse embedding. Defaults to False.
        sparse_embedding_field (str): The name of sparse embedding field, defaults to DEFAULT_SPARSE_EMBEDDING_KEY.
        sparse_embedding_function (Union[BaseSparseEmbeddingFunction, BaseMilvusBuiltInFunction], optional):
            If enable_sparse is True, this object should be provided to convert text to a sparse embedding.
            Defaults to None, which uses BM25 as the default sparse embedding function,
            or BGEM3 given existing collection without built-in functions.
        sparse_index_config (dict, optional): The configuration used to build the sparse embedding index.
            Defaults to None.
        collection_properties (dict, optional): The collection properties such as TTL
            (Time-To-Live) and MMAP (memory mapping). Defaults to None.
            It could include:
            - 'collection.ttl.seconds' (int): Once this property is set, data in the
                current collection expires in the specified time. Expired data in the
                collection will be cleaned up and will not be involved in searches or queries.
            - 'mmap.enabled' (bool): Whether to enable memory-mapped storage at the collection level.
        index_management (IndexManagement): Specifies the index management strategy to use. Defaults to "create_if_not_exists".
        batch_size (int): Configures the number of documents processed in one
            batch when inserting data into Milvus. Defaults to DEFAULT_BATCH_SIZE.
        consistency_level (str, optional): Which consistency level to use for a newly
            created collection. Defaults to "Session".
        hybrid_ranker (str): Specifies the type of ranker used in hybrid search queries.
            Currently only supports ['RRFRanker','WeightedRanker']. Defaults to "RRFRanker".
        hybrid_ranker_params (dict, optional): Configuration parameters for the hybrid ranker.
            The structure of this dictionary depends on the specific ranker being used:
            - For "RRFRanker", it should include:
                - 'k' (int): A parameter used in Reciprocal Rank Fusion (RRF). This value is used
                             to calculate the rank scores as part of the RRF algorithm, which combines
                             multiple ranking strategies into a single score to improve search relevance.
            - For "WeightedRanker", it expects:
                - 'weights' (list of float): A list of exactly two weights:
                     1. The weight for the dense embedding component.
                     2. The weight for the sparse embedding component.
                  These weights are used to adjust the importance of the dense and sparse components of the embeddings
                  in the hybrid retrieval process.
            Defaults to an empty dictionary, implying that the ranker will operate with its predefined default settings.
        use_asyc_client (bool, optional): Whether or not to set the async client. Setting this to `True` outside of asynchronous environments will cause errors.

    Raises:
        ImportError: Unable to import `pymilvus`.
        MilvusException: Error communicating with Milvus, more can be found in logging
            under Debug.

    Returns:
        MilvusVectorstore: Vectorstore that supports add, delete, and query.

    Examples:
        `pip install llama-index-vector-stores-milvus`

        ```python
        from llama_index.vector_stores.milvus import MilvusVectorStore

        # Setup MilvusVectorStore
        vector_store = MilvusVectorStore(
            dim=1536,
            collection_name="your_collection_name",
            uri="http://milvus_address:port",
            token="your_milvus_token_here",
            overwrite=True

        ```

    """

    stores_text: bool = True
    stores_node: bool = True

    uri: str = "./milvus_llamaindex.db"
    token: str = ""
    collection_name: str = "llamacollection"
    dim: Optional[int]
    embedding_field: str = DEFAULT_EMBEDDING_KEY
    doc_id_field: str = DEFAULT_DOC_ID_KEY
    similarity_metric: str = "IP"
    consistency_level: str = "Session"
    overwrite: bool = False
    upsert_mode: bool = False
    text_key: str = DEFAULT_TEXT_KEY
    output_fields: List[str] = Field(default_factory=list)
    index_config: Optional[dict]
    sparse_index_config: Optional[dict]
    search_config: Optional[dict]
    collection_properties: Optional[dict]
    batch_size: int = DEFAULT_BATCH_SIZE
    enable_dense: bool = True
    enable_sparse: bool = False
    sparse_embedding_field: str = DEFAULT_SPARSE_EMBEDDING_KEY
    sparse_embedding_function: Optional[
        Union[BaseMilvusBuiltInFunction, BaseSparseEmbeddingFunction]
    ]
    hybrid_ranker: str
    hybrid_ranker_params: dict = {}
    index_management: IndexManagement = IndexManagement.CREATE_IF_NOT_EXISTS
    scalar_field_names: Optional[List[str]]
    scalar_field_types: Optional[List[DataType]]
    use_async_client: bool = True

    _milvusclient: MilvusClient = PrivateAttr()
    _async_milvusclient: Optional[AsyncMilvusClient] = PrivateAttr()
    _collection_initialized: bool = PrivateAttr(default=False)

    def__init__(
        self,
        uri: str = "./milvus_llamaindex.db",
        token: str = "",
        collection_name: str = "llamacollection",
        overwrite: bool = False,
        upsert_mode: bool = False,
        collection_properties: Optional[dict] = None,
        doc_id_field: str = DEFAULT_DOC_ID_KEY,
        text_key: str = DEFAULT_TEXT_KEY,
        scalar_field_names: Optional[List[str]] = None,
        scalar_field_types: Optional[List[DataType]] = None,
        enable_dense: bool = True,
        dim: Optional[int] = None,
        embedding_field: str = DEFAULT_EMBEDDING_KEY,
        enable_sparse: bool = False,
        sparse_embedding_field: str = DEFAULT_SPARSE_EMBEDDING_KEY,
        sparse_embedding_function: Optional[BaseSparseEmbeddingFunction] = None,
        index_management: IndexManagement = IndexManagement.CREATE_IF_NOT_EXISTS,
        batch_size: int = DEFAULT_BATCH_SIZE,
        index_config: Optional[dict] = None,
        sparse_index_config: Optional[dict] = None,
        search_config: Optional[dict] = None,
        similarity_metric: str = "IP",
        consistency_level: str = "Session",
        output_fields: Optional[List[str]] = None,
        hybrid_ranker: str = "RRFRanker",
        hybrid_ranker_params: dict = {},
        use_async_client: bool = True,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__(
            collection_name=collection_name,
            enable_dense=enable_dense,
            dim=dim,
            embedding_field=embedding_field,
            doc_id_field=doc_id_field,
            consistency_level=consistency_level,
            overwrite=overwrite,
            upsert_mode=upsert_mode,
            text_key=text_key,
            output_fields=output_fields or [],
            index_config=index_config if index_config else {},
            search_config=search_config if search_config else {},
            collection_properties=collection_properties,
            batch_size=batch_size,
            enable_sparse=enable_sparse,
            sparse_embedding_field=sparse_embedding_field,
            sparse_embedding_function=sparse_embedding_function,
            sparse_index_config=sparse_index_config if sparse_index_config else {},
            hybrid_ranker=hybrid_ranker,
            hybrid_ranker_params=hybrid_ranker_params,
            index_management=index_management,
            scalar_field_names=scalar_field_names,
            scalar_field_types=scalar_field_types,
            use_async_client=use_async_client,
        )
        # Connect to Milvus instance
        self._milvusclient = MilvusClient(
            uri=uri,
            token=token,
            **kwargs,  # pass additional arguments such as server_pem_path
        )

        # As of writing, milvus sets alias internally in the async client.
        # This will cause an error if not removed.
        kwargs.pop("alias", None)
        if use_async_client:
            self._async_milvusclient = AsyncMilvusClient(
                uri=uri,
                token=token,
                **kwargs,  # pass additional arguments such as server_pem_path
            )
        else:
            self._async_milvusclient = None

        # Delete previous collection if overwriting
        if overwrite and collection_name in self.client.list_collections():
            self.client.drop_collection(collection_name)

        # Check if the collection exists
        if collection_name in self.client.list_collections():
            self._collection_initialized = True
            self._create_index_if_required()
        else:
            self._collection_initialized = False

        # Set default args
        self.similarity_metric = similarity_metrics_map.get(
            similarity_metric.lower(), "L2"
        )
        if self.enable_dense and self.embedding_field is None:
            logger.warning("Dense embedding field name is not provided, using default.")
            self.embedding_field = DEFAULT_EMBEDDING_KEY
        if self.enable_sparse:
            if self.sparse_embedding_field is None:
                logger.warning(
                    "Sparse embedding field name is not provided, using default."
                )
                self.sparse_embedding_field = DEFAULT_SPARSE_EMBEDDING_KEY
            if self.sparse_embedding_function is None:
                logger.warning(
                    "Sparse embedding function is not provided, using default."
                )
                collection_info = (
                    self.client.describe_collection(collection_name)
                    if self._collection_initialized
                    else None
                )
                self.sparse_embedding_function = get_default_sparse_embedding_function(
                    input_field_names=self.text_key,
                    output_field_names=self.sparse_embedding_field,
                    collection_info=collection_info,
                )

        # Create the collection & index if it does not exist
        if not self._collection_initialized:
            # Prepare schema
            schema = self.client.create_schema(auto_id=False, enable_dynamic_field=True)
            schema = self._add_fields_to_schema(schema)  # add fields
            schema = self._add_functions_to_schema(schema)  # add functions
            schema.verify()  # check schema

            # Prepare index
            index_params = self.client.prepare_index_params()
            if self.index_management is not IndexManagement.NO_VALIDATION:
                if self.enable_dense:
                    index_params = self._add_dense_index_params(index_params)
                if self.enable_sparse:
                    index_params = self._add_sparse_index_params(index_params)

            # Create collection
            self.client.create_collection(
                collection_name=self.collection_name,
                schema=schema,
                index_params=index_params,
                consistency_level=self.consistency_level,
            )
            logger.debug(
                f"Successfully created a new collection: {self.collection_name}"
            )
            self._collection_initialized = True

        # Set properties
        if collection_properties:
            if self.client.get_load_state(collection_name) == LoadState.Loaded:
                self.client.release_collection(collection_name)
                self.client.alter_collection_properties(
                    collection_name=collection_name,
                    properties=collection_properties,
                )
                self.client.load_collection(collection_name)
            else:
                self.client.alter_collection_properties(
                    collection_name=collection_name,
                    properties=collection_properties,
                )

        logger.debug(
            f"Successfully set properties for collection: {self.collection_name}"
        )

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "MilvusVectorStore"

    @property
    defclient(self) -> MilvusClient:
"""Get client."""
        return self._milvusclient

    @property
    defaclient(self) -> Optional[AsyncMilvusClient]:
"""Get async client."""
        return self._async_milvusclient

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add the embeddings and their nodes into Milvus.

        Args:
            nodes (List[BaseNode]): List of nodes with embeddings
                to insert.
            **add_kwargs (Any): Additional keyword arguments.
                - `milvus_partition_name` (Optional[str]): Specific Milvus partition.

        Raises:
            MilvusException: Failed to insert data.

        Returns:
            List[str]: List of ids inserted.

        """
        insert_list = []
        insert_ids = []

        if self.enable_sparse is True and self.sparse_embedding_function is None:
            logger.fatal(
                "sparse_embedding_function is None when enable_sparse is True."
            )

        # Process that data we are going to insert
        for node in nodes:
            entry = node_to_metadata_dict(
                node, remove_text=True, text_field=self.text_key
            )
            entry[self.text_key] = node.dict()[self.text_key]
            entry[MILVUS_ID_FIELD] = node.node_id
            if self.enable_dense:
                entry[self.embedding_field] = node.embedding
            if self.enable_sparse:
                if isinstance(
                    self.sparse_embedding_function, BaseSparseEmbeddingFunction
                ):
                    entry[self.sparse_embedding_field] = (
                        self.sparse_embedding_function.encode_documents([node.text])[0]
                    )
                else:  # BaseMilvusBuiltInFunction
                    pass

            insert_ids.append(node.node_id)
            insert_list.append(entry)

        if self.upsert_mode:
            executor_wrapper = self.client.upsert
        else:
            executor_wrapper = self.client.insert

        # Insert or Upsert the data into milvus
        for insert_batch in iter_batch(insert_list, self.batch_size):
            executor_wrapper(
                self.collection_name,
                insert_batch,
                partition_name=add_kwargs.get("milvus_partition_name"),
            )
        if add_kwargs.get("force_flush", False):
            self.client.flush(self.collection_name)
        logger.debug(
            f"Successfully inserted embeddings into: {self.collection_name} "
            f"Num Inserted: {len(insert_list)}"
        )
        return insert_ids

    async defasync_add(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""Asynchronous version of the add method."""
        assert self._async_milvusclient is not None, (
            "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
        )
        insert_list = []
        insert_ids = []

        if self.enable_sparse is True and self.sparse_embedding_function is None:
            logger.fatal(
                "sparse_embedding_function is None when enable_sparse is True."
            )

        # Process that data we are going to insert
        for node in nodes:
            entry = node_to_metadata_dict(
                node, remove_text=True, text_field=self.text_key
            )
            entry[self.text_key] = node.dict()[self.text_key]
            entry[MILVUS_ID_FIELD] = node.node_id
            if self.enable_dense:
                entry[self.embedding_field] = node.embedding
            if self.enable_sparse:
                if isinstance(
                    self.sparse_embedding_function, BaseSparseEmbeddingFunction
                ):
                    entry[self.sparse_embedding_field] = (
                        self.sparse_embedding_function.encode_documents([node.text])[0]
                    )
                else:  # BaseMilvusBuiltInFunction
                    pass

            insert_ids.append(node.node_id)
            insert_list.append(entry)

        if self.upsert_mode:
            executor_wrapper = self.aclient.upsert
        else:
            executor_wrapper = self.aclient.insert

        # Insert or Upsert the data into milvus
        for insert_batch in iter_batch(insert_list, self.batch_size):
            await executor_wrapper(
                self.collection_name,
                insert_batch,
                partition_name=add_kwargs.get("milvus_partition_name"),
            )
        if add_kwargs.get("force_flush", False):
            raise NotImplementedError("force_flush is not supported in async mode.")
            # await self.aclient.flush(self.collection_name)
        logger.debug(
            f"Successfully inserted embeddings into: {self.collection_name} "
            f"Num Inserted: {len(insert_list)}"
        )
        return insert_ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.
            **delete_kwargs (Any): Additional keyword arguments.
                - `milvus_partition_name` (Optional[str]): Specific Milvus partition.

        Raises:
            MilvusException: Failed to delete the doc.

        """
        # Adds ability for multiple doc delete in future.
        doc_ids: List[str]
        if isinstance(ref_doc_id, list):
            doc_ids = ref_doc_id  # type: ignore
        else:
            doc_ids = [ref_doc_id]

        # Begin by querying for the primary keys to delete
        doc_ids = ['"' + entry + '"' for entry in doc_ids]
        entries = self.client.query(
            collection_name=self.collection_name,
            filter=f"{self.doc_id_field} in [{','.join(doc_ids)}]",
        )
        if len(entries)  0:
            ids = [entry["id"] for entry in entries]
            self.client.delete(
                collection_name=self.collection_name,
                pks=ids,
                partition_name=delete_kwargs.get("milvus_partition_name"),
            )
            logger.debug(f"Successfully deleted embedding with doc_id: {doc_ids}")

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Asynchronous version of the delete method."""
        assert self._async_milvusclient is not None, (
            "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
        )
        # Adds ability for multiple doc delete in future.
        doc_ids: List[str]
        if isinstance(ref_doc_id, list):
            doc_ids = ref_doc_id  # type: ignore
        else:
            doc_ids = [ref_doc_id]

        # Begin by querying for the primary keys to delete
        doc_ids = ['"' + entry + '"' for entry in doc_ids]
        entries = await self.aclient.query(
            collection_name=self.collection_name,
            filter=f"{self.doc_id_field} in [{','.join(doc_ids)}]",
        )
        if len(entries)  0:
            ids = [entry["id"] for entry in entries]
            await self.aclient.delete(
                collection_name=self.collection_name,
                pks=ids,
                partition_name=delete_kwargs.get("milvus_partition_name"),
            )
            logger.debug(f"Successfully deleted embedding with doc_id: {doc_ids}")

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
            **delete_kwargs (Any): Additional keyword arguments.
                - `milvus_partition_name` (Optional[str]): Specific Milvus partition.

        """
        filters_cpy = deepcopy(filters) or MetadataFilters(filters=[])

        if node_ids:
            filters_cpy.filters.append(
                MetadataFilter(key="id", value=node_ids, operator=FilterOperator.IN)
            )

        if filters_cpy is not None:
            filter = _to_milvus_filter(filters_cpy)
        else:
            filter = None

        self.client.delete(
            collection_name=self.collection_name,
            filter=filter,
            partition_name=delete_kwargs.get("milvus_partition_name"),
            **delete_kwargs,
        )
        logger.debug(f"Successfully deleted node_ids: {node_ids}")

    async defadelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""Asynchronous version of the delete_nodes method."""
        assert self._async_milvusclient is not None, (
            "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
        )
        filters_cpy = deepcopy(filters) or MetadataFilters(filters=[])

        if node_ids:
            filters_cpy.filters.append(
                MetadataFilter(key="id", value=node_ids, operator=FilterOperator.IN)
            )

        if filters_cpy is not None:
            filter = _to_milvus_filter(filters_cpy)
        else:
            filter = None

        await self.aclient.delete(
            collection_name=self.collection_name,
            filter=filter,
            partition_name=delete_kwargs.get("milvus_partition_name"),
            **delete_kwargs,
        )
        logger.debug(f"Successfully deleted node_ids: {node_ids}")

    defclear(self) -> None:
"""Clears db."""
        self.client.drop_collection(self.collection_name)

    async defaclear(self) -> None:
"""Asynchronous version of the clear method."""
        assert self._async_milvusclient is not None, (
            "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
        )
        await self.aclient.drop_collection(self.collection_name)

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **kwargs,
    ) -> List[BaseNode]:
"""
        Get nodes by node ids or metadata filters.

        Args:
            node_ids (Optional[List[str]], optional): IDs of nodes to retrieve. Defaults to None.
            filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.
            **kwargs: Additional keyword arguments.
                - `milvus_partition_names` (Optional[List[str]]): Specific Milvus partitions.

        Raises:
            ValueError: Neither or both of node_ids and filters are provided.

        Returns:
            List[BaseNode]:

        """
        if node_ids is None and filters is None:
            raise ValueError("Either node_ids or filters must be provided.")

        filters_cpy = deepcopy(filters) or MetadataFilters(filters=[])
        milvus_filter = _to_milvus_filter(filters_cpy)

        if node_ids is not None and milvus_filter:
            raise ValueError("Only one of node_ids or filters can be provided.")

        res = self.client.query(
            ids=node_ids,
            collection_name=self.collection_name,
            filter=milvus_filter,
            partition_names=kwargs.get("milvus_partition_names"),
        )

        nodes = []
        for item in res:
            try:
                text_content = item.get(self.text_key)
            except Exception:
                raise ValueError(
                    "The passed in text_key value does not exist "
                    "in the retrieved entity."
                )
            if "_node_content" in item:
                node = metadata_dict_to_node(item, text=text_content)
            elif text_content:
                node = TextNode(
                    text=text_content,
                    metadata={key: item.get(key) for key in self.output_fields},
                )
            else:
                raise ValueError(
                    "Node content not found in metadata dict and no text content found."
                )
            node.embedding = item.get(self.embedding_field, None)
            nodes.append(node)
        return nodes

    async defaget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **kwargs,
    ) -> List[BaseNode]:
"""Asynchronous version of the get_nodes method."""
        assert self._async_milvusclient is not None, (
            "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
        )
        if node_ids is None and filters is None:
            raise ValueError("Either node_ids or filters must be provided.")

        filters_cpy = deepcopy(filters) or MetadataFilters(filters=[])
        milvus_filter = _to_milvus_filter(filters_cpy)

        if node_ids is not None and milvus_filter:
            raise ValueError("Only one of node_ids or filters can be provided.")

        res = await self.aclient.query(
            ids=node_ids,
            collection_name=self.collection_name,
            filter=milvus_filter,
            partition_names=kwargs.get("milvus_partition_names"),
        )

        nodes = []
        for item in res:
            try:
                text_content = item.get(self.text_key)
            except Exception:
                raise ValueError(
                    "The passed in text_key value does not exist "
                    "in the retrieved entity."
                )
            if "_node_content" in item:
                node = metadata_dict_to_node(item, text=text_content)
            elif text_content:
                node = TextNode(
                    text=text_content,
                    metadata={key: item.get(key) for key in self.output_fields},
                )
            else:
                raise ValueError(
                    "Node content not found in metadata dict and no text content found."
                )
            node.embedding = item.get(self.embedding_field, None)
            nodes.append(node)
        return nodes

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query_embedding (List[float]): query embedding
            similarity_top_k (int): top k most similar nodes
            doc_ids (Optional[List[str]]): list of doc_ids to filter by
            node_ids (Optional[List[str]]): list of node_ids to filter by
            output_fields (Optional[List[str]]): list of fields to return
            embedding_field (Optional[str]): name of embedding field
            milvus_partition_names (Optional[List[str]]): specific Milvus partitions.

        """
        if query.mode == VectorStoreQueryMode.DEFAULT:
            pass
        elif query.mode in [
            VectorStoreQueryMode.HYBRID,
            VectorStoreQueryMode.SPARSE,
            VectorStoreQueryMode.TEXT_SEARCH,
        ]:
            if self.enable_sparse is False:
                raise ValueError(
                    f"The query mode requires sparse embedding, but enable_sparse is False."
                )
        elif query.mode == VectorStoreQueryMode.MMR:
            pass
        else:
            raise ValueError(f"Milvus does not support {query.mode} yet.")

        filter_string_expr, output_fields = self._prepare_before_search(query, **kwargs)
        custom_string_expr = kwargs.pop("string_expr", "")
        if len(filter_string_expr) != 0:
            if len(custom_string_expr) != 0:
                logger.warning(
                    "string_expr in vector_store_kwargs is ignored because filters are provided."
                )
            string_expr = filter_string_expr
        else:
            string_expr = custom_string_expr

        # Perform the search
        if query.mode == VectorStoreQueryMode.MMR:
            nodes, similarities, ids = self._mmr_search(
                query, string_expr, output_fields, **kwargs
            )
        elif query.mode in [
            VectorStoreQueryMode.SPARSE,
            VectorStoreQueryMode.TEXT_SEARCH,
        ]:
            nodes, similarities, ids = self._sparse_search(
                query, string_expr, output_fields, **kwargs
            )
        elif query.mode == VectorStoreQueryMode.HYBRID:
            nodes, similarities, ids = self._hybrid_search(
                query, string_expr, output_fields, **kwargs
            )
        else:
            nodes, similarities, ids = self._default_search(
                query, string_expr, output_fields, **kwargs
            )
        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""Asynchronous version of the query method."""
        assert self._async_milvusclient is not None, (
            "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
        )
        if query.mode == VectorStoreQueryMode.DEFAULT:
            pass
        elif query.mode in [
            VectorStoreQueryMode.HYBRID,
            VectorStoreQueryMode.SPARSE,
            VectorStoreQueryMode.TEXT_SEARCH,
        ]:
            if self.enable_sparse is False:
                raise ValueError(
                    f"The query mode requires sparse embedding, but enable_sparse is False."
                )
        elif query.mode == VectorStoreQueryMode.MMR:
            pass
        else:
            raise ValueError(f"Milvus does not support {query.mode} yet.")

        string_expr, output_fields = self._prepare_before_search(query, **kwargs)

        # Perform the search
        if query.mode == VectorStoreQueryMode.MMR:
            nodes, similarities, ids = await self._async_mmr_search(
                query, string_expr, output_fields, **kwargs
            )
        elif query.mode in [
            VectorStoreQueryMode.SPARSE,
            VectorStoreQueryMode.TEXT_SEARCH,
        ]:
            nodes, similarities, ids = await self._async_sparse_search(
                query, string_expr, output_fields, **kwargs
            )
        elif query.mode == VectorStoreQueryMode.HYBRID:
            nodes, similarities, ids = await self._async_hybrid_search(
                query, string_expr, output_fields, **kwargs
            )
        else:
            nodes, similarities, ids = await self._async_default_search(
                query, string_expr, output_fields, **kwargs
            )
        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    def_prepare_before_search(
        self, query: VectorStoreQuery, **kwargs
    ) -> Tuple[str, List[str]]:
"""
        Prepare the expression and output fields for search.
        """
        expr = []
        output_fields = ["*"]
        # Parse the filter
        if query.filters is not None or "milvus_scalar_filters" in kwargs:
            expr.append(
                _to_milvus_filter(
                    query.filters,
                    (
                        kwargs["milvus_scalar_filters"]
                        if "milvus_scalar_filters" in kwargs
                        else None
                    ),
                )
            )
        # Parse any docs we are filtering on
        if query.doc_ids is not None and len(query.doc_ids) != 0:
            expr_list = ['"' + entry + '"' for entry in query.doc_ids]
            expr.append(f"{self.doc_id_field} in [{','.join(expr_list)}]")
        # Parse any nodes we are filtering on
        if query.node_ids is not None and len(query.node_ids) != 0:
            expr_list = ['"' + entry + '"' for entry in query.node_ids]
            expr.append(f"{MILVUS_ID_FIELD} in [{','.join(expr_list)}]")
        # Limit output fields
        outputs_limited = False
        if query.output_fields is not None:
            output_fields = query.output_fields
            outputs_limited = True
        elif len(self.output_fields)  0:
            output_fields = [*self.output_fields]
            outputs_limited = True
        # Add the text key to output fields if necessary
        if self.text_key not in output_fields and outputs_limited:
            output_fields.append(self.text_key)
        # Convert to string expression
        string_expr = ""
        if len(expr) != 0:
            string_expr = f" and ".join(expr)
        return string_expr, output_fields

    def_default_search(
        self,
        query: VectorStoreQuery,
        string_expr: str,
        output_fields: List[str],
        **kwargs,
    ) -> Tuple[List[BaseNode], List[float], List[str]]:
"""
        Perform default search: dense embedding search.
        """
        res = self.client.search(
            collection_name=self.collection_name,
            data=[query.query_embedding],
            filter=string_expr,
            limit=query.similarity_top_k,
            output_fields=output_fields,
            search_params=kwargs.get("milvus_search_config", self.search_config),
            anns_field=self.embedding_field,
            partition_names=kwargs.get("milvus_partition_names"),
        )
        logger.debug(
            f"Successfully searched embedding in collection: {self.collection_name}"
            f" Num Results: {len(res[0])}"
        )
        nodes, similarities, ids = self._parse_from_milvus_results(res)
        return nodes, similarities, ids

    async def_async_default_search(
        self,
        query: VectorStoreQuery,
        string_expr: str,
        output_fields: List[str],
        **kwargs,
    ) -> Tuple[List[BaseNode], List[float], List[str]]:
"""
        Perform asynchronous default search.
        """
        assert self._async_milvusclient is not None, (
            "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
        )
        res = await self.aclient.search(
            collection_name=self.collection_name,
            data=[query.query_embedding],
            filter=string_expr,
            limit=query.similarity_top_k,
            output_fields=output_fields,
            search_params=kwargs.get("milvus_search_config", self.search_config),
            anns_field=self.embedding_field,
            partition_names=kwargs.get("milvus_partition_names"),
        )
        logger.debug(
            f"Successfully searched embedding in collection: {self.collection_name}"
            f" Num Results: {len(res[0])}"
        )
        nodes, similarities, ids = self._parse_from_milvus_results(res)
        return nodes, similarities, ids

    def_mmr_search(
        self,
        query: VectorStoreQuery,
        string_expr: str,
        output_fields: List[str],
        **kwargs,
    ) -> Tuple[List[BaseNode], List[float], List[str]]:
"""
        Perform MMR search.
        """
        mmr_threshold = kwargs.get("mmr_threshold")
        if (
            kwargs.get("mmr_prefetch_factor") is not None
            and kwargs.get("mmr_prefetch_k") is not None
        ):
            raise ValueError(
                "'mmr_prefetch_factor' and 'mmr_prefetch_k' "
                "cannot coexist in a call to query()"
            )
        else:
            if kwargs.get("mmr_prefetch_k") is not None:
                prefetch_k0 = int(kwargs["mmr_prefetch_k"])
            else:
                prefetch_k0 = int(
                    query.similarity_top_k
                    * kwargs.get("mmr_prefetch_factor", DEFAULT_MMR_PREFETCH_FACTOR)
                )
        res = self.client.search(
            collection_name=self.collection_name,
            data=[query.query_embedding],
            filter=string_expr,
            limit=prefetch_k0,
            output_fields=output_fields,
            search_params=kwargs.get("milvus_search_config", self.search_config),
            anns_field=self.embedding_field,
            partition_names=kwargs.get("milvus_partition_names"),
        )
        nodes = res[0]
        node_embeddings = []
        node_ids = []
        for node in nodes:
            node_embeddings.append(node["entity"]["embedding"])
            node_ids.append(node["id"])
        mmr_similarities, mmr_ids = get_top_k_mmr_embeddings(
            query_embedding=query.query_embedding,
            embeddings=node_embeddings,
            similarity_top_k=query.similarity_top_k,
            embedding_ids=node_ids,
            mmr_threshold=mmr_threshold,
        )
        node_dict = dict(list(zip(node_ids, nodes)))
        selected_nodes = [node_dict[id] for id in mmr_ids if id in node_dict]
        similarities = mmr_similarities  # Passing the MMR similarities instead of the original similarities
        ids = mmr_ids
        nodes, _, _ = self._parse_from_milvus_results([selected_nodes])
        logger.debug(
            f"Successfully performed MMR on embeddings in collection: {self.collection_name}"
        )
        return nodes, similarities, ids

    async def_async_mmr_search(
        self,
        query: VectorStoreQuery,
        string_expr: str,
        output_fields: List[str],
        **kwargs,
    ) -> Tuple[List[BaseNode], List[float], List[str]]:
"""
        Perform asynchronous MMR search.
        """
        assert self._async_milvusclient is not None, (
            "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
        )
        mmr_threshold = kwargs.get("mmr_threshold")
        if (
            kwargs.get("mmr_prefetch_factor") is not None
            and kwargs.get("mmr_prefetch_k") is not None
        ):
            raise ValueError(
                "'mmr_prefetch_factor' and 'mmr_prefetch_k' "
                "cannot coexist in a call to query()"
            )
        else:
            if kwargs.get("mmr_prefetch_k") is not None:
                prefetch_k0 = int(kwargs["mmr_prefetch_k"])
            else:
                prefetch_k0 = int(
                    query.similarity_top_k
                    * kwargs.get("mmr_prefetch_factor", DEFAULT_MMR_PREFETCH_FACTOR)
                )

        res = await self.aclient.search(
            collection_name=self.collection_name,
            data=[query.query_embedding],
            filter=string_expr,
            limit=prefetch_k0,
            output_fields=output_fields,
            search_params=kwargs.get("milvus_search_config", self.search_config),
            anns_field=self.embedding_field,
            partition_names=kwargs.get("milvus_partition_names"),
        )
        nodes = res[0]
        node_embeddings = []
        node_ids = []
        for node in nodes:
            node_embeddings.append(node["entity"]["embedding"])
            node_ids.append(self._get_id_from_hit(node))

        mmr_similarities, mmr_ids = get_top_k_mmr_embeddings(
            query_embedding=query.query_embedding,
            embeddings=node_embeddings,
            similarity_top_k=query.similarity_top_k,
            embedding_ids=node_ids,
            mmr_threshold=mmr_threshold,
        )
        node_dict = dict(list(zip(node_ids, nodes)))
        selected_nodes = [node_dict[id] for id in mmr_ids if id in node_dict]
        similarities = mmr_similarities  # Passing the MMR similarities instead of the original similarities
        ids = mmr_ids
        nodes, _, _ = self._parse_from_milvus_results([selected_nodes])
        logger.debug(
            f"Successfully performed MMR on embeddings in collection: {self.collection_name}"
        )
        return nodes, similarities, ids

    def_sparse_search(
        self,
        query: VectorStoreQuery,
        string_expr: str,
        output_fields: List[str],
        **kwargs,
    ) -> Tuple[List[BaseNode], List[float], List[str]]:
"""
        Perform sparse search or full text search.
        """
        search_params = {"params": {"drop_ratio_search": 0.2}}
        if isinstance(self.sparse_embedding_function, BaseSparseEmbeddingFunction):
            sparse_emb = self.sparse_embedding_function.encode_queries(
                [query.query_str]
            )[0]
            query_data = [sparse_emb]
        elif isinstance(self.sparse_embedding_function, BaseMilvusBuiltInFunction):
            query_data = [query.query_str]
        res = self.client.search(
            collection_name=self.collection_name,
            data=query_data,
            anns_field=self.sparse_embedding_field,
            limit=query.similarity_top_k,
            filter=string_expr,
            output_fields=output_fields,
            search_params=search_params,
            partition_names=kwargs.get("milvus_partition_names"),
        )
        nodes, similarities, ids = self._parse_from_milvus_results(res)
        return nodes, similarities, ids

    async def_async_sparse_search(
        self,
        query: VectorStoreQuery,
        string_expr: str,
        output_fields: List[str],
        **kwargs,
    ) -> Tuple[List[BaseNode], List[float], List[str]]:
"""
        Perform asynchronous sparse search.
        """
        assert self._async_milvusclient is not None, (
            "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
        )
        search_params = {"params": {"drop_ratio_search": 0.2}}
        if isinstance(self.sparse_embedding_function, BaseSparseEmbeddingFunction):
            sparse_emb = self.sparse_embedding_function.encode_queries(
                [query.query_str]
            )[0]
            query_data = [sparse_emb]
        elif isinstance(self.sparse_embedding_function, BaseMilvusBuiltInFunction):
            query_data = [query.query_str]
        res = await self.aclient.search(
            collection_name=self.collection_name,
            data=query_data,
            anns_field=self.sparse_embedding_field,
            limit=query.similarity_top_k,
            filter=string_expr,
            output_fields=output_fields,
            search_params=search_params,
            partition_names=kwargs.get("milvus_partition_names"),
        )
        nodes, similarities, ids = self._parse_from_milvus_results(res)
        return nodes, similarities, ids

    def_hybrid_search(
        self,
        query: VectorStoreQuery,
        string_expr: str,
        output_fields: List[str],
        **kwargs,
    ) -> Tuple[List[BaseNode], List[float], List[str]]:
"""
        Perform hybrid search.
        """
        if isinstance(self.sparse_embedding_function, BaseSparseEmbeddingFunction):
            sparse_emb = self.sparse_embedding_function.encode_queries(
                [query.query_str]
            )[0]
            query_data = [sparse_emb]
            sparse_metric_type = "IP"
        elif isinstance(self.sparse_embedding_function, BaseMilvusBuiltInFunction):
            query_data = [query.query_str]
            sparse_metric_type = "BM25"
        sparse_req = AnnSearchRequest(
            data=query_data,
            anns_field=self.sparse_embedding_field,
            param={"metric_type": sparse_metric_type},
            limit=query.similarity_top_k,
            expr=string_expr,  # Apply metadata filters to sparse search
        )
        dense_search_params = {
            "metric_type": self.similarity_metric,
            "params": self.search_config,
        }
        dense_emb = query.query_embedding
        dense_req = AnnSearchRequest(
            data=[dense_emb],
            anns_field=self.embedding_field,
            param=dense_search_params,
            limit=query.similarity_top_k,
            expr=string_expr,  # Apply metadata filters to dense search
        )
        if WeightedRanker is None or RRFRanker is None:
            logger.error("Hybrid retrieval is only supported in Milvus 2.4.0 or later.")
            raise ValueError(
                "Hybrid retrieval is only supported in Milvus 2.4.0 or later."
            )
        if self.hybrid_ranker == "WeightedRanker":
            if self.hybrid_ranker_params == {}:
                self.hybrid_ranker_params = {"weights": [1.0, 1.0]}
            ranker = WeightedRanker(*self.hybrid_ranker_params["weights"])
        elif self.hybrid_ranker == "RRFRanker":
            if self.hybrid_ranker_params == {}:
                self.hybrid_ranker_params = {"k": 60}
            ranker = RRFRanker(self.hybrid_ranker_params["k"])
        else:
            raise ValueError(f"Unsupported ranker: {self.hybrid_ranker}")
        if not hasattr(self.client, "hybrid_search"):
            raise ValueError(
                "Your pymilvus version does not support hybrid search. please update it by `pip install -U pymilvus`"
            )
        res = self.client.hybrid_search(
            self.collection_name,
            [dense_req, sparse_req],
            ranker=ranker,
            limit=query.similarity_top_k,
            output_fields=output_fields,
            partition_names=kwargs.get("milvus_partition_names"),
        )
        logger.debug(
            f"Successfully searched embedding in collection: {self.collection_name}"
            f" Num Results: {len(res[0])}"
        )
        nodes, similarities, ids = self._parse_from_milvus_results(res)
        return nodes, similarities, ids

    async def_async_hybrid_search(
        self,
        query: VectorStoreQuery,
        string_expr: str,
        output_fields: List[str],
        **kwargs,
    ) -> Tuple[List[BaseNode], List[float], List[str]]:
"""
        Perform asynchronous hybrid search.
        """
        assert self._async_milvusclient is not None, (
            "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
        )
        if isinstance(self.sparse_embedding_function, BaseSparseEmbeddingFunction):
            sparse_emb = (
                await self.sparse_embedding_function.async_encode_queries(
                    [query.query_str]
                )
            )[0]
            query_data = [sparse_emb]
            sparse_metric_type = "IP"
        elif isinstance(self.sparse_embedding_function, BaseMilvusBuiltInFunction):
            query_data = [query.query_str]
            sparse_metric_type = "BM25"
        sparse_req = AnnSearchRequest(
            data=query_data,
            anns_field=self.sparse_embedding_field,
            param={"metric_type": sparse_metric_type},
            limit=query.similarity_top_k,
            expr=string_expr,  # Apply metadata filters to sparse search
        )
        dense_search_params = {
            "metric_type": self.similarity_metric,
            "params": self.search_config,
        }
        dense_emb = query.query_embedding
        dense_req = AnnSearchRequest(
            data=[dense_emb],
            anns_field=self.embedding_field,
            param=dense_search_params,
            limit=query.similarity_top_k,
            expr=string_expr,  # Apply metadata filters to dense search
        )
        if WeightedRanker is None or RRFRanker is None:
            logger.error("Hybrid retrieval is only supported in Milvus 2.4.0 or later.")
            raise ValueError(
                "Hybrid retrieval is only supported in Milvus 2.4.0 or later."
            )
        if self.hybrid_ranker == "WeightedRanker":
            if self.hybrid_ranker_params == {}:
                self.hybrid_ranker_params = {"weights": [1.0, 1.0]}
            ranker = WeightedRanker(*self.hybrid_ranker_params["weights"])
        elif self.hybrid_ranker == "RRFRanker":
            if self.hybrid_ranker_params == {}:
                self.hybrid_ranker_params = {"k": 60}
            ranker = RRFRanker(self.hybrid_ranker_params["k"])
        else:
            raise ValueError(f"Unsupported ranker: {self.hybrid_ranker}")
        if not hasattr(self.client, "hybrid_search"):
            raise ValueError(
                "Your pymilvus version does not support hybrid search. please update it by `pip install -U pymilvus`"
            )
        res = await self.aclient.hybrid_search(
            self.collection_name,
            [dense_req, sparse_req],
            ranker=ranker,
            limit=query.similarity_top_k,
            output_fields=output_fields,
            partition_names=kwargs.get("milvus_partition_names"),
        )
        logger.debug(
            f"Successfully searched embedding in collection: {self.collection_name}"
            f" Num Results: {len(res[0])}"
        )
        nodes, similarities, ids = self._parse_from_milvus_results(res)
        return nodes, similarities, ids

    def_create_index_if_required(self) -> None:
"""
        Create the index based on the index management strategy.

        This method only create index for existing collection without index.
        """
        if self.index_management == IndexManagement.NO_VALIDATION:
            return
        elif self.index_management == IndexManagement.CREATE_IF_NOT_EXISTS:
            if len(self.client.list_indexes(self.collection_name))  0:
                return
            else:
                index_params = self.client.prepare_index_params()
                if self.enable_dense:
                    index_params = self._add_dense_index_params(index_params)
                if self.enable_sparse:
                    index_params = self._add_sparse_index_params(index_params)
                self.client.create_index(self.collection_name, index_params)
                logger.debug(
                    f"Successfully created index for existing collection: {self.collection_name}"
                )
        else:
            logger.warning(
                f"Ignored unsupported index management strategy: {self.index_management}"
            )
            return

    def_add_dense_index_params(self, index_params: IndexParams):
"""Add dense vector index to params."""
        base_params: Dict[str, Any] = self.index_config.copy()
        field_name: str = base_params.pop("field_name", self.embedding_field)
        index_name: str = base_params.pop("index_name", self.embedding_field)
        index_type: str = base_params.pop("index_type", "FLAT")
        metric_type: str = base_params.pop("metric_type", self.similarity_metric)
        kwargs = {
            "field_name": field_name,
            "index_name": index_name,
            "index_type": index_type,
            "metric_type": metric_type,
        }
        if len(base_params) != 0:
            kwargs["params"] = base_params
        index_params.add_index(**kwargs)
        return index_params

    def_add_sparse_index_params(self, index_params: IndexParams):
"""Add sparse index params."""
        base_params: Dict[str, Any] = self.sparse_index_config.copy()
        field_name: str = base_params.pop("field_name", self.sparse_embedding_field)
        index_name: str = base_params.pop("index_name", self.sparse_embedding_field)
        index_type: str = base_params.pop("index_type", "SPARSE_INVERTED_INDEX")
        metric_type: str = base_params.pop(
            "metric_type", _get_index_metric_type(self.sparse_embedding_function)
        )
        kwargs = {
            "field_name": field_name,
            "index_name": index_name,
            "index_type": index_type,
            "metric_type": metric_type,
        }
        if len(base_params) != 0:
            kwargs["params"] = base_params
        index_params.add_index(**kwargs)
        return index_params

    def_add_fields_to_schema(self, schema: CollectionSchema):
        if self.enable_sparse and isinstance(
            self.sparse_embedding_function, BM25BuiltInFunction
        ):
            bm25_text_fields = self.sparse_embedding_function.input_field_names
            if isinstance(bm25_text_fields, str):
                bm25_text_fields = [bm25_text_fields]
        else:
            bm25_text_fields = []

        # Add scalar fields
        schema.add_field(
            field_name=MILVUS_ID_FIELD,
            datatype=DataType.VARCHAR,
            max_length=65_535,
            is_primary=True,
        )
        schema.add_field(
            field_name=self.doc_id_field,
            datatype=DataType.VARCHAR,
            max_length=65_535,
        )
        if self.text_key in bm25_text_fields:
            schema.add_field(
                field_name=self.text_key,
                datatype=DataType.VARCHAR,
                max_length=65_535,
                **self.sparse_embedding_function.get_field_kwargs(),
            )
        else:
            schema.add_field(
                field_name=self.text_key, datatype=DataType.VARCHAR, max_length=65_535
            )
        if self.scalar_field_names is not None and self.scalar_field_types is not None:
            if len(self.scalar_field_names) != len(self.scalar_field_types):
                raise ValueError(
                    "scalar_field_names and scalar_field_types must have same length."
                )
            for field_name, field_type in zip(
                self.scalar_field_names, self.scalar_field_types
            ):
                max_length = 65_535 if field_type == DataType.VARCHAR else None
                if field_name in bm25_text_fields:
                    schema.add_field(
                        field_name=field_name,
                        datatype=field_type,
                        max_length=max_length,
                        **self.sparse_embedding_function.get_field_kwargs(),
                    )
                else:
                    schema.add_field(
                        field_name=field_name,
                        datatype=field_type,
                        max_length=max_length,
                    )

        # Add embedding field(s)
        if self.enable_dense:  # dense field
            if self.dim is None or self.embedding_field is None:
                raise ValueError(
                    "Dim and embedding_field are required to add dense embedding field."
                )
            schema.add_field(
                field_name=self.embedding_field,
                datatype=DataType.FLOAT_VECTOR,
                dim=self.dim,
            )
        if self.enable_sparse:  # sparse field
            if (
                self.sparse_embedding_function is None
                or self.sparse_embedding_field is None
            ):
                raise ValueError(
                    "Sparse embedding function and sparse_embedding_field are required to add sparse field."
                )
            schema.add_field(
                field_name=self.sparse_embedding_field,
                datatype=DataType.SPARSE_FLOAT_VECTOR,
            )
        return schema

    def_add_functions_to_schema(self, schema: CollectionSchema):
        if self.enable_sparse and isinstance(
            self.sparse_embedding_function, BaseMilvusBuiltInFunction
        ):
            milvus_function = self.sparse_embedding_function
            schema.add_function(milvus_function)
        return schema

    def_parse_from_milvus_results(
        self, results: List
    ) -> Tuple[List[BaseNode], List[float], List[str]]:
"""
        Parses the results from Milvus and returns a list of nodes, similarities and ids.
        Only parse the first result since we are only searching for one query.
        """
        if len(results)  1:
            logger.warning(
                "More than one result found in Milvus search. Only parsing the first result."
            )
        nodes = []
        similarities = []
        ids = []
        # Parse the results
        for hit in results[0]:
            if "_node_content" in hit["entity"]:
                metadata = {
                    "_node_content": hit["entity"].get("_node_content", None),
                    "_node_type": hit["entity"].get("_node_type", None),
                }
                for key in self.output_fields:
                    metadata[key] = hit["entity"].get(key)
                node = metadata_dict_to_node(metadata)
            else:
                node = TextNode(
                    metadata={key: hit["entity"].get(key) for key in self.output_fields}
                )

            # Set the text field if it exists
            if self.text_key in hit["entity"]:
                text = hit["entity"].get(self.text_key)
                node.text = text

            nodes.append(node)
            similarities.append(hit["distance"])
            ids.append(self._get_id_from_hit(hit))
        return nodes, similarities, ids

    def_get_id_from_hit(self, hit: Dict) -> str:
        if "id" in hit:
            return hit["id"]
        else:
            return hit[next(iter(hit))]

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.client "Permanent link")

```
client: MilvusClient

```

Get client.
###  aclient `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.aclient "Permanent link")

```
aclient: Optional[AsyncMilvusClient]

```

Get async client.
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
| 
```
421
422
423
424
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "MilvusVectorStore"

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add the embeddings and their nodes into Milvus.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings to insert.  |  _required_  |  
|  `**add_kwargs`  |  Additional keyword arguments. - `milvus_partition_name` (Optional[str]): Specific Milvus partition.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `MilvusException`  |  Failed to insert data.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: List of ids inserted.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add the embeddings and their nodes into Milvus.

    Args:
        nodes (List[BaseNode]): List of nodes with embeddings
            to insert.
        **add_kwargs (Any): Additional keyword arguments.
            - `milvus_partition_name` (Optional[str]): Specific Milvus partition.

    Raises:
        MilvusException: Failed to insert data.

    Returns:
        List[str]: List of ids inserted.

    """
    insert_list = []
    insert_ids = []

    if self.enable_sparse is True and self.sparse_embedding_function is None:
        logger.fatal(
            "sparse_embedding_function is None when enable_sparse is True."
        )

    # Process that data we are going to insert
    for node in nodes:
        entry = node_to_metadata_dict(
            node, remove_text=True, text_field=self.text_key
        )
        entry[self.text_key] = node.dict()[self.text_key]
        entry[MILVUS_ID_FIELD] = node.node_id
        if self.enable_dense:
            entry[self.embedding_field] = node.embedding
        if self.enable_sparse:
            if isinstance(
                self.sparse_embedding_function, BaseSparseEmbeddingFunction
            ):
                entry[self.sparse_embedding_field] = (
                    self.sparse_embedding_function.encode_documents([node.text])[0]
                )
            else:  # BaseMilvusBuiltInFunction
                pass

        insert_ids.append(node.node_id)
        insert_list.append(entry)

    if self.upsert_mode:
        executor_wrapper = self.client.upsert
    else:
        executor_wrapper = self.client.insert

    # Insert or Upsert the data into milvus
    for insert_batch in iter_batch(insert_list, self.batch_size):
        executor_wrapper(
            self.collection_name,
            insert_batch,
            partition_name=add_kwargs.get("milvus_partition_name"),
        )
    if add_kwargs.get("force_flush", False):
        self.client.flush(self.collection_name)
    logger.debug(
        f"Successfully inserted embeddings into: {self.collection_name} "
        f"Num Inserted: {len(insert_list)}"
    )
    return insert_ids

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.async_add "Permanent link")

```
async_add(
    nodes: [], **add_kwargs: 
) -> []

```

Asynchronous version of the add method.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
| 
```
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
```
 | 
```
async defasync_add(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""Asynchronous version of the add method."""
    assert self._async_milvusclient is not None, (
        "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
    )
    insert_list = []
    insert_ids = []

    if self.enable_sparse is True and self.sparse_embedding_function is None:
        logger.fatal(
            "sparse_embedding_function is None when enable_sparse is True."
        )

    # Process that data we are going to insert
    for node in nodes:
        entry = node_to_metadata_dict(
            node, remove_text=True, text_field=self.text_key
        )
        entry[self.text_key] = node.dict()[self.text_key]
        entry[MILVUS_ID_FIELD] = node.node_id
        if self.enable_dense:
            entry[self.embedding_field] = node.embedding
        if self.enable_sparse:
            if isinstance(
                self.sparse_embedding_function, BaseSparseEmbeddingFunction
            ):
                entry[self.sparse_embedding_field] = (
                    self.sparse_embedding_function.encode_documents([node.text])[0]
                )
            else:  # BaseMilvusBuiltInFunction
                pass

        insert_ids.append(node.node_id)
        insert_list.append(entry)

    if self.upsert_mode:
        executor_wrapper = self.aclient.upsert
    else:
        executor_wrapper = self.aclient.insert

    # Insert or Upsert the data into milvus
    for insert_batch in iter_batch(insert_list, self.batch_size):
        await executor_wrapper(
            self.collection_name,
            insert_batch,
            partition_name=add_kwargs.get("milvus_partition_name"),
        )
    if add_kwargs.get("force_flush", False):
        raise NotImplementedError("force_flush is not supported in async mode.")
        # await self.aclient.flush(self.collection_name)
    logger.debug(
        f"Successfully inserted embeddings into: {self.collection_name} "
        f"Num Inserted: {len(insert_list)}"
    )
    return insert_ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
|  `**delete_kwargs`  |  Additional keyword arguments. - `milvus_partition_name` (Optional[str]): Specific Milvus partition.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `MilvusException`  |  Failed to delete the doc.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.
        **delete_kwargs (Any): Additional keyword arguments.
            - `milvus_partition_name` (Optional[str]): Specific Milvus partition.

    Raises:
        MilvusException: Failed to delete the doc.

    """
    # Adds ability for multiple doc delete in future.
    doc_ids: List[str]
    if isinstance(ref_doc_id, list):
        doc_ids = ref_doc_id  # type: ignore
    else:
        doc_ids = [ref_doc_id]

    # Begin by querying for the primary keys to delete
    doc_ids = ['"' + entry + '"' for entry in doc_ids]
    entries = self.client.query(
        collection_name=self.collection_name,
        filter=f"{self.doc_id_field} in [{','.join(doc_ids)}]",
    )
    if len(entries)  0:
        ids = [entry["id"] for entry in entries]
        self.client.delete(
            collection_name=self.collection_name,
            pks=ids,
            partition_name=delete_kwargs.get("milvus_partition_name"),
        )
        logger.debug(f"Successfully deleted embedding with doc_id: {doc_ids}")

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Asynchronous version of the delete method.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
| 
```
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
```
 | 
```
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Asynchronous version of the delete method."""
    assert self._async_milvusclient is not None, (
        "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
    )
    # Adds ability for multiple doc delete in future.
    doc_ids: List[str]
    if isinstance(ref_doc_id, list):
        doc_ids = ref_doc_id  # type: ignore
    else:
        doc_ids = [ref_doc_id]

    # Begin by querying for the primary keys to delete
    doc_ids = ['"' + entry + '"' for entry in doc_ids]
    entries = await self.aclient.query(
        collection_name=self.collection_name,
        filter=f"{self.doc_id_field} in [{','.join(doc_ids)}]",
    )
    if len(entries)  0:
        ids = [entry["id"] for entry in entries]
        await self.aclient.delete(
            collection_name=self.collection_name,
            pks=ids,
            partition_name=delete_kwargs.get("milvus_partition_name"),
        )
        logger.debug(f"Successfully deleted embedding with doc_id: {doc_ids}")

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.delete_nodes "Permanent link")

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
|  `**delete_kwargs`  |  Additional keyword arguments. - `milvus_partition_name` (Optional[str]): Specific Milvus partition.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
| 
```
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
        **delete_kwargs (Any): Additional keyword arguments.
            - `milvus_partition_name` (Optional[str]): Specific Milvus partition.

    """
    filters_cpy = deepcopy(filters) or MetadataFilters(filters=[])

    if node_ids:
        filters_cpy.filters.append(
            MetadataFilter(key="id", value=node_ids, operator=FilterOperator.IN)
        )

    if filters_cpy is not None:
        filter = _to_milvus_filter(filters_cpy)
    else:
        filter = None

    self.client.delete(
        collection_name=self.collection_name,
        filter=filter,
        partition_name=delete_kwargs.get("milvus_partition_name"),
        **delete_kwargs,
    )
    logger.debug(f"Successfully deleted node_ids: {node_ids}")

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Asynchronous version of the delete_nodes method.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
| 
```
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
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""Asynchronous version of the delete_nodes method."""
    assert self._async_milvusclient is not None, (
        "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
    )
    filters_cpy = deepcopy(filters) or MetadataFilters(filters=[])

    if node_ids:
        filters_cpy.filters.append(
            MetadataFilter(key="id", value=node_ids, operator=FilterOperator.IN)
        )

    if filters_cpy is not None:
        filter = _to_milvus_filter(filters_cpy)
    else:
        filter = None

    await self.aclient.delete(
        collection_name=self.collection_name,
        filter=filter,
        partition_name=delete_kwargs.get("milvus_partition_name"),
        **delete_kwargs,
    )
    logger.debug(f"Successfully deleted node_ids: {node_ids}")

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.clear "Permanent link")

```
clear() -> None

```

Clears db.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
| 
```
691
692
693
```
 | 
```
defclear(self) -> None:
"""Clears db."""
    self.client.drop_collection(self.collection_name)

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.aclear "Permanent link")

```
aclear() -> None

```

Asynchronous version of the clear method.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
| 
```
695
696
697
698
699
700
```
 | 
```
async defaclear(self) -> None:
"""Asynchronous version of the clear method."""
    assert self._async_milvusclient is not None, (
        "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
    )
    await self.aclient.drop_collection(self.collection_name)

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **kwargs
) -> []

```

Get nodes by node ids or metadata filters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  IDs of nodes to retrieve. Defaults to None.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters. Defaults to None.  |  `None`  |  
|  `**kwargs`  |  Additional keyword arguments. - `milvus_partition_names` (Optional[List[str]]): Specific Milvus partitions.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  Neither or both of node_ids and filters are provided.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[BaseNode]:  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
| 
```
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **kwargs,
) -> List[BaseNode]:
"""
    Get nodes by node ids or metadata filters.

    Args:
        node_ids (Optional[List[str]], optional): IDs of nodes to retrieve. Defaults to None.
        filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.
        **kwargs: Additional keyword arguments.
            - `milvus_partition_names` (Optional[List[str]]): Specific Milvus partitions.

    Raises:
        ValueError: Neither or both of node_ids and filters are provided.

    Returns:
        List[BaseNode]:

    """
    if node_ids is None and filters is None:
        raise ValueError("Either node_ids or filters must be provided.")

    filters_cpy = deepcopy(filters) or MetadataFilters(filters=[])
    milvus_filter = _to_milvus_filter(filters_cpy)

    if node_ids is not None and milvus_filter:
        raise ValueError("Only one of node_ids or filters can be provided.")

    res = self.client.query(
        ids=node_ids,
        collection_name=self.collection_name,
        filter=milvus_filter,
        partition_names=kwargs.get("milvus_partition_names"),
    )

    nodes = []
    for item in res:
        try:
            text_content = item.get(self.text_key)
        except Exception:
            raise ValueError(
                "The passed in text_key value does not exist "
                "in the retrieved entity."
            )
        if "_node_content" in item:
            node = metadata_dict_to_node(item, text=text_content)
        elif text_content:
            node = TextNode(
                text=text_content,
                metadata={key: item.get(key) for key in self.output_fields},
            )
        else:
            raise ValueError(
                "Node content not found in metadata dict and no text content found."
            )
        node.embedding = item.get(self.embedding_field, None)
        nodes.append(node)
    return nodes

```
 |  
| --- | --- |  
###  aget_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.aget_nodes "Permanent link")

```
aget_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **kwargs
) -> []

```

Asynchronous version of the get_nodes method.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
| 
```
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
```
 | 
```
async defaget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **kwargs,
) -> List[BaseNode]:
"""Asynchronous version of the get_nodes method."""
    assert self._async_milvusclient is not None, (
        "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
    )
    if node_ids is None and filters is None:
        raise ValueError("Either node_ids or filters must be provided.")

    filters_cpy = deepcopy(filters) or MetadataFilters(filters=[])
    milvus_filter = _to_milvus_filter(filters_cpy)

    if node_ids is not None and milvus_filter:
        raise ValueError("Only one of node_ids or filters can be provided.")

    res = await self.aclient.query(
        ids=node_ids,
        collection_name=self.collection_name,
        filter=milvus_filter,
        partition_names=kwargs.get("milvus_partition_names"),
    )

    nodes = []
    for item in res:
        try:
            text_content = item.get(self.text_key)
        except Exception:
            raise ValueError(
                "The passed in text_key value does not exist "
                "in the retrieved entity."
            )
        if "_node_content" in item:
            node = metadata_dict_to_node(item, text=text_content)
        elif text_content:
            node = TextNode(
                text=text_content,
                metadata={key: item.get(key) for key in self.output_fields},
            )
        else:
            raise ValueError(
                "Node content not found in metadata dict and no text content found."
            )
        node.embedding = item.get(self.embedding_field, None)
        nodes.append(node)
    return nodes

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_embedding`  |  `List[float]`  |  query embedding  |  _required_  |  
|  `similarity_top_k`  |  top k most similar nodes  |  _required_  |  
|  `doc_ids`  |  `Optional[List[str]]`  |  list of doc_ids to filter by  |  _required_  |  
|  `node_ids`  |  `Optional[List[str]]`  |  list of node_ids to filter by  |  _required_  |  
|  `output_fields`  |  `Optional[List[str]]`  |  list of fields to return  |  _required_  |  
|  `embedding_field`  |  `Optional[str]`  |  name of embedding field  |  _required_  |  
|  `milvus_partition_names`  |  `Optional[List[str]]`  |  specific Milvus partitions.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query_embedding (List[float]): query embedding
        similarity_top_k (int): top k most similar nodes
        doc_ids (Optional[List[str]]): list of doc_ids to filter by
        node_ids (Optional[List[str]]): list of node_ids to filter by
        output_fields (Optional[List[str]]): list of fields to return
        embedding_field (Optional[str]): name of embedding field
        milvus_partition_names (Optional[List[str]]): specific Milvus partitions.

    """
    if query.mode == VectorStoreQueryMode.DEFAULT:
        pass
    elif query.mode in [
        VectorStoreQueryMode.HYBRID,
        VectorStoreQueryMode.SPARSE,
        VectorStoreQueryMode.TEXT_SEARCH,
    ]:
        if self.enable_sparse is False:
            raise ValueError(
                f"The query mode requires sparse embedding, but enable_sparse is False."
            )
    elif query.mode == VectorStoreQueryMode.MMR:
        pass
    else:
        raise ValueError(f"Milvus does not support {query.mode} yet.")

    filter_string_expr, output_fields = self._prepare_before_search(query, **kwargs)
    custom_string_expr = kwargs.pop("string_expr", "")
    if len(filter_string_expr) != 0:
        if len(custom_string_expr) != 0:
            logger.warning(
                "string_expr in vector_store_kwargs is ignored because filters are provided."
            )
        string_expr = filter_string_expr
    else:
        string_expr = custom_string_expr

    # Perform the search
    if query.mode == VectorStoreQueryMode.MMR:
        nodes, similarities, ids = self._mmr_search(
            query, string_expr, output_fields, **kwargs
        )
    elif query.mode in [
        VectorStoreQueryMode.SPARSE,
        VectorStoreQueryMode.TEXT_SEARCH,
    ]:
        nodes, similarities, ids = self._sparse_search(
            query, string_expr, output_fields, **kwargs
        )
    elif query.mode == VectorStoreQueryMode.HYBRID:
        nodes, similarities, ids = self._hybrid_search(
            query, string_expr, output_fields, **kwargs
        )
    else:
        nodes, similarities, ids = self._default_search(
            query, string_expr, output_fields, **kwargs
        )
    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.MilvusVectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Asynchronous version of the query method.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
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
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:
"""Asynchronous version of the query method."""
    assert self._async_milvusclient is not None, (
        "Async Client should be non-null to perform async operations. Pass `use_async_client = True` to the constructor to instantiate an async client"
    )
    if query.mode == VectorStoreQueryMode.DEFAULT:
        pass
    elif query.mode in [
        VectorStoreQueryMode.HYBRID,
        VectorStoreQueryMode.SPARSE,
        VectorStoreQueryMode.TEXT_SEARCH,
    ]:
        if self.enable_sparse is False:
            raise ValueError(
                f"The query mode requires sparse embedding, but enable_sparse is False."
            )
    elif query.mode == VectorStoreQueryMode.MMR:
        pass
    else:
        raise ValueError(f"Milvus does not support {query.mode} yet.")

    string_expr, output_fields = self._prepare_before_search(query, **kwargs)

    # Perform the search
    if query.mode == VectorStoreQueryMode.MMR:
        nodes, similarities, ids = await self._async_mmr_search(
            query, string_expr, output_fields, **kwargs
        )
    elif query.mode in [
        VectorStoreQueryMode.SPARSE,
        VectorStoreQueryMode.TEXT_SEARCH,
    ]:
        nodes, similarities, ids = await self._async_sparse_search(
            query, string_expr, output_fields, **kwargs
        )
    elif query.mode == VectorStoreQueryMode.HYBRID:
        nodes, similarities, ids = await self._async_hybrid_search(
            query, string_expr, output_fields, **kwargs
        )
    else:
        nodes, similarities, ids = await self._async_default_search(
            query, string_expr, output_fields, **kwargs
        )
    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
##  IndexManagement [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/milvus/#llama_index.vector_stores.milvus.IndexManagement "Permanent link")
Bases: `Enum`
Enumeration representing the supported index management operations.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-milvus/llama_index/vector_stores/milvus/base.py`  
| 
```
66
67
68
69
70
```
 | 
```
classIndexManagement(Enum):
"""Enumeration representing the supported index management operations."""

    NO_VALIDATION = "no_validation"
    CREATE_IF_NOT_EXISTS = "create_if_not_exists"

```
 |  
| --- | --- |  
options: members: - MilvusVectorStore
