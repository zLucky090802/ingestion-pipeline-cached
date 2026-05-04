# Couchbase
##  CouchbaseDocumentStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/couchbase/#llama_index.storage.docstore.couchbase.CouchbaseDocumentStore "Permanent link")
Bases: `KVDocumentStore`
Couchbase Document (Node) store. A documents store for Document and Node objects using Couchbase.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-couchbase/llama_index/storage/docstore/couchbase/base.py`  
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
```
 | 
```
classCouchbaseDocumentStore(KVDocumentStore):
"""
    Couchbase Document (Node) store.
    A documents store for Document and Node objects using Couchbase.
    """

    def__init__(
        self,
        couchbase_kvstore: CouchbaseKVStore,
        namespace: Optional[str] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
        node_collection_suffix: Optional[str] = None,
        ref_doc_collection_suffix: Optional[str] = None,
        metadata_collection_suffix: Optional[str] = None,
    ) -> None:
"""
        Initialize a CouchbaseDocumentStore.

        Args:
            couchbase_kvstore (CouchbaseKVStore): Couchbase key-value store
            namespace (str): namespace for the docstore
            batch_size (int): batch size for fetching documents
            node_collection_suffix (str): suffix for the node collection
            ref_doc_collection_suffix (str): suffix for the  Refdoc collection
            metadata_collection_suffix (str): suffix for the metadata collection

        """
        super().__init__(
            couchbase_kvstore,
            namespace=namespace,
            batch_size=batch_size,
            node_collection_suffix=node_collection_suffix,
            ref_doc_collection_suffix=ref_doc_collection_suffix,
            metadata_collection_suffix=metadata_collection_suffix,
        )

    @classmethod
    deffrom_couchbase_client(
        cls,
        client: Any,
        bucket_name: str,
        scope_name: str,
        namespace: Optional[str] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
        node_collection_suffix: Optional[str] = None,
        ref_doc_collection_suffix: Optional[str] = None,
        metadata_collection_suffix: Optional[str] = None,
        async_client: Optional[Any] = None,
    ) -> "CouchbaseDocumentStore":
"""Initialize a CouchbaseDocumentStore from a Couchbase client."""
        couchbase_kvstore = CouchbaseKVStore.from_couchbase_client(
            client=client,
            bucket_name=bucket_name,
            scope_name=scope_name,
            async_client=async_client,
        )
        return cls(
            couchbase_kvstore,
            namespace,
            batch_size,
            node_collection_suffix,
            ref_doc_collection_suffix,
            metadata_collection_suffix,
        )

```
 |  
| --- | --- |  
###  from_couchbase_client `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/couchbase/#llama_index.storage.docstore.couchbase.CouchbaseDocumentStore.from_couchbase_client "Permanent link")

```
from_couchbase_client(
    client: ,
    bucket_name: ,
    scope_name: ,
    namespace: Optional[] = None,
    batch_size:  = DEFAULT_BATCH_SIZE,
    node_collection_suffix: Optional[] = None,
    ref_doc_collection_suffix: Optional[] = None,
    metadata_collection_suffix: Optional[] = None,
    async_client: Optional[] = None,
) -> 

```

Initialize a CouchbaseDocumentStore from a Couchbase client.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-couchbase/llama_index/storage/docstore/couchbase/base.py`  
| 
```
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
    batch_size: int = DEFAULT_BATCH_SIZE,
    node_collection_suffix: Optional[str] = None,
    ref_doc_collection_suffix: Optional[str] = None,
    metadata_collection_suffix: Optional[str] = None,
    async_client: Optional[Any] = None,
) -> "CouchbaseDocumentStore":
"""Initialize a CouchbaseDocumentStore from a Couchbase client."""
    couchbase_kvstore = CouchbaseKVStore.from_couchbase_client(
        client=client,
        bucket_name=bucket_name,
        scope_name=scope_name,
        async_client=async_client,
    )
    return cls(
        couchbase_kvstore,
        namespace,
        batch_size,
        node_collection_suffix,
        ref_doc_collection_suffix,
        metadata_collection_suffix,
    )

```
 |  
| --- | --- |  
options: members: - CouchbaseDocumentStore
