# Vertexai search
##  VertexAISearchRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/vertexai_search/#llama_index.retrievers.vertexai_search.VertexAISearchRetriever "Permanent link")
Bases: 
`Vertex AI Search` retrieval.
For a detailed explanation of the Vertex AI Search concepts and configuration parameters, refer to the product documentation. https://cloud.google.com/generative-ai-app-builder/docs/enterprise-search-introduction
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `project_id`  |  _required_  |  
|  `data_store_id`  |  _required_  |  
|  `location_id`  |  str = "global"  |  `'global'`  |  
|  `serving_config_id`  |  str = "default_config"  |  `'default_config'`  |  
|  `credentials`  |  Any = None  |  `None`  |  
|  `engine_data_type`  |  int = 0  |  
Example
retriever = VertexAISearchRetriever( project_id=PROJECT_ID, data_store_id=DATA_STORE_ID, location_id=LOCATION_ID, engine_data_type=0 )
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-vertexai-search/llama_index/retrievers/vertexai_search/base.py`  
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
```
 | 
```
classVertexAISearchRetriever(BaseRetriever):
"""
    `Vertex AI Search` retrieval.

    For a detailed explanation of the Vertex AI Search concepts
    and configuration parameters, refer to the product documentation.
    https://cloud.google.com/generative-ai-app-builder/docs/enterprise-search-introduction

    Args:
        project_id: str
        #Google Cloud Project ID

        data_store_id: str
        #Vertex AI Search data store ID.

        location_id: str = "global"
        #Vertex AI Search data store location.

        serving_config_id: str = "default_config"
        #Vertex AI Search serving config ID

        credentials: Any = None
        The default custom credentials (google.auth.credentials.Credentials) to use
        when making API calls. If not provided, credentials will be ascertained from
        the environment

        engine_data_type: int = 0
        Defines the Vertex AI Search data type
        0 - Unstructured data
        1 - Structured data
        2 - Website data

    Example:
        retriever = VertexAISearchRetriever(
            project_id=PROJECT_ID,
            data_store_id=DATA_STORE_ID,
            location_id=LOCATION_ID,
            engine_data_type=0


    """

"""
    The following parameter explanation can be found here:
    https://cloud.google.com/generative-ai-app-builder/docs/reference/rpc/google.cloud.discoveryengine.v1#contentsearchspec
    """
    filter: Optional[str] = None
"""Filter expression."""
    get_extractive_answers: bool = False
"""If True return Extractive Answers, otherwise return Extractive Segments or Snippets."""
    max_documents: int = 5
"""The maximum number of documents to return."""
    max_extractive_answer_count: int = 1
"""The maximum number of extractive answers returned in each search result.
    At most 5 answers will be returned for each SearchResult.
    """
    max_extractive_segment_count: int = 1
"""The maximum number of extractive segments returned in each search result.
    Currently one segment will be returned for each SearchResult.
    """
    query_expansion_condition: int = 1
"""Specification to determine under which conditions query expansion should occur.
    0 - Unspecified query expansion condition. In this case, server behavior defaults
        to disabled
    1 - Disabled query expansion. Only the exact search query is used, even if
        SearchResponse.total_size is zero.
    2 - Automatic query expansion built by the Search API.
    """
    spell_correction_mode: int = 1
"""Specification to determine under which conditions query expansion should occur.
    0 - Unspecified spell correction mode. In this case, server behavior defaults
        to auto.
    1 - Suggestion only. Search API will try to find a spell suggestion if there is any
        and put in the `SearchResponse.corrected_query`.
        The spell suggestion will not be used as the search query.
    2 - Automatic spell correction built by the Search API.
        Search will be based on the corrected query if found.
    """
    boost_spec: Optional[Dict[Any, Any]] = None
"""BoostSpec for boosting search results. A protobuf should be provided.
    https://cloud.google.com/generative-ai-app-builder/docs/boost-search-results
    https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1beta/BoostSpec
    """
    return_extractive_segment_score: bool = True
"""
    Specifies whether to return the confidence score from the extractive segments in each search result.
    This feature is available only for new or allowlisted data stores.
    """

    _client: SearchServiceClient
    _serving_config: str

    def__init__(
        self,
        project_id: str,
        data_store_id: str,
        location_id: str = "global",
        serving_config_id: str = "default_config",
        credentials: Any = None,
        engine_data_type: int = 0,
        max_documents: int = 5,
        user_agent: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
"""Initializes private fields."""
        self.project_id = project_id
        self.location_id = location_id
        self.data_store_id = data_store_id
        self.serving_config_id = serving_config_id
        self.engine_data_type = engine_data_type
        self.credentials = credentials
        self.max_documents = max_documents
        self._user_agent = user_agent or "llama-index/0.0.0"

        self.client_options = ClientOptions(
            api_endpoint=(
                f"{self.location_id}-discoveryengine.googleapis.com"
                if self.location_id != "global"
                else None
            )
        )

        try:
            fromgoogle.cloud.discoveryengine_v1betaimport SearchServiceClient
        except ImportError as exc:
            raise ImportError(
                "Could not import google-cloud-discoveryengine python package. "
                "Please, install vertexaisearch dependency group: "
            ) fromexc

        try:
            super().__init__(**kwargs)
        except ValueError as e:
            print(f"Error initializing GoogleVertexAISearchRetriever: {e!s}")
            raise

        #  For more information, refer to:
        # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store

        self._client = SearchServiceClient(
            credentials=self.credentials,
            client_options=self.client_options,
            client_info=get_client_info(module="vertex-ai-search"),
        )

        self._serving_config = self._client.serving_config_path(
            project=self.project_id,
            location=self.location_id,
            data_store=self.data_store_id,
            serving_config=self.serving_config_id,
        )

    def_get_content_spec_kwargs(self) -> Optional[Dict[str, Any]]:
"""Prepares a ContentSpec object."""
        fromgoogle.cloud.discoveryengine_v1betaimport SearchRequest

        if self.engine_data_type == 0:
            if self.get_extractive_answers:
                extractive_content_spec = SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
                    max_extractive_answer_count=self.max_extractive_answer_count,
                    return_extractive_segment_score=self.return_extractive_segment_score,
                )
            else:
                extractive_content_spec = SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
                    max_extractive_segment_count=self.max_extractive_segment_count,
                    return_extractive_segment_score=self.return_extractive_segment_score,
                )
            content_search_spec = {"extractive_content_spec": extractive_content_spec}
        elif self.engine_data_type == 1:
            content_search_spec = None
        elif self.engine_data_type == 2:
            content_search_spec = {
                "extractive_content_spec": SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
                    max_extractive_segment_count=self.max_extractive_segment_count,
                    max_extractive_answer_count=self.max_extractive_answer_count,
                    return_extractive_segment_score=self.return_extractive_segment_score,
                ),
                "snippet_spec": SearchRequest.ContentSearchSpec.SnippetSpec(
                    return_snippet=True
                ),
            }
        else:
            raise NotImplementedError(
                "Only data store type 0 (Unstructured), 1 (Structured),"
                "or 2 (Website) are supported currently."
                + f" Got {self.engine_data_type}"
            )
        return content_search_spec

    def_create_search_request(self, query: str) -> SearchRequest:
"""Prepares a SearchRequest object."""
        fromgoogle.cloud.discoveryengine_v1betaimport SearchRequest

        query_expansion_spec = SearchRequest.QueryExpansionSpec(
            condition=self.query_expansion_condition,
        )

        spell_correction_spec = SearchRequest.SpellCorrectionSpec(
            mode=self.spell_correction_mode
        )

        content_search_spec_kwargs = self._get_content_spec_kwargs()

        if content_search_spec_kwargs is not None:
            content_search_spec = SearchRequest.ContentSearchSpec(
                **content_search_spec_kwargs
            )
        else:
            content_search_spec = None

        return SearchRequest(
            query=query,
            filter=self.filter,
            serving_config=self._serving_config,
            page_size=self.max_documents,
            content_search_spec=content_search_spec,
            query_expansion_spec=query_expansion_spec,
            spell_correction_spec=spell_correction_spec,
            boost_spec=SearchRequest.BoostSpec(**self.boost_spec)
            if self.boost_spec
            else None,
        )

    def_convert_structured_datastore_response(
        self, results: Sequence[SearchResult]
    ) -> List[NodeWithScore]:
"""Converts a sequence of search results to a list of Llamaindex note_with_score."""
        note_with_score: List[NodeWithScore] = []

        for i, result in enumerate(results):
            # Structured datastore does not have relevance score. The results are ranked
            # in order. score is calculated by below. Index 0 has the highest score
            score = (len(results) - i) / len(results)

            document_dict = MessageToDict(
                result.document._pb, preserving_proto_field_name=True
            )
            note_with_score.append(
                NodeWithScore(
                    node=TextNode(
                        text=json.dumps(document_dict.get("struct_data", {}))
                    ),
                    score=score,
                )
            )

        return note_with_score

    def_convert_unstructured_datastore_response(
        self, results: Sequence[SearchResult], chunk_type: str
    ) -> List[NodeWithScore]:
"""Converts a sequence of search results to a list of LLamaindex note_with_score."""
        note_with_score: List[NodeWithScore] = []

        for result in results:
            document_dict = MessageToDict(
                result.document._pb, preserving_proto_field_name=True
            )
            derived_struct_data = document_dict.get("derived_struct_data")
            if not derived_struct_data:
                continue

            if chunk_type not in derived_struct_data:
                continue

            for chunk in derived_struct_data[chunk_type]:
                score = chunk.get("relevanceScore", 0)
                note_with_score.append(
                    NodeWithScore(
                        node=TextNode(text=chunk.get("content", "")),
                        score=score,
                    )
                )

        return note_with_score

    def_convert_website_datastore_response(
        self, results: Sequence[SearchResult], chunk_type: str
    ) -> List[NodeWithScore]:
"""Converts a sequence of search results to a list of LLamaindex note_with_score."""
        note_with_score: List[NodeWithScore] = []

        for result in results:
            document_dict = MessageToDict(
                result.document._pb, preserving_proto_field_name=True
            )

            derived_struct_data = document_dict.get("derived_struct_data")
            if not derived_struct_data:
                continue

            if chunk_type not in derived_struct_data:
                continue

            text_field = "snippet" if chunk_type == "snippets" else "content"

            for chunk in derived_struct_data[chunk_type]:
                score = chunk.get("relevanceScore", 0)
                note_with_score.append(
                    NodeWithScore(
                        node=TextNode(text=chunk.get(text_field, "")),
                        score=score,
                    )
                )

        if not note_with_score:
            print(f"No {chunk_type} could be found.")
            if chunk_type == "extractive_answers":
                print(
                    "Make sure that your data store is using Advanced Website "
                    "Indexing.\n"
                    "https://cloud.google.com/generative-ai-app-builder/docs/about-advanced-features#advanced-website-indexing"
                )

        return note_with_score

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve from the platform."""
"""Get note_with_score relevant for a query."""

        search_request = self._create_search_request(query_bundle.query_str)

        try:
            response = self._client.search(search_request)
        except InvalidArgument as exc:
            raise type(exc)(
                exc.message
                + " This might be due to engine_data_type not set correctly."
            )

        if self.engine_data_type == 0:
            chunk_type = (
                "extractive_answers"
                if self.get_extractive_answers
                else "extractive_segments"
            )
            note_with_score = self._convert_unstructured_datastore_response(
                response.results, chunk_type
            )
        elif self.engine_data_type == 1:
            note_with_score = self._convert_structured_datastore_response(
                response.results
            )
        elif self.engine_data_type == 2:
            chunk_type = (
                "extractive_answers"
                if self.get_extractive_answers
                else "extractive_segments"
            )
            note_with_score = self._convert_website_datastore_response(
                response.results, chunk_type
            )
        else:
            raise NotImplementedError(
                "Only data store type 0 (Unstructured), 1 (Structured),"
                "or 2 (Website) are supported currently."
                + f" Got {self.engine_data_type}"
            )

        return note_with_score

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Asynchronously retrieve from the platform."""
        return self._retrieve(query_bundle=query_bundle)

```
 |  
| --- | --- |  
###  filter `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/vertexai_search/#llama_index.retrievers.vertexai_search.VertexAISearchRetriever.filter "Permanent link")

```
filter: Optional[] = None

```

Filter expression.
###  get_extractive_answers `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/vertexai_search/#llama_index.retrievers.vertexai_search.VertexAISearchRetriever.get_extractive_answers "Permanent link")

```
get_extractive_answers:  = False

```

If True return Extractive Answers, otherwise return Extractive Segments or Snippets.
###  max_documents `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/vertexai_search/#llama_index.retrievers.vertexai_search.VertexAISearchRetriever.max_documents "Permanent link")

```
max_documents:  = max_documents

```

The maximum number of documents to return.
###  max_extractive_answer_count `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/vertexai_search/#llama_index.retrievers.vertexai_search.VertexAISearchRetriever.max_extractive_answer_count "Permanent link")

```
max_extractive_answer_count:  = 1

```

The maximum number of extractive answers returned in each search result. At most 5 answers will be returned for each SearchResult.
###  max_extractive_segment_count `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/vertexai_search/#llama_index.retrievers.vertexai_search.VertexAISearchRetriever.max_extractive_segment_count "Permanent link")

```
max_extractive_segment_count:  = 1

```

The maximum number of extractive segments returned in each search result. Currently one segment will be returned for each SearchResult.
###  query_expansion_condition `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/vertexai_search/#llama_index.retrievers.vertexai_search.VertexAISearchRetriever.query_expansion_condition "Permanent link")

```
query_expansion_condition:  = 1

```

Specification to determine under which conditions query expansion should occur. 0 - Unspecified query expansion condition. In this case, server behavior defaults to disabled 1 - Disabled query expansion. Only the exact search query is used, even if SearchResponse.total_size is zero. 2 - Automatic query expansion built by the Search API.
###  spell_correction_mode `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/vertexai_search/#llama_index.retrievers.vertexai_search.VertexAISearchRetriever.spell_correction_mode "Permanent link")

```
spell_correction_mode:  = 1

```

Specification to determine under which conditions query expansion should occur. 0 - Unspecified spell correction mode. In this case, server behavior defaults to auto. 1 - Suggestion only. Search API will try to find a spell suggestion if there is any and put in the `SearchResponse.corrected_query`. The spell suggestion will not be used as the search query. 2 - Automatic spell correction built by the Search API. Search will be based on the corrected query if found.
###  boost_spec `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/vertexai_search/#llama_index.retrievers.vertexai_search.VertexAISearchRetriever.boost_spec "Permanent link")

```
boost_spec: Optional[[, ]] = None

```

BoostSpec for boosting search results. A protobuf should be provided. https://cloud.google.com/generative-ai-app-builder/docs/boost-search-results https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1beta/BoostSpec
###  return_extractive_segment_score `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/vertexai_search/#llama_index.retrievers.vertexai_search.VertexAISearchRetriever.return_extractive_segment_score "Permanent link")

```
return_extractive_segment_score:  = True

```

Specifies whether to return the confidence score from the extractive segments in each search result. This feature is available only for new or allowlisted data stores.
options: members: - VertexAISearchRetriever
