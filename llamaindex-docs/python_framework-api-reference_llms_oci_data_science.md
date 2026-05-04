# Oci data science
##  OCIDataScience [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience "Permanent link")
Bases: `FunctionCallingLLM`
LLM deployed on OCI Data Science Model Deployment.
**Setup:** Install `oracle-ads` and `llama-index-llms-oci-data-science`.

```
```bash
pip install -U oracle-ads llama-index-llms-oci-data-science
```

Use `ads.set_auth()` to configure authentication.
For example, to use OCI resource_principal for authentication:

```python
import ads
ads.set_auth("resource_principal")
```

For more details on authentication, see:
https://accelerated-data-science.readthedocs.io/en/latest/user_guide/cli/authentication.html

Make sure to have the required policies to access the OCI Data
Science Model Deployment endpoint. See:
https://docs.oracle.com/en-us/iaas/data-science/using/model-dep-policies-auth.htm

To learn more about deploying LLM models in OCI Data Science, see:
https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions-model-deploy.htm

```

**Examples:**

```
**Basic Usage:**

```python
from llama_index.llms.oci_data_science import OCIDataScience
import ads
ads.set_auth(auth="security_token", profile="OC1")

llm = OCIDataScience(
    endpoint="https://<MD_OCID>/predict",
    model="odsc-llm",
)
prompt = "What is the capital of France?"
response = llm.complete(prompt)
print(response)
```

**Custom Parameters:**

```python
llm = OCIDataScience(
    endpoint="https://<MD_OCID>/predict",
    model="odsc-llm",
    temperature=0.7,
    max_tokens=150,
    additional_kwargs={"top_p": 0.9},
)
```

**Using Chat Interface:**

```python
messages = [
    ChatMessage(role="user", content="Tell me a joke."),
    ChatMessage(role="assistant", content="Why did the chicken cross the road?"),
    ChatMessage(role="user", content="I don't know, why?"),
]

chat_response = llm.chat(messages)
print(chat_response)
```

**Streaming Completion:**

```python
for chunk in llm.stream_complete("Once upon a time"):
    print(chunk.delta, end="")
```

**Asynchronous Chat:**

```python
import asyncio

async def async_chat():
    messages = [
        ChatMessage(role="user", content="What's the weather like today?")
    ]
    response = await llm.achat(messages)
    print(response)

asyncio.run(async_chat())
```

**Using Tools (Function Calling):**

```python
from llama_index.llms.oci_data_science import OCIDataScience
from llama_index.core.tools import FunctionTool
import ads
ads.set_auth(auth="security_token", profile="OC1")

def multiply(a: float, b: float) -> float:
    return a * b

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def divide(a: float, b: float) -> float:
    return a / b


multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)
sub_tool = FunctionTool.from_defaults(fn=subtract)
divide_tool = FunctionTool.from_defaults(fn=divide)

llm = OCIDataScience(
    endpoint="https://<MD_OCID>/predict",
    model="odsc-llm",
    temperature=0.7,
    max_tokens=150,
    additional_kwargs={"top_p": 0.9},
)

response = llm.chat_with_tools(
    user_msg="Calculate the result of 2 + 2.",
    tools=[multiply_tool, add_tool, sub_tool, divide_tool],
)
print(response)
```
**Using Dedicated Streaming endpoint**
```python
from llama_index.llms.oci_data_science import OCIDataScience
import ads
ads.set_auth(auth="security_token", profile="OC1")

llm = OCIDataScience(
    endpoint="https://<MD_OCID>/predictWithResponseStream",
    model="odsc-llm",
)
prompt = "What is the capital of France?"
response = llm.stream_complete(prompt)
for chunk in response:
    print(chunk.delta, end="")
print(response)
```

```
Source code in `llama-index-integrations/llms/llama-index-llms-oci-data-science/llama_index/llms/oci_data_science/base.py`  
| 
```
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
```
 | 
```
classOCIDataScience(FunctionCallingLLM):
"""
    LLM deployed on OCI Data Science Model Deployment.

    **Setup:**
        Install ``oracle-ads`` and ``llama-index-llms-oci-data-science``.

        ```bash
        pip install -U oracle-ads llama-index-llms-oci-data-science
        ```

        Use `ads.set_auth()` to configure authentication.
        For example, to use OCI resource_principal for authentication:

        ```python
        import ads
        ads.set_auth("resource_principal")
        ```

        For more details on authentication, see:
        https://accelerated-data-science.readthedocs.io/en/latest/user_guide/cli/authentication.html

        Make sure to have the required policies to access the OCI Data
        Science Model Deployment endpoint. See:
        https://docs.oracle.com/en-us/iaas/data-science/using/model-dep-policies-auth.htm

        To learn more about deploying LLM models in OCI Data Science, see:
        https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions-model-deploy.htm


    **Examples:**

        **Basic Usage:**

        ```python
        from llama_index.llms.oci_data_science import OCIDataScience
        import ads
        ads.set_auth(auth="security_token", profile="OC1")

        llm = OCIDataScience(
            endpoint="https://<MD_OCID>/predict",
            model="odsc-llm",

        prompt = "What is the capital of France?"
        response = llm.complete(prompt)
        print(response)
        ```

        **Custom Parameters:**

        ```python
        llm = OCIDataScience(
            endpoint="https://<MD_OCID>/predict",
            model="odsc-llm",
            temperature=0.7,
            max_tokens=150,
            additional_kwargs={"top_p": 0.9},

        ```

        **Using Chat Interface:**

        ```python
        messages = [
            ChatMessage(role="user", content="Tell me a joke."),
            ChatMessage(role="assistant", content="Why did the chicken cross the road?"),
            ChatMessage(role="user", content="I don't know, why?"),


        chat_response = llm.chat(messages)
        print(chat_response)
        ```

        **Streaming Completion:**

        ```python
        for chunk in llm.stream_complete("Once upon a time"):
            print(chunk.delta, end="")
        ```

        **Asynchronous Chat:**

        ```python
        import asyncio

        async def async_chat():
            messages = [
                ChatMessage(role="user", content="What's the weather like today?")

            response = await llm.achat(messages)
            print(response)

        asyncio.run(async_chat())
        ```

        **Using Tools (Function Calling):**

        ```python
        from llama_index.llms.oci_data_science import OCIDataScience
        from llama_index.core.tools import FunctionTool
        import ads
        ads.set_auth(auth="security_token", profile="OC1")

        def multiply(a: float, b: float) -> float:
            return a * b

        def add(a: float, b: float) -> float:
            return a + b

        def subtract(a: float, b: float) -> float:
            return a - b

        def divide(a: float, b: float) -> float:
            return a / b


        multiply_tool = FunctionTool.from_defaults(fn=multiply)
        add_tool = FunctionTool.from_defaults(fn=add)
        sub_tool = FunctionTool.from_defaults(fn=subtract)
        divide_tool = FunctionTool.from_defaults(fn=divide)

        llm = OCIDataScience(
            endpoint="https://<MD_OCID>/predict",
            model="odsc-llm",
            temperature=0.7,
            max_tokens=150,
            additional_kwargs={"top_p": 0.9},


        response = llm.chat_with_tools(
            user_msg="Calculate the result of 2 + 2.",
            tools=[multiply_tool, add_tool, sub_tool, divide_tool],

        print(response)
        ```
        **Using Dedicated Streaming endpoint**
        ```python
        from llama_index.llms.oci_data_science import OCIDataScience
        import ads
        ads.set_auth(auth="security_token", profile="OC1")

        llm = OCIDataScience(
            endpoint="https://<MD_OCID>/predictWithResponseStream",
            model="odsc-llm",

        prompt = "What is the capital of France?"
        response = llm.stream_complete(prompt)
        for chunk in response:
            print(chunk.delta, end="")
        print(response)
        ```

    """

    endpoint: str = Field(
        default=None, description="The URI of the endpoint from the deployed model."
    )

    auth: Dict[str, Any] = Field(
        default_factory=dict,
        exclude=True,
        description=(
            "The authentication dictionary used for OCI API requests. Default is an empty dictionary. "
            "If not provided, it will be autogenerated based on the environment variables. "
            "https://accelerated-data-science.readthedocs.io/en/latest/user_guide/cli/authentication.html."
        ),
    )
    model: Optional[str] = Field(
        default=DEFAULT_MODEL,
        description="The OCI Data Science default model. Defaults to `odsc-llm`.",
    )
    temperature: Optional[float] = Field(
        default=DEFAULT_TEMPERATURE,
        description="A non-negative float that tunes the degree of randomness in generation.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: Optional[int] = Field(
        default=DEFAULT_MAX_TOKENS,
        description="Denotes the number of tokens to predict per generation.",
        gt=0,
    )
    timeout: float = Field(
        default=DEFAULT_TIMEOUT, description="The timeout to use in seconds.", ge=0
    )
    max_retries: int = Field(
        default=DEFAULT_MAX_RETRIES,
        description="The maximum number of API retries.",
        ge=0,
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model.",
        gt=0,
    )
    is_chat_model: bool = Field(
        default=True,
        description="If the model exposes a chat interface.",
    )
    is_function_calling_model: bool = Field(
        default=True,
        description="If the model supports function calling messages.",
    )
    additional_kwargs: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional kwargs for the OCI Data Science AI request.",
    )
    strict: bool = Field(
        default=False,
        description="Whether to use strict mode for invoking tools/using schemas.",
    )
    default_headers: Optional[Dict[str, str]] = Field(
        default=None, description="The default headers for API requests."
    )

    _client: Client = PrivateAttr()
    _async_client: AsyncClient = PrivateAttr()

    def__init__(
        self,
        endpoint: str,
        auth: Optional[Dict[str, Any]] = None,
        model: Optional[str] = DEFAULT_MODEL,
        temperature: Optional[float] = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = DEFAULT_MAX_TOKENS,
        context_window: Optional[int] = DEFAULT_CONTEXT_WINDOW,
        timeout: Optional[float] = DEFAULT_TIMEOUT,
        max_retries: Optional[int] = DEFAULT_MAX_RETRIES,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        callback_manager: Optional[CallbackManager] = None,
        is_chat_model: Optional[bool] = True,
        is_function_calling_model: Optional[bool] = True,
        default_headers: Optional[Dict[str, str]] = None,
        # base class
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        strict: bool = False,
        **kwargs,
    ) -> None:
"""
        Initialize the OCIDataScience LLM class.

        Args:
            endpoint (str): The URI of the endpoint from the deployed model.
            auth (Optional[Dict[str, Any]]): Authentication dictionary for OCI API requests.
            model (Optional[str]): The model name to use. Defaults to `odsc-llm`.
            temperature (Optional[float]): Controls the randomness in generation.
            max_tokens (Optional[int]): Number of tokens to predict per generation.
            context_window (Optional[int]): Maximum number of context tokens for the model.
            timeout (Optional[float]): Timeout for API requests in seconds.
            max_retries (Optional[int]): Maximum number of API retries.
            additional_kwargs (Optional[Dict[str, Any]]): Additional parameters for the API request.
            callback_manager (Optional[CallbackManager]): Callback manager for LLM.
            is_chat_model (Optional[bool]): If the model exposes a chat interface. Defaults to `True`.
            is_function_calling_model (Optional[bool]): If the model supports function calling messages. Defaults to `True`.
            default_headers (Optional[Dict[str, str]]): The default headers for API requests.
            system_prompt (Optional[str]): System prompt to use.
            messages_to_prompt (Optional[Callable]): Function to convert messages to prompt.
            completion_to_prompt (Optional[Callable]): Function to convert completion to prompt.
            pydantic_program_mode (PydanticProgramMode): Pydantic program mode.
            output_parser (Optional[BaseOutputParser]): Output parser for the LLM.
            strict (bool): Whether to use strict mode for invoking tools/using schemas.
            **kwargs: Additional keyword arguments.

        """
        super().__init__(
            endpoint=endpoint,
            model=model,
            auth=auth,
            temperature=temperature,
            context_window=context_window,
            max_tokens=max_tokens,
            timeout=timeout,
            max_retries=max_retries,
            additional_kwargs=additional_kwargs or {},
            callback_manager=callback_manager or CallbackManager([]),
            is_chat_model=is_chat_model,
            is_function_calling_model=is_function_calling_model,
            default_headers=default_headers,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            strict=strict,
            **kwargs,
        )

        self._client: Client = None
        self._async_client: AsyncClient = None

        logger.debug(
            f"Initialized OCIDataScience LLM with endpoint: {self.endpoint} and model: {self.model}"
        )

    @model_validator(mode="before")
    # @_validate_dependency
    defvalidate_env(cls, values: Dict[str, Any]) -> Dict[str, Any]:
"""Validate the environment and dependencies."""
        return values

    @property
    defclient(self) -> Client:
"""
        Synchronous client for interacting with the OCI Data Science Model Deployment endpoint.

        Returns:
            Client: The synchronous client instance.

        """
        if self._client is None:
            self._client = Client(
                endpoint=self.endpoint,
                auth=self.auth,
                retries=self.max_retries,
                timeout=self.timeout,
            )
        return self._client

    @property
    defasync_client(self) -> AsyncClient:
"""
        Asynchronous client for interacting with the OCI Data Science Model Deployment endpoint.

        Returns:
            AsyncClient: The asynchronous client instance.

        """
        if self._async_client is None:
            self._async_client = AsyncClient(
                endpoint=self.endpoint,
                auth=self.auth,
                retries=self.max_retries,
                timeout=self.timeout,
            )
        return self._async_client

    @classmethod
    defclass_name(cls) -> str:
"""
        Return the class name.

        Returns:
            str: The name of the class.

        """
        return "OCIDataScience_LLM"

    @property
    defmetadata(self) -> LLMMetadata:
"""
        Return the metadata of the LLM.

        Returns:
            LLMMetadata: The metadata of the LLM.

        """
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_tokens or -1,
            is_chat_model=self.is_chat_model,
            is_function_calling_model=self.is_function_calling_model,
            model_name=self.model,
        )

    def_model_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
"""
        Get model-specific parameters for the API request.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            Dict[str, Any]: The combined model parameters.

        """
        base_kwargs = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        return {**base_kwargs, **self.additional_kwargs, **kwargs}

    def_prepare_headers(
        self,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
"""
        Construct and return the headers for a request.

        Args:
            headers (Optional[Dict[str, str]]): HTTP headers to include in the request.

        Returns:
            Dict[str, str]: The prepared headers.

        """
        return {**(self.default_headers or {}), **(headers or {})}

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
"""
        Generate a completion for the given prompt.

        Args:
            prompt (str): The prompt to generate a completion for.
            formatted (bool): Whether the prompt is formatted.
            **kwargs: Additional keyword arguments.

        Returns:
            CompletionResponse: The response from the LLM.

        """
        logger.debug(f"Calling complete with prompt: {prompt}")
        response = self.client.generate(
            prompt=prompt,
            payload=self._model_kwargs(**kwargs),
            headers=self._prepare_headers(kwargs.pop("headers", {})),
            stream=False,
        )

        logger.debug(f"Received response: {response}")
        try:
            choice = response["choices"][0]
            text = choice.get("text", "")
            logprobs = _from_completion_logprobs_dict(choice.get("logprobs") or {})

            return CompletionResponse(
                text=text,
                raw=response,
                logprobs=logprobs,
                additional_kwargs=_get_response_token_counts(response),
            )
        except (IndexError, KeyError, TypeError) as e:
            raise ValueError(f"Failed to parse response: {e!s}") frome

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
"""
        Stream the completion for the given prompt.

        Args:
            prompt (str): The prompt to generate a completion for.
            formatted (bool): Whether the prompt is formatted.
            **kwargs: Additional keyword arguments.

        Yields:
            CompletionResponse: The streamed response from the LLM.

        """
        logger.debug(f"Starting stream_complete with prompt: {prompt}")
        text = ""
        for response in self.client.generate(
            prompt=prompt,
            payload=self._model_kwargs(**kwargs),
            headers=self._prepare_headers(kwargs.pop("headers", {})),
            stream=True,
        ):
            logger.debug(f"Received chunk: {response}")
            if len(response.get("choices", []))  0:
                delta = response["choices"][0].get("text")
                if delta is None:
                    delta = ""
            else:
                delta = ""
            text += delta

            yield CompletionResponse(
                delta=delta,
                text=text,
                raw=response,
                additional_kwargs=_get_response_token_counts(response),
            )

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
"""
        Generate a chat completion based on the input messages.

        Args:
            messages (Sequence[ChatMessage]): A sequence of chat messages.
            **kwargs: Additional keyword arguments.

        Returns:
            ChatResponse: The chat response from the LLM.

        """
        logger.debug(f"Calling chat with messages: {messages}")
        response = self.client.chat(
            messages=_to_message_dicts(
                messages=messages, drop_none=kwargs.pop("drop_none", False)
            ),
            payload=self._model_kwargs(**kwargs),
            headers=self._prepare_headers(kwargs.pop("headers", {})),
            stream=False,
        )

        logger.debug(f"Received chat response: {response}")
        try:
            choice = response["choices"][0]
            message = _from_message_dict(choice.get("message", ""))
            logprobs = _from_token_logprob_dicts(
                (choice.get("logprobs") or {}).get("content", [])
            )
            return ChatResponse(
                message=message,
                raw=response,
                logprobs=logprobs,
                additional_kwargs=_get_response_token_counts(response),
            )
        except (IndexError, KeyError, TypeError) as e:
            raise ValueError(f"Failed to parse response: {e!s}") frome

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
"""
        Stream the chat completion based on the input messages.

        Args:
            messages (Sequence[ChatMessage]): A sequence of chat messages.
            **kwargs: Additional keyword arguments.

        Yields:
            ChatResponse: The streamed chat response from the LLM.

        """
        logger.debug(f"Starting stream_chat with messages: {messages}")
        content = ""
        is_function = False
        tool_calls = []
        for response in self.client.chat(
            messages=_to_message_dicts(
                messages=messages, drop_none=kwargs.pop("drop_none", False)
            ),
            payload=self._model_kwargs(**kwargs),
            headers=self._prepare_headers(kwargs.pop("headers", {})),
            stream=True,
        ):
            logger.debug(f"Received chat chunk: {response}")
            if len(response.get("choices", []))  0:
                delta = response["choices"][0].get("delta") or {}
            else:
                delta = {}

            # Check if this chunk is the start of a function call
            if delta.get("tool_calls"):
                is_function = True

            # Update using deltas
            role = delta.get("role") or MessageRole.ASSISTANT
            content_delta = delta.get("content") or ""
            content += content_delta

            additional_kwargs = {}
            if is_function:
                tool_calls = _update_tool_calls(tool_calls, delta.get("tool_calls"))
                if tool_calls:
                    additional_kwargs["tool_calls"] = tool_calls

            yield ChatResponse(
                message=ChatMessage(
                    role=role,
                    content=content,
                    additional_kwargs=additional_kwargs,
                ),
                delta=content_delta,
                raw=response,
                additional_kwargs=_get_response_token_counts(response),
            )

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
"""
        Asynchronously generate a completion for the given prompt.

        Args:
            prompt (str): The prompt to generate a completion for.
            formatted (bool): Whether the prompt is formatted.
            **kwargs: Additional keyword arguments.

        Returns:
            CompletionResponse: The response from the LLM.

        """
        logger.debug(f"Calling acomplete with prompt: {prompt}")
        response = await self.async_client.generate(
            prompt=prompt,
            payload=self._model_kwargs(**kwargs),
            headers=self._prepare_headers(kwargs.pop("headers", {})),
            stream=False,
        )

        logger.debug(f"Received async response: {response}")
        try:
            choice = response["choices"][0]
            text = choice.get("text", "")
            logprobs = _from_completion_logprobs_dict(choice.get("logprobs", {}) or {})

            return CompletionResponse(
                text=text,
                raw=response,
                logprobs=logprobs,
                additional_kwargs=_get_response_token_counts(response),
            )
        except (IndexError, KeyError, TypeError) as e:
            raise ValueError(f"Failed to parse response: {e!s}") frome

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
"""
        Asynchronously stream the completion for the given prompt.

        Args:
            prompt (str): The prompt to generate a completion for.
            formatted (bool): Whether the prompt is formatted.
            **kwargs: Additional keyword arguments.

        Yields:
            CompletionResponse: The streamed response from the LLM.

        """

        async defgen() -> CompletionResponseAsyncGen:
            logger.debug(f"Starting astream_complete with prompt: {prompt}")
            text = ""

            async for response in await self.async_client.generate(
                prompt=prompt,
                payload=self._model_kwargs(**kwargs),
                headers=self._prepare_headers(kwargs.pop("headers", {})),
                stream=True,
            ):
                logger.debug(f"Received async chunk: {response}")
                if len(response.get("choices", []))  0:
                    delta = response["choices"][0].get("text")
                    if delta is None:
                        delta = ""
                else:
                    delta = ""
                text += delta

                yield CompletionResponse(
                    delta=delta,
                    text=text,
                    raw=response,
                    additional_kwargs=_get_response_token_counts(response),
                )

        return gen()

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
"""
        Asynchronously generate a chat completion based on the input messages.

        Args:
            messages (Sequence[ChatMessage]): A sequence of chat messages.
            **kwargs: Additional keyword arguments.

        Returns:
            ChatResponse: The chat response from the LLM.

        """
        logger.debug(f"Calling achat with messages: {messages}")
        response = await self.async_client.chat(
            messages=_to_message_dicts(
                messages=messages, drop_none=kwargs.pop("drop_none", False)
            ),
            payload=self._model_kwargs(**kwargs),
            headers=self._prepare_headers(kwargs.pop("headers", {})),
            stream=False,
        )

        logger.debug(f"Received async chat response: {response}")
        try:
            choice = response["choices"][0]
            message = _from_message_dict(choice.get("message", ""))
            logprobs = _from_token_logprob_dicts(
                (choice.get("logprobs") or {}).get("content", {})
            )
            return ChatResponse(
                message=message,
                raw=response,
                logprobs=logprobs,
                additional_kwargs=_get_response_token_counts(response),
            )
        except (IndexError, KeyError, TypeError) as e:
            raise ValueError(f"Failed to parse response: {e!s}") frome

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
"""
        Asynchronously stream the chat completion based on the input messages.

        Args:
            messages (Sequence[ChatMessage]): A sequence of chat messages.
            **kwargs: Additional keyword arguments.

        Yields:
            ChatResponse: The streamed chat response from the LLM.

        """

        async defgen() -> ChatResponseAsyncGen:
            logger.debug(f"Starting astream_chat with messages: {messages}")
            content = ""
            is_function = False
            tool_calls = []
            async for response in await self.async_client.chat(
                messages=_to_message_dicts(
                    messages=messages, drop_none=kwargs.pop("drop_none", False)
                ),
                payload=self._model_kwargs(**kwargs),
                headers=self._prepare_headers(kwargs.pop("headers", {})),
                stream=True,
            ):
                logger.debug(f"Received async chat chunk: {response}")
                if len(response.get("choices", []))  0:
                    delta = response["choices"][0].get("delta") or {}
                else:
                    delta = {}

                # Check if this chunk is the start of a function call
                if delta.get("tool_calls"):
                    is_function = True

                # Update using deltas
                role = delta.get("role") or MessageRole.ASSISTANT
                content_delta = delta.get("content") or ""
                content += content_delta

                additional_kwargs = {}
                if is_function:
                    tool_calls = _update_tool_calls(tool_calls, delta.get("tool_calls"))
                    if tool_calls:
                        additional_kwargs["tool_calls"] = tool_calls

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                        additional_kwargs=additional_kwargs,
                    ),
                    delta=content_delta,
                    raw=response,
                    additional_kwargs=_get_response_token_counts(response),
                )

        return gen()

    def_prepare_chat_with_tools(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,
        tool_choice: Optional[Union[str, dict]] = None,
        strict: Optional[bool] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
"""
        Prepare the chat input with tools for function calling.

        Args:
            tools (List[BaseTool]): A list of tools to use.
            user_msg (Optional[Union[str, ChatMessage]]): The user's message.
            chat_history (Optional[List[ChatMessage]]): The chat history.
            verbose (bool): Whether to output verbose logs.
            allow_parallel_tool_calls (bool): Whether to allow parallel tool calls.
            tool_required (bool): Whether to require a tool call. tool_choice supersedes this if provided.
            tool_choice (Union[str, dict]): Tool choice strategy.
            strict (Optional[bool]): Whether to enforce strict mode.
            **kwargs: Additional keyword arguments.

        Returns:
            Dict[str, Any]: The prepared parameters for the chat request.

        """
        tool_specs = [tool.metadata.to_openai_tool() for tool in tools]

        logger.debug(
            f"Preparing chat with tools. Tools: {tool_specs}, User message: {user_msg}, "
            f"Chat history: {chat_history}"
        )

        # Determine strict mode
        strict = strict or self.strict

        if self.metadata.is_function_calling_model:
            for tool_spec in tool_specs:
                if tool_spec["type"] == "function":
                    if strict:
                        tool_spec["function"]["strict"] = strict
                    tool_spec["function"]["parameters"]["additionalProperties"] = False

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        messages = chat_history or []
        if user_msg:
            messages.append(user_msg)

        return {
            "messages": messages,
            "tools": tool_specs or None,
            "tool_choice": (
                _resolve_tool_choice(tool_choice, tool_required) if tool_specs else None
            ),
            **kwargs,
        }

    def_validate_chat_with_tools_response(
        self,
        response: ChatResponse,
        tools: List["BaseTool"],
        allow_parallel_tool_calls: bool = False,
        **kwargs: Any,
    ) -> ChatResponse:
"""
        Validate the response from chat_with_tools.

        Args:
            response (ChatResponse): The chat response to validate.
            tools (List[BaseTool]): A list of tools used.
            allow_parallel_tool_calls (bool): Whether parallel tool calls are allowed.
            **kwargs: Additional keyword arguments.

        Returns:
            ChatResponse: The validated chat response.

        """
        if not allow_parallel_tool_calls:
            # Ensures that the 'tool_calls' in the response contain only a single tool call.
            tool_calls = response.message.additional_kwargs.get("tool_calls", [])
            if len(tool_calls)  1:
                logger.warning(
                    "Multiple tool calls detected but parallel tool calls are not allowed. "
                    "Limiting to the first tool call."
                )
                response.message.additional_kwargs["tool_calls"] = [tool_calls[0]]
        return response

    defget_tool_calls_from_response(
        self,
        response: ChatResponse,
        error_on_no_tool_call: bool = True,
        **kwargs: Any,
    ) -> List[ToolSelection]:
"""
        Extract tool calls from the chat response.

        Args:
            response (ChatResponse): The chat response containing tool calls.
            error_on_no_tool_call (bool): Whether to raise an error if no tool calls are found.
            **kwargs: Additional keyword arguments.

        Returns:
            List[ToolSelection]: A list of tool selections extracted from the response.

        Raises:
            ValueError: If no tool calls are found and error_on_no_tool_call is True.

        """
        tool_calls = response.message.additional_kwargs.get("tool_calls", [])
        logger.debug(f"Getting tool calls from response: {tool_calls}")

        if len(tool_calls)  1:
            if error_on_no_tool_call:
                raise ValueError(
                    f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
                )
            else:
                return []

        tool_selections = []
        for tool_call in tool_calls:
            if tool_call.get("type") != "function":
                raise ValueError(f"Invalid tool type detected: {tool_call.get('type')}")

            # Handle both complete and partial JSON
            try:
                argument_dict = parse_partial_json(
                    tool_call.get("function", {}).get("arguments", {})
                )
            except ValueError as e:
                logger.debug(f"Failed to parse tool call arguments: {e!s}")
                argument_dict = {}

            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.get("id"),
                    tool_name=tool_call.get("function", {}).get("name"),
                    tool_kwargs=argument_dict,
                )
            )

        logger.debug(
            f"Extracted tool calls: {[tool_selection.model_dump()fortool_selectionintool_selections]}"
        )
        return tool_selections

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.client "Permanent link")

```
client: Client

```

Synchronous client for interacting with the OCI Data Science Model Deployment endpoint.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Client`  |  `Client`  |  The synchronous client instance.  |  
###  async_client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.async_client "Permanent link")

```
async_client: AsyncClient

```

Asynchronous client for interacting with the OCI Data Science Model Deployment endpoint.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `AsyncClient`  |  `AsyncClient`  |  The asynchronous client instance.  |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.metadata "Permanent link")

```
metadata: 

```

Return the metadata of the LLM.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `LLMMetadata`  |   |  The metadata of the LLM.  |  
###  validate_env [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.validate_env "Permanent link")

```
validate_env(values: [, ]) -> [, ]

```

Validate the environment and dependencies.
Source code in `llama-index-integrations/llms/llama-index-llms-oci-data-science/llama_index/llms/oci_data_science/base.py`  
| 
```
352
353
354
355
356
```
 | 
```
@model_validator(mode="before")
# @_validate_dependency
defvalidate_env(cls, values: Dict[str, Any]) -> Dict[str, Any]:
"""Validate the environment and dependencies."""
    return values

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.class_name "Permanent link")

```
class_name() -> 

```

Return the class name.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The name of the class.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-oci-data-science/llama_index/llms/oci_data_science/base.py`  
| 
```
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
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""
    Return the class name.

    Returns:
        str: The name of the class.

    """
    return "OCIDataScience_LLM"

```
 |  
| --- | --- |  
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.complete "Permanent link")

```
complete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Generate a completion for the given prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The prompt to generate a completion for.  |  _required_  |  
|  `formatted`  |  `bool`  |  Whether the prompt is formatted.  |  `False`  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `CompletionResponse`  |   |  The response from the LLM.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-oci-data-science/llama_index/llms/oci_data_science/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defcomplete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponse:
"""
    Generate a completion for the given prompt.

    Args:
        prompt (str): The prompt to generate a completion for.
        formatted (bool): Whether the prompt is formatted.
        **kwargs: Additional keyword arguments.

    Returns:
        CompletionResponse: The response from the LLM.

    """
    logger.debug(f"Calling complete with prompt: {prompt}")
    response = self.client.generate(
        prompt=prompt,
        payload=self._model_kwargs(**kwargs),
        headers=self._prepare_headers(kwargs.pop("headers", {})),
        stream=False,
    )

    logger.debug(f"Received response: {response}")
    try:
        choice = response["choices"][0]
        text = choice.get("text", "")
        logprobs = _from_completion_logprobs_dict(choice.get("logprobs") or {})

        return CompletionResponse(
            text=text,
            raw=response,
            logprobs=logprobs,
            additional_kwargs=_get_response_token_counts(response),
        )
    except (IndexError, KeyError, TypeError) as e:
        raise ValueError(f"Failed to parse response: {e!s}") frome

```
 |  
| --- | --- |  
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.stream_complete "Permanent link")

```
stream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseGen

```

Stream the completion for the given prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The prompt to generate a completion for.  |  _required_  |  
|  `formatted`  |  `bool`  |  Whether the prompt is formatted.  |  `False`  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `CompletionResponse`  |  `CompletionResponseGen`  |  The streamed response from the LLM.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-oci-data-science/llama_index/llms/oci_data_science/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defstream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseGen:
"""
    Stream the completion for the given prompt.

    Args:
        prompt (str): The prompt to generate a completion for.
        formatted (bool): Whether the prompt is formatted.
        **kwargs: Additional keyword arguments.

    Yields:
        CompletionResponse: The streamed response from the LLM.

    """
    logger.debug(f"Starting stream_complete with prompt: {prompt}")
    text = ""
    for response in self.client.generate(
        prompt=prompt,
        payload=self._model_kwargs(**kwargs),
        headers=self._prepare_headers(kwargs.pop("headers", {})),
        stream=True,
    ):
        logger.debug(f"Received chunk: {response}")
        if len(response.get("choices", []))  0:
            delta = response["choices"][0].get("text")
            if delta is None:
                delta = ""
        else:
            delta = ""
        text += delta

        yield CompletionResponse(
            delta=delta,
            text=text,
            raw=response,
            additional_kwargs=_get_response_token_counts(response),
        )

```
 |  
| --- | --- |  
###  chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.chat "Permanent link")

```
chat(
    messages: Sequence[], **kwargs: 
) -> 

```

Generate a chat completion based on the input messages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  A sequence of chat messages.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `ChatResponse`  |   |  The chat response from the LLM.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-oci-data-science/llama_index/llms/oci_data_science/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
"""
    Generate a chat completion based on the input messages.

    Args:
        messages (Sequence[ChatMessage]): A sequence of chat messages.
        **kwargs: Additional keyword arguments.

    Returns:
        ChatResponse: The chat response from the LLM.

    """
    logger.debug(f"Calling chat with messages: {messages}")
    response = self.client.chat(
        messages=_to_message_dicts(
            messages=messages, drop_none=kwargs.pop("drop_none", False)
        ),
        payload=self._model_kwargs(**kwargs),
        headers=self._prepare_headers(kwargs.pop("headers", {})),
        stream=False,
    )

    logger.debug(f"Received chat response: {response}")
    try:
        choice = response["choices"][0]
        message = _from_message_dict(choice.get("message", ""))
        logprobs = _from_token_logprob_dicts(
            (choice.get("logprobs") or {}).get("content", [])
        )
        return ChatResponse(
            message=message,
            raw=response,
            logprobs=logprobs,
            additional_kwargs=_get_response_token_counts(response),
        )
    except (IndexError, KeyError, TypeError) as e:
        raise ValueError(f"Failed to parse response: {e!s}") frome

```
 |  
| --- | --- |  
###  stream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.stream_chat "Permanent link")

```
stream_chat(
    messages: Sequence[], **kwargs: 
) -> ChatResponseGen

```

Stream the chat completion based on the input messages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  A sequence of chat messages.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `ChatResponse`  |  `ChatResponseGen`  |  The streamed chat response from the LLM.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-oci-data-science/llama_index/llms/oci_data_science/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
defstream_chat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponseGen:
"""
    Stream the chat completion based on the input messages.

    Args:
        messages (Sequence[ChatMessage]): A sequence of chat messages.
        **kwargs: Additional keyword arguments.

    Yields:
        ChatResponse: The streamed chat response from the LLM.

    """
    logger.debug(f"Starting stream_chat with messages: {messages}")
    content = ""
    is_function = False
    tool_calls = []
    for response in self.client.chat(
        messages=_to_message_dicts(
            messages=messages, drop_none=kwargs.pop("drop_none", False)
        ),
        payload=self._model_kwargs(**kwargs),
        headers=self._prepare_headers(kwargs.pop("headers", {})),
        stream=True,
    ):
        logger.debug(f"Received chat chunk: {response}")
        if len(response.get("choices", []))  0:
            delta = response["choices"][0].get("delta") or {}
        else:
            delta = {}

        # Check if this chunk is the start of a function call
        if delta.get("tool_calls"):
            is_function = True

        # Update using deltas
        role = delta.get("role") or MessageRole.ASSISTANT
        content_delta = delta.get("content") or ""
        content += content_delta

        additional_kwargs = {}
        if is_function:
            tool_calls = _update_tool_calls(tool_calls, delta.get("tool_calls"))
            if tool_calls:
                additional_kwargs["tool_calls"] = tool_calls

        yield ChatResponse(
            message=ChatMessage(
                role=role,
                content=content,
                additional_kwargs=additional_kwargs,
            ),
            delta=content_delta,
            raw=response,
            additional_kwargs=_get_response_token_counts(response),
        )

```
 |  
| --- | --- |  
###  acomplete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.acomplete "Permanent link")

```
acomplete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Asynchronously generate a completion for the given prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The prompt to generate a completion for.  |  _required_  |  
|  `formatted`  |  `bool`  |  Whether the prompt is formatted.  |  `False`  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `CompletionResponse`  |   |  The response from the LLM.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-oci-data-science/llama_index/llms/oci_data_science/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defacomplete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponse:
"""
    Asynchronously generate a completion for the given prompt.

    Args:
        prompt (str): The prompt to generate a completion for.
        formatted (bool): Whether the prompt is formatted.
        **kwargs: Additional keyword arguments.

    Returns:
        CompletionResponse: The response from the LLM.

    """
    logger.debug(f"Calling acomplete with prompt: {prompt}")
    response = await self.async_client.generate(
        prompt=prompt,
        payload=self._model_kwargs(**kwargs),
        headers=self._prepare_headers(kwargs.pop("headers", {})),
        stream=False,
    )

    logger.debug(f"Received async response: {response}")
    try:
        choice = response["choices"][0]
        text = choice.get("text", "")
        logprobs = _from_completion_logprobs_dict(choice.get("logprobs", {}) or {})

        return CompletionResponse(
            text=text,
            raw=response,
            logprobs=logprobs,
            additional_kwargs=_get_response_token_counts(response),
        )
    except (IndexError, KeyError, TypeError) as e:
        raise ValueError(f"Failed to parse response: {e!s}") frome

```
 |  
| --- | --- |  
###  astream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.astream_complete "Permanent link")

```
astream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseAsyncGen

```

Asynchronously stream the completion for the given prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The prompt to generate a completion for.  |  _required_  |  
|  `formatted`  |  `bool`  |  Whether the prompt is formatted.  |  `False`  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `CompletionResponse`  |  `CompletionResponseAsyncGen`  |  The streamed response from the LLM.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-oci-data-science/llama_index/llms/oci_data_science/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defastream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseAsyncGen:
"""
    Asynchronously stream the completion for the given prompt.

    Args:
        prompt (str): The prompt to generate a completion for.
        formatted (bool): Whether the prompt is formatted.
        **kwargs: Additional keyword arguments.

    Yields:
        CompletionResponse: The streamed response from the LLM.

    """

    async defgen() -> CompletionResponseAsyncGen:
        logger.debug(f"Starting astream_complete with prompt: {prompt}")
        text = ""

        async for response in await self.async_client.generate(
            prompt=prompt,
            payload=self._model_kwargs(**kwargs),
            headers=self._prepare_headers(kwargs.pop("headers", {})),
            stream=True,
        ):
            logger.debug(f"Received async chunk: {response}")
            if len(response.get("choices", []))  0:
                delta = response["choices"][0].get("text")
                if delta is None:
                    delta = ""
            else:
                delta = ""
            text += delta

            yield CompletionResponse(
                delta=delta,
                text=text,
                raw=response,
                additional_kwargs=_get_response_token_counts(response),
            )

    return gen()

```
 |  
| --- | --- |  
###  achat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.achat "Permanent link")

```
achat(
    messages: Sequence[], **kwargs: 
) -> 

```

Asynchronously generate a chat completion based on the input messages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  A sequence of chat messages.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `ChatResponse`  |   |  The chat response from the LLM.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-oci-data-science/llama_index/llms/oci_data_science/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
async defachat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponse:
"""
    Asynchronously generate a chat completion based on the input messages.

    Args:
        messages (Sequence[ChatMessage]): A sequence of chat messages.
        **kwargs: Additional keyword arguments.

    Returns:
        ChatResponse: The chat response from the LLM.

    """
    logger.debug(f"Calling achat with messages: {messages}")
    response = await self.async_client.chat(
        messages=_to_message_dicts(
            messages=messages, drop_none=kwargs.pop("drop_none", False)
        ),
        payload=self._model_kwargs(**kwargs),
        headers=self._prepare_headers(kwargs.pop("headers", {})),
        stream=False,
    )

    logger.debug(f"Received async chat response: {response}")
    try:
        choice = response["choices"][0]
        message = _from_message_dict(choice.get("message", ""))
        logprobs = _from_token_logprob_dicts(
            (choice.get("logprobs") or {}).get("content", {})
        )
        return ChatResponse(
            message=message,
            raw=response,
            logprobs=logprobs,
            additional_kwargs=_get_response_token_counts(response),
        )
    except (IndexError, KeyError, TypeError) as e:
        raise ValueError(f"Failed to parse response: {e!s}") frome

```
 |  
| --- | --- |  
###  astream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.astream_chat "Permanent link")

```
astream_chat(
    messages: Sequence[], **kwargs: 
) -> ChatResponseAsyncGen

```

Asynchronously stream the chat completion based on the input messages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  A sequence of chat messages.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `ChatResponse`  |  `ChatResponseAsyncGen`  |  The streamed chat response from the LLM.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-oci-data-science/llama_index/llms/oci_data_science/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
async defastream_chat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponseAsyncGen:
"""
    Asynchronously stream the chat completion based on the input messages.

    Args:
        messages (Sequence[ChatMessage]): A sequence of chat messages.
        **kwargs: Additional keyword arguments.

    Yields:
        ChatResponse: The streamed chat response from the LLM.

    """

    async defgen() -> ChatResponseAsyncGen:
        logger.debug(f"Starting astream_chat with messages: {messages}")
        content = ""
        is_function = False
        tool_calls = []
        async for response in await self.async_client.chat(
            messages=_to_message_dicts(
                messages=messages, drop_none=kwargs.pop("drop_none", False)
            ),
            payload=self._model_kwargs(**kwargs),
            headers=self._prepare_headers(kwargs.pop("headers", {})),
            stream=True,
        ):
            logger.debug(f"Received async chat chunk: {response}")
            if len(response.get("choices", []))  0:
                delta = response["choices"][0].get("delta") or {}
            else:
                delta = {}

            # Check if this chunk is the start of a function call
            if delta.get("tool_calls"):
                is_function = True

            # Update using deltas
            role = delta.get("role") or MessageRole.ASSISTANT
            content_delta = delta.get("content") or ""
            content += content_delta

            additional_kwargs = {}
            if is_function:
                tool_calls = _update_tool_calls(tool_calls, delta.get("tool_calls"))
                if tool_calls:
                    additional_kwargs["tool_calls"] = tool_calls

            yield ChatResponse(
                message=ChatMessage(
                    role=role,
                    content=content,
                    additional_kwargs=additional_kwargs,
                ),
                delta=content_delta,
                raw=response,
                additional_kwargs=_get_response_token_counts(response),
            )

    return gen()

```
 |  
| --- | --- |  
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_data_science/#llama_index.llms.oci_data_science.OCIDataScience.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
    **kwargs: 
) -> []

```

Extract tool calls from the chat response.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `response`  |   |  The chat response containing tool calls.  |  _required_  |  
|  `error_on_no_tool_call`  |  `bool`  |  Whether to raise an error if no tool calls are found.  |  `True`  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[ToolSelection[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.ToolSelection "ToolSelection \(llama_index.core.llms.llm.ToolSelection\)")]`  |  List[ToolSelection]: A list of tool selections extracted from the response.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If no tool calls are found and error_on_no_tool_call is True.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-oci-data-science/llama_index/llms/oci_data_science/base.py`  
| 
```
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
```
 | 
```
defget_tool_calls_from_response(
    self,
    response: ChatResponse,
    error_on_no_tool_call: bool = True,
    **kwargs: Any,
) -> List[ToolSelection]:
"""
    Extract tool calls from the chat response.

    Args:
        response (ChatResponse): The chat response containing tool calls.
        error_on_no_tool_call (bool): Whether to raise an error if no tool calls are found.
        **kwargs: Additional keyword arguments.

    Returns:
        List[ToolSelection]: A list of tool selections extracted from the response.

    Raises:
        ValueError: If no tool calls are found and error_on_no_tool_call is True.

    """
    tool_calls = response.message.additional_kwargs.get("tool_calls", [])
    logger.debug(f"Getting tool calls from response: {tool_calls}")

    if len(tool_calls)  1:
        if error_on_no_tool_call:
            raise ValueError(
                f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
            )
        else:
            return []

    tool_selections = []
    for tool_call in tool_calls:
        if tool_call.get("type") != "function":
            raise ValueError(f"Invalid tool type detected: {tool_call.get('type')}")

        # Handle both complete and partial JSON
        try:
            argument_dict = parse_partial_json(
                tool_call.get("function", {}).get("arguments", {})
            )
        except ValueError as e:
            logger.debug(f"Failed to parse tool call arguments: {e!s}")
            argument_dict = {}

        tool_selections.append(
            ToolSelection(
                tool_id=tool_call.get("id"),
                tool_name=tool_call.get("function", {}).get("name"),
                tool_kwargs=argument_dict,
            )
        )

    logger.debug(
        f"Extracted tool calls: {[tool_selection.model_dump()fortool_selectionintool_selections]}"
    )
    return tool_selections

```
 |  
| --- | --- |  
options: members: - OCIDataScience
