# Dashscope
##  DashScopeCloudIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/dashscope/#llama_index.indices.managed.dashscope.DashScopeCloudIndex "Permanent link")
Bases: `BaseManagedIndex`
DashScope Cloud Platform Index.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-dashscope/llama_index/indices/managed/dashscope/base.py`  
| 
```
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
```
 | 
```
classDashScopeCloudIndex(BaseManagedIndex):
"""DashScope Cloud Platform Index."""

    def__init__(
        self,
        name: str,
        nodes: Optional[List[BaseNode]] = None,
        transformations: Optional[List[TransformComponent]] = None,
        timeout: int = 60,
        workspace_id: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = DASHSCOPE_DEFAULT_BASE_URL,
        show_progress: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize the Platform Index."""
        self.name = name
        self.transformations = transformations or []

        if nodes is not None:
            raise ValueError(
                "DashScopeCloudIndex does not support nodes on initialization"
            )

        self.workspace_id = workspace_id or os.environ.get("DASHSCOPE_WORKSPACE_ID")
        self._api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
        self._base_url = os.environ.get("DASHSCOPE_BASE_URL", None) or base_url
        self._headers = {
            "Content-Type": "application/json",
            "Accept-Encoding": "utf-8",
            "X-DashScope-WorkSpace": self.workspace_id,
            "Authorization": "Bearer " + self._api_key,
            "X-DashScope-OpenAPISource": "CloudSDK",
        }
        self._timeout = timeout
        self._show_progress = show_progress
        self._service_context = None
        self._callback_manager = callback_manager or Settings.callback_manager

    @classmethod
    deffrom_documents(  # type: ignore
        cls: Type["DashScopeCloudIndex"],
        documents: List[Document],
        name: str,
        transformations: Optional[List[TransformComponent]] = None,
        workspace_id: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 60,
        verbose: bool = True,
        **kwargs: Any,
    ) -> "DashScopeCloudIndex":
"""Build a DashScope index from a sequence of documents."""
        pipeline_create = get_pipeline_create(
            name, transformations or default_transformations(), documents
        )

        workspace_id = workspace_id or os.environ.get("DASHSCOPE_WORKSPACE_ID")
        api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
        base_url = (
            base_url
            or os.environ.get("DASHSCOPE_BASE_URL", None)
            or DASHSCOPE_DEFAULT_BASE_URL
        )
        headers = {
            "Content-Type": "application/json",
            "Accept-Encoding": "utf-8",
            "X-DashScope-WorkSpace": workspace_id,
            "Authorization": "Bearer " + api_key,
            "X-DashScope-OpenAPISource": "CloudSDK",
        }

        response = requests.put(
            base_url + UPSERT_PIPELINE_ENDPOINT,
            data=json.dumps(pipeline_create),
            headers=headers,
        )
        response_text = response.json()
        pipeline_id = response_text.get("id", None)

        if response_text.get("code", "") != Status.SUCCESS.value or pipeline_id is None:
            raise ValueError(
                f"Failed to create index: {response_text.get('message','')}\n{response_text}"
            )
        if verbose:
            print(f"Starting creating index {name}, pipeline_id: {pipeline_id}")

        response = requests.post(
            base_url + START_PIPELINE_ENDPOINT.format(pipeline_id=pipeline_id),
            headers=headers,
        )
        response_text = response.json()
        ingestion_id = response_text.get("ingestionId", None)

        if (
            response_text.get("code", "") != Status.SUCCESS.value
            or ingestion_id is None
        ):
            raise ValueError(
                f"Failed to start ingestion: {response_text.get('message','')}\n{response_text}"
            )
        if verbose:
            print(f"Starting ingestion for index {name}, ingestion_id: {ingestion_id}")

        ingestion_status, failed_docs = run_ingestion(
            base_url
            + CHECK_INGESTION_ENDPOINT.format(
                pipeline_id=pipeline_id, ingestion_id=ingestion_id
            ),
            headers,
            verbose,
        )

        if verbose:
            print(f"ingestion_status {ingestion_status}")
            print(f"failed_docs: {failed_docs}")

        if ingestion_status == "FAILED":
            print("Index {name} created failed!")
            return None

        if verbose:
            print(f"Index {name} created successfully!")

        return cls(
            name,
            transformations=transformations,
            workspace_id=workspace_id,
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            **kwargs,
        )

    defas_retriever(self, **kwargs: Any) -> BaseRetriever:
"""Return a Retriever for this managed index."""
        fromllama_index.indices.managed.dashscope.retrieverimport (
            DashScopeCloudRetriever,
        )

        return DashScopeCloudRetriever(
            self.name,
            **kwargs,
        )

    defas_query_engine(self, **kwargs: Any) -> BaseQueryEngine:
        fromllama_index.core.query_engine.retriever_query_engineimport (
            RetrieverQueryEngine,
        )

        kwargs["retriever"] = self.as_retriever(**kwargs)
        return RetrieverQueryEngine.from_args(**kwargs)

    def_insert(
        self,
        documents: List[Document],
        transformations: Optional[List[TransformComponent]] = None,
        verbose: bool = True,
        **insert_kwargs: Any,
    ) -> None:
"""Insert a set of documents (each a node)."""
        pipeline_id = get_pipeline_id(
            self._base_url + PIPELINE_SIMPLE_ENDPOINT,
            self._headers,
            {"pipeline_name": self.name},
        )
        doc_insert = get_doc_insert(
            transformations or default_transformations(),
            documents,
        )
        response = requests.put(
            self._base_url + INSERT_DOC_ENDPOINT.format(pipeline_id=pipeline_id),
            data=json.dumps(doc_insert),
            headers=self._headers,
        )
        response_text = response.json()
        ingestion_id = response_text.get("ingestionId", None)
        if (
            response_text.get("code", "") != Status.SUCCESS.value
            or ingestion_id is None
        ):
            raise ValueError(
                f"Failed to insert documents: {response_text.get('message','')}\n{response_text}"
            )

        ingestion_status, failed_docs = run_ingestion(
            self._base_url
            + CHECK_INGESTION_ENDPOINT.format(
                pipeline_id=pipeline_id, ingestion_id=ingestion_id
            ),
            self._headers,
            verbose,
        )

        if verbose:
            print(f"ingestion_status {ingestion_status}")
            print(f"failed_docs: {failed_docs}")

    defdelete_ref_doc(
        self,
        ref_doc_ids: Union[str, List[str]],
        verbose: bool = True,
        **delete_kwargs: Any,
    ) -> None:
"""Delete documents in index."""
        if isinstance(ref_doc_ids, str):
            ref_doc_ids = [ref_doc_ids]
        pipeline_id = get_pipeline_id(
            self._base_url + PIPELINE_SIMPLE_ENDPOINT,
            self._headers,
            {"pipeline_name": self.name},
        )
        doc_delete = get_doc_delete(ref_doc_ids)
        response = requests.post(
            self._base_url + DELETE_DOC_ENDPOINT.format(pipeline_id=pipeline_id),
            json=doc_delete,
            headers=self._headers,
        )
        response_text = response.json()
        if response_text.get("code", "") != Status.SUCCESS.value:
            raise ValueError(
                f"Failed to delete documents: {response_text.get('message','')}\n{response_text}"
            )
        if verbose:
            print(f"Delete documents {ref_doc_ids} successfully!")

    defupdate_ref_doc(self, document: Document, **update_kwargs: Any) -> None:
"""Update a document and it's corresponding nodes."""
        raise NotImplementedError("update_ref_doc not implemented.")

```
 |  
| --- | --- |  
###  from_documents `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/dashscope/#llama_index.indices.managed.dashscope.DashScopeCloudIndex.from_documents "Permanent link")

```
from_documents(
    documents: [],
    name: ,
    transformations: Optional[
        []
    ] = None,
    workspace_id: Optional[] = None,
    api_key: Optional[] = None,
    base_url: Optional[] = None,
    timeout:  = 60,
    verbose:  = True,
    **kwargs: 
) -> 

```

Build a DashScope index from a sequence of documents.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-dashscope/llama_index/indices/managed/dashscope/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_documents(  # type: ignore
    cls: Type["DashScopeCloudIndex"],
    documents: List[Document],
    name: str,
    transformations: Optional[List[TransformComponent]] = None,
    workspace_id: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: int = 60,
    verbose: bool = True,
    **kwargs: Any,
) -> "DashScopeCloudIndex":
"""Build a DashScope index from a sequence of documents."""
    pipeline_create = get_pipeline_create(
        name, transformations or default_transformations(), documents
    )

    workspace_id = workspace_id or os.environ.get("DASHSCOPE_WORKSPACE_ID")
    api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
    base_url = (
        base_url
        or os.environ.get("DASHSCOPE_BASE_URL", None)
        or DASHSCOPE_DEFAULT_BASE_URL
    )
    headers = {
        "Content-Type": "application/json",
        "Accept-Encoding": "utf-8",
        "X-DashScope-WorkSpace": workspace_id,
        "Authorization": "Bearer " + api_key,
        "X-DashScope-OpenAPISource": "CloudSDK",
    }

    response = requests.put(
        base_url + UPSERT_PIPELINE_ENDPOINT,
        data=json.dumps(pipeline_create),
        headers=headers,
    )
    response_text = response.json()
    pipeline_id = response_text.get("id", None)

    if response_text.get("code", "") != Status.SUCCESS.value or pipeline_id is None:
        raise ValueError(
            f"Failed to create index: {response_text.get('message','')}\n{response_text}"
        )
    if verbose:
        print(f"Starting creating index {name}, pipeline_id: {pipeline_id}")

    response = requests.post(
        base_url + START_PIPELINE_ENDPOINT.format(pipeline_id=pipeline_id),
        headers=headers,
    )
    response_text = response.json()
    ingestion_id = response_text.get("ingestionId", None)

    if (
        response_text.get("code", "") != Status.SUCCESS.value
        or ingestion_id is None
    ):
        raise ValueError(
            f"Failed to start ingestion: {response_text.get('message','')}\n{response_text}"
        )
    if verbose:
        print(f"Starting ingestion for index {name}, ingestion_id: {ingestion_id}")

    ingestion_status, failed_docs = run_ingestion(
        base_url
        + CHECK_INGESTION_ENDPOINT.format(
            pipeline_id=pipeline_id, ingestion_id=ingestion_id
        ),
        headers,
        verbose,
    )

    if verbose:
        print(f"ingestion_status {ingestion_status}")
        print(f"failed_docs: {failed_docs}")

    if ingestion_status == "FAILED":
        print("Index {name} created failed!")
        return None

    if verbose:
        print(f"Index {name} created successfully!")

    return cls(
        name,
        transformations=transformations,
        workspace_id=workspace_id,
        api_key=api_key,
        base_url=base_url,
        timeout=timeout,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  as_retriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/dashscope/#llama_index.indices.managed.dashscope.DashScopeCloudIndex.as_retriever "Permanent link")

```
as_retriever(**kwargs: ) -> 

```

Return a Retriever for this managed index.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-dashscope/llama_index/indices/managed/dashscope/base.py`  
| 
```
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
```
 | 
```
defas_retriever(self, **kwargs: Any) -> BaseRetriever:
"""Return a Retriever for this managed index."""
    fromllama_index.indices.managed.dashscope.retrieverimport (
        DashScopeCloudRetriever,
    )

    return DashScopeCloudRetriever(
        self.name,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  delete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/dashscope/#llama_index.indices.managed.dashscope.DashScopeCloudIndex.delete_ref_doc "Permanent link")

```
delete_ref_doc(
    ref_doc_ids: Union[, []],
    verbose:  = True,
    **delete_kwargs: 
) -> None

```

Delete documents in index.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-dashscope/llama_index/indices/managed/dashscope/base.py`  
| 
```
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
```
 | 
```
defdelete_ref_doc(
    self,
    ref_doc_ids: Union[str, List[str]],
    verbose: bool = True,
    **delete_kwargs: Any,
) -> None:
"""Delete documents in index."""
    if isinstance(ref_doc_ids, str):
        ref_doc_ids = [ref_doc_ids]
    pipeline_id = get_pipeline_id(
        self._base_url + PIPELINE_SIMPLE_ENDPOINT,
        self._headers,
        {"pipeline_name": self.name},
    )
    doc_delete = get_doc_delete(ref_doc_ids)
    response = requests.post(
        self._base_url + DELETE_DOC_ENDPOINT.format(pipeline_id=pipeline_id),
        json=doc_delete,
        headers=self._headers,
    )
    response_text = response.json()
    if response_text.get("code", "") != Status.SUCCESS.value:
        raise ValueError(
            f"Failed to delete documents: {response_text.get('message','')}\n{response_text}"
        )
    if verbose:
        print(f"Delete documents {ref_doc_ids} successfully!")

```
 |  
| --- | --- |  
###  update_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/dashscope/#llama_index.indices.managed.dashscope.DashScopeCloudIndex.update_ref_doc "Permanent link")

```
update_ref_doc(
    document: , **update_kwargs: 
) -> None

```

Update a document and it's corresponding nodes.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-dashscope/llama_index/indices/managed/dashscope/base.py`  
| 
```
280
281
282
```
 | 
```
defupdate_ref_doc(self, document: Document, **update_kwargs: Any) -> None:
"""Update a document and it's corresponding nodes."""
    raise NotImplementedError("update_ref_doc not implemented.")

```
 |  
| --- | --- |  
##  DashScopeCloudRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/dashscope/#llama_index.indices.managed.dashscope.DashScopeCloudRetriever "Permanent link")
Bases: 
Initialize the DashScopeCloud Retriever.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-dashscope/llama_index/indices/managed/dashscope/retriever.py`  
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
```
 | 
```
classDashScopeCloudRetriever(BaseRetriever):
"""Initialize the DashScopeCloud Retriever."""

    def__init__(
        self,
        index_name: str,
        api_key: Optional[str] = None,
        workspace_id: Optional[str] = None,
        dense_similarity_top_k: Optional[int] = 100,
        sparse_similarity_top_k: Optional[int] = 100,
        enable_rewrite: Optional[bool] = False,
        rewrite_model_name: Optional[str] = "conv-rewrite-qwen-1.8b",
        enable_reranking: Optional[bool] = True,
        rerank_model_name: Optional[str] = "gte-rerank-hybrid",
        rerank_min_score: Optional[float] = 0.0,
        rerank_top_n: Optional[int] = 5,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs,
    ) -> None:
        self.index_name = index_name
        self.workspace_id = workspace_id or os.environ.get("DASHSCOPE_WORKSPACE_ID")
        self._api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
        self.dense_similarity_top_k = dense_similarity_top_k
        self.sparse_similarity_top_k = sparse_similarity_top_k
        self.enable_rewrite = enable_rewrite
        self.rewrite_model_name = rewrite_model_name
        self.enable_reranking = enable_reranking
        self.rerank_model_name = rerank_model_name
        self.rerank_min_score = rerank_min_score
        self.rerank_top_n = rerank_top_n

        self.headers = {
            "Content-Type": "application/json",
            "Accept-Encoding": "utf-8",
            "X-DashScope-WorkSpace": self.workspace_id,
            "Authorization": self._api_key,
            "X-DashScope-OpenAPISource": "CloudSDK",
        }

        base_url = (
            os.environ.get("DASHSCOPE_BASE_URL", None) or DASHSCOPE_DEFAULT_BASE_URL
        )
        self.pipeline_id = utils.get_pipeline_id(
            base_url + PIPELINE_SIMPLE_ENDPOINT,
            self.headers,
            {"pipeline_name": self.index_name},
        )

        self.base_url = base_url + RETRIEVE_PIPELINE_ENDPOINT.format(
            pipeline_id=self.pipeline_id
        )
        super().__init__(callback_manager)

    @dispatcher.span
    defretrieve(
        self, str_or_query_bundle: QueryType, query_history: List[Dict] = None
    ) -> List[NodeWithScore]:
"""
        Retrieve nodes given query.

        Args:
            str_or_query_bundle (QueryType): Either a query string or
                a QueryBundle object.

        """
        dispatch_event = dispatcher.get_dispatch_event()

        self._check_callback_manager()
        dispatch_event(
            RetrievalStartEvent(
                str_or_query_bundle=str_or_query_bundle,
            )
        )
        if isinstance(str_or_query_bundle, str):
            query_bundle = QueryBundle(str_or_query_bundle)
        else:
            query_bundle = str_or_query_bundle
        with self.callback_manager.as_trace("query"):
            with self.callback_manager.event(
                CBEventType.RETRIEVE,
                payload={EventPayload.QUERY_STR: query_bundle.query_str},
            ) as retrieve_event:
                nodes = self._retrieve(query_bundle, query_history=query_history)
                nodes = self._handle_recursive_retrieval(query_bundle, nodes)
                retrieve_event.on_end(
                    payload={EventPayload.NODES: nodes},
                )
        dispatch_event(
            RetrievalEndEvent(
                str_or_query_bundle=str_or_query_bundle,
                nodes=nodes,
            )
        )
        return nodes

    async def_aretrieve(
        self, query_bundle: QueryBundle, query_history: List[Dict] = None
    ) -> List[NodeWithScore]:
        return self._retrieve(query_bundle, query_history=query_history)

    @dispatcher.span
    async defaretrieve(
        self, str_or_query_bundle: QueryType, query_history: List[Dict] = None
    ) -> List[NodeWithScore]:
        self._check_callback_manager()
        dispatch_event = dispatcher.get_dispatch_event()

        dispatch_event(
            RetrievalStartEvent(
                str_or_query_bundle=str_or_query_bundle,
            )
        )
        if isinstance(str_or_query_bundle, str):
            query_bundle = QueryBundle(str_or_query_bundle)
        else:
            query_bundle = str_or_query_bundle
        with self.callback_manager.as_trace("query"):
            with self.callback_manager.event(
                CBEventType.RETRIEVE,
                payload={EventPayload.QUERY_STR: query_bundle.query_str},
            ) as retrieve_event:
                nodes = await self._aretrieve(
                    query_bundle=query_bundle, query_history=query_history
                )
                nodes = await self._ahandle_recursive_retrieval(
                    query_bundle=query_bundle, nodes=nodes
                )
                retrieve_event.on_end(
                    payload={EventPayload.NODES: nodes},
                )
        dispatch_event(
            RetrievalEndEvent(
                str_or_query_bundle=str_or_query_bundle,
                nodes=nodes,
            )
        )
        return nodes

    def_retrieve(self, query_bundle: QueryBundle, **kwargs) -> List[NodeWithScore]:
        # init params
        params = {
            "query": query_bundle.query_str,
            "dense_similarity_top_k": self.dense_similarity_top_k,
            "sparse_similarity_top_k": self.sparse_similarity_top_k,
            "enable_rewrite": self.enable_rewrite,
            "rewrite": [
                {
                    "model_name": self.rewrite_model_name,
                    "class_name": "DashScopeTextRewrite",
                }
            ],
            "enable_reranking": self.enable_reranking,
            "rerank": [
                {
                    "model_name": self.rerank_model_name,
                }
            ],
            "rerank_min_score": self.rerank_min_score,
            "rerank_top_n": self.rerank_top_n,
        }
        # extract query_history for multi-turn query rewrite
        if "query_history" in kwargs:
            params["query_hisory"] = kwargs.get("query_history")

        response_data = utils.post(self.base_url, headers=self.headers, params=params)
        nodes = []
        for ele in response_data["nodes"]:
            text_node = TextNode.parse_obj(ele["node"])
            nodes.append(NodeWithScore(node=text_node, score=ele["score"]))
        return nodes

```
 |  
| --- | --- |  
###  retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/dashscope/#llama_index.indices.managed.dashscope.DashScopeCloudRetriever.retrieve "Permanent link")

```
retrieve(
    str_or_query_bundle: QueryType,
    query_history: [] = None,
) -> []

```

Retrieve nodes given query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `str_or_query_bundle`  |  `QueryType`  |  Either a query string or a QueryBundle object.  |  _required_  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-dashscope/llama_index/indices/managed/dashscope/retriever.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defretrieve(
    self, str_or_query_bundle: QueryType, query_history: List[Dict] = None
) -> List[NodeWithScore]:
"""
    Retrieve nodes given query.

    Args:
        str_or_query_bundle (QueryType): Either a query string or
            a QueryBundle object.

    """
    dispatch_event = dispatcher.get_dispatch_event()

    self._check_callback_manager()
    dispatch_event(
        RetrievalStartEvent(
            str_or_query_bundle=str_or_query_bundle,
        )
    )
    if isinstance(str_or_query_bundle, str):
        query_bundle = QueryBundle(str_or_query_bundle)
    else:
        query_bundle = str_or_query_bundle
    with self.callback_manager.as_trace("query"):
        with self.callback_manager.event(
            CBEventType.RETRIEVE,
            payload={EventPayload.QUERY_STR: query_bundle.query_str},
        ) as retrieve_event:
            nodes = self._retrieve(query_bundle, query_history=query_history)
            nodes = self._handle_recursive_retrieval(query_bundle, nodes)
            retrieve_event.on_end(
                payload={EventPayload.NODES: nodes},
            )
    dispatch_event(
        RetrievalEndEvent(
            str_or_query_bundle=str_or_query_bundle,
            nodes=nodes,
        )
    )
    return nodes

```
 |  
| --- | --- |  
options: members: - DashScopeCloudIndex
