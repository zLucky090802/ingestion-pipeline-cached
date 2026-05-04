# Duckdb
##  DuckDBIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/duckdb/#llama_index.storage.index_store.duckdb.DuckDBIndexStore "Permanent link")
Bases: `KVIndexStore`
DuckDB Index store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `duckdb_kvstore`  |   |  DuckDB key-value store  |  _required_  |  
|  `namespace`  |  namespace for the index store  |  `None`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-duckdb/llama_index/storage/index_store/duckdb/base.py`  
| 
```
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
```
 | 
```
classDuckDBIndexStore(KVIndexStore):
"""
    DuckDB Index store.

    Args:
        duckdb_kvstore (DuckDBKVStore): DuckDB key-value store
        namespace (str): namespace for the index store

    """

    def__init__(
        self,
        duckdb_kvstore: DuckDBKVStore,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> None:
"""Init a DuckDBIndexStore."""
        super().__init__(
            duckdb_kvstore, namespace=namespace, collection_suffix=collection_suffix
        )
        # avoid conflicts with duckdb docstore
        if self._collection.endswith(DEFAULT_COLLECTION_SUFFIX):
            self._collection = f"{self._namespace}/index"

```
 |  
| --- | --- |  
options: members: - DuckDBIndexStore
