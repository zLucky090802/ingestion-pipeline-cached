# Google
##  GoogleIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/google/#llama_index.indices.managed.google.GoogleIndex "Permanent link")
Bases: `BaseManagedIndex`
Google's Generative AI Semantic vector store with AQA.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-google/llama_index/indices/managed/google/base.py`  
| 
```
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
```
 | 
```
classGoogleIndex(BaseManagedIndex):
"""Google's Generative AI Semantic vector store with AQA."""

    _store: GoogleVectorStore
    _index: VectorStoreIndex

    def__init__(
        self,
        vector_store: GoogleVectorStore,
        embed_model: Optional[BaseEmbedding] = None,
        # deprecated
        **kwargs: Any,
    ) -> None:
"""
        Creates an instance of GoogleIndex.

        Prefer to use the factories `from_corpus` or `create_corpus` instead.
        """
        embed_model = embed_model or MockEmbedding(embed_dim=3)

        self._store = vector_store
        self._index = VectorStoreIndex.from_vector_store(
            vector_store, embed_model=embed_model, **kwargs
        )

        super().__init__(
            index_struct=self._index.index_struct,
            **kwargs,
        )

    @classmethod
    deffrom_corpus(
        cls: Type[IndexType], *, corpus_id: str, **kwargs: Any
    ) -> IndexType:
"""
        Creates a GoogleIndex from an existing corpus.

        Args:
            corpus_id: ID of an existing corpus on Google's server.

        Returns:
            An instance of GoogleIndex pointing to the specified corpus.

        """
        _logger.debug(f"\n\nGoogleIndex.from_corpus(corpus_id={corpus_id})")
        return cls(
            vector_store=GoogleVectorStore.from_corpus(corpus_id=corpus_id), **kwargs
        )

    @classmethod
    defcreate_corpus(
        cls: Type[IndexType],
        *,
        corpus_id: Optional[str] = None,
        display_name: Optional[str] = None,
        **kwargs: Any,
    ) -> IndexType:
"""
        Creates a GoogleIndex from a new corpus.

        Args:
            corpus_id: ID of the new corpus to be created. If not provided,
                Google server will provide one.
            display_name: Title of the new corpus. If not provided, Google
                server will provide one.

        Returns:
            An instance of GoogleIndex pointing to the specified corpus.

        """
        _logger.debug(
            f"\n\nGoogleIndex.from_new_corpus(new_corpus_id={corpus_id}, new_display_name={display_name})"
        )
        return cls(
            vector_store=GoogleVectorStore.create_corpus(
                corpus_id=corpus_id, display_name=display_name
            ),
            **kwargs,
        )

    @classmethod
    deffrom_documents(
        cls: Type[IndexType],
        documents: Sequence[Document],
        storage_context: Optional[StorageContext] = None,
        show_progress: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        transformations: Optional[List[TransformComponent]] = None,
        # deprecated
        embed_model: Optional[BaseEmbedding] = None,
        **kwargs: Any,
    ) -> IndexType:
"""Build an index from a sequence of documents."""
        _logger.debug("\n\nGoogleIndex.from_documents(...)")

        new_display_name = f"Corpus created on {datetime.datetime.now()}"
        instance = cls(
            vector_store=GoogleVectorStore.create_corpus(display_name=new_display_name),
            embed_model=embed_model,
            storage_context=storage_context,
            show_progress=show_progress,
            callback_manager=callback_manager,
            transformations=transformations,
            **kwargs,
        )

        index = cast(GoogleIndex, instance)
        index.insert_documents(
            documents=documents,
        )

        return instance

    @property
    defcorpus_id(self) -> str:
"""Returns the corpus ID being used by this GoogleIndex."""
        return self._store.corpus_id

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Inserts a set of nodes."""
        self._index.insert_nodes(nodes=nodes, **insert_kwargs)

    definsert_documents(self, documents: Sequence[Document], **kwargs: Any) -> None:
"""Inserts a set of documents."""
        for document in documents:
            self.insert(document=document, **kwargs)

    defdelete_ref_doc(
        self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
    ) -> None:
"""Deletes a document and its nodes by using ref_doc_id."""
        self._index.delete_ref_doc(ref_doc_id=ref_doc_id, **delete_kwargs)

    defupdate_ref_doc(self, document: Document, **update_kwargs: Any) -> None:
"""Updates a document and its corresponding nodes."""
        self._index.update(document=document, **update_kwargs)

    defas_retriever(self, **kwargs: Any) -> BaseRetriever:
"""Returns a Retriever for this managed index."""
        return self._index.as_retriever(**kwargs)

    defas_query_engine(
        self,
        llm: Optional[LLMType] = None,
        temperature: float = 0.7,
        answer_style: Any = 1,
        safety_setting: List[Any] = [],
        **kwargs: Any,
    ) -> BaseQueryEngine:
"""
        Returns the AQA engine for this index.

        Example:
          query_engine = index.as_query_engine(
              temperature=0.7,
              answer_style=AnswerStyle.ABSTRACTIVE,
              safety_setting=[
                  SafetySetting(
                      category=HARM_CATEGORY_SEXUALLY_EXPLICIT,
                      threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,




        Args:
            temperature: 0.0 to 1.0.
            answer_style: See `google.ai.generativelanguage.GenerateAnswerRequest.AnswerStyle`
            safety_setting: See `google.ai.generativelanguage.SafetySetting`.

        Returns:
            A query engine that uses Google's AQA model. The query engine will
            return a `Response` object.

            `Response`'s `source_nodes` will begin with a list of attributed
            passages. These passages are the ones that were used to construct
            the grounded response. These passages will always have no score,
            the only way to mark them as attributed passages. Then, the list
            will follow with the originally provided passages, which will have
            a score from the retrieval.

            `Response`'s `metadata` may also have have an entry with key
            `answerable_probability`, which is the probability that the grounded
            answer is likely correct.

        """
        # NOTE: lazy import
        fromllama_index.core.query_engine.retriever_query_engineimport (
            RetrieverQueryEngine,
        )

        # Don't overwrite the caller's kwargs, which may surprise them.
        local_kwargs = kwargs.copy()

        if "retriever" in kwargs:
            _logger.warning(
                "Ignoring user's retriever to GoogleIndex.as_query_engine, "
                "which uses its own retriever."
            )
            del local_kwargs["retriever"]

        if "response_synthesizer" in kwargs:
            _logger.warning(
                "Ignoring user's response synthesizer to "
                "GoogleIndex.as_query_engine, which uses its own retriever."
            )
            del local_kwargs["response_synthesizer"]

        local_kwargs["retriever"] = self.as_retriever(**local_kwargs)
        local_kwargs["response_synthesizer"] = GoogleTextSynthesizer.from_defaults(
            temperature=temperature,
            answer_style=answer_style,
            safety_setting=safety_setting,
        )

        return RetrieverQueryEngine.from_args(**local_kwargs)

    def_build_index_from_nodes(self, nodes: Sequence[BaseNode]) -> IndexDict:
"""Build the index from nodes."""
        return self._index._build_index_from_nodes(nodes)

```
 |  
| --- | --- |  
###  corpus_id `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/google/#llama_index.indices.managed.google.GoogleIndex.corpus_id "Permanent link")

```
corpus_id: 

```

Returns the corpus ID being used by this GoogleIndex.
###  from_corpus `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/google/#llama_index.indices.managed.google.GoogleIndex.from_corpus "Permanent link")

```
from_corpus(*, corpus_id: , **kwargs: ) -> IndexType

```

Creates a GoogleIndex from an existing corpus.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `corpus_id`  |  ID of an existing corpus on Google's server.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `IndexType`  |  An instance of GoogleIndex pointing to the specified corpus.  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-google/llama_index/indices/managed/google/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_corpus(
    cls: Type[IndexType], *, corpus_id: str, **kwargs: Any
) -> IndexType:
"""
    Creates a GoogleIndex from an existing corpus.

    Args:
        corpus_id: ID of an existing corpus on Google's server.

    Returns:
        An instance of GoogleIndex pointing to the specified corpus.

    """
    _logger.debug(f"\n\nGoogleIndex.from_corpus(corpus_id={corpus_id})")
    return cls(
        vector_store=GoogleVectorStore.from_corpus(corpus_id=corpus_id), **kwargs
    )

```
 |  
| --- | --- |  
###  create_corpus `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/google/#llama_index.indices.managed.google.GoogleIndex.create_corpus "Permanent link")

```
create_corpus(
    *,
    corpus_id: Optional[] = None,
    display_name: Optional[] = None,
    **kwargs: 
) -> IndexType

```

Creates a GoogleIndex from a new corpus.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `corpus_id`  |  `Optional[str]`  |  ID of the new corpus to be created. If not provided, Google server will provide one.  |  `None`  |  
|  `display_name`  |  `Optional[str]`  |  Title of the new corpus. If not provided, Google server will provide one.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `IndexType`  |  An instance of GoogleIndex pointing to the specified corpus.  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-google/llama_index/indices/managed/google/base.py`  
| 
```
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
@classmethod
defcreate_corpus(
    cls: Type[IndexType],
    *,
    corpus_id: Optional[str] = None,
    display_name: Optional[str] = None,
    **kwargs: Any,
) -> IndexType:
"""
    Creates a GoogleIndex from a new corpus.

    Args:
        corpus_id: ID of the new corpus to be created. If not provided,
            Google server will provide one.
        display_name: Title of the new corpus. If not provided, Google
            server will provide one.

    Returns:
        An instance of GoogleIndex pointing to the specified corpus.

    """
    _logger.debug(
        f"\n\nGoogleIndex.from_new_corpus(new_corpus_id={corpus_id}, new_display_name={display_name})"
    )
    return cls(
        vector_store=GoogleVectorStore.create_corpus(
            corpus_id=corpus_id, display_name=display_name
        ),
        **kwargs,
    )

```
 |  
| --- | --- |  
###  from_documents `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/google/#llama_index.indices.managed.google.GoogleIndex.from_documents "Permanent link")

```
from_documents(
    documents: Sequence[],
    storage_context: Optional[] = None,
    show_progress:  = False,
    callback_manager: Optional[] = None,
    transformations: Optional[
        []
    ] = None,
    embed_model: Optional[] = None,
    **kwargs: 
) -> IndexType

```

Build an index from a sequence of documents.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-google/llama_index/indices/managed/google/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_documents(
    cls: Type[IndexType],
    documents: Sequence[Document],
    storage_context: Optional[StorageContext] = None,
    show_progress: bool = False,
    callback_manager: Optional[CallbackManager] = None,
    transformations: Optional[List[TransformComponent]] = None,
    # deprecated
    embed_model: Optional[BaseEmbedding] = None,
    **kwargs: Any,
) -> IndexType:
"""Build an index from a sequence of documents."""
    _logger.debug("\n\nGoogleIndex.from_documents(...)")

    new_display_name = f"Corpus created on {datetime.datetime.now()}"
    instance = cls(
        vector_store=GoogleVectorStore.create_corpus(display_name=new_display_name),
        embed_model=embed_model,
        storage_context=storage_context,
        show_progress=show_progress,
        callback_manager=callback_manager,
        transformations=transformations,
        **kwargs,
    )

    index = cast(GoogleIndex, instance)
    index.insert_documents(
        documents=documents,
    )

    return instance

```
 |  
| --- | --- |  
###  insert_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/google/#llama_index.indices.managed.google.GoogleIndex.insert_documents "Permanent link")

```
insert_documents(
    documents: Sequence[], **kwargs: 
) -> None

```

Inserts a set of documents.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-google/llama_index/indices/managed/google/base.py`  
| 
```
164
165
166
167
```
 | 
```
definsert_documents(self, documents: Sequence[Document], **kwargs: Any) -> None:
"""Inserts a set of documents."""
    for document in documents:
        self.insert(document=document, **kwargs)

```
 |  
| --- | --- |  
###  delete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/google/#llama_index.indices.managed.google.GoogleIndex.delete_ref_doc "Permanent link")

```
delete_ref_doc(
    ref_doc_id: ,
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Deletes a document and its nodes by using ref_doc_id.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-google/llama_index/indices/managed/google/base.py`  
| 
```
169
170
171
172
173
```
 | 
```
defdelete_ref_doc(
    self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
) -> None:
"""Deletes a document and its nodes by using ref_doc_id."""
    self._index.delete_ref_doc(ref_doc_id=ref_doc_id, **delete_kwargs)

```
 |  
| --- | --- |  
###  update_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/google/#llama_index.indices.managed.google.GoogleIndex.update_ref_doc "Permanent link")

```
update_ref_doc(
    document: , **update_kwargs: 
) -> None

```

Updates a document and its corresponding nodes.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-google/llama_index/indices/managed/google/base.py`  
| 
```
175
176
177
```
 | 
```
defupdate_ref_doc(self, document: Document, **update_kwargs: Any) -> None:
"""Updates a document and its corresponding nodes."""
    self._index.update(document=document, **update_kwargs)

```
 |  
| --- | --- |  
###  as_retriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/google/#llama_index.indices.managed.google.GoogleIndex.as_retriever "Permanent link")

```
as_retriever(**kwargs: ) -> 

```

Returns a Retriever for this managed index.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-google/llama_index/indices/managed/google/base.py`  
| 
```
179
180
181
```
 | 
```
defas_retriever(self, **kwargs: Any) -> BaseRetriever:
"""Returns a Retriever for this managed index."""
    return self._index.as_retriever(**kwargs)

```
 |  
| --- | --- |  
###  as_query_engine [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/google/#llama_index.indices.managed.google.GoogleIndex.as_query_engine "Permanent link")

```
as_query_engine(
    llm: Optional[LLMType] = None,
    temperature: float = 0.7,
    answer_style:  = 1,
    safety_setting: [] = [],
    **kwargs: 
) -> 

```

Returns the AQA engine for this index.
Example
query_engine = index.as_query_engine( temperature=0.7, answer_style=AnswerStyle.ABSTRACTIVE, safety_setting=[ SafetySetting( category=HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, ), ] )
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `temperature`  |  `float`  |  0.0 to 1.0.  |  `0.7`  |  
|  `answer_style`  |  See `google.ai.generativelanguage.GenerateAnswerRequest.AnswerStyle`  |  
|  `safety_setting`  |  `List[Any]`  |  See `google.ai.generativelanguage.SafetySetting`.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  A query engine that uses Google's AQA model. The query engine will  |  
|   |  return a `Response` object.  |  
|   |  `Response`'s `source_nodes` will begin with a list of attributed  |  
|   |  passages. These passages are the ones that were used to construct  |  
|   |  the grounded response. These passages will always have no score,  |  
|   |  the only way to mark them as attributed passages. Then, the list  |  
|   |  will follow with the originally provided passages, which will have  |  
|   |  a score from the retrieval.  |  
|   |  `Response`'s `metadata` may also have have an entry with key  |  
|   |  `answerable_probability`, which is the probability that the grounded  |  
|   |  answer is likely correct.  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-google/llama_index/indices/managed/google/base.py`  
| 
```
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
```
 | 
```
defas_query_engine(
    self,
    llm: Optional[LLMType] = None,
    temperature: float = 0.7,
    answer_style: Any = 1,
    safety_setting: List[Any] = [],
    **kwargs: Any,
) -> BaseQueryEngine:
"""
    Returns the AQA engine for this index.

    Example:
      query_engine = index.as_query_engine(
          temperature=0.7,
          answer_style=AnswerStyle.ABSTRACTIVE,
          safety_setting=[
              SafetySetting(
                  category=HARM_CATEGORY_SEXUALLY_EXPLICIT,
                  threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,




    Args:
        temperature: 0.0 to 1.0.
        answer_style: See `google.ai.generativelanguage.GenerateAnswerRequest.AnswerStyle`
        safety_setting: See `google.ai.generativelanguage.SafetySetting`.

    Returns:
        A query engine that uses Google's AQA model. The query engine will
        return a `Response` object.

        `Response`'s `source_nodes` will begin with a list of attributed
        passages. These passages are the ones that were used to construct
        the grounded response. These passages will always have no score,
        the only way to mark them as attributed passages. Then, the list
        will follow with the originally provided passages, which will have
        a score from the retrieval.

        `Response`'s `metadata` may also have have an entry with key
        `answerable_probability`, which is the probability that the grounded
        answer is likely correct.

    """
    # NOTE: lazy import
    fromllama_index.core.query_engine.retriever_query_engineimport (
        RetrieverQueryEngine,
    )

    # Don't overwrite the caller's kwargs, which may surprise them.
    local_kwargs = kwargs.copy()

    if "retriever" in kwargs:
        _logger.warning(
            "Ignoring user's retriever to GoogleIndex.as_query_engine, "
            "which uses its own retriever."
        )
        del local_kwargs["retriever"]

    if "response_synthesizer" in kwargs:
        _logger.warning(
            "Ignoring user's response synthesizer to "
            "GoogleIndex.as_query_engine, which uses its own retriever."
        )
        del local_kwargs["response_synthesizer"]

    local_kwargs["retriever"] = self.as_retriever(**local_kwargs)
    local_kwargs["response_synthesizer"] = GoogleTextSynthesizer.from_defaults(
        temperature=temperature,
        answer_style=answer_style,
        safety_setting=safety_setting,
    )

    return RetrieverQueryEngine.from_args(**local_kwargs)

```
 |  
| --- | --- |  
options: members: - GoogleIndex
