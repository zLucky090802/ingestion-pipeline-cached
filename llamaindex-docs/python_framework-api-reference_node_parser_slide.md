# Slide
##  SlideNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/slide/#llama_index.node_parser.slide.SlideNodeParser "Permanent link")
Bases: 
Node parser using the SLIDE based approach using LLMs to improve chunk context.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-slide/llama_index/node_parser/slide/base.py`  
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
```
 | 
```
classSlideNodeParser(NodeParser):
"""Node parser using the SLIDE based approach using LLMs to improve chunk context."""

    chunk_size: int = Field(
        default=1200,
        description="tokens per base chunk",
    )

    window_size: int = Field(
        default=11,
        description="Window size for the sliding window approach. This is the total number chunks to include in the context window, ideall an odd number.",
    )

    llm_workers: int = Field(
        default=1,
        description="Number of workers to use for LLM calls. This is only used when using the async version of the parser.",
    )

    llm: LLM = Field(description="The LLM model to use for generating local context")

    token_counter: TokenCounter = Field(description="Token counter for sentences")

    sentence_splitter: SentenceSplitterCallable = Field(
        default_factory=split_by_sentence_tokenizer,
        description="Sentence splitter to use for splitting text into sentences.",
        exclude=True,
    )

    @classmethod
    defclass_name(cls) -> str:
        return "SlideNodeParser"

    @classmethod
    deffrom_defaults(
        cls,
        chunk_size: int = 1200,
        window_size: int = 11,
        llm_workers: int = 1,
        llm: Optional[LLM] = None,
        token_counter: Optional[TokenCounter] = None,
        sentence_splitter: Optional[Callable[[str], List[str]]] = None,
        callback_manager: Optional[CallbackManager] = None,
        id_func: Optional[Callable[[int, Document], str]] = None,
    ) -> "SlideNodeParser":
"""Create instance of the class with default values."""
        fromllama_index.coreimport Settings

        callback_manager = callback_manager or CallbackManager([])
        id_func = id_func or default_id_func
        llm = llm or Settings.llm
        token_counter = token_counter or TokenCounter()
        sentence_splitter = sentence_splitter or split_by_sentence_tokenizer()

        return cls(
            callback_manager=callback_manager,
            id_func=id_func,
            chunk_size=chunk_size,
            window_size=window_size,
            llm_workers=llm_workers,
            llm=llm,
            token_counter=token_counter,
            sentence_splitter=sentence_splitter,
        )

    @model_validator(mode="after")
    defvalidate_slide_config(self):
        # 1) chunk_size ≥ 1
        if self.chunk_size  1:
            raise ValueError("`chunk_size` must be greater than or equal to 1.")

        # 2) Warn if chunk_size is impractically small
        if self.chunk_size  50:
            warnings.warn(
                f"chunk_size={self.chunk_size} may be too small for meaningful chunking. "
                "This could lead to poor context quality and high LLM call overhead.",
                stacklevel=2,
            )

        # 3) window_size ≥ 1
        if self.window_size  1:
            raise ValueError("`window_size` must be greater than or equal to 1.")

        # 4) Validate LLM context budget: chunk_size × window_size
        context_window = getattr(
            getattr(self.llm, "metadata", None), "context_window", None
        )
        if context_window is not None:
            estimated_tokens = self.chunk_size * self.window_size
            if estimated_tokens  context_window:
                raise ValueError(
                    f"SLIDE configuration exceeds LLM context window: "
                    f"{self.chunk_size}{self.window_size}{estimated_tokens} tokens, "
                    f"but the LLM supports only {context_window} tokens."
                )
        else:
            # 5) Warn if context_window not provided
            warnings.warn(
                "The LLM does not expose `metadata.context_window`. "
                "SLIDE cannot validate token usage, which may lead to truncation or generation failures.",
                stacklevel=2,
            )

        return self

    def_parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
    ) -> List[BaseNode]:
"""Parse document into nodes."""
        # Warn if someone set llm_workers > 1 but is using sync parsing
        if self.llm_workers != 1:
            warnings.warn(
                "llm_workers has no effect when using synchronous parsing. "
                "If you want parallel LLM calls, use `aget_nodes_from_documents(...)` "
                "with llm_workers > 1.",
                stacklevel=2,
            )
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")

        for node in nodes_with_progress:
            nodes = self.build_slide_nodes_from_documents([node])
            all_nodes.extend(nodes)

        return all_nodes

    async def_aparse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
    ) -> List[BaseNode]:
"""Asynchronous parse document into nodes."""
        # If llm_workers is left at 1, no parallelism will occur.
        if self.llm_workers == 1:
            warnings.warn(
                "To parallelize LLM calls in async parsing, initialize with llm_workers > 1.",
                stacklevel=2,
            )

        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(
            nodes, show_progress, "Parsing nodes (async)"
        )

        for node in nodes_with_progress:
            nodes = await self.abuild_slide_nodes_from_documents([node], show_progress)
            all_nodes.extend(nodes)

        return all_nodes

    defcreate_individual_chunks(self, sentences: List[str]) -> List[str]:
"""Greedily add sentences to each chunk until we reach the chunk size limit."""
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            potential_chunk = (current_chunk + " " + sentence).strip()
            if (
                not current_chunk
                or self.token_counter.get_string_tokens(potential_chunk)
                <= self.chunk_size
            ):
                current_chunk = potential_chunk
            else:
                chunks.append(current_chunk)
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    defbuild_localised_splits(
        self,
        chunks: List[str],
    ) -> List[Dict[str, str]]:
"""Generate localized context for each chunk using a sliding window approach."""
        half_window = self.window_size // 2
        localized_splits = []
        for i in range(len(chunks)):
            start = max(0, i - half_window)
            end = min(len(chunks), i + half_window + 1)
            window_chunk = " ".join(chunks[start:end])

            # format prompt with current chunk and window chunk
            llm_messages = [
                ChatMessage(role="system", content=CONTEXT_GENERATION_SYSTEM_PROMPT),
                ChatMessage(
                    role="user",
                    content=CONTEXT_GENERATION_USER_PROMPT.format(
                        window_chunk=window_chunk, chunk=chunks[i]
                    ),
                ),
            ]

            # generate localized context using LLM
            localized_context = str(self.llm.chat(messages=llm_messages))
            localized_splits.append(
                {
                    "text": chunks[i],
                    "context": localized_context,
                }
            )

        return localized_splits

    async defabuild_localised_splits(
        self,
        chunks: List[str],
        show_progress: bool = False,
    ) -> List[Dict[str, str]]:
"""Async version: batch all LLM calls for each chunk via run_jobs."""
        half_window = self.window_size // 2

        # prepare one achat() coroutine per chunk
        jobs = []
        for i, chunk in enumerate(chunks):
            start = max(0, i - half_window)
            end = min(len(chunks), i + half_window + 1)
            window_chunk = " ".join(chunks[start:end])

            llm_messages = [
                ChatMessage(role="system", content=CONTEXT_GENERATION_SYSTEM_PROMPT),
                ChatMessage(
                    role="user",
                    content=CONTEXT_GENERATION_USER_PROMPT.format(
                        window_chunk=window_chunk, chunk=chunk
                    ),
                ),
            ]
            jobs.append(self.llm.achat(messages=llm_messages))

        # run them up to a maximum of llm_workers at once, get ordered responses
        responses = await run_jobs(
            jobs=jobs,
            workers=self.llm_workers,
            show_progress=show_progress,
            desc="Generating local contexts",
        )

        # reassemble into the split format
        return [
            {"text": chunks[i], "context": str(resp)}
            for i, resp in enumerate(responses)
        ]

    defpost_process_nodes(
        self,
        nodes: List[BaseNode],
        contexts: List[str],
    ) -> List[BaseNode]:
"""
        Attach slide_context metadata to each node based on the provided contexts.
        """
        for node, context in zip(nodes, contexts):
            # Preserve any existing metadata, then add our slide context
            node.metadata["local_context"] = context
        return nodes

    defbuild_slide_nodes_from_documents(
        self,
        documents: Sequence[Document],
    ) -> List[BaseNode]:
"""
        Build nodes enriched with localized context using a sliding window approach.
        This is the primary function of the class.
        """
        all_nodes: List[BaseNode] = []
        for document in documents:
            # Split into sentences and base chunks
            doctext = document.get_content()
            sentences = self.sentence_splitter(doctext)
            chunks = self.create_individual_chunks(sentences)

            # build localized splits
            splits = self.build_localised_splits(chunks)
            texts = [split["text"] for split in splits]
            contexts = [split["context"] for split in splits]

            # build and annotate nodes
            nodes = build_nodes_from_splits(
                text_splits=texts, document=document, id_func=self.id_func
            )

            nodes = self.post_process_nodes(nodes, contexts)
            all_nodes.extend(nodes)

        return all_nodes

    async defabuild_slide_nodes_from_documents(
        self,
        documents: Sequence[Document],
        show_progress: bool = False,
    ) -> List[BaseNode]:
"""
        Asynchronously build nodes enriched with localized context using a sliding window approach.
        """
        all_nodes: List[BaseNode] = []
        for document in documents:
            # Split into sentences and base chunks
            doctext = document.get_content()
            sentences = self.sentence_splitter(doctext)
            chunks = self.create_individual_chunks(sentences)

            # get localized splits using an async function
            splits = await self.abuild_localised_splits(chunks, show_progress)
            texts = [s["text"] for s in splits]
            contexts = [s["context"] for s in splits]

            # build and annotate nodes
            nodes = build_nodes_from_splits(
                text_splits=texts, document=document, id_func=self.id_func
            )

            nodes = self.post_process_nodes(nodes, contexts)
            all_nodes.extend(nodes)

        return all_nodes

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/slide/#llama_index.node_parser.slide.SlideNodeParser.from_defaults "Permanent link")

```
from_defaults(
    chunk_size:  = 1200,
    window_size:  = 11,
    llm_workers:  = 1,
    llm: Optional[] = None,
    token_counter: Optional[TokenCounter] = None,
    sentence_splitter: Optional[
        Callable[[], []]
    ] = None,
    callback_manager: Optional[] = None,
    id_func: Optional[
        Callable[[, ], ]
    ] = None,
) -> 

```

Create instance of the class with default values.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-slide/llama_index/node_parser/slide/base.py`  
| 
```
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
@classmethod
deffrom_defaults(
    cls,
    chunk_size: int = 1200,
    window_size: int = 11,
    llm_workers: int = 1,
    llm: Optional[LLM] = None,
    token_counter: Optional[TokenCounter] = None,
    sentence_splitter: Optional[Callable[[str], List[str]]] = None,
    callback_manager: Optional[CallbackManager] = None,
    id_func: Optional[Callable[[int, Document], str]] = None,
) -> "SlideNodeParser":
"""Create instance of the class with default values."""
    fromllama_index.coreimport Settings

    callback_manager = callback_manager or CallbackManager([])
    id_func = id_func or default_id_func
    llm = llm or Settings.llm
    token_counter = token_counter or TokenCounter()
    sentence_splitter = sentence_splitter or split_by_sentence_tokenizer()

    return cls(
        callback_manager=callback_manager,
        id_func=id_func,
        chunk_size=chunk_size,
        window_size=window_size,
        llm_workers=llm_workers,
        llm=llm,
        token_counter=token_counter,
        sentence_splitter=sentence_splitter,
    )

```
 |  
| --- | --- |  
###  create_individual_chunks [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/slide/#llama_index.node_parser.slide.SlideNodeParser.create_individual_chunks "Permanent link")

```
create_individual_chunks(sentences: []) -> []

```

Greedily add sentences to each chunk until we reach the chunk size limit.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-slide/llama_index/node_parser/slide/base.py`  
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
```
 | 
```
defcreate_individual_chunks(self, sentences: List[str]) -> List[str]:
"""Greedily add sentences to each chunk until we reach the chunk size limit."""
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        potential_chunk = (current_chunk + " " + sentence).strip()
        if (
            not current_chunk
            or self.token_counter.get_string_tokens(potential_chunk)
            <= self.chunk_size
        ):
            current_chunk = potential_chunk
        else:
            chunks.append(current_chunk)
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

```
 |  
| --- | --- |  
###  build_localised_splits [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/slide/#llama_index.node_parser.slide.SlideNodeParser.build_localised_splits "Permanent link")

```
build_localised_splits(
    chunks: [],
) -> [[, ]]

```

Generate localized context for each chunk using a sliding window approach.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-slide/llama_index/node_parser/slide/base.py`  
| 
```
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
```
 | 
```
defbuild_localised_splits(
    self,
    chunks: List[str],
) -> List[Dict[str, str]]:
"""Generate localized context for each chunk using a sliding window approach."""
    half_window = self.window_size // 2
    localized_splits = []
    for i in range(len(chunks)):
        start = max(0, i - half_window)
        end = min(len(chunks), i + half_window + 1)
        window_chunk = " ".join(chunks[start:end])

        # format prompt with current chunk and window chunk
        llm_messages = [
            ChatMessage(role="system", content=CONTEXT_GENERATION_SYSTEM_PROMPT),
            ChatMessage(
                role="user",
                content=CONTEXT_GENERATION_USER_PROMPT.format(
                    window_chunk=window_chunk, chunk=chunks[i]
                ),
            ),
        ]

        # generate localized context using LLM
        localized_context = str(self.llm.chat(messages=llm_messages))
        localized_splits.append(
            {
                "text": chunks[i],
                "context": localized_context,
            }
        )

    return localized_splits

```
 |  
| --- | --- |  
###  abuild_localised_splits [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/slide/#llama_index.node_parser.slide.SlideNodeParser.abuild_localised_splits "Permanent link")

```
abuild_localised_splits(
    chunks: [], show_progress:  = False
) -> [[, ]]

```

Async version: batch all LLM calls for each chunk via run_jobs.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-slide/llama_index/node_parser/slide/base.py`  
| 
```
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
```
 | 
```
async defabuild_localised_splits(
    self,
    chunks: List[str],
    show_progress: bool = False,
) -> List[Dict[str, str]]:
"""Async version: batch all LLM calls for each chunk via run_jobs."""
    half_window = self.window_size // 2

    # prepare one achat() coroutine per chunk
    jobs = []
    for i, chunk in enumerate(chunks):
        start = max(0, i - half_window)
        end = min(len(chunks), i + half_window + 1)
        window_chunk = " ".join(chunks[start:end])

        llm_messages = [
            ChatMessage(role="system", content=CONTEXT_GENERATION_SYSTEM_PROMPT),
            ChatMessage(
                role="user",
                content=CONTEXT_GENERATION_USER_PROMPT.format(
                    window_chunk=window_chunk, chunk=chunk
                ),
            ),
        ]
        jobs.append(self.llm.achat(messages=llm_messages))

    # run them up to a maximum of llm_workers at once, get ordered responses
    responses = await run_jobs(
        jobs=jobs,
        workers=self.llm_workers,
        show_progress=show_progress,
        desc="Generating local contexts",
    )

    # reassemble into the split format
    return [
        {"text": chunks[i], "context": str(resp)}
        for i, resp in enumerate(responses)
    ]

```
 |  
| --- | --- |  
###  post_process_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/slide/#llama_index.node_parser.slide.SlideNodeParser.post_process_nodes "Permanent link")

```
post_process_nodes(
    nodes: [], contexts: []
) -> []

```

Attach slide_context metadata to each node based on the provided contexts.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-slide/llama_index/node_parser/slide/base.py`  
| 
```
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
```
 | 
```
defpost_process_nodes(
    self,
    nodes: List[BaseNode],
    contexts: List[str],
) -> List[BaseNode]:
"""
    Attach slide_context metadata to each node based on the provided contexts.
    """
    for node, context in zip(nodes, contexts):
        # Preserve any existing metadata, then add our slide context
        node.metadata["local_context"] = context
    return nodes

```
 |  
| --- | --- |  
###  build_slide_nodes_from_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/slide/#llama_index.node_parser.slide.SlideNodeParser.build_slide_nodes_from_documents "Permanent link")

```
build_slide_nodes_from_documents(
    documents: Sequence[],
) -> []

```

Build nodes enriched with localized context using a sliding window approach. This is the primary function of the class.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-slide/llama_index/node_parser/slide/base.py`  
| 
```
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
```
 | 
```
defbuild_slide_nodes_from_documents(
    self,
    documents: Sequence[Document],
) -> List[BaseNode]:
"""
    Build nodes enriched with localized context using a sliding window approach.
    This is the primary function of the class.
    """
    all_nodes: List[BaseNode] = []
    for document in documents:
        # Split into sentences and base chunks
        doctext = document.get_content()
        sentences = self.sentence_splitter(doctext)
        chunks = self.create_individual_chunks(sentences)

        # build localized splits
        splits = self.build_localised_splits(chunks)
        texts = [split["text"] for split in splits]
        contexts = [split["context"] for split in splits]

        # build and annotate nodes
        nodes = build_nodes_from_splits(
            text_splits=texts, document=document, id_func=self.id_func
        )

        nodes = self.post_process_nodes(nodes, contexts)
        all_nodes.extend(nodes)

    return all_nodes

```
 |  
| --- | --- |  
###  abuild_slide_nodes_from_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/slide/#llama_index.node_parser.slide.SlideNodeParser.abuild_slide_nodes_from_documents "Permanent link")

```
abuild_slide_nodes_from_documents(
    documents: Sequence[],
    show_progress:  = False,
) -> []

```

Asynchronously build nodes enriched with localized context using a sliding window approach.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-slide/llama_index/node_parser/slide/base.py`  
| 
```
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
```
 | 
```
async defabuild_slide_nodes_from_documents(
    self,
    documents: Sequence[Document],
    show_progress: bool = False,
) -> List[BaseNode]:
"""
    Asynchronously build nodes enriched with localized context using a sliding window approach.
    """
    all_nodes: List[BaseNode] = []
    for document in documents:
        # Split into sentences and base chunks
        doctext = document.get_content()
        sentences = self.sentence_splitter(doctext)
        chunks = self.create_individual_chunks(sentences)

        # get localized splits using an async function
        splits = await self.abuild_localised_splits(chunks, show_progress)
        texts = [s["text"] for s in splits]
        contexts = [s["context"] for s in splits]

        # build and annotate nodes
        nodes = build_nodes_from_splits(
            text_splits=texts, document=document, id_func=self.id_func
        )

        nodes = self.post_process_nodes(nodes, contexts)
        all_nodes.extend(nodes)

    return all_nodes

```
 |  
| --- | --- |  
options: members: - SlideNodeParser
