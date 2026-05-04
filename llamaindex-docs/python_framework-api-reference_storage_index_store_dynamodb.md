# Dynamodb
##  DynamoDBIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/dynamodb/#llama_index.storage.index_store.dynamodb.DynamoDBIndexStore "Permanent link")
Bases: `KVIndexStore`
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-dynamodb/llama_index/storage/index_store/dynamodb/base.py`  
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
```
 | 
```
classDynamoDBIndexStore(KVIndexStore):
    def__init__(
        self,
        dynamodb_kvstore: DynamoDBKVStore,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> None:
"""Init a DynamoDBIndexStore."""
        super().__init__(
            kvstore=dynamodb_kvstore,
            namespace=namespace,
            collection_suffix=collection_suffix,
        )

    @classmethod
    deffrom_table_name(
        cls,
        table_name: str,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> "DynamoDBIndexStore":
"""Load DynamoDBIndexStore from a DynamoDB table name."""
        ddb_kvstore = DynamoDBKVStore.from_table_name(table_name=table_name)
        return cls(
            dynamodb_kvstore=ddb_kvstore,
            namespace=namespace,
            collection_suffix=collection_suffix,
        )

```
 |  
| --- | --- |  
###  from_table_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/dynamodb/#llama_index.storage.index_store.dynamodb.DynamoDBIndexStore.from_table_name "Permanent link")

```
from_table_name(
    table_name: ,
    namespace: Optional[] = None,
    collection_suffix: Optional[] = None,
) -> 

```

Load DynamoDBIndexStore from a DynamoDB table name.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-dynamodb/llama_index/storage/index_store/dynamodb/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_table_name(
    cls,
    table_name: str,
    namespace: Optional[str] = None,
    collection_suffix: Optional[str] = None,
) -> "DynamoDBIndexStore":
"""Load DynamoDBIndexStore from a DynamoDB table name."""
    ddb_kvstore = DynamoDBKVStore.from_table_name(table_name=table_name)
    return cls(
        dynamodb_kvstore=ddb_kvstore,
        namespace=namespace,
        collection_suffix=collection_suffix,
    )

```
 |  
| --- | --- |  
options: members: - DynamoDBIndexStore
