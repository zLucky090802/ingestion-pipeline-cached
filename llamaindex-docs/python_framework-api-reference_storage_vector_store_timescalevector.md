# Timescalevector
##  TimescaleVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/timescalevector/#llama_index.vector_stores.timescalevector.TimescaleVectorStore "Permanent link")
Bases: 
Timescale vector store.
Examples:
`pip install llama-index-vector-stores-timescalevector`

```
fromllama_index.vector_stores.timescalevectorimport TimescaleVectorStore

# Set up the Timescale service URL
TIMESCALE_SERVICE_URL = "postgres://tsdbadmin:<password>@<id>.tsdb.cloud.timescale.com:<port>/tsdb?sslmode=require"

# Create a TimescaleVectorStore instance
vector_store = TimescaleVectorStore.from_params(
    service_url=TIMESCALE_SERVICE_URL,
    table_name="your_table_name_here",
    num_dimensions=1536,
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-timescalevector/llama_index/vector_stores/timescalevector/base.py`  
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
```
 | 
```
classTimescaleVectorStore(BasePydanticVectorStore):
"""
    Timescale vector store.

    Examples:
        `pip install llama-index-vector-stores-timescalevector`

        ```python
        from llama_index.vector_stores.timescalevector import TimescaleVectorStore

        # Set up the Timescale service URL
        TIMESCALE_SERVICE_URL = "postgres://tsdbadmin:<password>@<id>.tsdb.cloud.timescale.com:<port>/tsdb?sslmode=require"

        # Create a TimescaleVectorStore instance
        vector_store = TimescaleVectorStore.from_params(
            service_url=TIMESCALE_SERVICE_URL,
            table_name="your_table_name_here",
            num_dimensions=1536,

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    service_url: str
    table_name: str
    num_dimensions: int
    time_partition_interval: Optional[timedelta]

    _sync_client: client.Sync = PrivateAttr()
    _async_client: client.Async = PrivateAttr()

    def__init__(
        self,
        service_url: str,
        table_name: str,
        num_dimensions: int = DEFAULT_EMBEDDING_DIM,
        time_partition_interval: Optional[timedelta] = None,
    ) -> None:
        table_name = table_name.lower()

        super().__init__(
            service_url=service_url,
            table_name=table_name,
            num_dimensions=num_dimensions,
            time_partition_interval=time_partition_interval,
        )

        self._create_clients()
        self._create_tables()

    @classmethod
    defclass_name(cls) -> str:
        return "TimescaleVectorStore"

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._sync_client

    async defclose(self) -> None:
        self._sync_client.close()
        await self._async_client.close()

    @classmethod
    deffrom_params(
        cls,
        service_url: str,
        table_name: str,
        num_dimensions: int = DEFAULT_EMBEDDING_DIM,
        time_partition_interval: Optional[timedelta] = None,
    ) -> "TimescaleVectorStore":
        return cls(
            service_url=service_url,
            table_name=table_name,
            num_dimensions=num_dimensions,
            time_partition_interval=time_partition_interval,
        )

    def_create_clients(self) -> None:
        # in the normal case doesn't restrict the id type to even uuid.
        # Allow arbitrary text
        id_type = "TEXT"
        if self.time_partition_interval is not None:
            # for time partitioned tables, the id type must be UUID v1
            id_type = "UUID"

        self._sync_client = client.Sync(
            self.service_url,
            self.table_name,
            self.num_dimensions,
            id_type=id_type,
            time_partition_interval=self.time_partition_interval,
        )
        self._async_client = client.Async(
            self.service_url,
            self.table_name,
            self.num_dimensions,
            id_type=id_type,
            time_partition_interval=self.time_partition_interval,
        )

    def_create_tables(self) -> None:
        self._sync_client.create_tables()

    def_node_to_row(self, node: BaseNode) -> Any:
        metadata = node_to_metadata_dict(
            node,
            remove_text=True,
            flat_metadata=self.flat_metadata,
        )
        # reuse the node id in the common  case
        id = node.node_id
        if self.time_partition_interval is not None:
            # for time partitioned tables, the id must be a UUID v1,
            # so generate one if it's not already set
            try:
                # Attempt to parse the UUID from the string
                parsed_uuid = uuid.UUID(id)
                if parsed_uuid.version != 1:
                    id = str(uuid.uuid1())
            except ValueError:
                id = str(uuid.uuid1())
        return [
            id,
            metadata,
            node.get_content(metadata_mode=MetadataMode.NONE),
            node.embedding,
        ]

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
        rows_to_insert = [self._node_to_row(node) for node in nodes]
        ids = [result[0] for result in rows_to_insert]
        self._sync_client.upsert(rows_to_insert)
        return ids

    async defasync_add(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
        rows_to_insert = [self._node_to_row(node) for node in nodes]
        ids = [result.node_id for result in nodes]
        await self._async_client.upsert(rows_to_insert)
        return ids

    def_filter_to_dict(
        self, metadata_filters: Optional[MetadataFilters]
    ) -> Optional[Dict[str, str]]:
        if metadata_filters is None or len(metadata_filters.legacy_filters()) <= 0:
            return None

        res = {}
        for filter in metadata_filters.legacy_filters():
            res[filter.key] = filter.value

        return res

    def_db_rows_to_query_result(self, rows: List) -> VectorStoreQueryResult:
        nodes = []
        similarities = []
        ids = []
        for row in rows:
            try:
                node = metadata_dict_to_node(row[client.SEARCH_RESULT_METADATA_IDX])
                node.set_content(str(row[client.SEARCH_RESULT_CONTENTS_IDX]))
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                node = TextNode(
                    id_=row[client.SEARCH_RESULT_ID_IDX],
                    text=row[client.SEARCH_RESULT_CONTENTS_IDX],
                    metadata=row[client.SEARCH_RESULT_METADATA_IDX],
                )
            similarities.append(row[client.SEARCH_RESULT_DISTANCE_IDX])
            ids.append(row[client.SEARCH_RESULT_ID_IDX])
            nodes.append(node)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities,
            ids=ids,
        )

    defdate_to_range_filter(self, **kwargs: Any) -> Any:
        constructor_args = {
            key: kwargs[key]
            for key in [
                "start_date",
                "end_date",
                "time_delta",
                "start_inclusive",
                "end_inclusive",
            ]
            if key in kwargs
        }
        if not constructor_args or len(constructor_args) == 0:
            return None

        return client.UUIDTimeRange(**constructor_args)

    def_query_with_score(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        filter = self._filter_to_dict(metadata_filters)
        res = self._sync_client.search(
            embedding,
            limit,
            filter,
            uuid_time_filter=self.date_to_range_filter(**kwargs),
        )
        return self._db_rows_to_query_result(res)

    async def_aquery_with_score(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        filter = self._filter_to_dict(metadata_filters)
        res = await self._async_client.search(
            embedding,
            limit,
            filter,
            uuid_time_filter=self.date_to_range_filter(**kwargs),
        )
        return self._db_rows_to_query_result(res)

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        return self._query_with_score(
            query.query_embedding, query.similarity_top_k, query.filters, **kwargs
        )

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
        return await self._aquery_with_score(
            query.query_embedding,
            query.similarity_top_k,
            query.filters,
            **kwargs,
        )

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        filter: Dict[str, str] = {"doc_id": ref_doc_id}
        self._sync_client.delete_by_metadata(filter)

    DEFAULT_INDEX_TYPE: ClassVar = IndexType.TIMESCALE_VECTOR

    defcreate_index(
        self, index_type: IndexType = DEFAULT_INDEX_TYPE, **kwargs: Any
    ) -> None:
        if index_type == IndexType.PGVECTOR_IVFFLAT:
            self._sync_client.create_embedding_index(client.IvfflatIndex(**kwargs))

        if index_type == IndexType.PGVECTOR_HNSW:
            self._sync_client.create_embedding_index(client.HNSWIndex(**kwargs))

        if index_type == IndexType.TIMESCALE_VECTOR:
            self._sync_client.create_embedding_index(
                client.TimescaleVectorIndex(**kwargs)
            )

    defdrop_index(self) -> None:
        self._sync_client.drop_embedding_index()

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/timescalevector/#llama_index.vector_stores.timescalevector.TimescaleVectorStore.client "Permanent link")

```
client: 

```

Get client.
options: members: - TimescaleVectorStore
