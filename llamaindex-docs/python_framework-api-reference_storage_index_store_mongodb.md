# Mongodb
##  MongoIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/mongodb/#llama_index.storage.index_store.mongodb.MongoIndexStore "Permanent link")
Bases: `KVIndexStore`
Mongo Index store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `mongo_kvstore`  |   |  MongoDB key-value store  |  _required_  |  
|  `namespace`  |  namespace for the index store  |  `None`  |  
|  `collection_suffix`  |  suffix for the collection name  |  `None`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-mongodb/llama_index/storage/index_store/mongodb/base.py`  
| 
```
 7
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
```
 | 
```
classMongoIndexStore(KVIndexStore):
"""
    Mongo Index store.

    Args:
        mongo_kvstore (MongoDBKVStore): MongoDB key-value store
        namespace (str): namespace for the index store
        collection_suffix (str): suffix for the collection name

    """

    def__init__(
        self,
        mongo_kvstore: MongoDBKVStore,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> None:
"""Init a MongoIndexStore."""
        super().__init__(
            mongo_kvstore, namespace=namespace, collection_suffix=collection_suffix
        )

    @classmethod
    deffrom_uri(
        cls,
        uri: str,
        db_name: Optional[str] = None,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> "MongoIndexStore":
"""Load a MongoIndexStore from a MongoDB URI."""
        mongo_kvstore = MongoDBKVStore.from_uri(uri, db_name)
        return cls(mongo_kvstore, namespace, collection_suffix)

    @classmethod
    deffrom_host_and_port(
        cls,
        host: str,
        port: int,
        db_name: Optional[str] = None,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> "MongoIndexStore":
"""Load a MongoIndexStore from a MongoDB host and port."""
        mongo_kvstore = MongoDBKVStore.from_host_and_port(host, port, db_name)
        return cls(mongo_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_uri `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/mongodb/#llama_index.storage.index_store.mongodb.MongoIndexStore.from_uri "Permanent link")

```
from_uri(
    uri: ,
    db_name: Optional[] = None,
    namespace: Optional[] = None,
    collection_suffix: Optional[] = None,
) -> 

```

Load a MongoIndexStore from a MongoDB URI.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-mongodb/llama_index/storage/index_store/mongodb/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_uri(
    cls,
    uri: str,
    db_name: Optional[str] = None,
    namespace: Optional[str] = None,
    collection_suffix: Optional[str] = None,
) -> "MongoIndexStore":
"""Load a MongoIndexStore from a MongoDB URI."""
    mongo_kvstore = MongoDBKVStore.from_uri(uri, db_name)
    return cls(mongo_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_host_and_port `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/mongodb/#llama_index.storage.index_store.mongodb.MongoIndexStore.from_host_and_port "Permanent link")

```
from_host_and_port(
    host: ,
    port: ,
    db_name: Optional[] = None,
    namespace: Optional[] = None,
    collection_suffix: Optional[] = None,
) -> 

```

Load a MongoIndexStore from a MongoDB host and port.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-mongodb/llama_index/storage/index_store/mongodb/base.py`  
| 
```
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
    collection_suffix: Optional[str] = None,
) -> "MongoIndexStore":
"""Load a MongoIndexStore from a MongoDB host and port."""
    mongo_kvstore = MongoDBKVStore.from_host_and_port(host, port, db_name)
    return cls(mongo_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
options: members: - MongoIndexStore
