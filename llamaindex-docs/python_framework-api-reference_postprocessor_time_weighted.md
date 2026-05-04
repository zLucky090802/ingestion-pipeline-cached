# Time weighted
Node PostProcessor module.
##  LLMRerank [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.LLMRerank "Permanent link")
Bases: 
LLM-based reranker.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `top_n`  |  Top N nodes to return.  |  _required_  |  
|  `choice_select_prompt`  |   |  Choice select prompt.  |  _required_  |  
|  `choice_batch_size`  |  Batch size for choice select.  |  _required_  |  
|  `llm`  |  The LLM to rerank with.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/postprocessor/llm_rerank.py`  
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
```
 | 
```
classLLMRerank(BaseNodePostprocessor):
"""LLM-based reranker."""

    top_n: int = Field(description="Top N nodes to return.")
    choice_select_prompt: SerializeAsAny[BasePromptTemplate] = Field(
        description="Choice select prompt."
    )
    choice_batch_size: int = Field(description="Batch size for choice select.")
    llm: LLM = Field(description="The LLM to rerank with.")

    _format_node_batch_fn: Callable = PrivateAttr()
    _parse_choice_select_answer_fn: Callable = PrivateAttr()

    def__init__(
        self,
        llm: Optional[LLM] = None,
        choice_select_prompt: Optional[BasePromptTemplate] = None,
        choice_batch_size: int = 10,
        format_node_batch_fn: Optional[Callable] = None,
        parse_choice_select_answer_fn: Optional[Callable] = None,
        top_n: int = 10,
    ) -> None:
        choice_select_prompt = choice_select_prompt or SelectorPromptTemplate(
            default_template=DEFAULT_CHOICE_SELECT_PROMPT,
            conditionals=[(is_chat_model, CHAT_CHOICE_SELECT_PROMPT)],
        )

        llm = llm or Settings.llm

        super().__init__(
            llm=llm,
            choice_select_prompt=choice_select_prompt,
            choice_batch_size=choice_batch_size,
            top_n=top_n,
        )
        self._format_node_batch_fn = format_node_batch_fn or (
            default_format_node_batch_for_chat_fn
            if is_chat_model(llm)
            else default_format_node_batch_fn
        )
        self._parse_choice_select_answer_fn = (
            parse_choice_select_answer_fn or default_parse_choice_select_answer_fn
        )

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {"choice_select_prompt": self.choice_select_prompt}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "choice_select_prompt" in prompts:
            self.choice_select_prompt = prompts["choice_select_prompt"]

    @classmethod
    defclass_name(cls) -> str:
        return "LLMRerank"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        if query_bundle is None:
            raise ValueError("Query bundle must be provided.")
        if len(nodes) == 0:
            return []

        initial_results: List[NodeWithScore] = []
        for idx in range(0, len(nodes), self.choice_batch_size):
            nodes_batch = [
                node.node for node in nodes[idx : idx + self.choice_batch_size]
            ]

            query_str = query_bundle.query_str
            # Don't include non text types for non-chat models
            fmt_batch = self._format_node_batch_fn(nodes_batch)
            # call each batch independently
            kwargs = {"query_str": query_str}
            if is_chat_model(self.llm):
                kwargs["context_messages"] = fmt_batch
            else:
                kwargs["context_str"] = fmt_batch
            raw_response = self.llm.predict(self.choice_select_prompt, **kwargs)

            raw_choices, relevances = self._parse_choice_select_answer_fn(
                raw_response, len(nodes_batch)
            )
            choice_idxs = [int(choice) - 1 for choice in raw_choices]
            choice_nodes = [nodes_batch[idx] for idx in choice_idxs]
            relevances = relevances or [1.0 for _ in choice_nodes]
            initial_results.extend(
                [
                    NodeWithScore(node=node, score=relevance)
                    for node, relevance in zip(choice_nodes, relevances)
                ]
            )

        return sorted(initial_results, key=lambda x: x.score or 0.0, reverse=True)[
            : self.top_n
        ]

```
 |  
| --- | --- |  
##  StructuredLLMRerank [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.StructuredLLMRerank "Permanent link")
Bases: 
Structured LLM-based reranker.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `top_n`  |  Top N nodes to return.  |  _required_  |  
|  `choice_select_prompt`  |   |  Choice select prompt.  |  _required_  |  
|  `choice_batch_size`  |  Batch size for choice select.  |  _required_  |  
|  `llm`  |  The LLM to rerank with.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/postprocessor/structured_llm_rerank.py`  
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
```
 | 
```
classStructuredLLMRerank(BaseNodePostprocessor):
"""Structured LLM-based reranker."""

    top_n: int = Field(description="Top N nodes to return.")
    choice_select_prompt: SerializeAsAny[BasePromptTemplate] = Field(
        description="Choice select prompt."
    )
    choice_batch_size: int = Field(description="Batch size for choice select.")
    llm: LLM = Field(description="The LLM to rerank with.")

    _document_relevance_list_cls: type = PrivateAttr()
    _format_node_batch_fn: Callable = PrivateAttr()
    _parse_choice_select_answer_fn: Callable = PrivateAttr()
    _raise_on_prediction_failure: bool = PrivateAttr()

    def__init__(
        self,
        llm: Optional[LLM] = None,
        choice_select_prompt: Optional[BasePromptTemplate] = None,
        choice_batch_size: int = 10,
        format_node_batch_fn: Optional[Callable] = None,
        parse_choice_select_answer_fn: Optional[Callable] = None,
        document_relevance_list_cls: Optional[type] = None,
        raise_on_structured_prediction_failure: bool = True,
        top_n: int = 10,
    ) -> None:
        choice_select_prompt = choice_select_prompt or STRUCTURED_CHOICE_SELECT_PROMPT

        llm = llm or Settings.llm
        if not llm.metadata.is_function_calling_model:
            logger.warning(
                "StructuredLLMRerank constructed with a non-function-calling LLM. This may not work as expected."
            )

        super().__init__(
            llm=llm,
            choice_select_prompt=choice_select_prompt,
            choice_batch_size=choice_batch_size,
            top_n=top_n,
        )
        self._format_node_batch_fn = (
            format_node_batch_fn or default_format_node_batch_fn
        )
        self._parse_choice_select_answer_fn = (
            parse_choice_select_answer_fn
            or default_parse_structured_choice_select_answer
        )
        self._document_relevance_list_cls = (
            document_relevance_list_cls or DocumentRelevanceList
        )
        self._raise_on_structured_prediction_failure = (
            raise_on_structured_prediction_failure
        )

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {"choice_select_prompt": self.choice_select_prompt}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "choice_select_prompt" in prompts:
            self.choice_select_prompt = prompts["choice_select_prompt"]

    @classmethod
    defclass_name(cls) -> str:
        return "StructuredLLMRerank"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        dispatcher.event(
            ReRankStartEvent(
                query=query_bundle,
                nodes=nodes,
                top_n=self.top_n,
                model_name=self.llm.metadata.model_name,
            )
        )

        if query_bundle is None:
            raise ValueError("Query bundle must be provided.")
        if len(nodes) == 0:
            return []

        initial_results: List[NodeWithScore] = []
        with self.callback_manager.event(
            CBEventType.RERANKING,
            payload={
                EventPayload.NODES: nodes,
                EventPayload.MODEL_NAME: self.llm.metadata.model_name,
                EventPayload.QUERY_STR: query_bundle.query_str,
                EventPayload.TOP_K: self.top_n,
            },
        ) as event:
            for idx in range(0, len(nodes), self.choice_batch_size):
                nodes_batch = [
                    node.node for node in nodes[idx : idx + self.choice_batch_size]
                ]

                query_str = query_bundle.query_str
                fmt_batch_str = self._format_node_batch_fn(nodes_batch)
                # call each batch independently
                result: Union[BaseModel, str] = self.llm.structured_predict(
                    output_cls=self._document_relevance_list_cls,
                    prompt=self.choice_select_prompt,
                    context_str=fmt_batch_str,
                    query_str=query_str,
                )
                # in case structured prediction fails, a str of the raised exception is returned
                if isinstance(result, str):
                    if self._raise_on_structured_prediction_failure:
                        raise ValueError(
                            f"Structured prediction failed for nodes {idx}{idx+self.choice_batch_size}: {result}"
                        )
                    logger.warning(
                        f"Structured prediction failed for nodes {idx}{idx+self.choice_batch_size}: {result}"
                    )
                    # add all nodes with score 0
                    initial_results.extend(
                        [NodeWithScore(node=node, score=0.0) for node in nodes_batch]
                    )
                    continue

                raw_choices, relevances = self._parse_choice_select_answer_fn(
                    result, len(nodes_batch)
                )
                choice_idxs = [int(choice) - 1 for choice in raw_choices]
                choice_nodes = [nodes_batch[idx] for idx in choice_idxs]
                relevances = relevances or [1.0 for _ in choice_nodes]
                initial_results.extend(
                    [
                        NodeWithScore(node=node, score=relevance)
                        for node, relevance in zip(choice_nodes, relevances)
                    ]
                )

            reranked_nodes = sorted(
                initial_results, key=lambda x: x.score or 0.0, reverse=True
            )[: self.top_n]
            event.on_end(payload={EventPayload.NODES: reranked_nodes})

        dispatcher.event(ReRankEndEvent(nodes=reranked_nodes))
        return reranked_nodes

```
 |  
| --- | --- |  
##  DocumentWithRelevance [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.DocumentWithRelevance "Permanent link")
Bases: `BaseModel`
Document rankings as selected by model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `document_number`  |  The number of the document within the provided list  |  _required_  |  
|  `relevance`  |  Relevance score from 1-10 of the document to the given query - based on the document content  |  _required_  |  
Source code in `llama-index-core/llama_index/core/postprocessor/structured_llm_rerank.py`  
| 
```
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
```
 | 
```
classDocumentWithRelevance(BaseModel):
"""
    Document rankings as selected by model.
    """

    document_number: int = Field(
        description="The number of the document within the provided list"
    )
    # Put min/max as a json schema extra so that pydantic doesn't enforce it but the model sees it.
    # Doesn't need to be strictly enforced but is useful for the model.
    relevance: int = Field(
        description="Relevance score from 1-10 of the document to the given query - based on the document content",
        json_schema_extra={"minimum": 1, "maximum": 10},
    )

```
 |  
| --- | --- |  
##  MetadataReplacementPostProcessor [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.MetadataReplacementPostProcessor "Permanent link")
Bases: 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `target_metadata_key`  |  Target metadata key to replace node content with.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/postprocessor/metadata_replacement.py`  
| 
```
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
29
30
31
32
33
```
 | 
```
classMetadataReplacementPostProcessor(BaseNodePostprocessor):
    target_metadata_key: str = Field(
        description="Target metadata key to replace node content with."
    )

    def__init__(self, target_metadata_key: str) -> None:
        super().__init__(target_metadata_key=target_metadata_key)

    @classmethod
    defclass_name(cls) -> str:
        return "MetadataReplacementPostProcessor"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        for n in nodes:
            n.node.set_content(
                n.node.metadata.get(
                    self.target_metadata_key,
                    n.node.get_content(metadata_mode=MetadataMode.NONE),
                )
            )

        return nodes

```
 |  
| --- | --- |  
##  AutoPrevNextNodePostprocessor [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.AutoPrevNextNodePostprocessor "Permanent link")
Bases: 
Previous/Next Node post-processor.
Allows users to fetch additional nodes from the document store, based on the prev/next relationships of the nodes.
NOTE: difference with PrevNextPostprocessor is that this infers forward/backwards direction.
NOTE: this is a beta feature.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `docstore`  |   |  The document store.  |  _required_  |  
|  `num_nodes`  |  The number of nodes to return (default: 1)  |  
|  `infer_prev_next_tmpl`  |  The template to use for inference. Required fields are {context_str} and {query_str}.  |  `"The current context information is provided. \nA question is also provided. \nYou are a retrieval agent deciding whether to search the document store for additional prior context or future context. \nGiven the context and question, return PREVIOUS or NEXT or NONE. \nExamples: \n\nContext: Describes the author's experience at Y Combinator.Question: What did the author do after his time at Y Combinator? \nAnswer: NEXT \n\nContext: Describes the author's experience at Y Combinator.Question: What did the author do before his time at Y Combinator? \nAnswer: PREVIOUS \n\nContext: Describe the author's experience at Y Combinator.Question: What did the author do at Y Combinator? \nAnswer: NONE \n\nContext: {context_str}\nQuestion: {query_str}\nAnswer: "`  |  
|  `llm`  |  `Annotated[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.LLM\)"), SerializeAsAny] | None`  |  `None`  |  
|  `refine_prev_next_tmpl`  |  `'The current context information is provided. \nA question is also provided. \nAn existing answer is also provided.\nYou are a retrieval agent deciding whether to search the document store for additional prior context or future context. \nGiven the context, question, and previous answer, return PREVIOUS or NEXT or NONE.\nExamples: \n\nContext: {context_msg}\nQuestion: {query_str}\nExisting Answer: {existing_answer}\nAnswer: '`  |  
|  `verbose`  |  `bool`  |  `False`  |  
|  `response_mode`  |   |  `<ResponseMode.COMPACT: 'compact'>`  |  
Source code in `llama-index-core/llama_index/core/postprocessor/node.py`  
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
```
 | 
```
classAutoPrevNextNodePostprocessor(BaseNodePostprocessor):
"""
    Previous/Next Node post-processor.

    Allows users to fetch additional nodes from the document store,
    based on the prev/next relationships of the nodes.

    NOTE: difference with PrevNextPostprocessor is that
    this infers forward/backwards direction.

    NOTE: this is a beta feature.

    Args:
        docstore (BaseDocumentStore): The document store.
        num_nodes (int): The number of nodes to return (default: 1)
        infer_prev_next_tmpl (str): The template to use for inference.
            Required fields are {context_str} and {query_str}.

    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    docstore: BaseDocumentStore
    llm: Optional[SerializeAsAny[LLM]] = None
    num_nodes: int = Field(default=1)
    infer_prev_next_tmpl: str = Field(default=DEFAULT_INFER_PREV_NEXT_TMPL)
    refine_prev_next_tmpl: str = Field(default=DEFAULT_REFINE_INFER_PREV_NEXT_TMPL)
    verbose: bool = Field(default=False)
    response_mode: ResponseMode = Field(default=ResponseMode.COMPACT)

    @classmethod
    defclass_name(cls) -> str:
        return "AutoPrevNextNodePostprocessor"

    def_parse_prediction(self, raw_pred: str) -> str:
"""Parse prediction."""
        pred = raw_pred.strip().lower()
        if "previous" in pred:
            return "previous"
        elif "next" in pred:
            return "next"
        elif "none" in pred:
            return "none"
        raise ValueError(f"Invalid prediction: {raw_pred}")

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""
        llm = self.llm or Settings.llm

        if query_bundle is None:
            raise ValueError("Missing query bundle.")

        infer_prev_next_prompt = PromptTemplate(
            self.infer_prev_next_tmpl,
        )
        refine_infer_prev_next_prompt = PromptTemplate(self.refine_prev_next_tmpl)

        all_nodes: Dict[str, NodeWithScore] = {}
        for node in nodes:
            all_nodes[node.node.node_id] = node
            # use response builder instead of llm directly
            # to be more robust to handling long context
            response_builder = get_response_synthesizer(
                llm=llm,
                text_qa_template=infer_prev_next_prompt,
                refine_template=refine_infer_prev_next_prompt,
                response_mode=self.response_mode,
            )
            raw_pred = response_builder.get_response(
                text_chunks=[node.node.get_content()],
                query_str=query_bundle.query_str,
            )
            raw_pred = cast(str, raw_pred)
            mode = self._parse_prediction(raw_pred)

            logger.debug(f"> Postprocessor Predicted mode: {mode}")
            if self.verbose:
                print(f"> Postprocessor Predicted mode: {mode}")

            if mode == "next":
                all_nodes.update(get_forward_nodes(node, self.num_nodes, self.docstore))
            elif mode == "previous":
                all_nodes.update(
                    get_backward_nodes(node, self.num_nodes, self.docstore)
                )
            elif mode == "none":
                pass
            else:
                raise ValueError(f"Invalid mode: {mode}")

        sorted_nodes = sorted(all_nodes.values(), key=lambda x: x.node.node_id)
        return list(sorted_nodes)

```
 |  
| --- | --- |  
##  KeywordNodePostprocessor [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.KeywordNodePostprocessor "Permanent link")
Bases: 
Keyword-based Node processor.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `required_keywords`  |  `List[str]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
|  `exclude_keywords`  |  `List[str]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
|  `lang`  |  `'en'`  |  
Source code in `llama-index-core/llama_index/core/postprocessor/node.py`  
| 
```
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
```
 | 
```
classKeywordNodePostprocessor(BaseNodePostprocessor):
"""Keyword-based Node processor."""

    required_keywords: List[str] = Field(default_factory=list)
    exclude_keywords: List[str] = Field(default_factory=list)
    lang: str = Field(default="en")

    @classmethod
    defclass_name(cls) -> str:
        return "KeywordNodePostprocessor"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""
        try:
            importspacy
        except ImportError:
            raise ImportError(
                "Spacy is not installed, please install it with `pip install spacy`."
            )
        fromspacy.matcherimport PhraseMatcher

        nlp = spacy.blank(self.lang)
        required_matcher = PhraseMatcher(nlp.vocab)
        exclude_matcher = PhraseMatcher(nlp.vocab)
        required_matcher.add("RequiredKeywords", list(nlp.pipe(self.required_keywords)))
        exclude_matcher.add("ExcludeKeywords", list(nlp.pipe(self.exclude_keywords)))

        new_nodes = []
        for node_with_score in nodes:
            node = node_with_score.node
            doc = nlp(node.get_content())
            if self.required_keywords and not required_matcher(doc):
                continue
            if self.exclude_keywords and exclude_matcher(doc):
                continue
            new_nodes.append(node_with_score)

        return new_nodes

```
 |  
| --- | --- |  
##  LongContextReorder [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.LongContextReorder "Permanent link")
Bases: 
Models struggle to access significant details found in the center of extended contexts. A study (https://arxiv.org/abs/2307.03172) observed that the best performance typically arises when crucial data is positioned at the start or conclusion of the input context. Additionally, as the input context lengthens, performance drops notably, even in models designed for long contexts.".
Source code in `llama-index-core/llama_index/core/postprocessor/node.py`  
| 
```
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
```
 | 
```
classLongContextReorder(BaseNodePostprocessor):
"""
    Models struggle to access significant details found
    in the center of extended contexts. A study
    (https://arxiv.org/abs/2307.03172) observed that the best
    performance typically arises when crucial data is positioned
    at the start or conclusion of the input context. Additionally,
    as the input context lengthens, performance drops notably, even
    in models designed for long contexts.".
    """

    @classmethod
    defclass_name(cls) -> str:
        return "LongContextReorder"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""
        reordered_nodes: List[NodeWithScore] = []
        ordered_nodes: List[NodeWithScore] = sorted(
            nodes, key=lambda x: x.score if x.score is not None else 0
        )
        for i, node in enumerate(ordered_nodes):
            if i % 2 == 0:
                reordered_nodes.insert(0, node)
            else:
                reordered_nodes.append(node)
        return reordered_nodes

```
 |  
| --- | --- |  
##  PrevNextNodePostprocessor [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.PrevNextNodePostprocessor "Permanent link")
Bases: 
Previous/Next Node post-processor.
Allows users to fetch additional nodes from the document store, based on the relationships of the nodes.
NOTE: this is a beta feature.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `docstore`  |   |  The document store.  |  _required_  |  
|  `num_nodes`  |  The number of nodes to return (default: 1)  |  
|  `mode`  |  The mode of the post-processor. Can be "previous", "next", or "both.  |  `'next'`  |  
Source code in `llama-index-core/llama_index/core/postprocessor/node.py`  
| 
```
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
```
 | 
```
classPrevNextNodePostprocessor(BaseNodePostprocessor):
"""
    Previous/Next Node post-processor.

    Allows users to fetch additional nodes from the document store,
    based on the relationships of the nodes.

    NOTE: this is a beta feature.

    Args:
        docstore (BaseDocumentStore): The document store.
        num_nodes (int): The number of nodes to return (default: 1)
        mode (str): The mode of the post-processor.
            Can be "previous", "next", or "both.

    """

    docstore: BaseDocumentStore
    num_nodes: int = Field(default=1)
    mode: str = Field(default="next")

    @field_validator("mode")
    @classmethod
    def_validate_mode(cls, v: str) -> str:
"""Validate mode."""
        if v not in ["next", "previous", "both"]:
            raise ValueError(f"Invalid mode: {v}")
        return v

    @classmethod
    defclass_name(cls) -> str:
        return "PrevNextNodePostprocessor"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""
        all_nodes: Dict[str, NodeWithScore] = {}
        for node in nodes:
            all_nodes[node.node.node_id] = node
            if self.mode == "next":
                all_nodes.update(get_forward_nodes(node, self.num_nodes, self.docstore))
            elif self.mode == "previous":
                all_nodes.update(
                    get_backward_nodes(node, self.num_nodes, self.docstore)
                )
            elif self.mode == "both":
                all_nodes.update(get_forward_nodes(node, self.num_nodes, self.docstore))
                all_nodes.update(
                    get_backward_nodes(node, self.num_nodes, self.docstore)
                )
            else:
                raise ValueError(f"Invalid mode: {self.mode}")

        all_nodes_values: List[NodeWithScore] = list(all_nodes.values())
        sorted_nodes: List[NodeWithScore] = []
        for node in all_nodes_values:
            # variable to check if cand node is inserted
            node_inserted = False
            for i, cand in enumerate(sorted_nodes):
                node_id = node.node.node_id
                # prepend to current candidate
                prev_node_info = cand.node.prev_node
                next_node_info = cand.node.next_node
                if prev_node_info is not None and node_id == prev_node_info.node_id:
                    node_inserted = True
                    sorted_nodes.insert(i, node)
                    break
                # append to current candidate
                elif next_node_info is not None and node_id == next_node_info.node_id:
                    node_inserted = True
                    sorted_nodes.insert(i + 1, node)
                    break

            if not node_inserted:
                sorted_nodes.append(node)

        return sorted_nodes

```
 |  
| --- | --- |  
##  SimilarityPostprocessor [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.SimilarityPostprocessor "Permanent link")
Bases: 
Similarity-based Node processor.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `similarity_cutoff`  |  `float`  |  `0.0`  |  
Source code in `llama-index-core/llama_index/core/postprocessor/node.py`  
| 
```
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
```
 | 
```
classSimilarityPostprocessor(BaseNodePostprocessor):
"""Similarity-based Node processor."""

    similarity_cutoff: float = Field(default=0.0)

    @classmethod
    defclass_name(cls) -> str:
        return "SimilarityPostprocessor"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""
        sim_cutoff_exists = self.similarity_cutoff is not None

        new_nodes = []
        for node in nodes:
            should_use_node = True
            if sim_cutoff_exists:
                similarity = node.score
                if similarity is None:
                    should_use_node = False
                elif cast(float, similarity)  cast(float, self.similarity_cutoff):
                    should_use_node = False

            if should_use_node:
                new_nodes.append(node)

        return new_nodes

```
 |  
| --- | --- |  
##  EmbeddingRecencyPostprocessor [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.EmbeddingRecencyPostprocessor "Permanent link")
Bases: 
Embedding Recency post-processor.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `embed_model`  |   |  `<dynamic>`  |  
|  `date_key`  |  `'date'`  |  
|  `similarity_cutoff`  |  `float`  |  `0.7`  |  
|  `query_embedding_tmpl`  |  `'The current document is provided.\n----------------\n{context_str}\n----------------\nGiven the document, we wish to find documents that contain \nsimilar context. Note that these documents are older than the current document, meaning that certain details may be changed. \nHowever, the high-level context should be similar.\n'`  |  
Source code in `llama-index-core/llama_index/core/postprocessor/node_recency.py`  
| 
```
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
```
 | 
```
classEmbeddingRecencyPostprocessor(BaseNodePostprocessor):
"""Embedding Recency post-processor."""

    embed_model: SerializeAsAny[BaseEmbedding] = Field(
        default_factory=lambda: Settings.embed_model
    )
    date_key: str = "date"
    similarity_cutoff: float = Field(default=0.7)
    query_embedding_tmpl: str = Field(default=DEFAULT_QUERY_EMBEDDING_TMPL)

    @classmethod
    defclass_name(cls) -> str:
        return "EmbeddingRecencyPostprocessor"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""
        try:
            importpandasaspd
        except ImportError:
            raise ImportError(
                "pandas is required for this function. Please install it with `pip install pandas`."
            )

        if query_bundle is None:
            raise ValueError("Missing query bundle in extra info.")

        # sort nodes by date
        node_dates = pd.to_datetime(
            [node.node.metadata[self.date_key] for node in nodes]
        )
        sorted_node_idxs = np.flip(node_dates.argsort())
        sorted_nodes: List[NodeWithScore] = [nodes[idx] for idx in sorted_node_idxs]

        # get embeddings for each node
        texts = [node.get_content(metadata_mode=MetadataMode.EMBED) for node in nodes]
        text_embeddings = self.embed_model.get_text_embedding_batch(texts=texts)

        node_ids_to_skip: Set[str] = set()
        for idx, node in enumerate(sorted_nodes):
            if node.node.node_id in node_ids_to_skip:
                continue
            # get query embedding for the "query" node
            # NOTE: not the same as the text embedding because
            # we want to optimize for retrieval results

            query_text = self.query_embedding_tmpl.format(
                context_str=node.node.get_content(metadata_mode=MetadataMode.EMBED),
            )
            query_embedding = self.embed_model.get_query_embedding(query_text)

            for idx2 in range(idx + 1, len(sorted_nodes)):
                if sorted_nodes[idx2].node.node_id in node_ids_to_skip:
                    continue
                node2 = sorted_nodes[idx2]
                if (
                    np.dot(query_embedding, text_embeddings[idx2])
                     self.similarity_cutoff
                ):
                    node_ids_to_skip.add(node2.node.node_id)

        return [
            node for node in sorted_nodes if node.node.node_id not in node_ids_to_skip
        ]

```
 |  
| --- | --- |  
##  FixedRecencyPostprocessor [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.FixedRecencyPostprocessor "Permanent link")
Bases: 
Fixed Recency post-processor.
This post-processor does the following steps orders nodes by date.
Assumes the date_key corresponds to a date field in the metadata.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `top_k`  |  
|  `date_key`  |  `'date'`  |  
Source code in `llama-index-core/llama_index/core/postprocessor/node_recency.py`  
| 
```
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
```
 | 
```
classFixedRecencyPostprocessor(BaseNodePostprocessor):
"""
    Fixed Recency post-processor.

    This post-processor does the following steps orders nodes by date.

    Assumes the date_key corresponds to a date field in the metadata.
    """

    top_k: int = 1
    date_key: str = "date"

    @classmethod
    defclass_name(cls) -> str:
        return "FixedRecencyPostprocessor"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""
        try:
            importpandasaspd
        except ImportError:
            raise ImportError(
                "pandas is required for this function. Please install it with `pip install pandas`."
            )

        if query_bundle is None:
            raise ValueError("Missing query bundle in extra info.")

        # sort nodes by date
        node_dates = pd.to_datetime(
            [node.node.metadata[self.date_key] for node in nodes]
        )
        sorted_node_idxs = np.flip(node_dates.argsort())
        sorted_nodes = [nodes[idx] for idx in sorted_node_idxs]

        return sorted_nodes[: self.top_k]

```
 |  
| --- | --- |  
##  TimeWeightedPostprocessor [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.TimeWeightedPostprocessor "Permanent link")
Bases: 
Time-weighted post-processor.
Reranks a set of nodes based on their recency.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `time_decay`  |  `float`  |  `0.99`  |  
|  `last_accessed_key`  |  `'__last_accessed__'`  |  
|  `time_access_refresh`  |  `bool`  |  `True`  |  
|  `now`  |  `float | None`  |  `None`  |  
|  `top_k`  |  
Source code in `llama-index-core/llama_index/core/postprocessor/node_recency.py`  
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
```
 | 
```
classTimeWeightedPostprocessor(BaseNodePostprocessor):
"""
    Time-weighted post-processor.

    Reranks a set of nodes based on their recency.

    """

    time_decay: float = Field(default=0.99)
    last_accessed_key: str = "__last_accessed__"
    time_access_refresh: bool = True
    # optionally set now (makes it easier to test)
    now: Optional[float] = None
    top_k: int = 1

    @classmethod
    defclass_name(cls) -> str:
        return "TimeWeightedPostprocessor"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""
        now = self.now or datetime.now().timestamp()
        # TODO: refactor with get_top_k_embeddings

        similarities = []
        for node_with_score in nodes:
            # embedding similarity score
            score = node_with_score.score or 1.0
            node = node_with_score.node
            # time score
            if node.metadata is None:
                raise ValueError("metadata is None")

            last_accessed = node.metadata.get(self.last_accessed_key, None)
            if last_accessed is None:
                last_accessed = now

            hours_passed = (now - last_accessed) / 3600
            time_similarity = (1 - self.time_decay) ** hours_passed

            similarity = score + time_similarity

            similarities.append(similarity)

        sorted_tups = sorted(zip(similarities, nodes), key=lambda x: x[0], reverse=True)

        top_k = min(self.top_k, len(sorted_tups))
        result_tups = sorted_tups[:top_k]
        result_nodes = [
            NodeWithScore(node=n.node, score=score) for score, n in result_tups
        ]

        # set __last_accessed__ to now
        if self.time_access_refresh:
            for node_with_score in result_nodes:
                node_with_score.node.metadata[self.last_accessed_key] = now

        return result_nodes

```
 |  
| --- | --- |  
##  SentenceEmbeddingOptimizer [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.SentenceEmbeddingOptimizer "Permanent link")
Bases: 
Optimization of a text chunk given the query by shortening the input text.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `percentile_cutoff`  |  `float | None`  |  Percentile cutoff for the top k sentences to use.  |  _required_  |  
|  `threshold_cutoff`  |  `float | None`  |  Threshold cutoff for similarity for each sentence to use.  |  _required_  |  
|  `context_before`  |  `int | None`  |  Number of sentences before retrieved sentence for further context  |  _required_  |  
|  `context_after`  |  `int | None`  |  Number of sentences after retrieved sentence for further context  |  _required_  |  
Source code in `llama-index-core/llama_index/core/postprocessor/optimizer.py`  
| 
```
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
```
 | 
```
classSentenceEmbeddingOptimizer(BaseNodePostprocessor):
"""Optimization of a text chunk given the query by shortening the input text."""

    percentile_cutoff: Optional[float] = Field(
        description="Percentile cutoff for the top k sentences to use."
    )
    threshold_cutoff: Optional[float] = Field(
        description="Threshold cutoff for similarity for each sentence to use."
    )

    _embed_model: BaseEmbedding = PrivateAttr()
    _tokenizer_fn: Callable[[str], List[str]] = PrivateAttr()

    context_before: Optional[int] = Field(
        description="Number of sentences before retrieved sentence for further context"
    )

    context_after: Optional[int] = Field(
        description="Number of sentences after retrieved sentence for further context"
    )

    def__init__(
        self,
        embed_model: Optional[BaseEmbedding] = None,
        percentile_cutoff: Optional[float] = None,
        threshold_cutoff: Optional[float] = None,
        tokenizer_fn: Optional[Callable[[str], List[str]]] = None,
        context_before: Optional[int] = None,
        context_after: Optional[int] = None,
    ):
"""
        Optimizer class that is passed into BaseGPTIndexQuery.

        Should be set like this:

        .. code-block:: python
        from llama_index.core.optimization.optimizer import Optimizer
        optimizer = SentenceEmbeddingOptimizer(
                        percentile_cutoff=0.5
                        this means that the top 50% of sentences will be used.
                        Alternatively, you can set the cutoff using a threshold
                        on the similarity score. In this case only sentences with a
                        similarity score higher than the threshold will be used.
                        threshold_cutoff=0.7
                        these cutoffs can also be used together.


        query_engine = index.as_query_engine(
            optimizer=optimizer

        response = query_engine.query("<query_str>")
        """
        super().__init__(
            percentile_cutoff=percentile_cutoff,
            threshold_cutoff=threshold_cutoff,
            context_after=context_after,
            context_before=context_before,
        )
        self._embed_model = embed_model or Settings.embed_model
        if self._embed_model is None:
            try:
                fromllama_index.embeddings.openaiimport (
                    OpenAIEmbedding,
                )  # pants: no-infer-dep

                self._embed_model = OpenAIEmbedding()
            except ImportError:
                raise ImportError(
                    "`llama-index-embeddings-openai` package not found, "
                    "please run `pip install llama-index-embeddings-openai`"
                )

        if tokenizer_fn is None:
            tokenizer = globals_helper.punkt_tokenizer
            tokenizer_fn = tokenizer.tokenize
        self._tokenizer_fn = tokenizer_fn

    @classmethod
    defclass_name(cls) -> str:
        return "SentenceEmbeddingOptimizer"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Optimize a node text given the query by shortening the node text."""
        if query_bundle is None:
            return nodes

        for node_idx in range(len(nodes)):
            text = nodes[node_idx].node.get_content(metadata_mode=MetadataMode.LLM)

            split_text = self._tokenizer_fn(text)

            if query_bundle.embedding is None:
                query_bundle.embedding = (
                    self._embed_model.get_agg_embedding_from_queries(
                        query_bundle.embedding_strs
                    )
                )

            text_embeddings = self._embed_model._get_text_embeddings(split_text)

            num_top_k = None
            threshold = None
            if self.percentile_cutoff is not None:
                num_top_k = int(len(split_text) * self.percentile_cutoff)
            if self.threshold_cutoff is not None:
                threshold = self.threshold_cutoff

            top_similarities, top_idxs = get_top_k_embeddings(
                query_embedding=query_bundle.embedding,
                embeddings=text_embeddings,
                similarity_fn=self._embed_model.similarity,
                similarity_top_k=num_top_k,
                embedding_ids=list(range(len(text_embeddings))),
                similarity_cutoff=threshold,
            )

            if len(top_idxs) == 0:
                raise ValueError("Optimizer returned zero sentences.")

            rangeMin, rangeMax = 0, len(split_text)

            if self.context_before is None:
                self.context_before = 1
            if self.context_after is None:
                self.context_after = 1

            top_sentences = [
                " ".join(
                    split_text[
                        max(idx - self.context_before, rangeMin) : min(
                            idx + self.context_after + 1, rangeMax
                        )
                    ]
                )
                for idx in top_idxs
            ]

            logger.debug(f"> Top {len(top_idxs)} sentences with scores:\n")
            if logger.isEnabledFor(logging.DEBUG):
                for idx in range(len(top_idxs)):
                    logger.debug(
                        f"{idx}. {top_sentences[idx]} ({top_similarities[idx]})"
                    )

            nodes[node_idx].node.set_content(" ".join(top_sentences))

        return nodes

```
 |  
| --- | --- |  
##  NERPIINodePostprocessor [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.NERPIINodePostprocessor "Permanent link")
Bases: 
NER PII Node processor.
Uses a HF transformers model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `pii_node_info_key`  |  `'__pii_node_info__'`  |  
Source code in `llama-index-core/llama_index/core/postprocessor/pii.py`  
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
```
 | 
```
classNERPIINodePostprocessor(BaseNodePostprocessor):
"""
    NER PII Node processor.

    Uses a HF transformers model.

    """

    pii_node_info_key: str = "__pii_node_info__"

    @classmethod
    defclass_name(cls) -> str:
        return "NERPIINodePostprocessor"

    defmask_pii(self, ner: Callable, text: str) -> Tuple[str, Dict]:
"""Mask PII in text."""
        new_text = text
        response = ner(text)
        mapping = {}
        for entry in response:
            entity_group_tag = f"[{entry['entity_group']}_{entry['start']}]"
            new_text = new_text.replace(entry["word"], entity_group_tag).strip()
            mapping[entity_group_tag] = entry["word"]
        return new_text, mapping

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""
        fromtransformersimport pipeline  # pants: no-infer-dep

        ner = pipeline("ner", grouped_entities=True)

        # swap out text from nodes, with the original node mappings
        new_nodes = []
        for node_with_score in nodes:
            node = node_with_score.node
            new_text, mapping_info = self.mask_pii(
                ner, node.get_content(metadata_mode=MetadataMode.LLM)
            )
            new_node = deepcopy(node)
            new_node.excluded_embed_metadata_keys.append(self.pii_node_info_key)
            new_node.excluded_llm_metadata_keys.append(self.pii_node_info_key)
            new_node.metadata[self.pii_node_info_key] = mapping_info
            new_node.set_content(new_text)
            new_nodes.append(NodeWithScore(node=new_node, score=node_with_score.score))

        return new_nodes

```
 |  
| --- | --- |  
###  mask_pii [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.NERPIINodePostprocessor.mask_pii "Permanent link")

```
mask_pii(ner: Callable, text: ) -> Tuple[, ]

```

Mask PII in text.
Source code in `llama-index-core/llama_index/core/postprocessor/pii.py`  
| 
```
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
defmask_pii(self, ner: Callable, text: str) -> Tuple[str, Dict]:
"""Mask PII in text."""
    new_text = text
    response = ner(text)
    mapping = {}
    for entry in response:
        entity_group_tag = f"[{entry['entity_group']}_{entry['start']}]"
        new_text = new_text.replace(entry["word"], entity_group_tag).strip()
        mapping[entity_group_tag] = entry["word"]
    return new_text, mapping

```
 |  
| --- | --- |  
##  PIINodePostprocessor [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.PIINodePostprocessor "Permanent link")
Bases: 
PII Node processor.
NOTE: this is a beta feature, the API might change.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `llm`  |  The local LLM to use for prediction.  |  _required_  |  
|  `pii_str_tmpl`  |  `'The current context information is provided. \nA task is also provided to mask the PII within the context. \nReturn the text, with all PII masked out, and a mapping of the original PII to the masked PII. \nReturn the output of the task in JSON. \nContext:\nHello Zhang Wei, I am John. Your AnyCompany Financial Services, LLC credit card account 1111-0000-1111-0008 has a minimum payment of $24.53 that is due by July 31st. Based on your autopay settings, we will withdraw your payment. Task: Mask out the PII, replace each PII with a tag, and return the text. Return the mapping in JSON. \nOutput: \nHello [NAME1], I am [NAME2]. Your AnyCompany Financial Services, LLC credit card account [CREDIT_CARD_NUMBER] has a minimum payment of $24.53 that is due by [DATE_TIME]. Based on your autopay settings, we will withdraw your payment. Output Mapping:\n{{"NAME1": "Zhang Wei", "NAME2": "John", "CREDIT_CARD_NUMBER": "1111-0000-1111-0008", "DATE_TIME": "July 31st"}}\nContext:\n{context_str}\nTask: {query_str}\nOutput: \n'`  |  
|  `pii_node_info_key`  |  `'__pii_node_info__'`  |  
Source code in `llama-index-core/llama_index/core/postprocessor/pii.py`  
| 
```
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
classPIINodePostprocessor(BaseNodePostprocessor):
"""
    PII Node processor.

    NOTE: this is a beta feature, the API might change.

    Args:
        llm (LLM): The local LLM to use for prediction.

    """

    llm: LLM
    pii_str_tmpl: str = DEFAULT_PII_TMPL
    pii_node_info_key: str = "__pii_node_info__"

    @classmethod
    defclass_name(cls) -> str:
        return "PIINodePostprocessor"

    defmask_pii(self, text: str) -> Tuple[str, Dict]:
"""Mask PII in text."""
        pii_prompt = PromptTemplate(self.pii_str_tmpl)
        # TODO: allow customization
        task_str = (
            "Mask out the PII, replace each PII with a tag, and return the text. "
            "Return the mapping in JSON."
        )

        response = self.llm.predict(pii_prompt, context_str=text, query_str=task_str)
        splits = response.split("Output Mapping:")
        text_output = splits[0].strip()
        json_str_output = splits[1].strip()
        json_dict = json.loads(json_str_output)
        return text_output, json_dict

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""
        # swap out text from nodes, with the original node mappings
        new_nodes = []
        for node_with_score in nodes:
            node = node_with_score.node
            new_text, mapping_info = self.mask_pii(
                node.get_content(metadata_mode=MetadataMode.LLM)
            )
            new_node = deepcopy(node)
            new_node.excluded_embed_metadata_keys.append(self.pii_node_info_key)
            new_node.excluded_llm_metadata_keys.append(self.pii_node_info_key)
            new_node.metadata[self.pii_node_info_key] = mapping_info
            new_node.set_content(new_text)
            new_nodes.append(NodeWithScore(node=new_node, score=node_with_score.score))

        return new_nodes

```
 |  
| --- | --- |  
###  mask_pii [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.PIINodePostprocessor.mask_pii "Permanent link")

```
mask_pii(text: ) -> Tuple[, ]

```

Mask PII in text.
Source code in `llama-index-core/llama_index/core/postprocessor/pii.py`  
| 
```
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
defmask_pii(self, text: str) -> Tuple[str, Dict]:
"""Mask PII in text."""
    pii_prompt = PromptTemplate(self.pii_str_tmpl)
    # TODO: allow customization
    task_str = (
        "Mask out the PII, replace each PII with a tag, and return the text. "
        "Return the mapping in JSON."
    )

    response = self.llm.predict(pii_prompt, context_str=text, query_str=task_str)
    splits = response.split("Output Mapping:")
    text_output = splits[0].strip()
    json_str_output = splits[1].strip()
    json_dict = json.loads(json_str_output)
    return text_output, json_dict

```
 |  
| --- | --- |  
##  SentenceTransformerRerank [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/time_weighted/#llama_index.core.postprocessor.SentenceTransformerRerank "Permanent link")
Bases: 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  Sentence transformer model name.  |  _required_  |  
|  `top_n`  |  Number of nodes to return sorted by score.  |  _required_  |  
|  `device`  |  Device to use for sentence transformer.  |  `'cpu'`  |  
|  `keep_retrieval_score`  |  `bool`  |  Whether to keep the retrieval score in metadata.  |  `False`  |  
|  `trust_remote_code`  |  `bool`  |  Whether to trust remote code.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/postprocessor/sbert_rerank.py`  
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
```
 | 
```
classSentenceTransformerRerank(BaseNodePostprocessor):
    model: str = Field(description="Sentence transformer model name.")
    top_n: int = Field(description="Number of nodes to return sorted by score.")
    device: str = Field(
        default="cpu",
        description="Device to use for sentence transformer.",
    )
    keep_retrieval_score: bool = Field(
        default=False,
        description="Whether to keep the retrieval score in metadata.",
    )
    trust_remote_code: bool = Field(
        default=False,
        description="Whether to trust remote code.",
    )
    _model: Any = PrivateAttr()

    def__init__(
        self,
        top_n: int = 2,
        model: str = "cross-encoder/stsb-distilroberta-base",
        device: Optional[str] = None,
        keep_retrieval_score: bool = False,
        trust_remote_code: bool = True,
    ):
        try:
            fromsentence_transformersimport CrossEncoder  # pants: no-infer-dep
        except ImportError:
            raise ImportError(
                "Cannot import sentence-transformers or torch package,",
                "please `pip install torch sentence-transformers`",
            )
        device = infer_torch_device() if device is None else device
        super().__init__(
            top_n=top_n,
            model=model,
            device=device,
            keep_retrieval_score=keep_retrieval_score,
        )
        self._model = CrossEncoder(
            model,
            max_length=DEFAULT_SENTENCE_TRANSFORMER_MAX_LENGTH,
            device=device,
            trust_remote_code=trust_remote_code,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "SentenceTransformerRerank"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        if query_bundle is None:
            raise ValueError("Missing query bundle in extra info.")
        if len(nodes) == 0:
            return []

        query_and_nodes = [
            (
                query_bundle.query_str,
                node.node.get_content(metadata_mode=MetadataMode.EMBED),
            )
            for node in nodes
        ]

        with self.callback_manager.event(
            CBEventType.RERANKING,
            payload={
                EventPayload.NODES: nodes,
                EventPayload.MODEL_NAME: self.model,
                EventPayload.QUERY_STR: query_bundle.query_str,
                EventPayload.TOP_K: self.top_n,
            },
        ) as event:
            scores = self._model.predict(query_and_nodes)

            assert len(scores) == len(nodes)

            for node, score in zip(nodes, scores):
                if self.keep_retrieval_score:
                    # keep the retrieval score in metadata
                    node.node.metadata["retrieval_score"] = node.score
                node.score = score

            new_nodes = sorted(nodes, key=lambda x: -x.score if x.score else 0)[
                : self.top_n
            ]
            event.on_end(payload={EventPayload.NODES: new_nodes})

        return new_nodes

```
 |  
| --- | --- |  
options: members: - TimeWeightedPostprocessors
