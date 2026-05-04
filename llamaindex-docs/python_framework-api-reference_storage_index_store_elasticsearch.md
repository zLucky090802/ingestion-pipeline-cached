# Elasticsearch
##  ElasticsearchIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/elasticsearch/#llama_index.storage.index_store.elasticsearch.ElasticsearchIndexStore "Permanent link")
Bases: `KVIndexStore`
Elasticsearch Index store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `elasticsearch_kvstore`  |   |  Elasticsearch key-value store  |  _required_  |  
|  `namespace`  |  namespace for the index store  |  `None`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-elasticsearch/llama_index/storage/index_store/elasticsearch/base.py`  
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
```
 | 
```
classElasticsearchIndexStore(KVIndexStore):
"""
    Elasticsearch Index store.

    Args:
        elasticsearch_kvstore (ElasticsearchKVStore): Elasticsearch key-value store
        namespace (str): namespace for the index store

    """

    def__init__(
        self,
        elasticsearch_kvstore: ElasticsearchKVStore,
        collection_index: Optional[str] = None,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> None:
"""Init a ElasticsearchIndexStore."""
        super().__init__(
            elasticsearch_kvstore,
            namespace=namespace,
            collection_suffix=collection_suffix,
        )
        if collection_index:
            self._collection = collection_index
        else:
            self._collection = f"llama_index-index_store.data-{self._namespace}"

```
 |  
| --- | --- |  
options: members: - ElasticsearchIndexStore
