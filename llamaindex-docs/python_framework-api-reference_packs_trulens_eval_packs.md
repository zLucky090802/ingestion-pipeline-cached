# Trulens eval packs
##  TruLensHarmlessPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/trulens_eval_packs/#llama_index.packs.trulens_eval_packs.TruLensHarmlessPack "Permanent link")
Bases: 
The TruLens-Eval Harmless LlamaPack show how to instrument and evaluate your LlamaIndex query engine. It launches starts a logging database and launches a dashboard in the background, builds an index over an input list of nodes, and instantiates and instruments a query engine over that index. It also instantiates the a suite of Harmless evals so that query is logged and evaluated for harmlessness.
Note: Using this LlamaPack requires that your OpenAI and HuggingFace API keys are set via the OPENAI_API_KEY and HUGGINGFACE_API_KEY environment variable.
Source code in `llama-index-packs/llama-index-packs-trulens-eval-packs/llama_index/packs/trulens_eval_packs/base.py`  
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
```
 | 
```
classTruLensHarmlessPack(BaseLlamaPack):
"""
    The TruLens-Eval Harmless LlamaPack show how to instrument and evaluate your LlamaIndex query
    engine. It launches starts a logging database and launches a dashboard in the background,
    builds an index over an input list of nodes, and instantiates and instruments a query engine
    over that index. It also instantiates the a suite of Harmless evals so that query is logged
    and evaluated for harmlessness.

    Note: Using this LlamaPack requires that your OpenAI and HuggingFace API keys are set via the
    OPENAI_API_KEY and HUGGINGFACE_API_KEY environment variable.
    """

    def__init__(
        self,
        nodes: List[TextNode],
        app_id: str,
        **kwargs: Any,
    ) -> None:
"""
        Initializes a new instance of TruLensEvalPack.

        Args:
            nodes (List[TextNode]): An input list of nodes over which the index
            will be built.
            app_id (str): The application ID for the TruLensEvalPack.

        """
        try:
            fromtrulens_evalimport Feedback, Tru, TruLlama
            fromtrulens_eval.feedback.provider.openaiimport OpenAI
        except ImportError:
            raise ImportError(
                "The trulens-eval package could not be found. "
                "Please install with `pip install trulens-eval`."
            )
        self.app_id = app_id
        self._tru = Tru()
        self._tru.run_dashboard()
        self._index = VectorStoreIndex(nodes, **kwargs)
        self._query_engine = self._index.as_query_engine()

        # Initialize provider class
        provider = OpenAI()

        # LLM-based feedback functions
        f_controversiality = Feedback(
            provider.controversiality_with_cot_reasons,
            name="Criminality",
            higher_is_better=False,
        ).on_output()
        f_criminality = Feedback(
            provider.criminality_with_cot_reasons,
            name="Controversiality",
            higher_is_better=False,
        ).on_output()
        f_insensitivity = Feedback(
            provider.insensitivity_with_cot_reasons,
            name="Insensitivity",
            higher_is_better=False,
        ).on_output()
        f_maliciousness = Feedback(
            provider.maliciousness_with_cot_reasons,
            name="Maliciousness",
            higher_is_better=False,
        ).on_output()

        # Moderation feedback functions
        f_hate = Feedback(
            provider.moderation_hate, name="Hate", higher_is_better=False
        ).on_output()
        f_hatethreatening = Feedback(
            provider.moderation_hatethreatening,
            name="Hate/Threatening",
            higher_is_better=False,
        ).on_output()
        f_violent = Feedback(
            provider.moderation_violence, name="Violent", higher_is_better=False
        ).on_output()
        f_violentgraphic = Feedback(
            provider.moderation_violencegraphic,
            name="Violent/Graphic",
            higher_is_better=False,
        ).on_output()
        f_selfharm = Feedback(
            provider.moderation_selfharm, name="Self Harm", higher_is_better=False
        ).on_output()

        harmless_feedbacks = [
            f_controversiality,
            f_criminality,
            f_insensitivity,
            f_maliciousness,
            f_hate,
            f_hatethreatening,
            f_violent,
            f_violentgraphic,
            f_selfharm,
        ]

        self._tru_query_engine = TruLlama(
            self._query_engine, app_id=app_id, feedbacks=harmless_feedbacks
        )

    defget_modules(self) -> Dict[str, Any]:
"""
        Returns a dictionary containing the internals of the LlamaPack.

        Returns:
            Dict[str, Any]: A dictionary containing the internals of the
            LlamaPack.

        """
        return {
            "session": self._tru,
            "index": self._index,
            "tru_query_engine": self._tru_query_engine,
            "query_engine": self._query_engine,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""
        Runs queries against the index.

        Returns:
            Any: A response from the query engine.

        """
        with self._tru_query_engine as _:
            return self._query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/trulens_eval_packs/#llama_index.packs.trulens_eval_packs.TruLensHarmlessPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Returns a dictionary containing the internals of the LlamaPack.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: A dictionary containing the internals of the  |  
|  `Dict[str, Any]`  |  LlamaPack.  |  
Source code in `llama-index-packs/llama-index-packs-trulens-eval-packs/llama_index/packs/trulens_eval_packs/base.py`  
| 
```
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
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""
    Returns a dictionary containing the internals of the LlamaPack.

    Returns:
        Dict[str, Any]: A dictionary containing the internals of the
        LlamaPack.

    """
    return {
        "session": self._tru,
        "index": self._index,
        "tru_query_engine": self._tru_query_engine,
        "query_engine": self._query_engine,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/trulens_eval_packs/#llama_index.packs.trulens_eval_packs.TruLensHarmlessPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Runs queries against the index.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Any`  |  A response from the query engine.  |  
Source code in `llama-index-packs/llama-index-packs-trulens-eval-packs/llama_index/packs/trulens_eval_packs/base.py`  
| 
```
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
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""
    Runs queries against the index.

    Returns:
        Any: A response from the query engine.

    """
    with self._tru_query_engine as _:
        return self._query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
##  TruLensHelpfulPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/trulens_eval_packs/#llama_index.packs.trulens_eval_packs.TruLensHelpfulPack "Permanent link")
Bases: 
The TruLens-Eval Helpful LlamaPack show how to instrument and evaluate your LlamaIndex query engine. It launches starts a logging database and launches a dashboard in the background, builds an index over an input list of nodes, and instantiates and instruments a query engine over that index. It also instantiates the a suite of Helpful evals so that query is logged and evaluated for helpfulness.
Note: Using this LlamaPack requires that your OpenAI and HuggingFace API keys are set via the OPENAI_API_KEY and HUGGINGFACE_API_KEY environment variable.
Source code in `llama-index-packs/llama-index-packs-trulens-eval-packs/llama_index/packs/trulens_eval_packs/base.py`  
| 
```
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
```
 | 
```
classTruLensHelpfulPack(BaseLlamaPack):
"""
    The TruLens-Eval Helpful LlamaPack show how to instrument and evaluate your LlamaIndex query
    engine. It launches starts a logging database and launches a dashboard in the background,
    builds an index over an input list of nodes, and instantiates and instruments a query engine
    over that index. It also instantiates the a suite of Helpful evals so that query is logged
    and evaluated for helpfulness.

    Note: Using this LlamaPack requires that your OpenAI and HuggingFace API keys are set via the
    OPENAI_API_KEY and HUGGINGFACE_API_KEY environment variable.
    """

    def__init__(
        self,
        nodes: List[TextNode],
        app_id: str,
        **kwargs: Any,
    ) -> None:
"""
        Initializes a new instance of TruLensEvalPack.

        Args:
            nodes (List[TextNode]): An input list of nodes over which the index
            will be built.
            app_id (str): The application ID for the TruLensEvalPack.

        """
        try:
            fromtrulens_evalimport Feedback, Tru, TruLlama
            fromtrulens_eval.feedback.provider.hugsimport Huggingface
            fromtrulens_eval.feedback.provider.openaiimport OpenAI
        except ImportError:
            raise ImportError(
                "The trulens-eval package could not be found. "
                "Please install with `pip install trulens-eval`."
            )
        self.app_id = app_id
        self._tru = Tru()
        self._tru.run_dashboard()
        self._index = VectorStoreIndex(nodes, **kwargs)
        self._query_engine = self._index.as_query_engine()

        # Initialize provider class
        provider = OpenAI()

        hugs_provider = Huggingface()

        # LLM-based feedback functions
        f_coherence = Feedback(
            provider.coherence_with_cot_reasons, name="Coherence"
        ).on_output()
        f_input_sentiment = Feedback(
            provider.sentiment_with_cot_reasons, name="Input Sentiment"
        ).on_input()
        f_output_sentiment = Feedback(
            provider.sentiment_with_cot_reasons, name="Output Sentiment"
        ).on_output()
        f_langmatch = Feedback(
            hugs_provider.language_match, name="Language Match"
        ).on_input_output()

        helpful_feedbacks = [
            f_coherence,
            f_input_sentiment,
            f_output_sentiment,
            f_langmatch,
        ]

        self._tru_query_engine = TruLlama(
            self._query_engine, app_id=app_id, feedbacks=helpful_feedbacks
        )

    defget_modules(self) -> Dict[str, Any]:
"""
        Returns a dictionary containing the internals of the LlamaPack.

        Returns:
            Dict[str, Any]: A dictionary containing the internals of the
            LlamaPack.

        """
        return {
            "session": self._tru,
            "index": self._index,
            "tru_query_engine": self._tru_query_engine,
            "query_engine": self._query_engine,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""
        Runs queries against the index.

        Returns:
            Any: A response from the query engine.

        """
        with self._tru_query_engine as _:
            return self._query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/trulens_eval_packs/#llama_index.packs.trulens_eval_packs.TruLensHelpfulPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Returns a dictionary containing the internals of the LlamaPack.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: A dictionary containing the internals of the  |  
|  `Dict[str, Any]`  |  LlamaPack.  |  
Source code in `llama-index-packs/llama-index-packs-trulens-eval-packs/llama_index/packs/trulens_eval_packs/base.py`  
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
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""
    Returns a dictionary containing the internals of the LlamaPack.

    Returns:
        Dict[str, Any]: A dictionary containing the internals of the
        LlamaPack.

    """
    return {
        "session": self._tru,
        "index": self._index,
        "tru_query_engine": self._tru_query_engine,
        "query_engine": self._query_engine,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/trulens_eval_packs/#llama_index.packs.trulens_eval_packs.TruLensHelpfulPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Runs queries against the index.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Any`  |  A response from the query engine.  |  
Source code in `llama-index-packs/llama-index-packs-trulens-eval-packs/llama_index/packs/trulens_eval_packs/base.py`  
| 
```
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
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""
    Runs queries against the index.

    Returns:
        Any: A response from the query engine.

    """
    with self._tru_query_engine as _:
        return self._query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
##  TruLensRAGTriadPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/trulens_eval_packs/#llama_index.packs.trulens_eval_packs.TruLensRAGTriadPack "Permanent link")
Bases: 
The TruLens-Eval RAG Triad LlamaPack show how to instrument and evaluate your LlamaIndex query engine. It launches starts a logging database and launches a dashboard in the background, builds an index over an input list of nodes, and instantiates and instruments a query engine over that index. It also instantiates the RAG triad (groundedness, context relevance, answer relevance)' so that query is logged and evaluated by this triad for detecting hallucination.
Note: Using this LlamaPack requires that your OpenAI API key is set via the OPENAI_API_KEY environment variable.
Source code in `llama-index-packs/llama-index-packs-trulens-eval-packs/llama_index/packs/trulens_eval_packs/base.py`  
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
```
 | 
```
classTruLensRAGTriadPack(BaseLlamaPack):
"""
    The TruLens-Eval RAG Triad LlamaPack show how to instrument and evaluate your LlamaIndex query
    engine. It launches starts a logging database and launches a dashboard in the background,
    builds an index over an input list of nodes, and instantiates and instruments a query engine
    over that index. It also instantiates the RAG triad (groundedness, context relevance, answer relevance)'
    so that query is logged and evaluated by this triad for detecting hallucination.

    Note: Using this LlamaPack requires that your OpenAI API key is set via the
    OPENAI_API_KEY environment variable.
    """

    def__init__(
        self,
        nodes: List[TextNode],
        app_id: str,
        **kwargs: Any,
    ) -> None:
"""
        Initializes a new instance of TruLensEvalPack.

        Args:
            nodes (List[TextNode]): An input list of nodes over which the index
            will be built.
            app_id (str): The application ID for the TruLensEvalPack.

        """
        try:
            fromtrulens_evalimport Feedback, Tru, TruLlama
            fromtrulens_eval.feedbackimport Groundedness
            fromtrulens_eval.feedback.provider.openaiimport OpenAI
        except ImportError:
            raise ImportError(
                "The trulens-eval package could not be found. "
                "Please install with `pip install trulens-eval`."
            )
        self.app_id = app_id
        self._tru = Tru()
        self._tru.run_dashboard()
        self._index = VectorStoreIndex(nodes, **kwargs)
        self._query_engine = self._index.as_query_engine()

        importnumpyasnp

        # Initialize provider class
        provider = OpenAI()

        grounded = Groundedness(groundedness_provider=provider)

        # Define a groundedness feedback function
        f_groundedness = (
            Feedback(
                grounded.groundedness_measure_with_cot_reasons, name="Groundedness"
            )
            .on(TruLlama.select_source_nodes().node.text.collect())
            .on_output()
            .aggregate(grounded.grounded_statements_aggregator)
        )

        # Question/answer relevance between overall question and answer.
        f_qa_relevance = Feedback(
            provider.relevance, name="Answer Relevance"
        ).on_input_output()

        # Question/statement relevance between question and each context chunk.
        f_context_relevance = (
            Feedback(provider.qs_relevance, name="Context Relevance")
            .on_input()
            .on(TruLlama.select_source_nodes().node.text.collect())
            .aggregate(np.mean)
        )

        feedbacks = [f_groundedness, f_qa_relevance, f_context_relevance]

        self._tru_query_engine = TruLlama(
            self._query_engine, app_id=app_id, feedbacks=feedbacks
        )

    defget_modules(self) -> Dict[str, Any]:
"""
        Returns a dictionary containing the internals of the LlamaPack.

        Returns:
            Dict[str, Any]: A dictionary containing the internals of the
            LlamaPack.

        """
        return {
            "session": self._tru,
            "index": self._index,
            "tru_query_engine": self._tru_query_engine,
            "query_engine": self._query_engine,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""
        Runs queries against the index.

        Returns:
            Any: A response from the query engine.

        """
        with self._tru_query_engine as _:
            return self._query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/trulens_eval_packs/#llama_index.packs.trulens_eval_packs.TruLensRAGTriadPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Returns a dictionary containing the internals of the LlamaPack.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: A dictionary containing the internals of the  |  
|  `Dict[str, Any]`  |  LlamaPack.  |  
Source code in `llama-index-packs/llama-index-packs-trulens-eval-packs/llama_index/packs/trulens_eval_packs/base.py`  
| 
```
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
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""
    Returns a dictionary containing the internals of the LlamaPack.

    Returns:
        Dict[str, Any]: A dictionary containing the internals of the
        LlamaPack.

    """
    return {
        "session": self._tru,
        "index": self._index,
        "tru_query_engine": self._tru_query_engine,
        "query_engine": self._query_engine,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/trulens_eval_packs/#llama_index.packs.trulens_eval_packs.TruLensRAGTriadPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Runs queries against the index.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Any`  |  A response from the query engine.  |  
Source code in `llama-index-packs/llama-index-packs-trulens-eval-packs/llama_index/packs/trulens_eval_packs/base.py`  
| 
```
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
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""
    Runs queries against the index.

    Returns:
        Any: A response from the query engine.

    """
    with self._tru_query_engine as _:
        return self._query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - TruLensHarmlessPack - TruLensHelpfulPack - TruLensRAGTriadPack
