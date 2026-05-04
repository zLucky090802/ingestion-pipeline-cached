# Postgres
##  PostgresIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/postgres/#llama_index.storage.index_store.postgres.PostgresIndexStore "Permanent link")
Bases: `KVIndexStore`
Postgres Index store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `postgres_kvstore`  |   |  Postgres key-value store  |  _required_  |  
|  `namespace`  |  namespace for the index store  |  `None`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-postgres/llama_index/storage/index_store/postgres/base.py`  
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
```
 | 
```
classPostgresIndexStore(KVIndexStore):
"""
    Postgres Index store.

    Args:
        postgres_kvstore (PostgresKVStore): Postgres key-value store
        namespace (str): namespace for the index store

    """

    def__init__(
        self,
        postgres_kvstore: PostgresKVStore,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> None:
"""Init a PostgresIndexStore."""
        super().__init__(
            postgres_kvstore, namespace=namespace, collection_suffix=collection_suffix
        )

    @classmethod
    deffrom_uri(
        cls,
        uri: str,
        namespace: Optional[str] = None,
        table_name: str = "indexstore",
        schema_name: str = "public",
        perform_setup: bool = True,
        debug: bool = False,
        use_jsonb: bool = False,
        collection_suffix: Optional[str] = None,
    ) -> "PostgresIndexStore":
"""Load a PostgresIndexStore from a PostgresURI."""
        postgres_kvstore = PostgresKVStore.from_uri(
            uri=uri,
            table_name=table_name,
            schema_name=schema_name,
            perform_setup=perform_setup,
            debug=debug,
            use_jsonb=use_jsonb,
        )
        return cls(postgres_kvstore, namespace, collection_suffix)

    @classmethod
    deffrom_params(
        cls,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        namespace: Optional[str] = None,
        table_name: str = "indexstore",
        schema_name: str = "public",
        perform_setup: bool = True,
        debug: bool = False,
        use_jsonb: bool = False,
        collection_suffix: Optional[str] = None,
    ) -> "PostgresIndexStore":
"""Load a PostgresIndexStore from a Postgres host and port."""
        postgres_kvstore = PostgresKVStore.from_params(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            table_name=table_name,
            schema_name=schema_name,
            perform_setup=perform_setup,
            debug=debug,
            use_jsonb=use_jsonb,
        )
        return cls(postgres_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_uri `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/postgres/#llama_index.storage.index_store.postgres.PostgresIndexStore.from_uri "Permanent link")

```
from_uri(
    uri: ,
    namespace: Optional[] = None,
    table_name:  = "indexstore",
    schema_name:  = "public",
    perform_setup:  = True,
    debug:  = False,
    use_jsonb:  = False,
    collection_suffix: Optional[] = None,
) -> 

```

Load a PostgresIndexStore from a PostgresURI.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-postgres/llama_index/storage/index_store/postgres/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_uri(
    cls,
    uri: str,
    namespace: Optional[str] = None,
    table_name: str = "indexstore",
    schema_name: str = "public",
    perform_setup: bool = True,
    debug: bool = False,
    use_jsonb: bool = False,
    collection_suffix: Optional[str] = None,
) -> "PostgresIndexStore":
"""Load a PostgresIndexStore from a PostgresURI."""
    postgres_kvstore = PostgresKVStore.from_uri(
        uri=uri,
        table_name=table_name,
        schema_name=schema_name,
        perform_setup=perform_setup,
        debug=debug,
        use_jsonb=use_jsonb,
    )
    return cls(postgres_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/postgres/#llama_index.storage.index_store.postgres.PostgresIndexStore.from_params "Permanent link")

```
from_params(
    host: Optional[] = None,
    port: Optional[] = None,
    database: Optional[] = None,
    user: Optional[] = None,
    password: Optional[] = None,
    namespace: Optional[] = None,
    table_name:  = "indexstore",
    schema_name:  = "public",
    perform_setup:  = True,
    debug:  = False,
    use_jsonb:  = False,
    collection_suffix: Optional[] = None,
) -> 

```

Load a PostgresIndexStore from a Postgres host and port.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-postgres/llama_index/storage/index_store/postgres/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_params(
    cls,
    host: Optional[str] = None,
    port: Optional[str] = None,
    database: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    namespace: Optional[str] = None,
    table_name: str = "indexstore",
    schema_name: str = "public",
    perform_setup: bool = True,
    debug: bool = False,
    use_jsonb: bool = False,
    collection_suffix: Optional[str] = None,
) -> "PostgresIndexStore":
"""Load a PostgresIndexStore from a Postgres host and port."""
    postgres_kvstore = PostgresKVStore.from_params(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        table_name=table_name,
        schema_name=schema_name,
        perform_setup=perform_setup,
        debug=debug,
        use_jsonb=use_jsonb,
    )
    return cls(postgres_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
options: members: - PostgresIndexStore
