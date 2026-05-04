# Diff private simple dataset
##  DiffPrivateSimpleDatasetPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/diff_private_simple_dataset/#llama_index.packs.diff_private_simple_dataset.DiffPrivateSimpleDatasetPack "Permanent link")
Bases: 
A pack for creating differentially private simple llama-dataset.
Source code in `llama-index-packs/llama-index-packs-diff-private-simple-dataset/llama_index/packs/diff_private_simple_dataset/base.py`  
| 
```
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
```
 | 
```
classDiffPrivateSimpleDatasetPack(BaseLlamaPack):
"""A pack for creating differentially private simple llama-dataset."""

    def__init__(
        self,
        llm: LLM,  # currently only supports OpenAI completion LLMs
        tokenizer: Any,
        prompt_bundle: PromptBundle,
        simple_dataset: LabelledSimpleDataset,
        batch_size: int = 5,
        sleep_time_in_seconds: float = 0,
        sephamore_counter_size: int = 1,
        cache_checkpoints: bool = True,
        show_progress: bool = True,
    ):
        self.llm = llm
        self.tokenizer = tokenizer
        self.prompt_bundle = prompt_bundle
        self.simple_dataset = simple_dataset
        self._num_examples = len(self.simple_dataset.examples)
        self.labels = list({el.reference_label for el in self.simple_dataset[:]})
        self.sleep_time_in_seconds = sleep_time_in_seconds
        self._semaphore = asyncio.Semaphore(sephamore_counter_size)
        self.show_progress = show_progress
        self.batch_size = batch_size
        self.cache_checkpoints = cache_checkpoints

    defsigma_to_eps(
        self,
        sigma: float,
        mechanism: PrivacyMechanism,
        size: int,
        max_token_cnt: int,
        max_self_compositions: int = 1000,
        eps_error: float = 0.01,
        delta_error: float = 1e-10,
    ) -> float:
"""
        Return the epsilon value given a sigma.

        Args:
            sigma (float): The parameter associated with noise mechanism.
            mechanism (PrivacyMechanism): Noise mechanism.
            size (int): Number of samples to be generated.
            max_token_cnt (int): Number of tokens generated per sample.
            max_self_compositions (int, optional): PRV algorithm parameter. Defaults to 1000.
            eps_error (float, optional): PRV algorithm parameter. Defaults to 0.01.
            delta_error (float, optional): PRV algorithm parameter. Defaults to 1e-10.

        Returns:
            float: The epsilon value.

        """
        if max_token_cnt  max_self_compositions:
            raise ValueError(
                "`max_token_cnt` cannot be greater than `max_self_composition`."
            )

        sample_rate = size / self._num_examples
        if mechanism == PrivacyMechanism.GAUSSIAN:
            prv_0 = PoissonSubsampledGaussianMechanism(
                noise_multiplier=sigma, sampling_probability=sample_rate
            )
        elif mechanism == PrivacyMechanism.EXPONENTIAL:
            sigma_bar = math.log(1 + sample_rate * (math.exp(sigma) - 1))
            prv_0 = PureDPMechanism(eps=sigma_bar)
        else:
            raise ValueError(
                "Invalid value for mechanism entered."
                " Please use either 'gaussian' or 'exponential'."
            )
        accountant = PRVAccountant(
            prvs=[
                prv_0,
            ],
            max_self_compositions=[max_self_compositions],
            eps_error=eps_error,
            delta_error=delta_error,
        )
        _eps_low, eps_est, _eps_up = accountant.compute_epsilon(
            delta=1 / self._num_examples, num_self_compositions=[max_token_cnt]
        )
        return eps_est

    async def_async_worker(self, job: Coroutine) -> Any:
        async with self._semaphore:
            await asyncio.sleep(self.sleep_time_in_seconds)
            return await job

    @dispatcher.span
    def_filter_dataset_by_label(self, label: str) -> LabelledSimpleDataset:
"""Filter simple_dataset by label."""
        if label not in self.labels:
            raise ValueError(
                "There are no examples with `label` in the associated `simple_dataset`."
            )
        examples = [el for el in self.simple_dataset[:] if el.reference_label == label]
        return LabelledSimpleDataset(examples=examples)

    @dispatcher.span
    def_split_dataset(
        self,
        dataset: LabelledSimpleDataset,
        num_splits: int,
        num_samples_per_split: int,
    ) -> List[LabelledSimpleDataset]:
"""Splits a dataset into a set of disjoint datasets with equal number of examples."""
        indexes = list(range(len(dataset.examples)))
        random.shuffle(indexes)
        partitions = [indexes[i::num_splits] for i in range(num_splits)]
        splits = []
        for p in partitions:
            sample = random.sample(p, num_samples_per_split)
            if not len(sample) == num_samples_per_split:
                raise ValueError(
                    "Not able to create disjoint sets with current values of `num_splits` and `num_samples_per_split`."
                )
            examples = [dataset.examples[ix] for ix in sample]
            splits.append(LabelledSimpleDataset(examples=examples))
        return splits

    def_get_public_prompt(
        self,
        synthetic_example: str,
        label: str,
    ) -> str:
"""Get completion prompt for token universe."""
        return zero_shot_completion_template.format(
            synthetic_text=synthetic_example,
            label=label,
            instruction=self.prompt_bundle.instruction,
            label_heading=self.prompt_bundle.label_heading,
            text_heading=self.prompt_bundle.text_heading,
        )

    def_get_private_prompt(
        self,
        split: LabelledSimpleDataset,
        synthetic_example: str,
        label: str,
    ) -> str:
"""Get prompt for completion endpoint."""
        single_templates = [
            single_example_template.format(
                label_heading=self.prompt_bundle.label_heading,
                text_heading=self.prompt_bundle.text_heading,
                example_label=x.reference_label,
                example_text=x.text,
            )
            for x in split.examples
        ]

        few_shot_examples = reduce(lambda x, y: x + y, single_templates)
        return few_shot_completion_template.format(
            instruction=self.prompt_bundle.instruction,
            label_heading=self.prompt_bundle.label_heading,
            text_heading=self.prompt_bundle.text_heading,
            few_shot_examples=few_shot_examples,
            label=label,
            synthetic_text=synthetic_example,
        )

    def_normalize(
        self, split_probs: Dict[str, float], token_universe_proba: Dict[str, float]
    ) -> Dict[str, float]:
"""Normalize a probability distribution over tokens to become a valid probability distribution."""
        scale = sum(proba for proba in split_probs.values())
        if scale == 0:
            # universe
            dispatcher.event(
                EmptyIntersectionEvent(
                    public_tokens=list(token_universe_proba),
                    private_tokens=list(split_probs),
                )
            )
            split_probs = token_universe_proba  # use public probas instead
            scale = sum(proba for proba in split_probs.values())

        return {token: proba / scale for token, proba in split_probs.items()}

    def_extract_and_normalize_next_token_probas(
        self, response: CompletionResponse, token_universe_probas: Dict[str, float]
    ) -> Dict[str, float]:
"""Extract and normalize LogProba from a CompletionResponse."""
        try:
            next_token_proba_distn = response.logprobs[0]
        except IndexError:
            dispatcher.event(LLMEmptyResponseEvent())
            return token_universe_probas
        except Exception as e:
            raise ValueError(
                "Something went wrong when trying to get LogProb from CompletionResponse."
            )

        split_probs = dict.fromkeys(token_universe_probas, 0)
        for el in next_token_proba_distn:  # for immediate next token only
            if el.token in split_probs:
                split_probs[el.token] = np.exp(el.logprob)
        return self._normalize(
            split_probs, token_universe_probas
        )  # to make into a valid prob distribution

    def_generate_noise(
        self, sigma: float, size: int, mechanism: PrivacyMechanism
    ) -> float:
"""Generates noise that satisfies eps-delta differential privacy."""
        noise_rng = np.random.RandomState()
        if mechanism == PrivacyMechanism.GAUSSIAN:
            return noise_rng.normal(0, sigma, size=size)
        elif mechanism == PrivacyMechanism.LAPLACE:
            return noise_rng.exponential(scale=sigma, size=size)
        else:
            raise ValueError("Value entered for `mechanism` is not supported.")

    def_merge_probas(self, list_of_probas: List[Dict[str, float]]) -> Dict[str, float]:
"""Merges a set of probabillity distributions over a common token universe."""
        scale = len(list_of_probas)
        tokens = list_of_probas[0].keys()
        merged_distribution = {}
        for token in tokens:
            merged_distribution[token] = sum(pr[token] / scale for pr in list_of_probas)
        return merged_distribution

    def_add_noise(
        self, proba: Dict[str, float], noise_array=Sequence[float]
    ) -> Dict[str, float]:
"""Add noise to proba distribution."""
        return {
            token: proba + noise
            for (token, proba), noise in zip(proba.items(), noise_array)
        }

    def_mode_of_distribution(self, proba: Dict[str, float]) -> str:
"""Returns the mode of a given probability distribution."""
        return max(proba, key=proba.get)

    @dispatcher.span
    defgenerate_dp_synthetic_example(
        self,
        label: str,
        t_max: int = 1,
        sigma: float = 0.5,
        num_splits: int = 5,
        num_samples_per_split: int = 1,
    ) -> LabelledSimpleDataExample:
"""Generates a differentially private synthetic example."""
        return asyncio.run(
            self.agenerate_dp_synthetic_example(
                label=label,
                t_max=t_max,
                sigma=sigma,
                num_splits=num_splits,
                num_samples_per_split=num_samples_per_split,
            )
        )

    @dispatcher.span
    async defagenerate_dp_synthetic_example(
        self,
        label: str,
        t_max: int = 1,
        sigma: float = 0.5,
        num_splits: int = 5,
        num_samples_per_split: int = 1,
    ) -> LabelledSimpleDataExample:
"""Generates a differentially private synthetic example."""
        dispatcher.event(SyntheticExampleStartEvent())
        synthetic_example = ""

        iterator = range(1, t_max + 1)
        if self.show_progress:
            iterator = tqdm.tqdm(iterator, position=0, leave=True)

        for _ in iterator:
            token_universe_prompt = self._get_public_prompt(
                synthetic_example=synthetic_example, label=label
            )
            try:
                response = await self._async_worker(
                    self.llm.acomplete(token_universe_prompt)
                )
                token_universe_probas = {
                    el.token: np.exp(el.logprob)
                    for el in response.logprobs[0]  # only for next immediate token
                }
            except IndexError as e:
                continue  # try again in next iteration

            # filter dataset by label
            filtered_simple_dataset = self._filter_dataset_by_label(label=label)

            # split the private dataset
            disjoint_splits = self._split_dataset(
                dataset=filtered_simple_dataset,
                num_splits=num_splits,
                num_samples_per_split=num_samples_per_split,
            )

            # generate next token probability distributions per split
            split_tasks = []
            for split in disjoint_splits:
                prompt = self._get_private_prompt(split, synthetic_example, label)
                split_tasks.append(self._async_worker(self.llm.acomplete(prompt)))

            split_responses: List[CompletionResponse] = await asyncio.gather(
                *split_tasks
            )

            # get and normalized next-token probas per split
            splits = [
                self._extract_and_normalize_next_token_probas(
                    response, token_universe_probas
                )
                for response in split_responses
            ]

            # noisy aggrergation
            sigma_calib = np.sqrt(2) / num_splits * sigma
            noise_array = self._generate_noise(
                sigma=sigma_calib, size=len(token_universe_probas), mechanism="gaussian"
            )
            merged_probas = self._merge_probas(splits)
            noisy_probs = self._add_noise(merged_probas, noise_array)

            # next token
            next_token = self._mode_of_distribution(noisy_probs)
            if next_token in STOP_TOKENS:
                break
            else:
                synthetic_example += next_token

        # synthetic example remove [RESULT]
        try:
            synthetic_example = synthetic_example.split("[RESULT]")[-1].strip()
        except Exception as e:
            synthetic_example = synthetic_example

        simple_example = LabelledSimpleDataExample(
            reference_label=label,
            text=synthetic_example,
            text_by=CreatedBy(type=CreatedByType.AI, model_name=self.llm.model),
        )
        dispatcher.event(SyntheticExampleEndEvent())
        return simple_example

    @dispatcher.span
    defrun(
        self,
        sizes: Union[int, Dict[str, int]],
        t_max: int = 1,
        sigma: float = 0.5,
        num_splits: int = 5,
        num_samples_per_split: int = 1,
    ) -> LabelledSimpleDataset:
"""Main run method."""
        if num_samples_per_split  1:
            raise ValueError(
                "`num_samples_per_split` must be an integer greater than 1."
            )

        if isinstance(sizes, int):
            sizes_dict = dict.fromkeys(self.labels, sizes)
        elif isinstance(sizes, dict):
            sizes_dict = sizes
        else:
            raise TypeError(
                "Invalid type of `sizes`. Must be either an `int` or `dict`."
            )

        if not all(c in sizes_dict for c in self.labels):
            raise ValueError("Not all labels have sizes.")

        examples = []
        for label in self.labels:
            size = sizes_dict[label]
            for _ in range(size):
                example = self.generate_dp_synthetic_example(
                    label=label,
                    t_max=t_max,
                    sigma=sigma,
                    num_splits=num_splits,
                    num_samples_per_split=num_samples_per_split,
                )
                examples.append(example)

        return LabelledSimpleDataset(examples=examples)

    @dispatcher.span
    async defarun(
        self,
        sizes: Dict[str, int],
        t_max: int = 1,
        sigma: float = 0.5,
        num_splits: int = 5,
        num_samples_per_split: int = 1,
    ) -> LabelledSimpleDataset:
"""Main async run method."""
        if num_samples_per_split  1:
            raise ValueError(
                "`num_samples_per_split` must be an integer greater than 1."
            )

        if isinstance(sizes, int):
            sizes_dict = dict.fromkeys(self.labels, sizes)
        elif isinstance(sizes, dict):
            sizes_dict = sizes
        else:
            raise TypeError(
                "Invalid type of `sizes`. Must be either an `int` or `dict`."
            )

        if not all(c in sizes_dict for c in self.labels):
            raise ValueError("Not all labels have sizes.")

        tasks = []
        for label in self.labels:
            size = sizes_dict[label]
            for _ in range(size):
                example_task = self.agenerate_dp_synthetic_example(
                    label=label,
                    t_max=t_max,
                    sigma=sigma,
                    num_splits=num_splits,
                    num_samples_per_split=num_samples_per_split,
                )
                tasks.append(example_task)

        asyncio_runner = asyncio_module(self.show_progress)

        # run in batch
        examples = []
        for batch in _batch(tasks, self.batch_size):
            batch_examples = await asyncio_runner.gather(*batch)
            examples += batch_examples
            if self.cache_checkpoints:
                checkpoint = LabelledSimpleDataset(examples=examples)
                checkpoint.save_json("checkpoint.json")

        return LabelledSimpleDataset(examples=examples)

```
 |  
| --- | --- |  
###  sigma_to_eps [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/diff_private_simple_dataset/#llama_index.packs.diff_private_simple_dataset.DiffPrivateSimpleDatasetPack.sigma_to_eps "Permanent link")

```
sigma_to_eps(
    sigma: float,
    mechanism: PrivacyMechanism,
    size: ,
    max_token_cnt: ,
    max_self_compositions:  = 1000,
    eps_error: float = 0.01,
    delta_error: float = 1e-10,
) -> float

```

Return the epsilon value given a sigma.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sigma`  |  `float`  |  The parameter associated with noise mechanism.  |  _required_  |  
|  `mechanism`  |  `PrivacyMechanism`  |  Noise mechanism.  |  _required_  |  
|  `size`  |  Number of samples to be generated.  |  _required_  |  
|  `max_token_cnt`  |  Number of tokens generated per sample.  |  _required_  |  
|  `max_self_compositions`  |  PRV algorithm parameter. Defaults to 1000.  |  `1000`  |  
|  `eps_error`  |  `float`  |  PRV algorithm parameter. Defaults to 0.01.  |  `0.01`  |  
|  `delta_error`  |  `float`  |  PRV algorithm parameter. Defaults to 1e-10.  |  `1e-10`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `float`  |  `float`  |  The epsilon value.  |  
Source code in `llama-index-packs/llama-index-packs-diff-private-simple-dataset/llama_index/packs/diff_private_simple_dataset/base.py`  
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
```
 | 
```
defsigma_to_eps(
    self,
    sigma: float,
    mechanism: PrivacyMechanism,
    size: int,
    max_token_cnt: int,
    max_self_compositions: int = 1000,
    eps_error: float = 0.01,
    delta_error: float = 1e-10,
) -> float:
"""
    Return the epsilon value given a sigma.

    Args:
        sigma (float): The parameter associated with noise mechanism.
        mechanism (PrivacyMechanism): Noise mechanism.
        size (int): Number of samples to be generated.
        max_token_cnt (int): Number of tokens generated per sample.
        max_self_compositions (int, optional): PRV algorithm parameter. Defaults to 1000.
        eps_error (float, optional): PRV algorithm parameter. Defaults to 0.01.
        delta_error (float, optional): PRV algorithm parameter. Defaults to 1e-10.

    Returns:
        float: The epsilon value.

    """
    if max_token_cnt  max_self_compositions:
        raise ValueError(
            "`max_token_cnt` cannot be greater than `max_self_composition`."
        )

    sample_rate = size / self._num_examples
    if mechanism == PrivacyMechanism.GAUSSIAN:
        prv_0 = PoissonSubsampledGaussianMechanism(
            noise_multiplier=sigma, sampling_probability=sample_rate
        )
    elif mechanism == PrivacyMechanism.EXPONENTIAL:
        sigma_bar = math.log(1 + sample_rate * (math.exp(sigma) - 1))
        prv_0 = PureDPMechanism(eps=sigma_bar)
    else:
        raise ValueError(
            "Invalid value for mechanism entered."
            " Please use either 'gaussian' or 'exponential'."
        )
    accountant = PRVAccountant(
        prvs=[
            prv_0,
        ],
        max_self_compositions=[max_self_compositions],
        eps_error=eps_error,
        delta_error=delta_error,
    )
    _eps_low, eps_est, _eps_up = accountant.compute_epsilon(
        delta=1 / self._num_examples, num_self_compositions=[max_token_cnt]
    )
    return eps_est

```
 |  
| --- | --- |  
###  generate_dp_synthetic_example [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/diff_private_simple_dataset/#llama_index.packs.diff_private_simple_dataset.DiffPrivateSimpleDatasetPack.generate_dp_synthetic_example "Permanent link")

```
generate_dp_synthetic_example(
    label: ,
    t_max:  = 1,
    sigma: float = 0.5,
    num_splits:  = 5,
    num_samples_per_split:  = 1,
) -> LabelledSimpleDataExample

```

Generates a differentially private synthetic example.
Source code in `llama-index-packs/llama-index-packs-diff-private-simple-dataset/llama_index/packs/diff_private_simple_dataset/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defgenerate_dp_synthetic_example(
    self,
    label: str,
    t_max: int = 1,
    sigma: float = 0.5,
    num_splits: int = 5,
    num_samples_per_split: int = 1,
) -> LabelledSimpleDataExample:
"""Generates a differentially private synthetic example."""
    return asyncio.run(
        self.agenerate_dp_synthetic_example(
            label=label,
            t_max=t_max,
            sigma=sigma,
            num_splits=num_splits,
            num_samples_per_split=num_samples_per_split,
        )
    )

```
 |  
| --- | --- |  
###  agenerate_dp_synthetic_example [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/diff_private_simple_dataset/#llama_index.packs.diff_private_simple_dataset.DiffPrivateSimpleDatasetPack.agenerate_dp_synthetic_example "Permanent link")

```
agenerate_dp_synthetic_example(
    label: ,
    t_max:  = 1,
    sigma: float = 0.5,
    num_splits:  = 5,
    num_samples_per_split:  = 1,
) -> LabelledSimpleDataExample

```

Generates a differentially private synthetic example.
Source code in `llama-index-packs/llama-index-packs-diff-private-simple-dataset/llama_index/packs/diff_private_simple_dataset/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
async defagenerate_dp_synthetic_example(
    self,
    label: str,
    t_max: int = 1,
    sigma: float = 0.5,
    num_splits: int = 5,
    num_samples_per_split: int = 1,
) -> LabelledSimpleDataExample:
"""Generates a differentially private synthetic example."""
    dispatcher.event(SyntheticExampleStartEvent())
    synthetic_example = ""

    iterator = range(1, t_max + 1)
    if self.show_progress:
        iterator = tqdm.tqdm(iterator, position=0, leave=True)

    for _ in iterator:
        token_universe_prompt = self._get_public_prompt(
            synthetic_example=synthetic_example, label=label
        )
        try:
            response = await self._async_worker(
                self.llm.acomplete(token_universe_prompt)
            )
            token_universe_probas = {
                el.token: np.exp(el.logprob)
                for el in response.logprobs[0]  # only for next immediate token
            }
        except IndexError as e:
            continue  # try again in next iteration

        # filter dataset by label
        filtered_simple_dataset = self._filter_dataset_by_label(label=label)

        # split the private dataset
        disjoint_splits = self._split_dataset(
            dataset=filtered_simple_dataset,
            num_splits=num_splits,
            num_samples_per_split=num_samples_per_split,
        )

        # generate next token probability distributions per split
        split_tasks = []
        for split in disjoint_splits:
            prompt = self._get_private_prompt(split, synthetic_example, label)
            split_tasks.append(self._async_worker(self.llm.acomplete(prompt)))

        split_responses: List[CompletionResponse] = await asyncio.gather(
            *split_tasks
        )

        # get and normalized next-token probas per split
        splits = [
            self._extract_and_normalize_next_token_probas(
                response, token_universe_probas
            )
            for response in split_responses
        ]

        # noisy aggrergation
        sigma_calib = np.sqrt(2) / num_splits * sigma
        noise_array = self._generate_noise(
            sigma=sigma_calib, size=len(token_universe_probas), mechanism="gaussian"
        )
        merged_probas = self._merge_probas(splits)
        noisy_probs = self._add_noise(merged_probas, noise_array)

        # next token
        next_token = self._mode_of_distribution(noisy_probs)
        if next_token in STOP_TOKENS:
            break
        else:
            synthetic_example += next_token

    # synthetic example remove [RESULT]
    try:
        synthetic_example = synthetic_example.split("[RESULT]")[-1].strip()
    except Exception as e:
        synthetic_example = synthetic_example

    simple_example = LabelledSimpleDataExample(
        reference_label=label,
        text=synthetic_example,
        text_by=CreatedBy(type=CreatedByType.AI, model_name=self.llm.model),
    )
    dispatcher.event(SyntheticExampleEndEvent())
    return simple_example

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/diff_private_simple_dataset/#llama_index.packs.diff_private_simple_dataset.DiffPrivateSimpleDatasetPack.run "Permanent link")

```
run(
    sizes: Union[, [, ]],
    t_max:  = 1,
    sigma: float = 0.5,
    num_splits:  = 5,
    num_samples_per_split:  = 1,
) -> LabelledSimpleDataset

```

Main run method.
Source code in `llama-index-packs/llama-index-packs-diff-private-simple-dataset/llama_index/packs/diff_private_simple_dataset/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defrun(
    self,
    sizes: Union[int, Dict[str, int]],
    t_max: int = 1,
    sigma: float = 0.5,
    num_splits: int = 5,
    num_samples_per_split: int = 1,
) -> LabelledSimpleDataset:
"""Main run method."""
    if num_samples_per_split  1:
        raise ValueError(
            "`num_samples_per_split` must be an integer greater than 1."
        )

    if isinstance(sizes, int):
        sizes_dict = dict.fromkeys(self.labels, sizes)
    elif isinstance(sizes, dict):
        sizes_dict = sizes
    else:
        raise TypeError(
            "Invalid type of `sizes`. Must be either an `int` or `dict`."
        )

    if not all(c in sizes_dict for c in self.labels):
        raise ValueError("Not all labels have sizes.")

    examples = []
    for label in self.labels:
        size = sizes_dict[label]
        for _ in range(size):
            example = self.generate_dp_synthetic_example(
                label=label,
                t_max=t_max,
                sigma=sigma,
                num_splits=num_splits,
                num_samples_per_split=num_samples_per_split,
            )
            examples.append(example)

    return LabelledSimpleDataset(examples=examples)

```
 |  
| --- | --- |  
###  arun [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/diff_private_simple_dataset/#llama_index.packs.diff_private_simple_dataset.DiffPrivateSimpleDatasetPack.arun "Permanent link")

```
arun(
    sizes: [, ],
    t_max:  = 1,
    sigma: float = 0.5,
    num_splits:  = 5,
    num_samples_per_split:  = 1,
) -> LabelledSimpleDataset

```

Main async run method.
Source code in `llama-index-packs/llama-index-packs-diff-private-simple-dataset/llama_index/packs/diff_private_simple_dataset/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
async defarun(
    self,
    sizes: Dict[str, int],
    t_max: int = 1,
    sigma: float = 0.5,
    num_splits: int = 5,
    num_samples_per_split: int = 1,
) -> LabelledSimpleDataset:
"""Main async run method."""
    if num_samples_per_split  1:
        raise ValueError(
            "`num_samples_per_split` must be an integer greater than 1."
        )

    if isinstance(sizes, int):
        sizes_dict = dict.fromkeys(self.labels, sizes)
    elif isinstance(sizes, dict):
        sizes_dict = sizes
    else:
        raise TypeError(
            "Invalid type of `sizes`. Must be either an `int` or `dict`."
        )

    if not all(c in sizes_dict for c in self.labels):
        raise ValueError("Not all labels have sizes.")

    tasks = []
    for label in self.labels:
        size = sizes_dict[label]
        for _ in range(size):
            example_task = self.agenerate_dp_synthetic_example(
                label=label,
                t_max=t_max,
                sigma=sigma,
                num_splits=num_splits,
                num_samples_per_split=num_samples_per_split,
            )
            tasks.append(example_task)

    asyncio_runner = asyncio_module(self.show_progress)

    # run in batch
    examples = []
    for batch in _batch(tasks, self.batch_size):
        batch_examples = await asyncio_runner.gather(*batch)
        examples += batch_examples
        if self.cache_checkpoints:
            checkpoint = LabelledSimpleDataset(examples=examples)
            checkpoint.save_json("checkpoint.json")

    return LabelledSimpleDataset(examples=examples)

```
 |  
| --- | --- |  
options: members: - DiffPrivateSimpleDatasetPack
