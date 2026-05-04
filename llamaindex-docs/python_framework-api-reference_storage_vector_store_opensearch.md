# Opensearch
##  OpensearchVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore "Permanent link")
Bases: 
Elasticsearch/Opensearch vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `client`  |   |  Vector index client to use for data insertion/querying.  |  _required_  |  
Examples:
`pip install llama-index-vector-stores-opensearch`

```
fromllama_index.vector_stores.opensearchimport (
    OpensearchVectorStore,
    OpensearchVectorClient,
)

# http endpoint for your cluster (opensearch required for vector index usage)
endpoint = "http://localhost:9200"
# index to demonstrate the VectorStore impl
idx = "gpt-index-demo"

# OpensearchVectorClient stores text in this field by default
text_field = "content"
# OpensearchVectorClient stores embeddings in this field by default
embedding_field = "embedding"

# OpensearchVectorClient encapsulates logic for a
# single opensearch index with vector search enabled
client = OpensearchVectorClient(
    endpoint, idx, 1536, embedding_field=embedding_field, text_field=text_field
)

# initialize vector store
vector_store = OpensearchVectorStore(client)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
```
 | 
```
classOpensearchVectorStore(BasePydanticVectorStore):
"""
    Elasticsearch/Opensearch vector store.

    Args:
        client (OpensearchVectorClient): Vector index client to use
            for data insertion/querying.

    Examples:
        `pip install llama-index-vector-stores-opensearch`

        ```python
        from llama_index.vector_stores.opensearch import (
            OpensearchVectorStore,
            OpensearchVectorClient,


        # http endpoint for your cluster (opensearch required for vector index usage)
        endpoint = "http://localhost:9200"
        # index to demonstrate the VectorStore impl
        idx = "gpt-index-demo"

        # OpensearchVectorClient stores text in this field by default
        text_field = "content"
        # OpensearchVectorClient stores embeddings in this field by default
        embedding_field = "embedding"

        # OpensearchVectorClient encapsulates logic for a
        # single opensearch index with vector search enabled
        client = OpensearchVectorClient(
            endpoint, idx, 1536, embedding_field=embedding_field, text_field=text_field


        # initialize vector store
        vector_store = OpensearchVectorStore(client)
        ```

    """

    stores_text: bool = True
    _client: OpensearchVectorClient = PrivateAttr(default=None)

    def__init__(
        self,
        client: OpensearchVectorClient,
    ) -> None:
"""Initialize params."""
        super().__init__()
        self._client = client

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._client

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings.

        """
        self._client.index_results(nodes)
        return [result.node_id for result in nodes]

    async defasync_add(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Async add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings.

        """
        await self._client.aindex_results(nodes)
        return [result.node_id for result in nodes]

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        self._client.delete_by_doc_id(ref_doc_id)

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Async delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        await self._client.adelete_by_doc_id(ref_doc_id)

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Deletes nodes async.

        Args:
            node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
            filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

        """
        self._client.delete_nodes(node_ids, filters, **delete_kwargs)

    async defadelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Async deletes nodes async.

        Args:
            node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
            filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

        """
        await self._client.adelete_nodes(node_ids, filters, **delete_kwargs)

    defclear(self) -> None:
"""Clears index."""
        self._client.clear()

    async defaclear(self) -> None:
"""Async clears index."""
        await self._client.aclear()

    defclose(self) -> None:
"""Close the vector store and release resources."""
        self._client.close()

    async defaclose(self) -> None:
"""Asynchronously close the vector store and release resources."""
        await self._client.aclose()

    def__del__(self) -> None:
"""Clean up resources during garbage collection."""
        try:
            self.close()
        except Exception as exc:
            logger.debug(
                "Failed to close OpenSearch vector store during garbage collection, "
                "type=%s err='%s'",
                type(exc),
                exc,
            )

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): Store query object.

        """
        query_embedding = cast(List[float], query.query_embedding)

        return self._client.query(
            query.mode,
            query.query_str,
            query_embedding,
            query.similarity_top_k,
            filters=query.filters,
        )

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Async query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): Store query object.

        """
        query_embedding = cast(List[float], query.query_embedding)

        return await self._client.aquery(
            query.mode,
            query.query_str,
            query_embedding,
            query.similarity_top_k,
            filters=query.filters,
        )

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.client "Permanent link")

```
client: 

```

Get client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings.

    """
    self._client.index_results(nodes)
    return [result.node_id for result in nodes]

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.async_add "Permanent link")

```
async_add(
    nodes: [], **add_kwargs: 
) -> []

```

Async add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
```
 | 
```
async defasync_add(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""
    Async add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings.

    """
    await self._client.aindex_results(nodes)
    return [result.node_id for result in nodes]

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1137
1138
1139
1140
1141
1142
1143
1144
1145
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    self._client.delete_by_doc_id(ref_doc_id)

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Async delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1147
1148
1149
1150
1151
1152
1153
1154
1155
```
 | 
```
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Async delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    await self._client.adelete_by_doc_id(ref_doc_id)

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Deletes nodes async.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  IDs of nodes to delete. Defaults to None.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters. Defaults to None.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Deletes nodes async.

    Args:
        node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
        filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

    """
    self._client.delete_nodes(node_ids, filters, **delete_kwargs)

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Async deletes nodes async.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  IDs of nodes to delete. Defaults to None.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters. Defaults to None.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Async deletes nodes async.

    Args:
        node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
        filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

    """
    await self._client.adelete_nodes(node_ids, filters, **delete_kwargs)

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.clear "Permanent link")

```
clear() -> None

```

Clears index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1189
1190
1191
```
 | 
```
defclear(self) -> None:
"""Clears index."""
    self._client.clear()

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.aclear "Permanent link")

```
aclear() -> None

```

Async clears index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1193
1194
1195
```
 | 
```
async defaclear(self) -> None:
"""Async clears index."""
    await self._client.aclear()

```
 |  
| --- | --- |  
###  close [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.close "Permanent link")

```
close() -> None

```

Close the vector store and release resources.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1197
1198
1199
```
 | 
```
defclose(self) -> None:
"""Close the vector store and release resources."""
    self._client.close()

```
 |  
| --- | --- |  
###  aclose [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.aclose "Permanent link")

```
aclose() -> None

```

Asynchronously close the vector store and release resources.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1201
1202
1203
```
 | 
```
async defaclose(self) -> None:
"""Asynchronously close the vector store and release resources."""
    await self._client.aclose()

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Store query object.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
1232
1233
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): Store query object.

    """
    query_embedding = cast(List[float], query.query_embedding)

    return self._client.query(
        query.mode,
        query.query_str,
        query_embedding,
        query.similarity_top_k,
        filters=query.filters,
    )

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Async query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Store query object.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:
"""
    Async query index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): Store query object.

    """
    query_embedding = cast(List[float], query.query_embedding)

    return await self._client.aquery(
        query.mode,
        query.query_str,
        query_embedding,
        query.similarity_top_k,
        filters=query.filters,
    )

```
 |  
| --- | --- |  
##  OpensearchVectorClient [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorClient "Permanent link")
Object encapsulating an Opensearch index that has vector search enabled.
Index creation is deferred until first use (e.g., query, add, delete) rather than during construction. This avoids making network calls in **init** , which prevents `RuntimeError: This event loop is already running` in environments like Jupyter notebooks and FastAPI that already have a running event loop.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `endpoint`  |  URL (http/https) of elasticsearch endpoint  |  _required_  |  
|  `index`  |  Name of the elasticsearch index  |  _required_  |  
|  `dim`  |  Dimension of the vector  |  _required_  |  
|  `embedding_field`  |  Name of the field in the index to store embedding array in.  |  `'embedding'`  |  
|  `text_field`  |  Name of the field to grab text from  |  `'content'`  |  
|  `method`  |  `Optional[dict]`  |  Opensearch "method" JSON obj for configuring the KNN index. This includes engine, metric, and other config params. Defaults to: {"name": "hnsw", "space_type": "l2", "engine": "faiss", "parameters": {"ef_construction": 256, "m": 48}}  |  `None`  |  
|  `settings`  |  `Optional[dict]`  |  Optional[dict]: Settings for the Opensearch index creation. Defaults to: {"index": {"knn": True, "knn.algo_param.ef_search": 100}}  |  `None`  |  
|  `space_type`  |  `Optional[str]`  |  space type for distance metric calculation. Defaults to: l2  |  `'l2'`  |  
|  `idx_conf`  |  `Optional[dict]`  |  Optional[dict]: Custom index configuration for Opensearch. Defaults to None and will overwrite settings above.  |  `None`  |  
|  `os_client`  |  `Optional[Client]`  |  Custom synchronous client (see OpenSearch from opensearch-py)  |  `None`  |  
|  `os_async_client`  |  `Optional[Client]`  |  Custom asynchronous client (see AsyncOpenSearch from opensearch-py)  |  `None`  |  
|  `excluded_source_fields`  |  `Optional[List[str]]`  |  Optional list of document "source" fields to exclude from OpenSearch responses.  |  `None`  |  
|  `**kwargs`  |  Optional arguments passed to the OpenSearch client from opensearch-py.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
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
 147
 148
 149
 150
 151
 152
 153
 154
 155
 156
 157
 158
 159
 160
 161
 162
 163
 164
 165
 166
 167
 168
 169
 170
 171
 172
 173
 174
 175
 176
 177
 178
 179
 180
 181
 182
 183
 184
 185
 186
 187
 188
 189
 190
 191
 192
 193
 194
 195
 196
 197
 198
 199
 200
 201
 202
 203
 204
 205
 206
 207
 208
 209
 210
 211
 212
 213
 214
 215
 216
 217
 218
 219
 220
 221
 222
 223
 224
 225
 226
 227
 228
 229
 230
 231
 232
 233
 234
 235
 236
 237
 238
 239
 240
 241
 242
 243
 244
 245
 246
 247
 248
 249
 250
 251
 252
 253
 254
 255
 256
 257
 258
 259
 260
 261
 262
 263
 264
 265
 266
 267
 268
 269
 270
 271
 272
 273
 274
 275
 276
 277
 278
 279
 280
 281
 282
 283
 284
 285
 286
 287
 288
 289
 290
 291
 292
 293
 294
 295
 296
 297
 298
 299
 300
 301
 302
 303
 304
 305
 306
 307
 308
 309
 310
 311
 312
 313
 314
 315
 316
 317
 318
 319
 320
 321
 322
 323
 324
 325
 326
 327
 328
 329
 330
 331
 332
 333
 334
 335
 336
 337
 338
 339
 340
 341
 342
 343
 344
 345
 346
 347
 348
 349
 350
 351
 352
 353
 354
 355
 356
 357
 358
 359
 360
 361
 362
 363
 364
 365
 366
 367
 368
 369
 370
 371
 372
 373
 374
 375
 376
 377
 378
 379
 380
 381
 382
 383
 384
 385
 386
 387
 388
 389
 390
 391
 392
 393
 394
 395
 396
 397
 398
 399
 400
 401
 402
 403
 404
 405
 406
 407
 408
 409
 410
 411
 412
 413
 414
 415
 416
 417
 418
 419
 420
 421
 422
 423
 424
 425
 426
 427
 428
 429
 430
 431
 432
 433
 434
 435
 436
 437
 438
 439
 440
 441
 442
 443
 444
 445
 446
 447
 448
 449
 450
 451
 452
 453
 454
 455
 456
 457
 458
 459
 460
 461
 462
 463
 464
 465
 466
 467
 468
 469
 470
 471
 472
 473
 474
 475
 476
 477
 478
 479
 480
 481
 482
 483
 484
 485
 486
 487
 488
 489
 490
 491
 492
 493
 494
 495
 496
 497
 498
 499
 500
 501
 502
 503
 504
 505
 506
 507
 508
 509
 510
 511
 512
 513
 514
 515
 516
 517
 518
 519
 520
 521
 522
 523
 524
 525
 526
 527
 528
 529
 530
 531
 532
 533
 534
 535
 536
 537
 538
 539
 540
 541
 542
 543
 544
 545
 546
 547
 548
 549
 550
 551
 552
 553
 554
 555
 556
 557
 558
 559
 560
 561
 562
 563
 564
 565
 566
 567
 568
 569
 570
 571
 572
 573
 574
 575
 576
 577
 578
 579
 580
 581
 582
 583
 584
 585
 586
 587
 588
 589
 590
 591
 592
 593
 594
 595
 596
 597
 598
 599
 600
 601
 602
 603
 604
 605
 606
 607
 608
 609
 610
 611
 612
 613
 614
 615
 616
 617
 618
 619
 620
 621
 622
 623
 624
 625
 626
 627
 628
 629
 630
 631
 632
 633
 634
 635
 636
 637
 638
 639
 640
 641
 642
 643
 644
 645
 646
 647
 648
 649
 650
 651
 652
 653
 654
 655
 656
 657
 658
 659
 660
 661
 662
 663
 664
 665
 666
 667
 668
 669
 670
 671
 672
 673
 674
 675
 676
 677
 678
 679
 680
 681
 682
 683
 684
 685
 686
 687
 688
 689
 690
 691
 692
 693
 694
 695
 696
 697
 698
 699
 700
 701
 702
 703
 704
 705
 706
 707
 708
 709
 710
 711
 712
 713
 714
 715
 716
 717
 718
 719
 720
 721
 722
 723
 724
 725
 726
 727
 728
 729
 730
 731
 732
 733
 734
 735
 736
 737
 738
 739
 740
 741
 742
 743
 744
 745
 746
 747
 748
 749
 750
 751
 752
 753
 754
 755
 756
 757
 758
 759
 760
 761
 762
 763
 764
 765
 766
 767
 768
 769
 770
 771
 772
 773
 774
 775
 776
 777
 778
 779
 780
 781
 782
 783
 784
 785
 786
 787
 788
 789
 790
 791
 792
 793
 794
 795
 796
 797
 798
 799
 800
 801
 802
 803
 804
 805
 806
 807
 808
 809
 810
 811
 812
 813
 814
 815
 816
 817
 818
 819
 820
 821
 822
 823
 824
 825
 826
 827
 828
 829
 830
 831
 832
 833
 834
 835
 836
 837
 838
 839
 840
 841
 842
 843
 844
 845
 846
 847
 848
 849
 850
 851
 852
 853
 854
 855
 856
 857
 858
 859
 860
 861
 862
 863
 864
 865
 866
 867
 868
 869
 870
 871
 872
 873
 874
 875
 876
 877
 878
 879
 880
 881
 882
 883
 884
 885
 886
 887
 888
 889
 890
 891
 892
 893
 894
 895
 896
 897
 898
 899
 900
 901
 902
 903
 904
 905
 906
 907
 908
 909
 910
 911
 912
 913
 914
 915
 916
 917
 918
 919
 920
 921
 922
 923
 924
 925
 926
 927
 928
 929
 930
 931
 932
 933
 934
 935
 936
 937
 938
 939
 940
 941
 942
 943
 944
 945
 946
 947
 948
 949
 950
 951
 952
 953
 954
 955
 956
 957
 958
 959
 960
 961
 962
 963
 964
 965
 966
 967
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
```
 | 
```
classOpensearchVectorClient:
"""
    Object encapsulating an Opensearch index that has vector search enabled.

    Index creation is deferred until first use (e.g., query, add, delete) rather
    than during construction. This avoids making network calls in __init__, which
    prevents ``RuntimeError: This event loop is already running`` in environments
    like Jupyter notebooks and FastAPI that already have a running event loop.

    Args:
        endpoint (str): URL (http/https) of elasticsearch endpoint
        index (str): Name of the elasticsearch index
        dim (int): Dimension of the vector
        embedding_field (str): Name of the field in the index to store
            embedding array in.
        text_field (str): Name of the field to grab text from
        method (Optional[dict]): Opensearch "method" JSON obj for configuring
            the KNN index.
            This includes engine, metric, and other config params. Defaults to:
            {"name": "hnsw", "space_type": "l2", "engine": "faiss",
            "parameters": {"ef_construction": 256, "m": 48}}
        settings: Optional[dict]: Settings for the Opensearch index creation. Defaults to:
            {"index": {"knn": True, "knn.algo_param.ef_search": 100}}
        space_type (Optional[str]): space type for distance metric calculation. Defaults to: l2
        idx_conf: Optional[dict]: Custom index configuration for Opensearch. Defaults to None and will overwrite settings above.
        os_client (Optional[OSClient]): Custom synchronous client (see OpenSearch from opensearch-py)
        os_async_client (Optional[OSClient]): Custom asynchronous client (see AsyncOpenSearch from opensearch-py)
        excluded_source_fields (Optional[List[str]]): Optional list of document "source" fields to exclude from OpenSearch responses.
        **kwargs: Optional arguments passed to the OpenSearch client from opensearch-py.

    """

    def__init__(
        self,
        endpoint: str,
        index: str,
        dim: int,
        embedding_field: str = "embedding",
        text_field: str = "content",
        method: Optional[dict] = None,
        settings: Optional[dict] = None,
        engine: Optional[str] = "faiss",
        space_type: Optional[str] = "l2",
        idx_conf: Optional[dict] = None,
        max_chunk_bytes: int = 1 * 1024 * 1024,
        search_pipeline: Optional[str] = None,
        os_client: Optional[OSClient] = None,
        os_async_client: Optional[OSClient] = None,
        excluded_source_fields: Optional[List[str]] = None,
        **kwargs: Any,
    ):
"""Init params."""
        if engine == "nmslib":
            warnings.warn(
                "nmslib engine is deprecated in OpenSearch starting from version 3.0.0, consider using faiss or lucene instead.",
                FutureWarning,
            )
        if method is None:
            method = {
                "name": "hnsw",
                "space_type": "l2",
                "engine": engine,
                "parameters": {"ef_construction": 256, "m": 48},
            }
        if settings is None:
            settings = {"index": {"knn": True, "knn.algo_param.ef_search": 100}}
        if embedding_field is None:
            embedding_field = "embedding"

        self._method = method
        self._embedding_field = embedding_field
        self._endpoint = endpoint
        self._dim = dim
        self._index = index
        self._text_field = text_field
        self._max_chunk_bytes = max_chunk_bytes
        self._excluded_source_fields = excluded_source_fields

        self._search_pipeline = search_pipeline
        http_auth = kwargs.get("http_auth")
        self.space_type = space_type
        self.is_aoss = self._is_aoss_enabled(http_auth=http_auth)
        # initialize mapping
        if idx_conf is None:
            idx_conf = {
                "settings": settings,
                "mappings": {
                    "properties": {
                        embedding_field: {
                            "type": "knn_vector",
                            "dimension": dim,
                            "method": method,
                        },
                    }
                },
            }
        self._idx_conf = idx_conf
        self._owns_os_client = os_client is None
        self._owns_os_async_client = os_async_client is None
        self._os_client = os_client or self._get_opensearch_client(
            self._endpoint, **kwargs
        )
        self._os_async_client = os_async_client or self._get_async_opensearch_client(
            self._endpoint, **kwargs
        )
        self._initialized = False
        self._efficient_filtering_enabled = False

    def_import_opensearch(self) -> Any:
"""Import OpenSearch if available, otherwise raise error."""
        try:
            fromopensearchpyimport OpenSearch
        except ImportError:
            raise ImportError(IMPORT_OPENSEARCH_PY_ERROR)
        return OpenSearch

    def_import_async_opensearch(self) -> Any:
"""Import AsyncOpenSearch if available, otherwise raise error."""
        try:
            fromopensearchpyimport AsyncOpenSearch
        except ImportError:
            raise ImportError(IMPORT_ASYNC_OPENSEARCH_PY_ERROR)
        return AsyncOpenSearch

    def_import_bulk(self) -> Any:
"""Import bulk if available, otherwise raise error."""
        try:
            fromopensearchpy.helpersimport bulk
        except ImportError:
            raise ImportError(IMPORT_OPENSEARCH_PY_ERROR)
        return bulk

    def_import_async_bulk(self) -> Any:
"""Import async_bulk if available, otherwise raise error."""
        try:
            fromopensearchpy.helpersimport async_bulk
        except ImportError:
            raise ImportError(IMPORT_ASYNC_OPENSEARCH_PY_ERROR)
        return async_bulk

    def_import_not_found_error(self) -> Any:
"""Import not found error if available, otherwise raise error."""
        try:
            fromopensearchpy.exceptionsimport NotFoundError
        except ImportError:
            raise ImportError(IMPORT_OPENSEARCH_PY_ERROR)
        return NotFoundError

    def_get_opensearch_client(self, opensearch_url: str, **kwargs: Any) -> Any:
"""Get OpenSearch client from the opensearch_url, otherwise raise error."""
        try:
            opensearch = self._import_opensearch()
            client = opensearch(opensearch_url, **kwargs)
        except ValueError as e:
            raise ImportError(
                f"OpenSearch client string provided is not in proper format. "
                f"Got error: {e} "
            )
        return client

    def_get_async_opensearch_client(self, opensearch_url: str, **kwargs: Any) -> Any:
"""Get AsyncOpenSearch client from the opensearch_url, otherwise raise error."""
        try:
            opensearch = self._import_async_opensearch()
            client = opensearch(opensearch_url, **kwargs)

        except ValueError as e:
            raise ValueError(
                f"AsyncOpenSearch client string provided is not in proper format. "
                f"Got error: {e} "
            )
        return client

    def_get_opensearch_version(self) -> str:
        info = self._os_client.info()
        return info["version"]["number"]

    async def_aget_opensearch_version(self) -> str:
        info = await self._os_async_client.info()
        return info["version"]["number"]

    def_ensure_initialized(self) -> None:
"""Lazily initialize the index on first use (sync)."""
        if self._initialized:
            return
        self._efficient_filtering_enabled = self._is_efficient_filtering_enabled()
        not_found_error = self._import_not_found_error()
        try:
            self._os_client.indices.get(index=self._index)
        except not_found_error:
            self._os_client.indices.create(index=self._index, body=self._idx_conf)
            if self.is_aoss:
                self._os_client.indices.exists(index=self._index)
            else:
                self._os_client.indices.refresh(index=self._index)
        self._initialized = True

    async def_async_ensure_initialized(self) -> None:
"""Lazily initialize the index on first use (async)."""
        if self._initialized:
            return
        self._efficient_filtering_enabled = (
            await self._async_is_efficient_filtering_enabled()
        )
        not_found_error = self._import_not_found_error()
        try:
            await self._os_async_client.indices.get(index=self._index)
        except not_found_error:
            await self._os_async_client.indices.create(
                index=self._index, body=self._idx_conf
            )
            if self.is_aoss:
                await self._os_async_client.indices.exists(index=self._index)
            else:
                await self._os_async_client.indices.refresh(index=self._index)
        self._initialized = True

    def_bulk_ingest_embeddings(
        self,
        client: Any,
        index_name: str,
        embeddings: List[List[float]],
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        vector_field: str = "embedding",
        text_field: str = "content",
        mapping: Optional[Dict] = None,
        max_chunk_bytes: Optional[int] = 1 * 1024 * 1024,
        is_aoss: bool = False,
    ) -> List[str]:
"""Bulk Ingest Embeddings into given index."""
        if not mapping:
            mapping = {}

        bulk = self._import_bulk()
        not_found_error = self._import_not_found_error()
        requests = []
        return_ids = []

        try:
            client.indices.get(index=index_name)
        except not_found_error:
            client.indices.create(index=index_name, body=mapping)

        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas else {}
            _id = ids[i] if ids else str(uuid.uuid4())
            request = {
                "_op_type": "index",
                "_index": index_name,
                vector_field: embeddings[i],
                text_field: text,
                "metadata": metadata,
            }
            if is_aoss:
                request["id"] = _id
            else:
                request["_id"] = _id
            requests.append(request)
            return_ids.append(_id)

        bulk(client, requests, max_chunk_bytes=max_chunk_bytes)
        if not is_aoss:
            client.indices.refresh(index=index_name)

        return return_ids

    async def_abulk_ingest_embeddings(
        self,
        client: Any,
        index_name: str,
        embeddings: List[List[float]],
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        vector_field: str = "embedding",
        text_field: str = "content",
        mapping: Optional[Dict] = None,
        max_chunk_bytes: Optional[int] = 1 * 1024 * 1024,
        is_aoss: bool = False,
    ) -> List[str]:
"""Async Bulk Ingest Embeddings into given index."""
        if not mapping:
            mapping = {}

        async_bulk = self._import_async_bulk()
        not_found_error = self._import_not_found_error()
        requests = []
        return_ids = []

        try:
            await client.indices.get(index=index_name)
        except not_found_error:
            await client.indices.create(index=index_name, body=mapping)

        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas else {}
            _id = ids[i] if ids else str(uuid.uuid4())
            request = {
                "_op_type": "index",
                "_index": index_name,
                vector_field: embeddings[i],
                text_field: text,
                "metadata": metadata,
            }
            if is_aoss:
                request["id"] = _id
            else:
                request["_id"] = _id
            requests.append(request)
            return_ids.append(_id)

        await async_bulk(client, requests, max_chunk_bytes=max_chunk_bytes)
        if not is_aoss:
            await client.indices.refresh(index=index_name)

        return return_ids

    def_default_approximate_search_query(
        self,
        query_vector: List[float],
        k: int = 4,
        filters: Optional[Union[Dict, List]] = None,
        vector_field: str = "embedding",
        excluded_source_fields: Optional[List[str]] = None,
    ) -> Dict:
"""For Approximate k-NN Search, this is the default query."""
        query = {
            "size": k,
            "query": {
                "knn": {
                    vector_field: {
                        "vector": query_vector,
                        "k": k,
                    }
                }
            },
        }

        if filters:
            # filter key must be added only when filtering to avoid "filter doesn't support values of type: START_ARRAY" exception
            query["query"]["knn"][vector_field]["filter"] = filters
        if excluded_source_fields:
            query["_source"] = {"exclude": excluded_source_fields}
        return query

    def_is_text_field(self, value: Any) -> bool:
"""
        Check if value is a string and keyword filtering needs to be performed.

        Not applied to datetime strings.
        """
        if isinstance(value, str):
            try:
                datetime.fromisoformat(value)
                return False
            except ValueError as e:
                return True
        else:
            return False

    def_parse_filter(self, filter: MetadataFilter) -> dict:
"""
        Parse a single MetadataFilter to equivalent OpenSearch expression.

        As Opensearch does not differentiate between scalar/array keyword fields, IN and ANY are equivalent.
        """
        key = f"metadata.{filter.key}"
        op = filter.operator

        equality_postfix = ".keyword" if self._is_text_field(value=filter.value) else ""

        if op == FilterOperator.EQ:
            return {"term": {f"{key}{equality_postfix}": filter.value}}
        elif op in [
            FilterOperator.GT,
            FilterOperator.GTE,
            FilterOperator.LT,
            FilterOperator.LTE,
        ]:
            return {"range": {key: {filter.operator.name.lower(): filter.value}}}
        elif op == FilterOperator.NE:
            return {
                "bool": {
                    "must_not": {"term": {f"{key}{equality_postfix}": filter.value}}
                }
            }
        elif op in [FilterOperator.IN, FilterOperator.ANY]:
            if isinstance(filter.value, list) and all(
                self._is_text_field(val) for val in filter.value
            ):
                return {"terms": {f"{key}.keyword": filter.value}}
            else:
                return {"terms": {key: filter.value}}
        elif op == FilterOperator.NIN:
            return {"bool": {"must_not": {"terms": {key: filter.value}}}}
        elif op == FilterOperator.ALL:
            return {
                "terms_set": {
                    key: {
                        "terms": filter.value,
                        "minimum_should_match_script": {"source": "params.num_terms"},
                    }
                }
            }
        elif op in (FilterOperator.TEXT_MATCH, FilterOperator.TEXT_MATCH_INSENSITIVE):
            return {"match": {key: {"query": filter.value, "fuzziness": "AUTO"}}}
        elif op == FilterOperator.CONTAINS:
            return {"wildcard": {key: f"*{filter.value}*"}}
        elif op == FilterOperator.IS_EMPTY:
            return {"bool": {"must_not": {"exists": {"field": key}}}}
        else:
            raise ValueError(f"Unsupported filter operator: {filter.operator}")

    def_parse_filters_recursively(self, filters: MetadataFilters) -> dict:
"""Parse (possibly nested) MetadataFilters to equivalent OpenSearch expression."""
        condition_map = {FilterCondition.AND: "must", FilterCondition.OR: "should"}

        bool_clause = condition_map[filters.condition]
        bool_query: dict[str, dict[str, list[dict]]] = {"bool": {bool_clause: []}}

        for filter_item in filters.filters:
            if isinstance(filter_item, MetadataFilter):
                bool_query["bool"][bool_clause].append(self._parse_filter(filter_item))
            elif isinstance(filter_item, MetadataFilters):
                bool_query["bool"][bool_clause].append(
                    self._parse_filters_recursively(filter_item)
                )
            else:
                raise ValueError(f"Unsupported filter type: {type(filter_item)}")

        return bool_query

    def_parse_filters(self, filters: Optional[MetadataFilters]) -> List[dict]:
"""Parse MetadataFilters to equivalent OpenSearch expression."""
        if filters is None:
            return []
        return [self._parse_filters_recursively(filters=filters)]

    def_knn_search_query(
        self,
        embedding_field: str,
        query_embedding: List[float],
        k: int,
        filters: Optional[MetadataFilters] = None,
        search_method="approximate",
        excluded_source_fields: Optional[List[str]] = None,
    ) -> Dict:
"""
        Perform a k-Nearest Neighbors (kNN) search.

        If the search method is "approximate" and the engine is "lucene" or "faiss", use efficient kNN filtering.
        Otherwise, perform an exhaustive exact kNN search using "painless scripting" if the version of
        OpenSearch supports it. If the OpenSearch version does not support it, use scoring script search.

        Note:
            - AWS OpenSearch Serverless does not support the painless scripting functionality at this time according to AWS.
            - Approximate kNN search does not support pre-filtering.

        Args:
            query_embedding (List[float]): Vector embedding to query.
            k (int): Maximum number of results.
            filters (Optional[MetadataFilters]): Optional filters to apply for the search.
                Supports filter-context queries documented at
                https://opensearch.org/docs/latest/query-dsl/query-filter-context/
            excluded_source_fields: Optional list of document "source" fields to exclude from the response.

        Returns:
            Dict: Up to k documents closest to query_embedding.

        """
        filters = self._parse_filters(filters)

        if not filters:
            search_query = self._default_approximate_search_query(
                query_embedding,
                k,
                vector_field=embedding_field,
                excluded_source_fields=excluded_source_fields,
            )
        elif (
            search_method == "approximate"
            and self._method["engine"]
            in [
                "lucene",
                "faiss",
            ]
            and self._efficient_filtering_enabled
        ):
            # if engine is lucene or faiss, opensearch recommends efficient-kNN filtering.
            search_query = self._default_approximate_search_query(
                query_embedding,
                k,
                filters={"bool": {"filter": filters}},
                vector_field=embedding_field,
                excluded_source_fields=excluded_source_fields,
            )
        else:
            if self.is_aoss:
                # if is_aoss is set we are using Opensearch Serverless AWS offering which cannot use
                # painless scripting so default scoring script returned will be just normal knn_score script
                search_query = self._default_scoring_script_query(
                    query_embedding,
                    k,
                    space_type=self.space_type,
                    pre_filter={"bool": {"filter": filters}},
                    vector_field=embedding_field,
                    excluded_source_fields=excluded_source_fields,
                )
            else:
                # https://opensearch.org/docs/latest/search-plugins/knn/painless-functions/
                search_query = self._default_scoring_script_query(
                    query_embedding,
                    k,
                    space_type="l2Squared",
                    pre_filter={"bool": {"filter": filters}},
                    vector_field=embedding_field,
                    excluded_source_fields=excluded_source_fields,
                )
        return search_query

    def_hybrid_search_query(
        self,
        text_field: str,
        query_str: str,
        embedding_field: str,
        query_embedding: List[float],
        k: int,
        filters: Optional[MetadataFilters] = None,
        excluded_source_fields: Optional[List[str]] = None,
    ) -> Dict:
        knn_query = self._knn_search_query(embedding_field, query_embedding, k, filters)
        lexical_query = self._lexical_search_query(text_field, query_str, k, filters)

        query = {
            "size": k,
            "query": {
                "hybrid": {"queries": [lexical_query["query"], knn_query["query"]]}
            },
        }
        if excluded_source_fields:
            query["_source"] = {"exclude": excluded_source_fields}
        return query

    def_lexical_search_query(
        self,
        text_field: str,
        query_str: str,
        k: int,
        filters: Optional[MetadataFilters] = None,
        excluded_source_fields: Optional[List[str]] = None,
    ) -> Dict:
        lexical_query = {
            "bool": {"must": {"match": {text_field: {"query": query_str}}}}
        }

        parsed_filters = self._parse_filters(filters)
        if len(parsed_filters)  0:
            lexical_query["bool"]["filter"] = parsed_filters

        query = {
            "size": k,
            "query": lexical_query,
        }
        if excluded_source_fields:
            query["_source"] = {"exclude": excluded_source_fields}
        return query

    def__get_painless_scripting_source(
        self, space_type: str, vector_field: str = "embedding"
    ) -> str:
"""
        For Painless Scripting, it returns the script source based on space type.
        This does not work with Opensearch Serverless currently.
        """
        source_value = (
            f"(1.0 + {space_type}(params.query_value, doc['{vector_field}']))"
        )
        if space_type == "cosineSimilarity":
            return source_value
        else:
            return f"1/{source_value}"

    def_get_knn_scoring_script(self, space_type, vector_field, query_vector):
"""Default scoring script that will work with AWS Opensearch Serverless."""
        return {
            "source": "knn_score",
            "lang": "knn",
            "params": {
                "field": vector_field,
                "query_value": query_vector,
                "space_type": space_type,
            },
        }

    def_get_painless_scoring_script(self, space_type, vector_field, query_vector):
        source = self.__get_painless_scripting_source(space_type, vector_field)
        return {
            "source": source,
            "params": {
                "field": vector_field,
                "query_value": query_vector,
            },
        }

    def_default_scoring_script_query(
        self,
        query_vector: List[float],
        k: int = 4,
        space_type: str = "l2Squared",
        pre_filter: Optional[Union[Dict, List]] = None,
        vector_field: str = "embedding",
        excluded_source_fields: Optional[List[str]] = None,
    ) -> Dict:
"""
        For Scoring Script Search, this is the default query. Has to account for Opensearch Service
        Serverless which does not support painless scripting functions so defaults to knn_score.
        """
        if not pre_filter:
            pre_filter = MATCH_ALL_QUERY

        # check if we can use painless scripting or have to use default knn_score script
        if self.is_aoss:
            if space_type == "l2Squared":
                raise ValueError(
                    "Unsupported space type for aoss. Can only use l1, l2, cosinesimil."
                )
            script = self._get_knn_scoring_script(
                space_type, vector_field, query_vector
            )
        else:
            script = self._get_painless_scoring_script(
                space_type, vector_field, query_vector
            )
        query = {
            "size": k,
            "query": {
                "script_score": {
                    "query": pre_filter,
                    "script": script,
                }
            },
        }
        if excluded_source_fields:
            query["_source"] = {"exclude": excluded_source_fields}
        return query

    def_is_aoss_enabled(self, http_auth: Any) -> bool:
"""Check if the service is http_auth is set as `aoss`."""
        return (
            http_auth is not None
            and hasattr(http_auth, "service")
            and http_auth.service == "aoss"
        )

    @staticmethod
    def_version_supports_efficient_filtering(version: str) -> bool:
"""Return True if the OpenSearch version supports efficient kNN filtering."""
        major, minor, _patch = version.split(".")
        return int(major)  2 or (int(major) == 2 and int(minor) >= 9)

    def_is_efficient_filtering_enabled(self) -> bool:
"""Check if kNN with efficient filtering is enabled."""
        # Technically, AOSS supports efficient filtering,
        # but we can't check the version number using .info(); AOSS doesn't support 'GET /'
        #  so we must skip and disable by default.
        if self.is_aoss:
            return False
        self._os_version = self._get_opensearch_version()
        return self._version_supports_efficient_filtering(self._os_version)

    async def_async_is_efficient_filtering_enabled(self) -> bool:
"""Async check if kNN with efficient filtering is enabled."""
        if self.is_aoss:
            return False
        self._os_version = await self._aget_opensearch_version()
        return self._version_supports_efficient_filtering(self._os_version)

    defindex_results(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
"""Store results in the index."""
        self._ensure_initialized()
        embeddings: List[List[float]] = []
        texts: List[str] = []
        metadatas: List[dict] = []
        ids: List[str] = []
        for node in nodes:
            ids.append(node.node_id)
            embeddings.append(node.get_embedding())
            texts.append(node.get_content(metadata_mode=MetadataMode.NONE))
            metadatas.append(node_to_metadata_dict(node, remove_text=True))

        return self._bulk_ingest_embeddings(
            self._os_client,
            self._index,
            embeddings,
            texts,
            metadatas=metadatas,
            ids=ids,
            vector_field=self._embedding_field,
            text_field=self._text_field,
            mapping=None,
            max_chunk_bytes=self._max_chunk_bytes,
            is_aoss=self.is_aoss,
        )

    async defaindex_results(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
"""Store results in the index."""
        await self._async_ensure_initialized()
        embeddings: List[List[float]] = []
        texts: List[str] = []
        metadatas: List[dict] = []
        ids: List[str] = []
        for node in nodes:
            ids.append(node.node_id)
            embeddings.append(node.get_embedding())
            texts.append(node.get_content(metadata_mode=MetadataMode.NONE))
            metadatas.append(node_to_metadata_dict(node, remove_text=True))

        return await self._abulk_ingest_embeddings(
            self._os_async_client,
            self._index,
            embeddings,
            texts,
            metadatas=metadatas,
            ids=ids,
            vector_field=self._embedding_field,
            text_field=self._text_field,
            mapping=None,
            max_chunk_bytes=self._max_chunk_bytes,
            is_aoss=self.is_aoss,
        )

    defdelete_by_doc_id(self, doc_id: str) -> None:
"""
        Deletes all OpenSearch documents corresponding to the given LlamaIndex `Document` ID.

        Args:
            doc_id (str): a LlamaIndex `Document` id

        """
        self._ensure_initialized()
        search_query = {
            "query": {"term": {"metadata.doc_id.keyword": {"value": doc_id}}}
        }
        self._os_client.delete_by_query(
            index=self._index, body=search_query, refresh=True
        )

    async defadelete_by_doc_id(self, doc_id: str) -> None:
"""
        Deletes all OpenSearch documents corresponding to the given LlamaIndex `Document` ID.

        Args:
            doc_id (str): a LlamaIndex `Document` id

        """
        await self._async_ensure_initialized()
        search_query = {
            "query": {"term": {"metadata.doc_id.keyword": {"value": doc_id}}}
        }
        await self._os_async_client.delete_by_query(
            index=self._index, body=search_query, refresh=True
        )

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Deletes nodes.

        Args:
            node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
            filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

        """
        self._ensure_initialized()
        if not node_ids and not filters:
            return

        query = {"query": {"bool": {"filter": []}}}
        if node_ids:
            query["query"]["bool"]["filter"].append({"terms": {"_id": node_ids or []}})

        if filters:
            query["query"]["bool"]["filter"].extend(self._parse_filters(filters))

        self._os_client.delete_by_query(index=self._index, body=query, refresh=True)

    async defadelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Deletes nodes.

        Args:
            node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
            filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

        """
        await self._async_ensure_initialized()
        if not node_ids and not filters:
            return

        query = {"query": {"bool": {"filter": []}}}
        if node_ids:
            query["query"]["bool"]["filter"].append({"terms": {"_id": node_ids or []}})

        if filters:
            query["query"]["bool"]["filter"].extend(self._parse_filters(filters))

        await self._os_async_client.delete_by_query(
            index=self._index, body=query, refresh=True
        )

    defclear(self) -> None:
"""Clears index."""
        self._ensure_initialized()
        query = {"query": {"bool": {"filter": []}}}
        self._os_client.delete_by_query(index=self._index, body=query, refresh=True)

    async defaclear(self) -> None:
"""Clears index."""
        await self._async_ensure_initialized()
        query = {"query": {"bool": {"filter": []}}}
        await self._os_async_client.delete_by_query(
            index=self._index, body=query, refresh=True
        )

    defclose(self) -> None:
"""
        Close the OpenSearch clients and release resources.

        Only closes clients that were created internally by this class.
        Clients passed in by the user are not closed.
        """
        if self._owns_os_client and self._os_client is not None:
            self._os_client.close()
        if self._owns_os_async_client and self._os_async_client is not None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                asyncio.run(self._os_async_client.close())
            else:
                loop.create_task(self._os_async_client.close())

    async defaclose(self) -> None:
"""
        Asynchronously close the OpenSearch clients and release resources.

        Only closes clients that were created internally by this class.
        Clients passed in by the user are not closed.
        """
        if self._owns_os_client and self._os_client is not None:
            self._os_client.close()
        if self._owns_os_async_client and self._os_async_client is not None:
            await self._os_async_client.close()

    def__del__(self) -> None:
"""Clean up OpenSearch clients during garbage collection."""
        try:
            self.close()
        except Exception as exc:
            logger.debug(
                "Failed to close OpenSearch clients during garbage collection, "
                "type=%s err='%s'",
                type(exc),
                exc,
            )

    defquery(
        self,
        query_mode: VectorStoreQueryMode,
        query_str: Optional[str],
        query_embedding: List[float],
        k: int,
        filters: Optional[MetadataFilters] = None,
    ) -> VectorStoreQueryResult:
        self._ensure_initialized()
        if query_mode == VectorStoreQueryMode.HYBRID:
            if query_str is None or self._search_pipeline is None:
                raise ValueError(INVALID_HYBRID_QUERY_ERROR)
            search_query = self._hybrid_search_query(
                self._text_field,
                query_str,
                self._embedding_field,
                query_embedding,
                k,
                filters=filters,
                excluded_source_fields=self._excluded_source_fields,
            )
            params = {
                "search_pipeline": self._search_pipeline,
            }
        elif query_mode == VectorStoreQueryMode.TEXT_SEARCH:
            search_query = self._lexical_search_query(
                self._text_field,
                query_str,
                k,
                filters=filters,
                excluded_source_fields=self._excluded_source_fields,
            )
            params = None
        else:
            search_query = self._knn_search_query(
                self._embedding_field,
                query_embedding,
                k,
                filters=filters,
                excluded_source_fields=self._excluded_source_fields,
            )
            params = None

        res = self._os_client.search(
            index=self._index, body=search_query, params=params
        )

        return self._to_query_result(res)

    async defaquery(
        self,
        query_mode: VectorStoreQueryMode,
        query_str: Optional[str],
        query_embedding: List[float],
        k: int,
        filters: Optional[MetadataFilters] = None,
    ) -> VectorStoreQueryResult:
        await self._async_ensure_initialized()
        if query_mode == VectorStoreQueryMode.HYBRID:
            if query_str is None or self._search_pipeline is None:
                raise ValueError(INVALID_HYBRID_QUERY_ERROR)
            search_query = self._hybrid_search_query(
                self._text_field,
                query_str,
                self._embedding_field,
                query_embedding,
                k,
                filters=filters,
                excluded_source_fields=self._excluded_source_fields,
            )
            params = {
                "search_pipeline": self._search_pipeline,
            }
        elif query_mode == VectorStoreQueryMode.TEXT_SEARCH:
            search_query = self._lexical_search_query(
                self._text_field,
                query_str,
                k,
                filters=filters,
                excluded_source_fields=self._excluded_source_fields,
            )
            params = None
        else:
            search_query = self._knn_search_query(
                self._embedding_field,
                query_embedding,
                k,
                filters=filters,
                excluded_source_fields=self._excluded_source_fields,
            )
            params = None

        res = await self._os_async_client.search(
            index=self._index, body=search_query, params=params
        )

        return self._to_query_result(res)

    def_to_query_result(self, res) -> VectorStoreQueryResult:
        nodes = []
        ids = []
        scores = []
        for hit in res["hits"]["hits"]:
            source = hit["_source"]
            node_id = hit["_id"]
            text = source[self._text_field]
            metadata = source.get("metadata", None)

            try:
                node = metadata_dict_to_node(metadata)
                node.text = text
            except Exception:
                # TODO: Legacy support for old nodes
                node_info = source.get("node_info")
                relationships = source.get("relationships") or {}
                start_char_idx = None
                end_char_idx = None
                if isinstance(node_info, dict):
                    start_char_idx = node_info.get("start", None)
                    end_char_idx = node_info.get("end", None)

                node = TextNode(
                    text=text,
                    metadata=metadata,
                    id_=node_id,
                    start_char_idx=start_char_idx,
                    end_char_idx=end_char_idx,
                    relationships=relationships,
                )
            ids.append(node_id)
            nodes.append(node)
            scores.append(hit["_score"])

        return VectorStoreQueryResult(nodes=nodes, ids=ids, similarities=scores)

```
 |  
| --- | --- |  
###  index_results [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorClient.index_results "Permanent link")

```
index_results(
    nodes: [], **kwargs: 
) -> []

```

Store results in the index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
```
 | 
```
defindex_results(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
"""Store results in the index."""
    self._ensure_initialized()
    embeddings: List[List[float]] = []
    texts: List[str] = []
    metadatas: List[dict] = []
    ids: List[str] = []
    for node in nodes:
        ids.append(node.node_id)
        embeddings.append(node.get_embedding())
        texts.append(node.get_content(metadata_mode=MetadataMode.NONE))
        metadatas.append(node_to_metadata_dict(node, remove_text=True))

    return self._bulk_ingest_embeddings(
        self._os_client,
        self._index,
        embeddings,
        texts,
        metadatas=metadatas,
        ids=ids,
        vector_field=self._embedding_field,
        text_field=self._text_field,
        mapping=None,
        max_chunk_bytes=self._max_chunk_bytes,
        is_aoss=self.is_aoss,
    )

```
 |  
| --- | --- |  
###  aindex_results [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorClient.aindex_results "Permanent link")

```
aindex_results(
    nodes: [], **kwargs: 
) -> []

```

Store results in the index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
```
 | 
```
async defaindex_results(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
"""Store results in the index."""
    await self._async_ensure_initialized()
    embeddings: List[List[float]] = []
    texts: List[str] = []
    metadatas: List[dict] = []
    ids: List[str] = []
    for node in nodes:
        ids.append(node.node_id)
        embeddings.append(node.get_embedding())
        texts.append(node.get_content(metadata_mode=MetadataMode.NONE))
        metadatas.append(node_to_metadata_dict(node, remove_text=True))

    return await self._abulk_ingest_embeddings(
        self._os_async_client,
        self._index,
        embeddings,
        texts,
        metadatas=metadatas,
        ids=ids,
        vector_field=self._embedding_field,
        text_field=self._text_field,
        mapping=None,
        max_chunk_bytes=self._max_chunk_bytes,
        is_aoss=self.is_aoss,
    )

```
 |  
| --- | --- |  
###  delete_by_doc_id [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorClient.delete_by_doc_id "Permanent link")

```
delete_by_doc_id(doc_id: ) -> None

```

Deletes all OpenSearch documents corresponding to the given LlamaIndex `Document` ID.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `doc_id`  |  a LlamaIndex `Document` id  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
```
 | 
```
defdelete_by_doc_id(self, doc_id: str) -> None:
"""
    Deletes all OpenSearch documents corresponding to the given LlamaIndex `Document` ID.

    Args:
        doc_id (str): a LlamaIndex `Document` id

    """
    self._ensure_initialized()
    search_query = {
        "query": {"term": {"metadata.doc_id.keyword": {"value": doc_id}}}
    }
    self._os_client.delete_by_query(
        index=self._index, body=search_query, refresh=True
    )

```
 |  
| --- | --- |  
###  adelete_by_doc_id [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorClient.adelete_by_doc_id "Permanent link")

```
adelete_by_doc_id(doc_id: ) -> None

```

Deletes all OpenSearch documents corresponding to the given LlamaIndex `Document` ID.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `doc_id`  |  a LlamaIndex `Document` id  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
```
 | 
```
async defadelete_by_doc_id(self, doc_id: str) -> None:
"""
    Deletes all OpenSearch documents corresponding to the given LlamaIndex `Document` ID.

    Args:
        doc_id (str): a LlamaIndex `Document` id

    """
    await self._async_ensure_initialized()
    search_query = {
        "query": {"term": {"metadata.doc_id.keyword": {"value": doc_id}}}
    }
    await self._os_async_client.delete_by_query(
        index=self._index, body=search_query, refresh=True
    )

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorClient.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Deletes nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  IDs of nodes to delete. Defaults to None.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters. Defaults to None.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Deletes nodes.

    Args:
        node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
        filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

    """
    self._ensure_initialized()
    if not node_ids and not filters:
        return

    query = {"query": {"bool": {"filter": []}}}
    if node_ids:
        query["query"]["bool"]["filter"].append({"terms": {"_id": node_ids or []}})

    if filters:
        query["query"]["bool"]["filter"].extend(self._parse_filters(filters))

    self._os_client.delete_by_query(index=self._index, body=query, refresh=True)

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorClient.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Deletes nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  IDs of nodes to delete. Defaults to None.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters. Defaults to None.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Deletes nodes.

    Args:
        node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
        filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

    """
    await self._async_ensure_initialized()
    if not node_ids and not filters:
        return

    query = {"query": {"bool": {"filter": []}}}
    if node_ids:
        query["query"]["bool"]["filter"].append({"terms": {"_id": node_ids or []}})

    if filters:
        query["query"]["bool"]["filter"].extend(self._parse_filters(filters))

    await self._os_async_client.delete_by_query(
        index=self._index, body=query, refresh=True
    )

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorClient.clear "Permanent link")

```
clear() -> None

```

Clears index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
861
862
863
864
865
```
 | 
```
defclear(self) -> None:
"""Clears index."""
    self._ensure_initialized()
    query = {"query": {"bool": {"filter": []}}}
    self._os_client.delete_by_query(index=self._index, body=query, refresh=True)

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorClient.aclear "Permanent link")

```
aclear() -> None

```

Clears index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
867
868
869
870
871
872
873
```
 | 
```
async defaclear(self) -> None:
"""Clears index."""
    await self._async_ensure_initialized()
    query = {"query": {"bool": {"filter": []}}}
    await self._os_async_client.delete_by_query(
        index=self._index, body=query, refresh=True
    )

```
 |  
| --- | --- |  
###  close [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorClient.close "Permanent link")

```
close() -> None

```

Close the OpenSearch clients and release resources.
Only closes clients that were created internally by this class. Clients passed in by the user are not closed.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
```
 | 
```
defclose(self) -> None:
"""
    Close the OpenSearch clients and release resources.

    Only closes clients that were created internally by this class.
    Clients passed in by the user are not closed.
    """
    if self._owns_os_client and self._os_client is not None:
        self._os_client.close()
    if self._owns_os_async_client and self._os_async_client is not None:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(self._os_async_client.close())
        else:
            loop.create_task(self._os_async_client.close())

```
 |  
| --- | --- |  
###  aclose [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/#llama_index.vector_stores.opensearch.OpensearchVectorClient.aclose "Permanent link")

```
aclose() -> None

```

Asynchronously close the OpenSearch clients and release resources.
Only closes clients that were created internally by this class. Clients passed in by the user are not closed.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-opensearch/llama_index/vector_stores/opensearch/base.py`  
| 
```
892
893
894
895
896
897
898
899
900
901
902
```
 | 
```
async defaclose(self) -> None:
"""
    Asynchronously close the OpenSearch clients and release resources.

    Only closes clients that were created internally by this class.
    Clients passed in by the user are not closed.
    """
    if self._owns_os_client and self._os_client is not None:
        self._os_client.close()
    if self._owns_os_async_client and self._os_async_client is not None:
        await self._os_async_client.close()

```
 |  
| --- | --- |  
options: members: - OpensearchVectorStore
