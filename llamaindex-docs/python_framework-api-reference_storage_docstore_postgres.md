# Postgres
##  PostgresDocumentStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/postgres/#llama_index.storage.docstore.postgres.PostgresDocumentStore "Permanent link")
Bases: `KVDocumentStore`
Postgres Document (Node) store.
A Postgres store for Document and Node objects.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `postgres_kvstore`  |   |  Postgres key-value store  |  _required_  |  
|  `namespace`  |  namespace for the docstore  |  `None`  |  
|  `batch_size`  |  batch size for bulk operations  |  `DEFAULT_BATCH_SIZE`  |  
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-postgres/llama_index/storage/docstore/postgres/base.py`  
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
```
 | 
```
classPostgresDocumentStore(KVDocumentStore):
"""
    Postgres Document (Node) store.

    A Postgres store for Document and Node objects.

    Args:
        postgres_kvstore (PostgresKVStore): Postgres key-value store
        namespace (str): namespace for the docstore
        batch_size (int): batch size for bulk operations

    """

    def__init__(
        self,
        postgres_kvstore: PostgresKVStore,
        namespace: Optional[str] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""Init a PostgresDocumentStore."""
        super().__init__(postgres_kvstore, namespace=namespace, batch_size=batch_size)

    @classmethod
    deffrom_uri(
        cls,
        uri: str,
        namespace: Optional[str] = None,
        table_name: str = "docstore",
        schema_name: str = "public",
        perform_setup: bool = True,
        debug: bool = False,
        use_jsonb: bool = False,
        create_engine_kwargs: Optional[Dict[str, Any]] = None,
    ) -> "PostgresDocumentStore":
"""Load a PostgresDocumentStore from a Postgres URI."""
        postgres_kvstore = PostgresKVStore.from_uri(
            uri=uri,
            table_name=table_name,
            schema_name=schema_name,
            perform_setup=perform_setup,
            debug=debug,
            use_jsonb=use_jsonb,
            create_engine_kwargs=create_engine_kwargs,
        )
        return cls(postgres_kvstore, namespace)

    @classmethod
    deffrom_params(
        cls,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        namespace: Optional[str] = None,
        table_name: str = "docstore",
        schema_name: str = "public",
        perform_setup: bool = True,
        debug: bool = False,
        use_jsonb: bool = False,
        create_engine_kwargs: Optional[Dict[str, Any]] = None,
    ) -> "PostgresDocumentStore":
"""Load a PostgresDocumentStore from a Postgres host and port."""
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
            create_engine_kwargs=create_engine_kwargs,
        )
        return cls(postgres_kvstore, namespace)

```
 |  
| --- | --- |  
###  from_uri `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/postgres/#llama_index.storage.docstore.postgres.PostgresDocumentStore.from_uri "Permanent link")

```
from_uri(
    uri: ,
    namespace: Optional[] = None,
    table_name:  = "docstore",
    schema_name:  = "public",
    perform_setup:  = True,
    debug:  = False,
    use_jsonb:  = False,
    create_engine_kwargs: Optional[[, ]] = None,
) -> 

```

Load a PostgresDocumentStore from a Postgres URI.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-postgres/llama_index/storage/docstore/postgres/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_uri(
    cls,
    uri: str,
    namespace: Optional[str] = None,
    table_name: str = "docstore",
    schema_name: str = "public",
    perform_setup: bool = True,
    debug: bool = False,
    use_jsonb: bool = False,
    create_engine_kwargs: Optional[Dict[str, Any]] = None,
) -> "PostgresDocumentStore":
"""Load a PostgresDocumentStore from a Postgres URI."""
    postgres_kvstore = PostgresKVStore.from_uri(
        uri=uri,
        table_name=table_name,
        schema_name=schema_name,
        perform_setup=perform_setup,
        debug=debug,
        use_jsonb=use_jsonb,
        create_engine_kwargs=create_engine_kwargs,
    )
    return cls(postgres_kvstore, namespace)

```
 |  
| --- | --- |  
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/postgres/#llama_index.storage.docstore.postgres.PostgresDocumentStore.from_params "Permanent link")

```
from_params(
    host: Optional[] = None,
    port: Optional[] = None,
    database: Optional[] = None,
    user: Optional[] = None,
    password: Optional[] = None,
    namespace: Optional[] = None,
    table_name:  = "docstore",
    schema_name:  = "public",
    perform_setup:  = True,
    debug:  = False,
    use_jsonb:  = False,
    create_engine_kwargs: Optional[[, ]] = None,
) -> 

```

Load a PostgresDocumentStore from a Postgres host and port.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-postgres/llama_index/storage/docstore/postgres/base.py`  
| 
```
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
    table_name: str = "docstore",
    schema_name: str = "public",
    perform_setup: bool = True,
    debug: bool = False,
    use_jsonb: bool = False,
    create_engine_kwargs: Optional[Dict[str, Any]] = None,
) -> "PostgresDocumentStore":
"""Load a PostgresDocumentStore from a Postgres host and port."""
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
        create_engine_kwargs=create_engine_kwargs,
    )
    return cls(postgres_kvstore, namespace)

```
 |  
| --- | --- |  
options: members: - PostgresDocumentStore
