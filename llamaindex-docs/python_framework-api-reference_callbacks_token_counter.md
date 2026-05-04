# Token counter
##  TokenCountingEvent `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/token_counter/#llama_index.core.callbacks.token_counting.TokenCountingEvent "Permanent link")
TokenCountingEvent(prompt: str, completion: str, completion_token_count: int, prompt_token_count: int, total_token_count: int = 0, event_id: str = '')
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  _required_  |  
|  `completion`  |  _required_  |  
|  `completion_token_count`  |  _required_  |  
|  `prompt_token_count`  |  _required_  |  
|  `total_token_count`  |  
|  `event_id`  |  
Source code in `llama-index-core/llama_index/core/callbacks/token_counting.py`  
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
```
 | 
```
@dataclass
classTokenCountingEvent:
    prompt: str
    completion: str
    completion_token_count: int
    prompt_token_count: int
    total_token_count: int = 0
    event_id: str = ""

    def__post_init__(self) -> None:
        self.total_token_count = self.prompt_token_count + self.completion_token_count

```
 |  
| --- | --- |  
##  TokenCountingHandler [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/token_counter/#llama_index.core.callbacks.token_counting.TokenCountingHandler "Permanent link")
Bases: `PythonicallyPrintingBaseHandler`
Callback handler for counting tokens in LLM and Embedding events.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `tokenizer`  |  `Optional[Callable[[str], List]]`  |  Tokenizer to use. Defaults to the global tokenizer (see llama_index.core.utils.globals_helper).  |  `None`  |  
|  `event_starts_to_ignore`  |  `Optional[List[CBEventType[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.schema.CBEventType "CBEventType \(llama_index.core.callbacks.schema.CBEventType\)")]]`  |  List of event types to ignore at the start of a trace.  |  `None`  |  
|  `event_ends_to_ignore`  |  `Optional[List[CBEventType[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.schema.CBEventType "CBEventType \(llama_index.core.callbacks.schema.CBEventType\)")]]`  |  List of event types to ignore at the end of a trace.  |  `None`  |  
|  `token_budget`  |  `Optional[int]`  |  Optional maximum allowed total LLM token usage across the lifetime of this handler instance. If exceeded, a ValueError is raised. (Currently applies to LLM token counts only.)  |  `None`  |  
Source code in `llama-index-core/llama_index/core/callbacks/token_counting.py`  
| 
```
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
```
 | 
```
classTokenCountingHandler(PythonicallyPrintingBaseHandler):
"""
    Callback handler for counting tokens in LLM and Embedding events.

    Args:
        tokenizer:
            Tokenizer to use. Defaults to the global tokenizer
            (see llama_index.core.utils.globals_helper).
        event_starts_to_ignore: List of event types to ignore at the start of a trace.
        event_ends_to_ignore: List of event types to ignore at the end of a trace.
        token_budget:
            Optional maximum allowed total LLM token usage across the lifetime of this
            handler instance. If exceeded, a ValueError is raised. (Currently applies
            to LLM token counts only.)

    """

    def__init__(
        self,
        tokenizer: Optional[Callable[[str], List]] = None,
        event_starts_to_ignore: Optional[List[CBEventType]] = None,
        event_ends_to_ignore: Optional[List[CBEventType]] = None,
        verbose: bool = False,
        logger: Optional[logging.Logger] = None,
        token_budget: Optional[int] = None,
    ) -> None:
        self.llm_token_counts: List[TokenCountingEvent] = []
        self.embedding_token_counts: List[TokenCountingEvent] = []
        self.token_budget = token_budget
        self.tokenizer = tokenizer or get_tokenizer()

        self._token_counter = TokenCounter(tokenizer=self.tokenizer)
        self._verbose = verbose

        super().__init__(
            event_starts_to_ignore=event_starts_to_ignore or [],
            event_ends_to_ignore=event_ends_to_ignore or [],
            logger=logger,
        )

    defstart_trace(self, trace_id: Optional[str] = None) -> None:
        return

    defend_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        return

    def_check_budget(self) -> None:
        if (
            self.token_budget is not None
            and self.total_llm_token_count  self.token_budget
        ):
            raise ValueError(
                f"Token budget exceeded! Limit: {self.token_budget}, "
                f"Current: {self.total_llm_token_count}"
            )

    defon_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        self._check_budget()
        return event_id

    defon_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
"""Count the LLM or Embedding tokens as needed."""
        if (
            event_type == CBEventType.LLM
            and event_type not in self.event_ends_to_ignore
            and payload is not None
        ):
            self.llm_token_counts.append(
                get_llm_token_counts(
                    token_counter=self._token_counter,
                    payload=payload,
                    event_id=event_id,
                )
            )

            if self._verbose:
                self._print(
                    "LLM Prompt Token Usage: "
                    f"{self.llm_token_counts[-1].prompt_token_count}\n"
                    "LLM Completion Token Usage: "
                    f"{self.llm_token_counts[-1].completion_token_count}",
                )
            self._check_budget()
        elif (
            event_type == CBEventType.EMBEDDING
            and event_type not in self.event_ends_to_ignore
            and payload is not None
        ):
            total_chunk_tokens = 0
            for chunk in payload.get(EventPayload.CHUNKS, []):
                self.embedding_token_counts.append(
                    TokenCountingEvent(
                        event_id=event_id,
                        prompt=chunk,
                        prompt_token_count=self._token_counter.get_string_tokens(chunk),
                        completion="",
                        completion_token_count=0,
                    )
                )
                total_chunk_tokens += self.embedding_token_counts[-1].total_token_count

            if self._verbose:
                self._print(f"Embedding Token Usage: {total_chunk_tokens}")

    @property
    deftotal_llm_token_count(self) -> int:
"""Get the current total LLM token count."""
        return sum([x.total_token_count for x in self.llm_token_counts])

    @property
    defprompt_llm_token_count(self) -> int:
"""Get the current total LLM prompt token count."""
        return sum([x.prompt_token_count for x in self.llm_token_counts])

    @property
    defcompletion_llm_token_count(self) -> int:
"""Get the current total LLM completion token count."""
        return sum([x.completion_token_count for x in self.llm_token_counts])

    @property
    deftotal_embedding_token_count(self) -> int:
"""Get the current total Embedding token count."""
        return sum([x.total_token_count for x in self.embedding_token_counts])

    defreset_counts(self) -> None:
"""Reset the token counts."""
        self.llm_token_counts = []
        self.embedding_token_counts = []

```
 |  
| --- | --- |  
###  total_llm_token_count `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/token_counter/#llama_index.core.callbacks.token_counting.TokenCountingHandler.total_llm_token_count "Permanent link")

```
total_llm_token_count: 

```

Get the current total LLM token count.
###  prompt_llm_token_count `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/token_counter/#llama_index.core.callbacks.token_counting.TokenCountingHandler.prompt_llm_token_count "Permanent link")

```
prompt_llm_token_count: 

```

Get the current total LLM prompt token count.
###  completion_llm_token_count `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/token_counter/#llama_index.core.callbacks.token_counting.TokenCountingHandler.completion_llm_token_count "Permanent link")

```
completion_llm_token_count: 

```

Get the current total LLM completion token count.
###  total_embedding_token_count `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/token_counter/#llama_index.core.callbacks.token_counting.TokenCountingHandler.total_embedding_token_count "Permanent link")

```
total_embedding_token_count: 

```

Get the current total Embedding token count.
###  on_event_end [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/token_counter/#llama_index.core.callbacks.token_counting.TokenCountingHandler.on_event_end "Permanent link")

```
on_event_end(
    event_type: ,
    payload: Optional[[, ]] = None,
    event_id:  = "",
    **kwargs: 
) -> None

```

Count the LLM or Embedding tokens as needed.
Source code in `llama-index-core/llama_index/core/callbacks/token_counting.py`  
| 
```
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
```
 | 
```
defon_event_end(
    self,
    event_type: CBEventType,
    payload: Optional[Dict[str, Any]] = None,
    event_id: str = "",
    **kwargs: Any,
) -> None:
"""Count the LLM or Embedding tokens as needed."""
    if (
        event_type == CBEventType.LLM
        and event_type not in self.event_ends_to_ignore
        and payload is not None
    ):
        self.llm_token_counts.append(
            get_llm_token_counts(
                token_counter=self._token_counter,
                payload=payload,
                event_id=event_id,
            )
        )

        if self._verbose:
            self._print(
                "LLM Prompt Token Usage: "
                f"{self.llm_token_counts[-1].prompt_token_count}\n"
                "LLM Completion Token Usage: "
                f"{self.llm_token_counts[-1].completion_token_count}",
            )
        self._check_budget()
    elif (
        event_type == CBEventType.EMBEDDING
        and event_type not in self.event_ends_to_ignore
        and payload is not None
    ):
        total_chunk_tokens = 0
        for chunk in payload.get(EventPayload.CHUNKS, []):
            self.embedding_token_counts.append(
                TokenCountingEvent(
                    event_id=event_id,
                    prompt=chunk,
                    prompt_token_count=self._token_counter.get_string_tokens(chunk),
                    completion="",
                    completion_token_count=0,
                )
            )
            total_chunk_tokens += self.embedding_token_counts[-1].total_token_count

        if self._verbose:
            self._print(f"Embedding Token Usage: {total_chunk_tokens}")

```
 |  
| --- | --- |  
###  reset_counts [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/token_counter/#llama_index.core.callbacks.token_counting.TokenCountingHandler.reset_counts "Permanent link")

```
reset_counts() -> None

```

Reset the token counts.
Source code in `llama-index-core/llama_index/core/callbacks/token_counting.py`  
| 
```
284
285
286
287
```
 | 
```
defreset_counts(self) -> None:
"""Reset the token counts."""
    self.llm_token_counts = []
    self.embedding_token_counts = []

```
 |  
| --- | --- |  
##  get_tokens_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/token_counter/#llama_index.core.callbacks.token_counting.get_tokens_from_response "Permanent link")

```
get_tokens_from_response(
    response: Union[, ]
) -> Tuple[, ]

```

Get the token counts from a raw response.
Source code in `llama-index-core/llama_index/core/callbacks/token_counting.py`  
| 
```
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
```
 | 
```
defget_tokens_from_response(
    response: Union["CompletionResponse", "ChatResponse"],
) -> Tuple[int, int]:
"""Get the token counts from a raw response."""
    raw_response = response.raw
    if not isinstance(raw_response, dict):
        raw_response = dict(raw_response or {})

    usage = raw_response.get("usage", raw_response.get("usage_metadata", {}))
    if usage is None:
        usage = response.additional_kwargs

    if not usage:
        return 0, 0

    if not isinstance(usage, dict):
        usage = usage.model_dump()

    possible_input_keys = ("prompt_tokens", "input_tokens", "prompt_token_count")
    possible_output_keys = (
        "completion_tokens",
        "output_tokens",
        "candidates_token_count",
    )

    prompt_tokens = 0
    for input_key in possible_input_keys:
        if input_key in usage:
            prompt_tokens = usage[input_key]
            break

    completion_tokens = 0
    for output_key in possible_output_keys:
        if output_key in usage:
            completion_tokens = usage[output_key]
            break

    return prompt_tokens, completion_tokens

```
 |  
| --- | --- |  
options: members: - TokenCountingHandler
