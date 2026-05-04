# Sql
##  BaseRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.BaseRetriever "Permanent link")
Bases: `PromptMixin`, `DispatcherSpanMixin`
Base retriever.
Source code in `llama-index-core/llama_index/core/base/base_retriever.py`  
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
```
 | 
```
classBaseRetriever(PromptMixin, DispatcherSpanMixin):
"""Base retriever."""

    def__init__(
        self,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[Dict] = None,
        objects: Optional[List[IndexNode]] = None,
        verbose: bool = False,
    ) -> None:
        self.callback_manager = callback_manager or CallbackManager()

        if objects is not None:
            object_map = {obj.index_id: obj.obj for obj in objects}

        self.object_map = object_map or {}
        self._verbose = verbose

    def_check_callback_manager(self) -> None:
"""Check callback manager."""
        if not hasattr(self, "callback_manager"):
            self.callback_manager = Settings.callback_manager

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {}

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt modules."""
        return {}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""

    def_retrieve_from_object(
        self,
        obj: Any,
        query_bundle: QueryBundle,
        score: float,
    ) -> List[NodeWithScore]:
"""Retrieve nodes from object."""
        if self._verbose:
            print_text(
                f"Retrieving from object {obj.__class__.__name__} with query {query_bundle.query_str}\n",
                color="llama_pink",
            )
        if isinstance(obj, NodeWithScore):
            return [obj]
        elif isinstance(obj, BaseNode):
            return [NodeWithScore(node=obj, score=score)]
        elif isinstance(obj, BaseQueryEngine):
            response = obj.query(query_bundle)
            return [
                NodeWithScore(
                    node=TextNode(text=str(response), metadata=response.metadata or {}),
                    score=score,
                )
            ]
        elif isinstance(obj, BaseRetriever):
            return obj.retrieve(query_bundle)
        else:
            raise ValueError(f"Object {obj} is not retrievable.")

    async def_aretrieve_from_object(
        self,
        obj: Any,
        query_bundle: QueryBundle,
        score: float,
    ) -> List[NodeWithScore]:
"""Retrieve nodes from object."""
        if isinstance(obj, NodeWithScore):
            return [obj]
        elif isinstance(obj, BaseNode):
            return [NodeWithScore(node=obj, score=score)]
        elif isinstance(obj, BaseQueryEngine):
            response = await obj.aquery(query_bundle)
            return [
                NodeWithScore(
                    node=TextNode(text=str(response), metadata=response.metadata or {}),
                    score=score,
                )
            ]
        elif isinstance(obj, BaseRetriever):
            return await obj.aretrieve(query_bundle)
        else:
            raise ValueError(f"Object {obj} is not retrievable.")

    def_handle_recursive_retrieval(
        self, query_bundle: QueryBundle, nodes: List[NodeWithScore]
    ) -> List[NodeWithScore]:
        retrieved_nodes: List[NodeWithScore] = []
        for n in nodes:
            node = n.node
            score = n.score or 1.0
            if isinstance(node, IndexNode):
                obj = node.obj or self.object_map.get(node.index_id, None)
                if obj is not None:
                    if self._verbose:
                        print_text(
                            f"Retrieval entering {node.index_id}: {obj.__class__.__name__}\n",
                            color="llama_turquoise",
                        )
                    retrieved_nodes.extend(
                        self._retrieve_from_object(
                            obj, query_bundle=query_bundle, score=score
                        )
                    )
                else:
                    retrieved_nodes.append(n)
            else:
                retrieved_nodes.append(n)

        seen = set()
        return [
            n
            for n in retrieved_nodes
            if not (
                n.node.node_id in seen or seen.add(n.node.node_id)  # type: ignore[func-returns-value]
            )
        ]

    async def_ahandle_recursive_retrieval(
        self, query_bundle: QueryBundle, nodes: List[NodeWithScore]
    ) -> List[NodeWithScore]:
        retrieved_nodes: List[NodeWithScore] = []
        for n in nodes:
            node = n.node
            score = n.score or 1.0
            if isinstance(node, IndexNode):
                obj = node.obj or self.object_map.get(node.index_id, None)
                if obj is not None:
                    if self._verbose:
                        print_text(
                            f"Retrieval entering {node.index_id}: {obj.__class__.__name__}\n",
                            color="llama_turquoise",
                        )
                    # TODO: Add concurrent execution via `run_jobs()` ?
                    retrieved_nodes.extend(
                        await self._aretrieve_from_object(
                            obj, query_bundle=query_bundle, score=score
                        )
                    )
                else:
                    retrieved_nodes.append(n)
            else:
                retrieved_nodes.append(n)

        # remove any duplicates based on node_id
        seen = set()
        return [
            n
            for n in retrieved_nodes
            if not (
                n.node.node_id in seen or seen.add(n.node.node_id)  # type: ignore[func-returns-value]
            )
        ]

    @dispatcher.span
    defretrieve(self, str_or_query_bundle: QueryType) -> List[NodeWithScore]:
"""
        Retrieve nodes given query.

        Args:
            str_or_query_bundle (QueryType): Either a query string or
                a QueryBundle object.

        """
        self._check_callback_manager()
        dispatcher.event(
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
                nodes = self._retrieve(query_bundle)
                nodes = self._handle_recursive_retrieval(query_bundle, nodes)
                retrieve_event.on_end(
                    payload={EventPayload.NODES: nodes},
                )
        dispatcher.event(
            RetrievalEndEvent(
                str_or_query_bundle=str_or_query_bundle,
                nodes=nodes,
            )
        )
        return nodes

    @dispatcher.span
    async defaretrieve(self, str_or_query_bundle: QueryType) -> List[NodeWithScore]:
        self._check_callback_manager()

        dispatcher.event(
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
                nodes = await self._aretrieve(query_bundle=query_bundle)
                nodes = await self._ahandle_recursive_retrieval(
                    query_bundle=query_bundle, nodes=nodes
                )
                retrieve_event.on_end(
                    payload={EventPayload.NODES: nodes},
                )
        dispatcher.event(
            RetrievalEndEvent(
                str_or_query_bundle=str_or_query_bundle,
                nodes=nodes,
            )
        )
        return nodes

    @abstractmethod
    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""
        Retrieve nodes given query.

        Implemented by the user.

        """

    # TODO: make this abstract
    # @abstractmethod
    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""
        Asynchronously retrieve nodes given query.

        Implemented by the user.

        """
        return self._retrieve(query_bundle)

```
 |  
| --- | --- |  
###  retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.BaseRetriever.retrieve "Permanent link")

```
retrieve(
    str_or_query_bundle: QueryType,
) -> []

```

Retrieve nodes given query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `str_or_query_bundle`  |  `QueryType`  |  Either a query string or a QueryBundle object.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/base/base_retriever.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defretrieve(self, str_or_query_bundle: QueryType) -> List[NodeWithScore]:
"""
    Retrieve nodes given query.

    Args:
        str_or_query_bundle (QueryType): Either a query string or
            a QueryBundle object.

    """
    self._check_callback_manager()
    dispatcher.event(
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
            nodes = self._retrieve(query_bundle)
            nodes = self._handle_recursive_retrieval(query_bundle, nodes)
            retrieve_event.on_end(
                payload={EventPayload.NODES: nodes},
            )
    dispatcher.event(
        RetrievalEndEvent(
            str_or_query_bundle=str_or_query_bundle,
            nodes=nodes,
        )
    )
    return nodes

```
 |  
| --- | --- |  
##  BaseImageRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.BaseImageRetriever "Permanent link")
Bases: `PromptMixin`, `DispatcherSpanMixin`
Base Image Retriever Abstraction.
Source code in `llama-index-core/llama_index/core/image_retriever.py`  
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
```
 | 
```
classBaseImageRetriever(PromptMixin, DispatcherSpanMixin):
"""Base Image Retriever Abstraction."""

    deftext_to_image_retrieve(
        self, str_or_query_bundle: QueryType
    ) -> List[NodeWithScore]:
"""
        Retrieve image nodes given query or single image input.

        Args:
            str_or_query_bundle (QueryType): a query text
            string or a QueryBundle object.

        """
        if isinstance(str_or_query_bundle, str):
            str_or_query_bundle = QueryBundle(query_str=str_or_query_bundle)
        return self._text_to_image_retrieve(str_or_query_bundle)

    @abstractmethod
    def_text_to_image_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""
        Retrieve image nodes or documents given query text.

        Implemented by the user.

        """

    defimage_to_image_retrieve(
        self, str_or_query_bundle: QueryType
    ) -> List[NodeWithScore]:
"""
        Retrieve image nodes given single image input.

        Args:
            str_or_query_bundle (QueryType): a image path
            string or a QueryBundle object.

        """
        if isinstance(str_or_query_bundle, str):
            # leave query_str as empty since we are using image_path for image retrieval
            str_or_query_bundle = QueryBundle(
                query_str="", image_path=str_or_query_bundle
            )
        return self._image_to_image_retrieve(str_or_query_bundle)

    @abstractmethod
    def_image_to_image_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""
        Retrieve image nodes or documents given image.

        Implemented by the user.

        """

    # Async Methods
    async defatext_to_image_retrieve(
        self,
        str_or_query_bundle: QueryType,
    ) -> List[NodeWithScore]:
        if isinstance(str_or_query_bundle, str):
            str_or_query_bundle = QueryBundle(query_str=str_or_query_bundle)
        return await self._atext_to_image_retrieve(str_or_query_bundle)

    @abstractmethod
    async def_atext_to_image_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""
        Async retrieve image nodes or documents given query text.

        Implemented by the user.

        """

    async defaimage_to_image_retrieve(
        self,
        str_or_query_bundle: QueryType,
    ) -> List[NodeWithScore]:
        if isinstance(str_or_query_bundle, str):
            # leave query_str as empty since we are using image_path for image retrieval
            str_or_query_bundle = QueryBundle(
                query_str="", image_path=str_or_query_bundle
            )
        return await self._aimage_to_image_retrieve(str_or_query_bundle)

    @abstractmethod
    async def_aimage_to_image_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""
        Async retrieve image nodes or documents given image.

        Implemented by the user.

        """

```
 |  
| --- | --- |  
###  text_to_image_retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.BaseImageRetriever.text_to_image_retrieve "Permanent link")

```
text_to_image_retrieve(
    str_or_query_bundle: QueryType,
) -> []

```

Retrieve image nodes given query or single image input.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `str_or_query_bundle`  |  `QueryType`  |  a query text  |  _required_  |  
Source code in `llama-index-core/llama_index/core/image_retriever.py`  
| 
```
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
```
 | 
```
deftext_to_image_retrieve(
    self, str_or_query_bundle: QueryType
) -> List[NodeWithScore]:
"""
    Retrieve image nodes given query or single image input.

    Args:
        str_or_query_bundle (QueryType): a query text
        string or a QueryBundle object.

    """
    if isinstance(str_or_query_bundle, str):
        str_or_query_bundle = QueryBundle(query_str=str_or_query_bundle)
    return self._text_to_image_retrieve(str_or_query_bundle)

```
 |  
| --- | --- |  
###  image_to_image_retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.BaseImageRetriever.image_to_image_retrieve "Permanent link")

```
image_to_image_retrieve(
    str_or_query_bundle: QueryType,
) -> []

```

Retrieve image nodes given single image input.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `str_or_query_bundle`  |  `QueryType`  |  a image path  |  _required_  |  
Source code in `llama-index-core/llama_index/core/image_retriever.py`  
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
```
 | 
```
defimage_to_image_retrieve(
    self, str_or_query_bundle: QueryType
) -> List[NodeWithScore]:
"""
    Retrieve image nodes given single image input.

    Args:
        str_or_query_bundle (QueryType): a image path
        string or a QueryBundle object.

    """
    if isinstance(str_or_query_bundle, str):
        # leave query_str as empty since we are using image_path for image retrieval
        str_or_query_bundle = QueryBundle(
            query_str="", image_path=str_or_query_bundle
        )
    return self._image_to_image_retrieve(str_or_query_bundle)

```
 |  
| --- | --- |  
##  EmptyIndexRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.EmptyIndexRetriever "Permanent link")
Bases: 
EmptyIndex query.
Passes the raw LLM call to the underlying LLM model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `input_prompt`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Simple Input Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
Source code in `llama-index-core/llama_index/core/indices/empty/retrievers.py`  
| 
```
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
```
 | 
```
classEmptyIndexRetriever(BaseRetriever):
"""
    EmptyIndex query.

    Passes the raw LLM call to the underlying LLM model.

    Args:
        input_prompt (Optional[BasePromptTemplate]): A Simple Input Prompt
            (see :ref:`Prompt-Templates`).

    """

    def__init__(
        self,
        index: EmptyIndex,
        input_prompt: Optional[BasePromptTemplate] = None,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._index = index
        self._input_prompt = input_prompt or DEFAULT_SIMPLE_INPUT_PROMPT
        super().__init__(callback_manager)

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve relevant nodes."""
        del query_bundle  # Unused
        return []

```
 |  
| --- | --- |  
##  KeywordTableSimpleRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.KeywordTableSimpleRetriever "Permanent link")
Bases: 
Keyword Table Index Simple Retriever.
Extracts keywords using simple regex-based keyword extractor. Set when `retriever_mode="simple"`.
See BaseGPTKeywordTableQuery for arguments.
Source code in `llama-index-core/llama_index/core/indices/keyword_table/retrievers.py`  
| 
```
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
```
 | 
```
classKeywordTableSimpleRetriever(BaseKeywordTableRetriever):
"""
    Keyword Table Index Simple Retriever.

    Extracts keywords using simple regex-based keyword extractor.
    Set when `retriever_mode="simple"`.

    See BaseGPTKeywordTableQuery for arguments.

    """

    def_get_keywords(self, query_str: str) -> List[str]:
"""Extract keywords."""
        return list(
            simple_extract_keywords(query_str, max_keywords=self.max_keywords_per_query)
        )

```
 |  
| --- | --- |  
##  KGTableRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.KGTableRetriever "Permanent link")
Bases: 
KG Table Retriever.
Arguments are shared among subclasses.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_keyword_extract_template`  |  `Optional[QueryKGExtractPrompt]`  |  A Query KG Extraction Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `refine_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Refinement Prompt (see :ref:`Prompt-Templates`).  |  _required_  |  
|  `text_qa_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Question Answering Prompt (see :ref:`Prompt-Templates`).  |  _required_  |  
|  `max_keywords_per_query`  |  Maximum number of keywords to extract from query.  |  
|  `num_chunks_per_query`  |  Maximum number of text chunks to query.  |  
|  `include_text`  |  `bool`  |  Use the document text source from each relevant triplet during queries.  |  `True`  |  
|  `retriever_mode`  |  `KGRetrieverMode`  |  Specifies whether to use keywords, embeddings, or both to find relevant triplets. Should be one of "keyword", "embedding", or "hybrid".  |  `KEYWORD`  |  
|  `similarity_top_k`  |  The number of top embeddings to use (if embeddings are used).  |  
|  `graph_store_query_depth`  |  The depth of the graph store query.  |  
|  `use_global_node_triplets`  |  `bool`  |  Whether to get more keywords(entities) from text chunks matched by keywords. This helps introduce more global knowledge. While it's more expensive, thus to be turned off by default.  |  `False`  |  
|  `max_knowledge_sequence`  |  The maximum number of knowledge sequence to include in the response. By default, it's 30.  |  `REL_TEXT_LIMIT`  |  
Source code in `llama-index-core/llama_index/core/indices/knowledge_graph/retrievers.py`  
| 
```
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
```
 | 
```
@deprecated.deprecated(
    version="0.10.53",
    reason=(
        "KGTableRetriever is deprecated, it is recommended to use "
        "PropertyGraphIndex and associated retrievers instead."
    ),
)
classKGTableRetriever(BaseRetriever):
"""
    KG Table Retriever.

    Arguments are shared among subclasses.

    Args:
        query_keyword_extract_template (Optional[QueryKGExtractPrompt]): A Query
            KG Extraction
            Prompt (see :ref:`Prompt-Templates`).
        refine_template (Optional[BasePromptTemplate]): A Refinement Prompt
            (see :ref:`Prompt-Templates`).
        text_qa_template (Optional[BasePromptTemplate]): A Question Answering Prompt
            (see :ref:`Prompt-Templates`).
        max_keywords_per_query (int): Maximum number of keywords to extract from query.
        num_chunks_per_query (int): Maximum number of text chunks to query.
        include_text (bool): Use the document text source from each relevant triplet
            during queries.
        retriever_mode (KGRetrieverMode): Specifies whether to use keywords,
            embeddings, or both to find relevant triplets. Should be one of "keyword",
            "embedding", or "hybrid".
        similarity_top_k (int): The number of top embeddings to use
            (if embeddings are used).
        graph_store_query_depth (int): The depth of the graph store query.
        use_global_node_triplets (bool): Whether to get more keywords(entities) from
            text chunks matched by keywords. This helps introduce more global knowledge.
            While it's more expensive, thus to be turned off by default.
        max_knowledge_sequence (int): The maximum number of knowledge sequence to
            include in the response. By default, it's 30.

    """

    def__init__(
        self,
        index: KnowledgeGraphIndex,
        llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        query_keyword_extract_template: Optional[BasePromptTemplate] = None,
        max_keywords_per_query: int = 10,
        num_chunks_per_query: int = 10,
        include_text: bool = True,
        retriever_mode: Optional[KGRetrieverMode] = KGRetrieverMode.KEYWORD,
        similarity_top_k: int = 2,
        graph_store_query_depth: int = 2,
        use_global_node_triplets: bool = False,
        max_knowledge_sequence: int = REL_TEXT_LIMIT,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        assert isinstance(index, KnowledgeGraphIndex)
        self._index = index
        self._index_struct = self._index.index_struct
        self._docstore = self._index.docstore

        self.max_keywords_per_query = max_keywords_per_query
        self.num_chunks_per_query = num_chunks_per_query
        self.query_keyword_extract_template = query_keyword_extract_template or DQKET
        self.similarity_top_k = similarity_top_k
        self._include_text = include_text
        self._retriever_mode = (
            KGRetrieverMode(retriever_mode)
            if retriever_mode
            else KGRetrieverMode.KEYWORD
        )

        self._llm = llm or Settings.llm
        self._embed_model = embed_model or Settings.embed_model
        self._graph_store = index.graph_store
        self.graph_store_query_depth = graph_store_query_depth
        self.use_global_node_triplets = use_global_node_triplets
        self.max_knowledge_sequence = max_knowledge_sequence
        self._verbose = kwargs.get("verbose", False)
        refresh_schema = kwargs.get("refresh_schema", False)
        try:
            self._graph_schema = self._graph_store.get_schema(refresh=refresh_schema)
        except NotImplementedError:
            self._graph_schema = ""
        except Exception as e:
            logger.warning(f"Failed to get graph schema: {e}")
            self._graph_schema = ""
        super().__init__(
            callback_manager=callback_manager or Settings.callback_manager,
            object_map=object_map,
            verbose=verbose,
        )

    def_get_keywords(self, query_str: str) -> List[str]:
"""Extract keywords."""
        response = self._llm.predict(
            self.query_keyword_extract_template,
            max_keywords=self.max_keywords_per_query,
            question=query_str,
        )
        keywords = extract_keywords_given_response(
            response, start_token="KEYWORDS:", lowercase=False
        )
        return list(keywords)

    def_extract_rel_text_keywords(self, rel_texts: List[str]) -> List[str]:
"""Find the keywords for given rel text triplets."""
        keywords = []

        for rel_text in rel_texts:
            splited_texts = rel_text.split(",")

            if len(splited_texts) <= 0:
                continue
            keyword = splited_texts[0]
            if keyword:
                keywords.append(keyword.strip("(\"'"))

            # Return the Object as well
            if len(splited_texts) <= 2:
                continue
            keyword = splited_texts[2]
            if keyword:
                keywords.append(keyword.strip(" ()\"'"))
        return keywords

    def_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""Get nodes for response."""
        node_visited = set()
        keywords = self._get_keywords(query_bundle.query_str)
        if self._verbose:
            print_text(f"Extracted keywords: {keywords}\n", color="green")
        rel_texts = []
        cur_rel_map = {}
        chunk_indices_count: Dict[str, int] = defaultdict(int)
        if self._retriever_mode != KGRetrieverMode.EMBEDDING:
            for keyword in keywords:
                subjs = {keyword}
                node_ids = self._index_struct.search_node_by_keyword(keyword)
                for node_id in node_ids[:GLOBAL_EXPLORE_NODE_LIMIT]:
                    if node_id in node_visited:
                        continue

                    if self._include_text:
                        chunk_indices_count[node_id] += 1

                    node_visited.add(node_id)
                    if self.use_global_node_triplets:
                        # Get nodes from keyword search, and add them to the subjs
                        # set. This helps introduce more global knowledge into the
                        # query. While it's more expensive, thus to be turned off
                        # by default, it can be useful for some applications.

                        # TODO: we should a keyword-node_id map in IndexStruct, so that
                        # node-keywords extraction with LLM will be called only once
                        # during indexing.
                        extended_subjs = self._get_keywords(
                            self._docstore.get_node(node_id).get_content(
                                metadata_mode=MetadataMode.LLM
                            )
                        )
                        subjs.update(extended_subjs)

                rel_map = self._graph_store.get_rel_map(
                    list(subjs), self.graph_store_query_depth
                )

                logger.debug(f"rel_map: {rel_map}")

                if not rel_map:
                    continue
                rel_texts.extend(
                    [
                        str(rel_obj)
                        for rel_objs in rel_map.values()
                        for rel_obj in rel_objs
                    ]
                )
                cur_rel_map.update(rel_map)

        if (
            self._retriever_mode != KGRetrieverMode.KEYWORD
            and len(self._index_struct.embedding_dict)  0
        ):
            query_embedding = self._embed_model.get_text_embedding(
                query_bundle.query_str
            )
            all_rel_texts = list(self._index_struct.embedding_dict.keys())

            rel_text_embeddings = [
                self._index_struct.embedding_dict[_id] for _id in all_rel_texts
            ]
            similarities, top_rel_texts = get_top_k_embeddings(
                query_embedding,
                rel_text_embeddings,
                similarity_top_k=self.similarity_top_k,
                embedding_ids=all_rel_texts,
            )
            logger.debug(
                f"Found the following rel_texts+query similarites: {similarities!s}"
            )
            logger.debug(f"Found the following top_k rel_texts: {rel_texts!s}")
            rel_texts.extend(top_rel_texts)

        elif len(self._index_struct.embedding_dict) == 0:
            logger.warning(
                "Index was not constructed with embeddings, skipping embedding usage..."
            )

        # remove any duplicates from keyword + embedding queries
        if self._retriever_mode == KGRetrieverMode.HYBRID:
            rel_texts = list(set(rel_texts))

            # remove shorter rel_texts that are substrings of longer rel_texts
            rel_texts.sort(key=len, reverse=True)
            for i in range(len(rel_texts)):
                for j in range(i + 1, len(rel_texts)):
                    if rel_texts[j] in rel_texts[i]:
                        rel_texts[j] = ""
            rel_texts = [rel_text for rel_text in rel_texts if rel_text != ""]

            # truncate rel_texts
            rel_texts = rel_texts[: self.max_knowledge_sequence]

        # When include_text = True just get the actual content of all the nodes
        # (Nodes with actual keyword match, Nodes which are found from the depth search and Nodes founnd from top_k similarity)
        if self._include_text:
            keywords = self._extract_rel_text_keywords(
                rel_texts
            )  # rel_texts will have all the Triplets retrieved with respect to the Query
            nested_node_ids = [
                self._index_struct.search_node_by_keyword(keyword)
                for keyword in keywords
            ]
            node_ids = [_id for ids in nested_node_ids for _id in ids]
            for node_id in node_ids:
                chunk_indices_count[node_id] += 1

        sorted_chunk_indices = sorted(
            chunk_indices_count.keys(),
            key=lambda x: chunk_indices_count[x],
            reverse=True,
        )
        sorted_chunk_indices = sorted_chunk_indices[: self.num_chunks_per_query]
        sorted_nodes = self._docstore.get_nodes(sorted_chunk_indices)

        # TMP/TODO: also filter rel_texts as nodes until we figure out better
        # abstraction
        # TODO(suo): figure out what this does
        # rel_text_nodes = [Node(text=rel_text) for rel_text in rel_texts]
        # for node_processor in self._node_postprocessors:
        #     rel_text_nodes = node_processor.postprocess_nodes(rel_text_nodes)
        # rel_texts = [node.get_content() for node in rel_text_nodes]

        sorted_nodes_with_scores = []
        for chunk_idx, node in zip(sorted_chunk_indices, sorted_nodes):
            # nodes are found with keyword mapping, give high conf to avoid cutoff
            sorted_nodes_with_scores.append(
                NodeWithScore(node=node, score=DEFAULT_NODE_SCORE)
            )
            logger.info(
                f"> Querying with idx: {chunk_idx}: "
                f"{truncate_text(node.get_content(),80)}"
            )
        # if no relationship is found, return the nodes found by keywords
        if not rel_texts:
            logger.info("> No relationships found, returning nodes found by keywords.")
            if len(sorted_nodes_with_scores) == 0:
                logger.info("> No nodes found by keywords, returning empty response.")
                return [
                    NodeWithScore(
                        node=TextNode(text="No relationships found."), score=1.0
                    )
                ]
            # In else case the sorted_nodes_with_scores is not empty
            # thus returning the nodes found by keywords
            return sorted_nodes_with_scores

        # add relationships as Node
        # TODO: make initial text customizable
        rel_initial_text = (
            f"The following are knowledge sequence in max depth"
            f" {self.graph_store_query_depth} "
            f"in the form of directed graph like:\n"
            f"`subject -[predicate]->, object, <-[predicate_next_hop]-,"
            f" object_next_hop ...`"
        )
        rel_info = [rel_initial_text, *rel_texts]
        rel_node_info = {
            "kg_rel_texts": rel_texts,
            "kg_rel_map": cur_rel_map,
        }
        if self._graph_schema != "":
            rel_node_info["kg_schema"] = {"schema": self._graph_schema}
        rel_info_text = "\n".join(
            [
                str(item)
                for sublist in rel_info
                for item in (sublist if isinstance(sublist, list) else [sublist])
            ]
        )
        if self._verbose:
            print_text(f"KG context:\n{rel_info_text}\n", color="blue")
        rel_text_node = TextNode(
            text=rel_info_text,
            metadata=rel_node_info,
            excluded_embed_metadata_keys=["kg_rel_map", "kg_rel_texts"],
            excluded_llm_metadata_keys=["kg_rel_map", "kg_rel_texts"],
        )
        # this node is constructed from rel_texts, give high confidence to avoid cutoff
        sorted_nodes_with_scores.append(
            NodeWithScore(node=rel_text_node, score=DEFAULT_NODE_SCORE)
        )

        return sorted_nodes_with_scores

    def_get_metadata_for_response(
        self, nodes: List[BaseNode]
    ) -> Optional[Dict[str, Any]]:
"""Get metadata for response."""
        for node in nodes:
            if node.metadata is None or "kg_rel_map" not in node.metadata:
                continue
            return node.metadata
        raise ValueError("kg_rel_map must be found in at least one Node.")

```
 |  
| --- | --- |  
##  KnowledgeGraphRAGRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.KnowledgeGraphRAGRetriever "Permanent link")
Bases: 
Knowledge Graph RAG retriever.
Retriever that perform SubGraph RAG towards knowledge graph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `storage_context`  |  `Optional[StorageContext[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.storage.storage_context.StorageContext "StorageContext


  
      dataclass
   \(llama_index.core.storage.storage_context.StorageContext\)")]`  |  A storage context to use.  |  `None`  |  
|  `entity_extract_fn`  |  `Optional[Callable]`  |  A function to extract entities.  |  `None`  |  
|  `entity_extract_template Optional[BasePromptTemplate])`  |  A Query Key Entity Extraction Prompt (see :ref:`Prompt-Templates`).  |  _required_  |  
|  `entity_extract_policy`  |  `Optional[str]`  |  The entity extraction policy to use. default: "union" possible values: "union", "intersection"  |  `'union'`  |  
|  `synonym_expand_fn`  |  `Optional[Callable]`  |  A function to expand synonyms.  |  `None`  |  
|  `synonym_expand_template`  |  `Optional[QueryKeywordExpandPrompt]`  |  A Query Key Entity Expansion Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `synonym_expand_policy`  |  `Optional[str]`  |  The synonym expansion policy to use. default: "union" possible values: "union", "intersection"  |  `'union'`  |  
|  `max_entities`  |  The maximum number of entities to extract. default: 5  |  
|  `max_synonyms`  |  The maximum number of synonyms to expand per entity. default: 5  |  
|  `retriever_mode`  |  `Optional[str]`  |  The retriever mode to use. default: "keyword" possible values: "keyword", "embedding", "keyword_embedding"  |  `'keyword'`  |  
|  `with_nl2graphquery`  |  `bool`  |  Whether to combine NL2GraphQuery in context. default: False  |  `False`  |  
|  `graph_traversal_depth`  |  The depth of graph traversal. default: 2  |  
|  `max_knowledge_sequence`  |  The maximum number of knowledge sequence to include in the response. By default, it's 30.  |  `REL_TEXT_LIMIT`  |  
|  `verbose`  |  `bool`  |  Whether to print out debug info.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/knowledge_graph/retrievers.py`  
| 
```
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
```
 | 
```
@deprecated.deprecated(
    version="0.10.53",
    reason=(
        "KnowledgeGraphRAGRetriever is deprecated, it is recommended to use "
        "PropertyGraphIndex and associated retrievers instead."
    ),
)
classKnowledgeGraphRAGRetriever(BaseRetriever):
"""
    Knowledge Graph RAG retriever.

    Retriever that perform SubGraph RAG towards knowledge graph.

    Args:
        storage_context (Optional[StorageContext]): A storage context to use.
        entity_extract_fn (Optional[Callable]): A function to extract entities.
        entity_extract_template Optional[BasePromptTemplate]): A Query Key Entity
            Extraction Prompt (see :ref:`Prompt-Templates`).
        entity_extract_policy (Optional[str]): The entity extraction policy to use.
            default: "union"
            possible values: "union", "intersection"
        synonym_expand_fn (Optional[Callable]): A function to expand synonyms.
        synonym_expand_template (Optional[QueryKeywordExpandPrompt]): A Query Key Entity
            Expansion Prompt (see :ref:`Prompt-Templates`).
        synonym_expand_policy (Optional[str]): The synonym expansion policy to use.
            default: "union"
            possible values: "union", "intersection"
        max_entities (int): The maximum number of entities to extract.
            default: 5
        max_synonyms (int): The maximum number of synonyms to expand per entity.
            default: 5
        retriever_mode (Optional[str]): The retriever mode to use.
            default: "keyword"
            possible values: "keyword", "embedding", "keyword_embedding"
        with_nl2graphquery (bool): Whether to combine NL2GraphQuery in context.
            default: False
        graph_traversal_depth (int): The depth of graph traversal.
            default: 2
        max_knowledge_sequence (int): The maximum number of knowledge sequence to
            include in the response. By default, it's 30.
        verbose (bool): Whether to print out debug info.

    """

    def__init__(
        self,
        storage_context: Optional[StorageContext] = None,
        llm: Optional[LLM] = None,
        entity_extract_fn: Optional[Callable] = None,
        entity_extract_template: Optional[BasePromptTemplate] = None,
        entity_extract_policy: Optional[str] = "union",
        synonym_expand_fn: Optional[Callable] = None,
        synonym_expand_template: Optional[BasePromptTemplate] = None,
        synonym_expand_policy: Optional[str] = "union",
        max_entities: int = 5,
        max_synonyms: int = 5,
        retriever_mode: Optional[str] = "keyword",
        with_nl2graphquery: bool = False,
        graph_traversal_depth: int = 2,
        max_knowledge_sequence: int = REL_TEXT_LIMIT,
        verbose: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize the retriever."""
        # Ensure that we have a graph store
        assert storage_context is not None, "Must provide a storage context."
        assert storage_context.graph_store is not None, (
            "Must provide a graph store in the storage context."
        )
        self._storage_context = storage_context
        self._graph_store = storage_context.graph_store

        self._llm = llm or Settings.llm

        self._entity_extract_fn = entity_extract_fn
        self._entity_extract_template = (
            entity_extract_template or DEFAULT_QUERY_KEYWORD_EXTRACT_TEMPLATE
        )
        self._entity_extract_policy = entity_extract_policy

        self._synonym_expand_fn = synonym_expand_fn
        self._synonym_expand_template = (
            synonym_expand_template or DEFAULT_SYNONYM_EXPAND_PROMPT
        )
        self._synonym_expand_policy = synonym_expand_policy

        self._max_entities = max_entities
        self._max_synonyms = max_synonyms
        self._retriever_mode = retriever_mode
        self._with_nl2graphquery = with_nl2graphquery
        if self._with_nl2graphquery:
            fromllama_index.core.query_engine.knowledge_graph_query_engineimport (
                KnowledgeGraphQueryEngine,
            )

            graph_query_synthesis_prompt = kwargs.get("graph_query_synthesis_prompt")
            if graph_query_synthesis_prompt is not None:
                del kwargs["graph_query_synthesis_prompt"]

            graph_response_answer_prompt = kwargs.get("graph_response_answer_prompt")
            if graph_response_answer_prompt is not None:
                del kwargs["graph_response_answer_prompt"]

            refresh_schema = kwargs.get("refresh_schema", False)
            response_synthesizer = kwargs.get("response_synthesizer")
            self._kg_query_engine = KnowledgeGraphQueryEngine(
                llm=self._llm,
                storage_context=self._storage_context,
                graph_query_synthesis_prompt=graph_query_synthesis_prompt,
                graph_response_answer_prompt=graph_response_answer_prompt,
                refresh_schema=refresh_schema,
                verbose=verbose,
                response_synthesizer=response_synthesizer,
                **kwargs,
            )

        self._graph_traversal_depth = graph_traversal_depth
        self._max_knowledge_sequence = max_knowledge_sequence
        self._verbose = verbose
        refresh_schema = kwargs.get("refresh_schema", False)
        try:
            self._graph_schema = self._graph_store.get_schema(refresh=refresh_schema)
        except NotImplementedError:
            self._graph_schema = ""
        except Exception as e:
            logger.warning(f"Failed to get graph schema: {e}")
            self._graph_schema = ""

        super().__init__(callback_manager=callback_manager or Settings.callback_manager)

    def_process_entities(
        self,
        query_str: str,
        handle_fn: Optional[Callable],
        handle_llm_prompt_template: Optional[BasePromptTemplate],
        cross_handle_policy: Optional[str] = "union",
        max_items: Optional[int] = 5,
        result_start_token: str = "KEYWORDS:",
    ) -> List[str]:
"""Get entities from query string."""
        assert cross_handle_policy in [
            "union",
            "intersection",
        ], "Invalid entity extraction policy."
        if cross_handle_policy == "intersection":
            assert all(
                [
                    handle_fn is not None,
                    handle_llm_prompt_template is not None,
                ]
            ), "Must provide entity extract function and template."
        assert any(
            [
                handle_fn is not None,
                handle_llm_prompt_template is not None,
            ]
        ), "Must provide either entity extract function or template."
        enitities_fn: List[str] = []
        enitities_llm: Set[str] = set()

        if handle_fn is not None:
            enitities_fn = handle_fn(query_str)
        if handle_llm_prompt_template is not None:
            response = self._llm.predict(
                handle_llm_prompt_template,
                max_keywords=max_items,
                question=query_str,
            )
            enitities_llm = extract_keywords_given_response(
                response, start_token=result_start_token, lowercase=False
            )
        if cross_handle_policy == "union":
            entities = list(set(enitities_fn) | enitities_llm)
        elif cross_handle_policy == "intersection":
            entities = list(set(enitities_fn).intersection(set(enitities_llm)))
        if self._verbose:
            print_text(f"Entities processed: {entities}\n", color="green")

        return entities

    async def_aprocess_entities(
        self,
        query_str: str,
        handle_fn: Optional[Callable],
        handle_llm_prompt_template: Optional[BasePromptTemplate],
        cross_handle_policy: Optional[str] = "union",
        max_items: Optional[int] = 5,
        result_start_token: str = "KEYWORDS:",
    ) -> List[str]:
"""Get entities from query string."""
        assert cross_handle_policy in [
            "union",
            "intersection",
        ], "Invalid entity extraction policy."
        if cross_handle_policy == "intersection":
            assert all(
                [
                    handle_fn is not None,
                    handle_llm_prompt_template is not None,
                ]
            ), "Must provide entity extract function and template."
        assert any(
            [
                handle_fn is not None,
                handle_llm_prompt_template is not None,
            ]
        ), "Must provide either entity extract function or template."
        enitities_fn: List[str] = []
        enitities_llm: Set[str] = set()

        if handle_fn is not None:
            enitities_fn = handle_fn(query_str)
        if handle_llm_prompt_template is not None:
            response = await self._llm.apredict(
                handle_llm_prompt_template,
                max_keywords=max_items,
                question=query_str,
            )
            enitities_llm = extract_keywords_given_response(
                response, start_token=result_start_token, lowercase=False
            )
        if cross_handle_policy == "union":
            entities = list(set(enitities_fn) | enitities_llm)
        elif cross_handle_policy == "intersection":
            entities = list(set(enitities_fn).intersection(set(enitities_llm)))
        if self._verbose:
            print_text(f"Entities processed: {entities}\n", color="green")

        return entities

    def_get_entities(self, query_str: str) -> List[str]:
"""Get entities from query string."""
        entities = self._process_entities(
            query_str,
            self._entity_extract_fn,
            self._entity_extract_template,
            self._entity_extract_policy,
            self._max_entities,
            "KEYWORDS:",
        )
        expanded_entities = self._expand_synonyms(entities)
        return list(set(entities) | set(expanded_entities))

    async def_aget_entities(self, query_str: str) -> List[str]:
"""Get entities from query string."""
        entities = await self._aprocess_entities(
            query_str,
            self._entity_extract_fn,
            self._entity_extract_template,
            self._entity_extract_policy,
            self._max_entities,
            "KEYWORDS:",
        )
        expanded_entities = await self._aexpand_synonyms(entities)
        return list(set(entities) | set(expanded_entities))

    def_expand_synonyms(self, keywords: List[str]) -> List[str]:
"""Expand synonyms or similar expressions for keywords."""
        return self._process_entities(
            str(keywords),
            self._synonym_expand_fn,
            self._synonym_expand_template,
            self._synonym_expand_policy,
            self._max_synonyms,
            "SYNONYMS:",
        )

    async def_aexpand_synonyms(self, keywords: List[str]) -> List[str]:
"""Expand synonyms or similar expressions for keywords."""
        return await self._aprocess_entities(
            str(keywords),
            self._synonym_expand_fn,
            self._synonym_expand_template,
            self._synonym_expand_policy,
            self._max_synonyms,
            "SYNONYMS:",
        )

    def_get_knowledge_sequence(
        self, entities: List[str]
    ) -> Tuple[List[str], Optional[Dict[Any, Any]]]:
"""Get knowledge sequence from entities."""
        # Get SubGraph from Graph Store as Knowledge Sequence
        rel_map: Optional[Dict] = self._graph_store.get_rel_map(
            entities, self._graph_traversal_depth, limit=self._max_knowledge_sequence
        )
        logger.debug(f"rel_map: {rel_map}")

        # Build Knowledge Sequence
        knowledge_sequence = []
        if rel_map:
            knowledge_sequence.extend(
                [str(rel_obj) for rel_objs in rel_map.values() for rel_obj in rel_objs]
            )
        else:
            logger.info("> No knowledge sequence extracted from entities.")
            return [], None

        return knowledge_sequence, rel_map

    async def_aget_knowledge_sequence(
        self, entities: List[str]
    ) -> Tuple[List[str], Optional[Dict[Any, Any]]]:
"""Get knowledge sequence from entities."""
        # Get SubGraph from Graph Store as Knowledge Sequence
        # TBD: async in graph store
        rel_map: Optional[Dict] = self._graph_store.get_rel_map(
            entities, self._graph_traversal_depth, limit=self._max_knowledge_sequence
        )
        logger.debug(f"rel_map from GraphStore:\n{rel_map}")

        # Build Knowledge Sequence
        knowledge_sequence = []
        if rel_map:
            knowledge_sequence.extend(
                [str(rel_obj) for rel_objs in rel_map.values() for rel_obj in rel_objs]
            )
        else:
            logger.info("> No knowledge sequence extracted from entities.")
            return [], None

        return knowledge_sequence, rel_map

    def_build_nodes(
        self, knowledge_sequence: List[str], rel_map: Optional[Dict[Any, Any]] = None
    ) -> List[NodeWithScore]:
"""Build nodes from knowledge sequence."""
        if len(knowledge_sequence) == 0:
            logger.info("> No knowledge sequence extracted from entities.")
            return []
        _new_line_char = "\n"
        context_string = (
            f"The following are knowledge sequence in max depth"
            f" {self._graph_traversal_depth} "
            f"in the form of directed graph like:\n"
            f"`subject -[predicate]->, object, <-[predicate_next_hop]-,"
            f" object_next_hop ...`"
            f" extracted based on key entities as subject:\n"
            f"{_new_line_char.join(knowledge_sequence)}"
        )
        if self._verbose:
            print_text(f"Graph RAG context:\n{context_string}\n", color="blue")

        rel_node_info = {
            "kg_rel_map": rel_map,
            "kg_rel_text": knowledge_sequence,
        }
        metadata_keys = ["kg_rel_map", "kg_rel_text"]
        if self._graph_schema != "":
            rel_node_info["kg_schema"] = {"schema": self._graph_schema}
            metadata_keys.append("kg_schema")
        node = NodeWithScore(
            node=TextNode(
                text=context_string,
                score=1.0,
                metadata=rel_node_info,
                excluded_embed_metadata_keys=metadata_keys,
                excluded_llm_metadata_keys=metadata_keys,
            )
        )
        return [node]

    def_retrieve_keyword(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve in keyword mode."""
        if self._retriever_mode not in ["keyword", "keyword_embedding"]:
            return []
        # Get entities
        entities = self._get_entities(query_bundle.query_str)
        # Before we enable embedding/semantic search, we need to make sure
        # we don't miss any entities that's synoynm of the entities we extracted
        # in string matching based retrieval in following steps, thus we expand
        # synonyms here.
        if len(entities) == 0:
            logger.info("> No entities extracted from query string.")
            return []

        # Get SubGraph from Graph Store as Knowledge Sequence
        knowledge_sequence, rel_map = self._get_knowledge_sequence(entities)

        return self._build_nodes(knowledge_sequence, rel_map)

    async def_aretrieve_keyword(
        self, query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
"""Retrieve in keyword mode."""
        if self._retriever_mode not in ["keyword", "keyword_embedding"]:
            return []
        # Get entities
        entities = await self._aget_entities(query_bundle.query_str)
        # Before we enable embedding/semantic search, we need to make sure
        # we don't miss any entities that's synoynm of the entities we extracted
        # in string matching based retrieval in following steps, thus we expand
        # synonyms here.
        if len(entities) == 0:
            logger.info("> No entities extracted from query string.")
            return []

        # Get SubGraph from Graph Store as Knowledge Sequence
        knowledge_sequence, rel_map = await self._aget_knowledge_sequence(entities)

        return self._build_nodes(knowledge_sequence, rel_map)

    def_retrieve_embedding(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve in embedding mode."""
        if self._retriever_mode not in ["embedding", "keyword_embedding"]:
            return []
        # TBD: will implement this later with vector store.
        raise NotImplementedError

    async def_aretrieve_embedding(
        self, query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
"""Retrieve in embedding mode."""
        if self._retriever_mode not in ["embedding", "keyword_embedding"]:
            return []
        # TBD: will implement this later with vector store.
        raise NotImplementedError

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Build nodes for response."""
        nodes: List[NodeWithScore] = []
        if self._with_nl2graphquery:
            try:
                nodes_nl2graphquery = self._kg_query_engine._retrieve(query_bundle)
                nodes.extend(nodes_nl2graphquery)
            except Exception as e:
                logger.warning(f"Error in retrieving from nl2graphquery: {e}")

        nodes.extend(self._retrieve_keyword(query_bundle))
        nodes.extend(self._retrieve_embedding(query_bundle))

        return nodes

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Build nodes for response."""
        nodes: List[NodeWithScore] = []
        if self._with_nl2graphquery:
            try:
                nodes_nl2graphquery = await self._kg_query_engine._aretrieve(
                    query_bundle
                )
                nodes.extend(nodes_nl2graphquery)
            except Exception as e:
                logger.warning(f"Error in retrieving from nl2graphquery: {e}")

        nodes.extend(await self._aretrieve_keyword(query_bundle))
        nodes.extend(await self._aretrieve_embedding(query_bundle))

        return nodes

```
 |  
| --- | --- |  
##  SummaryIndexEmbeddingRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.SummaryIndexEmbeddingRetriever "Permanent link")
Bases: 
Embedding based retriever for SummaryIndex.
Generates embeddings in a lazy fashion for all nodes that are traversed.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index`  |   |  The index to retrieve from.  |  _required_  |  
|  `similarity_top_k`  |  `Optional[int]`  |  The number of top nodes to return.  |  
Source code in `llama-index-core/llama_index/core/indices/list/retrievers.py`  
| 
```
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
```
 | 
```
classSummaryIndexEmbeddingRetriever(BaseRetriever):
"""
    Embedding based retriever for SummaryIndex.

    Generates embeddings in a lazy fashion for all
    nodes that are traversed.

    Args:
        index (SummaryIndex): The index to retrieve from.
        similarity_top_k (Optional[int]): The number of top nodes to return.

    """

    def__init__(
        self,
        index: SummaryIndex,
        embed_model: Optional[BaseEmbedding] = None,
        similarity_top_k: Optional[int] = 1,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
        self._index = index
        self._similarity_top_k = similarity_top_k
        self._embed_model = embed_model or Settings.embed_model

        super().__init__(
            callback_manager=callback_manager, object_map=object_map, verbose=verbose
        )

    def_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""Retrieve nodes."""
        node_ids = self._index.index_struct.nodes
        # top k nodes
        nodes = self._index.docstore.get_nodes(node_ids)
        query_embedding, node_embeddings = self._get_embeddings(query_bundle, nodes)

        top_similarities, top_idxs = get_top_k_embeddings(
            query_embedding,
            node_embeddings,
            similarity_top_k=self._similarity_top_k,
            embedding_ids=list(range(len(nodes))),
        )

        top_k_nodes = [nodes[i] for i in top_idxs]

        node_with_scores = []
        for node, similarity in zip(top_k_nodes, top_similarities):
            node_with_scores.append(NodeWithScore(node=node, score=similarity))

        logger.debug(f"> Top {len(top_idxs)} nodes:\n")
        nl = "\n"
        logger.debug(f"{nl.join([n.get_content()fornintop_k_nodes])}")
        return node_with_scores

    def_get_embeddings(
        self, query_bundle: QueryBundle, nodes: List[BaseNode]
    ) -> Tuple[List[float], List[List[float]]]:
"""Get top nodes by similarity to the query."""
        if query_bundle.embedding is None:
            query_bundle.embedding = self._embed_model.get_agg_embedding_from_queries(
                query_bundle.embedding_strs
            )

        node_embeddings: List[List[float]] = []
        nodes_embedded = 0
        for node in nodes:
            if node.embedding is None:
                nodes_embedded += 1
                node.embedding = self._embed_model.get_text_embedding(
                    node.get_content(metadata_mode=MetadataMode.EMBED)
                )

            node_embeddings.append(node.embedding)
        return query_bundle.embedding, node_embeddings

```
 |  
| --- | --- |  
##  SummaryIndexLLMRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.SummaryIndexLLMRetriever "Permanent link")
Bases: 
LLM retriever for SummaryIndex.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index`  |   |  The index to retrieve from.  |  _required_  |  
|  `choice_select_prompt`  |  `Optional[PromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.PromptTemplate "PromptTemplate \(llama_index.core.prompts.PromptTemplate\)")]`  |  A Choice-Select Prompt (see :ref:`Prompt-Templates`).)  |  `None`  |  
|  `choice_batch_size`  |  The number of nodes to query at a time.  |  
|  `format_node_batch_fn`  |  `Optional[Callable]`  |  A function that formats a batch of nodes.  |  `None`  |  
|  `parse_choice_select_answer_fn`  |  `Optional[Callable]`  |  A function that parses the choice select answer.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/indices/list/retrievers.py`  
| 
```
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
```
 | 
```
classSummaryIndexLLMRetriever(BaseRetriever):
"""
    LLM retriever for SummaryIndex.

    Args:
        index (SummaryIndex): The index to retrieve from.
        choice_select_prompt (Optional[PromptTemplate]): A Choice-Select Prompt
           (see :ref:`Prompt-Templates`).)
        choice_batch_size (int): The number of nodes to query at a time.
        format_node_batch_fn (Optional[Callable]): A function that formats a
            batch of nodes.
        parse_choice_select_answer_fn (Optional[Callable]): A function that parses the
            choice select answer.

    """

    def__init__(
        self,
        index: SummaryIndex,
        llm: Optional[LLM] = None,
        choice_select_prompt: Optional[PromptTemplate] = None,
        choice_batch_size: int = 10,
        format_node_batch_fn: Optional[Callable] = None,
        parse_choice_select_answer_fn: Optional[Callable] = None,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
        self._index = index
        self._choice_select_prompt = (
            choice_select_prompt or DEFAULT_CHOICE_SELECT_PROMPT
        )
        self._choice_batch_size = choice_batch_size
        self._format_node_batch_fn = (
            format_node_batch_fn or default_format_node_batch_fn
        )
        self._parse_choice_select_answer_fn = (
            parse_choice_select_answer_fn or default_parse_choice_select_answer_fn
        )
        self._llm = llm or Settings.llm
        super().__init__(
            callback_manager=callback_manager, object_map=object_map, verbose=verbose
        )

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve nodes."""
        node_ids = self._index.index_struct.nodes
        results = []
        for idx in range(0, len(node_ids), self._choice_batch_size):
            node_ids_batch = node_ids[idx : idx + self._choice_batch_size]
            nodes_batch = self._index.docstore.get_nodes(node_ids_batch)

            query_str = query_bundle.query_str
            fmt_batch_str = self._format_node_batch_fn(nodes_batch)
            # call each batch independently
            raw_response = self._llm.predict(
                self._choice_select_prompt,
                context_str=fmt_batch_str,
                query_str=query_str,
            )

            raw_choices, relevances = self._parse_choice_select_answer_fn(
                raw_response, len(nodes_batch)
            )
            choice_idxs = [int(choice) - 1 for choice in raw_choices]
            choice_node_ids = [node_ids_batch[idx] for idx in choice_idxs]

            choice_nodes = self._index.docstore.get_nodes(choice_node_ids)
            relevances = relevances or [1.0 for _ in choice_nodes]
            results.extend(
                [
                    NodeWithScore(node=node, score=relevance)
                    for node, relevance in zip(choice_nodes, relevances)
                ]
            )
        return results

```
 |  
| --- | --- |  
##  SummaryIndexRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.SummaryIndexRetriever "Permanent link")
Bases: 
Simple retriever for SummaryIndex that returns all nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index`  |   |  The index to retrieve from.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/list/retrievers.py`  
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
```
 | 
```
classSummaryIndexRetriever(BaseRetriever):
"""
    Simple retriever for SummaryIndex that returns all nodes.

    Args:
        index (SummaryIndex): The index to retrieve from.

    """

    def__init__(
        self,
        index: SummaryIndex,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
        self._index = index
        super().__init__(
            callback_manager=callback_manager, object_map=object_map, verbose=verbose
        )

    def_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""Retrieve nodes."""
        del query_bundle

        node_ids = self._index.index_struct.nodes
        nodes = self._index.docstore.get_nodes(node_ids)
        return [NodeWithScore(node=node) for node in nodes]

```
 |  
| --- | --- |  
##  BasePGRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.BasePGRetriever "Permanent link")
Bases: 
The base class for property graph retrievers.
By default, will retrieve nodes from the graph store and add source text to the nodes if needed.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `graph_store`  |   |  The graph store to retrieve data from.  |  _required_  |  
|  `include_text`  |  `bool`  |  Whether to include source text in the retrieved nodes. Defaults to True.  |  `True`  |  
|  `include_text_preamble`  |  `Optional[str]`  |  The preamble to include before the source text. Defaults to DEFAULT_PREAMBLE.  |  `DEFAULT_PREAMBLE`  |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/base.py`  
| 
```
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
```
 | 
```
classBasePGRetriever(BaseRetriever):
"""
    The base class for property graph retrievers.

    By default, will retrieve nodes from the graph store and add source text to the nodes if needed.

    Args:
        graph_store (PropertyGraphStore):
            The graph store to retrieve data from.
        include_text (bool, optional):
            Whether to include source text in the retrieved nodes. Defaults to True.
        include_text_preamble (Optional[str], optional):
            The preamble to include before the source text. Defaults to DEFAULT_PREAMBLE.

    """

    def__init__(
        self,
        graph_store: PropertyGraphStore,
        include_text: bool = True,
        include_text_preamble: Optional[str] = DEFAULT_PREAMBLE,
        include_properties: bool = False,
        **kwargs: Any,
    ) -> None:
        self._graph_store = graph_store
        self.include_text = include_text
        self._include_text_preamble = include_text_preamble
        self.include_properties = include_properties
        super().__init__(callback_manager=kwargs.get("callback_manager"))

    def_get_nodes_with_score(
        self, triplets: List[Triplet], scores: Optional[List[float]] = None
    ) -> List[NodeWithScore]:
        results = []
        for i, triplet in enumerate(triplets):
            source_id = triplet[0].properties.get(TRIPLET_SOURCE_KEY, None)
            relationships = {}
            if source_id is not None:
                relationships[NodeRelationship.SOURCE] = RelatedNodeInfo(
                    node_id=source_id
                )

            if self.include_properties:
                text = f"{triplet[0]!s} -> {triplet[1]!s} -> {triplet[2]!s}"
            else:
                text = f"{triplet[0].id} -> {triplet[1].id} -> {triplet[2].id}"
            results.append(
                NodeWithScore(
                    node=TextNode(
                        text=text,
                        relationships=relationships,
                    ),
                    score=1.0 if scores is None else scores[i],
                )
            )

        return results

    def_add_source_text(
        self, retrieved_nodes: List[NodeWithScore], og_node_map: Dict[str, BaseNode]
    ) -> List[NodeWithScore]:
"""Combine retrieved nodes/triplets with their source text, using provided preamble."""
        # map of ref doc id to triplets/retrieved labelled nodes
        graph_node_map: Dict[str, List[str]] = {}
        for node in retrieved_nodes:
            ref_doc_id = node.node.ref_doc_id or ""
            if ref_doc_id not in graph_node_map:
                graph_node_map[ref_doc_id] = []

            graph_node_map[ref_doc_id].append(node.node.get_content())

        result_nodes: List[NodeWithScore] = []
        for node_with_score in retrieved_nodes:
            mapped_node = og_node_map.get(node_with_score.node.ref_doc_id or "", None)

            if mapped_node:
                graph_content = graph_node_map.get(mapped_node.node_id, [])
                if len(graph_content)  0:
                    graph_content_str = "\n".join(graph_content)
                    cur_content = mapped_node.get_content()
                    preamble_text = (
                        self._include_text_preamble
                        if self._include_text_preamble
                        else ""
                    )
                    new_content = (
                        preamble_text + graph_content_str + "\n\n" + cur_content
                    )
                    mapped_node = TextNode(**mapped_node.dict())
                    mapped_node.text = new_content
                result_nodes.append(
                    NodeWithScore(
                        node=mapped_node,
                        score=node_with_score.score,
                    )
                )
            else:
                result_nodes.append(node_with_score)

        return result_nodes

    defadd_source_text(self, nodes: List[NodeWithScore]) -> List[NodeWithScore]:
"""Combine retrieved nodes/triplets with their source text."""
        og_nodes = self._graph_store.get_llama_nodes(
            [x.node.ref_doc_id for x in nodes if x.node.ref_doc_id is not None]
        )
        node_map = {node.node_id: node for node in og_nodes}

        return self._add_source_text(nodes, node_map)

    async defasync_add_source_text(
        self, nodes: List[NodeWithScore]
    ) -> List[NodeWithScore]:
"""Combine retrieved nodes/triplets with their source text."""
        og_nodes = await self._graph_store.aget_llama_nodes(
            [x.node.ref_doc_id for x in nodes if x.node.ref_doc_id is not None]
        )
        og_node_map = {node.node_id: node for node in og_nodes}

        return self._add_source_text(nodes, og_node_map)

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        nodes = self.retrieve_from_graph(query_bundle)
        if self.include_text and nodes:
            nodes = self.add_source_text(nodes)
        return nodes

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        nodes = await self.aretrieve_from_graph(query_bundle)
        if self.include_text and nodes:
            nodes = await self.async_add_source_text(nodes)
        return nodes

    @abstractmethod
    defretrieve_from_graph(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve nodes from the labelled property graph."""
        ...

    @abstractmethod
    async defaretrieve_from_graph(
        self, query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
"""Retrieve nodes from the labelled property graph."""
        ...

```
 |  
| --- | --- |  
###  add_source_text [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.BasePGRetriever.add_source_text "Permanent link")

```
add_source_text(
    nodes: [],
) -> []

```

Combine retrieved nodes/triplets with their source text.
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/base.py`  
| 
```
123
124
125
126
127
128
129
130
```
 | 
```
defadd_source_text(self, nodes: List[NodeWithScore]) -> List[NodeWithScore]:
"""Combine retrieved nodes/triplets with their source text."""
    og_nodes = self._graph_store.get_llama_nodes(
        [x.node.ref_doc_id for x in nodes if x.node.ref_doc_id is not None]
    )
    node_map = {node.node_id: node for node in og_nodes}

    return self._add_source_text(nodes, node_map)

```
 |  
| --- | --- |  
###  async_add_source_text [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.BasePGRetriever.async_add_source_text "Permanent link")

```
async_add_source_text(
    nodes: [],
) -> []

```

Combine retrieved nodes/triplets with their source text.
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/base.py`  
| 
```
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
```
 | 
```
async defasync_add_source_text(
    self, nodes: List[NodeWithScore]
) -> List[NodeWithScore]:
"""Combine retrieved nodes/triplets with their source text."""
    og_nodes = await self._graph_store.aget_llama_nodes(
        [x.node.ref_doc_id for x in nodes if x.node.ref_doc_id is not None]
    )
    og_node_map = {node.node_id: node for node in og_nodes}

    return self._add_source_text(nodes, og_node_map)

```
 |  
| --- | --- |  
###  retrieve_from_graph `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.BasePGRetriever.retrieve_from_graph "Permanent link")

```
retrieve_from_graph(
    query_bundle: ,
) -> []

```

Retrieve nodes from the labelled property graph.
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/base.py`  
| 
```
155
156
157
158
```
 | 
```
@abstractmethod
defretrieve_from_graph(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve nodes from the labelled property graph."""
    ...

```
 |  
| --- | --- |  
###  aretrieve_from_graph `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.BasePGRetriever.aretrieve_from_graph "Permanent link")

```
aretrieve_from_graph(
    query_bundle: ,
) -> []

```

Retrieve nodes from the labelled property graph.
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/base.py`  
| 
```
160
161
162
163
164
165
```
 | 
```
@abstractmethod
async defaretrieve_from_graph(
    self, query_bundle: QueryBundle
) -> List[NodeWithScore]:
"""Retrieve nodes from the labelled property graph."""
    ...

```
 |  
| --- | --- |  
##  CustomPGRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.CustomPGRetriever "Permanent link")
Bases: 
A retriever meant to be easily subclassed to implement custom retrieval logic.
The user only has to implement: - `init` to initialize the retriever and assign any necessary attributes. - `custom_retrieve` to implement the custom retrieval logic. - `aretrieve_custom` (optional) to implement asynchronous retrieval logic.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `graph_store`  |   |  The graph store to retrieve data from.  |  _required_  |  
|  `include_text`  |  `bool`  |  Whether to include text in the retrieved nodes. Only works for kg nodes inserted by LlamaIndex.  |  `False`  |  
|  `**kwargs`  |  Additional keyword arguments passed to init().  |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/custom.py`  
| 
```
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
```
 | 
```
classCustomPGRetriever(BasePGRetriever):
"""
    A retriever meant to be easily subclassed to implement custom retrieval logic.

    The user only has to implement:
    - `init` to initialize the retriever and assign any necessary attributes.
    - `custom_retrieve` to implement the custom retrieval logic.
    - `aretrieve_custom` (optional) to implement asynchronous retrieval logic.

    Args:
        graph_store (PropertyGraphStore):
            The graph store to retrieve data from.
        include_text (bool):
            Whether to include text in the retrieved nodes. Only works for kg nodes
            inserted by LlamaIndex.
        **kwargs:
            Additional keyword arguments passed to init().

    """

    def__init__(
        self,
        graph_store: PropertyGraphStore,
        include_text: bool = False,
        include_properties: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            graph_store=graph_store,
            include_text=include_text,
            include_properties=include_properties,
            **kwargs,
        )
        self.init(**kwargs)

    @property
    defgraph_store(self) -> PropertyGraphStore:
        return self._graph_store

    @abstractmethod
    definit(self, **kwargs: Any) -> None:
"""
        Initialize the retriever.

        Has access to all keyword arguments passed to the retriever, as well as:
        - `self.graph_store`: The graph store to retrieve data from.
        - `self.include_text``: Whether to include text in the retrieved nodes.
        """
        ...

    @abstractmethod
    defcustom_retrieve(self, query_str: str) -> CUSTOM_RETRIEVE_TYPE:
"""
        Retrieve data from the graph store based on the query string.

        Args:
            query_str (str): The query string to retrieve data for.

        Returns:
            The retrieved data. The return type can be one of:
            - str: A single string.
            - List[str]: A list of strings.
            - TextNode: A single TextNode.
            - List[TextNode]: A list of TextNodes.
            - NodeWithScore: A single NodeWithScore.
            - List[NodeWithScore]: A list of NodeWithScores.

        """
        ...

    async defacustom_retrieve(self, query_str: str) -> CUSTOM_RETRIEVE_TYPE:
"""
        Asynchronously retrieve data from the graph store based on the query string.

        Args:
            query_str (str): The query string to retrieve data for.

        Returns:
            The retrieved data. The return type can be one of:
            - str: A single string.
            - List[str]: A list of strings.
            - TextNode: A single TextNode.
            - List[TextNode]: A list of TextNodes.
            - NodeWithScore: A single NodeWithScore.
            - List[NodeWithScore]: A list of NodeWithScores.

        """
        return self.custom_retrieve(query_str)

    def_parse_custom_return_type(
        self, result: CUSTOM_RETRIEVE_TYPE
    ) -> List[NodeWithScore]:
        if isinstance(result, str):
            return [NodeWithScore(node=TextNode(text=result), score=1.0)]
        elif isinstance(result, list):
            if all(isinstance(item, str) for item in result):
                return [
                    NodeWithScore(node=TextNode(text=item), score=1.0)
                    for item in result
                ]
            elif all(isinstance(item, TextNode) for item in result):
                return [NodeWithScore(node=item, score=1.0) for item in result]
            elif all(isinstance(item, NodeWithScore) for item in result):
                return result  # type: ignore
            else:
                raise ValueError(
                    "Invalid return type. All items in the list must be of the same type."
                )
        elif isinstance(result, TextNode):
            return [NodeWithScore(node=result, score=1.0)]
        elif isinstance(result, NodeWithScore):
            return [result]
        else:
            raise ValueError(f"Invalid return type: {type(result)}")

    defretrieve_from_graph(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        result = self.custom_retrieve(query_bundle.query_str)
        return self._parse_custom_return_type(result)

    async defaretrieve_from_graph(
        self, query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        result = await self.acustom_retrieve(query_bundle.query_str)
        return self._parse_custom_return_type(result)

```
 |  
| --- | --- |  
###  init `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.CustomPGRetriever.init "Permanent link")

```
init(**kwargs: ) -> None

```

Initialize the retriever.
Has access to all keyword arguments passed to the retriever, as well as: - `self.graph_store`: The graph store to retrieve data from. - `self.include_text``: Whether to include text in the retrieved nodes.
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/custom.py`  
| 
```
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
```
 | 
```
@abstractmethod
definit(self, **kwargs: Any) -> None:
"""
    Initialize the retriever.

    Has access to all keyword arguments passed to the retriever, as well as:
    - `self.graph_store`: The graph store to retrieve data from.
    - `self.include_text``: Whether to include text in the retrieved nodes.
    """
    ...

```
 |  
| --- | --- |  
###  custom_retrieve `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.CustomPGRetriever.custom_retrieve "Permanent link")

```
custom_retrieve(query_str: ) -> CUSTOM_RETRIEVE_TYPE

```

Retrieve data from the graph store based on the query string.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_str`  |  The query string to retrieve data for.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `CUSTOM_RETRIEVE_TYPE`  |  The retrieved data. The return type can be one of:  |  
|  `CUSTOM_RETRIEVE_TYPE`  | 
  * str: A single string.

 |  
|  `CUSTOM_RETRIEVE_TYPE`  | 
  * List[str]: A list of strings.

 |  
|  `CUSTOM_RETRIEVE_TYPE`  | 
  * TextNode: A single TextNode.

 |  
|  `CUSTOM_RETRIEVE_TYPE`  | 
  * List[TextNode]: A list of TextNodes.

 |  
|  `CUSTOM_RETRIEVE_TYPE`  | 
  * NodeWithScore: A single NodeWithScore.

 |  
|  `CUSTOM_RETRIEVE_TYPE`  | 
  * List[NodeWithScore]: A list of NodeWithScores.

 |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/custom.py`  
| 
```
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
```
 | 
```
@abstractmethod
defcustom_retrieve(self, query_str: str) -> CUSTOM_RETRIEVE_TYPE:
"""
    Retrieve data from the graph store based on the query string.

    Args:
        query_str (str): The query string to retrieve data for.

    Returns:
        The retrieved data. The return type can be one of:
        - str: A single string.
        - List[str]: A list of strings.
        - TextNode: A single TextNode.
        - List[TextNode]: A list of TextNodes.
        - NodeWithScore: A single NodeWithScore.
        - List[NodeWithScore]: A list of NodeWithScores.

    """
    ...

```
 |  
| --- | --- |  
###  acustom_retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.CustomPGRetriever.acustom_retrieve "Permanent link")

```
acustom_retrieve(query_str: ) -> CUSTOM_RETRIEVE_TYPE

```

Asynchronously retrieve data from the graph store based on the query string.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_str`  |  The query string to retrieve data for.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `CUSTOM_RETRIEVE_TYPE`  |  The retrieved data. The return type can be one of:  |  
|  `CUSTOM_RETRIEVE_TYPE`  | 
  * str: A single string.

 |  
|  `CUSTOM_RETRIEVE_TYPE`  | 
  * List[str]: A list of strings.

 |  
|  `CUSTOM_RETRIEVE_TYPE`  | 
  * TextNode: A single TextNode.

 |  
|  `CUSTOM_RETRIEVE_TYPE`  | 
  * List[TextNode]: A list of TextNodes.

 |  
|  `CUSTOM_RETRIEVE_TYPE`  | 
  * NodeWithScore: A single NodeWithScore.

 |  
|  `CUSTOM_RETRIEVE_TYPE`  | 
  * List[NodeWithScore]: A list of NodeWithScores.

 |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/custom.py`  
| 
```
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
```
 | 
```
async defacustom_retrieve(self, query_str: str) -> CUSTOM_RETRIEVE_TYPE:
"""
    Asynchronously retrieve data from the graph store based on the query string.

    Args:
        query_str (str): The query string to retrieve data for.

    Returns:
        The retrieved data. The return type can be one of:
        - str: A single string.
        - List[str]: A list of strings.
        - TextNode: A single TextNode.
        - List[TextNode]: A list of TextNodes.
        - NodeWithScore: A single NodeWithScore.
        - List[NodeWithScore]: A list of NodeWithScores.

    """
    return self.custom_retrieve(query_str)

```
 |  
| --- | --- |  
##  CypherTemplateRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.CypherTemplateRetriever "Permanent link")
Bases: 
A Cypher retriever that fills in params for a cypher query using an LLM.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `graph_store`  |   |  The graph store to retrieve data from.  |  _required_  |  
|  `output_cls`  |  `Type[BaseModel]`  |  The output class to use for the LLM. Should contain the params needed for the cypher query.  |  _required_  |  
|  `cypher_query`  |  The cypher query to use, with templated params.  |  _required_  |  
|  `llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.LLM\)")]`  |  The language model to use. Defaults to Settings.llm.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/cypher_template.py`  
| 
```
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
```
 | 
```
classCypherTemplateRetriever(BasePGRetriever):
"""
    A Cypher retriever that fills in params for a cypher query using an LLM.

    Args:
        graph_store (PropertyGraphStore):
            The graph store to retrieve data from.
        output_cls (Type[BaseModel]):
            The output class to use for the LLM.
            Should contain the params needed for the cypher query.
        cypher_query (str):
            The cypher query to use, with templated params.
        llm (Optional[LLM], optional):
            The language model to use. Defaults to Settings.llm.

    """

    def__init__(
        self,
        graph_store: PropertyGraphStore,
        output_cls: Type[BaseModel],
        cypher_query: str,
        llm: Optional[LLM] = None,
        **kwargs: Any,
    ) -> None:
        if not graph_store.supports_structured_queries:
            raise ValueError(
                "The provided graph store does not support cypher queries."
            )

        self.llm = llm or Settings.llm
        # Explicit type hint to suppress:
        #   `Expected type '_SpecialForm[BaseModel]', got 'Type[BaseModel]' instead`
        self.output_cls: Type[BaseModel] = output_cls
        self.cypher_query = cypher_query

        super().__init__(
            graph_store=graph_store, include_text=False, include_properties=False
        )

    defretrieve_from_graph(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        question = query_bundle.query_str

        response = self.llm.structured_predict(
            self.output_cls, PromptTemplate(question)
        )

        cypher_response = self._graph_store.structured_query(
            self.cypher_query,
            param_map=response.model_dump(),
        )

        return [
            NodeWithScore(
                node=TextNode(
                    text=str(cypher_response),
                ),
                score=1.0,
            )
        ]

    async defaretrieve_from_graph(
        self, query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        question = query_bundle.query_str

        response = await self.llm.astructured_predict(
            self.output_cls, PromptTemplate(question)
        )

        cypher_response = await self._graph_store.astructured_query(
            self.cypher_query,
            param_map=response.model_dump(),
        )

        return [
            NodeWithScore(
                node=TextNode(
                    text=str(cypher_response),
                ),
                score=1.0,
            )
        ]

```
 |  
| --- | --- |  
##  LLMSynonymRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.LLMSynonymRetriever "Permanent link")
Bases: 
A retriever that uses a language model to expand a query with synonyms. The synonyms are then used to retrieve nodes from a property graph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `graph_store`  |   |  The graph store to retrieve data from.  |  _required_  |  
|  `include_text`  |  `bool`  |  Whether to include source text in the retrieved nodes. Defaults to True.  |  `True`  |  
|  `synonym_prompt`  |  `Union[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)"), str]`  |  The template to use for the synonym expansion query. Defaults to DEFAULT_SYNONYM_EXPAND_TEMPLATE.  |  `DEFAULT_SYNONYM_EXPAND_TEMPLATE`  |  
|  `max_keywords`  |  The maximum number of synonyms to generate. Defaults to 10.  |  
|  `path_depth`  |  The depth of the path to retrieve for each node. Defaults to 1 (i.e. a triple).  |  
|  `output_parsing_fn`  |  `Optional[callable]`  |  A callable function to parse the output of the language model. Defaults to None.  |  `None`  |  
|  `llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.llm.LLM\)")]`  |  The language model to use. Defaults to Settings.llm.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/llm_synonym.py`  
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
```
 | 
```
classLLMSynonymRetriever(BasePGRetriever):
"""
    A retriever that uses a language model to expand a query with synonyms.
    The synonyms are then used to retrieve nodes from a property graph.

    Args:
        graph_store (PropertyGraphStore):
            The graph store to retrieve data from.
        include_text (bool, optional):
            Whether to include source text in the retrieved nodes. Defaults to True.
        synonym_prompt (Union[BasePromptTemplate, str], optional):
            The template to use for the synonym expansion query.
            Defaults to DEFAULT_SYNONYM_EXPAND_TEMPLATE.
        max_keywords (int, optional):
            The maximum number of synonyms to generate. Defaults to 10.
        path_depth (int, optional):
            The depth of the path to retrieve for each node. Defaults to 1 (i.e. a triple).
        output_parsing_fn (Optional[callable], optional):
            A callable function to parse the output of the language model. Defaults to None.
        llm (Optional[LLM], optional):
            The language model to use. Defaults to Settings.llm.

    """

    def__init__(
        self,
        graph_store: PropertyGraphStore,
        include_text: bool = True,
        include_properties: bool = False,
        synonym_prompt: Union[
            BasePromptTemplate, str
        ] = DEFAULT_SYNONYM_EXPAND_TEMPLATE,
        max_keywords: int = 10,
        path_depth: int = 1,
        limit: int = 30,
        output_parsing_fn: Optional[Callable] = None,
        llm: Optional[LLM] = None,
        **kwargs: Any,
    ) -> None:
        self._llm = llm or Settings.llm
        if isinstance(synonym_prompt, str):
            synonym_prompt = PromptTemplate(synonym_prompt)
        self._synonym_prompt = synonym_prompt
        self._output_parsing_fn = output_parsing_fn
        self._max_keywords = max_keywords
        self._path_depth = path_depth
        self._limit = limit
        super().__init__(
            graph_store=graph_store,
            include_text=include_text,
            include_properties=include_properties,
            **kwargs,
        )

    def_parse_llm_output(self, output: str) -> List[str]:
        if self._output_parsing_fn:
            matches = self._output_parsing_fn(output)
        else:
            matches = output.strip().split("^")

        # capitalize to normalize with ingestion
        return [x.strip().capitalize() for x in matches if x.strip()]

    def_prepare_matches(
        self, matches: List[str], limit: Optional[int] = None
    ) -> List[NodeWithScore]:
        kg_nodes = self._graph_store.get(ids=matches)
        triplets = self._graph_store.get_rel_map(
            kg_nodes,
            depth=self._path_depth,
            limit=limit or self._limit,
            ignore_rels=[KG_SOURCE_REL],
        )

        return self._get_nodes_with_score(triplets)

    async def_aprepare_matches(
        self, matches: List[str], limit: Optional[int] = None
    ) -> List[NodeWithScore]:
        kg_nodes = await self._graph_store.aget(ids=matches)
        triplets = await self._graph_store.aget_rel_map(
            kg_nodes,
            depth=self._path_depth,
            limit=limit or self._limit,
            ignore_rels=[KG_SOURCE_REL],
        )

        return self._get_nodes_with_score(triplets)

    defretrieve_from_graph(
        self, query_bundle: QueryBundle, limit: Optional[int] = None
    ) -> List[NodeWithScore]:
        response = self._llm.predict(
            self._synonym_prompt,
            query_str=query_bundle.query_str,
            max_keywords=self._max_keywords,
        )
        matches = self._parse_llm_output(response)

        return self._prepare_matches(matches, limit=limit or self._limit)

    async defaretrieve_from_graph(
        self, query_bundle: QueryBundle, limit: Optional[int] = None
    ) -> List[NodeWithScore]:
        response = await self._llm.apredict(
            self._synonym_prompt,
            query_str=query_bundle.query_str,
            max_keywords=self._max_keywords,
        )
        matches = self._parse_llm_output(response)

        return await self._aprepare_matches(matches, limit=limit or self._limit)

```
 |  
| --- | --- |  
##  PGRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.PGRetriever "Permanent link")
Bases: 
A retriever that uses multiple sub-retrievers to retrieve nodes from a property graph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sub_retrievers`  |  `List[BasePGRetriever[](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.BasePGRetriever "BasePGRetriever \(llama_index.core.indices.property_graph.sub_retrievers.base.BasePGRetriever\)")]`  |  The sub-retrievers to use.  |  _required_  |  
|  `num_workers`  |  The number of workers to use for async retrieval. Defaults to 4.  |  
|  `use_async`  |  `bool`  |  Whether to use async retrieval. Defaults to True.  |  `True`  |  
|  `show_progress`  |  `bool`  |  Whether to show progress bars. Defaults to False.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/retriever.py`  
| 
```
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
```
 | 
```
classPGRetriever(BaseRetriever):
"""
    A retriever that uses multiple sub-retrievers to retrieve nodes from a property graph.

    Args:
        sub_retrievers (List[BasePGRetriever]):
            The sub-retrievers to use.
        num_workers (int, optional):
            The number of workers to use for async retrieval. Defaults to 4.
        use_async (bool, optional):
            Whether to use async retrieval. Defaults to True.
        show_progress (bool, optional):
            Whether to show progress bars. Defaults to False.

    """

    def__init__(
        self,
        sub_retrievers: List[BasePGRetriever],
        num_workers: int = 4,
        use_async: bool = True,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> None:
        self.sub_retrievers = sub_retrievers
        self.use_async = use_async
        self.num_workers = num_workers
        self.show_progress = show_progress

    def_deduplicate(self, nodes: List[NodeWithScore]) -> List[NodeWithScore]:
        seen = set()
        deduped = []
        for node in nodes:
            if node.text not in seen:
                deduped.append(node)
                seen.add(node.text)

        return deduped

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        results = []
        if self.use_async:
            return asyncio_run(self._aretrieve(query_bundle))

        for sub_retriever in tqdm(self.sub_retrievers, disable=not self.show_progress):
            results.extend(sub_retriever.retrieve(query_bundle))

        return self._deduplicate(results)

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        tasks = []
        for sub_retriever in self.sub_retrievers:
            tasks.append(sub_retriever.aretrieve(query_bundle))

        async_results = await run_jobs(
            tasks, workers=self.num_workers, show_progress=self.show_progress
        )

        # flatten the results
        return self._deduplicate([node for nodes in async_results for node in nodes])

```
 |  
| --- | --- |  
##  TextToCypherRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.TextToCypherRetriever "Permanent link")
Bases: 
A Text-to-Cypher retriever that uses a language model to generate Cypher queries.
NOTE: Executing arbitrary cypher has its risks. Ensure you take the needed measures (read-only roles, sandboxed env, etc.) to ensure safe usage in a production environment.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `graph_store`  |   |  The graph store to retrieve data from.  |  _required_  |  
|  `llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.LLM\)")]`  |  The language model to use. Defaults to Settings.llm.  |  `None`  |  
|  `text_to_cypher_template`  |  `Optional[Union[PromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.PromptTemplate "PromptTemplate \(llama_index.core.prompts.PromptTemplate\)"), str]]`  |  The template to use for the text-to-cypher query. Defaults to None.  |  `None`  |  
|  `response_template`  |  `Optional[str]`  |  The template to use for the response. Defaults to None.  |  `None`  |  
|  `cypher_validator`  |  `Optional[callable]`  |  A callable function to validate the generated Cypher query. Defaults to None.  |  `None`  |  
|  `allowed_query_fields`  |  `Optional[List[str]]`  |  The fields to allow in the query output. Defaults to ["text", "label", "type"].  |  _required_  |  
|  `include_raw_response_as_metadata`  |  `Optional[bool]`  |  If True this will add the query and raw response data to the metadata property. Defaults to False.  |  `False`  |  
|  `summarize_response`  |  `Optional[bool]`  |  If True this will run the response through the provided LLM to create a more human readable response, If False this uses the provided or default response_template. Defaults to False.  |  `False`  |  
|  `summarization_template`  |  `Optional[str]`  |  The template to use for summarizing the response. Defaults to None.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/text_to_cypher.py`  
| 
```
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
```
 | 
```
classTextToCypherRetriever(BasePGRetriever):
"""
    A Text-to-Cypher retriever that uses a language model to generate Cypher queries.

    NOTE: Executing arbitrary cypher has its risks. Ensure you take the needed measures
    (read-only roles, sandboxed env, etc.) to ensure safe usage in a production environment.

    Args:
        graph_store (PropertyGraphStore):
            The graph store to retrieve data from.
        llm (Optional[LLM], optional):
            The language model to use. Defaults to Settings.llm.
        text_to_cypher_template (Optional[Union[PromptTemplate, str]], optional):
            The template to use for the text-to-cypher query. Defaults to None.
        response_template (Optional[str], optional):
            The template to use for the response. Defaults to None.
        cypher_validator (Optional[callable], optional):
            A callable function to validate the generated Cypher query. Defaults to None.
        allowed_query_fields (Optional[List[str]], optional):
            The fields to allow in the query output. Defaults to ["text", "label", "type"].
        include_raw_response_as_metadata (Optional[bool], optional):
            If True this will add the query and raw response data to the metadata property. Defaults to False.
        summarize_response (Optional[bool], optional):
            If True this will run the response through the provided LLM to create a more human readable
            response, If False this uses the provided or default response_template. Defaults to False.
        summarization_template (Optional[str], optional):
            The template to use for summarizing the response. Defaults to None.

    """

    def__init__(
        self,
        graph_store: PropertyGraphStore,
        llm: Optional[LLM] = None,
        text_to_cypher_template: Optional[Union[PromptTemplate, str]] = None,
        response_template: Optional[str] = None,
        cypher_validator: Optional[Callable] = None,
        allowed_output_fields: Optional[List[str]] = None,
        include_raw_response_as_metadata: Optional[bool] = False,
        summarize_response: Optional[bool] = False,
        summarization_template: Optional[Union[PromptTemplate, str]] = None,
        **kwargs: Any,
    ) -> None:
        if not graph_store.supports_structured_queries:
            raise ValueError(
                "The provided graph store does not support cypher queries."
            )

        self.llm = llm or Settings.llm

        if isinstance(text_to_cypher_template, str):
            text_to_cypher_template = PromptTemplate(text_to_cypher_template)

        if isinstance(summarization_template, str):
            summarization_template = PromptTemplate(summarization_template)

        self.response_template = response_template or DEFAULT_RESPONSE_TEMPLATE
        self.text_to_cypher_template = (
            text_to_cypher_template or graph_store.text_to_cypher_template
        )
        self.cypher_validator = cypher_validator
        self.allowed_output_fields = allowed_output_fields
        self.include_raw_response_as_metadata = include_raw_response_as_metadata
        self.summarize_response = summarize_response
        self.summarization_template = summarization_template or DEFAULT_SUMMARY_TEMPLATE

        super().__init__(
            graph_store=graph_store, include_text=False, include_properties=False
        )

    def_parse_generated_cypher(self, cypher_query: str) -> str:
        if self.cypher_validator is not None:
            return self.cypher_validator(cypher_query)
        return cypher_query

    def_clean_query_output(self, query_output: Any) -> Any:
"""Iterate the cypher response, looking for the allowed fields."""
        if isinstance(query_output, dict):
            filtered_dict = {}
            for key, value in query_output.items():
                if (
                    self.allowed_output_fields is None
                    or key in self.allowed_output_fields
                ):
                    filtered_dict[key] = value
                elif isinstance(value, (dict, list)):
                    filtered_value = self._clean_query_output(value)
                    if filtered_value:
                        filtered_dict[key] = filtered_value
            return filtered_dict
        elif isinstance(query_output, list):
            filtered_list = []
            for item in query_output:
                filtered_item = self._clean_query_output(item)
                if filtered_item:
                    filtered_list.append(filtered_item)
            return filtered_list

        return None

    defretrieve_from_graph(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        schema = self._graph_store.get_schema_str()
        question = query_bundle.query_str

        response = self.llm.predict(
            self.text_to_cypher_template,
            schema=schema,
            question=question,
        )

        parsed_cypher_query = self._parse_generated_cypher(response)

        query_output = self._graph_store.structured_query(parsed_cypher_query)

        cleaned_query_output = self._clean_query_output(query_output)

        if self.summarize_response:
            summarized_response = self.llm.predict(
                self.summarization_template,
                context=str(cleaned_query_output),
                question=parsed_cypher_query,
            )
            node_text = summarized_response
        else:
            node_text = self.response_template.format(
                query=parsed_cypher_query,
                response=str(cleaned_query_output),
            )

        return [
            NodeWithScore(
                node=TextNode(
                    text=node_text,
                    metadata=(
                        {"query": parsed_cypher_query, "response": cleaned_query_output}
                        if self.include_raw_response_as_metadata
                        else {}
                    ),
                ),
                score=1.0,
            )
        ]

    async defaretrieve_from_graph(
        self, query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        schema = await self._graph_store.aget_schema_str()
        question = query_bundle.query_str

        response = await self.llm.apredict(
            self.text_to_cypher_template,
            schema=schema,
            question=question,
        )

        parsed_cypher_query = self._parse_generated_cypher(response)

        query_output = await self._graph_store.astructured_query(parsed_cypher_query)

        cleaned_query_output = self._clean_query_output(query_output)

        if self.summarize_response:
            summarized_response = await self.llm.apredict(
                self.summarization_template,
                context=str(cleaned_query_output),
                question=parsed_cypher_query,
            )
            node_text = summarized_response
        else:
            node_text = self.response_template.format(
                query=parsed_cypher_query,
                response=str(cleaned_query_output),
            )

        return [
            NodeWithScore(
                node=TextNode(
                    text=node_text,
                    metadata=(
                        {"query": parsed_cypher_query, "response": cleaned_query_output}
                        if self.include_raw_response_as_metadata
                        else {}
                    ),
                ),
                score=1.0,
            )
        ]

```
 |  
| --- | --- |  
##  VectorContextRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.VectorContextRetriever "Permanent link")
Bases: 
A retriever that uses a vector store to retrieve nodes based on a query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `graph_store`  |   |  The graph store to retrieve data from.  |  _required_  |  
|  `include_text`  |  `bool`  |  Whether to include source text in the retrieved nodes. Defaults to True.  |  `True`  |  
|  `embed_model`  |  `Optional[BaseEmbedding[](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding "BaseEmbedding \(llama_index.core.base.embeddings.base.BaseEmbedding\)")]`  |  The embedding model to use. Defaults to Settings.embed_model.  |  `None`  |  
|  `vector_store`  |  `Optional[BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)")]`  |  The vector store to use. Defaults to None. Should be supplied if the graph store does not support vector queries.  |  `None`  |  
|  `similarity_top_k`  |  The number of top similar kg nodes to retrieve. Defaults to 4.  |  
|  `path_depth`  |  The depth of the path to retrieve for each node. Defaults to 1 (i.e. a triple).  |  
|  `similarity_score`  |  `float`  |  The minimum similarity score to retrieve the nodes. Defaults to None.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/sub_retrievers/vector.py`  
| 
```
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
```
 | 
```
classVectorContextRetriever(BasePGRetriever):
"""
    A retriever that uses a vector store to retrieve nodes based on a query.

    Args:
        graph_store (PropertyGraphStore):
            The graph store to retrieve data from.
        include_text (bool, optional):
            Whether to include source text in the retrieved nodes. Defaults to True.
        embed_model (Optional[BaseEmbedding], optional):
            The embedding model to use. Defaults to Settings.embed_model.
        vector_store (Optional[BasePydanticVectorStore], optional):
            The vector store to use. Defaults to None.
            Should be supplied if the graph store does not support vector queries.
        similarity_top_k (int, optional):
            The number of top similar kg nodes to retrieve. Defaults to 4.
        path_depth (int, optional):
            The depth of the path to retrieve for each node. Defaults to 1 (i.e. a triple).
        similarity_score (float, optional):
            The minimum similarity score to retrieve the nodes. Defaults to None.

    """

    def__init__(
        self,
        graph_store: PropertyGraphStore,
        include_text: bool = True,
        include_properties: bool = False,
        embed_model: Optional[BaseEmbedding] = None,
        vector_store: Optional[BasePydanticVectorStore] = None,
        similarity_top_k: int = 4,
        path_depth: int = 1,
        limit: int = 30,
        similarity_score: Optional[float] = None,
        filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> None:
        self._retriever_kwargs = self._filter_vector_store_query_kwargs(kwargs or {})
        self._embed_model = embed_model or Settings.embed_model
        self._similarity_top_k = similarity_top_k
        self._vector_store = vector_store
        self._path_depth = path_depth
        self._limit = limit
        self._similarity_score = similarity_score
        self._filters = filters

        super().__init__(
            graph_store=graph_store,
            include_text=include_text,
            include_properties=include_properties,
            **kwargs,
        )

    @staticmethod
    def_get_valid_vector_store_params() -> Set[str]:
        return {x.name for x in dataclasses.fields(VectorStoreQuery)}

    def_filter_vector_store_query_kwargs(
        self, kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        valid_params = self._get_valid_vector_store_params()
        return {k: v for k, v in kwargs.items() if k in valid_params}

    def_get_vector_store_query(self, query_bundle: QueryBundle) -> VectorStoreQuery:
        if query_bundle.embedding is None:
            query_bundle.embedding = self._embed_model.get_agg_embedding_from_queries(
                query_bundle.embedding_strs
            )

        return VectorStoreQuery(
            query_embedding=query_bundle.embedding,
            similarity_top_k=self._similarity_top_k,
            filters=self._filters,
            **self._retriever_kwargs,
        )

    def_get_kg_ids(self, kg_nodes: Sequence[BaseNode]) -> List[str]:
"""Backward compatibility method to get kg_ids from kg_nodes."""
        return [node.metadata.get(VECTOR_SOURCE_KEY, node.id_) for node in kg_nodes]

    async def_aget_vector_store_query(
        self, query_bundle: QueryBundle
    ) -> VectorStoreQuery:
        if query_bundle.embedding is None:
            query_bundle.embedding = (
                await self._embed_model.aget_agg_embedding_from_queries(
                    query_bundle.embedding_strs
                )
            )

        return VectorStoreQuery(
            query_embedding=query_bundle.embedding,
            similarity_top_k=self._similarity_top_k,
            filters=self._filters,
            **self._retriever_kwargs,
        )

    defretrieve_from_graph(
        self, query_bundle: QueryBundle, limit: Optional[int] = None
    ) -> List[NodeWithScore]:
        vector_store_query = self._get_vector_store_query(query_bundle)

        triplets = []
        kg_ids = []
        new_scores = []
        if self._graph_store.supports_vector_queries:
            result = self._graph_store.vector_query(vector_store_query)
            if len(result) != 2:
                raise ValueError("No nodes returned by vector_query")
            kg_nodes, scores = result

            kg_ids = [node.id for node in kg_nodes]
            triplets = self._graph_store.get_rel_map(
                kg_nodes,
                depth=self._path_depth,
                limit=limit or self._limit,
                ignore_rels=[KG_SOURCE_REL],
            )

        elif self._vector_store is not None:
            query_result = self._vector_store.query(vector_store_query)
            if query_result.nodes is not None and query_result.similarities is not None:
                kg_ids = self._get_kg_ids(query_result.nodes)
                scores = query_result.similarities
                kg_nodes = self._graph_store.get(ids=kg_ids)
                triplets = self._graph_store.get_rel_map(
                    kg_nodes,
                    depth=self._path_depth,
                    limit=limit or self._limit,
                    ignore_rels=[KG_SOURCE_REL],
                )

            elif query_result.ids is not None and query_result.similarities is not None:
                kg_ids = query_result.ids
                scores = query_result.similarities
                kg_nodes = self._graph_store.get(ids=kg_ids)
                triplets = self._graph_store.get_rel_map(
                    kg_nodes,
                    depth=self._path_depth,
                    limit=limit or self._limit,
                    ignore_rels=[KG_SOURCE_REL],
                )

        for triplet in triplets:
            score1 = (
                scores[kg_ids.index(triplet[0].id)] if triplet[0].id in kg_ids else 0.0
            )
            score2 = (
                scores[kg_ids.index(triplet[2].id)] if triplet[2].id in kg_ids else 0.0
            )
            new_scores.append(max(score1, score2))

        assert len(triplets) == len(new_scores)

        # filter by similarity score
        if self._similarity_score:
            filtered_data = [
                (triplet, score)
                for triplet, score in zip(triplets, new_scores)
                if score >= self._similarity_score
            ]
            # sort by score
            top_k = sorted(filtered_data, key=lambda x: x[1], reverse=True)
        else:
            # sort by score
            top_k = sorted(zip(triplets, new_scores), key=lambda x: x[1], reverse=True)

        return self._get_nodes_with_score([x[0] for x in top_k], [x[1] for x in top_k])

    async defaretrieve_from_graph(
        self, query_bundle: QueryBundle, limit: Optional[int] = None
    ) -> List[NodeWithScore]:
        vector_store_query = await self._aget_vector_store_query(query_bundle)

        triplets = []
        kg_ids = []
        new_scores = []
        if self._graph_store.supports_vector_queries:
            result = await self._graph_store.avector_query(vector_store_query)
            if len(result) != 2:
                raise ValueError("No nodes returned by vector_query")

            kg_nodes, scores = result
            kg_ids = [node.id for node in kg_nodes]
            triplets = await self._graph_store.aget_rel_map(
                kg_nodes,
                depth=self._path_depth,
                limit=limit or self._limit,
                ignore_rels=[KG_SOURCE_REL],
            )

        elif self._vector_store is not None:
            query_result = await self._vector_store.aquery(vector_store_query)
            if query_result.nodes is not None and query_result.similarities is not None:
                kg_ids = self._get_kg_ids(query_result.nodes)
                scores = query_result.similarities
                kg_nodes = await self._graph_store.aget(ids=kg_ids)
                triplets = await self._graph_store.aget_rel_map(
                    kg_nodes,
                    depth=self._path_depth,
                    limit=limit or self._limit,
                    ignore_rels=[KG_SOURCE_REL],
                )

            elif query_result.ids is not None and query_result.similarities is not None:
                kg_ids = query_result.ids
                scores = query_result.similarities
                kg_nodes = await self._graph_store.aget(ids=kg_ids)
                triplets = await self._graph_store.aget_rel_map(
                    kg_nodes,
                    depth=self._path_depth,
                    limit=limit or self._limit,
                    ignore_rels=[KG_SOURCE_REL],
                )

        for triplet in triplets:
            score1 = (
                scores[kg_ids.index(triplet[0].id)] if triplet[0].id in kg_ids else 0.0
            )
            score2 = (
                scores[kg_ids.index(triplet[2].id)] if triplet[2].id in kg_ids else 0.0
            )
            new_scores.append(max(score1, score2))

        assert len(triplets) == len(new_scores)

        # filter by similarity score
        if self._similarity_score:
            filtered_data = [
                (triplet, score)
                for triplet, score in zip(triplets, new_scores)
                if score >= self._similarity_score
            ]
            # sort by score
            top_k = sorted(filtered_data, key=lambda x: x[1], reverse=True)
        else:
            # sort by score
            top_k = sorted(zip(triplets, new_scores), key=lambda x: x[1], reverse=True)

        return self._get_nodes_with_score([x[0] for x in top_k], [x[1] for x in top_k])

```
 |  
| --- | --- |  
##  NLSQLRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.NLSQLRetriever "Permanent link")
Bases: , `PromptMixin`
Text-to-SQL Retriever.
Retrieves via text.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sql_database`  |   |  SQL database.  |  _required_  |  
|  `text_to_sql_prompt`  |   |  Prompt template for text-to-sql. Defaults to DEFAULT_TEXT_TO_SQL_PROMPT.  |  `None`  |  
|  `context_query_kwargs`  |  `dict`  |  Mapping from table name to context query. Defaults to None.  |  `None`  |  
|  `tables`  |  `Union[List[str], List[Table]]`  |  List of table names or Table objects.  |  `None`  |  
|  `table_retriever`  |  `ObjectRetriever[](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.ObjectRetriever "ObjectRetriever \(llama_index.core.objects.base.ObjectRetriever\)")[SQLTableSchema[](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.SQLTableSchema "SQLTableSchema \(llama_index.core.objects.table_node_mapping.SQLTableSchema\)")]`  |  Object retriever for SQLTableSchema objects. Defaults to None.  |  `None`  |  
|  `rows_retriever`  |  `Dict[str, VectorIndexRetriever]`  |  a mapping between table name and a vector index retriever of its rows. Defaults to None.  |  _required_  |  
|  `context_str_prefix`  |  Prefix for context string. Defaults to None.  |  `None`  |  
|  `return_raw`  |  `bool`  |  Whether to return plain-text dump of SQL results, or parsed into Nodes.  |  `True`  |  
|  `handle_sql_errors`  |  `bool`  |  Whether to handle SQL errors. Defaults to True.  |  `True`  |  
|  `sql_only (bool) `  |  Whether to get only sql and not the sql query result. Default to False.  |  _required_  |  
|  `llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.llm.LLM\)")]`  |  Language model to use.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/indices/struct_store/sql_retriever.py`  
| 
```
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
```
 | 
```
classNLSQLRetriever(BaseRetriever, PromptMixin):
"""
    Text-to-SQL Retriever.

    Retrieves via text.

    Args:
        sql_database (SQLDatabase): SQL database.
        text_to_sql_prompt (BasePromptTemplate): Prompt template for text-to-sql.
            Defaults to DEFAULT_TEXT_TO_SQL_PROMPT.
        context_query_kwargs (dict): Mapping from table name to context query.
            Defaults to None.
        tables (Union[List[str], List[Table]]): List of table names or Table objects.
        table_retriever (ObjectRetriever[SQLTableSchema]): Object retriever for
            SQLTableSchema objects. Defaults to None.
        rows_retriever (Dict[str, VectorIndexRetriever]): a mapping between table name and
            a vector index retriever of its rows. Defaults to None.
        context_str_prefix (str): Prefix for context string. Defaults to None.
        return_raw (bool): Whether to return plain-text dump of SQL results, or parsed into Nodes.
        handle_sql_errors (bool): Whether to handle SQL errors. Defaults to True.
        sql_only (bool) : Whether to get only sql and not the sql query result.
            Default to False.
        llm (Optional[LLM]): Language model to use.

    """

    def__init__(
        self,
        sql_database: SQLDatabase,
        text_to_sql_prompt: Optional[BasePromptTemplate] = None,
        context_query_kwargs: Optional[dict] = None,
        tables: Optional[Union[List[str], List[Table]]] = None,
        table_retriever: Optional[ObjectRetriever[SQLTableSchema]] = None,
        rows_retrievers: Optional[dict[str, BaseRetriever]] = None,
        cols_retrievers: Optional[dict[str, dict[str, BaseRetriever]]] = None,
        context_str_prefix: Optional[str] = None,
        sql_parser_mode: SQLParserMode = SQLParserMode.DEFAULT,
        llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        return_raw: bool = True,
        handle_sql_errors: bool = True,
        sql_only: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._sql_retriever = SQLRetriever(sql_database, return_raw=return_raw)
        self._sql_database = sql_database
        self._get_tables = self._load_get_tables_fn(
            sql_database, tables, context_query_kwargs, table_retriever
        )
        self._context_str_prefix = context_str_prefix
        self._llm = llm or Settings.llm
        self._text_to_sql_prompt = text_to_sql_prompt or DEFAULT_TEXT_TO_SQL_PROMPT
        self._sql_parser_mode = sql_parser_mode

        embed_model = embed_model or Settings.embed_model
        self._sql_parser = self._load_sql_parser(sql_parser_mode, embed_model)
        self._handle_sql_errors = handle_sql_errors
        self._sql_only = sql_only
        self._verbose = verbose

        # To retrieve relevant rows or cols from each retrieved table
        self._rows_retrievers = rows_retrievers
        self._cols_retrievers = cols_retrievers
        super().__init__(
            callback_manager=callback_manager or Settings.callback_manager,
            verbose=verbose,
        )

    def_get_prompts(self) -> Dict[str, Any]:
"""Get prompts."""
        return {
            "text_to_sql_prompt": self._text_to_sql_prompt,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "text_to_sql_prompt" in prompts:
            self._text_to_sql_prompt = prompts["text_to_sql_prompt"]

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt modules."""
        return {}

    def_load_sql_parser(
        self, sql_parser_mode: SQLParserMode, embed_model: BaseEmbedding
    ) -> BaseSQLParser:
"""Load SQL parser."""
        if sql_parser_mode == SQLParserMode.DEFAULT:
            return DefaultSQLParser()
        elif sql_parser_mode == SQLParserMode.PGVECTOR:
            return PGVectorSQLParser(embed_model=embed_model)
        else:
            raise ValueError(f"Unknown SQL parser mode: {sql_parser_mode}")

    def_load_get_tables_fn(
        self,
        sql_database: SQLDatabase,
        tables: Optional[Union[List[str], List[Table]]] = None,
        context_query_kwargs: Optional[dict] = None,
        table_retriever: Optional[ObjectRetriever[SQLTableSchema]] = None,
    ) -> Callable[[str], List[SQLTableSchema]]:
"""Load get_tables function."""
        context_query_kwargs = context_query_kwargs or {}
        if table_retriever is not None:
            return lambda query_str: cast(Any, table_retriever).retrieve(query_str)
        else:
            if tables is not None:
                table_names: List[str] = [
                    t.name if isinstance(t, Table) else t for t in tables
                ]
            else:
                table_names = list(sql_database.get_usable_table_names())
            context_strs = [context_query_kwargs.get(t, None) for t in table_names]
            table_schemas = [
                SQLTableSchema(table_name=t, context_str=c)
                for t, c in zip(table_names, context_strs)
            ]
            return lambda _: table_schemas

    defretrieve_with_metadata(
        self, str_or_query_bundle: QueryType
    ) -> Tuple[List[NodeWithScore], Dict]:
"""Retrieve with metadata."""
        if isinstance(str_or_query_bundle, str):
            query_bundle = QueryBundle(str_or_query_bundle)
        else:
            query_bundle = str_or_query_bundle
        table_desc_str = self._get_table_context(query_bundle)
        logger.info(f"> Table desc str: {table_desc_str}")
        if self._verbose:
            print(f"> Table desc str: {table_desc_str}")

        response_str = self._llm.predict(
            self._text_to_sql_prompt,
            query_str=query_bundle.query_str,
            schema=table_desc_str,
            dialect=self._sql_database.dialect,
        )

        sql_query_str = self._sql_parser.parse_response_to_sql(
            response_str, query_bundle
        )
        # assume that it's a valid SQL query
        logger.debug(f"> Predicted SQL query: {sql_query_str}")
        if self._verbose:
            print(f"> Predicted SQL query: {sql_query_str}")

        if self._sql_only:
            sql_only_node = TextNode(text=f"{sql_query_str}")
            retrieved_nodes = [NodeWithScore(node=sql_only_node)]
            metadata = {"result": sql_query_str}
        else:
            try:
                retrieved_nodes, metadata = self._sql_retriever.retrieve_with_metadata(
                    sql_query_str
                )
            except BaseException as e:
                # if handle_sql_errors is True, then return error message
                if self._handle_sql_errors:
                    err_node = TextNode(text=f"Error: {e!s}")
                    retrieved_nodes = [NodeWithScore(node=err_node)]
                    metadata = {}
                else:
                    raise

        return retrieved_nodes, {"sql_query": sql_query_str, **metadata}

    async defaretrieve_with_metadata(
        self, str_or_query_bundle: QueryType
    ) -> Tuple[List[NodeWithScore], Dict]:
"""Async retrieve with metadata."""
        if isinstance(str_or_query_bundle, str):
            query_bundle = QueryBundle(str_or_query_bundle)
        else:
            query_bundle = str_or_query_bundle
        table_desc_str = self._get_table_context(query_bundle)
        logger.info(f"> Table desc str: {table_desc_str}")

        response_str = await self._llm.apredict(
            self._text_to_sql_prompt,
            query_str=query_bundle.query_str,
            schema=table_desc_str,
            dialect=self._sql_database.dialect,
        )

        sql_query_str = self._sql_parser.parse_response_to_sql(
            response_str, query_bundle
        )
        # assume that it's a valid SQL query
        logger.debug(f"> Predicted SQL query: {sql_query_str}")

        if self._sql_only:
            sql_only_node = TextNode(text=f"{sql_query_str}")
            retrieved_nodes = [NodeWithScore(node=sql_only_node)]
            metadata: Dict[str, Any] = {}
        else:
            try:
                (
                    retrieved_nodes,
                    metadata,
                ) = await self._sql_retriever.aretrieve_with_metadata(sql_query_str)
            except BaseException as e:
                # if handle_sql_errors is True, then return error message
                if self._handle_sql_errors:
                    err_node = TextNode(text=f"Error: {e!s}")
                    retrieved_nodes = [NodeWithScore(node=err_node)]
                    metadata = {}
                else:
                    raise
        return retrieved_nodes, {"sql_query": sql_query_str, **metadata}

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve nodes given query."""
        retrieved_nodes, _ = self.retrieve_with_metadata(query_bundle)
        return retrieved_nodes

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Async retrieve nodes given query."""
        retrieved_nodes, _ = await self.aretrieve_with_metadata(query_bundle)
        return retrieved_nodes

    def_get_table_context(self, query_bundle: QueryBundle) -> str:
"""Get table context string."""
        table_schema_objs = self._get_tables(query_bundle.query_str)
        context_strs = []

        for table_schema_obj in table_schema_objs:
            # first append table info + additional context
            table_info = self._sql_database.get_single_table_info(
                table_schema_obj.table_name
            )
            if table_schema_obj.context_str:
                table_opt_context = " The table description is: "
                table_opt_context += table_schema_obj.context_str
                table_info += table_opt_context

            # also lookup vector index to return relevant table rows
            # if rows_retrievers was not passed, no rows will be returned
            if self._rows_retrievers is not None:
                rows_retriever = self._rows_retrievers[table_schema_obj.table_name]
                relevant_nodes = rows_retriever.retrieve(query_bundle.query_str)
                if len(relevant_nodes)  0:
                    table_row_context = "\nHere are some relevant example rows (values in the same order as columns above)\n"
                    for node in relevant_nodes:
                        table_row_context += str(node.get_content()) + "\n"
                    table_info += table_row_context

            # lookup column index to return relevant column values
            if self._cols_retrievers is not None:
                cols_retrievers = self._cols_retrievers[table_schema_obj.table_name]

                col_values_context = (
                    "\nHere are some relevant values of text columns:\n"
                )
                has_col_values = False
                for col_name, retriever in cols_retrievers.items():
                    relevant_nodes = retriever.retrieve(query_bundle.query_str)
                    if len(relevant_nodes)  0:
                        col_values_context += (
                            f"{col_name}: "
                            + ", ".join(
                                [str(node.get_content()) for node in relevant_nodes]
                            )
                            + "\n"
                        )
                        has_col_values = True

                if has_col_values:
                    table_info += col_values_context

            if self._verbose:
                print(f"> Table Info: {table_info}")
            context_strs.append(table_info)

        return "\n\n".join(context_strs)

```
 |  
| --- | --- |  
###  retrieve_with_metadata [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.NLSQLRetriever.retrieve_with_metadata "Permanent link")

```
retrieve_with_metadata(
    str_or_query_bundle: QueryType,
) -> Tuple[[], ]

```

Retrieve with metadata.
Source code in `llama-index-core/llama_index/core/indices/struct_store/sql_retriever.py`  
| 
```
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
```
 | 
```
defretrieve_with_metadata(
    self, str_or_query_bundle: QueryType
) -> Tuple[List[NodeWithScore], Dict]:
"""Retrieve with metadata."""
    if isinstance(str_or_query_bundle, str):
        query_bundle = QueryBundle(str_or_query_bundle)
    else:
        query_bundle = str_or_query_bundle
    table_desc_str = self._get_table_context(query_bundle)
    logger.info(f"> Table desc str: {table_desc_str}")
    if self._verbose:
        print(f"> Table desc str: {table_desc_str}")

    response_str = self._llm.predict(
        self._text_to_sql_prompt,
        query_str=query_bundle.query_str,
        schema=table_desc_str,
        dialect=self._sql_database.dialect,
    )

    sql_query_str = self._sql_parser.parse_response_to_sql(
        response_str, query_bundle
    )
    # assume that it's a valid SQL query
    logger.debug(f"> Predicted SQL query: {sql_query_str}")
    if self._verbose:
        print(f"> Predicted SQL query: {sql_query_str}")

    if self._sql_only:
        sql_only_node = TextNode(text=f"{sql_query_str}")
        retrieved_nodes = [NodeWithScore(node=sql_only_node)]
        metadata = {"result": sql_query_str}
    else:
        try:
            retrieved_nodes, metadata = self._sql_retriever.retrieve_with_metadata(
                sql_query_str
            )
        except BaseException as e:
            # if handle_sql_errors is True, then return error message
            if self._handle_sql_errors:
                err_node = TextNode(text=f"Error: {e!s}")
                retrieved_nodes = [NodeWithScore(node=err_node)]
                metadata = {}
            else:
                raise

    return retrieved_nodes, {"sql_query": sql_query_str, **metadata}

```
 |  
| --- | --- |  
###  aretrieve_with_metadata [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.NLSQLRetriever.aretrieve_with_metadata "Permanent link")

```
aretrieve_with_metadata(
    str_or_query_bundle: QueryType,
) -> Tuple[[], ]

```

Async retrieve with metadata.
Source code in `llama-index-core/llama_index/core/indices/struct_store/sql_retriever.py`  
| 
```
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
```
 | 
```
async defaretrieve_with_metadata(
    self, str_or_query_bundle: QueryType
) -> Tuple[List[NodeWithScore], Dict]:
"""Async retrieve with metadata."""
    if isinstance(str_or_query_bundle, str):
        query_bundle = QueryBundle(str_or_query_bundle)
    else:
        query_bundle = str_or_query_bundle
    table_desc_str = self._get_table_context(query_bundle)
    logger.info(f"> Table desc str: {table_desc_str}")

    response_str = await self._llm.apredict(
        self._text_to_sql_prompt,
        query_str=query_bundle.query_str,
        schema=table_desc_str,
        dialect=self._sql_database.dialect,
    )

    sql_query_str = self._sql_parser.parse_response_to_sql(
        response_str, query_bundle
    )
    # assume that it's a valid SQL query
    logger.debug(f"> Predicted SQL query: {sql_query_str}")

    if self._sql_only:
        sql_only_node = TextNode(text=f"{sql_query_str}")
        retrieved_nodes = [NodeWithScore(node=sql_only_node)]
        metadata: Dict[str, Any] = {}
    else:
        try:
            (
                retrieved_nodes,
                metadata,
            ) = await self._sql_retriever.aretrieve_with_metadata(sql_query_str)
        except BaseException as e:
            # if handle_sql_errors is True, then return error message
            if self._handle_sql_errors:
                err_node = TextNode(text=f"Error: {e!s}")
                retrieved_nodes = [NodeWithScore(node=err_node)]
                metadata = {}
            else:
                raise
    return retrieved_nodes, {"sql_query": sql_query_str, **metadata}

```
 |  
| --- | --- |  
##  SQLParserMode [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.SQLParserMode "Permanent link")
Bases: `str`, `Enum`
SQL Parser Mode.
Source code in `llama-index-core/llama_index/core/indices/struct_store/sql_retriever.py`  
| 
```
118
119
120
121
122
```
 | 
```
classSQLParserMode(str, Enum):
"""SQL Parser Mode."""

    DEFAULT = "default"
    PGVECTOR = "pgvector"

```
 |  
| --- | --- |  
##  SQLRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.SQLRetriever "Permanent link")
Bases: 
SQL Retriever.
Retrieves via raw SQL statements.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sql_database`  |   |  SQL database.  |  _required_  |  
|  `return_raw`  |  `bool`  |  Whether to return raw results or format results. Defaults to True.  |  `True`  |  
Source code in `llama-index-core/llama_index/core/indices/struct_store/sql_retriever.py`  
| 
```
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
```
 | 
```
classSQLRetriever(BaseRetriever):
"""
    SQL Retriever.

    Retrieves via raw SQL statements.

    Args:
        sql_database (SQLDatabase): SQL database.
        return_raw (bool): Whether to return raw results or format results.
            Defaults to True.

    """

    def__init__(
        self,
        sql_database: SQLDatabase,
        return_raw: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._sql_database = sql_database
        self._return_raw = return_raw
        super().__init__(callback_manager)

    def_format_node_results(
        self, results: List[List[Any]], col_keys: List[str]
    ) -> List[NodeWithScore]:
"""Format node results."""
        nodes = []
        for result in results:
            # associate column keys with result tuple
            metadata = dict(zip(col_keys, result))
            # NOTE: leave text field blank for now
            text_node = TextNode(
                text="",
                metadata=metadata,
            )
            nodes.append(NodeWithScore(node=text_node))
        return nodes

    defretrieve_with_metadata(
        self, str_or_query_bundle: QueryType
    ) -> Tuple[List[NodeWithScore], Dict]:
"""Retrieve with metadata."""
        if isinstance(str_or_query_bundle, str):
            query_bundle = QueryBundle(str_or_query_bundle)
        else:
            query_bundle = str_or_query_bundle
        raw_response_str, metadata = self._sql_database.run_sql(query_bundle.query_str)
        if self._return_raw:
            return [
                NodeWithScore(
                    node=TextNode(
                        text=raw_response_str,
                        metadata={
                            "sql_query": query_bundle.query_str,
                            "result": metadata["result"],
                            "col_keys": metadata["col_keys"],
                        },
                        excluded_embed_metadata_keys=[
                            "sql_query",
                            "result",
                            "col_keys",
                        ],
                        excluded_llm_metadata_keys=["sql_query", "result", "col_keys"],
                    )
                )
            ], metadata
        else:
            # return formatted
            results = metadata["result"]
            col_keys = metadata["col_keys"]
            return self._format_node_results(results, col_keys), metadata

    async defaretrieve_with_metadata(
        self, str_or_query_bundle: QueryType
    ) -> Tuple[List[NodeWithScore], Dict]:
        return self.retrieve_with_metadata(str_or_query_bundle)

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve nodes given query."""
        retrieved_nodes, _ = self.retrieve_with_metadata(query_bundle)
        return retrieved_nodes

```
 |  
| --- | --- |  
###  retrieve_with_metadata [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.SQLRetriever.retrieve_with_metadata "Permanent link")

```
retrieve_with_metadata(
    str_or_query_bundle: QueryType,
) -> Tuple[[], ]

```

Retrieve with metadata.
Source code in `llama-index-core/llama_index/core/indices/struct_store/sql_retriever.py`  
| 
```
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
```
 | 
```
defretrieve_with_metadata(
    self, str_or_query_bundle: QueryType
) -> Tuple[List[NodeWithScore], Dict]:
"""Retrieve with metadata."""
    if isinstance(str_or_query_bundle, str):
        query_bundle = QueryBundle(str_or_query_bundle)
    else:
        query_bundle = str_or_query_bundle
    raw_response_str, metadata = self._sql_database.run_sql(query_bundle.query_str)
    if self._return_raw:
        return [
            NodeWithScore(
                node=TextNode(
                    text=raw_response_str,
                    metadata={
                        "sql_query": query_bundle.query_str,
                        "result": metadata["result"],
                        "col_keys": metadata["col_keys"],
                    },
                    excluded_embed_metadata_keys=[
                        "sql_query",
                        "result",
                        "col_keys",
                    ],
                    excluded_llm_metadata_keys=["sql_query", "result", "col_keys"],
                )
            )
        ], metadata
    else:
        # return formatted
        results = metadata["result"]
        col_keys = metadata["col_keys"]
        return self._format_node_results(results, col_keys), metadata

```
 |  
| --- | --- |  
##  TreeAllLeafRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.TreeAllLeafRetriever "Permanent link")
Bases: 
GPT all leaf retriever.
This class builds a query-specific tree from leaf nodes to return a response. Using this query mode means that the tree index doesn't need to be built when initialized, since we rebuild the tree for each query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `text_qa_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  Question-Answer Prompt (see :ref:`Prompt-Templates`).  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/tree/all_leaf_retriever.py`  
| 
```
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
```
 | 
```
classTreeAllLeafRetriever(BaseRetriever):
"""
    GPT all leaf retriever.

    This class builds a query-specific tree from leaf nodes to return a response.
    Using this query mode means that the tree index doesn't need to be built
    when initialized, since we rebuild the tree for each query.

    Args:
        text_qa_template (Optional[BasePromptTemplate]): Question-Answer Prompt
            (see :ref:`Prompt-Templates`).

    """

    def__init__(
        self,
        index: TreeIndex,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
        self._index = index
        self._index_struct = index.index_struct
        self._docstore = index.docstore
        super().__init__(
            callback_manager=callback_manager, object_map=object_map, verbose=verbose
        )

    def_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""Get nodes for response."""
        logger.info(f"> Starting query: {query_bundle.query_str}")
        index_struct = cast(IndexGraph, self._index_struct)
        all_nodes = self._docstore.get_node_dict(index_struct.all_nodes)
        sorted_node_list = get_sorted_node_list(all_nodes)
        return [NodeWithScore(node=node) for node in sorted_node_list]

```
 |  
| --- | --- |  
##  TreeSelectLeafEmbeddingRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.TreeSelectLeafEmbeddingRetriever "Permanent link")
Bases: 
Tree select leaf embedding retriever.
This class traverses the index graph using the embedding similarity between the query and the node text.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  Tree Select Query Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `query_template_multiple`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  Tree Select Query Prompt (Multiple) (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `text_qa_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  Question-Answer Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `refine_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  Refinement Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `child_branch_factor`  |  Number of child nodes to consider at each level. If child_branch_factor is 1, then the query will only choose one child node to traverse for any given parent node. If child_branch_factor is 2, then the query will choose two child nodes.  |  
|  `embed_model`  |  `Optional[BaseEmbedding[](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding "BaseEmbedding \(llama_index.core.base.embeddings.base.BaseEmbedding\)")]`  |  Embedding model to use for embedding similarity.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/indices/tree/select_leaf_embedding_retriever.py`  
| 
```
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
```
 | 
```
classTreeSelectLeafEmbeddingRetriever(TreeSelectLeafRetriever):
"""
    Tree select leaf embedding retriever.

    This class traverses the index graph using the embedding similarity between the
    query and the node text.

    Args:
        query_template (Optional[BasePromptTemplate]): Tree Select Query Prompt
            (see :ref:`Prompt-Templates`).
        query_template_multiple (Optional[BasePromptTemplate]): Tree Select
            Query Prompt (Multiple)
            (see :ref:`Prompt-Templates`).
        text_qa_template (Optional[BasePromptTemplate]): Question-Answer Prompt
            (see :ref:`Prompt-Templates`).
        refine_template (Optional[BasePromptTemplate]): Refinement Prompt
            (see :ref:`Prompt-Templates`).
        child_branch_factor (int): Number of child nodes to consider at each level.
            If child_branch_factor is 1, then the query will only choose one child node
            to traverse for any given parent node.
            If child_branch_factor is 2, then the query will choose two child nodes.
        embed_model (Optional[BaseEmbedding]): Embedding model to use for
            embedding similarity.

    """

    def__init__(
        self,
        index: TreeIndex,
        embed_model: Optional[BaseEmbedding] = None,
        query_template: Optional[BasePromptTemplate] = None,
        text_qa_template: Optional[BasePromptTemplate] = None,
        refine_template: Optional[BasePromptTemplate] = None,
        query_template_multiple: Optional[BasePromptTemplate] = None,
        child_branch_factor: int = 1,
        verbose: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        **kwargs: Any,
    ):
        super().__init__(
            index,
            query_template=query_template,
            text_qa_template=text_qa_template,
            refine_template=refine_template,
            query_template_multiple=query_template_multiple,
            child_branch_factor=child_branch_factor,
            verbose=verbose,
            callback_manager=callback_manager,
            object_map=object_map,
            **kwargs,
        )
        self._embed_model = embed_model or Settings.embed_model

    def_query_level(
        self,
        cur_node_ids: Dict[int, str],
        query_bundle: QueryBundle,
        level: int = 0,
    ) -> str:
"""Answer a query recursively."""
        cur_nodes = {
            index: self._docstore.get_node(node_id)
            for index, node_id in cur_node_ids.items()
        }
        cur_node_list = get_sorted_node_list(cur_nodes)

        # Get the node with the highest similarity to the query
        selected_nodes, selected_indices = self._get_most_similar_nodes(
            cur_node_list, query_bundle
        )

        result_response = None
        for node, index in zip(selected_nodes, selected_indices):
            logger.debug(
                f">[Level {level}] Node [{index+1}] Summary text: "
                f"{' '.join(node.get_content().splitlines())}"
            )

            # Get the response for the selected node
            result_response = self._query_with_selected_node(
                node, query_bundle, level=level, prev_response=result_response
            )

        return cast(str, result_response)

    def_get_query_text_embedding_similarities(
        self, query_bundle: QueryBundle, nodes: List[BaseNode]
    ) -> List[float]:
"""
        Get query text embedding similarity.

        Cache the query embedding and the node text embedding.

        """
        if query_bundle.embedding is None:
            query_bundle.embedding = self._embed_model.get_agg_embedding_from_queries(
                query_bundle.embedding_strs
            )
        similarities = []
        for node in nodes:
            if node.embedding is None:
                node.embedding = self._embed_model.get_text_embedding(
                    node.get_content(metadata_mode=MetadataMode.EMBED)
                )

            similarity = self._embed_model.similarity(
                query_bundle.embedding, node.embedding
            )
            similarities.append(similarity)
        return similarities

    def_get_most_similar_nodes(
        self, nodes: List[BaseNode], query_bundle: QueryBundle
    ) -> Tuple[List[BaseNode], List[int]]:
"""Get the node with the highest similarity to the query."""
        similarities = self._get_query_text_embedding_similarities(query_bundle, nodes)

        selected_nodes: List[BaseNode] = []
        selected_indices: List[int] = []
        for node, _ in sorted(
            zip(nodes, similarities), key=lambda x: x[1], reverse=True
        ):
            if len(selected_nodes)  self.child_branch_factor:
                selected_nodes.append(node)
                selected_indices.append(nodes.index(node))
            else:
                break

        return selected_nodes, selected_indices

    def_select_nodes(
        self,
        cur_node_list: List[BaseNode],
        query_bundle: QueryBundle,
        level: int = 0,
    ) -> List[BaseNode]:
        selected_nodes, _ = self._get_most_similar_nodes(cur_node_list, query_bundle)
        return selected_nodes

```
 |  
| --- | --- |  
##  TreeSelectLeafRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.TreeSelectLeafRetriever "Permanent link")
Bases: 
Tree select leaf retriever.
This class traverses the index graph and searches for a leaf node that can best answer the query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  Tree Select Query Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `query_template_multiple`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  Tree Select Query Prompt (Multiple) (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `child_branch_factor`  |  Number of child nodes to consider at each level. If child_branch_factor is 1, then the query will only choose one child node to traverse for any given parent node. If child_branch_factor is 2, then the query will choose two child nodes.  |  
Source code in `llama-index-core/llama_index/core/indices/tree/select_leaf_retriever.py`  
| 
```
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
```
 | 
```
classTreeSelectLeafRetriever(BaseRetriever):
"""
    Tree select leaf retriever.

    This class traverses the index graph and searches for a leaf node that can best
    answer the query.

    Args:
        query_template (Optional[BasePromptTemplate]): Tree Select Query Prompt
            (see :ref:`Prompt-Templates`).
        query_template_multiple (Optional[BasePromptTemplate]): Tree Select
            Query Prompt (Multiple)
            (see :ref:`Prompt-Templates`).
        child_branch_factor (int): Number of child nodes to consider at each level.
            If child_branch_factor is 1, then the query will only choose one child node
            to traverse for any given parent node.
            If child_branch_factor is 2, then the query will choose two child nodes.

    """

    def__init__(
        self,
        index: TreeIndex,
        query_template: Optional[BasePromptTemplate] = None,
        text_qa_template: Optional[BasePromptTemplate] = None,
        refine_template: Optional[BasePromptTemplate] = None,
        query_template_multiple: Optional[BasePromptTemplate] = None,
        child_branch_factor: int = 1,
        verbose: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        **kwargs: Any,
    ):
        self._index = index
        self._llm = index._llm
        self._index_struct = index.index_struct
        self._docstore = index.docstore
        self._prompt_helper = Settings._prompt_helper or PromptHelper.from_llm_metadata(
            self._llm.metadata,
        )

        self._text_qa_template = text_qa_template or DEFAULT_TEXT_QA_PROMPT
        self._refine_template = refine_template or DEFAULT_REFINE_PROMPT_SEL
        self.query_template = query_template or DEFAULT_QUERY_PROMPT
        self.query_template_multiple = (
            query_template_multiple or DEFAULT_QUERY_PROMPT_MULTIPLE
        )
        self.child_branch_factor = child_branch_factor
        super().__init__(
            callback_manager=callback_manager or Settings.callback_manager,
            object_map=object_map,
            verbose=verbose,
        )

    def_query_with_selected_node(
        self,
        selected_node: BaseNode,
        query_bundle: QueryBundle,
        prev_response: Optional[str] = None,
        level: int = 0,
    ) -> str:
"""
        Get response for selected node.

        If not leaf node, it will recursively call _query on the child nodes.
        If prev_response is provided, we will update prev_response with the answer.

        """
        query_str = query_bundle.query_str

        if len(self._index_struct.get_children(selected_node)) == 0:
            response_builder = get_response_synthesizer(
                llm=self._llm,
                text_qa_template=self._text_qa_template,
                refine_template=self._refine_template,
                callback_manager=self.callback_manager,
            )
            # use response builder to get answer from node
            node_text = get_text_from_node(selected_node, level=level)
            cur_response = response_builder.get_response(
                query_str, [node_text], prev_response=prev_response
            )
            cur_response = str(cur_response)
            logger.debug(f">[Level {level}] Current answer response: {cur_response} ")
        else:
            cur_response = self._query_level(
                self._index_struct.get_children(selected_node),
                query_bundle,
                level=level + 1,
            )

        if prev_response is None:
            return cur_response
        else:
            context_msg = selected_node.get_content(metadata_mode=MetadataMode.LLM)
            cur_response = self._llm.predict(
                self._refine_template,
                query_str=query_str,
                existing_answer=prev_response,
                context_msg=context_msg,
            )

            logger.debug(f">[Level {level}] Current refined response: {cur_response} ")
            return str(cur_response)

    def_query_level(
        self,
        cur_node_ids: Dict[int, str],
        query_bundle: QueryBundle,
        level: int = 0,
    ) -> str:
"""Answer a query recursively."""
        query_str = query_bundle.query_str
        cur_nodes = {
            index: self._docstore.get_node(node_id)
            for index, node_id in cur_node_ids.items()
        }
        cur_node_list = get_sorted_node_list(cur_nodes)

        if len(cur_node_list) == 1:
            logger.debug(f">[Level {level}] Only one node left. Querying node.")
            return self._query_with_selected_node(
                cur_node_list[0], query_bundle, level=level
            )
        elif self.child_branch_factor == 1:
            query_template = self.query_template.partial_format(
                num_chunks=len(cur_node_list), query_str=query_str
            )
            text_splitter = self._prompt_helper.get_text_splitter_given_prompt(
                prompt=query_template,
                num_chunks=len(cur_node_list),
                llm=self._llm,
            )
            numbered_node_text = get_numbered_text_from_nodes(
                cur_node_list, text_splitter=text_splitter
            )

            response = self._llm.predict(
                query_template,
                context_list=numbered_node_text,
            )
        else:
            query_template_multiple = self.query_template_multiple.partial_format(
                num_chunks=len(cur_node_list),
                query_str=query_str,
                branching_factor=self.child_branch_factor,
            )

            text_splitter = self._prompt_helper.get_text_splitter_given_prompt(
                prompt=query_template_multiple,
                num_chunks=len(cur_node_list),
                llm=self._llm,
            )
            numbered_node_text = get_numbered_text_from_nodes(
                cur_node_list, text_splitter=text_splitter
            )

            response = self._llm.predict(
                query_template_multiple,
                context_list=numbered_node_text,
            )

        debug_str = f">[Level {level}] Current response: {response}"
        logger.debug(debug_str)
        if self._verbose:
            print_text(debug_str, end="\n")

        numbers = extract_numbers_given_response(response, n=self.child_branch_factor)
        if numbers is None:
            debug_str = (
                f">[Level {level}] Could not retrieve response - no numbers present"
            )
            logger.debug(debug_str)
            if self._verbose:
                print_text(debug_str, end="\n")
            # just join text from current nodes as response
            return response
        result_response = None
        for number_str in numbers:
            number = int(number_str)
            if number  len(cur_node_list):
                logger.debug(
                    f">[Level {level}] Invalid response: {response} - "
                    f"number {number} out of range"
                )
                return response

            # number is 1-indexed, so subtract 1
            selected_node = cur_node_list[number - 1]

            info_str = (
                f">[Level {level}] Selected node: "
                f"[{number}]/[{','.join([str(int(n))forninnumbers])}]"
            )
            logger.info(info_str)
            if self._verbose:
                print_text(info_str, end="\n")
            debug_str = " ".join(
                selected_node.get_content(metadata_mode=MetadataMode.LLM).splitlines()
            )
            full_debug_str = (
                f">[Level {level}] Node "
                f"[{number}] Summary text: "
                f"{selected_node.get_content(metadata_mode=MetadataMode.LLM)}"
            )
            logger.debug(full_debug_str)
            if self._verbose:
                print_text(full_debug_str, end="\n")
            result_response = self._query_with_selected_node(
                selected_node,
                query_bundle,
                prev_response=result_response,
                level=level,
            )
        # result_response should not be None
        return cast(str, result_response)

    def_query(self, query_bundle: QueryBundle) -> Response:
"""Answer a query."""
        # NOTE: this overrides the _query method in the base class
        info_str = f"> Starting query: {query_bundle.query_str}"
        logger.info(info_str)
        if self._verbose:
            print_text(info_str, end="\n")
        response_str = self._query_level(
            self._index_struct.root_nodes,
            query_bundle,
            level=0,
        ).strip()
        # TODO: fix source nodes
        return Response(response_str, source_nodes=[])

    def_select_nodes(
        self,
        cur_node_list: List[BaseNode],
        query_bundle: QueryBundle,
        level: int = 0,
    ) -> List[BaseNode]:
        query_str = query_bundle.query_str

        if self.child_branch_factor == 1:
            query_template = self.query_template.partial_format(
                num_chunks=len(cur_node_list), query_str=query_str
            )
            text_splitter = self._prompt_helper.get_text_splitter_given_prompt(
                prompt=query_template,
                num_chunks=len(cur_node_list),
                llm=self._llm,
            )
            numbered_node_text = get_numbered_text_from_nodes(
                cur_node_list, text_splitter=text_splitter
            )

            response = self._llm.predict(
                query_template,
                context_list=numbered_node_text,
            )
        else:
            query_template_multiple = self.query_template_multiple.partial_format(
                num_chunks=len(cur_node_list),
                query_str=query_str,
                branching_factor=self.child_branch_factor,
            )

            text_splitter = self._prompt_helper.get_text_splitter_given_prompt(
                prompt=query_template_multiple,
                num_chunks=len(cur_node_list),
                llm=self._llm,
            )
            numbered_node_text = get_numbered_text_from_nodes(
                cur_node_list, text_splitter=text_splitter
            )

            response = self._llm.predict(
                query_template_multiple,
                context_list=numbered_node_text,
            )

        debug_str = f">[Level {level}] Current response: {response}"
        logger.debug(debug_str)
        if self._verbose:
            print_text(debug_str, end="\n")

        numbers = extract_numbers_given_response(response, n=self.child_branch_factor)
        if numbers is None:
            debug_str = (
                f">[Level {level}] Could not retrieve response - no numbers present"
            )
            logger.debug(debug_str)
            if self._verbose:
                print_text(debug_str, end="\n")
            # just join text from current nodes as response
            return []

        selected_nodes = []
        for number_str in numbers:
            number = int(number_str)
            if number  len(cur_node_list):
                logger.debug(
                    f">[Level {level}] Invalid response: {response} - "
                    f"number {number} out of range"
                )
                continue

            # number is 1-indexed, so subtract 1
            selected_node = cur_node_list[number - 1]

            info_str = (
                f">[Level {level}] Selected node: "
                f"[{number}]/[{','.join([str(int(n))forninnumbers])}]"
            )
            logger.info(info_str)
            if self._verbose:
                print_text(info_str, end="\n")
            debug_str = " ".join(
                selected_node.get_content(metadata_mode=MetadataMode.LLM).splitlines()
            )
            full_debug_str = (
                f">[Level {level}] Node "
                f"[{number}] Summary text: "
                f"{selected_node.get_content(metadata_mode=MetadataMode.LLM)}"
            )
            logger.debug(full_debug_str)
            if self._verbose:
                print_text(full_debug_str, end="\n")
            selected_nodes.append(selected_node)

        return selected_nodes

    def_retrieve_level(
        self,
        cur_node_ids: Dict[int, str],
        query_bundle: QueryBundle,
        level: int = 0,
    ) -> List[BaseNode]:
"""Answer a query recursively."""
        cur_nodes = {
            index: self._docstore.get_node(node_id)
            for index, node_id in cur_node_ids.items()
        }
        cur_node_list = get_sorted_node_list(cur_nodes)

        if len(cur_node_list)  self.child_branch_factor:
            selected_nodes = self._select_nodes(
                cur_node_list,
                query_bundle,
                level=level,
            )
        else:
            selected_nodes = cur_node_list

        children_nodes = {}
        for node in selected_nodes:
            node_dict = self._index_struct.get_children(node)
            children_nodes.update(node_dict)

        if len(children_nodes) == 0:
            # NOTE: leaf level
            return selected_nodes
        else:
            return self._retrieve_level(children_nodes, query_bundle, level + 1)

    def_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""Get nodes for response."""
        nodes = self._retrieve_level(
            self._index_struct.root_nodes,
            query_bundle,
            level=0,
        )
        return [NodeWithScore(node=node) for node in nodes]

```
 |  
| --- | --- |  
##  TreeRootRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.TreeRootRetriever "Permanent link")
Bases: 
Tree root retriever.
This class directly retrieves the answer from the root nodes.
Unlike GPTTreeIndexLeafQuery, this class assumes the graph already stores the answer (because it was constructed with a query_str), so it does not attempt to parse information down the graph in order to synthesize an answer.
Source code in `llama-index-core/llama_index/core/indices/tree/tree_root_retriever.py`  
| 
```
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
classTreeRootRetriever(BaseRetriever):
"""
    Tree root retriever.

    This class directly retrieves the answer from the root nodes.

    Unlike GPTTreeIndexLeafQuery, this class assumes the graph already stores
    the answer (because it was constructed with a query_str), so it does not
    attempt to parse information down the graph in order to synthesize an answer.
    """

    def__init__(
        self,
        index: TreeIndex,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
        self._index = index
        self._index_struct = index.index_struct
        self._docstore = index.docstore
        super().__init__(
            callback_manager=callback_manager, object_map=object_map, verbose=verbose
        )

    def_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""Get nodes for response."""
        logger.info(f"> Starting query: {query_bundle.query_str}")
        root_nodes = self._docstore.get_node_dict(self._index_struct.root_nodes)
        sorted_nodes = get_sorted_node_list(root_nodes)
        return [NodeWithScore(node=node) for node in sorted_nodes]

```
 |  
| --- | --- |  
##  VectorIndexAutoRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.VectorIndexAutoRetriever "Permanent link")
Bases: `BaseAutoRetriever`
Vector store auto retriever.
A retriever for vector store index that uses an LLM to automatically set vector store query parameters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index`  |   |  vector store index  |  _required_  |  
|  `vector_store_info`  |   |  additional information about vector store content and supported metadata filters. The natural language description is used by an LLM to automatically set vector store query parameters.  |  _required_  |  
|  `prompt_template_str`  |  `Optional[str]`  |  custom prompt template string for LLM. Uses default template string if None.  |  `None`  |  
|  `similarity_top_k`  |  number of top k results to return.  |  `DEFAULT_SIMILARITY_TOP_K`  |  
|  `empty_query_top_k`  |  `Optional[int]`  |  number of top k results to return if the inferred query string is blank (uses metadata filters only). Can be set to None, which would use the similarity_top_k instead. By default, set to 10.  |  
|  `max_top_k`  |  the maximum top_k allowed. The top_k set by LLM or similarity_top_k will be clamped to this value.  |  
|  `vector_store_query_mode`  |  vector store query mode See reference for VectorStoreQueryMode for full list of supported modes.  |  `DEFAULT`  |  
|  `default_empty_query_vector`  |  `Optional[List[float]]`  |  default empty query vector. Defaults to None. If not None, then this vector will be used as the query vector if the query is empty.  |  `None`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  callback manager  |  `None`  |  
|  `verbose`  |  `bool`  |  verbose mode  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/vector_store/retrievers/auto_retriever/auto_retriever.py`  
| 
```
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
```
 | 
```
classVectorIndexAutoRetriever(BaseAutoRetriever):
"""
    Vector store auto retriever.

    A retriever for vector store index that uses an LLM to automatically set
    vector store query parameters.

    Args:
        index (VectorStoreIndex): vector store index
        vector_store_info (VectorStoreInfo): additional information about
            vector store content and supported metadata filters. The natural language
            description is used by an LLM to automatically set vector store query
            parameters.
        prompt_template_str: custom prompt template string for LLM.
            Uses default template string if None.
        similarity_top_k (int): number of top k results to return.
        empty_query_top_k (Optional[int]): number of top k results to return
            if the inferred query string is blank (uses metadata filters only).
            Can be set to None, which would use the similarity_top_k instead.
            By default, set to 10.
        max_top_k (int):
            the maximum top_k allowed. The top_k set by LLM or similarity_top_k will
            be clamped to this value.
        vector_store_query_mode (str): vector store query mode
            See reference for VectorStoreQueryMode for full list of supported modes.
        default_empty_query_vector (Optional[List[float]]): default empty query vector.
            Defaults to None. If not None, then this vector will be used as the query
            vector if the query is empty.
        callback_manager (Optional[CallbackManager]): callback manager
        verbose (bool): verbose mode

    """

    def__init__(
        self,
        index: VectorStoreIndex,
        vector_store_info: VectorStoreInfo,
        llm: Optional[LLM] = None,
        prompt_template_str: Optional[str] = None,
        max_top_k: int = 10,
        similarity_top_k: int = DEFAULT_SIMILARITY_TOP_K,
        empty_query_top_k: Optional[int] = 10,
        vector_store_query_mode: VectorStoreQueryMode = VectorStoreQueryMode.DEFAULT,
        default_empty_query_vector: Optional[List[float]] = None,
        callback_manager: Optional[CallbackManager] = None,
        verbose: bool = False,
        extra_filters: Optional[MetadataFilters] = None,
        object_map: Optional[dict] = None,
        objects: Optional[List[IndexNode]] = None,
        **kwargs: Any,
    ) -> None:
        self._index = index
        self._vector_store_info = vector_store_info
        self._default_empty_query_vector = default_empty_query_vector
        self._llm = llm or Settings.llm
        callback_manager = callback_manager or Settings.callback_manager

        # prompt
        prompt_template_str = (
            prompt_template_str or DEFAULT_VECTOR_STORE_QUERY_PROMPT_TMPL
        )
        self._output_parser = VectorStoreQueryOutputParser()
        self._prompt: BasePromptTemplate = PromptTemplate(template=prompt_template_str)

        # additional config
        self._max_top_k = max_top_k
        self._similarity_top_k = similarity_top_k
        self._empty_query_top_k = empty_query_top_k
        self._vector_store_query_mode = vector_store_query_mode
        # if extra_filters is OR condition, we don't support that yet
        if extra_filters is not None and extra_filters.condition == FilterCondition.OR:
            raise ValueError("extra_filters cannot be OR condition")
        self._extra_filters = extra_filters or MetadataFilters(filters=[])
        self._kwargs = kwargs
        super().__init__(
            callback_manager=callback_manager,
            object_map=object_map or self._index._object_map,
            objects=objects,
            verbose=verbose,
        )

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {
            "prompt": self._prompt,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Get prompt modules."""
        if "prompt" in prompts:
            self._prompt = prompts["prompt"]

    def_get_query_bundle(self, query: str) -> QueryBundle:
"""Get query bundle."""
        if not query and self._default_empty_query_vector is not None:
            return QueryBundle(
                query_str="",
                embedding=self._default_empty_query_vector,
            )
        else:
            return QueryBundle(query_str=query)

    def_parse_generated_spec(
        self, output: str, query_bundle: QueryBundle
    ) -> BaseModel:
"""Parse generated spec."""
        try:
            structured_output = cast(
                StructuredOutput, self._output_parser.parse(output)
            )
            query_spec = cast(VectorStoreQuerySpec, structured_output.parsed_output)
        except OutputParserException:
            _logger.warning("Failed to parse query spec, using defaults as fallback.")
            query_spec = VectorStoreQuerySpec(
                query=query_bundle.query_str,
                filters=[],
                top_k=None,
            )

        return query_spec

    defgenerate_retrieval_spec(
        self, query_bundle: QueryBundle, **kwargs: Any
    ) -> BaseModel:
        # prepare input
        info_str = self._vector_store_info.model_dump_json(indent=4)
        schema_str = VectorStoreQuerySpec.model_json_schema()

        # call LLM
        output = self._llm.predict(
            self._prompt,
            schema_str=schema_str,
            info_str=info_str,
            query_str=query_bundle.query_str,
        )

        # parse output
        return self._parse_generated_spec(output, query_bundle)

    async defagenerate_retrieval_spec(
        self, query_bundle: QueryBundle, **kwargs: Any
    ) -> BaseModel:
        # prepare input
        info_str = self._vector_store_info.model_dump_json(indent=4)
        schema_str = VectorStoreQuerySpec.model_json_schema()

        # call LLM
        output = await self._llm.apredict(
            self._prompt,
            schema_str=schema_str,
            info_str=info_str,
            query_str=query_bundle.query_str,
        )

        # parse output
        return self._parse_generated_spec(output, query_bundle)

    def_build_retriever_from_spec(  # type: ignore
        self, spec: VectorStoreQuerySpec
    ) -> Tuple[BaseRetriever, QueryBundle]:
        # construct new query bundle from query_spec
        # insert 0 vector if query is empty and default_empty_query_vector is not None
        new_query_bundle = self._get_query_bundle(spec.query)

        _logger.info(f"Using query str: {spec.query}")
        filter_list = [
            (filter.key, filter.operator.value, filter.value) for filter in spec.filters
        ]
        _logger.info(f"Using filters: {filter_list}")
        if self._verbose:
            print(f"Using query str: {spec.query}")
            print(f"Using filters: {filter_list}")

        # define similarity_top_k
        # if query is specified, then use similarity_top_k
        # if query is blank, then use empty_query_top_k
        if spec.query or self._empty_query_top_k is None:
            similarity_top_k = self._similarity_top_k
        else:
            similarity_top_k = self._empty_query_top_k

        # if query_spec.top_k is specified, then use it
        # as long as below max_top_k and similarity_top_k
        if spec.top_k is not None:
            similarity_top_k = min(spec.top_k, self._max_top_k, similarity_top_k)

        _logger.info(f"Using top_k: {similarity_top_k}")

        # avoid passing empty filters to retriever
        if len(spec.filters) + len(self._extra_filters.filters) == 0:
            filters = None
        else:
            filters = MetadataFilters(
                filters=[*spec.filters, *self._extra_filters.filters]
            )

        return (
            VectorIndexRetriever(
                self._index,
                filters=filters,
                similarity_top_k=similarity_top_k,
                vector_store_query_mode=self._vector_store_query_mode,
                object_map=self.object_map,
                verbose=self._verbose,
                **self._kwargs,
            ),
            new_query_bundle,
        )

```
 |  
| --- | --- |  
##  VectorIndexRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.VectorIndexRetriever "Permanent link")
Bases: 
Vector index retriever.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index`  |   |  vector store index.  |  _required_  |  
|  `similarity_top_k`  |  number of top k results to return.  |  `DEFAULT_SIMILARITY_TOP_K`  |  
|  `vector_store_query_mode`  |  vector store query mode See reference for VectorStoreQueryMode for full list of supported modes.  |  `DEFAULT`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  metadata filters, defaults to None  |  `None`  |  
|  `alpha`  |  `float`  |  weight for sparse/dense retrieval, only used for hybrid query mode.  |  `None`  |  
|  `doc_ids`  |  `Optional[List[str]]`  |  list of documents to constrain search.  |  `None`  |  
|  `vector_store_kwargs`  |  `dict`  |  Additional vector store specific kwargs to pass through to the vector store at query time.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/vector_store/retrievers/retriever.py`  
| 
```
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
```
 | 
```
classVectorIndexRetriever(BaseRetriever):
"""
    Vector index retriever.

    Args:
        index (VectorStoreIndex): vector store index.
        similarity_top_k (int): number of top k results to return.
        vector_store_query_mode (str): vector store query mode
            See reference for VectorStoreQueryMode for full list of supported modes.
        filters (Optional[MetadataFilters]): metadata filters, defaults to None
        alpha (float): weight for sparse/dense retrieval, only used for
            hybrid query mode.
        doc_ids (Optional[List[str]]): list of documents to constrain search.
        vector_store_kwargs (dict): Additional vector store specific kwargs to pass
            through to the vector store at query time.

    """

    def__init__(
        self,
        index: VectorStoreIndex,
        similarity_top_k: int = DEFAULT_SIMILARITY_TOP_K,
        vector_store_query_mode: VectorStoreQueryMode = VectorStoreQueryMode.DEFAULT,
        filters: Optional[MetadataFilters] = None,
        alpha: Optional[float] = None,
        node_ids: Optional[List[str]] = None,
        doc_ids: Optional[List[str]] = None,
        sparse_top_k: Optional[int] = None,
        hybrid_top_k: Optional[int] = None,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        embed_model: Optional[BaseEmbedding] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._index = index
        self._vector_store = self._index.vector_store
        self._embed_model = embed_model or self._index._embed_model
        self._docstore = self._index.docstore

        self._similarity_top_k = similarity_top_k
        self._vector_store_query_mode = VectorStoreQueryMode(vector_store_query_mode)
        self._alpha = alpha
        self._node_ids = node_ids
        self._doc_ids = doc_ids
        self._filters = filters
        self._sparse_top_k = sparse_top_k
        self._hybrid_top_k = hybrid_top_k
        self._kwargs: Dict[str, Any] = kwargs.get("vector_store_kwargs", {})

        callback_manager = callback_manager or CallbackManager()
        super().__init__(
            callback_manager=callback_manager,
            object_map=object_map,
            verbose=verbose,
        )

    @property
    defsimilarity_top_k(self) -> int:
"""Return similarity top k."""
        return self._similarity_top_k

    @similarity_top_k.setter
    defsimilarity_top_k(self, similarity_top_k: int) -> None:
"""Set similarity top k."""
        self._similarity_top_k = similarity_top_k

    def_needs_embedding(self) -> bool:
"""Check if the current query mode requires embeddings."""
        return (
            self._vector_store.is_embedding_query
            and self._vector_store_query_mode
            not in (
                VectorStoreQueryMode.TEXT_SEARCH,
                VectorStoreQueryMode.SPARSE,
            )
        )

    @dispatcher.span
    def_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
        if self._needs_embedding():
            if query_bundle.embedding is None and len(query_bundle.embedding_strs)  0:
                query_bundle.embedding = (
                    self._embed_model.get_agg_embedding_from_queries(
                        query_bundle.embedding_strs
                    )
                )
        return self._get_nodes_with_embeddings(query_bundle)

    @dispatcher.span
    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        embedding = query_bundle.embedding
        if self._needs_embedding():
            if query_bundle.embedding is None and len(query_bundle.embedding_strs)  0:
                embed_model = self._embed_model
                embedding = await embed_model.aget_agg_embedding_from_queries(
                    query_bundle.embedding_strs
                )
        return await self._aget_nodes_with_embeddings(
            QueryBundle(query_str=query_bundle.query_str, embedding=embedding)
        )

    def_build_vector_store_query(
        self, query_bundle_with_embeddings: QueryBundle
    ) -> VectorStoreQuery:
        return VectorStoreQuery(
            query_embedding=query_bundle_with_embeddings.embedding,
            similarity_top_k=self._similarity_top_k,
            node_ids=self._node_ids,
            doc_ids=self._doc_ids,
            query_str=query_bundle_with_embeddings.query_str,
            mode=self._vector_store_query_mode,
            alpha=self._alpha,
            filters=self._filters,
            sparse_top_k=self._sparse_top_k,
            hybrid_top_k=self._hybrid_top_k,
        )

    def_determine_nodes_to_fetch(
        self, query_result: VectorStoreQueryResult
    ) -> list[str]:
"""
        Determine the nodes to fetch from the docstore.

        If the vector store does not store text, we need to fetch every node from the docstore.
        If the vector store stores text, we need to fetch only the nodes that are not text.
        """
        if query_result.nodes:
            # Fetch non-text nodes from the docstore
            return [
                node.node_id
                for node in query_result.nodes  # no folding
                if node.as_related_node_info().node_type
                != ObjectType.TEXT  # TODO: no need to fetch multimodal `Node` if they only include text
            ]
        elif query_result.ids:
            # Fetch all nodes from the docstore
            return [
                self._index.index_struct.nodes_dict[idx] for idx in query_result.ids
            ]

        else:
            return []

    def_insert_fetched_nodes_into_query_result(
        self, query_result: VectorStoreQueryResult, fetched_nodes: List[BaseNode]
    ) -> Sequence[BaseNode]:
"""
        Insert the fetched nodes into the query result.

        If the vector store does not store text, all nodes are inserted into the query result.
        If the vector store stores text, we replace non-text nodes with those fetched from the docstore,
            unless the node was not found in the docstore, in which case we keep the original node.
        """
        fetched_nodes_by_id: Dict[str, BaseNode] = {
            str(node.node_id): node for node in fetched_nodes
        }
        new_nodes: List[BaseNode] = []

        if query_result.nodes:
            for node in list(query_result.nodes):
                node_id_str = str(node.node_id)
                if node_id_str in fetched_nodes_by_id:
                    new_nodes.append(fetched_nodes_by_id[node_id_str])
                else:
                    # We did not fetch a replacement node, so we keep the original node
                    new_nodes.append(node)
        elif query_result.ids:
            for node_id in query_result.ids:
                if node_id not in self._index.index_struct.nodes_dict:
                    raise KeyError(f"Node ID {node_id} not found in index. ")
                node_id_str = str(self._index.index_struct.nodes_dict[node_id])
                if node_id_str in fetched_nodes_by_id:
                    new_nodes.append(fetched_nodes_by_id[node_id_str])
                else:
                    raise KeyError(
                        f"Node ID {node_id_str} not found in fetched nodes. "
                    )
        elif query_result.ids is None and query_result.nodes is None:
            raise ValueError(
                "Vector store query result should return at least one of nodes or ids."
            )
        return new_nodes

    def_convert_nodes_to_scored_nodes(
        self, query_result: VectorStoreQueryResult
    ) -> List[NodeWithScore]:
"""Create scored nodes from the vector store query result."""
        node_with_scores: List[NodeWithScore] = []

        for ind, node in enumerate(list(query_result.nodes or [])):
            score: Optional[float] = None
            if query_result.similarities is not None:
                score = query_result.similarities[ind]

            node_with_scores.append(NodeWithScore(node=node, score=score))

        return node_with_scores

    def_get_nodes_with_embeddings(
        self, query_bundle_with_embeddings: QueryBundle
    ) -> List[NodeWithScore]:
        query = self._build_vector_store_query(query_bundle_with_embeddings)
        query_result = self._vector_store.query(query, **self._kwargs)

        nodes_to_fetch = self._determine_nodes_to_fetch(query_result)
        if nodes_to_fetch:
            # Fetch any missing nodes from the docstore and insert them into the query result
            fetched_nodes: List[BaseNode] = self._docstore.get_nodes(
                node_ids=nodes_to_fetch, raise_error=False
            )

            query_result.nodes = self._insert_fetched_nodes_into_query_result(
                query_result, fetched_nodes
            )

        log_vector_store_query_result(query_result)

        return self._convert_nodes_to_scored_nodes(query_result)

    async def_aget_nodes_with_embeddings(
        self, query_bundle_with_embeddings: QueryBundle
    ) -> List[NodeWithScore]:
        query = self._build_vector_store_query(query_bundle_with_embeddings)
        query_result = await self._vector_store.aquery(query, **self._kwargs)

        nodes_to_fetch = self._determine_nodes_to_fetch(query_result)
        if nodes_to_fetch:
            # Fetch any missing nodes from the docstore and insert them into the query result
            fetched_nodes: List[BaseNode] = await self._docstore.aget_nodes(
                node_ids=nodes_to_fetch, raise_error=False
            )

            query_result.nodes = self._insert_fetched_nodes_into_query_result(
                query_result, fetched_nodes
            )

        log_vector_store_query_result(query_result)

        return self._convert_nodes_to_scored_nodes(query_result)

```
 |  
| --- | --- |  
###  similarity_top_k `property` `writable` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.VectorIndexRetriever.similarity_top_k "Permanent link")

```
similarity_top_k: 

```

Return similarity top k.
##  AutoMergingRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.AutoMergingRetriever "Permanent link")
Bases: 
This retriever will try to merge context into parent context.
The retriever first retrieves chunks from a vector store. Then, it will try to merge the chunks into a single context.
Source code in `llama-index-core/llama_index/core/retrievers/auto_merging_retriever.py`  
| 
```
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
```
 | 
```
classAutoMergingRetriever(BaseRetriever):
"""
    This retriever will try to merge context into parent context.

    The retriever first retrieves chunks from a vector store.
    Then, it will try to merge the chunks into a single context.

    """

    def__init__(
        self,
        vector_retriever: VectorIndexRetriever,
        storage_context: StorageContext,
        simple_ratio_thresh: float = 0.5,
        verbose: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        objects: Optional[List[IndexNode]] = None,
    ) -> None:
"""Init params."""
        self._vector_retriever = vector_retriever
        self._storage_context = storage_context
        self._simple_ratio_thresh = simple_ratio_thresh
        super().__init__(
            callback_manager=callback_manager,
            object_map=object_map,
            objects=objects,
            verbose=verbose,
        )

    def_get_parents_and_merge(
        self, nodes: List[NodeWithScore]
    ) -> Tuple[List[NodeWithScore], bool]:
"""Get parents and merge nodes."""
        # retrieve all parent nodes
        parent_nodes: Dict[str, BaseNode] = {}
        parent_cur_children_dict: Dict[str, List[NodeWithScore]] = defaultdict(list)
        for node in nodes:
            if node.node.parent_node is None:
                continue
            parent_node_info = node.node.parent_node

            # Fetch actual parent node if doesn't exist in `parent_nodes` cache yet
            parent_node_id = parent_node_info.node_id
            if parent_node_id not in parent_nodes:
                parent_node = self._storage_context.docstore.get_document(
                    parent_node_id
                )
                parent_nodes[parent_node_id] = cast(BaseNode, parent_node)

            # add reference to child from parent
            parent_cur_children_dict[parent_node_id].append(node)

        # compute ratios and "merge" nodes
        # merging: delete some children nodes, add some parent nodes
        node_ids_to_delete = set()
        nodes_to_add: Dict[str, NodeWithScore] = {}
        for parent_node_id, parent_node in parent_nodes.items():
            parent_child_nodes = parent_node.child_nodes
            parent_num_children = len(parent_child_nodes) if parent_child_nodes else 1
            parent_cur_children = parent_cur_children_dict[parent_node_id]
            ratio = len(parent_cur_children) / parent_num_children

            # if ratio is high enough, merge
            if ratio  self._simple_ratio_thresh:
                node_ids_to_delete.update(
                    set({n.node.node_id for n in parent_cur_children})
                )

                parent_node_text = truncate_text(
                    parent_node.get_content(metadata_mode=MetadataMode.NONE), 100
                )
                info_str = (
                    f"> Merging {len(parent_cur_children)} nodes into parent node.\n"
                    f"> Parent node id: {parent_node_id}.\n"
                    f"> Parent node text: {parent_node_text}\n"
                )
                logger.info(info_str)
                if self._verbose:
                    print(info_str)

                # add parent node
                # can try averaging score across embeddings for now

                avg_score = sum(
                    [n.get_score() or 0.0 for n in parent_cur_children]
                ) / len(parent_cur_children)
                parent_node_with_score = NodeWithScore(
                    node=parent_node, score=avg_score
                )
                nodes_to_add[parent_node_id] = parent_node_with_score

        # delete old child nodes, add new parent nodes
        new_nodes = [n for n in nodes if n.node.node_id not in node_ids_to_delete]
        # add parent nodes
        new_nodes.extend(list(nodes_to_add.values()))

        is_changed = len(node_ids_to_delete)  0

        return new_nodes, is_changed

    def_fill_in_nodes(
        self, nodes: List[NodeWithScore]
    ) -> Tuple[List[NodeWithScore], bool]:
"""Fill in nodes."""
        new_nodes = []
        is_changed = False
        for idx, node in enumerate(nodes):
            new_nodes.append(node)
            if idx >= len(nodes) - 1:
                continue

            cur_node = cast(BaseNode, node.node)
            # if there's a node in the middle, add that to the queue
            if (
                cur_node.next_node is not None
                and cur_node.next_node == nodes[idx + 1].node.prev_node
            ):
                is_changed = True
                next_node = self._storage_context.docstore.get_document(
                    cur_node.next_node.node_id
                )
                next_node = cast(BaseNode, next_node)

                next_node_text = truncate_text(
                    next_node.get_content(metadata_mode=MetadataMode.NONE), 100
                )
                info_str = (
                    f"> Filling in node. Node id: {cur_node.next_node.node_id}"
                    f"> Node text: {next_node_text}\n"
                )
                logger.info(info_str)
                if self._verbose:
                    print(info_str)

                # set score to be average of current node and next node
                avg_score = (node.get_score() + nodes[idx + 1].get_score()) / 2
                new_nodes.append(NodeWithScore(node=next_node, score=avg_score))
        return new_nodes, is_changed

    def_try_merging(
        self, nodes: List[NodeWithScore]
    ) -> Tuple[List[NodeWithScore], bool]:
"""Try different ways to merge nodes."""
        # first try filling in nodes
        nodes, is_changed_0 = self._fill_in_nodes(nodes)
        # then try merging nodes
        nodes, is_changed_1 = self._get_parents_and_merge(nodes)
        return nodes, is_changed_0 or is_changed_1

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""
        Retrieve nodes given query.

        Implemented by the user.

        """
        initial_nodes = self._vector_retriever.retrieve(query_bundle)

        cur_nodes, is_changed = self._try_merging(initial_nodes)
        # cur_nodes, is_changed = self._get_parents_and_merge(initial_nodes)
        while is_changed:
            cur_nodes, is_changed = self._try_merging(cur_nodes)
            # cur_nodes, is_changed = self._get_parents_and_merge(cur_nodes)

        # sort by similarity
        cur_nodes.sort(key=lambda x: x.get_score(), reverse=True)

        return cur_nodes

```
 |  
| --- | --- |  
##  QueryFusionRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.QueryFusionRetriever "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/retrievers/fusion_retriever.py`  
| 
```
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
297
298
299
300
301
302
303
304
```
 | 
```
classQueryFusionRetriever(BaseRetriever):
    def__init__(
        self,
        retrievers: List[BaseRetriever],
        llm: Optional[LLMType] = None,
        query_gen_prompt: Optional[str] = None,
        mode: FUSION_MODES = FUSION_MODES.SIMPLE,
        similarity_top_k: int = DEFAULT_SIMILARITY_TOP_K,
        num_queries: int = 4,
        use_async: bool = True,
        verbose: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        objects: Optional[List[IndexNode]] = None,
        object_map: Optional[dict] = None,
        retriever_weights: Optional[List[float]] = None,
    ) -> None:
        self.num_queries = num_queries
        self.query_gen_prompt = query_gen_prompt or QUERY_GEN_PROMPT
        self.similarity_top_k = similarity_top_k
        self.mode = mode
        self.use_async = use_async

        self._retrievers = retrievers
        if retriever_weights is None:
            self._retriever_weights = [1.0 / len(retrievers)] * len(retrievers)
        else:
            # Sum of retriever_weights must be 1
            total_weight = sum(retriever_weights)
            self._retriever_weights = [w / total_weight for w in retriever_weights]
        self._llm = (
            resolve_llm(llm, callback_manager=callback_manager) if llm else Settings.llm
        )
        super().__init__(
            callback_manager=callback_manager,
            object_map=object_map,
            objects=objects,
            verbose=verbose,
        )

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {"query_gen_prompt": PromptTemplate(self.query_gen_prompt)}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "query_gen_prompt" in prompts:
            self.query_gen_prompt = cast(
                PromptTemplate, prompts["query_gen_prompt"]
            ).template

    def_get_queries(self, original_query: str) -> List[QueryBundle]:
        prompt_str = self.query_gen_prompt.format(
            num_queries=self.num_queries - 1,
            query=original_query,
        )
        response = self._llm.complete(prompt_str)

        # Strip code block and assume LLM properly put each query on a newline
        queries = response.text.strip("`").split("\n")
        queries = [q.strip() for q in queries if q.strip()]
        if self._verbose:
            queries_str = "\n".join(queries)
            print(f"Generated queries:\n{queries_str}")

        # The LLM often returns more queries than we asked for, so trim the list.
        return [QueryBundle(q) for q in queries[: self.num_queries - 1]]

    def_reciprocal_rerank_fusion(
        self, results: Dict[Tuple[str, int], List[NodeWithScore]]
    ) -> List[NodeWithScore]:
"""
        Apply reciprocal rank fusion.

        The original paper uses k=60 for best results:
        https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
        """
        k = 60.0  # `k` is a parameter used to control the impact of outlier rankings.
        fused_scores = {}
        hash_to_node = {}

        # compute reciprocal rank scores
        for nodes_with_scores in results.values():
            for rank, node_with_score in enumerate(
                sorted(nodes_with_scores, key=lambda x: x.score or 0.0, reverse=True)
            ):
                hash = node_with_score.node.hash
                hash_to_node[hash] = node_with_score
                if hash not in fused_scores:
                    fused_scores[hash] = 0.0
                fused_scores[hash] += 1.0 / (rank + k)

        # sort results
        reranked_results = dict(
            sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        )

        # adjust node scores
        reranked_nodes: List[NodeWithScore] = []
        for hash, score in reranked_results.items():
            reranked_nodes.append(hash_to_node[hash])
            reranked_nodes[-1].score = score

        return reranked_nodes

    def_relative_score_fusion(
        self,
        results: Dict[Tuple[str, int], List[NodeWithScore]],
        dist_based: Optional[bool] = False,
    ) -> List[NodeWithScore]:
"""Apply relative score fusion."""
        # MinMax scale scores of each result set (highest value becomes 1, lowest becomes 0)
        # then scale by the weight of the retriever
        min_max_scores = {}
        for query_tuple, nodes_with_scores in results.items():
            if not nodes_with_scores:
                min_max_scores[query_tuple] = (0.0, 0.0)
                continue
            scores = [
                node_with_score.score or 0.0 for node_with_score in nodes_with_scores
            ]
            if dist_based:
                # Set min and max based on mean and std dev
                mean_score = sum(scores) / len(scores)
                std_dev = (
                    sum((x - mean_score) ** 2 for x in scores) / len(scores)
                ) ** 0.5
                min_score = mean_score - 3 * std_dev
                max_score = mean_score + 3 * std_dev
            else:
                min_score = min(scores)
                max_score = max(scores)
            min_max_scores[query_tuple] = (min_score, max_score)

        for query_tuple, nodes_with_scores in results.items():
            for node_with_score in nodes_with_scores:
                min_score, max_score = min_max_scores[query_tuple]
                # Scale the score to be between 0 and 1
                if max_score == min_score:
                    node_with_score.score = 1.0 if max_score  0 else 0.0
                else:
                    node_with_score.score = (node_with_score.score - min_score) / (
                        max_score - min_score
                    )
                # Scale by the weight of the retriever
                retriever_idx = query_tuple[1]
                existing_score = node_with_score.score or 0.0
                node_with_score.score = (
                    existing_score * self._retriever_weights[retriever_idx]
                )
                # Divide by the number of queries
                node_with_score.score /= self.num_queries

        # Use a dict to de-duplicate nodes
        all_nodes: Dict[str, NodeWithScore] = {}

        # Sum scores for each node
        for nodes_with_scores in results.values():
            for node_with_score in nodes_with_scores:
                hash = node_with_score.node.hash
                if hash in all_nodes:
                    cur_score = all_nodes[hash].score or 0.0
                    all_nodes[hash].score = cur_score + (node_with_score.score or 0.0)
                else:
                    all_nodes[hash] = node_with_score

        return sorted(all_nodes.values(), key=lambda x: x.score or 0.0, reverse=True)

    def_simple_fusion(
        self, results: Dict[Tuple[str, int], List[NodeWithScore]]
    ) -> List[NodeWithScore]:
"""Apply simple fusion."""
        # Use a dict to de-duplicate nodes
        all_nodes: Dict[str, NodeWithScore] = {}
        for nodes_with_scores in results.values():
            for node_with_score in nodes_with_scores:
                hash = node_with_score.node.hash
                if hash in all_nodes:
                    max_score = max(
                        node_with_score.score or 0.0, all_nodes[hash].score or 0.0
                    )
                    all_nodes[hash].score = max_score
                else:
                    all_nodes[hash] = node_with_score

        return sorted(all_nodes.values(), key=lambda x: x.score or 0.0, reverse=True)

    def_run_nested_async_queries(
        self, queries: List[QueryBundle]
    ) -> Dict[Tuple[str, int], List[NodeWithScore]]:
        tasks, task_queries = [], []
        for query in queries:
            for i, retriever in enumerate(self._retrievers):
                tasks.append(retriever.aretrieve(query))
                task_queries.append((query.query_str, i))

        task_results = run_async_tasks(tasks)

        results = {}
        for query_tuple, query_result in zip(task_queries, task_results):
            results[query_tuple] = query_result

        return results

    async def_run_async_queries(
        self, queries: List[QueryBundle]
    ) -> Dict[Tuple[str, int], List[NodeWithScore]]:
        tasks, task_queries = [], []
        for query in queries:
            for i, retriever in enumerate(self._retrievers):
                tasks.append(retriever.aretrieve(query))
                task_queries.append((query.query_str, i))

        task_results = await asyncio.gather(*tasks)

        results = {}
        for query_tuple, query_result in zip(task_queries, task_results):
            results[query_tuple] = query_result

        return results

    def_run_sync_queries(
        self, queries: List[QueryBundle]
    ) -> Dict[Tuple[str, int], List[NodeWithScore]]:
        results = {}
        for query in queries:
            for i, retriever in enumerate(self._retrievers):
                results[(query.query_str, i)] = retriever.retrieve(query)

        return results

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        queries: List[QueryBundle] = [query_bundle]
        if self.num_queries  1:
            queries.extend(self._get_queries(query_bundle.query_str))

        if self.use_async:
            results = self._run_nested_async_queries(queries)
        else:
            results = self._run_sync_queries(queries)

        if self.mode == FUSION_MODES.RECIPROCAL_RANK:
            return self._reciprocal_rerank_fusion(results)[: self.similarity_top_k]
        elif self.mode == FUSION_MODES.RELATIVE_SCORE:
            return self._relative_score_fusion(results)[: self.similarity_top_k]
        elif self.mode == FUSION_MODES.DIST_BASED_SCORE:
            return self._relative_score_fusion(results, dist_based=True)[
                : self.similarity_top_k
            ]
        elif self.mode == FUSION_MODES.SIMPLE:
            return self._simple_fusion(results)[: self.similarity_top_k]
        else:
            raise ValueError(f"Invalid fusion mode: {self.mode}")

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        queries: List[QueryBundle] = [query_bundle]
        if self.num_queries  1:
            queries.extend(self._get_queries(query_bundle.query_str))

        results = await self._run_async_queries(queries)

        if self.mode == FUSION_MODES.RECIPROCAL_RANK:
            return self._reciprocal_rerank_fusion(results)[: self.similarity_top_k]
        elif self.mode == FUSION_MODES.RELATIVE_SCORE:
            return self._relative_score_fusion(results)[: self.similarity_top_k]
        elif self.mode == FUSION_MODES.DIST_BASED_SCORE:
            return self._relative_score_fusion(results, dist_based=True)[
                : self.similarity_top_k
            ]
        elif self.mode == FUSION_MODES.SIMPLE:
            return self._simple_fusion(results)[: self.similarity_top_k]
        else:
            raise ValueError(f"Invalid fusion mode: {self.mode}")

```
 |  
| --- | --- |  
##  RecursiveRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.RecursiveRetriever "Permanent link")
Bases: 
Recursive retriever.
This retriever will recursively explore links from nodes to other retrievers/query engines.
For any retrieved nodes, if any of the nodes are IndexNodes, then it will explore the linked retriever/query engine, and query that.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `root_id`  |  The root id of the query graph.  |  _required_  |  
|  `retriever_dict`  |  `Optional[Dict[str, BaseRetriever[](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/#llama_index.core.base.base_retriever.BaseRetriever "BaseRetriever \(llama_index.core.base.base_retriever.BaseRetriever\)")]]`  |  A dictionary of id to retrievers.  |  _required_  |  
|  `query_engine_dict`  |  `Optional[Dict[str, BaseQueryEngine[](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/#llama_index.core.base.base_query_engine.BaseQueryEngine "BaseQueryEngine \(llama_index.core.base.base_query_engine.BaseQueryEngine\)")]]`  |  A dictionary of id to query engines.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/retrievers/recursive_retriever.py`  
| 
```
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
```
 | 
```
classRecursiveRetriever(BaseRetriever):
"""
    Recursive retriever.

    This retriever will recursively explore links from nodes to other
    retrievers/query engines.

    For any retrieved nodes, if any of the nodes are IndexNodes,
    then it will explore the linked retriever/query engine, and query that.

    Args:
        root_id (str): The root id of the query graph.
        retriever_dict (Optional[Dict[str, BaseRetriever]]): A dictionary
            of id to retrievers.
        query_engine_dict (Optional[Dict[str, BaseQueryEngine]]): A dictionary of
            id to query engines.

    """

    def__init__(
        self,
        root_id: str,
        retriever_dict: Dict[str, BaseRetriever],
        query_engine_dict: Optional[Dict[str, BaseQueryEngine]] = None,
        node_dict: Optional[Dict[str, BaseNode]] = None,
        callback_manager: Optional[CallbackManager] = None,
        query_response_tmpl: Optional[str] = None,
        verbose: bool = False,
    ) -> None:
"""Init params."""
        self._root_id = root_id
        if root_id not in retriever_dict:
            raise ValueError(
                f"Root id {root_id} not in retriever_dict, it must be a retriever."
            )
        self._retriever_dict = retriever_dict
        self._query_engine_dict = query_engine_dict or {}
        self._node_dict = node_dict or {}

        # make sure keys don't overlap
        if set(self._retriever_dict.keys())  set(self._query_engine_dict.keys()):
            raise ValueError("Retriever and query engine ids must not overlap.")

        self._query_response_tmpl = query_response_tmpl or DEFAULT_QUERY_RESPONSE_TMPL
        super().__init__(callback_manager, verbose=verbose)

    def_deduplicate_nodes(
        self, nodes_with_score: List[NodeWithScore]
    ) -> List[NodeWithScore]:
"""
        Deduplicate nodes according to node id.
        Keep the node with the highest score/first returned.
        """
        node_ids = set()
        deduplicate_nodes = []
        for node_with_score in nodes_with_score:
            node = node_with_score.node
            if node.id_ not in node_ids:
                node_ids.add(node.id_)
                deduplicate_nodes.append(node_with_score)
        return deduplicate_nodes

    def_query_retrieved_nodes(
        self, query_bundle: QueryBundle, nodes_with_score: List[NodeWithScore]
    ) -> Tuple[List[NodeWithScore], List[NodeWithScore]]:
"""
        Query for retrieved nodes.

        If node is an IndexNode, then recursively query the retriever/query engine.
        If node is a TextNode, then simply return the node.

        """
        nodes_to_add = []
        additional_nodes = []
        visited_ids = set()

        # dedup index nodes that reference same index id
        new_nodes_with_score = []
        for node_with_score in nodes_with_score:
            node = node_with_score.node
            if isinstance(node, IndexNode):
                if node.index_id not in visited_ids:
                    visited_ids.add(node.index_id)
                    new_nodes_with_score.append(node_with_score)
            else:
                new_nodes_with_score.append(node_with_score)

        nodes_with_score = new_nodes_with_score

        # recursively retrieve
        for node_with_score in nodes_with_score:
            node = node_with_score.node
            if isinstance(node, IndexNode):
                if self._verbose:
                    print_text(
                        f"Retrieved node with id, entering: {node.index_id}\n",
                        color="pink",
                    )
                cur_retrieved_nodes, cur_additional_nodes = self._retrieve_rec(
                    query_bundle,
                    query_id=node.index_id,
                    cur_similarity=node_with_score.score,
                )
            else:
                assert isinstance(node, TextNode)
                if self._verbose:
                    print_text(
                        f"Retrieving text node: {node.get_content()}\n",
                        color="pink",
                    )
                cur_retrieved_nodes = [node_with_score]
                cur_additional_nodes = []
            nodes_to_add.extend(cur_retrieved_nodes)
            additional_nodes.extend(cur_additional_nodes)

        # dedup nodes in case some nodes could be retrieved from multiple sources
        nodes_to_add = self._deduplicate_nodes(nodes_to_add)
        additional_nodes = self._deduplicate_nodes(additional_nodes)
        return nodes_to_add, additional_nodes

    def_get_object(self, query_id: str) -> RQN_TYPE:
"""Fetch retriever or query engine."""
        node = self._node_dict.get(query_id, None)
        if node is not None:
            return node
        retriever = self._retriever_dict.get(query_id, None)
        if retriever is not None:
            return retriever
        query_engine = self._query_engine_dict.get(query_id, None)
        if query_engine is not None:
            return query_engine
        raise ValueError(
            f"Query id {query_id} not found in either `retriever_dict` "
            "or `query_engine_dict`."
        )

    def_retrieve_rec(
        self,
        query_bundle: QueryBundle,
        query_id: Optional[str] = None,
        cur_similarity: Optional[float] = None,
    ) -> Tuple[List[NodeWithScore], List[NodeWithScore]]:
"""Query recursively."""
        if self._verbose:
            print_text(
                f"Retrieving with query id {query_id}: {query_bundle.query_str}\n",
                color="blue",
            )
        query_id = query_id or self._root_id
        cur_similarity = cur_similarity or 1.0

        obj = self._get_object(query_id)
        if isinstance(obj, BaseNode):
            nodes_to_add = [NodeWithScore(node=obj, score=cur_similarity)]
            additional_nodes: List[NodeWithScore] = []
        elif isinstance(obj, BaseRetriever):
            with self.callback_manager.event(
                CBEventType.RETRIEVE,
                payload={EventPayload.QUERY_STR: query_bundle.query_str},
            ) as event:
                nodes = obj.retrieve(query_bundle)
                event.on_end(payload={EventPayload.NODES: nodes})

            nodes_to_add, additional_nodes = self._query_retrieved_nodes(
                query_bundle, nodes
            )

        elif isinstance(obj, BaseQueryEngine):
            sub_resp = obj.query(query_bundle)
            if self._verbose:
                print_text(
                    f"Got response: {sub_resp!s}\n",
                    color="green",
                )
            # format with both the query and the response
            node_text = self._query_response_tmpl.format(
                query_str=query_bundle.query_str, response=str(sub_resp)
            )
            node = TextNode(text=node_text)
            nodes_to_add = [NodeWithScore(node=node, score=cur_similarity)]
            additional_nodes = sub_resp.source_nodes
        else:
            raise ValueError("Must be a retriever or query engine.")

        return nodes_to_add, additional_nodes

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        retrieved_nodes, _ = self._retrieve_rec(query_bundle, query_id=None)
        return retrieved_nodes

    defretrieve_all(
        self, query_bundle: QueryBundle
    ) -> Tuple[List[NodeWithScore], List[NodeWithScore]]:
"""
        Retrieve all nodes.

        Unlike default `retrieve` method, this also fetches additional sources.

        """
        return self._retrieve_rec(query_bundle, query_id=None)

```
 |  
| --- | --- |  
###  retrieve_all [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.RecursiveRetriever.retrieve_all "Permanent link")

```
retrieve_all(
    query_bundle: ,
) -> Tuple[[], []]

```

Retrieve all nodes.
Unlike default `retrieve` method, this also fetches additional sources.
Source code in `llama-index-core/llama_index/core/retrievers/recursive_retriever.py`  
| 
```
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
```
 | 
```
defretrieve_all(
    self, query_bundle: QueryBundle
) -> Tuple[List[NodeWithScore], List[NodeWithScore]]:
"""
    Retrieve all nodes.

    Unlike default `retrieve` method, this also fetches additional sources.

    """
    return self._retrieve_rec(query_bundle, query_id=None)

```
 |  
| --- | --- |  
##  RouterRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.RouterRetriever "Permanent link")
Bases: 
Router retriever.
Selects one (or multiple) out of several candidate retrievers to execute a query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  `BaseSelector`  |  A selector that chooses one out of many options based on each candidate's metadata and query.  |  _required_  |  
|  `retriever_tools`  |  `Sequence[RetrieverTool[](https://developers.llamaindex.ai/python/framework-api-reference/tools/retriever/#llama_index.core.tools.retriever_tool.RetrieverTool "RetrieverTool \(llama_index.core.tools.retriever_tool.RetrieverTool\)")]`  |  A sequence of candidate retrievers. They must be wrapped as tools to expose metadata to the selector.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/retrievers/router_retriever.py`  
| 
```
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
```
 | 
```
classRouterRetriever(BaseRetriever):
"""
    Router retriever.

    Selects one (or multiple) out of several candidate retrievers to execute a query.

    Args:
        selector (BaseSelector): A selector that chooses one out of many options based
            on each candidate's metadata and query.
        retriever_tools (Sequence[RetrieverTool]): A sequence of candidate
            retrievers. They must be wrapped as tools to expose metadata to
            the selector.

    """

    def__init__(
        self,
        selector: BaseSelector,
        retriever_tools: Sequence[RetrieverTool],
        llm: Optional[LLM] = None,
        objects: Optional[List[IndexNode]] = None,
        object_map: Optional[dict] = None,
        verbose: bool = False,
    ) -> None:
        self._llm = llm or Settings.llm
        self._selector = selector
        self._retrievers: List[BaseRetriever] = [x.retriever for x in retriever_tools]
        self._metadatas = [x.metadata for x in retriever_tools]

        super().__init__(
            callback_manager=Settings.callback_manager,
            object_map=object_map,
            objects=objects,
            verbose=verbose,
        )

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        # NOTE: don't include tools for now
        return {"selector": self._selector}

    @classmethod
    deffrom_defaults(
        cls,
        retriever_tools: Sequence[RetrieverTool],
        llm: Optional[LLM] = None,
        selector: Optional[BaseSelector] = None,
        select_multi: bool = False,
    ) -> "RouterRetriever":
        llm = llm or Settings.llm
        selector = selector or get_selector_from_llm(llm, is_multi=select_multi)

        return cls(
            selector,
            retriever_tools,
            llm=llm,
        )

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        with self.callback_manager.event(
            CBEventType.RETRIEVE,
            payload={EventPayload.QUERY_STR: query_bundle.query_str},
        ) as query_event:
            result = self._selector.select(self._metadatas, query_bundle)

            if len(result.inds)  1:
                retrieved_results = {}
                for i, engine_ind in enumerate(result.inds):
                    logger.info(
                        f"Selecting retriever {engine_ind}: {result.reasons[i]}."
                    )
                    selected_retriever = self._retrievers[engine_ind]
                    cur_results = selected_retriever.retrieve(query_bundle)
                    retrieved_results.update({n.node.node_id: n for n in cur_results})
            else:
                try:
                    selected_retriever = self._retrievers[result.ind]
                    logger.info(f"Selecting retriever {result.ind}: {result.reason}.")
                except ValueError as e:
                    raise ValueError("Failed to select retriever") frome

                cur_results = selected_retriever.retrieve(query_bundle)
                retrieved_results = {n.node.node_id: n for n in cur_results}

            query_event.on_end(payload={EventPayload.NODES: retrieved_results.values()})

        return list(retrieved_results.values())

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        with self.callback_manager.event(
            CBEventType.RETRIEVE,
            payload={EventPayload.QUERY_STR: query_bundle.query_str},
        ) as query_event:
            result = await self._selector.aselect(self._metadatas, query_bundle)

            if len(result.inds)  1:
                retrieved_results = {}
                tasks = []
                for i, engine_ind in enumerate(result.inds):
                    logger.info(
                        f"Selecting retriever {engine_ind}: {result.reasons[i]}."
                    )
                    selected_retriever = self._retrievers[engine_ind]
                    tasks.append(selected_retriever.aretrieve(query_bundle))

                results_of_results = await asyncio.gather(*tasks)
                cur_results = [
                    item for sublist in results_of_results for item in sublist
                ]
                retrieved_results.update({n.node.node_id: n for n in cur_results})
            else:
                try:
                    selected_retriever = self._retrievers[result.ind]
                    logger.info(f"Selecting retriever {result.ind}: {result.reason}.")
                except ValueError as e:
                    raise ValueError("Failed to select retriever") frome

                cur_results = await selected_retriever.aretrieve(query_bundle)
                retrieved_results = {n.node.node_id: n for n in cur_results}

            query_event.on_end(payload={EventPayload.NODES: retrieved_results.values()})

        return list(retrieved_results.values())

```
 |  
| --- | --- |  
##  TransformRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/sql/#llama_index.core.retrievers.TransformRetriever "Permanent link")
Bases: 
Transform Retriever.
Takes in an existing retriever and a query transform and runs the query transform before running the retriever.
Source code in `llama-index-core/llama_index/core/retrievers/transform_retriever.py`  
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
```
 | 
```
classTransformRetriever(BaseRetriever):
"""
    Transform Retriever.

    Takes in an existing retriever and a query transform and runs the query transform
    before running the retriever.

    """

    def__init__(
        self,
        retriever: BaseRetriever,
        query_transform: BaseQueryTransform,
        transform_metadata: Optional[dict] = None,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        verbose: bool = False,
    ) -> None:
        self._retriever = retriever
        self._query_transform = query_transform
        self._transform_metadata = transform_metadata
        super().__init__(
            callback_manager=callback_manager, object_map=object_map, verbose=verbose
        )

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        # NOTE: don't include tools for now
        return {"query_transform": self._query_transform}

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        query_bundle = self._query_transform.run(
            query_bundle, metadata=self._transform_metadata
        )
        return self._retriever.retrieve(query_bundle)

```
 |  
| --- | --- |  
options: members: - NLSQLRetriever - SQLParserMode - SQLRetriever
