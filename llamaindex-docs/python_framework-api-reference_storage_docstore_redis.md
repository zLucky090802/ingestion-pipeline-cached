# Redis
##  RedisDocumentStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/redis/#llama_index.storage.docstore.redis.RedisDocumentStore "Permanent link")
Bases: `KVDocumentStore`
Redis Document (Node) store.
A Redis store for Document and Node objects.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `redis_kvstore`  |   |  Redis key-value store  |  _required_  |  
|  `namespace`  |  namespace for the docstore  |  `None`  |  
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-redis/llama_index/storage/docstore/redis/base.py`  
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
```
 | 
```
classRedisDocumentStore(KVDocumentStore):
"""
    Redis Document (Node) store.

    A Redis store for Document and Node objects.

    Args:
        redis_kvstore (RedisKVStore): Redis key-value store
        namespace (str): namespace for the docstore

    """

    def__init__(
        self,
        redis_kvstore: RedisKVStore,
        namespace: Optional[str] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""Init a RedisDocumentStore."""
        super().__init__(redis_kvstore, namespace=namespace, batch_size=batch_size)
        # avoid conflicts with redis index store
        self._node_collection = f"{self._namespace}/doc"

    @classmethod
    deffrom_redis_client(
        cls,
        redis_client: Any,
        namespace: Optional[str] = None,
    ) -> "RedisDocumentStore":
"""Load a RedisDocumentStore from a Redis Client."""
        redis_kvstore = RedisKVStore.from_redis_client(redis_client=redis_client)
        return cls(redis_kvstore, namespace)

    @classmethod
    deffrom_host_and_port(
        cls,
        host: str,
        port: int,
        namespace: Optional[str] = None,
    ) -> "RedisDocumentStore":
"""Load a RedisDocumentStore from a Redis host and port."""
        redis_kvstore = RedisKVStore.from_host_and_port(host, port)
        return cls(redis_kvstore, namespace)

```
 |  
| --- | --- |  
###  from_redis_client `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/redis/#llama_index.storage.docstore.redis.RedisDocumentStore.from_redis_client "Permanent link")

```
from_redis_client(
    redis_client: , namespace: Optional[] = None
) -> 

```

Load a RedisDocumentStore from a Redis Client.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-redis/llama_index/storage/docstore/redis/base.py`  
| 
```
31
32
33
34
35
36
37
38
39
```
 | 
```
@classmethod
deffrom_redis_client(
    cls,
    redis_client: Any,
    namespace: Optional[str] = None,
) -> "RedisDocumentStore":
"""Load a RedisDocumentStore from a Redis Client."""
    redis_kvstore = RedisKVStore.from_redis_client(redis_client=redis_client)
    return cls(redis_kvstore, namespace)

```
 |  
| --- | --- |  
###  from_host_and_port `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/redis/#llama_index.storage.docstore.redis.RedisDocumentStore.from_host_and_port "Permanent link")

```
from_host_and_port(
    host: , port: , namespace: Optional[] = None
) -> 

```

Load a RedisDocumentStore from a Redis host and port.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-redis/llama_index/storage/docstore/redis/base.py`  
| 
```
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
deffrom_host_and_port(
    cls,
    host: str,
    port: int,
    namespace: Optional[str] = None,
) -> "RedisDocumentStore":
"""Load a RedisDocumentStore from a Redis host and port."""
    redis_kvstore = RedisKVStore.from_host_and_port(host, port)
    return cls(redis_kvstore, namespace)

```
 |  
| --- | --- |  
options: members: - RedisDocumentStore
