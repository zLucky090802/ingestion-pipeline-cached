# Tablestore
##  TablestoreDocumentStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/tablestore/#llama_index.storage.docstore.tablestore.TablestoreDocumentStore "Permanent link")
Bases: `KVDocumentStore`
TablestoreDocument Store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `tablestore_kvstore`  |   |  tablestore_kvstore key-value store  |  _required_  |  
|  `namespace`  |  namespace for the docstore  |  `'llama_index_doc_store_'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `TablestoreDocumentStore`  |  A Tablestore document store object.  |  
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-tablestore/llama_index/storage/docstore/tablestore/base.py`  
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
```
 | 
```
classTablestoreDocumentStore(KVDocumentStore):
"""
    TablestoreDocument Store.

    Args:
        tablestore_kvstore (TablestoreKVStore): tablestore_kvstore key-value store
        namespace (str): namespace for the docstore

    Returns:
        TablestoreDocumentStore: A Tablestore document store object.

    """

    def__init__(
        self,
        tablestore_kvstore: TablestoreKVStore,
        namespace: str = "llama_index_doc_store_",
        batch_size: int = DEFAULT_BATCH_SIZE,
        node_collection_suffix: str = "data",
        ref_doc_collection_suffix: str = "ref_doc_info",
        metadata_collection_suffix: str = "metadata",
    ) -> None:
        super().__init__(
            kvstore=tablestore_kvstore,
            namespace=namespace,
            batch_size=batch_size,
            node_collection_suffix=node_collection_suffix,
            ref_doc_collection_suffix=ref_doc_collection_suffix,
            metadata_collection_suffix=metadata_collection_suffix,
        )
        self._tablestore_kvstore = tablestore_kvstore

    defclear_all(self):
        doc = self.docs
        self._tablestore_kvstore.delete_all(self._node_collection)
        self._tablestore_kvstore.delete_all(self._ref_doc_collection)
        self._tablestore_kvstore.delete_all(self._metadata_collection)
        for key in doc:
            self.delete_document(doc_id=key)

    @classmethod
    deffrom_config(
        cls,
        endpoint: Optional[str] = None,
        instance_name: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        **kwargs: Any,
    ) -> "TablestoreDocumentStore":
        kv_store = TablestoreKVStore(
            endpoint=endpoint,
            instance_name=instance_name,
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            kwargs=kwargs,
        )
        return cls(tablestore_kvstore=kv_store)

```
 |  
| --- | --- |  
options: members: - TablestoreDocumentStore
