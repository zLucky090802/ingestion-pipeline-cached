# Index
Evaluation modules.
##  AnswerRelevancyEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.AnswerRelevancyEvaluator "Permanent link")
Bases: 
Answer relevancy evaluator.
Evaluates the relevancy of response to a query. This evaluator considers the query string and response string.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `raise_error`  |  `Optional[bool]`  |  Whether to raise an error if the response is invalid. Defaults to False.  |  `False`  |  
|  `eval_template`  |  `Optional[Union[str, BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]]`  |  The template to use for evaluation.  |  `None`  |  
|  `refine_template`  |  `Optional[Union[str, BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]]`  |  The template to use for refinement.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/evaluation/answer_relevancy.py`  
| 
```
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
```
 | 
```
classAnswerRelevancyEvaluator(BaseEvaluator):
"""
    Answer relevancy evaluator.

    Evaluates the relevancy of response to a query.
    This evaluator considers the query string and response string.

    Args:
        raise_error(Optional[bool]):
            Whether to raise an error if the response is invalid.
            Defaults to False.
        eval_template(Optional[Union[str, BasePromptTemplate]]):
            The template to use for evaluation.
        refine_template(Optional[Union[str, BasePromptTemplate]]):
            The template to use for refinement.

    """

    def__init__(
        self,
        llm: Optional[LLM] = None,
        raise_error: bool = False,
        eval_template: str | BasePromptTemplate | None = None,
        score_threshold: float = _DEFAULT_SCORE_THRESHOLD,
        parser_function: Callable[
            [str], Tuple[Optional[float], Optional[str]]
        ] = _default_parser_function,
    ) -> None:
"""Init params."""
        self._llm = llm or Settings.llm
        self._raise_error = raise_error

        self._eval_template: BasePromptTemplate
        if isinstance(eval_template, str):
            self._eval_template = PromptTemplate(eval_template)
        else:
            self._eval_template = eval_template or DEFAULT_EVAL_TEMPLATE

        self.parser_function = parser_function
        self.score_threshold = score_threshold

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {
            "eval_template": self._eval_template,
            "refine_template": self._refine_template,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "eval_template" in prompts:
            self._eval_template = prompts["eval_template"]
        if "refine_template" in prompts:
            self._refine_template = prompts["refine_template"]

    async defaevaluate(
        self,
        query: str | None = None,
        response: str | None = None,
        contexts: Sequence[str] | None = None,
        sleep_time_in_seconds: int = 0,
        **kwargs: Any,
    ) -> EvaluationResult:
"""Evaluate whether the response is relevant to the query."""
        del kwargs  # Unused
        del contexts  # Unused

        if query is None or response is None:
            raise ValueError("query and response must be provided")

        await asyncio.sleep(sleep_time_in_seconds)

        eval_response = await self._llm.apredict(
            prompt=self._eval_template,
            query=query,
            response=response,
        )

        score, reasoning = self.parser_function(eval_response)

        invalid_result, invalid_reason = False, None
        if score is None and reasoning is None:
            if self._raise_error:
                raise ValueError("The response is invalid")
            invalid_result = True
            invalid_reason = "Unable to parse the output string."

        if score:
            score /= self.score_threshold

        return EvaluationResult(
            query=query,
            response=response,
            score=score,
            feedback=eval_response,
            invalid_result=invalid_result,
            invalid_reason=invalid_reason,
        )

```
 |  
| --- | --- |  
###  aevaluate [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.AnswerRelevancyEvaluator.aevaluate "Permanent link")

```
aevaluate(
    query:  | None = None,
    response:  | None = None,
    contexts: Sequence[] | None = None,
    sleep_time_in_seconds:  = 0,
    **kwargs: 
) -> 

```

Evaluate whether the response is relevant to the query.
Source code in `llama-index-core/llama_index/core/evaluation/answer_relevancy.py`  
| 
```
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
```
 | 
```
async defaevaluate(
    self,
    query: str | None = None,
    response: str | None = None,
    contexts: Sequence[str] | None = None,
    sleep_time_in_seconds: int = 0,
    **kwargs: Any,
) -> EvaluationResult:
"""Evaluate whether the response is relevant to the query."""
    del kwargs  # Unused
    del contexts  # Unused

    if query is None or response is None:
        raise ValueError("query and response must be provided")

    await asyncio.sleep(sleep_time_in_seconds)

    eval_response = await self._llm.apredict(
        prompt=self._eval_template,
        query=query,
        response=response,
    )

    score, reasoning = self.parser_function(eval_response)

    invalid_result, invalid_reason = False, None
    if score is None and reasoning is None:
        if self._raise_error:
            raise ValueError("The response is invalid")
        invalid_result = True
        invalid_reason = "Unable to parse the output string."

    if score:
        score /= self.score_threshold

    return EvaluationResult(
        query=query,
        response=response,
        score=score,
        feedback=eval_response,
        invalid_result=invalid_result,
        invalid_reason=invalid_reason,
    )

```
 |  
| --- | --- |  
##  BaseEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseEvaluator "Permanent link")
Bases: `PromptMixin`
Base Evaluator class.
Source code in `llama-index-core/llama_index/core/evaluation/base.py`  
| 
```
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
```
 | 
```
classBaseEvaluator(PromptMixin):
"""Base Evaluator class."""

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt modules."""
        return {}

    defevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
"""
        Run evaluation with query string, retrieved contexts,
        and generated response string.

        Subclasses can override this method to provide custom evaluation logic and
        take in additional arguments.
        """
        return asyncio_run(
            self.aevaluate(
                query=query,
                response=response,
                contexts=contexts,
                **kwargs,
            )
        )

    @abstractmethod
    async defaevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
"""
        Run evaluation with query string, retrieved contexts,
        and generated response string.

        Subclasses can override this method to provide custom evaluation logic and
        take in additional arguments.
        """
        raise NotImplementedError

    defevaluate_response(
        self,
        query: Optional[str] = None,
        response: Optional[Response] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
"""
        Run evaluation with query string and generated Response object.

        Subclasses can override this method to provide custom evaluation logic and
        take in additional arguments.
        """
        response_str: Optional[str] = None
        contexts: Optional[Sequence[str]] = None
        if response is not None:
            response_str = response.response
            contexts = [node.get_content() for node in response.source_nodes]

        return self.evaluate(
            query=query, response=response_str, contexts=contexts, **kwargs
        )

    async defaevaluate_response(
        self,
        query: Optional[str] = None,
        response: Optional[Response] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
"""
        Run evaluation with query string and generated Response object.

        Subclasses can override this method to provide custom evaluation logic and
        take in additional arguments.
        """
        response_str: Optional[str] = None
        contexts: Optional[Sequence[str]] = None
        if response is not None:
            response_str = response.response
            contexts = [node.get_content() for node in response.source_nodes]

        return await self.aevaluate(
            query=query, response=response_str, contexts=contexts, **kwargs
        )

```
 |  
| --- | --- |  
###  evaluate [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseEvaluator.evaluate "Permanent link")

```
evaluate(
    query: Optional[] = None,
    response: Optional[] = None,
    contexts: Optional[Sequence[]] = None,
    **kwargs: 
) -> 

```

Run evaluation with query string, retrieved contexts, and generated response string.
Subclasses can override this method to provide custom evaluation logic and take in additional arguments.
Source code in `llama-index-core/llama_index/core/evaluation/base.py`  
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
```
 | 
```
defevaluate(
    self,
    query: Optional[str] = None,
    response: Optional[str] = None,
    contexts: Optional[Sequence[str]] = None,
    **kwargs: Any,
) -> EvaluationResult:
"""
    Run evaluation with query string, retrieved contexts,
    and generated response string.

    Subclasses can override this method to provide custom evaluation logic and
    take in additional arguments.
    """
    return asyncio_run(
        self.aevaluate(
            query=query,
            response=response,
            contexts=contexts,
            **kwargs,
        )
    )

```
 |  
| --- | --- |  
###  aevaluate `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseEvaluator.aevaluate "Permanent link")

```
aevaluate(
    query: Optional[] = None,
    response: Optional[] = None,
    contexts: Optional[Sequence[]] = None,
    **kwargs: 
) -> 

```

Run evaluation with query string, retrieved contexts, and generated response string.
Subclasses can override this method to provide custom evaluation logic and take in additional arguments.
Source code in `llama-index-core/llama_index/core/evaluation/base.py`  
| 
```
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
```
 | 
```
@abstractmethod
async defaevaluate(
    self,
    query: Optional[str] = None,
    response: Optional[str] = None,
    contexts: Optional[Sequence[str]] = None,
    **kwargs: Any,
) -> EvaluationResult:
"""
    Run evaluation with query string, retrieved contexts,
    and generated response string.

    Subclasses can override this method to provide custom evaluation logic and
    take in additional arguments.
    """
    raise NotImplementedError

```
 |  
| --- | --- |  
###  evaluate_response [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseEvaluator.evaluate_response "Permanent link")

```
evaluate_response(
    query: Optional[] = None,
    response: Optional[] = None,
    **kwargs: 
) -> 

```

Run evaluation with query string and generated Response object.
Subclasses can override this method to provide custom evaluation logic and take in additional arguments.
Source code in `llama-index-core/llama_index/core/evaluation/base.py`  
| 
```
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
```
 | 
```
defevaluate_response(
    self,
    query: Optional[str] = None,
    response: Optional[Response] = None,
    **kwargs: Any,
) -> EvaluationResult:
"""
    Run evaluation with query string and generated Response object.

    Subclasses can override this method to provide custom evaluation logic and
    take in additional arguments.
    """
    response_str: Optional[str] = None
    contexts: Optional[Sequence[str]] = None
    if response is not None:
        response_str = response.response
        contexts = [node.get_content() for node in response.source_nodes]

    return self.evaluate(
        query=query, response=response_str, contexts=contexts, **kwargs
    )

```
 |  
| --- | --- |  
###  aevaluate_response [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseEvaluator.aevaluate_response "Permanent link")

```
aevaluate_response(
    query: Optional[] = None,
    response: Optional[] = None,
    **kwargs: 
) -> 

```

Run evaluation with query string and generated Response object.
Subclasses can override this method to provide custom evaluation logic and take in additional arguments.
Source code in `llama-index-core/llama_index/core/evaluation/base.py`  
| 
```
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
```
 | 
```
async defaevaluate_response(
    self,
    query: Optional[str] = None,
    response: Optional[Response] = None,
    **kwargs: Any,
) -> EvaluationResult:
"""
    Run evaluation with query string and generated Response object.

    Subclasses can override this method to provide custom evaluation logic and
    take in additional arguments.
    """
    response_str: Optional[str] = None
    contexts: Optional[Sequence[str]] = None
    if response is not None:
        response_str = response.response
        contexts = [node.get_content() for node in response.source_nodes]

    return await self.aevaluate(
        query=query, response=response_str, contexts=contexts, **kwargs
    )

```
 |  
| --- | --- |  
##  EvaluationResult [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.EvaluationResult "Permanent link")
Bases: `BaseModel`
Evaluation result.
Output of an BaseEvaluator.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  `str | None`  |  Query string  |  `None`  |  
|  `contexts`  |  `Sequence[str] | None`  |  Context strings  |  `None`  |  
|  `response`  |  `str | None`  |  Response string  |  `None`  |  
|  `passing`  |  `bool | None`  |  Binary evaluation result (passing or not)  |  `None`  |  
|  `feedback`  |  `str | None`  |  Feedback or reasoning for the response  |  `None`  |  
|  `score`  |  `float | None`  |  Score for the response  |  `None`  |  
|  `pairwise_source`  |  `str | None`  |  Used only for pairwise and specifies whether it is from original order of presented answers or flipped order  |  `None`  |  
|  `invalid_result`  |  `bool`  |  Whether the evaluation result is an invalid one.  |  `False`  |  
|  `invalid_reason`  |  `str | None`  |  Reason for invalid evaluation.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/evaluation/base.py`  
| 
```
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
```
 | 
```
classEvaluationResult(BaseModel):
"""
    Evaluation result.

    Output of an BaseEvaluator.
    """

    query: Optional[str] = Field(default=None, description="Query string")
    contexts: Optional[Sequence[str]] = Field(
        default=None, description="Context strings"
    )
    response: Optional[str] = Field(default=None, description="Response string")
    passing: Optional[bool] = Field(
        default=None, description="Binary evaluation result (passing or not)"
    )
    feedback: Optional[str] = Field(
        default=None, description="Feedback or reasoning for the response"
    )
    score: Optional[float] = Field(default=None, description="Score for the response")
    pairwise_source: Optional[str] = Field(
        default=None,
        description=(
            "Used only for pairwise and specifies whether it is from original order of"
            " presented answers or flipped order"
        ),
    )
    invalid_result: bool = Field(
        default=False, description="Whether the evaluation result is an invalid one."
    )
    invalid_reason: Optional[str] = Field(
        default=None, description="Reason for invalid evaluation."
    )

```
 |  
| --- | --- |  
##  BatchEvalRunner [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BatchEvalRunner "Permanent link")
Batch evaluation runner.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `evaluators`  |  `Dict[str, BaseEvaluator[](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseEvaluator "BaseEvaluator \(llama_index.core.evaluation.base.BaseEvaluator\)")]`  |  Dictionary of evaluators.  |  _required_  |  
|  `workers`  |  Number of workers to use for parallelization. Defaults to 2.  |  
|  `show_progress`  |  `bool`  |  Whether to show progress bars. Defaults to False.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/evaluation/batch_runner.py`  
| 
```
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
```
 | 
```
classBatchEvalRunner:
"""
    Batch evaluation runner.

    Args:
        evaluators (Dict[str, BaseEvaluator]): Dictionary of evaluators.
        workers (int): Number of workers to use for parallelization.
            Defaults to 2.
        show_progress (bool): Whether to show progress bars. Defaults to False.

    """

    def__init__(
        self,
        evaluators: Dict[str, BaseEvaluator],
        workers: int = 2,
        show_progress: bool = False,
    ):
        self.evaluators = evaluators
        self.workers = workers
        self.semaphore = asyncio.Semaphore(self.workers)
        self.show_progress = show_progress
        self.asyncio_mod = asyncio_module(show_progress=self.show_progress)

    def_format_results(
        self, results: List[Tuple[str, EvaluationResult]]
    ) -> Dict[str, List[EvaluationResult]]:
"""Format results."""
        # Format results
        results_dict: Dict[str, List[EvaluationResult]] = {
            name: [] for name in self.evaluators
        }
        for name, result in results:
            results_dict[name].append(result)

        return results_dict

    def_validate_and_clean_inputs(
        self,
        *inputs_list: Any,
    ) -> List[Any]:
"""
        Validate and clean input lists.

        Enforce that at least one of the inputs is not None.
        Make sure that all inputs have the same length.
        Make sure that None inputs are replaced with [None] * len(inputs).

        """
        assert len(inputs_list)  0
        # first, make sure at least one of queries or response_strs is not None
        input_len: Optional[int] = None
        for inputs in inputs_list:
            if inputs is not None:
                input_len = len(inputs)
                break
        if input_len is None:
            raise ValueError("At least one item in inputs_list must be provided.")

        new_inputs_list = []
        for inputs in inputs_list:
            if inputs is None:
                new_inputs_list.append([None] * input_len)
            else:
                if len(inputs) != input_len:
                    raise ValueError("All inputs must have the same length.")
                new_inputs_list.append(inputs)
        return new_inputs_list

    def_validate_nested_eval_kwargs_types(
        self, eval_kwargs_lists: Dict[str, Any]
    ) -> Dict[str, Any]:
"""
        Ensure eval kwargs are acceptable format.
            either a Dict[str, List] or a Dict[str, Dict[str, List]].

        Allows use of different kwargs (e.g. references) with different evaluators
            while keeping backwards compatibility for single evaluators

        """
        if not isinstance(eval_kwargs_lists, dict):
            raise ValueError(
                f"eval_kwargs_lists must be a dict. Got {eval_kwargs_lists}"
            )

        for evaluator, eval_kwargs in eval_kwargs_lists.items():
            if isinstance(eval_kwargs, list):
                # maintain backwards compatibility - for use with single evaluator
                eval_kwargs_lists[evaluator] = self._validate_and_clean_inputs(
                    eval_kwargs
                )[0]
            elif isinstance(eval_kwargs, dict):
                # for use with multiple evaluators
                for k in eval_kwargs:
                    v = eval_kwargs[k]
                    if not isinstance(v, list):
                        raise ValueError(
                            f"nested inner values in eval_kwargs must be a list. Got {evaluator}: {k}: {v}"
                        )
                    eval_kwargs_lists[evaluator][k] = self._validate_and_clean_inputs(
                        v
                    )[0]
            else:
                raise ValueError(
                    f"eval_kwargs must be a list or a dict. Got {evaluator}: {eval_kwargs}"
                )
        return eval_kwargs_lists

    def_get_eval_kwargs(
        self, eval_kwargs_lists: Dict[str, Any], idx: int
    ) -> Dict[str, Any]:
"""
        Get eval kwargs from eval_kwargs_lists at a given idx.

        Since eval_kwargs_lists is a dict of lists, we need to get the
        value at idx for each key.

        """
        return {k: v[idx] for k, v in eval_kwargs_lists.items()}

    async defaevaluate_response_strs(
        self,
        queries: Optional[List[str]] = None,
        response_strs: Optional[List[str]] = None,
        contexts_list: Optional[List[List[str]]] = None,
        **eval_kwargs_lists: Dict[str, Any],
    ) -> Dict[str, List[EvaluationResult]]:
"""
        Evaluate query, response pairs.

        This evaluates queries, responses, contexts as string inputs.
        Can supply additional kwargs to the evaluator in eval_kwargs_lists.

        Args:
            queries (Optional[List[str]]): List of query strings. Defaults to None.
            response_strs (Optional[List[str]]): List of response strings.
                Defaults to None.
            contexts_list (Optional[List[List[str]]]): List of context lists.
                Defaults to None.
            **eval_kwargs_lists (Dict[str, Any]): Dict of either dicts or lists
                of kwargs to pass to evaluator. Defaults to None.
                    multiple evaluators: {evaluator: {kwarg: [list of values]},...}
                    single evaluator:    {kwarg: [list of values]}

        """
        queries, response_strs, contexts_list = self._validate_and_clean_inputs(
            queries, response_strs, contexts_list
        )
        eval_kwargs_lists = self._validate_nested_eval_kwargs_types(eval_kwargs_lists)

        # boolean to check if using multi kwarg evaluator
        multi_kwargs = len(eval_kwargs_lists)  0 and isinstance(
            next(iter(eval_kwargs_lists.values())), dict
        )

        # run evaluations
        eval_jobs = []
        for idx, query in enumerate(cast(List[str], queries)):
            response_str = cast(List, response_strs)[idx]
            contexts = cast(List, contexts_list)[idx]
            for name, evaluator in self.evaluators.items():
                if multi_kwargs:
                    # multi-evaluator - get appropriate runtime kwargs if present
                    kwargs = (
                        eval_kwargs_lists[name] if name in eval_kwargs_lists else {}
                    )
                else:
                    # single evaluator (maintain backwards compatibility)
                    kwargs = eval_kwargs_lists
                eval_kwargs = self._get_eval_kwargs(kwargs, idx)
                eval_jobs.append(
                    eval_worker(
                        self.semaphore,
                        evaluator,
                        name,
                        query=query,
                        response_str=response_str,
                        contexts=contexts,
                        eval_kwargs=eval_kwargs,
                    )
                )
        results = await self.asyncio_mod.gather(*eval_jobs)

        # Format results
        return self._format_results(results)

    async defaevaluate_responses(
        self,
        queries: Optional[List[str]] = None,
        responses: Optional[List[Response]] = None,
        **eval_kwargs_lists: Dict[str, Any],
    ) -> Dict[str, List[EvaluationResult]]:
"""
        Evaluate query, response pairs.

        This evaluates queries and response objects.

        Args:
            queries (Optional[List[str]]): List of query strings. Defaults to None.
            responses (Optional[List[Response]]): List of response objects.
                Defaults to None.
            **eval_kwargs_lists (Dict[str, Any]): Dict of either dicts or lists
                of kwargs to pass to evaluator. Defaults to None.
                    multiple evaluators: {evaluator: {kwarg: [list of values]},...}
                    single evaluator:    {kwarg: [list of values]}

        """
        queries, responses = self._validate_and_clean_inputs(queries, responses)
        eval_kwargs_lists = self._validate_nested_eval_kwargs_types(eval_kwargs_lists)

        # boolean to check if using multi kwarg evaluator
        multi_kwargs = len(eval_kwargs_lists)  0 and isinstance(
            next(iter(eval_kwargs_lists.values())), dict
        )

        # run evaluations
        eval_jobs = []
        for idx, query in enumerate(cast(List[str], queries)):
            response = cast(List, responses)[idx]
            for name, evaluator in self.evaluators.items():
                if multi_kwargs:
                    # multi-evaluator - get appropriate runtime kwargs if present
                    kwargs = (
                        eval_kwargs_lists[name] if name in eval_kwargs_lists else {}
                    )
                else:
                    # single evaluator (maintain backwards compatibility)
                    kwargs = eval_kwargs_lists
                eval_kwargs = self._get_eval_kwargs(kwargs, idx)
                eval_jobs.append(
                    eval_response_worker(
                        self.semaphore,
                        evaluator,
                        name,
                        query=query,
                        response=response,
                        eval_kwargs=eval_kwargs,
                    )
                )
        results = await self.asyncio_mod.gather(*eval_jobs)

        # Format results
        return self._format_results(results)

    async defaevaluate_queries(
        self,
        query_engine: BaseQueryEngine,
        queries: Optional[List[str]] = None,
        **eval_kwargs_lists: Dict[str, Any],
    ) -> Dict[str, List[EvaluationResult]]:
"""
        Evaluate queries.

        Args:
            query_engine (BaseQueryEngine): Query engine.
            queries (Optional[List[str]]): List of query strings. Defaults to None.
            **eval_kwargs_lists (Dict[str, Any]): Dict of lists of kwargs to
                pass to evaluator. Defaults to None.

        """
        if queries is None:
            raise ValueError("`queries` must be provided")

        # gather responses
        response_jobs = []
        for query in queries:
            response_jobs.append(response_worker(self.semaphore, query_engine, query))
        responses = await self.asyncio_mod.gather(*response_jobs)

        return await self.aevaluate_responses(
            queries=queries,
            responses=responses,
            **eval_kwargs_lists,
        )

    defevaluate_response_strs(
        self,
        queries: Optional[List[str]] = None,
        response_strs: Optional[List[str]] = None,
        contexts_list: Optional[List[List[str]]] = None,
        **eval_kwargs_lists: Dict[str, Any],
    ) -> Dict[str, List[EvaluationResult]]:
"""
        Evaluate query, response pairs.

        Sync version of aevaluate_response_strs.

        """
        return asyncio_run(
            self.aevaluate_response_strs(
                queries=queries,
                response_strs=response_strs,
                contexts_list=contexts_list,
                **eval_kwargs_lists,
            )
        )

    defevaluate_responses(
        self,
        queries: Optional[List[str]] = None,
        responses: Optional[List[Response]] = None,
        **eval_kwargs_lists: Dict[str, Any],
    ) -> Dict[str, List[EvaluationResult]]:
"""
        Evaluate query, response objs.

        Sync version of aevaluate_responses.

        """
        return asyncio_run(
            self.aevaluate_responses(
                queries=queries,
                responses=responses,
                **eval_kwargs_lists,
            )
        )

    defevaluate_queries(
        self,
        query_engine: BaseQueryEngine,
        queries: Optional[List[str]] = None,
        **eval_kwargs_lists: Dict[str, Any],
    ) -> Dict[str, List[EvaluationResult]]:
"""
        Evaluate queries.

        Sync version of aevaluate_queries.

        """
        return asyncio_run(
            self.aevaluate_queries(
                query_engine=query_engine,
                queries=queries,
                **eval_kwargs_lists,
            )
        )

```
 |  
| --- | --- |  
###  aevaluate_response_strs [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BatchEvalRunner.aevaluate_response_strs "Permanent link")

```
aevaluate_response_strs(
    queries: Optional[[]] = None,
    response_strs: Optional[[]] = None,
    contexts_list: Optional[[[]]] = None,
    **eval_kwargs_lists: [, ]
) -> [, []]

```

Evaluate query, response pairs.
This evaluates queries, responses, contexts as string inputs. Can supply additional kwargs to the evaluator in eval_kwargs_lists.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `queries`  |  `Optional[List[str]]`  |  List of query strings. Defaults to None.  |  `None`  |  
|  `response_strs`  |  `Optional[List[str]]`  |  List of response strings. Defaults to None.  |  `None`  |  
|  `contexts_list`  |  `Optional[List[List[str]]]`  |  List of context lists. Defaults to None.  |  `None`  |  
|  `**eval_kwargs_lists`  |  `Dict[str, Any]`  |  Dict of either dicts or lists of kwargs to pass to evaluator. Defaults to None. multiple evaluators: {evaluator: {kwarg: [list of values]},...} single evaluator: {kwarg: [list of values]}  |  
Source code in `llama-index-core/llama_index/core/evaluation/batch_runner.py`  
| 
```
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
```
 | 
```
async defaevaluate_response_strs(
    self,
    queries: Optional[List[str]] = None,
    response_strs: Optional[List[str]] = None,
    contexts_list: Optional[List[List[str]]] = None,
    **eval_kwargs_lists: Dict[str, Any],
) -> Dict[str, List[EvaluationResult]]:
"""
    Evaluate query, response pairs.

    This evaluates queries, responses, contexts as string inputs.
    Can supply additional kwargs to the evaluator in eval_kwargs_lists.

    Args:
        queries (Optional[List[str]]): List of query strings. Defaults to None.
        response_strs (Optional[List[str]]): List of response strings.
            Defaults to None.
        contexts_list (Optional[List[List[str]]]): List of context lists.
            Defaults to None.
        **eval_kwargs_lists (Dict[str, Any]): Dict of either dicts or lists
            of kwargs to pass to evaluator. Defaults to None.
                multiple evaluators: {evaluator: {kwarg: [list of values]},...}
                single evaluator:    {kwarg: [list of values]}

    """
    queries, response_strs, contexts_list = self._validate_and_clean_inputs(
        queries, response_strs, contexts_list
    )
    eval_kwargs_lists = self._validate_nested_eval_kwargs_types(eval_kwargs_lists)

    # boolean to check if using multi kwarg evaluator
    multi_kwargs = len(eval_kwargs_lists)  0 and isinstance(
        next(iter(eval_kwargs_lists.values())), dict
    )

    # run evaluations
    eval_jobs = []
    for idx, query in enumerate(cast(List[str], queries)):
        response_str = cast(List, response_strs)[idx]
        contexts = cast(List, contexts_list)[idx]
        for name, evaluator in self.evaluators.items():
            if multi_kwargs:
                # multi-evaluator - get appropriate runtime kwargs if present
                kwargs = (
                    eval_kwargs_lists[name] if name in eval_kwargs_lists else {}
                )
            else:
                # single evaluator (maintain backwards compatibility)
                kwargs = eval_kwargs_lists
            eval_kwargs = self._get_eval_kwargs(kwargs, idx)
            eval_jobs.append(
                eval_worker(
                    self.semaphore,
                    evaluator,
                    name,
                    query=query,
                    response_str=response_str,
                    contexts=contexts,
                    eval_kwargs=eval_kwargs,
                )
            )
    results = await self.asyncio_mod.gather(*eval_jobs)

    # Format results
    return self._format_results(results)

```
 |  
| --- | --- |  
###  aevaluate_responses [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BatchEvalRunner.aevaluate_responses "Permanent link")

```
aevaluate_responses(
    queries: Optional[[]] = None,
    responses: Optional[[]] = None,
    **eval_kwargs_lists: [, ]
) -> [, []]

```

Evaluate query, response pairs.
This evaluates queries and response objects.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `queries`  |  `Optional[List[str]]`  |  List of query strings. Defaults to None.  |  `None`  |  
|  `responses`  |  `Optional[List[Response[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Response "Response


  
      dataclass
   \(llama_index.core.base.response.schema.Response\)")]]`  |  List of response objects. Defaults to None.  |  `None`  |  
|  `**eval_kwargs_lists`  |  `Dict[str, Any]`  |  Dict of either dicts or lists of kwargs to pass to evaluator. Defaults to None. multiple evaluators: {evaluator: {kwarg: [list of values]},...} single evaluator: {kwarg: [list of values]}  |  
Source code in `llama-index-core/llama_index/core/evaluation/batch_runner.py`  
| 
```
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
```
 | 
```
async defaevaluate_responses(
    self,
    queries: Optional[List[str]] = None,
    responses: Optional[List[Response]] = None,
    **eval_kwargs_lists: Dict[str, Any],
) -> Dict[str, List[EvaluationResult]]:
"""
    Evaluate query, response pairs.

    This evaluates queries and response objects.

    Args:
        queries (Optional[List[str]]): List of query strings. Defaults to None.
        responses (Optional[List[Response]]): List of response objects.
            Defaults to None.
        **eval_kwargs_lists (Dict[str, Any]): Dict of either dicts or lists
            of kwargs to pass to evaluator. Defaults to None.
                multiple evaluators: {evaluator: {kwarg: [list of values]},...}
                single evaluator:    {kwarg: [list of values]}

    """
    queries, responses = self._validate_and_clean_inputs(queries, responses)
    eval_kwargs_lists = self._validate_nested_eval_kwargs_types(eval_kwargs_lists)

    # boolean to check if using multi kwarg evaluator
    multi_kwargs = len(eval_kwargs_lists)  0 and isinstance(
        next(iter(eval_kwargs_lists.values())), dict
    )

    # run evaluations
    eval_jobs = []
    for idx, query in enumerate(cast(List[str], queries)):
        response = cast(List, responses)[idx]
        for name, evaluator in self.evaluators.items():
            if multi_kwargs:
                # multi-evaluator - get appropriate runtime kwargs if present
                kwargs = (
                    eval_kwargs_lists[name] if name in eval_kwargs_lists else {}
                )
            else:
                # single evaluator (maintain backwards compatibility)
                kwargs = eval_kwargs_lists
            eval_kwargs = self._get_eval_kwargs(kwargs, idx)
            eval_jobs.append(
                eval_response_worker(
                    self.semaphore,
                    evaluator,
                    name,
                    query=query,
                    response=response,
                    eval_kwargs=eval_kwargs,
                )
            )
    results = await self.asyncio_mod.gather(*eval_jobs)

    # Format results
    return self._format_results(results)

```
 |  
| --- | --- |  
###  aevaluate_queries [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BatchEvalRunner.aevaluate_queries "Permanent link")

```
aevaluate_queries(
    query_engine: ,
    queries: Optional[[]] = None,
    **eval_kwargs_lists: [, ]
) -> [, []]

```

Evaluate queries.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_engine`  |   |  Query engine.  |  _required_  |  
|  `queries`  |  `Optional[List[str]]`  |  List of query strings. Defaults to None.  |  `None`  |  
|  `**eval_kwargs_lists`  |  `Dict[str, Any]`  |  Dict of lists of kwargs to pass to evaluator. Defaults to None.  |  
Source code in `llama-index-core/llama_index/core/evaluation/batch_runner.py`  
| 
```
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
async defaevaluate_queries(
    self,
    query_engine: BaseQueryEngine,
    queries: Optional[List[str]] = None,
    **eval_kwargs_lists: Dict[str, Any],
) -> Dict[str, List[EvaluationResult]]:
"""
    Evaluate queries.

    Args:
        query_engine (BaseQueryEngine): Query engine.
        queries (Optional[List[str]]): List of query strings. Defaults to None.
        **eval_kwargs_lists (Dict[str, Any]): Dict of lists of kwargs to
            pass to evaluator. Defaults to None.

    """
    if queries is None:
        raise ValueError("`queries` must be provided")

    # gather responses
    response_jobs = []
    for query in queries:
        response_jobs.append(response_worker(self.semaphore, query_engine, query))
    responses = await self.asyncio_mod.gather(*response_jobs)

    return await self.aevaluate_responses(
        queries=queries,
        responses=responses,
        **eval_kwargs_lists,
    )

```
 |  
| --- | --- |  
###  evaluate_response_strs [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BatchEvalRunner.evaluate_response_strs "Permanent link")

```
evaluate_response_strs(
    queries: Optional[[]] = None,
    response_strs: Optional[[]] = None,
    contexts_list: Optional[[[]]] = None,
    **eval_kwargs_lists: [, ]
) -> [, []]

```

Evaluate query, response pairs.
Sync version of aevaluate_response_strs.
Source code in `llama-index-core/llama_index/core/evaluation/batch_runner.py`  
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
370
```
 | 
```
defevaluate_response_strs(
    self,
    queries: Optional[List[str]] = None,
    response_strs: Optional[List[str]] = None,
    contexts_list: Optional[List[List[str]]] = None,
    **eval_kwargs_lists: Dict[str, Any],
) -> Dict[str, List[EvaluationResult]]:
"""
    Evaluate query, response pairs.

    Sync version of aevaluate_response_strs.

    """
    return asyncio_run(
        self.aevaluate_response_strs(
            queries=queries,
            response_strs=response_strs,
            contexts_list=contexts_list,
            **eval_kwargs_lists,
        )
    )

```
 |  
| --- | --- |  
###  evaluate_responses [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BatchEvalRunner.evaluate_responses "Permanent link")

```
evaluate_responses(
    queries: Optional[[]] = None,
    responses: Optional[[]] = None,
    **eval_kwargs_lists: [, ]
) -> [, []]

```

Evaluate query, response objs.
Sync version of aevaluate_responses.
Source code in `llama-index-core/llama_index/core/evaluation/batch_runner.py`  
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
386
387
388
389
390
```
 | 
```
defevaluate_responses(
    self,
    queries: Optional[List[str]] = None,
    responses: Optional[List[Response]] = None,
    **eval_kwargs_lists: Dict[str, Any],
) -> Dict[str, List[EvaluationResult]]:
"""
    Evaluate query, response objs.

    Sync version of aevaluate_responses.

    """
    return asyncio_run(
        self.aevaluate_responses(
            queries=queries,
            responses=responses,
            **eval_kwargs_lists,
        )
    )

```
 |  
| --- | --- |  
###  evaluate_queries [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BatchEvalRunner.evaluate_queries "Permanent link")

```
evaluate_queries(
    query_engine: ,
    queries: Optional[[]] = None,
    **eval_kwargs_lists: [, ]
) -> [, []]

```

Evaluate queries.
Sync version of aevaluate_queries.
Source code in `llama-index-core/llama_index/core/evaluation/batch_runner.py`  
| 
```
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
```
 | 
```
defevaluate_queries(
    self,
    query_engine: BaseQueryEngine,
    queries: Optional[List[str]] = None,
    **eval_kwargs_lists: Dict[str, Any],
) -> Dict[str, List[EvaluationResult]]:
"""
    Evaluate queries.

    Sync version of aevaluate_queries.

    """
    return asyncio_run(
        self.aevaluate_queries(
            query_engine=query_engine,
            queries=queries,
            **eval_kwargs_lists,
        )
    )

```
 |  
| --- | --- |  
##  ContextRelevancyEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.ContextRelevancyEvaluator "Permanent link")
Bases: 
Context relevancy evaluator.
Evaluates the relevancy of retrieved contexts to a query. This evaluator considers the query string and retrieved contexts.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `raise_error`  |  `Optional[bool]`  |  Whether to raise an error if the response is invalid. Defaults to False.  |  `False`  |  
|  `eval_template`  |  `Optional[Union[str, BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]]`  |  The template to use for evaluation.  |  `None`  |  
|  `refine_template`  |  `Optional[Union[str, BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]]`  |  The template to use for refinement.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/evaluation/context_relevancy.py`  
| 
```
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
```
 | 
```
classContextRelevancyEvaluator(BaseEvaluator):
"""
    Context relevancy evaluator.

    Evaluates the relevancy of retrieved contexts to a query.
    This evaluator considers the query string and retrieved contexts.

    Args:
        raise_error(Optional[bool]):
            Whether to raise an error if the response is invalid.
            Defaults to False.
        eval_template(Optional[Union[str, BasePromptTemplate]]):
            The template to use for evaluation.
        refine_template(Optional[Union[str, BasePromptTemplate]]):
            The template to use for refinement.

    """

    def__init__(
        self,
        llm: Optional[LLM] = None,
        raise_error: bool = False,
        eval_template: str | BasePromptTemplate | None = None,
        refine_template: str | BasePromptTemplate | None = None,
        score_threshold: float = _DEFAULT_SCORE_THRESHOLD,
        parser_function: Callable[
            [str], Tuple[Optional[float], Optional[str]]
        ] = _default_parser_function,
    ) -> None:
"""Init params."""
        fromllama_index.coreimport Settings

        self._llm = llm or Settings.llm
        self._raise_error = raise_error

        self._eval_template: BasePromptTemplate
        if isinstance(eval_template, str):
            self._eval_template = PromptTemplate(eval_template)
        else:
            self._eval_template = eval_template or DEFAULT_EVAL_TEMPLATE

        self._refine_template: BasePromptTemplate
        if isinstance(refine_template, str):
            self._refine_template = PromptTemplate(refine_template)
        else:
            self._refine_template = refine_template or DEFAULT_REFINE_TEMPLATE

        self.parser_function = parser_function
        self.score_threshold = score_threshold

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {
            "eval_template": self._eval_template,
            "refine_template": self._refine_template,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "eval_template" in prompts:
            self._eval_template = prompts["eval_template"]
        if "refine_template" in prompts:
            self._refine_template = prompts["refine_template"]

    async defaevaluate(
        self,
        query: str | None = None,
        response: str | None = None,
        contexts: Sequence[str] | None = None,
        sleep_time_in_seconds: int = 0,
        **kwargs: Any,
    ) -> EvaluationResult:
"""Evaluate whether the contexts is relevant to the query."""
        del kwargs  # Unused
        del response  # Unused

        if query is None or contexts is None:
            raise ValueError("Both query and contexts must be provided")

        docs = [Document(text=context) for context in contexts]
        index = SummaryIndex.from_documents(docs)

        await asyncio.sleep(sleep_time_in_seconds)

        query_engine = index.as_query_engine(
            llm=self._llm,
            text_qa_template=self._eval_template,
            refine_template=self._refine_template,
        )
        response_obj = await query_engine.aquery(query)
        raw_response_txt = str(response_obj)

        score, reasoning = self.parser_function(raw_response_txt)

        invalid_result, invalid_reason = False, None
        if score is None and reasoning is None:
            if self._raise_error:
                raise ValueError("The response is invalid")
            invalid_result = True
            invalid_reason = "Unable to parse the output string."

        if score:
            score /= self.score_threshold

        return EvaluationResult(
            query=query,
            contexts=contexts,
            score=score,
            feedback=raw_response_txt,
            invalid_result=invalid_result,
            invalid_reason=invalid_reason,
        )

```
 |  
| --- | --- |  
###  aevaluate [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.ContextRelevancyEvaluator.aevaluate "Permanent link")

```
aevaluate(
    query:  | None = None,
    response:  | None = None,
    contexts: Sequence[] | None = None,
    sleep_time_in_seconds:  = 0,
    **kwargs: 
) -> 

```

Evaluate whether the contexts is relevant to the query.
Source code in `llama-index-core/llama_index/core/evaluation/context_relevancy.py`  
| 
```
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
```
 | 
```
async defaevaluate(
    self,
    query: str | None = None,
    response: str | None = None,
    contexts: Sequence[str] | None = None,
    sleep_time_in_seconds: int = 0,
    **kwargs: Any,
) -> EvaluationResult:
"""Evaluate whether the contexts is relevant to the query."""
    del kwargs  # Unused
    del response  # Unused

    if query is None or contexts is None:
        raise ValueError("Both query and contexts must be provided")

    docs = [Document(text=context) for context in contexts]
    index = SummaryIndex.from_documents(docs)

    await asyncio.sleep(sleep_time_in_seconds)

    query_engine = index.as_query_engine(
        llm=self._llm,
        text_qa_template=self._eval_template,
        refine_template=self._refine_template,
    )
    response_obj = await query_engine.aquery(query)
    raw_response_txt = str(response_obj)

    score, reasoning = self.parser_function(raw_response_txt)

    invalid_result, invalid_reason = False, None
    if score is None and reasoning is None:
        if self._raise_error:
            raise ValueError("The response is invalid")
        invalid_result = True
        invalid_reason = "Unable to parse the output string."

    if score:
        score /= self.score_threshold

    return EvaluationResult(
        query=query,
        contexts=contexts,
        score=score,
        feedback=raw_response_txt,
        invalid_result=invalid_result,
        invalid_reason=invalid_reason,
    )

```
 |  
| --- | --- |  
##  CorrectnessEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.CorrectnessEvaluator "Permanent link")
Bases: 
Correctness evaluator.
Evaluates the correctness of a question answering system. This evaluator depends on `reference` answer to be provided, in addition to the query string and response string.
It outputs a score between 1 and 5, where 1 is the worst and 5 is the best, along with a reasoning for the score. Passing is defined as a score greater than or equal to the given threshold.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `eval_template`  |  `Optional[Union[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)"), str]]`  |  Template for the evaluation prompt.  |  `None`  |  
|  `score_threshold`  |  `float`  |  Numerical threshold for passing the evaluation, defaults to 4.0.  |  `4.0`  |  
Source code in `llama-index-core/llama_index/core/evaluation/correctness.py`  
| 
```
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
```
 | 
```
classCorrectnessEvaluator(BaseEvaluator):
"""
    Correctness evaluator.

    Evaluates the correctness of a question answering system.
    This evaluator depends on `reference` answer to be provided, in addition to the
    query string and response string.

    It outputs a score between 1 and 5, where 1 is the worst and 5 is the best,
    along with a reasoning for the score.
    Passing is defined as a score greater than or equal to the given threshold.

    Args:
        eval_template (Optional[Union[BasePromptTemplate, str]]):
            Template for the evaluation prompt.
        score_threshold (float): Numerical threshold for passing the evaluation,
            defaults to 4.0.

    """

    def__init__(
        self,
        llm: Optional[LLM] = None,
        eval_template: Optional[Union[BasePromptTemplate, str]] = None,
        score_threshold: float = 4.0,
        parser_function: Callable[
            [str], Tuple[Optional[float], Optional[str]]
        ] = default_parser,
    ) -> None:
        self._llm = llm or Settings.llm

        self._eval_template: BasePromptTemplate
        if isinstance(eval_template, str):
            self._eval_template = PromptTemplate(eval_template)
        else:
            self._eval_template = eval_template or DEFAULT_EVAL_TEMPLATE

        self._score_threshold = score_threshold
        self.parser_function = parser_function

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {
            "eval_template": self._eval_template,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "eval_template" in prompts:
            self._eval_template = prompts["eval_template"]

    async defaevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        reference: Optional[str] = None,
        sleep_time_in_seconds: int = 0,
        **kwargs: Any,
    ) -> EvaluationResult:
        del kwargs  # Unused
        del contexts  # Unused

        await asyncio.sleep(sleep_time_in_seconds)

        if query is None or response is None:
            raise ValueError("query, and response must be provided")

        eval_response = await self._llm.apredict(
            prompt=self._eval_template,
            query=query,
            generated_answer=response,
            reference_answer=reference or "(NO REFERENCE ANSWER SUPPLIED)",
        )

        # Use the parser function
        score, reasoning = self.parser_function(eval_response)

        return EvaluationResult(
            query=query,
            response=response,
            passing=score >= self._score_threshold if score is not None else None,
            score=score,
            feedback=reasoning,
        )

```
 |  
| --- | --- |  
##  DatasetGenerator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.DatasetGenerator "Permanent link")
Bases: `PromptMixin`
Generate dataset (question/ question-answer pairs) based on the given documents.
NOTE: this is a beta feature, subject to change!
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `List[Node]`  |  List of nodes. (Optional)  |  _required_  |  
|  `llm`  |  Language model.  |  `None`  |  
|  `callback_manager`  |   |  Callback manager.  |  `None`  |  
|  `num_questions_per_chunk`  |  number of question to be generated per chunk. Each document is chunked of size 512 words.  |  
|  `text_question_template`  |  `BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.base.BasePromptTemplate\)") | None`  |  Question generation template.  |  `None`  |  
|  `question_gen_query`  |  `str | None`  |  Question generation query.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/evaluation/dataset_generation.py`  
| 
```
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
```
 | 
```
@deprecated(
    "Deprecated in favor of `RagDatasetGenerator` which should be used instead.",
    action="always",
)
classDatasetGenerator(PromptMixin):
"""Generate dataset (question/ question-answer pairs) \
    based on the given documents.

    NOTE: this is a beta feature, subject to change!

    Args:
        nodes (List[Node]): List of nodes. (Optional)
        llm (LLM): Language model.
        callback_manager (CallbackManager): Callback manager.
        num_questions_per_chunk: number of question to be \
        generated per chunk. Each document is chunked of size 512 words.
        text_question_template: Question generation template.
        question_gen_query: Question generation query.

    """

    def__init__(
        self,
        nodes: List[BaseNode],
        llm: Optional[LLM] = None,
        callback_manager: Optional[CallbackManager] = None,
        num_questions_per_chunk: int = 10,
        text_question_template: BasePromptTemplate | None = None,
        text_qa_template: BasePromptTemplate | None = None,
        question_gen_query: str | None = None,
        metadata_mode: MetadataMode = MetadataMode.NONE,
        show_progress: bool = False,
    ) -> None:
"""Init params."""
        self.llm = llm or Settings.llm
        self.callback_manager = callback_manager or Settings.callback_manager
        self.text_question_template = text_question_template or PromptTemplate(
            DEFAULT_QUESTION_GENERATION_PROMPT
        )
        self.text_qa_template = text_qa_template or DEFAULT_TEXT_QA_PROMPT
        self.question_gen_query = (
            question_gen_query
            or f"You are a Teacher/Professor. Your task is to setup \
{num_questions_per_chunk} questions for an upcoming \
                        quiz/examination. The questions should be diverse in nature \
                            across the document. Restrict the questions to the \
                                context information provided."
        )
        self.nodes = nodes
        self._metadata_mode = metadata_mode
        self._show_progress = show_progress

    @classmethod
    deffrom_documents(
        cls,
        documents: List[Document],
        llm: Optional[LLM] = None,
        transformations: Optional[List[TransformComponent]] = None,
        callback_manager: Optional[CallbackManager] = None,
        num_questions_per_chunk: int = 10,
        text_question_template: BasePromptTemplate | None = None,
        text_qa_template: BasePromptTemplate | None = None,
        question_gen_query: str | None = None,
        required_keywords: List[str] | None = None,
        exclude_keywords: List[str] | None = None,
        show_progress: bool = False,
    ) -> DatasetGenerator:
"""Generate dataset from documents."""
        llm = llm or Settings.llm
        transformations = transformations or Settings.transformations
        callback_manager = callback_manager or Settings.callback_manager

        nodes = run_transformations(
            documents, transformations, show_progress=show_progress
        )

        # use node postprocessor to filter nodes
        required_keywords = required_keywords or []
        exclude_keywords = exclude_keywords or []
        node_postprocessor = KeywordNodePostprocessor(
            callback_manager=callback_manager,
            required_keywords=required_keywords,
            exclude_keywords=exclude_keywords,
        )
        node_with_scores = [NodeWithScore(node=node) for node in nodes]
        node_with_scores = node_postprocessor.postprocess_nodes(node_with_scores)
        nodes = [node_with_score.node for node_with_score in node_with_scores]

        return cls(
            nodes=nodes,
            llm=llm,
            callback_manager=callback_manager,
            num_questions_per_chunk=num_questions_per_chunk,
            text_question_template=text_question_template,
            text_qa_template=text_qa_template,
            question_gen_query=question_gen_query,
            show_progress=show_progress,
        )

    async def_agenerate_dataset(
        self,
        nodes: List[BaseNode],
        num: int | None = None,
        generate_response: bool = False,
    ) -> QueryResponseDataset:
"""Node question generator."""
        query_tasks: List[Coroutine] = []
        queries: Dict[str, str] = {}
        responses_dict: Dict[str, str] = {}

        if self._show_progress:
            fromtqdm.asyncioimport tqdm_asyncio

            async_module = tqdm_asyncio
        else:
            async_module = asyncio

        summary_indices: List[SummaryIndex] = []
        for node in nodes:
            if num is not None and len(query_tasks) >= num:
                break
            index = SummaryIndex.from_documents(
                [
                    Document(
                        text=node.get_content(metadata_mode=self._metadata_mode),
                        metadata=node.metadata,  # type: ignore
                    )
                ],
                callback_manager=self.callback_manager,
            )

            query_engine = index.as_query_engine(
                llm=self.llm,
                text_qa_template=self.text_question_template,
                use_async=True,
            )
            task = query_engine.aquery(
                self.question_gen_query,
            )
            query_tasks.append(task)
            summary_indices.append(index)

        responses = await async_module.gather(*query_tasks)
        for idx, response in enumerate(responses):
            result = str(response).strip().split("\n")
            cleaned_questions = [
                re.sub(r"^\d+[\).\s]", "", question).strip() for question in result
            ]
            cleaned_questions = [
                question for question in cleaned_questions if len(question)  0
            ]
            cur_queries = {
                str(uuid.uuid4()): question for question in cleaned_questions
            }
            queries.update(cur_queries)

            if generate_response:
                index = summary_indices[idx]
                qr_tasks = []
                cur_query_items = list(cur_queries.items())
                cur_query_keys = [query_id for query_id, _ in cur_query_items]
                for query_id, query in cur_query_items:
                    qa_query_engine = index.as_query_engine(
                        llm=self.llm,
                        text_qa_template=self.text_qa_template,
                    )
                    qr_task = qa_query_engine.aquery(query)
                    qr_tasks.append(qr_task)
                qr_responses = await async_module.gather(*qr_tasks)
                for query_id, qa_response in zip(cur_query_keys, qr_responses):
                    responses_dict[query_id] = str(qa_response)
            else:
                pass

        query_ids = list(queries.keys())
        if num is not None:
            query_ids = query_ids[:num]
            # truncate queries, responses to the subset of query ids
            queries = {query_id: queries[query_id] for query_id in query_ids}
            if generate_response:
                responses_dict = {
                    query_id: responses_dict[query_id] for query_id in query_ids
                }

        return QueryResponseDataset(queries=queries, responses=responses_dict)

    async defagenerate_questions_from_nodes(self, num: int | None = None) -> List[str]:
"""Generates questions for each document."""
        dataset = await self._agenerate_dataset(
            self.nodes, num=num, generate_response=False
        )
        return dataset.questions

    async defagenerate_dataset_from_nodes(
        self, num: int | None = None
    ) -> QueryResponseDataset:
"""Generates questions for each document."""
        return await self._agenerate_dataset(
            self.nodes, num=num, generate_response=True
        )

    defgenerate_questions_from_nodes(self, num: int | None = None) -> List[str]:
"""Generates questions for each document."""
        return asyncio_run(self.agenerate_questions_from_nodes(num=num))

    defgenerate_dataset_from_nodes(
        self, num: int | None = None
    ) -> QueryResponseDataset:
"""Generates questions for each document."""
        return asyncio_run(self.agenerate_dataset_from_nodes(num=num))

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {
            "text_question_template": self.text_question_template,
            "text_qa_template": self.text_qa_template,
        }

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt modules."""
        return {}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "text_question_template" in prompts:
            self.text_question_template = prompts["text_question_template"]
        if "text_qa_template" in prompts:
            self.text_qa_template = prompts["text_qa_template"]

```
 |  
| --- | --- |  
###  from_documents `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.DatasetGenerator.from_documents "Permanent link")

```
from_documents(
    documents: [],
    llm: Optional[] = None,
    transformations: Optional[
        []
    ] = None,
    callback_manager: Optional[] = None,
    num_questions_per_chunk:  = 10,
    text_question_template: (
         | None
    ) = None,
    text_qa_template:  | None = None,
    question_gen_query:  | None = None,
    required_keywords: [] | None = None,
    exclude_keywords: [] | None = None,
    show_progress:  = False,
) -> 

```

Generate dataset from documents.
Source code in `llama-index-core/llama_index/core/evaluation/dataset_generation.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_documents(
    cls,
    documents: List[Document],
    llm: Optional[LLM] = None,
    transformations: Optional[List[TransformComponent]] = None,
    callback_manager: Optional[CallbackManager] = None,
    num_questions_per_chunk: int = 10,
    text_question_template: BasePromptTemplate | None = None,
    text_qa_template: BasePromptTemplate | None = None,
    question_gen_query: str | None = None,
    required_keywords: List[str] | None = None,
    exclude_keywords: List[str] | None = None,
    show_progress: bool = False,
) -> DatasetGenerator:
"""Generate dataset from documents."""
    llm = llm or Settings.llm
    transformations = transformations or Settings.transformations
    callback_manager = callback_manager or Settings.callback_manager

    nodes = run_transformations(
        documents, transformations, show_progress=show_progress
    )

    # use node postprocessor to filter nodes
    required_keywords = required_keywords or []
    exclude_keywords = exclude_keywords or []
    node_postprocessor = KeywordNodePostprocessor(
        callback_manager=callback_manager,
        required_keywords=required_keywords,
        exclude_keywords=exclude_keywords,
    )
    node_with_scores = [NodeWithScore(node=node) for node in nodes]
    node_with_scores = node_postprocessor.postprocess_nodes(node_with_scores)
    nodes = [node_with_score.node for node_with_score in node_with_scores]

    return cls(
        nodes=nodes,
        llm=llm,
        callback_manager=callback_manager,
        num_questions_per_chunk=num_questions_per_chunk,
        text_question_template=text_question_template,
        text_qa_template=text_qa_template,
        question_gen_query=question_gen_query,
        show_progress=show_progress,
    )

```
 |  
| --- | --- |  
###  agenerate_questions_from_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.DatasetGenerator.agenerate_questions_from_nodes "Permanent link")

```
agenerate_questions_from_nodes(
    num:  | None = None,
) -> []

```

Generates questions for each document.
Source code in `llama-index-core/llama_index/core/evaluation/dataset_generation.py`  
| 
```
299
300
301
302
303
304
```
 | 
```
async defagenerate_questions_from_nodes(self, num: int | None = None) -> List[str]:
"""Generates questions for each document."""
    dataset = await self._agenerate_dataset(
        self.nodes, num=num, generate_response=False
    )
    return dataset.questions

```
 |  
| --- | --- |  
###  agenerate_dataset_from_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.DatasetGenerator.agenerate_dataset_from_nodes "Permanent link")

```
agenerate_dataset_from_nodes(
    num:  | None = None,
) -> 

```

Generates questions for each document.
Source code in `llama-index-core/llama_index/core/evaluation/dataset_generation.py`  
| 
```
306
307
308
309
310
311
312
```
 | 
```
async defagenerate_dataset_from_nodes(
    self, num: int | None = None
) -> QueryResponseDataset:
"""Generates questions for each document."""
    return await self._agenerate_dataset(
        self.nodes, num=num, generate_response=True
    )

```
 |  
| --- | --- |  
###  generate_questions_from_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.DatasetGenerator.generate_questions_from_nodes "Permanent link")

```
generate_questions_from_nodes(
    num:  | None = None,
) -> []

```

Generates questions for each document.
Source code in `llama-index-core/llama_index/core/evaluation/dataset_generation.py`  
| 
```
314
315
316
```
 | 
```
defgenerate_questions_from_nodes(self, num: int | None = None) -> List[str]:
"""Generates questions for each document."""
    return asyncio_run(self.agenerate_questions_from_nodes(num=num))

```
 |  
| --- | --- |  
###  generate_dataset_from_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.DatasetGenerator.generate_dataset_from_nodes "Permanent link")

```
generate_dataset_from_nodes(
    num:  | None = None,
) -> 

```

Generates questions for each document.
Source code in `llama-index-core/llama_index/core/evaluation/dataset_generation.py`  
| 
```
318
319
320
321
322
```
 | 
```
defgenerate_dataset_from_nodes(
    self, num: int | None = None
) -> QueryResponseDataset:
"""Generates questions for each document."""
    return asyncio_run(self.agenerate_dataset_from_nodes(num=num))

```
 |  
| --- | --- |  
##  QueryResponseDataset [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.QueryResponseDataset "Permanent link")
Bases: `BaseModel`
Query Response Dataset.
The response can be empty if the dataset is generated from documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `queries`  |  `Dict[str, str]`  |  Query id -> query.  |  `<class 'dict'>`  |  
|  `responses`  |  `Dict[str, str]`  |  Query id -> response.  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/evaluation/dataset_generation.py`  
| 
```
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
```
 | 
```
@deprecated(
    "Deprecated in favor of `LabelledRagDataset` which should be used instead.",
    action="always",
)
classQueryResponseDataset(BaseModel):
"""
    Query Response Dataset.

    The response can be empty if the dataset is generated from documents.

    Args:
        queries (Dict[str, str]): Query id -> query.
        responses (Dict[str, str]): Query id -> response.

    """

    queries: Dict[str, str] = Field(
        default_factory=dict, description="Query id -> query"
    )
    responses: Dict[str, str] = Field(
        default_factory=dict, description="Query id -> response"
    )

    @classmethod
    deffrom_qr_pairs(
        cls,
        qr_pairs: List[Tuple[str, str]],
    ) -> QueryResponseDataset:
"""Create from qr pairs."""
        # define ids as simple integers
        queries = {str(idx): query for idx, (query, _) in enumerate(qr_pairs)}
        responses = {str(idx): response for idx, (_, response) in enumerate(qr_pairs)}
        return cls(queries=queries, responses=responses)

    @property
    defqr_pairs(self) -> List[Tuple[str, str]]:
"""Get pairs."""
        # if query_id not in response, throw error
        for query_id in self.queries:
            if query_id not in self.responses:
                raise ValueError(f"Query id {query_id} not in responses")

        return [
            (self.queries[query_id], self.responses[query_id])
            for query_id in self.queries
        ]

    @property
    defquestions(self) -> List[str]:
"""Get questions."""
        return list(self.queries.values())

    defsave_json(self, path: str) -> None:
"""Save json."""
        with open(path, "w") as f:
            json.dump(self.model_dump(), f, indent=4)

    @classmethod
    deffrom_json(cls, path: str) -> QueryResponseDataset:
"""Load json."""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)

```
 |  
| --- | --- |  
###  qr_pairs `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.QueryResponseDataset.qr_pairs "Permanent link")

```
qr_pairs: [Tuple[, ]]

```

Get pairs.
###  questions `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.QueryResponseDataset.questions "Permanent link")

```
questions: []

```

Get questions.
###  from_qr_pairs `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.QueryResponseDataset.from_qr_pairs "Permanent link")

```
from_qr_pairs(
    qr_pairs: [Tuple[, ]]
) -> 

```

Create from qr pairs.
Source code in `llama-index-core/llama_index/core/evaluation/dataset_generation.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_qr_pairs(
    cls,
    qr_pairs: List[Tuple[str, str]],
) -> QueryResponseDataset:
"""Create from qr pairs."""
    # define ids as simple integers
    queries = {str(idx): query for idx, (query, _) in enumerate(qr_pairs)}
    responses = {str(idx): response for idx, (_, response) in enumerate(qr_pairs)}
    return cls(queries=queries, responses=responses)

```
 |  
| --- | --- |  
###  save_json [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.QueryResponseDataset.save_json "Permanent link")

```
save_json(path: ) -> None

```

Save json.
Source code in `llama-index-core/llama_index/core/evaluation/dataset_generation.py`  
| 
```
100
101
102
103
```
 | 
```
defsave_json(self, path: str) -> None:
"""Save json."""
    with open(path, "w") as f:
        json.dump(self.model_dump(), f, indent=4)

```
 |  
| --- | --- |  
###  from_json `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.QueryResponseDataset.from_json "Permanent link")

```
from_json(path: ) -> 

```

Load json.
Source code in `llama-index-core/llama_index/core/evaluation/dataset_generation.py`  
| 
```
105
106
107
108
109
110
```
 | 
```
@classmethod
deffrom_json(cls, path: str) -> QueryResponseDataset:
"""Load json."""
    with open(path) as f:
        data = json.load(f)
    return cls(**data)

```
 |  
| --- | --- |  
##  FaithfulnessEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.FaithfulnessEvaluator "Permanent link")
Bases: 
Faithfulness evaluator.
Evaluates whether a response is faithful to the contexts (i.e. whether the response is supported by the contexts or hallucinated.)
This evaluator only considers the response string and the list of context strings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `raise_error`  |  `bool`  |  Whether to raise an error when the response is invalid. Defaults to False.  |  `False`  |  
|  `eval_template`  |  `Optional[Union[str, BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]]`  |  The template to use for evaluation.  |  `None`  |  
|  `refine_template`  |  `Optional[Union[str, BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]]`  |  The template to use for refining the evaluation.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/evaluation/faithfulness.py`  
| 
```
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
```
 | 
```
classFaithfulnessEvaluator(BaseEvaluator):
"""
    Faithfulness evaluator.

    Evaluates whether a response is faithful to the contexts
    (i.e. whether the response is supported by the contexts or hallucinated.)

    This evaluator only considers the response string and the list of context strings.

    Args:
        raise_error(bool): Whether to raise an error when the response is invalid.
            Defaults to False.
        eval_template(Optional[Union[str, BasePromptTemplate]]):
            The template to use for evaluation.
        refine_template(Optional[Union[str, BasePromptTemplate]]):
            The template to use for refining the evaluation.

    """

    def__init__(
        self,
        llm: Optional[LLM] = None,
        raise_error: bool = False,
        eval_template: Optional[Union[str, BasePromptTemplate]] = None,
        refine_template: Optional[Union[str, BasePromptTemplate]] = None,
    ) -> None:
"""Init params."""
        self._llm = llm or Settings.llm
        self._raise_error = raise_error

        self._eval_template: BasePromptTemplate
        if isinstance(eval_template, str):
            self._eval_template = PromptTemplate(eval_template)
        if isinstance(eval_template, BasePromptTemplate):
            self._eval_template = eval_template
        else:
            model_name = self._llm.metadata.model_name
            self._eval_template = TEMPLATES_CATALOG.get(
                model_name, DEFAULT_EVAL_TEMPLATE
            )

        self._refine_template: BasePromptTemplate
        if isinstance(refine_template, str):
            self._refine_template = PromptTemplate(refine_template)
        else:
            self._refine_template = refine_template or DEFAULT_REFINE_TEMPLATE

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {
            "eval_template": self._eval_template,
            "refine_template": self._refine_template,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "eval_template" in prompts:
            self._eval_template = prompts["eval_template"]
        if "refine_template" in prompts:
            self._refine_template = prompts["refine_template"]

    async defaevaluate(
        self,
        query: str | None = None,
        response: str | None = None,
        contexts: Sequence[str] | None = None,
        sleep_time_in_seconds: int = 0,
        **kwargs: Any,
    ) -> EvaluationResult:
"""Evaluate whether the response is faithful to the contexts."""
        del kwargs  # Unused

        await asyncio.sleep(sleep_time_in_seconds)

        if contexts is None or response is None:
            raise ValueError("contexts and response must be provided")

        docs = [Document(text=context) for context in contexts]
        index = SummaryIndex.from_documents(docs)

        query_engine = index.as_query_engine(
            llm=self._llm,
            text_qa_template=self._eval_template,
            refine_template=self._refine_template,
        )
        response_obj = await query_engine.aquery(response)

        raw_response_txt = str(response_obj)

        if "yes" in raw_response_txt.lower():
            passing = True
        else:
            passing = False
            if self._raise_error:
                raise ValueError("The response is invalid")

        return EvaluationResult(
            query=query,
            response=response,
            contexts=contexts,
            passing=passing,
            score=1.0 if passing else 0.0,
            feedback=raw_response_txt,
        )

```
 |  
| --- | --- |  
###  aevaluate [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.FaithfulnessEvaluator.aevaluate "Permanent link")

```
aevaluate(
    query:  | None = None,
    response:  | None = None,
    contexts: Sequence[] | None = None,
    sleep_time_in_seconds:  = 0,
    **kwargs: 
) -> 

```

Evaluate whether the response is faithful to the contexts.
Source code in `llama-index-core/llama_index/core/evaluation/faithfulness.py`  
| 
```
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
```
 | 
```
async defaevaluate(
    self,
    query: str | None = None,
    response: str | None = None,
    contexts: Sequence[str] | None = None,
    sleep_time_in_seconds: int = 0,
    **kwargs: Any,
) -> EvaluationResult:
"""Evaluate whether the response is faithful to the contexts."""
    del kwargs  # Unused

    await asyncio.sleep(sleep_time_in_seconds)

    if contexts is None or response is None:
        raise ValueError("contexts and response must be provided")

    docs = [Document(text=context) for context in contexts]
    index = SummaryIndex.from_documents(docs)

    query_engine = index.as_query_engine(
        llm=self._llm,
        text_qa_template=self._eval_template,
        refine_template=self._refine_template,
    )
    response_obj = await query_engine.aquery(response)

    raw_response_txt = str(response_obj)

    if "yes" in raw_response_txt.lower():
        passing = True
    else:
        passing = False
        if self._raise_error:
            raise ValueError("The response is invalid")

    return EvaluationResult(
        query=query,
        response=response,
        contexts=contexts,
        passing=passing,
        score=1.0 if passing else 0.0,
        feedback=raw_response_txt,
    )

```
 |  
| --- | --- |  
##  GuidelineEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.GuidelineEvaluator "Permanent link")
Bases: 
Guideline evaluator.
Evaluates whether a query and response pair passes the given guidelines.
This evaluator only considers the query string and the response string.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `guidelines`  |  `Optional[str]`  |  User-added guidelines to use for evaluation. Defaults to None, which uses the default guidelines.  |  `None`  |  
|  `eval_template`  |  `Optional[Union[str, BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]]`  |  The template to use for evaluation.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/evaluation/guideline.py`  
| 
```
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
```
 | 
```
classGuidelineEvaluator(BaseEvaluator):
"""
    Guideline evaluator.

    Evaluates whether a query and response pair passes the given guidelines.

    This evaluator only considers the query string and the response string.

    Args:
        guidelines(Optional[str]): User-added guidelines to use for evaluation.
            Defaults to None, which uses the default guidelines.
        eval_template(Optional[Union[str, BasePromptTemplate]] ):
            The template to use for evaluation.

    """

    def__init__(
        self,
        llm: Optional[LLM] = None,
        guidelines: Optional[str] = None,
        eval_template: Optional[Union[str, BasePromptTemplate]] = None,
        output_parser: Optional[PydanticOutputParser] = None,
    ) -> None:
        self._llm = llm or Settings.llm
        self._guidelines = guidelines or DEFAULT_GUIDELINES

        self._eval_template: BasePromptTemplate
        if isinstance(eval_template, str):
            self._eval_template = PromptTemplate(eval_template)
        else:
            self._eval_template = eval_template or DEFAULT_EVAL_TEMPLATE

        self._output_parser = output_parser or PydanticOutputParser(
            output_cls=EvaluationData
        )
        self._eval_template.output_parser = self._output_parser

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {
            "eval_template": self._eval_template,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "eval_template" in prompts:
            self._eval_template = prompts["eval_template"]

    async defaevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        sleep_time_in_seconds: int = 0,
        **kwargs: Any,
    ) -> EvaluationResult:
"""Evaluate whether the query and response pair passes the guidelines."""
        del contexts  # Unused
        del kwargs  # Unused
        if query is None or response is None:
            raise ValueError("query and response must be provided")

        logger.debug("prompt: %s", self._eval_template)
        logger.debug("query: %s", query)
        logger.debug("response: %s", response)
        logger.debug("guidelines: %s", self._guidelines)

        await asyncio.sleep(sleep_time_in_seconds)

        eval_response = await self._llm.apredict(
            self._eval_template,
            query=query,
            response=response,
            guidelines=self._guidelines,
        )
        eval_data = self._output_parser.parse(eval_response)
        eval_data = cast(EvaluationData, eval_data)

        return EvaluationResult(
            query=query,
            response=response,
            passing=eval_data.passing,
            score=1.0 if eval_data.passing else 0.0,
            feedback=eval_data.feedback,
        )

```
 |  
| --- | --- |  
###  aevaluate [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.GuidelineEvaluator.aevaluate "Permanent link")

```
aevaluate(
    query: Optional[] = None,
    response: Optional[] = None,
    contexts: Optional[Sequence[]] = None,
    sleep_time_in_seconds:  = 0,
    **kwargs: 
) -> 

```

Evaluate whether the query and response pair passes the guidelines.
Source code in `llama-index-core/llama_index/core/evaluation/guideline.py`  
| 
```
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
```
 | 
```
async defaevaluate(
    self,
    query: Optional[str] = None,
    response: Optional[str] = None,
    contexts: Optional[Sequence[str]] = None,
    sleep_time_in_seconds: int = 0,
    **kwargs: Any,
) -> EvaluationResult:
"""Evaluate whether the query and response pair passes the guidelines."""
    del contexts  # Unused
    del kwargs  # Unused
    if query is None or response is None:
        raise ValueError("query and response must be provided")

    logger.debug("prompt: %s", self._eval_template)
    logger.debug("query: %s", query)
    logger.debug("response: %s", response)
    logger.debug("guidelines: %s", self._guidelines)

    await asyncio.sleep(sleep_time_in_seconds)

    eval_response = await self._llm.apredict(
        self._eval_template,
        query=query,
        response=response,
        guidelines=self._guidelines,
    )
    eval_data = self._output_parser.parse(eval_response)
    eval_data = cast(EvaluationData, eval_data)

    return EvaluationResult(
        query=query,
        response=response,
        passing=eval_data.passing,
        score=1.0 if eval_data.passing else 0.0,
        feedback=eval_data.feedback,
    )

```
 |  
| --- | --- |  
##  PairwiseComparisonEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.PairwiseComparisonEvaluator "Permanent link")
Bases: 
Pairwise comparison evaluator.
Evaluates the quality of a response vs. a "reference" response given a question by having an LLM judge which response is better.
Outputs whether the `response` given is better than the `reference` response.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `eval_template`  |  `Optional[Union[str, BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]]`  |  The template to use for evaluation.  |  `None`  |  
|  `enforce_consensus`  |  `bool`  |  Whether to enforce consensus (consistency if we flip the order of the answers). Defaults to True.  |  `True`  |  
Source code in `llama-index-core/llama_index/core/evaluation/pairwise.py`  
| 
```
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
```
 | 
```
classPairwiseComparisonEvaluator(BaseEvaluator):
"""
    Pairwise comparison evaluator.

    Evaluates the quality of a response vs. a "reference" response given a question by
    having an LLM judge which response is better.

    Outputs whether the `response` given is better than the `reference` response.

    Args:
        eval_template (Optional[Union[str, BasePromptTemplate]]):
            The template to use for evaluation.
        enforce_consensus (bool): Whether to enforce consensus (consistency if we
            flip the order of the answers). Defaults to True.

    """

    def__init__(
        self,
        llm: Optional[LLM] = None,
        eval_template: Optional[Union[BasePromptTemplate, str]] = None,
        parser_function: Callable[
            [str], Tuple[Optional[bool], Optional[float], Optional[str]]
        ] = _default_parser_function,
        enforce_consensus: bool = True,
    ) -> None:
        self._llm = llm or Settings.llm

        self._eval_template: BasePromptTemplate
        if isinstance(eval_template, str):
            self._eval_template = PromptTemplate(eval_template)
        else:
            self._eval_template = eval_template or DEFAULT_EVAL_TEMPLATE

        self._enforce_consensus = enforce_consensus
        self._parser_function = parser_function

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {
            "eval_template": self._eval_template,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "eval_template" in prompts:
            self._eval_template = prompts["eval_template"]

    async def_get_eval_result(
        self,
        query: str,
        response: str,
        second_response: str,
        reference: Optional[str],
    ) -> EvaluationResult:
"""Get evaluation result."""
        eval_response = await self._llm.apredict(
            prompt=self._eval_template,
            query=query,
            answer_1=response,
            answer_2=second_response,
            reference=reference or "",
        )

        # Extract from response
        passing, score, feedback = self._parser_function(eval_response)

        if passing is None and score is None and feedback is None:
            return EvaluationResult(
                query=query,
                invalid_result=True,
                invalid_reason="Output cannot be parsed",
                feedback=eval_response,
            )
        else:
            return EvaluationResult(
                query=query,
                response=eval_response,
                passing=passing,
                score=score,
                feedback=eval_response,
                pairwise_source=EvaluationSource.ORIGINAL,
            )

    async def_resolve_results(
        self,
        eval_result: EvaluationResult,
        flipped_eval_result: EvaluationResult,
    ) -> EvaluationResult:
"""
        Resolve eval results from evaluation + flipped evaluation.

        Args:
            eval_result (EvaluationResult): Result when answer_1 is shown first
            flipped_eval_result (EvaluationResult): Result when answer_2 is shown first

        Returns:
            EvaluationResult: The final evaluation result

        """
        # add pairwise_source to eval_result and flipped_eval_result
        eval_result.pairwise_source = EvaluationSource.ORIGINAL
        flipped_eval_result.pairwise_source = EvaluationSource.FLIPPED

        # count the votes for each of the 2 answers
        votes_1 = 0.0
        votes_2 = 0.0
        if eval_result.score is not None and flipped_eval_result.score is not None:
            votes_1 = eval_result.score + (1 - flipped_eval_result.score)
            votes_2 = (1 - eval_result.score) + flipped_eval_result.score

        if votes_1 + votes_2 != 2:  # each round, the judge can give a total of 1 vote
            raise ValueError("Impossible score results. Total amount of votes is 2.")

        # get the judges (original and flipped) who voted for answer_1
        voters_1 = [eval_result] * (eval_result.score == 1.0) + [
            flipped_eval_result
        ] * (flipped_eval_result.score == 0.0)

        # get the judges (original and flipped) who voted for answer_2
        voters_2 = [eval_result] * (eval_result.score == 0.0) + [
            flipped_eval_result
        ] * (flipped_eval_result.score == 1.0)

        if votes_1  votes_2:
            return voters_1[0]  # return any voter for answer_1
        elif votes_2  votes_1:
            return voters_2[0]  # return any vote for answer_2
        else:
            if (
                eval_result.score == 0.5
            ):  # votes_1 == votes_2 can only happen if both are 1.0 (so actual tie)
                # doesn't matter which one we return here
                return eval_result
            else:  # Inconclusive case!
                return EvaluationResult(
                    query=eval_result.query,
                    response="",
                    passing=None,
                    score=0.5,
                    feedback="",
                    pairwise_source=EvaluationSource.NEITHER,
                )

    async defaevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        second_response: Optional[str] = None,
        reference: Optional[str] = None,
        sleep_time_in_seconds: int = 0,
        **kwargs: Any,
    ) -> EvaluationResult:
        del kwargs  # Unused
        del contexts  # Unused

        if query is None or response is None or second_response is None:
            raise ValueError(
                "query, response, second_response, and reference must be provided"
            )

        await asyncio.sleep(sleep_time_in_seconds)

        eval_result = await self._get_eval_result(
            query, response, second_response, reference
        )
        if self._enforce_consensus and not eval_result.invalid_result:
            # Flip the order of the answers and see if the answer is consistent
            # (which means that the score should flip from 0 to 1 and vice-versa)
            # if not, then we return a tie
            flipped_eval_result = await self._get_eval_result(
                query, second_response, response, reference
            )
            if not flipped_eval_result.invalid_result:
                resolved_eval_result = await self._resolve_results(
                    eval_result, flipped_eval_result
                )
            else:
                resolved_eval_result = EvaluationResult(
                    query=eval_result.query,
                    response=eval_result.response,
                    feedback=flipped_eval_result.response,
                    invalid_result=True,
                    invalid_reason="Output cannot be parsed.",
                )
        else:
            resolved_eval_result = eval_result

        return resolved_eval_result

```
 |  
| --- | --- |  
##  RelevancyEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.RelevancyEvaluator "Permanent link")
Bases: 
Relenvancy evaluator.
Evaluates the relevancy of retrieved contexts and response to a query. This evaluator considers the query string, retrieved contexts, and response string.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `raise_error`  |  `Optional[bool]`  |  Whether to raise an error if the response is invalid. Defaults to False.  |  `False`  |  
|  `eval_template`  |  `Optional[Union[str, BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]]`  |  The template to use for evaluation.  |  `None`  |  
|  `refine_template`  |  `Optional[Union[str, BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]]`  |  The template to use for refinement.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/evaluation/relevancy.py`  
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
```
 | 
```
classRelevancyEvaluator(BaseEvaluator):
"""
    Relenvancy evaluator.

    Evaluates the relevancy of retrieved contexts and response to a query.
    This evaluator considers the query string, retrieved contexts, and response string.

    Args:
        raise_error(Optional[bool]):
            Whether to raise an error if the response is invalid.
            Defaults to False.
        eval_template(Optional[Union[str, BasePromptTemplate]]):
            The template to use for evaluation.
        refine_template(Optional[Union[str, BasePromptTemplate]]):
            The template to use for refinement.

    """

    def__init__(
        self,
        llm: Optional[LLM] = None,
        raise_error: bool = False,
        eval_template: Optional[Union[str, BasePromptTemplate]] = None,
        refine_template: Optional[Union[str, BasePromptTemplate]] = None,
    ) -> None:
"""Init params."""
        self._llm = llm or Settings.llm
        self._raise_error = raise_error

        self._eval_template: BasePromptTemplate
        if isinstance(eval_template, str):
            self._eval_template = PromptTemplate(eval_template)
        else:
            self._eval_template = eval_template or DEFAULT_EVAL_TEMPLATE

        self._refine_template: BasePromptTemplate
        if isinstance(refine_template, str):
            self._refine_template = PromptTemplate(refine_template)
        else:
            self._refine_template = refine_template or DEFAULT_REFINE_TEMPLATE

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {
            "eval_template": self._eval_template,
            "refine_template": self._refine_template,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "eval_template" in prompts:
            self._eval_template = prompts["eval_template"]
        if "refine_template" in prompts:
            self._refine_template = prompts["refine_template"]

    async defaevaluate(
        self,
        query: str | None = None,
        response: str | None = None,
        contexts: Sequence[str] | None = None,
        sleep_time_in_seconds: int = 0,
        **kwargs: Any,
    ) -> EvaluationResult:
"""Evaluate whether the contexts and response are relevant to the query."""
        del kwargs  # Unused

        if query is None or contexts is None or response is None:
            raise ValueError("query, contexts, and response must be provided")

        docs = [Document(text=context) for context in contexts]
        index = SummaryIndex.from_documents(docs)

        query_response = f"Question: {query}\nResponse: {response}"

        await asyncio.sleep(sleep_time_in_seconds)

        query_engine = index.as_query_engine(
            llm=self._llm,
            text_qa_template=self._eval_template,
            refine_template=self._refine_template,
        )
        response_obj = await query_engine.aquery(query_response)

        raw_response_txt = str(response_obj)

        if "yes" in raw_response_txt.lower():
            passing = True
        else:
            if self._raise_error:
                raise ValueError("The response is invalid")
            passing = False

        return EvaluationResult(
            query=query,
            response=response,
            passing=passing,
            score=1.0 if passing else 0.0,
            feedback=raw_response_txt,
            contexts=contexts,
        )

```
 |  
| --- | --- |  
###  aevaluate [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.RelevancyEvaluator.aevaluate "Permanent link")

```
aevaluate(
    query:  | None = None,
    response:  | None = None,
    contexts: Sequence[] | None = None,
    sleep_time_in_seconds:  = 0,
    **kwargs: 
) -> 

```

Evaluate whether the contexts and response are relevant to the query.
Source code in `llama-index-core/llama_index/core/evaluation/relevancy.py`  
| 
```
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
```
 | 
```
async defaevaluate(
    self,
    query: str | None = None,
    response: str | None = None,
    contexts: Sequence[str] | None = None,
    sleep_time_in_seconds: int = 0,
    **kwargs: Any,
) -> EvaluationResult:
"""Evaluate whether the contexts and response are relevant to the query."""
    del kwargs  # Unused

    if query is None or contexts is None or response is None:
        raise ValueError("query, contexts, and response must be provided")

    docs = [Document(text=context) for context in contexts]
    index = SummaryIndex.from_documents(docs)

    query_response = f"Question: {query}\nResponse: {response}"

    await asyncio.sleep(sleep_time_in_seconds)

    query_engine = index.as_query_engine(
        llm=self._llm,
        text_qa_template=self._eval_template,
        refine_template=self._refine_template,
    )
    response_obj = await query_engine.aquery(query_response)

    raw_response_txt = str(response_obj)

    if "yes" in raw_response_txt.lower():
        passing = True
    else:
        if self._raise_error:
            raise ValueError("The response is invalid")
        passing = False

    return EvaluationResult(
        query=query,
        response=response,
        passing=passing,
        score=1.0 if passing else 0.0,
        feedback=raw_response_txt,
        contexts=contexts,
    )

```
 |  
| --- | --- |  
##  BaseRetrievalEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseRetrievalEvaluator "Permanent link")
Bases: `BaseModel`
Base Retrieval Evaluator class.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `metrics`  |  `List[BaseRetrievalMetric]`  |  List of metrics to evaluate  |  _required_  |  
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/base.py`  
| 
```
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
```
 | 
```
classBaseRetrievalEvaluator(BaseModel):
"""Base Retrieval Evaluator class."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    metrics: List[BaseRetrievalMetric] = Field(
        ..., description="List of metrics to evaluate"
    )

    @classmethod
    deffrom_metric_names(
        cls, metric_names: List[str], **kwargs: Any
    ) -> "BaseRetrievalEvaluator":
"""
        Create evaluator from metric names.

        Args:
            metric_names (List[str]): List of metric names
            **kwargs: Additional arguments for the evaluator

        """
        metric_types = resolve_metrics(metric_names)
        return cls(metrics=[metric() for metric in metric_types], **kwargs)

    @abstractmethod
    async def_aget_retrieved_ids_and_texts(
        self, query: str, mode: RetrievalEvalMode = RetrievalEvalMode.TEXT
    ) -> Tuple[List[str], List[str]]:
"""Get retrieved ids and texts."""
        raise NotImplementedError

    defevaluate(
        self,
        query: str,
        expected_ids: List[str],
        expected_texts: Optional[List[str]] = None,
        mode: RetrievalEvalMode = RetrievalEvalMode.TEXT,
        **kwargs: Any,
    ) -> RetrievalEvalResult:
"""
        Run evaluation results with query string and expected ids.

        Args:
            query (str): Query string
            expected_ids (List[str]): Expected ids

        Returns:
            RetrievalEvalResult: Evaluation result

        """
        return asyncio_run(
            self.aevaluate(
                query=query,
                expected_ids=expected_ids,
                expected_texts=expected_texts,
                mode=mode,
                **kwargs,
            )
        )

    # @abstractmethod
    async defaevaluate(
        self,
        query: str,
        expected_ids: List[str],
        expected_texts: Optional[List[str]] = None,
        mode: RetrievalEvalMode = RetrievalEvalMode.TEXT,
        **kwargs: Any,
    ) -> RetrievalEvalResult:
"""
        Run evaluation with query string, retrieved contexts,
        and generated response string.

        Subclasses can override this method to provide custom evaluation logic and
        take in additional arguments.
        """
        retrieved_ids, retrieved_texts = await self._aget_retrieved_ids_and_texts(
            query, mode
        )
        metric_dict = {}
        for metric in self.metrics:
            eval_result = metric.compute(
                query, expected_ids, retrieved_ids, expected_texts, retrieved_texts
            )
            metric_dict[metric.metric_name] = eval_result

        return RetrievalEvalResult(
            query=query,
            expected_ids=expected_ids,
            expected_texts=expected_texts,
            retrieved_ids=retrieved_ids,
            retrieved_texts=retrieved_texts,
            mode=mode,
            metric_dict=metric_dict,
        )

    async defaevaluate_dataset(
        self,
        dataset: EmbeddingQAFinetuneDataset,
        workers: int = 2,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[RetrievalEvalResult]:
"""Run evaluation with dataset."""
        semaphore = asyncio.Semaphore(workers)

        async defeval_worker(
            query: str, expected_ids: List[str], mode: RetrievalEvalMode
        ) -> RetrievalEvalResult:
            async with semaphore:
                return await self.aevaluate(query, expected_ids=expected_ids, mode=mode)

        response_jobs = []
        mode = RetrievalEvalMode.from_str(dataset.mode)
        for query_id, query in dataset.queries.items():
            expected_ids = dataset.relevant_docs[query_id]
            response_jobs.append(eval_worker(query, expected_ids, mode))
        if show_progress:
            fromtqdm.asyncioimport tqdm_asyncio

            eval_results = await tqdm_asyncio.gather(*response_jobs)
        else:
            eval_results = await asyncio.gather(*response_jobs)

        return eval_results

```
 |  
| --- | --- |  
###  from_metric_names `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseRetrievalEvaluator.from_metric_names "Permanent link")

```
from_metric_names(
    metric_names: [], **kwargs: 
) -> 

```

Create evaluator from metric names.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `metric_names`  |  `List[str]`  |  List of metric names  |  _required_  |  
|  `**kwargs`  |  Additional arguments for the evaluator  |  
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/base.py`  
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
```
 | 
```
@classmethod
deffrom_metric_names(
    cls, metric_names: List[str], **kwargs: Any
) -> "BaseRetrievalEvaluator":
"""
    Create evaluator from metric names.

    Args:
        metric_names (List[str]): List of metric names
        **kwargs: Additional arguments for the evaluator

    """
    metric_types = resolve_metrics(metric_names)
    return cls(metrics=[metric() for metric in metric_types], **kwargs)

```
 |  
| --- | --- |  
###  evaluate [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseRetrievalEvaluator.evaluate "Permanent link")

```
evaluate(
    query: ,
    expected_ids: [],
    expected_texts: Optional[[]] = None,
    mode: RetrievalEvalMode = ,
    **kwargs: 
) -> 

```

Run evaluation results with query string and expected ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query string  |  _required_  |  
|  `expected_ids`  |  `List[str]`  |  Expected ids  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `RetrievalEvalResult`  |   |  Evaluation result  |  
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/base.py`  
| 
```
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
```
 | 
```
defevaluate(
    self,
    query: str,
    expected_ids: List[str],
    expected_texts: Optional[List[str]] = None,
    mode: RetrievalEvalMode = RetrievalEvalMode.TEXT,
    **kwargs: Any,
) -> RetrievalEvalResult:
"""
    Run evaluation results with query string and expected ids.

    Args:
        query (str): Query string
        expected_ids (List[str]): Expected ids

    Returns:
        RetrievalEvalResult: Evaluation result

    """
    return asyncio_run(
        self.aevaluate(
            query=query,
            expected_ids=expected_ids,
            expected_texts=expected_texts,
            mode=mode,
            **kwargs,
        )
    )

```
 |  
| --- | --- |  
###  aevaluate [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseRetrievalEvaluator.aevaluate "Permanent link")

```
aevaluate(
    query: ,
    expected_ids: [],
    expected_texts: Optional[[]] = None,
    mode: RetrievalEvalMode = ,
    **kwargs: 
) -> 

```

Run evaluation with query string, retrieved contexts, and generated response string.
Subclasses can override this method to provide custom evaluation logic and take in additional arguments.
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/base.py`  
| 
```
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
```
 | 
```
async defaevaluate(
    self,
    query: str,
    expected_ids: List[str],
    expected_texts: Optional[List[str]] = None,
    mode: RetrievalEvalMode = RetrievalEvalMode.TEXT,
    **kwargs: Any,
) -> RetrievalEvalResult:
"""
    Run evaluation with query string, retrieved contexts,
    and generated response string.

    Subclasses can override this method to provide custom evaluation logic and
    take in additional arguments.
    """
    retrieved_ids, retrieved_texts = await self._aget_retrieved_ids_and_texts(
        query, mode
    )
    metric_dict = {}
    for metric in self.metrics:
        eval_result = metric.compute(
            query, expected_ids, retrieved_ids, expected_texts, retrieved_texts
        )
        metric_dict[metric.metric_name] = eval_result

    return RetrievalEvalResult(
        query=query,
        expected_ids=expected_ids,
        expected_texts=expected_texts,
        retrieved_ids=retrieved_ids,
        retrieved_texts=retrieved_texts,
        mode=mode,
        metric_dict=metric_dict,
    )

```
 |  
| --- | --- |  
###  aevaluate_dataset [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseRetrievalEvaluator.aevaluate_dataset "Permanent link")

```
aevaluate_dataset(
    dataset: ,
    workers:  = 2,
    show_progress:  = False,
    **kwargs: 
) -> []

```

Run evaluation with dataset.
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/base.py`  
| 
```
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
```
 | 
```
async defaevaluate_dataset(
    self,
    dataset: EmbeddingQAFinetuneDataset,
    workers: int = 2,
    show_progress: bool = False,
    **kwargs: Any,
) -> List[RetrievalEvalResult]:
"""Run evaluation with dataset."""
    semaphore = asyncio.Semaphore(workers)

    async defeval_worker(
        query: str, expected_ids: List[str], mode: RetrievalEvalMode
    ) -> RetrievalEvalResult:
        async with semaphore:
            return await self.aevaluate(query, expected_ids=expected_ids, mode=mode)

    response_jobs = []
    mode = RetrievalEvalMode.from_str(dataset.mode)
    for query_id, query in dataset.queries.items():
        expected_ids = dataset.relevant_docs[query_id]
        response_jobs.append(eval_worker(query, expected_ids, mode))
    if show_progress:
        fromtqdm.asyncioimport tqdm_asyncio

        eval_results = await tqdm_asyncio.gather(*response_jobs)
    else:
        eval_results = await asyncio.gather(*response_jobs)

    return eval_results

```
 |  
| --- | --- |  
##  RetrievalEvalResult [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.RetrievalEvalResult "Permanent link")
Bases: `BaseModel`
Retrieval eval result.
NOTE: this abstraction might change in the future.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query string  |  _required_  |  
|  `expected_ids`  |  `List[str]`  |  Expected ids  |  _required_  |  
|  `expected_texts`  |  `List[str] | None`  |  Expected texts associated with nodes provided in `expected_ids`  |  `None`  |  
|  `retrieved_ids`  |  `List[str]`  |  Retrieved ids  |  _required_  |  
|  `retrieved_texts`  |  `List[str]`  |  Retrieved texts  |  _required_  |  
|  `mode`  |  `RetrievalEvalMode`  |  text or image  |  `<RetrievalEvalMode.TEXT: 'text'>`  |  
|  `metric_dict`  |  `Dict[str, RetrievalMetricResult[](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.RetrievalMetricResult "RetrievalMetricResult \(llama_index.core.evaluation.retrieval.metrics_base.RetrievalMetricResult\)")]`  |  Metric dictionary for the evaluation  |  _required_  |  
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/base.py`  
| 
```
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
```
 | 
```
classRetrievalEvalResult(BaseModel):
"""
    Retrieval eval result.

    NOTE: this abstraction might change in the future.

    Attributes:
        query (str): Query string
        expected_ids (List[str]): Expected ids
        retrieved_ids (List[str]): Retrieved ids
        metric_dict (Dict[str, BaseRetrievalMetric]): \
            Metric dictionary for the evaluation

    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    query: str = Field(..., description="Query string")
    expected_ids: List[str] = Field(..., description="Expected ids")
    expected_texts: Optional[List[str]] = Field(
        default=None,
        description="Expected texts associated with nodes provided in `expected_ids`",
    )
    retrieved_ids: List[str] = Field(..., description="Retrieved ids")
    retrieved_texts: List[str] = Field(..., description="Retrieved texts")
    mode: "RetrievalEvalMode" = Field(
        default=RetrievalEvalMode.TEXT, description="text or image"
    )
    metric_dict: Dict[str, RetrievalMetricResult] = Field(
        ..., description="Metric dictionary for the evaluation"
    )

    @property
    defmetric_vals_dict(self) -> Dict[str, float]:
"""Dictionary of metric values."""
        return {k: v.score for k, v in self.metric_dict.items()}

    def__str__(self) -> str:
"""String representation."""
        return f"Query: {self.query}\nMetrics: {self.metric_vals_dict!s}\n"

```
 |  
| --- | --- |  
###  metric_vals_dict `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.RetrievalEvalResult.metric_vals_dict "Permanent link")

```
metric_vals_dict: [, float]

```

Dictionary of metric values.
##  MultiModalRetrieverEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.MultiModalRetrieverEvaluator "Permanent link")
Bases: 
Retriever evaluator.
This module will evaluate a retriever using a set of metrics.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `metrics`  |  `List[BaseRetrievalMetric]`  |  Sequence of metrics to evaluate  |  _required_  |  
|  `retriever`  |   |  Retriever to evaluate.  |  _required_  |  
|  `node_postprocessors`  |  `List[Annotated[BaseNodePostprocessor[](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/#llama_index.core.postprocessor.types.BaseNodePostprocessor "BaseNodePostprocessor \(llama_index.core.postprocessor.types.BaseNodePostprocessor\)"), SerializeAsAny]] | None`  |  Post-processor to apply after retrieval.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/evaluator.py`  
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
```
 | 
```
classMultiModalRetrieverEvaluator(BaseRetrievalEvaluator):
"""
    Retriever evaluator.

    This module will evaluate a retriever using a set of metrics.

    Args:
        metrics (List[BaseRetrievalMetric]): Sequence of metrics to evaluate
        retriever: Retriever to evaluate.
        node_postprocessors (Optional[List[BaseNodePostprocessor]]): Post-processor to apply after retrieval.

    """

    retriever: BaseRetriever = Field(..., description="Retriever to evaluate")
    node_postprocessors: Optional[List[SerializeAsAny[BaseNodePostprocessor]]] = Field(
        default=None, description="Optional post-processor"
    )

    async def_aget_retrieved_ids_and_texts(
        self, query: str, mode: RetrievalEvalMode = RetrievalEvalMode.TEXT
    ) -> Tuple[List[str], List[str]]:
"""Get retrieved ids."""
        retrieved_nodes = await self.retriever.aretrieve(query)
        image_nodes: List[ImageNode] = []
        text_nodes: List[TextNode] = []

        if self.node_postprocessors:
            for node_postprocessor in self.node_postprocessors:
                retrieved_nodes = node_postprocessor.postprocess_nodes(
                    retrieved_nodes, query_str=query
                )

        for scored_node in retrieved_nodes:
            node = scored_node.node
            if isinstance(node, ImageNode):
                image_nodes.append(node)
            if isinstance(node, TextNode):
                text_nodes.append(node)

        if mode == "text":
            return (
                [node.node_id for node in text_nodes],
                [node.text for node in text_nodes],
            )
        elif mode == "image":
            return (
                [node.node_id for node in image_nodes],
                [node.text for node in image_nodes],
            )
        else:
            raise ValueError("Unsupported mode.")

```
 |  
| --- | --- |  
##  RetrieverEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.RetrieverEvaluator "Permanent link")
Bases: 
Retriever evaluator.
This module will evaluate a retriever using a set of metrics.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `metrics`  |  `List[BaseRetrievalMetric]`  |  Sequence of metrics to evaluate  |  _required_  |  
|  `retriever`  |   |  Retriever to evaluate.  |  _required_  |  
|  `node_postprocessors`  |  `List[Annotated[BaseNodePostprocessor[](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/#llama_index.core.postprocessor.types.BaseNodePostprocessor "BaseNodePostprocessor \(llama_index.core.postprocessor.types.BaseNodePostprocessor\)"), SerializeAsAny]] | None`  |  Post-processor to apply after retrieval.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/evaluator.py`  
| 
```
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
```
 | 
```
classRetrieverEvaluator(BaseRetrievalEvaluator):
"""
    Retriever evaluator.

    This module will evaluate a retriever using a set of metrics.

    Args:
        metrics (List[BaseRetrievalMetric]): Sequence of metrics to evaluate
        retriever: Retriever to evaluate.
        node_postprocessors (Optional[List[BaseNodePostprocessor]]): Post-processor to apply after retrieval.


    """

    retriever: BaseRetriever = Field(..., description="Retriever to evaluate")
    node_postprocessors: Optional[List[SerializeAsAny[BaseNodePostprocessor]]] = Field(
        default=None, description="Optional post-processor"
    )

    async def_aget_retrieved_ids_and_texts(
        self, query: str, mode: RetrievalEvalMode = RetrievalEvalMode.TEXT
    ) -> Tuple[List[str], List[str]]:
"""Get retrieved ids and texts, potentially applying a post-processor."""
        retrieved_nodes = await self.retriever.aretrieve(query)

        if self.node_postprocessors:
            for node_postprocessor in self.node_postprocessors:
                retrieved_nodes = node_postprocessor.postprocess_nodes(
                    retrieved_nodes, query_str=query
                )

        return (
            [node.node.node_id for node in retrieved_nodes],
            [node.text for node in retrieved_nodes],
        )

```
 |  
| --- | --- |  
##  MRR [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.MRR "Permanent link")
Bases: `BaseRetrievalMetric`
MRR (Mean Reciprocal Rank) metric with two calculation options.
  * The default method calculates the reciprocal rank of the first relevant retrieved document.
  * The more granular method sums the reciprocal ranks of all relevant retrieved documents and divides by the count of relevant documents.


Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `metric_name`  |  The name of the metric.  |  
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `use_granular_mrr`  |  `bool`  |  `False`  |  
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/metrics.py`  
| 
```
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
```
 | 
```
classMRR(BaseRetrievalMetric):
"""
    MRR (Mean Reciprocal Rank) metric with two calculation options.

    - The default method calculates the reciprocal rank of the first relevant retrieved document.
    - The more granular method sums the reciprocal ranks of all relevant retrieved documents and divides by the count of relevant documents.

    Attributes:
        metric_name (str): The name of the metric.
        use_granular_mrr (bool): Determines whether to use the granular method for calculation.

    """

    metric_name: ClassVar[str] = "mrr"
    use_granular_mrr: bool = False

    defcompute(
        self,
        query: Optional[str] = None,
        expected_ids: Optional[List[str]] = None,
        retrieved_ids: Optional[List[str]] = None,
        expected_texts: Optional[List[str]] = None,
        retrieved_texts: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> RetrievalMetricResult:
"""
        Compute MRR based on the provided inputs and selected method.

        Parameters
        ----------
            query (Optional[str]): The query string (not used in the current implementation).
            expected_ids (Optional[List[str]]): Expected document IDs.
            retrieved_ids (Optional[List[str]]): Retrieved document IDs.
            expected_texts (Optional[List[str]]): Expected texts (not used in the current implementation).
            retrieved_texts (Optional[List[str]]): Retrieved texts (not used in the current implementation).

        Raises
        ------
            ValueError: If the necessary IDs are not provided.

        Returns
        -------
            RetrievalMetricResult: The result with the computed MRR score.

        """
        # Checking for the required arguments
        if (
            retrieved_ids is None
            or expected_ids is None
            or not retrieved_ids
            or not expected_ids
        ):
            raise ValueError("Retrieved ids and expected ids must be provided")

        if self.use_granular_mrr:
            # Granular MRR calculation: All relevant retrieved docs have their reciprocal ranks summed and averaged
            expected_set = set(expected_ids)
            reciprocal_rank_sum = 0.0
            relevant_docs_count = 0
            for index, doc_id in enumerate(retrieved_ids):
                if doc_id in expected_set:
                    relevant_docs_count += 1
                    reciprocal_rank_sum += 1.0 / (index + 1)
            mrr_score = (
                reciprocal_rank_sum / relevant_docs_count
                if relevant_docs_count  0
                else 0.0
            )
        else:
            # Default MRR calculation: Reciprocal rank of the first relevant document retrieved
            for i, id in enumerate(retrieved_ids):
                if id in expected_ids:
                    return RetrievalMetricResult(score=1.0 / (i + 1))
            mrr_score = 0.0

        return RetrievalMetricResult(score=mrr_score)

```
 |  
| --- | --- |  
###  compute [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.MRR.compute "Permanent link")

```
compute(
    query: Optional[] = None,
    expected_ids: Optional[[]] = None,
    retrieved_ids: Optional[[]] = None,
    expected_texts: Optional[[]] = None,
    retrieved_texts: Optional[[]] = None,
    **kwargs: 
) -> 

```

Compute MRR based on the provided inputs and selected method.
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.MRR.compute--parameters "Permanent link")

```
query (Optional[str]): The query string (not used in the current implementation).
expected_ids (Optional[List[str]]): Expected document IDs.
retrieved_ids (Optional[List[str]]): Retrieved document IDs.
expected_texts (Optional[List[str]]): Expected texts (not used in the current implementation).
retrieved_texts (Optional[List[str]]): Retrieved texts (not used in the current implementation).

```

##### Raises[#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.MRR.compute--raises "Permanent link")

```
ValueError: If the necessary IDs are not provided.

```

##### Returns[#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.MRR.compute--returns "Permanent link")

```
RetrievalMetricResult: The result with the computed MRR score.

```
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/metrics.py`  
| 
```
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
```
 | 
```
defcompute(
    self,
    query: Optional[str] = None,
    expected_ids: Optional[List[str]] = None,
    retrieved_ids: Optional[List[str]] = None,
    expected_texts: Optional[List[str]] = None,
    retrieved_texts: Optional[List[str]] = None,
    **kwargs: Any,
) -> RetrievalMetricResult:
"""
    Compute MRR based on the provided inputs and selected method.

    Parameters
    ----------
        query (Optional[str]): The query string (not used in the current implementation).
        expected_ids (Optional[List[str]]): Expected document IDs.
        retrieved_ids (Optional[List[str]]): Retrieved document IDs.
        expected_texts (Optional[List[str]]): Expected texts (not used in the current implementation).
        retrieved_texts (Optional[List[str]]): Retrieved texts (not used in the current implementation).

    Raises
    ------
        ValueError: If the necessary IDs are not provided.

    Returns
    -------
        RetrievalMetricResult: The result with the computed MRR score.

    """
    # Checking for the required arguments
    if (
        retrieved_ids is None
        or expected_ids is None
        or not retrieved_ids
        or not expected_ids
    ):
        raise ValueError("Retrieved ids and expected ids must be provided")

    if self.use_granular_mrr:
        # Granular MRR calculation: All relevant retrieved docs have their reciprocal ranks summed and averaged
        expected_set = set(expected_ids)
        reciprocal_rank_sum = 0.0
        relevant_docs_count = 0
        for index, doc_id in enumerate(retrieved_ids):
            if doc_id in expected_set:
                relevant_docs_count += 1
                reciprocal_rank_sum += 1.0 / (index + 1)
        mrr_score = (
            reciprocal_rank_sum / relevant_docs_count
            if relevant_docs_count  0
            else 0.0
        )
    else:
        # Default MRR calculation: Reciprocal rank of the first relevant document retrieved
        for i, id in enumerate(retrieved_ids):
            if id in expected_ids:
                return RetrievalMetricResult(score=1.0 / (i + 1))
        mrr_score = 0.0

    return RetrievalMetricResult(score=mrr_score)

```
 |  
| --- | --- |  
##  HitRate [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.HitRate "Permanent link")
Bases: `BaseRetrievalMetric`
Hit rate metric: Compute hit rate with two calculation options.
  * The default method checks for a single match between any of the retrieved docs and expected docs.
  * The more granular method checks for all potential matches between retrieved docs and expected docs.


Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `metric_name`  |  The name of the metric.  |  
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `use_granular_hit_rate`  |  `bool`  |  `False`  |  
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/metrics.py`  
| 
```
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
```
 | 
```
classHitRate(BaseRetrievalMetric):
"""
    Hit rate metric: Compute hit rate with two calculation options.

    - The default method checks for a single match between any of the retrieved docs and expected docs.
    - The more granular method checks for all potential matches between retrieved docs and expected docs.

    Attributes:
        metric_name (str): The name of the metric.
        use_granular_hit_rate (bool): Determines whether to use the granular method for calculation.

    """

    metric_name: ClassVar[str] = "hit_rate"
    use_granular_hit_rate: bool = False

    defcompute(
        self,
        query: Optional[str] = None,
        expected_ids: Optional[List[str]] = None,
        retrieved_ids: Optional[List[str]] = None,
        expected_texts: Optional[List[str]] = None,
        retrieved_texts: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> RetrievalMetricResult:
"""
        Compute metric based on the provided inputs.

        Parameters
        ----------
            query (Optional[str]): The query string (not used in the current implementation).
            expected_ids (Optional[List[str]]): Expected document IDs.
            retrieved_ids (Optional[List[str]]): Retrieved document IDs.
            expected_texts (Optional[List[str]]): Expected texts (not used in the current implementation).
            retrieved_texts (Optional[List[str]]): Retrieved texts (not used in the current implementation).

        Raises
        ------
            ValueError: If the necessary IDs are not provided.

        Returns
        -------
            RetrievalMetricResult: The result with the computed hit rate score.

        """
        # Checking for the required arguments
        if (
            retrieved_ids is None
            or expected_ids is None
            or not retrieved_ids
            or not expected_ids
        ):
            raise ValueError("Retrieved ids and expected ids must be provided")

        if self.use_granular_hit_rate:
            # Granular HitRate calculation: Calculate all hits and divide by the number of expected docs
            expected_set = set(expected_ids)
            hits = sum(1 for doc_id in retrieved_ids if doc_id in expected_set)
            score = hits / len(expected_ids) if expected_ids else 0.0
        else:
            # Default HitRate calculation: Check if there is a single hit
            is_hit = any(id in expected_ids for id in retrieved_ids)
            score = 1.0 if is_hit else 0.0

        return RetrievalMetricResult(score=score)

```
 |  
| --- | --- |  
###  compute [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.HitRate.compute "Permanent link")

```
compute(
    query: Optional[] = None,
    expected_ids: Optional[[]] = None,
    retrieved_ids: Optional[[]] = None,
    expected_texts: Optional[[]] = None,
    retrieved_texts: Optional[[]] = None,
    **kwargs: 
) -> 

```

Compute metric based on the provided inputs.
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.HitRate.compute--parameters "Permanent link")

```
query (Optional[str]): The query string (not used in the current implementation).
expected_ids (Optional[List[str]]): Expected document IDs.
retrieved_ids (Optional[List[str]]): Retrieved document IDs.
expected_texts (Optional[List[str]]): Expected texts (not used in the current implementation).
retrieved_texts (Optional[List[str]]): Retrieved texts (not used in the current implementation).

```

##### Raises[#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.HitRate.compute--raises "Permanent link")

```
ValueError: If the necessary IDs are not provided.

```

##### Returns[#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.HitRate.compute--returns "Permanent link")

```
RetrievalMetricResult: The result with the computed hit rate score.

```
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/metrics.py`  
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
```
 | 
```
defcompute(
    self,
    query: Optional[str] = None,
    expected_ids: Optional[List[str]] = None,
    retrieved_ids: Optional[List[str]] = None,
    expected_texts: Optional[List[str]] = None,
    retrieved_texts: Optional[List[str]] = None,
    **kwargs: Any,
) -> RetrievalMetricResult:
"""
    Compute metric based on the provided inputs.

    Parameters
    ----------
        query (Optional[str]): The query string (not used in the current implementation).
        expected_ids (Optional[List[str]]): Expected document IDs.
        retrieved_ids (Optional[List[str]]): Retrieved document IDs.
        expected_texts (Optional[List[str]]): Expected texts (not used in the current implementation).
        retrieved_texts (Optional[List[str]]): Retrieved texts (not used in the current implementation).

    Raises
    ------
        ValueError: If the necessary IDs are not provided.

    Returns
    -------
        RetrievalMetricResult: The result with the computed hit rate score.

    """
    # Checking for the required arguments
    if (
        retrieved_ids is None
        or expected_ids is None
        or not retrieved_ids
        or not expected_ids
    ):
        raise ValueError("Retrieved ids and expected ids must be provided")

    if self.use_granular_hit_rate:
        # Granular HitRate calculation: Calculate all hits and divide by the number of expected docs
        expected_set = set(expected_ids)
        hits = sum(1 for doc_id in retrieved_ids if doc_id in expected_set)
        score = hits / len(expected_ids) if expected_ids else 0.0
    else:
        # Default HitRate calculation: Check if there is a single hit
        is_hit = any(id in expected_ids for id in retrieved_ids)
        score = 1.0 if is_hit else 0.0

    return RetrievalMetricResult(score=score)

```
 |  
| --- | --- |  
##  RetrievalMetricResult [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.RetrievalMetricResult "Permanent link")
Bases: `BaseModel`
Metric result.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `score`  |  `float`  |  Score for the metric  |  _required_  |  
|  `metadata`  |  `Dict[str, Any]`  |  Metadata for the metric result  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/metrics_base.py`  
| 
```
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
```
 | 
```
classRetrievalMetricResult(BaseModel):
"""
    Metric result.

    Attributes:
        score (float): Score for the metric
        metadata (Dict[str, Any]): Metadata for the metric result

    """

    score: float = Field(..., description="Score for the metric")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadata for the metric result"
    )

    def__str__(self) -> str:
"""String representation."""
        return f"Score: {self.score}\nMetadata: {self.metadata}"

    def__float__(self) -> float:
"""Float representation."""
        return self.score

```
 |  
| --- | --- |  
##  SemanticSimilarityEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.SemanticSimilarityEvaluator "Permanent link")
Bases: 
Embedding similarity evaluator.
Evaluate the quality of a question answering system by comparing the similarity between embeddings of the generated answer and the reference answer.
Inspired by this paper: - Semantic Answer Similarity for Evaluating Question Answering Models https://arxiv.org/pdf/2108.06130.pdf
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `similarity_threshold`  |  `float`  |  Embedding similarity threshold for "passing". Defaults to 0.8.  |  `0.8`  |  
Source code in `llama-index-core/llama_index/core/evaluation/semantic_similarity.py`  
| 
```
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
```
 | 
```
classSemanticSimilarityEvaluator(BaseEvaluator):
"""
    Embedding similarity evaluator.

    Evaluate the quality of a question answering system by
    comparing the similarity between embeddings of the generated answer
    and the reference answer.

    Inspired by this paper:
    - Semantic Answer Similarity for Evaluating Question Answering Models
        https://arxiv.org/pdf/2108.06130.pdf

    Args:
        similarity_threshold (float): Embedding similarity threshold for "passing".
            Defaults to 0.8.

    """

    def__init__(
        self,
        embed_model: Optional[BaseEmbedding] = None,
        similarity_fn: Optional[Callable[..., float]] = None,
        similarity_mode: Optional[SimilarityMode] = None,
        similarity_threshold: float = 0.8,
    ) -> None:
        self._embed_model = embed_model or Settings.embed_model

        if similarity_fn is None:
            similarity_mode = similarity_mode or SimilarityMode.DEFAULT
            self._similarity_fn = lambda x, y: similarity(x, y, mode=similarity_mode)
        else:
            if similarity_mode is not None:
                raise ValueError(
                    "Cannot specify both similarity_fn and similarity_mode"
                )
            self._similarity_fn = similarity_fn

        self._similarity_threshold = similarity_threshold

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""

    async defaevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        reference: Optional[str] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        del query, contexts, kwargs  # Unused

        if response is None or reference is None:
            raise ValueError("Must specify both response and reference")

        response_embedding = await self._embed_model.aget_text_embedding(response)
        reference_embedding = await self._embed_model.aget_text_embedding(reference)

        similarity_score = self._similarity_fn(response_embedding, reference_embedding)
        passing = similarity_score >= self._similarity_threshold
        return EvaluationResult(
            score=similarity_score,
            passing=passing,
            feedback=f"Similarity score: {similarity_score}",
        )

```
 |  
| --- | --- |  
##  EmbeddingQAFinetuneDataset [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.EmbeddingQAFinetuneDataset "Permanent link")
Bases: `BaseModel`
Embedding QA Finetuning Dataset.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `queries`  |  `Dict[str, str]`  |  Dict id -> query.  |  _required_  |  
|  `corpus`  |  `Dict[str, str]`  |  Dict id -> string.  |  _required_  |  
|  `relevant_docs`  |  `Dict[str, List[str]]`  |  Dict query id -> list of doc ids.  |  _required_  |  
|  `mode`  |  `'text'`  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/legacy/embedding.py`  
| 
```
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
```
 | 
```
classEmbeddingQAFinetuneDataset(BaseModel):
"""
    Embedding QA Finetuning Dataset.

    Args:
        queries (Dict[str, str]): Dict id -> query.
        corpus (Dict[str, str]): Dict id -> string.
        relevant_docs (Dict[str, List[str]]): Dict query id -> list of doc ids.

    """

    queries: Dict[str, str]  # dict id -> query
    corpus: Dict[str, str]  # dict id -> string
    relevant_docs: Dict[str, List[str]]  # query id -> list of doc ids
    mode: str = "text"

    @property
    defquery_docid_pairs(self) -> List[Tuple[str, List[str]]]:
"""Get query, relevant doc ids."""
        return [
            (query, self.relevant_docs[query_id])
            for query_id, query in self.queries.items()
        ]

    defsave_json(self, path: str) -> None:
"""Save json."""
        with open(path, "w") as f:
            json.dump(self.model_dump(), f, indent=4)

    @classmethod
    deffrom_json(cls, path: str) -> "EmbeddingQAFinetuneDataset":
"""Load json."""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)

```
 |  
| --- | --- |  
###  query_docid_pairs `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.EmbeddingQAFinetuneDataset.query_docid_pairs "Permanent link")

```
query_docid_pairs: [Tuple[, []]]

```

Get query, relevant doc ids.
###  save_json [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.EmbeddingQAFinetuneDataset.save_json "Permanent link")

```
save_json(path: ) -> None

```

Save json.
Source code in `llama-index-core/llama_index/core/llama_dataset/legacy/embedding.py`  
| 
```
40
41
42
43
```
 | 
```
defsave_json(self, path: str) -> None:
"""Save json."""
    with open(path, "w") as f:
        json.dump(self.model_dump(), f, indent=4)

```
 |  
| --- | --- |  
###  from_json `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.EmbeddingQAFinetuneDataset.from_json "Permanent link")

```
from_json(path: ) -> 

```

Load json.
Source code in `llama-index-core/llama_index/core/llama_dataset/legacy/embedding.py`  
| 
```
45
46
47
48
49
50
```
 | 
```
@classmethod
deffrom_json(cls, path: str) -> "EmbeddingQAFinetuneDataset":
"""Load json."""
    with open(path) as f:
        data = json.load(f)
    return cls(**data)

```
 |  
| --- | --- |  
##  get_retrieval_results_df [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.get_retrieval_results_df "Permanent link")

```
get_retrieval_results_df(
    names: [],
    results_arr: [[]],
    metric_keys: Optional[[]] = None,
) -> 

```

Display retrieval results.
Source code in `llama-index-core/llama_index/core/evaluation/notebook_utils.py`  
| 
```
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
```
 | 
```
defget_retrieval_results_df(
    names: List[str],
    results_arr: List[List[RetrievalEvalResult]],
    metric_keys: Optional[List[str]] = None,
) -> Any:
"""Display retrieval results."""
    try:
        importpandasaspd
    except ImportError:
        raise ImportError(
            "pandas is required for this function. Please install it with `pip install pandas`."
        )

    metric_keys = metric_keys or DEFAULT_METRIC_KEYS

    avg_metrics_dict = defaultdict(list)
    for name, eval_results in zip(names, results_arr):
        metric_dicts = []
        for eval_result in eval_results:
            metric_dict = eval_result.metric_vals_dict
            metric_dicts.append(metric_dict)
        results_df = pd.DataFrame(metric_dicts)

        for metric_key in metric_keys:
            if metric_key not in results_df.columns:
                raise ValueError(f"Metric key {metric_key} not in results_df")
            avg_metrics_dict[metric_key].append(results_df[metric_key].mean())

    return pd.DataFrame({"retrievers": names, **avg_metrics_dict})

```
 |  
| --- | --- |  
##  resolve_metrics [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.resolve_metrics "Permanent link")

```
resolve_metrics(
    metrics: [],
) -> [[BaseRetrievalMetric]]

```

Resolve metrics from list of metric names.
Source code in `llama-index-core/llama_index/core/evaluation/retrieval/metrics.py`  
| 
```
507
508
509
510
511
512
513
```
 | 
```
defresolve_metrics(metrics: List[str]) -> List[Type[BaseRetrievalMetric]]:
"""Resolve metrics from list of metric names."""
    for metric in metrics:
        if metric not in METRIC_REGISTRY:
            raise ValueError(f"Invalid metric name: {metric}")

    return [METRIC_REGISTRY[metric] for metric in metrics]

```
 |  
| --- | --- |  
##  generate_qa_embedding_pairs [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.generate_qa_embedding_pairs "Permanent link")

```
generate_qa_embedding_pairs(
    nodes: [],
    llm: Optional[] = None,
    qa_generate_prompt_tmpl:  = DEFAULT_QA_GENERATE_PROMPT_TMPL,
    num_questions_per_chunk:  = 2,
) -> 

```

Generate examples given a set of nodes.
Source code in `llama-index-core/llama_index/core/llama_dataset/legacy/embedding.py`  
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
```
 | 
```
defgenerate_qa_embedding_pairs(
    nodes: List[TextNode],
    llm: Optional[LLM] = None,
    qa_generate_prompt_tmpl: str = DEFAULT_QA_GENERATE_PROMPT_TMPL,
    num_questions_per_chunk: int = 2,
) -> EmbeddingQAFinetuneDataset:
"""Generate examples given a set of nodes."""
    llm = llm or Settings.llm
    node_dict = {
        node.node_id: node.get_content(metadata_mode=MetadataMode.NONE)
        for node in nodes
    }

    queries = {}
    relevant_docs = {}
    for node_id, text in tqdm(node_dict.items()):
        query = qa_generate_prompt_tmpl.format(
            context_str=text, num_questions_per_chunk=num_questions_per_chunk
        )
        response = llm.complete(query)

        result = str(response).strip().split("\n")
        questions = [
            re.sub(r"^\d+[\).\s]", "", question).strip() for question in result
        ]
        questions = [question for question in questions if len(question)  0][
            :num_questions_per_chunk
        ]

        num_questions_generated = len(questions)
        if num_questions_generated  num_questions_per_chunk:
            warnings.warn(
                f"Fewer questions generated ({num_questions_generated}) "
                f"than requested ({num_questions_per_chunk}).",
                stacklevel=2,
            )

        for question in questions:
            question_id = str(uuid.uuid4())
            queries[question_id] = question
            relevant_docs[question_id] = [node_id]

    # construct dataset
    return EmbeddingQAFinetuneDataset(
        queries=queries, corpus=node_dict, relevant_docs=relevant_docs
    )

```
 |  
| --- | --- |  
options: members: - BaseEvaluator - EvaluationResult - BatchEvalRunner
