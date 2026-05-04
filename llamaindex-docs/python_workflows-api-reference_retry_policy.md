# Retry Policy[#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#retry-policy "Permanent link")
The retry API is built from three families of callables modeled after [tenacity](https://tenacity.readthedocs.io/en/latest/):
  * decide whether an exception should be retried.
  * decide how long to sleep before the next attempt.
  * decide when retries should stop.


You can compose them into a policy with `retry_policy(retry=..., wait=..., stop=...)`. Retry conditions support `|` and , wait strategies support `+`, and stop conditions support `|` and .
## Quick Example[#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#quick-example "Permanent link")

```
fromworkflows.retry_policyimport (
    retry_policy,
    retry_if_exception_message,
    retry_if_exception_type,
    stop_after_attempt,
    stop_before_delay,
    wait_fixed,
    wait_random,
)

policy = retry_policy(
    retry=retry_if_exception_type((TimeoutError, ConnectionError))
    | retry_if_exception_message(match="rate limit|temporarily unavailable"),
    wait=wait_fixed(1) + wait_random(0, 1),
    stop=stop_after_attempt(5) | stop_before_delay(30),
)

```

## Policy Constructor[#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#policy-constructor "Permanent link")
##  RetryPolicy [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.RetryPolicy "Permanent link")
Bases: `Protocol`
Structural interface for step retry policies.
Any object with a compatible `next` method satisfies this protocol, including policies built with `retry_policy()`, `ConstantDelayRetryPolicy`, `ExponentialBackoffRetryPolicy`, and user-defined policies.
Most users do not implement this protocol directly. Instead, construct a policy with `retry_policy(retry=..., wait=..., stop=...)` and combine retry conditions, wait strategies, and stop conditions with the operators supported by this module.
Examples:

```
fromworkflows.retry_policyimport (
    retry_policy,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

policy = retry_policy(
    retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    wait=wait_exponential(multiplier=1, exp_base=2, max=30),
    stop=stop_after_attempt(5),
)

```

See Also Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
@runtime_checkable
classRetryPolicy(Protocol):
"""
    Structural interface for step retry policies.

    Any object with a compatible ``next`` method satisfies this protocol,
    including policies built with `retry_policy()`, `ConstantDelayRetryPolicy`,
    `ExponentialBackoffRetryPolicy`, and user-defined policies.

    Most users do not implement this protocol directly. Instead, construct a
    policy with ``retry_policy(retry=..., wait=..., stop=...)`` and combine
    retry conditions, wait strategies, and stop conditions with the operators
    supported by this module.

    Examples:
        ```python
        from workflows.retry_policy import (
            retry_policy,
            retry_if_exception_type,
            stop_after_attempt,
            wait_exponential,


        policy = retry_policy(
            retry=retry_if_exception_type((TimeoutError, ConnectionError)),
            wait=wait_exponential(multiplier=1, exp_base=2, max=30),
            stop=stop_after_attempt(5),

        ```

    See Also:
        - [step][workflows.decorators.step]
    """

    defnext(
        self,
        elapsed_time: float,
        attempts: int,
        error: Exception,
        *,
        seed: int | None = None,
    ) -> float | None:
"""
        Decide if another retry should occur and the delay before it.

        Args:
            elapsed_time: Seconds since the first failure.
            attempts: Number of attempts made so far.
            error: The last exception encountered.
            seed: Optional RNG seed for deterministic jitter (DBOS replay).

        Returns:
            Seconds to wait before retrying, or ``None`` to stop.
        """

```
 |  
| --- | --- |  
###  next [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.RetryPolicy.next "Permanent link")

```
next(elapsed_time: float, attempts: , error: Exception, *, seed:  | None = None) -> float | None

```

Decide if another retry should occur and the delay before it.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `elapsed_time`  |  `float`  |  Seconds since the first failure.  |  _required_  |  
|  `attempts`  |  Number of attempts made so far.  |  _required_  |  
|  `error`  |  `Exception`  |  The last exception encountered.  |  _required_  |  
|  `seed`  |  `int | None`  |  Optional RNG seed for deterministic jitter (DBOS replay).  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `float | None`  |  Seconds to wait before retrying, or `None` to stop.  |  
Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
defnext(
    self,
    elapsed_time: float,
    attempts: int,
    error: Exception,
    *,
    seed: int | None = None,
) -> float | None:
"""
    Decide if another retry should occur and the delay before it.

    Args:
        elapsed_time: Seconds since the first failure.
        attempts: Number of attempts made so far.
        error: The last exception encountered.
        seed: Optional RNG seed for deterministic jitter (DBOS replay).

    Returns:
        Seconds to wait before retrying, or ``None`` to stop.
    """

```
 |  
| --- | --- |  
##  retry_policy [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.retry_policy "Permanent link")

```
retry_policy(retry: RetryCondition | None = None, wait: WaitStrategy = (5), stop: StopCondition = (3)) -> 

```

Construct a composable retry policy from retry, wait, and stop components.
This is the primary way to create retry policies. Combine retry conditions, wait strategies, and stop conditions using operators (`|`, , `+`) or the named combinators.
Examples:

```
fromworkflows.retry_policyimport (
    retry_policy,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

policy = retry_policy(
    retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    wait=wait_exponential(multiplier=1, exp_base=2, max=30),
    stop=stop_after_attempt(5),
)

```

With no arguments, `retry_policy()` retries all exceptions up to 3 attempts with a 5-second fixed delay between each.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `retry`  |  `RetryCondition | None`  |  Predicate that decides whether an exception is retryable. When `None`, all exceptions are retried.  |  `None`  |  
|  `wait`  |  `WaitStrategy`  |  Strategy that computes the delay before the next attempt. Defaults to `wait_fixed(5)` (5 seconds).  |   |  
|  `stop`  |  `StopCondition`  |  Predicate that decides when to give up. Defaults to `stop_after_attempt(3)`.  |   |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  A `RetryPolicy` implementation.  |  
Source code in `workflows/retry_policy.py`  
| 
```
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
```
 | 
```
defretry_policy(
    retry: RetryCondition | None = None,
    wait: WaitStrategy = wait_fixed(5),
    stop: StopCondition = stop_after_attempt(3),
) -> RetryPolicy:
"""
    Construct a composable retry policy from retry, wait, and stop components.

    This is the primary way to create retry policies. Combine retry conditions,
    wait strategies, and stop conditions using operators (``|``, ``&``, ``+``)
    or the named combinators.

    Examples:
        ```python
        from workflows.retry_policy import (
            retry_policy,
            retry_if_exception_type,
            stop_after_attempt,
            wait_exponential,


        policy = retry_policy(
            retry=retry_if_exception_type((TimeoutError, ConnectionError)),
            wait=wait_exponential(multiplier=1, exp_base=2, max=30),
            stop=stop_after_attempt(5),

        ```

    With no arguments, ``retry_policy()`` retries all exceptions up to 3
    attempts with a 5-second fixed delay between each.

    Args:
        retry: Predicate that decides whether an exception is retryable.
            When ``None``, all exceptions are retried.
        wait: Strategy that computes the delay before the next attempt.
            Defaults to ``wait_fixed(5)`` (5 seconds).
        stop: Predicate that decides when to give up.
            Defaults to ``stop_after_attempt(3)``.

    Returns:
        A `RetryPolicy` implementation.
    """
    return _ComposableRetryPolicy(retry=retry, wait=wait, stop=stop)

```
 |  
| --- | --- |  
## Retry Conditions[#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#retry-conditions "Permanent link")
Modeled after [tenacity retry functions](https://tenacity.readthedocs.io/en/latest/api.html#retry-functions).
##  retry_if_exception [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.retry_if_exception "Permanent link")
Bases: `_RetryConditionBase`
Retry when the raised exception satisfies a custom predicate.
Use this when your retry decision depends on exception details that are not covered by the built-in helpers.
Examples:

```
retry_if_exception(lambda error: "rate limit" in str(error).lower())

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classretry_if_exception(_RetryConditionBase):
"""
    Retry when the raised exception satisfies a custom predicate.

    Use this when your retry decision depends on exception details that are not
    covered by the built-in helpers.

    Examples:
        ```python
        retry_if_exception(lambda error: "rate limit" in str(error).lower())
        ```
    """

    def__init__(self, predicate: Callable[[BaseException], bool]) -> None:
        self.predicate = predicate

    def__call__(self, error: BaseException) -> bool:
        return self.predicate(error)

```
 |  
| --- | --- |  
##  retry_if_exception_type [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.retry_if_exception_type "Permanent link")
Bases: 
Retry only when the exception is an instance of one of the given types.
This is the most common retry predicate for transient network and provider failures.
Examples:

```
retry_if_exception_type((TimeoutError, ConnectionError))

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classretry_if_exception_type(retry_if_exception):
"""
    Retry only when the exception is an instance of one of the given types.

    This is the most common retry predicate for transient network and provider
    failures.

    Examples:
        ```python
        retry_if_exception_type((TimeoutError, ConnectionError))
        ```
    """

    def__init__(
        self,
        exception_types: type[BaseException]
        | tuple[type[BaseException], ...] = Exception,
    ) -> None:
        self.exception_types = exception_types
        super().__init__(lambda error: isinstance(error, exception_types))

```
 |  
| --- | --- |  
##  retry_if_not_exception_type [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.retry_if_not_exception_type "Permanent link")
Bases: 
Retry unless the exception is an instance of one of the given types.
This is useful when most failures are retryable except for a small set of known permanent errors.
Examples:

```
retry_if_not_exception_type((ValueError, PermissionError))

```

Source code in `workflows/retry_policy.py`  
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
```
 | 
```
classretry_if_not_exception_type(retry_if_exception):
"""
    Retry unless the exception is an instance of one of the given types.

    This is useful when most failures are retryable except for a small set of
    known permanent errors.

    Examples:
        ```python
        retry_if_not_exception_type((ValueError, PermissionError))
        ```
    """

    def__init__(
        self,
        exception_types: type[BaseException]
        | tuple[type[BaseException], ...] = Exception,
    ) -> None:
        self.exception_types = exception_types
        super().__init__(lambda error: not isinstance(error, exception_types))

```
 |  
| --- | --- |  
##  retry_unless_exception_type [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.retry_unless_exception_type "Permanent link")
Bases: 
Retry unless the exception is an instance of one of the given types.
Tenacity-style alias for `retry_if_not_exception_type`.
Examples:

```
retry_unless_exception_type(AuthenticationError)

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classretry_unless_exception_type(retry_if_not_exception_type):
"""
    Retry unless the exception is an instance of one of the given types.

    Tenacity-style alias for `retry_if_not_exception_type`.

    Examples:
        ```python
        retry_unless_exception_type(AuthenticationError)
        ```
    """

    pass

```
 |  
| --- | --- |  
##  retry_if_exception_message [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.retry_if_exception_message "Permanent link")
Bases: `_RetryConditionBase`
Retry when the exception message matches an exact string or regex pattern.
Pass either `message` for an exact string match or `match` for a regular expression. Passing both is an error.
Examples:

```
retry_if_exception_message(message="please retry")
retry_if_exception_message(match=r"HTTP 5\d\d")

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classretry_if_exception_message(_RetryConditionBase):
"""
    Retry when the exception message matches an exact string or regex pattern.

    Pass either ``message`` for an exact string match or ``match`` for a regular
    expression. Passing both is an error.

    Examples:
        ```python
        retry_if_exception_message(message="please retry")
        retry_if_exception_message(match=r"HTTP 5\\d\\d")
        ```
    """

    def__init__(
        self,
        message: str | None = None,
        match: str | re.Pattern[str] | None = None,
    ) -> None:
        if message is None and match is None:
            raise TypeError(
                "retry_if_exception_message() missing 1 required argument "
                "'message' or 'match'"
            )
        if message is not None and match is not None:
            raise TypeError(
                "retry_if_exception_message() takes either 'message' or 'match', not both"
            )
        self.message = message
        self.match = match
        self._pattern = _compile_pattern(match)

    def__call__(self, error: BaseException) -> bool:
        error_message = str(error)
        if self.message is not None:
            return error_message == self.message
        return bool(self._pattern and self._pattern.search(error_message))

```
 |  
| --- | --- |  
##  retry_if_not_exception_message [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.retry_if_not_exception_message "Permanent link")
Bases: 
Retry when the exception message does not match the given string or regex.
This is useful when a provider uses specific messages to signal permanent failures that should stop retries.
Examples:

```
retry_if_not_exception_message(match="invalid_api_key|permission denied")

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classretry_if_not_exception_message(retry_if_exception_message):
"""
    Retry when the exception message does not match the given string or regex.

    This is useful when a provider uses specific messages to signal permanent
    failures that should stop retries.

    Examples:
        ```python
        retry_if_not_exception_message(match="invalid_api_key|permission denied")
        ```
    """

    def__call__(self, error: BaseException) -> bool:
        return not super().__call__(error)

```
 |  
| --- | --- |  
##  retry_if_exception_cause_type [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.retry_if_exception_cause_type "Permanent link")
Bases: `_RetryConditionBase`
Retry when any exception in the `__cause__` chain matches the given type.
Only explicit exception chaining (`raise X from Y`) is followed. Implicit chaining via `__context__` is **not** inspected, matching tenacity's behavior. If you need to match implicitly chained exceptions, use `retry_if_exception` with a custom predicate that walks `__context__`.
Examples:

```
retry_if_exception_cause_type(ConnectionError)

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classretry_if_exception_cause_type(_RetryConditionBase):
"""
    Retry when any exception in the ``__cause__`` chain matches the given type.

    Only explicit exception chaining (``raise X from Y``) is followed. Implicit
    chaining via ``__context__`` is **not** inspected, matching tenacity's
    behavior. If you need to match implicitly chained exceptions, use
    `retry_if_exception` with a custom predicate that walks ``__context__``.

    Examples:
        ```python
        retry_if_exception_cause_type(ConnectionError)
        ```
    """

    def__init__(
        self,
        exception_types: type[BaseException]
        | tuple[type[BaseException], ...] = Exception,
    ) -> None:
        self.exception_types = exception_types

    def__call__(self, error: BaseException) -> bool:
        current: BaseException | None = error
        while current is not None:
            cause = current.__cause__
            if isinstance(cause, self.exception_types):
                return True
            current = cause
        return False

```
 |  
| --- | --- |  
##  retry_any [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.retry_any "Permanent link")
Bases: `_RetryConditionBase`
Retry if any of the provided retry predicates match.
Equivalent to combining retry predicates with `|`.
Examples:

```
retry_any(
    retry_if_exception_type(ConnectionError),
    retry_if_exception_message(match="rate limit"),
)

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classretry_any(_RetryConditionBase):
"""
    Retry if any of the provided retry predicates match.

    Equivalent to combining retry predicates with ``|``.

    Examples:
        ```python
        retry_any(
            retry_if_exception_type(ConnectionError),
            retry_if_exception_message(match="rate limit"),

        ```
    """

    def__init__(self, *retries: RetryCondition) -> None:
        self.retries = retries

    def__call__(self, error: BaseException) -> bool:
        return any(retry(error) for retry in self.retries)

```
 |  
| --- | --- |  
##  retry_all [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.retry_all "Permanent link")
Bases: `_RetryConditionBase`
Retry if all of the provided retry predicates match.
Equivalent to combining retry predicates with .
Examples:

```
retry_all(
    retry_if_exception_type(RuntimeError),
    retry_if_exception_message(match="temporary"),
)

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classretry_all(_RetryConditionBase):
"""
    Retry if all of the provided retry predicates match.

    Equivalent to combining retry predicates with ``&``.

    Examples:
        ```python
        retry_all(
            retry_if_exception_type(RuntimeError),
            retry_if_exception_message(match="temporary"),

        ```
    """

    def__init__(self, *retries: RetryCondition) -> None:
        self.retries = retries

    def__call__(self, error: BaseException) -> bool:
        return all(retry(error) for retry in self.retries)

```
 |  
| --- | --- |  
##  retry_always [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.retry_always "Permanent link")
Bases: `_RetryConditionBase`
Retry condition that always retries.
This is mainly useful when you want to be explicit in a composed policy.
Examples:

```
retry_policy(retry=retry_always(), stop=stop_after_attempt(3))

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classretry_always(_RetryConditionBase):
"""
    Retry condition that always retries.

    This is mainly useful when you want to be explicit in a composed policy.

    Examples:
        ```python
        retry_policy(retry=retry_always(), stop=stop_after_attempt(3))
        ```
    """

    def__call__(self, error: BaseException) -> bool:
        return True

```
 |  
| --- | --- |  
##  retry_never [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.retry_never "Permanent link")
Bases: `_RetryConditionBase`
Retry condition that never retries.
This can be useful in tests or to disable one branch of a composed retry expression.
Examples:

```
retry_never() | retry_if_exception_type(ConnectionError)

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classretry_never(_RetryConditionBase):
"""
    Retry condition that never retries.

    This can be useful in tests or to disable one branch of a composed retry
    expression.

    Examples:
        ```python
        retry_never() | retry_if_exception_type(ConnectionError)
        ```
    """

    def__call__(self, error: BaseException) -> bool:
        return False

```
 |  
| --- | --- |  
## Wait Strategies[#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#wait-strategies "Permanent link")
Modeled after [tenacity wait functions](https://tenacity.readthedocs.io/en/latest/api.html#wait-functions).
##  wait_fixed [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.wait_fixed "Permanent link")
Bases: `_WaitStrategyBase`
Wait a fixed number of seconds between attempts.
Examples:

```
wait_fixed(5)

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classwait_fixed(_WaitStrategyBase):
"""
    Wait a fixed number of seconds between attempts.

    Examples:
        ```python
        wait_fixed(5)
        ```
    """

    def__init__(self, wait: time_unit_type) -> None:
        self.wait = _to_seconds(wait)

    def__call__(self, attempts: int, *, seed: int | None = None) -> float:
        return self.wait

```
 |  
| --- | --- |  
##  wait_none [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.wait_none "Permanent link")
Bases: 
Wait strategy that does not delay retries.
Examples:

```
wait_none()

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classwait_none(wait_fixed):
"""
    Wait strategy that does not delay retries.

    Examples:
        ```python
        wait_none()
        ```
    """

    def__init__(self) -> None:
        super().__init__(0)

```
 |  
| --- | --- |  
##  wait_exponential [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.wait_exponential "Permanent link")
Bases: `_WaitStrategyBase`
Wait with exponentially increasing delays, clamped between `min` and `max`.
The delay for attempt `n` is `multiplier * exp_base**n` before clamping.
Examples:

```
wait_exponential(multiplier=1, exp_base=2, max=60)

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classwait_exponential(_WaitStrategyBase):
"""
    Wait with exponentially increasing delays, clamped between ``min`` and ``max``.

    The delay for attempt ``n`` is ``multiplier * exp_base**n`` before clamping.

    Examples:
        ```python
        wait_exponential(multiplier=1, exp_base=2, max=60)
        ```
    """

    def__init__(
        self,
        multiplier: int | float = 1.0,
        exp_base: int | float = 2.0,
        max: time_unit_type = 60.0,
        min: time_unit_type = 0.0,
    ) -> None:
        self.multiplier = float(multiplier)
        self.exp_base = float(exp_base)
        self.max = _to_seconds(max)
        self.min = _to_seconds(min)

    def__call__(self, attempts: int, *, seed: int | None = None) -> float:
        return max(
            max(0.0, self.min),
            min(self.multiplier * self.exp_base**attempts, self.max),
        )

```
 |  
| --- | --- |  
##  wait_incrementing [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.wait_incrementing "Permanent link")
Bases: `_WaitStrategyBase`
Wait an incrementally larger amount after each attempt.
The delay starts at `start` and increases by `increment` on each retry, capped by `max` and never going below zero.
Examples:

```
wait_incrementing(start=1, increment=2, max=10)

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classwait_incrementing(_WaitStrategyBase):
"""
    Wait an incrementally larger amount after each attempt.

    The delay starts at ``start`` and increases by ``increment`` on each retry,
    capped by ``max`` and never going below zero.

    Examples:
        ```python
        wait_incrementing(start=1, increment=2, max=10)
        ```
    """

    def__init__(
        self,
        start: time_unit_type = 0.0,
        increment: time_unit_type = 100.0,
        max: time_unit_type = float("inf"),
    ) -> None:
        self.start = _to_seconds(start)
        self.increment = _to_seconds(increment)
        self.max = _to_seconds(max)

    def__call__(self, attempts: int, *, seed: int | None = None) -> float:
        result = self.start + (self.increment * attempts)
        return max(0.0, min(result, self.max))

```
 |  
| --- | --- |  
##  wait_random [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.wait_random "Permanent link")
Bases: `_WaitStrategyBase`
Wait a random duration uniformly sampled from `[min, max]`.
When the workflow runtime provides a `seed`, the sampled value is deterministic across replayed runs.
Examples:

```
wait_random(min=0.5, max=1.5)

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classwait_random(_WaitStrategyBase):
"""
    Wait a random duration uniformly sampled from ``[min, max]``.

    When the workflow runtime provides a ``seed``, the sampled value is
    deterministic across replayed runs.

    Examples:
        ```python
        wait_random(min=0.5, max=1.5)
        ```
    """

    def__init__(self, min: time_unit_type = 0.0, max: time_unit_type = 1.0) -> None:
        self.min = _to_seconds(min)
        self.max = _to_seconds(max)

    def__call__(self, attempts: int, *, seed: int | None = None) -> float:
        rng = random.Random(seed) if seed is not None else random
        return rng.uniform(self.min, self.max)

```
 |  
| --- | --- |  
##  wait_exponential_jitter [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.wait_exponential_jitter "Permanent link")
Bases: `_WaitStrategyBase`
Exponential backoff with additive random jitter.
The deterministic base delay grows exponentially and a random value in `[0, jitter]` is added on top.
Examples:

```
wait_exponential_jitter(initial=1, exp_base=2, max=60, jitter=1)

```

Source code in `workflows/retry_policy.py`  
| 
```
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
```
 | 
```
classwait_exponential_jitter(_WaitStrategyBase):
"""
    Exponential backoff with additive random jitter.

    The deterministic base delay grows exponentially and a random value in
    ``[0, jitter]`` is added on top.

    Examples:
        ```python
        wait_exponential_jitter(initial=1, exp_base=2, max=60, jitter=1)
        ```
    """

    def__init__(
        self,
        initial: float = 1.0,
        exp_base: float = 2.0,
        max: float = 60.0,
        jitter: float = 1.0,
    ) -> None:
        self.initial = initial
        self.exp_base = exp_base
        self.max = max
        self.jitter = jitter

    def__call__(self, attempts: int, *, seed: int | None = None) -> float:
        base = min(self.initial * self.exp_base**attempts, self.max)
        rng = random.Random(seed) if seed is not None else random
        return min(base + rng.uniform(0, self.jitter), self.max)

```
 |  
| --- | --- |  
##  wait_random_exponential [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.wait_random_exponential "Permanent link")
Bases: `_WaitStrategyBase`
Exponential backoff with full jitter.
A random delay is sampled between `min` and the exponential upper bound for the current attempt.
Examples:

```
wait_random_exponential(multiplier=1, exp_base=2, max=60)

```

Source code in `workflows/retry_policy.py`  
| 
```
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
classwait_random_exponential(_WaitStrategyBase):
"""
    Exponential backoff with full jitter.

    A random delay is sampled between ``min`` and the exponential upper bound
    for the current attempt.

    Examples:
        ```python
        wait_random_exponential(multiplier=1, exp_base=2, max=60)
        ```
    """

    def__init__(
        self,
        multiplier: int | float = 1.0,
        exp_base: int | float = 2.0,
        max: time_unit_type = 60.0,
        min: time_unit_type = 0.0,
    ) -> None:
        self.multiplier = float(multiplier)
        self.exp_base = float(exp_base)
        self.max = _to_seconds(max)
        self.min = _to_seconds(min)

    def__call__(self, attempts: int, *, seed: int | None = None) -> float:
        rng = random.Random(seed) if seed is not None else random
        upper = max(
            max(0.0, self.min),
            min(self.multiplier * self.exp_base**attempts, self.max),
        )
        return rng.uniform(self.min, upper)

```
 |  
| --- | --- |  
##  wait_chain [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.wait_chain "Permanent link")
Bases: `_WaitStrategyBase`
Use a different wait strategy for each attempt in order.
After the provided strategies are exhausted, the last strategy is reused for all subsequent attempts.
Examples:

```
wait_chain(wait_fixed(1), wait_fixed(2), wait_fixed(5))

```

Source code in `workflows/retry_policy.py`  
| 
```
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
```
 | 
```
classwait_chain(_WaitStrategyBase):
"""
    Use a different wait strategy for each attempt in order.

    After the provided strategies are exhausted, the last strategy is reused
    for all subsequent attempts.

    Examples:
        ```python
        wait_chain(wait_fixed(1), wait_fixed(2), wait_fixed(5))
        ```
    """

    def__init__(self, *strategies: WaitStrategy) -> None:
        if not strategies:
            raise ValueError("wait_chain requires at least one strategy")
        self.strategies = strategies

    def__call__(self, attempts: int, *, seed: int | None = None) -> float:
        idx = min(attempts, len(self.strategies) - 1)
        return self.strategies[idx](attempts, seed=seed)

```
 |  
| --- | --- |  
##  wait_combine [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.wait_combine "Permanent link")
Bases: `_WaitStrategyBase`
Combine multiple wait strategies by summing their delays.
Equivalent to combining waits with `+`.
Examples:

```
wait_combine(wait_fixed(1), wait_random(0, 1))

```

Source code in `workflows/retry_policy.py`  
| 
```
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
```
 | 
```
classwait_combine(_WaitStrategyBase):
"""
    Combine multiple wait strategies by summing their delays.

    Equivalent to combining waits with ``+``.

    Examples:
        ```python
        wait_combine(wait_fixed(1), wait_random(0, 1))
        ```
    """

    def__init__(self, *strategies: WaitStrategy) -> None:
        self.strategies = strategies

    def__call__(self, attempts: int, *, seed: int | None = None) -> float:
        return sum(strategy(attempts, seed=seed) for strategy in self.strategies)

```
 |  
| --- | --- |  
##  wait_full_jitter [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.wait_full_jitter "Permanent link")

```
wait_full_jitter(multiplier:  | float = 1.0, exp_base:  | float = 2.0, max: time_unit_type = 60.0, min: time_unit_type = 0.0) -> 

```

Alias for `wait_random_exponential`.
Examples:

```
wait_full_jitter(multiplier=1, exp_base=2, max=60)

```

Source code in `workflows/retry_policy.py`  
| 
```
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
```
 | 
```
defwait_full_jitter(
    multiplier: int | float = 1.0,
    exp_base: int | float = 2.0,
    max: time_unit_type = 60.0,
    min: time_unit_type = 0.0,
) -> wait_random_exponential:
"""
    Alias for `wait_random_exponential`.

    Examples:
        ```python
        wait_full_jitter(multiplier=1, exp_base=2, max=60)
        ```
    """

    return wait_random_exponential(
        multiplier=multiplier,
        exp_base=exp_base,
        max=max,
        min=min,
    )

```
 |  
| --- | --- |  
## Stop Conditions[#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#stop-conditions "Permanent link")
Modeled after [tenacity stop functions](https://tenacity.readthedocs.io/en/latest/api.html#stop-functions).
##  stop_after_attempt [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.stop_after_attempt "Permanent link")
Bases: `_StopConditionBase`
Stop after a fixed number of attempts.
Examples:

```
stop_after_attempt(5)

```

Source code in `workflows/retry_policy.py`  
| 
```
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
```
 | 
```
classstop_after_attempt(_StopConditionBase):
"""
    Stop after a fixed number of attempts.

    Examples:
        ```python
        stop_after_attempt(5)
        ```
    """

    def__init__(self, max_attempt_number: int) -> None:
        self.max_attempt_number = max_attempt_number

    def__call__(
        self, attempts: int, elapsed_time: float, *, upcoming_sleep: float = 0.0
    ) -> bool:
        return attempts >= self.max_attempt_number

```
 |  
| --- | --- |  
##  stop_after_delay [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.stop_after_delay "Permanent link")
Bases: `_StopConditionBase`
Stop after a maximum elapsed time in seconds.
Examples:

```
stop_after_delay(30)

```

Source code in `workflows/retry_policy.py`  
| 
```
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
```
 | 
```
classstop_after_delay(_StopConditionBase):
"""
    Stop after a maximum elapsed time in seconds.

    Examples:
        ```python
        stop_after_delay(30)
        ```
    """

    def__init__(self, max_delay: time_unit_type) -> None:
        self.max_delay = _to_seconds(max_delay)

    def__call__(
        self, attempts: int, elapsed_time: float, *, upcoming_sleep: float = 0.0
    ) -> bool:
        return elapsed_time >= self.max_delay

```
 |  
| --- | --- |  
##  stop_before_delay [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.stop_before_delay "Permanent link")
Bases: `_StopConditionBase`
Stop if the next sleep would move the retry past the configured limit.
Unlike `stop_after_delay`, this condition considers the `upcoming_sleep` value produced by the wait strategy.
Examples:

```
stop_before_delay(30)

```

Source code in `workflows/retry_policy.py`  
| 
```
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
```
 | 
```
classstop_before_delay(_StopConditionBase):
"""
    Stop if the next sleep would move the retry past the configured limit.

    Unlike `stop_after_delay`, this condition considers the ``upcoming_sleep``
    value produced by the wait strategy.

    Examples:
        ```python
        stop_before_delay(30)
        ```
    """

    def__init__(self, max_delay: time_unit_type) -> None:
        self.max_delay = _to_seconds(max_delay)

    def__call__(
        self, attempts: int, elapsed_time: float, *, upcoming_sleep: float = 0.0
    ) -> bool:
        return elapsed_time + upcoming_sleep >= self.max_delay

```
 |  
| --- | --- |  
##  stop_any [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.stop_any "Permanent link")
Bases: `_StopConditionBase`
Stop if any of the provided stop predicates match.
Equivalent to combining stop conditions with `|`.
Examples:

```
stop_any(stop_after_attempt(5), stop_after_delay(30))

```

Source code in `workflows/retry_policy.py`  
| 
```
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
```
 | 
```
classstop_any(_StopConditionBase):
"""
    Stop if any of the provided stop predicates match.

    Equivalent to combining stop conditions with ``|``.

    Examples:
        ```python
        stop_any(stop_after_attempt(5), stop_after_delay(30))
        ```
    """

    def__init__(self, *stops: StopCondition) -> None:
        self.stops = stops

    def__call__(
        self, attempts: int, elapsed_time: float, *, upcoming_sleep: float = 0.0
    ) -> bool:
        return any(
            stop(attempts, elapsed_time, upcoming_sleep=upcoming_sleep)
            for stop in self.stops
        )

```
 |  
| --- | --- |  
##  stop_all [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.stop_all "Permanent link")
Bases: `_StopConditionBase`
Stop if all of the provided stop predicates match.
Equivalent to combining stop conditions with .
Examples:

```
stop_all(stop_after_attempt(5), stop_after_delay(30))

```

Source code in `workflows/retry_policy.py`  
| 
```
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
```
 | 
```
classstop_all(_StopConditionBase):
"""
    Stop if all of the provided stop predicates match.

    Equivalent to combining stop conditions with ``&``.

    Examples:
        ```python
        stop_all(stop_after_attempt(5), stop_after_delay(30))
        ```
    """

    def__init__(self, *stops: StopCondition) -> None:
        self.stops = stops

    def__call__(
        self, attempts: int, elapsed_time: float, *, upcoming_sleep: float = 0.0
    ) -> bool:
        return all(
            stop(attempts, elapsed_time, upcoming_sleep=upcoming_sleep)
            for stop in self.stops
        )

```
 |  
| --- | --- |  
##  stop_never [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.stop_never "Permanent link")
Bases: `_StopConditionBase`
Stop condition that never stops.
This is typically paired with a retry predicate or workflow timeout that provides the real upper bound.
Examples:

```
stop_never()

```

Source code in `workflows/retry_policy.py`  
| 
```
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
```
 | 
```
classstop_never(_StopConditionBase):
"""
    Stop condition that never stops.

    This is typically paired with a retry predicate or workflow timeout that
    provides the real upper bound.

    Examples:
        ```python
        stop_never()
        ```
    """

    def__call__(
        self, attempts: int, elapsed_time: float, *, upcoming_sleep: float = 0.0
    ) -> bool:
        return False

```
 |  
| --- | --- |  
## Deprecated Constructors[#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#deprecated-constructors "Permanent link")
The following helpers predate the composable API and are kept for backwards compatibility. Prefer `retry_policy(...)` with explicit retry, wait, and stop arguments.
##  ConstantDelayRetryPolicy [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.ConstantDelayRetryPolicy "Permanent link")

```
ConstantDelayRetryPolicy(maximum_attempts:  = 3, delay: float = 5) -> 

```

Retry at a fixed interval up to a maximum number of attempts.
Deprecated: use `retry_policy(wait=wait_fixed(delay), stop=stop_after_attempt(n))` instead.
Examples:

```
ConstantDelayRetryPolicy(delay=5, maximum_attempts=10)

```

Source code in `workflows/retry_policy.py`  
| 
```
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
```
 | 
```
defConstantDelayRetryPolicy(
    maximum_attempts: int = 3,
    delay: float = 5,
) -> RetryPolicy:
"""
    Retry at a fixed interval up to a maximum number of attempts.

    Deprecated: use ``retry_policy(wait=wait_fixed(delay), stop=stop_after_attempt(n))`` instead.

    Examples:
        ```python
        ConstantDelayRetryPolicy(delay=5, maximum_attempts=10)
        ```
    """
    warnings.warn(
        "ConstantDelayRetryPolicy is deprecated, use "
        "retry_policy(wait=wait_fixed(delay), stop=stop_after_attempt(n)) instead",
        DeprecationWarning,
        stacklevel=2,
    )

    return _ComposableRetryPolicy(
        wait=wait_fixed(delay),
        stop=stop_after_attempt(maximum_attempts),
    )

```
 |  
| --- | --- |  
##  ExponentialBackoffRetryPolicy [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.ExponentialBackoffRetryPolicy "Permanent link")

```
ExponentialBackoffRetryPolicy(maximum_attempts:  = 5, initial_delay: float = 1.0, multiplier: float = 2.0, max_delay: float = 60.0, jitter:  = True) -> 

```

Retry with exponentially increasing delays, optional jitter, and a cap.
Deprecated: use `retry_policy(wait=wait_exponential(...), stop=stop_after_attempt(n))` instead. For jitter, use `wait_random_exponential` or `wait_exponential_jitter`.
Examples:

```
ExponentialBackoffRetryPolicy(
    initial_delay=1,
    multiplier=2,
    max_delay=30,
    maximum_attempts=5,
    jitter=True,
)

```

Source code in `workflows/retry_policy.py`  
| 
```
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
921
922
923
924
925
926
927
928
929
930
931
932
933
934
935
```
 | 
```
defExponentialBackoffRetryPolicy(
    maximum_attempts: int = 5,
    initial_delay: float = 1.0,
    multiplier: float = 2.0,
    max_delay: float = 60.0,
    jitter: bool = True,
) -> RetryPolicy:
"""
    Retry with exponentially increasing delays, optional jitter, and a cap.

    Deprecated: use ``retry_policy(wait=wait_exponential(...), stop=stop_after_attempt(n))`` instead.
    For jitter, use ``wait_random_exponential`` or ``wait_exponential_jitter``.

    Examples:
        ```python
        ExponentialBackoffRetryPolicy(
            initial_delay=1,
            multiplier=2,
            max_delay=30,
            maximum_attempts=5,
            jitter=True,

        ```
    """
    warnings.warn(
        "ExponentialBackoffRetryPolicy is deprecated, use "
        "retry_policy(wait=wait_exponential(...), stop=stop_after_attempt(n)) instead",
        DeprecationWarning,
        stacklevel=2,
    )

    wait: WaitStrategy
    if jitter:
        wait = wait_random_exponential(
            multiplier=initial_delay,
            exp_base=multiplier,
            max=max_delay,
        )
    else:
        wait = wait_exponential(
            multiplier=initial_delay,
            exp_base=multiplier,
            max=max_delay,
        )

    return _ComposableRetryPolicy(
        wait=wait,
        stop=stop_after_attempt(maximum_attempts),
    )

```
 |  
| --- | --- |
