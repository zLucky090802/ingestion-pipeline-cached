# Function
##  FunctionTool [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.FunctionTool "Permanent link")
Bases: 
Function Tool.
A tool that takes in a function, optionally handles workflow context, and allows the use of callbacks. The callback can return a new ToolOutput to override the default one or a string that will be used as the final content.
Source code in `llama-index-core/llama_index/core/tools/function_tool.py`  
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
```
 | 
```
classFunctionTool(AsyncBaseTool):
"""
    Function Tool.

    A tool that takes in a function, optionally handles workflow context,
    and allows the use of callbacks. The callback can return a new ToolOutput
    to override the default one or a string that will be used as the final content.
    """

    def__init__(
        self,
        fn: Optional[Callable[..., Any]] = None,
        metadata: Optional[ToolMetadata] = None,
        async_fn: Optional[AsyncCallable] = None,
        callback: Optional[Callable[..., Any]] = None,
        async_callback: Optional[Callable[..., Any]] = None,
        partial_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        if fn is None and async_fn is None:
            raise ValueError("fn or async_fn must be provided.")

        # Handle function (sync and async)
        self._real_fn = fn or async_fn
        if async_fn is not None:
            self._async_fn = async_fn
            self._fn = fn or async_to_sync(async_fn)
        else:
            assert fn is not None
            if inspect.iscoroutinefunction(fn):
                self._async_fn = fn
                self._fn = async_to_sync(fn)
            else:
                self._fn = fn
                self._async_fn = sync_to_async(fn)

        # Determine if the function requires context by inspecting its signature
        fn_to_inspect = fn or async_fn
        assert fn_to_inspect is not None
        sig = inspect.signature(fn_to_inspect)
        self.requires_context = any(
            _is_context_param(param.annotation) for param in sig.parameters.values()
        )
        self.ctx_param_name = (
            next(
                param.name
                for param in sig.parameters.values()
                if _is_context_param(param.annotation)
            )
            if self.requires_context
            else None
        )

        if metadata is None:
            raise ValueError("metadata must be provided")
        self._metadata = metadata

        # Handle callback (sync and async)
        self._callback = None
        if callback is not None:
            self._callback = callback
        elif async_callback is not None:
            self._callback = async_to_sync(async_callback)

        self._async_callback = None
        if async_callback is not None:
            self._async_callback = async_callback
        elif self._callback is not None:
            self._async_callback = sync_to_async(self._callback)

        self.partial_params = partial_params or {}

        # Extract actual default values from FieldInfo defaults so they are
        # applied when the function is called without those arguments.
        self._field_defaults: Dict[str, Any] = {}
        for param in sig.parameters.values():
            if isinstance(param.default, FieldInfo) and not param.default.is_required():
                self._field_defaults[param.name] = param.default.get_default(
                    call_default_factory=True
                )

    def_run_sync_callback(self, result: Any) -> CallbackReturn:
"""
        Runs the sync callback, if provided, and returns either a ToolOutput
        to override the default output or a string to override the content.
        """
        if self._callback:
            ret: CallbackReturn = self._callback(result)
            return ret
        return None

    async def_run_async_callback(self, result: Any) -> CallbackReturn:
"""
        Runs the async callback, if provided, and returns either a ToolOutput
        to override the default output or a string to override the content.
        """
        if self._async_callback:
            ret: CallbackReturn = await self._async_callback(result)
            return ret
        return None

    @classmethod
    deffrom_defaults(
        cls,
        fn: Optional[Callable[..., Any]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        return_direct: bool = False,
        fn_schema: Optional[Type[BaseModel]] = None,
        async_fn: Optional[AsyncCallable] = None,
        tool_metadata: Optional[ToolMetadata] = None,
        callback: Optional[Callable[[Any], Any]] = None,
        async_callback: Optional[AsyncCallable] = None,
        partial_params: Optional[Dict[str, Any]] = None,
    ) -> "FunctionTool":
        partial_params = partial_params or {}

        if tool_metadata is None:
            fn_to_parse = fn or async_fn
            assert fn_to_parse is not None, "fn must be provided"
            name = name or fn_to_parse.__name__
            docstring = fn_to_parse.__doc__ or ""

            # Get function signature
            fn_sig = inspect.signature(fn_to_parse)
            fn_params = set(fn_sig.parameters.keys())

            # 1. Extract docstring param descriptions
            param_docs, unknown_params = cls.extract_param_docs(docstring, fn_params)

            # 2. Filter context and self in a single pass
            ctx_param_name = None
            has_self = False
            filtered_params = []
            for param in fn_sig.parameters.values():
                if _is_context_param(param.annotation):
                    ctx_param_name = param.name
                    continue
                if param.name == "self":
                    has_self = True
                    continue
                filtered_params.append(param)

            # 3. Remove FieldInfo defaults and partial_params
            final_params = [
                param.replace(default=inspect.Parameter.empty)
                if isinstance(param.default, FieldInfo)
                else param
                for param in filtered_params
                if param.name not in (partial_params or {})
            ]

            # 4. Replace signature in one go
            fn_sig = fn_sig.replace(parameters=final_params)

            # 5. Build description
            if description is None:
                description = f"{name}{fn_sig}\n"
                if docstring:
                    description += docstring

                description = description.strip()

            # 6. Build fn_schema only if not already provided
            if fn_schema is None:
                ignore_fields = []
                if ctx_param_name:
                    ignore_fields.append(ctx_param_name)
                if has_self:
                    ignore_fields.append("self")
                ignore_fields.extend(partial_params.keys())

                fn_schema = create_schema_from_function(
                    f"{name}",
                    fn_to_parse,
                    additional_fields=None,
                    ignore_fields=ignore_fields,
                )
                if fn_schema is not None and param_docs:
                    for param_name, field in fn_schema.model_fields.items():
                        if not field.description and param_name in param_docs:
                            field.description = param_docs[param_name].strip()

            tool_metadata = ToolMetadata(
                name=name,
                description=description,
                fn_schema=fn_schema,
                return_direct=return_direct,
            )
        return cls(
            fn=fn,
            metadata=tool_metadata,
            async_fn=async_fn,
            callback=callback,
            async_callback=async_callback,
            partial_params=partial_params,
        )

    @property
    defmetadata(self) -> ToolMetadata:
"""Metadata."""
        return self._metadata

    @property
    deffn(self) -> Callable[..., Any]:
"""Function."""
        return self._fn

    @property
    defasync_fn(self) -> AsyncCallable:
"""Async function."""
        return self._async_fn

    @property
    defreal_fn(self) -> Union[Callable[..., Any], AsyncCallable]:
"""Real function."""
        if self._real_fn is None:
            raise ValueError("Real function is not set!")

        return self._real_fn

    def_parse_tool_output(self, raw_output: Any) -> List[ContentBlock]:
"""Parse tool output into content blocks."""
        if isinstance(
            raw_output, (TextBlock, ImageBlock, AudioBlock, CitableBlock, CitationBlock)
        ):
            return [raw_output]
        elif isinstance(raw_output, list) and all(
            isinstance(
                item, (TextBlock, ImageBlock, AudioBlock, CitableBlock, CitationBlock)
            )
            for item in raw_output
        ):
            return raw_output
        elif isinstance(raw_output, (BaseNode, Document)):
            return [TextBlock(text=raw_output.get_content())]
        elif isinstance(raw_output, list) and all(
            isinstance(item, (BaseNode, Document)) for item in raw_output
        ):
            return [TextBlock(text=item.get_content()) for item in raw_output]
        else:
            return [TextBlock(text=str(raw_output))]

    def__call__(self, *args: Any, **kwargs: Any) -> ToolOutput:
        all_kwargs = {**self.partial_params, **kwargs}
        return self.call(*args, **all_kwargs)

    defcall(self, *args: Any, **kwargs: Any) -> ToolOutput:
"""Sync Call."""
        all_kwargs = {**self._field_defaults, **self.partial_params, **kwargs}
        if self.requires_context and self.ctx_param_name is not None:
            if self.ctx_param_name not in all_kwargs:
                raise ValueError("Context is required for this tool")

        raw_output = self._fn(*args, **all_kwargs)

        # Exclude the Context param from the tool output so that the Context can be serialized
        tool_output_kwargs = {
            k: v for k, v in all_kwargs.items() if k != self.ctx_param_name
        }

        # Parse tool output into content blocks
        output_blocks = self._parse_tool_output(raw_output)

        # Default ToolOutput based on the raw output
        default_output = ToolOutput(
            blocks=output_blocks,
            tool_name=self.metadata.get_name(),
            raw_input={"args": args, "kwargs": tool_output_kwargs},
            raw_output=raw_output,
        )
        # Check for a sync callback override
        callback_result = self._run_sync_callback(raw_output)
        if callback_result is not None:
            if isinstance(callback_result, ToolOutput):
                return callback_result
            else:
                # Assume callback_result is a string to override the content.
                return ToolOutput(
                    content=str(callback_result),
                    tool_name=self.metadata.get_name(),
                    raw_input={"args": args, "kwargs": tool_output_kwargs},
                    raw_output=raw_output,
                )
        return default_output

    async defacall(self, *args: Any, **kwargs: Any) -> ToolOutput:
"""Async Call."""
        all_kwargs = {**self._field_defaults, **self.partial_params, **kwargs}
        if self.requires_context and self.ctx_param_name is not None:
            if self.ctx_param_name not in all_kwargs:
                raise ValueError("Context is required for this tool")

        raw_output = await self._async_fn(*args, **all_kwargs)

        # Exclude the Context param from the tool output so that the Context can be serialized
        tool_output_kwargs = {
            k: v for k, v in all_kwargs.items() if k != self.ctx_param_name
        }

        # Parse tool output into content blocks
        output_blocks = self._parse_tool_output(raw_output)

        # Default ToolOutput based on the raw output
        default_output = ToolOutput(
            blocks=output_blocks,
            tool_name=self.metadata.get_name(),
            raw_input={"args": args, "kwargs": tool_output_kwargs},
            raw_output=raw_output,
        )
        # Check for an async callback override
        callback_result = await self._run_async_callback(raw_output)
        if callback_result is not None:
            if isinstance(callback_result, ToolOutput):
                return callback_result
            else:
                # Assume callback_result is a string to override the content.
                return ToolOutput(
                    content=str(callback_result),
                    tool_name=self.metadata.get_name(),
                    raw_input={"args": args, "kwargs": tool_output_kwargs},
                    raw_output=raw_output,
                )
        return default_output

    defto_langchain_tool(self, **langchain_tool_kwargs: Any) -> "Tool":
"""To langchain tool."""
        fromllama_index.core.bridge.langchainimport Tool

        langchain_tool_kwargs = self._process_langchain_tool_kwargs(
            langchain_tool_kwargs
        )
        return Tool.from_function(
            func=self.fn,
            coroutine=self.async_fn,
            **langchain_tool_kwargs,
        )

    defto_langchain_structured_tool(
        self, **langchain_tool_kwargs: Any
    ) -> "StructuredTool":
"""To langchain structured tool."""
        fromllama_index.core.bridge.langchainimport StructuredTool

        langchain_tool_kwargs = self._process_langchain_tool_kwargs(
            langchain_tool_kwargs
        )
        return StructuredTool.from_function(
            func=self.fn,
            coroutine=self.async_fn,
            **langchain_tool_kwargs,
        )

    @staticmethod
    defextract_param_docs(
        docstring: str, fn_params: Optional[set] = None
    ) -> Tuple[dict, set]:
"""
        Parses param descriptions from a docstring.

        Returns:
            - param_docs: Only for params in fn_params with non-conflicting descriptions.
            - unknown_params: Params found in docstring but not in fn_params (ignored in final output).

        """
        raw_param_docs: dict[str, str] = {}
        unknown_params = set()

        deftry_add_param(name: str, desc: str) -> None:
            desc = desc.strip()
            if fn_params and name not in fn_params:
                unknown_params.add(name)
                return
            if name in raw_param_docs and raw_param_docs[name] != desc:
                return
            raw_param_docs[name] = desc

        # Sphinx style
        for match in re.finditer(r":param (\w+): (.+)", docstring):
            try_add_param(match.group(1), match.group(2))

        # Google style
        for match in re.finditer(
            r"^\s*(\w+)\s*\(.*?\):\s*(.+)$", docstring, re.MULTILINE
        ):
            try_add_param(match.group(1), match.group(2))

        # Javadoc style
        for match in re.finditer(r"@param (\w+)\s+(.+)", docstring):
            try_add_param(match.group(1), match.group(2))

        return raw_param_docs, unknown_params

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.FunctionTool.metadata "Permanent link")

```
metadata: 

```

Metadata.
###  fn `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.FunctionTool.fn "Permanent link")

```
fn: Callable[..., ]

```

Function.
###  async_fn `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.FunctionTool.async_fn "Permanent link")

```
async_fn: AsyncCallable

```

Async function.
###  real_fn `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.FunctionTool.real_fn "Permanent link")

```
real_fn: Union[Callable[..., ], AsyncCallable]

```

Real function.
###  call [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.FunctionTool.call "Permanent link")

```
call(*args: , **kwargs: ) -> 

```

Sync Call.
Source code in `llama-index-core/llama_index/core/tools/function_tool.py`  
| 
```
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
```
 | 
```
defcall(self, *args: Any, **kwargs: Any) -> ToolOutput:
"""Sync Call."""
    all_kwargs = {**self._field_defaults, **self.partial_params, **kwargs}
    if self.requires_context and self.ctx_param_name is not None:
        if self.ctx_param_name not in all_kwargs:
            raise ValueError("Context is required for this tool")

    raw_output = self._fn(*args, **all_kwargs)

    # Exclude the Context param from the tool output so that the Context can be serialized
    tool_output_kwargs = {
        k: v for k, v in all_kwargs.items() if k != self.ctx_param_name
    }

    # Parse tool output into content blocks
    output_blocks = self._parse_tool_output(raw_output)

    # Default ToolOutput based on the raw output
    default_output = ToolOutput(
        blocks=output_blocks,
        tool_name=self.metadata.get_name(),
        raw_input={"args": args, "kwargs": tool_output_kwargs},
        raw_output=raw_output,
    )
    # Check for a sync callback override
    callback_result = self._run_sync_callback(raw_output)
    if callback_result is not None:
        if isinstance(callback_result, ToolOutput):
            return callback_result
        else:
            # Assume callback_result is a string to override the content.
            return ToolOutput(
                content=str(callback_result),
                tool_name=self.metadata.get_name(),
                raw_input={"args": args, "kwargs": tool_output_kwargs},
                raw_output=raw_output,
            )
    return default_output

```
 |  
| --- | --- |  
###  acall [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.FunctionTool.acall "Permanent link")

```
acall(*args: , **kwargs: ) -> 

```

Async Call.
Source code in `llama-index-core/llama_index/core/tools/function_tool.py`  
| 
```
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
```
 | 
```
async defacall(self, *args: Any, **kwargs: Any) -> ToolOutput:
"""Async Call."""
    all_kwargs = {**self._field_defaults, **self.partial_params, **kwargs}
    if self.requires_context and self.ctx_param_name is not None:
        if self.ctx_param_name not in all_kwargs:
            raise ValueError("Context is required for this tool")

    raw_output = await self._async_fn(*args, **all_kwargs)

    # Exclude the Context param from the tool output so that the Context can be serialized
    tool_output_kwargs = {
        k: v for k, v in all_kwargs.items() if k != self.ctx_param_name
    }

    # Parse tool output into content blocks
    output_blocks = self._parse_tool_output(raw_output)

    # Default ToolOutput based on the raw output
    default_output = ToolOutput(
        blocks=output_blocks,
        tool_name=self.metadata.get_name(),
        raw_input={"args": args, "kwargs": tool_output_kwargs},
        raw_output=raw_output,
    )
    # Check for an async callback override
    callback_result = await self._run_async_callback(raw_output)
    if callback_result is not None:
        if isinstance(callback_result, ToolOutput):
            return callback_result
        else:
            # Assume callback_result is a string to override the content.
            return ToolOutput(
                content=str(callback_result),
                tool_name=self.metadata.get_name(),
                raw_input={"args": args, "kwargs": tool_output_kwargs},
                raw_output=raw_output,
            )
    return default_output

```
 |  
| --- | --- |  
###  to_langchain_tool [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.FunctionTool.to_langchain_tool "Permanent link")

```
to_langchain_tool(**langchain_tool_kwargs: ) -> 

```

To langchain tool.
Source code in `llama-index-core/llama_index/core/tools/function_tool.py`  
| 
```
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
```
 | 
```
defto_langchain_tool(self, **langchain_tool_kwargs: Any) -> "Tool":
"""To langchain tool."""
    fromllama_index.core.bridge.langchainimport Tool

    langchain_tool_kwargs = self._process_langchain_tool_kwargs(
        langchain_tool_kwargs
    )
    return Tool.from_function(
        func=self.fn,
        coroutine=self.async_fn,
        **langchain_tool_kwargs,
    )

```
 |  
| --- | --- |  
###  to_langchain_structured_tool [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.FunctionTool.to_langchain_structured_tool "Permanent link")

```
to_langchain_structured_tool(
    **langchain_tool_kwargs: ,
) -> StructuredTool

```

To langchain structured tool.
Source code in `llama-index-core/llama_index/core/tools/function_tool.py`  
| 
```
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
```
 | 
```
defto_langchain_structured_tool(
    self, **langchain_tool_kwargs: Any
) -> "StructuredTool":
"""To langchain structured tool."""
    fromllama_index.core.bridge.langchainimport StructuredTool

    langchain_tool_kwargs = self._process_langchain_tool_kwargs(
        langchain_tool_kwargs
    )
    return StructuredTool.from_function(
        func=self.fn,
        coroutine=self.async_fn,
        **langchain_tool_kwargs,
    )

```
 |  
| --- | --- |  
###  extract_param_docs `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.FunctionTool.extract_param_docs "Permanent link")

```
extract_param_docs(
    docstring: , fn_params: Optional[] = None
) -> Tuple[, ]

```

Parses param descriptions from a docstring.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `dict`  | 
  * param_docs: Only for params in fn_params with non-conflicting descriptions.

 |  
| 
  * unknown_params: Params found in docstring but not in fn_params (ignored in final output).

 |  
Source code in `llama-index-core/llama_index/core/tools/function_tool.py`  
| 
```
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
```
 | 
```
@staticmethod
defextract_param_docs(
    docstring: str, fn_params: Optional[set] = None
) -> Tuple[dict, set]:
"""
    Parses param descriptions from a docstring.

    Returns:
        - param_docs: Only for params in fn_params with non-conflicting descriptions.
        - unknown_params: Params found in docstring but not in fn_params (ignored in final output).

    """
    raw_param_docs: dict[str, str] = {}
    unknown_params = set()

    deftry_add_param(name: str, desc: str) -> None:
        desc = desc.strip()
        if fn_params and name not in fn_params:
            unknown_params.add(name)
            return
        if name in raw_param_docs and raw_param_docs[name] != desc:
            return
        raw_param_docs[name] = desc

    # Sphinx style
    for match in re.finditer(r":param (\w+): (.+)", docstring):
        try_add_param(match.group(1), match.group(2))

    # Google style
    for match in re.finditer(
        r"^\s*(\w+)\s*\(.*?\):\s*(.+)$", docstring, re.MULTILINE
    ):
        try_add_param(match.group(1), match.group(2))

    # Javadoc style
    for match in re.finditer(r"@param (\w+)\s+(.+)", docstring):
        try_add_param(match.group(1), match.group(2))

    return raw_param_docs, unknown_params

```
 |  
| --- | --- |  
##  sync_to_async [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.sync_to_async "Permanent link")

```
sync_to_async(fn: Callable[..., ]) -> AsyncCallable

```

Sync to async.
Source code in `llama-index-core/llama_index/core/tools/function_tool.py`  
| 
```
44
45
46
47
48
49
50
51
```
 | 
```
defsync_to_async(fn: Callable[..., Any]) -> AsyncCallable:
"""Sync to async."""

    async def_async_wrapped_fn(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))

    return _async_wrapped_fn

```
 |  
| --- | --- |  
##  async_to_sync [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.async_to_sync "Permanent link")

```
async_to_sync(func_async: AsyncCallable) -> Callable

```

Async to sync.
Source code in `llama-index-core/llama_index/core/tools/function_tool.py`  
| 
```
54
55
56
57
58
59
60
```
 | 
```
defasync_to_sync(func_async: AsyncCallable) -> Callable:
"""Async to sync."""

    def_sync_wrapped_fn(*args: Any, **kwargs: Any) -> Any:
        return asyncio_run(func_async(*args, **kwargs))  # type: ignore[arg-type]

    return _sync_wrapped_fn

```
 |  
| --- | --- |  
options: members: - FunctionTool
