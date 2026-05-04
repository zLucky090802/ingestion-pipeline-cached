# Pydantic
##  BaseExtractor [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.BaseExtractor "Permanent link")
Bases: 
Metadata extractor.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `is_text_node_only`  |  `bool`  |  `True`  |  
|  `show_progress`  |  `bool`  |  Whether to show progress.  |  `True`  |  
|  `metadata_mode`  |  `MetadataMode`  |  Metadata mode to use when reading nodes.  |  `<MetadataMode.ALL: 'all'>`  |  
|  `node_text_template`  |  Template to represent how node text is mixed with metadata text.  |  `'[Excerpt from document]\n{metadata_str}\nExcerpt:\n-----\n{content}\n-----\n'`  |  
|  `disable_template_rewrite`  |  `bool`  |  Disable the node template rewrite.  |  `False`  |  
|  `in_place`  |  `bool`  |  Whether to process nodes in place.  |  `True`  |  
|  `num_workers`  |  Number of workers to use for concurrent async processing.  |  
|  `max_retries`  |  Maximum number of retry attempts when aextract() raises an exception. 0 means no retries (fail immediately, preserving current behaviour).  |  
|  `retry_backoff`  |  `float`  |  Base delay in seconds for exponential backoff between retries. Actual delay is retry_backoff * 2^attempt.  |  `1.0`  |  
|  `raise_on_error`  |  `bool`  |  Whether to raise exceptions when extraction fails after all retries. If True, the exception propagates (current behaviour). If False, logs a warning and returns empty metadata dicts.  |  `True`  |  
Source code in `llama-index-core/llama_index/core/extractors/interface.py`  
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
```
 | 
```
classBaseExtractor(TransformComponent):
"""Metadata extractor."""

    is_text_node_only: bool = True

    show_progress: bool = Field(default=True, description="Whether to show progress.")

    metadata_mode: MetadataMode = Field(
        default=MetadataMode.ALL, description="Metadata mode to use when reading nodes."
    )

    node_text_template: str = Field(
        default=DEFAULT_NODE_TEXT_TEMPLATE,
        description="Template to represent how node text is mixed with metadata text.",
    )
    disable_template_rewrite: bool = Field(
        default=False, description="Disable the node template rewrite."
    )

    in_place: bool = Field(
        default=True, description="Whether to process nodes in place."
    )

    num_workers: int = Field(
        default=4,
        description="Number of workers to use for concurrent async processing.",
    )

    max_retries: int = Field(
        default=0,
        description=(
            "Maximum number of retry attempts when aextract() raises an exception. "
            "0 means no retries (fail immediately, preserving current behaviour)."
        ),
    )

    retry_backoff: float = Field(
        default=1.0,
        description=(
            "Base delay in seconds for exponential backoff between retries. "
            "Actual delay is retry_backoff * 2^attempt."
        ),
    )

    raise_on_error: bool = Field(
        default=True,
        description=(
            "Whether to raise exceptions when extraction fails after all retries. "
            "If True, the exception propagates (current behaviour). "
            "If False, logs a warning and returns empty metadata dicts."
        ),
    )

    @classmethod
    deffrom_dict(cls, data: Dict[str, Any], **kwargs: Any) -> Self:  # type: ignore
        if isinstance(kwargs, dict):
            data.update(kwargs)

        data.pop("class_name", None)

        llm_predictor = data.get("llm_predictor")
        if llm_predictor:
            fromllama_index.core.llm_predictor.loadingimport load_predictor

            llm_predictor = load_predictor(llm_predictor)
            data["llm_predictor"] = llm_predictor

        llm = data.get("llm")
        if llm:
            fromllama_index.core.llms.loadingimport load_llm

            llm = load_llm(llm)
            data["llm"] = llm

        return cls(**data)

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "MetadataExtractor"

    @abstractmethod
    async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
        Extracts metadata for a sequence of nodes, returning a list of
        metadata dictionaries corresponding to each node.

        Args:
            nodes (Sequence[Document]): nodes to extract metadata from

        """

    defextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
        Extracts metadata for a sequence of nodes, returning a list of
        metadata dictionaries corresponding to each node.

        Args:
            nodes (Sequence[Document]): nodes to extract metadata from

        """
        return asyncio_run(self.aextract(nodes))

    async def_aextract_with_retry(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""Call aextract() with optional retry and error-policy logic."""
        last_exception: Optional[Exception] = None
        for attempt in range(1 + self.max_retries):
            try:
                return await self.aextract(nodes)
            except Exception as e:
                last_exception = e
                if attempt  self.max_retries:
                    delay = self.retry_backoff * (2**attempt)
                    logger.warning(
                        "Extraction attempt %d/%d failed (%s), retrying in %.1fs ...",
                        attempt + 1,
                        self.max_retries + 1,
                        e,
                        delay,
                    )
                    await asyncio.sleep(delay)

        # All retries exhausted
        if not self.raise_on_error:
            logger.warning(
                "Extraction failed after %d attempt(s) (%s). "
                "Returning empty metadata for %d node(s).",
                self.max_retries + 1,
                last_exception,
                len(nodes),
            )
            return [{} for _ in nodes]

        raise last_exception  # type: ignore[misc]

    async defaprocess_nodes(
        self,
        nodes: Sequence[BaseNode],
        excluded_embed_metadata_keys: Optional[List[str]] = None,
        excluded_llm_metadata_keys: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""
        Post process nodes parsed from documents.

        Allows extractors to be chained.

        Args:
            nodes (List[BaseNode]): nodes to post-process
            excluded_embed_metadata_keys (Optional[List[str]]):
                keys to exclude from embed metadata
            excluded_llm_metadata_keys (Optional[List[str]]):
                keys to exclude from llm metadata

        """
        if self.in_place:
            new_nodes = nodes
        else:
            new_nodes = [deepcopy(node) for node in nodes]

        cur_metadata_list = await self._aextract_with_retry(new_nodes)
        for idx, node in enumerate(new_nodes):
            node.metadata.update(cur_metadata_list[idx])

        for idx, node in enumerate(new_nodes):
            if excluded_embed_metadata_keys is not None:
                node.excluded_embed_metadata_keys.extend(excluded_embed_metadata_keys)
            if excluded_llm_metadata_keys is not None:
                node.excluded_llm_metadata_keys.extend(excluded_llm_metadata_keys)
            if not self.disable_template_rewrite:
                if isinstance(node, TextNode):
                    cast(TextNode, node).text_template = self.node_text_template

        return new_nodes  # type: ignore

    defprocess_nodes(
        self,
        nodes: Sequence[BaseNode],
        excluded_embed_metadata_keys: Optional[List[str]] = None,
        excluded_llm_metadata_keys: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[BaseNode]:
        return asyncio_run(
            self.aprocess_nodes(
                nodes,
                excluded_embed_metadata_keys=excluded_embed_metadata_keys,
                excluded_llm_metadata_keys=excluded_llm_metadata_keys,
                **kwargs,
            )
        )

    def__call__(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
"""
        Post process nodes parsed from documents.

        Allows extractors to be chained.

        Args:
            nodes (List[BaseNode]): nodes to post-process

        """
        return self.process_nodes(nodes, **kwargs)

    async defacall(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
"""
        Post process nodes parsed from documents.

        Allows extractors to be chained.

        Args:
            nodes (List[BaseNode]): nodes to post-process

        """
        return await self.aprocess_nodes(nodes, **kwargs)

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.BaseExtractor.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/extractors/interface.py`  
| 
```
102
103
104
105
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "MetadataExtractor"

```
 |  
| --- | --- |  
###  aextract `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.BaseExtractor.aextract "Permanent link")

```
aextract(nodes: Sequence[]) -> []

```

Extracts metadata for a sequence of nodes, returning a list of metadata dictionaries corresponding to each node.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Sequence[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]`  |  nodes to extract metadata from  |  _required_  |  
Source code in `llama-index-core/llama_index/core/extractors/interface.py`  
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
```
 | 
```
@abstractmethod
async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
    Extracts metadata for a sequence of nodes, returning a list of
    metadata dictionaries corresponding to each node.

    Args:
        nodes (Sequence[Document]): nodes to extract metadata from

    """

```
 |  
| --- | --- |  
###  extract [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.BaseExtractor.extract "Permanent link")

```
extract(nodes: Sequence[]) -> []

```

Extracts metadata for a sequence of nodes, returning a list of metadata dictionaries corresponding to each node.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Sequence[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]`  |  nodes to extract metadata from  |  _required_  |  
Source code in `llama-index-core/llama_index/core/extractors/interface.py`  
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
```
 | 
```
defextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
    Extracts metadata for a sequence of nodes, returning a list of
    metadata dictionaries corresponding to each node.

    Args:
        nodes (Sequence[Document]): nodes to extract metadata from

    """
    return asyncio_run(self.aextract(nodes))

```
 |  
| --- | --- |  
###  aprocess_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.BaseExtractor.aprocess_nodes "Permanent link")

```
aprocess_nodes(
    nodes: Sequence[],
    excluded_embed_metadata_keys: Optional[
        []
    ] = None,
    excluded_llm_metadata_keys: Optional[[]] = None,
    **kwargs: 
) -> []

```

Post process nodes parsed from documents.
Allows extractors to be chained.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  nodes to post-process  |  _required_  |  
|  `excluded_embed_metadata_keys`  |  `Optional[List[str]]`  |  keys to exclude from embed metadata  |  `None`  |  
|  `excluded_llm_metadata_keys`  |  `Optional[List[str]]`  |  keys to exclude from llm metadata  |  `None`  |  
Source code in `llama-index-core/llama_index/core/extractors/interface.py`  
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
```
 | 
```
async defaprocess_nodes(
    self,
    nodes: Sequence[BaseNode],
    excluded_embed_metadata_keys: Optional[List[str]] = None,
    excluded_llm_metadata_keys: Optional[List[str]] = None,
    **kwargs: Any,
) -> List[BaseNode]:
"""
    Post process nodes parsed from documents.

    Allows extractors to be chained.

    Args:
        nodes (List[BaseNode]): nodes to post-process
        excluded_embed_metadata_keys (Optional[List[str]]):
            keys to exclude from embed metadata
        excluded_llm_metadata_keys (Optional[List[str]]):
            keys to exclude from llm metadata

    """
    if self.in_place:
        new_nodes = nodes
    else:
        new_nodes = [deepcopy(node) for node in nodes]

    cur_metadata_list = await self._aextract_with_retry(new_nodes)
    for idx, node in enumerate(new_nodes):
        node.metadata.update(cur_metadata_list[idx])

    for idx, node in enumerate(new_nodes):
        if excluded_embed_metadata_keys is not None:
            node.excluded_embed_metadata_keys.extend(excluded_embed_metadata_keys)
        if excluded_llm_metadata_keys is not None:
            node.excluded_llm_metadata_keys.extend(excluded_llm_metadata_keys)
        if not self.disable_template_rewrite:
            if isinstance(node, TextNode):
                cast(TextNode, node).text_template = self.node_text_template

    return new_nodes  # type: ignore

```
 |  
| --- | --- |  
###  acall [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.BaseExtractor.acall "Permanent link")

```
acall(
    nodes: Sequence[], **kwargs: 
) -> []

```

Post process nodes parsed from documents.
Allows extractors to be chained.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  nodes to post-process  |  _required_  |  
Source code in `llama-index-core/llama_index/core/extractors/interface.py`  
| 
```
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
```
 | 
```
async defacall(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
"""
    Post process nodes parsed from documents.

    Allows extractors to be chained.

    Args:
        nodes (List[BaseNode]): nodes to post-process

    """
    return await self.aprocess_nodes(nodes, **kwargs)

```
 |  
| --- | --- |  
##  KeywordExtractor [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.KeywordExtractor "Permanent link")
Bases: 
Keyword extractor. Node-level extractor. Extracts `excerpt_keywords` metadata field.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `llm`  |  `None`  |  
|  `keywords`  |  number of keywords to extract  |  
|  `prompt_template`  |  template for keyword extraction  |  `DEFAULT_KEYWORD_EXTRACT_TEMPLATE`  |  
Source code in `llama-index-core/llama_index/core/extractors/metadata_extractors.py`  
| 
```
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
```
 | 
```
classKeywordExtractor(BaseExtractor):
"""
    Keyword extractor. Node-level extractor. Extracts
    `excerpt_keywords` metadata field.

    Args:
        llm (Optional[LLM]): LLM
        keywords (int): number of keywords to extract
        prompt_template (str): template for keyword extraction

    """

    llm: SerializeAsAny[LLM] = Field(description="The LLM to use for generation.")
    keywords: int = Field(
        default=5, description="The number of keywords to extract.", gt=0
    )

    prompt_template: str = Field(
        default=DEFAULT_KEYWORD_EXTRACT_TEMPLATE,
        description="Prompt template to use when generating keywords.",
    )

    def__init__(
        self,
        llm: Optional[LLM] = None,
        # TODO: llm_predictor arg is deprecated
        llm_predictor: Optional[LLM] = None,
        keywords: int = 5,
        prompt_template: str = DEFAULT_KEYWORD_EXTRACT_TEMPLATE,
        num_workers: int = DEFAULT_NUM_WORKERS,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        if keywords  1:
            raise ValueError("num_keywords must be >= 1")

        super().__init__(
            llm=llm or llm_predictor or Settings.llm,
            keywords=keywords,
            prompt_template=prompt_template,
            num_workers=num_workers,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "KeywordExtractor"

    async def_aextract_keywords_from_node(self, node: BaseNode) -> Dict[str, str]:
"""Extract keywords from a node and return it's metadata dict."""
        if self.is_text_node_only and not isinstance(node, TextNode):
            return {}

        context_str = node.get_content(metadata_mode=self.metadata_mode)
        keywords = await self.llm.apredict(
            PromptTemplate(template=self.prompt_template),
            keywords=self.keywords,
            context_str=context_str,
        )

        return {"excerpt_keywords": keywords.strip()}

    async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
        keyword_jobs = []
        for node in nodes:
            keyword_jobs.append(self._aextract_keywords_from_node(node))

        metadata_list: List[Dict] = await run_jobs(
            keyword_jobs, show_progress=self.show_progress, workers=self.num_workers
        )

        return metadata_list

```
 |  
| --- | --- |  
##  PydanticProgramExtractor [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.PydanticProgramExtractor "Permanent link")
Bases: , `Generic[Model]`
Pydantic program extractor.
Uses an LLM to extract out a Pydantic object. Return attributes of that object in a dictionary.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `program`  |  `BasePydanticProgram[](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BasePydanticProgram "BasePydanticProgram \(llama_index.core.types.BasePydanticProgram\)")[Model]`  |  Pydantic program to extract.  |  _required_  |  
|  `input_key`  |  Key to use as input to the program (the program template string must expose this key).  |  `'input'`  |  
|  `extract_template_str`  |  Template to use for extraction.  |  `'Here is the content of the section:\n----------------\n{context_str}\n----------------\nGiven the contextual information, extract out a {class_name} object.'`  |  
Source code in `llama-index-core/llama_index/core/extractors/metadata_extractors.py`  
| 
```
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
515
516
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
```
 | 
```
classPydanticProgramExtractor(BaseExtractor, Generic[Model]):
"""
    Pydantic program extractor.

    Uses an LLM to extract out a Pydantic object. Return attributes of that object
    in a dictionary.

    """

    program: SerializeAsAny[BasePydanticProgram[Model]] = Field(
        ..., description="Pydantic program to extract."
    )
    input_key: str = Field(
        default="input",
        description=(
            "Key to use as input to the program (the program "
            "template string must expose this key)."
        ),
    )
    extract_template_str: str = Field(
        default=DEFAULT_EXTRACT_TEMPLATE_STR,
        description="Template to use for extraction.",
    )

    @classmethod
    defclass_name(cls) -> str:
        return "PydanticModelExtractor"

    async def_acall_program(self, node: BaseNode) -> Dict[str, Any]:
"""Call the program on a node."""
        if self.is_text_node_only and not isinstance(node, TextNode):
            return {}

        extract_str = self.extract_template_str.format(
            context_str=node.get_content(metadata_mode=self.metadata_mode),
            class_name=self.program.output_cls.__name__,
        )

        ret_object = await self.program.acall(**{self.input_key: extract_str})
        assert not isinstance(ret_object, list)

        return ret_object.model_dump()

    async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""Extract pydantic program."""
        program_jobs = []
        for node in nodes:
            program_jobs.append(self._acall_program(node))

        metadata_list: List[Dict] = await run_jobs(
            program_jobs, show_progress=self.show_progress, workers=self.num_workers
        )

        return metadata_list

```
 |  
| --- | --- |  
###  aextract [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.PydanticProgramExtractor.aextract "Permanent link")

```
aextract(nodes: Sequence[]) -> []

```

Extract pydantic program.
Source code in `llama-index-core/llama_index/core/extractors/metadata_extractors.py`  
| 
```
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
```
 | 
```
async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""Extract pydantic program."""
    program_jobs = []
    for node in nodes:
        program_jobs.append(self._acall_program(node))

    metadata_list: List[Dict] = await run_jobs(
        program_jobs, show_progress=self.show_progress, workers=self.num_workers
    )

    return metadata_list

```
 |  
| --- | --- |  
##  QuestionsAnsweredExtractor [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.QuestionsAnsweredExtractor "Permanent link")
Bases: 
Questions answered extractor. Node-level extractor. Extracts `questions_this_excerpt_can_answer` metadata field.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `llm`  |  `None`  |  
|  `questions`  |  number of questions to extract  |  
|  `prompt_template`  |  template for question extraction,  |  `DEFAULT_QUESTION_GEN_TMPL`  |  
|  `embedding_only`  |  `bool`  |  whether to use embedding only  |  `True`  |  
Source code in `llama-index-core/llama_index/core/extractors/metadata_extractors.py`  
| 
```
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
```
 | 
```
classQuestionsAnsweredExtractor(BaseExtractor):
"""
    Questions answered extractor. Node-level extractor.
    Extracts `questions_this_excerpt_can_answer` metadata field.

    Args:
        llm (Optional[LLM]): LLM
        questions (int): number of questions to extract
        prompt_template (str): template for question extraction,
        embedding_only (bool): whether to use embedding only

    """

    llm: SerializeAsAny[LLM] = Field(description="The LLM to use for generation.")
    questions: int = Field(
        default=5,
        description="The number of questions to generate.",
        gt=0,
    )
    prompt_template: str = Field(
        default=DEFAULT_QUESTION_GEN_TMPL,
        description="Prompt template to use when generating questions.",
    )
    embedding_only: bool = Field(
        default=True, description="Whether to use metadata for emebddings only."
    )

    def__init__(
        self,
        llm: Optional[LLM] = None,
        # TODO: llm_predictor arg is deprecated
        llm_predictor: Optional[LLM] = None,
        questions: int = 5,
        prompt_template: str = DEFAULT_QUESTION_GEN_TMPL,
        embedding_only: bool = True,
        num_workers: int = DEFAULT_NUM_WORKERS,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        if questions  1:
            raise ValueError("questions must be >= 1")

        super().__init__(
            llm=llm or llm_predictor or Settings.llm,
            questions=questions,
            prompt_template=prompt_template,
            embedding_only=embedding_only,
            num_workers=num_workers,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "QuestionsAnsweredExtractor"

    async def_aextract_questions_from_node(self, node: BaseNode) -> Dict[str, str]:
"""Extract questions from a node and return it's metadata dict."""
        if self.is_text_node_only and not isinstance(node, TextNode):
            return {}

        context_str = node.get_content(metadata_mode=self.metadata_mode)
        prompt = PromptTemplate(template=self.prompt_template)
        questions = await self.llm.apredict(
            prompt, num_questions=self.questions, context_str=context_str
        )

        return {"questions_this_excerpt_can_answer": questions.strip()}

    async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
        questions_jobs = []
        for node in nodes:
            questions_jobs.append(self._aextract_questions_from_node(node))

        metadata_list: List[Dict] = await run_jobs(
            questions_jobs, show_progress=self.show_progress, workers=self.num_workers
        )

        return metadata_list

```
 |  
| --- | --- |  
##  SummaryExtractor [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.SummaryExtractor "Permanent link")
Bases: 
Summary extractor. Node-level extractor with adjacent sharing. Extracts `section_summary`, `prev_section_summary`, `next_section_summary` metadata fields.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `llm`  |  `None`  |  
|  `summaries`  |  `List[str]`  |  list of summaries to extract: 'self', 'prev', 'next'  |  `['self']`  |  
|  `prompt_template`  |  template for summary extraction  |  `DEFAULT_SUMMARY_EXTRACT_TEMPLATE`  |  
Source code in `llama-index-core/llama_index/core/extractors/metadata_extractors.py`  
| 
```
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
```
 | 
```
classSummaryExtractor(BaseExtractor):
"""
    Summary extractor. Node-level extractor with adjacent sharing.
    Extracts `section_summary`, `prev_section_summary`, `next_section_summary`
    metadata fields.

    Args:
        llm (Optional[LLM]): LLM
        summaries (List[str]): list of summaries to extract: 'self', 'prev', 'next'
        prompt_template (str): template for summary extraction

    """

    llm: SerializeAsAny[LLM] = Field(description="The LLM to use for generation.")
    summaries: List[str] = Field(
        description="List of summaries to extract: 'self', 'prev', 'next'"
    )
    prompt_template: str = Field(
        default=DEFAULT_SUMMARY_EXTRACT_TEMPLATE,
        description="Template to use when generating summaries.",
    )

    _self_summary: bool = PrivateAttr()
    _prev_summary: bool = PrivateAttr()
    _next_summary: bool = PrivateAttr()

    def__init__(
        self,
        llm: Optional[LLM] = None,
        # TODO: llm_predictor arg is deprecated
        llm_predictor: Optional[LLM] = None,
        summaries: List[str] = ["self"],
        prompt_template: str = DEFAULT_SUMMARY_EXTRACT_TEMPLATE,
        num_workers: int = DEFAULT_NUM_WORKERS,
        **kwargs: Any,
    ):
        # validation
        if not all(s in ["self", "prev", "next"] for s in summaries):
            raise ValueError("summaries must be one of ['self', 'prev', 'next']")

        super().__init__(
            llm=llm or llm_predictor or Settings.llm,
            summaries=summaries,
            prompt_template=prompt_template,
            num_workers=num_workers,
            **kwargs,
        )

        self._self_summary = "self" in summaries
        self._prev_summary = "prev" in summaries
        self._next_summary = "next" in summaries

    @classmethod
    defclass_name(cls) -> str:
        return "SummaryExtractor"

    async def_agenerate_node_summary(self, node: BaseNode) -> str:
"""Generate a summary for a node."""
        if self.is_text_node_only and not isinstance(node, TextNode):
            return ""

        context_str = node.get_content(metadata_mode=self.metadata_mode)
        summary = await self.llm.apredict(
            PromptTemplate(template=self.prompt_template), context_str=context_str
        )

        return summary.strip()

    async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
        if not all(isinstance(node, TextNode) for node in nodes):
            raise ValueError("Only `TextNode` is allowed for `Summary` extractor")

        node_summaries_jobs = []
        for node in nodes:
            node_summaries_jobs.append(self._agenerate_node_summary(node))

        node_summaries = await run_jobs(
            node_summaries_jobs,
            show_progress=self.show_progress,
            workers=self.num_workers,
        )

        # Extract node-level summary metadata
        metadata_list: List[Dict] = [{} for _ in nodes]
        for i, metadata in enumerate(metadata_list):
            if i  0 and self._prev_summary and node_summaries[i - 1]:
                metadata["prev_section_summary"] = node_summaries[i - 1]
            if i  len(nodes) - 1 and self._next_summary and node_summaries[i + 1]:
                metadata["next_section_summary"] = node_summaries[i + 1]
            if self._self_summary and node_summaries[i]:
                metadata["section_summary"] = node_summaries[i]

        return metadata_list

```
 |  
| --- | --- |  
##  TitleExtractor [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.TitleExtractor "Permanent link")
Bases: 
Title extractor. Useful for long documents. Extracts `document_title` metadata field.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `llm`  |  `None`  |  
|  `nodes`  |  number of nodes from front to use for title extraction  |  
|  `node_template`  |  template for node-level title clues extraction  |  `DEFAULT_TITLE_NODE_TEMPLATE`  |  
|  `combine_template`  |  template for combining node-level clues into a document-level title  |  `DEFAULT_TITLE_COMBINE_TEMPLATE`  |  
|  `is_text_node_only`  |  `bool`  |  `False`  |  
Source code in `llama-index-core/llama_index/core/extractors/metadata_extractors.py`  
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
```
 | 
```
classTitleExtractor(BaseExtractor):
"""
    Title extractor. Useful for long documents. Extracts `document_title`
    metadata field.

    Args:
        llm (Optional[LLM]): LLM
        nodes (int): number of nodes from front to use for title extraction
        node_template (str): template for node-level title clues extraction
        combine_template (str): template for combining node-level clues into
            a document-level title

    """

    is_text_node_only: bool = False  # can work for mixture of text and non-text nodes
    llm: SerializeAsAny[LLM] = Field(description="The LLM to use for generation.")
    nodes: int = Field(
        default=5,
        description="The number of nodes to extract titles from.",
        gt=0,
    )
    node_template: str = Field(
        default=DEFAULT_TITLE_NODE_TEMPLATE,
        description="The prompt template to extract titles with.",
    )
    combine_template: str = Field(
        default=DEFAULT_TITLE_COMBINE_TEMPLATE,
        description="The prompt template to merge titles with.",
    )

    def__init__(
        self,
        llm: Optional[LLM] = None,
        # TODO: llm_predictor arg is deprecated
        llm_predictor: Optional[LLM] = None,
        nodes: int = 5,
        node_template: str = DEFAULT_TITLE_NODE_TEMPLATE,
        combine_template: str = DEFAULT_TITLE_COMBINE_TEMPLATE,
        num_workers: int = DEFAULT_NUM_WORKERS,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        if nodes  1:
            raise ValueError("num_nodes must be >= 1")

        super().__init__(
            llm=llm or llm_predictor or Settings.llm,
            nodes=nodes,
            node_template=node_template,
            combine_template=combine_template,
            num_workers=num_workers,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "TitleExtractor"

    async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
        nodes_by_doc_id = self.separate_nodes_by_ref_id(nodes)
        titles_by_doc_id = await self.extract_titles(nodes_by_doc_id)
        return [{"document_title": titles_by_doc_id[node.ref_doc_id]} for node in nodes]

    deffilter_nodes(self, nodes: Sequence[BaseNode]) -> List[BaseNode]:
        filtered_nodes: List[BaseNode] = []
        for node in nodes:
            if self.is_text_node_only and not isinstance(node, TextNode):
                continue
            filtered_nodes.append(node)
        return filtered_nodes

    defseparate_nodes_by_ref_id(self, nodes: Sequence[BaseNode]) -> Dict:
        separated_items: Dict[Optional[str], List[BaseNode]] = {}

        for node in nodes:
            key = node.ref_doc_id
            if key not in separated_items:
                separated_items[key] = []

            if len(separated_items[key])  self.nodes:
                separated_items[key].append(node)

        return separated_items

    async defextract_titles(self, nodes_by_doc_id: Dict) -> Dict:
        jobs = []
        final_dict = {}

        async defget_titles_by_doc(nodes: List[BaseNode], key: str) -> Dict:
            titles_by_doc_id = {}
            title_candidates = await self.get_title_candidates(nodes)
            combined_titles = ", ".join(title_candidates)
            titles_by_doc_id[key] = await self.llm.apredict(
                PromptTemplate(template=self.combine_template),
                context_str=combined_titles,
            )
            return titles_by_doc_id

        for key, nodes in nodes_by_doc_id.items():
            jobs.append(get_titles_by_doc(nodes, key))
        list_dict_titles: List[Dict] = await run_jobs(
            jobs=jobs,
            show_progress=self.show_progress,
        )
        for d in list_dict_titles:
            for key, value in d.items():
                final_dict.update({key: value})
        return final_dict

    async defget_title_candidates(self, nodes: List[BaseNode]) -> List[str]:
        return [
            await self.llm.apredict(
                PromptTemplate(template=self.node_template),
                context_str=cast(TextNode, node).text,
            )
            for node in nodes
        ]

```
 |  
| --- | --- |  
##  DocumentContextExtractor [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.DocumentContextExtractor "Permanent link")
Bases: 
An LLM-based context extractor for enhancing RAG accuracy through document analysis.
! Nodes that already have the 'key' in node.metadata will NOT be processed - will be skipped !
This extractor processes documents and their nodes to generate contextual metadata, implementing the approach described in the Anthropic "Contextual Retrieval" blog post. It handles rate limits, document size constraints, and parallel processing of nodes.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
Example

```
extractor = DocumentContextExtractor(
    docstore=my_docstore,
    llm=my_llm,
    max_context_length=64000,
    max_output_tokens=256
)
metadata_list = await extractor.aextract(nodes)

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `num_workers`  |  
|  `llm`  |  _required_  |  
|  `docstore`  |   |  _required_  |  
|  `key`  |  _required_  |  
|  `prompt`  |  _required_  |  
|  `doc_ids`  |  `Set[str]`  |  _required_  |  
|  `max_context_length`  |  _required_  |  
|  `max_output_tokens`  |  _required_  |  
|  `oversized_document_strategy`  |  `Literal['warn', 'error', 'ignore']`  |  _required_  |  
|  `DEFAULT_KEY`  |  `'context'`  |  
Source code in `llama-index-core/llama_index/core/extractors/document_context.py`  
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
```
 | 
```
classDocumentContextExtractor(BaseExtractor):
"""
    An LLM-based context extractor for enhancing RAG accuracy through document analysis.

    ! Nodes that already have the 'key' in node.metadata will NOT be processed - will be skipped !

    This extractor processes documents and their nodes to generate contextual metadata,
    implementing the approach described in the Anthropic "Contextual Retrieval" blog post.
    It handles rate limits, document size constraints, and parallel processing of nodes.

    Attributes:
        llm (LLM): Language model instance for generating context
        docstore (BaseDocumentStore): Storage for parent documents
        key (str): Metadata key for storing extracted context
        prompt (str): Prompt template for context generation
        doc_ids (Set[str]): Set of processed document IDs
        max_context_length (int): Maximum allowed document context length
        max_output_tokens (int): Maximum tokens in generated context
        oversized_document_strategy (OversizeStrategy): Strategy for handling large documents

    Example:
        ```python
        extractor = DocumentContextExtractor(
            docstore=my_docstore,
            llm=my_llm,
            max_context_length=64000,
            max_output_tokens=256

        metadata_list = await extractor.aextract(nodes)
        ```

    """

    # Pydantic fields
    llm: LLM
    docstore: BaseDocumentStore
    key: str
    prompt: str
    doc_ids: Set[str]
    max_context_length: int
    max_output_tokens: int
    oversized_document_strategy: OversizeStrategy
    num_workers: int = DEFAULT_NUM_WORKERS

    ORIGINAL_CONTEXT_PROMPT: ClassVar[str] = ORIGINAL_CONTEXT_PROMPT
    SUCCINCT_CONTEXT_PROMPT: ClassVar[str] = SUCCINCT_CONTEXT_PROMPT

    DEFAULT_KEY: str = "context"

    def__init__(
        self,
        docstore: BaseDocumentStore,
        llm: Optional[LLM] = None,
        max_context_length: int = 1000,
        key: str = DEFAULT_KEY,
        prompt: str = ORIGINAL_CONTEXT_PROMPT,
        num_workers: int = DEFAULT_NUM_WORKERS,
        max_output_tokens: int = 512,
        oversized_document_strategy: OversizeStrategy = "warn",
        **kwargs: Any,
    ) -> None:
"""Init params."""
        assert hasattr(
            llm, "achat"
        )  # not all LLMs have this, particularly the huggingfaceapi ones.

        super().__init__(
            llm=llm or Settings.llm,
            docstore=docstore,
            key=key,
            prompt=prompt,
            doc_ids=set(),
            max_context_length=max_context_length,
            max_output_tokens=max_output_tokens,
            oversized_document_strategy=oversized_document_strategy,
            num_workers=num_workers,
            **kwargs,
        )

    # this can take a surprisingly long time on longer docs so we cache it. For oversized docs, we end up counting twice, the 2nd time without the cache.
    # but if you're repeateddly running way oversize docs, the time that takes won't be what matters anyways.
    @staticmethod
    @lru_cache(maxsize=1000)
    def_count_tokens(text: str) -> int:
"""
        This can take a surprisingly long time on longer docs so we cache it, and we need to call it on every doc, regardless of size.
        """
        encoder = Settings.tokenizer
        tokens = encoder(text)
        return len(tokens)

    async def_agenerate_node_context(
        self,
        node: Union[Node, TextNode],
        metadata: Dict,
        document: Union[Node, TextNode],
        prompt: str,
        key: str,
    ) -> Dict:
"""
        Generate context for a node using LLM with retry logic.

        Implements exponential backoff for rate limit handling and uses prompt
        caching when available. The function retries on rate limits.

        Args:
            node: Node to generate context for
            metadata: Metadata dictionary to update
            document: Parent document containing the node
            prompt: Prompt template for context generation
            key: Metadata key for storing generated context

        Returns:
            Updated metadata dictionary with generated context

        Note:
            Uses exponential backoff starting at 60 seconds with up to 5 retries
            for rate limit handling.

        """
        cached_text = f"<document>{document.get_content()}</document>"
        messages = [
            ChatMessage(
                role="user",
                content=[
                    TextBlock(
                        text=cached_text,
                        type="text",
                    )
                ],
                additional_kwargs={"cache_control": {"type": "ephemeral"}},
            ),
            ChatMessage(
                role="user",
                content=[
                    TextBlock(
                        text=f"Here is the chunk we want to situate within the whole document:\n<chunk>{node.get_content()}</chunk>\n{prompt}",
                        type="text",
                    )
                ],
            ),
        ]

        max_retries = 5
        base_delay = 60

        for attempt in range(max_retries):
            try:
                # Extra headers typically dont cause issues
                headers = {"anthropic-beta": "prompt-caching-2024-07-31"}

                response: ChatResponse = await self.llm.achat(
                    messages, max_tokens=self.max_output_tokens, extra_headers=headers
                )

                first_block: Union[TextBlock, ImageBlock, AudioBlock, DocumentBlock] = (
                    cast(
                        Union[TextBlock, ImageBlock, AudioBlock, DocumentBlock],
                        response.message.blocks[0],
                    )
                )
                if isinstance(first_block, TextBlock):
                    metadata[key] = first_block.text
                else:
                    logging.warning(
                        f"Received non-text block type: {type(first_block)}"
                    )
                return metadata

            except Exception as e:
                is_rate_limit = any(
                    message in str(e).lower()
                    for message in ["rate limit", "too many requests", "429"]
                )

                if is_rate_limit and attempt  max_retries - 1:
                    delay = (base_delay * (2**attempt)) + (random.random() * 0.5)
                    logging.warning(
                        f"Rate limit hit, retrying in {delay:.1f} seconds "
                        f"(attempt {attempt+1}/{max_retries})"
                    )
                    await asyncio.sleep(delay)
                    continue

                if is_rate_limit:
                    logging.error(
                        f"Failed after {max_retries} retries due to rate limiting"
                    )
                else:
                    logging.warning(
                        f"Error generating context for node {node.node_id}: {e}",
                        exc_info=True,
                    )
                return metadata

        return metadata

    async def_get_document(self, doc_id: str) -> Optional[Union[Node, TextNode]]:
"""Counting tokens can be slow, as can awaiting the docstore (potentially), so we keep a small lru_cache."""
        # first we need to get the document
        try:
            doc = await self.docstore.aget_document(doc_id)
        except ValueError as e:
            if "not found" in str(e):
                logging.warning(f"Document {doc_id} not found in docstore")
                return None
        if not doc:
            logging.warning(f"Document {doc_id} not found in docstore")
            return None
        if not is_text_node(doc):
            logging.warning(f"Document {doc_id} is not an instance of (TextNode, Node)")
            return None

        # then truncate if necessary.
        if self.max_context_length is not None:
            strategy = self.oversized_document_strategy
            token_count = self._count_tokens(doc.get_content())
            if token_count  self.max_context_length:
                message = (
                    f"Document {doc.node_id} is too large ({token_count} tokens) "
                    f"to be processed. Doc metadata: {doc.metadata}"
                )

                if strategy == "warn":
                    logging.warning(message)
                elif strategy == "error":
                    raise ValueError(message)
                elif strategy == "ignore":
                    pass
                else:
                    raise ValueError(f"Unknown oversized document strategy: {strategy}")

        return doc

    async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
        Extract context for multiple nodes asynchronously, optimized for loosely ordered nodes.
        Processes each node independently without guaranteeing sequential document handling.
        Nodes will be *mostly* processed in document-order assuming nodes get passed in document-order.

        Args:
            nodes: List of nodes to process, ideally grouped by source document

        Returns:
            List of metadata dictionaries with generated context

        """
        metadata_list: List[Dict] = []
        for _ in nodes:
            metadata_list.append({})
        metadata_map = {
            node.node_id: metadata_dict
            for metadata_dict, node in zip(metadata_list, nodes)
        }

        # sorting takes a tiny amount of time - 0.4s for 1_000_000 nodes. but 1_000_000 nodes takes potentially hours to process
        # considering sorting CAN save the users hundreds of dollars in API costs, we just sort and leave no option to do otherwise.
        # The math always works out in the user's favor and we can't guarantee things are sorted in the first place.
        sorted_nodes = sorted(
            nodes, key=lambda n: n.source_node.node_id if n.source_node else ""
        )

        # iterate over all the nodes and generate the jobs
        node_tasks: List[Coroutine[Any, Any, Any]] = []
        for node in sorted_nodes:
            if not (node.source_node and is_text_node(node)):
                continue

            # Skip already processed nodes
            if self.key in node.metadata:
                continue

            doc: Optional[Union[Node, TextNode]] = await self._get_document(
                node.source_node.node_id
            )
            if not doc:
                continue

            metadata = metadata_map[node.node_id]
            # this modifies metadata in-place, adding a new key to the dictionary - we needed do anytyhing with the return value
            task = self._agenerate_node_context(
                node, metadata, doc, self.prompt, self.key
            )
            node_tasks.append(task)

        # then run the jobs - this does return the metadata list, but we already have it
        await run_jobs(
            node_tasks,
            show_progress=self.show_progress,
            workers=self.num_workers,
        )

        return metadata_list

```
 |  
| --- | --- |  
###  aextract [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/pydantic/#llama_index.core.extractors.DocumentContextExtractor.aextract "Permanent link")

```
aextract(nodes: Sequence[]) -> []

```

Extract context for multiple nodes asynchronously, optimized for loosely ordered nodes. Processes each node independently without guaranteeing sequential document handling. Nodes will be _mostly_ processed in document-order assuming nodes get passed in document-order.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]`  |  List of nodes to process, ideally grouped by source document  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[Dict]`  |  List of metadata dictionaries with generated context  |  
Source code in `llama-index-core/llama_index/core/extractors/document_context.py`  
| 
```
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
```
 | 
```
async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
    Extract context for multiple nodes asynchronously, optimized for loosely ordered nodes.
    Processes each node independently without guaranteeing sequential document handling.
    Nodes will be *mostly* processed in document-order assuming nodes get passed in document-order.

    Args:
        nodes: List of nodes to process, ideally grouped by source document

    Returns:
        List of metadata dictionaries with generated context

    """
    metadata_list: List[Dict] = []
    for _ in nodes:
        metadata_list.append({})
    metadata_map = {
        node.node_id: metadata_dict
        for metadata_dict, node in zip(metadata_list, nodes)
    }

    # sorting takes a tiny amount of time - 0.4s for 1_000_000 nodes. but 1_000_000 nodes takes potentially hours to process
    # considering sorting CAN save the users hundreds of dollars in API costs, we just sort and leave no option to do otherwise.
    # The math always works out in the user's favor and we can't guarantee things are sorted in the first place.
    sorted_nodes = sorted(
        nodes, key=lambda n: n.source_node.node_id if n.source_node else ""
    )

    # iterate over all the nodes and generate the jobs
    node_tasks: List[Coroutine[Any, Any, Any]] = []
    for node in sorted_nodes:
        if not (node.source_node and is_text_node(node)):
            continue

        # Skip already processed nodes
        if self.key in node.metadata:
            continue

        doc: Optional[Union[Node, TextNode]] = await self._get_document(
            node.source_node.node_id
        )
        if not doc:
            continue

        metadata = metadata_map[node.node_id]
        # this modifies metadata in-place, adding a new key to the dictionary - we needed do anytyhing with the return value
        task = self._agenerate_node_context(
            node, metadata, doc, self.prompt, self.key
        )
        node_tasks.append(task)

    # then run the jobs - this does return the metadata list, but we already have it
    await run_jobs(
        node_tasks,
        show_progress=self.show_progress,
        workers=self.num_workers,
    )

    return metadata_list

```
 |  
| --- | --- |  
options: members: - PydanticProgramExtractor
