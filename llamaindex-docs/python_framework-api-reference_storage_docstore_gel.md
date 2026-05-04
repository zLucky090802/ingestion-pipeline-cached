# Gel
##  GelDocumentStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/gel/#llama_index.storage.docstore.gel.GelDocumentStore "Permanent link")
Bases: `KVDocumentStore`
Gel Document (Node) store.
A Gel store for Document and Node objects.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `gel_kvstore`  |   |  Gel key-value store  |  _required_  |  
|  `namespace`  |  namespace for the docstore  |  `None`  |  
|  `batch_size`  |  batch size for bulk operations  |  `DEFAULT_BATCH_SIZE`  |  
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-gel/llama_index/storage/docstore/gel/base.py`  
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
```
 | 
```
classGelDocumentStore(KVDocumentStore):
"""
    Gel Document (Node) store.

    A Gel store for Document and Node objects.

    Args:
        gel_kvstore (GelKVStore): Gel key-value store
        namespace (str): namespace for the docstore
        batch_size (int): batch size for bulk operations

    """

    def__init__(
        self,
        gel_kvstore: GelKVStore,
        namespace: Optional[str] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""Init a GelDocumentStore."""
        super().__init__(gel_kvstore, namespace=namespace, batch_size=batch_size)

```
 |  
| --- | --- |  
options: members: - GelDocumentStore
