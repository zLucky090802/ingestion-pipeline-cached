# Tonic validate
##  AnswerConsistencyEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/tonic_validate/#llama_index.evaluation.tonic_validate.AnswerConsistencyEvaluator "Permanent link")
Bases: 
Tonic Validate's answer consistency metric.
The output score is a float between 0.0 and 1.0.
See https://docs.tonic.ai/validate/ for more details.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `openai_service`  |  `OpenAIService`  |  The OpenAI service to use. Specifies the chat completion model to use as the LLM evaluator. Defaults to "gpt-4".  |  `None`  |  
Source code in `llama-index-integrations/evaluation/llama-index-evaluation-tonic-validate/llama_index/evaluation/tonic_validate/answer_consistency.py`  
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
```
 | 
```
classAnswerConsistencyEvaluator(BaseEvaluator):
"""
    Tonic Validate's answer consistency metric.

    The output score is a float between 0.0 and 1.0.

    See https://docs.tonic.ai/validate/ for more details.

    Args:
        openai_service(OpenAIService): The OpenAI service to use. Specifies the chat
            completion model to use as the LLM evaluator. Defaults to "gpt-4".

    """

    def__init__(self, openai_service: Optional[Any] = None):
        if openai_service is None:
            openai_service = OpenAIService("gpt-4")
        self.openai_service = openai_service
        self.metric = AnswerConsistencyMetric()

    async defaevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        fromtonic_validate.classes.benchmarkimport BenchmarkItem
        fromtonic_validate.classes.llm_responseimport LLMResponse

        benchmark_item = BenchmarkItem(question=query)

        llm_response = LLMResponse(
            llm_answer=response,
            llm_context_list=contexts,
            benchmark_item=benchmark_item,
        )

        score = self.metric.score(llm_response, self.openai_service)

        return EvaluationResult(
            query=query, contexts=contexts, response=response, score=score
        )

    def_get_prompts(self) -> PromptDictType:
        return {}

    def_get_prompt_modules(self) -> PromptMixinType:
        return {}

    def_update_prompts(self, prompts_dict: PromptDictType) -> None:
        return

```
 |  
| --- | --- |  
##  AnswerConsistencyBinaryEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/tonic_validate/#llama_index.evaluation.tonic_validate.AnswerConsistencyBinaryEvaluator "Permanent link")
Bases: 
Tonic Validate's answer consistency binary metric.
The output score is a float that is either 0.0 or 1.0.
See https://docs.tonic.ai/validate/ for more details.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `openai_service`  |  `OpenAIService`  |  The OpenAI service to use. Specifies the chat completion model to use as the LLM evaluator. Defaults to "gpt-4".  |  `None`  |  
Source code in `llama-index-integrations/evaluation/llama-index-evaluation-tonic-validate/llama_index/evaluation/tonic_validate/answer_consistency_binary.py`  
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
```
 | 
```
classAnswerConsistencyBinaryEvaluator(BaseEvaluator):
"""
    Tonic Validate's answer consistency binary metric.

    The output score is a float that is either 0.0 or 1.0.

    See https://docs.tonic.ai/validate/ for more details.

    Args:
        openai_service(OpenAIService): The OpenAI service to use. Specifies the chat
            completion model to use as the LLM evaluator. Defaults to "gpt-4".

    """

    def__init__(self, openai_service: Optional[Any] = None):
        if openai_service is None:
            openai_service = OpenAIService("gpt-4")
        self.openai_service = openai_service
        self.metric = AnswerConsistencyBinaryMetric()

    async defaevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        fromtonic_validate.classes.benchmarkimport BenchmarkItem
        fromtonic_validate.classes.llm_responseimport LLMResponse

        benchmark_item = BenchmarkItem(question=query)

        llm_response = LLMResponse(
            llm_answer=response,
            llm_context_list=contexts,
            benchmark_item=benchmark_item,
        )

        score = self.metric.score(llm_response, self.openai_service)

        return EvaluationResult(
            query=query, contexts=contexts, response=response, score=score
        )

    def_get_prompts(self) -> PromptDictType:
        return {}

    def_get_prompt_modules(self) -> PromptMixinType:
        return {}

    def_update_prompts(self, prompts_dict: PromptDictType) -> None:
        return

```
 |  
| --- | --- |  
##  AnswerSimilarityEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/tonic_validate/#llama_index.evaluation.tonic_validate.AnswerSimilarityEvaluator "Permanent link")
Bases: 
Tonic Validate's answer similarity metric.
The output score is a float between 0.0 and 5.0.
See https://docs.tonic.ai/validate/ for more details.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `openai_service`  |  `OpenAIService`  |  The OpenAI service to use. Specifies the chat completion model to use as the LLM evaluator. Defaults to "gpt-4".  |  `None`  |  
Source code in `llama-index-integrations/evaluation/llama-index-evaluation-tonic-validate/llama_index/evaluation/tonic_validate/answer_similarity.py`  
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
```
 | 
```
classAnswerSimilarityEvaluator(BaseEvaluator):
"""
    Tonic Validate's answer similarity metric.

    The output score is a float between 0.0 and 5.0.

    See https://docs.tonic.ai/validate/ for more details.

    Args:
        openai_service(OpenAIService): The OpenAI service to use. Specifies the chat
            completion model to use as the LLM evaluator. Defaults to "gpt-4".

    """

    def__init__(self, openai_service: Optional[Any] = None):
        if openai_service is None:
            openai_service = OpenAIService("gpt-4")
        self.openai_service = openai_service
        self.metric = AnswerSimilarityMetric()

    async defaevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        reference_response: Optional[str] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        fromtonic_validate.classes.benchmarkimport BenchmarkItem
        fromtonic_validate.classes.llm_responseimport LLMResponse

        benchmark_item = BenchmarkItem(question=query, answer=reference_response)

        llm_response = LLMResponse(
            llm_answer=response,
            llm_context_list=contexts,
            benchmark_item=benchmark_item,
        )

        score = self.metric.score(llm_response, self.openai_service)

        return EvaluationResult(
            query=query, contexts=contexts, response=response, score=score
        )

    def_get_prompts(self) -> PromptDictType:
        return {}

    def_get_prompt_modules(self) -> PromptMixinType:
        return {}

    def_update_prompts(self, prompts_dict: PromptDictType) -> None:
        return

```
 |  
| --- | --- |  
##  AugmentationAccuracyEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/tonic_validate/#llama_index.evaluation.tonic_validate.AugmentationAccuracyEvaluator "Permanent link")
Bases: 
Tonic Validate's augmentation accuracy metric.
The output score is a float between 0.0 and 1.0.
See https://docs.tonic.ai/validate/ for more details.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `openai_service`  |  `OpenAIService`  |  The OpenAI service to use. Specifies the chat completion model to use as the LLM evaluator. Defaults to "gpt-4".  |  `None`  |  
Source code in `llama-index-integrations/evaluation/llama-index-evaluation-tonic-validate/llama_index/evaluation/tonic_validate/augmentation_accuracy.py`  
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
```
 | 
```
classAugmentationAccuracyEvaluator(BaseEvaluator):
"""
    Tonic Validate's augmentation accuracy metric.

    The output score is a float between 0.0 and 1.0.

    See https://docs.tonic.ai/validate/ for more details.

    Args:
        openai_service(OpenAIService): The OpenAI service to use. Specifies the chat
            completion model to use as the LLM evaluator. Defaults to "gpt-4".

    """

    def__init__(self, openai_service: Optional[Any] = None):
        if openai_service is None:
            openai_service = OpenAIService("gpt-4")
        self.openai_service = openai_service
        self.metric = AugmentationAccuracyMetric()

    async defaevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        fromtonic_validate.classes.benchmarkimport BenchmarkItem
        fromtonic_validate.classes.llm_responseimport LLMResponse

        benchmark_item = BenchmarkItem(question=query)

        llm_response = LLMResponse(
            llm_answer=response,
            llm_context_list=contexts,
            benchmark_item=benchmark_item,
        )

        score = self.metric.score(llm_response, self.openai_service)

        return EvaluationResult(
            query=query, contexts=contexts, response=response, score=score
        )

    def_get_prompts(self) -> PromptDictType:
        return {}

    def_get_prompt_modules(self) -> PromptMixinType:
        return {}

    def_update_prompts(self, prompts_dict: PromptDictType) -> None:
        return

```
 |  
| --- | --- |  
##  AugmentationPrecisionEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/tonic_validate/#llama_index.evaluation.tonic_validate.AugmentationPrecisionEvaluator "Permanent link")
Bases: 
Tonic Validate's augmentation precision metric.
The output score is a float between 0.0 and 1.0.
See https://docs.tonic.ai/validate/ for more details.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `openai_service`  |  `OpenAIService`  |  The OpenAI service to use. Specifies the chat completion model to use as the LLM evaluator. Defaults to "gpt-4".  |  `None`  |  
Source code in `llama-index-integrations/evaluation/llama-index-evaluation-tonic-validate/llama_index/evaluation/tonic_validate/augmentation_precision.py`  
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
```
 | 
```
classAugmentationPrecisionEvaluator(BaseEvaluator):
"""
    Tonic Validate's augmentation precision metric.

    The output score is a float between 0.0 and 1.0.

    See https://docs.tonic.ai/validate/ for more details.

    Args:
        openai_service(OpenAIService): The OpenAI service to use. Specifies the chat
            completion model to use as the LLM evaluator. Defaults to "gpt-4".

    """

    def__init__(self, openai_service: Optional[Any] = None):
        if openai_service is None:
            openai_service = OpenAIService("gpt-4")
        self.openai_service = openai_service
        self.metric = AugmentationPrecisionMetric()

    async defaevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        fromtonic_validate.classes.benchmarkimport BenchmarkItem
        fromtonic_validate.classes.llm_responseimport LLMResponse

        benchmark_item = BenchmarkItem(question=query)

        llm_response = LLMResponse(
            llm_answer=response,
            llm_context_list=contexts,
            benchmark_item=benchmark_item,
        )

        score = self.metric.score(llm_response, self.openai_service)

        return EvaluationResult(
            query=query, contexts=contexts, response=response, score=score
        )

    def_get_prompts(self) -> PromptDictType:
        return {}

    def_get_prompt_modules(self) -> PromptMixinType:
        return {}

    def_update_prompts(self, prompts_dict: PromptDictType) -> None:
        return

```
 |  
| --- | --- |  
##  RetrievalPrecisionEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/tonic_validate/#llama_index.evaluation.tonic_validate.RetrievalPrecisionEvaluator "Permanent link")
Bases: 
Tonic Validate's retrieval precision metric.
The output score is a float between 0.0 and 1.0.
See https://docs.tonic.ai/validate/ for more details.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `openai_service`  |  `OpenAIService`  |  The OpenAI service to use. Specifies the chat completion model to use as the LLM evaluator. Defaults to "gpt-4".  |  `None`  |  
Source code in `llama-index-integrations/evaluation/llama-index-evaluation-tonic-validate/llama_index/evaluation/tonic_validate/retrieval_precision.py`  
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
```
 | 
```
classRetrievalPrecisionEvaluator(BaseEvaluator):
"""
    Tonic Validate's retrieval precision metric.

    The output score is a float between 0.0 and 1.0.

    See https://docs.tonic.ai/validate/ for more details.

    Args:
        openai_service(OpenAIService): The OpenAI service to use. Specifies the chat
            completion model to use as the LLM evaluator. Defaults to "gpt-4".

    """

    def__init__(self, openai_service: Optional[Any] = None):
        if openai_service is None:
            openai_service = OpenAIService("gpt-4")
        self.openai_service = openai_service
        self.metric = RetrievalPrecisionMetric()

    async defaevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        fromtonic_validate.classes.benchmarkimport BenchmarkItem
        fromtonic_validate.classes.llm_responseimport LLMResponse

        benchmark_item = BenchmarkItem(question=query, answer=response)

        llm_response = LLMResponse(
            llm_answer=response,
            llm_context_list=contexts,
            benchmark_item=benchmark_item,
        )

        score = self.metric.score(llm_response, self.openai_service)

        return EvaluationResult(
            query=query, contexts=contexts, response=response, score=score
        )

    def_get_prompts(self) -> PromptDictType:
        return {}

    def_get_prompt_modules(self) -> PromptMixinType:
        return {}

    def_update_prompts(self, prompts_dict: PromptDictType) -> None:
        return

```
 |  
| --- | --- |  
##  TonicValidateEvaluator [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/tonic_validate/#llama_index.evaluation.tonic_validate.TonicValidateEvaluator "Permanent link")
Bases: 
Tonic Validate's validate scorer. Calculates all of Tonic Validate's metrics.
See https://docs.tonic.ai/validate/ for more details.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `metrics`  |  `List[Metric]`  |  The metrics to use. Defaults to all of Tonic Validate's metrics.  |  `None`  |  
|  `model_evaluator`  |  The OpenAI service to use. Specifies the chat completion model to use as the LLM evaluator. Defaults to "gpt-4".  |  `'gpt-4'`  |  
Source code in `llama-index-integrations/evaluation/llama-index-evaluation-tonic-validate/llama_index/evaluation/tonic_validate/tonic_validate_evaluator.py`  
| 
```
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
```
 | 
```
classTonicValidateEvaluator(BaseEvaluator):
"""
    Tonic Validate's validate scorer. Calculates all of Tonic Validate's metrics.

    See https://docs.tonic.ai/validate/ for more details.

    Args:
        metrics(List[Metric]): The metrics to use. Defaults to all of Tonic Validate's
            metrics.
        model_evaluator(str): The OpenAI service to use. Specifies the chat completion
            model to use as the LLM evaluator. Defaults to "gpt-4".

    """

    def__init__(
        self, metrics: Optional[List[Any]] = None, model_evaluator: str = "gpt-4"
    ):
        if metrics is None:
            metrics = [
                AnswerConsistencyMetric(),
                AnswerSimilarityMetric(),
                AugmentationAccuracyMetric(),
                AugmentationPrecisionMetric(),
                RetrievalPrecisionMetric(),
            ]

        self.metrics = metrics
        self.model_evaluator = model_evaluator
        self.validate_scorer = ValidateScorer(metrics, model_evaluator)

    def_calculate_average_score(self, run: Any) -> float:
        fromtonic_validate.metrics.answer_similarity_metricimport (
            AnswerSimilarityMetric,
        )

        ave_score = 0.0
        metric_cnt = 0
        for metric_name, score in run.overall_scores.items():
            if metric_name == AnswerSimilarityMetric.name:
                ave_score += score / 5
            else:
                ave_score += score
            metric_cnt += 1
        return ave_score / metric_cnt

    async defaevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        reference_response: Optional[str] = None,
        **kwargs: Any,
    ) -> TonicValidateEvaluationResult:
        fromtonic_validate.classes.benchmarkimport BenchmarkItem
        fromtonic_validate.classes.llm_responseimport LLMResponse

        benchmark_item = BenchmarkItem(question=query, answer=reference_response)

        llm_response = LLMResponse(
            llm_answer=response,
            llm_context_list=contexts,
            benchmark_item=benchmark_item,
        )

        responses = [llm_response]

        run = self.validate_scorer.score_run(responses)

        ave_score = self._calculate_average_score(run)

        return TonicValidateEvaluationResult(
            query=query,
            contexts=contexts,
            response=response,
            score=ave_score,
            score_dict=run.run_data[0].scores,
        )

    async defaevaluate_run(
        self,
        queries: List[str],
        responses: List[str],
        contexts_list: List[List[str]],
        reference_responses: List[str],
        **kwargs: Any,
    ) -> Any:
"""
        Evaluates a batch of responses.

        Returns a Tonic Validate Run object, which can be logged to the Tonic Validate
        UI. See https://docs.tonic.ai/validate/ for more details.
        """
        fromtonic_validate.classes.benchmarkimport BenchmarkItem
        fromtonic_validate.classes.llm_responseimport LLMResponse

        llm_responses = []

        for query, response, contexts, reference_response in zip(
            queries, responses, contexts_list, reference_responses
        ):
            benchmark_item = BenchmarkItem(question=query, answer=reference_response)

            llm_response = LLMResponse(
                llm_answer=response,
                llm_context_list=contexts,
                benchmark_item=benchmark_item,
            )

            llm_responses.append(llm_response)

        return self.validate_scorer.score_run(llm_responses)

    defevaluate_run(
        self,
        queries: List[str],
        responses: List[str],
        contexts_list: List[List[str]],
        reference_responses: List[str],
        **kwargs: Any,
    ) -> Any:
"""
        Evaluates a batch of responses.

        Returns a Tonic Validate Run object, which can be logged to the Tonic Validate
        UI. See https://docs.tonic.ai/validate/ for more details.
        """
        return asyncio.run(
            self.aevaluate_run(
                queries=queries,
                responses=responses,
                contexts_list=contexts_list,
                reference_responses=reference_responses,
                **kwargs,
            )
        )

    def_get_prompts(self) -> PromptDictType:
        return {}

    def_get_prompt_modules(self) -> PromptMixinType:
        return {}

    def_update_prompts(self, prompts_dict: PromptDictType) -> None:
        return

```
 |  
| --- | --- |  
###  aevaluate_run [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/tonic_validate/#llama_index.evaluation.tonic_validate.TonicValidateEvaluator.aevaluate_run "Permanent link")

```
aevaluate_run(
    queries: [],
    responses: [],
    contexts_list: [[]],
    reference_responses: [],
    **kwargs: 
) -> 

```

Evaluates a batch of responses.
Returns a Tonic Validate Run object, which can be logged to the Tonic Validate UI. See https://docs.tonic.ai/validate/ for more details.
Source code in `llama-index-integrations/evaluation/llama-index-evaluation-tonic-validate/llama_index/evaluation/tonic_validate/tonic_validate_evaluator.py`  
| 
```
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
```
 | 
```
async defaevaluate_run(
    self,
    queries: List[str],
    responses: List[str],
    contexts_list: List[List[str]],
    reference_responses: List[str],
    **kwargs: Any,
) -> Any:
"""
    Evaluates a batch of responses.

    Returns a Tonic Validate Run object, which can be logged to the Tonic Validate
    UI. See https://docs.tonic.ai/validate/ for more details.
    """
    fromtonic_validate.classes.benchmarkimport BenchmarkItem
    fromtonic_validate.classes.llm_responseimport LLMResponse

    llm_responses = []

    for query, response, contexts, reference_response in zip(
        queries, responses, contexts_list, reference_responses
    ):
        benchmark_item = BenchmarkItem(question=query, answer=reference_response)

        llm_response = LLMResponse(
            llm_answer=response,
            llm_context_list=contexts,
            benchmark_item=benchmark_item,
        )

        llm_responses.append(llm_response)

    return self.validate_scorer.score_run(llm_responses)

```
 |  
| --- | --- |  
###  evaluate_run [#](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/tonic_validate/#llama_index.evaluation.tonic_validate.TonicValidateEvaluator.evaluate_run "Permanent link")

```
evaluate_run(
    queries: [],
    responses: [],
    contexts_list: [[]],
    reference_responses: [],
    **kwargs: 
) -> 

```

Evaluates a batch of responses.
Returns a Tonic Validate Run object, which can be logged to the Tonic Validate UI. See https://docs.tonic.ai/validate/ for more details.
Source code in `llama-index-integrations/evaluation/llama-index-evaluation-tonic-validate/llama_index/evaluation/tonic_validate/tonic_validate_evaluator.py`  
| 
```
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
```
 | 
```
defevaluate_run(
    self,
    queries: List[str],
    responses: List[str],
    contexts_list: List[List[str]],
    reference_responses: List[str],
    **kwargs: Any,
) -> Any:
"""
    Evaluates a batch of responses.

    Returns a Tonic Validate Run object, which can be logged to the Tonic Validate
    UI. See https://docs.tonic.ai/validate/ for more details.
    """
    return asyncio.run(
        self.aevaluate_run(
            queries=queries,
            responses=responses,
            contexts_list=contexts_list,
            reference_responses=reference_responses,
            **kwargs,
        )
    )

```
 |  
| --- | --- |  
options: members: - AnswerConsistencyBinaryEvaluator - AnswerConsistencyEvaluator - AnswerSimilarityEvaluator - AugmentationAccuracyEvaluator - AugmentationPrecisionEvaluator - RetrievalPrecisionEvaluator - TonicValidateEvaluator
