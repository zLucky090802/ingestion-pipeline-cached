# Airweave
Airweave tool integration for LlamaIndex.
##  AirweaveToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/airweave/#llama_index.tools.airweave.AirweaveToolSpec "Permanent link")
Bases: 
Airweave tool spec for searching collections.
Airweave is an open-source platform that makes any app searchable for your agent by syncing data from various sources.
To use this tool, you need: 1. An Airweave account and API key 2. At least one collection set up with data
Get started at https://airweave.ai/
Source code in `llama-index-integrations/tools/llama-index-tools-airweave/llama_index/tools/airweave/base.py`  
| 
```
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
```
 | 
```
classAirweaveToolSpec(BaseToolSpec):
"""
    Airweave tool spec for searching collections.

    Airweave is an open-source platform that makes any app searchable
    for your agent by syncing data from various sources.

    To use this tool, you need:
    1. An Airweave account and API key
    2. At least one collection set up with data

    Get started at https://airweave.ai/
    """

    spec_functions = [
        "search_collection",
        "advanced_search_collection",
        "search_and_generate_answer",
        "list_collections",
        "get_collection_info",
    ]

    def__init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        framework_name: str = "llamaindex",
        framework_version: str = "0.1.0",
    ) -> None:
"""
        Initialize with Airweave API credentials.

        Args:
            api_key: Your Airweave API key from the dashboard
            base_url: Optional custom base URL for self-hosted instances
            framework_name: Framework name for analytics (default: "llamaindex")
            framework_version: Framework version for analytics

        """
        init_kwargs: Dict[str, Any] = {
            "api_key": api_key,
            "framework_name": framework_name,
            "framework_version": framework_version,
        }

        if base_url:
            init_kwargs["base_url"] = base_url

        self.client = AirweaveSDK(**init_kwargs)

    defsearch_collection(
        self,
        collection_id: str,
        query: str,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ) -> List[Document]:
"""
        Search a specific Airweave collection with a natural language query.

        This is a simple search function for common use cases. For advanced
        options like reranking or answer generation, use advanced_search_collection.

        Args:
            collection_id: The readable ID of the collection to search
                          (e.g., 'finance-data-ab123')
            query: The search query in natural language
            limit: Maximum number of results to return (default: 10)
            offset: Number of results to skip for pagination (default: 0)

        Returns:
            List of Document objects containing search results with metadata

        """
        response = self.client.collections.search(
            readable_id=collection_id,
            request=SearchRequest(query=query, limit=limit, offset=offset),
        )

        return self._parse_search_response(response, collection_id)

    defadvanced_search_collection(
        self,
        collection_id: str,
        query: str,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        retrieval_strategy: Optional[str] = None,
        temporal_relevance: Optional[float] = None,
        expand_query: Optional[bool] = None,
        interpret_filters: Optional[bool] = None,
        rerank: Optional[bool] = None,
        generate_answer: Optional[bool] = None,
    ) -> Dict[str, Any]:
"""
        Advanced search with full control over retrieval parameters.

        Args:
            collection_id: The readable ID of the collection
            query: The search query in natural language
            limit: Maximum number of results to return (default: 10)
            offset: Number of results to skip for pagination (default: 0)
            retrieval_strategy: Search strategy - "hybrid", "neural", or "keyword"
                              - hybrid: combines semantic and keyword search (default)
                              - neural: pure semantic/embedding search
                              - keyword: traditional BM25 keyword search
            temporal_relevance: Weight recent content higher (0.0-1.0)
                              0.0 = no recency bias, 1.0 = only recent matters
            expand_query: Generate query variations for better recall
            interpret_filters: Extract structured filters from natural language
            rerank: Use LLM-based reranking for improved relevance
            generate_answer: Generate a natural language answer from results

        Returns:
            Dictionary with 'documents' list and optional 'answer' field
            Example: {"documents": [...], "answer": "Generated answer text"}

        """
        search_params: Dict[str, Any] = {
            "query": query,
            "limit": limit,
            "offset": offset,
        }

        # Add optional parameters
        if retrieval_strategy:
            search_params["retrieval_strategy"] = retrieval_strategy
        if temporal_relevance is not None:
            search_params["temporal_relevance"] = temporal_relevance
        if expand_query is not None:
            search_params["expand_query"] = expand_query
        if interpret_filters is not None:
            search_params["interpret_filters"] = interpret_filters
        if rerank is not None:
            search_params["rerank"] = rerank
        if generate_answer is not None:
            search_params["generate_answer"] = generate_answer

        response = self.client.collections.search(
            readable_id=collection_id,
            request=SearchRequest(**search_params),
        )

        result: Dict[str, Any] = {
            "documents": self._parse_search_response(response, collection_id),
        }

        # Add generated answer if available
        if hasattr(response, "completion") and response.completion:
            result["answer"] = response.completion

        return result

    defsearch_and_generate_answer(
        self,
        collection_id: str,
        query: str,
        limit: Optional[int] = 10,
        use_reranking: bool = True,
    ) -> Optional[str]:
"""
        Search collection and generate a natural language answer (RAG-style).

        This is a convenience method that combines search with answer generation,
        perfect for agents that need direct answers rather than raw documents.

        Args:
            collection_id: The readable ID of the collection
            query: The search query / question in natural language
            limit: Maximum number of results to consider (default: 10)
            use_reranking: Whether to use LLM reranking (default: True)

        Returns:
            Natural language answer generated from the search results,
            or None if no answer could be generated (with a warning)

        """
        response = self.client.collections.search(
            readable_id=collection_id,
            request=SearchRequest(
                query=query,
                limit=limit,
                generate_answer=True,
                rerank=use_reranking,
            ),
        )

        if hasattr(response, "completion") and response.completion:
            return response.completion
        else:
            # Fallback if no answer generated
            warnings.warn(
                "No answer could be generated from the search results", UserWarning
            )
            return None

    def_parse_search_response(
        self, response: Any, collection_id: str
    ) -> List[Document]:
"""Parse Airweave search response into LlamaIndex Documents."""
        documents = []

        if hasattr(response, "results") and response.results:
            for result in response.results:
                # Extract text content
                text_content = ""
                if isinstance(result, dict):
                    text_content = (
                        result.get("content") or result.get("text") or str(result)
                    )
                elif hasattr(result, "content"):
                    text_content = result.content
                elif hasattr(result, "text"):
                    text_content = result.text
                else:
                    text_content = str(result)

                # Build metadata
                metadata: Dict[str, Any] = {"collection_id": collection_id}

                if isinstance(result, dict):
                    if "metadata" in result:
                        metadata.update(result["metadata"])
                    if "score" in result:
                        metadata["score"] = result["score"]
                    if "source" in result:
                        metadata["source"] = result["source"]
                    if "id" in result:
                        metadata["result_id"] = result["id"]
                else:
                    if hasattr(result, "metadata") and result.metadata:
                        metadata.update(result.metadata)
                    if hasattr(result, "score"):
                        metadata["score"] = result.score
                    if hasattr(result, "source"):
                        metadata["source"] = result.source
                    if hasattr(result, "id"):
                        metadata["result_id"] = result.id

                documents.append(Document(text=text_content, metadata=metadata))

        return documents

    deflist_collections(
        self,
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
    ) -> List[Dict[str, Any]]:
"""
        List all collections available in your Airweave organization.

        Useful for discovering what collections are available to search.

        Args:
            skip: Number of collections to skip for pagination (default: 0)
            limit: Maximum number of collections to return, 1-1000 (default: 100)

        Returns:
            List of dictionaries with collection information

        """
        collections = self.client.collections.list(skip=skip, limit=limit)

        return [
            {
                "id": (
                    coll.readable_id if hasattr(coll, "readable_id") else str(coll.id)
                ),
                "name": coll.name,
                "created_at": (
                    str(coll.created_at) if hasattr(coll, "created_at") else None
                ),
            }
            for coll in collections
        ]

    defget_collection_info(self, collection_id: str) -> Dict[str, Any]:
"""
        Get detailed information about a specific collection.

        Args:
            collection_id: The readable ID of the collection

        Returns:
            Dictionary with detailed collection information

        """
        collection = self.client.collections.get(readable_id=collection_id)

        return {
            "id": (
                collection.readable_id
                if hasattr(collection, "readable_id")
                else str(collection.id)
            ),
            "name": collection.name,
            "created_at": (
                str(collection.created_at)
                if hasattr(collection, "created_at")
                else None
            ),
            "description": getattr(collection, "description", None),
        }

```
 |  
| --- | --- |  
###  search_collection [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/airweave/#llama_index.tools.airweave.AirweaveToolSpec.search_collection "Permanent link")

```
search_collection(
    collection_id: ,
    query: ,
    limit: Optional[] = 10,
    offset: Optional[] = 0,
) -> []

```

Search a specific Airweave collection with a natural language query.
This is a simple search function for common use cases. For advanced options like reranking or answer generation, use advanced_search_collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_id`  |  The readable ID of the collection to search (e.g., 'finance-data-ab123')  |  _required_  |  
|  `query`  |  The search query in natural language  |  _required_  |  
|  `limit`  |  `Optional[int]`  |  Maximum number of results to return (default: 10)  |  
|  `offset`  |  `Optional[int]`  |  Number of results to skip for pagination (default: 0)  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List of Document objects containing search results with metadata  |  
Source code in `llama-index-integrations/tools/llama-index-tools-airweave/llama_index/tools/airweave/base.py`  
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
```
 | 
```
defsearch_collection(
    self,
    collection_id: str,
    query: str,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
) -> List[Document]:
"""
    Search a specific Airweave collection with a natural language query.

    This is a simple search function for common use cases. For advanced
    options like reranking or answer generation, use advanced_search_collection.

    Args:
        collection_id: The readable ID of the collection to search
                      (e.g., 'finance-data-ab123')
        query: The search query in natural language
        limit: Maximum number of results to return (default: 10)
        offset: Number of results to skip for pagination (default: 0)

    Returns:
        List of Document objects containing search results with metadata

    """
    response = self.client.collections.search(
        readable_id=collection_id,
        request=SearchRequest(query=query, limit=limit, offset=offset),
    )

    return self._parse_search_response(response, collection_id)

```
 |  
| --- | --- |  
###  advanced_search_collection [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/airweave/#llama_index.tools.airweave.AirweaveToolSpec.advanced_search_collection "Permanent link")

```
advanced_search_collection(
    collection_id: ,
    query: ,
    limit: Optional[] = 10,
    offset: Optional[] = 0,
    retrieval_strategy: Optional[] = None,
    temporal_relevance: Optional[float] = None,
    expand_query: Optional[] = None,
    interpret_filters: Optional[] = None,
    rerank: Optional[] = None,
    generate_answer: Optional[] = None,
) -> [, ]

```

Advanced search with full control over retrieval parameters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_id`  |  The readable ID of the collection  |  _required_  |  
|  `query`  |  The search query in natural language  |  _required_  |  
|  `limit`  |  `Optional[int]`  |  Maximum number of results to return (default: 10)  |  
|  `offset`  |  `Optional[int]`  |  Number of results to skip for pagination (default: 0)  |  
|  `retrieval_strategy`  |  `Optional[str]`  |  Search strategy - "hybrid", "neural", or "keyword" - hybrid: combines semantic and keyword search (default) - neural: pure semantic/embedding search - keyword: traditional BM25 keyword search  |  `None`  |  
|  `temporal_relevance`  |  `Optional[float]`  |  Weight recent content higher (0.0-1.0) 0.0 = no recency bias, 1.0 = only recent matters  |  `None`  |  
|  `expand_query`  |  `Optional[bool]`  |  Generate query variations for better recall  |  `None`  |  
|  `interpret_filters`  |  `Optional[bool]`  |  Extract structured filters from natural language  |  `None`  |  
|  `rerank`  |  `Optional[bool]`  |  Use LLM-based reranking for improved relevance  |  `None`  |  
|  `generate_answer`  |  `Optional[bool]`  |  Generate a natural language answer from results  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
|  `Dict[str, Any]`  |  Dictionary with 'documents' list and optional 'answer' field  |  
| `Example`  |  `Dict[str, Any]`  |  {"documents": [...], "answer": "Generated answer text"}  |  
Source code in `llama-index-integrations/tools/llama-index-tools-airweave/llama_index/tools/airweave/base.py`  
| 
```
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
```
 | 
```
defadvanced_search_collection(
    self,
    collection_id: str,
    query: str,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    retrieval_strategy: Optional[str] = None,
    temporal_relevance: Optional[float] = None,
    expand_query: Optional[bool] = None,
    interpret_filters: Optional[bool] = None,
    rerank: Optional[bool] = None,
    generate_answer: Optional[bool] = None,
) -> Dict[str, Any]:
"""
    Advanced search with full control over retrieval parameters.

    Args:
        collection_id: The readable ID of the collection
        query: The search query in natural language
        limit: Maximum number of results to return (default: 10)
        offset: Number of results to skip for pagination (default: 0)
        retrieval_strategy: Search strategy - "hybrid", "neural", or "keyword"
                          - hybrid: combines semantic and keyword search (default)
                          - neural: pure semantic/embedding search
                          - keyword: traditional BM25 keyword search
        temporal_relevance: Weight recent content higher (0.0-1.0)
                          0.0 = no recency bias, 1.0 = only recent matters
        expand_query: Generate query variations for better recall
        interpret_filters: Extract structured filters from natural language
        rerank: Use LLM-based reranking for improved relevance
        generate_answer: Generate a natural language answer from results

    Returns:
        Dictionary with 'documents' list and optional 'answer' field
        Example: {"documents": [...], "answer": "Generated answer text"}

    """
    search_params: Dict[str, Any] = {
        "query": query,
        "limit": limit,
        "offset": offset,
    }

    # Add optional parameters
    if retrieval_strategy:
        search_params["retrieval_strategy"] = retrieval_strategy
    if temporal_relevance is not None:
        search_params["temporal_relevance"] = temporal_relevance
    if expand_query is not None:
        search_params["expand_query"] = expand_query
    if interpret_filters is not None:
        search_params["interpret_filters"] = interpret_filters
    if rerank is not None:
        search_params["rerank"] = rerank
    if generate_answer is not None:
        search_params["generate_answer"] = generate_answer

    response = self.client.collections.search(
        readable_id=collection_id,
        request=SearchRequest(**search_params),
    )

    result: Dict[str, Any] = {
        "documents": self._parse_search_response(response, collection_id),
    }

    # Add generated answer if available
    if hasattr(response, "completion") and response.completion:
        result["answer"] = response.completion

    return result

```
 |  
| --- | --- |  
###  search_and_generate_answer [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/airweave/#llama_index.tools.airweave.AirweaveToolSpec.search_and_generate_answer "Permanent link")

```
search_and_generate_answer(
    collection_id: ,
    query: ,
    limit: Optional[] = 10,
    use_reranking:  = True,
) -> Optional[]

```

Search collection and generate a natural language answer (RAG-style).
This is a convenience method that combines search with answer generation, perfect for agents that need direct answers rather than raw documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_id`  |  The readable ID of the collection  |  _required_  |  
|  `query`  |  The search query / question in natural language  |  _required_  |  
|  `limit`  |  `Optional[int]`  |  Maximum number of results to consider (default: 10)  |  
|  `use_reranking`  |  `bool`  |  Whether to use LLM reranking (default: True)  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[str]`  |  Natural language answer generated from the search results,  |  
|  `Optional[str]`  |  or None if no answer could be generated (with a warning)  |  
Source code in `llama-index-integrations/tools/llama-index-tools-airweave/llama_index/tools/airweave/base.py`  
| 
```
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
```
 | 
```
defsearch_and_generate_answer(
    self,
    collection_id: str,
    query: str,
    limit: Optional[int] = 10,
    use_reranking: bool = True,
) -> Optional[str]:
"""
    Search collection and generate a natural language answer (RAG-style).

    This is a convenience method that combines search with answer generation,
    perfect for agents that need direct answers rather than raw documents.

    Args:
        collection_id: The readable ID of the collection
        query: The search query / question in natural language
        limit: Maximum number of results to consider (default: 10)
        use_reranking: Whether to use LLM reranking (default: True)

    Returns:
        Natural language answer generated from the search results,
        or None if no answer could be generated (with a warning)

    """
    response = self.client.collections.search(
        readable_id=collection_id,
        request=SearchRequest(
            query=query,
            limit=limit,
            generate_answer=True,
            rerank=use_reranking,
        ),
    )

    if hasattr(response, "completion") and response.completion:
        return response.completion
    else:
        # Fallback if no answer generated
        warnings.warn(
            "No answer could be generated from the search results", UserWarning
        )
        return None

```
 |  
| --- | --- |  
###  list_collections [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/airweave/#llama_index.tools.airweave.AirweaveToolSpec.list_collections "Permanent link")

```
list_collections(
    skip: Optional[] = 0, limit: Optional[] = 100
) -> [[, ]]

```

List all collections available in your Airweave organization.
Useful for discovering what collections are available to search.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `skip`  |  `Optional[int]`  |  Number of collections to skip for pagination (default: 0)  |  
|  `limit`  |  `Optional[int]`  |  Maximum number of collections to return, 1-1000 (default: 100)  |  `100`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[Dict[str, Any]]`  |  List of dictionaries with collection information  |  
Source code in `llama-index-integrations/tools/llama-index-tools-airweave/llama_index/tools/airweave/base.py`  
| 
```
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
```
 | 
```
deflist_collections(
    self,
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> List[Dict[str, Any]]:
"""
    List all collections available in your Airweave organization.

    Useful for discovering what collections are available to search.

    Args:
        skip: Number of collections to skip for pagination (default: 0)
        limit: Maximum number of collections to return, 1-1000 (default: 100)

    Returns:
        List of dictionaries with collection information

    """
    collections = self.client.collections.list(skip=skip, limit=limit)

    return [
        {
            "id": (
                coll.readable_id if hasattr(coll, "readable_id") else str(coll.id)
            ),
            "name": coll.name,
            "created_at": (
                str(coll.created_at) if hasattr(coll, "created_at") else None
            ),
        }
        for coll in collections
    ]

```
 |  
| --- | --- |  
###  get_collection_info [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/airweave/#llama_index.tools.airweave.AirweaveToolSpec.get_collection_info "Permanent link")

```
get_collection_info(collection_id: ) -> [, ]

```

Get detailed information about a specific collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_id`  |  The readable ID of the collection  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dictionary with detailed collection information  |  
Source code in `llama-index-integrations/tools/llama-index-tools-airweave/llama_index/tools/airweave/base.py`  
| 
```
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
```
 | 
```
defget_collection_info(self, collection_id: str) -> Dict[str, Any]:
"""
    Get detailed information about a specific collection.

    Args:
        collection_id: The readable ID of the collection

    Returns:
        Dictionary with detailed collection information

    """
    collection = self.client.collections.get(readable_id=collection_id)

    return {
        "id": (
            collection.readable_id
            if hasattr(collection, "readable_id")
            else str(collection.id)
        ),
        "name": collection.name,
        "created_at": (
            str(collection.created_at)
            if hasattr(collection, "created_at")
            else None
        ),
        "description": getattr(collection, "description", None),
    }

```
 |  
| --- | --- |  
options: members: - AirweaveToolSpec
