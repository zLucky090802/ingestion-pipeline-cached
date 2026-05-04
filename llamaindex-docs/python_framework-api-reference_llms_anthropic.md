# Anthropic
##  Anthropic [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/anthropic/#llama_index.llms.anthropic.Anthropic "Permanent link")
Bases: `FunctionCallingLLM`
Anthropic LLM.
Examples:
`pip install llama-index-llms-anthropic`

```
fromllama_index.llms.anthropicimport Anthropic

llm = Anthropic(model="claude-instant-1")
resp = llm.stream_complete("Paul Graham is ")
for r in resp:
    print(r.delta, end="")

```

Source code in `llama-index-integrations/llms/llama-index-llms-anthropic/llama_index/llms/anthropic/base.py`  
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
1034
1035
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
1057
1058
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
1103
1104
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
1134
1135
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
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
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
```
 | 
```
classAnthropic(FunctionCallingLLM):
"""
    Anthropic LLM.

    Examples:
        `pip install llama-index-llms-anthropic`

        ```python
        from llama_index.llms.anthropic import Anthropic

        llm = Anthropic(model="claude-instant-1")
        resp = llm.stream_complete("Paul Graham is ")
        for r in resp:
            print(r.delta, end="")
        ```

    """

    model: str = Field(
        default=DEFAULT_ANTHROPIC_MODEL, description="The anthropic model to use."
    )
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use for sampling.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: int = Field(
        default=DEFAULT_ANTHROPIC_MAX_TOKENS,
        description="The maximum number of tokens to generate.",
        gt=0,
    )

    base_url: Optional[str] = Field(default=None, description="The base URL to use.")
    timeout: Optional[float] = Field(
        default=None, description="The timeout to use in seconds.", ge=0
    )
    max_retries: int = Field(
        default=10, description="The maximum number of API retries.", ge=0
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the anthropic API."
    )
    cache_idx: Optional[int] = Field(
        default=None,
        description=(
            "Set the cache_control for every message up to and including this index. "
            "Set to -1 to cache all messages. "
            "Set to None to disable caching."
        ),
    )
    thinking_dict: Optional[Dict[str, Any]] = Field(
        default=None,
        description=(
            "Configure thinking controls for the LLM. See the Anthropic API docs for more details. "
            "For example: thinking_dict={'type': 'enabled', 'budget_tokens': 16000}"
        ),
    )
    tools: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description=(
            "List of tools to provide to the model. "
            "For example: tools=[{'type': 'web_search_20250305', 'name': 'web_search', 'max_uses': 3}]"
        ),
    )
    mcp_servers: Optional[List[dict]] = Field(
        default=None,
        description=(
            "List of MCP servers to use for the model. "
            "For example: mcp_servers=[{'type': 'url', 'url': 'https://mcp.example.com/sse', 'name': 'example-mcp', 'authorization_token': 'YOUR_TOKEN'}]"
        ),
    )

    _client: Union[
        anthropic.Anthropic, anthropic.AnthropicVertex, anthropic.AnthropicBedrock
    ] = PrivateAttr()
    _aclient: Union[
        anthropic.AsyncAnthropic,
        anthropic.AsyncAnthropicVertex,
        anthropic.AsyncAnthropicBedrock,
    ] = PrivateAttr()

    def__init__(
        self,
        model: str = DEFAULT_ANTHROPIC_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_ANTHROPIC_MAX_TOKENS,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: int = 10,
        api_key: Optional[str] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        callback_manager: Optional[CallbackManager] = None,
        default_headers: Optional[Dict[str, str]] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        region: Optional[str] = None,
        project_id: Optional[str] = None,
        aws_region: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        cache_idx: Optional[int] = None,
        thinking_dict: Optional[Dict[str, Any]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        mcp_servers: Optional[List[dict]] = None,
    ) -> None:
        additional_kwargs = additional_kwargs or {}
        callback_manager = callback_manager or CallbackManager([])
        # set the temperature to 1 when thinking is enabled, as per: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#important-considerations-when-using-extended-thinking
        if thinking_dict and thinking_dict.get("type") == "enabled":
            temperature = 1

        super().__init__(
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            model=model,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            cache_idx=cache_idx,
            thinking_dict=thinking_dict,
            tools=tools,
            mcp_servers=mcp_servers,
        )

        # Merge default User-Agent header with user-provided headers
        merged_headers = _get_default_headers(default_headers)

        if region and project_id and not aws_region:
            self._client = anthropic.AnthropicVertex(
                region=region,
                project_id=project_id,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=merged_headers,
            )

            self._aclient = anthropic.AsyncAnthropicVertex(
                region=region,
                project_id=project_id,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=merged_headers,
            )
        elif aws_region:
            self._client = anthropic.AnthropicBedrock(
                aws_region=aws_region,
                aws_access_key=aws_access_key_id,
                aws_secret_key=aws_secret_access_key,
                max_retries=max_retries,
                default_headers=merged_headers,
                timeout=timeout,
            )
            self._aclient = anthropic.AsyncAnthropicBedrock(
                aws_region=aws_region,
                aws_access_key=aws_access_key_id,
                aws_secret_key=aws_secret_access_key,
                max_retries=max_retries,
                default_headers=merged_headers,
                timeout=timeout,
            )
        else:
            self._client = anthropic.Anthropic(
                api_key=api_key,
                base_url=base_url,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=merged_headers,
            )
            self._aclient = anthropic.AsyncAnthropic(
                api_key=api_key,
                base_url=base_url,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=merged_headers,
            )

    @classmethod
    defclass_name(cls) -> str:
        return "Anthropic_LLM"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=anthropic_modelname_to_contextsize(self.model),
            num_output=self.max_tokens,
            is_chat_model=True,
            model_name=self.model,
            is_function_calling_model=is_function_calling_model(self.model),
        )

    @property
    deftokenizer(self) -> Tokenizer:
        return AnthropicTokenizer(self._client, self.model)

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        return {
            **base_kwargs,
            **self.additional_kwargs,
        }

    def_get_all_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs = {
            **self._model_kwargs,
            **kwargs,
        }

        if self.thinking_dict and "thinking" not in kwargs:
            kwargs["thinking"] = self.thinking_dict

        if self.tools and "tools" not in kwargs:
            kwargs["tools"] = self.tools
        elif self.tools and "tools" in kwargs:
            kwargs["tools"] = [*self.tools, *kwargs["tools"]]

        if self.mcp_servers and "mcp_servers" not in kwargs:
            kwargs["mcp_servers"] = self.mcp_servers
            kwargs["betas"] = ["mcp-client-2025-04-04"]
        elif self.mcp_servers and "mcp_servers" in kwargs:
            kwargs["mcp_servers"] = [*self.mcp_servers, *kwargs["mcp_servers"]]
            kwargs["betas"] = ["mcp-client-2025-04-04"]

        return kwargs

    def_completion_response_from_chat_response(
        self, chat_response: AnthropicChatResponse
    ) -> AnthropicCompletionResponse:
        return AnthropicCompletionResponse(
            text=chat_response.message.content or "",
            delta=chat_response.delta,
            additional_kwargs=chat_response.additional_kwargs,
            raw=chat_response.raw,
            citations=chat_response.citations,
        )

    def_get_blocks_and_tool_calls_and_thinking(
        self, response: Any
    ) -> Tuple[List[ContentBlock], List[Dict[str, Any]]]:
        blocks: List[ContentBlock] = []
        citations: List[TextCitation] = []
        tracked_citations: Set[str] = set()

        for content_block in response.content:
            if isinstance(content_block, TextBlock):
                blocks.append(LITextBlock(text=content_block.text))
                # Check for citations in this text block
                if hasattr(content_block, "citations") and content_block.citations:
                    for citation in content_block.citations:
                        if (
                            isinstance(citation, CitationsSearchResultLocation)
                            and str(citation) not in tracked_citations
                        ):
                            tracked_citations.add(str(citation))
                            blocks.append(
                                LICitationBlock(
                                    cited_content=LITextBlock(text=citation.cited_text),
                                    source=citation.source,
                                    title=citation.title,
                                    additional_location_info={
                                        "start_block_index": citation.start_block_index,
                                        "end_block_index": citation.end_block_index,
                                        "search_result_index": citation.search_result_index,
                                    },
                                )
                            )
                    citations.extend(content_block.citations)
            # this assumes a single thinking block, which as of 2025-03-06, is always true
            elif isinstance(content_block, ThinkingBlock):
                blocks.append(
                    LIThinkingBlock(
                        content=content_block.thinking,
                        additional_information=content_block.model_dump(
                            exclude={"thinking"}
                        ),
                    )
                )
            elif isinstance(content_block, ToolUseBlock):
                blocks.append(
                    ToolCallBlock(
                        tool_call_id=content_block.id,
                        tool_kwargs=cast(Dict[str, Any] | str, content_block.input),
                        tool_name=content_block.name,
                    )
                )

        return blocks, [x.model_dump() for x in citations]

    @llm_chat_callback()
    defchat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> AnthropicChatResponse:
        anthropic_messages, system_prompt = messages_to_anthropic_messages(
            messages, self.cache_idx, self.model
        )
        all_kwargs = self._get_all_kwargs(**kwargs)

        response = self._client.messages.create(
            messages=anthropic_messages,
            stream=False,
            system=system_prompt,
            **all_kwargs,
        )

        blocks, citations = self._get_blocks_and_tool_calls_and_thinking(response)

        return AnthropicChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                blocks=blocks,
            ),
            citations=citations,
            raw=dict(response),
        )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> AnthropicCompletionResponse:
        chat_message = ChatMessage(role=MessageRole.USER, content=prompt)
        chat_response = self.chat([chat_message], **kwargs)
        return self._completion_response_from_chat_response(chat_response)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> Generator[AnthropicChatResponse, None, None]:
        anthropic_messages, system_prompt = messages_to_anthropic_messages(
            messages, self.cache_idx, self.model
        )
        all_kwargs = self._get_all_kwargs(**kwargs)

        response = self._client.messages.create(
            messages=anthropic_messages, system=system_prompt, stream=True, **all_kwargs
        )

        defgen() -> Generator[AnthropicChatResponse, None, None]:
            content = []
            cur_block = None
            content_delta = ""
            thinking = None
            cur_tool_calls: List[ToolUseBlock] = []
            cur_tool_call: Optional[ToolUseBlock] = None
            cur_tool_json: str = ""
            cur_citations: List[Dict[str, Any]] = []
            tracked_citations: Set[str] = set()
            role = MessageRole.ASSISTANT
            # Track usage metadata and stop_reason from RawMessage events
            usage_metadata: Dict[str, Any] = {}
            input_tokens: Optional[int] = None
            stop_reason: Optional[str] = None
            for r in response:
                if isinstance(r, (ContentBlockDeltaEvent, RawContentBlockDeltaEvent)):
                    if isinstance(r.delta, TextDelta):
                        content_delta = r.delta.text or ""
                        if not isinstance(cur_block, LITextBlock):
                            cur_block = LITextBlock(text=content_delta)
                        else:
                            cur_block.text += content_delta

                    elif isinstance(r.delta, CitationsDelta) and isinstance(
                        r.delta.citation, CitationsSearchResultLocation
                    ):
                        content_delta = ""
                        citation = r.delta.citation
                        if str(citation) not in tracked_citations:
                            tracked_citations.add(str(citation))
                            content.append(
                                LICitationBlock(
                                    cited_content=LITextBlock(text=citation.cited_text),
                                    source=citation.source,
                                    title=citation.title,
                                    additional_location_info={
                                        "start_block_index": citation.start_block_index,
                                        "end_block_index": citation.end_block_index,
                                        "search_result_index": citation.search_result_index,
                                    },
                                )
                            )
                    elif isinstance(r.delta, SignatureDelta):
                        content_delta = ""
                        if not isinstance(cur_block, LIThinkingBlock):
                            cur_block = LIThinkingBlock(
                                content="",
                                additional_information={"signature": r.delta.signature},
                            )
                        else:
                            cur_block.additional_information["signature"] += (
                                r.delta.signature
                            )
                    elif isinstance(r.delta, ThinkingDelta):
                        content_delta = ""
                        if cur_block is None:
                            cur_block = LIThinkingBlock(
                                content=r.delta.thinking or "",
                                additional_information={"signature": ""},
                            )
                        else:
                            cur_block.content += r.delta.thinking
                    elif isinstance(r.delta, CitationsDelta):
                        content_delta = ""
                        # TODO: handle citation deltas
                        cur_citations.append(r.delta.citation.model_dump())
                    elif isinstance(r.delta, InputJSONDelta) and not isinstance(
                        cur_tool_call, ToolUseBlock
                    ):
                        # TODO: handle server-side tool calls
                        content_delta = ""
                    else:
                        content_delta = ""
                        if not isinstance(cur_tool_call, ToolUseBlock):
                            raise ValueError(
                                "Tool call not started, but got block type "
                                + str(type(r.delta))
                            )
                        cur_tool_json += r.delta.partial_json or ""
                        try:
                            argument_dict = parse_partial_json(cur_tool_json)
                            cur_tool_call.input = argument_dict
                        except ValueError:
                            pass

                    if cur_tool_call is not None:
                        tool_calls_to_send = [*cur_tool_calls, cur_tool_call]
                    else:
                        tool_calls_to_send = cur_tool_calls

                    for tool_call in tool_calls_to_send:
                        tc = ToolCallBlock(
                            tool_call_id=tool_call.id,
                            tool_name=tool_call.name,
                            tool_kwargs=cast(Dict[str, Any] | str, tool_call.input),
                        )
                        update_tool_calls(content, tc)

                    yield AnthropicChatResponse(
                        message=ChatMessage(
                            role=role,
                            blocks=content,
                            additional_kwargs={
                                "usage": usage_metadata if usage_metadata else None,
                                "stop_reason": stop_reason,
                            },
                        ),
                        citations=cur_citations,
                        delta=content_delta,
                        raw=dict(r),
                    )
                elif isinstance(r, (ContentBlockStartEvent, RawContentBlockStartEvent)):
                    if isinstance(r.content_block, ToolUseBlock):
                        cur_tool_call = r.content_block
                        cur_tool_json = ""
                elif isinstance(r, (ContentBlockStopEvent, RawContentBlockStopEvent)):
                    if isinstance(cur_tool_call, ToolUseBlock):
                        cur_tool_calls.append(cur_tool_call)

                    if cur_block is not None:
                        content.append(cur_block)
                        cur_block = None

                    if cur_tool_call is not None:
                        tool_calls_to_send = [*cur_tool_calls, cur_tool_call]
                    else:
                        tool_calls_to_send = cur_tool_calls

                    for tool_call in tool_calls_to_send:
                        tc = ToolCallBlock(
                            tool_call_id=tool_call.id,
                            tool_name=tool_call.name,
                            tool_kwargs=cast(Dict[str, Any] | str, tool_call.input),
                        )
                        update_tool_calls(content, tc)

                    yield AnthropicChatResponse(
                        message=ChatMessage(
                            role=role,
                            blocks=content,
                            additional_kwargs={
                                "usage": usage_metadata if usage_metadata else None,
                                "stop_reason": stop_reason,
                            },
                        ),
                        citations=cur_citations,
                        delta="",
                        raw=dict(r),
                    )
                elif isinstance(r, RawMessageStartEvent):
                    # Capture initial usage metadata from message_start
                    if hasattr(r.message, "usage") and r.message.usage:
                        # Save input tokens for later
                        input_tokens = r.message.usage.input_tokens
                        usage_metadata = {
                            "input_tokens": r.message.usage.input_tokens,
                            "output_tokens": r.message.usage.output_tokens,
                        }
                elif isinstance(r, RawMessageDeltaEvent):
                    # Update usage metadata and capture stop_reason from message_delta
                    if hasattr(r, "usage") and r.usage:
                        # Modify r.usage.input_tokens if None with saved input tokens value
                        r.usage.input_tokens = r.usage.input_tokens or input_tokens
                        usage_metadata = {
                            "input_tokens": r.usage.input_tokens,
                            "output_tokens": r.usage.output_tokens,
                        }
                    if hasattr(r, "delta") and hasattr(r.delta, "stop_reason"):
                        stop_reason = r.delta.stop_reason

                    # Yield a final chunk with updated metadata including stop_reason
                    yield AnthropicChatResponse(
                        message=ChatMessage(
                            role=role,
                            blocks=content,
                            additional_kwargs={
                                "usage": usage_metadata if usage_metadata else None,
                                "stop_reason": stop_reason,
                            },
                        ),
                        citations=cur_citations,
                        delta="",
                        raw=dict(r),
                    )
                elif isinstance(r, RawMessageStopEvent):
                    # Final event - no additional data to capture
                    pass

        return gen()

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> Generator[AnthropicCompletionResponse, None, None]:
        chat_message = ChatMessage(role=MessageRole.USER, content=prompt)
        chat_response = self.stream_chat([chat_message], **kwargs)

        defgen() -> Generator[AnthropicCompletionResponse, None, None]:
            for r in chat_response:
                yield self._completion_response_from_chat_response(r)

        return gen()

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> AnthropicChatResponse:
        anthropic_messages, system_prompt = messages_to_anthropic_messages(
            messages, self.cache_idx, self.model
        )
        all_kwargs = self._get_all_kwargs(**kwargs)

        response = await self._aclient.messages.create(
            messages=anthropic_messages,
            system=system_prompt,
            stream=False,
            **all_kwargs,
        )

        blocks, citations = self._get_blocks_and_tool_calls_and_thinking(response)

        return AnthropicChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                blocks=blocks,
            ),
            citations=citations,
            raw=dict(response),
        )

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> AnthropicCompletionResponse:
        chat_message = ChatMessage(role=MessageRole.USER, content=prompt)
        chat_response = await self.achat([chat_message], **kwargs)
        return self._completion_response_from_chat_response(chat_response)

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> AsyncGenerator[AnthropicChatResponse, None]:
        anthropic_messages, system_prompt = messages_to_anthropic_messages(
            messages, self.cache_idx, self.model
        )
        all_kwargs = self._get_all_kwargs(**kwargs)

        response = await self._aclient.messages.create(
            messages=anthropic_messages, system=system_prompt, stream=True, **all_kwargs
        )

        async defgen() -> ChatResponseAsyncGen:
            content = []
            cur_block = None
            content_delta = ""
            thinking = None
            cur_tool_calls: List[ToolUseBlock] = []
            cur_tool_call: Optional[ToolUseBlock] = None
            cur_tool_json: str = ""
            cur_citations: List[Dict[str, Any]] = []
            tracked_citations: Set[str] = set()
            role = MessageRole.ASSISTANT
            # Track usage metadata and stop_reason from RawMessage events
            usage_metadata: Dict[str, Any] = {}
            input_tokens: Optional[int] = None
            stop_reason: Optional[str] = None
            async for r in response:
                if isinstance(r, (ContentBlockDeltaEvent, RawContentBlockDeltaEvent)):
                    if isinstance(r.delta, TextDelta):
                        content_delta = r.delta.text or ""
                        if not isinstance(cur_block, LITextBlock):
                            cur_block = LITextBlock(text=content_delta)
                        else:
                            cur_block.text += content_delta

                    elif isinstance(r.delta, CitationsDelta) and isinstance(
                        r.delta.citation, CitationsSearchResultLocation
                    ):
                        content_delta = ""
                        citation = r.delta.citation
                        if str(citation) not in tracked_citations:
                            tracked_citations.add(str(citation))
                            content.append(
                                LICitationBlock(
                                    cited_content=LITextBlock(text=citation.cited_text),
                                    source=citation.source,
                                    title=citation.title,
                                    additional_location_info={
                                        "start_block_index": citation.start_block_index,
                                        "end_block_index": citation.end_block_index,
                                        "search_result_index": citation.search_result_index,
                                    },
                                )
                            )
                    elif isinstance(r.delta, SignatureDelta):
                        content_delta = ""
                        if not isinstance(cur_block, LIThinkingBlock):
                            cur_block = LIThinkingBlock(
                                content="",
                                additional_information={"signature": r.delta.signature},
                            )
                        else:
                            cur_block.additional_information["signature"] += (
                                r.delta.signature
                            )
                    elif isinstance(r.delta, ThinkingDelta):
                        content_delta = ""
                        if cur_block is None:
                            cur_block = LIThinkingBlock(
                                content=r.delta.thinking or "",
                                additional_information={"signature": ""},
                            )
                        else:
                            cur_block.content += r.delta.thinking
                    elif isinstance(r.delta, CitationsDelta):
                        content_delta = ""
                        # TODO: handle citation deltas
                        cur_citations.append(r.delta.citation.model_dump())
                    elif isinstance(r.delta, InputJSONDelta) and not isinstance(
                        cur_tool_call, ToolUseBlock
                    ):
                        # TODO: handle server-side tool calls
                        content_delta = ""
                    else:
                        content_delta = ""
                        if not isinstance(cur_tool_call, ToolUseBlock):
                            raise ValueError(
                                "Tool call not started, but got block type "
                                + str(type(r.delta))
                            )
                        cur_tool_json += r.delta.partial_json or ""
                        try:
                            argument_dict = parse_partial_json(cur_tool_json)
                            cur_tool_call.input = argument_dict
                        except ValueError:
                            pass

                    if cur_tool_call is not None:
                        tool_calls_to_send = [*cur_tool_calls, cur_tool_call]
                    else:
                        tool_calls_to_send = cur_tool_calls

                    for tool_call in tool_calls_to_send:
                        tc = ToolCallBlock(
                            tool_call_id=tool_call.id,
                            tool_name=tool_call.name,
                            tool_kwargs=cast(Dict[str, Any] | str, tool_call.input),
                        )
                        update_tool_calls(content, tc)

                    yield AnthropicChatResponse(
                        message=ChatMessage(
                            role=role,
                            blocks=content,
                            additional_kwargs={
                                "usage": usage_metadata if usage_metadata else None,
                                "stop_reason": stop_reason,
                            },
                        ),
                        citations=cur_citations,
                        delta=content_delta,
                        raw=dict(r),
                    )
                elif isinstance(r, (ContentBlockStartEvent, RawContentBlockStartEvent)):
                    if isinstance(r.content_block, ToolUseBlock):
                        cur_tool_call = r.content_block
                        cur_tool_json = ""
                elif isinstance(r, (ContentBlockStopEvent, RawContentBlockStopEvent)):
                    if isinstance(cur_tool_call, ToolUseBlock):
                        cur_tool_calls.append(cur_tool_call)

                    if cur_block is not None:
                        content.append(cur_block)
                        cur_block = None

                    if cur_tool_call is not None:
                        tool_calls_to_send = [*cur_tool_calls, cur_tool_call]
                    else:
                        tool_calls_to_send = cur_tool_calls

                    for tool_call in tool_calls_to_send:
                        tc = ToolCallBlock(
                            tool_call_id=tool_call.id,
                            tool_name=tool_call.name,
                            tool_kwargs=cast(Dict[str, Any] | str, tool_call.input),
                        )
                        update_tool_calls(content, tc)

                    yield AnthropicChatResponse(
                        message=ChatMessage(
                            role=role,
                            blocks=content,
                            additional_kwargs={
                                "usage": usage_metadata if usage_metadata else None,
                                "stop_reason": stop_reason,
                            },
                        ),
                        citations=cur_citations,
                        delta="",
                        raw=dict(r),
                    )
                elif isinstance(r, RawMessageStartEvent):
                    # Capture initial usage metadata from message_start
                    if hasattr(r.message, "usage") and r.message.usage:
                        # Save input tokens for later
                        input_tokens = r.message.usage.input_tokens
                        usage_metadata = {
                            "input_tokens": r.message.usage.input_tokens,
                            "output_tokens": r.message.usage.output_tokens,
                        }
                elif isinstance(r, RawMessageDeltaEvent):
                    # Update usage metadata and capture stop_reason from message_delta
                    if hasattr(r, "usage") and r.usage:
                        # Modify r.usage.input_tokens if None with saved input tokens value
                        r.usage.input_tokens = r.usage.input_tokens or input_tokens
                        usage_metadata = {
                            "input_tokens": r.usage.input_tokens,
                            "output_tokens": r.usage.output_tokens,
                        }
                    if hasattr(r, "delta") and hasattr(r.delta, "stop_reason"):
                        stop_reason = r.delta.stop_reason

                    # Yield a final chunk with updated metadata including stop_reason
                    yield AnthropicChatResponse(
                        message=ChatMessage(
                            role=role,
                            blocks=content,
                            additional_kwargs={
                                "usage": usage_metadata if usage_metadata else None,
                                "stop_reason": stop_reason,
                            },
                        ),
                        citations=cur_citations,
                        delta="",
                        raw=dict(r),
                    )
                elif isinstance(r, RawMessageStopEvent):
                    # Final event - no additional data to capture
                    pass

        return gen()

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> AsyncGenerator[AnthropicCompletionResponse, None]:
        chat_message = ChatMessage(role=MessageRole.USER, content=prompt)
        chat_response_gen = await self.astream_chat([chat_message], **kwargs)

        async defgen() -> AsyncGenerator[AnthropicCompletionResponse, None]:
            async for r in chat_response_gen:
                yield self._completion_response_from_chat_response(r)

        return gen()

    def_map_tool_choice_to_anthropic(
        self, tool_required: bool, allow_parallel_tool_calls: bool
    ) -> dict:
        is_thinking_enabled = (
            self.thinking_dict and self.thinking_dict.get("type") == "enabled"
        )
        return {
            "disable_parallel_tool_use": not allow_parallel_tool_calls,
            "type": "any" if tool_required and not is_thinking_enabled else "auto",
        }

    def_prepare_chat_with_tools(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
"""Prepare the chat with tools."""
        chat_history = chat_history or []

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)
            chat_history.append(user_msg)

        tool_dicts = []
        if tools:
            for tool in tools:
                tool_dicts.append(
                    {
                        "name": tool.metadata.name,
                        "description": tool.metadata.description,
                        "input_schema": tool.metadata.get_parameters_dict(),
                    }
                )
            if "prompt-caching" in kwargs.get("extra_headers", {}).get(
                "anthropic-beta", ""
            ):
                if is_anthropic_prompt_caching_supported_model(self.model):
                    tool_dicts[-1]["cache_control"] = {"type": "ephemeral"}
                else:
                    logger.warning(
                        f"Model '{self.model}' does not support prompt caching. "
                        "Cache control will be ignored. "
                        "See: https://docs.claude.com/en/docs/build-with-claude/prompt-caching"
                    )

        # anthropic doesn't like you specifying a tool choice if you don't have any tools
        tool_choice_dict = (
            {}
            if not tools and not tool_required
            else {
                "tool_choice": self._map_tool_choice_to_anthropic(
                    tool_required, allow_parallel_tool_calls
                )
            }
        )

        return {
            "messages": chat_history,
            "tools": tool_dicts,
            **tool_choice_dict,
            **kwargs,
        }

    def_validate_chat_with_tools_response(
        self,
        response: ChatResponse,
        tools: List["BaseTool"],
        allow_parallel_tool_calls: bool = False,
        **kwargs: Any,
    ) -> ChatResponse:
"""Validate the response from chat_with_tools."""
        if not allow_parallel_tool_calls:
            force_single_tool_call(response)
        return response

    defget_tool_calls_from_response(
        self,
        response: "ChatResponse",
        error_on_no_tool_call: bool = True,
        **kwargs: Any,
    ) -> List[ToolSelection]:
"""Predict and call the tool."""
        tool_calls = [
            block
            for block in response.message.blocks
            if isinstance(block, ToolCallBlock)
        ]

        if len(tool_calls)  1:
            if error_on_no_tool_call:
                raise ValueError(
                    f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
                )
            else:
                return []

        tool_selections = []
        for tool_call in tool_calls:
            argument_dict = (
                json.loads(tool_call.tool_kwargs)
                if isinstance(tool_call.tool_kwargs, str)
                else tool_call.tool_kwargs
            )

            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.tool_call_id or "",
                    tool_name=tool_call.tool_name,
                    tool_kwargs=argument_dict,
                )
            )

        return tool_selections

    @dispatcher.span
    defstructured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
        messages = prompt.format_messages(**prompt_args)
        ant_messages, system = messages_to_anthropic_beta_messages(messages)
        if isinstance(
            self._client, (anthropic.AnthropicVertex, anthropic.AnthropicBedrock)
        ) or not is_anthropic_structured_output_supported(self.model):
            return super().structured_predict(
                output_cls, prompt, llm_kwargs, **prompt_args
            )
        response = self._client.beta.messages.parse(
            messages=ant_messages,
            model=self.model,
            max_tokens=(llm_kwargs or {}).get("max_tokens", 8192),
            output_format=output_cls,
            system=system,
            betas=["structured-outputs-2025-11-13"],
            **(llm_kwargs or {}),
        )
        parsed = response.parsed_output
        stop_reason = response.stop_reason
        if parsed is not None:
            return parsed
        raise ValueError(
            f"It was not possible to produce a structured response{' because of '+stop_reasonifstop_reasonisnotNoneelse''}"
        )

    @dispatcher.span
    async defastructured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
        messages = prompt.format_messages(**prompt_args)
        ant_messages, system = messages_to_anthropic_beta_messages(messages)
        if isinstance(
            self._aclient,
            (anthropic.AsyncAnthropicVertex, anthropic.AsyncAnthropicBedrock),
        ) or not is_anthropic_structured_output_supported(self.model):
            return await super().astructured_predict(
                output_cls, prompt, llm_kwargs, **prompt_args
            )
        response = await self._aclient.beta.messages.parse(
            messages=ant_messages,
            model=self.model,
            max_tokens=(llm_kwargs or {}).get("max_tokens", 8192),
            output_format=output_cls,
            system=system,
            betas=["structured-outputs-2025-11-13"],
            **(llm_kwargs or {}),
        )
        parsed = response.parsed_output
        stop_reason = response.stop_reason
        if parsed is not None:
            return parsed
        raise ValueError(
            f"It was not possible to produce a structured response{' because of '+stop_reasonifstop_reasonisnotNoneelse''}"
        )

    @dispatcher.span
    defstream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Generator[Union[Model, "FlexibleModel"], Any, Any]:
        logger.warning(
            "Streaming not fully supported for Anthropic structured outputs."
        )
        messages = prompt.format_messages(**prompt_args)
        ant_messages, system = messages_to_anthropic_beta_messages(messages)
        if isinstance(
            self._client, (anthropic.AnthropicVertex, anthropic.AnthropicBedrock)
        ) or not is_anthropic_structured_output_supported(self.model):
            return super().stream_structured_predict(
                output_cls, prompt, llm_kwargs, **prompt_args
            )
        response = self._client.beta.messages.parse(
            messages=ant_messages,
            model=self.model,
            max_tokens=(llm_kwargs or {}).get("max_tokens", 8192),
            output_format=output_cls,
            system=system,
            betas=["structured-outputs-2025-11-13"],
            **(llm_kwargs or {}),
        )
        parsed = response.parsed_output
        stop_reason = response.stop_reason
        if parsed is not None:

            defgen() -> Generator[Model, Any, None]:
                yield parsed

            return gen()
        raise ValueError(
            f"It was not possible to produce a structured response{' because of '+stop_reasonifstop_reasonisnotNoneelse''}"
        )

    @dispatcher.span
    async defastream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> AsyncGenerator[Union[Model, "FlexibleModel"], Any]:
        logger.warning(
            "Streaming not fully supported for Anthropic structured outputs."
        )
        messages = prompt.format_messages(**prompt_args)
        ant_messages, system = messages_to_anthropic_beta_messages(messages)
        if isinstance(
            self._aclient,
            (anthropic.AsyncAnthropicVertex, anthropic.AsyncAnthropicBedrock),
        ) or not is_anthropic_structured_output_supported(self.model):
            return await super().astream_structured_predict(
                output_cls, prompt, llm_kwargs, **prompt_args
            )
        response = await self._aclient.beta.messages.parse(
            messages=ant_messages,
            model=self.model,
            max_tokens=(llm_kwargs or {}).get("max_tokens", 8192),
            output_format=output_cls,
            system=system,
            betas=["structured-outputs-2025-11-13"],
            **(llm_kwargs or {}),
        )
        parsed = response.parsed_output
        stop_reason = response.stop_reason
        if parsed is not None:

            async defgen() -> AsyncGenerator[Model, Any]:
                yield parsed

            return gen()
        raise ValueError(
            f"It was not possible to produce a structured response{' because of '+stop_reasonifstop_reasonisnotNoneelse''}"
        )

```
 |  
| --- | --- |  
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/anthropic/#llama_index.llms.anthropic.Anthropic.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
    **kwargs: 
) -> [ToolSelection]

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-anthropic/llama_index/llms/anthropic/base.py`  
| 
```
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
1034
1035
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
1057
1058
1059
```
 | 
```
defget_tool_calls_from_response(
    self,
    response: "ChatResponse",
    error_on_no_tool_call: bool = True,
    **kwargs: Any,
) -> List[ToolSelection]:
"""Predict and call the tool."""
    tool_calls = [
        block
        for block in response.message.blocks
        if isinstance(block, ToolCallBlock)
    ]

    if len(tool_calls)  1:
        if error_on_no_tool_call:
            raise ValueError(
                f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
            )
        else:
            return []

    tool_selections = []
    for tool_call in tool_calls:
        argument_dict = (
            json.loads(tool_call.tool_kwargs)
            if isinstance(tool_call.tool_kwargs, str)
            else tool_call.tool_kwargs
        )

        tool_selections.append(
            ToolSelection(
                tool_id=tool_call.tool_call_id or "",
                tool_name=tool_call.tool_name,
                tool_kwargs=argument_dict,
            )
        )

    return tool_selections

```
 |  
| --- | --- |  
options: members: - Anthropic
