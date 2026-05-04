# Azurecosmosnosql
##  AzureCosmosNoSqlIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/azurecosmosnosql/#llama_index.storage.index_store.azurecosmosnosql.AzureCosmosNoSqlIndexStore "Permanent link")
Bases: 
Creates an Azure Cosmos DB NoSql Index Store.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-azurecosmosnosql/llama_index/storage/index_store/azurecosmosnosql/base.py`  
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
71
72
73
74
75
76
77
78
79
80
81
82
```
 | 
```
classAzureCosmosNoSqlIndexStore(BaseKVStore):
"""Creates an Azure Cosmos DB NoSql Index Store."""

    def__init__(
        self,
        azure_cosmos_nosql_kvstore: AzureCosmosNoSqlKVStore,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> None:
"""Initializes the Azure Cosmos NoSql Index Store."""
        super().__init__(azure_cosmos_nosql_kvstore, namespace, collection_suffix)

    @classmethod
    deffrom_connection_string(
        cls,
        connection_string: str,
        index_db_name: str = DEFAULT_INDEX_DATABASE,
        index_container_name: str = DEFAULT_INDEX_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
    ) -> "AzureCosmosNoSqlIndexStore":
"""Creates an instance of Azure Cosmos DB NoSql KV Store using a connection string."""
        azure_cosmos_nosql_kvstore = AzureCosmosNoSqlKVStore.from_connection_string(
            connection_string,
            index_db_name,
            index_container_name,
            cosmos_container_properties,
            cosmos_database_properties,
        )
        namespace = index_db_name + "." + index_container_name
        return cls(azure_cosmos_nosql_kvstore, namespace)

    @classmethod
    deffrom_account_and_key(
        cls,
        endpoint: str,
        key: str,
        index_db_name: str = DEFAULT_INDEX_DATABASE,
        index_container_name: str = DEFAULT_INDEX_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
    ) -> "AzureCosmosNoSqlIndexStore":
"""Creates an instance of Azure Cosmos DB NoSql KV Store using an account endpoint and key."""
        azure_cosmos_nosql_kvstore = AzureCosmosNoSqlKVStore.from_account_and_key(
            endpoint,
            key,
            index_db_name,
            index_container_name,
            cosmos_container_properties,
            cosmos_database_properties,
        )
        namespace = index_db_name + "." + index_container_name
        return cls(azure_cosmos_nosql_kvstore, namespace)

    @classmethod
    deffrom_aad_token(
        cls,
        endpoint: str,
        index_db_name: str = DEFAULT_INDEX_DATABASE,
        index_container_name: str = DEFAULT_INDEX_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
    ) -> "AzureCosmosNoSqlIndexStore":
"""Creates an instance of Azure Cosmos DB NoSql KV Store using an aad token."""
        azure_cosmos_nosql_kvstore = AzureCosmosNoSqlKVStore.from_aad_token(
            endpoint,
            index_db_name,
            index_container_name,
            cosmos_container_properties,
            cosmos_database_properties,
        )
        namespace = index_db_name + "." + index_container_name
        return cls(azure_cosmos_nosql_kvstore, namespace)

```
 |  
| --- | --- |  
###  from_connection_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/azurecosmosnosql/#llama_index.storage.index_store.azurecosmosnosql.AzureCosmosNoSqlIndexStore.from_connection_string "Permanent link")

```
from_connection_string(
    connection_string: ,
    index_db_name:  = DEFAULT_INDEX_DATABASE,
    index_container_name:  = DEFAULT_INDEX_CONTAINER,
    cosmos_container_properties: [, ] = None,
    cosmos_database_properties: [, ] = None,
) -> 

```

Creates an instance of Azure Cosmos DB NoSql KV Store using a connection string.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-azurecosmosnosql/llama_index/storage/index_store/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_connection_string(
    cls,
    connection_string: str,
    index_db_name: str = DEFAULT_INDEX_DATABASE,
    index_container_name: str = DEFAULT_INDEX_CONTAINER,
    cosmos_container_properties: Dict[str, Any] = None,
    cosmos_database_properties: Dict[str, Any] = None,
) -> "AzureCosmosNoSqlIndexStore":
"""Creates an instance of Azure Cosmos DB NoSql KV Store using a connection string."""
    azure_cosmos_nosql_kvstore = AzureCosmosNoSqlKVStore.from_connection_string(
        connection_string,
        index_db_name,
        index_container_name,
        cosmos_container_properties,
        cosmos_database_properties,
    )
    namespace = index_db_name + "." + index_container_name
    return cls(azure_cosmos_nosql_kvstore, namespace)

```
 |  
| --- | --- |  
###  from_account_and_key `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/azurecosmosnosql/#llama_index.storage.index_store.azurecosmosnosql.AzureCosmosNoSqlIndexStore.from_account_and_key "Permanent link")

```
from_account_and_key(
    endpoint: ,
    key: ,
    index_db_name:  = DEFAULT_INDEX_DATABASE,
    index_container_name:  = DEFAULT_INDEX_CONTAINER,
    cosmos_container_properties: [, ] = None,
    cosmos_database_properties: [, ] = None,
) -> 

```

Creates an instance of Azure Cosmos DB NoSql KV Store using an account endpoint and key.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-azurecosmosnosql/llama_index/storage/index_store/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_account_and_key(
    cls,
    endpoint: str,
    key: str,
    index_db_name: str = DEFAULT_INDEX_DATABASE,
    index_container_name: str = DEFAULT_INDEX_CONTAINER,
    cosmos_container_properties: Dict[str, Any] = None,
    cosmos_database_properties: Dict[str, Any] = None,
) -> "AzureCosmosNoSqlIndexStore":
"""Creates an instance of Azure Cosmos DB NoSql KV Store using an account endpoint and key."""
    azure_cosmos_nosql_kvstore = AzureCosmosNoSqlKVStore.from_account_and_key(
        endpoint,
        key,
        index_db_name,
        index_container_name,
        cosmos_container_properties,
        cosmos_database_properties,
    )
    namespace = index_db_name + "." + index_container_name
    return cls(azure_cosmos_nosql_kvstore, namespace)

```
 |  
| --- | --- |  
###  from_aad_token `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/azurecosmosnosql/#llama_index.storage.index_store.azurecosmosnosql.AzureCosmosNoSqlIndexStore.from_aad_token "Permanent link")

```
from_aad_token(
    endpoint: ,
    index_db_name:  = DEFAULT_INDEX_DATABASE,
    index_container_name:  = DEFAULT_INDEX_CONTAINER,
    cosmos_container_properties: [, ] = None,
    cosmos_database_properties: [, ] = None,
) -> 

```

Creates an instance of Azure Cosmos DB NoSql KV Store using an aad token.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-azurecosmosnosql/llama_index/storage/index_store/azurecosmosnosql/base.py`  
| 
```
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
```
 | 
```
@classmethod
deffrom_aad_token(
    cls,
    endpoint: str,
    index_db_name: str = DEFAULT_INDEX_DATABASE,
    index_container_name: str = DEFAULT_INDEX_CONTAINER,
    cosmos_container_properties: Dict[str, Any] = None,
    cosmos_database_properties: Dict[str, Any] = None,
) -> "AzureCosmosNoSqlIndexStore":
"""Creates an instance of Azure Cosmos DB NoSql KV Store using an aad token."""
    azure_cosmos_nosql_kvstore = AzureCosmosNoSqlKVStore.from_aad_token(
        endpoint,
        index_db_name,
        index_container_name,
        cosmos_container_properties,
        cosmos_database_properties,
    )
    namespace = index_db_name + "." + index_container_name
    return cls(azure_cosmos_nosql_kvstore, namespace)

```
 |  
| --- | --- |  
options: members: - AzureCosmosNoSqlIndexStore
