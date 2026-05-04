# Simple summarize
Init file.
##  Accumulate [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.Accumulate "Permanent link")
Bases: 
Accumulate responses from multiple text chunks.
Source code in `llama-index-core/llama_index/core/response_synthesizers/accumulate.py`  
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
classAccumulate(BaseSynthesizer):
"""Accumulate responses from multiple text chunks."""

    def__init__(
        self,
        llm: Optional[LLM] = None,
        callback_manager: Optional[CallbackManager] = None,
        prompt_helper: Optional[PromptHelper] = None,
        text_qa_template: Optional[BasePromptTemplate] = None,
        output_cls: Optional[Type[BaseModel]] = None,
        streaming: bool = False,
        use_async: bool = False,
    ) -> None:
        super().__init__(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            streaming=streaming,
        )
        self._text_qa_template = text_qa_template or DEFAULT_TEXT_QA_PROMPT_SEL
        self._use_async = use_async
        self._output_cls = output_cls

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {"text_qa_template": self._text_qa_template}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "text_qa_template" in prompts:
            self._text_qa_template = prompts["text_qa_template"]

    defflatten_list(self, md_array: List[List[Any]]) -> List[Any]:
        return [item for sublist in md_array for item in sublist]

    def_format_response(self, outputs: List[Any], separator: str) -> str:
        responses: List[str] = []
        for response in outputs:
            responses.append(response or "Empty Response")

        return separator.join(
            [f"Response {index+1}: {item}" for index, item in enumerate(responses)]
        )

    async defaget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        separator: str = "\n---------------------\n",
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
"""Apply the same prompt to text chunks and return async responses."""
        if self._streaming:
            raise ValueError("Unable to stream in Accumulate response mode")

        tasks = [
            self._give_responses(
                query_str, text_chunk, use_async=True, **response_kwargs
            )
            for text_chunk in text_chunks
        ]

        flattened_tasks = self.flatten_list(tasks)
        outputs = await asyncio.gather(*flattened_tasks)

        return self._format_response(outputs, separator)

    defget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        separator: str = "\n---------------------\n",
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
"""Apply the same prompt to text chunks and return responses."""
        if self._streaming:
            raise ValueError("Unable to stream in Accumulate response mode")

        tasks = [
            self._give_responses(
                query_str, text_chunk, use_async=self._use_async, **response_kwargs
            )
            for text_chunk in text_chunks
        ]

        outputs = self.flatten_list(tasks)

        if self._use_async:
            outputs = run_async_tasks(outputs)

        return self._format_response(outputs, separator)

    def_give_responses(
        self,
        query_str: str,
        text_chunk: str,
        use_async: bool = False,
        **response_kwargs: Any,
    ) -> List[Any]:
"""Give responses given a query and a corresponding text chunk."""
        text_qa_template = self._text_qa_template.partial_format(query_str=query_str)

        text_chunks = self._prompt_helper.repack(
            text_qa_template, [text_chunk], llm=self._llm
        )

        predictor: Callable
        if self._output_cls is None:
            predictor = self._llm.apredict if use_async else self._llm.predict

            return [
                predictor(
                    text_qa_template,
                    context_str=cur_text_chunk,
                    **response_kwargs,
                )
                for cur_text_chunk in text_chunks
            ]
        else:
            predictor = (
                self._llm.astructured_predict
                if use_async
                else self._llm.structured_predict
            )

            return [
                predictor(
                    self._output_cls,
                    text_qa_template,
                    context_str=cur_text_chunk,
                    **response_kwargs,
                )
                for cur_text_chunk in text_chunks
            ]

```
 |  
| --- | --- |  
###  aget_response [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.Accumulate.aget_response "Permanent link")

```
aget_response(
    query_str: ,
    text_chunks: Sequence[],
    separator:  = "\n---------------------\n",
    **response_kwargs: 
) -> RESPONSE_TEXT_TYPE

```

Apply the same prompt to text chunks and return async responses.
Source code in `llama-index-core/llama_index/core/response_synthesizers/accumulate.py`  
| 
```
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
```
 | 
```
async defaget_response(
    self,
    query_str: str,
    text_chunks: Sequence[str],
    separator: str = "\n---------------------\n",
    **response_kwargs: Any,
) -> RESPONSE_TEXT_TYPE:
"""Apply the same prompt to text chunks and return async responses."""
    if self._streaming:
        raise ValueError("Unable to stream in Accumulate response mode")

    tasks = [
        self._give_responses(
            query_str, text_chunk, use_async=True, **response_kwargs
        )
        for text_chunk in text_chunks
    ]

    flattened_tasks = self.flatten_list(tasks)
    outputs = await asyncio.gather(*flattened_tasks)

    return self._format_response(outputs, separator)

```
 |  
| --- | --- |  
###  get_response [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.Accumulate.get_response "Permanent link")

```
get_response(
    query_str: ,
    text_chunks: Sequence[],
    separator:  = "\n---------------------\n",
    **response_kwargs: 
) -> RESPONSE_TEXT_TYPE

```

Apply the same prompt to text chunks and return responses.
Source code in `llama-index-core/llama_index/core/response_synthesizers/accumulate.py`  
| 
```
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
```
 | 
```
defget_response(
    self,
    query_str: str,
    text_chunks: Sequence[str],
    separator: str = "\n---------------------\n",
    **response_kwargs: Any,
) -> RESPONSE_TEXT_TYPE:
"""Apply the same prompt to text chunks and return responses."""
    if self._streaming:
        raise ValueError("Unable to stream in Accumulate response mode")

    tasks = [
        self._give_responses(
            query_str, text_chunk, use_async=self._use_async, **response_kwargs
        )
        for text_chunk in text_chunks
    ]

    outputs = self.flatten_list(tasks)

    if self._use_async:
        outputs = run_async_tasks(outputs)

    return self._format_response(outputs, separator)

```
 |  
| --- | --- |  
##  BaseSynthesizer [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.BaseSynthesizer "Permanent link")
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
###  get_response `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.BaseSynthesizer.get_response "Permanent link")

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
###  aget_response `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.BaseSynthesizer.aget_response "Permanent link")

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
##  CompactAndRefine [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.CompactAndRefine "Permanent link")
Bases: 
Refine responses across compact text chunks.
Source code in `llama-index-core/llama_index/core/response_synthesizers/compact_and_refine.py`  
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
```
 | 
```
classCompactAndRefine(Refine):
"""Refine responses across compact text chunks."""

    @dispatcher.span
    async defaget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        prev_response: Optional[RESPONSE_TEXT_TYPE] = None,
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
        compact_texts = self._make_compact_text_chunks(query_str, text_chunks)
        return await super().aget_response(
            query_str=query_str,
            text_chunks=compact_texts,
            prev_response=prev_response,
            **response_kwargs,
        )

    @dispatcher.span
    defget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        prev_response: Optional[RESPONSE_TEXT_TYPE] = None,
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
"""Get compact response."""
        # use prompt helper to fix compact text_chunks under the prompt limitation
        # TODO: This is a temporary fix - reason it's temporary is that
        # the refine template does not account for size of previous answer.
        new_texts = self._make_compact_text_chunks(query_str, text_chunks)
        return super().get_response(
            query_str=query_str,
            text_chunks=new_texts,
            prev_response=prev_response,
            **response_kwargs,
        )

    def_make_compact_text_chunks(
        self, query_str: str, text_chunks: Sequence[str]
    ) -> List[str]:
        text_qa_template = self._text_qa_template.partial_format(query_str=query_str)
        refine_template = self._refine_template.partial_format(query_str=query_str)

        max_prompt = get_biggest_prompt([text_qa_template, refine_template])
        return self._prompt_helper.repack(max_prompt, text_chunks, llm=self._llm)

```
 |  
| --- | --- |  
###  get_response [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.CompactAndRefine.get_response "Permanent link")

```
get_response(
    query_str: ,
    text_chunks: Sequence[],
    prev_response: Optional[RESPONSE_TEXT_TYPE] = None,
    **response_kwargs: 
) -> RESPONSE_TEXT_TYPE

```

Get compact response.
Source code in `llama-index-core/llama_index/core/response_synthesizers/compact_and_refine.py`  
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
```
 | 
```
@dispatcher.span
defget_response(
    self,
    query_str: str,
    text_chunks: Sequence[str],
    prev_response: Optional[RESPONSE_TEXT_TYPE] = None,
    **response_kwargs: Any,
) -> RESPONSE_TEXT_TYPE:
"""Get compact response."""
    # use prompt helper to fix compact text_chunks under the prompt limitation
    # TODO: This is a temporary fix - reason it's temporary is that
    # the refine template does not account for size of previous answer.
    new_texts = self._make_compact_text_chunks(query_str, text_chunks)
    return super().get_response(
        query_str=query_str,
        text_chunks=new_texts,
        prev_response=prev_response,
        **response_kwargs,
    )

```
 |  
| --- | --- |  
##  Generation [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.Generation "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/response_synthesizers/generation.py`  
| 
```
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
```
 | 
```
classGeneration(BaseSynthesizer):
    def__init__(
        self,
        llm: Optional[LLM] = None,
        callback_manager: Optional[CallbackManager] = None,
        prompt_helper: Optional[PromptHelper] = None,
        simple_template: Optional[BasePromptTemplate] = None,
        streaming: bool = False,
    ) -> None:
        super().__init__(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            streaming=streaming,
        )
        self._input_prompt = simple_template or DEFAULT_SIMPLE_INPUT_PROMPT

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {"simple_template": self._input_prompt}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "simple_template" in prompts:
            self._input_prompt = prompts["simple_template"]

    async defaget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
        # NOTE: ignore text chunks and previous response
        del text_chunks

        if not self._streaming:
            return await self._llm.apredict(
                self._input_prompt,
                query_str=query_str,
                **response_kwargs,
            )
        else:
            return await self._llm.astream(
                self._input_prompt,
                query_str=query_str,
                **response_kwargs,
            )

    defget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
        # NOTE: ignore text chunks and previous response
        del text_chunks

        if not self._streaming:
            return self._llm.predict(
                self._input_prompt,
                query_str=query_str,
                **response_kwargs,
            )
        else:
            return self._llm.stream(
                self._input_prompt,
                query_str=query_str,
                **response_kwargs,
            )

    # NOTE: synthesize and asynthesize are copied from the base class,
    #       but modified to return when zero nodes are provided

    @dispatcher.span
    defsynthesize(
        self,
        query: QueryType,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
        **response_kwargs: Any,
    ) -> RESPONSE_TYPE:
        dispatcher.event(
            SynthesizeStartEvent(
                query=query,
            )
        )

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
        query: QueryType,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
        **response_kwargs: Any,
    ) -> RESPONSE_TYPE:
        dispatcher.event(
            SynthesizeStartEvent(
                query=query,
            )
        )

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
##  Refine [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.Refine "Permanent link")
Bases: 
Refine a response to a query across text chunks.
Source code in `llama-index-core/llama_index/core/response_synthesizers/refine.py`  
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
```
 | 
```
classRefine(BaseSynthesizer):
"""Refine a response to a query across text chunks."""

    def__init__(
        self,
        llm: Optional[LLM] = None,
        callback_manager: Optional[CallbackManager] = None,
        prompt_helper: Optional[PromptHelper] = None,
        text_qa_template: Optional[BasePromptTemplate] = None,
        refine_template: Optional[BasePromptTemplate] = None,
        output_cls: Optional[Type[BaseModel]] = None,
        streaming: bool = False,
        verbose: bool = False,
        structured_answer_filtering: bool = False,
        program_factory: Optional[
            Callable[[BasePromptTemplate], BasePydanticProgram]
        ] = None,
    ) -> None:
        super().__init__(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            streaming=streaming,
        )
        self._text_qa_template = text_qa_template or DEFAULT_TEXT_QA_PROMPT_SEL
        self._refine_template = refine_template or DEFAULT_REFINE_PROMPT_SEL
        self._verbose = verbose
        self._structured_answer_filtering = structured_answer_filtering
        self._output_cls = output_cls

        if self._streaming and self._structured_answer_filtering:
            raise ValueError(
                "Streaming not supported with structured answer filtering."
            )
        if not self._structured_answer_filtering and program_factory is not None:
            raise ValueError(
                "Program factory not supported without structured answer filtering."
            )
        self._program_factory = program_factory or self._default_program_factory

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {
            "text_qa_template": self._text_qa_template,
            "refine_template": self._refine_template,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "text_qa_template" in prompts:
            self._text_qa_template = prompts["text_qa_template"]
        if "refine_template" in prompts:
            self._refine_template = prompts["refine_template"]

    @dispatcher.span
    defget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        prev_response: Optional[RESPONSE_TEXT_TYPE] = None,
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
"""Give response over chunks."""
        dispatcher.event(
            GetResponseStartEvent(query_str=query_str, text_chunks=text_chunks)
        )
        response: Optional[RESPONSE_TEXT_TYPE] = None
        for text_chunk in text_chunks:
            if prev_response is None:
                # if this is the first chunk, and text chunk already
                # is an answer, then return it
                response = self._give_response_single(
                    query_str, text_chunk, **response_kwargs
                )
            else:
                # refine response if possible
                response = self._refine_response_single(
                    prev_response, query_str, text_chunk, **response_kwargs
                )
            prev_response = response
        if isinstance(response, str):
            if self._output_cls is not None:
                try:
                    response = self._output_cls.model_validate_json(response)
                except ValidationError:
                    pass
            else:
                response = response or "Empty Response"
        else:
            response = cast(Generator, response)
        dispatcher.event(GetResponseEndEvent())
        return response

    def_default_program_factory(
        self, prompt: BasePromptTemplate
    ) -> BasePydanticProgram:
        if self._structured_answer_filtering:
            fromllama_index.core.program.utilsimport get_program_for_llm

            return get_program_for_llm(
                StructuredRefineResponse,
                prompt,
                self._llm,
                verbose=self._verbose,
            )
        else:
            return DefaultRefineProgram(
                prompt=prompt,
                llm=self._llm,
                output_cls=self._output_cls,
            )

    def_give_response_single(
        self,
        query_str: str,
        text_chunk: str,
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
"""Give response given a query and a corresponding text chunk."""
        text_qa_template = self._text_qa_template.partial_format(query_str=query_str)
        text_chunks = self._prompt_helper.repack(
            text_qa_template, [text_chunk], llm=self._llm
        )

        response: Optional[RESPONSE_TEXT_TYPE] = None
        program = self._program_factory(text_qa_template)
        # TODO: consolidate with loop in get_response_default
        for cur_text_chunk in text_chunks:
            query_satisfied = False
            if response is None and not self._streaming:
                try:
                    structured_response = cast(
                        StructuredRefineResponse,
                        program(
                            context_str=cur_text_chunk,
                            **response_kwargs,
                        ),
                    )
                    query_satisfied = structured_response.query_satisfied
                    if query_satisfied:
                        response = structured_response.answer
                except ValidationError as e:
                    logger.warning(
                        f"Validation error on structured response: {e}", exc_info=True
                    )
            elif response is None and self._streaming:
                response = self._llm.stream(
                    text_qa_template,
                    context_str=cur_text_chunk,
                    **response_kwargs,
                )
                query_satisfied = True
            else:
                response = self._refine_response_single(
                    cast(RESPONSE_TEXT_TYPE, response),
                    query_str,
                    cur_text_chunk,
                    **response_kwargs,
                )
        if response is None:
            response = "Empty Response"
        if isinstance(response, str):
            response = response or "Empty Response"
        else:
            response = cast(Generator, response)
        return response

    def_refine_response_single(
        self,
        response: RESPONSE_TEXT_TYPE,
        query_str: str,
        text_chunk: str,
        **response_kwargs: Any,
    ) -> Optional[RESPONSE_TEXT_TYPE]:
"""Refine response."""
        # TODO: consolidate with logic in response/schema.py
        if isinstance(response, Generator):
            response = get_response_text(response)

        fmt_text_chunk = truncate_text(text_chunk, 50)
        logger.debug(f"> Refine context: {fmt_text_chunk}")
        if self._verbose:
            print(f"> Refine context: {fmt_text_chunk}")

        # NOTE: partial format refine template with query_str and existing_answer here
        refine_template = self._refine_template.partial_format(
            query_str=query_str, existing_answer=response
        )

        # compute available chunk size to see if there is any available space
        # determine if the refine template is too big (which can happen if
        # prompt template + query + existing answer is too large)
        avail_chunk_size = self._prompt_helper._get_available_chunk_size(
            refine_template
        )

        if avail_chunk_size  0:
            # if the available chunk size is negative, then the refine template
            # is too big and we just return the original response
            return response

        # obtain text chunks to add to the refine template
        text_chunks = self._prompt_helper.repack(
            refine_template, text_chunks=[text_chunk], llm=self._llm
        )

        program = self._program_factory(refine_template)
        for cur_text_chunk in text_chunks:
            query_satisfied = False
            if not self._streaming:
                try:
                    structured_response = cast(
                        StructuredRefineResponse,
                        program(
                            context_msg=cur_text_chunk,
                            **response_kwargs,
                        ),
                    )
                    query_satisfied = structured_response.query_satisfied
                    if query_satisfied:
                        response = structured_response.answer
                except ValidationError as e:
                    logger.warning(
                        f"Validation error on structured response: {e}", exc_info=True
                    )
            else:
                # TODO: structured response not supported for streaming
                if isinstance(response, Generator):
                    response = "".join(response)

                refine_template = self._refine_template.partial_format(
                    query_str=query_str, existing_answer=response
                )

                response = self._llm.stream(
                    refine_template,
                    context_msg=cur_text_chunk,
                    **response_kwargs,
                )

        return response

    @dispatcher.span
    async defaget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        prev_response: Optional[RESPONSE_TEXT_TYPE] = None,
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
        dispatcher.event(
            GetResponseStartEvent(query_str=query_str, text_chunks=text_chunks)
        )
        response: Optional[RESPONSE_TEXT_TYPE] = None
        for text_chunk in text_chunks:
            if prev_response is None:
                # if this is the first chunk, and text chunk already
                # is an answer, then return it
                response = await self._agive_response_single(
                    query_str, text_chunk, **response_kwargs
                )
            else:
                response = await self._arefine_response_single(
                    prev_response, query_str, text_chunk, **response_kwargs
                )
            prev_response = response
        if response is None:
            response = "Empty Response"
        if isinstance(response, str):
            if self._output_cls is not None:
                response = self._output_cls.model_validate_json(response)
            else:
                response = response or "Empty Response"
        else:
            response = cast(AsyncGenerator, response)
        dispatcher.event(GetResponseEndEvent())
        return response

    async def_arefine_response_single(
        self,
        response: RESPONSE_TEXT_TYPE,
        query_str: str,
        text_chunk: str,
        **response_kwargs: Any,
    ) -> Optional[RESPONSE_TEXT_TYPE]:
"""Refine response."""
        # TODO: consolidate with logic in response/schema.py
        if isinstance(response, AsyncGenerator):
            response = await aget_response_text(response)

        fmt_text_chunk = truncate_text(text_chunk, 50)
        logger.debug(f"> Refine context: {fmt_text_chunk}")

        # NOTE: partial format refine template with query_str and existing_answer here
        refine_template = self._refine_template.partial_format(
            query_str=query_str, existing_answer=response
        )

        # compute available chunk size to see if there is any available space
        # determine if the refine template is too big (which can happen if
        # prompt template + query + existing answer is too large)
        avail_chunk_size = self._prompt_helper._get_available_chunk_size(
            refine_template
        )

        if avail_chunk_size  0:
            # if the available chunk size is negative, then the refine template
            # is too big and we just return the original response
            return response

        # obtain text chunks to add to the refine template
        text_chunks = self._prompt_helper.repack(
            refine_template, text_chunks=[text_chunk], llm=self._llm
        )

        program = self._program_factory(refine_template)
        for cur_text_chunk in text_chunks:
            query_satisfied = False
            if not self._streaming:
                try:
                    structured_response = await program.acall(
                        context_msg=cur_text_chunk,
                        **response_kwargs,
                    )
                    structured_response = cast(
                        StructuredRefineResponse, structured_response
                    )
                    query_satisfied = structured_response.query_satisfied
                    if query_satisfied:
                        response = structured_response.answer
                except ValidationError as e:
                    logger.warning(
                        f"Validation error on structured response: {e}", exc_info=True
                    )
            else:
                if isinstance(response, Generator):
                    response = "".join(response)

                if isinstance(response, AsyncGenerator):
                    _r = ""
                    async for text in response:
                        _r += text
                    response = _r

                refine_template = self._refine_template.partial_format(
                    query_str=query_str, existing_answer=response
                )

                response = await self._llm.astream(
                    refine_template,
                    context_msg=cur_text_chunk,
                    **response_kwargs,
                )

            if query_satisfied:
                refine_template = self._refine_template.partial_format(
                    query_str=query_str, existing_answer=response
                )

        return response

    async def_agive_response_single(
        self,
        query_str: str,
        text_chunk: str,
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
"""Give response given a query and a corresponding text chunk."""
        text_qa_template = self._text_qa_template.partial_format(query_str=query_str)
        text_chunks = self._prompt_helper.repack(
            text_qa_template, [text_chunk], llm=self._llm
        )

        response: Optional[RESPONSE_TEXT_TYPE] = None
        program = self._program_factory(text_qa_template)
        # TODO: consolidate with loop in get_response_default
        for cur_text_chunk in text_chunks:
            if response is None and not self._streaming:
                try:
                    structured_response = await program.acall(
                        context_str=cur_text_chunk,
                        **response_kwargs,
                    )
                    structured_response = cast(
                        StructuredRefineResponse, structured_response
                    )
                    query_satisfied = structured_response.query_satisfied
                    if query_satisfied:
                        response = structured_response.answer
                except ValidationError as e:
                    logger.warning(
                        f"Validation error on structured response: {e}", exc_info=True
                    )
            elif response is None and self._streaming:
                response = await self._llm.astream(
                    text_qa_template,
                    context_str=cur_text_chunk,
                    **response_kwargs,
                )
                query_satisfied = True
            else:
                response = await self._arefine_response_single(
                    cast(RESPONSE_TEXT_TYPE, response),
                    query_str,
                    cur_text_chunk,
                    **response_kwargs,
                )
        if response is None:
            response = "Empty Response"
        if isinstance(response, str):
            response = response or "Empty Response"
        else:
            response = cast(AsyncGenerator, response)
        return response

```
 |  
| --- | --- |  
###  get_response [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.Refine.get_response "Permanent link")

```
get_response(
    query_str: ,
    text_chunks: Sequence[],
    prev_response: Optional[RESPONSE_TEXT_TYPE] = None,
    **response_kwargs: 
) -> RESPONSE_TEXT_TYPE

```

Give response over chunks.
Source code in `llama-index-core/llama_index/core/response_synthesizers/refine.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defget_response(
    self,
    query_str: str,
    text_chunks: Sequence[str],
    prev_response: Optional[RESPONSE_TEXT_TYPE] = None,
    **response_kwargs: Any,
) -> RESPONSE_TEXT_TYPE:
"""Give response over chunks."""
    dispatcher.event(
        GetResponseStartEvent(query_str=query_str, text_chunks=text_chunks)
    )
    response: Optional[RESPONSE_TEXT_TYPE] = None
    for text_chunk in text_chunks:
        if prev_response is None:
            # if this is the first chunk, and text chunk already
            # is an answer, then return it
            response = self._give_response_single(
                query_str, text_chunk, **response_kwargs
            )
        else:
            # refine response if possible
            response = self._refine_response_single(
                prev_response, query_str, text_chunk, **response_kwargs
            )
        prev_response = response
    if isinstance(response, str):
        if self._output_cls is not None:
            try:
                response = self._output_cls.model_validate_json(response)
            except ValidationError:
                pass
        else:
            response = response or "Empty Response"
    else:
        response = cast(Generator, response)
    dispatcher.event(GetResponseEndEvent())
    return response

```
 |  
| --- | --- |  
##  SimpleSummarize [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.SimpleSummarize "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/response_synthesizers/simple_summarize.py`  
| 
```
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
```
 | 
```
classSimpleSummarize(BaseSynthesizer):
    def__init__(
        self,
        llm: Optional[LLM] = None,
        callback_manager: Optional[CallbackManager] = None,
        prompt_helper: Optional[PromptHelper] = None,
        text_qa_template: Optional[BasePromptTemplate] = None,
        streaming: bool = False,
    ) -> None:
        super().__init__(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            streaming=streaming,
        )
        self._text_qa_template = text_qa_template or DEFAULT_TEXT_QA_PROMPT_SEL

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {"text_qa_template": self._text_qa_template}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "text_qa_template" in prompts:
            self._text_qa_template = prompts["text_qa_template"]

    async defaget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
        text_qa_template = self._text_qa_template.partial_format(query_str=query_str)
        single_text_chunk = "\n".join(text_chunks)
        truncated_chunks = self._prompt_helper.truncate(
            prompt=text_qa_template,
            text_chunks=[single_text_chunk],
            llm=self._llm,
        )

        response: RESPONSE_TEXT_TYPE
        if not self._streaming:
            response = await self._llm.apredict(
                text_qa_template,
                context_str=truncated_chunks,
                **response_kwargs,
            )
        else:
            response = await self._llm.astream(
                text_qa_template,
                context_str=truncated_chunks,
                **response_kwargs,
            )

        if isinstance(response, str):
            response = response or "Empty Response"
        else:
            response = cast(Generator, response)

        return response

    defget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        **kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
        text_qa_template = self._text_qa_template.partial_format(query_str=query_str)
        single_text_chunk = "\n".join(text_chunks)
        truncated_chunks = self._prompt_helper.truncate(
            prompt=text_qa_template,
            text_chunks=[single_text_chunk],
            llm=self._llm,
        )

        response: RESPONSE_TEXT_TYPE
        if not self._streaming:
            response = self._llm.predict(
                text_qa_template,
                context_str=truncated_chunks,
                **kwargs,
            )
        else:
            response = self._llm.stream(
                text_qa_template,
                context_str=truncated_chunks,
                **kwargs,
            )

        if isinstance(response, str):
            response = response or "Empty Response"
        else:
            response = cast(Generator, response)

        return response

```
 |  
| --- | --- |  
##  TreeSummarize [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.TreeSummarize "Permanent link")
Bases: 
Tree summarize response builder.
This response builder recursively merges text chunks and summarizes them in a bottom-up fashion (i.e. building a tree from leaves to root).
More concretely, at each recursively step: 1. we repack the text chunks so that each chunk fills the context window of the LLM 2. if there is only one chunk, we give the final response 3. otherwise, we summarize each chunk and recursively summarize the summaries.
Source code in `llama-index-core/llama_index/core/response_synthesizers/tree_summarize.py`  
| 
```
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
```
 | 
```
classTreeSummarize(BaseSynthesizer):
"""
    Tree summarize response builder.

    This response builder recursively merges text chunks and summarizes them
    in a bottom-up fashion (i.e. building a tree from leaves to root).

    More concretely, at each recursively step:
    1. we repack the text chunks so that each chunk fills the context window of the LLM
    2. if there is only one chunk, we give the final response
    3. otherwise, we summarize each chunk and recursively summarize the summaries.
    """

    def__init__(
        self,
        llm: Optional[LLM] = None,
        callback_manager: Optional[CallbackManager] = None,
        prompt_helper: Optional[PromptHelper] = None,
        summary_template: Optional[BasePromptTemplate] = None,
        output_cls: Optional[Type[BaseModel]] = None,
        streaming: bool = False,
        use_async: bool = False,
        verbose: bool = False,
    ) -> None:
        super().__init__(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            streaming=streaming,
            output_cls=output_cls,
        )
        self._summary_template = summary_template or DEFAULT_TREE_SUMMARIZE_PROMPT_SEL
        self._use_async = use_async
        self._verbose = verbose

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {"summary_template": self._summary_template}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "summary_template" in prompts:
            self._summary_template = prompts["summary_template"]

    async defaget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
"""Get tree summarize response."""
        summary_template = self._summary_template.partial_format(query_str=query_str)
        # repack text_chunks so that each chunk fills the context window
        text_chunks = self._prompt_helper.repack(
            summary_template, text_chunks=text_chunks, llm=self._llm
        )

        if self._verbose:
            print(f"{len(text_chunks)} text chunks after repacking")

        # give final response if there is only one chunk
        if len(text_chunks) == 1:
            response: RESPONSE_TEXT_TYPE
            if self._streaming:
                response = await self._llm.astream(
                    summary_template, context_str=text_chunks[0], **response_kwargs
                )
            else:
                if self._output_cls is None:
                    response = await self._llm.apredict(
                        summary_template,
                        context_str=text_chunks[0],
                        **response_kwargs,
                    )
                else:
                    response = await self._llm.astructured_predict(
                        self._output_cls,
                        summary_template,
                        context_str=text_chunks[0],
                        **response_kwargs,
                    )

            # return pydantic object if output_cls is specified
            return response

        else:
            # summarize each chunk
            if self._output_cls is None:
                str_tasks = [
                    self._llm.apredict(
                        summary_template,
                        context_str=text_chunk,
                        **response_kwargs,
                    )
                    for text_chunk in text_chunks
                ]
                summaries = await asyncio.gather(*str_tasks)
            else:
                model_tasks = [
                    self._llm.astructured_predict(
                        self._output_cls,
                        summary_template,
                        context_str=text_chunk,
                        **response_kwargs,
                    )
                    for text_chunk in text_chunks
                ]
                summary_models = await asyncio.gather(*model_tasks)
                summaries = [
                    summary.model_dump_json()
                    if isinstance(summary, BaseModel)
                    else str(summary)
                    for summary in summary_models
                ]

            # recursively summarize the summaries
            return await self.aget_response(
                query_str=query_str,
                text_chunks=summaries,
                **response_kwargs,
            )

    defget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
"""Get tree summarize response."""
        summary_template = self._summary_template.partial_format(query_str=query_str)
        # repack text_chunks so that each chunk fills the context window
        text_chunks = self._prompt_helper.repack(
            summary_template, text_chunks=text_chunks, llm=self._llm
        )

        if self._verbose:
            print(f"{len(text_chunks)} text chunks after repacking")

        # give final response if there is only one chunk
        if len(text_chunks) == 1:
            response: RESPONSE_TEXT_TYPE
            if self._streaming:
                response = self._llm.stream(
                    summary_template, context_str=text_chunks[0], **response_kwargs
                )
            else:
                if self._output_cls is None:
                    response = self._llm.predict(
                        summary_template,
                        context_str=text_chunks[0],
                        **response_kwargs,
                    )
                else:
                    response = self._llm.structured_predict(
                        self._output_cls,
                        summary_template,
                        context_str=text_chunks[0],
                        **response_kwargs,
                    )

            return response

        else:
            # summarize each chunk
            if self._use_async:
                if self._output_cls is None:
                    tasks = [
                        self._llm.apredict(
                            summary_template,
                            context_str=text_chunk,
                            **response_kwargs,
                        )
                        for text_chunk in text_chunks
                    ]
                else:
                    tasks = [
                        self._llm.astructured_predict(
                            self._output_cls,
                            summary_template,
                            context_str=text_chunk,
                            **response_kwargs,
                        )
                        for text_chunk in text_chunks
                    ]

                summary_responses = run_async_tasks(tasks)

                if self._output_cls is not None:
                    summaries = [
                        summary.model_dump_json()
                        if isinstance(summary, BaseModel)
                        else str(summary)
                        for summary in summary_responses
                    ]
                else:
                    summaries = summary_responses
            else:
                if self._output_cls is None:
                    summaries = [
                        self._llm.predict(
                            summary_template,
                            context_str=text_chunk,
                            **response_kwargs,
                        )
                        for text_chunk in text_chunks
                    ]
                else:
                    summary_models = [
                        self._llm.structured_predict(
                            self._output_cls,
                            summary_template,
                            context_str=text_chunk,
                            **response_kwargs,
                        )
                        for text_chunk in text_chunks
                    ]
                    summaries = [
                        summary.model_dump_json()
                        if isinstance(summary, BaseModel)
                        else str(summary)
                        for summary in summary_models
                    ]

            # recursively summarize the summaries
            return self.get_response(
                query_str=query_str, text_chunks=summaries, **response_kwargs
            )

```
 |  
| --- | --- |  
###  aget_response [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.TreeSummarize.aget_response "Permanent link")

```
aget_response(
    query_str: ,
    text_chunks: Sequence[],
    **response_kwargs: 
) -> RESPONSE_TEXT_TYPE

```

Get tree summarize response.
Source code in `llama-index-core/llama_index/core/response_synthesizers/tree_summarize.py`  
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
```
 | 
```
async defaget_response(
    self,
    query_str: str,
    text_chunks: Sequence[str],
    **response_kwargs: Any,
) -> RESPONSE_TEXT_TYPE:
"""Get tree summarize response."""
    summary_template = self._summary_template.partial_format(query_str=query_str)
    # repack text_chunks so that each chunk fills the context window
    text_chunks = self._prompt_helper.repack(
        summary_template, text_chunks=text_chunks, llm=self._llm
    )

    if self._verbose:
        print(f"{len(text_chunks)} text chunks after repacking")

    # give final response if there is only one chunk
    if len(text_chunks) == 1:
        response: RESPONSE_TEXT_TYPE
        if self._streaming:
            response = await self._llm.astream(
                summary_template, context_str=text_chunks[0], **response_kwargs
            )
        else:
            if self._output_cls is None:
                response = await self._llm.apredict(
                    summary_template,
                    context_str=text_chunks[0],
                    **response_kwargs,
                )
            else:
                response = await self._llm.astructured_predict(
                    self._output_cls,
                    summary_template,
                    context_str=text_chunks[0],
                    **response_kwargs,
                )

        # return pydantic object if output_cls is specified
        return response

    else:
        # summarize each chunk
        if self._output_cls is None:
            str_tasks = [
                self._llm.apredict(
                    summary_template,
                    context_str=text_chunk,
                    **response_kwargs,
                )
                for text_chunk in text_chunks
            ]
            summaries = await asyncio.gather(*str_tasks)
        else:
            model_tasks = [
                self._llm.astructured_predict(
                    self._output_cls,
                    summary_template,
                    context_str=text_chunk,
                    **response_kwargs,
                )
                for text_chunk in text_chunks
            ]
            summary_models = await asyncio.gather(*model_tasks)
            summaries = [
                summary.model_dump_json()
                if isinstance(summary, BaseModel)
                else str(summary)
                for summary in summary_models
            ]

        # recursively summarize the summaries
        return await self.aget_response(
            query_str=query_str,
            text_chunks=summaries,
            **response_kwargs,
        )

```
 |  
| --- | --- |  
###  get_response [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.TreeSummarize.get_response "Permanent link")

```
get_response(
    query_str: ,
    text_chunks: Sequence[],
    **response_kwargs: 
) -> RESPONSE_TEXT_TYPE

```

Get tree summarize response.
Source code in `llama-index-core/llama_index/core/response_synthesizers/tree_summarize.py`  
| 
```
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
```
 | 
```
defget_response(
    self,
    query_str: str,
    text_chunks: Sequence[str],
    **response_kwargs: Any,
) -> RESPONSE_TEXT_TYPE:
"""Get tree summarize response."""
    summary_template = self._summary_template.partial_format(query_str=query_str)
    # repack text_chunks so that each chunk fills the context window
    text_chunks = self._prompt_helper.repack(
        summary_template, text_chunks=text_chunks, llm=self._llm
    )

    if self._verbose:
        print(f"{len(text_chunks)} text chunks after repacking")

    # give final response if there is only one chunk
    if len(text_chunks) == 1:
        response: RESPONSE_TEXT_TYPE
        if self._streaming:
            response = self._llm.stream(
                summary_template, context_str=text_chunks[0], **response_kwargs
            )
        else:
            if self._output_cls is None:
                response = self._llm.predict(
                    summary_template,
                    context_str=text_chunks[0],
                    **response_kwargs,
                )
            else:
                response = self._llm.structured_predict(
                    self._output_cls,
                    summary_template,
                    context_str=text_chunks[0],
                    **response_kwargs,
                )

        return response

    else:
        # summarize each chunk
        if self._use_async:
            if self._output_cls is None:
                tasks = [
                    self._llm.apredict(
                        summary_template,
                        context_str=text_chunk,
                        **response_kwargs,
                    )
                    for text_chunk in text_chunks
                ]
            else:
                tasks = [
                    self._llm.astructured_predict(
                        self._output_cls,
                        summary_template,
                        context_str=text_chunk,
                        **response_kwargs,
                    )
                    for text_chunk in text_chunks
                ]

            summary_responses = run_async_tasks(tasks)

            if self._output_cls is not None:
                summaries = [
                    summary.model_dump_json()
                    if isinstance(summary, BaseModel)
                    else str(summary)
                    for summary in summary_responses
                ]
            else:
                summaries = summary_responses
        else:
            if self._output_cls is None:
                summaries = [
                    self._llm.predict(
                        summary_template,
                        context_str=text_chunk,
                        **response_kwargs,
                    )
                    for text_chunk in text_chunks
                ]
            else:
                summary_models = [
                    self._llm.structured_predict(
                        self._output_cls,
                        summary_template,
                        context_str=text_chunk,
                        **response_kwargs,
                    )
                    for text_chunk in text_chunks
                ]
                summaries = [
                    summary.model_dump_json()
                    if isinstance(summary, BaseModel)
                    else str(summary)
                    for summary in summary_models
                ]

        # recursively summarize the summaries
        return self.get_response(
            query_str=query_str, text_chunks=summaries, **response_kwargs
        )

```
 |  
| --- | --- |  
##  ResponseMode [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.ResponseMode "Permanent link")
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
###  REFINE `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.ResponseMode.REFINE "Permanent link")

```
REFINE = 'refine'

```

Refine is an iterative way of generating a response. We first use the context in the first node, along with the query, to generate an initial answer. We then pass this answer, the query, and the context of the second node as input into a “refine prompt” to generate a refined answer. We refine through N-1 nodes, where N is the total number of nodes.
###  COMPACT `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.ResponseMode.COMPACT "Permanent link")

```
COMPACT = 'compact'

```

Compact and refine mode first combine text chunks into larger consolidated chunks that more fully utilize the available context window, then refine answers across them. This mode is faster than refine since we make fewer calls to the LLM.
###  SIMPLE_SUMMARIZE `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.ResponseMode.SIMPLE_SUMMARIZE "Permanent link")

```
SIMPLE_SUMMARIZE = 'simple_summarize'

```

Merge all text chunks into one, and make a LLM call. This will fail if the merged text chunk exceeds the context window size.
###  TREE_SUMMARIZE `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.ResponseMode.TREE_SUMMARIZE "Permanent link")

```
TREE_SUMMARIZE = 'tree_summarize'

```

Build a tree index over the set of candidate nodes, with a summary prompt seeded with the query. The tree is built in a bottoms-up fashion, and in the end the root node is returned as the response
###  GENERATION `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.ResponseMode.GENERATION "Permanent link")

```
GENERATION = 'generation'

```

Ignore context, just use LLM to generate a response.
###  NO_TEXT `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.ResponseMode.NO_TEXT "Permanent link")

```
NO_TEXT = 'no_text'

```

Return the retrieved context nodes, without synthesizing a final response.
###  CONTEXT_ONLY `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.ResponseMode.CONTEXT_ONLY "Permanent link")

```
CONTEXT_ONLY = 'context_only'

```

Returns a concatenated string of all text chunks.
###  ACCUMULATE `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.ResponseMode.ACCUMULATE "Permanent link")

```
ACCUMULATE = 'accumulate'

```

Synthesize a response for each text chunk, and then return the concatenation.
###  COMPACT_ACCUMULATE `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.ResponseMode.COMPACT_ACCUMULATE "Permanent link")

```
COMPACT_ACCUMULATE = 'compact_accumulate'

```

Compact and accumulate mode first combine text chunks into larger consolidated chunks that more fully utilize the available context window, then accumulate answers for each of them and finally return the concatenation. This mode is faster than accumulate since we make fewer calls to the LLM.
##  get_response_synthesizer [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/simple_summarize/#llama_index.core.response_synthesizers.get_response_synthesizer "Permanent link")

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
options: members: - SimpleSummarize
