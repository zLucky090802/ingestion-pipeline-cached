# Rag evaluator
##  RagEvaluatorPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/rag_evaluator/#llama_index.packs.rag_evaluator.RagEvaluatorPack "Permanent link")
Bases: 
A pack for performing evaluation with your own RAG pipeline.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_engine`  |   |  The RAG pipeline to evaluate.  |  _required_  |  
|  `rag_dataset`  |   |  The BaseLlamaDataset to evaluate on.  |  _required_  |  
|  `judge_llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.LLM\)")]`  |  The LLM to use as the evaluator.  |  `None`  |  
Source code in `llama-index-packs/llama-index-packs-rag-evaluator/llama_index/packs/rag_evaluator/base.py`  
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
```
 | 
```
classRagEvaluatorPack(BaseLlamaPack):
"""
    A pack for performing evaluation with your own RAG pipeline.

    Args:
        query_engine: The RAG pipeline to evaluate.
        rag_dataset: The BaseLlamaDataset to evaluate on.
        judge_llm: The LLM to use as the evaluator.

    """

    def__init__(
        self,
        query_engine: BaseQueryEngine,
        rag_dataset: BaseLlamaDataset,
        judge_llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        show_progress: bool = True,
        result_path: Optional[str] = None,
    ):
        self.query_engine = query_engine
        self.rag_dataset = rag_dataset
        self._num_examples = len(self.rag_dataset.examples)
        if judge_llm is None:
            self.judge_llm = OpenAI(temperature=0, model="gpt-4-1106-preview")
        else:
            assert isinstance(judge_llm, LLM)
            self.judge_llm = judge_llm

        self.embed_model = embed_model or Settings.embed_model
        self.show_progress = show_progress
        self.evals = {
            "correctness": [],
            "relevancy": [],
            "faithfulness": [],
            "context_similarity": [],
        }
        self.eval_queue = deque(range(len(rag_dataset.examples)))
        self.prediction_dataset = None
        if result_path is None:
            self.result_path = Path.cwd()
        else:
            self.result_path = Path(result_path)
            if not self.result_path.is_absolute():
                self.result_path = Path.cwd() / self.result_path

        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

    async def_amake_predictions(
        self,
        batch_size: int = 20,
        sleep_time_in_seconds: int = 1,
    ):
"""Async make predictions with query engine."""
        self.prediction_dataset: BaseLlamaPredictionDataset = (
            await self.rag_dataset.amake_predictions_with(
                self.query_engine,
                show_progress=self.show_progress,
                batch_size=batch_size,
                sleep_time_in_seconds=sleep_time_in_seconds,
            )
        )

    def_make_predictions(
        self,
        batch_size: int = 20,
        sleep_time_in_seconds: int = 1,
    ):
"""Sync make predictions with query engine."""
        self.prediction_dataset: BaseLlamaPredictionDataset = (
            self.rag_dataset.make_predictions_with(
                self.query_engine,
                show_progress=self.show_progress,
                batch_size=batch_size,
                sleep_time_in_seconds=sleep_time_in_seconds,
            )
        )

    def_prepare_judges(self):
"""Construct the evaluators."""
        judges = {}
        judges["correctness"] = CorrectnessEvaluator(
            llm=self.judge_llm,
        )
        judges["relevancy"] = RelevancyEvaluator(
            llm=self.judge_llm,
        )
        judges["faithfulness"] = FaithfulnessEvaluator(
            llm=self.judge_llm,
        )
        judges["semantic_similarity"] = SemanticSimilarityEvaluator(
            embed_model=self.embed_model
        )
        return judges

    async def_areturn_null_eval_result(self, query) -> EvaluationResult:
"""
        A dummy async method that returns None.

        NOTE: this is used to handle case when creating async tasks for evaluating
        predictions where contexts do not exist.
        """
        return EvaluationResult(
            query=query,
        )

    def_return_null_eval_result(self, query) -> EvaluationResult:
"""
        A dummy async method that returns None.

        NOTE: this is used to handle case when creating async tasks for evaluating
        predictions where contexts do not exist.
        """
        return EvaluationResult(
            query=query,
        )

    def_create_async_evaluate_example_prediction_tasks(
        self, judges, example, prediction, sleep_time_in_seconds
    ):
"""Collect the co-routines."""
        correctness_task = judges["correctness"].aevaluate(
            query=example.query,
            response=prediction.response,
            reference=example.reference_answer,
            sleep_time_in_seconds=sleep_time_in_seconds,
        )

        relevancy_task = judges["relevancy"].aevaluate(
            query=example.query,
            response=prediction.response,
            contexts=prediction.contexts,
            sleep_time_in_seconds=sleep_time_in_seconds,
        )

        faithfulness_task = judges["faithfulness"].aevaluate(
            query=example.query,
            response=prediction.response,
            contexts=prediction.contexts,
            sleep_time_in_seconds=sleep_time_in_seconds,
        )

        if example.reference_contexts and prediction.contexts:
            semantic_similarity_task = judges["semantic_similarity"].aevaluate(
                query=example.query,
                response="\n".join(prediction.contexts),
                reference="\n".join(example.reference_contexts),
            )
        else:
            semantic_similarity_task = self._areturn_null_eval_result(
                query=example.query
            )

        return (
            correctness_task,
            relevancy_task,
            faithfulness_task,
            semantic_similarity_task,
        )

    def_evaluate_example_prediction(self, judges, example, prediction):
"""Collect the co-routines."""
        correctness_result = judges["correctness"].evaluate(
            query=example.query,
            response=prediction.response,
            reference=example.reference_answer,
        )

        relevancy_result = judges["relevancy"].evaluate(
            query=example.query,
            response=prediction.response,
            contexts=prediction.contexts,
        )

        faithfulness_result = judges["faithfulness"].evaluate(
            query=example.query,
            response=prediction.response,
            contexts=prediction.contexts,
        )

        if example.reference_contexts and prediction.contexts:
            semantic_similarity_result = judges["semantic_similarity"].evaluate(
                query=example.query,
                response="\n".join(prediction.contexts),
                reference="\n".join(example.reference_contexts),
            )
        else:
            semantic_similarity_result = self._return_null_eval_result(
                query=example.query
            )

        return (
            correctness_result,
            relevancy_result,
            faithfulness_result,
            semantic_similarity_result,
        )

    def_save_evaluations(self):
"""Save evaluation json object."""
        # saving evaluations
        evaluations_objects = {
            "context_similarity": [e.dict() for e in self.evals["context_similarity"]],
            "correctness": [e.dict() for e in self.evals["correctness"]],
            "faithfulness": [e.dict() for e in self.evals["faithfulness"]],
            "relevancy": [e.dict() for e in self.evals["relevancy"]],
        }

        with open(
            os.path.join(self.result_path, "_evaluations.json"), "w"
        ) as json_file:
            json.dump(evaluations_objects, json_file)

    def_prepare_and_save_benchmark_results(self):
"""Get mean score across all of the evaluated examples-predictions."""
        _, mean_correctness_df = get_eval_results_df(
            ["base_rag"] * len(self.evals["correctness"]),
            self.evals["correctness"],
            metric="correctness",
        )
        _, mean_relevancy_df = get_eval_results_df(
            ["base_rag"] * len(self.evals["relevancy"]),
            self.evals["relevancy"],
            metric="relevancy",
        )
        _, mean_faithfulness_df = get_eval_results_df(
            ["base_rag"] * len(self.evals["faithfulness"]),
            self.evals["faithfulness"],
            metric="faithfulness",
        )
        _, mean_context_similarity_df = get_eval_results_df(
            ["base_rag"] * len(self.evals["context_similarity"]),
            self.evals["context_similarity"],
            metric="context_similarity",
        )

        mean_scores_df = pd.concat(
            [
                mean_correctness_df.reset_index(),
                mean_relevancy_df.reset_index(),
                mean_faithfulness_df.reset_index(),
                mean_context_similarity_df.reset_index(),
            ],
            axis=0,
            ignore_index=True,
        )
        mean_scores_df = mean_scores_df.set_index("index")
        mean_scores_df.index = mean_scores_df.index.set_names(["metrics"])

        # save mean_scores_df
        mean_scores_df.to_csv(os.path.join(self.result_path, "benchmark.csv"))
        return mean_scores_df

    def_make_evaluations(
        self,
        batch_size,
        sleep_time_in_seconds,
    ):
"""Sync make evaluations."""
        judges = self._prepare_judges()

        start_ix = self.eval_queue[0]
        for batch in self._batch_examples_and_preds(
            self.rag_dataset.examples,
            self.prediction_dataset.predictions,
            batch_size=batch_size,
            start_position=start_ix,
        ):
            examples, predictions = batch
            for example, prediction in tqdm.tqdm(zip(examples, predictions)):
                (
                    correctness_result,
                    relevancy_result,
                    faithfulness_result,
                    semantic_similarity_result,
                ) = self._evaluate_example_prediction(
                    judges=judges, example=example, prediction=prediction
                )

                self.evals["correctness"].append(correctness_result)
                self.evals["relevancy"].append(relevancy_result)
                self.evals["faithfulness"].append(faithfulness_result)
                self.evals["context_similarity"].append(semantic_similarity_result)
            time.sleep(sleep_time_in_seconds)

        self._save_evaluations()
        return self._prepare_and_save_benchmark_results()

    def_batch_examples_and_preds(
        self,
        examples: List[Any],
        predictions: List[Any],
        batch_size: int = 10,
        start_position: int = 0,
    ):
"""Batches examples and predictions with a given batch_size."""
        assert self._num_examples == len(predictions)
        for ndx in range(start_position, self._num_examples, batch_size):
            yield (
                examples[ndx : min(ndx + batch_size, self._num_examples)],
                predictions[ndx : min(ndx + batch_size, self._num_examples)],
            )

    async def_amake_evaluations(self, batch_size, sleep_time_in_seconds):
"""Async make evaluations."""
        judges = self._prepare_judges()

        ix = self.eval_queue[0]
        batch_iterator = self._batch_examples_and_preds(
            self.rag_dataset.examples,
            self.prediction_dataset.predictions,
            batch_size=batch_size,
            start_position=ix,
        )
        total_batches = (self._num_examples - ix + 1) / batch_size + (
            (self._num_examples - ix + 1) % batch_size != 0
        )
        if self.show_progress:
            batch_iterator = tqdm_asyncio(
                batch_iterator,
                desc="Batch processing of evaluations",
                total=total_batches,
            )

        for batch in batch_iterator:
            examples, predictions = batch
            tasks = []
            for example, prediction in zip(examples, predictions):
                (
                    correctness_task,
                    relevancy_task,
                    faithfulness_task,
                    semantic_similarity_task,
                ) = self._create_async_evaluate_example_prediction_tasks(
                    judges=judges,
                    example=example,
                    prediction=prediction,
                    sleep_time_in_seconds=sleep_time_in_seconds,
                )

                tasks += [
                    correctness_task,
                    relevancy_task,
                    faithfulness_task,
                    semantic_similarity_task,
                ]

            # do this in batches to avoid RateLimitError
            try:
                eval_results: List[EvaluationResult] = await asyncio.gather(*tasks)
            except RateLimitError as err:
                if self.show_progress:
                    batch_iterator.close()
                raise ValueError(
                    "You've hit rate limits on your OpenAI subscription. This"
                    " `RagEvaluatorPack` maintains state of evaluations. Simply"
                    " re-invoke .arun() in order to continue from where you left"
                    " off."
                ) fromerr
            # store in memory
            # since final result of eval_results respects order of inputs
            # just take appropriate slices
            self.evals["correctness"] += eval_results[::4]
            self.evals["relevancy"] += eval_results[1::4]
            self.evals["faithfulness"] += eval_results[2::4]
            self.evals["context_similarity"] += eval_results[3::4]
            # update queue
            for _ in range(batch_size):
                if self.eval_queue:
                    self.eval_queue.popleft()
            ix += 1
            if self.show_progress:
                batch_iterator.update()
                batch_iterator.refresh()

        self._save_evaluations()
        return self._prepare_and_save_benchmark_results()

    defrun(self, batch_size: int = 10, sleep_time_in_seconds: int = 1):
        if batch_size  10:
            warnings.warn(
                "You've set a large batch_size (>10). If using OpenAI GPT-4 as "
                " `judge_llm` (which is the default judge_llm),"
                " you may experience a RateLimitError. Previous successful eval "
                " responses are cached per batch. So hitting a RateLimitError"
                " would mean you'd lose all of the current batches successful "
                " GPT-4 calls."
            )
        if self.prediction_dataset is None:
            self._make_predictions(batch_size, sleep_time_in_seconds)

        # evaluate predictions
        eval_sleep_time_in_seconds = (
            sleep_time_in_seconds * 2
        )  # since we make 3 evaluator llm calls
        eval_batch_size = int(max(batch_size / 4, 1))
        return self._make_evaluations(
            batch_size=eval_batch_size, sleep_time_in_seconds=eval_sleep_time_in_seconds
        )

    async defarun(
        self,
        batch_size: int = 10,
        sleep_time_in_seconds: int = 1,
    ):
        if batch_size  10:
            warnings.warn(
                "You've set a large batch_size (>10). If using OpenAI GPT-4 as "
                " `judge_llm` (which is the default judge_llm),"
                " you may experience a RateLimitError. Previous successful eval "
                " responses are cached per batch. So hitting a RateLimitError"
                " would mean you'd lose all of the current batches successful "
                " GPT-4 calls."
            )

        # make predictions
        if self.prediction_dataset is None:
            await self._amake_predictions(batch_size, sleep_time_in_seconds)

        # evaluate predictions
        eval_sleep_time_in_seconds = (
            sleep_time_in_seconds * 2
        )  # since we make 3 evaluator llm calls and default is gpt-4
        # which is heavily rate-limited
        eval_batch_size = int(max(batch_size / 4, 1))
        return await self._amake_evaluations(
            batch_size=eval_batch_size, sleep_time_in_seconds=eval_sleep_time_in_seconds
        )

```
 |  
| --- | --- |  
options: members: - RagEvaluatorPack
