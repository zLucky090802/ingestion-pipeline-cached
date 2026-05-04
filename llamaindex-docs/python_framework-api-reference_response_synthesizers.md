# Index
Response builder class.
This class provides general functions for taking in a set of text and generating a response.
Will support different modes, from 1) stuffing chunks into prompt, 2) create and refine separately over each chunk, 3) tree summarization.
##  BaseSynthesizer [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.base.BaseSynthesizer "Permanent link")
Bases: `PromptMixin`, `DispatcherSpanMixin`
Response builder class.
Source code in `llama-index-core/llama_index/core/response_synthesizers/base.py`  
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
```
 | 
```
classBaseSynthesizer(PromptMixin, DispatcherSpanMixin):
"""Response builder class."""

    def__init__(
        self,
        llm: Optional[LLM] = None,
        callback_manager: Optional[CallbackManager] = None,
        prompt_helper: Optional[PromptHelper] = None,
        streaming: bool = False,
        output_cls: Optional[Type[BaseModel]] = None,
        empty_response: Optional[str] = None,
    ) -> None:
"""Init params."""
        self._llm = llm or Settings.llm

        if callback_manager:
            self._llm.callback_manager = callback_manager

        self._callback_manager = callback_manager or Settings.callback_manager

        self._prompt_helper = (
            prompt_helper
            or Settings._prompt_helper
            or PromptHelper.from_llm_metadata(
                self._llm.metadata,
            )
        )

        self._streaming = streaming
        self._output_cls = output_cls
        self._empty_response = empty_response or "Empty Response"

    def_empty_response_generator(self) -> Generator[str, None, None]:
        yield self._empty_response

    async def_empty_response_agenerator(self) -> AsyncGenerator[str, None]:
        yield self._empty_response

    def_get_prompt_modules(self) -> Dict[str, Any]:
"""Get prompt modules."""
        # TODO: keep this for now since response synthesizers don't generally have sub-modules
        return {}

    @property
    defcallback_manager(self) -> CallbackManager:
        return self._callback_manager

    @callback_manager.setter
    defcallback_manager(self, callback_manager: CallbackManager) -> None:
"""Set callback manager."""
        self._callback_manager = callback_manager
        # TODO: please fix this later
        self._callback_manager = callback_manager
        self._llm.callback_manager = callback_manager

    @abstractmethod
    defget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
"""Get response."""
        ...

    @abstractmethod
    async defaget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
"""Get response."""
        ...

    def_log_prompt_and_response(
        self,
        formatted_prompt: str,
        response: RESPONSE_TEXT_TYPE,
        log_prefix: str = "",
    ) -> None:
"""Log prompt and response from LLM."""
        logger.debug(f"> {log_prefix} prompt template: {formatted_prompt}")
        logger.debug(f"> {log_prefix} response: {response}")

    def_get_metadata_for_response(
        self,
        nodes: List[BaseNode],
    ) -> Optional[Dict[str, Any]]:
"""Get metadata for response."""
        return {node.node_id: node.metadata for node in nodes}

    def_prepare_response_output(
        self,
        response_str: Optional[RESPONSE_TEXT_TYPE],
        source_nodes: List[NodeWithScore],
    ) -> RESPONSE_TYPE:
"""Prepare response object from response string."""
        response_metadata = self._get_metadata_for_response(
            [node_with_score.node for node_with_score in source_nodes]
        )

        if isinstance(self._llm, StructuredLLM):
            # convert string to output_cls
            output = self._llm.output_cls.model_validate_json(str(response_str))
            return PydanticResponse(
                output,
                source_nodes=source_nodes,
                metadata=response_metadata,
            )

        if isinstance(response_str, str):
            return Response(
                response_str,
                source_nodes=source_nodes,
                metadata=response_metadata,
            )
        if isinstance(response_str, Generator):
            return StreamingResponse(
                response_str,
                source_nodes=source_nodes,
                metadata=response_metadata,
            )
        if isinstance(response_str, AsyncGenerator):
            return AsyncStreamingResponse(
                response_str,
                source_nodes=source_nodes,
                metadata=response_metadata,
            )

        if self._output_cls is not None and isinstance(response_str, self._output_cls):
            return PydanticResponse(
                response_str, source_nodes=source_nodes, metadata=response_metadata
            )

        raise ValueError(
            f"Response must be a string or a generator. Found {type(response_str)}"
        )

    @dispatcher.span
    defsynthesize(
        self,
        query: QueryTextType,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
        **response_kwargs: Any,
    ) -> RESPONSE_TYPE:
        dispatcher.event(
            SynthesizeStartEvent(
                query=query,
            )
        )

        if len(nodes) == 0:
            if self._streaming:
                empty_response_stream = StreamingResponse(
                    response_gen=self._empty_response_generator()
                )
                dispatcher.event(
                    SynthesizeEndEvent(
                        query=query,
                        response=empty_response_stream,
                    )
                )
                return empty_response_stream
            else:
                empty_response = Response(self._empty_response)
                dispatcher.event(
                    SynthesizeEndEvent(
                        query=query,
                        response=empty_response,
                    )
                )
                return empty_response

        if isinstance(query, str):
            query = QueryBundle(query_str=query)

        with self._callback_manager.event(
            CBEventType.SYNTHESIZE,
            payload={EventPayload.QUERY_STR: query.query_str},
        ) as event:
            response_str = self.get_response(
                query_str=query.query_str,
                text_chunks=[
                    n.node.get_content(metadata_mode=MetadataMode.LLM) for n in nodes
                ],
                **response_kwargs,
            )

            additional_source_nodes = additional_source_nodes or []
            source_nodes = list(nodes) + list(additional_source_nodes)

            response = self._prepare_response_output(response_str, source_nodes)

            event.on_end(payload={EventPayload.RESPONSE: response})

        dispatcher.event(
            SynthesizeEndEvent(
                query=query,
                response=response,
            )
        )
        return response

    @dispatcher.span
    async defasynthesize(
        self,
        query: QueryTextType,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
        **response_kwargs: Any,
    ) -> RESPONSE_TYPE:
        dispatcher.event(
            SynthesizeStartEvent(
                query=query,
            )
        )
        if len(nodes) == 0:
            if self._streaming:
                empty_response_stream = AsyncStreamingResponse(
                    response_gen=self._empty_response_agenerator()
                )
                dispatcher.event(
                    SynthesizeEndEvent(
                        query=query,
                        response=empty_response_stream,
                    )
                )
                return empty_response_stream
            else:
                empty_response = Response(self._empty_response)
                dispatcher.event(
                    SynthesizeEndEvent(
                        query=query,
                        response=empty_response,
                    )
                )
                return empty_response

        if isinstance(query, str):
            query = QueryBundle(query_str=query)

        with self._callback_manager.event(
            CBEventType.SYNTHESIZE,
            payload={EventPayload.QUERY_STR: query.query_str},
        ) as event:
            response_str = await self.aget_response(
                query_str=query.query_str,
                text_chunks=[
                    n.node.get_content(metadata_mode=MetadataMode.LLM) for n in nodes
                ],
                **response_kwargs,
            )

            additional_source_nodes = additional_source_nodes or []
            source_nodes = list(nodes) + list(additional_source_nodes)

            response = self._prepare_response_output(response_str, source_nodes)

            event.on_end(payload={EventPayload.RESPONSE: response})

        dispatcher.event(
            SynthesizeEndEvent(
                query=query,
                response=response,
            )
        )
        return response

```
 |  
| --- | --- |  
###  get_response `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.base.BaseSynthesizer.get_response "Permanent link")

```
get_response(
    query_str: ,
    text_chunks: Sequence[],
    **response_kwargs: 
) -> RESPONSE_TEXT_TYPE

```

Get response.
Source code in `llama-index-core/llama_index/core/response_synthesizers/base.py`  
| 
```
108
109
110
111
112
113
114
115
116
```
 | 
```
@abstractmethod
defget_response(
    self,
    query_str: str,
    text_chunks: Sequence[str],
    **response_kwargs: Any,
) -> RESPONSE_TEXT_TYPE:
"""Get response."""
    ...

```
 |  
| --- | --- |  
###  aget_response `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.base.BaseSynthesizer.aget_response "Permanent link")

```
aget_response(
    query_str: ,
    text_chunks: Sequence[],
    **response_kwargs: 
) -> RESPONSE_TEXT_TYPE

```

Get response.
Source code in `llama-index-core/llama_index/core/response_synthesizers/base.py`  
| 
```
118
119
120
121
122
123
124
125
126
```
 | 
```
@abstractmethod
async defaget_response(
    self,
    query_str: str,
    text_chunks: Sequence[str],
    **response_kwargs: Any,
) -> RESPONSE_TEXT_TYPE:
"""Get response."""
    ...

```
 |  
| --- | --- |  
options: members: - BaseSynthesizer
##  get_response_synthesizer [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.factory.get_response_synthesizer "Permanent link")

```
get_response_synthesizer(
    llm: Optional[] = None,
    prompt_helper: Optional[] = None,
    text_qa_template: Optional[] = None,
    refine_template: Optional[] = None,
    summary_template: Optional[] = None,
    simple_template: Optional[] = None,
    response_mode:  = ,
    callback_manager: Optional[] = None,
    use_async:  = False,
    streaming:  = False,
    structured_answer_filtering:  = False,
    output_cls: Optional[[BaseModel]] = None,
    program_factory: Optional[
        Callable[[], ]
    ] = None,
    verbose:  = False,
) -> 

```

Get a response synthesizer.
Source code in `llama-index-core/llama_index/core/response_synthesizers/factory.py`  
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
```
 | 
```
defget_response_synthesizer(
    llm: Optional[LLM] = None,
    prompt_helper: Optional[PromptHelper] = None,
    text_qa_template: Optional[BasePromptTemplate] = None,
    refine_template: Optional[BasePromptTemplate] = None,
    summary_template: Optional[BasePromptTemplate] = None,
    simple_template: Optional[BasePromptTemplate] = None,
    response_mode: ResponseMode = ResponseMode.COMPACT,
    callback_manager: Optional[CallbackManager] = None,
    use_async: bool = False,
    streaming: bool = False,
    structured_answer_filtering: bool = False,
    output_cls: Optional[Type[BaseModel]] = None,
    program_factory: Optional[
        Callable[[BasePromptTemplate], BasePydanticProgram]
    ] = None,
    verbose: bool = False,
) -> BaseSynthesizer:
"""Get a response synthesizer."""
    text_qa_template = text_qa_template or DEFAULT_TEXT_QA_PROMPT_SEL
    refine_template = refine_template or DEFAULT_REFINE_PROMPT_SEL
    simple_template = simple_template or DEFAULT_SIMPLE_INPUT_PROMPT
    summary_template = summary_template or DEFAULT_TREE_SUMMARIZE_PROMPT_SEL

    callback_manager = callback_manager or Settings.callback_manager
    llm = llm or Settings.llm
    prompt_helper = (
        prompt_helper
        or Settings._prompt_helper
        or PromptHelper.from_llm_metadata(
            llm.metadata,
        )
    )

    if response_mode == ResponseMode.REFINE:
        return Refine(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            refine_template=refine_template,
            output_cls=output_cls,
            streaming=streaming,
            structured_answer_filtering=structured_answer_filtering,
            program_factory=program_factory,
            verbose=verbose,
        )
    elif response_mode == ResponseMode.COMPACT:
        return CompactAndRefine(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            refine_template=refine_template,
            output_cls=output_cls,
            streaming=streaming,
            structured_answer_filtering=structured_answer_filtering,
            program_factory=program_factory,
            verbose=verbose,
        )
    elif response_mode == ResponseMode.TREE_SUMMARIZE:
        return TreeSummarize(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            summary_template=summary_template,
            output_cls=output_cls,
            streaming=streaming,
            use_async=use_async,
            verbose=verbose,
        )
    elif response_mode == ResponseMode.SIMPLE_SUMMARIZE:
        return SimpleSummarize(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            streaming=streaming,
        )
    elif response_mode == ResponseMode.GENERATION:
        return Generation(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            simple_template=simple_template,
            streaming=streaming,
        )
    elif response_mode == ResponseMode.ACCUMULATE:
        return Accumulate(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            output_cls=output_cls,
            streaming=streaming,
            use_async=use_async,
        )
    elif response_mode == ResponseMode.COMPACT_ACCUMULATE:
        return CompactAndAccumulate(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            output_cls=output_cls,
            streaming=streaming,
            use_async=use_async,
        )
    elif response_mode == ResponseMode.NO_TEXT:
        return NoText(
            callback_manager=callback_manager,
            streaming=streaming,
        )
    elif response_mode == ResponseMode.CONTEXT_ONLY:
        return ContextOnly(
            callback_manager=callback_manager,
            streaming=streaming,
        )
    else:
        raise ValueError(f"Unknown mode: {response_mode}")

```
 |  
| --- | --- |  
options: members: - get_response_synthesizer
##  ResponseMode [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.type.ResponseMode "Permanent link")
Bases: `str`, `Enum`
Response modes of the response builder (and synthesizer).
Source code in `llama-index-core/llama_index/core/response_synthesizers/type.py`  
| 
```
 4
 5
 6
 7
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
51
52
53
54
55
56
57
```
 | 
```
classResponseMode(str, Enum):
"""Response modes of the response builder (and synthesizer)."""

    REFINE = "refine"
"""
    Refine is an iterative way of generating a response.
    We first use the context in the first node, along with the query, to generate an \
    initial answer.
    We then pass this answer, the query, and the context of the second node as input \
    into a “refine prompt” to generate a refined answer. We refine through N-1 nodes, \
    where N is the total number of nodes.
    """

    COMPACT = "compact"
"""
    Compact and refine mode first combine text chunks into larger consolidated chunks \
    that more fully utilize the available context window, then refine answers \
    across them.
    This mode is faster than refine since we make fewer calls to the LLM.
    """

    SIMPLE_SUMMARIZE = "simple_summarize"
"""
    Merge all text chunks into one, and make a LLM call.
    This will fail if the merged text chunk exceeds the context window size.
    """

    TREE_SUMMARIZE = "tree_summarize"
"""
    Build a tree index over the set of candidate nodes, with a summary prompt seeded \
    with the query.
    The tree is built in a bottoms-up fashion, and in the end the root node is \
    returned as the response
    """

    GENERATION = "generation"
"""Ignore context, just use LLM to generate a response."""

    NO_TEXT = "no_text"
"""Return the retrieved context nodes, without synthesizing a final response."""

    CONTEXT_ONLY = "context_only"
"""Returns a concatenated string of all text chunks."""

    ACCUMULATE = "accumulate"
"""Synthesize a response for each text chunk, and then return the concatenation."""

    COMPACT_ACCUMULATE = "compact_accumulate"
"""
    Compact and accumulate mode first combine text chunks into larger consolidated \
    chunks that more fully utilize the available context window, then accumulate \
    answers for each of them and finally return the concatenation.
    This mode is faster than accumulate since we make fewer calls to the LLM.
    """

```
 |  
| --- | --- |  
###  REFINE `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.type.ResponseMode.REFINE "Permanent link")

```
REFINE = 'refine'

```

Refine is an iterative way of generating a response. We first use the context in the first node, along with the query, to generate an initial answer. We then pass this answer, the query, and the context of the second node as input into a “refine prompt” to generate a refined answer. We refine through N-1 nodes, where N is the total number of nodes.
###  COMPACT `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.type.ResponseMode.COMPACT "Permanent link")

```
COMPACT = 'compact'

```

Compact and refine mode first combine text chunks into larger consolidated chunks that more fully utilize the available context window, then refine answers across them. This mode is faster than refine since we make fewer calls to the LLM.
###  SIMPLE_SUMMARIZE `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.type.ResponseMode.SIMPLE_SUMMARIZE "Permanent link")

```
SIMPLE_SUMMARIZE = 'simple_summarize'

```

Merge all text chunks into one, and make a LLM call. This will fail if the merged text chunk exceeds the context window size.
###  TREE_SUMMARIZE `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.type.ResponseMode.TREE_SUMMARIZE "Permanent link")

```
TREE_SUMMARIZE = 'tree_summarize'

```

Build a tree index over the set of candidate nodes, with a summary prompt seeded with the query. The tree is built in a bottoms-up fashion, and in the end the root node is returned as the response
###  GENERATION `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.type.ResponseMode.GENERATION "Permanent link")

```
GENERATION = 'generation'

```

Ignore context, just use LLM to generate a response.
###  NO_TEXT `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.type.ResponseMode.NO_TEXT "Permanent link")

```
NO_TEXT = 'no_text'

```

Return the retrieved context nodes, without synthesizing a final response.
###  CONTEXT_ONLY `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.type.ResponseMode.CONTEXT_ONLY "Permanent link")

```
CONTEXT_ONLY = 'context_only'

```

Returns a concatenated string of all text chunks.
###  ACCUMULATE `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.type.ResponseMode.ACCUMULATE "Permanent link")

```
ACCUMULATE = 'accumulate'

```

Synthesize a response for each text chunk, and then return the concatenation.
###  COMPACT_ACCUMULATE `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/#llama_index.core.response_synthesizers.type.ResponseMode.COMPACT_ACCUMULATE "Permanent link")

```
COMPACT_ACCUMULATE = 'compact_accumulate'

```

Compact and accumulate mode first combine text chunks into larger consolidated chunks that more fully utilize the available context window, then accumulate answers for each of them and finally return the concatenation. This mode is faster than accumulate since we make fewer calls to the LLM.
options: members: - ResponseMode
