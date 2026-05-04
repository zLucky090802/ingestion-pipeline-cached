# Wordlift
##  WordliftVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/wordlift/#llama_index.vector_stores.wordlift.WordliftVectorStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-wordlift/llama_index/vector_stores/wordlift/base.py`  
| 
```
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
```
 | 
```
classWordliftVectorStore(BasePydanticVectorStore):
    stores_text: bool = True

    _account: Optional[AccountInfo] = PrivateAttr(default=None)
    _configuration: Configuration = PrivateAttr()
    _fields: Optional[List[str]] = PrivateAttr()

    def__init__(
        self,
        key: Optional[str] = None,
        configuration: Optional[Configuration] = None,
        fields: Optional[List[str]] = None,
    ):
        super().__init__(use_async=True)

        try:
            nest_asyncio.apply()
        except ValueError:
            # We may not be in asyncio
            pass

        if configuration is None:
            self._configuration = _make_configuration(key=key)
        else:
            self._configuration = configuration

        if fields is None:
            self._fields = ["schema:url", "schema:name"]
        else:
            self._fields = fields

    @property
    defaccount(self) -> AccountInfo:
        if self._account is None:
            self._account = asyncio.get_event_loop().run_until_complete(
                self._get_account()
            )

        return self._account

    async def_get_account(self):
"""
        Get the account data for the provided key.

        :return:
        """
        async with wordlift_client.ApiClient(self._configuration) as api_client:
            api_instance = wordlift_client.AccountApi(api_client)

            try:
                return await api_instance.get_me()
            except ApiException as e:
                raise RuntimeError(
                    "Failed to get account info, check the provided key"
                ) frome

    @property
    defclient(self) -> Any:
        return self.account

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
        return asyncio.get_event_loop().run_until_complete(
            self.async_add(nodes, **add_kwargs)
        )

    async defasync_add(
        self,
        nodes: List[BaseNode],
        **kwargs: Any,
    ) -> List[str]:
        # Empty nodes, return empty list
        if not nodes:
            return []

        log.debug(f"{len(nodes)} node(s) received\n")

        requests = []
        for node in nodes:
            node_dict = node.dict()
            # metadata: Dict[str, Any] = node_dict.get("metadata", {})
            metadata = _make_metadata_as_node_request_metadata_value(
                node_dict.get("metadata", {})
            )

            # Get or generate an ID
            entity_id = metadata.get("entity_id", None)
            if entity_id is None:
                entity_id = _generate_id(self.account, node.id_)

            entry = NodeRequest(
                entity_id=entity_id,
                node_id=node.node_id,
                embeddings=node.get_embedding(),
                text=node.get_content(metadata_mode=MetadataMode.NONE) or "",
                metadata=metadata,
            )
            requests.append(entry)

        async with wordlift_client.ApiClient(self._configuration) as api_client:
            api_instance = wordlift_client.VectorSearchNodesApi(api_client)

            try:
                await api_instance.update_nodes_collection(node_request=requests)
            except ApiException as e:
                raise RuntimeError("Error creating entities") frome

        return [node.node_id for node in nodes]

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        return asyncio.get_event_loop().run_until_complete(
            self.adelete(ref_doc_id, **delete_kwargs)
        )

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        await self.adelete_nodes([ref_doc_id], **delete_kwargs)

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
        return asyncio.get_event_loop().run_until_complete(
            self.adelete_nodes(node_ids, filters, **delete_kwargs)
        )

    async defadelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
        # Bail out if the list is not provided.
        if node_ids is None:
            return

        # Create the IDs.
        ids = []
        for node_id in node_ids:
            ids.append(_generate_id(self.account, node_id))

        async with wordlift_client.ApiClient(self._configuration) as api_client:
            api_instance = wordlift_client.EntitiesApi(api_client)

            try:
                await api_instance.delete_entities(id=ids)
            except ApiException as e:
                raise RuntimeError("Error deleting entities") frome

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        return asyncio.get_event_loop().run_until_complete(self.aquery(query, **kwargs))

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
        filters = MetadataFiltersToFilters.metadata_filters_to_filters(
            query.filters if query.filters else []
        )
        if query.query_str:
            request = VectorSearchQueryRequest(
                query_string=query.query_str,
                similarity_top_k=query.similarity_top_k,
                fields=self._fields,
                filters=filters,
            )
        else:
            request = VectorSearchQueryRequest(
                query_embedding=query.query_embedding,
                similarity_top_k=query.similarity_top_k,
                fields=self._fields,
                filters=filters,
            )

        async with wordlift_client.ApiClient(self._configuration) as api_client:
            api_instance = wordlift_client.VectorSearchQueriesApi(api_client)

            try:
                page = await api_instance.create_query(
                    vector_search_query_request=request,
                )
            except ApiException as e:
                log.error(
                    f"Error querying for entities with the following request: {json.dumps(api_client.sanitize_for_serialization(request))}",
                    exc_info=True,
                )

        nodes: List[TextNode] = []
        similarities: List[float] = []
        ids: List[str] = []

        for item in page.items:
            metadata = item.metadata if item.metadata else {}
            fields = item.fields if item.fields else {}
            metadata = {**metadata, **fields}

            nodes.append(
                TextNode(
                    text=item.text if item.text else "",
                    id_=item.node_id if item.node_id else "",
                    embedding=(item.embeddings if "embeddings" in item else None),
                    metadata=metadata,
                )
            )
            similarities.append(item.score)
            ids.append(item.node_id)
        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
options: members: - WordliftVectorStore
