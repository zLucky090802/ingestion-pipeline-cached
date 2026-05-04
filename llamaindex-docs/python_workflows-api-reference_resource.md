# Resource
Declare a resource to inject into step functions.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `factory`  |  `Callable[..., T] | None`  |  Function returning the resource instance. May be async.  |  _required_  |  
|  `cache`  |  `bool`  |  If True, reuse the produced resource across steps. Defaults to True.  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `_Resource`  |  _Resource[T]: A resource descriptor to be used in `typing.Annotated`.  |  
Examples:

```
fromtypingimport Annotated
fromworkflows.resourceimport Resource

defget_memory(**kwargs) -> Memory:
    return Memory.from_defaults("user123", token_limit=60000)

classMyWorkflow(Workflow):
    @step
    async deffirst(
        self,
        ev: StartEvent,
        memory: Annotated[Memory, Resource(get_memory)],
    ) -> StopEvent:
        await memory.aput(...)
        return StopEvent(result="ok")

```

Source code in `workflows/resource.py`  
| 
```
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
```
 | 
```
defResource(
    factory: Callable[..., T],
    cache: bool = True,
) -> _Resource:
"""Declare a resource to inject into step functions.

    Args:
        factory (Callable[..., T] | None): Function returning the resource instance. May be async.
        cache (bool): If True, reuse the produced resource across steps. Defaults to True.

    Returns:
        _Resource[T]: A resource descriptor to be used in `typing.Annotated`.

    Examples:
        ```python
        from typing import Annotated
        from workflows.resource import Resource

        def get_memory(**kwargs) -> Memory:
            return Memory.from_defaults("user123", token_limit=60000)

        class MyWorkflow(Workflow):
            @step
            async def first(
                self,
                ev: StartEvent,
                memory: Annotated[Memory, Resource(get_memory)],
            ) -> StopEvent:
                await memory.aput(...)
                return StopEvent(result="ok")
        ```
    """
    return _Resource(factory, cache)

```
 |  
| --- | --- |  
Create a config-backed resource that loads a Pydantic model from a JSON file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `config_file`  |  JSON file where the configuration is stored.  |  _required_  |  
|  `path_selector`  |  `str | None`  |  Path selector to retrieve a specific value from the JSON map.  |  `None`  |  
|  `label`  |  `str | None`  |  Human-friendly short name for display in visualizations.  |  `None`  |  
|  `description`  |  `str | None`  |  Longer description explaining the purpose and contents of this config.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `_ResourceConfig`  |  `_ResourceConfig`  |  A configured resource representation.  |  
Example

```
fromtypingimport Annotated
frompydanticimport BaseModel
fromworkflowsimport Workflow, step
fromworkflows.eventsimport StartEvent, StopEvent
fromworkflows.resourceimport ResourceConfig


classClassifierConfig(BaseModel):
    categories: list[str]
    threshold: float


classMyWorkflow(Workflow):
    @step
    async defclassify(
        self,
        ev: StartEvent,
        config: Annotated[
            ClassifierConfig,
            ResourceConfig(
                config_file="classifier.json",
                label="Classifier",
                description="Classification categories and threshold",
            ),
        ],
    ) -> StopEvent:
        return StopEvent(result=config.categories)

```

Source code in `workflows/resource.py`  
| 
```
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
```
 | 
```
defResourceConfig(
    config_file: str,
    path_selector: str | None = None,
    label: str | None = None,
    description: str | None = None,
) -> _ResourceConfig:
"""
    Create a config-backed resource that loads a Pydantic model from a JSON file.

    Args:
        config_file: JSON file where the configuration is stored.
        path_selector: Path selector to retrieve a specific value from the JSON map.
        label: Human-friendly short name for display in visualizations.
        description: Longer description explaining the purpose and contents of this config.

    Returns:
        _ResourceConfig: A configured resource representation.

    Example:
        ```python
        from typing import Annotated
        from pydantic import BaseModel
        from workflows import Workflow, step
        from workflows.events import StartEvent, StopEvent
        from workflows.resource import ResourceConfig


        class ClassifierConfig(BaseModel):
            categories: list[str]
            threshold: float


        class MyWorkflow(Workflow):
            @step
            async def classify(
                self,
                ev: StartEvent,
                config: Annotated[
                    ClassifierConfig,
                    ResourceConfig(
                        config_file="classifier.json",
                        label="Classifier",
                        description="Classification categories and threshold",


            ) -> StopEvent:
                return StopEvent(result=config.categories)
        ```
    """
    return _ResourceConfig(
        config_file=config_file,
        path_selector=path_selector,
        label=label,
        description=description,
    )

```
 |  
| --- | --- |
