# Elasticsearch
##  ElasticsearchDocumentStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/elasticsearch/#llama_index.storage.docstore.elasticsearch.ElasticsearchDocumentStore "Permanent link")
Bases: `KVDocumentStore`
Elasticsearch Document (Node) store.
An Elasticsearch store for Document and Node objects.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `elasticsearch_kvstore`  |   |  Elasticsearch key-value store  |  _required_  |  
|  `namespace`  |  namespace for the docstore  |  `None`  |  
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-elasticsearch/llama_index/storage/docstore/elasticsearch/base.py`  
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
classElasticsearchDocumentStore(KVDocumentStore):
"""
    Elasticsearch Document (Node) store.

    An Elasticsearch store for Document and Node objects.

    Args:
        elasticsearch_kvstore (ElasticsearchKVStore): Elasticsearch key-value store
        namespace (str): namespace for the docstore

    """

    def__init__(
        self,
        elasticsearch_kvstore: ElasticsearchKVStore,
        namespace: Optional[str] = None,
        node_collection_index: str = None,
        ref_doc_collection_index: str = None,
        metadata_collection_index: str = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""Init a ElasticsearchDocumentStore."""
        super().__init__(
            elasticsearch_kvstore, namespace=namespace, batch_size=batch_size
        )
        if node_collection_index:
            self._node_collection = node_collection_index
        else:
            self._node_collection = f"llama_index-docstore.data-{self._namespace}"

        if ref_doc_collection_index:
            self._ref_doc_collection = ref_doc_collection_index
        else:
            self._ref_doc_collection = (
                f"llama_index-docstore.ref_doc_info-{self._namespace}"
            )

        if metadata_collection_index:
            self._metadata_collection = metadata_collection_index
        else:
            self._metadata_collection = (
                f"llama_index-docstore.metadata-{self._namespace}"
            )

```
 |  
| --- | --- |  
options: members: - ElasticsearchDocumentStore
