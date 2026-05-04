# Index
##  ToolSelection [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.ToolSelection "Permanent link")
Bases: `BaseModel`
Tool selection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `tool_id`  |  Tool ID to select.  |  _required_  |  
|  `tool_name`  |  Tool name to select.  |  _required_  |  
|  `tool_kwargs`  |  `Dict[str, Any]`  |  Keyword arguments for the tool.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/llms/llm.py`  
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
```
 | 
```
classToolSelection(BaseModel):
"""Tool selection."""

    tool_id: str = Field(description="Tool ID to select.")
    tool_name: str = Field(description="Tool name to select.")
    tool_kwargs: Dict[str, Any] = Field(description="Keyword arguments for the tool.")

    @field_validator("tool_kwargs", mode="wrap")
    @classmethod
    defignore_non_dict_arguments(cls, v: Any, handler: Any) -> Dict[str, Any]:
        try:
            return handler(v)
        except ValidationError:
            return handler({})

```
 |  
| --- | --- |  
##  LLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "Permanent link")
Bases: `BaseLLM`
The LLM class is the main class for interacting with language models.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `system_prompt`  |  `str | None`  |  System prompt for LLM calls.  |  `None`  |  
|  `messages_to_prompt`  |  `MessagesToPromptType | None`  |  Function to convert a list of messages to an LLM prompt.  |  `None`  |  
|  `completion_to_prompt`  |  `CompletionToPromptType | None`  |  Function to convert a completion to an LLM prompt.  |  `None`  |  
|  `output_parser`  |  `BaseOutputParser[](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BaseOutputParser "BaseOutputParser \(llama_index.core.types.BaseOutputParser\)") | None`  |  Output parser to parse, validate, and correct errors programmatically.  |  `None`  |  
|  `pydantic_program_mode`  |   |  `<PydanticProgramMode.DEFAULT: 'default'>`  |  
|  `query_wrapper_prompt`  |  `BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)") | None`  |  Query wrapper prompt for LLM calls.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/llms/llm.py`  
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
537
538
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
596
597
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
645
646
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
664
665
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
683
684
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
705
706
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
729
730
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
753
754
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
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
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
858
859
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
885
886
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
936
937
938
939
940
941
942
943
944
945
946
```
 | 
```
classLLM(BaseLLM):
"""
    The LLM class is the main class for interacting with language models.

    Attributes:
        system_prompt (Optional[str]):
            System prompt for LLM calls.
        messages_to_prompt (Callable):
            Function to convert a list of messages to an LLM prompt.
        completion_to_prompt (Callable):
            Function to convert a completion to an LLM prompt.
        output_parser (Optional[BaseOutputParser]):
            Output parser to parse, validate, and correct errors programmatically.
        pydantic_program_mode (PydanticProgramMode):
            Pydantic program mode to use for structured prediction.

    """

    system_prompt: Optional[str] = Field(
        default=None, description="System prompt for LLM calls."
    )
    messages_to_prompt: MessagesToPromptCallable = Field(
        description="Function to convert a list of messages to an LLM prompt.",
        default=None,
        exclude=True,
    )
    completion_to_prompt: CompletionToPromptCallable = Field(
        description="Function to convert a completion to an LLM prompt.",
        default=None,
        exclude=True,
    )
    output_parser: Optional[BaseOutputParser] = Field(
        description="Output parser to parse, validate, and correct errors programmatically.",
        default=None,
        exclude=True,
    )
    pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT

    # deprecated
    query_wrapper_prompt: Optional[BasePromptTemplate] = Field(
        description="Query wrapper prompt for LLM calls.",
        default=None,
        exclude=True,
    )

    # -- Pydantic Configs --

    @field_validator("messages_to_prompt")
    @classmethod
    defset_messages_to_prompt(
        cls, messages_to_prompt: Optional[MessagesToPromptType]
    ) -> MessagesToPromptType:
        return messages_to_prompt or generic_messages_to_prompt

    @field_validator("completion_to_prompt")
    @classmethod
    defset_completion_to_prompt(
        cls, completion_to_prompt: Optional[CompletionToPromptType]
    ) -> CompletionToPromptType:
        return completion_to_prompt or default_completion_to_prompt

    @model_validator(mode="after")
    defcheck_prompts(self) -> "LLM":
        if self.completion_to_prompt is None:
            self.completion_to_prompt = default_completion_to_prompt
        if self.messages_to_prompt is None:
            self.messages_to_prompt = generic_messages_to_prompt
        return self

    # -- Utils --

    def_log_template_data(
        self, prompt: BasePromptTemplate, **prompt_args: Any
    ) -> None:
        template_vars = {
            k: v
            for k, v in ChainMap(prompt.kwargs, prompt_args).items()
            if k in prompt.template_vars
        }
        with self.callback_manager.event(
            CBEventType.TEMPLATING,
            payload={
                EventPayload.TEMPLATE: prompt.get_template(llm=self),
                EventPayload.TEMPLATE_VARS: template_vars,
                EventPayload.SYSTEM_PROMPT: self.system_prompt,
                EventPayload.QUERY_WRAPPER_PROMPT: self.query_wrapper_prompt,
            },
        ):
            pass

    def_get_prompt(self, prompt: BasePromptTemplate, **prompt_args: Any) -> str:
        formatted_prompt = prompt.format(
            llm=self,
            messages_to_prompt=self.messages_to_prompt,
            completion_to_prompt=self.completion_to_prompt,
            **prompt_args,
        )
        if self.output_parser is not None:
            formatted_prompt = self.output_parser.format(formatted_prompt)
        return self._extend_prompt(formatted_prompt)

    def_get_messages(
        self, prompt: BasePromptTemplate, **prompt_args: Any
    ) -> List[ChatMessage]:
        messages = prompt.format_messages(llm=self, **prompt_args)
        if self.output_parser is not None:
            messages = self.output_parser.format_messages(messages)
        return self._extend_messages(messages)

    def_parse_output(self, output: str) -> str:
        if self.output_parser is not None:
            return str(self.output_parser.parse(output))

        return output

    def_extend_prompt(
        self,
        formatted_prompt: str,
    ) -> str:
"""Add system and query wrapper prompts to base prompt."""
        extended_prompt = formatted_prompt

        if self.system_prompt:
            extended_prompt = self.system_prompt + "\n\n" + extended_prompt

        if self.query_wrapper_prompt:
            extended_prompt = self.query_wrapper_prompt.format(
                query_str=extended_prompt
            )

        return extended_prompt

    def_extend_messages(self, messages: List[ChatMessage]) -> List[ChatMessage]:
"""Add system prompt to chat message list."""
        if self.system_prompt:
            messages = [
                ChatMessage(role=MessageRole.SYSTEM, content=self.system_prompt),
                *messages,
            ]
        return messages

    # -- Structured outputs --

    @dispatcher.span
    defstructured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
r"""
        Structured predict.

        Args:
            output_cls (BaseModel):
                Output class to use for structured prediction.
            prompt (PromptTemplate):
                Prompt template to use for structured prediction.
            llm_kwargs (Optional[Dict[str, Any]]):
                Arguments that are passed down to the LLM invoked by the program.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            BaseModel: The structured prediction output.

        Examples:
            ```python
            from pydantic import BaseModel

            class Test(BaseModel):
                \"\"\"My test class.\"\"\"
                name: str

            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
            output = llm.structured_predict(Test, prompt, topic="cats")
            print(output.name)


        """
        fromllama_index.core.program.utilsimport get_program_for_llm

        dispatcher.event(
            LLMStructuredPredictStartEvent(
                output_cls=output_cls, template=prompt, template_args=prompt_args
            )
        )
        program = get_program_for_llm(
            output_cls,
            prompt,
            self,
            pydantic_program_mode=self.pydantic_program_mode,
        )

        result = program(llm_kwargs=llm_kwargs, **prompt_args)
        assert not isinstance(result, list)

        if not isinstance(result, BaseModel):
            raise TypeError(
                f"structured_predict expected a {output_cls.__name__} instance "
                f"but got {type(result).__name__}: {result!r}. "
                f"The LLM failed to produce valid structured output."
            )

        dispatcher.event(LLMStructuredPredictEndEvent(output=result))
        return result

    @dispatcher.span
    async defastructured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
r"""
        Async Structured predict.

        Args:
            output_cls (BaseModel):
                Output class to use for structured prediction.
            prompt (PromptTemplate):
                Prompt template to use for structured prediction.
            llm_kwargs (Optional[Dict[str, Any]]):
                Arguments that are passed down to the LLM invoked by the program.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            BaseModel: The structured prediction output.

        Examples:
            ```python
            from pydantic import BaseModel

            class Test(BaseModel):
                \"\"\"My test class.\"\"\"
                name: str

            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
            output = await llm.astructured_predict(Test, prompt, topic="cats")
            print(output.name)


        """
        fromllama_index.core.program.utilsimport get_program_for_llm

        dispatcher.event(
            LLMStructuredPredictStartEvent(
                output_cls=output_cls, template=prompt, template_args=prompt_args
            )
        )

        program = get_program_for_llm(
            output_cls,
            prompt,
            self,
            pydantic_program_mode=self.pydantic_program_mode,
        )

        result = await program.acall(llm_kwargs=llm_kwargs, **prompt_args)
        assert not isinstance(result, list)

        if not isinstance(result, BaseModel):
            raise TypeError(
                f"astructured_predict expected a {output_cls.__name__} instance "
                f"but got {type(result).__name__}: {result!r}. "
                f"The LLM failed to produce valid structured output."
            )

        dispatcher.event(LLMStructuredPredictEndEvent(output=result))
        return result

    def_structured_stream_call(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Generator[
        Union[Model, List[Model], "FlexibleModel", List["FlexibleModel"]], None, None
    ]:
        fromllama_index.core.program.utilsimport get_program_for_llm

        program = get_program_for_llm(
            output_cls,
            prompt,
            self,
            pydantic_program_mode=self.pydantic_program_mode,
        )
        return program.stream_call(llm_kwargs=llm_kwargs, **prompt_args)

    @dispatcher.span
    defstream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Generator[Union[Model, "FlexibleModel"], None, None]:
r"""
        Stream Structured predict.

        Args:
            output_cls (BaseModel):
                Output class to use for structured prediction.
            prompt (PromptTemplate):
                Prompt template to use for structured prediction.
            llm_kwargs (Optional[Dict[str, Any]]):
                Arguments that are passed down to the LLM invoked by the program.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            Generator: A generator returning partial copies of the model or list of models.

        Examples:
            ```python
            from pydantic import BaseModel

            class Test(BaseModel):
                \"\"\"My test class.\"\"\"
                name: str

            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
            stream_output = llm.stream_structured_predict(Test, prompt, topic="cats")
            for partial_output in stream_output:
                # stream partial outputs until completion
                print(partial_output.name)


        """
        dispatcher.event(
            LLMStructuredPredictStartEvent(
                output_cls=output_cls, template=prompt, template_args=prompt_args
            )
        )

        result = self._structured_stream_call(
            output_cls, prompt, llm_kwargs, **prompt_args
        )
        for r in result:
            dispatcher.event(LLMStructuredPredictInProgressEvent(output=r))
            assert not isinstance(r, list)
            yield r

        dispatcher.event(LLMStructuredPredictEndEvent(output=r))

    async def_structured_astream_call(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> AsyncGenerator[
        Union[Model, List[Model], "FlexibleModel", List["FlexibleModel"]], None
    ]:
        fromllama_index.core.program.utilsimport get_program_for_llm

        program = get_program_for_llm(
            output_cls,
            prompt,
            self,
            pydantic_program_mode=self.pydantic_program_mode,
        )

        return await program.astream_call(llm_kwargs=llm_kwargs, **prompt_args)

    @dispatcher.span
    async defastream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> AsyncGenerator[Union[Model, "FlexibleModel"], None]:
r"""
        Async Stream Structured predict.

        Args:
            output_cls (BaseModel):
                Output class to use for structured prediction.
            prompt (PromptTemplate):
                Prompt template to use for structured prediction.
            llm_kwargs (Optional[Dict[str, Any]]):
                Arguments that are passed down to the LLM invoked by the program.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            Generator: A generator returning partial copies of the model or list of models.

        Examples:
            ```python
            from pydantic import BaseModel

            class Test(BaseModel):
                \"\"\"My test class.\"\"\"
                name: str

            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
            stream_output = await llm.astream_structured_predict(Test, prompt, topic="cats")
            async for partial_output in stream_output:
                # stream partial outputs until completion
                print(partial_output.name)


        """

        async defgen() -> AsyncGenerator[Union[Model, "FlexibleModel"], None]:
            dispatcher.event(
                LLMStructuredPredictStartEvent(
                    output_cls=output_cls, template=prompt, template_args=prompt_args
                )
            )

            result = await self._structured_astream_call(
                output_cls, prompt, llm_kwargs, **prompt_args
            )
            async for r in result:
                dispatcher.event(LLMStructuredPredictInProgressEvent(output=r))
                assert not isinstance(r, list)
                yield r

            dispatcher.event(LLMStructuredPredictEndEvent(output=r))

        return gen()

    # -- Prompt Chaining --

    @dispatcher.span
    defpredict(
        self,
        prompt: BasePromptTemplate,
        **prompt_args: Any,
    ) -> str:
"""
        Predict for a given prompt.

        Args:
            prompt (BasePromptTemplate):
                The prompt to use for prediction.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            str: The prediction output.

        Examples:
            ```python
            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please write a random name related to {topic}.")
            output = llm.predict(prompt, topic="cats")
            print(output)


        """
        dispatcher.event(
            LLMPredictStartEvent(template=prompt, template_args=prompt_args)
        )
        self._log_template_data(prompt, **prompt_args)

        if self.metadata.is_chat_model:
            messages = self._get_messages(prompt, **prompt_args)
            chat_response = self.chat(messages)
            output = chat_response.message.content or ""
        else:
            formatted_prompt = self._get_prompt(prompt, **prompt_args)
            response = self.complete(formatted_prompt, formatted=True)
            output = response.text
        parsed_output = self._parse_output(output)
        dispatcher.event(LLMPredictEndEvent(output=parsed_output))
        return parsed_output

    @dispatcher.span
    defstream(
        self,
        prompt: BasePromptTemplate,
        **prompt_args: Any,
    ) -> TokenGen:
"""
        Stream predict for a given prompt.

        Args:
            prompt (BasePromptTemplate):
                The prompt to use for prediction.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Yields:
            str: Each streamed token.

        Examples:
            ```python
            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please write a random name related to {topic}.")
            gen = llm.stream(prompt, topic="cats")
            for token in gen:
                print(token, end="", flush=True)


        """
        self._log_template_data(prompt, **prompt_args)

        dispatcher.event(
            LLMPredictStartEvent(template=prompt, template_args=prompt_args)
        )
        if self.metadata.is_chat_model:
            messages = self._get_messages(prompt, **prompt_args)
            chat_response = self.stream_chat(messages)
            stream_tokens = stream_chat_response_to_tokens(chat_response)
        else:
            formatted_prompt = self._get_prompt(prompt, **prompt_args)
            stream_response = self.stream_complete(formatted_prompt, formatted=True)
            stream_tokens = stream_completion_response_to_tokens(stream_response)

        if prompt.output_parser is not None or self.output_parser is not None:
            raise NotImplementedError("Output parser is not supported for streaming.")

        return stream_tokens

    @dispatcher.span
    async defapredict(
        self,
        prompt: BasePromptTemplate,
        **prompt_args: Any,
    ) -> str:
"""
        Async Predict for a given prompt.

        Args:
            prompt (BasePromptTemplate):
                The prompt to use for prediction.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            str: The prediction output.

        Examples:
            ```python
            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please write a random name related to {topic}.")
            output = await llm.apredict(prompt, topic="cats")
            print(output)


        """
        dispatcher.event(
            LLMPredictStartEvent(template=prompt, template_args=prompt_args)
        )
        self._log_template_data(prompt, **prompt_args)

        if self.metadata.is_chat_model:
            messages = self._get_messages(prompt, **prompt_args)
            chat_response = await self.achat(messages)
            output = chat_response.message.content or ""
        else:
            formatted_prompt = self._get_prompt(prompt, **prompt_args)
            response = await self.acomplete(formatted_prompt, formatted=True)
            output = response.text

        parsed_output = self._parse_output(output)
        dispatcher.event(LLMPredictEndEvent(output=parsed_output))
        return parsed_output

    @dispatcher.span
    async defastream(
        self,
        prompt: BasePromptTemplate,
        **prompt_args: Any,
    ) -> TokenAsyncGen:
"""
        Async stream predict for a given prompt.

        Args:
        prompt (BasePromptTemplate):
            The prompt to use for prediction.
        prompt_args (Any):
            Additional arguments to format the prompt with.

        Yields:
            str: An async generator that yields strings of tokens.

        Examples:
            ```python
            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please write a random name related to {topic}.")
            gen = await llm.astream(prompt, topic="cats")
            async for token in gen:
                print(token, end="", flush=True)


        """
        self._log_template_data(prompt, **prompt_args)

        dispatcher.event(
            LLMPredictStartEvent(template=prompt, template_args=prompt_args)
        )
        if self.metadata.is_chat_model:
            messages = self._get_messages(prompt, **prompt_args)
            chat_response = await self.astream_chat(messages)
            stream_tokens = await astream_chat_response_to_tokens(chat_response)
        else:
            formatted_prompt = self._get_prompt(prompt, **prompt_args)
            stream_response = await self.astream_complete(
                formatted_prompt, formatted=True
            )
            stream_tokens = await astream_completion_response_to_tokens(stream_response)

        if prompt.output_parser is not None or self.output_parser is not None:
            raise NotImplementedError("Output parser is not supported for streaming.")

        return stream_tokens

    @dispatcher.span
    defpredict_and_call(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> "AgentChatResponse":
"""
        Predict and call the tool.

        By default uses a ReAct agent to do tool calling (through text prompting),
        but function calling LLMs will implement this differently.

        """
        fromllama_index.core.agent.workflowimport ReActAgent
        fromllama_index.core.agent.workflow.agent_contextimport SimpleAgentContext
        fromllama_index.core.chat_engine.typesimport AgentChatResponse
        fromllama_index.core.memoryimport Memory
        fromllama_index.core.toolsimport adapt_to_async_tool
        fromllama_index.core.tools.callingimport call_tool_with_selection

        agent = ReActAgent(
            tools=tools,
            llm=self,
            verbose=verbose,
            formatter=kwargs.get("react_chat_formatter"),
            output_parser=kwargs.get("output_parser"),
            tool_retriever=kwargs.get("tool_retriever"),
        )

        memory = kwargs.get("memory", Memory.from_defaults())

        if isinstance(user_msg, ChatMessage) and isinstance(user_msg.content, str):
            pass
        elif isinstance(user_msg, str):
            user_msg = ChatMessage(content=user_msg, role=MessageRole.USER)

        llm_input = []
        if chat_history:
            llm_input.extend(chat_history)
        if user_msg:
            llm_input.append(user_msg)

        ctx = SimpleAgentContext()
        async_tools = [adapt_to_async_tool(t) for t in (tools or [])]

        try:
            resp = asyncio_run(
                agent.take_step(
                    ctx=ctx, llm_input=llm_input, tools=async_tools, memory=memory
                )
            )
            tool_outputs = []
            for tool_call in resp.tool_calls:
                tool_output = call_tool_with_selection(
                    tool_call=tool_call,
                    tools=tools or [],
                    verbose=verbose,
                )
                tool_outputs.append(tool_output)
            output_text = "\n\n".join(
                [tool_output.content for tool_output in tool_outputs]
            )
            return AgentChatResponse(
                response=output_text,
                sources=tool_outputs,
            )
        except Exception as e:
            output = AgentChatResponse(
                response="An error occurred while running the tool: " + str(e),
                sources=[],
            )

        return output

    @dispatcher.span
    async defapredict_and_call(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> "AgentChatResponse":
"""Predict and call the tool."""
        fromllama_index.core.agent.workflowimport ReActAgent
        fromllama_index.core.agent.workflow.agent_contextimport SimpleAgentContext
        fromllama_index.core.chat_engine.typesimport AgentChatResponse
        fromllama_index.core.memoryimport Memory
        fromllama_index.core.toolsimport adapt_to_async_tool
        fromllama_index.core.tools.callingimport acall_tool_with_selection

        agent = ReActAgent(
            tools=tools,
            llm=self,
            verbose=verbose,
            formatter=kwargs.get("react_chat_formatter"),
            output_parser=kwargs.get("output_parser"),
            tool_retriever=kwargs.get("tool_retriever"),
        )

        memory = kwargs.get("memory", Memory.from_defaults())

        if isinstance(user_msg, ChatMessage) and isinstance(user_msg.content, str):
            pass
        elif isinstance(user_msg, str):
            user_msg = ChatMessage(content=user_msg, role=MessageRole.USER)

        llm_input = []
        if chat_history:
            llm_input.extend(chat_history)
        if user_msg:
            llm_input.append(user_msg)

        ctx = SimpleAgentContext()
        async_tools = [adapt_to_async_tool(t) for t in (tools or [])]

        try:
            resp = await agent.take_step(
                ctx=ctx, llm_input=llm_input, tools=async_tools, memory=memory
            )
            tool_outputs = []
            for tool_call in resp.tool_calls:
                tool_output = await acall_tool_with_selection(
                    tool_call=tool_call,
                    tools=tools or [],
                    verbose=verbose,
                )
                tool_outputs.append(tool_output)

            output_text = "\n\n".join(
                [tool_output.content for tool_output in tool_outputs]
            )
            return AgentChatResponse(
                response=output_text,
                sources=tool_outputs,
            )
        except Exception as e:
            output = AgentChatResponse(
                response="An error occurred while running the tool: " + str(e),
                sources=[],
            )

        return output

    defas_structured_llm(
        self,
        output_cls: Type[BaseModel],
        **kwargs: Any,
    ) -> "StructuredLLM":
"""Return a structured LLM around a given object."""
        fromllama_index.core.llms.structured_llmimport StructuredLLM

        return StructuredLLM(llm=self, output_cls=output_cls, **kwargs)

```
 |  
| --- | --- |  
###  structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.structured_predict "Permanent link")

```
structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> 

```

Structured predict.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `output_cls`  |  `BaseModel`  |  Output class to use for structured prediction.  |  _required_  |  
|  `prompt`  |   |  Prompt template to use for structured prediction.  |  _required_  |  
|  `llm_kwargs`  |  `Optional[Dict[str, Any]]`  |  Arguments that are passed down to the LLM invoked by the program.  |  `None`  |  
|  `prompt_args`  |  Additional arguments to format the prompt with.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `BaseModel`  |  `Model`  |  The structured prediction output.  |  
Examples:

```
frompydanticimport BaseModel

classTest(BaseModel):
    \"\"\"My test class.\"\"\"
    name: str

fromllama_index.core.promptsimport PromptTemplate

prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
output = llm.structured_predict(Test, prompt, topic="cats")
print(output.name)

```

Source code in `llama-index-core/llama_index/core/llms/llm.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defstructured_predict(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> Model:
r"""
    Structured predict.

    Args:
        output_cls (BaseModel):
            Output class to use for structured prediction.
        prompt (PromptTemplate):
            Prompt template to use for structured prediction.
        llm_kwargs (Optional[Dict[str, Any]]):
            Arguments that are passed down to the LLM invoked by the program.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Returns:
        BaseModel: The structured prediction output.

    Examples:
        ```python
        from pydantic import BaseModel

        class Test(BaseModel):
            \"\"\"My test class.\"\"\"
            name: str

        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
        output = llm.structured_predict(Test, prompt, topic="cats")
        print(output.name)
        ```

    """
    fromllama_index.core.program.utilsimport get_program_for_llm

    dispatcher.event(
        LLMStructuredPredictStartEvent(
            output_cls=output_cls, template=prompt, template_args=prompt_args
        )
    )
    program = get_program_for_llm(
        output_cls,
        prompt,
        self,
        pydantic_program_mode=self.pydantic_program_mode,
    )

    result = program(llm_kwargs=llm_kwargs, **prompt_args)
    assert not isinstance(result, list)

    if not isinstance(result, BaseModel):
        raise TypeError(
            f"structured_predict expected a {output_cls.__name__} instance "
            f"but got {type(result).__name__}: {result!r}. "
            f"The LLM failed to produce valid structured output."
        )

    dispatcher.event(LLMStructuredPredictEndEvent(output=result))
    return result

```
 |  
| --- | --- |  
###  astructured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.astructured_predict "Permanent link")

```
astructured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> 

```

Async Structured predict.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `output_cls`  |  `BaseModel`  |  Output class to use for structured prediction.  |  _required_  |  
|  `prompt`  |   |  Prompt template to use for structured prediction.  |  _required_  |  
|  `llm_kwargs`  |  `Optional[Dict[str, Any]]`  |  Arguments that are passed down to the LLM invoked by the program.  |  `None`  |  
|  `prompt_args`  |  Additional arguments to format the prompt with.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `BaseModel`  |  `Model`  |  The structured prediction output.  |  
Examples:

```
frompydanticimport BaseModel

classTest(BaseModel):
    \"\"\"My test class.\"\"\"
    name: str

fromllama_index.core.promptsimport PromptTemplate

prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
output = await llm.astructured_predict(Test, prompt, topic="cats")
print(output.name)

```

Source code in `llama-index-core/llama_index/core/llms/llm.py`  
| 
```
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
```
 | 
```
@dispatcher.span
async defastructured_predict(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> Model:
r"""
    Async Structured predict.

    Args:
        output_cls (BaseModel):
            Output class to use for structured prediction.
        prompt (PromptTemplate):
            Prompt template to use for structured prediction.
        llm_kwargs (Optional[Dict[str, Any]]):
            Arguments that are passed down to the LLM invoked by the program.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Returns:
        BaseModel: The structured prediction output.

    Examples:
        ```python
        from pydantic import BaseModel

        class Test(BaseModel):
            \"\"\"My test class.\"\"\"
            name: str

        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
        output = await llm.astructured_predict(Test, prompt, topic="cats")
        print(output.name)
        ```

    """
    fromllama_index.core.program.utilsimport get_program_for_llm

    dispatcher.event(
        LLMStructuredPredictStartEvent(
            output_cls=output_cls, template=prompt, template_args=prompt_args
        )
    )

    program = get_program_for_llm(
        output_cls,
        prompt,
        self,
        pydantic_program_mode=self.pydantic_program_mode,
    )

    result = await program.acall(llm_kwargs=llm_kwargs, **prompt_args)
    assert not isinstance(result, list)

    if not isinstance(result, BaseModel):
        raise TypeError(
            f"astructured_predict expected a {output_cls.__name__} instance "
            f"but got {type(result).__name__}: {result!r}. "
            f"The LLM failed to produce valid structured output."
        )

    dispatcher.event(LLMStructuredPredictEndEvent(output=result))
    return result

```
 |  
| --- | --- |  
###  stream_structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.stream_structured_predict "Permanent link")

```
stream_structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> Generator[Union[, FlexibleModel], None, None]

```

Stream Structured predict.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `output_cls`  |  `BaseModel`  |  Output class to use for structured prediction.  |  _required_  |  
|  `prompt`  |   |  Prompt template to use for structured prediction.  |  _required_  |  
|  `llm_kwargs`  |  `Optional[Dict[str, Any]]`  |  Arguments that are passed down to the LLM invoked by the program.  |  `None`  |  
|  `prompt_args`  |  Additional arguments to format the prompt with.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Generator`  |  `None`  |  A generator returning partial copies of the model or list of models.  |  
Examples:

```
frompydanticimport BaseModel

classTest(BaseModel):
    \"\"\"My test class.\"\"\"
    name: str

fromllama_index.core.promptsimport PromptTemplate

prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
stream_output = llm.stream_structured_predict(Test, prompt, topic="cats")
for partial_output in stream_output:
    # stream partial outputs until completion
    print(partial_output.name)

```

Source code in `llama-index-core/llama_index/core/llms/llm.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defstream_structured_predict(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> Generator[Union[Model, "FlexibleModel"], None, None]:
r"""
    Stream Structured predict.

    Args:
        output_cls (BaseModel):
            Output class to use for structured prediction.
        prompt (PromptTemplate):
            Prompt template to use for structured prediction.
        llm_kwargs (Optional[Dict[str, Any]]):
            Arguments that are passed down to the LLM invoked by the program.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Returns:
        Generator: A generator returning partial copies of the model or list of models.

    Examples:
        ```python
        from pydantic import BaseModel

        class Test(BaseModel):
            \"\"\"My test class.\"\"\"
            name: str

        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
        stream_output = llm.stream_structured_predict(Test, prompt, topic="cats")
        for partial_output in stream_output:
            # stream partial outputs until completion
            print(partial_output.name)
        ```

    """
    dispatcher.event(
        LLMStructuredPredictStartEvent(
            output_cls=output_cls, template=prompt, template_args=prompt_args
        )
    )

    result = self._structured_stream_call(
        output_cls, prompt, llm_kwargs, **prompt_args
    )
    for r in result:
        dispatcher.event(LLMStructuredPredictInProgressEvent(output=r))
        assert not isinstance(r, list)
        yield r

    dispatcher.event(LLMStructuredPredictEndEvent(output=r))

```
 |  
| --- | --- |  
###  astream_structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.astream_structured_predict "Permanent link")

```
astream_structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> AsyncGenerator[Union[, FlexibleModel], None]

```

Async Stream Structured predict.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `output_cls`  |  `BaseModel`  |  Output class to use for structured prediction.  |  _required_  |  
|  `prompt`  |   |  Prompt template to use for structured prediction.  |  _required_  |  
|  `llm_kwargs`  |  `Optional[Dict[str, Any]]`  |  Arguments that are passed down to the LLM invoked by the program.  |  `None`  |  
|  `prompt_args`  |  Additional arguments to format the prompt with.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Generator`  |  `AsyncGenerator[Union[Model, FlexibleModel], None]`  |  A generator returning partial copies of the model or list of models.  |  
Examples:

```
frompydanticimport BaseModel

classTest(BaseModel):
    \"\"\"My test class.\"\"\"
    name: str

fromllama_index.core.promptsimport PromptTemplate

prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
stream_output = await llm.astream_structured_predict(Test, prompt, topic="cats")
async for partial_output in stream_output:
    # stream partial outputs until completion
    print(partial_output.name)

```

Source code in `llama-index-core/llama_index/core/llms/llm.py`  
| 
```
538
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
596
597
598
```
 | 
```
@dispatcher.span
async defastream_structured_predict(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> AsyncGenerator[Union[Model, "FlexibleModel"], None]:
r"""
    Async Stream Structured predict.

    Args:
        output_cls (BaseModel):
            Output class to use for structured prediction.
        prompt (PromptTemplate):
            Prompt template to use for structured prediction.
        llm_kwargs (Optional[Dict[str, Any]]):
            Arguments that are passed down to the LLM invoked by the program.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Returns:
        Generator: A generator returning partial copies of the model or list of models.

    Examples:
        ```python
        from pydantic import BaseModel

        class Test(BaseModel):
            \"\"\"My test class.\"\"\"
            name: str

        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
        stream_output = await llm.astream_structured_predict(Test, prompt, topic="cats")
        async for partial_output in stream_output:
            # stream partial outputs until completion
            print(partial_output.name)
        ```

    """

    async defgen() -> AsyncGenerator[Union[Model, "FlexibleModel"], None]:
        dispatcher.event(
            LLMStructuredPredictStartEvent(
                output_cls=output_cls, template=prompt, template_args=prompt_args
            )
        )

        result = await self._structured_astream_call(
            output_cls, prompt, llm_kwargs, **prompt_args
        )
        async for r in result:
            dispatcher.event(LLMStructuredPredictInProgressEvent(output=r))
            assert not isinstance(r, list)
            yield r

        dispatcher.event(LLMStructuredPredictEndEvent(output=r))

    return gen()

```
 |  
| --- | --- |  
###  predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.predict "Permanent link")

```
predict(
    prompt: , **prompt_args: 
) -> 

```

Predict for a given prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |   |  The prompt to use for prediction.  |  _required_  |  
|  `prompt_args`  |  Additional arguments to format the prompt with.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The prediction output.  |  
Examples:

```
fromllama_index.core.promptsimport PromptTemplate

prompt = PromptTemplate("Please write a random name related to {topic}.")
output = llm.predict(prompt, topic="cats")
print(output)

```

Source code in `llama-index-core/llama_index/core/llms/llm.py`  
| 
```
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
645
```
 | 
```
@dispatcher.span
defpredict(
    self,
    prompt: BasePromptTemplate,
    **prompt_args: Any,
) -> str:
"""
    Predict for a given prompt.

    Args:
        prompt (BasePromptTemplate):
            The prompt to use for prediction.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Returns:
        str: The prediction output.

    Examples:
        ```python
        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please write a random name related to {topic}.")
        output = llm.predict(prompt, topic="cats")
        print(output)
        ```

    """
    dispatcher.event(
        LLMPredictStartEvent(template=prompt, template_args=prompt_args)
    )
    self._log_template_data(prompt, **prompt_args)

    if self.metadata.is_chat_model:
        messages = self._get_messages(prompt, **prompt_args)
        chat_response = self.chat(messages)
        output = chat_response.message.content or ""
    else:
        formatted_prompt = self._get_prompt(prompt, **prompt_args)
        response = self.complete(formatted_prompt, formatted=True)
        output = response.text
    parsed_output = self._parse_output(output)
    dispatcher.event(LLMPredictEndEvent(output=parsed_output))
    return parsed_output

```
 |  
| --- | --- |  
###  stream [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.stream "Permanent link")

```
stream(
    prompt: , **prompt_args: 
) -> TokenGen

```

Stream predict for a given prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |   |  The prompt to use for prediction.  |  _required_  |  
|  `prompt_args`  |  Additional arguments to format the prompt with.  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  `TokenGen`  |  Each streamed token.  |  
Examples:

```
fromllama_index.core.promptsimport PromptTemplate

prompt = PromptTemplate("Please write a random name related to {topic}.")
gen = llm.stream(prompt, topic="cats")
for token in gen:
    print(token, end="", flush=True)

```

Source code in `llama-index-core/llama_index/core/llms/llm.py`  
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
664
665
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
683
684
685
686
687
688
689
690
691
692
693
```
 | 
```
@dispatcher.span
defstream(
    self,
    prompt: BasePromptTemplate,
    **prompt_args: Any,
) -> TokenGen:
"""
    Stream predict for a given prompt.

    Args:
        prompt (BasePromptTemplate):
            The prompt to use for prediction.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Yields:
        str: Each streamed token.

    Examples:
        ```python
        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please write a random name related to {topic}.")
        gen = llm.stream(prompt, topic="cats")
        for token in gen:
            print(token, end="", flush=True)
        ```

    """
    self._log_template_data(prompt, **prompt_args)

    dispatcher.event(
        LLMPredictStartEvent(template=prompt, template_args=prompt_args)
    )
    if self.metadata.is_chat_model:
        messages = self._get_messages(prompt, **prompt_args)
        chat_response = self.stream_chat(messages)
        stream_tokens = stream_chat_response_to_tokens(chat_response)
    else:
        formatted_prompt = self._get_prompt(prompt, **prompt_args)
        stream_response = self.stream_complete(formatted_prompt, formatted=True)
        stream_tokens = stream_completion_response_to_tokens(stream_response)

    if prompt.output_parser is not None or self.output_parser is not None:
        raise NotImplementedError("Output parser is not supported for streaming.")

    return stream_tokens

```
 |  
| --- | --- |  
###  apredict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.apredict "Permanent link")

```
apredict(
    prompt: , **prompt_args: 
) -> 

```

Async Predict for a given prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |   |  The prompt to use for prediction.  |  _required_  |  
|  `prompt_args`  |  Additional arguments to format the prompt with.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The prediction output.  |  
Examples:

```
fromllama_index.core.promptsimport PromptTemplate

prompt = PromptTemplate("Please write a random name related to {topic}.")
output = await llm.apredict(prompt, topic="cats")
print(output)

```

Source code in `llama-index-core/llama_index/core/llms/llm.py`  
| 
```
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
705
706
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
729
730
731
732
733
734
735
736
737
738
739
```
 | 
```
@dispatcher.span
async defapredict(
    self,
    prompt: BasePromptTemplate,
    **prompt_args: Any,
) -> str:
"""
    Async Predict for a given prompt.

    Args:
        prompt (BasePromptTemplate):
            The prompt to use for prediction.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Returns:
        str: The prediction output.

    Examples:
        ```python
        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please write a random name related to {topic}.")
        output = await llm.apredict(prompt, topic="cats")
        print(output)
        ```

    """
    dispatcher.event(
        LLMPredictStartEvent(template=prompt, template_args=prompt_args)
    )
    self._log_template_data(prompt, **prompt_args)

    if self.metadata.is_chat_model:
        messages = self._get_messages(prompt, **prompt_args)
        chat_response = await self.achat(messages)
        output = chat_response.message.content or ""
    else:
        formatted_prompt = self._get_prompt(prompt, **prompt_args)
        response = await self.acomplete(formatted_prompt, formatted=True)
        output = response.text

    parsed_output = self._parse_output(output)
    dispatcher.event(LLMPredictEndEvent(output=parsed_output))
    return parsed_output

```
 |  
| --- | --- |  
###  astream [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.astream "Permanent link")

```
astream(
    prompt: , **prompt_args: 
) -> TokenAsyncGen

```

Async stream predict for a given prompt.
prompt (BasePromptTemplate): The prompt to use for prediction. prompt_args (Any): Additional arguments to format the prompt with.
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  `TokenAsyncGen`  |  An async generator that yields strings of tokens.  |  
Examples:

```
fromllama_index.core.promptsimport PromptTemplate

prompt = PromptTemplate("Please write a random name related to {topic}.")
gen = await llm.astream(prompt, topic="cats")
async for token in gen:
    print(token, end="", flush=True)

```

Source code in `llama-index-core/llama_index/core/llms/llm.py`  
| 
```
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
753
754
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
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
```
 | 
```
@dispatcher.span
async defastream(
    self,
    prompt: BasePromptTemplate,
    **prompt_args: Any,
) -> TokenAsyncGen:
"""
    Async stream predict for a given prompt.

    Args:
    prompt (BasePromptTemplate):
        The prompt to use for prediction.
    prompt_args (Any):
        Additional arguments to format the prompt with.

    Yields:
        str: An async generator that yields strings of tokens.

    Examples:
        ```python
        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please write a random name related to {topic}.")
        gen = await llm.astream(prompt, topic="cats")
        async for token in gen:
            print(token, end="", flush=True)
        ```

    """
    self._log_template_data(prompt, **prompt_args)

    dispatcher.event(
        LLMPredictStartEvent(template=prompt, template_args=prompt_args)
    )
    if self.metadata.is_chat_model:
        messages = self._get_messages(prompt, **prompt_args)
        chat_response = await self.astream_chat(messages)
        stream_tokens = await astream_chat_response_to_tokens(chat_response)
    else:
        formatted_prompt = self._get_prompt(prompt, **prompt_args)
        stream_response = await self.astream_complete(
            formatted_prompt, formatted=True
        )
        stream_tokens = await astream_completion_response_to_tokens(stream_response)

    if prompt.output_parser is not None or self.output_parser is not None:
        raise NotImplementedError("Output parser is not supported for streaming.")

    return stream_tokens

```
 |  
| --- | --- |  
###  predict_and_call [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.predict_and_call "Permanent link")

```
predict_and_call(
    tools: [],
    user_msg: Optional[Union[, ]] = None,
    chat_history: Optional[[]] = None,
    verbose:  = False,
    **kwargs: 
) -> 

```

Predict and call the tool.
By default uses a ReAct agent to do tool calling (through text prompting), but function calling LLMs will implement this differently.
Source code in `llama-index-core/llama_index/core/llms/llm.py`  
| 
```
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
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
858
859
860
861
862
863
864
865
866
```
 | 
```
@dispatcher.span
defpredict_and_call(
    self,
    tools: List["BaseTool"],
    user_msg: Optional[Union[str, ChatMessage]] = None,
    chat_history: Optional[List[ChatMessage]] = None,
    verbose: bool = False,
    **kwargs: Any,
) -> "AgentChatResponse":
"""
    Predict and call the tool.

    By default uses a ReAct agent to do tool calling (through text prompting),
    but function calling LLMs will implement this differently.

    """
    fromllama_index.core.agent.workflowimport ReActAgent
    fromllama_index.core.agent.workflow.agent_contextimport SimpleAgentContext
    fromllama_index.core.chat_engine.typesimport AgentChatResponse
    fromllama_index.core.memoryimport Memory
    fromllama_index.core.toolsimport adapt_to_async_tool
    fromllama_index.core.tools.callingimport call_tool_with_selection

    agent = ReActAgent(
        tools=tools,
        llm=self,
        verbose=verbose,
        formatter=kwargs.get("react_chat_formatter"),
        output_parser=kwargs.get("output_parser"),
        tool_retriever=kwargs.get("tool_retriever"),
    )

    memory = kwargs.get("memory", Memory.from_defaults())

    if isinstance(user_msg, ChatMessage) and isinstance(user_msg.content, str):
        pass
    elif isinstance(user_msg, str):
        user_msg = ChatMessage(content=user_msg, role=MessageRole.USER)

    llm_input = []
    if chat_history:
        llm_input.extend(chat_history)
    if user_msg:
        llm_input.append(user_msg)

    ctx = SimpleAgentContext()
    async_tools = [adapt_to_async_tool(t) for t in (tools or [])]

    try:
        resp = asyncio_run(
            agent.take_step(
                ctx=ctx, llm_input=llm_input, tools=async_tools, memory=memory
            )
        )
        tool_outputs = []
        for tool_call in resp.tool_calls:
            tool_output = call_tool_with_selection(
                tool_call=tool_call,
                tools=tools or [],
                verbose=verbose,
            )
            tool_outputs.append(tool_output)
        output_text = "\n\n".join(
            [tool_output.content for tool_output in tool_outputs]
        )
        return AgentChatResponse(
            response=output_text,
            sources=tool_outputs,
        )
    except Exception as e:
        output = AgentChatResponse(
            response="An error occurred while running the tool: " + str(e),
            sources=[],
        )

    return output

```
 |  
| --- | --- |  
###  apredict_and_call [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.apredict_and_call "Permanent link")

```
apredict_and_call(
    tools: [],
    user_msg: Optional[Union[, ]] = None,
    chat_history: Optional[[]] = None,
    verbose:  = False,
    **kwargs: 
) -> 

```

Predict and call the tool.
Source code in `llama-index-core/llama_index/core/llms/llm.py`  
| 
```
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
885
886
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
936
```
 | 
```
@dispatcher.span
async defapredict_and_call(
    self,
    tools: List["BaseTool"],
    user_msg: Optional[Union[str, ChatMessage]] = None,
    chat_history: Optional[List[ChatMessage]] = None,
    verbose: bool = False,
    **kwargs: Any,
) -> "AgentChatResponse":
"""Predict and call the tool."""
    fromllama_index.core.agent.workflowimport ReActAgent
    fromllama_index.core.agent.workflow.agent_contextimport SimpleAgentContext
    fromllama_index.core.chat_engine.typesimport AgentChatResponse
    fromllama_index.core.memoryimport Memory
    fromllama_index.core.toolsimport adapt_to_async_tool
    fromllama_index.core.tools.callingimport acall_tool_with_selection

    agent = ReActAgent(
        tools=tools,
        llm=self,
        verbose=verbose,
        formatter=kwargs.get("react_chat_formatter"),
        output_parser=kwargs.get("output_parser"),
        tool_retriever=kwargs.get("tool_retriever"),
    )

    memory = kwargs.get("memory", Memory.from_defaults())

    if isinstance(user_msg, ChatMessage) and isinstance(user_msg.content, str):
        pass
    elif isinstance(user_msg, str):
        user_msg = ChatMessage(content=user_msg, role=MessageRole.USER)

    llm_input = []
    if chat_history:
        llm_input.extend(chat_history)
    if user_msg:
        llm_input.append(user_msg)

    ctx = SimpleAgentContext()
    async_tools = [adapt_to_async_tool(t) for t in (tools or [])]

    try:
        resp = await agent.take_step(
            ctx=ctx, llm_input=llm_input, tools=async_tools, memory=memory
        )
        tool_outputs = []
        for tool_call in resp.tool_calls:
            tool_output = await acall_tool_with_selection(
                tool_call=tool_call,
                tools=tools or [],
                verbose=verbose,
            )
            tool_outputs.append(tool_output)

        output_text = "\n\n".join(
            [tool_output.content for tool_output in tool_outputs]
        )
        return AgentChatResponse(
            response=output_text,
            sources=tool_outputs,
        )
    except Exception as e:
        output = AgentChatResponse(
            response="An error occurred while running the tool: " + str(e),
            sources=[],
        )

    return output

```
 |  
| --- | --- |  
###  as_structured_llm [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.as_structured_llm "Permanent link")

```
as_structured_llm(
    output_cls: [BaseModel], **kwargs: 
) -> StructuredLLM

```

Return a structured LLM around a given object.
Source code in `llama-index-core/llama_index/core/llms/llm.py`  
| 
```
938
939
940
941
942
943
944
945
946
```
 | 
```
defas_structured_llm(
    self,
    output_cls: Type[BaseModel],
    **kwargs: Any,
) -> "StructuredLLM":
"""Return a structured LLM around a given object."""
    fromllama_index.core.llms.structured_llmimport StructuredLLM

    return StructuredLLM(llm=self, output_cls=output_cls, **kwargs)

```
 |  
| --- | --- |  
##  stream_completion_response_to_tokens [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.stream_completion_response_to_tokens "Permanent link")

```
stream_completion_response_to_tokens(
    completion_response_gen: CompletionResponseGen,
) -> TokenGen

```

Convert a stream completion response to a stream of tokens.
Source code in `llama-index-core/llama_index/core/llms/llm.py`  
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
```
 | 
```
defstream_completion_response_to_tokens(
    completion_response_gen: CompletionResponseGen,
) -> TokenGen:
"""Convert a stream completion response to a stream of tokens."""

    defgen() -> TokenGen:
        for response in completion_response_gen:
            yield response.delta or ""

    return gen()

```
 |  
| --- | --- |  
##  stream_chat_response_to_tokens [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.stream_chat_response_to_tokens "Permanent link")

```
stream_chat_response_to_tokens(
    chat_response_gen: ChatResponseGen,
) -> TokenGen

```

Convert a stream completion response to a stream of tokens.
Source code in `llama-index-core/llama_index/core/llms/llm.py`  
| 
```
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
```
 | 
```
defstream_chat_response_to_tokens(
    chat_response_gen: ChatResponseGen,
) -> TokenGen:
"""Convert a stream completion response to a stream of tokens."""

    defgen() -> TokenGen:
        for response in chat_response_gen:
            yield response.delta or ""

    return gen()

```
 |  
| --- | --- |  
##  astream_completion_response_to_tokens [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.astream_completion_response_to_tokens "Permanent link")

```
astream_completion_response_to_tokens(
    completion_response_gen: CompletionResponseAsyncGen,
) -> TokenAsyncGen

```

Convert a stream completion response to a stream of tokens.
Source code in `llama-index-core/llama_index/core/llms/llm.py`  
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
```
 | 
```
async defastream_completion_response_to_tokens(
    completion_response_gen: CompletionResponseAsyncGen,
) -> TokenAsyncGen:
"""Convert a stream completion response to a stream of tokens."""

    async defgen() -> TokenAsyncGen:
        async for response in completion_response_gen:
            yield response.delta or ""

    return gen()

```
 |  
| --- | --- |  
##  astream_chat_response_to_tokens [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.astream_chat_response_to_tokens "Permanent link")

```
astream_chat_response_to_tokens(
    chat_response_gen: ChatResponseAsyncGen,
) -> TokenAsyncGen

```

Convert a stream completion response to a stream of tokens.
Source code in `llama-index-core/llama_index/core/llms/llm.py`  
| 
```
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
```
 | 
```
async defastream_chat_response_to_tokens(
    chat_response_gen: ChatResponseAsyncGen,
) -> TokenAsyncGen:
"""Convert a stream completion response to a stream of tokens."""

    async defgen() -> TokenAsyncGen:
        async for response in chat_response_gen:
            yield response.delta or ""

    return gen()

```
 |  
| --- | --- |  
options: members: - LLM show_source: false inherited_members: true
##  MessageRole [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.MessageRole "Permanent link")
Bases: `str`, `Enum`
Message role.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
```
 | 
```
classMessageRole(str, Enum):
"""Message role."""

    SYSTEM = "system"
    DEVELOPER = "developer"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    TOOL = "tool"
    CHATBOT = "chatbot"
    MODEL = "model"

```
 |  
| --- | --- |  
##  BaseContentBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseContentBlock "Permanent link")
Bases: , `BaseModel`
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
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
```
 | 
```
classBaseContentBlock(ABC, BaseModel):
    @classmethod
    async defamerge(
        cls, splits: List[Self], chunk_size: int, tokenizer: Any | None = None
    ) -> list[Self]:
"""
        Async merge smaller content blocks into larger blocks up to chunk_size tokens.
        Default implementation returns splits without merging, should be overridden by subclasses that support merging.
        """
        return splits

    @classmethod
    defmerge(
        cls, splits: List[Self], chunk_size: int, tokenizer: Any | None = None
    ) -> list[Self]:
"""Merge smaller content blocks into larger blocks up to chunk_size tokens."""
        return asyncio_run(
            cls.amerge(splits=splits, chunk_size=chunk_size, tokenizer=tokenizer)
        )

    async defaestimate_tokens(self, tokenizer: Any | None = None) -> int:
"""
        Async estimate the number of tokens in this content block.

        Default implementation returns 0, should be overridden by subclasses to provide meaningful estimates.
        """
        return 0

    defestimate_tokens(self, tokenizer: Any | None = None) -> int:
"""Estimate the number of tokens in this content block."""
        return asyncio_run(self.aestimate_tokens(tokenizer=tokenizer))

    async defasplit(
        self, max_tokens: int, overlap: int = 0, tokenizer: Any | None = None
    ) -> List[Self]:
"""
        Async split the content block into smaller blocks with up to max_tokens tokens each.

        Default implementation returns self in a list, should be overridden by subclasses that support splitting.
        """
        return [self]

    defsplit(
        self, max_tokens: int, overlap: int = 0, tokenizer: Any | None = None
    ) -> List[Self]:
"""Split the content block into smaller blocks with up to max_tokens tokens each."""
        return asyncio_run(
            self.asplit(max_tokens=max_tokens, overlap=overlap, tokenizer=tokenizer)
        )

    async defatruncate(
        self, max_tokens: int, tokenizer: Any | None = None, reverse: bool = False
    ) -> Self:
"""Async truncate the content block to up to max_tokens tokens."""
        tknizer = tokenizer or get_tokenizer()
        estimated_tokens = await self.aestimate_tokens(tokenizer=tknizer)
        if estimated_tokens <= max_tokens:
            return self

        split_blocks = await self.asplit(max_tokens=max_tokens, tokenizer=tknizer)
        return split_blocks[0] if not reverse else split_blocks[-1]

    deftruncate(
        self, max_tokens: int, tokenizer: Any | None = None, reverse: bool = False
    ) -> Self:
"""Truncate the content block to up to max_tokens tokens."""
        return asyncio_run(
            self.atruncate(max_tokens=max_tokens, tokenizer=tokenizer, reverse=reverse)
        )

    @property
    deftemplatable_attributes(self) -> List[str]:
"""
        List of attributes that can be templated.

        Can be overridden by subclasses.
        """
        return []

    @staticmethod
    def_get_template_str_from_attribute(attribute: Any) -> str | None:
"""
        Helper function to get template string from attribute.

        It primarily enables cases of template_vars in binary strings for non text types such as:
            - ImageBlock(image=b'{image_bytes}')
            - AudioBlock(audio=b'{audio_bytes}')
            - VideoBlock(video=b'{video_bytes}')
            - DocumentBlock(data=b'{document_bytes}')

        However, it could in theory also work with other attributes like:
            - ImageBlock(path=b'{image_path}')
            - AudioBlock(url=b'{audio_url}')

        For that to work, the validation on those fields would need to be updated though.
        """
        if attribute is None:
            return None
        if isinstance(attribute, str):
            return attribute
        elif isinstance(attribute, bytes):
            try:
                return resolve_binary(attribute).read().decode("utf-8")
            except UnicodeDecodeError:
                return None
        else:
            return str(attribute)

    defget_template_vars(self) -> list[str]:
"""
        Get template variables from the content block.
        """
        fromllama_index.core.prompts.utilsimport get_template_vars

        for attribute_name in self.templatable_attributes:
            attribute = getattr(self, attribute_name, None)
            template_str = self._get_template_str_from_attribute(attribute)
            if template_str:
                return get_template_vars(template_str)
        return []

    defformat_vars(self, **kwargs: Any) -> "BaseContentBlock":
"""
        Format the content block with the given keyword arguments.

        This function primarily enables formatting of template_vars in Textblocks and binary strings for non text:
            - ImageBlock(image=b'{image_bytes}')
            - AudioBlock(audio=b'{audio_bytes}')
            - VideoBlock(video=b'{video_bytes}')
            - DocumentBlock(data=b'{document_bytes}')

        However, it could in theory also work with other attributes like:
            - ImageBlock(path=b'{image_path}')
            - AudioBlock(url=b'{audio_url}')

        For that to work, the validation on those fields would need to be updated though.
        """
        fromllama_index.core.prompts.utilsimport format_string

        formatted_attrs: Dict[str, Any] = {}
        for attribute_name in self.templatable_attributes:
            attribute = getattr(self, attribute_name, None)
            att_type = type(attribute)
            template_str = self._get_template_str_from_attribute(attribute)
            # If the attribute is a binary string, we need to coerce to string for formatting,
            # but then we need to re-encode to bytes after formatting, which is what the code below does.
            formatted_kwargs = {
                k: resolve_binary(v, as_base64=True).read().decode()
                if isinstance(v, bytes)
                else v
                for k, v in kwargs.items()
            }
            if template_str:
                formatted_str = format_string(template_str, **formatted_kwargs)
                if att_type is str:
                    formatted_attrs[attribute_name] = formatted_str
                elif att_type is bytes:
                    formatted_attrs[attribute_name] = formatted_str.encode()
                else:
                    try:
                        formatted_attrs[attribute_name] = att_type(formatted_str)  # type: ignore
                    except Exception:
                        raise ValueError(
                            "Could not format attribute {attribute_name} with value {template_str} to type {att_type}"
                        )
        return type(self).model_validate(self.model_copy(update=formatted_attrs))

    @staticmethod
    defmimetype_from_inline_url(url: str) -> filetype.Type | None:
        if url.startswith("data:"):
            try:
                mimetype = url.split(";base64,")[0].split("data:")[1]
                return filetype.get_type(mime=mimetype)
            except Exception:
                try:
                    data = url.split(";base64,")[1]
                    decoded_data = base64.b64decode(data)
                    return filetype.guess(decoded_data)
                except Exception:
                    return None
        return None

```
 |  
| --- | --- |  
###  templatable_attributes `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseContentBlock.templatable_attributes "Permanent link")

```
templatable_attributes: []

```

List of attributes that can be templated.
Can be overridden by subclasses.
###  amerge `async` `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseContentBlock.amerge "Permanent link")

```
amerge(
    splits: [],
    chunk_size: ,
    tokenizer:  | None = None,
) -> []

```

Async merge smaller content blocks into larger blocks up to chunk_size tokens. Default implementation returns splits without merging, should be overridden by subclasses that support merging.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
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
```
 | 
```
@classmethod
async defamerge(
    cls, splits: List[Self], chunk_size: int, tokenizer: Any | None = None
) -> list[Self]:
"""
    Async merge smaller content blocks into larger blocks up to chunk_size tokens.
    Default implementation returns splits without merging, should be overridden by subclasses that support merging.
    """
    return splits

```
 |  
| --- | --- |  
###  merge `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseContentBlock.merge "Permanent link")

```
merge(
    splits: [],
    chunk_size: ,
    tokenizer:  | None = None,
) -> []

```

Merge smaller content blocks into larger blocks up to chunk_size tokens.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
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
```
 | 
```
@classmethod
defmerge(
    cls, splits: List[Self], chunk_size: int, tokenizer: Any | None = None
) -> list[Self]:
"""Merge smaller content blocks into larger blocks up to chunk_size tokens."""
    return asyncio_run(
        cls.amerge(splits=splits, chunk_size=chunk_size, tokenizer=tokenizer)
    )

```
 |  
| --- | --- |  
###  aestimate_tokens [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseContentBlock.aestimate_tokens "Permanent link")

```
aestimate_tokens(tokenizer:  | None = None) -> 

```

Async estimate the number of tokens in this content block.
Default implementation returns 0, should be overridden by subclasses to provide meaningful estimates.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
async defaestimate_tokens(self, tokenizer: Any | None = None) -> int:
"""
    Async estimate the number of tokens in this content block.

    Default implementation returns 0, should be overridden by subclasses to provide meaningful estimates.
    """
    return 0

```
 |  
| --- | --- |  
###  estimate_tokens [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseContentBlock.estimate_tokens "Permanent link")

```
estimate_tokens(tokenizer:  | None = None) -> 

```

Estimate the number of tokens in this content block.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
93
94
95
```
 | 
```
defestimate_tokens(self, tokenizer: Any | None = None) -> int:
"""Estimate the number of tokens in this content block."""
    return asyncio_run(self.aestimate_tokens(tokenizer=tokenizer))

```
 |  
| --- | --- |  
###  asplit [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseContentBlock.asplit "Permanent link")

```
asplit(
    max_tokens: ,
    overlap:  = 0,
    tokenizer:  | None = None,
) -> []

```

Async split the content block into smaller blocks with up to max_tokens tokens each.
Default implementation returns self in a list, should be overridden by subclasses that support splitting.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
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
```
 | 
```
async defasplit(
    self, max_tokens: int, overlap: int = 0, tokenizer: Any | None = None
) -> List[Self]:
"""
    Async split the content block into smaller blocks with up to max_tokens tokens each.

    Default implementation returns self in a list, should be overridden by subclasses that support splitting.
    """
    return [self]

```
 |  
| --- | --- |  
###  split [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseContentBlock.split "Permanent link")

```
split(
    max_tokens: ,
    overlap:  = 0,
    tokenizer:  | None = None,
) -> []

```

Split the content block into smaller blocks with up to max_tokens tokens each.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
defsplit(
    self, max_tokens: int, overlap: int = 0, tokenizer: Any | None = None
) -> List[Self]:
"""Split the content block into smaller blocks with up to max_tokens tokens each."""
    return asyncio_run(
        self.asplit(max_tokens=max_tokens, overlap=overlap, tokenizer=tokenizer)
    )

```
 |  
| --- | --- |  
###  atruncate [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseContentBlock.atruncate "Permanent link")

```
atruncate(
    max_tokens: ,
    tokenizer:  | None = None,
    reverse:  = False,
) -> 

```

Async truncate the content block to up to max_tokens tokens.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
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
```
 | 
```
async defatruncate(
    self, max_tokens: int, tokenizer: Any | None = None, reverse: bool = False
) -> Self:
"""Async truncate the content block to up to max_tokens tokens."""
    tknizer = tokenizer or get_tokenizer()
    estimated_tokens = await self.aestimate_tokens(tokenizer=tknizer)
    if estimated_tokens <= max_tokens:
        return self

    split_blocks = await self.asplit(max_tokens=max_tokens, tokenizer=tknizer)
    return split_blocks[0] if not reverse else split_blocks[-1]

```
 |  
| --- | --- |  
###  truncate [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseContentBlock.truncate "Permanent link")

```
truncate(
    max_tokens: ,
    tokenizer:  | None = None,
    reverse:  = False,
) -> 

```

Truncate the content block to up to max_tokens tokens.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
127
128
129
130
131
132
133
```
 | 
```
deftruncate(
    self, max_tokens: int, tokenizer: Any | None = None, reverse: bool = False
) -> Self:
"""Truncate the content block to up to max_tokens tokens."""
    return asyncio_run(
        self.atruncate(max_tokens=max_tokens, tokenizer=tokenizer, reverse=reverse)
    )

```
 |  
| --- | --- |  
###  get_template_vars [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseContentBlock.get_template_vars "Permanent link")

```
get_template_vars() -> []

```

Get template variables from the content block.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
```
 | 
```
defget_template_vars(self) -> list[str]:
"""
    Get template variables from the content block.
    """
    fromllama_index.core.prompts.utilsimport get_template_vars

    for attribute_name in self.templatable_attributes:
        attribute = getattr(self, attribute_name, None)
        template_str = self._get_template_str_from_attribute(attribute)
        if template_str:
            return get_template_vars(template_str)
    return []

```
 |  
| --- | --- |  
###  format_vars [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseContentBlock.format_vars "Permanent link")

```
format_vars(**kwargs: ) -> 'BaseContentBlock'

```

Format the content block with the given keyword arguments.
This function primarily enables formatting of template_vars in Textblocks and binary strings for non text
  * ImageBlock(image=b'{image_bytes}')
  * AudioBlock(audio=b'{audio_bytes}')
  * VideoBlock(video=b'{video_bytes}')
  * DocumentBlock(data=b'{document_bytes}')


However, it could in theory also work with other attributes like: - ImageBlock(path=b'{image_path}') - AudioBlock(url=b'{audio_url}')
For that to work, the validation on those fields would need to be updated though.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
```
 | 
```
defformat_vars(self, **kwargs: Any) -> "BaseContentBlock":
"""
    Format the content block with the given keyword arguments.

    This function primarily enables formatting of template_vars in Textblocks and binary strings for non text:
        - ImageBlock(image=b'{image_bytes}')
        - AudioBlock(audio=b'{audio_bytes}')
        - VideoBlock(video=b'{video_bytes}')
        - DocumentBlock(data=b'{document_bytes}')

    However, it could in theory also work with other attributes like:
        - ImageBlock(path=b'{image_path}')
        - AudioBlock(url=b'{audio_url}')

    For that to work, the validation on those fields would need to be updated though.
    """
    fromllama_index.core.prompts.utilsimport format_string

    formatted_attrs: Dict[str, Any] = {}
    for attribute_name in self.templatable_attributes:
        attribute = getattr(self, attribute_name, None)
        att_type = type(attribute)
        template_str = self._get_template_str_from_attribute(attribute)
        # If the attribute is a binary string, we need to coerce to string for formatting,
        # but then we need to re-encode to bytes after formatting, which is what the code below does.
        formatted_kwargs = {
            k: resolve_binary(v, as_base64=True).read().decode()
            if isinstance(v, bytes)
            else v
            for k, v in kwargs.items()
        }
        if template_str:
            formatted_str = format_string(template_str, **formatted_kwargs)
            if att_type is str:
                formatted_attrs[attribute_name] = formatted_str
            elif att_type is bytes:
                formatted_attrs[attribute_name] = formatted_str.encode()
            else:
                try:
                    formatted_attrs[attribute_name] = att_type(formatted_str)  # type: ignore
                except Exception:
                    raise ValueError(
                        "Could not format attribute {attribute_name} with value {template_str} to type {att_type}"
                    )
    return type(self).model_validate(self.model_copy(update=formatted_attrs))

```
 |  
| --- | --- |  
##  TextBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.TextBlock "Permanent link")
Bases: 
A representation of text data to directly pass to/from the LLM.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `block_type`  |  `Literal['text']`  |  `'text'`  |  
|  `text`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
```
 | 
```
classTextBlock(BaseContentBlock):
"""A representation of text data to directly pass to/from the LLM."""

    block_type: Literal["text"] = "text"
    text: str

    @classmethod
    async defamerge(
        cls, splits: List["TextBlock"], chunk_size: int, tokenizer: Any | None = None
    ) -> list["TextBlock"]:
        merged_blocks = []
        current_block_texts = []
        current_block_tokens = 0

        # TODO: Think about separators when merging, since correctly joining them requires us to understand how they
        #  were previously split. For now, we just universally join with spaces.
        for split in splits:
            split_tokens = await split.aestimate_tokens(tokenizer=tokenizer)

            if current_block_tokens + split_tokens <= chunk_size:
                current_block_texts.append(split.text)
                current_block_tokens += split_tokens
            else:
                merged_blocks.append(TextBlock(text=" ".join(current_block_texts)))
                current_block_texts = [split.text]
                current_block_tokens = split_tokens

        if current_block_texts:
            merged_blocks.append(TextBlock(text=" ".join(current_block_texts)))

        return merged_blocks

    async defaestimate_tokens(self, tokenizer: Any | None = None) -> int:
        tknizer = tokenizer or get_tokenizer()
        return len(tknizer(self.text))

    async defasplit(
        self, max_tokens: int, overlap: int = 0, tokenizer: Any | None = None
    ) -> List["TextBlock"]:
        fromllama_index.core.node_parserimport TokenTextSplitter

        text_splitter = TokenTextSplitter(
            chunk_size=max_tokens, chunk_overlap=overlap, tokenizer=tokenizer
        )
        chunks = text_splitter.split_text(self.text)
        return [TextBlock(text=chunk) for chunk in chunks]

    @property
    deftemplatable_attributes(self) -> list[str]:
        return ["text"]

```
 |  
| --- | --- |  
##  ImageBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock "Permanent link")
Bases: 
A representation of image data to directly pass to/from the LLM.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `block_type`  |  `Literal['image']`  |  `'image'`  |  
|  `image`  |  `bytes | IOBase | None`  |  `None`  |  
|  `path`  |  `Annotated[Path, PathType] | None`  |  `None`  |  
|  `url`  |  `AnyUrl | str | None`  |  `None`  |  
|  `image_mimetype`  |  `str | None`  |  `None`  |  
|  `detail`  |  `str | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
```
 | 
```
classImageBlock(BaseContentBlock):
"""A representation of image data to directly pass to/from the LLM."""

    block_type: Literal["image"] = "image"
    image: bytes | IOBase | None = None
    path: FilePath | None = None
    url: AnyUrl | str | None = None
    image_mimetype: str | None = None
    detail: str | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("url", mode="after")
    @classmethod
    defurlstr_to_anyurl(cls, url: str | AnyUrl | None) -> AnyUrl | None:
"""Store the url as Anyurl."""
        if isinstance(url, (AnyUrl, NoneType)):
            return url

        return AnyUrl(url=url)

    @field_serializer("image")
    defserialize_image(self, image: bytes | IOBase | None) -> bytes | None:
"""Serialize the image field."""
        if isinstance(image, bytes):
            return image
        if isinstance(image, IOBase):
            image.seek(0)
            return image.read()
        return None

    @model_validator(mode="after")
    defimage_to_base64(self) -> Self:
"""
        Store the image as base64 and guess the mimetype when possible.

        In case the model was built passing image data but without a mimetype,
        we try to guess it using the filetype library. To avoid resource-intense
        operations, we won't load the path or the URL to guess the mimetype.
        """
        if not self.image or not isinstance(self.image, bytes):
            if not self.image_mimetype:
                path = self.path or self.url
                if path:
                    suffix = Path(str(path)).suffix.replace(".", "") or None
                    mimetype = filetype.get_type(ext=suffix)
                    if not mimetype or not mimetype.mime:
                        mimetype = self.mimetype_from_inline_url(str(path))
                    if mimetype and str(mimetype.mime).startswith("image/"):
                        self.image_mimetype = str(mimetype.mime)

            return self

        self._guess_mimetype(resolve_binary(self.image).read())
        self.image = resolve_binary(self.image, as_base64=True).read()
        return self

    def_guess_mimetype(self, img_data: bytes) -> None:
        if not self.image_mimetype:
            guess = filetype.guess(img_data)
            self.image_mimetype = guess.mime if guess else None

    defresolve_image(self, as_base64: bool = False) -> IOBase:
"""
        Resolve an image such that PIL can read it.

        Args:
            as_base64 (bool): whether the resolved image should be returned as base64-encoded bytes

        """
        data_buffer = (
            resolve_binary(
                raw_bytes=self.image.read(),
                path=self.path,
                url=str(self.url) if self.url else None,
                as_base64=as_base64,
            )
            if isinstance(self.image, IOBase)
            else resolve_binary(
                raw_bytes=self.image,
                path=self.path,
                url=str(self.url) if self.url else None,
                as_base64=as_base64,
            )
        )

        # Check size by seeking to end and getting position
        data_buffer.seek(0, 2)  # Seek to end
        size = data_buffer.tell()
        data_buffer.seek(0)  # Reset to beginning

        if size == 0:
            raise ValueError("resolve_image returned zero bytes")
        return data_buffer

    definline_url(self) -> str:
        b64 = self.resolve_image(as_base64=True)
        b64_str = b64.read().decode("utf-8")
        return f"data:{self.image_mimetype};base64,{b64_str}"

    async defaestimate_tokens(self, *args: Any, **kwargs: Any) -> int:
"""
        Many APIs measure images differently. Here, we take a large estimate.

        This is based on a 2048 x 1536 image using OpenAI.

        TODO: In the future, LLMs should be able to count their own tokens.
        """
        try:
            self.resolve_image()
            return 2125
        except ValueError as e:
            # Null case
            if str(e) == "resolve_image returned zero bytes":
                return 0
            raise

    @property
    deftemplatable_attributes(self) -> list[str]:
        return ["image"]

```
 |  
| --- | --- |  
###  urlstr_to_anyurl `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock.urlstr_to_anyurl "Permanent link")

```
urlstr_to_anyurl(url:  | AnyUrl | None) -> AnyUrl | None

```

Store the url as Anyurl.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
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
```
 | 
```
@field_validator("url", mode="after")
@classmethod
defurlstr_to_anyurl(cls, url: str | AnyUrl | None) -> AnyUrl | None:
"""Store the url as Anyurl."""
    if isinstance(url, (AnyUrl, NoneType)):
        return url

    return AnyUrl(url=url)

```
 |  
| --- | --- |  
###  serialize_image [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock.serialize_image "Permanent link")

```
serialize_image(
    image: bytes | IOBase | None,
) -> bytes | None

```

Serialize the image field.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
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
```
 | 
```
@field_serializer("image")
defserialize_image(self, image: bytes | IOBase | None) -> bytes | None:
"""Serialize the image field."""
    if isinstance(image, bytes):
        return image
    if isinstance(image, IOBase):
        image.seek(0)
        return image.read()
    return None

```
 |  
| --- | --- |  
###  image_to_base64 [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock.image_to_base64 "Permanent link")

```
image_to_base64() -> 

```

Store the image as base64 and guess the mimetype when possible.
In case the model was built passing image data but without a mimetype, we try to guess it using the filetype library. To avoid resource-intense operations, we won't load the path or the URL to guess the mimetype.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
```
 | 
```
@model_validator(mode="after")
defimage_to_base64(self) -> Self:
"""
    Store the image as base64 and guess the mimetype when possible.

    In case the model was built passing image data but without a mimetype,
    we try to guess it using the filetype library. To avoid resource-intense
    operations, we won't load the path or the URL to guess the mimetype.
    """
    if not self.image or not isinstance(self.image, bytes):
        if not self.image_mimetype:
            path = self.path or self.url
            if path:
                suffix = Path(str(path)).suffix.replace(".", "") or None
                mimetype = filetype.get_type(ext=suffix)
                if not mimetype or not mimetype.mime:
                    mimetype = self.mimetype_from_inline_url(str(path))
                if mimetype and str(mimetype.mime).startswith("image/"):
                    self.image_mimetype = str(mimetype.mime)

        return self

    self._guess_mimetype(resolve_binary(self.image).read())
    self.image = resolve_binary(self.image, as_base64=True).read()
    return self

```
 |  
| --- | --- |  
###  resolve_image [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock.resolve_image "Permanent link")

```
resolve_image(as_base64:  = False) -> IOBase

```

Resolve an image such that PIL can read it.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `as_base64`  |  `bool`  |  whether the resolved image should be returned as base64-encoded bytes  |  `False`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
```
 | 
```
defresolve_image(self, as_base64: bool = False) -> IOBase:
"""
    Resolve an image such that PIL can read it.

    Args:
        as_base64 (bool): whether the resolved image should be returned as base64-encoded bytes

    """
    data_buffer = (
        resolve_binary(
            raw_bytes=self.image.read(),
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=as_base64,
        )
        if isinstance(self.image, IOBase)
        else resolve_binary(
            raw_bytes=self.image,
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=as_base64,
        )
    )

    # Check size by seeking to end and getting position
    data_buffer.seek(0, 2)  # Seek to end
    size = data_buffer.tell()
    data_buffer.seek(0)  # Reset to beginning

    if size == 0:
        raise ValueError("resolve_image returned zero bytes")
    return data_buffer

```
 |  
| --- | --- |  
###  aestimate_tokens [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock.aestimate_tokens "Permanent link")

```
aestimate_tokens(*args: , **kwargs: ) -> 

```

Many APIs measure images differently. Here, we take a large estimate.
This is based on a 2048 x 1536 image using OpenAI.
TODO: In the future, LLMs should be able to count their own tokens.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
```
 | 
```
async defaestimate_tokens(self, *args: Any, **kwargs: Any) -> int:
"""
    Many APIs measure images differently. Here, we take a large estimate.

    This is based on a 2048 x 1536 image using OpenAI.

    TODO: In the future, LLMs should be able to count their own tokens.
    """
    try:
        self.resolve_image()
        return 2125
    except ValueError as e:
        # Null case
        if str(e) == "resolve_image returned zero bytes":
            return 0
        raise

```
 |  
| --- | --- |  
##  AudioBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock "Permanent link")
Bases: 
A representation of audio data to directly pass to/from the LLM.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `block_type`  |  `Literal['audio']`  |  `'audio'`  |  
|  `audio`  |  `bytes | IOBase | None`  |  `None`  |  
|  `path`  |  `Annotated[Path, PathType] | None`  |  `None`  |  
|  `url`  |  `AnyUrl | str | None`  |  `None`  |  
|  `format`  |  `str | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
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
537
538
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
```
 | 
```
classAudioBlock(BaseContentBlock):
"""A representation of audio data to directly pass to/from the LLM."""

    block_type: Literal["audio"] = "audio"
    audio: bytes | IOBase | None = None
    path: FilePath | None = None
    url: AnyUrl | str | None = None
    format: str | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("url", mode="after")
    @classmethod
    defurlstr_to_anyurl(cls, url: str | AnyUrl | None) -> AnyUrl | None:
"""Store the url as Anyurl."""
        if isinstance(url, (AnyUrl, NoneType)):
            return url
        return AnyUrl(url=url)

    @field_serializer("audio")
    defserialize_audio(self, audio: bytes | IOBase | None) -> bytes | None:
"""Serialize the audio field."""
        if isinstance(audio, bytes):
            return audio
        if isinstance(audio, IOBase):
            audio.seek(0)
            return audio.read()
        return None

    @model_validator(mode="after")
    defaudio_to_base64(self) -> Self:
"""
        Store the audio as base64 and guess the mimetype when possible.

        In case the model was built passing audio data but without a format,
        we try to guess it using the filetype library. To avoid resource-intense
        operations, we won't load the path or the URL to guess the format.
        """
        if not self.audio or not isinstance(self.audio, bytes):
            if not self.format:
                path = self.path or self.url
                if path:
                    suffix = Path(str(path)).suffix.replace(".", "") or None
                    mimetype = filetype.get_type(ext=suffix)
                    if not mimetype or not mimetype.mime:
                        mimetype = self.mimetype_from_inline_url(str(path))
                    if mimetype and str(mimetype.mime).startswith("audio/"):
                        self.format = str(mimetype.extension)

            return self

        self._guess_format(resolve_binary(self.audio).read())
        self.audio = resolve_binary(self.audio, as_base64=True).read()
        return self

    def_guess_format(self, audio_data: bytes) -> None:
        if not self.format:
            guess = filetype.guess(audio_data)
            self.format = guess.extension if guess else None

    defresolve_audio(self, as_base64: bool = False) -> IOBase:
"""
        Resolve an audio such that PIL can read it.

        Args:
            as_base64 (bool): whether the resolved audio should be returned as base64-encoded bytes

        """
        data_buffer = (
            resolve_binary(
                raw_bytes=self.audio.read(),
                path=self.path,
                url=str(self.url) if self.url else None,
                as_base64=as_base64,
            )
            if isinstance(self.audio, IOBase)
            else resolve_binary(
                raw_bytes=self.audio,
                path=self.path,
                url=str(self.url) if self.url else None,
                as_base64=as_base64,
            )
        )
        # Check size by seeking to end and getting position
        data_buffer.seek(0, 2)  # Seek to end
        size = data_buffer.tell()
        data_buffer.seek(0)  # Reset to beginning

        if size == 0:
            raise ValueError("resolve_audio returned zero bytes")
        return data_buffer

    definline_url(self) -> str:
        b64 = self.resolve_audio(as_base64=True)
        b64_str = b64.read().decode("utf-8")
        if self.format:
            mimetype = filetype.get_type(ext=self.format).mime
            if mimetype:
                return f"data:{mimetype};base64,{b64_str}"
        return f"data:audio;base64,{b64_str}"

    async defaestimate_tokens(self, *args: Any, **kwargs: Any) -> int:
"""
        Use TinyTag to estimate the duration of the audio file and convert to tokens.

        Gemini estimates 32 tokens per second of audio
        https://ai.google.dev/gemini-api/docs/tokens?lang=python

        OpenAI estimates 1 token per 0.1 second for user input and 1 token per 0.05 seconds for assistant output
        https://platform.openai.com/docs/guides/realtime-costs
        """
        try:
            # First try tinytag
            try:
                tag = TinyTag.get(file_obj=cast(BytesIO, self.resolve_audio()))
                if duration := tag.duration:
                    # We conservatively return the max estimate
                    return max((int(duration) + 1) * 32, int(duration / 0.05) + 1)
            except UnsupportedFormatError:
                _logger.info(
                    "TinyTag does not support file type for video token estimation."
                )
            return 256  # fallback
        except ValueError as e:
            # Null case
            if str(e) == "resolve_audio returned zero bytes":
                return 0
            raise

    @property
    deftemplatable_attributes(self) -> list[str]:
        return ["audio"]

```
 |  
| --- | --- |  
###  urlstr_to_anyurl `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock.urlstr_to_anyurl "Permanent link")

```
urlstr_to_anyurl(url:  | AnyUrl | None) -> AnyUrl | None

```

Store the url as Anyurl.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
433
434
435
436
437
438
439
```
 | 
```
@field_validator("url", mode="after")
@classmethod
defurlstr_to_anyurl(cls, url: str | AnyUrl | None) -> AnyUrl | None:
"""Store the url as Anyurl."""
    if isinstance(url, (AnyUrl, NoneType)):
        return url
    return AnyUrl(url=url)

```
 |  
| --- | --- |  
###  serialize_audio [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock.serialize_audio "Permanent link")

```
serialize_audio(
    audio: bytes | IOBase | None,
) -> bytes | None

```

Serialize the audio field.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
@field_serializer("audio")
defserialize_audio(self, audio: bytes | IOBase | None) -> bytes | None:
"""Serialize the audio field."""
    if isinstance(audio, bytes):
        return audio
    if isinstance(audio, IOBase):
        audio.seek(0)
        return audio.read()
    return None

```
 |  
| --- | --- |  
###  audio_to_base64 [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock.audio_to_base64 "Permanent link")

```
audio_to_base64() -> 

```

Store the audio as base64 and guess the mimetype when possible.
In case the model was built passing audio data but without a format, we try to guess it using the filetype library. To avoid resource-intense operations, we won't load the path or the URL to guess the format.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
```
 | 
```
@model_validator(mode="after")
defaudio_to_base64(self) -> Self:
"""
    Store the audio as base64 and guess the mimetype when possible.

    In case the model was built passing audio data but without a format,
    we try to guess it using the filetype library. To avoid resource-intense
    operations, we won't load the path or the URL to guess the format.
    """
    if not self.audio or not isinstance(self.audio, bytes):
        if not self.format:
            path = self.path or self.url
            if path:
                suffix = Path(str(path)).suffix.replace(".", "") or None
                mimetype = filetype.get_type(ext=suffix)
                if not mimetype or not mimetype.mime:
                    mimetype = self.mimetype_from_inline_url(str(path))
                if mimetype and str(mimetype.mime).startswith("audio/"):
                    self.format = str(mimetype.extension)

        return self

    self._guess_format(resolve_binary(self.audio).read())
    self.audio = resolve_binary(self.audio, as_base64=True).read()
    return self

```
 |  
| --- | --- |  
###  resolve_audio [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock.resolve_audio "Permanent link")

```
resolve_audio(as_base64:  = False) -> IOBase

```

Resolve an audio such that PIL can read it.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `as_base64`  |  `bool`  |  whether the resolved audio should be returned as base64-encoded bytes  |  `False`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
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
```
 | 
```
defresolve_audio(self, as_base64: bool = False) -> IOBase:
"""
    Resolve an audio such that PIL can read it.

    Args:
        as_base64 (bool): whether the resolved audio should be returned as base64-encoded bytes

    """
    data_buffer = (
        resolve_binary(
            raw_bytes=self.audio.read(),
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=as_base64,
        )
        if isinstance(self.audio, IOBase)
        else resolve_binary(
            raw_bytes=self.audio,
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=as_base64,
        )
    )
    # Check size by seeking to end and getting position
    data_buffer.seek(0, 2)  # Seek to end
    size = data_buffer.tell()
    data_buffer.seek(0)  # Reset to beginning

    if size == 0:
        raise ValueError("resolve_audio returned zero bytes")
    return data_buffer

```
 |  
| --- | --- |  
###  aestimate_tokens [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock.aestimate_tokens "Permanent link")

```
aestimate_tokens(*args: , **kwargs: ) -> 

```

Use TinyTag to estimate the duration of the audio file and convert to tokens.
Gemini estimates 32 tokens per second of audio https://ai.google.dev/gemini-api/docs/tokens?lang=python
OpenAI estimates 1 token per 0.1 second for user input and 1 token per 0.05 seconds for assistant output https://platform.openai.com/docs/guides/realtime-costs
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
546
547
548
549
```
 | 
```
async defaestimate_tokens(self, *args: Any, **kwargs: Any) -> int:
"""
    Use TinyTag to estimate the duration of the audio file and convert to tokens.

    Gemini estimates 32 tokens per second of audio
    https://ai.google.dev/gemini-api/docs/tokens?lang=python

    OpenAI estimates 1 token per 0.1 second for user input and 1 token per 0.05 seconds for assistant output
    https://platform.openai.com/docs/guides/realtime-costs
    """
    try:
        # First try tinytag
        try:
            tag = TinyTag.get(file_obj=cast(BytesIO, self.resolve_audio()))
            if duration := tag.duration:
                # We conservatively return the max estimate
                return max((int(duration) + 1) * 32, int(duration / 0.05) + 1)
        except UnsupportedFormatError:
            _logger.info(
                "TinyTag does not support file type for video token estimation."
            )
        return 256  # fallback
    except ValueError as e:
        # Null case
        if str(e) == "resolve_audio returned zero bytes":
            return 0
        raise

```
 |  
| --- | --- |  
##  VideoBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock "Permanent link")
Bases: 
A representation of video data to directly pass to/from the LLM.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `block_type`  |  `Literal['video']`  |  `'video'`  |  
|  `video`  |  `bytes | IOBase | None`  |  `None`  |  
|  `path`  |  `Annotated[Path, PathType] | None`  |  `None`  |  
|  `url`  |  `AnyUrl | str | None`  |  `None`  |  
|  `video_mimetype`  |  `str | None`  |  `None`  |  
|  `detail`  |  `str | None`  |  `None`  |  
|  `fps`  |  `int | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
596
597
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
645
646
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
664
665
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
683
```
 | 
```
classVideoBlock(BaseContentBlock):
"""A representation of video data to directly pass to/from the LLM."""

    block_type: Literal["video"] = "video"
    video: bytes | IOBase | None = None
    path: FilePath | None = None
    url: AnyUrl | str | None = None
    video_mimetype: str | None = None
    detail: str | None = None
    fps: int | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("url", mode="after")
    @classmethod
    defurlstr_to_anyurl(cls, url: str | AnyUrl | None) -> AnyUrl | None:
"""Store the url as AnyUrl."""
        if isinstance(url, (AnyUrl, NoneType)):
            return url
        return AnyUrl(url=url)

    @field_serializer("video")
    defserialize_video(self, video: bytes | IOBase | None) -> bytes | None:
"""Serialize the video field."""
        if isinstance(video, bytes):
            return video
        if isinstance(video, IOBase):
            video.seek(0)
            return video.read()
        return None

    @model_validator(mode="after")
    defvideo_to_base64(self) -> "VideoBlock":
"""
        Store the video as base64 and guess the mimetype when possible.

        If video data is passed but no mimetype is provided, try to infer it.
        """
        if not self.video or not isinstance(self.video, bytes):
            if not self.video_mimetype:
                path = self.path or self.url
                if path:
                    suffix = Path(str(path)).suffix.replace(".", "") or None
                    mimetype = filetype.get_type(ext=suffix)
                    if not mimetype or not mimetype.mime:
                        mimetype = self.mimetype_from_inline_url(str(path))
                    if mimetype and str(mimetype.mime).startswith("video/"):
                        self.video_mimetype = str(mimetype.mime)
            return self

        self._guess_mimetype(resolve_binary(self.video).read())
        self.video = resolve_binary(self.video, as_base64=True).read()
        return self

    def_guess_mimetype(self, vid_data: bytes) -> None:
        if not self.video_mimetype:
            guess = filetype.guess(vid_data)
            if guess and guess.mime.startswith("video/"):
                self.video_mimetype = guess.mime

    defresolve_video(self, as_base64: bool = False) -> IOBase:
"""
        Resolve a video file to a IOBase buffer.

        Args:
            as_base64 (bool): whether to return the video as base64-encoded bytes

        """
        data_buffer = (
            resolve_binary(
                raw_bytes=self.video.read(),
                path=self.path,
                url=str(self.url) if self.url else None,
                as_base64=as_base64,
            )
            if isinstance(self.video, IOBase)
            else resolve_binary(
                raw_bytes=self.video,
                path=self.path,
                url=str(self.url) if self.url else None,
                as_base64=as_base64,
            )
        )

        # Check size by seeking to end and getting position
        data_buffer.seek(0, 2)  # Seek to end
        size = data_buffer.tell()
        data_buffer.seek(0)  # Reset to beginning

        if size == 0:
            raise ValueError("resolve_video returned zero bytes")
        return data_buffer

    definline_url(self) -> str:
        b64 = self.resolve_video(as_base64=True)
        b64_str = b64.read().decode("utf-8")
        if self.video_mimetype:
            return f"data:{self.video_mimetype};base64,{b64_str}"
        return f"data:video;base64,{b64_str}"

    async defaestimate_tokens(self, *args: Any, **kwargs: Any) -> int:
"""
        Use TinyTag to estimate the duration of the video file and convert to tokens.

        Gemini estimates 263 tokens per second of video
        https://ai.google.dev/gemini-api/docs/tokens?lang=python
        """
        try:
            # First try tinytag
            try:
                tag = TinyTag.get(file_obj=cast(BytesIO, self.resolve_video()))
                if duration := tag.duration:
                    return (int(duration) + 1) * 263
            except UnsupportedFormatError:
                _logger.info(
                    "TinyTag does not support file type for video token estimation."
                )
            # fallback of roughly 8 times the fallback cost of audio (263 // 32; based on gemini pricing per sec)
            return 256 * 8
        except ValueError as e:
            # Null case
            if str(e) == "resolve_video returned zero bytes":
                return 0
            raise

    @property
    deftemplatable_attributes(self) -> list[str]:
        return ["video"]

```
 |  
| --- | --- |  
###  urlstr_to_anyurl `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock.urlstr_to_anyurl "Permanent link")

```
urlstr_to_anyurl(url:  | AnyUrl | None) -> AnyUrl | None

```

Store the url as AnyUrl.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
569
570
571
572
573
574
575
```
 | 
```
@field_validator("url", mode="after")
@classmethod
defurlstr_to_anyurl(cls, url: str | AnyUrl | None) -> AnyUrl | None:
"""Store the url as AnyUrl."""
    if isinstance(url, (AnyUrl, NoneType)):
        return url
    return AnyUrl(url=url)

```
 |  
| --- | --- |  
###  serialize_video [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock.serialize_video "Permanent link")

```
serialize_video(
    video: bytes | IOBase | None,
) -> bytes | None

```

Serialize the video field.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
577
578
579
580
581
582
583
584
585
```
 | 
```
@field_serializer("video")
defserialize_video(self, video: bytes | IOBase | None) -> bytes | None:
"""Serialize the video field."""
    if isinstance(video, bytes):
        return video
    if isinstance(video, IOBase):
        video.seek(0)
        return video.read()
    return None

```
 |  
| --- | --- |  
###  video_to_base64 [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock.video_to_base64 "Permanent link")

```
video_to_base64() -> 'VideoBlock'

```

Store the video as base64 and guess the mimetype when possible.
If video data is passed but no mimetype is provided, try to infer it.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
603
604
605
606
607
608
```
 | 
```
@model_validator(mode="after")
defvideo_to_base64(self) -> "VideoBlock":
"""
    Store the video as base64 and guess the mimetype when possible.

    If video data is passed but no mimetype is provided, try to infer it.
    """
    if not self.video or not isinstance(self.video, bytes):
        if not self.video_mimetype:
            path = self.path or self.url
            if path:
                suffix = Path(str(path)).suffix.replace(".", "") or None
                mimetype = filetype.get_type(ext=suffix)
                if not mimetype or not mimetype.mime:
                    mimetype = self.mimetype_from_inline_url(str(path))
                if mimetype and str(mimetype.mime).startswith("video/"):
                    self.video_mimetype = str(mimetype.mime)
        return self

    self._guess_mimetype(resolve_binary(self.video).read())
    self.video = resolve_binary(self.video, as_base64=True).read()
    return self

```
 |  
| --- | --- |  
###  resolve_video [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock.resolve_video "Permanent link")

```
resolve_video(as_base64:  = False) -> IOBase

```

Resolve a video file to a IOBase buffer.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `as_base64`  |  `bool`  |  whether to return the video as base64-encoded bytes  |  `False`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
645
646
647
```
 | 
```
defresolve_video(self, as_base64: bool = False) -> IOBase:
"""
    Resolve a video file to a IOBase buffer.

    Args:
        as_base64 (bool): whether to return the video as base64-encoded bytes

    """
    data_buffer = (
        resolve_binary(
            raw_bytes=self.video.read(),
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=as_base64,
        )
        if isinstance(self.video, IOBase)
        else resolve_binary(
            raw_bytes=self.video,
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=as_base64,
        )
    )

    # Check size by seeking to end and getting position
    data_buffer.seek(0, 2)  # Seek to end
    size = data_buffer.tell()
    data_buffer.seek(0)  # Reset to beginning

    if size == 0:
        raise ValueError("resolve_video returned zero bytes")
    return data_buffer

```
 |  
| --- | --- |  
###  aestimate_tokens [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock.aestimate_tokens "Permanent link")

```
aestimate_tokens(*args: , **kwargs: ) -> 

```

Use TinyTag to estimate the duration of the video file and convert to tokens.
Gemini estimates 263 tokens per second of video https://ai.google.dev/gemini-api/docs/tokens?lang=python
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
656
657
658
659
660
661
662
663
664
665
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
```
 | 
```
async defaestimate_tokens(self, *args: Any, **kwargs: Any) -> int:
"""
    Use TinyTag to estimate the duration of the video file and convert to tokens.

    Gemini estimates 263 tokens per second of video
    https://ai.google.dev/gemini-api/docs/tokens?lang=python
    """
    try:
        # First try tinytag
        try:
            tag = TinyTag.get(file_obj=cast(BytesIO, self.resolve_video()))
            if duration := tag.duration:
                return (int(duration) + 1) * 263
        except UnsupportedFormatError:
            _logger.info(
                "TinyTag does not support file type for video token estimation."
            )
        # fallback of roughly 8 times the fallback cost of audio (263 // 32; based on gemini pricing per sec)
        return 256 * 8
    except ValueError as e:
        # Null case
        if str(e) == "resolve_video returned zero bytes":
            return 0
        raise

```
 |  
| --- | --- |  
##  DocumentBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.DocumentBlock "Permanent link")
Bases: 
A representation of a document to directly pass to the LLM.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `block_type`  |  `Literal['document']`  |  `'document'`  |  
|  `data`  |  `bytes | IOBase | None`  |  `None`  |  
|  `path`  |  `Annotated[Path, PathType] | str | None`  |  `None`  |  
|  `url`  |  `str | None`  |  `None`  |  
|  `title`  |  `str | None`  |  `None`  |  
|  `document_mimetype`  |  `str | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
705
706
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
729
730
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
753
754
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
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
```
 | 
```
classDocumentBlock(BaseContentBlock):
"""A representation of a document to directly pass to the LLM."""

    block_type: Literal["document"] = "document"
    data: bytes | IOBase | None = None
    path: Optional[Union[FilePath | str]] = None
    url: Optional[str] = None
    title: Optional[str] = None
    document_mimetype: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="after")
    defdocument_validation(self) -> Self:
        self.document_mimetype = self.document_mimetype or self._guess_mimetype()

        if not self.title:
            self.title = "input_document"

        # skip data validation if no byte is provided
        if not self.data or not isinstance(self.data, bytes):
            return self

        self.data = resolve_binary(self.data, as_base64=True).read()
        return self

    @field_serializer("data")
    defserialize_data(self, data: bytes | IOBase | None) -> bytes | None:
"""Serialize the data field."""
        if isinstance(data, bytes):
            return data
        if isinstance(data, IOBase):
            data.seek(0)
            return data.read()
        return None

    defresolve_document(self) -> IOBase:
"""
        Resolve a document such that it is represented by a BufferIO object.
        """
        data_buffer = (
            self.data
            if isinstance(self.data, IOBase)
            else resolve_binary(
                raw_bytes=self.data,
                path=self.path,
                url=str(self.url) if self.url else None,
                as_base64=False,
            )
        )
        # Check size by seeking to end and getting position
        data_buffer.seek(0, 2)  # Seek to end
        size = data_buffer.tell()
        data_buffer.seek(0)  # Reset to beginning

        if size == 0:
            raise ValueError("resolve_document returned zero bytes")
        return data_buffer

    def_get_b64_bytes(self, data_buffer: IOBase) -> bytes:
"""
        Get base64-encoded bytes from a IOBase buffer.
        """
        return resolve_binary(data_buffer.read(), as_base64=True).read()

    def_get_b64_string(self, data_buffer: IOBase) -> str:
"""
        Get base64-encoded string from a IOBase buffer.
        """
        return self._get_b64_bytes(data_buffer).decode("utf-8")

    definline_url(self) -> str:
        b64_str = self._get_b64_string(data_buffer=self.resolve_document())
        if self.document_mimetype:
            return f"data:{self.document_mimetype};base64,{b64_str}"
        return f"data:application;base64,{b64_str}"

    defguess_format(self) -> str | None:
        path = self.path or self.url
        if not path:
            return None

        return Path(str(path)).suffix.replace(".", "")

    def_guess_mimetype(self) -> str | None:
        if self.document_mimetype:
            return self.document_mimetype

        if self.data:
            guess = filetype.guess(self.data)
            return str(guess.mime) if guess else None

        suffix = self.guess_format()
        if not suffix:
            return None

        guess = filetype.get_type(ext=suffix)
        return str(guess.mime) if guess else None

    async defaestimate_tokens(self, *args: Any, **kwargs: Any) -> int:
        try:
            self.resolve_document()
        except ValueError as e:
            # Null case
            if str(e) == "resolve_document returned zero bytes":
                return 0
            raise
        # We currently only use this fallback estimate for documents which are non zero bytes
        return 512

    @property
    deftemplatable_attributes(self) -> list[str]:
        return ["data"]

```
 |  
| --- | --- |  
###  serialize_data [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.DocumentBlock.serialize_data "Permanent link")

```
serialize_data(data: bytes | IOBase | None) -> bytes | None

```

Serialize the data field.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
712
713
714
715
716
717
718
719
720
```
 | 
```
@field_serializer("data")
defserialize_data(self, data: bytes | IOBase | None) -> bytes | None:
"""Serialize the data field."""
    if isinstance(data, bytes):
        return data
    if isinstance(data, IOBase):
        data.seek(0)
        return data.read()
    return None

```
 |  
| --- | --- |  
###  resolve_document [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.DocumentBlock.resolve_document "Permanent link")

```
resolve_document() -> IOBase

```

Resolve a document such that it is represented by a BufferIO object.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
722
723
724
725
726
727
728
729
730
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
```
 | 
```
defresolve_document(self) -> IOBase:
"""
    Resolve a document such that it is represented by a BufferIO object.
    """
    data_buffer = (
        self.data
        if isinstance(self.data, IOBase)
        else resolve_binary(
            raw_bytes=self.data,
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=False,
        )
    )
    # Check size by seeking to end and getting position
    data_buffer.seek(0, 2)  # Seek to end
    size = data_buffer.tell()
    data_buffer.seek(0)  # Reset to beginning

    if size == 0:
        raise ValueError("resolve_document returned zero bytes")
    return data_buffer

```
 |  
| --- | --- |  
##  CacheControl [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CacheControl "Permanent link")
Bases: 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `type`  |  _required_  |  
|  `ttl`  |  `'5m'`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
801
802
803
```
 | 
```
classCacheControl(BaseContentBlock):
    type: str
    ttl: str = Field(default="5m")

```
 |  
| --- | --- |  
##  CachePoint [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CachePoint "Permanent link")
Bases: 
Used to set the point to cache up to, if the LLM supports caching.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `block_type`  |  `Literal['cache']`  |  `'cache'`  |  
|  `cache_control`  |   |  _required_  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
806
807
808
809
810
```
 | 
```
classCachePoint(BaseContentBlock):
"""Used to set the point to cache up to, if the LLM supports caching."""

    block_type: Literal["cache"] = "cache"
    cache_control: CacheControl

```
 |  
| --- | --- |  
##  BaseRecursiveContentBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseRecursiveContentBlock "Permanent link")
Bases: 
Base class for content blocks that can contain other content blocks.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
 813
 814
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
 858
 859
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
 885
 886
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
 936
 937
 938
 939
 940
 941
 942
 943
 944
 945
 946
 947
 948
 949
 950
 951
 952
 953
 954
 955
 956
 957
 958
 959
 960
 961
 962
 963
 964
 965
 966
 967
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
```
 | 
```
classBaseRecursiveContentBlock(BaseContentBlock):
"""Base class for content blocks that can contain other content blocks."""

    @classmethod
    defnested_blocks_field_name(cls) -> str:
"""
        Return the name of the field that contains nested content blocks.

        By default, this is "content", but subclasses can override this method
        """
        return "content"

    @property
    defnested_blocks(self) -> List[BaseContentBlock]:
"""Return the nested content blocks."""
        blocks = getattr(self, self.nested_blocks_field_name())
        if isinstance(blocks, str):
            blocks = TextBlock(text=blocks)
        return blocks if isinstance(blocks, list) else [blocks]

    defcan_merge(self, other: Self) -> bool:
"""Check if this block can be merged with another block of the same type."""
        atts = {
            k: v
            for k, v in self.model_dump().items()
            if k != self.nested_blocks_field_name()
        }
        other_atts = {
            k: v
            for k, v in other.model_dump().items()
            if k != self.nested_blocks_field_name()
        }
        return atts == other_atts

    @staticmethod
    async defamerge_nested(
        nested_blocks: list[BaseContentBlock],
        chunk_size: int,
        tokenizer: Any | None = None,
    ) -> list[BaseContentBlock]:
        # make list of lists out of nested blocks of same type
        nested_blocks_by_type: list[list[BaseContentBlock]] = []
        for nb in nested_blocks:
            if not nested_blocks_by_type or type(
                nested_blocks_by_type[-1][0]
            ) is not type(nb):
                nested_blocks_by_type.append([nb])
            else:
                nested_blocks_by_type[-1].append(nb)

        new_nested_blocks = []
        # merge nested blocks of same type
        for nbs in nested_blocks_by_type:
            new_nested_blocks.extend(
                await type(nbs[0]).amerge(
                    nbs, chunk_size=chunk_size, tokenizer=tokenizer
                )
            )
        return new_nested_blocks

    @classmethod
    async defamerge(
        cls,
        splits: List["BaseRecursiveContentBlock"],
        chunk_size: int,
        tokenizer: Any | None = None,
    ) -> list["BaseRecursiveContentBlock"]:
"""
        First merge nested_blocks of consecutive BaseRecursiveContentBlock types based on token estimates

        Then, merge consecutive nested content blocks of the same type.
        """
        merged_blocks = []
        cur_blocks: list["BaseRecursiveContentBlock"] = []
        cur_block_tokens = 0

        for split in splits:
            split_tokens = await split.aestimate_tokens(tokenizer=tokenizer)
            can_merge = len(cur_blocks) == 0 or cur_blocks[-1].can_merge(split)
            if cur_block_tokens + split_tokens <= chunk_size and can_merge:
                cur_blocks.append(split)
                cur_block_tokens += split_tokens
            else:
                if cur_blocks:
                    attributes = cur_blocks[0].model_dump() | {
                        # Overwrite nested blocks
                        cls.nested_blocks_field_name(): await cls.amerge_nested(
                            nested_blocks=[
                                nested_block
                                for block in cur_blocks
                                for nested_block in block.nested_blocks
                            ],
                            chunk_size=chunk_size,
                            tokenizer=tokenizer,
                        )
                    }
                    merged_blocks.append(cls(**attributes))
                cur_blocks = [split]
                cur_block_tokens = split_tokens

        if cur_blocks:
            attributes = cur_blocks[0].model_dump() | {
                # Overwrite nested blocks attribute and merge nested blocks of the same type
                cls.nested_blocks_field_name(): await cls.amerge_nested(
                    nested_blocks=[
                        nested_block
                        for block in cur_blocks
                        for nested_block in block.nested_blocks
                    ],
                    chunk_size=chunk_size,
                    tokenizer=tokenizer,
                )
            }
            merged_blocks.append(cls(**attributes))

        return merged_blocks

    async defaestimate_tokens(self, *args: Any, **kwargs: Any) -> int:
"""Estimate the number of tokens in this content block."""
        return sum(
            [
                await block.aestimate_tokens(*args, **kwargs)
                for block in self.nested_blocks
            ]
        )

    async defasplit(
        self, max_tokens: int, overlap: int = 0, tokenizer: Any | None = None
    ) -> List["BaseRecursiveContentBlock"]:
"""Split the content block into smaller blocks with up to max_tokens tokens each."""
        splits = []

        cls = type(self)
        for block in self.nested_blocks:
            block_tokens = await block.aestimate_tokens(tokenizer=tokenizer)
            if block_tokens <= max_tokens:
                attributes = self.model_dump() | {
                    # Overwrite nested blocks
                    self.nested_blocks_field_name(): [block]
                }
                splits.append(cls(**attributes))
            else:
                split_blocks = await block.asplit(
                    max_tokens=max_tokens, tokenizer=tokenizer
                )
                for split_block in split_blocks:
                    attributes = self.model_dump() | {
                        # Overwrite nested blocks
                        self.nested_blocks_field_name(): [split_block]
                    }
                    splits.append(cls(**attributes))

        return splits

    async defatruncate(
        self, max_tokens: int, tokenizer: Any | None = None, reverse: bool = False
    ) -> "BaseRecursiveContentBlock":
"""Truncate the content block to have at most max_tokens tokens."""
        tknizer = tokenizer or get_tokenizer()
        current_tokens = 0
        truncated_blocks = []

        cls = type(self)
        for block in (
            self.nested_blocks if not reverse else reversed(self.nested_blocks)
        ):
            block_tokens = await block.aestimate_tokens(tokenizer=tknizer)
            if current_tokens + block_tokens <= max_tokens:
                if not reverse:
                    truncated_blocks.append(block)
                else:
                    truncated_blocks.insert(0, block)
                current_tokens += block_tokens
            else:
                remaining_tokens = max_tokens - current_tokens
                if remaining_tokens  0:
                    truncated_block = await block.atruncate(
                        max_tokens=remaining_tokens, tokenizer=tknizer, reverse=reverse
                    )
                    # For some block types, truncate may return a block larger than requested
                    # However, we still want to include it if no other truncated blocks were added
                    # We leave it the user to handle cases where even the truncated block exceeds max_tokens
                    if (
                        await truncated_block.aestimate_tokens(tokenizer=tknizer)
                        <= remaining_tokens
                        or not truncated_blocks
                    ):
                        if not reverse:
                            truncated_blocks.append(truncated_block)
                        else:
                            truncated_blocks.insert(0, truncated_block)
                break  # Stop after reaching max_tokens

        attributes = self.model_dump() | {
            # Overwrite nested blocks
            self.nested_blocks_field_name(): truncated_blocks
        }
        return cls(**attributes)

    @property
    deftemplatable_attributes(self) -> list[str]:
        return [self.nested_blocks_field_name()]

    defget_template_vars(self) -> list[str]:
        vars = []
        for block in self.nested_blocks:
            vars.extend(block.get_template_vars())
        return vars

    defformat_vars(self, **kwargs: Any) -> Self:
        formatted_blocks = []
        for block in self.nested_blocks:
            relevant_kwargs = {
                k: v for k, v in kwargs.items() if k in block.get_template_vars()
            }
            formatted_blocks.append(block.format_vars(**relevant_kwargs))
        attributes = self.model_dump() | {
            # Overwrite nested blocks
            self.nested_blocks_field_name(): formatted_blocks
        }
        return type(self)(**attributes)

```
 |  
| --- | --- |  
###  nested_blocks `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseRecursiveContentBlock.nested_blocks "Permanent link")

```
nested_blocks: []

```

Return the nested content blocks.
###  nested_blocks_field_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseRecursiveContentBlock.nested_blocks_field_name "Permanent link")

```
nested_blocks_field_name() -> 

```

Return the name of the field that contains nested content blocks.
By default, this is "content", but subclasses can override this method
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
816
817
818
819
820
821
822
823
```
 | 
```
@classmethod
defnested_blocks_field_name(cls) -> str:
"""
    Return the name of the field that contains nested content blocks.

    By default, this is "content", but subclasses can override this method
    """
    return "content"

```
 |  
| --- | --- |  
###  can_merge [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseRecursiveContentBlock.can_merge "Permanent link")

```
can_merge(other: ) -> 

```

Check if this block can be merged with another block of the same type.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
```
 | 
```
defcan_merge(self, other: Self) -> bool:
"""Check if this block can be merged with another block of the same type."""
    atts = {
        k: v
        for k, v in self.model_dump().items()
        if k != self.nested_blocks_field_name()
    }
    other_atts = {
        k: v
        for k, v in other.model_dump().items()
        if k != self.nested_blocks_field_name()
    }
    return atts == other_atts

```
 |  
| --- | --- |  
###  amerge `async` `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseRecursiveContentBlock.amerge "Permanent link")

```
amerge(
    splits: ["BaseRecursiveContentBlock"],
    chunk_size: ,
    tokenizer:  | None = None,
) -> ["BaseRecursiveContentBlock"]

```

First merge nested_blocks of consecutive BaseRecursiveContentBlock types based on token estimates
Then, merge consecutive nested content blocks of the same type.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
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
885
886
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
```
 | 
```
@classmethod
async defamerge(
    cls,
    splits: List["BaseRecursiveContentBlock"],
    chunk_size: int,
    tokenizer: Any | None = None,
) -> list["BaseRecursiveContentBlock"]:
"""
    First merge nested_blocks of consecutive BaseRecursiveContentBlock types based on token estimates

    Then, merge consecutive nested content blocks of the same type.
    """
    merged_blocks = []
    cur_blocks: list["BaseRecursiveContentBlock"] = []
    cur_block_tokens = 0

    for split in splits:
        split_tokens = await split.aestimate_tokens(tokenizer=tokenizer)
        can_merge = len(cur_blocks) == 0 or cur_blocks[-1].can_merge(split)
        if cur_block_tokens + split_tokens <= chunk_size and can_merge:
            cur_blocks.append(split)
            cur_block_tokens += split_tokens
        else:
            if cur_blocks:
                attributes = cur_blocks[0].model_dump() | {
                    # Overwrite nested blocks
                    cls.nested_blocks_field_name(): await cls.amerge_nested(
                        nested_blocks=[
                            nested_block
                            for block in cur_blocks
                            for nested_block in block.nested_blocks
                        ],
                        chunk_size=chunk_size,
                        tokenizer=tokenizer,
                    )
                }
                merged_blocks.append(cls(**attributes))
            cur_blocks = [split]
            cur_block_tokens = split_tokens

    if cur_blocks:
        attributes = cur_blocks[0].model_dump() | {
            # Overwrite nested blocks attribute and merge nested blocks of the same type
            cls.nested_blocks_field_name(): await cls.amerge_nested(
                nested_blocks=[
                    nested_block
                    for block in cur_blocks
                    for nested_block in block.nested_blocks
                ],
                chunk_size=chunk_size,
                tokenizer=tokenizer,
            )
        }
        merged_blocks.append(cls(**attributes))

    return merged_blocks

```
 |  
| --- | --- |  
###  aestimate_tokens [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseRecursiveContentBlock.aestimate_tokens "Permanent link")

```
aestimate_tokens(*args: , **kwargs: ) -> 

```

Estimate the number of tokens in this content block.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
930
931
932
933
934
935
936
937
```
 | 
```
async defaestimate_tokens(self, *args: Any, **kwargs: Any) -> int:
"""Estimate the number of tokens in this content block."""
    return sum(
        [
            await block.aestimate_tokens(*args, **kwargs)
            for block in self.nested_blocks
        ]
    )

```
 |  
| --- | --- |  
###  asplit [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseRecursiveContentBlock.asplit "Permanent link")

```
asplit(
    max_tokens: ,
    overlap:  = 0,
    tokenizer:  | None = None,
) -> ["BaseRecursiveContentBlock"]

```

Split the content block into smaller blocks with up to max_tokens tokens each.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
939
940
941
942
943
944
945
946
947
948
949
950
951
952
953
954
955
956
957
958
959
960
961
962
963
964
965
```
 | 
```
async defasplit(
    self, max_tokens: int, overlap: int = 0, tokenizer: Any | None = None
) -> List["BaseRecursiveContentBlock"]:
"""Split the content block into smaller blocks with up to max_tokens tokens each."""
    splits = []

    cls = type(self)
    for block in self.nested_blocks:
        block_tokens = await block.aestimate_tokens(tokenizer=tokenizer)
        if block_tokens <= max_tokens:
            attributes = self.model_dump() | {
                # Overwrite nested blocks
                self.nested_blocks_field_name(): [block]
            }
            splits.append(cls(**attributes))
        else:
            split_blocks = await block.asplit(
                max_tokens=max_tokens, tokenizer=tokenizer
            )
            for split_block in split_blocks:
                attributes = self.model_dump() | {
                    # Overwrite nested blocks
                    self.nested_blocks_field_name(): [split_block]
                }
                splits.append(cls(**attributes))

    return splits

```
 |  
| --- | --- |  
###  atruncate [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.BaseRecursiveContentBlock.atruncate "Permanent link")

```
atruncate(
    max_tokens: ,
    tokenizer:  | None = None,
    reverse:  = False,
) -> "BaseRecursiveContentBlock"

```

Truncate the content block to have at most max_tokens tokens.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
 967
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
```
 | 
```
async defatruncate(
    self, max_tokens: int, tokenizer: Any | None = None, reverse: bool = False
) -> "BaseRecursiveContentBlock":
"""Truncate the content block to have at most max_tokens tokens."""
    tknizer = tokenizer or get_tokenizer()
    current_tokens = 0
    truncated_blocks = []

    cls = type(self)
    for block in (
        self.nested_blocks if not reverse else reversed(self.nested_blocks)
    ):
        block_tokens = await block.aestimate_tokens(tokenizer=tknizer)
        if current_tokens + block_tokens <= max_tokens:
            if not reverse:
                truncated_blocks.append(block)
            else:
                truncated_blocks.insert(0, block)
            current_tokens += block_tokens
        else:
            remaining_tokens = max_tokens - current_tokens
            if remaining_tokens  0:
                truncated_block = await block.atruncate(
                    max_tokens=remaining_tokens, tokenizer=tknizer, reverse=reverse
                )
                # For some block types, truncate may return a block larger than requested
                # However, we still want to include it if no other truncated blocks were added
                # We leave it the user to handle cases where even the truncated block exceeds max_tokens
                if (
                    await truncated_block.aestimate_tokens(tokenizer=tknizer)
                    <= remaining_tokens
                    or not truncated_blocks
                ):
                    if not reverse:
                        truncated_blocks.append(truncated_block)
                    else:
                        truncated_blocks.insert(0, truncated_block)
            break  # Stop after reaching max_tokens

    attributes = self.model_dump() | {
        # Overwrite nested blocks
        self.nested_blocks_field_name(): truncated_blocks
    }
    return cls(**attributes)

```
 |  
| --- | --- |  
##  CitableBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CitableBlock "Permanent link")
Bases: 
Supports providing citable content to LLMs that have built-in citation support.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `block_type`  |  `Literal['citable']`  |  `'citable'`  |  
|  `title`  |  _required_  |  
|  `source`  |  _required_  |  
|  `content`  |  `List[Annotated[TextBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.TextBlock "TextBlock \(llama_index.core.base.llms.types.TextBlock\)") | ImageBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock "ImageBlock \(llama_index.core.base.llms.types.ImageBlock\)") | DocumentBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.DocumentBlock "DocumentBlock \(llama_index.core.base.llms.types.DocumentBlock\)"), FieldInfo]]`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
```
 | 
```
classCitableBlock(BaseRecursiveContentBlock):
"""Supports providing citable content to LLMs that have built-in citation support."""

    block_type: Literal["citable"] = "citable"
    title: str
    source: str
    # TODO: We could maybe expand the types here,
    # limiting for now to known use cases
    content: List[
        Annotated[
            Union[TextBlock, ImageBlock, DocumentBlock],
            Field(discriminator="block_type"),
        ]
    ]

    @field_validator("content", mode="before")
    @classmethod
    defvalidate_content(cls, v: Any) -> Any:
        if isinstance(v, str):
            return [TextBlock(text=v)]
        return v

```
 |  
| --- | --- |  
##  CitationBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CitationBlock "Permanent link")
Bases: 
A representation of cited content from past messages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `block_type`  |  `Literal['citation']`  |  `'citation'`  |  
|  `cited_content`  |   |  _required_  |  
|  `source`  |  _required_  |  
|  `title`  |  _required_  |  
|  `additional_location_info`  |  `Dict[str, int]`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
```
 | 
```
classCitationBlock(BaseRecursiveContentBlock):
"""A representation of cited content from past messages."""

    block_type: Literal["citation"] = "citation"
    cited_content: Annotated[
        Union[TextBlock, ImageBlock], Field(discriminator="block_type")
    ]
    source: str
    title: str
    additional_location_info: Dict[str, int]

    @field_validator("cited_content", mode="before")
    @classmethod
    defvalidate_cited_content(cls, v: Any) -> Any:
        if isinstance(v, str):
            return TextBlock(text=v)
        if isinstance(v, list):
            if len(v) != 1:
                raise ValueError(
                    "CitableBlock content must contain exactly one block when provided as a list."
                )
            value = v[0]
            if isinstance(value, str):
                return TextBlock(text=value)
            else:
                return value
        return v

    @classmethod
    defnested_blocks_field_name(self) -> str:
        return "cited_content"

    defcan_merge(self, other: Self) -> bool:
"""Check if this block can be merged with another block of the same type."""
        # Only merge if cited_content is of the same type and is a TextBlock
        if type(self.cited_content) is type(other.cited_content) and isinstance(
            self.cited_content, TextBlock
        ):
            atts = {k: v for k, v in self.model_dump().items() if k != "cited_content"}
            other_atts = {
                k: v for k, v in other.model_dump().items() if k != "cited_content"
            }
            return atts == other_atts
        return False

```
 |  
| --- | --- |  
###  can_merge [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CitationBlock.can_merge "Permanent link")

```
can_merge(other: ) -> 

```

Check if this block can be merged with another block of the same type.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
```
 | 
```
defcan_merge(self, other: Self) -> bool:
"""Check if this block can be merged with another block of the same type."""
    # Only merge if cited_content is of the same type and is a TextBlock
    if type(self.cited_content) is type(other.cited_content) and isinstance(
        self.cited_content, TextBlock
    ):
        atts = {k: v for k, v in self.model_dump().items() if k != "cited_content"}
        other_atts = {
            k: v for k, v in other.model_dump().items() if k != "cited_content"
        }
        return atts == other_atts
    return False

```
 |  
| --- | --- |  
##  ThinkingBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ThinkingBlock "Permanent link")
Bases: 
A representation of the content streamed from reasoning/thinking processes by LLMs
Because of LLM provider's reliance on signatures for Thought Processes, we do not support merging/splitting/truncating for this block, as we want to preserve the integrity of the content provided by the LLM.
For the same reason, they are also not templatable.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `block_type`  |  `Literal['thinking']`  |  `'thinking'`  |  
|  `content`  |  `str | None`  |  Content of the reasoning/thinking process, if available  |  `None`  |  
|  `num_tokens`  |  `int | None`  |  Number of token used for reasoning/thinking, if available  |  `None`  |  
|  `additional_information`  |  `Dict[str, Any]`  |  Additional information related to the thinking/reasoning process, if available  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
```
 | 
```
classThinkingBlock(BaseContentBlock):
"""
    A representation of the content streamed from reasoning/thinking processes by LLMs

    Because of LLM provider's reliance on signatures for Thought Processes,
    we do not support merging/splitting/truncating for this block, as we want to preserve the integrity of the content
    provided by the LLM.

    For the same reason, they are also not templatable.
    """

    block_type: Literal["thinking"] = "thinking"
    content: Optional[str] = Field(
        description="Content of the reasoning/thinking process, if available",
        default=None,
    )
    num_tokens: Optional[int] = Field(
        description="Number of token used for reasoning/thinking, if available",
        default=None,
    )
    additional_information: Dict[str, Any] = Field(
        description="Additional information related to the thinking/reasoning process, if available",
        default_factory=dict,
    )

    async defaestimate_tokens(self, tokenizer: Any | None = None) -> int:
        return self.num_tokens or await TextBlock(
            text=self.content or ""
        ).aestimate_tokens(tokenizer=tokenizer)

```
 |  
| --- | --- |  
##  ToolCallBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ToolCallBlock "Permanent link")
Bases: 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `block_type`  |  `Literal['tool_call']`  |  `'tool_call'`  |  
|  `tool_call_id`  |  `str | None`  |  ID of the tool call, if provided  |  `None`  |  
|  `tool_name`  |  Name of the called tool  |  _required_  |  
|  `tool_kwargs`  |  `dict[str, Any] | str`  |  Arguments provided to the tool, if available  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
```
 | 
```
classToolCallBlock(BaseContentBlock):
    block_type: Literal["tool_call"] = "tool_call"
    tool_call_id: Optional[str] = Field(
        default=None, description="ID of the tool call, if provided"
    )
    tool_name: str = Field(description="Name of the called tool")
    tool_kwargs: dict[str, Any] | str = Field(
        default_factory=dict,  # type: ignore
        description="Arguments provided to the tool, if available",
    )

    async defaestimate_tokens(self, *args: Any, **kwargs: Any) -> int:
        return await TextBlock(text=self.model_dump_json()).aestimate_tokens(
            *args, **kwargs
        )

```
 |  
| --- | --- |  
##  ChatMessage [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "Permanent link")
Bases: 
Chat message.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `role`  |   |  `<MessageRole.USER: 'user'>`  |  
|  `additional_kwargs`  |  `dict[str, Any]`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
|  `blocks`  |  `list[Annotated[TextBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.TextBlock "TextBlock \(llama_index.core.base.llms.types.TextBlock\)") | ImageBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock "ImageBlock \(llama_index.core.base.llms.types.ImageBlock\)") | AudioBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock "AudioBlock \(llama_index.core.base.llms.types.AudioBlock\)") | VideoBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock "VideoBlock \(llama_index.core.base.llms.types.VideoBlock\)") | DocumentBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.DocumentBlock "DocumentBlock \(llama_index.core.base.llms.types.DocumentBlock\)") | CachePoint[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CachePoint "CachePoint \(llama_index.core.base.llms.types.CachePoint\)") | CitableBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CitableBlock "CitableBlock \(llama_index.core.base.llms.types.CitableBlock\)") | CitationBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CitationBlock "CitationBlock \(llama_index.core.base.llms.types.CitationBlock\)") | ThinkingBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ThinkingBlock "ThinkingBlock \(llama_index.core.base.llms.types.ThinkingBlock\)") | ToolCallBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ToolCallBlock "ToolCallBlock \(llama_index.core.base.llms.types.ToolCallBlock\)"), FieldInfo]]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
1263
1264
1265
1266
1267
1268
1269
1270
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
```
 | 
```
classChatMessage(BaseRecursiveContentBlock):
"""Chat message."""

    role: MessageRole = MessageRole.USER
    additional_kwargs: dict[str, Any] = Field(default_factory=dict)
    blocks: list[ContentBlock] = Field(default_factory=list)

    def__init__(self, /, content: Any | None = None, **data: Any) -> None:
"""
        Keeps backward compatibility with the old `content` field.

        If content was passed and contained text, store a single TextBlock.
        If content was passed and it was a list, assume it's a list of content blocks and store it.
        """
        if content is not None:
            if isinstance(content, str):
                data["blocks"] = [TextBlock(text=content)]
            elif isinstance(content, list):
                data["blocks"] = content

        super().__init__(**data)

    @model_validator(mode="after")
    deflegacy_additional_kwargs_image(self) -> Self:
"""
        Provided for backward compatibility.

        If `additional_kwargs` contains an `images` key, assume the value is a list
        of ImageDocument and convert them into image blocks.
        """
        if documents := self.additional_kwargs.get("images"):
            documents = cast(list[ImageDocument], documents)
            for doc in documents:
                img_base64_bytes = doc.resolve_image(as_base64=True).read()
                self.blocks.append(ImageBlock(image=img_base64_bytes))
        return self

    @classmethod
    defnested_blocks_field_name(self) -> str:
        return "blocks"

    @property
    defcontent(self) -> str | None:
"""
        Keeps backward compatibility with the old `content` field.

        Returns:
            The cumulative content of the TextBlock blocks, None if there are none.

        """
        content_strs = []
        for block in self.blocks:
            if isinstance(block, TextBlock):
                content_strs.append(block.text)

        ct = "\n".join(content_strs) or None
        if ct is None and len(content_strs) == 1:
            return ""
        return ct

    @content.setter
    defcontent(self, content: str) -> None:
"""
        Keeps backward compatibility with the old `content` field.

        Raises:
            ValueError: if blocks contains more than a block, or a block that's not TextBlock.

        """
        if not self.blocks:
            self.blocks = [TextBlock(text=content)]
        elif len(self.blocks) == 1 and isinstance(self.blocks[0], TextBlock):
            self.blocks = [TextBlock(text=content)]
        else:
            raise ValueError(
                "ChatMessage contains multiple blocks, use 'ChatMessage.blocks' instead."
            )

    def__str__(self) -> str:
        return f"{self.role.value}: {self.content}"

    @classmethod
    deffrom_str(
        cls,
        content: str,
        role: Union[MessageRole, str] = MessageRole.USER,
        **kwargs: Any,
    ) -> Self:
        if isinstance(role, str):
            role = MessageRole(role)
        return cls(role=role, blocks=[TextBlock(text=content)], **kwargs)

    def_recursive_serialization(self, value: Any) -> Any:
        if isinstance(value, BaseModel):
            value.model_rebuild()  # ensures all fields are initialized and serializable
            return value.model_dump()  # type: ignore
        if isinstance(value, dict):
            return {
                key: self._recursive_serialization(value)
                for key, value in value.items()
            }
        if isinstance(value, list):
            return [self._recursive_serialization(item) for item in value]

        if isinstance(value, bytes):
            return base64.b64encode(value).decode("utf-8")

        return value

    @field_serializer("additional_kwargs", check_fields=False)
    defserialize_additional_kwargs(self, value: Any, _info: Any) -> Any:
        return self._recursive_serialization(value)

```
 |  
| --- | --- |  
###  content `property` `writable` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage.content "Permanent link")

```
content:  | None

```

Keeps backward compatibility with the old `content` field.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `str | None`  |  The cumulative content of the TextBlock blocks, None if there are none.  |  
###  legacy_additional_kwargs_image [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage.legacy_additional_kwargs_image "Permanent link")

```
legacy_additional_kwargs_image() -> 

```

Provided for backward compatibility.
If `additional_kwargs` contains an `images` key, assume the value is a list of ImageDocument and convert them into image blocks.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
```
 | 
```
@model_validator(mode="after")
deflegacy_additional_kwargs_image(self) -> Self:
"""
    Provided for backward compatibility.

    If `additional_kwargs` contains an `images` key, assume the value is a list
    of ImageDocument and convert them into image blocks.
    """
    if documents := self.additional_kwargs.get("images"):
        documents = cast(list[ImageDocument], documents)
        for doc in documents:
            img_base64_bytes = doc.resolve_image(as_base64=True).read()
            self.blocks.append(ImageBlock(image=img_base64_bytes))
    return self

```
 |  
| --- | --- |  
##  LogProb [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.LogProb "Permanent link")
Bases: `BaseModel`
LogProb of a token.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `token`  |  str(object='') -> str str(bytes_or_buffer[, encoding[, errors]]) -> str Create a new string object from the given object. If encoding or errors is specified, then the object must expose a data buffer that will be decoded using the given encoding and error handler. Otherwise, returns the result of object.**str**() (if defined) or repr(object). encoding defaults to 'utf-8'. errors defaults to 'strict'.  |  `<class 'str'>`  |  
|  `logprob`  |  `float`  |  Convert a string or number to a floating-point number, if possible.  |  `<dynamic>`  |  
|  `bytes`  |  `List[int]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1284
1285
1286
1287
1288
1289
```
 | 
```
classLogProb(BaseModel):
"""LogProb of a token."""

    token: str = Field(default_factory=str)
    logprob: float = Field(default_factory=float)
    bytes: List[int] = Field(default_factory=list)

```
 |  
| --- | --- |  
##  ChatResponse [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatResponse "Permanent link")
Bases: `BaseModel`
Chat response.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `message`  |   |  _required_  |  
|  `raw`  |  `Any | None`  |  `None`  |  
|  `delta`  |  `str | None`  |  `None`  |  
|  `logprobs`  |  `List[List[LogProb[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.LogProb "LogProb \(llama_index.core.base.llms.types.LogProb\)")]] | None`  |  `None`  |  
|  `additional_kwargs`  |  `dict`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1293
1294
1295
1296
1297
1298
1299
1300
1301
1302
1303
```
 | 
```
classChatResponse(BaseModel):
"""Chat response."""

    message: ChatMessage
    raw: Optional[Any] = None
    delta: Optional[str] = None
    logprobs: Optional[List[List[LogProb]]] = None
    additional_kwargs: dict = Field(default_factory=dict)

    def__str__(self) -> str:
        return str(self.message)

```
 |  
| --- | --- |  
##  CompletionResponse [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CompletionResponse "Permanent link")
Bases: `BaseModel`
Completion response.
Fields
text: Text content of the response if not streaming, or if streaming, the current extent of streamed text. additional_kwargs: Additional information on the response(i.e. token counts, function calling information). raw: Optional raw JSON that was parsed to populate text, if relevant. delta: New text that just streamed in (only relevant when streaming).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `text`  |  _required_  |  
|  `additional_kwargs`  |  `dict`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
|  `raw`  |  `Any | None`  |  `None`  |  
|  `logprobs`  |  `List[List[LogProb[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.LogProb "LogProb \(llama_index.core.base.llms.types.LogProb\)")]] | None`  |  `None`  |  
|  `delta`  |  `str | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1311
1312
1313
1314
1315
1316
1317
1318
1319
1320
1321
1322
1323
1324
1325
1326
1327
1328
1329
1330
1331
```
 | 
```
classCompletionResponse(BaseModel):
"""
    Completion response.

    Fields:
        text: Text content of the response if not streaming, or if streaming,
            the current extent of streamed text.
        additional_kwargs: Additional information on the response(i.e. token
            counts, function calling information).
        raw: Optional raw JSON that was parsed to populate text, if relevant.
        delta: New text that just streamed in (only relevant when streaming).
    """

    text: str
    additional_kwargs: dict = Field(default_factory=dict)
    raw: Optional[Any] = None
    logprobs: Optional[List[List[LogProb]]] = None
    delta: Optional[str] = None

    def__str__(self) -> str:
        return self.text

```
 |  
| --- | --- |  
##  LLMMetadata [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.LLMMetadata "Permanent link")
Bases: `BaseModel`
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `context_window`  |  Total number of tokens the model can be input and output for one response.  |  `3900`  |  
|  `num_output`  |  Number of tokens the model can output when generating a response.  |  `256`  |  
|  `is_chat_model`  |  `bool`  |  Set True if the model exposes a chat interface (i.e. can be passed a sequence of messages, rather than text), like OpenAI's /v1/chat/completions endpoint.  |  `False`  |  
|  `is_function_calling_model`  |  `bool`  |  Set True if the model supports function calling messages, similar to OpenAI's function calling API. For example, converting 'Email Anya to see if she wants to get coffee next Friday' to a function call like `send_email(to: string, body: string)`.  |  `False`  |  
|  `model_name`  |  The model's name used for logging, testing, and sanity checking. For some models this can be automatically discerned. For other models, like locally loaded models, this must be manually specified.  |  `'unknown'`  |  
|  `system_role`  |   |  The role this specific LLM providerexpects for system prompt. E.g. 'SYSTEM' for OpenAI, 'CHATBOT' for Cohere  |  `<MessageRole.SYSTEM: 'system'>`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
1352
1353
1354
1355
1356
1357
1358
1359
1360
1361
1362
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
1379
1380
1381
1382
```
 | 
```
classLLMMetadata(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=("pydantic_model_",), arbitrary_types_allowed=True
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description=(
            "Total number of tokens the model can be input and output for one response."
        ),
    )
    num_output: int = Field(
        default=DEFAULT_NUM_OUTPUTS,
        description="Number of tokens the model can output when generating a response.",
    )
    is_chat_model: bool = Field(
        default=False,
        description=(
            "Set True if the model exposes a chat interface (i.e. can be passed a"
            " sequence of messages, rather than text), like OpenAI's"
            " /v1/chat/completions endpoint."
        ),
    )
    is_function_calling_model: bool = Field(
        default=False,
        # SEE: https://openai.com/blog/function-calling-and-other-api-updates
        description=(
            "Set True if the model supports function calling messages, similar to"
            " OpenAI's function calling API. For example, converting 'Email Anya to"
            " see if she wants to get coffee next Friday' to a function call like"
            " `send_email(to: string, body: string)`."
        ),
    )
    model_name: str = Field(
        default="unknown",
        description=(
            "The model's name used for logging, testing, and sanity checking. For some"
            " models this can be automatically discerned. For other models, like"
            " locally loaded models, this must be manually specified."
        ),
    )
    system_role: MessageRole = Field(
        default=MessageRole.SYSTEM,
        description="The role this specific LLM provider"
        "expects for system prompt. E.g. 'SYSTEM' for OpenAI, 'CHATBOT' for Cohere",
    )

```
 |  
| --- | --- |
