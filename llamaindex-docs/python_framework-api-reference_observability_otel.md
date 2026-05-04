# Otel
##  LlamaIndexOpenTelemetry [#](https://developers.llamaindex.ai/python/framework-api-reference/observability/otel/#llama_index.observability.otel.LlamaIndexOpenTelemetry "Permanent link")
Bases: `BaseModel`
LlamaIndexOpenTelemetry is a configuration and integration class for OpenTelemetry tracing within LlamaIndex. This class manages the setup and registration of OpenTelemetry span and event handlers, configures the tracer provider, and exports trace data using the specified span exporter and processor. It supports both simple and batch span processors, and allows customization of the service name or resource, as well as the dispatcher name.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `span_exporter`  |  `Optional[SpanExporter]`  |  The OpenTelemetry span exporter. Defaults to ConsoleSpanExporter.  |  
| `span_processor`  |  `Literal['simple', 'batch']`  |  The span processor type, either 'simple' or 'batch'. Defaults to 'batch'.  |  
| `service_name_or_resource`  |  `Union[str, Resource]`  |  The service name or OpenTelemetry Resource. Defaults to a Resource with service name 'llamaindex.opentelemetry'.  |  
Source code in `llama-index-integrations/observability/llama-index-observability-otel/llama_index/observability/otel/base.py`  
| 
```
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
```
 | 
```
classLlamaIndexOpenTelemetry(BaseModel):
"""
    LlamaIndexOpenTelemetry is a configuration and integration class for OpenTelemetry tracing within LlamaIndex.
    This class manages the setup and registration of OpenTelemetry span and event handlers, configures the tracer provider,
    and exports trace data using the specified span exporter and processor. It supports both simple and batch span processors,
    and allows customization of the service name or resource, as well as the dispatcher name.

    Attributes:
        span_exporter (Optional[SpanExporter]): The OpenTelemetry span exporter. Defaults to ConsoleSpanExporter.
        span_processor (Literal["simple", "batch"]): The span processor type, either 'simple' or 'batch'. Defaults to 'batch'.
        service_name_or_resource (Union[str, Resource]): The service name or OpenTelemetry Resource. Defaults to a Resource with service name 'llamaindex.opentelemetry'.

    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    span_exporter: Optional[SpanExporter] = Field(
        default=ConsoleSpanExporter(),
        description="OpenTelemetry span exporter. Supports all SpanExporter-compatible interfaces, defaults to ConsoleSpanExporter.",
    )
    span_processor: Literal["simple", "batch"] = Field(
        default="batch",
        description="OpenTelemetry span processor. Can be either 'batch' (-> BatchSpanProcessor), 'simple' (-> SimpleSpanProcessor). Defaults to 'batch'",
    )
    extra_span_processors: List[SpanProcessor] = Field(
        default_factory=list,
        description="List of OpenTelemetry Span Processors to add to the tracer provider.",
    )
    tracer_provider: Optional[TracerProvider] = Field(
        default=None,
        description="Tracer Provider to inherint from the existing observability context. Defaults to None.",
    )
    service_name_or_resource: Union[str, Resource] = Field(
        default=Resource(attributes={SERVICE_NAME: "llamaindex.opentelemetry"}),
        description="Service name or resource for OpenTelemetry. Defaults to a Resource with 'llamaindex.opentelemetry' as service name.",
    )
    debug: bool = Field(
        default=False,
        description="Debug the start and end of span and the recording of events",
    )
    _tracer: Optional[trace.Tracer] = PrivateAttr(default=None)
    _tracer_provider_instance: Optional[TracerProvider] = PrivateAttr(default=None)

    def_start_otel(
        self,
    ) -> None:
        if isinstance(self.service_name_or_resource, str):
            self.service_name_or_resource = Resource(
                attributes={SERVICE_NAME: self.service_name_or_resource}
            )
        if self.tracer_provider is None:
            tracer_provider = TracerProvider(resource=self.service_name_or_resource)
        else:
            tracer_provider = self.tracer_provider
        assert self.span_exporter is not None, (
            "span_exporter has to be non-null to be used within simple or batch span processors"
        )
        if self.span_processor == "simple":
            span_processor = SimpleSpanProcessor(self.span_exporter)
        else:
            span_processor = BatchSpanProcessor(self.span_exporter)
        for extra_span_processor in self.extra_span_processors:
            tracer_provider.add_span_processor(extra_span_processor)
        tracer_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(tracer_provider)
        self._tracer_provider_instance = tracer_provider
        self._tracer = trace.get_tracer("llamaindex.opentelemetry.tracer")

    defstart_registering(
        self,
    ) -> None:
"""Starts LlamaIndex instrumentation."""
        self._start_otel()
        dispatcher = instrument.get_dispatcher()
        assert self._tracer is not None, (
            "The tracer has to be non-null to start observabiliy"
        )
        span_handler = OTelCompatibleSpanHandler(
            tracer=self._tracer,
            debug=self.debug,
            tracer_provider=self._tracer_provider_instance,
        )
        dispatcher.add_span_handler(span_handler)
        dispatcher.add_event_handler(
            OTelCompatibleEventHandler(span_handler=span_handler, debug=self.debug)
        )

```
 |  
| --- | --- |  
###  start_registering [#](https://developers.llamaindex.ai/python/framework-api-reference/observability/otel/#llama_index.observability.otel.LlamaIndexOpenTelemetry.start_registering "Permanent link")

```
start_registering() -> None

```

Starts LlamaIndex instrumentation.
Source code in `llama-index-integrations/observability/llama-index-observability-otel/llama_index/observability/otel/base.py`  
| 
```
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
```
 | 
```
defstart_registering(
    self,
) -> None:
"""Starts LlamaIndex instrumentation."""
    self._start_otel()
    dispatcher = instrument.get_dispatcher()
    assert self._tracer is not None, (
        "The tracer has to be non-null to start observabiliy"
    )
    span_handler = OTelCompatibleSpanHandler(
        tracer=self._tracer,
        debug=self.debug,
        tracer_provider=self._tracer_provider_instance,
    )
    dispatcher.add_span_handler(span_handler)
    dispatcher.add_event_handler(
        OTelCompatibleEventHandler(span_handler=span_handler, debug=self.debug)
    )

```
 |  
| --- | --- |  
options: members: - LlamaIndexOpenTelemetry
