# Wandb
##  WandbCallbackHandler [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/wandb/#llama_index.callbacks.wandb.WandbCallbackHandler "Permanent link")
Bases: 
Callback handler that logs events to wandb.
NOTE: this is a beta feature. The usage within our codebase, and the interface may change.
Use the `WandbCallbackHandler` to log trace events to wandb. This handler is useful for debugging and visualizing the trace events. It captures the payload of the events and logs them to wandb. The handler also tracks the start and end of events. This is particularly useful for debugging your LLM calls.
The `WandbCallbackHandler` can also be used to log the indices and graphs to wandb using the `persist_index` method. This will save the indexes as artifacts in wandb. The `load_storage_context` method can be used to load the indexes from wandb artifacts. This method will return a `StorageContext` object that can be used to build the index, using `load_index_from_storage`, `load_indices_from_storage` or `load_graph_from_storage` functions.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `event_starts_to_ignore`  |  `Optional[List[CBEventType[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.schema.CBEventType "CBEventType \(llama_index.core.callbacks.schema.CBEventType\)")]]`  |  list of event types to ignore when tracking event starts.  |  `None`  |  
|  `event_ends_to_ignore`  |  `Optional[List[CBEventType[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.schema.CBEventType "CBEventType \(llama_index.core.callbacks.schema.CBEventType\)")]]`  |  list of event types to ignore when tracking event ends.  |  `None`  |  
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-wandb/llama_index/callbacks/wandb/base.py`  
| 
```
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
```
 | 
```
classWandbCallbackHandler(BaseCallbackHandler):
"""
    Callback handler that logs events to wandb.

    NOTE: this is a beta feature. The usage within our codebase, and the interface
    may change.

    Use the `WandbCallbackHandler` to log trace events to wandb. This handler is
    useful for debugging and visualizing the trace events. It captures the payload of
    the events and logs them to wandb. The handler also tracks the start and end of
    events. This is particularly useful for debugging your LLM calls.

    The `WandbCallbackHandler` can also be used to log the indices and graphs to wandb
    using the `persist_index` method. This will save the indexes as artifacts in wandb.
    The `load_storage_context` method can be used to load the indexes from wandb
    artifacts. This method will return a `StorageContext` object that can be used to
    build the index, using `load_index_from_storage`, `load_indices_from_storage` or
    `load_graph_from_storage` functions.


    Args:
        event_starts_to_ignore (Optional[List[CBEventType]]): list of event types to
            ignore when tracking event starts.
        event_ends_to_ignore (Optional[List[CBEventType]]): list of event types to
            ignore when tracking event ends.

    """

    def__init__(
        self,
        run_args: Optional[WandbRunArgs] = None,
        tokenizer: Optional[Callable[[str], List]] = None,
        event_starts_to_ignore: Optional[List[CBEventType]] = None,
        event_ends_to_ignore: Optional[List[CBEventType]] = None,
    ) -> None:
        try:
            importwandb
            fromwandb.sdk.data_typesimport trace_tree

            self._wandb = wandb
            self._trace_tree = trace_tree
        except ImportError:
            raise ImportError(
                "WandbCallbackHandler requires wandb. "
                "Please install it with `pip install wandb`."
            )

        fromllama_index.core.indicesimport (
            ComposableGraph,
            GPTEmptyIndex,
            GPTKeywordTableIndex,
            GPTRAKEKeywordTableIndex,
            GPTSimpleKeywordTableIndex,
            GPTSQLStructStoreIndex,
            GPTTreeIndex,
            GPTVectorStoreIndex,
            SummaryIndex,
        )

        self._IndexType = (
            ComposableGraph,
            GPTKeywordTableIndex,
            GPTSimpleKeywordTableIndex,
            GPTRAKEKeywordTableIndex,
            SummaryIndex,
            GPTEmptyIndex,
            GPTTreeIndex,
            GPTVectorStoreIndex,
            GPTSQLStructStoreIndex,
        )

        self._run_args = run_args
        # Check if a W&B run is already initialized; if not, initialize one
        self._ensure_run(should_print_url=(self._wandb.run is None))  # type: ignore[attr-defined]

        self._event_pairs_by_id: Dict[str, List[CBEvent]] = defaultdict(list)
        self._cur_trace_id: Optional[str] = None
        self._trace_map: Dict[str, List[str]] = defaultdict(list)

        self.tokenizer = tokenizer or get_tokenizer()
        self._token_counter = TokenCounter(tokenizer=self.tokenizer)

        event_starts_to_ignore = (
            event_starts_to_ignore if event_starts_to_ignore else []
        )
        event_ends_to_ignore = event_ends_to_ignore if event_ends_to_ignore else []
        super().__init__(
            event_starts_to_ignore=event_starts_to_ignore,
            event_ends_to_ignore=event_ends_to_ignore,
        )

    defon_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
"""
        Store event start data by event type.

        Args:
            event_type (CBEventType): event type to store.
            payload (Optional[Dict[str, Any]]): payload to store.
            event_id (str): event id to store.
            parent_id (str): parent event id.

        """
        event = CBEvent(event_type, payload=payload, id_=event_id)
        self._event_pairs_by_id[event.id_].append(event)
        return event.id_

    defon_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
"""
        Store event end data by event type.

        Args:
            event_type (CBEventType): event type to store.
            payload (Optional[Dict[str, Any]]): payload to store.
            event_id (str): event id to store.

        """
        event = CBEvent(event_type, payload=payload, id_=event_id)
        self._event_pairs_by_id[event.id_].append(event)
        self._trace_map = defaultdict(list)

    defstart_trace(self, trace_id: Optional[str] = None) -> None:
"""Launch a trace."""
        self._trace_map = defaultdict(list)
        self._cur_trace_id = trace_id
        self._start_time = datetime.now()

    defend_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        # Ensure W&B run is initialized
        self._ensure_run()

        self._trace_map = trace_map or defaultdict(list)
        self._end_time = datetime.now()

        # Log the trace map to wandb
        # We can control what trace ids we want to log here.
        self.log_trace_tree()

        # TODO (ayulockin): Log the LLM token counts to wandb when weave is ready

    deflog_trace_tree(self) -> None:
"""Log the trace tree to wandb."""
        try:
            child_nodes = self._trace_map["root"]
            root_span = self._convert_event_pair_to_wb_span(
                self._event_pairs_by_id[child_nodes[0]],
                trace_id=self._cur_trace_id if len(child_nodes)  1 else None,
            )

            if len(child_nodes) == 1:
                child_nodes = self._trace_map[child_nodes[0]]
                root_span = self._build_trace_tree(child_nodes, root_span)
            else:
                root_span = self._build_trace_tree(child_nodes, root_span)
            if root_span:
                root_trace = self._trace_tree.WBTraceTree(root_span)
                if self._wandb.run:  # type: ignore[attr-defined]
                    self._wandb.run.log({"trace": root_trace})  # type: ignore[attr-defined]
                self._wandb.termlog("Logged trace tree to W&B.")  # type: ignore[attr-defined]
        except Exception as e:
            print(f"Failed to log trace tree to W&B: {e}")
            # ignore errors to not break user code

    defpersist_index(
        self, index: "IndexType", index_name: str, persist_dir: Union[str, None] = None
    ) -> None:
"""
        Upload an index to wandb as an artifact. You can learn more about W&B
        artifacts here: https://docs.wandb.ai/guides/artifacts.

        For the `ComposableGraph` index, the root id is stored as artifact metadata.

        Args:
            index (IndexType): index to upload.
            index_name (str): name of the index. This will be used as the artifact name.
            persist_dir (Union[str, None]): directory to persist the index. If None, a
                temporary directory will be created and used.

        """
        _default_persist_dir = False
        if persist_dir is None:
            persist_dir = f"{self._wandb.run.dir}/storage"  # type: ignore
            _default_persist_dir = True
        if not os.path.exists(persist_dir):
            os.makedirs(persist_dir)

        if isinstance(index, self._IndexType):
            try:
                index.storage_context.persist(persist_dir)  # type: ignore

                metadata = None
                # For the `ComposableGraph` index, store the root id as metadata
                if isinstance(index, self._IndexType[0]):
                    root_id = index.root_id
                    metadata = {"root_id": root_id}

                self._upload_index_as_wb_artifact(persist_dir, index_name, metadata)
            except Exception as e:
                # Silently ignore errors to not break user code
                self._print_upload_index_fail_message(e)

        # clear the default storage dir
        if _default_persist_dir:
            shutil.rmtree(persist_dir, ignore_errors=True)

    defload_storage_context(
        self, artifact_url: str, index_download_dir: Union[str, None] = None
    ) -> "StorageContext":
"""
        Download an index from wandb and return a storage context.

        Use this storage context to load the index into memory using
        `load_index_from_storage`, `load_indices_from_storage` or
        `load_graph_from_storage` functions.

        Args:
            artifact_url (str): url of the artifact to download. The artifact url will
                be of the form: `entity/project/index_name:version` and can be found in
                the W&B UI.
            index_download_dir (Union[str, None]): directory to download the index to.

        """
        fromllama_index.core.storage.storage_contextimport StorageContext

        artifact = self._wandb.use_artifact(artifact_url, type="storage_context")  # type: ignore[attr-defined]
        artifact_dir = artifact.download(root=index_download_dir)

        return StorageContext.from_defaults(persist_dir=artifact_dir)

    def_upload_index_as_wb_artifact(
        self, dir_path: str, artifact_name: str, metadata: Optional[Dict]
    ) -> None:
"""Utility function to upload a dir to W&B as an artifact."""
        artifact = self._wandb.Artifact(artifact_name, type="storage_context")  # type: ignore[attr-defined]

        if metadata:
            artifact.metadata = metadata

        artifact.add_dir(dir_path)
        self._wandb.run.log_artifact(artifact)  # type: ignore

    def_build_trace_tree(
        self, events: List[str], span: "trace_tree.Span"
    ) -> "trace_tree.Span":
"""Build the trace tree from the trace map."""
        for child_event in events:
            child_span = self._convert_event_pair_to_wb_span(
                self._event_pairs_by_id[child_event]
            )
            child_span = self._build_trace_tree(
                self._trace_map[child_event], child_span
            )
            span.add_child_span(child_span)

        return span

    def_convert_event_pair_to_wb_span(
        self,
        event_pair: List[CBEvent],
        trace_id: Optional[str] = None,
    ) -> "trace_tree.Span":
"""Convert a pair of events to a wandb trace tree span."""
        start_time_ms, end_time_ms = self._get_time_in_ms(event_pair)

        if trace_id is None:
            event_type = event_pair[0].event_type
            span_kind = self._map_event_type_to_span_kind(event_type)
        else:
            event_type = trace_id  # type: ignore
            span_kind = None

        wb_span = self._trace_tree.Span(
            name=f"{event_type}",
            span_kind=span_kind,
            start_time_ms=start_time_ms,
            end_time_ms=end_time_ms,
        )

        inputs, outputs, wb_span = self._add_payload_to_span(wb_span, event_pair)
        wb_span.add_named_result(inputs=inputs, outputs=outputs)  # type: ignore

        return wb_span

    def_map_event_type_to_span_kind(
        self, event_type: CBEventType
    ) -> Union[None, "trace_tree.SpanKind"]:
"""Map a CBEventType to a wandb trace tree SpanKind."""
        if event_type == CBEventType.CHUNKING:
            span_kind = None
        elif event_type == CBEventType.NODE_PARSING:
            span_kind = None
        elif event_type == CBEventType.EMBEDDING:
            # TODO: add span kind for EMBEDDING when it's available
            span_kind = None
        elif event_type == CBEventType.LLM:
            span_kind = self._trace_tree.SpanKind.LLM
        elif event_type == CBEventType.QUERY:
            span_kind = self._trace_tree.SpanKind.AGENT
        elif event_type == CBEventType.AGENT_STEP:
            span_kind = self._trace_tree.SpanKind.AGENT
        elif event_type == CBEventType.RETRIEVE:
            span_kind = self._trace_tree.SpanKind.TOOL
        elif event_type == CBEventType.SYNTHESIZE:
            span_kind = self._trace_tree.SpanKind.CHAIN
        elif event_type == CBEventType.TREE:
            span_kind = self._trace_tree.SpanKind.CHAIN
        elif event_type == CBEventType.SUB_QUESTION:
            span_kind = self._trace_tree.SpanKind.CHAIN
        elif event_type == CBEventType.RERANKING:
            span_kind = self._trace_tree.SpanKind.CHAIN
        elif event_type == CBEventType.FUNCTION_CALL:
            span_kind = self._trace_tree.SpanKind.TOOL
        else:
            span_kind = None

        return span_kind

    def_add_payload_to_span(
        self, span: "trace_tree.Span", event_pair: List[CBEvent]
    ) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], "trace_tree.Span"]:
"""Add the event's payload to the span."""
        assert len(event_pair) == 2
        event_type = event_pair[0].event_type
        inputs = None
        outputs = None

        if event_type == CBEventType.NODE_PARSING:
            # TODO: disabled full detailed inputs/outputs due to UI lag
            inputs, outputs = self._handle_node_parsing_payload(event_pair)
        elif event_type == CBEventType.LLM:
            inputs, outputs, span = self._handle_llm_payload(event_pair, span)
        elif event_type == CBEventType.QUERY:
            inputs, outputs = self._handle_query_payload(event_pair)
        elif event_type == CBEventType.EMBEDDING:
            inputs, outputs = self._handle_embedding_payload(event_pair)

        return inputs, outputs, span

    def_handle_node_parsing_payload(
        self, event_pair: List[CBEvent]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
"""Handle the payload of a NODE_PARSING event."""
        inputs = event_pair[0].payload
        outputs = event_pair[-1].payload

        if inputs and EventPayload.DOCUMENTS in inputs:
            documents = inputs.pop(EventPayload.DOCUMENTS)
            inputs["num_documents"] = len(documents)

        if outputs and EventPayload.NODES in outputs:
            nodes = outputs.pop(EventPayload.NODES)
            outputs["num_nodes"] = len(nodes)

        return inputs or {}, outputs or {}

    def_handle_llm_payload(
        self, event_pair: List[CBEvent], span: "trace_tree.Span"
    ) -> Tuple[Dict[str, Any], Dict[str, Any], "trace_tree.Span"]:
"""Handle the payload of a LLM event."""
        inputs = event_pair[0].payload
        outputs = event_pair[-1].payload

        assert isinstance(inputs, dict) and isinstance(outputs, dict)

        # Get `original_template` from Prompt
        if EventPayload.PROMPT in inputs:
            inputs[EventPayload.PROMPT] = inputs[EventPayload.PROMPT]

        # Format messages
        if EventPayload.MESSAGES in inputs:
            inputs[EventPayload.MESSAGES] = "\n".join(
                [str(x) for x in inputs[EventPayload.MESSAGES]]
            )

        token_counts = get_llm_token_counts(self._token_counter, outputs)
        metadata = {
            "formatted_prompt_tokens_count": token_counts.prompt_token_count,
            "prediction_tokens_count": token_counts.completion_token_count,
            "total_tokens_used": token_counts.total_token_count,
        }
        span.attributes = metadata

        # Make `response` part of `outputs`
        outputs = {EventPayload.RESPONSE: str(outputs[EventPayload.RESPONSE])}

        return inputs, outputs, span

    def_handle_query_payload(
        self, event_pair: List[CBEvent]
    ) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:
"""Handle the payload of a QUERY event."""
        inputs = event_pair[0].payload
        outputs = event_pair[-1].payload

        if outputs:
            response_obj = outputs[EventPayload.RESPONSE]
            response = str(outputs[EventPayload.RESPONSE])

            if type(response).__name__ == "Response":
                response = response_obj.response
            elif type(response).__name__ == "StreamingResponse":
                response = response_obj.get_response().response
        else:
            response = " "

        outputs = {"response": response}

        return inputs, outputs

    def_handle_embedding_payload(
        self,
        event_pair: List[CBEvent],
    ) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:
        event_pair[0].payload
        outputs = event_pair[-1].payload

        chunks = []
        if outputs:
            chunks = outputs.get(EventPayload.CHUNKS, [])

        return {}, {"num_chunks": len(chunks)}

    def_get_time_in_ms(self, event_pair: List[CBEvent]) -> Tuple[int, int]:
"""Get the start and end time of an event pair in milliseconds."""
        start_time = datetime.strptime(event_pair[0].time, TIMESTAMP_FORMAT)
        end_time = datetime.strptime(event_pair[1].time, TIMESTAMP_FORMAT)

        start_time_in_ms = int(
            (start_time - datetime(1970, 1, 1)).total_seconds() * 1000
        )
        end_time_in_ms = int((end_time - datetime(1970, 1, 1)).total_seconds() * 1000)

        return start_time_in_ms, end_time_in_ms

    def_ensure_run(self, should_print_url: bool = False) -> None:
"""
        Ensures an active W&B run exists.

        If not, will start a new run with the provided run_args.
        """
        if self._wandb.run is None:  # type: ignore[attr-defined]
            # Make a shallow copy of the run args, so we don't modify the original
            run_args = self._run_args or {}  # type: ignore
            run_args: dict = {**run_args}  # type: ignore

            # Prefer to run in silent mode since W&B has a lot of output
            # which can be undesirable when dealing with text-based models.
            if "settings" not in run_args:  # type: ignore
                run_args["settings"] = {"silent": True}  # type: ignore

            # Start the run and add the stream table
            self._wandb.init(**run_args)  # type: ignore[attr-defined]
            self._wandb.run._label(repo="llama_index")  # type: ignore

            if should_print_url:
                self._print_wandb_init_message(
                    self._wandb.run.settings.run_url  # type: ignore
                )

    def_print_wandb_init_message(self, run_url: str) -> None:
"""Print a message to the terminal when W&B is initialized."""
        self._wandb.termlog(  # type: ignore[attr-defined]
            f"Streaming LlamaIndex events to W&B at {run_url}\n"
            "`WandbCallbackHandler` is currently in beta.\n"
            "Please report any issues to https://github.com/wandb/wandb/issues "
            "with the tag `llamaindex`."
        )

    def_print_upload_index_fail_message(self, e: Exception) -> None:
"""Print a message to the terminal when uploading the index fails."""
        self._wandb.termlog(  # type: ignore[attr-defined]
            f"Failed to upload index to W&B with the following error: {e}\n"
        )

    deffinish(self) -> None:
"""Finish the callback handler."""
        self._wandb.finish()  # type: ignore[attr-defined]

```
 |  
| --- | --- |  
###  on_event_start [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/wandb/#llama_index.callbacks.wandb.WandbCallbackHandler.on_event_start "Permanent link")

```
on_event_start(
    event_type: ,
    payload: Optional[[, ]] = None,
    event_id:  = "",
    parent_id:  = "",
    **kwargs: 
) -> 

```

Store event start data by event type.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `event_type`  |   |  event type to store.  |  _required_  |  
|  `payload`  |  `Optional[Dict[str, Any]]`  |  payload to store.  |  `None`  |  
|  `event_id`  |  event id to store.  |  
|  `parent_id`  |  parent event id.  |  
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-wandb/llama_index/callbacks/wandb/base.py`  
| 
```
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
```
 | 
```
defon_event_start(
    self,
    event_type: CBEventType,
    payload: Optional[Dict[str, Any]] = None,
    event_id: str = "",
    parent_id: str = "",
    **kwargs: Any,
) -> str:
"""
    Store event start data by event type.

    Args:
        event_type (CBEventType): event type to store.
        payload (Optional[Dict[str, Any]]): payload to store.
        event_id (str): event id to store.
        parent_id (str): parent event id.

    """
    event = CBEvent(event_type, payload=payload, id_=event_id)
    self._event_pairs_by_id[event.id_].append(event)
    return event.id_

```
 |  
| --- | --- |  
###  on_event_end [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/wandb/#llama_index.callbacks.wandb.WandbCallbackHandler.on_event_end "Permanent link")

```
on_event_end(
    event_type: ,
    payload: Optional[[, ]] = None,
    event_id:  = "",
    **kwargs: 
) -> None

```

Store event end data by event type.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `event_type`  |   |  event type to store.  |  _required_  |  
|  `payload`  |  `Optional[Dict[str, Any]]`  |  payload to store.  |  `None`  |  
|  `event_id`  |  event id to store.  |  
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-wandb/llama_index/callbacks/wandb/base.py`  
| 
```
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
"""
    Store event end data by event type.

    Args:
        event_type (CBEventType): event type to store.
        payload (Optional[Dict[str, Any]]): payload to store.
        event_id (str): event id to store.

    """
    event = CBEvent(event_type, payload=payload, id_=event_id)
    self._event_pairs_by_id[event.id_].append(event)
    self._trace_map = defaultdict(list)

```
 |  
| --- | --- |  
###  start_trace [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/wandb/#llama_index.callbacks.wandb.WandbCallbackHandler.start_trace "Permanent link")

```
start_trace(trace_id: Optional[] = None) -> None

```

Launch a trace.
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-wandb/llama_index/callbacks/wandb/base.py`  
| 
```
220
221
222
223
224
```
 | 
```
defstart_trace(self, trace_id: Optional[str] = None) -> None:
"""Launch a trace."""
    self._trace_map = defaultdict(list)
    self._cur_trace_id = trace_id
    self._start_time = datetime.now()

```
 |  
| --- | --- |  
###  log_trace_tree [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/wandb/#llama_index.callbacks.wandb.WandbCallbackHandler.log_trace_tree "Permanent link")

```
log_trace_tree() -> None

```

Log the trace tree to wandb.
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-wandb/llama_index/callbacks/wandb/base.py`  
| 
```
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
```
 | 
```
deflog_trace_tree(self) -> None:
"""Log the trace tree to wandb."""
    try:
        child_nodes = self._trace_map["root"]
        root_span = self._convert_event_pair_to_wb_span(
            self._event_pairs_by_id[child_nodes[0]],
            trace_id=self._cur_trace_id if len(child_nodes)  1 else None,
        )

        if len(child_nodes) == 1:
            child_nodes = self._trace_map[child_nodes[0]]
            root_span = self._build_trace_tree(child_nodes, root_span)
        else:
            root_span = self._build_trace_tree(child_nodes, root_span)
        if root_span:
            root_trace = self._trace_tree.WBTraceTree(root_span)
            if self._wandb.run:  # type: ignore[attr-defined]
                self._wandb.run.log({"trace": root_trace})  # type: ignore[attr-defined]
            self._wandb.termlog("Logged trace tree to W&B.")  # type: ignore[attr-defined]
    except Exception as e:
        print(f"Failed to log trace tree to W&B: {e}")

```
 |  
| --- | --- |  
###  persist_index [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/wandb/#llama_index.callbacks.wandb.WandbCallbackHandler.persist_index "Permanent link")

```
persist_index(
    index: IndexType,
    index_name: ,
    persist_dir: Union[, None] = None,
) -> None

```

Upload an index to wandb as an artifact. You can learn more about W&B artifacts here: https://docs.wandb.ai/guides/artifacts.
For the `ComposableGraph` index, the root id is stored as artifact metadata.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index`  |  `IndexType`  |  index to upload.  |  _required_  |  
|  `index_name`  |  name of the index. This will be used as the artifact name.  |  _required_  |  
|  `persist_dir`  |  `Union[str, None]`  |  directory to persist the index. If None, a temporary directory will be created and used.  |  `None`  |  
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-wandb/llama_index/callbacks/wandb/base.py`  
| 
```
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
```
 | 
```
defpersist_index(
    self, index: "IndexType", index_name: str, persist_dir: Union[str, None] = None
) -> None:
"""
    Upload an index to wandb as an artifact. You can learn more about W&B
    artifacts here: https://docs.wandb.ai/guides/artifacts.

    For the `ComposableGraph` index, the root id is stored as artifact metadata.

    Args:
        index (IndexType): index to upload.
        index_name (str): name of the index. This will be used as the artifact name.
        persist_dir (Union[str, None]): directory to persist the index. If None, a
            temporary directory will be created and used.

    """
    _default_persist_dir = False
    if persist_dir is None:
        persist_dir = f"{self._wandb.run.dir}/storage"  # type: ignore
        _default_persist_dir = True
    if not os.path.exists(persist_dir):
        os.makedirs(persist_dir)

    if isinstance(index, self._IndexType):
        try:
            index.storage_context.persist(persist_dir)  # type: ignore

            metadata = None
            # For the `ComposableGraph` index, store the root id as metadata
            if isinstance(index, self._IndexType[0]):
                root_id = index.root_id
                metadata = {"root_id": root_id}

            self._upload_index_as_wb_artifact(persist_dir, index_name, metadata)
        except Exception as e:
            # Silently ignore errors to not break user code
            self._print_upload_index_fail_message(e)

    # clear the default storage dir
    if _default_persist_dir:
        shutil.rmtree(persist_dir, ignore_errors=True)

```
 |  
| --- | --- |  
###  load_storage_context [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/wandb/#llama_index.callbacks.wandb.WandbCallbackHandler.load_storage_context "Permanent link")

```
load_storage_context(
    artifact_url: ,
    index_download_dir: Union[, None] = None,
) -> 

```

Download an index from wandb and return a storage context.
Use this storage context to load the index into memory using `load_index_from_storage`, `load_indices_from_storage` or `load_graph_from_storage` functions.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `artifact_url`  |  url of the artifact to download. The artifact url will be of the form: `entity/project/index_name:version` and can be found in the W&B UI.  |  _required_  |  
|  `index_download_dir`  |  `Union[str, None]`  |  directory to download the index to.  |  `None`  |  
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-wandb/llama_index/callbacks/wandb/base.py`  
| 
```
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
```
 | 
```
defload_storage_context(
    self, artifact_url: str, index_download_dir: Union[str, None] = None
) -> "StorageContext":
"""
    Download an index from wandb and return a storage context.

    Use this storage context to load the index into memory using
    `load_index_from_storage`, `load_indices_from_storage` or
    `load_graph_from_storage` functions.

    Args:
        artifact_url (str): url of the artifact to download. The artifact url will
            be of the form: `entity/project/index_name:version` and can be found in
            the W&B UI.
        index_download_dir (Union[str, None]): directory to download the index to.

    """
    fromllama_index.core.storage.storage_contextimport StorageContext

    artifact = self._wandb.use_artifact(artifact_url, type="storage_context")  # type: ignore[attr-defined]
    artifact_dir = artifact.download(root=index_download_dir)

    return StorageContext.from_defaults(persist_dir=artifact_dir)

```
 |  
| --- | --- |  
###  finish [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/wandb/#llama_index.callbacks.wandb.WandbCallbackHandler.finish "Permanent link")

```
finish() -> None

```

Finish the callback handler.
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-wandb/llama_index/callbacks/wandb/base.py`  
| 
```
577
578
579
```
 | 
```
deffinish(self) -> None:
"""Finish the callback handler."""
    self._wandb.finish()  # type: ignore[attr-defined]

```
 |  
| --- | --- |  
options: members: - WandbCallbackHandler
