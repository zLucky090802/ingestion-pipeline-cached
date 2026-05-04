# Memgraph
##  MemgraphGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphGraphStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/kg_base.py`  
| 
```
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
```
 | 
```
classMemgraphGraphStore(GraphStore):
    def__init__(
        self,
        username: str,
        password: str,
        url: str,
        database: str = "memgraph",
        node_label: str = "Entity",
        **kwargs: Any,
    ) -> None:
        try:
            importneo4j
        except ImportError:
            raise ImportError("Please install neo4j: pip install neo4j")
        self.node_label = node_label
        self._driver = neo4j.GraphDatabase.driver(url, auth=(username, password))
        self._database = database
        self.schema = ""
        # verify connection
        try:
            self._driver.verify_connectivity()
        except neo4j.exceptions.ServiceUnavailable:
            raise ValueError(
                "Could not connect to Memgraph database. "
                "Please ensure that the url is correct"
            )
        except neo4j.exceptions.AuthError:
            raise ValueError(
                "Could not connect to Memgraph database. "
                "Please ensure that the username and password are correct"
            )
        # set schema
        self.refresh_schema()

        # create constraint
        self.query(
"""
            CREATE CONSTRAINT ON (n:%s) ASSERT n.id IS UNIQUE;

            % (self.node_label)
        )

        # create index
        self.query(
"""
            CREATE INDEX ON :%s(id);

            % (self.node_label)
        )

    @property
    defclient(self) -> Any:
        return self._driver

    defquery(self, query: str, param_map: Optional[Dict[str, Any]] = {}) -> Any:
"""Execute a Cypher query."""
        with self._driver.session(database=self._database) as session:
            result = session.run(query, param_map)
            return [record.data() for record in result]

    defget(self, subj: str) -> List[List[str]]:
"""Get triplets."""
        query = f"""
            MATCH (n1:{self.node_label})-[r]->(n2:{self.node_label})
            WHERE n1.id = $subj
            RETURN type(r), n2.id;
        """

        with self._driver.session(database=self._database) as session:
            data = session.run(query, {"subj": subj})
            return [record.values() for record in data]

    defget_rel_map(
        self, subjs: Optional[List[str]] = None, depth: int = 2
    ) -> Dict[str, List[List[str]]]:
"""Get flat relation map."""
        rel_map: Dict[Any, List[Any]] = {}
        if subjs is None or len(subjs) == 0:
            return rel_map

        query = (
            f"""MATCH p=(n1:{self.node_label})-[*1..{depth}]->() """
            f"""{"WHERE n1.id IN $subjs"ifsubjselse""} """
            "UNWIND relationships(p) AS rel "
            "WITH n1.id AS subj, collect([type(rel), endNode(rel).id]) AS rels "
            "RETURN subj, rels"
        )

        data = list(self.query(query, {"subjs": subjs}))
        if not data:
            return rel_map

        for record in data:
            rel_map[record["subj"]] = record["rels"]

        return rel_map

    defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
        query = f"""
            MERGE (n1:`{self.node_label}` {{id:$subj}})
            MERGE (n2:`{self.node_label}` {{id:$obj}})
            MERGE (n1)-[:`{rel.replace(" ","_").upper()}`]->(n2)
        """
        self.query(query, {"subj": subj, "obj": obj})

    defdelete(self, subj: str, rel: str, obj: str) -> None:
"""Delete triplet."""
        query = f"""
            MATCH (n1:`{self.node_label}`)-[r:`{rel}`]->(n2:`{self.node_label}`)
            WHERE n1.id = $subj AND n2.id = $obj
            DELETE r
        """
        self.query(query, {"subj": subj, "obj": obj})

    defrefresh_schema(self) -> None:
"""
        Refreshes the Memgraph graph schema information.
        """
        node_properties = self.query(node_properties_query)
        relationships_properties = self.query(rel_properties_query)
        relationships = self.query(rel_query)

        self.schema = f"""
        Node properties are the following:
{node_properties}
        Relationship properties are the following:
{relationships_properties}
        The relationships are the following:
{relationships}
        """

    defget_schema(self, refresh: bool = False) -> str:
"""Get the schema of the MemgraphGraph store."""
        if self.schema and not refresh:
            return self.schema
        self.refresh_schema()
        logger.debug(f"get_schema() schema:\n{self.schema}")
        return self.schema

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphGraphStore.query "Permanent link")

```
query(
    query: , param_map: Optional[[, ]] = {}
) -> 

```

Execute a Cypher query.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/kg_base.py`  
| 
```
86
87
88
89
90
```
 | 
```
defquery(self, query: str, param_map: Optional[Dict[str, Any]] = {}) -> Any:
"""Execute a Cypher query."""
    with self._driver.session(database=self._database) as session:
        result = session.run(query, param_map)
        return [record.data() for record in result]

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphGraphStore.get "Permanent link")

```
get(subj: ) -> [[]]

```

Get triplets.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/kg_base.py`  
| 
```
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
```
 | 
```
defget(self, subj: str) -> List[List[str]]:
"""Get triplets."""
    query = f"""
        MATCH (n1:{self.node_label})-[r]->(n2:{self.node_label})
        WHERE n1.id = $subj
        RETURN type(r), n2.id;
    """

    with self._driver.session(database=self._database) as session:
        data = session.run(query, {"subj": subj})
        return [record.values() for record in data]

```
 |  
| --- | --- |  
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    subjs: Optional[[]] = None, depth:  = 2
) -> [, [[]]]

```

Get flat relation map.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/kg_base.py`  
| 
```
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
```
 | 
```
defget_rel_map(
    self, subjs: Optional[List[str]] = None, depth: int = 2
) -> Dict[str, List[List[str]]]:
"""Get flat relation map."""
    rel_map: Dict[Any, List[Any]] = {}
    if subjs is None or len(subjs) == 0:
        return rel_map

    query = (
        f"""MATCH p=(n1:{self.node_label})-[*1..{depth}]->() """
        f"""{"WHERE n1.id IN $subjs"ifsubjselse""} """
        "UNWIND relationships(p) AS rel "
        "WITH n1.id AS subj, collect([type(rel), endNode(rel).id]) AS rels "
        "RETURN subj, rels"
    )

    data = list(self.query(query, {"subjs": subjs}))
    if not data:
        return rel_map

    for record in data:
        rel_map[record["subj"]] = record["rels"]

    return rel_map

```
 |  
| --- | --- |  
###  upsert_triplet [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphGraphStore.upsert_triplet "Permanent link")

```
upsert_triplet(subj: , rel: , obj: ) -> None

```

Add triplet.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/kg_base.py`  
| 
```
129
130
131
132
133
134
135
136
```
 | 
```
defupsert_triplet(self, subj: str, rel: str, obj: str) -> None:
"""Add triplet."""
    query = f"""
        MERGE (n1:`{self.node_label}` {{id:$subj}})
        MERGE (n2:`{self.node_label}` {{id:$obj}})
        MERGE (n1)-[:`{rel.replace(" ","_").upper()}`]->(n2)
    """
    self.query(query, {"subj": subj, "obj": obj})

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphGraphStore.delete "Permanent link")

```
delete(subj: , rel: , obj: ) -> None

```

Delete triplet.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/kg_base.py`  
| 
```
138
139
140
141
142
143
144
145
```
 | 
```
defdelete(self, subj: str, rel: str, obj: str) -> None:
"""Delete triplet."""
    query = f"""
        MATCH (n1:`{self.node_label}`)-[r:`{rel}`]->(n2:`{self.node_label}`)
        WHERE n1.id = $subj AND n2.id = $obj
        DELETE r
    """
    self.query(query, {"subj": subj, "obj": obj})

```
 |  
| --- | --- |  
###  refresh_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphGraphStore.refresh_schema "Permanent link")

```
refresh_schema() -> None

```

Refreshes the Memgraph graph schema information.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/kg_base.py`  
| 
```
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
```
 | 
```
defrefresh_schema(self) -> None:
"""
    Refreshes the Memgraph graph schema information.
    """
    node_properties = self.query(node_properties_query)
    relationships_properties = self.query(rel_properties_query)
    relationships = self.query(rel_query)

    self.schema = f"""
    Node properties are the following:
{node_properties}
    Relationship properties are the following:
{relationships_properties}
    The relationships are the following:
{relationships}
    """

```
 |  
| --- | --- |  
###  get_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphGraphStore.get_schema "Permanent link")

```
get_schema(refresh:  = False) -> 

```

Get the schema of the MemgraphGraph store.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/kg_base.py`  
| 
```
164
165
166
167
168
169
170
```
 | 
```
defget_schema(self, refresh: bool = False) -> str:
"""Get the schema of the MemgraphGraph store."""
    if self.schema and not refresh:
        return self.schema
    self.refresh_schema()
    logger.debug(f"get_schema() schema:\n{self.schema}")
    return self.schema

```
 |  
| --- | --- |  
##  MemgraphPropertyGraphStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphPropertyGraphStore "Permanent link")
Bases: 
Memgraph Property Graph Store.
This class implements a Memgraph property graph store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `username`  |  The username for the Memgraph database.  |  _required_  |  
|  `password`  |  The password for the Memgraph database.  |  _required_  |  
|  `url`  |  The URL for the Memgraph database.  |  _required_  |  
|  `database`  |  `Optional[str]`  |  The name of the database to connect to. Defaults to "memgraph".  |  `'memgraph'`  |  
Examples:

```
fromllama_index.core.indices.property_graphimport PropertyGraphIndex
fromllama_index.graph_stores.memgraphimport MemgraphPropertyGraphStore

# Create a MemgraphPropertyGraphStore instance
graph_store = MemgraphPropertyGraphStore(
    username="memgraph",
    password="password",
    url="bolt://localhost:7687",
    database="memgraph"
)

# Create the index
index = PropertyGraphIndex.from_documents(
    documents,
    property_graph_store=graph_store,
)

# Close the Memgraph connection explicitly.
graph_store.close()

```

Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/property_graph.py`  
| 
```
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
```
 | 
```
classMemgraphPropertyGraphStore(PropertyGraphStore):
r"""
    Memgraph Property Graph Store.

    This class implements a Memgraph property graph store.

    Args:
        username (str): The username for the Memgraph database.
        password (str): The password for the Memgraph database.
        url (str): The URL for the Memgraph database.
        database (Optional[str]): The name of the database to connect to. Defaults to "memgraph".

    Examples:
        ```python
        from llama_index.core.indices.property_graph import PropertyGraphIndex
        from llama_index.graph_stores.memgraph import MemgraphPropertyGraphStore

        # Create a MemgraphPropertyGraphStore instance
        graph_store = MemgraphPropertyGraphStore(
            username="memgraph",
            password="password",
            url="bolt://localhost:7687",
            database="memgraph"


        # Create the index
        index = PropertyGraphIndex.from_documents(
            documents,
            property_graph_store=graph_store,


        # Close the Memgraph connection explicitly.
        graph_store.close()
        ```

    """

    supports_structured_queries: bool = True
    supports_vector_queries: bool = True
    text_to_cypher_template: PromptTemplate = DEFAULT_CYPHER_TEMPALTE

    def__init__(
        self,
        username: str,
        password: str,
        url: str,
        database: Optional[str] = "memgraph",
        refresh_schema: bool = True,
        sanitize_query_output: bool = True,
        enhanced_schema: bool = False,
        create_indexes: bool = True,
        **neo4j_kwargs: Any,
    ) -> None:
        self.sanitize_query_output = sanitize_query_output
        self.enhanced_schema = enhanced_schema
        self._driver = neo4j.GraphDatabase.driver(
            url, auth=(username, password), **neo4j_kwargs
        )
        self._database = database
        self.structured_schema = {}
        if refresh_schema:
            self.refresh_schema()
        # Check if we can use vector index
        self.verify_vector_support()
        if create_indexes:
            # Create index for faster imports and retrieval
            self.structured_query(f"""CREATE INDEX ON :{BASE_NODE_LABEL}(id);""")
            self.structured_query(f"""CREATE INDEX ON :{BASE_ENTITY_LABEL}(id);""")

    @property
    defclient(self):
        return self._driver

    defclose(self) -> None:
"""Close the database driver connection."""
        self._driver.close()

    defget_schema_subset(self, schema_result: Dict[str, Any]) -> None:
"""Refresh the schema using the SHOW SCHEMA INFO."""
        # Parse the 'schema' field for each entry
        parsed_data = []
        for entry in schema_result:
            schema_str = entry.get("schema", "{}")
            try:
                parsed_schema = json.loads(schema_str)
                parsed_data.append(parsed_schema)
            except json.JSONDecodeError as decode_error:
                print(f"Failed to parse schema: {decode_error}")
                continue
        node_properties = []
        rel_properties = []
        relationships = []

        for schema in parsed_data:
            # Extract node properties
            for node in schema.get("nodes", []):
                node_label = node.get("labels", [None])[0]
                if node_label in [
                    BASE_ENTITY_LABEL,
                    BASE_NODE_LABEL,
                ]:
                    continue
                properties = [
                    {
                        "property": prop.get("key"),
                        "type": prop.get("types", [{}])[0].get("type"),
                    }
                    for prop in node.get("properties", [])
                ]
                if node_label and properties:
                    node_properties.append(
                        {"labels": node_label, "properties": properties}
                    )
            # Extract relationship properties, types & count
            for edge in schema.get("edges", []):
                rel_type = edge.get("type")
                properties = [
                    {
                        "property": prop.get("key"),
                        "type": prop.get("types", [{}])[0].get("type"),
                    }
                    for prop in edge.get("properties", [])
                ]
                if rel_type and properties:
                    rel_properties.append(
                        {"properties": properties, "type": f":`{rel_type}`"}
                    )

                start = edge.get("start_node_labels", [None])[0]
                end = edge.get("end_node_labels", [None])[0]
                if start and end and rel_type:
                    relationships.append({"start": start, "end": end, "type": rel_type})
        self.structured_schema = {
            "node_props": {el["labels"]: el["properties"] for el in node_properties},
            "rel_props": {el["type"]: el["properties"] for el in rel_properties},
            "relationships": relationships,
        }

    defrefresh_schema(self) -> None:
"""Refresh the schema."""
        # Leave schema empty if db is empty
        if self.structured_query("MATCH (n) RETURN n LIMIT 1") == []:
            return

        # First try with SHOW SCHEMA INFO
        try:
            node_query_results = self.structured_query(
                SHOW_SCHEMA_INFO,
                param_map={
                    "EXCLUDED_LABELS": [
                        BASE_ENTITY_LABEL,
                        BASE_NODE_LABEL,
                    ]
                },
            )
            if node_query_results is not None and isinstance(
                node_query_results, (str, ast.AST)
            ):
                schema_result = ast.literal_eval(node_query_results)
            else:
                schema_result = node_query_results
            assert schema_result is not None

            self.get_schema_subset(schema_result)
            return
        except neo4j.exceptions.Neo4jError as decode_error:
            if (
                decode_error.code == "Memgraph.ClientError.MemgraphError.MemgraphError"
                and "SchemaInfo disabled" in decode_error.message
            ):
                logger.info(
                    "Schema generation with SHOW SCHEMA INFO query failed. "
                    "Set --schema-info-enabled=true to use SHOW SCHEMA INFO query. "
                    "Falling back to alternative queries."
                )

        # fallback on Cypher without SHOW SCHEMA INFO
        node_query_results = self.structured_query(
            NODE_PROPERTIES_QUERY,
            param_map={
                "EXCLUDED_LABELS": [
                    BASE_ENTITY_LABEL,
                    BASE_NODE_LABEL,
                ]
            },
        )
        node_properties = {}
        for result in node_query_results:
            if result["output"]["labels"] in [
                BASE_ENTITY_LABEL,
                BASE_NODE_LABEL,
            ]:
                continue

            label = result["output"]["labels"]
            properties = result["output"]["properties"]
            if label in node_properties:
                node_properties[label]["properties"].extend(
                    prop
                    for prop in properties
                    if prop not in node_properties[label]["properties"]
                )
            else:
                node_properties[label] = {"properties": properties}

        node_properties = [
            {"labels": label, **value} for label, value in node_properties.items()
        ]
        rels_query_result = self.structured_query(REL_PROPERTIES_QUERY)
        rel_properties = (
            [
                result["output"]
                for result in rels_query_result
                if any(
                    prop["property"] for prop in result["output"].get("properties", [])
                )
            ]
            if rels_query_result
            else []
        )
        rel_objs_query_result = self.structured_query(
            REL_QUERY,
            param_map={
                "EXCLUDED_LABELS": [
                    BASE_ENTITY_LABEL,
                    BASE_NODE_LABEL,
                ]
            },
        )
        relationships = [
            el["output"]
            for el in rel_objs_query_result
            if rel_objs_query_result
            and el["output"]["start"] not in [BASE_ENTITY_LABEL, BASE_NODE_LABEL]
            and el["output"]["end"] not in [BASE_ENTITY_LABEL, BASE_NODE_LABEL]
        ]
        self.structured_schema = {
            "node_props": {el["labels"]: el["properties"] for el in node_properties},
            "rel_props": {el["type"]: el["properties"] for el in rel_properties},
            "relationships": relationships,
        }

    defupsert_nodes(self, nodes: List[LabelledNode]) -> None:
        # Lists to hold separated types
        entity_dicts: List[dict] = []
        chunk_dicts: List[dict] = []

        # Sort by type
        for item in nodes:
            if isinstance(item, EntityNode):
                entity_dicts.append({**item.dict(), "id": item.id})
            elif isinstance(item, ChunkNode):
                chunk_dicts.append({**item.dict(), "id": item.id})
            else:
                pass
        if chunk_dicts:
            for index in range(0, len(chunk_dicts), CHUNK_SIZE):
                chunked_params = chunk_dicts[index : index + CHUNK_SIZE]
                self.structured_query(
                    f"""
                    UNWIND $data AS row
                    MERGE (c:{BASE_NODE_LABEL}{{id: row.id}})
                    SET c.`text` = row.text, c:Chunk
                    WITH c, row
                    SET c += row.properties
                    WITH c, row.embedding as embedding
                    WHERE embedding IS NOT NULL
                    SET c.embedding = embedding
                    RETURN count(*)
,
                    param_map={"data": chunked_params},
                )

        if entity_dicts:
            for index in range(0, len(entity_dicts), CHUNK_SIZE):
                chunked_params = entity_dicts[index : index + CHUNK_SIZE]
                self.structured_query(
                    f"""
                    UNWIND $data AS row
                    MERGE (e:{BASE_NODE_LABEL}{{id: row.id}})
                    SET e += CASE WHEN row.properties IS NOT NULL THEN row.properties ELSE e END
                    SET e.name = CASE WHEN row.name IS NOT NULL THEN row.name ELSE e.name END,
{BASE_ENTITY_LABEL}
                    WITH e, row
                    SET e:row.label
                    WITH e, row
                    WHERE row.embedding IS NOT NULL
                    SET e.embedding = row.embedding
                    WITH e, row
                    WHERE row.properties.triplet_source_id IS NOT NULL
                    MERGE (c:{BASE_NODE_LABEL}{{id: row.properties.triplet_source_id}})
                    MERGE (e)<-[:MENTIONS]-(c)
,
                    param_map={"data": chunked_params},
                )

    defupsert_relations(self, relations: List[Relation]) -> None:
"""Add relations."""
        params = [r.dict() for r in relations]
        for index in range(0, len(params), CHUNK_SIZE):
            chunked_params = params[index : index + CHUNK_SIZE]

            self.structured_query(
                f"""
                UNWIND $data AS row
                MERGE (source: {BASE_NODE_LABEL}{{id: row.source_id}})
                ON CREATE SET source:Chunk
                MERGE (target: {BASE_NODE_LABEL}{{id: row.target_id}})
                ON CREATE SET target:Chunk
                WITH source, target, row
                CREATE (source)-[r:row.label]->(target)
                SET r += row.properties
                RETURN count(*)
,
                param_map={"data": chunked_params},
            )

    defget(
        self,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[LabelledNode]:
"""Get nodes."""
        cypher_statement = f"MATCH (e:{BASE_NODE_LABEL}) "

        params = {}
        cypher_statement += "WHERE e.id IS NOT NULL "

        if ids:
            cypher_statement += "AND e.id IN $ids "
            params["ids"] = ids

        if properties:
            prop_list = []
            for i, prop in enumerate(properties):
                prop_list.append(f"e.`{prop}` = $property_{i}")
                params[f"property_{i}"] = properties[prop]
            cypher_statement += " AND " + " AND ".join(prop_list)

        return_statement = """
            RETURN
            e.id AS name,
            CASE
                WHEN labels(e)[0] IN ['__Entity__', '__Node__'] THEN
                    CASE
                        WHEN size(labels(e)) > 2 THEN labels(e)[2]
                        WHEN size(labels(e)) > 1 THEN labels(e)[1]
                        ELSE NULL

                ELSE labels(e)[0]
            END AS type,
            properties(e) AS properties
        """
        cypher_statement += return_statement
        response = self.structured_query(cypher_statement, param_map=params)
        response = response if response else []

        nodes = []
        for record in response:
            if "text" in record["properties"] or record["type"] is None:
                text = record["properties"].pop("text", "")
                nodes.append(
                    ChunkNode(
                        id_=record["name"],
                        text=text,
                        properties=remove_empty_values(record["properties"]),
                    )
                )
            else:
                nodes.append(
                    EntityNode(
                        name=record["name"],
                        label=record["type"],
                        properties=remove_empty_values(record["properties"]),
                    )
                )

        return nodes

    defget_triplets(
        self,
        entity_names: Optional[List[str]] = None,
        relation_names: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> List[Triplet]:
        cypher_statement = f"MATCH (e:`{BASE_ENTITY_LABEL}`)-[r]->(t) "

        params = {}
        if entity_names or relation_names or properties or ids:
            cypher_statement += "WHERE "

        if entity_names:
            cypher_statement += "e.name in $entity_names "
            params["entity_names"] = entity_names

        if relation_names and entity_names:
            cypher_statement += "AND "

        if relation_names:
            cypher_statement += "type(r) in $relation_names "
            params["relation_names"] = relation_names

        if ids:
            cypher_statement += "e.id in $ids "
            params["ids"] = ids

        if properties:
            prop_list = []
            for i, prop in enumerate(properties):
                prop_list.append(f"e.`{prop}` = $property_{i}")
                params[f"property_{i}"] = properties[prop]
            cypher_statement += " AND ".join(prop_list)

        if not (entity_names or properties or relation_names or ids):
            return_statement = """
                WHERE NOT ANY(label IN labels(e) WHERE label = 'Chunk')
                RETURN type(r) as type, properties(r) as rel_prop, e.id as source_id,
                CASE
                    WHEN labels(e)[0] IN ['__Entity__', '__Node__'] THEN

                            WHEN size(labels(e)) > 2 THEN labels(e)[2]
                            WHEN size(labels(e)) > 1 THEN labels(e)[1]
                            ELSE NULL

                    ELSE labels(e)[0]
                END AS source_type,
                properties(e) AS source_properties,
                t.id as target_id,
                CASE
                    WHEN labels(t)[0] IN ['__Entity__', '__Node__'] THEN

                            WHEN size(labels(t)) > 2 THEN labels(t)[2]
                            WHEN size(labels(t)) > 1 THEN labels(t)[1]
                            ELSE NULL

                    ELSE labels(t)[0]
                END AS target_type, properties(t) AS target_properties LIMIT 100;

        else:
            return_statement = """
            AND NOT ANY(label IN labels(e) WHERE label = 'Chunk')
                RETURN type(r) as type, properties(r) as rel_prop, e.id as source_id,
                CASE
                    WHEN labels(e)[0] IN ['__Entity__', '__Node__'] THEN

                            WHEN size(labels(e)) > 2 THEN labels(e)[2]
                            WHEN size(labels(e)) > 1 THEN labels(e)[1]
                            ELSE NULL

                    ELSE labels(e)[0]
                END AS source_type,
                properties(e) AS source_properties,
                t.id as target_id,
                CASE
                    WHEN labels(t)[0] IN ['__Entity__', '__Node__'] THEN

                            WHEN size(labels(t)) > 2 THEN labels(t)[2]
                            WHEN size(labels(t)) > 1 THEN labels(t)[1]
                            ELSE NULL

                    ELSE labels(t)[0]
                END AS target_type, properties(t) AS target_properties LIMIT 100;


        cypher_statement += return_statement
        data = self.structured_query(cypher_statement, param_map=params)
        data = data if data else []

        triplets = []
        for record in data:
            source = EntityNode(
                name=record["source_id"],
                label=record["source_type"],
                properties=remove_empty_values(record["source_properties"]),
            )
            target = EntityNode(
                name=record["target_id"],
                label=record["target_type"],
                properties=remove_empty_values(record["target_properties"]),
            )
            rel = Relation(
                source_id=record["source_id"],
                target_id=record["target_id"],
                label=record["type"],
                properties=remove_empty_values(record["rel_prop"]),
            )
            triplets.append([source, rel, target])
        return triplets

    defget_rel_map(
        self,
        graph_nodes: List[LabelledNode],
        depth: int = 2,
        limit: int = 30,
        ignore_rels: Optional[List[str]] = None,
    ) -> List[Triplet]:
"""Get depth-aware rel map."""
        triples = []

        ids = [node.id for node in graph_nodes]
        response = self.structured_query(
            f"""
            WITH $ids AS id_list
            UNWIND range(0, size(id_list) - 1) AS idx
            MATCH (e:__Node__)
            WHERE e.id = id_list[idx]
            MATCH p=(e)-[r*1..{depth}]-(other)
            WHERE ALL(rel in relationships(p) WHERE type(rel) <> 'MENTIONS')
            UNWIND relationships(p) AS rel
            WITH DISTINCT rel, idx
            WITH startNode(rel) AS source,
                type(rel) AS type,
{{.*}} AS rel_properties,
                endNode(rel) AS endNode,

            LIMIT toInteger($limit)
            RETURN source.id AS source_id,
                CASE
                    WHEN labels(source)[0] IN ['__Entity__', '__Node__'] THEN

                            WHEN size(labels(source)) > 2 THEN labels(source)[2]
                            WHEN size(labels(source)) > 1 THEN labels(source)[1]
                            ELSE NULL

                    ELSE labels(source)[0]
                END AS source_type,
                properties(source) AS source_properties,
                type,
                rel_properties,
                endNode.id AS target_id,
                CASE
                    WHEN labels(endNode)[0] IN ['__Entity__', '__Node__'] THEN

                            WHEN size(labels(endNode)) > 2 THEN labels(endNode)[2]
                            WHEN size(labels(endNode)) > 1 THEN labels(endNode)[1] ELSE NULL

                    ELSE labels(endNode)[0]
                END AS target_type,
                properties(endNode) AS target_properties,

            ORDER BY idx
            LIMIT toInteger($limit)
,
            param_map={"ids": ids, "limit": limit},
        )
        response = response if response else []

        ignore_rels = ignore_rels or []
        for record in response:
            if record["type"] in ignore_rels:
                continue

            source = EntityNode(
                name=record["source_id"],
                label=record["source_type"],
                properties=remove_empty_values(record["source_properties"]),
            )
            target = EntityNode(
                name=record["target_id"],
                label=record["target_type"],
                properties=remove_empty_values(record["target_properties"]),
            )
            rel = Relation(
                source_id=record["source_id"],
                target_id=record["target_id"],
                label=record["type"],
                properties=remove_empty_values(record["rel_properties"]),
            )
            triples.append([source, rel, target])

        return triples

    defstructured_query(
        self, query: str, param_map: Optional[Dict[str, Any]] = None
    ) -> Any:
        param_map = param_map or {}

        with self._driver.session(database=self._database) as session:
            result = session.run(query, param_map)
            full_result = [d.data() for d in result]

        if self.sanitize_query_output:
            return [value_sanitize(el) for el in full_result]
        return full_result

    defvector_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> Tuple[List[LabelledNode], List[float]]:
"""Query the graph store with a vector store query."""
        if self._supports_vector_index:
            data = self.structured_query(
                f"""CALL vector_search.search('{VECTOR_INDEX_NAME}', $limit, $embedding)
                    YIELD node, similarity
                    WITH node, similarity, labels(node) AS all_labels
                    UNWIND all_labels AS label
                    WITH node, similarity, label
                    WHERE NOT label IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}']
                    WITH node, similarity, label, properties(node) AS originalProperties
                    RETURN
                        node.id AS name,
                        label AS type,
{{.* , embedding: Null, name: Null, id: Null}} AS properties,
                        similarity
,
                param_map={
                    "embedding": query.query_embedding,
                    "limit": query.similarity_top_k,
                },
            )
        else:
            data = []
        data = data if data else []

        nodes = []
        scores = []
        for record in data:
            node = EntityNode(
                name=record["name"],
                label=record["type"],
                properties=remove_empty_values(record["properties"]),
            )
            nodes.append(node)
            scores.append(record["similarity"])

        return (nodes, scores)

    defdelete(
        self,
        entity_names: Optional[List[str]] = None,
        relation_names: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
"""Delete matching data."""
        if entity_names:
            self.structured_query(
                "MATCH (n) WHERE n.name IN $entity_names DETACH DELETE n",
                param_map={"entity_names": entity_names},
            )
        if ids:
            self.structured_query(
                "MATCH (n) WHERE n.id IN $ids DETACH DELETE n",
                param_map={"ids": ids},
            )
        if relation_names:
            for rel in relation_names:
                self.structured_query(f"MATCH ()-[r:`{rel}`]->() DELETE r")

        if properties:
            cypher = "MATCH (e) WHERE "
            prop_list = []
            params = {}
            for i, prop in enumerate(properties):
                prop_list.append(f"e.`{prop}` = $property_{i}")
                params[f"property_{i}"] = properties[prop]
            cypher += " AND ".join(prop_list)
            self.structured_query(cypher + " DETACH DELETE e", param_map=params)

    def_enhanced_schema_cypher(
        self,
        label_or_type: str,
        properties: List[Dict[str, Any]],
        exhaustive: bool,
        is_relationship: bool = False,
    ) -> str:
        if is_relationship:
            match_clause = f"MATCH ()-[n:`{label_or_type}`]->()"
        else:
            match_clause = f"MATCH (n:`{label_or_type}`)"

        with_clauses = []
        return_clauses = []
        output_dict = {}
        if exhaustive:
            for prop in properties:
                if prop["property"]:
                    prop_name = prop["property"]
                else:
                    prop_name = None
                if prop["type"]:
                    prop_type = prop["type"]
                else:
                    prop_type = None
                if prop_type == "String":
                    with_clauses.append(
                        f"collect(distinct substring(toString(n.`{prop_name}`), 0, 50)) "
                        f"AS `{prop_name}_values`"
                    )
                    return_clauses.append(
                        f"values:`{prop_name}_values`[..{DISTINCT_VALUE_LIMIT}],"
                        f" distinct_count: size(`{prop_name}_values`)"
                    )
                elif prop_type in [
                    "Integer",
                    "Int",
                    "Double",
                    "Float",
                    "Date",
                    "LocalTime",
                    "LocalDateTime",
                ]:
                    with_clauses.append(f"min(n.`{prop_name}`) AS `{prop_name}_min`")
                    with_clauses.append(f"max(n.`{prop_name}`) AS `{prop_name}_max`")
                    with_clauses.append(
                        f"count(distinct n.`{prop_name}`) AS `{prop_name}_distinct`"
                    )
                    return_clauses.append(
                        f"min: toString(`{prop_name}_min`), "
                        f"max: toString(`{prop_name}_max`), "
                        f"distinct_count: `{prop_name}_distinct`"
                    )
                elif prop_type in ["List", "List[Any]"]:
                    with_clauses.append(
                        f"min(size(n.`{prop_name}`)) AS `{prop_name}_size_min`, "
                        f"max(size(n.`{prop_name}`)) AS `{prop_name}_size_max`"
                    )
                    return_clauses.append(
                        f"min_size: `{prop_name}_size_min`, "
                        f"max_size: `{prop_name}_size_max`"
                    )
                elif prop_type in ["Bool", "Duration"]:
                    continue
                if return_clauses:
                    output_dict[prop_name] = "{" + return_clauses.pop() + "}"
                else:
                    output_dict[prop_name] = None
        else:
            # Just sample 5 random nodes
            match_clause += " WITH n LIMIT 5"
            for prop in properties:
                prop_name = prop["property"]
                prop_type = prop["type"]
                # Check if indexed property, we can still do exhaustive
                prop_index = [
                    el
                    for el in self.structured_schema["metadata"]["index"]
                    if el["label"] == label_or_type
                    and el["properties"] == [prop_name]
                    and el["type"] == "RANGE"
                ]
                if prop_type == "String":
                    if (
                        prop_index
                        and prop_index[0].get("size")  0
                        and prop_index[0].get("distinctValues") <= DISTINCT_VALUE_LIMIT
                    ):
                        distinct_values_query = f"""
                            MATCH (n:{label_or_type})
                            RETURN DISTINCT n.`{prop_name}` AS value
                            LIMIT {DISTINCT_VALUE_LIMIT}

                        distinct_values = self.structured_query(distinct_values_query)

                        # Extract values from the result set
                        distinct_values = [
                            record["value"] for record in distinct_values
                        ]

                        return_clauses.append(
                            f"values: {distinct_values},"
                            f" distinct_count: {len(distinct_values)}"
                        )
                    else:
                        with_clauses.append(
                            f"collect(distinct substring(n.`{prop_name}`, 0, 50)) "
                            f"AS `{prop_name}_values`"
                        )
                        return_clauses.append(f"values: `{prop_name}_values`")
                elif prop_type in [
                    "Integer",
                    "Int",
                    "Double",
                    "Float",
                    "Date",
                    "LocalTime",
                    "LocalDateTime",
                ]:
                    if not prop_index:
                        with_clauses.append(
                            f"collect(distinct toString(n.`{prop_name}`)) "
                            f"AS `{prop_name}_values`"
                        )
                        return_clauses.append(f"values: `{prop_name}_values`")
                    else:
                        with_clauses.append(
                            f"min(n.`{prop_name}`) AS `{prop_name}_min`"
                        )
                        with_clauses.append(
                            f"max(n.`{prop_name}`) AS `{prop_name}_max`"
                        )
                        with_clauses.append(
                            f"count(distinct n.`{prop_name}`) AS `{prop_name}_distinct`"
                        )
                        return_clauses.append(
                            f"min: toString(`{prop_name}_min`), "
                            f"max: toString(`{prop_name}_max`), "
                            f"distinct_count: `{prop_name}_distinct`"
                        )

                elif prop_type in ["List", "List[Any]"]:
                    with_clauses.append(
                        f"min(size(n.`{prop_name}`)) AS `{prop_name}_size_min`, "
                        f"max(size(n.`{prop_name}`)) AS `{prop_name}_size_max`"
                    )
                    return_clauses.append(
                        f"min_size: `{prop_name}_size_min`, "
                        f"max_size: `{prop_name}_size_max`"
                    )
                elif prop_type in ["Bool", "Duration"]:
                    continue
                if return_clauses:
                    output_dict[prop_name] = "{" + return_clauses.pop() + "}"
                else:
                    output_dict[prop_name] = None

        with_clause = "WITH " + ",\n.join(with_clauses)
        return_clause = (
            "RETURN {"
            + ", ".join(f"`{k}`: {v}" for k, v in output_dict.items())
            + "} AS output"
        )
        # Combine all parts of the Cypher query
        return f"{match_clause}\n{with_clause}\n{return_clause}"

    defget_schema(self, refresh: bool = False) -> Any:
        if refresh:
            self.refresh_schema()

        return self.structured_schema

    defget_schema_str(self, refresh: bool = False) -> str:
        schema = self.get_schema(refresh=refresh)

        formatted_node_props = []
        formatted_rel_props = []

        if self.enhanced_schema:
            # Enhanced formatting for nodes
            for node_type, properties in schema["node_props"].items():
                formatted_node_props.append(f"- **{node_type}**")
                for prop in properties:
                    example = ""
                    if prop["type"] == "String" and prop.get("values"):
                        if prop.get("distinct_count", 11)  DISTINCT_VALUE_LIMIT:
                            example = (
                                f'Example: "{clean_string_values(prop["values"][0])}"'
                                if prop["values"]
                                else ""
                            )
                        else:  # If less than 10 possible values return all
                            example = (
                                (
                                    "Available options: "
                                    f"{[clean_string_values(el)forelinprop['values']]}"
                                )
                                if prop["values"]
                                else ""
                            )

                    elif prop["type"] in [
                        "Integer",
                        "Int",
                        "Double",
                        "Float",
                        "Date",
                        "LocalTime",
                        "LocalDateTime",
                    ]:
                        if prop.get("min") is not None:
                            example = f"Min: {prop['min']}, Max: {prop['max']}"
                        else:
                            example = (
                                f'Example: "{prop["values"][0]}"'
                                if prop.get("values")
                                else ""
                            )
                    elif prop["type"] in ["List", "List[Any]"]:
                        # Skip embeddings
                        if not prop.get("min_size") or prop["min_size"]  LIST_LIMIT:
                            continue
                        example = f"Min Size: {prop['min_size']}, Max Size: {prop['max_size']}"
                    formatted_node_props.append(
                        f"  - `{prop['property']}`: {prop['type']}{example}"
                    )

            # Enhanced formatting for relationships
            for rel_type, properties in schema["rel_props"].items():
                formatted_rel_props.append(f"- **{rel_type}**")
                for prop in properties:
                    example = ""
                    if prop["type"] == "STRING":
                        if prop.get("distinct_count", 11)  DISTINCT_VALUE_LIMIT:
                            example = (
                                f'Example: "{clean_string_values(prop["values"][0])}"'
                                if prop.get("values")
                                else ""
                            )
                        else:  # If less than 10 possible values return all
                            example = (
                                (
                                    "Available options: "
                                    f"{[clean_string_values(el)forelinprop['values']]}"
                                )
                                if prop.get("values")
                                else ""
                            )
                    elif prop["type"] in [
                        "Integer",
                        "Int",
                        "Double",
                        "Float",
                        "Date",
                        "LocalTime",
                        "LocalDateTime",
                    ]:
                        if prop.get("min"):  # If we have min/max
                            example = f"Min: {prop['min']}, Max:  {prop['max']}"
                        else:  # return a single value
                            example = (
                                f'Example: "{prop["values"][0]}"'
                                if prop.get("values")
                                else ""
                            )
                    elif prop["type"] == "List[Any]":
                        # Skip embeddings
                        if prop["min_size"]  LIST_LIMIT:
                            continue
                        example = f"Min Size: {prop['min_size']}, Max Size: {prop['max_size']}"
                    formatted_rel_props.append(
                        f"  - `{prop['property']}: {prop['type']}` {example}"
                    )
        else:
            # Format node properties
            for label, props in schema["node_props"].items():
                props_str = ", ".join(
                    [f"{prop['property']}: {prop['type']}" for prop in props]
                )
                formatted_node_props.append(f"{label}{{{props_str}}}")

            # Format relationship properties using structured_schema
            for label, props in schema["rel_props"].items():
                props_str = ", ".join(
                    [f"{prop['property']}: {prop['type']}" for prop in props]
                )
                formatted_rel_props.append(f"{label}{{{props_str}}}")

        # Format relationships
        formatted_rels = [
            f"(:{el['start']})-[:{el['type']}]->(:{el['end']})"
            for el in schema["relationships"]
        ]

        return "\n".join(
            [
                "Node properties:",
                "\n".join(formatted_node_props),
                "Relationship properties:",
                "\n".join(formatted_rel_props),
                "The relationships:",
                "\n".join(formatted_rels),
            ]
        )

    defverify_vector_support(self) -> None:
"""
        Check if the connected Memgraph database supports vector indices.

        Compares the current version with the required version (2.22.0) that
        supports vector indexing.
        """
        response = self.structured_query("SHOW VERSION;")
        current_version = response[0]["version"]
        current_version = tuple(map(int, current_version.split(".")))
        required_version = "2.22"
        required_version = tuple(map(int, required_version.split(".")))

        # Check if the version is equal to or larger than the required version
        if current_version >= required_version:
            # Check if vector index is configured
            try:
                self.structured_query(
                    f"""
                    CREATE VECTOR INDEX {VECTOR_INDEX_NAME} ON :{BASE_ENTITY_LABEL}(embedding) WITH CONFIG {{"dimension": 1536, "capacity": 1000}};

                )
                self._supports_vector_index = True
                logger.info(
                    "Vector index %s was created with a fixed embedding dimension of 1536. "
                    "If your chosen LLM model uses a different dimension, manually create the vector index with the following query:\n"
                    'CREATE VECTOR INDEX %s ON :%s(embedding) WITH CONFIG {"dimension": <INSERT_DIMENSION>, "capacity": 1000};',
                    VECTOR_INDEX_NAME,
                    VECTOR_INDEX_NAME,
                    BASE_ENTITY_LABEL,
                )
            except neo4j.exceptions.Neo4jError as decode_error:
                self._supports_vector_index = False
                if (
                    decode_error.code
                    == "Memgraph.ClientError.MemgraphError.MemgraphError"
                    and "vector_search.show_index_info" in decode_error.message
                ):
                    logger.info(
"""Failed to create vector index entity:
                        Given vector index already exists."""
                    )
        else:
            self._supports_vector_index = False
            logger.info(
"""Vector indexing is not supported by your current Memgraph
                version (%s). Please upgrade to version 2.22.0 or newer to use
                vector indices.""",
                ".".join(map(str, current_version)),
            )

```
 |  
| --- | --- |  
###  close [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphPropertyGraphStore.close "Permanent link")

```
close() -> None

```

Close the database driver connection.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/property_graph.py`  
| 
```
148
149
150
```
 | 
```
defclose(self) -> None:
"""Close the database driver connection."""
    self._driver.close()

```
 |  
| --- | --- |  
###  get_schema_subset [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphPropertyGraphStore.get_schema_subset "Permanent link")

```
get_schema_subset(schema_result: [, ]) -> None

```

Refresh the schema using the SHOW SCHEMA INFO.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/property_graph.py`  
| 
```
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
```
 | 
```
defget_schema_subset(self, schema_result: Dict[str, Any]) -> None:
"""Refresh the schema using the SHOW SCHEMA INFO."""
    # Parse the 'schema' field for each entry
    parsed_data = []
    for entry in schema_result:
        schema_str = entry.get("schema", "{}")
        try:
            parsed_schema = json.loads(schema_str)
            parsed_data.append(parsed_schema)
        except json.JSONDecodeError as decode_error:
            print(f"Failed to parse schema: {decode_error}")
            continue
    node_properties = []
    rel_properties = []
    relationships = []

    for schema in parsed_data:
        # Extract node properties
        for node in schema.get("nodes", []):
            node_label = node.get("labels", [None])[0]
            if node_label in [
                BASE_ENTITY_LABEL,
                BASE_NODE_LABEL,
            ]:
                continue
            properties = [
                {
                    "property": prop.get("key"),
                    "type": prop.get("types", [{}])[0].get("type"),
                }
                for prop in node.get("properties", [])
            ]
            if node_label and properties:
                node_properties.append(
                    {"labels": node_label, "properties": properties}
                )
        # Extract relationship properties, types & count
        for edge in schema.get("edges", []):
            rel_type = edge.get("type")
            properties = [
                {
                    "property": prop.get("key"),
                    "type": prop.get("types", [{}])[0].get("type"),
                }
                for prop in edge.get("properties", [])
            ]
            if rel_type and properties:
                rel_properties.append(
                    {"properties": properties, "type": f":`{rel_type}`"}
                )

            start = edge.get("start_node_labels", [None])[0]
            end = edge.get("end_node_labels", [None])[0]
            if start and end and rel_type:
                relationships.append({"start": start, "end": end, "type": rel_type})
    self.structured_schema = {
        "node_props": {el["labels"]: el["properties"] for el in node_properties},
        "rel_props": {el["type"]: el["properties"] for el in rel_properties},
        "relationships": relationships,
    }

```
 |  
| --- | --- |  
###  refresh_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphPropertyGraphStore.refresh_schema "Permanent link")

```
refresh_schema() -> None

```

Refresh the schema.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/property_graph.py`  
| 
```
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
```
 | 
```
defrefresh_schema(self) -> None:
"""Refresh the schema."""
    # Leave schema empty if db is empty
    if self.structured_query("MATCH (n) RETURN n LIMIT 1") == []:
        return

    # First try with SHOW SCHEMA INFO
    try:
        node_query_results = self.structured_query(
            SHOW_SCHEMA_INFO,
            param_map={
                "EXCLUDED_LABELS": [
                    BASE_ENTITY_LABEL,
                    BASE_NODE_LABEL,
                ]
            },
        )
        if node_query_results is not None and isinstance(
            node_query_results, (str, ast.AST)
        ):
            schema_result = ast.literal_eval(node_query_results)
        else:
            schema_result = node_query_results
        assert schema_result is not None

        self.get_schema_subset(schema_result)
        return
    except neo4j.exceptions.Neo4jError as decode_error:
        if (
            decode_error.code == "Memgraph.ClientError.MemgraphError.MemgraphError"
            and "SchemaInfo disabled" in decode_error.message
        ):
            logger.info(
                "Schema generation with SHOW SCHEMA INFO query failed. "
                "Set --schema-info-enabled=true to use SHOW SCHEMA INFO query. "
                "Falling back to alternative queries."
            )

    # fallback on Cypher without SHOW SCHEMA INFO
    node_query_results = self.structured_query(
        NODE_PROPERTIES_QUERY,
        param_map={
            "EXCLUDED_LABELS": [
                BASE_ENTITY_LABEL,
                BASE_NODE_LABEL,
            ]
        },
    )
    node_properties = {}
    for result in node_query_results:
        if result["output"]["labels"] in [
            BASE_ENTITY_LABEL,
            BASE_NODE_LABEL,
        ]:
            continue

        label = result["output"]["labels"]
        properties = result["output"]["properties"]
        if label in node_properties:
            node_properties[label]["properties"].extend(
                prop
                for prop in properties
                if prop not in node_properties[label]["properties"]
            )
        else:
            node_properties[label] = {"properties": properties}

    node_properties = [
        {"labels": label, **value} for label, value in node_properties.items()
    ]
    rels_query_result = self.structured_query(REL_PROPERTIES_QUERY)
    rel_properties = (
        [
            result["output"]
            for result in rels_query_result
            if any(
                prop["property"] for prop in result["output"].get("properties", [])
            )
        ]
        if rels_query_result
        else []
    )
    rel_objs_query_result = self.structured_query(
        REL_QUERY,
        param_map={
            "EXCLUDED_LABELS": [
                BASE_ENTITY_LABEL,
                BASE_NODE_LABEL,
            ]
        },
    )
    relationships = [
        el["output"]
        for el in rel_objs_query_result
        if rel_objs_query_result
        and el["output"]["start"] not in [BASE_ENTITY_LABEL, BASE_NODE_LABEL]
        and el["output"]["end"] not in [BASE_ENTITY_LABEL, BASE_NODE_LABEL]
    ]
    self.structured_schema = {
        "node_props": {el["labels"]: el["properties"] for el in node_properties},
        "rel_props": {el["type"]: el["properties"] for el in rel_properties},
        "relationships": relationships,
    }

```
 |  
| --- | --- |  
###  upsert_relations [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphPropertyGraphStore.upsert_relations "Permanent link")

```
upsert_relations(relations: []) -> None

```

Add relations.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/property_graph.py`  
| 
```
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
```
 | 
```
defupsert_relations(self, relations: List[Relation]) -> None:
"""Add relations."""
    params = [r.dict() for r in relations]
    for index in range(0, len(params), CHUNK_SIZE):
        chunked_params = params[index : index + CHUNK_SIZE]

        self.structured_query(
            f"""
            UNWIND $data AS row
            MERGE (source: {BASE_NODE_LABEL}{{id: row.source_id}})
            ON CREATE SET source:Chunk
            MERGE (target: {BASE_NODE_LABEL}{{id: row.target_id}})
            ON CREATE SET target:Chunk
            WITH source, target, row
            CREATE (source)-[r:row.label]->(target)
            SET r += row.properties
            RETURN count(*)
,
            param_map={"data": chunked_params},
        )

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphPropertyGraphStore.get "Permanent link")

```
get(
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> []

```

Get nodes.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/property_graph.py`  
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
```
 | 
```
defget(
    self,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> List[LabelledNode]:
"""Get nodes."""
    cypher_statement = f"MATCH (e:{BASE_NODE_LABEL}) "

    params = {}
    cypher_statement += "WHERE e.id IS NOT NULL "

    if ids:
        cypher_statement += "AND e.id IN $ids "
        params["ids"] = ids

    if properties:
        prop_list = []
        for i, prop in enumerate(properties):
            prop_list.append(f"e.`{prop}` = $property_{i}")
            params[f"property_{i}"] = properties[prop]
        cypher_statement += " AND " + " AND ".join(prop_list)

    return_statement = """
        RETURN
        e.id AS name,
        CASE
            WHEN labels(e)[0] IN ['__Entity__', '__Node__'] THEN
                CASE
                    WHEN size(labels(e)) > 2 THEN labels(e)[2]
                    WHEN size(labels(e)) > 1 THEN labels(e)[1]
                    ELSE NULL

            ELSE labels(e)[0]
        END AS type,
        properties(e) AS properties
    """
    cypher_statement += return_statement
    response = self.structured_query(cypher_statement, param_map=params)
    response = response if response else []

    nodes = []
    for record in response:
        if "text" in record["properties"] or record["type"] is None:
            text = record["properties"].pop("text", "")
            nodes.append(
                ChunkNode(
                    id_=record["name"],
                    text=text,
                    properties=remove_empty_values(record["properties"]),
                )
            )
        else:
            nodes.append(
                EntityNode(
                    name=record["name"],
                    label=record["type"],
                    properties=remove_empty_values(record["properties"]),
                )
            )

    return nodes

```
 |  
| --- | --- |  
###  get_rel_map [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphPropertyGraphStore.get_rel_map "Permanent link")

```
get_rel_map(
    graph_nodes: [],
    depth:  = 2,
    limit:  = 30,
    ignore_rels: Optional[[]] = None,
) -> [Triplet]

```

Get depth-aware rel map.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/property_graph.py`  
| 
```
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
```
 | 
```
defget_rel_map(
    self,
    graph_nodes: List[LabelledNode],
    depth: int = 2,
    limit: int = 30,
    ignore_rels: Optional[List[str]] = None,
) -> List[Triplet]:
"""Get depth-aware rel map."""
    triples = []

    ids = [node.id for node in graph_nodes]
    response = self.structured_query(
        f"""
        WITH $ids AS id_list
        UNWIND range(0, size(id_list) - 1) AS idx
        MATCH (e:__Node__)
        WHERE e.id = id_list[idx]
        MATCH p=(e)-[r*1..{depth}]-(other)
        WHERE ALL(rel in relationships(p) WHERE type(rel) <> 'MENTIONS')
        UNWIND relationships(p) AS rel
        WITH DISTINCT rel, idx
        WITH startNode(rel) AS source,
            type(rel) AS type,
{{.*}} AS rel_properties,
            endNode(rel) AS endNode,

        LIMIT toInteger($limit)
        RETURN source.id AS source_id,
            CASE
                WHEN labels(source)[0] IN ['__Entity__', '__Node__'] THEN
                    CASE
                        WHEN size(labels(source)) > 2 THEN labels(source)[2]
                        WHEN size(labels(source)) > 1 THEN labels(source)[1]
                        ELSE NULL

                ELSE labels(source)[0]
            END AS source_type,
            properties(source) AS source_properties,
            type,
            rel_properties,
            endNode.id AS target_id,
            CASE
                WHEN labels(endNode)[0] IN ['__Entity__', '__Node__'] THEN
                    CASE
                        WHEN size(labels(endNode)) > 2 THEN labels(endNode)[2]
                        WHEN size(labels(endNode)) > 1 THEN labels(endNode)[1] ELSE NULL

                ELSE labels(endNode)[0]
            END AS target_type,
            properties(endNode) AS target_properties,

        ORDER BY idx
        LIMIT toInteger($limit)
        """,
        param_map={"ids": ids, "limit": limit},
    )
    response = response if response else []

    ignore_rels = ignore_rels or []
    for record in response:
        if record["type"] in ignore_rels:
            continue

        source = EntityNode(
            name=record["source_id"],
            label=record["source_type"],
            properties=remove_empty_values(record["source_properties"]),
        )
        target = EntityNode(
            name=record["target_id"],
            label=record["target_type"],
            properties=remove_empty_values(record["target_properties"]),
        )
        rel = Relation(
            source_id=record["source_id"],
            target_id=record["target_id"],
            label=record["type"],
            properties=remove_empty_values(record["rel_properties"]),
        )
        triples.append([source, rel, target])

    return triples

```
 |  
| --- | --- |  
###  vector_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphPropertyGraphStore.vector_query "Permanent link")

```
vector_query(
    query: , **kwargs: 
) -> Tuple[[], [float]]

```

Query the graph store with a vector store query.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/property_graph.py`  
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
```
 | 
```
defvector_query(
    self, query: VectorStoreQuery, **kwargs: Any
) -> Tuple[List[LabelledNode], List[float]]:
"""Query the graph store with a vector store query."""
    if self._supports_vector_index:
        data = self.structured_query(
            f"""CALL vector_search.search('{VECTOR_INDEX_NAME}', $limit, $embedding)
                YIELD node, similarity
                WITH node, similarity, labels(node) AS all_labels
                UNWIND all_labels AS label
                WITH node, similarity, label
                WHERE NOT label IN ['{BASE_ENTITY_LABEL}', '{BASE_NODE_LABEL}']
                WITH node, similarity, label, properties(node) AS originalProperties
                RETURN
                    node.id AS name,
                    label AS type,
                    node{{.* , embedding: Null, name: Null, id: Null}} AS properties,
                    similarity
,
            param_map={
                "embedding": query.query_embedding,
                "limit": query.similarity_top_k,
            },
        )
    else:
        data = []
    data = data if data else []

    nodes = []
    scores = []
    for record in data:
        node = EntityNode(
            name=record["name"],
            label=record["type"],
            properties=remove_empty_values(record["properties"]),
        )
        nodes.append(node)
        scores.append(record["similarity"])

    return (nodes, scores)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphPropertyGraphStore.delete "Permanent link")

```
delete(
    entity_names: Optional[[]] = None,
    relation_names: Optional[[]] = None,
    properties: Optional[] = None,
    ids: Optional[[]] = None,
) -> None

```

Delete matching data.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/property_graph.py`  
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
```
 | 
```
defdelete(
    self,
    entity_names: Optional[List[str]] = None,
    relation_names: Optional[List[str]] = None,
    properties: Optional[dict] = None,
    ids: Optional[List[str]] = None,
) -> None:
"""Delete matching data."""
    if entity_names:
        self.structured_query(
            "MATCH (n) WHERE n.name IN $entity_names DETACH DELETE n",
            param_map={"entity_names": entity_names},
        )
    if ids:
        self.structured_query(
            "MATCH (n) WHERE n.id IN $ids DETACH DELETE n",
            param_map={"ids": ids},
        )
    if relation_names:
        for rel in relation_names:
            self.structured_query(f"MATCH ()-[r:`{rel}`]->() DELETE r")

    if properties:
        cypher = "MATCH (e) WHERE "
        prop_list = []
        params = {}
        for i, prop in enumerate(properties):
            prop_list.append(f"e.`{prop}` = $property_{i}")
            params[f"property_{i}"] = properties[prop]
        cypher += " AND ".join(prop_list)
        self.structured_query(cypher + " DETACH DELETE e", param_map=params)

```
 |  
| --- | --- |  
###  verify_vector_support [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/memgraph/#llama_index.graph_stores.memgraph.MemgraphPropertyGraphStore.verify_vector_support "Permanent link")

```
verify_vector_support() -> None

```

Check if the connected Memgraph database supports vector indices.
Compares the current version with the required version (2.22.0) that supports vector indexing.
Source code in `llama-index-integrations/graph_stores/llama-index-graph-stores-memgraph/llama_index/graph_stores/memgraph/property_graph.py`  
| 
```
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
```
 | 
```
defverify_vector_support(self) -> None:
"""
    Check if the connected Memgraph database supports vector indices.

    Compares the current version with the required version (2.22.0) that
    supports vector indexing.
    """
    response = self.structured_query("SHOW VERSION;")
    current_version = response[0]["version"]
    current_version = tuple(map(int, current_version.split(".")))
    required_version = "2.22"
    required_version = tuple(map(int, required_version.split(".")))

    # Check if the version is equal to or larger than the required version
    if current_version >= required_version:
        # Check if vector index is configured
        try:
            self.structured_query(
                f"""
                CREATE VECTOR INDEX {VECTOR_INDEX_NAME} ON :{BASE_ENTITY_LABEL}(embedding) WITH CONFIG {{"dimension": 1536, "capacity": 1000}};

            )
            self._supports_vector_index = True
            logger.info(
                "Vector index %s was created with a fixed embedding dimension of 1536. "
                "If your chosen LLM model uses a different dimension, manually create the vector index with the following query:\n"
                'CREATE VECTOR INDEX %s ON :%s(embedding) WITH CONFIG {"dimension": <INSERT_DIMENSION>, "capacity": 1000};',
                VECTOR_INDEX_NAME,
                VECTOR_INDEX_NAME,
                BASE_ENTITY_LABEL,
            )
        except neo4j.exceptions.Neo4jError as decode_error:
            self._supports_vector_index = False
            if (
                decode_error.code
                == "Memgraph.ClientError.MemgraphError.MemgraphError"
                and "vector_search.show_index_info" in decode_error.message
            ):
                logger.info(
"""Failed to create vector index entity:
                    Given vector index already exists."""
                )
    else:
        self._supports_vector_index = False
        logger.info(
"""Vector indexing is not supported by your current Memgraph
            version (%s). Please upgrade to version 2.22.0 or newer to use
            vector indices.""",
            ".".join(map(str, current_version)),
        )

```
 |  
| --- | --- |  
options: members: - MemgraphGraphStore - MemgraphPropertyGraphStore
