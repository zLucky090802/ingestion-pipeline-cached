# Gel
##  GelIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/gel/#llama_index.storage.index_store.gel.GelIndexStore "Permanent link")
Bases: `KVIndexStore`
Gel Index store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `gel_kvstore`  |   |  Gel key-value store  |  _required_  |  
|  `namespace`  |  namespace for the index store  |  `None`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-gel/llama_index/storage/index_store/gel/base.py`  
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
```
 | 
```
classGelIndexStore(KVIndexStore):
"""
    Gel Index store.

    Args:
        gel_kvstore (GelKVStore): Gel key-value store
        namespace (str): namespace for the index store

    """

    def__init__(
        self,
        gel_kvstore: GelKVStore,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> None:
"""Init a GelIndexStore."""
        super().__init__(
            gel_kvstore, namespace=namespace, collection_suffix=collection_suffix
        )

```
 |  
| --- | --- |  
options: members: - GelIndexStore
