# Redis
##  RedisIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/redis/#llama_index.storage.index_store.redis.RedisIndexStore "Permanent link")
Bases: `KVIndexStore`
Redis Index store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `redis_kvstore`  |   |  Redis key-value store  |  _required_  |  
|  `namespace`  |  namespace for the index store  |  `None`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-redis/llama_index/storage/index_store/redis/base.py`  
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
```
 | 
```
classRedisIndexStore(KVIndexStore):
"""
    Redis Index store.

    Args:
        redis_kvstore (RedisKVStore): Redis key-value store
        namespace (str): namespace for the index store

    """

    def__init__(
        self,
        redis_kvstore: RedisKVStore,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> None:
"""Init a RedisIndexStore."""
        super().__init__(
            redis_kvstore, namespace=namespace, collection_suffix=collection_suffix
        )
        # avoid conflicts with redis docstore
        if self._collection.endswith(DEFAULT_COLLECTION_SUFFIX):
            self._collection = f"{self._namespace}/index"

    @classmethod
    deffrom_redis_client(
        cls,
        redis_client: Any,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> "RedisIndexStore":
"""Load a RedisIndexStore from a Redis Client."""
        redis_kvstore = RedisKVStore.from_redis_client(redis_client=redis_client)
        return cls(redis_kvstore, namespace, collection_suffix)

    @classmethod
    deffrom_host_and_port(
        cls,
        host: str,
        port: int,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> "RedisIndexStore":
"""Load a RedisIndexStore from a Redis host and port."""
        redis_kvstore = RedisKVStore.from_host_and_port(host, port)
        return cls(redis_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_redis_client `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/redis/#llama_index.storage.index_store.redis.RedisIndexStore.from_redis_client "Permanent link")

```
from_redis_client(
    redis_client: ,
    namespace: Optional[] = None,
    collection_suffix: Optional[] = None,
) -> 

```

Load a RedisIndexStore from a Redis Client.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-redis/llama_index/storage/index_store/redis/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_redis_client(
    cls,
    redis_client: Any,
    namespace: Optional[str] = None,
    collection_suffix: Optional[str] = None,
) -> "RedisIndexStore":
"""Load a RedisIndexStore from a Redis Client."""
    redis_kvstore = RedisKVStore.from_redis_client(redis_client=redis_client)
    return cls(redis_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_host_and_port `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/redis/#llama_index.storage.index_store.redis.RedisIndexStore.from_host_and_port "Permanent link")

```
from_host_and_port(
    host: ,
    port: ,
    namespace: Optional[] = None,
    collection_suffix: Optional[] = None,
) -> 

```

Load a RedisIndexStore from a Redis host and port.
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-redis/llama_index/storage/index_store/redis/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_host_and_port(
    cls,
    host: str,
    port: int,
    namespace: Optional[str] = None,
    collection_suffix: Optional[str] = None,
) -> "RedisIndexStore":
"""Load a RedisIndexStore from a Redis host and port."""
    redis_kvstore = RedisKVStore.from_host_and_port(host, port)
    return cls(redis_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
options: members: - RedisIndexStore
