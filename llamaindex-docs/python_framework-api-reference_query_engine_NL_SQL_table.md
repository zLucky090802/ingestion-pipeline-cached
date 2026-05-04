# NL SQL table
##  BaseQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.BaseQueryEngine "Permanent link")
Bases: `PromptMixin`, `DispatcherSpanMixin`
Base query engine.
Source code in `llama-index-core/llama_index/core/base/base_query_engine.py`  
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
```
 | 
```
classBaseQueryEngine(PromptMixin, DispatcherSpanMixin):
"""Base query engine."""

    def__init__(
        self,
        callback_manager: Optional[CallbackManager],
    ) -> None:
        self.callback_manager = callback_manager or CallbackManager([])

    def_get_prompts(self) -> Dict[str, Any]:
"""Get prompts."""
        return {}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""

    @dispatcher.span
    defquery(self, str_or_query_bundle: QueryType) -> RESPONSE_TYPE:
        dispatcher.event(QueryStartEvent(query=str_or_query_bundle))
        with self.callback_manager.as_trace("query"):
            if isinstance(str_or_query_bundle, str):
                str_or_query_bundle = QueryBundle(str_or_query_bundle)
            query_result = self._query(str_or_query_bundle)
        dispatcher.event(
            QueryEndEvent(query=str_or_query_bundle, response=query_result)
        )
        return query_result

    @dispatcher.span
    async defaquery(self, str_or_query_bundle: QueryType) -> RESPONSE_TYPE:
        dispatcher.event(QueryStartEvent(query=str_or_query_bundle))
        with self.callback_manager.as_trace("query"):
            if isinstance(str_or_query_bundle, str):
                str_or_query_bundle = QueryBundle(str_or_query_bundle)
            query_result = await self._aquery(str_or_query_bundle)
        dispatcher.event(
            QueryEndEvent(query=str_or_query_bundle, response=query_result)
        )
        return query_result

    defretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        raise NotImplementedError(
            "This query engine does not support retrieve, use query directly"
        )

    defsynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        raise NotImplementedError(
            "This query engine does not support synthesize, use query directly"
        )

    async defasynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        raise NotImplementedError(
            "This query engine does not support asynthesize, use aquery directly"
        )

    @abstractmethod
    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        pass

    @abstractmethod
    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        pass

```
 |  
| --- | --- |  
##  NLSQLTableQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.NLSQLTableQueryEngine "Permanent link")
Bases: `BaseSQLTableQueryEngine`
Natural language SQL Table query engine.
Read NLStructStoreQueryEngine's docstring for more info on NL SQL.
NOTE: Any Text-to-SQL application should be aware that executing arbitrary SQL queries can be a security risk. It is recommended to take precautions as needed, such as using restricted roles, read-only databases, sandboxing, etc.
Source code in `llama-index-core/llama_index/core/indices/struct_store/sql_query.py`  
| 
```
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
536
```
 | 
```
classNLSQLTableQueryEngine(BaseSQLTableQueryEngine):
"""
    Natural language SQL Table query engine.

    Read NLStructStoreQueryEngine's docstring for more info on NL SQL.

    NOTE: Any Text-to-SQL application should be aware that executing
    arbitrary SQL queries can be a security risk. It is recommended to
    take precautions as needed, such as using restricted roles, read-only
    databases, sandboxing, etc.
    """

    def__init__(
        self,
        sql_database: SQLDatabase,
        llm: Optional[LLM] = None,
        text_to_sql_prompt: Optional[BasePromptTemplate] = None,
        context_query_kwargs: Optional[dict] = None,
        synthesize_response: bool = True,
        markdown_response: bool = False,
        response_synthesis_prompt: Optional[BasePromptTemplate] = None,
        refine_synthesis_prompt: Optional[BasePromptTemplate] = None,
        tables: Optional[Union[List[str], List[Table]]] = None,
        table_retriever: Optional[ObjectRetriever[SQLTableSchema]] = None,
        rows_retrievers: Optional[dict[str, BaseRetriever]] = None,
        cols_retrievers: Optional[dict[str, dict[str, BaseRetriever]]] = None,
        context_str_prefix: Optional[str] = None,
        embed_model: Optional[BaseEmbedding] = None,
        sql_only: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        # self._tables = tables
        self._sql_retriever = NLSQLRetriever(
            sql_database,
            llm=llm,
            text_to_sql_prompt=text_to_sql_prompt,
            context_query_kwargs=context_query_kwargs,
            tables=tables,
            table_retriever=table_retriever,
            rows_retrievers=rows_retrievers,
            cols_retrievers=cols_retrievers,
            context_str_prefix=context_str_prefix,
            embed_model=embed_model,
            sql_only=sql_only,
            callback_manager=callback_manager,
            verbose=verbose,
        )
        super().__init__(
            synthesize_response=synthesize_response,
            markdown_response=markdown_response,
            response_synthesis_prompt=response_synthesis_prompt,
            refine_synthesis_prompt=refine_synthesis_prompt,
            llm=llm,
            callback_manager=callback_manager,
            verbose=verbose,
            **kwargs,
        )

    @property
    defsql_retriever(self) -> NLSQLRetriever:
"""Get SQL retriever."""
        return self._sql_retriever

```
 |  
| --- | --- |  
###  sql_retriever `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.NLSQLTableQueryEngine.sql_retriever "Permanent link")

```
sql_retriever: 

```

Get SQL retriever.
##  PGVectorSQLQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.PGVectorSQLQueryEngine "Permanent link")
Bases: `BaseSQLTableQueryEngine`
PGvector SQL query engine.
A modified version of the normal text-to-SQL query engine because we can infer embedding vectors in the sql query.
NOTE: this is a beta feature
NOTE: Any Text-to-SQL application should be aware that executing arbitrary SQL queries can be a security risk. It is recommended to take precautions as needed, such as using restricted roles, read-only databases, sandboxing, etc.
Source code in `llama-index-core/llama_index/core/indices/struct_store/sql_query.py`  
| 
```
539
540
541
542
543
544
545
546
547
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
580
581
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
```
 | 
```
classPGVectorSQLQueryEngine(BaseSQLTableQueryEngine):
"""
    PGvector SQL query engine.

    A modified version of the normal text-to-SQL query engine because
    we can infer embedding vectors in the sql query.

    NOTE: this is a beta feature

    NOTE: Any Text-to-SQL application should be aware that executing
    arbitrary SQL queries can be a security risk. It is recommended to
    take precautions as needed, such as using restricted roles, read-only
    databases, sandboxing, etc.

    """

    def__init__(
        self,
        sql_database: SQLDatabase,
        llm: Optional[LLM] = None,
        text_to_sql_prompt: Optional[BasePromptTemplate] = None,
        context_query_kwargs: Optional[dict] = None,
        synthesize_response: bool = True,
        response_synthesis_prompt: Optional[BasePromptTemplate] = None,
        refine_synthesis_prompt: Optional[BasePromptTemplate] = None,
        tables: Optional[Union[List[str], List[Table]]] = None,
        context_str_prefix: Optional[str] = None,
        sql_only: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        text_to_sql_prompt = text_to_sql_prompt or DEFAULT_TEXT_TO_SQL_PGVECTOR_PROMPT
        self._sql_retriever = NLSQLRetriever(
            sql_database,
            llm=llm,
            text_to_sql_prompt=text_to_sql_prompt,
            context_query_kwargs=context_query_kwargs,
            tables=tables,
            sql_parser_mode=SQLParserMode.PGVECTOR,
            context_str_prefix=context_str_prefix,
            sql_only=sql_only,
            callback_manager=callback_manager,
        )
        super().__init__(
            synthesize_response=synthesize_response,
            response_synthesis_prompt=response_synthesis_prompt,
            refine_synthesis_prompt=refine_synthesis_prompt,
            llm=llm,
            callback_manager=callback_manager,
            **kwargs,
        )

    @property
    defsql_retriever(self) -> NLSQLRetriever:
"""Get SQL retriever."""
        return self._sql_retriever

```
 |  
| --- | --- |  
###  sql_retriever `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.PGVectorSQLQueryEngine.sql_retriever "Permanent link")

```
sql_retriever: 

```

Get SQL retriever.
##  SQLTableRetrieverQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.SQLTableRetrieverQueryEngine "Permanent link")
Bases: `BaseSQLTableQueryEngine`
SQL Table retriever query engine.
Source code in `llama-index-core/llama_index/core/indices/struct_store/sql_query.py`  
| 
```
598
599
600
601
602
603
604
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
626
627
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
classSQLTableRetrieverQueryEngine(BaseSQLTableQueryEngine):
"""SQL Table retriever query engine."""

    def__init__(
        self,
        sql_database: SQLDatabase,
        table_retriever: ObjectRetriever[SQLTableSchema],
        rows_retrievers: Optional[dict[str, BaseRetriever]] = None,
        cols_retrievers: Optional[dict[str, dict[str, BaseRetriever]]] = None,
        llm: Optional[LLM] = None,
        text_to_sql_prompt: Optional[BasePromptTemplate] = None,
        context_query_kwargs: Optional[dict] = None,
        synthesize_response: bool = True,
        response_synthesis_prompt: Optional[BasePromptTemplate] = None,
        refine_synthesis_prompt: Optional[BasePromptTemplate] = None,
        context_str_prefix: Optional[str] = None,
        sql_only: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._sql_retriever = NLSQLRetriever(
            sql_database,
            llm=llm,
            text_to_sql_prompt=text_to_sql_prompt,
            context_query_kwargs=context_query_kwargs,
            table_retriever=table_retriever,
            rows_retrievers=rows_retrievers,
            cols_retrievers=cols_retrievers,
            context_str_prefix=context_str_prefix,
            sql_only=sql_only,
            callback_manager=callback_manager,
            verbose=kwargs.get("verbose", False),
        )
        super().__init__(
            synthesize_response=synthesize_response,
            response_synthesis_prompt=response_synthesis_prompt,
            refine_synthesis_prompt=refine_synthesis_prompt,
            llm=llm,
            callback_manager=callback_manager,
            **kwargs,
        )

    @property
    defsql_retriever(self) -> NLSQLRetriever:
"""Get SQL retriever."""
        return self._sql_retriever

```
 |  
| --- | --- |  
###  sql_retriever `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.SQLTableRetrieverQueryEngine.sql_retriever "Permanent link")

```
sql_retriever: 

```

Get SQL retriever.
##  CitationQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.CitationQueryEngine "Permanent link")
Bases: 
Citation query engine.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `retriever`  |   |  A retriever object.  |  _required_  |  
|  `response_synthesizer`  |  `Optional[BaseSynthesizer[](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/accumulate/#llama_index.core.response_synthesizers.BaseSynthesizer "BaseSynthesizer \(llama_index.core.response_synthesizers.BaseSynthesizer\)")]`  |  A BaseSynthesizer object.  |  `None`  |  
|  `citation_chunk_size`  |  Size of citation chunks, default=512. Useful for controlling granularity of sources.  |  `DEFAULT_CITATION_CHUNK_SIZE`  |  
|  `citation_chunk_overlap`  |  Overlap of citation nodes, default=20.  |  `DEFAULT_CITATION_CHUNK_OVERLAP`  |  
|  `text_splitter`  |  `Optional[TextSplitter[](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/code/#llama_index.core.node_parser.TextSplitter "TextSplitter \(llama_index.core.node_parser.TextSplitter\)")]`  |  A text splitter for creating citation source nodes. Default is a SentenceSplitter.  |  `None`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  A callback manager.  |  `None`  |  
|  `metadata_mode`  |  `MetadataMode`  |  A MetadataMode object that controls how metadata is included in the citation prompt.  |  `NONE`  |  
Source code in `llama-index-core/llama_index/core/query_engine/citation_query_engine.py`  
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
```
 | 
```
classCitationQueryEngine(BaseQueryEngine):
"""
    Citation query engine.

    Args:
        retriever (BaseRetriever): A retriever object.
        response_synthesizer (Optional[BaseSynthesizer]):
            A BaseSynthesizer object.
        citation_chunk_size (int):
            Size of citation chunks, default=512. Useful for controlling
            granularity of sources.
        citation_chunk_overlap (int): Overlap of citation nodes, default=20.
        text_splitter (Optional[TextSplitter]):
            A text splitter for creating citation source nodes. Default is
            a SentenceSplitter.
        callback_manager (Optional[CallbackManager]): A callback manager.
        metadata_mode (MetadataMode): A MetadataMode object that controls how
            metadata is included in the citation prompt.

    """

    def__init__(
        self,
        retriever: BaseRetriever,
        llm: Optional[LLM] = None,
        response_synthesizer: Optional[BaseSynthesizer] = None,
        citation_chunk_size: int = DEFAULT_CITATION_CHUNK_SIZE,
        citation_chunk_overlap: int = DEFAULT_CITATION_CHUNK_OVERLAP,
        text_splitter: Optional[TextSplitter] = None,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        callback_manager: Optional[CallbackManager] = None,
        metadata_mode: MetadataMode = MetadataMode.NONE,
    ) -> None:
        self.text_splitter = text_splitter or SentenceSplitter(
            chunk_size=citation_chunk_size, chunk_overlap=citation_chunk_overlap
        )
        self._retriever = retriever

        callback_manager = callback_manager or Settings.callback_manager
        llm = llm or Settings.llm

        self._response_synthesizer = response_synthesizer or get_response_synthesizer(
            llm=llm,
            callback_manager=callback_manager,
            text_qa_template=CITATION_QA_TEMPLATE,
            refine_template=CITATION_REFINE_TEMPLATE,
            response_mode=ResponseMode.COMPACT,
            use_async=False,
            streaming=False,
        )

        self._node_postprocessors = node_postprocessors or []
        self._metadata_mode = metadata_mode

        for node_postprocessor in self._node_postprocessors:
            node_postprocessor.callback_manager = callback_manager

        super().__init__(callback_manager=callback_manager)

    @classmethod
    deffrom_args(
        cls,
        index: BaseGPTIndex,
        llm: Optional[LLM] = None,
        response_synthesizer: Optional[BaseSynthesizer] = None,
        citation_chunk_size: int = DEFAULT_CITATION_CHUNK_SIZE,
        citation_chunk_overlap: int = DEFAULT_CITATION_CHUNK_OVERLAP,
        text_splitter: Optional[TextSplitter] = None,
        citation_qa_template: BasePromptTemplate = CITATION_QA_TEMPLATE,
        citation_refine_template: BasePromptTemplate = CITATION_REFINE_TEMPLATE,
        retriever: Optional[BaseRetriever] = None,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        # response synthesizer args
        response_mode: ResponseMode = ResponseMode.COMPACT,
        use_async: bool = False,
        streaming: bool = False,
        # class-specific args
        metadata_mode: MetadataMode = MetadataMode.NONE,
        **kwargs: Any,
    ) -> "CitationQueryEngine":
"""
        Initialize a CitationQueryEngine object.".

        Args:
            index: (BastGPTIndex): index to use for querying
            llm: (Optional[LLM]): LLM object to use for response generation.
            citation_chunk_size (int):
                Size of citation chunks, default=512. Useful for controlling
                granularity of sources.
            citation_chunk_overlap (int): Overlap of citation nodes, default=20.
            text_splitter (Optional[TextSplitter]):
                A text splitter for creating citation source nodes. Default is
                a SentenceSplitter.
            citation_qa_template (BasePromptTemplate): Template for initial citation QA
            citation_refine_template (BasePromptTemplate):
                Template for citation refinement.
            retriever (BaseRetriever): A retriever object.
            node_postprocessors (Optional[List[BaseNodePostprocessor]]): A list of
                node postprocessors.
            verbose (bool): Whether to print out debug info.
            response_mode (ResponseMode): A ResponseMode object.
            use_async (bool): Whether to use async.
            streaming (bool): Whether to use streaming.
            optimizer (Optional[BaseTokenUsageOptimizer]): A BaseTokenUsageOptimizer
                object.

        """
        retriever = retriever or index.as_retriever(**kwargs)

        response_synthesizer = response_synthesizer or get_response_synthesizer(
            llm=llm,
            text_qa_template=citation_qa_template,
            refine_template=citation_refine_template,
            response_mode=response_mode,
            use_async=use_async,
            streaming=streaming,
        )

        return cls(
            retriever=retriever,
            llm=llm,
            response_synthesizer=response_synthesizer,
            callback_manager=Settings.callback_manager,
            citation_chunk_size=citation_chunk_size,
            citation_chunk_overlap=citation_chunk_overlap,
            text_splitter=text_splitter,
            node_postprocessors=node_postprocessors,
            metadata_mode=metadata_mode,
        )

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {"response_synthesizer": self._response_synthesizer}

    def_create_citation_nodes(self, nodes: List[NodeWithScore]) -> List[NodeWithScore]:
"""Modify retrieved nodes to be granular sources."""
        new_nodes: List[NodeWithScore] = []
        for node in nodes:
            text_chunks = self.text_splitter.split_text(
                node.node.get_content(metadata_mode=self._metadata_mode)
            )

            for text_chunk in text_chunks:
                text = f"Source {len(new_nodes)+1}:\n{text_chunk}\n"

                new_node = NodeWithScore(
                    node=TextNode.model_validate(node.node.model_dump()),
                    score=node.score,
                )
                new_node.node.set_content(text)
                new_nodes.append(new_node)
        return new_nodes

    defretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        nodes = self._retriever.retrieve(query_bundle)

        for postprocessor in self._node_postprocessors:
            nodes = postprocessor.postprocess_nodes(nodes, query_bundle=query_bundle)

        return nodes

    async defaretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        nodes = await self._retriever.aretrieve(query_bundle)

        for postprocessor in self._node_postprocessors:
            nodes = await postprocessor.apostprocess_nodes(
                nodes, query_bundle=query_bundle
            )

        return nodes

    @property
    defretriever(self) -> BaseRetriever:
"""Get the retriever object."""
        return self._retriever

    defsynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        nodes = self._create_citation_nodes(nodes)
        return self._response_synthesizer.synthesize(
            query=query_bundle,
            nodes=nodes,
            additional_source_nodes=additional_source_nodes,
        )

    async defasynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        nodes = self._create_citation_nodes(nodes)
        return await self._response_synthesizer.asynthesize(
            query=query_bundle,
            nodes=nodes,
            additional_source_nodes=additional_source_nodes,
        )

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            with self.callback_manager.event(
                CBEventType.RETRIEVE,
                payload={EventPayload.QUERY_STR: query_bundle.query_str},
            ) as retrieve_event:
                nodes = self.retrieve(query_bundle)
                nodes = self._create_citation_nodes(nodes)

                retrieve_event.on_end(payload={EventPayload.NODES: nodes})

            response = self._response_synthesizer.synthesize(
                query=query_bundle,
                nodes=nodes,
            )

            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            with self.callback_manager.event(
                CBEventType.RETRIEVE,
                payload={EventPayload.QUERY_STR: query_bundle.query_str},
            ) as retrieve_event:
                nodes = await self.aretrieve(query_bundle)
                nodes = self._create_citation_nodes(nodes)

                retrieve_event.on_end(payload={EventPayload.NODES: nodes})

            response = await self._response_synthesizer.asynthesize(
                query=query_bundle,
                nodes=nodes,
            )

            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

```
 |  
| --- | --- |  
###  retriever `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.CitationQueryEngine.retriever "Permanent link")

```
retriever: 

```

Get the retriever object.
###  from_args `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.CitationQueryEngine.from_args "Permanent link")

```
from_args(
    index: BaseGPTIndex,
    llm: Optional[] = None,
    response_synthesizer: Optional[] = None,
    citation_chunk_size:  = DEFAULT_CITATION_CHUNK_SIZE,
    citation_chunk_overlap:  = DEFAULT_CITATION_CHUNK_OVERLAP,
    text_splitter: Optional[] = None,
    citation_qa_template:  = CITATION_QA_TEMPLATE,
    citation_refine_template:  = CITATION_REFINE_TEMPLATE,
    retriever: Optional[] = None,
    node_postprocessors: Optional[
        []
    ] = None,
    response_mode:  = ,
    use_async:  = False,
    streaming:  = False,
    metadata_mode: MetadataMode = ,
    **kwargs: 
) -> 

```

Initialize a CitationQueryEngine object.".
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index`  |  `BaseGPTIndex`  |  (BastGPTIndex): index to use for querying  |  _required_  |  
|  `llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.llm.LLM\)")]`  |  (Optional[LLM]): LLM object to use for response generation.  |  `None`  |  
|  `citation_chunk_size`  |  Size of citation chunks, default=512. Useful for controlling granularity of sources.  |  `DEFAULT_CITATION_CHUNK_SIZE`  |  
|  `citation_chunk_overlap`  |  Overlap of citation nodes, default=20.  |  `DEFAULT_CITATION_CHUNK_OVERLAP`  |  
|  `text_splitter`  |  `Optional[TextSplitter[](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/code/#llama_index.core.node_parser.TextSplitter "TextSplitter \(llama_index.core.node_parser.TextSplitter\)")]`  |  A text splitter for creating citation source nodes. Default is a SentenceSplitter.  |  `None`  |  
|  `citation_qa_template`  |   |  Template for initial citation QA  |  `CITATION_QA_TEMPLATE`  |  
|  `citation_refine_template`  |   |  Template for citation refinement.  |  `CITATION_REFINE_TEMPLATE`  |  
|  `retriever`  |   |  A retriever object.  |  `None`  |  
|  `node_postprocessors`  |  `Optional[List[BaseNodePostprocessor[](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/#llama_index.core.postprocessor.types.BaseNodePostprocessor "BaseNodePostprocessor \(llama_index.core.postprocessor.types.BaseNodePostprocessor\)")]]`  |  A list of node postprocessors.  |  `None`  |  
|  `verbose`  |  `bool`  |  Whether to print out debug info.  |  _required_  |  
|  `response_mode`  |   |  A ResponseMode object.  |   |  
|  `use_async`  |  `bool`  |  Whether to use async.  |  `False`  |  
|  `streaming`  |  `bool`  |  Whether to use streaming.  |  `False`  |  
|  `optimizer`  |  `Optional[BaseTokenUsageOptimizer]`  |  A BaseTokenUsageOptimizer object.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/query_engine/citation_query_engine.py`  
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
```
 | 
```
@classmethod
deffrom_args(
    cls,
    index: BaseGPTIndex,
    llm: Optional[LLM] = None,
    response_synthesizer: Optional[BaseSynthesizer] = None,
    citation_chunk_size: int = DEFAULT_CITATION_CHUNK_SIZE,
    citation_chunk_overlap: int = DEFAULT_CITATION_CHUNK_OVERLAP,
    text_splitter: Optional[TextSplitter] = None,
    citation_qa_template: BasePromptTemplate = CITATION_QA_TEMPLATE,
    citation_refine_template: BasePromptTemplate = CITATION_REFINE_TEMPLATE,
    retriever: Optional[BaseRetriever] = None,
    node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
    # response synthesizer args
    response_mode: ResponseMode = ResponseMode.COMPACT,
    use_async: bool = False,
    streaming: bool = False,
    # class-specific args
    metadata_mode: MetadataMode = MetadataMode.NONE,
    **kwargs: Any,
) -> "CitationQueryEngine":
"""
    Initialize a CitationQueryEngine object.".

    Args:
        index: (BastGPTIndex): index to use for querying
        llm: (Optional[LLM]): LLM object to use for response generation.
        citation_chunk_size (int):
            Size of citation chunks, default=512. Useful for controlling
            granularity of sources.
        citation_chunk_overlap (int): Overlap of citation nodes, default=20.
        text_splitter (Optional[TextSplitter]):
            A text splitter for creating citation source nodes. Default is
            a SentenceSplitter.
        citation_qa_template (BasePromptTemplate): Template for initial citation QA
        citation_refine_template (BasePromptTemplate):
            Template for citation refinement.
        retriever (BaseRetriever): A retriever object.
        node_postprocessors (Optional[List[BaseNodePostprocessor]]): A list of
            node postprocessors.
        verbose (bool): Whether to print out debug info.
        response_mode (ResponseMode): A ResponseMode object.
        use_async (bool): Whether to use async.
        streaming (bool): Whether to use streaming.
        optimizer (Optional[BaseTokenUsageOptimizer]): A BaseTokenUsageOptimizer
            object.

    """
    retriever = retriever or index.as_retriever(**kwargs)

    response_synthesizer = response_synthesizer or get_response_synthesizer(
        llm=llm,
        text_qa_template=citation_qa_template,
        refine_template=citation_refine_template,
        response_mode=response_mode,
        use_async=use_async,
        streaming=streaming,
    )

    return cls(
        retriever=retriever,
        llm=llm,
        response_synthesizer=response_synthesizer,
        callback_manager=Settings.callback_manager,
        citation_chunk_size=citation_chunk_size,
        citation_chunk_overlap=citation_chunk_overlap,
        text_splitter=text_splitter,
        node_postprocessors=node_postprocessors,
        metadata_mode=metadata_mode,
    )

```
 |  
| --- | --- |  
##  CogniswitchQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.CogniswitchQueryEngine "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/query_engine/cogniswitch_query_engine.py`  
| 
```
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
```
 | 
```
classCogniswitchQueryEngine(BaseQueryEngine):
    def__init__(self, cs_token: str, OAI_token: str, apiKey: str) -> None:
"""
        The required fields.

        Args:
            cs_token (str): Cogniswitch token.
            OAI_token (str): OpenAI token.
            apiKey (str): Oauth token.

        """
        self.cs_token = cs_token
        self.OAI_token = OAI_token
        self.apiKey = apiKey
        self.knowledge_request_endpoint = (
            "https://api.cogniswitch.ai:8243/cs-api/0.0.1/cs/knowledgeRequest"
        )
        self.headers = {
            "apiKey": self.apiKey,
            "platformToken": self.cs_token,
            "openAIToken": self.OAI_token,
        }

    defquery_knowledge(self, query: str) -> Response:
"""
        Send a query to the Cogniswitch service and retrieve the response.

        Args:
            query (str): Query to be answered.

        Returns:
            dict: Response JSON from the Cogniswitch service.

        """
        data = {"query": query}
        response = requests.post(
            self.knowledge_request_endpoint,
            headers=self.headers,
            data=data,
        )
        if response.status_code == 200:
            resp = response.json()
            answer = resp["data"]["answer"]

            return Response(response=answer)
        else:
            error_message = response.json()["message"]
            return Response(response=error_message)

    def_query(self, query_bundle: QueryBundle) -> Response:
        return self.query_knowledge(query_bundle.query_str)

    async def_aquery(self, query_bundle: QueryBundle) -> Response:
        return self.query_knowledge(query_bundle.query_str)

    def_get_prompt_modules(self) -> Dict[str, Any]:
"""Get prompts."""
        return {}

```
 |  
| --- | --- |  
###  query_knowledge [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.CogniswitchQueryEngine.query_knowledge "Permanent link")

```
query_knowledge(query: ) -> 

```

Send a query to the Cogniswitch service and retrieve the response.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query to be answered.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `dict`  |   |  Response JSON from the Cogniswitch service.  |  
Source code in `llama-index-core/llama_index/core/query_engine/cogniswitch_query_engine.py`  
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
```
 | 
```
defquery_knowledge(self, query: str) -> Response:
"""
    Send a query to the Cogniswitch service and retrieve the response.

    Args:
        query (str): Query to be answered.

    Returns:
        dict: Response JSON from the Cogniswitch service.

    """
    data = {"query": query}
    response = requests.post(
        self.knowledge_request_endpoint,
        headers=self.headers,
        data=data,
    )
    if response.status_code == 200:
        resp = response.json()
        answer = resp["data"]["answer"]

        return Response(response=answer)
    else:
        error_message = response.json()["message"]
        return Response(response=error_message)

```
 |  
| --- | --- |  
##  CustomQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.CustomQueryEngine "Permanent link")
Bases: `BaseModel`, 
Custom query engine.
Subclasses can define additional attributes as Pydantic fields. Subclasses must implement the `custom_query` method, which takes a query string and returns either a Response object or a string as output.
They can optionally implement the `acustom_query` method for async support.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `callback_manager`  |   |  `<llama_index.core.callbacks.base.CallbackManager object at 0x7f00aef0ad50>`  |  
Source code in `llama-index-core/llama_index/core/query_engine/custom.py`  
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
```
 | 
```
classCustomQueryEngine(BaseModel, BaseQueryEngine):
"""
    Custom query engine.

    Subclasses can define additional attributes as Pydantic fields.
    Subclasses must implement the `custom_query` method, which takes a query string
    and returns either a Response object or a string as output.

    They can optionally implement the `acustom_query` method for async support.

    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    callback_manager: CallbackManager = Field(
        default_factory=lambda: CallbackManager([]), exclude=True
    )

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {}

    defquery(self, str_or_query_bundle: QueryType) -> RESPONSE_TYPE:
        with self.callback_manager.as_trace("query"):
            # if query bundle, just run the query
            if isinstance(str_or_query_bundle, QueryBundle):
                query_str = str_or_query_bundle.query_str
            else:
                query_str = str_or_query_bundle
            raw_response = self.custom_query(query_str)
            return (
                Response(raw_response)
                if isinstance(raw_response, str)
                else raw_response
            )

    async defaquery(self, str_or_query_bundle: QueryType) -> RESPONSE_TYPE:
        with self.callback_manager.as_trace("query"):
            if isinstance(str_or_query_bundle, QueryBundle):
                query_str = str_or_query_bundle.query_str
            else:
                query_str = str_or_query_bundle
            raw_response = await self.acustom_query(query_str)
            return (
                Response(raw_response)
                if isinstance(raw_response, str)
                else raw_response
            )

    @abstractmethod
    defcustom_query(self, query_str: str) -> STR_OR_RESPONSE_TYPE:
"""Run a custom query."""

    async defacustom_query(self, query_str: str) -> STR_OR_RESPONSE_TYPE:
"""Run a custom query asynchronously."""
        # by default, just run the synchronous version
        return self.custom_query(query_str)

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        raise NotImplementedError("This query engine does not support _query.")

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        raise NotImplementedError("This query engine does not support _aquery.")

```
 |  
| --- | --- |  
###  custom_query `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.CustomQueryEngine.custom_query "Permanent link")

```
custom_query(query_str: ) -> STR_OR_RESPONSE_TYPE

```

Run a custom query.
Source code in `llama-index-core/llama_index/core/query_engine/custom.py`  
| 
```
64
65
66
```
 | 
```
@abstractmethod
defcustom_query(self, query_str: str) -> STR_OR_RESPONSE_TYPE:
"""Run a custom query."""

```
 |  
| --- | --- |  
###  acustom_query [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.CustomQueryEngine.acustom_query "Permanent link")

```
acustom_query(query_str: ) -> STR_OR_RESPONSE_TYPE

```

Run a custom query asynchronously.
Source code in `llama-index-core/llama_index/core/query_engine/custom.py`  
| 
```
68
69
70
71
```
 | 
```
async defacustom_query(self, query_str: str) -> STR_OR_RESPONSE_TYPE:
"""Run a custom query asynchronously."""
    # by default, just run the synchronous version
    return self.custom_query(query_str)

```
 |  
| --- | --- |  
##  FLAREInstructQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.FLAREInstructQueryEngine "Permanent link")
Bases: 
FLARE Instruct query engine.
This is the version of FLARE that uses retrieval-encouraging instructions.
NOTE: this is a beta feature. Interfaces might change, and it might not always give correct answers.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_engine`  |   |  query engine to use  |  _required_  |  
|  `llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.llm.LLM\)")]`  |  LLM model. Defaults to None.  |  `None`  |  
|  `instruct_prompt`  |  `Optional[PromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.PromptTemplate "PromptTemplate \(llama_index.core.prompts.base.PromptTemplate\)")]`  |  instruct prompt. Defaults to None.  |  `None`  |  
|  `lookahead_answer_inserter`  |  `Optional[BaseLookaheadAnswerInserter]`  |  lookahead answer inserter. Defaults to None.  |  `None`  |  
|  `done_output_parser`  |  `Optional[IsDoneOutputParser]`  |  done output parser. Defaults to None.  |  `None`  |  
|  `query_task_output_parser`  |  `Optional[QueryTaskOutputParser]`  |  query task output parser. Defaults to None.  |  `None`  |  
|  `max_iterations`  |  max iterations. Defaults to 10.  |  
|  `max_lookahead_query_tasks`  |  max lookahead query tasks. Defaults to 1.  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  callback manager. Defaults to None.  |  `None`  |  
|  `verbose`  |  `bool`  |  give verbose outputs. Defaults to False.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/query_engine/flare/base.py`  
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
```
 | 
```
classFLAREInstructQueryEngine(BaseQueryEngine):
"""
    FLARE Instruct query engine.

    This is the version of FLARE that uses retrieval-encouraging instructions.

    NOTE: this is a beta feature. Interfaces might change, and it might not
    always give correct answers.

    Args:
        query_engine (BaseQueryEngine): query engine to use
        llm (Optional[LLM]): LLM model. Defaults to None.
        instruct_prompt (Optional[PromptTemplate]): instruct prompt. Defaults to None.
        lookahead_answer_inserter (Optional[BaseLookaheadAnswerInserter]):
            lookahead answer inserter. Defaults to None.
        done_output_parser (Optional[IsDoneOutputParser]): done output parser.
            Defaults to None.
        query_task_output_parser (Optional[QueryTaskOutputParser]):
            query task output parser. Defaults to None.
        max_iterations (int): max iterations. Defaults to 10.
        max_lookahead_query_tasks (int): max lookahead query tasks. Defaults to 1.
        callback_manager (Optional[CallbackManager]): callback manager.
            Defaults to None.
        verbose (bool): give verbose outputs. Defaults to False.

    """

    def__init__(
        self,
        query_engine: BaseQueryEngine,
        llm: Optional[LLM] = None,
        instruct_prompt: Optional[BasePromptTemplate] = None,
        lookahead_answer_inserter: Optional[BaseLookaheadAnswerInserter] = None,
        done_output_parser: Optional[IsDoneOutputParser] = None,
        query_task_output_parser: Optional[QueryTaskOutputParser] = None,
        max_iterations: int = 10,
        max_lookahead_query_tasks: int = 1,
        callback_manager: Optional[CallbackManager] = None,
        verbose: bool = False,
    ) -> None:
"""Init params."""
        super().__init__(callback_manager=callback_manager)
        self._query_engine = query_engine
        self._llm = llm or Settings.llm
        self._instruct_prompt = instruct_prompt or DEFAULT_INSTRUCT_PROMPT
        self._lookahead_answer_inserter = lookahead_answer_inserter or (
            LLMLookaheadAnswerInserter(llm=self._llm)
        )
        self._done_output_parser = done_output_parser or IsDoneOutputParser()
        self._query_task_output_parser = (
            query_task_output_parser or QueryTaskOutputParser()
        )
        self._max_iterations = max_iterations
        self._max_lookahead_query_tasks = max_lookahead_query_tasks
        self._verbose = verbose

    def_get_prompts(self) -> Dict[str, Any]:
"""Get prompts."""
        return {
            "instruct_prompt": self._instruct_prompt,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "instruct_prompt" in prompts:
            self._instruct_prompt = prompts["instruct_prompt"]

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {
            "query_engine": self._query_engine,
            "lookahead_answer_inserter": self._lookahead_answer_inserter,
        }

    def_get_relevant_lookahead_response(self, updated_lookahead_resp: str) -> str:
"""Get relevant lookahead response."""
        # if there's remaining query tasks, then truncate the response
        # until the start position of the first tag
        # there may be remaining query tasks because the _max_lookahead_query_tasks
        # is less than the total number of generated [Search(query)] tags
        remaining_query_tasks = self._query_task_output_parser.parse(
            updated_lookahead_resp
        )
        if len(remaining_query_tasks) == 0:
            relevant_lookahead_resp = updated_lookahead_resp
        else:
            first_task = remaining_query_tasks[0]
            relevant_lookahead_resp = updated_lookahead_resp[: first_task.start_idx]
        return relevant_lookahead_resp

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Query and get response."""
        print_text(f"Query: {query_bundle.query_str}\n", color="green")
        cur_response = ""
        source_nodes = []
        for iter in range(self._max_iterations):
            if self._verbose:
                print_text(f"Current response: {cur_response}\n", color="blue")
            # generate "lookahead response" that contains "[Search(query)]" tags
            # e.g.
            # The colors on the flag of Ghana have the following meanings. Red is
            # for [Search(Ghana flag meaning)],...
            lookahead_resp = self._llm.predict(
                self._instruct_prompt,
                query_str=query_bundle.query_str,
                existing_answer=cur_response,
            )
            lookahead_resp = lookahead_resp.strip()
            if self._verbose:
                print_text(f"Lookahead response: {lookahead_resp}\n", color="pink")

            is_done, fmt_lookahead = self._done_output_parser.parse(lookahead_resp)
            if is_done:
                cur_response = cur_response.strip() + " " + fmt_lookahead.strip()
                break

            # parse lookahead response into query tasks
            query_tasks = self._query_task_output_parser.parse(lookahead_resp)

            # get answers for each query task
            query_tasks = query_tasks[: self._max_lookahead_query_tasks]
            query_answers = []
            for _, query_task in enumerate(query_tasks):
                answer_obj = self._query_engine.query(query_task.query_str)
                if not isinstance(answer_obj, Response):
                    raise ValueError(
                        f"Expected Response object, got {type(answer_obj)} instead."
                    )
                query_answer = str(answer_obj)
                query_answers.append(query_answer)
                source_nodes.extend(answer_obj.source_nodes)

            # fill in the lookahead response template with the query answers
            # from the query engine
            updated_lookahead_resp = self._lookahead_answer_inserter.insert(
                lookahead_resp, query_tasks, query_answers, prev_response=cur_response
            )

            # get "relevant" lookahead response by truncating the updated
            # lookahead response until the start position of the first tag
            # also remove the prefix from the lookahead response, so that
            # we can concatenate it with the existing response
            relevant_lookahead_resp_wo_prefix = self._get_relevant_lookahead_response(
                updated_lookahead_resp
            )

            if self._verbose:
                print_text(
                    "Updated lookahead response: "
                    + f"{relevant_lookahead_resp_wo_prefix}\n",
                    color="pink",
                )

            # append the relevant lookahead response to the final response
            cur_response = (
                cur_response.strip() + " " + relevant_lookahead_resp_wo_prefix.strip()
            )

        # NOTE: at the moment, does not support streaming
        return Response(response=cur_response, source_nodes=source_nodes)

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        return self._query(query_bundle)

    defretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        # if the query engine is a retriever, then use the retrieve method
        if isinstance(self._query_engine, RetrieverQueryEngine):
            return self._query_engine.retrieve(query_bundle)
        else:
            raise NotImplementedError(
                "This query engine does not support retrieve, use query directly"
            )

    async defaretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        # if the query engine is a retriever, then use the retrieve method
        if isinstance(self._query_engine, RetrieverQueryEngine):
            return await self._query_engine.aretrieve(query_bundle)
        else:
            raise NotImplementedError(
                "This query engine does not support retrieve, use query directly"
            )

```
 |  
| --- | --- |  
##  ComposableGraphQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.ComposableGraphQueryEngine "Permanent link")
Bases: 
Composable graph query engine.
This query engine can operate over a ComposableGraph. It can take in custom query engines for its sub-indices.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `graph`  |   |  A ComposableGraph object.  |  _required_  |  
|  `custom_query_engines`  |  `Optional[Dict[str, BaseQueryEngine[](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/#llama_index.core.base.base_query_engine.BaseQueryEngine "BaseQueryEngine \(llama_index.core.base.base_query_engine.BaseQueryEngine\)")]]`  |  A dictionary of custom query engines.  |  `None`  |  
|  `recursive`  |  `bool`  |  Whether to recursively query the graph.  |  `True`  |  
|  `**kwargs`  |  additional arguments to be passed to the underlying index query engine.  |  
Source code in `llama-index-core/llama_index/core/query_engine/graph_query_engine.py`  
| 
```
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
```
 | 
```
classComposableGraphQueryEngine(BaseQueryEngine):
"""
    Composable graph query engine.

    This query engine can operate over a ComposableGraph.
    It can take in custom query engines for its sub-indices.

    Args:
        graph (ComposableGraph): A ComposableGraph object.
        custom_query_engines (Optional[Dict[str, BaseQueryEngine]]): A dictionary of
            custom query engines.
        recursive (bool): Whether to recursively query the graph.
        **kwargs: additional arguments to be passed to the underlying index query
            engine.

    """

    def__init__(
        self,
        graph: ComposableGraph,
        custom_query_engines: Optional[Dict[str, BaseQueryEngine]] = None,
        recursive: bool = True,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        self._graph = graph
        self._custom_query_engines = custom_query_engines or {}
        self._kwargs = kwargs

        # additional configs
        self._recursive = recursive
        callback_manager = Settings.callback_manager
        super().__init__(callback_manager=callback_manager)

    def_get_prompt_modules(self) -> Dict[str, Any]:
"""Get prompt modules."""
        return {}

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        return self._query_index(query_bundle, index_id=None, level=0)

    @dispatcher.span
    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        return self._query_index(query_bundle, index_id=None, level=0)

    def_query_index(
        self,
        query_bundle: QueryBundle,
        index_id: Optional[str] = None,
        level: int = 0,
    ) -> RESPONSE_TYPE:
"""Query a single index."""
        index_id = index_id or self._graph.root_id

        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            # get query engine
            if index_id in self._custom_query_engines:
                query_engine = self._custom_query_engines[index_id]
            else:
                query_engine = self._graph.get_index(index_id).as_query_engine(
                    **self._kwargs
                )

            with self.callback_manager.event(
                CBEventType.RETRIEVE,
                payload={EventPayload.QUERY_STR: query_bundle.query_str},
            ) as retrieve_event:
                nodes = query_engine.retrieve(query_bundle)
                retrieve_event.on_end(payload={EventPayload.NODES: nodes})

            if self._recursive:
                # do recursion here
                nodes_for_synthesis = []
                additional_source_nodes = []
                for node_with_score in nodes:
                    node_with_score, source_nodes = self._fetch_recursive_nodes(
                        node_with_score, query_bundle, level
                    )
                    nodes_for_synthesis.append(node_with_score)
                    additional_source_nodes.extend(source_nodes)
                response = query_engine.synthesize(
                    query_bundle, nodes_for_synthesis, additional_source_nodes
                )
            else:
                response = query_engine.synthesize(query_bundle, nodes)

            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

    def_fetch_recursive_nodes(
        self,
        node_with_score: NodeWithScore,
        query_bundle: QueryBundle,
        level: int,
    ) -> Tuple[NodeWithScore, List[NodeWithScore]]:
"""
        Fetch nodes.

        Uses existing node if it's not an index node.
        Otherwise fetch response from corresponding index.

        """
        if isinstance(node_with_score.node, IndexNode):
            index_node = node_with_score.node
            # recursive call
            response = self._query_index(query_bundle, index_node.index_id, level + 1)

            new_node = TextNode(text=str(response))
            new_node_with_score = NodeWithScore(
                node=new_node, score=node_with_score.score
            )
            return new_node_with_score, response.source_nodes
        else:
            return node_with_score, []

```
 |  
| --- | --- |  
##  JSONalyzeQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.JSONalyzeQueryEngine "Permanent link")
JSONalyze query engine.
DEPRECATED: Use `JSONalyzeQueryEngine` from `llama-index-experimental` instead.
Source code in `llama-index-core/llama_index/core/query_engine/jsonalyze/jsonalyze_query_engine.py`  
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
```
 | 
```
classJSONalyzeQueryEngine:
"""
    JSONalyze query engine.

    DEPRECATED: Use `JSONalyzeQueryEngine` from `llama-index-experimental` instead.
    """

    def__init__(self, *args: Any, **kwargs: Any) -> None:
        raise DeprecationWarning(
            "JSONalyzeQueryEngine has been moved to `llama-index-experimental`.\n"
            "`pip install llama-index-experimental`\n"
            "`from llama_index.experimental.query_engine import JSONalyzeQueryEngine`\n"
            "Note that the JSONalyzeQueryEngine allows for arbitrary file creation, \n"
            "and should be used in a secure environment."
        )

```
 |  
| --- | --- |  
##  KnowledgeGraphQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.KnowledgeGraphQueryEngine "Permanent link")
Bases: 
Knowledge graph query engine.
Query engine to call a knowledge graph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `storage_context`  |  `Optional[StorageContext[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.storage.storage_context.StorageContext "StorageContext


  
      dataclass
   \(llama_index.core.storage.storage_context.StorageContext\)")]`  |  A storage context to use.  |  `None`  |  
|  `refresh_schema`  |  `bool`  |  Whether to refresh the schema.  |  `False`  |  
|  `verbose`  |  `bool`  |  Whether to print intermediate results.  |  `False`  |  
|  `response_synthesizer`  |  `Optional[BaseSynthesizer[](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/accumulate/#llama_index.core.response_synthesizers.BaseSynthesizer "BaseSynthesizer \(llama_index.core.response_synthesizers.BaseSynthesizer\)")]`  |  A BaseSynthesizer object.  |  `None`  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Source code in `llama-index-core/llama_index/core/query_engine/knowledge_graph_query_engine.py`  
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
```
 | 
```
@deprecated.deprecated(
    version="0.10.53",
    reason=(
        "KnowledgeGraphQueryEngine is deprecated. It is recommended to use "
        "the PropertyGraphIndex and associated retrievers instead."
    ),
)
classKnowledgeGraphQueryEngine(BaseQueryEngine):
"""
    Knowledge graph query engine.

    Query engine to call a knowledge graph.

    Args:
        storage_context (Optional[StorageContext]): A storage context to use.
        refresh_schema (bool): Whether to refresh the schema.
        verbose (bool): Whether to print intermediate results.
        response_synthesizer (Optional[BaseSynthesizer]):
            A BaseSynthesizer object.
        **kwargs: Additional keyword arguments.

    """

    def__init__(
        self,
        llm: Optional[LLM] = None,
        storage_context: Optional[StorageContext] = None,
        graph_query_synthesis_prompt: Optional[BasePromptTemplate] = None,
        graph_response_answer_prompt: Optional[BasePromptTemplate] = None,
        refresh_schema: bool = False,
        verbose: bool = False,
        response_synthesizer: Optional[BaseSynthesizer] = None,
        **kwargs: Any,
    ):
        # Ensure that we have a graph store
        assert storage_context is not None, "Must provide a storage context."
        assert storage_context.graph_store is not None, (
            "Must provide a graph store in the storage context."
        )
        self._storage_context = storage_context
        self.graph_store = storage_context.graph_store

        self._llm = llm or Settings.llm

        # Get Graph schema
        self._graph_schema = self.graph_store.get_schema(refresh=refresh_schema)

        # Get graph store query synthesis prompt
        self._graph_query_synthesis_prompt = graph_query_synthesis_prompt

        self._graph_response_answer_prompt = (
            graph_response_answer_prompt or DEFAULT_KG_RESPONSE_ANSWER_PROMPT
        )
        self._verbose = verbose
        callback_manager = Settings.callback_manager
        self._response_synthesizer = response_synthesizer or get_response_synthesizer(
            llm=self._llm, callback_manager=callback_manager
        )

        super().__init__(callback_manager=callback_manager)

    def_get_prompts(self) -> Dict[str, Any]:
"""Get prompts."""
        return {
            "graph_query_synthesis_prompt": self._graph_query_synthesis_prompt,
            "graph_response_answer_prompt": self._graph_response_answer_prompt,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "graph_query_synthesis_prompt" in prompts:
            self._graph_query_synthesis_prompt = prompts["graph_query_synthesis_prompt"]
        if "graph_response_answer_prompt" in prompts:
            self._graph_response_answer_prompt = prompts["graph_response_answer_prompt"]

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {"response_synthesizer": self._response_synthesizer}

    defgenerate_query(self, query_str: str) -> str:
"""Generate a Graph Store Query from a query bundle."""
        # Get the query engine query string

        graph_store_query: str = self._llm.predict(
            self._graph_query_synthesis_prompt,
            query_str=query_str,
            schema=self._graph_schema,
        )

        return graph_store_query

    async defagenerate_query(self, query_str: str) -> str:
"""Generate a Graph Store Query from a query bundle."""
        # Get the query engine query string

        graph_store_query: str = await self._llm.apredict(
            self._graph_query_synthesis_prompt,
            query_str=query_str,
            schema=self._graph_schema,
        )

        return graph_store_query

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Get nodes for response."""
        graph_store_query = self.generate_query(query_bundle.query_str)
        if self._verbose:
            print_text(f"Graph Store Query:\n{graph_store_query}\n", color="yellow")
        logger.debug(f"Graph Store Query:\n{graph_store_query}")

        with self.callback_manager.event(
            CBEventType.RETRIEVE,
            payload={EventPayload.QUERY_STR: graph_store_query},
        ) as retrieve_event:
            # Get the graph store response
            graph_store_response = self.graph_store.query(query=graph_store_query)
            if self._verbose:
                print_text(
                    f"Graph Store Response:\n{graph_store_response}\n",
                    color="yellow",
                )
            logger.debug(f"Graph Store Response:\n{graph_store_response}")

            retrieve_event.on_end(payload={EventPayload.RESPONSE: graph_store_response})

        retrieved_graph_context: Sequence = self._graph_response_answer_prompt.format(
            query_str=query_bundle.query_str,
            kg_query_str=graph_store_query,
            kg_response_str=graph_store_response,
        )

        node = NodeWithScore(
            node=TextNode(
                text=retrieved_graph_context,
                metadata={
                    "query_str": query_bundle.query_str,
                    "graph_store_query": graph_store_query,
                    "graph_store_response": graph_store_response,
                    "graph_schema": self._graph_schema,
                },
            ),
            score=1.0,
        )
        return [node]

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Query the graph store."""
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            nodes: List[NodeWithScore] = self._retrieve(query_bundle)

            response = self._response_synthesizer.synthesize(
                query=query_bundle,
                nodes=nodes,
            )

            if self._verbose:
                print_text(f"Final Response: {response}\n", color="green")

            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        graph_store_query = await self.agenerate_query(query_bundle.query_str)
        if self._verbose:
            print_text(f"Graph Store Query:\n{graph_store_query}\n", color="yellow")
        logger.debug(f"Graph Store Query:\n{graph_store_query}")

        with self.callback_manager.event(
            CBEventType.RETRIEVE,
            payload={EventPayload.QUERY_STR: graph_store_query},
        ) as retrieve_event:
            # Get the graph store response
            # TBD: This is a blocking call. We need to make it async.
            graph_store_response = self.graph_store.query(query=graph_store_query)
            if self._verbose:
                print_text(
                    f"Graph Store Response:\n{graph_store_response}\n",
                    color="yellow",
                )
            logger.debug(f"Graph Store Response:\n{graph_store_response}")

            retrieve_event.on_end(payload={EventPayload.RESPONSE: graph_store_response})

        retrieved_graph_context: Sequence = self._graph_response_answer_prompt.format(
            query_str=query_bundle.query_str,
            kg_query_str=graph_store_query,
            kg_response_str=graph_store_response,
        )

        node = NodeWithScore(
            node=TextNode(
                text=retrieved_graph_context,
                metadata={
                    "query_str": query_bundle.query_str,
                    "graph_store_query": graph_store_query,
                    "graph_store_response": graph_store_response,
                    "graph_schema": self._graph_schema,
                },
            ),
            score=1.0,
        )
        return [node]

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Query the graph store."""
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            nodes = await self._aretrieve(query_bundle)
            response = await self._response_synthesizer.asynthesize(
                query=query_bundle,
                nodes=nodes,
            )

            if self._verbose:
                print_text(f"Final Response: {response}\n", color="green")

            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

```
 |  
| --- | --- |  
###  generate_query [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.KnowledgeGraphQueryEngine.generate_query "Permanent link")

```
generate_query(query_str: ) -> 

```

Generate a Graph Store Query from a query bundle.
Source code in `llama-index-core/llama_index/core/query_engine/knowledge_graph_query_engine.py`  
| 
```
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
defgenerate_query(self, query_str: str) -> str:
"""Generate a Graph Store Query from a query bundle."""
    # Get the query engine query string

    graph_store_query: str = self._llm.predict(
        self._graph_query_synthesis_prompt,
        query_str=query_str,
        schema=self._graph_schema,
    )

    return graph_store_query

```
 |  
| --- | --- |  
###  agenerate_query [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.KnowledgeGraphQueryEngine.agenerate_query "Permanent link")

```
agenerate_query(query_str: ) -> 

```

Generate a Graph Store Query from a query bundle.
Source code in `llama-index-core/llama_index/core/query_engine/knowledge_graph_query_engine.py`  
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
```
 | 
```
async defagenerate_query(self, query_str: str) -> str:
"""Generate a Graph Store Query from a query bundle."""
    # Get the query engine query string

    graph_store_query: str = await self._llm.apredict(
        self._graph_query_synthesis_prompt,
        query_str=query_str,
        schema=self._graph_schema,
    )

    return graph_store_query

```
 |  
| --- | --- |  
##  SimpleMultiModalQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.SimpleMultiModalQueryEngine "Permanent link")
Bases: 
Simple Multi Modal Retriever query engine.
Assumes that retrieved text context fits within context window of LLM, along with images.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `retriever`  |  `MultiModalVectorIndexRetriever`  |  A retriever object.  |  _required_  |  
|  `multi_modal_llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.LLM\)")]`  |  An LLM model.  |  `None`  |  
|  `text_qa_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  Text QA Prompt Template.  |  `None`  |  
|  `image_qa_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  Image QA Prompt Template.  |  `None`  |  
|  `node_postprocessors`  |  `Optional[List[BaseNodePostprocessor[](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/#llama_index.core.postprocessor.types.BaseNodePostprocessor "BaseNodePostprocessor \(llama_index.core.postprocessor.types.BaseNodePostprocessor\)")]]`  |  Node Postprocessors.  |  `None`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  A callback manager.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/query_engine/multi_modal.py`  
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
```
 | 
```
classSimpleMultiModalQueryEngine(BaseQueryEngine):
"""
    Simple Multi Modal Retriever query engine.

    Assumes that retrieved text context fits within context window of LLM, along with images.

    Args:
        retriever (MultiModalVectorIndexRetriever): A retriever object.
        multi_modal_llm (Optional[LLM]): An LLM model.
        text_qa_template (Optional[BasePromptTemplate]): Text QA Prompt Template.
        image_qa_template (Optional[BasePromptTemplate]): Image QA Prompt Template.
        node_postprocessors (Optional[List[BaseNodePostprocessor]]): Node Postprocessors.
        callback_manager (Optional[CallbackManager]): A callback manager.

    """

    def__init__(
        self,
        retriever: "MultiModalVectorIndexRetriever",
        multi_modal_llm: Optional[LLM] = None,
        text_qa_template: Optional[BasePromptTemplate] = None,
        image_qa_template: Optional[BasePromptTemplate] = None,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
        self._retriever = retriever
        if multi_modal_llm:
            self._multi_modal_llm = multi_modal_llm
        else:
            try:
                fromllama_index.llms.openaiimport (
                    OpenAIResponses,
                )  # pants: no-infer-dep

                self._multi_modal_llm = OpenAIResponses(
                    model="gpt-4.1", max_output_tokens=1000
                )
            except ImportError as e:
                raise ImportError(
                    "`llama-index-llms-openai` package cannot be found. "
                    "Please install it by using `pip install `llama-index-llms-openai`"
                )
        self._text_qa_template = text_qa_template or DEFAULT_TEXT_QA_PROMPT
        self._image_qa_template = image_qa_template or DEFAULT_TEXT_QA_PROMPT

        self._node_postprocessors = node_postprocessors or []
        callback_manager = callback_manager or CallbackManager([])
        for node_postprocessor in self._node_postprocessors:
            node_postprocessor.callback_manager = callback_manager

        super().__init__(callback_manager)

    def_get_prompts(self) -> Dict[str, Any]:
"""Get prompts."""
        return {"text_qa_template": self._text_qa_template}

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {}

    def_apply_node_postprocessors(
        self, nodes: List[NodeWithScore], query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        for node_postprocessor in self._node_postprocessors:
            nodes = node_postprocessor.postprocess_nodes(
                nodes, query_bundle=query_bundle
            )
        return nodes

    async def_async_apply_node_postprocessors(
        self, nodes: List[NodeWithScore], query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        for node_postprocessor in self._node_postprocessors:
            nodes = await node_postprocessor.apostprocess_nodes(
                nodes, query_bundle=query_bundle
            )
        return nodes

    defretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        nodes = self._retriever.retrieve(query_bundle)
        return self._apply_node_postprocessors(nodes, query_bundle=query_bundle)

    async defaretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        nodes = await self._retriever.aretrieve(query_bundle)
        return await self._async_apply_node_postprocessors(
            nodes, query_bundle=query_bundle
        )

    defsynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        image_nodes, text_nodes = _get_image_and_text_nodes(nodes)
        context_str = "\n\n".join(
            [r.get_content(metadata_mode=MetadataMode.LLM) for r in text_nodes]
        )
        fmt_prompt = self._text_qa_template.format(
            context_str=context_str, query_str=query_bundle.query_str
        )

        blocks: List[Union[ImageBlock, TextBlock]] = [
            image_node_to_image_block(image_node.node)
            for image_node in image_nodes
            if isinstance(image_node.node, ImageNode)
        ]

        blocks.append(TextBlock(text=fmt_prompt))

        llm_response = self._multi_modal_llm.chat(
            [ChatMessage(role="user", blocks=blocks)]
        )
        return Response(
            response=llm_response.message.content,
            source_nodes=nodes,
            metadata={"text_nodes": text_nodes, "image_nodes": image_nodes},
        )

    def_get_response_with_images(
        self,
        prompt_str: str,
        image_nodes: List[NodeWithScore],
    ) -> RESPONSE_TYPE:
        assert all(isinstance(node.node, ImageNode) for node in image_nodes)

        fmt_prompt = self._image_qa_template.format(
            query_str=prompt_str,
        )

        blocks: List[Union[ImageBlock, TextBlock]] = [
            image_node_to_image_block(image_node.node)
            for image_node in image_nodes
            if isinstance(image_node.node, ImageNode)
        ]

        blocks.append(TextBlock(text=fmt_prompt))

        llm_response = self._multi_modal_llm.chat(
            [ChatMessage(role="user", blocks=blocks)]
        )
        return Response(
            response=llm_response.message.content,
            source_nodes=image_nodes,
            metadata={"image_nodes": image_nodes},
        )

    async defasynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        image_nodes, text_nodes = _get_image_and_text_nodes(nodes)
        context_str = "\n\n".join(
            [r.get_content(metadata_mode=MetadataMode.LLM) for r in text_nodes]
        )
        fmt_prompt = self._text_qa_template.format(
            context_str=context_str, query_str=query_bundle.query_str
        )

        blocks: List[Union[ImageBlock, TextBlock]] = [
            image_node_to_image_block(image_node.node)
            for image_node in image_nodes
            if isinstance(image_node.node, ImageNode)
        ]

        blocks.append(TextBlock(text=fmt_prompt))

        llm_response = await self._multi_modal_llm.achat(
            [ChatMessage(role="user", blocks=blocks)]
        )
        return Response(
            response=llm_response.message.content,
            source_nodes=nodes,
            metadata={"text_nodes": text_nodes, "image_nodes": image_nodes},
        )

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            with self.callback_manager.event(
                CBEventType.RETRIEVE,
                payload={EventPayload.QUERY_STR: query_bundle.query_str},
            ) as retrieve_event:
                nodes = self.retrieve(query_bundle)

                retrieve_event.on_end(
                    payload={EventPayload.NODES: nodes},
                )

            response = self.synthesize(
                query_bundle,
                nodes=nodes,
            )

            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

    defimage_query(self, image_path: QueryType, prompt_str: str) -> RESPONSE_TYPE:
"""Answer a image query."""
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: str(image_path)}
        ) as query_event:
            with self.callback_manager.event(
                CBEventType.RETRIEVE,
                payload={EventPayload.QUERY_STR: str(image_path)},
            ) as retrieve_event:
                nodes = self._retriever.image_to_image_retrieve(image_path)

                retrieve_event.on_end(
                    payload={EventPayload.NODES: nodes},
                )

            image_nodes, _ = _get_image_and_text_nodes(nodes)
            response = self._get_response_with_images(
                prompt_str=prompt_str,
                image_nodes=image_nodes,
            )

            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            with self.callback_manager.event(
                CBEventType.RETRIEVE,
                payload={EventPayload.QUERY_STR: query_bundle.query_str},
            ) as retrieve_event:
                nodes = await self.aretrieve(query_bundle)

                retrieve_event.on_end(
                    payload={EventPayload.NODES: nodes},
                )

            response = await self.asynthesize(
                query_bundle,
                nodes=nodes,
            )

            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

    @property
    defretriever(self) -> "MultiModalVectorIndexRetriever":
"""Get the retriever object."""
        return self._retriever

```
 |  
| --- | --- |  
###  retriever `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.SimpleMultiModalQueryEngine.retriever "Permanent link")

```
retriever: MultiModalVectorIndexRetriever

```

Get the retriever object.
###  image_query [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.SimpleMultiModalQueryEngine.image_query "Permanent link")

```
image_query(
    image_path: QueryType, prompt_str: 
) -> RESPONSE_TYPE

```

Answer a image query.
Source code in `llama-index-core/llama_index/core/query_engine/multi_modal.py`  
| 
```
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
defimage_query(self, image_path: QueryType, prompt_str: str) -> RESPONSE_TYPE:
"""Answer a image query."""
    with self.callback_manager.event(
        CBEventType.QUERY, payload={EventPayload.QUERY_STR: str(image_path)}
    ) as query_event:
        with self.callback_manager.event(
            CBEventType.RETRIEVE,
            payload={EventPayload.QUERY_STR: str(image_path)},
        ) as retrieve_event:
            nodes = self._retriever.image_to_image_retrieve(image_path)

            retrieve_event.on_end(
                payload={EventPayload.NODES: nodes},
            )

        image_nodes, _ = _get_image_and_text_nodes(nodes)
        response = self._get_response_with_images(
            prompt_str=prompt_str,
            image_nodes=image_nodes,
        )

        query_event.on_end(payload={EventPayload.RESPONSE: response})

    return response

```
 |  
| --- | --- |  
##  MultiStepQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.MultiStepQueryEngine "Permanent link")
Bases: 
Multi-step query engine.
This query engine can operate over an existing base query engine, along with the multi-step query transform.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_engine`  |   |  A BaseQueryEngine object.  |  _required_  |  
|  `query_transform`  |  `StepDecomposeQueryTransform`  |  A StepDecomposeQueryTransform object.  |  _required_  |  
|  `response_synthesizer`  |  `Optional[BaseSynthesizer[](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/accumulate/#llama_index.core.response_synthesizers.BaseSynthesizer "BaseSynthesizer \(llama_index.core.response_synthesizers.BaseSynthesizer\)")]`  |  A BaseSynthesizer object.  |  `None`  |  
|  `num_steps`  |  `Optional[int]`  |  Number of steps to run the multi-step query.  |  
|  `early_stopping`  |  `bool`  |  Whether to stop early if the stop function returns True.  |  `True`  |  
|  `index_summary`  |  A string summary of the index.  |  `'None'`  |  
|  `stop_fn`  |  `Optional[Callable[[Dict], bool]]`  |  A stop function that takes in a dictionary of information and returns a boolean.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/query_engine/multistep_query_engine.py`  
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
```
 | 
```
classMultiStepQueryEngine(BaseQueryEngine):
"""
    Multi-step query engine.

    This query engine can operate over an existing base query engine,
    along with the multi-step query transform.

    Args:
        query_engine (BaseQueryEngine): A BaseQueryEngine object.
        query_transform (StepDecomposeQueryTransform): A StepDecomposeQueryTransform
            object.
        response_synthesizer (Optional[BaseSynthesizer]): A BaseSynthesizer
            object.
        num_steps (Optional[int]): Number of steps to run the multi-step query.
        early_stopping (bool): Whether to stop early if the stop function returns True.
        index_summary (str): A string summary of the index.
        stop_fn (Optional[Callable[[Dict], bool]]): A stop function that takes in a
            dictionary of information and returns a boolean.

    """

    def__init__(
        self,
        query_engine: BaseQueryEngine,
        query_transform: StepDecomposeQueryTransform,
        response_synthesizer: Optional[BaseSynthesizer] = None,
        num_steps: Optional[int] = 3,
        early_stopping: bool = True,
        index_summary: str = "None",
        stop_fn: Optional[Callable[[Dict], bool]] = None,
    ) -> None:
        self._query_engine = query_engine
        self._query_transform = query_transform
        self._response_synthesizer = response_synthesizer or get_response_synthesizer(
            callback_manager=self._query_engine.callback_manager
        )

        self._index_summary = index_summary
        self._num_steps = num_steps
        self._early_stopping = early_stopping
        # TODO: make interface to stop function better
        self._stop_fn = stop_fn or default_stop_fn
        # num_steps must be provided if early_stopping is False
        if not self._early_stopping and self._num_steps is None:
            raise ValueError("Must specify num_steps if early_stopping is False.")

        callback_manager = self._query_engine.callback_manager
        super().__init__(callback_manager)

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {
            "response_synthesizer": self._response_synthesizer,
            "query_transform": self._query_transform,
        }

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            nodes, source_nodes, metadata = self._query_multistep(query_bundle)

            final_response = self._response_synthesizer.synthesize(
                query=query_bundle,
                nodes=nodes,
                additional_source_nodes=source_nodes,
            )
            final_response.metadata = metadata

            query_event.on_end(payload={EventPayload.RESPONSE: final_response})

        return final_response

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            nodes, source_nodes, metadata = self._query_multistep(query_bundle)

            final_response = await self._response_synthesizer.asynthesize(
                query=query_bundle,
                nodes=nodes,
                additional_source_nodes=source_nodes,
            )
            final_response.metadata = metadata

            query_event.on_end(payload={EventPayload.RESPONSE: final_response})

        return final_response

    def_combine_queries(
        self, query_bundle: QueryBundle, prev_reasoning: str
    ) -> QueryBundle:
"""Combine queries."""
        transform_metadata = {
            "prev_reasoning": prev_reasoning,
            "index_summary": self._index_summary,
        }
        return self._query_transform(query_bundle, metadata=transform_metadata)

    def_query_multistep(
        self, query_bundle: QueryBundle
    ) -> Tuple[List[NodeWithScore], List[NodeWithScore], Dict[str, Any]]:
"""Run query combiner."""
        prev_reasoning = ""
        cur_response = None
        should_stop = False
        cur_steps = 0

        # use response
        final_response_metadata: Dict[str, Any] = {"sub_qa": []}

        text_chunks = []
        source_nodes = []
        while not should_stop:
            if self._num_steps is not None and cur_steps >= self._num_steps:
                should_stop = True
                break
            elif should_stop:
                break

            updated_query_bundle = self._combine_queries(query_bundle, prev_reasoning)

            # TODO: make stop logic better
            stop_dict = {"query_bundle": updated_query_bundle}
            if self._stop_fn(stop_dict):
                should_stop = True
                break

            cur_response = self._query_engine.query(updated_query_bundle)

            # append to response builder
            cur_qa_text = (
                f"\nQuestion: {updated_query_bundle.query_str}\n"
                f"Answer: {cur_response!s}"
            )
            text_chunks.append(cur_qa_text)
            for source_node in cur_response.source_nodes:
                source_nodes.append(source_node)
            # update metadata
            final_response_metadata["sub_qa"].append(
                (updated_query_bundle.query_str, cur_response)
            )

            prev_reasoning += (
                f"- {updated_query_bundle.query_str}\n- {cur_response!s}\n"
            )
            cur_steps += 1

        nodes = [
            NodeWithScore(node=TextNode(text=text_chunk)) for text_chunk in text_chunks
        ]
        return nodes, source_nodes, final_response_metadata

```
 |  
| --- | --- |  
##  PandasQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.PandasQueryEngine "Permanent link")
Pandas query engine.
DEPRECATED: Use `PandasQueryEngine` from `llama-index-experimental` instead.
Source code in `llama-index-core/llama_index/core/query_engine/pandas/pandas_query_engine.py`  
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
```
 | 
```
classPandasQueryEngine:
"""
    Pandas query engine.

    DEPRECATED: Use `PandasQueryEngine` from `llama-index-experimental` instead.
    """

    def__init__(self, *args: Any, **kwargs: Any) -> None:
        raise DeprecationWarning(
            "PandasQueryEngine has been moved to `llama-index-experimental`.\n"
            "`pip install llama-index-experimental`\n"
            "`from llama_index.experimental.query_engine import PandasQueryEngine`\n"
            "Note that the PandasQueryEngine allows for arbitrary code execution, \n"
            "and should be used in a secure environment."
        )

```
 |  
| --- | --- |  
##  RetrieverQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.RetrieverQueryEngine "Permanent link")
Bases: 
Retriever query engine.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `retriever`  |   |  A retriever object.  |  _required_  |  
|  `response_synthesizer`  |  `Optional[BaseSynthesizer[](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/accumulate/#llama_index.core.response_synthesizers.BaseSynthesizer "BaseSynthesizer \(llama_index.core.response_synthesizers.BaseSynthesizer\)")]`  |  A BaseSynthesizer object.  |  `None`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  A callback manager.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/query_engine/retriever_query_engine.py`  
| 
```
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
```
 | 
```
classRetrieverQueryEngine(BaseQueryEngine):
"""
    Retriever query engine.

    Args:
        retriever (BaseRetriever): A retriever object.
        response_synthesizer (Optional[BaseSynthesizer]): A BaseSynthesizer
            object.
        callback_manager (Optional[CallbackManager]): A callback manager.

    """

    def__init__(
        self,
        retriever: BaseRetriever,
        response_synthesizer: Optional[BaseSynthesizer] = None,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        self._retriever = retriever
        self._response_synthesizer = response_synthesizer or get_response_synthesizer(
            llm=Settings.llm,
            callback_manager=callback_manager or Settings.callback_manager,
        )

        self._node_postprocessors = node_postprocessors or []
        callback_manager = (
            callback_manager or self._response_synthesizer.callback_manager
        )
        for node_postprocessor in self._node_postprocessors:
            node_postprocessor.callback_manager = callback_manager
        super().__init__(callback_manager=callback_manager)

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {"response_synthesizer": self._response_synthesizer}

    @classmethod
    deffrom_args(
        cls,
        retriever: BaseRetriever,
        llm: Optional[LLM] = None,
        response_synthesizer: Optional[BaseSynthesizer] = None,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        callback_manager: Optional[CallbackManager] = None,
        # response synthesizer args
        response_mode: ResponseMode = ResponseMode.COMPACT,
        text_qa_template: Optional[BasePromptTemplate] = None,
        refine_template: Optional[BasePromptTemplate] = None,
        summary_template: Optional[BasePromptTemplate] = None,
        simple_template: Optional[BasePromptTemplate] = None,
        output_cls: Optional[Type[BaseModel]] = None,
        use_async: bool = False,
        streaming: bool = False,
        verbose: bool = False,
        **kwargs: Any,
    ) -> "RetrieverQueryEngine":
"""
        Initialize a RetrieverQueryEngine object.".

        Args:
            retriever (BaseRetriever): A retriever object.
            llm (Optional[LLM]): An instance of an LLM.
            response_synthesizer (Optional[BaseSynthesizer]): An instance of a response
                synthesizer.
            node_postprocessors (Optional[List[BaseNodePostprocessor]]): A list of
                node postprocessors.
            callback_manager (Optional[CallbackManager]): A callback manager.
            response_mode (ResponseMode): A ResponseMode object.
            text_qa_template (Optional[BasePromptTemplate]): A BasePromptTemplate
                object.
            refine_template (Optional[BasePromptTemplate]): A BasePromptTemplate object.
            summary_template (Optional[BasePromptTemplate]): A BasePromptTemplate object.
            simple_template (Optional[BasePromptTemplate]): A BasePromptTemplate object.
            output_cls (Optional[Type[BaseModel]]): The pydantic model to pass to the
                response synthesizer.
            use_async (bool): Whether to use async.
            streaming (bool): Whether to use streaming.
            verbose (bool): Whether to print verbose output.

        """
        llm = llm or Settings.llm

        response_synthesizer = response_synthesizer or get_response_synthesizer(
            llm=llm,
            text_qa_template=text_qa_template,
            refine_template=refine_template,
            summary_template=summary_template,
            simple_template=simple_template,
            response_mode=response_mode,
            output_cls=output_cls,
            use_async=use_async,
            streaming=streaming,
            verbose=verbose,
        )

        callback_manager = callback_manager or Settings.callback_manager

        return cls(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            callback_manager=callback_manager,
            node_postprocessors=node_postprocessors,
        )

    def_apply_node_postprocessors(
        self, nodes: List[NodeWithScore], query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        for node_postprocessor in self._node_postprocessors:
            nodes = node_postprocessor.postprocess_nodes(
                nodes, query_bundle=query_bundle
            )
        return nodes

    async def_async_apply_node_postprocessors(
        self, nodes: List[NodeWithScore], query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        for node_postprocessor in self._node_postprocessors:
            nodes = await node_postprocessor.apostprocess_nodes(
                nodes, query_bundle=query_bundle
            )
        return nodes

    defretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        nodes = self._retriever.retrieve(query_bundle)
        return self._apply_node_postprocessors(nodes, query_bundle=query_bundle)

    async defaretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        nodes = await self._retriever.aretrieve(query_bundle)
        return await self._async_apply_node_postprocessors(
            nodes, query_bundle=query_bundle
        )

    defwith_retriever(self, retriever: BaseRetriever) -> "RetrieverQueryEngine":
        return RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=self._response_synthesizer,
            callback_manager=self.callback_manager,
            node_postprocessors=self._node_postprocessors,
        )

    defsynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        return self._response_synthesizer.synthesize(
            query=query_bundle,
            nodes=nodes,
            additional_source_nodes=additional_source_nodes,
        )

    async defasynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        return await self._response_synthesizer.asynthesize(
            query=query_bundle,
            nodes=nodes,
            additional_source_nodes=additional_source_nodes,
        )

    @dispatcher.span
    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            nodes = self.retrieve(query_bundle)
            response = self._response_synthesizer.synthesize(
                query=query_bundle,
                nodes=nodes,
            )
            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

    @dispatcher.span
    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            nodes = await self.aretrieve(query_bundle)

            response = await self._response_synthesizer.asynthesize(
                query=query_bundle,
                nodes=nodes,
            )

            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

    @property
    defretriever(self) -> BaseRetriever:
"""Get the retriever object."""
        return self._retriever

```
 |  
| --- | --- |  
###  retriever `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.RetrieverQueryEngine.retriever "Permanent link")

```
retriever: 

```

Get the retriever object.
###  from_args `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.RetrieverQueryEngine.from_args "Permanent link")

```
from_args(
    retriever: ,
    llm: Optional[] = None,
    response_synthesizer: Optional[] = None,
    node_postprocessors: Optional[
        []
    ] = None,
    callback_manager: Optional[] = None,
    response_mode:  = ,
    text_qa_template: Optional[] = None,
    refine_template: Optional[] = None,
    summary_template: Optional[] = None,
    simple_template: Optional[] = None,
    output_cls: Optional[[BaseModel]] = None,
    use_async:  = False,
    streaming:  = False,
    verbose:  = False,
    **kwargs: 
) -> 

```

Initialize a RetrieverQueryEngine object.".
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `retriever`  |   |  A retriever object.  |  _required_  |  
|  `llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.llm.LLM\)")]`  |  An instance of an LLM.  |  `None`  |  
|  `response_synthesizer`  |  `Optional[BaseSynthesizer[](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/accumulate/#llama_index.core.response_synthesizers.BaseSynthesizer "BaseSynthesizer \(llama_index.core.response_synthesizers.BaseSynthesizer\)")]`  |  An instance of a response synthesizer.  |  `None`  |  
|  `node_postprocessors`  |  `Optional[List[BaseNodePostprocessor[](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/#llama_index.core.postprocessor.types.BaseNodePostprocessor "BaseNodePostprocessor \(llama_index.core.postprocessor.types.BaseNodePostprocessor\)")]]`  |  A list of node postprocessors.  |  `None`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  A callback manager.  |  `None`  |  
|  `response_mode`  |   |  A ResponseMode object.  |   |  
|  `text_qa_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A BasePromptTemplate object.  |  `None`  |  
|  `refine_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A BasePromptTemplate object.  |  `None`  |  
|  `summary_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A BasePromptTemplate object.  |  `None`  |  
|  `simple_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A BasePromptTemplate object.  |  `None`  |  
|  `output_cls`  |  `Optional[Type[BaseModel]]`  |  The pydantic model to pass to the response synthesizer.  |  `None`  |  
|  `use_async`  |  `bool`  |  Whether to use async.  |  `False`  |  
|  `streaming`  |  `bool`  |  Whether to use streaming.  |  `False`  |  
|  `verbose`  |  `bool`  |  Whether to print verbose output.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/query_engine/retriever_query_engine.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_args(
    cls,
    retriever: BaseRetriever,
    llm: Optional[LLM] = None,
    response_synthesizer: Optional[BaseSynthesizer] = None,
    node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
    callback_manager: Optional[CallbackManager] = None,
    # response synthesizer args
    response_mode: ResponseMode = ResponseMode.COMPACT,
    text_qa_template: Optional[BasePromptTemplate] = None,
    refine_template: Optional[BasePromptTemplate] = None,
    summary_template: Optional[BasePromptTemplate] = None,
    simple_template: Optional[BasePromptTemplate] = None,
    output_cls: Optional[Type[BaseModel]] = None,
    use_async: bool = False,
    streaming: bool = False,
    verbose: bool = False,
    **kwargs: Any,
) -> "RetrieverQueryEngine":
"""
    Initialize a RetrieverQueryEngine object.".

    Args:
        retriever (BaseRetriever): A retriever object.
        llm (Optional[LLM]): An instance of an LLM.
        response_synthesizer (Optional[BaseSynthesizer]): An instance of a response
            synthesizer.
        node_postprocessors (Optional[List[BaseNodePostprocessor]]): A list of
            node postprocessors.
        callback_manager (Optional[CallbackManager]): A callback manager.
        response_mode (ResponseMode): A ResponseMode object.
        text_qa_template (Optional[BasePromptTemplate]): A BasePromptTemplate
            object.
        refine_template (Optional[BasePromptTemplate]): A BasePromptTemplate object.
        summary_template (Optional[BasePromptTemplate]): A BasePromptTemplate object.
        simple_template (Optional[BasePromptTemplate]): A BasePromptTemplate object.
        output_cls (Optional[Type[BaseModel]]): The pydantic model to pass to the
            response synthesizer.
        use_async (bool): Whether to use async.
        streaming (bool): Whether to use streaming.
        verbose (bool): Whether to print verbose output.

    """
    llm = llm or Settings.llm

    response_synthesizer = response_synthesizer or get_response_synthesizer(
        llm=llm,
        text_qa_template=text_qa_template,
        refine_template=refine_template,
        summary_template=summary_template,
        simple_template=simple_template,
        response_mode=response_mode,
        output_cls=output_cls,
        use_async=use_async,
        streaming=streaming,
        verbose=verbose,
    )

    callback_manager = callback_manager or Settings.callback_manager

    return cls(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        callback_manager=callback_manager,
        node_postprocessors=node_postprocessors,
    )

```
 |  
| --- | --- |  
##  RetryGuidelineQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.RetryGuidelineQueryEngine "Permanent link")
Bases: 
Does retry with evaluator feedback if query engine fails evaluation.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_engine`  |   |  A query engine object  |  _required_  |  
|  `guideline_evaluator`  |   |  A guideline evaluator object  |  _required_  |  
|  `resynthesize_query`  |  `bool`  |  Whether to resynthesize query  |  `False`  |  
|  `max_retries`  |  Maximum number of retries  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  A callback manager object  |  `None`  |  
Source code in `llama-index-core/llama_index/core/query_engine/retry_query_engine.py`  
| 
```
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
classRetryGuidelineQueryEngine(BaseQueryEngine):
"""
    Does retry with evaluator feedback
    if query engine fails evaluation.

    Args:
        query_engine (BaseQueryEngine): A query engine object
        guideline_evaluator (GuidelineEvaluator): A guideline evaluator object
        resynthesize_query (bool): Whether to resynthesize query
        max_retries (int): Maximum number of retries
        callback_manager (Optional[CallbackManager]): A callback manager object

    """

    def__init__(
        self,
        query_engine: BaseQueryEngine,
        guideline_evaluator: GuidelineEvaluator,
        resynthesize_query: bool = False,
        max_retries: int = 3,
        callback_manager: Optional[CallbackManager] = None,
        query_transformer: Optional[FeedbackQueryTransformation] = None,
    ) -> None:
        self._query_engine = query_engine
        self._guideline_evaluator = guideline_evaluator
        self.max_retries = max_retries
        self.resynthesize_query = resynthesize_query
        self.query_transformer = query_transformer or FeedbackQueryTransformation(
            resynthesize_query=self.resynthesize_query
        )
        super().__init__(callback_manager)

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {
            "query_engine": self._query_engine,
            "guideline_evalator": self._guideline_evaluator,
        }

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        response = self._query_engine._query(query_bundle)
        assert not isinstance(response, AsyncStreamingResponse)
        if self.max_retries <= 0:
            return response
        typed_response = (
            response if isinstance(response, Response) else response.get_response()
        )
        query_str = query_bundle.query_str
        eval = self._guideline_evaluator.evaluate_response(query_str, typed_response)
        if eval.passing:
            logger.debug("Evaluation returned True.")
            return response
        else:
            logger.debug("Evaluation returned False.")
            new_query_engine = RetryGuidelineQueryEngine(
                self._query_engine,
                self._guideline_evaluator,
                self.resynthesize_query,
                self.max_retries - 1,
                self.callback_manager,
            )
            new_query = self.query_transformer.run(query_bundle, {"evaluation": eval})
            logger.debug("New query: %s", new_query.query_str)
            return new_query_engine.query(new_query)

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Not supported."""
        return self._query(query_bundle)

```
 |  
| --- | --- |  
##  RetryQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.RetryQueryEngine "Permanent link")
Bases: 
Does retry on query engine if it fails evaluation.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_engine`  |   |  A query engine object  |  _required_  |  
|  `evaluator`  |   |  An evaluator object  |  _required_  |  
|  `max_retries`  |  Maximum number of retries  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  A callback manager object  |  `None`  |  
Source code in `llama-index-core/llama_index/core/query_engine/retry_query_engine.py`  
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
```
 | 
```
classRetryQueryEngine(BaseQueryEngine):
"""
    Does retry on query engine if it fails evaluation.

    Args:
        query_engine (BaseQueryEngine): A query engine object
        evaluator (BaseEvaluator): An evaluator object
        max_retries (int): Maximum number of retries
        callback_manager (Optional[CallbackManager]): A callback manager object

    """

    def__init__(
        self,
        query_engine: BaseQueryEngine,
        evaluator: BaseEvaluator,
        max_retries: int = 3,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        self._query_engine = query_engine
        self._evaluator = evaluator
        self.max_retries = max_retries
        super().__init__(callback_manager)

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {"query_engine": self._query_engine, "evaluator": self._evaluator}

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        response = self._query_engine._query(query_bundle)
        assert not isinstance(response, AsyncStreamingResponse)
        if self.max_retries <= 0:
            return response
        typed_response = (
            response if isinstance(response, Response) else response.get_response()
        )
        query_str = query_bundle.query_str
        eval = self._evaluator.evaluate_response(query_str, typed_response)
        if eval.passing:
            logger.debug("Evaluation returned True.")
            return response
        else:
            logger.debug("Evaluation returned False.")
            new_query_engine = RetryQueryEngine(
                self._query_engine, self._evaluator, self.max_retries - 1
            )
            query_transformer = FeedbackQueryTransformation()
            new_query = query_transformer.run(query_bundle, {"evaluation": eval})
            return new_query_engine.query(new_query)

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Not supported."""
        return self._query(query_bundle)

```
 |  
| --- | --- |  
##  RetrySourceQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.RetrySourceQueryEngine "Permanent link")
Bases: 
Retry with different source nodes.
Source code in `llama-index-core/llama_index/core/query_engine/retry_source_query_engine.py`  
| 
```
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
```
 | 
```
classRetrySourceQueryEngine(BaseQueryEngine):
"""Retry with different source nodes."""

    def__init__(
        self,
        query_engine: RetrieverQueryEngine,
        evaluator: BaseEvaluator,
        llm: Optional[LLM] = None,
        max_retries: int = 3,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
"""Run a BaseQueryEngine with retries."""
        self._query_engine = query_engine
        self._evaluator = evaluator
        self._llm = llm or Settings.llm
        self.max_retries = max_retries
        super().__init__(callback_manager=callback_manager or Settings.callback_manager)

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {"query_engine": self._query_engine, "evaluator": self._evaluator}

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        response = self._query_engine._query(query_bundle)
        assert not isinstance(response, AsyncStreamingResponse)
        if self.max_retries <= 0:
            return response
        typed_response = (
            response if isinstance(response, Response) else response.get_response()
        )
        query_str = query_bundle.query_str
        eval = self._evaluator.evaluate_response(query_str, typed_response)
        if eval.passing:
            logger.debug("Evaluation returned True.")
            return response
        else:
            logger.debug("Evaluation returned False.")
            # Test source nodes
            source_evals = [
                self._evaluator.evaluate(
                    query=query_str,
                    response=typed_response.response,
                    contexts=[source_node.get_content()],
                )
                for source_node in typed_response.source_nodes
            ]
            orig_nodes = typed_response.source_nodes
            assert len(source_evals) == len(orig_nodes)
            new_docs = []
            for node, eval_result in zip(orig_nodes, source_evals):
                if eval_result:
                    new_docs.append(Document(text=node.node.get_content()))
            if len(new_docs) == 0:
                raise ValueError("No source nodes passed evaluation.")
            new_index = SummaryIndex.from_documents(
                new_docs,
            )
            new_retriever_engine = RetrieverQueryEngine(new_index.as_retriever())
            new_query_engine = RetrySourceQueryEngine(
                new_retriever_engine,
                self._evaluator,
                self._llm,
                self.max_retries - 1,
            )
            return new_query_engine.query(query_bundle)

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Not supported."""
        return self._query(query_bundle)

```
 |  
| --- | --- |  
##  RetrieverRouterQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.RetrieverRouterQueryEngine "Permanent link")
Bases: 
Retriever-based router query engine.
NOTE: this is deprecated, please use our new ToolRetrieverRouterQueryEngine
Use a retriever to select a set of Nodes. Each node will be converted into a ToolMetadata object, and also used to retrieve a query engine, to form a QueryEngineTool.
NOTE: this is a beta feature. We are figuring out the right interface between the retriever and query engine.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  `BaseSelector`  |  A selector that chooses one out of many options based on each candidate's metadata and query.  |  _required_  |  
|  `query_engine_tools`  |  `Sequence[QueryEngineTool[](https://developers.llamaindex.ai/python/framework-api-reference/tools/query_engine/#llama_index.core.tools.query_engine.QueryEngineTool "QueryEngineTool \(llama_index.core.tools.query_engine.QueryEngineTool\)")]`  |  A sequence of candidate query engines. They must be wrapped as tools to expose metadata to the selector.  |  _required_  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  A callback manager.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/query_engine/router_query_engine.py`  
| 
```
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
```
 | 
```
classRetrieverRouterQueryEngine(BaseQueryEngine):
"""
    Retriever-based router query engine.

    NOTE: this is deprecated, please use our new ToolRetrieverRouterQueryEngine

    Use a retriever to select a set of Nodes. Each node will be converted
    into a ToolMetadata object, and also used to retrieve a query engine, to form
    a QueryEngineTool.

    NOTE: this is a beta feature. We are figuring out the right interface
    between the retriever and query engine.

    Args:
        selector (BaseSelector): A selector that chooses one out of many options based
            on each candidate's metadata and query.
        query_engine_tools (Sequence[QueryEngineTool]): A sequence of candidate
            query engines. They must be wrapped as tools to expose metadata to
            the selector.
        callback_manager (Optional[CallbackManager]): A callback manager.

    """

    def__init__(
        self,
        retriever: BaseRetriever,
        node_to_query_engine_fn: Callable,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        self._retriever = retriever
        self._node_to_query_engine_fn = node_to_query_engine_fn
        super().__init__(callback_manager)

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        # NOTE: don't include tools for now
        return {"retriever": self._retriever}

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        nodes_with_score = self._retriever.retrieve(query_bundle)
        # TODO: for now we only support retrieving one node
        if len(nodes_with_score)  1:
            raise ValueError("Retrieved more than one node.")

        node = nodes_with_score[0].node
        query_engine = self._node_to_query_engine_fn(node)
        return query_engine.query(query_bundle)

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        return self._query(query_bundle)

```
 |  
| --- | --- |  
##  RouterQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.RouterQueryEngine "Permanent link")
Bases: 
Router query engine.
Selects one out of several candidate query engines to execute a query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  `BaseSelector`  |  A selector that chooses one out of many options based on each candidate's metadata and query.  |  _required_  |  
|  `query_engine_tools`  |  `Sequence[QueryEngineTool[](https://developers.llamaindex.ai/python/framework-api-reference/tools/query_engine/#llama_index.core.tools.query_engine.QueryEngineTool "QueryEngineTool \(llama_index.core.tools.query_engine.QueryEngineTool\)")]`  |  A sequence of candidate query engines. They must be wrapped as tools to expose metadata to the selector.  |  _required_  |  
|  `summarizer`  |  `Optional[TreeSummarize[](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/accumulate/#llama_index.core.response_synthesizers.TreeSummarize "TreeSummarize \(llama_index.core.response_synthesizers.TreeSummarize\)")]`  |  Tree summarizer to summarize sub-results.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/query_engine/router_query_engine.py`  
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
```
 | 
```
classRouterQueryEngine(BaseQueryEngine):
"""
    Router query engine.

    Selects one out of several candidate query engines to execute a query.

    Args:
        selector (BaseSelector): A selector that chooses one out of many options based
            on each candidate's metadata and query.
        query_engine_tools (Sequence[QueryEngineTool]): A sequence of candidate
            query engines. They must be wrapped as tools to expose metadata to
            the selector.
        summarizer (Optional[TreeSummarize]): Tree summarizer to summarize sub-results.

    """

    def__init__(
        self,
        selector: BaseSelector,
        query_engine_tools: Sequence[QueryEngineTool],
        llm: Optional[LLM] = None,
        summarizer: Optional[TreeSummarize] = None,
        verbose: bool = False,
    ) -> None:
        self._llm = llm or Settings.llm
        self._selector = selector
        self._query_engines = [x.query_engine for x in query_engine_tools]
        self._metadatas = [x.metadata for x in query_engine_tools]
        self._summarizer = summarizer or TreeSummarize(
            llm=self._llm,
            summary_template=DEFAULT_TREE_SUMMARIZE_PROMPT_SEL,
        )
        self._verbose = verbose

        super().__init__(callback_manager=Settings.callback_manager)

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        # NOTE: don't include tools for now
        return {"summarizer": self._summarizer, "selector": self._selector}

    @classmethod
    deffrom_defaults(
        cls,
        query_engine_tools: Sequence[QueryEngineTool],
        llm: Optional[LLM] = None,
        selector: Optional[BaseSelector] = None,
        summarizer: Optional[TreeSummarize] = None,
        select_multi: bool = False,
        **kwargs: Any,
    ) -> "RouterQueryEngine":
        llm = llm or Settings.llm

        selector = selector or get_selector_from_llm(llm, is_multi=select_multi)

        assert selector is not None

        return cls(
            selector,
            query_engine_tools,
            llm=llm,
            summarizer=summarizer,
            **kwargs,
        )

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            result = self._selector.select(self._metadatas, query_bundle)

            if len(result.inds)  1:
                responses = []
                for i, engine_ind in enumerate(result.inds):
                    log_str = (
                        f"Selecting query engine {engine_ind}: {result.reasons[i]}."
                    )
                    logger.info(log_str)
                    if self._verbose:
                        print_text(log_str + "\n", color="pink")

                    selected_query_engine = self._query_engines[engine_ind]
                    responses.append(selected_query_engine.query(query_bundle))

                if len(responses)  1:
                    final_response = combine_responses(
                        self._summarizer, responses, query_bundle
                    )
                else:
                    final_response = responses[0]
            else:
                try:
                    selected_query_engine = self._query_engines[result.ind]
                    log_str = f"Selecting query engine {result.ind}: {result.reason}."
                    logger.info(log_str)
                    if self._verbose:
                        print_text(log_str + "\n", color="pink")
                except ValueError as e:
                    raise ValueError("Failed to select query engine") frome

                final_response = selected_query_engine.query(query_bundle)

            # add selected result
            final_response.metadata = final_response.metadata or {}
            final_response.metadata["selector_result"] = result

            query_event.on_end(payload={EventPayload.RESPONSE: final_response})

        return final_response

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            result = await self._selector.aselect(self._metadatas, query_bundle)

            if len(result.inds)  1:
                tasks = []
                for i, engine_ind in enumerate(result.inds):
                    log_str = (
                        f"Selecting query engine {engine_ind}: {result.reasons[i]}."
                    )
                    logger.info(log_str)
                    if self._verbose:
                        print_text(log_str + "\n", color="pink")
                    selected_query_engine = self._query_engines[engine_ind]
                    tasks.append(selected_query_engine.aquery(query_bundle))

                responses = await asyncio.gather(*tasks)
                if len(responses)  1:
                    final_response = await acombine_responses(
                        self._summarizer, responses, query_bundle
                    )
                else:
                    final_response = responses[0]
            else:
                try:
                    selected_query_engine = self._query_engines[result.ind]
                    log_str = f"Selecting query engine {result.ind}: {result.reason}."
                    logger.info(log_str)
                    if self._verbose:
                        print_text(log_str + "\n", color="pink")
                except ValueError as e:
                    raise ValueError("Failed to select query engine") frome

                final_response = await selected_query_engine.aquery(query_bundle)

            # add selected result
            final_response.metadata = final_response.metadata or {}
            final_response.metadata["selector_result"] = result

            query_event.on_end(payload={EventPayload.RESPONSE: final_response})

        return final_response

```
 |  
| --- | --- |  
##  ToolRetrieverRouterQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.ToolRetrieverRouterQueryEngine "Permanent link")
Bases: 
Tool Retriever router query engine.
Selects a set of candidate query engines to execute a query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `retriever`  |   |  A retriever that retrieves a set of query engine tools.  |  _required_  |  
|  `summarizer`  |  `Optional[TreeSummarize[](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/accumulate/#llama_index.core.response_synthesizers.TreeSummarize "TreeSummarize \(llama_index.core.response_synthesizers.TreeSummarize\)")]`  |  Tree summarizer to summarize sub-results.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/query_engine/router_query_engine.py`  
| 
```
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
```
 | 
```
classToolRetrieverRouterQueryEngine(BaseQueryEngine):
"""
    Tool Retriever router query engine.

    Selects a set of candidate query engines to execute a query.

    Args:
        retriever (ObjectRetriever): A retriever that retrieves a set of
            query engine tools.
        summarizer (Optional[TreeSummarize]): Tree summarizer to summarize sub-results.

    """

    def__init__(
        self,
        retriever: ObjectRetriever[QueryEngineTool],
        llm: Optional[LLM] = None,
        summarizer: Optional[TreeSummarize] = None,
    ) -> None:
        llm = llm or Settings.llm
        self._summarizer = summarizer or TreeSummarize(
            llm=llm,
            summary_template=DEFAULT_TREE_SUMMARIZE_PROMPT_SEL,
        )
        self._retriever = retriever

        super().__init__(Settings.callback_manager)

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        # NOTE: don't include tools for now
        return {"summarizer": self._summarizer}

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            query_engine_tools = self._retriever.retrieve(query_bundle)
            responses = []
            for query_engine_tool in query_engine_tools:
                query_engine = query_engine_tool.query_engine
                responses.append(query_engine.query(query_bundle))

            if len(responses)  1:
                final_response = combine_responses(
                    self._summarizer, responses, query_bundle
                )
            else:
                final_response = responses[0]

            # add selected result
            final_response.metadata = final_response.metadata or {}
            final_response.metadata["retrieved_tools"] = query_engine_tools

            query_event.on_end(payload={EventPayload.RESPONSE: final_response})

        return final_response

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            query_engine_tools = self._retriever.retrieve(query_bundle)
            tasks = []
            for query_engine_tool in query_engine_tools:
                query_engine = query_engine_tool.query_engine
                tasks.append(query_engine.aquery(query_bundle))
            responses = await asyncio.gather(*tasks)
            if len(responses)  1:
                final_response = await acombine_responses(
                    self._summarizer, responses, query_bundle
                )
            else:
                final_response = responses[0]

            # add selected result
            final_response.metadata = final_response.metadata or {}
            final_response.metadata["retrieved_tools"] = query_engine_tools

            query_event.on_end(payload={EventPayload.RESPONSE: final_response})

        return final_response

```
 |  
| --- | --- |  
##  SQLJoinQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.SQLJoinQueryEngine "Permanent link")
Bases: 
SQL Join Query Engine.
This query engine can "Join" a SQL database results with another query engine. It can decide it needs to query the SQL database or the other query engine. If it decides to query the SQL database, it will first query the SQL database, whether to augment information with retrieved results from the other query engine.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sql_query_tool`  |   |  Query engine tool for SQL database. other_query_tool (QueryEngineTool): Other query engine tool.  |  _required_  |  
|  `selector`  |  `Optional[Union[LLMSingleSelector, PydanticSingleSelector]]`  |  Selector to use.  |  `None`  |  
|  `sql_join_synthesis_prompt`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.base.BasePromptTemplate\)")]`  |  PromptTemplate to use for SQL join synthesis.  |  `None`  |  
|  `sql_augment_query_transform`  |  `Optional[SQLAugmentQueryTransform]`  |  Query transform to use for SQL augmentation.  |  `None`  |  
|  `use_sql_join_synthesis`  |  `bool`  |  Whether to use SQL join synthesis.  |  `True`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  Callback manager to use.  |  `None`  |  
|  `verbose`  |  `bool`  |  Whether to print intermediate results.  |  `True`  |  
Source code in `llama-index-core/llama_index/core/query_engine/sql_join_query_engine.py`  
| 
```
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
```
 | 
```
classSQLJoinQueryEngine(BaseQueryEngine):
"""
    SQL Join Query Engine.

    This query engine can "Join" a SQL database results
    with another query engine.
    It can decide it needs to query the SQL database or the other query engine.
    If it decides to query the SQL database, it will first query the SQL database,
    whether to augment information with retrieved results from the other query engine.

    Args:
        sql_query_tool (QueryEngineTool): Query engine tool for SQL database.
            other_query_tool (QueryEngineTool): Other query engine tool.
        selector (Optional[Union[LLMSingleSelector, PydanticSingleSelector]]):
            Selector to use.
        sql_join_synthesis_prompt (Optional[BasePromptTemplate]):
            PromptTemplate to use for SQL join synthesis.
        sql_augment_query_transform (Optional[SQLAugmentQueryTransform]): Query
            transform to use for SQL augmentation.
        use_sql_join_synthesis (bool): Whether to use SQL join synthesis.
        callback_manager (Optional[CallbackManager]): Callback manager to use.
        verbose (bool): Whether to print intermediate results.

    """

    def__init__(
        self,
        sql_query_tool: QueryEngineTool,
        other_query_tool: QueryEngineTool,
        selector: Optional[Union[LLMSingleSelector, PydanticSingleSelector]] = None,
        llm: Optional[LLM] = None,
        sql_join_synthesis_prompt: Optional[BasePromptTemplate] = None,
        sql_augment_query_transform: Optional[SQLAugmentQueryTransform] = None,
        use_sql_join_synthesis: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        verbose: bool = True,
        streaming: bool = False,
    ) -> None:
"""Initialize params."""
        super().__init__(callback_manager=callback_manager)
        # validate that the query engines are of the right type
        if not isinstance(
            sql_query_tool.query_engine,
            (BaseSQLTableQueryEngine, NLSQLTableQueryEngine),
        ):
            raise ValueError(
                "sql_query_tool.query_engine must be an instance of "
                "BaseSQLTableQueryEngine or NLSQLTableQueryEngine"
            )
        self._sql_query_tool = sql_query_tool
        self._other_query_tool = other_query_tool

        self._llm = llm or Settings.llm

        self._selector = selector or get_selector_from_llm(self._llm, is_multi=False)  # type: ignore
        assert isinstance(self._selector, (LLMSingleSelector, PydanticSingleSelector))

        self._sql_join_synthesis_prompt = (
            sql_join_synthesis_prompt or DEFAULT_SQL_JOIN_SYNTHESIS_PROMPT
        )
        self._sql_augment_query_transform = (
            sql_augment_query_transform or SQLAugmentQueryTransform(llm=self._llm)
        )
        self._use_sql_join_synthesis = use_sql_join_synthesis
        self._verbose = verbose
        self._streaming = streaming

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {
            "selector": self._selector,
            "sql_augment_query_transform": self._sql_augment_query_transform,
        }

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {"sql_join_synthesis_prompt": self._sql_join_synthesis_prompt}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "sql_join_synthesis_prompt" in prompts:
            self._sql_join_synthesis_prompt = prompts["sql_join_synthesis_prompt"]

    def_query_sql_other(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Query SQL database + other query engine in sequence."""
        # first query SQL database
        sql_response = self._sql_query_tool.query_engine.query(query_bundle)
        if not self._use_sql_join_synthesis:
            return sql_response

        sql_query = (
            sql_response.metadata["sql_query"] if sql_response.metadata else None
        )
        if self._verbose:
            print_text(f"SQL query: {sql_query}\n", color="yellow")
            print_text(f"SQL response: {sql_response}\n", color="yellow")

        # given SQL db, transform query into new query
        new_query = self._sql_augment_query_transform(
            query_bundle.query_str,
            metadata={
                "sql_query": _format_sql_query(sql_query),
                "sql_query_response": str(sql_response),
            },
        )

        if self._verbose:
            print_text(
                f"Transformed query given SQL response: {new_query.query_str}\n",
                color="blue",
            )
        logger.info(f"> Transformed query given SQL response: {new_query.query_str}")
        if self._sql_augment_query_transform.check_stop(new_query):
            return sql_response

        other_response = self._other_query_tool.query_engine.query(new_query)
        if self._verbose:
            print_text(f"query engine response: {other_response}\n", color="pink")
        logger.info(f"> query engine response: {other_response}")

        if self._streaming:
            response_gen = self._llm.stream(
                self._sql_join_synthesis_prompt,
                query_str=query_bundle.query_str,
                sql_query_str=sql_query,
                sql_response_str=str(sql_response),
                query_engine_query_str=new_query.query_str,
                query_engine_response_str=str(other_response),
            )

            response_metadata = {
                **(sql_response.metadata or {}),
                **(other_response.metadata or {}),
            }
            source_nodes = other_response.source_nodes
            return StreamingResponse(
                response_gen,
                metadata=response_metadata,
                source_nodes=source_nodes,
            )
        else:
            response_str = self._llm.predict(
                self._sql_join_synthesis_prompt,
                query_str=query_bundle.query_str,
                sql_query_str=sql_query,
                sql_response_str=str(sql_response),
                query_engine_query_str=new_query.query_str,
                query_engine_response_str=str(other_response),
            )

            response_metadata = {
                **(sql_response.metadata or {}),
                **(other_response.metadata or {}),
            }
            source_nodes = other_response.source_nodes
            return Response(
                response_str,
                metadata=response_metadata,
                source_nodes=source_nodes,
            )

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Query and get response."""
        # TODO: see if this can be consolidated with logic in RouterQueryEngine
        metadatas = [self._sql_query_tool.metadata, self._other_query_tool.metadata]
        result = self._selector.select(metadatas, query_bundle)
        # pick sql query
        if result.ind == 0:
            if self._verbose:
                print_text(f"Querying SQL database: {result.reason}\n", color="blue")
            logger.info(f"> Querying SQL database: {result.reason}")
            return self._query_sql_other(query_bundle)
        elif result.ind == 1:
            if self._verbose:
                print_text(
                    f"Querying other query engine: {result.reason}\n", color="blue"
                )
            logger.info(f"> Querying other query engine: {result.reason}")
            return self._other_query_tool.query_engine.query(query_bundle)
        else:
            raise ValueError(f"Invalid result.ind: {result.ind}")

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        # TODO: make async
        return self._query(query_bundle)

```
 |  
| --- | --- |  
##  SQLAutoVectorQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.SQLAutoVectorQueryEngine "Permanent link")
Bases: 
SQL + Vector Index Auto Retriever Query Engine.
This query engine can query both a SQL database as well as a vector database. It will first decide whether it needs to query the SQL database or vector store. If it decides to query the SQL database, it will also decide whether to augment information with retrieved results from the vector store. We use the VectorIndexAutoRetriever to retrieve results.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sql_query_tool`  |   |  Query engine tool for SQL database.  |  _required_  |  
|  `vector_query_tool`  |   |  Query engine tool for vector database.  |  _required_  |  
|  `selector`  |  `Optional[Union[LLMSingleSelector, PydanticSingleSelector]]`  |  Selector to use.  |  `None`  |  
|  `sql_vector_synthesis_prompt`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.base.BasePromptTemplate\)")]`  |  Prompt to use for SQL vector synthesis.  |  `None`  |  
|  `sql_augment_query_transform`  |  `Optional[SQLAugmentQueryTransform]`  |  Query transform to use for SQL augmentation.  |  `None`  |  
|  `use_sql_vector_synthesis`  |  `bool`  |  Whether to use SQL vector synthesis.  |  `True`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  Callback manager to use.  |  `None`  |  
|  `verbose`  |  `bool`  |  Whether to print intermediate results.  |  `True`  |  
Source code in `llama-index-core/llama_index/core/query_engine/sql_vector_query_engine.py`  
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
```
 | 
```
classSQLAutoVectorQueryEngine(SQLJoinQueryEngine):
"""
    SQL + Vector Index Auto Retriever Query Engine.

    This query engine can query both a SQL database
    as well as a vector database. It will first decide
    whether it needs to query the SQL database or vector store.
    If it decides to query the SQL database, it will also decide
    whether to augment information with retrieved results from the vector store.
    We use the VectorIndexAutoRetriever to retrieve results.

    Args:
        sql_query_tool (QueryEngineTool): Query engine tool for SQL database.
        vector_query_tool (QueryEngineTool): Query engine tool for vector database.
        selector (Optional[Union[LLMSingleSelector, PydanticSingleSelector]]):
            Selector to use.
        sql_vector_synthesis_prompt (Optional[BasePromptTemplate]):
            Prompt to use for SQL vector synthesis.
        sql_augment_query_transform (Optional[SQLAugmentQueryTransform]): Query
            transform to use for SQL augmentation.
        use_sql_vector_synthesis (bool): Whether to use SQL vector synthesis.
        callback_manager (Optional[CallbackManager]): Callback manager to use.
        verbose (bool): Whether to print intermediate results.

    """

    def__init__(
        self,
        sql_query_tool: QueryEngineTool,
        vector_query_tool: QueryEngineTool,
        selector: Optional[Union[LLMSingleSelector, PydanticSingleSelector]] = None,
        llm: Optional[LLM] = None,
        sql_vector_synthesis_prompt: Optional[BasePromptTemplate] = None,
        sql_augment_query_transform: Optional[SQLAugmentQueryTransform] = None,
        use_sql_vector_synthesis: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        verbose: bool = True,
    ) -> None:
"""Initialize params."""
        # validate that the query engines are of the right type
        if not isinstance(
            sql_query_tool.query_engine,
            (BaseSQLTableQueryEngine, NLSQLTableQueryEngine),
        ):
            raise ValueError(
                "sql_query_tool.query_engine must be an instance of "
                "BaseSQLTableQueryEngine or NLSQLTableQueryEngine"
            )
        if not isinstance(vector_query_tool.query_engine, RetrieverQueryEngine):
            raise ValueError(
                "vector_query_tool.query_engine must be an instance of "
                "RetrieverQueryEngine"
            )
        if not isinstance(
            vector_query_tool.query_engine.retriever, VectorIndexAutoRetriever
        ):
            raise ValueError(
                "vector_query_tool.query_engine.retriever must be an instance "
                "of VectorIndexAutoRetriever"
            )

        sql_vector_synthesis_prompt = (
            sql_vector_synthesis_prompt or DEFAULT_SQL_VECTOR_SYNTHESIS_PROMPT
        )
        super().__init__(
            sql_query_tool,
            vector_query_tool,
            selector=selector,
            llm=llm,
            sql_join_synthesis_prompt=sql_vector_synthesis_prompt,
            sql_augment_query_transform=sql_augment_query_transform,
            use_sql_join_synthesis=use_sql_vector_synthesis,
            callback_manager=callback_manager,
            verbose=verbose,
        )

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {
            "selector": self._selector,
            "sql_augment_query_transform": self._sql_augment_query_transform,
        }

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {"sql_join_synthesis_prompt": self._sql_join_synthesis_prompt}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "sql_join_synthesis_prompt" in prompts:
            self._sql_join_synthesis_prompt = prompts["sql_join_synthesis_prompt"]

    @classmethod
    deffrom_sql_and_vector_query_engines(
        cls,
        sql_query_engine: Union[BaseSQLTableQueryEngine, NLSQLTableQueryEngine],
        sql_tool_name: str,
        sql_tool_description: str,
        vector_auto_retriever: RetrieverQueryEngine,
        vector_tool_name: str,
        vector_tool_description: str,
        selector: Optional[Union[LLMSingleSelector, PydanticSingleSelector]] = None,
        **kwargs: Any,
    ) -> "SQLAutoVectorQueryEngine":
"""
        From SQL and vector query engines.

        Args:
            sql_query_engine (BaseSQLTableQueryEngine): SQL query engine.
            vector_query_engine (VectorIndexAutoRetriever): Vector retriever.
            selector (Optional[Union[LLMSingleSelector, PydanticSingleSelector]]):
                Selector to use.

        """
        sql_query_tool = QueryEngineTool.from_defaults(
            sql_query_engine, name=sql_tool_name, description=sql_tool_description
        )
        vector_query_tool = QueryEngineTool.from_defaults(
            vector_auto_retriever,
            name=vector_tool_name,
            description=vector_tool_description,
        )
        return cls(sql_query_tool, vector_query_tool, selector, **kwargs)

```
 |  
| --- | --- |  
###  from_sql_and_vector_query_engines `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.SQLAutoVectorQueryEngine.from_sql_and_vector_query_engines "Permanent link")

```
from_sql_and_vector_query_engines(
    sql_query_engine: Union[
        BaseSQLTableQueryEngine, 
    ],
    sql_tool_name: ,
    sql_tool_description: ,
    vector_auto_retriever: ,
    vector_tool_name: ,
    vector_tool_description: ,
    selector: Optional[
        Union[LLMSingleSelector, PydanticSingleSelector]
    ] = None,
    **kwargs: 
) -> 

```

From SQL and vector query engines.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sql_query_engine`  |  `BaseSQLTableQueryEngine`  |  SQL query engine.  |  _required_  |  
|  `vector_query_engine`  |   |  Vector retriever.  |  _required_  |  
|  `selector`  |  `Optional[Union[LLMSingleSelector, PydanticSingleSelector]]`  |  Selector to use.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/query_engine/sql_vector_query_engine.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_sql_and_vector_query_engines(
    cls,
    sql_query_engine: Union[BaseSQLTableQueryEngine, NLSQLTableQueryEngine],
    sql_tool_name: str,
    sql_tool_description: str,
    vector_auto_retriever: RetrieverQueryEngine,
    vector_tool_name: str,
    vector_tool_description: str,
    selector: Optional[Union[LLMSingleSelector, PydanticSingleSelector]] = None,
    **kwargs: Any,
) -> "SQLAutoVectorQueryEngine":
"""
    From SQL and vector query engines.

    Args:
        sql_query_engine (BaseSQLTableQueryEngine): SQL query engine.
        vector_query_engine (VectorIndexAutoRetriever): Vector retriever.
        selector (Optional[Union[LLMSingleSelector, PydanticSingleSelector]]):
            Selector to use.

    """
    sql_query_tool = QueryEngineTool.from_defaults(
        sql_query_engine, name=sql_tool_name, description=sql_tool_description
    )
    vector_query_tool = QueryEngineTool.from_defaults(
        vector_auto_retriever,
        name=vector_tool_name,
        description=vector_tool_description,
    )
    return cls(sql_query_tool, vector_query_tool, selector, **kwargs)

```
 |  
| --- | --- |  
##  SubQuestionAnswerPair [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.SubQuestionAnswerPair "Permanent link")
Bases: `BaseModel`
Pair of the sub question and optionally its answer (if its been answered yet).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sub_q`  |   |  _required_  |  
|  `answer`  |  `str | None`  |  `None`  |  
|  `sources`  |  `List[NodeWithScore[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.NodeWithScore "NodeWithScore \(llama_index.core.schema.NodeWithScore\)")]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
Source code in `llama-index-core/llama_index/core/query_engine/sub_question_query_engine.py`  
| 
```
27
28
29
30
31
32
33
34
```
 | 
```
classSubQuestionAnswerPair(BaseModel):
"""
    Pair of the sub question and optionally its answer (if its been answered yet).
    """

    sub_q: SubQuestion
    answer: Optional[str] = None
    sources: List[NodeWithScore] = Field(default_factory=list)

```
 |  
| --- | --- |  
##  SubQuestionQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.SubQuestionQueryEngine "Permanent link")
Bases: 
Sub question query engine.
A query engine that breaks down a complex query (e.g. compare and contrast) into many sub questions and their target query engine for execution. After executing all sub questions, all responses are gathered and sent to response synthesizer to produce the final response.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `question_gen`  |   |  A module for generating sub questions given a complex question and tools.  |  _required_  |  
|  `response_synthesizer`  |   |  A response synthesizer for generating the final response  |  _required_  |  
|  `query_engine_tools`  |  `Sequence[QueryEngineTool[](https://developers.llamaindex.ai/python/framework-api-reference/tools/query_engine/#llama_index.core.tools.query_engine.QueryEngineTool "QueryEngineTool \(llama_index.core.tools.query_engine.QueryEngineTool\)")]`  |  Tools to answer the sub questions.  |  _required_  |  
|  `verbose`  |  `bool`  |  whether to print intermediate questions and answers. Defaults to True  |  `True`  |  
|  `use_async`  |  `bool`  |  whether to execute the sub questions with asyncio. Defaults to True  |  `False`  |  
Source code in `llama-index-core/llama_index/core/query_engine/sub_question_query_engine.py`  
| 
```
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
```
 | 
```
classSubQuestionQueryEngine(BaseQueryEngine):
"""
    Sub question query engine.

    A query engine that breaks down a complex query (e.g. compare and contrast) into
        many sub questions and their target query engine for execution.
        After executing all sub questions, all responses are gathered and sent to
        response synthesizer to produce the final response.

    Args:
        question_gen (BaseQuestionGenerator): A module for generating sub questions
            given a complex question and tools.
        response_synthesizer (BaseSynthesizer): A response synthesizer for
            generating the final response
        query_engine_tools (Sequence[QueryEngineTool]): Tools to answer the
            sub questions.
        verbose (bool): whether to print intermediate questions and answers.
            Defaults to True
        use_async (bool): whether to execute the sub questions with asyncio.
            Defaults to True

    """

    def__init__(
        self,
        question_gen: BaseQuestionGenerator,
        response_synthesizer: BaseSynthesizer,
        query_engine_tools: Sequence[QueryEngineTool],
        callback_manager: Optional[CallbackManager] = None,
        verbose: bool = True,
        use_async: bool = False,
    ) -> None:
        self._question_gen = question_gen
        self._response_synthesizer = response_synthesizer
        self._metadatas = [x.metadata for x in query_engine_tools]
        self._query_engines = {
            tool.metadata.name: tool.query_engine for tool in query_engine_tools
        }
        self._verbose = verbose
        self._use_async = use_async
        super().__init__(callback_manager)

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {
            "question_gen": self._question_gen,
            "response_synthesizer": self._response_synthesizer,
        }

    @classmethod
    deffrom_defaults(
        cls,
        query_engine_tools: Sequence[QueryEngineTool],
        llm: Optional[LLM] = None,
        question_gen: Optional[BaseQuestionGenerator] = None,
        response_synthesizer: Optional[BaseSynthesizer] = None,
        verbose: bool = True,
        use_async: bool = True,
    ) -> "SubQuestionQueryEngine":
        callback_manager = Settings.callback_manager
        if len(query_engine_tools)  0:
            callback_manager = query_engine_tools[0].query_engine.callback_manager

        llm = llm or Settings.llm
        if question_gen is None:
            try:
                fromllama_index.question_gen.openaiimport (
                    OpenAIQuestionGenerator,
                )  # pants: no-infer-dep

                # try to use OpenAI function calling based question generator.
                # if incompatible, use general LLM question generator
                question_gen = OpenAIQuestionGenerator.from_defaults(llm=llm)

            except ImportError as e:
                raise ImportError(
                    "`llama-index-question-gen-openai` package cannot be found. "
                    "Please install it by using `pip install `llama-index-question-gen-openai`"
                )
            except ValueError:
                question_gen = LLMQuestionGenerator.from_defaults(llm=llm)

        synth = response_synthesizer or get_response_synthesizer(
            llm=llm,
            callback_manager=callback_manager,
            use_async=use_async,
        )

        return cls(
            question_gen,
            synth,
            query_engine_tools,
            callback_manager=callback_manager,
            verbose=verbose,
            use_async=use_async,
        )

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            sub_questions = self._question_gen.generate(self._metadatas, query_bundle)

            colors = get_color_mapping([str(i) for i in range(len(sub_questions))])

            if self._verbose:
                print_text(f"Generated {len(sub_questions)} sub questions.\n")

            if self._use_async:
                tasks = [
                    self._aquery_subq(sub_q, color=colors[str(ind)])
                    for ind, sub_q in enumerate(sub_questions)
                ]

                qa_pairs_all = run_async_tasks(tasks)
                qa_pairs_all = cast(List[Optional[SubQuestionAnswerPair]], qa_pairs_all)
            else:
                qa_pairs_all = [
                    self._query_subq(sub_q, color=colors[str(ind)])
                    for ind, sub_q in enumerate(sub_questions)
                ]

            # filter out sub questions that failed
            qa_pairs: List[SubQuestionAnswerPair] = list(filter(None, qa_pairs_all))

            nodes = [self._construct_node(pair) for pair in qa_pairs]

            source_nodes = [node for qa_pair in qa_pairs for node in qa_pair.sources]
            response = self._response_synthesizer.synthesize(
                query=query_bundle,
                nodes=nodes,
                additional_source_nodes=source_nodes,
            )

            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            sub_questions = await self._question_gen.agenerate(
                self._metadatas, query_bundle
            )

            colors = get_color_mapping([str(i) for i in range(len(sub_questions))])

            if self._verbose:
                print_text(f"Generated {len(sub_questions)} sub questions.\n")

            tasks = [
                self._aquery_subq(sub_q, color=colors[str(ind)])
                for ind, sub_q in enumerate(sub_questions)
            ]

            qa_pairs_all = await asyncio.gather(*tasks)
            qa_pairs_all = cast(List[Optional[SubQuestionAnswerPair]], qa_pairs_all)

            # filter out sub questions that failed
            qa_pairs: List[SubQuestionAnswerPair] = list(filter(None, qa_pairs_all))

            nodes = [self._construct_node(pair) for pair in qa_pairs]

            source_nodes = [node for qa_pair in qa_pairs for node in qa_pair.sources]
            response = await self._response_synthesizer.asynthesize(
                query=query_bundle,
                nodes=nodes,
                additional_source_nodes=source_nodes,
            )

            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

    def_construct_node(self, qa_pair: SubQuestionAnswerPair) -> NodeWithScore:
        node_text = (
            f"Sub question: {qa_pair.sub_q.sub_question}\nResponse: {qa_pair.answer}"
        )
        return NodeWithScore(node=TextNode(text=node_text))

    async def_aquery_subq(
        self, sub_q: SubQuestion, color: Optional[str] = None
    ) -> Optional[SubQuestionAnswerPair]:
        try:
            with self.callback_manager.event(
                CBEventType.SUB_QUESTION,
                payload={EventPayload.SUB_QUESTION: SubQuestionAnswerPair(sub_q=sub_q)},
            ) as event:
                question = sub_q.sub_question
                query_engine = self._query_engines[sub_q.tool_name]

                if self._verbose:
                    print_text(f"[{sub_q.tool_name}] Q: {question}\n", color=color)

                response = await query_engine.aquery(question)
                response_text = str(response)

                if self._verbose:
                    print_text(f"[{sub_q.tool_name}] A: {response_text}\n", color=color)

                qa_pair = SubQuestionAnswerPair(
                    sub_q=sub_q, answer=response_text, sources=response.source_nodes
                )

                event.on_end(payload={EventPayload.SUB_QUESTION: qa_pair})

            return qa_pair
        except Exception:
            logger.warning(
                f"[{sub_q.tool_name}] Failed to run {question}",
                exc_info=True,
            )
            return None

    def_query_subq(
        self, sub_q: SubQuestion, color: Optional[str] = None
    ) -> Optional[SubQuestionAnswerPair]:
        try:
            with self.callback_manager.event(
                CBEventType.SUB_QUESTION,
                payload={EventPayload.SUB_QUESTION: SubQuestionAnswerPair(sub_q=sub_q)},
            ) as event:
                question = sub_q.sub_question
                query_engine = self._query_engines[sub_q.tool_name]

                if self._verbose:
                    print_text(f"[{sub_q.tool_name}] Q: {question}\n", color=color)

                response = query_engine.query(question)
                response_text = str(response)

                if self._verbose:
                    print_text(f"[{sub_q.tool_name}] A: {response_text}\n", color=color)

                qa_pair = SubQuestionAnswerPair(
                    sub_q=sub_q, answer=response_text, sources=response.source_nodes
                )

                event.on_end(payload={EventPayload.SUB_QUESTION: qa_pair})

            return qa_pair
        except Exception:
            logger.warning(
                f"[{sub_q.tool_name}] Failed to run {question}",
                exc_info=True,
            )
            return None

```
 |  
| --- | --- |  
##  TransformQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/NL_SQL_table/#llama_index.core.query_engine.TransformQueryEngine "Permanent link")
Bases: 
Transform query engine.
Applies a query transform to a query bundle before passing it to a query engine.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_engine`  |   |  A query engine object.  |  _required_  |  
|  `query_transform`  |  `BaseQueryTransform`  |  A query transform object.  |  _required_  |  
|  `transform_metadata`  |  `Optional[dict]`  |  metadata to pass to the query transform.  |  `None`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  A callback manager.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/query_engine/transform_query_engine.py`  
| 
```
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
```
 | 
```
classTransformQueryEngine(BaseQueryEngine):
"""
    Transform query engine.

    Applies a query transform to a query bundle before passing
        it to a query engine.

    Args:
        query_engine (BaseQueryEngine): A query engine object.
        query_transform (BaseQueryTransform): A query transform object.
        transform_metadata (Optional[dict]): metadata to pass to the
            query transform.
        callback_manager (Optional[CallbackManager]): A callback manager.

    """

    def__init__(
        self,
        query_engine: BaseQueryEngine,
        query_transform: BaseQueryTransform,
        transform_metadata: Optional[dict] = None,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        self._query_engine = query_engine
        self._query_transform = query_transform
        self._transform_metadata = transform_metadata
        super().__init__(callback_manager)

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {
            "query_transform": self._query_transform,
            "query_engine": self._query_engine,
        }

    defretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        query_bundle = self._query_transform.run(
            query_bundle, metadata=self._transform_metadata
        )
        return self._query_engine.retrieve(query_bundle)

    defsynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        query_bundle = self._query_transform.run(
            query_bundle, metadata=self._transform_metadata
        )
        return self._query_engine.synthesize(
            query_bundle=query_bundle,
            nodes=nodes,
            additional_source_nodes=additional_source_nodes,
        )

    async defasynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        query_bundle = self._query_transform.run(
            query_bundle, metadata=self._transform_metadata
        )
        return await self._query_engine.asynthesize(
            query_bundle=query_bundle,
            nodes=nodes,
            additional_source_nodes=additional_source_nodes,
        )

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        query_bundle = self._query_transform.run(
            query_bundle, metadata=self._transform_metadata
        )
        return self._query_engine.query(query_bundle)

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        query_bundle = self._query_transform.run(
            query_bundle, metadata=self._transform_metadata
        )
        return await self._query_engine.aquery(query_bundle)

```
 |  
| --- | --- |  
options: members: - NLSQLTableQueryEngine
