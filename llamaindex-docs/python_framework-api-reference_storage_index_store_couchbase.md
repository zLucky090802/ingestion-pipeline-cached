# Couchbase
##  CouchbaseIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/couchbase/#llama_index.storage.index_store.couchbase.CouchbaseIndexStore "Permanent link")
Bases: `KVIndexStore`
Couchbase Index store.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-couchbase/llama_index/storage/index_store/couchbase/base.py`  
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
```
 | 
```
classCouchbaseIndexStore(KVIndexStore):
"""Couchbase Index store."""

    def__init__(
        self,
        couchbase_kvstore: CouchbaseKVStore,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> None:
"""
        Initialize a CouchbaseIndexStore.

        Args:
        couchbase_kvstore (CouchbaseKVStore): Couchbase key-value store
        namespace (str): namespace for the index store
        collection_suffix (str): suffix for the collection name

        """
        super().__init__(
            couchbase_kvstore,
            namespace=namespace,
            collection_suffix=collection_suffix,
        )

    @classmethod
    deffrom_couchbase_client(
        cls,
        client: Any,
        bucket_name: str,
        scope_name: str,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
        async_client: Optional[Any] = None,
    ) -> "CouchbaseIndexStore":
"""Initialize a CouchbaseIndexStore from a Couchbase client."""
        couchbase_kvstore = CouchbaseKVStore.from_couchbase_client(
            client=client,
            bucket_name=bucket_name,
            scope_name=scope_name,
            async_client=async_client,
        )
        return cls(couchbase_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_couchbase_client `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/couchbase/#llama_index.storage.index_store.couchbase.CouchbaseIndexStore.from_couchbase_client "Permanent link")

```
from_couchbase_client(
    client: ,
    bucket_name: ,
    scope_name: ,
    namespace: Optional[] = None,
    collection_suffix: Optional[] = None,
    async_client: Optional[] = None,
) -> 

```

Initialize a CouchbaseIndexStore from a Couchbase client.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-couchbase/llama_index/storage/index_store/couchbase/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_couchbase_client(
    cls,
    client: Any,
    bucket_name: str,
    scope_name: str,
    namespace: Optional[str] = None,
    collection_suffix: Optional[str] = None,
    async_client: Optional[Any] = None,
) -> "CouchbaseIndexStore":
"""Initialize a CouchbaseIndexStore from a Couchbase client."""
    couchbase_kvstore = CouchbaseKVStore.from_couchbase_client(
        client=client,
        bucket_name=bucket_name,
        scope_name=scope_name,
        async_client=async_client,
    )
    return cls(couchbase_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
options: members: - CouchbaseIndexStore
