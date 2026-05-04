# Index
Dataset Module.
##  BaseLlamaDataExample [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataExample "Permanent link")
Bases: `BaseModel`
Base llama dataset example class.
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
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
```
 | 
```
classBaseLlamaDataExample(BaseModel):
"""Base llama dataset example class."""

    @property
    @abstractmethod
    defclass_name(self) -> str:
"""Class name."""
        return "BaseLlamaDataExample"

```
 |  
| --- | --- |  
###  class_name `abstractmethod` `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataExample.class_name "Permanent link")

```
class_name: 

```

Class name.
##  BaseLlamaDataset [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataset "Permanent link")
Bases: `BaseModel`, `Generic[P]`
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `examples`  |  `List[BaseLlamaDataExample[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataExample "BaseLlamaDataExample \(llama_index.core.llama_dataset.base.BaseLlamaDataExample\)")]`  |  Data examples of this dataset.  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
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
```
 | 
```
classBaseLlamaDataset(BaseModel, Generic[P]):
    _example_type: ClassVar[Type[BaseLlamaDataExample]]
    examples: List[BaseLlamaDataExample] = Field(
        default=[], description="Data examples of this dataset."
    )
    _predictions_cache: List[BaseLlamaExamplePrediction] = PrivateAttr(
        default_factory=list
    )

    def__getitem__(
        self, val: Union[slice, int]
    ) -> Union[Sequence[BaseLlamaDataExample], BaseLlamaDataExample]:
"""
        Enable slicing and indexing.

        Returns the desired slice on `examples`.
        """
        return self.examples[val]

    @abstractmethod
    defto_pandas(self) -> Any:
"""Create pandas dataframe."""

    defsave_json(self, path: str) -> None:
"""Save json."""
        with open(path, "w") as f:
            examples = [self._example_type.model_dump(el) for el in self.examples]
            data = {
                "examples": examples,
            }

            json.dump(data, f, indent=4)

    @classmethod
    deffrom_json(cls, path: str) -> "BaseLlamaDataset":
"""Load json."""
        with open(path) as f:
            data = json.load(f)

        examples = [cls._example_type.model_validate(el) for el in data["examples"]]

        return cls(
            examples=examples,
        )

    @abstractmethod
    def_construct_prediction_dataset(
        self, predictions: Sequence[BaseLlamaExamplePrediction]
    ) -> BaseLlamaPredictionDataset:
"""
        Construct the specific prediction dataset.

        Args:
            predictions (List[BaseLlamaExamplePrediction]): the list of predictions.

        Returns:
            BaseLlamaPredictionDataset: A dataset of predictions.

        """

    @abstractmethod
    def_predict_example(
        self,
        predictor: P,
        example: BaseLlamaDataExample,
        sleep_time_in_seconds: int = 0,
    ) -> BaseLlamaExamplePrediction:
"""
        Predict on a single example.

        NOTE: Subclasses need to implement this.

        Args:
            predictor (PredictorType): The predictor to make the prediction with.
            example (BaseLlamaDataExample): The example to predict on.

        Returns:
            BaseLlamaExamplePrediction: The prediction.

        """

    defmake_predictions_with(
        self,
        predictor: P,
        show_progress: bool = False,
        batch_size: int = 20,
        sleep_time_in_seconds: int = 0,
    ) -> BaseLlamaPredictionDataset:
"""
        Predict with a given query engine.

        Args:
            predictor (PredictorType): The predictor to make predictions with.
            show_progress (bool, optional): Show progress of making predictions.
            batch_size (int): Used to batch async calls, especially to reduce chances
                            of hitting RateLimitError from openai.
            sleep_time_in_seconds (int): Amount of time to sleep between batch call
                            to reduce chance of hitting RateLimitError from openai.

        Returns:
            BaseLlamaPredictionDataset: A dataset of predictions.

        """
        if self._predictions_cache:
            start_example_position = len(self._predictions_cache)
        else:
            start_example_position = 0

        for batch in self._batch_examples(
            batch_size=batch_size, start_position=start_example_position
        ):
            if show_progress:
                example_iterator = tqdm.tqdm(batch)
            else:
                example_iterator = batch
            for example in example_iterator:
                self._predictions_cache.append(
                    self._predict_example(predictor, example, sleep_time_in_seconds)
                )

        return self._construct_prediction_dataset(predictions=self._predictions_cache)

    # async methods
    @abstractmethod
    async def_apredict_example(
        self,
        predictor: P,
        example: BaseLlamaDataExample,
        sleep_time_in_seconds: int,
    ) -> BaseLlamaExamplePrediction:
"""
        Async predict on a single example.

        NOTE: Subclasses need to implement this.

        Args:
            predictor (PredictorType): The predictor to make the prediction with.
            example (BaseLlamaDataExample): The example to predict on.

        Returns:
            BaseLlamaExamplePrediction: The prediction.

        """

    def_batch_examples(
        self,
        batch_size: int = 20,
        start_position: int = 0,
    ) -> Generator[Sequence[BaseLlamaDataExample], None, None]:
"""Batches examples and predictions with a given batch_size."""
        num_examples = len(self.examples)
        for ndx in range(start_position, num_examples, batch_size):
            yield self.examples[ndx : min(ndx + batch_size, num_examples)]

    async defamake_predictions_with(
        self,
        predictor: P,
        show_progress: bool = False,
        batch_size: int = 20,
        sleep_time_in_seconds: int = 1,
    ) -> BaseLlamaPredictionDataset:
"""
        Async predict with a given query engine.

        Args:
            predictor (PredictorType): The predictor to make predictions with.
            show_progress (bool, optional): Show progress of making predictions.
            batch_size (int): Used to batch async calls, especially to reduce chances
                            of hitting RateLimitError from openai.
            sleep_time_in_seconds (int): Amount of time to sleep between batch call
                            to reduce chance of hitting RateLimitError from openai.

        Returns:
            BaseLlamaPredictionDataset: A dataset of predictions.

        """
        if self._predictions_cache:
            start_example_position = len(self._predictions_cache)
        else:
            start_example_position = 0

        for batch in self._batch_examples(
            batch_size=batch_size, start_position=start_example_position
        ):
            tasks = []
            for example in batch:
                tasks.append(
                    self._apredict_example(predictor, example, sleep_time_in_seconds)
                )
            asyncio_mod = asyncio_module(show_progress=show_progress)

            try:
                if show_progress:
                    batch_predictions = await asyncio_mod.gather(
                        *tasks, desc="Batch processing of predictions"
                    )
                else:
                    batch_predictions = await asyncio_mod.gather(*tasks)
            except Exception as err:
                if show_progress:
                    asyncio_mod.close()

                if "RateLimitError" in str(err):
                    raise ValueError(
                        "You've hit rate limits on your OpenAI subscription. This"
                        " class caches previous predictions after each successful"
                        " batch execution. Based off this cache, when executing this"
                        " command again it will attempt to predict on only the examples "
                        "that have not yet been predicted. Try reducing your batch_size."
                    ) fromerr
                else:
                    raise err  # noqa: TRY201

            self._predictions_cache += batch_predictions
            # time.sleep(sleep_time_in_seconds)

        prediction_dataset = self._construct_prediction_dataset(
            predictions=self._predictions_cache
        )
        self._predictions_cache = []  # clear cache
        return prediction_dataset

    @property
    @abstractmethod
    defclass_name(self) -> str:
"""Class name."""
        return "BaseLlamaDataset"

```
 |  
| --- | --- |  
###  class_name `abstractmethod` `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataset.class_name "Permanent link")

```
class_name: 

```

Class name.
###  to_pandas `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataset.to_pandas "Permanent link")

```
to_pandas() -> 

```

Create pandas dataframe.
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
| 
```
149
150
151
```
 | 
```
@abstractmethod
defto_pandas(self) -> Any:
"""Create pandas dataframe."""

```
 |  
| --- | --- |  
###  save_json [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataset.save_json "Permanent link")

```
save_json(path: ) -> None

```

Save json.
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
| 
```
153
154
155
156
157
158
159
160
161
```
 | 
```
defsave_json(self, path: str) -> None:
"""Save json."""
    with open(path, "w") as f:
        examples = [self._example_type.model_dump(el) for el in self.examples]
        data = {
            "examples": examples,
        }

        json.dump(data, f, indent=4)

```
 |  
| --- | --- |  
###  from_json `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataset.from_json "Permanent link")

```
from_json(path: ) -> 

```

Load json.
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_json(cls, path: str) -> "BaseLlamaDataset":
"""Load json."""
    with open(path) as f:
        data = json.load(f)

    examples = [cls._example_type.model_validate(el) for el in data["examples"]]

    return cls(
        examples=examples,
    )

```
 |  
| --- | --- |  
###  make_predictions_with [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataset.make_predictions_with "Permanent link")

```
make_predictions_with(
    predictor: ,
    show_progress:  = False,
    batch_size:  = 20,
    sleep_time_in_seconds:  = 0,
) -> 

```

Predict with a given query engine.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `predictor`  |  `PredictorType`  |  The predictor to make predictions with.  |  _required_  |  
|  `show_progress`  |  `bool`  |  Show progress of making predictions.  |  `False`  |  
|  `batch_size`  |  Used to batch async calls, especially to reduce chances of hitting RateLimitError from openai.  |  
|  `sleep_time_in_seconds`  |  Amount of time to sleep between batch call to reduce chance of hitting RateLimitError from openai.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `BaseLlamaPredictionDataset`  |   |  A dataset of predictions.  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
| 
```
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
```
 | 
```
defmake_predictions_with(
    self,
    predictor: P,
    show_progress: bool = False,
    batch_size: int = 20,
    sleep_time_in_seconds: int = 0,
) -> BaseLlamaPredictionDataset:
"""
    Predict with a given query engine.

    Args:
        predictor (PredictorType): The predictor to make predictions with.
        show_progress (bool, optional): Show progress of making predictions.
        batch_size (int): Used to batch async calls, especially to reduce chances
                        of hitting RateLimitError from openai.
        sleep_time_in_seconds (int): Amount of time to sleep between batch call
                        to reduce chance of hitting RateLimitError from openai.

    Returns:
        BaseLlamaPredictionDataset: A dataset of predictions.

    """
    if self._predictions_cache:
        start_example_position = len(self._predictions_cache)
    else:
        start_example_position = 0

    for batch in self._batch_examples(
        batch_size=batch_size, start_position=start_example_position
    ):
        if show_progress:
            example_iterator = tqdm.tqdm(batch)
        else:
            example_iterator = batch
        for example in example_iterator:
            self._predictions_cache.append(
                self._predict_example(predictor, example, sleep_time_in_seconds)
            )

    return self._construct_prediction_dataset(predictions=self._predictions_cache)

```
 |  
| --- | --- |  
###  amake_predictions_with [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataset.amake_predictions_with "Permanent link")

```
amake_predictions_with(
    predictor: ,
    show_progress:  = False,
    batch_size:  = 20,
    sleep_time_in_seconds:  = 1,
) -> 

```

Async predict with a given query engine.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `predictor`  |  `PredictorType`  |  The predictor to make predictions with.  |  _required_  |  
|  `show_progress`  |  `bool`  |  Show progress of making predictions.  |  `False`  |  
|  `batch_size`  |  Used to batch async calls, especially to reduce chances of hitting RateLimitError from openai.  |  
|  `sleep_time_in_seconds`  |  Amount of time to sleep between batch call to reduce chance of hitting RateLimitError from openai.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `BaseLlamaPredictionDataset`  |   |  A dataset of predictions.  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
| 
```
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
```
 | 
```
async defamake_predictions_with(
    self,
    predictor: P,
    show_progress: bool = False,
    batch_size: int = 20,
    sleep_time_in_seconds: int = 1,
) -> BaseLlamaPredictionDataset:
"""
    Async predict with a given query engine.

    Args:
        predictor (PredictorType): The predictor to make predictions with.
        show_progress (bool, optional): Show progress of making predictions.
        batch_size (int): Used to batch async calls, especially to reduce chances
                        of hitting RateLimitError from openai.
        sleep_time_in_seconds (int): Amount of time to sleep between batch call
                        to reduce chance of hitting RateLimitError from openai.

    Returns:
        BaseLlamaPredictionDataset: A dataset of predictions.

    """
    if self._predictions_cache:
        start_example_position = len(self._predictions_cache)
    else:
        start_example_position = 0

    for batch in self._batch_examples(
        batch_size=batch_size, start_position=start_example_position
    ):
        tasks = []
        for example in batch:
            tasks.append(
                self._apredict_example(predictor, example, sleep_time_in_seconds)
            )
        asyncio_mod = asyncio_module(show_progress=show_progress)

        try:
            if show_progress:
                batch_predictions = await asyncio_mod.gather(
                    *tasks, desc="Batch processing of predictions"
                )
            else:
                batch_predictions = await asyncio_mod.gather(*tasks)
        except Exception as err:
            if show_progress:
                asyncio_mod.close()

            if "RateLimitError" in str(err):
                raise ValueError(
                    "You've hit rate limits on your OpenAI subscription. This"
                    " class caches previous predictions after each successful"
                    " batch execution. Based off this cache, when executing this"
                    " command again it will attempt to predict on only the examples "
                    "that have not yet been predicted. Try reducing your batch_size."
                ) fromerr
            else:
                raise err  # noqa: TRY201

        self._predictions_cache += batch_predictions
        # time.sleep(sleep_time_in_seconds)

    prediction_dataset = self._construct_prediction_dataset(
        predictions=self._predictions_cache
    )
    self._predictions_cache = []  # clear cache
    return prediction_dataset

```
 |  
| --- | --- |  
##  BaseLlamaExamplePrediction [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaExamplePrediction "Permanent link")
Bases: `BaseModel`
Base llama dataset example class.
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
| 
```
55
56
57
58
59
60
61
62
```
 | 
```
classBaseLlamaExamplePrediction(BaseModel):
"""Base llama dataset example class."""

    @property
    @abstractmethod
    defclass_name(self) -> str:
"""Class name."""
        return "BaseLlamaPrediction"

```
 |  
| --- | --- |  
###  class_name `abstractmethod` `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaExamplePrediction.class_name "Permanent link")

```
class_name: 

```

Class name.
##  BaseLlamaPredictionDataset [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaPredictionDataset "Permanent link")
Bases: `BaseModel`
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `predictions`  |  `List[BaseLlamaExamplePrediction[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaExamplePrediction "BaseLlamaExamplePrediction \(llama_index.core.llama_dataset.base.BaseLlamaExamplePrediction\)")]`  |  Predictions on train_examples.  |  `<dynamic>`  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
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
```
 | 
```
classBaseLlamaPredictionDataset(BaseModel):
    _prediction_type: ClassVar[Type[BaseLlamaExamplePrediction]]
    predictions: List[BaseLlamaExamplePrediction] = Field(
        default_factory=list, description="Predictions on train_examples."
    )

    def__getitem__(
        self, val: Union[slice, int]
    ) -> Union[Sequence[BaseLlamaExamplePrediction], BaseLlamaExamplePrediction]:
"""
        Enable slicing and indexing.

        Returns the desired slice on `predictions`.
        """
        return self.predictions[val]

    @abstractmethod
    defto_pandas(self) -> Any:
"""Create pandas dataframe."""

    defsave_json(self, path: str) -> None:
"""Save json."""
        with open(path, "w") as f:
            predictions = None
            if self.predictions:
                predictions = [
                    self._prediction_type.model_dump(el) for el in self.predictions
                ]
            data = {
                "predictions": predictions,
            }

            json.dump(data, f, indent=4)

    @classmethod
    deffrom_json(cls, path: str) -> "BaseLlamaPredictionDataset":
"""Load json."""
        with open(path) as f:
            data = json.load(f)

        predictions = [
            cls._prediction_type.model_validate(el) for el in data["predictions"]
        ]

        return cls(
            predictions=predictions,
        )

    @property
    @abstractmethod
    defclass_name(self) -> str:
"""Class name."""
        return "BaseLlamaPredictionDataset"

```
 |  
| --- | --- |  
###  class_name `abstractmethod` `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaPredictionDataset.class_name "Permanent link")

```
class_name: 

```

Class name.
###  to_pandas `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaPredictionDataset.to_pandas "Permanent link")

```
to_pandas() -> 

```

Create pandas dataframe.
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
| 
```
91
92
93
```
 | 
```
@abstractmethod
defto_pandas(self) -> Any:
"""Create pandas dataframe."""

```
 |  
| --- | --- |  
###  save_json [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaPredictionDataset.save_json "Permanent link")

```
save_json(path: ) -> None

```

Save json.
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
| 
```
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
```
 | 
```
defsave_json(self, path: str) -> None:
"""Save json."""
    with open(path, "w") as f:
        predictions = None
        if self.predictions:
            predictions = [
                self._prediction_type.model_dump(el) for el in self.predictions
            ]
        data = {
            "predictions": predictions,
        }

        json.dump(data, f, indent=4)

```
 |  
| --- | --- |  
###  from_json `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaPredictionDataset.from_json "Permanent link")

```
from_json(path: ) -> 

```

Load json.
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_json(cls, path: str) -> "BaseLlamaPredictionDataset":
"""Load json."""
    with open(path) as f:
        data = json.load(f)

    predictions = [
        cls._prediction_type.model_validate(el) for el in data["predictions"]
    ]

    return cls(
        predictions=predictions,
    )

```
 |  
| --- | --- |  
##  CreatedBy [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.CreatedBy "Permanent link")
Bases: `BaseModel`
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_name`  |  `str | None`  |  When CreatedByType.AI, specify model name.  |  `<class 'str'>`  |  
|  `type`  |   |  _required_  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
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
```
 | 
```
classCreatedBy(BaseModel):
    model_config = ConfigDict(protected_namespaces=("pydantic_model_",))
    model_name: Optional[str] = Field(
        default_factory=str, description="When CreatedByType.AI, specify model name."
    )
    type: CreatedByType

    def__str__(self) -> str:
        if self.type == "ai":
            return f"{self.type!s} ({self.model_name})"
        else:
            return str(self.type)

```
 |  
| --- | --- |  
##  CreatedByType [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.CreatedByType "Permanent link")
Bases: `str`, `Enum`
The kinds of rag data examples.
Source code in `llama-index-core/llama_index/core/llama_dataset/base.py`  
| 
```
31
32
33
34
35
36
37
38
```
 | 
```
classCreatedByType(str, Enum):
"""The kinds of rag data examples."""

    HUMAN = "human"
    AI = "ai"

    def__str__(self) -> str:
        return self.value

```
 |  
| --- | --- |  
##  EvaluatorExamplePrediction [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.EvaluatorExamplePrediction "Permanent link")
Bases: 
Evaluation example prediction class.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `feedback`  |  The evaluator's feedback.  |  `<class 'str'>`  |  
|  `score`  |  `float | None`  |  The evaluator's score.  |  `None`  |  
|  `invalid_prediction`  |  `bool`  |  Whether or not the prediction is a valid one.  |  `False`  |  
|  `invalid_reason`  |  `str | None`  |  Reason as to why prediction is invalid.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/evaluator_evaluation.py`  
| 
```
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
classEvaluatorExamplePrediction(BaseLlamaExamplePrediction):
"""
    Evaluation example prediction class.

    Args:
        feedback (Optional[str]): The evaluator's feedback.
        score (Optional[float]): The evaluator's score.

    """

    feedback: str = Field(
        default_factory=str,
        description="The generated (predicted) response that can be compared to a reference (ground-truth) answer.",
    )
    score: Optional[float] = Field(
        default=None,
        description="The generated (predicted) response that can be compared to a reference (ground-truth) answer.",
    )
    invalid_prediction: bool = Field(
        default=False, description="Whether or not the prediction is a valid one."
    )
    invalid_reason: Optional[str] = Field(
        default=None, description="Reason as to why prediction is invalid."
    )

    @property
    defclass_name(self) -> str:
"""Data example class name."""
        return "EvaluatorExamplePrediction"

```
 |  
| --- | --- |  
###  class_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.EvaluatorExamplePrediction.class_name "Permanent link")

```
class_name: 

```

Data example class name.
##  EvaluatorPredictionDataset [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.EvaluatorPredictionDataset "Permanent link")
Bases: 
Evaluation Prediction Dataset Class.
Source code in `llama-index-core/llama_index/core/llama_dataset/evaluator_evaluation.py`  
| 
```
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
classEvaluatorPredictionDataset(BaseLlamaPredictionDataset):
"""Evaluation Prediction Dataset Class."""

    _prediction_type = EvaluatorExamplePrediction

    defto_pandas(self) -> Any:
"""Create pandas dataframe."""
        try:
            importpandasaspd
        except ImportError:
            raise ImportError(
                "pandas is required for this function. Please install it with `pip install pandas`."
            )

        data: Dict[str, List] = {
            "feedback": [],
            "score": [],
        }
        for pred in self.predictions:
            if not isinstance(pred, EvaluatorExamplePrediction):
                raise ValueError(
                    "EvaluatorPredictionDataset can only contain EvaluatorExamplePrediction instances."
                )
            data["feedback"].append(pred.feedback)
            data["score"].append(pred.score)

        return pd.DataFrame(data)

    @property
    defclass_name(self) -> str:
"""Class name."""
        return "EvaluatorPredictionDataset"

```
 |  
| --- | --- |  
###  class_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.EvaluatorPredictionDataset.class_name "Permanent link")

```
class_name: 

```

Class name.
###  to_pandas [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.EvaluatorPredictionDataset.to_pandas "Permanent link")

```
to_pandas() -> 

```

Create pandas dataframe.
Source code in `llama-index-core/llama_index/core/llama_dataset/evaluator_evaluation.py`  
| 
```
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
```
 | 
```
defto_pandas(self) -> Any:
"""Create pandas dataframe."""
    try:
        importpandasaspd
    except ImportError:
        raise ImportError(
            "pandas is required for this function. Please install it with `pip install pandas`."
        )

    data: Dict[str, List] = {
        "feedback": [],
        "score": [],
    }
    for pred in self.predictions:
        if not isinstance(pred, EvaluatorExamplePrediction):
            raise ValueError(
                "EvaluatorPredictionDataset can only contain EvaluatorExamplePrediction instances."
            )
        data["feedback"].append(pred.feedback)
        data["score"].append(pred.score)

    return pd.DataFrame(data)

```
 |  
| --- | --- |  
##  LabelledEvaluatorDataExample [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledEvaluatorDataExample "Permanent link")
Bases: 
Evaluation example class.
This data class contains the ingredients to perform a new "prediction" i.e., evaluation. Here an evaluator is meant to evaluate a response against an associated query as well as optionally contexts.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The user query  |  `<class 'str'>`  |  
|  `query_by`  |  `CreatedBy[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.CreatedBy "CreatedBy \(llama_index.core.llama_dataset.base.CreatedBy\)") | None`  |  Query generated by human or ai (model-name)  |  `None`  |  
|  `contexts`  |  `List[str] | None`  |  The contexts used for response  |  `None`  |  
|  `answer`  |  Answer to the query that is to be evaluated.  |  `<class 'str'>`  |  
|  `answer_by`  |  `CreatedBy[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.CreatedBy "CreatedBy \(llama_index.core.llama_dataset.base.CreatedBy\)") | None`  |  The reference answer generated by human or ai (model-name).  |  `None`  |  
|  `ground_truth_answer`  |  `str | None`  |  `None`  |  
|  `ground_truth_answer_by`  |  `CreatedBy[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.CreatedBy "CreatedBy \(llama_index.core.llama_dataset.base.CreatedBy\)") | None`  |  `None`  |  
|  `reference_feedback`  |  `str | None`  |  The reference feedback evaluation.  |  `None`  |  
|  `reference_score`  |  `float`  |  The reference score evaluation.  |  `<dynamic>`  |  
|  `reference_evaluation_by`  |  `CreatedBy[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.CreatedBy "CreatedBy \(llama_index.core.llama_dataset.base.CreatedBy\)") | None`  |  Evaluation generated by human or ai (model-name)  |  `None`  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/evaluator_evaluation.py`  
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
```
 | 
```
classLabelledEvaluatorDataExample(BaseLlamaDataExample):
"""
    Evaluation example class.

    This data class contains the ingredients to perform a new "prediction" i.e.,
    evaluation. Here an evaluator is meant to evaluate a response against an
    associated query as well as optionally contexts.

    Args:
        query (str): The user query
        query_by (CreatedBy): Query generated by human or ai (model-name)
        contexts (Optional[List[str]]): The contexts used for response
        answer (str): Answer to the query that is to be evaluated.
        answer_by: The reference answer generated by human or ai (model-name).
        ground_truth_answer (Optional[str]):
        ground_truth_answer_by (Optional[CreatedBy]):
        reference_feedback (str): The reference feedback evaluation.
        reference_score (float): The reference score evaluation.
        reference_evaluation_by (CreatedBy): Evaluation generated by human or ai (model-name)

    """

    query: str = Field(
        default_factory=str, description="The user query for the example."
    )
    query_by: Optional[CreatedBy] = Field(
        default=None, description="What generated the query."
    )
    contexts: Optional[List[str]] = Field(
        default=None,
        description="The contexts used to generate the answer.",
    )
    answer: str = Field(
        default_factory=str,
        description="The provided answer to the example that is to be evaluated.",
    )
    answer_by: Optional[CreatedBy] = Field(
        default=None, description="What generated the answer."
    )
    ground_truth_answer: Optional[str] = Field(
        default=None,
        description="The ground truth answer to the example that is used to evaluate the provided `answer`.",
    )
    ground_truth_answer_by: Optional[CreatedBy] = Field(
        default=None, description="What generated the ground-truth answer."
    )
    reference_feedback: Optional[str] = Field(
        default=None,
        description="The reference feedback (ground-truth).",
    )
    reference_score: float = Field(
        default_factory=float, description="The reference score (ground-truth)."
    )
    reference_evaluation_by: Optional[CreatedBy] = Field(
        default=None, description="What generated the evaluation (feedback and score)."
    )

    @property
    defclass_name(self) -> str:
"""Data example class name."""
        return "LabelledEvaluatorDataExample"

```
 |  
| --- | --- |  
###  class_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledEvaluatorDataExample.class_name "Permanent link")

```
class_name: 

```

Data example class name.
##  LabelledEvaluatorDataset [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledEvaluatorDataset "Permanent link")
Bases: `BaseLlamaDataset[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataset "BaseLlamaDataset \(llama_index.core.llama_dataset.base.BaseLlamaDataset\)")[BaseEvaluator[](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseEvaluator "BaseEvaluator \(llama_index.core.evaluation.BaseEvaluator\)")]`
LabelledEvalationDataset class.
Source code in `llama-index-core/llama_index/core/llama_dataset/evaluator_evaluation.py`  
| 
```
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
```
 | 
```
classLabelledEvaluatorDataset(BaseLlamaDataset[BaseEvaluator]):
"""LabelledEvalationDataset class."""

    _example_type = LabelledEvaluatorDataExample

    defto_pandas(self) -> Any:
"""Create pandas dataframe."""
        try:
            importpandasaspd
        except ImportError:
            raise ImportError(
                "pandas is required for this function. Please install it with `pip install pandas`."
            )

        data: Dict[str, List] = {
            "query": [],
            "answer": [],
            "contexts": [],
            "ground_truth_answer": [],
            "query_by": [],
            "answer_by": [],
            "ground_truth_answer_by": [],
            "reference_feedback": [],
            "reference_score": [],
            "reference_evaluation_by": [],
        }

        for example in self.examples:
            if not isinstance(example, LabelledEvaluatorDataExample):
                raise ValueError(
                    "LabelledEvaluatorDataset can only contain LabelledEvaluatorDataExample instances."
                )
            data["query"].append(example.query)
            data["answer"].append(example.answer)
            data["contexts"].append(example.contexts)
            data["ground_truth_answer"].append(example.ground_truth_answer)
            data["query_by"].append(str(example.query_by))
            data["answer_by"].append(str(example.answer_by))
            data["ground_truth_answer_by"].append(str(example.ground_truth_answer_by))
            data["reference_feedback"].append(example.reference_feedback)
            data["reference_score"].append(example.reference_score)
            data["reference_evaluation_by"].append(str(example.reference_evaluation_by))

        return pd.DataFrame(data)

    async def_apredict_example(  # type: ignore
        self,
        predictor: BaseEvaluator,
        example: LabelledEvaluatorDataExample,
        sleep_time_in_seconds: int,
    ) -> EvaluatorExamplePrediction:
"""Async predict RAG example with a query engine."""
        await asyncio.sleep(sleep_time_in_seconds)
        try:
            eval_result: EvaluationResult = await predictor.aevaluate(
                query=example.query,
                response=example.answer,
                contexts=example.contexts,
                reference=example.ground_truth_answer,
                sleep_time_in_seconds=sleep_time_in_seconds,
            )
        except Exception as err:
            # TODO: raise warning here as well
            return EvaluatorExamplePrediction(
                invalid_prediction=True, invalid_reason=f"Caught error {err!s}"
            )

        if not eval_result.invalid_result:
            return EvaluatorExamplePrediction(
                feedback=eval_result.feedback or "", score=eval_result.score
            )
        else:
            return EvaluatorExamplePrediction(
                invalid_prediction=True, invalid_reason=eval_result.invalid_reason
            )

    def_predict_example(  # type: ignore
        self,
        predictor: BaseEvaluator,
        example: LabelledEvaluatorDataExample,
        sleep_time_in_seconds: int = 0,
    ) -> EvaluatorExamplePrediction:
"""Predict RAG example with a query engine."""
        time.sleep(sleep_time_in_seconds)
        try:
            eval_result: EvaluationResult = predictor.evaluate(
                query=example.query,
                response=example.answer,
                contexts=example.contexts,
                reference=example.ground_truth_answer,
                sleep_time_in_seconds=sleep_time_in_seconds,
            )
        except Exception as err:
            # TODO: raise warning here as well
            return EvaluatorExamplePrediction(
                invalid_prediction=True, invalid_reason=f"Caught error {err!s}"
            )

        if not eval_result.invalid_result:
            return EvaluatorExamplePrediction(
                feedback=eval_result.feedback or "", score=eval_result.score
            )
        else:
            return EvaluatorExamplePrediction(
                invalid_prediction=True, invalid_reason=eval_result.invalid_reason
            )

    def_construct_prediction_dataset(  # type: ignore
        self, predictions: Sequence[EvaluatorExamplePrediction]
    ) -> EvaluatorPredictionDataset:
"""Construct prediction dataset."""
        return EvaluatorPredictionDataset(predictions=predictions)

    @property
    defclass_name(self) -> str:
"""Class name."""
        return "LabelledEvaluatorDataset"

```
 |  
| --- | --- |  
###  class_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledEvaluatorDataset.class_name "Permanent link")

```
class_name: 

```

Class name.
###  to_pandas [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledEvaluatorDataset.to_pandas "Permanent link")

```
to_pandas() -> 

```

Create pandas dataframe.
Source code in `llama-index-core/llama_index/core/llama_dataset/evaluator_evaluation.py`  
| 
```
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
```
 | 
```
defto_pandas(self) -> Any:
"""Create pandas dataframe."""
    try:
        importpandasaspd
    except ImportError:
        raise ImportError(
            "pandas is required for this function. Please install it with `pip install pandas`."
        )

    data: Dict[str, List] = {
        "query": [],
        "answer": [],
        "contexts": [],
        "ground_truth_answer": [],
        "query_by": [],
        "answer_by": [],
        "ground_truth_answer_by": [],
        "reference_feedback": [],
        "reference_score": [],
        "reference_evaluation_by": [],
    }

    for example in self.examples:
        if not isinstance(example, LabelledEvaluatorDataExample):
            raise ValueError(
                "LabelledEvaluatorDataset can only contain LabelledEvaluatorDataExample instances."
            )
        data["query"].append(example.query)
        data["answer"].append(example.answer)
        data["contexts"].append(example.contexts)
        data["ground_truth_answer"].append(example.ground_truth_answer)
        data["query_by"].append(str(example.query_by))
        data["answer_by"].append(str(example.answer_by))
        data["ground_truth_answer_by"].append(str(example.ground_truth_answer_by))
        data["reference_feedback"].append(example.reference_feedback)
        data["reference_score"].append(example.reference_score)
        data["reference_evaluation_by"].append(str(example.reference_evaluation_by))

    return pd.DataFrame(data)

```
 |  
| --- | --- |  
##  LabelledPairwiseEvaluatorDataExample [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledPairwiseEvaluatorDataExample "Permanent link")
Bases: 
Labelled pairwise evaluation data example class.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `second_answer`  |  The second answer to the example that is to be evaluated along versus `answer`.  |  `<class 'str'>`  |  
|  `second_answer_by`  |  `CreatedBy[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.CreatedBy "CreatedBy \(llama_index.core.llama_dataset.base.CreatedBy\)") | None`  |  What generated the second answer.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/evaluator_evaluation.py`  
| 
```
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
```
 | 
```
classLabelledPairwiseEvaluatorDataExample(LabelledEvaluatorDataExample):
"""Labelled pairwise evaluation data example class."""

    second_answer: str = Field(
        default_factory=str,
        description="The second answer to the example that is to be evaluated along versus `answer`.",
    )
    second_answer_by: Optional[CreatedBy] = Field(
        default=None, description="What generated the second answer."
    )

    @property
    defclass_name(self) -> str:
"""Data example class name."""
        return "LabelledPairwiseEvaluatorDataExample"

```
 |  
| --- | --- |  
###  class_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledPairwiseEvaluatorDataExample.class_name "Permanent link")

```
class_name: 

```

Data example class name.
##  LabelledPairwiseEvaluatorDataset [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledPairwiseEvaluatorDataset "Permanent link")
Bases: `BaseLlamaDataset[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataset "BaseLlamaDataset \(llama_index.core.llama_dataset.base.BaseLlamaDataset\)")[BaseEvaluator[](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/#llama_index.core.evaluation.BaseEvaluator "BaseEvaluator \(llama_index.core.evaluation.BaseEvaluator\)")]`
Labelled pairwise evaluation dataset. For evaluating the evaluator in performing pairwise evaluations.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `BaseLlamaDataset`  |  `_type_`  |  _description_  |  _required_  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/evaluator_evaluation.py`  
| 
```
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
```
 | 
```
classLabelledPairwiseEvaluatorDataset(BaseLlamaDataset[BaseEvaluator]):
"""
    Labelled pairwise evaluation dataset. For evaluating the evaluator in
    performing pairwise evaluations.

    Args:
        BaseLlamaDataset (_type_): _description_

    """

    _example_type = LabelledPairwiseEvaluatorDataExample

    defto_pandas(self) -> Any:
"""Create pandas dataframe."""
        try:
            importpandasaspd
        except ImportError:
            raise ImportError(
                "pandas is required for this function. Please install it with `pip install pandas`."
            )

        data: Dict[str, List] = {
            "query": [],
            "answer": [],
            "second_answer": [],
            "contexts": [],
            "ground_truth_answer": [],
            "query_by": [],
            "answer_by": [],
            "second_answer_by": [],
            "ground_truth_answer_by": [],
            "reference_feedback": [],
            "reference_score": [],
            "reference_evaluation_by": [],
        }
        for example in self.examples:
            if not isinstance(example, LabelledPairwiseEvaluatorDataExample):
                raise ValueError(
                    "LabelledPairwiseEvaluatorDataset can only contain LabelledPairwiseEvaluatorDataExample instances."
                )
            data["query"].append(example.query)
            data["answer"].append(example.answer)
            data["second_answer"].append(example.second_answer)
            data["contexts"].append(example.contexts)
            data["ground_truth_answer"].append(example.ground_truth_answer)
            data["query_by"].append(str(example.query_by))
            data["answer_by"].append(str(example.answer_by))
            data["second_answer_by"].append(str(example.second_answer_by))
            data["ground_truth_answer_by"].append(str(example.ground_truth_answer_by))
            data["reference_feedback"].append(example.reference_feedback)
            data["reference_score"].append(example.reference_score)
            data["reference_evaluation_by"].append(str(example.reference_evaluation_by))

        return pd.DataFrame(data)

    async def_apredict_example(  # type: ignore
        self,
        predictor: BaseEvaluator,
        example: LabelledPairwiseEvaluatorDataExample,
        sleep_time_in_seconds: int,
    ) -> PairwiseEvaluatorExamplePrediction:
"""Async predict evaluation example with an Evaluator."""
        await asyncio.sleep(sleep_time_in_seconds)
        try:
            eval_result: EvaluationResult = await predictor.aevaluate(
                query=example.query,
                response=example.answer,
                second_response=example.second_answer,
                contexts=example.contexts,
                reference=example.ground_truth_answer,
                sleep_time_in_seconds=sleep_time_in_seconds,
            )
        except Exception as err:
            # TODO: raise warning here as well
            return PairwiseEvaluatorExamplePrediction(
                invalid_prediction=True, invalid_reason=f"Caught error {err!s}"
            )

        if not eval_result.invalid_result:
            return PairwiseEvaluatorExamplePrediction(
                feedback=eval_result.feedback or "",
                score=eval_result.score,
                evaluation_source=EvaluationSource(eval_result.pairwise_source),
            )
        else:
            return PairwiseEvaluatorExamplePrediction(
                invalid_prediction=True, invalid_reason=eval_result.invalid_reason
            )

    def_predict_example(  # type: ignore
        self,
        predictor: BaseEvaluator,
        example: LabelledPairwiseEvaluatorDataExample,
        sleep_time_in_seconds: int = 0,
    ) -> PairwiseEvaluatorExamplePrediction:
"""Predict RAG example with a query engine."""
        time.sleep(sleep_time_in_seconds)
        try:
            eval_result: EvaluationResult = predictor.evaluate(
                query=example.query,
                response=example.answer,
                second_response=example.second_answer,
                contexts=example.contexts,
                reference=example.ground_truth_answer,
                sleep_time_in_seconds=sleep_time_in_seconds,
            )
        except Exception as err:
            # TODO: raise warning here as well
            return PairwiseEvaluatorExamplePrediction(
                invalid_prediction=True, invalid_reason=f"Caught error {err!s}"
            )

        if not eval_result.invalid_result:
            return PairwiseEvaluatorExamplePrediction(
                feedback=eval_result.feedback or "",
                score=eval_result.score,
                evaluation_source=EvaluationSource(eval_result.pairwise_source),
            )
        else:
            return PairwiseEvaluatorExamplePrediction(
                invalid_prediction=True, invalid_reason=eval_result.invalid_reason
            )

    def_construct_prediction_dataset(  # type: ignore
        self, predictions: Sequence[PairwiseEvaluatorExamplePrediction]
    ) -> PairwiseEvaluatorPredictionDataset:
"""Construct prediction dataset."""
        return PairwiseEvaluatorPredictionDataset(predictions=predictions)

    @property
    defclass_name(self) -> str:
"""Class name."""
        return "LabelledPairwiseEvaluatorDataset"

```
 |  
| --- | --- |  
###  class_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledPairwiseEvaluatorDataset.class_name "Permanent link")

```
class_name: 

```

Class name.
###  to_pandas [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledPairwiseEvaluatorDataset.to_pandas "Permanent link")

```
to_pandas() -> 

```

Create pandas dataframe.
Source code in `llama-index-core/llama_index/core/llama_dataset/evaluator_evaluation.py`  
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
```
 | 
```
defto_pandas(self) -> Any:
"""Create pandas dataframe."""
    try:
        importpandasaspd
    except ImportError:
        raise ImportError(
            "pandas is required for this function. Please install it with `pip install pandas`."
        )

    data: Dict[str, List] = {
        "query": [],
        "answer": [],
        "second_answer": [],
        "contexts": [],
        "ground_truth_answer": [],
        "query_by": [],
        "answer_by": [],
        "second_answer_by": [],
        "ground_truth_answer_by": [],
        "reference_feedback": [],
        "reference_score": [],
        "reference_evaluation_by": [],
    }
    for example in self.examples:
        if not isinstance(example, LabelledPairwiseEvaluatorDataExample):
            raise ValueError(
                "LabelledPairwiseEvaluatorDataset can only contain LabelledPairwiseEvaluatorDataExample instances."
            )
        data["query"].append(example.query)
        data["answer"].append(example.answer)
        data["second_answer"].append(example.second_answer)
        data["contexts"].append(example.contexts)
        data["ground_truth_answer"].append(example.ground_truth_answer)
        data["query_by"].append(str(example.query_by))
        data["answer_by"].append(str(example.answer_by))
        data["second_answer_by"].append(str(example.second_answer_by))
        data["ground_truth_answer_by"].append(str(example.ground_truth_answer_by))
        data["reference_feedback"].append(example.reference_feedback)
        data["reference_score"].append(example.reference_score)
        data["reference_evaluation_by"].append(str(example.reference_evaluation_by))

    return pd.DataFrame(data)

```
 |  
| --- | --- |  
##  PairwiseEvaluatorExamplePrediction [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.PairwiseEvaluatorExamplePrediction "Permanent link")
Bases: 
Pairwise evaluation example prediction class.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `feedback`  |  The evaluator's feedback.  |  `<class 'str'>`  |  
|  `score`  |  `float | None`  |  The evaluator's score.  |  `None`  |  
|  `evaluation_source`  |  `EvaluationSource | None`  |  If the evaluation came from original order or flipped; or inconclusive.  |  `None`  |  
|  `invalid_prediction`  |  `bool`  |  Whether or not the prediction is a valid one.  |  `False`  |  
|  `invalid_reason`  |  `str | None`  |  Reason as to why prediction is invalid.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/evaluator_evaluation.py`  
| 
```
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
```
 | 
```
classPairwiseEvaluatorExamplePrediction(BaseLlamaExamplePrediction):
"""
    Pairwise evaluation example prediction class.

    Args:
        feedback (Optional[str]): The evaluator's feedback.
        score (Optional[float]): The evaluator's score.
        evaluation_source (EvaluationSource): If the evaluation came from original order or flipped; or inconclusive.

    """

    feedback: str = Field(
        default_factory=str,
        description="The generated (predicted) response that can be compared to a reference (ground-truth) answer.",
    )
    score: Optional[float] = Field(
        default=None,
        description="The generated (predicted) response that can be compared to a reference (ground-truth) answer.",
    )
    evaluation_source: Optional[EvaluationSource] = Field(
        default=None,
        description=(
            "Whether the evaluation comes from original, or flipped ordering. Can also be neither here indicating inconclusive judgement."
        ),
    )
    invalid_prediction: bool = Field(
        default=False, description="Whether or not the prediction is a valid one."
    )
    invalid_reason: Optional[str] = Field(
        default=None, description="Reason as to why prediction is invalid."
    )

    @property
    defclass_name(self) -> str:
"""Data example class name."""
        return "PairwiseEvaluatorExamplePrediction"

```
 |  
| --- | --- |  
###  class_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.PairwiseEvaluatorExamplePrediction.class_name "Permanent link")

```
class_name: 

```

Data example class name.
##  PairwiseEvaluatorPredictionDataset [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.PairwiseEvaluatorPredictionDataset "Permanent link")
Bases: 
Pairwise evaluation predictions dataset class.
Source code in `llama-index-core/llama_index/core/llama_dataset/evaluator_evaluation.py`  
| 
```
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
classPairwiseEvaluatorPredictionDataset(BaseLlamaPredictionDataset):
"""Pairwise evaluation predictions dataset class."""

    _prediction_type = PairwiseEvaluatorExamplePrediction

    defto_pandas(self) -> Any:
"""Create pandas dataframe."""
        try:
            importpandasaspd
        except ImportError:
            raise ImportError(
                "pandas is required for this function. Please install it with `pip install pandas`."
            )

        data: Dict[str, List] = {
            "feedback": [],
            "score": [],
            "ordering": [],
        }
        for prediction in self.predictions:
            if not isinstance(prediction, PairwiseEvaluatorExamplePrediction):
                raise ValueError(
                    "PairwiseEvaluatorPredictionDataset can only contain PairwiseEvaluatorExamplePrediction instances."
                )
            data["feedback"].append(prediction.feedback)
            data["score"].append(prediction.score)
            data["ordering"].append(str(prediction.evaluation_source))

        return pd.DataFrame(data)

    @property
    defclass_name(self) -> str:
"""Class name."""
        return "PairwiseEvaluatorPredictionDataset"

```
 |  
| --- | --- |  
###  class_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.PairwiseEvaluatorPredictionDataset.class_name "Permanent link")

```
class_name: 

```

Class name.
###  to_pandas [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.PairwiseEvaluatorPredictionDataset.to_pandas "Permanent link")

```
to_pandas() -> 

```

Create pandas dataframe.
Source code in `llama-index-core/llama_index/core/llama_dataset/evaluator_evaluation.py`  
| 
```
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
```
 | 
```
defto_pandas(self) -> Any:
"""Create pandas dataframe."""
    try:
        importpandasaspd
    except ImportError:
        raise ImportError(
            "pandas is required for this function. Please install it with `pip install pandas`."
        )

    data: Dict[str, List] = {
        "feedback": [],
        "score": [],
        "ordering": [],
    }
    for prediction in self.predictions:
        if not isinstance(prediction, PairwiseEvaluatorExamplePrediction):
            raise ValueError(
                "PairwiseEvaluatorPredictionDataset can only contain PairwiseEvaluatorExamplePrediction instances."
            )
        data["feedback"].append(prediction.feedback)
        data["score"].append(prediction.score)
        data["ordering"].append(str(prediction.evaluation_source))

    return pd.DataFrame(data)

```
 |  
| --- | --- |  
##  LabelledRagDataExample [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledRagDataExample "Permanent link")
Bases: 
RAG example class. Analogous to traditional ML datasets, this dataset contains the "features" (i.e., query + context) to make a prediction and the "label" (i.e., response) to evaluate the prediction.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The user query  |  `<class 'str'>`  |  
|  `query_by`  |  `CreatedBy[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.CreatedBy "CreatedBy \(llama_index.core.llama_dataset.base.CreatedBy\)") | None`  |  Query generated by human or ai (model-name)  |  `None`  |  
|  `reference_contexts`  |  `List[str] | None`  |  The contexts used for response  |  `None`  |  
|  `reference_answer`  |  Reference answer to the query. An answer that would receive full marks upon evaluation.  |  `<class 'str'>`  |  
|  `reference_answer_by`  |  `CreatedBy[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.CreatedBy "CreatedBy \(llama_index.core.llama_dataset.base.CreatedBy\)") | None`  |  The reference answer generated by human or ai (model-name).  |  `None`  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/rag.py`  
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
classLabelledRagDataExample(BaseLlamaDataExample):
"""
    RAG example class. Analogous to traditional ML datasets, this dataset contains
    the "features" (i.e., query + context) to make a prediction and the "label" (i.e., response)
    to evaluate the prediction.

    Args:
        query (str): The user query
        query_by (CreatedBy): Query generated by human or ai (model-name)
        reference_contexts (Optional[List[str]]): The contexts used for response
        reference_answer ([str]): Reference answer to the query. An answer
                                    that would receive full marks upon evaluation.
        reference_answer_by: The reference answer generated by human or ai (model-name).

    """

    query: str = Field(
        default_factory=str, description="The user query for the example."
    )
    query_by: Optional[CreatedBy] = Field(
        default=None, description="What generated the query."
    )
    reference_contexts: Optional[List[str]] = Field(
        default=None,
        description="The contexts used to generate the reference answer.",
    )
    reference_answer: str = Field(
        default_factory=str,
        description="The reference (ground-truth) answer to the example.",
    )
    reference_answer_by: Optional[CreatedBy] = Field(
        default=None, description="What generated the reference answer."
    )

    @property
    defclass_name(self) -> str:
"""Data example class name."""
        return "LabelledRagDataExample"

```
 |  
| --- | --- |  
###  class_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledRagDataExample.class_name "Permanent link")

```
class_name: 

```

Data example class name.
##  LabelledRagDataset [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledRagDataset "Permanent link")
Bases: `BaseLlamaDataset[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataset "BaseLlamaDataset \(llama_index.core.llama_dataset.base.BaseLlamaDataset\)")[BaseQueryEngine[](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/#llama_index.core.base.base_query_engine.BaseQueryEngine "BaseQueryEngine \(llama_index.core.base.base_query_engine.BaseQueryEngine\)")]`
RagDataset class.
Source code in `llama-index-core/llama_index/core/llama_dataset/rag.py`  
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
```
 | 
```
classLabelledRagDataset(BaseLlamaDataset[BaseQueryEngine]):
"""RagDataset class."""

    _example_type = LabelledRagDataExample

    defto_pandas(self) -> Any:
"""Create pandas dataframe."""
        try:
            importpandasaspd
        except ImportError:
            raise ImportError(
                "pandas is required for this function. Please install it with `pip install pandas`."
            )

        data: Dict[str, List] = {
            "query": [],
            "reference_contexts": [],
            "reference_answer": [],
            "reference_answer_by": [],
            "query_by": [],
        }
        for example in self.examples:
            if not isinstance(example, LabelledRagDataExample):
                raise ValueError(
                    "All examples in the dataset must be of type LabelledRagDataExample."
                )
            data["query"].append(example.query)
            data["reference_contexts"].append(example.reference_contexts)
            data["reference_answer"].append(example.reference_answer)
            data["reference_answer_by"].append(str(example.reference_answer_by))
            data["query_by"].append(str(example.query_by))

        return pd.DataFrame(data)

    async def_apredict_example(  # type: ignore
        self,
        predictor: BaseQueryEngine,
        example: LabelledRagDataExample,
        sleep_time_in_seconds: int,
    ) -> RagExamplePrediction:
"""Async predict RAG example with a query engine."""
        await asyncio.sleep(sleep_time_in_seconds)
        response = await predictor.aquery(example.query)
        return RagExamplePrediction(
            response=str(response), contexts=[s.text for s in response.source_nodes]
        )

    def_predict_example(  # type: ignore
        self,
        predictor: BaseQueryEngine,
        example: LabelledRagDataExample,
        sleep_time_in_seconds: int = 0,
    ) -> RagExamplePrediction:
"""Predict RAG example with a query engine."""
        time.sleep(sleep_time_in_seconds)
        response = predictor.query(example.query)
        return RagExamplePrediction(
            response=str(response), contexts=[s.text for s in response.source_nodes]
        )

    def_construct_prediction_dataset(  # type: ignore
        self, predictions: Sequence[RagExamplePrediction]
    ) -> RagPredictionDataset:
"""Construct prediction dataset."""
        return RagPredictionDataset(predictions=predictions)

    @property
    defclass_name(self) -> str:
"""Class name."""
        return "LabelledRagDataset"

```
 |  
| --- | --- |  
###  class_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledRagDataset.class_name "Permanent link")

```
class_name: 

```

Class name.
###  to_pandas [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.LabelledRagDataset.to_pandas "Permanent link")

```
to_pandas() -> 

```

Create pandas dataframe.
Source code in `llama-index-core/llama_index/core/llama_dataset/rag.py`  
| 
```
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
```
 | 
```
defto_pandas(self) -> Any:
"""Create pandas dataframe."""
    try:
        importpandasaspd
    except ImportError:
        raise ImportError(
            "pandas is required for this function. Please install it with `pip install pandas`."
        )

    data: Dict[str, List] = {
        "query": [],
        "reference_contexts": [],
        "reference_answer": [],
        "reference_answer_by": [],
        "query_by": [],
    }
    for example in self.examples:
        if not isinstance(example, LabelledRagDataExample):
            raise ValueError(
                "All examples in the dataset must be of type LabelledRagDataExample."
            )
        data["query"].append(example.query)
        data["reference_contexts"].append(example.reference_contexts)
        data["reference_answer"].append(example.reference_answer)
        data["reference_answer_by"].append(str(example.reference_answer_by))
        data["query_by"].append(str(example.query_by))

    return pd.DataFrame(data)

```
 |  
| --- | --- |  
##  RagExamplePrediction [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.RagExamplePrediction "Permanent link")
Bases: 
RAG example prediction class.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `response`  |  The response generated by the LLM.  |  
|  `contexts`  |  `List[str] | None`  |  The retrieved context (text) for generating response.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/rag.py`  
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
```
 | 
```
classRagExamplePrediction(BaseLlamaExamplePrediction):
"""
    RAG example prediction class.

    Args:
        response (str): The response generated by the LLM.
        contexts (Optional[List[str]]): The retrieved context (text) for generating
                                        response.

    """

    response: str = Field(
        default="",
        description="The generated (predicted) response that can be compared to a reference (ground-truth) answer.",
    )
    contexts: Optional[List[str]] = Field(
        default=None,
        description="The contexts in raw text form used to generate the response.",
    )

    @property
    defclass_name(self) -> str:
"""Data example class name."""
        return "RagExamplePrediction"

```
 |  
| --- | --- |  
###  class_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.RagExamplePrediction.class_name "Permanent link")

```
class_name: 

```

Data example class name.
##  RagPredictionDataset [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.RagPredictionDataset "Permanent link")
Bases: 
RagDataset class.
Source code in `llama-index-core/llama_index/core/llama_dataset/rag.py`  
| 
```
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
```
 | 
```
classRagPredictionDataset(BaseLlamaPredictionDataset):
"""RagDataset class."""

    _prediction_type = RagExamplePrediction

    defto_pandas(self) -> Any:
"""Create pandas dataframe."""
        try:
            importpandasaspd
        except ImportError:
            raise ImportError(
                "pandas is required for this function. Please install it with `pip install pandas`."
            )

        data: Dict[str, List] = {
            "response": [],
            "contexts": [],
        }
        for pred in self.predictions:
            if not isinstance(pred, RagExamplePrediction):
                raise ValueError(
                    "All predictions in the dataset must be of type RagExamplePrediction."
                )
            data["response"].append(pred.response)
            data["contexts"].append(pred.contexts)

        return pd.DataFrame(data)

    @property
    defclass_name(self) -> str:
"""Class name."""
        return "RagPredictionDataset"

```
 |  
| --- | --- |  
###  class_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.RagPredictionDataset.class_name "Permanent link")

```
class_name: 

```

Class name.
###  to_pandas [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.RagPredictionDataset.to_pandas "Permanent link")

```
to_pandas() -> 

```

Create pandas dataframe.
Source code in `llama-index-core/llama_index/core/llama_dataset/rag.py`  
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
```
 | 
```
defto_pandas(self) -> Any:
"""Create pandas dataframe."""
    try:
        importpandasaspd
    except ImportError:
        raise ImportError(
            "pandas is required for this function. Please install it with `pip install pandas`."
        )

    data: Dict[str, List] = {
        "response": [],
        "contexts": [],
    }
    for pred in self.predictions:
        if not isinstance(pred, RagExamplePrediction):
            raise ValueError(
                "All predictions in the dataset must be of type RagExamplePrediction."
            )
        data["response"].append(pred.response)
        data["contexts"].append(pred.contexts)

    return pd.DataFrame(data)

```
 |  
| --- | --- |  
##  download_llama_dataset [#](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.download_llama_dataset "Permanent link")

```
download_llama_dataset(
    llama_dataset_class: ,
    download_dir: ,
    llama_datasets_url:  = LLAMA_DATASETS_URL,
    llama_datasets_lfs_url:  = LLAMA_DATASETS_LFS_URL,
    llama_datasets_source_files_tree_url:  = LLAMA_DATASETS_SOURCE_FILES_GITHUB_TREE_URL,
    show_progress:  = False,
    load_documents:  = True,
) -> Tuple[, []]

```

Download dataset from datasets-LFS and llamahub.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `dataset_class`  |  The name of the llamadataset class you want to download, such as `PaulGrahamEssayDataset`.  |  _required_  |  
|  `custom_dir`  |  Custom dir name to download loader into (under parent folder).  |  _required_  |  
|  `custom_path`  |  Custom dirpath to download loader into.  |  _required_  |  
|  `llama_datasets_url`  |  Url for getting ordinary files from llama_datasets repo  |  `LLAMA_DATASETS_URL`  |  
|  `llama_datasets_lfs_url`  |  Url for lfs-traced files llama_datasets repo  |  `LLAMA_DATASETS_LFS_URL`  |  
|  `llama_datasets_source_files_tree_url`  |  Url for listing source_files contents  |  `LLAMA_DATASETS_SOURCE_FILES_GITHUB_TREE_URL`  |  
|  `refresh_cache`  |  If true, the local cache will be skipped and the loader will be fetched directly from the remote repo.  |  _required_  |  
|  `source_files_dirpath`  |  The directory for storing source files  |  _required_  |  
|  `library_path`  |  File name of the library file.  |  _required_  |  
|  `base_file_name`  |  The rag dataset json file  |  _required_  |  
|  `disable_library_cache`  |  Boolean to control library cache  |  _required_  |  
|  `override_path`  |  Boolean to control overriding path  |  _required_  |  
|  `show_progress`  |  `bool`  |  Boolean for showing progress on downloading source files  |  `False`  |  
|  `load_documents`  |  `bool`  |  Boolean for whether or not source_files for LabelledRagDataset should be loaded.  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Tuple[BaseLlamaDataset[](https://developers.llamaindex.ai/python/framework-api-reference/llama_dataset/#llama_index.core.llama_dataset.BaseLlamaDataset "BaseLlamaDataset \(llama_index.core.llama_dataset.base.BaseLlamaDataset\)"), List[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]]`  |  a `BaseLlamaDataset` and a `List[Document]`  |  
Source code in `llama-index-core/llama_index/core/llama_dataset/download.py`  
| 
```
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
```
 | 
```
defdownload_llama_dataset(
    llama_dataset_class: str,
    download_dir: str,
    llama_datasets_url: str = LLAMA_DATASETS_URL,
    llama_datasets_lfs_url: str = LLAMA_DATASETS_LFS_URL,
    llama_datasets_source_files_tree_url: str = LLAMA_DATASETS_SOURCE_FILES_GITHUB_TREE_URL,
    show_progress: bool = False,
    load_documents: bool = True,
) -> Tuple[BaseLlamaDataset, List[Document]]:
"""
    Download dataset from datasets-LFS and llamahub.

    Args:
        dataset_class: The name of the llamadataset class you want to download,
            such as `PaulGrahamEssayDataset`.
        custom_dir: Custom dir name to download loader into (under parent folder).
        custom_path: Custom dirpath to download loader into.
        llama_datasets_url: Url for getting ordinary files from llama_datasets repo
        llama_datasets_lfs_url: Url for lfs-traced files llama_datasets repo
        llama_datasets_source_files_tree_url: Url for listing source_files contents
        refresh_cache: If true, the local cache will be skipped and the
            loader will be fetched directly from the remote repo.
        source_files_dirpath: The directory for storing source files
        library_path: File name of the library file.
        base_file_name: The rag dataset json file
        disable_library_cache: Boolean to control library cache
        override_path: Boolean to control overriding path
        show_progress: Boolean for showing progress on downloading source files
        load_documents: Boolean for whether or not source_files for LabelledRagDataset should
                        be loaded.

    Returns:
        a `BaseLlamaDataset` and a `List[Document]`

    """
    filenames: Tuple[str, str] = download(
        llama_dataset_class,
        llama_datasets_url=llama_datasets_url,
        llama_datasets_lfs_url=llama_datasets_lfs_url,
        llama_datasets_source_files_tree_url=llama_datasets_source_files_tree_url,
        refresh_cache=True,
        custom_path=download_dir,
        library_path="library.json",
        disable_library_cache=True,
        override_path=True,
        show_progress=show_progress,
    )
    dataset_filename, source_files_dir = filenames
    track_download(llama_dataset_class, MODULE_TYPE.DATASETS)

    dataset = _resolve_dataset_class(dataset_filename).from_json(dataset_filename)
    documents = []

    # for now only rag datasets need to provide the documents
    # in order to build an index over them
    if "rag_dataset.json" in dataset_filename and load_documents:
        documents = SimpleDirectoryReader(input_dir=source_files_dir).load_data(
            show_progress=show_progress
        )

    return (dataset, documents)

```
 |  
| --- | --- |
