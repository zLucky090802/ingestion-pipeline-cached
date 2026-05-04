# Mongodb
##  MongoDocumentStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/mongodb/#llama_index.storage.docstore.mongodb.MongoDocumentStore "Permanent link")
Bases: `KVDocumentStore`
Mongo Document (Node) store.
A MongoDB store for Document and Node objects.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `mongo_kvstore`  |   |  MongoDB key-value store  |  _required_  |  
|  `namespace`  |  namespace for the docstore  |  `None`  |  
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-mongodb/llama_index/storage/docstore/mongodb/base.py`  
| 
```
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
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
```
 | 
```
classMongoDocumentStore(KVDocumentStore):
"""
    Mongo Document (Node) store.

    A MongoDB store for Document and Node objects.

    Args:
        mongo_kvstore (MongoDBKVStore): MongoDB key-value store
        namespace (str): namespace for the docstore

    """

    def__init__(
        self,
        mongo_kvstore: MongoDBKVStore,
        namespace: Optional[str] = None,
        node_collection_suffix: Optional[str] = None,
        ref_doc_collection_suffix: Optional[str] = None,
        metadata_collection_suffix: Optional[str] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""Init a MongoDocumentStore."""
        super().__init__(
            mongo_kvstore,
            namespace=namespace,
            batch_size=batch_size,
            node_collection_suffix=node_collection_suffix,
            ref_doc_collection_suffix=ref_doc_collection_suffix,
            metadata_collection_suffix=metadata_collection_suffix,
        )

    @classmethod
    deffrom_uri(
        cls,
        uri: str,
        db_name: Optional[str] = None,
        namespace: Optional[str] = None,
        node_collection_suffix: Optional[str] = None,
        ref_doc_collection_suffix: Optional[str] = None,
        metadata_collection_suffix: Optional[str] = None,
    ) -> "MongoDocumentStore":
"""Load a MongoDocumentStore from a MongoDB URI."""
        mongo_kvstore = MongoDBKVStore.from_uri(uri, db_name)
        return cls(
            mongo_kvstore,
            namespace,
            node_collection_suffix,
            ref_doc_collection_suffix,
            metadata_collection_suffix,
        )

    @classmethod
    deffrom_host_and_port(
        cls,
        host: str,
        port: int,
        db_name: Optional[str] = None,
        namespace: Optional[str] = None,
        node_collection_suffix: Optional[str] = None,
        ref_doc_collection_suffix: Optional[str] = None,
        metadata_collection_suffix: Optional[str] = None,
    ) -> "MongoDocumentStore":
"""Load a MongoDocumentStore from a MongoDB host and port."""
        mongo_kvstore = MongoDBKVStore.from_host_and_port(host, port, db_name)
        return cls(
            mongo_kvstore,
            namespace,
            node_collection_suffix,
            ref_doc_collection_suffix,
            metadata_collection_suffix,
        )

```
 |  
| --- | --- |  
###  from_uri `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/mongodb/#llama_index.storage.docstore.mongodb.MongoDocumentStore.from_uri "Permanent link")

```
from_uri(
    uri: ,
    db_name: Optional[] = None,
    namespace: Optional[] = None,
    node_collection_suffix: Optional[] = None,
    ref_doc_collection_suffix: Optional[] = None,
    metadata_collection_suffix: Optional[] = None,
) -> 

```

Load a MongoDocumentStore from a MongoDB URI.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-mongodb/llama_index/storage/docstore/mongodb/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_uri(
    cls,
    uri: str,
    db_name: Optional[str] = None,
    namespace: Optional[str] = None,
    node_collection_suffix: Optional[str] = None,
    ref_doc_collection_suffix: Optional[str] = None,
    metadata_collection_suffix: Optional[str] = None,
) -> "MongoDocumentStore":
"""Load a MongoDocumentStore from a MongoDB URI."""
    mongo_kvstore = MongoDBKVStore.from_uri(uri, db_name)
    return cls(
        mongo_kvstore,
        namespace,
        node_collection_suffix,
        ref_doc_collection_suffix,
        metadata_collection_suffix,
    )

```
 |  
| --- | --- |  
###  from_host_and_port `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/mongodb/#llama_index.storage.docstore.mongodb.MongoDocumentStore.from_host_and_port "Permanent link")

```
from_host_and_port(
    host: ,
    port: ,
    db_name: Optional[] = None,
    namespace: Optional[] = None,
    node_collection_suffix: Optional[] = None,
    ref_doc_collection_suffix: Optional[] = None,
    metadata_collection_suffix: Optional[] = None,
) -> 

```

Load a MongoDocumentStore from a MongoDB host and port.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-mongodb/llama_index/storage/docstore/mongodb/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_host_and_port(
    cls,
    host: str,
    port: int,
    db_name: Optional[str] = None,
    namespace: Optional[str] = None,
    node_collection_suffix: Optional[str] = None,
    ref_doc_collection_suffix: Optional[str] = None,
    metadata_collection_suffix: Optional[str] = None,
) -> "MongoDocumentStore":
"""Load a MongoDocumentStore from a MongoDB host and port."""
    mongo_kvstore = MongoDBKVStore.from_host_and_port(host, port, db_name)
    return cls(
        mongo_kvstore,
        namespace,
        node_collection_suffix,
        ref_doc_collection_suffix,
        metadata_collection_suffix,
    )

```
 |  
| --- | --- |  
options: members: - MongoDocumentStore
