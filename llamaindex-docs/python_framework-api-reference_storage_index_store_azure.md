# Azure
##  AzureIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/azure/#llama_index.storage.index_store.azure.AzureIndexStore "Permanent link")
Bases: `KVIndexStore`
Azure Table Index store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `azure_kvstore`  |   |  Azure key-value store  |  _required_  |  
|  `namespace`  |  namespace for the index store  |  `None`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-azure/llama_index/storage/index_store/azure/base.py`  
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
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
```
 | 
```
classAzureIndexStore(KVIndexStore):
"""
    Azure Table Index store.

    Args:
        azure_kvstore (AzureKVStore): Azure key-value store
        namespace (str): namespace for the index store

    """

    def__init__(
        self,
        azure_kvstore: AzureKVStore,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> None:
"""Init a MongoIndexStore."""
        super().__init__(azure_kvstore, namespace, collection_suffix)

    @classmethod
    deffrom_connection_string(
        cls,
        connection_string: str,
        namespace: Optional[str] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> "AzureIndexStore":
"""
        Load an AzureIndexStore from an Azure connection string.

        Args:
            connection_string (str): Azure connection string
            namespace (Optional[str]): namespace for the AzureIndexStore
            service_mode (ServiceMode): CosmosDB or Azure Table service mode

        """
        azure_kvstore = AzureKVStore.from_connection_string(
            connection_string, service_mode, partition_key
        )
        return cls(azure_kvstore, namespace, collection_suffix)

    @classmethod
    deffrom_account_and_key(
        cls,
        account_name: str,
        account_key: str,
        namespace: Optional[str] = None,
        endpoint: Optional[str] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> "AzureIndexStore":
"""
        Load an AzureIndexStore from an account name and key.

        Args:
            account_name (str): Azure Storage Account Name
            account_key (str): Azure Storage Account Key
            namespace (Optional[str]): namespace for the AzureIndexStore
            service_mode (ServiceMode): CosmosDB or Azure Table service mode

        """
        azure_kvstore = AzureKVStore.from_account_and_key(
            account_name, account_key, endpoint, service_mode, partition_key
        )
        return cls(azure_kvstore, namespace, collection_suffix)

    @classmethod
    deffrom_account_and_id(
        cls,
        account_name: str,
        namespace: Optional[str] = None,
        endpoint: Optional[str] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> "AzureIndexStore":
"""
        Load an AzureIndexStore from an account name and managed ID.

        Args:
            account_name (str): Azure Storage Account Name
            namespace (Optional[str]): namespace for the AzureIndexStore
            service_mode (ServiceMode): CosmosDB or Azure Table service mode

        """
        azure_kvstore = AzureKVStore.from_account_and_id(
            account_name, endpoint, service_mode, partition_key
        )
        return cls(azure_kvstore, namespace, collection_suffix)

    @classmethod
    deffrom_sas_token(
        cls,
        endpoint: str,
        sas_token: str,
        namespace: Optional[str] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> "AzureIndexStore":
"""
        Load an AzureIndexStore from a SAS token.

        Args:
            endpoint (str): Azure Table service endpoint
            sas_token (str): Shared Access Signature token
            namespace (Optional[str]): namespace for the AzureIndexStore
            service_mode (ServiceMode): CosmosDB or Azure Table service mode

        """
        azure_kvstore = AzureKVStore.from_sas_token(
            endpoint, sas_token, service_mode, partition_key
        )
        return cls(azure_kvstore, namespace, collection_suffix)

    @classmethod
    deffrom_aad_token(
        cls,
        endpoint: str,
        namespace: Optional[str] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> "AzureIndexStore":
"""
        Load an AzureIndexStore from an AAD token.

        Args:
            endpoint (str): Azure Table service endpoint
            namespace (Optional[str]): namespace for the AzureIndexStore
            service_mode (ServiceMode): CosmosDB or Azure Table service mode

        """
        azure_kvstore = AzureKVStore.from_aad_token(
            endpoint, service_mode, partition_key
        )
        return cls(azure_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_connection_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/azure/#llama_index.storage.index_store.azure.AzureIndexStore.from_connection_string "Permanent link")

```
from_connection_string(
    connection_string: ,
    namespace: Optional[] = None,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    collection_suffix: Optional[] = None,
) -> 

```

Load an AzureIndexStore from an Azure connection string.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `connection_string`  |  Azure connection string  |  _required_  |  
|  `namespace`  |  `Optional[str]`  |  namespace for the AzureIndexStore  |  `None`  |  
|  `service_mode`  |  `ServiceMode`  |  CosmosDB or Azure Table service mode  |  `STORAGE`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-azure/llama_index/storage/index_store/azure/base.py`  
| 
```
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
@classmethod
deffrom_connection_string(
    cls,
    connection_string: str,
    namespace: Optional[str] = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    collection_suffix: Optional[str] = None,
) -> "AzureIndexStore":
"""
    Load an AzureIndexStore from an Azure connection string.

    Args:
        connection_string (str): Azure connection string
        namespace (Optional[str]): namespace for the AzureIndexStore
        service_mode (ServiceMode): CosmosDB or Azure Table service mode

    """
    azure_kvstore = AzureKVStore.from_connection_string(
        connection_string, service_mode, partition_key
    )
    return cls(azure_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_account_and_key `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/azure/#llama_index.storage.index_store.azure.AzureIndexStore.from_account_and_key "Permanent link")

```
from_account_and_key(
    account_name: ,
    account_key: ,
    namespace: Optional[] = None,
    endpoint: Optional[] = None,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    collection_suffix: Optional[] = None,
) -> 

```

Load an AzureIndexStore from an account name and key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `account_name`  |  Azure Storage Account Name  |  _required_  |  
|  `account_key`  |  Azure Storage Account Key  |  _required_  |  
|  `namespace`  |  `Optional[str]`  |  namespace for the AzureIndexStore  |  `None`  |  
|  `service_mode`  |  `ServiceMode`  |  CosmosDB or Azure Table service mode  |  `STORAGE`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-azure/llama_index/storage/index_store/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_account_and_key(
    cls,
    account_name: str,
    account_key: str,
    namespace: Optional[str] = None,
    endpoint: Optional[str] = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    collection_suffix: Optional[str] = None,
) -> "AzureIndexStore":
"""
    Load an AzureIndexStore from an account name and key.

    Args:
        account_name (str): Azure Storage Account Name
        account_key (str): Azure Storage Account Key
        namespace (Optional[str]): namespace for the AzureIndexStore
        service_mode (ServiceMode): CosmosDB or Azure Table service mode

    """
    azure_kvstore = AzureKVStore.from_account_and_key(
        account_name, account_key, endpoint, service_mode, partition_key
    )
    return cls(azure_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_account_and_id `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/azure/#llama_index.storage.index_store.azure.AzureIndexStore.from_account_and_id "Permanent link")

```
from_account_and_id(
    account_name: ,
    namespace: Optional[] = None,
    endpoint: Optional[] = None,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    collection_suffix: Optional[] = None,
) -> 

```

Load an AzureIndexStore from an account name and managed ID.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `account_name`  |  Azure Storage Account Name  |  _required_  |  
|  `namespace`  |  `Optional[str]`  |  namespace for the AzureIndexStore  |  `None`  |  
|  `service_mode`  |  `ServiceMode`  |  CosmosDB or Azure Table service mode  |  `STORAGE`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-azure/llama_index/storage/index_store/azure/base.py`  
| 
```
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
```
 | 
```
@classmethod
deffrom_account_and_id(
    cls,
    account_name: str,
    namespace: Optional[str] = None,
    endpoint: Optional[str] = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    collection_suffix: Optional[str] = None,
) -> "AzureIndexStore":
"""
    Load an AzureIndexStore from an account name and managed ID.

    Args:
        account_name (str): Azure Storage Account Name
        namespace (Optional[str]): namespace for the AzureIndexStore
        service_mode (ServiceMode): CosmosDB or Azure Table service mode

    """
    azure_kvstore = AzureKVStore.from_account_and_id(
        account_name, endpoint, service_mode, partition_key
    )
    return cls(azure_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_sas_token `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/azure/#llama_index.storage.index_store.azure.AzureIndexStore.from_sas_token "Permanent link")

```
from_sas_token(
    endpoint: ,
    sas_token: ,
    namespace: Optional[] = None,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    collection_suffix: Optional[] = None,
) -> 

```

Load an AzureIndexStore from a SAS token.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `endpoint`  |  Azure Table service endpoint  |  _required_  |  
|  `sas_token`  |  Shared Access Signature token  |  _required_  |  
|  `namespace`  |  `Optional[str]`  |  namespace for the AzureIndexStore  |  `None`  |  
|  `service_mode`  |  `ServiceMode`  |  CosmosDB or Azure Table service mode  |  `STORAGE`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-azure/llama_index/storage/index_store/azure/base.py`  
| 
```
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
```
 | 
```
@classmethod
deffrom_sas_token(
    cls,
    endpoint: str,
    sas_token: str,
    namespace: Optional[str] = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    collection_suffix: Optional[str] = None,
) -> "AzureIndexStore":
"""
    Load an AzureIndexStore from a SAS token.

    Args:
        endpoint (str): Azure Table service endpoint
        sas_token (str): Shared Access Signature token
        namespace (Optional[str]): namespace for the AzureIndexStore
        service_mode (ServiceMode): CosmosDB or Azure Table service mode

    """
    azure_kvstore = AzureKVStore.from_sas_token(
        endpoint, sas_token, service_mode, partition_key
    )
    return cls(azure_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_aad_token `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/azure/#llama_index.storage.index_store.azure.AzureIndexStore.from_aad_token "Permanent link")

```
from_aad_token(
    endpoint: ,
    namespace: Optional[] = None,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    collection_suffix: Optional[] = None,
) -> 

```

Load an AzureIndexStore from an AAD token.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `endpoint`  |  Azure Table service endpoint  |  _required_  |  
|  `namespace`  |  `Optional[str]`  |  namespace for the AzureIndexStore  |  `None`  |  
|  `service_mode`  |  `ServiceMode`  |  CosmosDB or Azure Table service mode  |  `STORAGE`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-azure/llama_index/storage/index_store/azure/base.py`  
| 
```
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
```
 | 
```
@classmethod
deffrom_aad_token(
    cls,
    endpoint: str,
    namespace: Optional[str] = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    collection_suffix: Optional[str] = None,
) -> "AzureIndexStore":
"""
    Load an AzureIndexStore from an AAD token.

    Args:
        endpoint (str): Azure Table service endpoint
        namespace (Optional[str]): namespace for the AzureIndexStore
        service_mode (ServiceMode): CosmosDB or Azure Table service mode

    """
    azure_kvstore = AzureKVStore.from_aad_token(
        endpoint, service_mode, partition_key
    )
    return cls(azure_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
options: members: - AzureIndexStore
