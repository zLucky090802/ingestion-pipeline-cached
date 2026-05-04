# Tablestore
##  TablestoreIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/tablestore/#llama_index.storage.index_store.tablestore.TablestoreIndexStore "Permanent link")
Bases: `KVIndexStore`
Tablestore Index store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `tablestore_kvstore`  |   |  Tablestore key-value store  |  _required_  |  
|  `namespace`  |  namespace for the index store  |  `'llama_index_index_store_'`  |  
|  `collection_suffix`  |  suffix for the table name  |  `'data'`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-tablestore/llama_index/storage/index_store/tablestore/base.py`  
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
```
 | 
```
classTablestoreIndexStore(KVIndexStore):
"""
    Tablestore Index store.

    Args:
        tablestore_kvstore (TablestoreKVStore): Tablestore key-value store
        namespace (str): namespace for the index store
        collection_suffix (str): suffix for the table name

    """

    def__init__(
        self,
        tablestore_kvstore: TablestoreKVStore,
        namespace: str = "llama_index_index_store_",
        collection_suffix: str = "data",
    ) -> None:
"""Init a TablestoreIndexStore."""
        super().__init__(
            kvstore=tablestore_kvstore,
            namespace=namespace,
            collection_suffix=collection_suffix,
        )
        self._tablestore_kvstore = tablestore_kvstore

    @classmethod
    deffrom_config(
        cls,
        endpoint: Optional[str] = None,
        instance_name: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        **kwargs: Any,
    ) -> "TablestoreIndexStore":
"""Load a TablestoreIndexStore from config."""
        kv_store = TablestoreKVStore(
            endpoint=endpoint,
            instance_name=instance_name,
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            kwargs=kwargs,
        )
        return cls(tablestore_kvstore=kv_store)

    defdelete_all_index(self):
"""Delete all index."""
        self._tablestore_kvstore.delete_all(self._collection)

```
 |  
| --- | --- |  
###  from_config `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/tablestore/#llama_index.storage.index_store.tablestore.TablestoreIndexStore.from_config "Permanent link")

```
from_config(
    endpoint: Optional[] = None,
    instance_name: Optional[] = None,
    access_key_id: Optional[] = None,
    access_key_secret: Optional[] = None,
    **kwargs: 
) -> 

```

Load a TablestoreIndexStore from config.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-tablestore/llama_index/storage/index_store/tablestore/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_config(
    cls,
    endpoint: Optional[str] = None,
    instance_name: Optional[str] = None,
    access_key_id: Optional[str] = None,
    access_key_secret: Optional[str] = None,
    **kwargs: Any,
) -> "TablestoreIndexStore":
"""Load a TablestoreIndexStore from config."""
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
###  delete_all_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/tablestore/#llama_index.storage.index_store.tablestore.TablestoreIndexStore.delete_all_index "Permanent link")

```
delete_all_index()

```

Delete all index.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-tablestore/llama_index/storage/index_store/tablestore/base.py`  
| 
```
52
53
54
```
 | 
```
defdelete_all_index(self):
"""Delete all index."""
    self._tablestore_kvstore.delete_all(self._collection)

```
 |  
| --- | --- |  
options: members: - TablestoreIndexStore
