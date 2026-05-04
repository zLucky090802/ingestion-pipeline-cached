# Duckdb
##  DuckDBDocumentStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/duckdb/#llama_index.storage.docstore.duckdb.DuckDBDocumentStore "Permanent link")
Bases: `KVDocumentStore`
DuckDB Document (Node) store.
A DuckDB store for Document and Node objects.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `duckdb_kvstore`  |   |  DuckDB key-value store  |  _required_  |  
|  `namespace`  |  namespace for the docstore  |  `None`  |  
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-duckdb/llama_index/storage/docstore/duckdb/base.py`  
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
```
 | 
```
classDuckDBDocumentStore(KVDocumentStore):
"""
    DuckDB Document (Node) store.

    A DuckDB store for Document and Node objects.

    Args:
        duckdb_kvstore (DuckDBKVStore): DuckDB key-value store
        namespace (str): namespace for the docstore

    """

    def__init__(
        self,
        duckdb_kvstore: DuckDBKVStore,
        namespace: Optional[str] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""Init a DuckDBDocumentStore."""
        super().__init__(duckdb_kvstore, namespace=namespace, batch_size=batch_size)
        # avoid conflicts with duckdb index store
        self._node_collection = f"{self._namespace}/doc"

```
 |  
| --- | --- |  
options: members: - DuckDBDocumentStore
