# Openai
##  OpenAI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAI "Permanent link")
Bases: `FunctionCallingLLM`
OpenAI LLM.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  name of the OpenAI model to use.  |  `DEFAULT_OPENAI_MODEL`  |  
|  `temperature`  |  `float`  |  a float from 0 to 1 controlling randomness in generation; higher will lead to more creative, less deterministic responses.  |  `DEFAULT_TEMPERATURE`  |  
|  `max_tokens`  |  `int | None`  |  the maximum number of tokens to generate.  |  `None`  |  
|  `additional_kwargs`  |  `Dict[str, Any]`  |  Add additional parameters to OpenAI request body.  |  `None`  |  
|  `max_retries`  |  How many times to retry the API call if it fails.  |  
|  `timeout`  |  `float`  |  How long to wait, in seconds, for an API call before failing.  |  `60.0`  |  
|  `reuse_client`  |  `bool`  |  Reuse the OpenAI client between requests. When doing anything with large volumes of async API calls, setting this to false can improve stability.  |  `True`  |  
|  `api_key`  |  `str | None`  |  Your OpenAI api key  |  `None`  |  
|  `api_base`  |  `str | None`  |  The base URL of the API to call  |  `None`  |  
|  `api_version`  |  `str | None`  |  the version of the API to call  |  `None`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.CallbackManager\)")]`  |  the callback manager is used for observability.  |  `None`  |  
|  `default_headers`  |  `Dict[str, str] | None`  |  override the default headers for API requests.  |  `None`  |  
|  `http_client`  |  `Optional[Client]`  |  pass in your own httpx.Client instance.  |  `None`  |  
|  `async_http_client`  |  `Optional[AsyncClient]`  |  pass in your own httpx.AsyncClient instance.  |  `None`  |  
|  `logprobs`  |  `bool | None`  |  Whether to return logprobs per token.  |  `None`  |  
|  `top_logprobs`  |  The number of top token log probs to return.  |  
|  `strict`  |  `bool`  |  Whether to use strict mode for invoking tools/using schemas.  |  `False`  |  
|  `reasoning_effort`  |  `Literal['none', 'minimal', 'low', 'medium', 'high', 'xhigh'] | None`  |  The effort to use for reasoning models.  |  `None`  |  
|  `modalities`  |  `List[str] | None`  |  The output modalities to use for the model.  |  `None`  |  
|  `audio_config`  |  `Dict[str, Any] | None`  |  The audio configuration to use for the model.  |  `None`  |  
Examples:
`pip install llama-index-llms-openai`

```
importos
importopenai

os.environ["OPENAI_API_KEY"] = "sk-..."
openai.api_key = os.environ["OPENAI_API_KEY"]

fromllama_index.llms.openaiimport OpenAI

llm = OpenAI(model="gpt-3.5-turbo")

stream = llm.stream_complete("Hi, write a short story")

for r in stream:
    print(r.delta, end="")

```

Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/base.py`  
| 
```
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
1282
1283
1284
1285
1286
1287
```
 | 
```
classOpenAI(FunctionCallingLLM):
"""
    OpenAI LLM.

    Args:
        model: name of the OpenAI model to use.
        temperature: a float from 0 to 1 controlling randomness in generation; higher will lead to more creative, less deterministic responses.
        max_tokens: the maximum number of tokens to generate.
        additional_kwargs: Add additional parameters to OpenAI request body.
        max_retries: How many times to retry the API call if it fails.
        timeout: How long to wait, in seconds, for an API call before failing.
        reuse_client: Reuse the OpenAI client between requests. When doing anything with large volumes of async API calls, setting this to false can improve stability.
        api_key: Your OpenAI api key
        api_base: The base URL of the API to call
        api_version: the version of the API to call
        callback_manager: the callback manager is used for observability.
        default_headers: override the default headers for API requests.
        http_client: pass in your own httpx.Client instance.
        async_http_client: pass in your own httpx.AsyncClient instance.

    Examples:
        `pip install llama-index-llms-openai`

        ```python
        import os
        import openai

        os.environ["OPENAI_API_KEY"] = "sk-..."
        openai.api_key = os.environ["OPENAI_API_KEY"]

        from llama_index.llms.openai import OpenAI

        llm = OpenAI(model="gpt-3.5-turbo")

        stream = llm.stream_complete("Hi, write a short story")

        for r in stream:
            print(r.delta, end="")
        ```
    """

    model: str = Field(
        default=DEFAULT_OPENAI_MODEL, description="The OpenAI model to use."
    )
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use during generation.",
        ge=0.0,
        le=2.0,
    )
    max_tokens: Optional[int] = Field(
        description="The maximum number of tokens to generate.",
        default=None,
        gt=0,
    )
    logprobs: Optional[bool] = Field(
        description="Whether to return logprobs per token.",
        default=None,
    )
    top_logprobs: int = Field(
        description="The number of top token log probs to return.",
        default=0,
        ge=0,
        le=20,
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the OpenAI API."
    )
    max_retries: int = Field(
        default=3,
        description="The maximum number of API retries.",
        ge=0,
    )
    timeout: float = Field(
        default=60.0,
        description="The timeout, in seconds, for API requests.",
        ge=0,
    )
    default_headers: Optional[Dict[str, str]] = Field(
        default=None, description="The default headers for API requests."
    )
    reuse_client: bool = Field(
        default=True,
        description=(
            "Reuse the OpenAI client between requests. When doing anything with large "
            "volumes of async API calls, setting this to false can improve stability."
        ),
    )

    api_key: Optional[str] = Field(default=None, description="The OpenAI API key.")
    api_base: Optional[str] = Field(
        default=None, description="The base URL for OpenAI API."
    )
    api_version: Optional[str] = Field(
        default=None, description="The API version for OpenAI API."
    )
    strict: bool = Field(
        default=False,
        description="Whether to use strict mode for invoking tools/using schemas.",
    )
    reasoning_effort: Optional[
        Literal["none", "minimal", "low", "medium", "high", "xhigh"]
    ] = Field(
        default=None,
        description="The effort to use for reasoning models.",
    )
    modalities: Optional[List[str]] = Field(
        default=None,
        description="The output modalities to use for the model.",
    )
    audio_config: Optional[Dict[str, Any]] = Field(
        default=None,
        description="The audio configuration to use for the model.",
    )

    _client: Optional[SyncOpenAI] = PrivateAttr()
    _aclient: Optional[AsyncOpenAI] = PrivateAttr()
    _http_client: Optional[httpx.Client] = PrivateAttr()
    _async_http_client: Optional[httpx.AsyncClient] = PrivateAttr()

    def__init__(
        self,
        model: str = DEFAULT_OPENAI_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        timeout: float = 60.0,
        reuse_client: bool = True,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        default_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        async_http_client: Optional[httpx.AsyncClient] = None,
        openai_client: Optional[SyncOpenAI] = None,
        async_openai_client: Optional[AsyncOpenAI] = None,
        # base class
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        strict: bool = False,
        reasoning_effort: Optional[
            Literal["none", "minimal", "low", "medium", "high", "xhigh"]
        ] = None,
        modalities: Optional[List[str]] = None,
        audio_config: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        # TODO: Support deprecated max_new_tokens
        if "max_new_tokens" in kwargs:
            max_tokens = kwargs["max_new_tokens"]
            del kwargs["max_new_tokens"]

        additional_kwargs = additional_kwargs or {}

        api_key, api_base, api_version = resolve_openai_credentials(
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
        )

        # TODO: Temp forced to 1.0 for o1
        if model in O1_MODELS:
            temperature = 1.0

        if not is_chatcomp_api_supported(model):
            raise ValueError(
                f"Cannot use model {model} as it is only supported by the Responses API. Use the OpenAIResponses class for it."
            )

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            callback_manager=callback_manager,
            api_key=api_key,
            api_version=api_version,
            api_base=api_base,
            timeout=timeout,
            reuse_client=reuse_client,
            default_headers=default_headers,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            strict=strict,
            reasoning_effort=reasoning_effort,
            modalities=modalities,
            audio_config=audio_config,
            **kwargs,
        )

        self._client = openai_client
        self._aclient = async_openai_client
        self._http_client = http_client
        self._async_http_client = async_http_client

    def_get_client(self) -> SyncOpenAI:
        if not self.reuse_client:
            return SyncOpenAI(**self._get_credential_kwargs())

        if self._client is None:
            self._client = SyncOpenAI(**self._get_credential_kwargs())
        return self._client

    def_get_aclient(self) -> AsyncOpenAI:
        if not self.reuse_client:
            return AsyncOpenAI(**self._get_credential_kwargs(is_async=True))

        if self._aclient is None:
            self._aclient = AsyncOpenAI(**self._get_credential_kwargs(is_async=True))
        return self._aclient

    def_get_model_name(self) -> str:
        model_name = self.model
        if "ft-" in model_name:  # legacy fine-tuning
            model_name = model_name.split(":")[0]
        elif model_name.startswith("ft:"):
            model_name = model_name.split(":")[1]
        return model_name

    @classmethod
    defclass_name(cls) -> str:
        return "openai_llm"

    @property
    def_tokenizer(self) -> Optional[Tokenizer]:
"""
        Get a tokenizer for this model, or None if a tokenizing method is unknown.

        OpenAI can do this using the tiktoken package, subclasses may not have
        this convenience.
        """
        return tiktoken.encoding_for_model(self._get_model_name())

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=openai_modelname_to_contextsize(self._get_model_name()),
            num_output=self.max_tokens or -1,
            is_chat_model=is_chat_model(model=self._get_model_name()),
            is_function_calling_model=is_function_calling_model(
                model=self._get_model_name()
            ),
            model_name=self.model,
            # TODO: Temp for O1 beta
            system_role=MessageRole.USER
            if self.model in O1_MODELS
            else MessageRole.SYSTEM,
        )

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        if self._use_chat_completions(kwargs):
            chat_fn = self._chat
        else:
            chat_fn = completion_to_chat_decorator(self._complete)
        return chat_fn(messages, **kwargs)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if self._use_chat_completions(kwargs):
            stream_chat_fn = self._stream_chat
        else:
            stream_chat_fn = stream_completion_to_chat_decorator(self._stream_complete)
        return stream_chat_fn(messages, **kwargs)

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        if self.modalities and "audio" in self.modalities:
            raise ValueError(
                "Audio is not supported for completion. Use chat/achat instead."
            )

        if self._use_chat_completions(kwargs):
            complete_fn = chat_to_completion_decorator(self._chat)
        else:
            complete_fn = self._complete
        return complete_fn(prompt, **kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        if self._use_chat_completions(kwargs):
            stream_complete_fn = stream_chat_to_completion_decorator(self._stream_chat)
        else:
            stream_complete_fn = self._stream_complete
        return stream_complete_fn(prompt, **kwargs)

    def_use_chat_completions(self, kwargs: Dict[str, Any]) -> bool:
        if "use_chat_completions" in kwargs:
            return kwargs["use_chat_completions"]
        return self.metadata.is_chat_model

    def_get_credential_kwargs(self, is_async: bool = False) -> Dict[str, Any]:
        return {
            "api_key": self.api_key,
            "base_url": self.api_base,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "default_headers": self.default_headers,
            "http_client": self._async_http_client if is_async else self._http_client,
        }

    def_get_model_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        base_kwargs = {"model": self.model, "temperature": self.temperature, **kwargs}
        if self.max_tokens is not None:
            # If max_tokens is None, don't include in the payload:
            # https://platform.openai.com/docs/api-reference/chat
            # https://platform.openai.com/docs/api-reference/completions
            base_kwargs["max_tokens"] = self.max_tokens
        if self.logprobs is not None and self.logprobs is True:
            if self.metadata.is_chat_model:
                base_kwargs["logprobs"] = self.logprobs
                base_kwargs["top_logprobs"] = self.top_logprobs
            else:
                base_kwargs["logprobs"] = self.top_logprobs  # int in this case

        # can't send stream_options to the API when not streaming
        all_kwargs = {**base_kwargs, **self.additional_kwargs}
        if "stream" not in all_kwargs and "stream_options" in all_kwargs:
            del all_kwargs["stream_options"]
        if self.model in O1_MODELS and base_kwargs.get("max_tokens") is not None:
            # O1 models use max_completion_tokens instead of max_tokens
            all_kwargs["max_completion_tokens"] = all_kwargs.get(
                "max_completion_tokens", all_kwargs["max_tokens"]
            )
            all_kwargs.pop("max_tokens", None)
        if self.model in O1_MODELS and self.reasoning_effort is not None:
            # O1 models support reasoning_effort of none, minimal, low, medium, high, xhigh
            all_kwargs["reasoning_effort"] = self.reasoning_effort

        if self.modalities is not None:
            all_kwargs["modalities"] = self.modalities
        if self.audio_config is not None:
            all_kwargs["audio"] = self.audio_config

        return all_kwargs

    @llm_retry_decorator
    def_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        client = self._get_client()
        message_dicts = to_openai_message_dicts(
            messages,
            model=self.model,
        )

        if self.reuse_client:
            response = client.chat.completions.create(
                messages=message_dicts,
                stream=False,
                **self._get_model_kwargs(**kwargs),
            )
        else:
            with client:
                response = client.chat.completions.create(
                    messages=message_dicts,
                    stream=False,
                    **self._get_model_kwargs(**kwargs),
                )

        openai_message = response.choices[0].message
        message = from_openai_message(
            openai_message, modalities=self.modalities or ["text"]
        )
        openai_token_logprobs = response.choices[0].logprobs
        logprobs = None
        if openai_token_logprobs and openai_token_logprobs.content:
            logprobs = from_openai_token_logprobs(openai_token_logprobs.content)

        return ChatResponse(
            message=message,
            raw=response,
            logprobs=logprobs,
            additional_kwargs=self._get_response_token_counts(response),
        )

    @llm_retry_decorator
    def_stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if self.modalities and "audio" in self.modalities:
            raise ValueError("Audio is not supported for chat streaming")

        client = self._get_client()
        message_dicts = to_openai_message_dicts(
            messages,
            model=self.model,
        )

        defgen() -> ChatResponseGen:
            content = ""
            reasoning_content = ""
            tool_calls: List[ChoiceDeltaToolCall] = []

            is_function = False
            for response in client.chat.completions.create(
                messages=message_dicts,
                **self._get_model_kwargs(stream=True, **kwargs),
            ):
                blocks = []
                response = cast(ChatCompletionChunk, response)
                if len(response.choices)  0:
                    delta = response.choices[0].delta
                else:
                    delta = ChoiceDelta()

                if delta is None:
                    continue

                # check if this chunk is the start of a function call
                if delta.tool_calls:
                    is_function = True

                # update using deltas
                role = delta.role or MessageRole.ASSISTANT
                content_delta = delta.content or ""
                content += content_delta

                # Extract reasoning_content for chain-of-thought streaming.
                # Many OpenAI-compatible providers surface this extra field.
                raw_reasoning = getattr(delta, "reasoning_content", None)
                reasoning_delta = (
                    raw_reasoning if isinstance(raw_reasoning, str) else ""
                )
                reasoning_content += reasoning_delta

                if reasoning_content:
                    blocks.append(ThinkingBlock(content=reasoning_content))
                blocks.append(TextBlock(text=content))

                message_additional_kwargs = {}
                if is_function:
                    tool_calls = update_tool_calls(tool_calls, delta.tool_calls)
                    if tool_calls:
                        message_additional_kwargs["tool_calls"] = tool_calls
                        for tool_call in tool_calls:
                            if tool_call.function:
                                blocks.append(
                                    ToolCallBlock(
                                        tool_call_id=tool_call.id,
                                        tool_kwargs=tool_call.function.arguments or {},
                                        tool_name=tool_call.function.name or "",
                                    )
                                )

                # thinking_delta goes in ChatResponse.additional_kwargs
                # (same pattern as Ollama) so agents can read it
                response_additional_kwargs = self._get_response_token_counts(response)
                if reasoning_delta:
                    response_additional_kwargs["thinking_delta"] = reasoning_delta

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        blocks=blocks,
                        additional_kwargs=message_additional_kwargs,
                    ),
                    delta=content_delta,
                    raw=response,
                    additional_kwargs=response_additional_kwargs,
                )

        return gen()

    @llm_retry_decorator
    def_complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        client = self._get_client()
        all_kwargs = self._get_model_kwargs(**kwargs)
        self._update_max_tokens(all_kwargs, prompt)

        if self.reuse_client:
            response = client.completions.create(
                prompt=prompt,
                stream=False,
                **all_kwargs,
            )
        else:
            with client:
                response = client.completions.create(
                    prompt=prompt,
                    stream=False,
                    **all_kwargs,
                )
        text = response.choices[0].text

        openai_completion_logprobs = response.choices[0].logprobs
        logprobs = None
        if openai_completion_logprobs:
            logprobs = from_openai_completion_logprobs(openai_completion_logprobs)

        return CompletionResponse(
            text=text,
            raw=response,
            logprobs=logprobs,
            additional_kwargs=self._get_response_token_counts(response),
        )

    @llm_retry_decorator
    def_stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        client = self._get_client()
        all_kwargs = self._get_model_kwargs(stream=True, **kwargs)
        self._update_max_tokens(all_kwargs, prompt)

        defgen() -> CompletionResponseGen:
            text = ""
            for response in client.completions.create(
                prompt=prompt,
                **all_kwargs,
            ):
                if len(response.choices)  0:
                    delta = response.choices[0].text
                    if delta is None:
                        delta = ""
                else:
                    delta = ""
                text += delta
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()

    def_update_max_tokens(self, all_kwargs: Dict[str, Any], prompt: str) -> None:
"""Infer max_tokens for the payload, if possible."""
        if self.max_tokens is not None or self._tokenizer is None:
            return
        # NOTE: non-chat completion endpoint requires max_tokens to be set
        num_tokens = len(self._tokenizer.encode(prompt))
        max_tokens = self.metadata.context_window - num_tokens
        if max_tokens <= 0:
            raise ValueError(
                f"The prompt has {num_tokens} tokens, which is too long for"
                " the model. Please use a prompt that fits within"
                f" {self.metadata.context_window} tokens."
            )
        all_kwargs["max_tokens"] = max_tokens

    def_get_response_token_counts(self, raw_response: Any) -> dict:
"""Get the token usage reported by the response."""
        if hasattr(raw_response, "usage"):
            try:
                prompt_tokens = raw_response.usage.prompt_tokens
                completion_tokens = raw_response.usage.completion_tokens
                total_tokens = raw_response.usage.total_tokens
            except AttributeError:
                return {}
        elif isinstance(raw_response, dict):
            usage = raw_response.get("usage", {})
            # NOTE: other model providers that use the OpenAI client may not report usage
            if usage is None:
                return {}
            # Backwards compatibility with old dict type
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)
        else:
            return {}

        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        }

    # ===== Async Endpoints =====
    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        achat_fn: Callable[..., Awaitable[ChatResponse]]
        if self._use_chat_completions(kwargs):
            achat_fn = self._achat
        else:
            achat_fn = acompletion_to_chat_decorator(self._acomplete)
        return await achat_fn(messages, **kwargs)

    @llm_chat_callback()
    async defastream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        astream_chat_fn: Callable[..., Awaitable[ChatResponseAsyncGen]]
        if self._use_chat_completions(kwargs):
            astream_chat_fn = self._astream_chat
        else:
            astream_chat_fn = astream_completion_to_chat_decorator(
                self._astream_complete
            )
        return await astream_chat_fn(messages, **kwargs)

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        if self.modalities and "audio" in self.modalities:
            raise ValueError(
                "Audio is not supported for completion. Use chat/achat instead."
            )

        if self._use_chat_completions(kwargs):
            acomplete_fn = achat_to_completion_decorator(self._achat)
        else:
            acomplete_fn = self._acomplete
        return await acomplete_fn(prompt, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        if self._use_chat_completions(kwargs):
            astream_complete_fn = astream_chat_to_completion_decorator(
                self._astream_chat
            )
        else:
            astream_complete_fn = self._astream_complete
        return await astream_complete_fn(prompt, **kwargs)

    @llm_retry_decorator
    async def_achat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        aclient = self._get_aclient()
        message_dicts = to_openai_message_dicts(
            messages,
            model=self.model,
        )

        if self.reuse_client:
            response = await aclient.chat.completions.create(
                messages=message_dicts, stream=False, **self._get_model_kwargs(**kwargs)
            )
        else:
            async with aclient:
                response = await aclient.chat.completions.create(
                    messages=message_dicts,
                    stream=False,
                    **self._get_model_kwargs(**kwargs),
                )

        openai_message = response.choices[0].message
        message = from_openai_message(
            openai_message, modalities=self.modalities or ["text"]
        )
        openai_token_logprobs = response.choices[0].logprobs
        logprobs = None
        if openai_token_logprobs and openai_token_logprobs.content:
            logprobs = from_openai_token_logprobs(openai_token_logprobs.content)

        return ChatResponse(
            message=message,
            raw=response,
            logprobs=logprobs,
            additional_kwargs=self._get_response_token_counts(response),
        )

    @llm_retry_decorator
    async def_astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        if self.modalities and "audio" in self.modalities:
            raise ValueError("Audio is not supported for chat streaming")

        aclient = self._get_aclient()
        message_dicts = to_openai_message_dicts(
            messages,
            model=self.model,
        )

        async defgen() -> ChatResponseAsyncGen:
            content = ""
            reasoning_content = ""
            tool_calls: List[ChoiceDeltaToolCall] = []

            is_function = False
            first_chat_chunk = True
            async for response in await aclient.chat.completions.create(
                messages=message_dicts,
                **self._get_model_kwargs(stream=True, **kwargs),
            ):
                blocks = []
                response = cast(ChatCompletionChunk, response)
                if len(response.choices)  0:
                    # check if the first chunk has neither content nor tool_calls
                    # this happens when 1106 models end up calling multiple tools
                    if (
                        first_chat_chunk
                        and response.choices[0].delta.content is None
                        and response.choices[0].delta.tool_calls is None
                    ):
                        first_chat_chunk = False
                        continue
                    delta = response.choices[0].delta
                else:
                    delta = ChoiceDelta()
                first_chat_chunk = False

                if delta is None:
                    continue

                # check if this chunk is the start of a function call
                if delta.tool_calls:
                    is_function = True

                # update using deltas
                role = delta.role or MessageRole.ASSISTANT
                content_delta = delta.content or ""
                content += content_delta

                # Extract reasoning_content for chain-of-thought streaming.
                # Many OpenAI-compatible providers surface this extra field.
                raw_reasoning = getattr(delta, "reasoning_content", None)
                reasoning_delta = (
                    raw_reasoning if isinstance(raw_reasoning, str) else ""
                )
                reasoning_content += reasoning_delta

                if reasoning_content:
                    blocks.append(ThinkingBlock(content=reasoning_content))
                blocks.append(TextBlock(text=content))

                message_additional_kwargs = {}
                if is_function:
                    tool_calls = update_tool_calls(tool_calls, delta.tool_calls)
                    if tool_calls:
                        message_additional_kwargs["tool_calls"] = tool_calls
                        for tool_call in tool_calls:
                            if tool_call.function:
                                blocks.append(
                                    ToolCallBlock(
                                        tool_call_id=tool_call.id,
                                        tool_kwargs=tool_call.function.arguments or {},
                                        tool_name=tool_call.function.name or "",
                                    )
                                )

                # thinking_delta goes in ChatResponse.additional_kwargs
                # (same pattern as Ollama) so agents can read it
                response_additional_kwargs = self._get_response_token_counts(response)
                if reasoning_delta:
                    response_additional_kwargs["thinking_delta"] = reasoning_delta

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        blocks=blocks,
                        additional_kwargs=message_additional_kwargs,
                    ),
                    delta=content_delta,
                    raw=response,
                    additional_kwargs=response_additional_kwargs,
                )

        return gen()

    @llm_retry_decorator
    async def_acomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        aclient = self._get_aclient()
        all_kwargs = self._get_model_kwargs(**kwargs)
        self._update_max_tokens(all_kwargs, prompt)

        if self.reuse_client:
            response = await aclient.completions.create(
                prompt=prompt,
                stream=False,
                **all_kwargs,
            )
        else:
            async with aclient:
                response = await aclient.completions.create(
                    prompt=prompt,
                    stream=False,
                    **all_kwargs,
                )

        text = response.choices[0].text
        openai_completion_logprobs = response.choices[0].logprobs
        logprobs = None
        if openai_completion_logprobs:
            logprobs = from_openai_completion_logprobs(openai_completion_logprobs)

        return CompletionResponse(
            text=text,
            raw=response,
            logprobs=logprobs,
            additional_kwargs=self._get_response_token_counts(response),
        )

    @llm_retry_decorator
    async def_astream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        aclient = self._get_aclient()
        all_kwargs = self._get_model_kwargs(stream=True, **kwargs)
        self._update_max_tokens(all_kwargs, prompt)

        async defgen() -> CompletionResponseAsyncGen:
            text = ""
            async for response in await aclient.completions.create(
                prompt=prompt,
                **all_kwargs,
            ):
                if len(response.choices)  0:
                    delta = response.choices[0].text
                    if delta is None:
                        delta = ""
                else:
                    delta = ""
                text += delta
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()

    def_prepare_chat_with_tools(
        self,
        tools: Sequence["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,
        tool_choice: Optional[Union[str, dict]] = None,
        strict: Optional[bool] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
"""Predict and call the tool."""
        tool_specs = [
            tool.metadata.to_openai_tool(skip_length_check=True) for tool in tools
        ]

        # if strict is passed in, use, else default to the class-level attribute, else default to True`
        if strict is not None:
            strict = strict
        else:
            strict = self.strict

        if self.metadata.is_function_calling_model:
            for tool_spec in tool_specs:
                if tool_spec["type"] == "function":
                    tool_spec["function"]["strict"] = strict
                    # in current openai 1.40.0 it is always false.
                    tool_spec["function"]["parameters"]["additionalProperties"] = False

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        messages = chat_history or []
        if user_msg:
            messages.append(user_msg)

        kwargs = {
            "messages": messages,
            "tools": tool_specs or None,
            "tool_choice": resolve_tool_choice(tool_choice, tool_required)
            if tool_specs
            else None,
            **kwargs,
        }

        if tool_specs and self.model not in O1_MODELS:
            kwargs["parallel_tool_calls"] = allow_parallel_tool_calls

        return kwargs

    def_validate_chat_with_tools_response(
        self,
        response: ChatResponse,
        tools: Sequence["BaseTool"],
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
        if tool_calls:
            if len(tool_calls)  1:
                if error_on_no_tool_call:
                    raise ValueError(
                        f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
                    )
                else:
                    return []

            tool_selections = []
            for tool_call in tool_calls:
                # this should handle both complete and partial jsons
                try:
                    if isinstance(tool_call.tool_kwargs, str):
                        argument_dict = parse_partial_json(tool_call.tool_kwargs)
                    else:
                        argument_dict = tool_call.tool_kwargs
                except (ValueError, TypeError, JSONDecodeError):
                    argument_dict = {}

                tool_selections.append(
                    ToolSelection(
                        tool_id=tool_call.tool_call_id or "",
                        tool_name=tool_call.tool_name,
                        tool_kwargs=argument_dict,
                    )
                )

            return tool_selections
        else:  # keep it backward-compatible
            tool_calls = response.message.additional_kwargs.get("tool_calls", [])

            if len(tool_calls)  1:
                if error_on_no_tool_call:
                    raise ValueError(
                        f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
                    )
                else:
                    return []

            tool_selections = []
            for tool_call in tool_calls:
                if tool_call.type != "function":
                    raise ValueError("Invalid tool type. Unsupported by OpenAI llm")

                # this should handle both complete and partial jsons
                try:
                    argument_dict = parse_partial_json(tool_call.function.arguments)
                except (ValueError, TypeError, JSONDecodeError):
                    argument_dict = {}

                tool_selections.append(
                    ToolSelection(
                        tool_id=tool_call.id,
                        tool_name=tool_call.function.name,
                        tool_kwargs=argument_dict,
                    )
                )

            return tool_selections

    def_prepare_schema(
        self, llm_kwargs: Optional[Dict[str, Any]], output_cls: Type[Model]
    ) -> Dict[str, Any]:
        fromopenai.resources.chat.completions.completionsimport (
            _type_to_response_format,
        )

        llm_kwargs = llm_kwargs or {}
        response_format = _type_to_response_format(output_cls)
        if isinstance(response_format, dict):
            json_schema = response_format.get("json_schema")
            if isinstance(json_schema, dict) and "name" in json_schema:
                json_schema["name"] = re.sub(
                    r"[^a-zA-Z0-9_-]", "_", str(json_schema["name"])
                )
        llm_kwargs["response_format"] = response_format
        if "tool_choice" in llm_kwargs:
            del llm_kwargs["tool_choice"]
        return llm_kwargs

    def_should_use_structure_outputs(self) -> bool:
        return (
            self.pydantic_program_mode == PydanticProgramMode.DEFAULT
            and is_json_schema_supported(self.model)
        )

    @dispatcher.span
    defstructured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
"""Structured predict."""
        llm_kwargs = llm_kwargs or {}

        if self._should_use_structure_outputs():
            messages = self._extend_messages(prompt.format_messages(**prompt_args))
            llm_kwargs = self._prepare_schema(llm_kwargs, output_cls)
            response = self.chat(messages, **llm_kwargs)
            return output_cls.model_validate_json(str(response.message.content))

        # when uses function calling to extract structured outputs
        # here we force tool_choice to be required
        llm_kwargs["tool_choice"] = (
            "required" if "tool_choice" not in llm_kwargs else llm_kwargs["tool_choice"]
        )
        return super().structured_predict(
            output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
        )

    @dispatcher.span
    async defastructured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
"""Structured predict."""
        llm_kwargs = llm_kwargs or {}

        if self._should_use_structure_outputs():
            messages = self._extend_messages(prompt.format_messages(**prompt_args))
            llm_kwargs = self._prepare_schema(llm_kwargs, output_cls)
            response = await self.achat(messages, **llm_kwargs)
            return output_cls.model_validate_json(str(response.message.content))

        # when uses function calling to extract structured outputs
        # here we force tool_choice to be required
        llm_kwargs["tool_choice"] = (
            "required" if "tool_choice" not in llm_kwargs else llm_kwargs["tool_choice"]
        )
        return await super().astructured_predict(
            output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
        )

    def_structured_stream_call(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Generator[
        Union[Model, List[Model], "FlexibleModel", List["FlexibleModel"]], None, None
    ]:
        if self._should_use_structure_outputs():
            fromllama_index.core.program.streaming_utilsimport (
                process_streaming_content_incremental,
            )

            messages = self._extend_messages(prompt.format_messages(**prompt_args))
            llm_kwargs = self._prepare_schema(llm_kwargs, output_cls)
            curr = None
            for response in self.stream_chat(messages, **llm_kwargs):
                curr = process_streaming_content_incremental(response, output_cls, curr)
                yield curr
        else:
            llm_kwargs["tool_choice"] = (
                "required"
                if "tool_choice" not in llm_kwargs
                else llm_kwargs["tool_choice"]
            )
            yield from super()._structured_stream_call(
                output_cls, prompt, llm_kwargs, **prompt_args
            )

    async def_structured_astream_call(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> AsyncGenerator[
        Union[Model, List[Model], "FlexibleModel", List["FlexibleModel"]], None
    ]:
        if self._should_use_structure_outputs():

            async defgen(
                llm_kwargs=llm_kwargs,
            ) -> AsyncGenerator[
                Union[Model, List[Model], FlexibleModel, List[FlexibleModel]], None
            ]:
                fromllama_index.core.program.streaming_utilsimport (
                    process_streaming_content_incremental,
                )

                messages = self._extend_messages(prompt.format_messages(**prompt_args))
                llm_kwargs = self._prepare_schema(llm_kwargs, output_cls)
                curr = None
                async for response in await self.astream_chat(messages, **llm_kwargs):
                    curr = process_streaming_content_incremental(
                        response, output_cls, curr
                    )
                    yield curr

            return gen()
        else:
            llm_kwargs["tool_choice"] = (
                "required"
                if "tool_choice" not in llm_kwargs
                else llm_kwargs["tool_choice"]
            )
            return await super()._structured_astream_call(
                output_cls, prompt, llm_kwargs, **prompt_args
            )

    @dispatcher.span
    defstream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Generator[Union[Model, FlexibleModel], None, None]:
"""Stream structured predict."""
        llm_kwargs = llm_kwargs or {}

        return super().stream_structured_predict(
            output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
        )

    @dispatcher.span
    async defastream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> AsyncGenerator[Union[Model, FlexibleModel], None]:
"""Stream structured predict."""
        llm_kwargs = llm_kwargs or {}
        return await super().astream_structured_predict(
            output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
        )

```
 |  
| --- | --- |  
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAI.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
    **kwargs: 
) -> []

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/base.py`  
| 
```
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
    if tool_calls:
        if len(tool_calls)  1:
            if error_on_no_tool_call:
                raise ValueError(
                    f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
                )
            else:
                return []

        tool_selections = []
        for tool_call in tool_calls:
            # this should handle both complete and partial jsons
            try:
                if isinstance(tool_call.tool_kwargs, str):
                    argument_dict = parse_partial_json(tool_call.tool_kwargs)
                else:
                    argument_dict = tool_call.tool_kwargs
            except (ValueError, TypeError, JSONDecodeError):
                argument_dict = {}

            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.tool_call_id or "",
                    tool_name=tool_call.tool_name,
                    tool_kwargs=argument_dict,
                )
            )

        return tool_selections
    else:  # keep it backward-compatible
        tool_calls = response.message.additional_kwargs.get("tool_calls", [])

        if len(tool_calls)  1:
            if error_on_no_tool_call:
                raise ValueError(
                    f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
                )
            else:
                return []

        tool_selections = []
        for tool_call in tool_calls:
            if tool_call.type != "function":
                raise ValueError("Invalid tool type. Unsupported by OpenAI llm")

            # this should handle both complete and partial jsons
            try:
                argument_dict = parse_partial_json(tool_call.function.arguments)
            except (ValueError, TypeError, JSONDecodeError):
                argument_dict = {}

            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.id,
                    tool_name=tool_call.function.name,
                    tool_kwargs=argument_dict,
                )
            )

        return tool_selections

```
 |  
| --- | --- |  
###  structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAI.structured_predict "Permanent link")

```
structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> 

```

Structured predict.
Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/base.py`  
| 
```
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
"""Structured predict."""
    llm_kwargs = llm_kwargs or {}

    if self._should_use_structure_outputs():
        messages = self._extend_messages(prompt.format_messages(**prompt_args))
        llm_kwargs = self._prepare_schema(llm_kwargs, output_cls)
        response = self.chat(messages, **llm_kwargs)
        return output_cls.model_validate_json(str(response.message.content))

    # when uses function calling to extract structured outputs
    # here we force tool_choice to be required
    llm_kwargs["tool_choice"] = (
        "required" if "tool_choice" not in llm_kwargs else llm_kwargs["tool_choice"]
    )
    return super().structured_predict(
        output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
    )

```
 |  
| --- | --- |  
###  astructured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAI.astructured_predict "Permanent link")

```
astructured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> 

```

Structured predict.
Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/base.py`  
| 
```
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
"""Structured predict."""
    llm_kwargs = llm_kwargs or {}

    if self._should_use_structure_outputs():
        messages = self._extend_messages(prompt.format_messages(**prompt_args))
        llm_kwargs = self._prepare_schema(llm_kwargs, output_cls)
        response = await self.achat(messages, **llm_kwargs)
        return output_cls.model_validate_json(str(response.message.content))

    # when uses function calling to extract structured outputs
    # here we force tool_choice to be required
    llm_kwargs["tool_choice"] = (
        "required" if "tool_choice" not in llm_kwargs else llm_kwargs["tool_choice"]
    )
    return await super().astructured_predict(
        output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
    )

```
 |  
| --- | --- |  
###  stream_structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAI.stream_structured_predict "Permanent link")

```
stream_structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> Generator[Union[, FlexibleModel], None, None]

```

Stream structured predict.
Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/base.py`  
| 
```
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
) -> Generator[Union[Model, FlexibleModel], None, None]:
"""Stream structured predict."""
    llm_kwargs = llm_kwargs or {}

    return super().stream_structured_predict(
        output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
    )

```
 |  
| --- | --- |  
###  astream_structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAI.astream_structured_predict "Permanent link")

```
astream_structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> AsyncGenerator[Union[, FlexibleModel], None]

```

Stream structured predict.
Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/base.py`  
| 
```
1275
1276
1277
1278
1279
1280
1281
1282
1283
1284
1285
1286
1287
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
) -> AsyncGenerator[Union[Model, FlexibleModel], None]:
"""Stream structured predict."""
    llm_kwargs = llm_kwargs or {}
    return await super().astream_structured_predict(
        output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
    )

```
 |  
| --- | --- |  
##  Tokenizer [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.Tokenizer "Permanent link")
Bases: `Protocol`
Tokenizers support an encode function that returns a list of ints.
Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/base.py`  
| 
```
120
121
122
123
124
125
```
 | 
```
@runtime_checkable
classTokenizer(Protocol):
"""Tokenizers support an encode function that returns a list of ints."""

    defencode(self, text: str) -> List[int]:  # fmt: skip
        ...

```
 |  
| --- | --- |  
##  OpenAIResponses [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAIResponses "Permanent link")
Bases: `FunctionCallingLLM`
OpenAI Responses LLM.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  name of the OpenAI model to use.  |  `DEFAULT_OPENAI_MODEL`  |  
|  `temperature`  |  `float`  |  a float from 0 to 1 controlling randomness in generation; higher will lead to more creative, less deterministic responses.  |  `DEFAULT_TEMPERATURE`  |  
|  `max_output_tokens`  |  `int | None`  |  the maximum number of tokens to generate.  |  `None`  |  
|  `reasoning_options`  |  `Dict[str, Any] | None`  |  Optional dictionary to configure reasoning for O1 models. Corresponds to the 'reasoning' parameter in the OpenAI API. Example: {"effort": "low", "summary": "concise"}  |  `None`  |  
|  `include`  |  `List[str] | None`  |  Additional output data to include in the model response.  |  `None`  |  
|  `instructions`  |  `str | None`  |  Instructions for the model to follow.  |  `None`  |  
|  `track_previous_responses`  |  `bool`  |  Whether to track previous responses. If true, the LLM class will statefully track previous responses.  |  `False`  |  
|  `store`  |  `bool`  |  Whether to store previous responses in OpenAI's storage.  |  `False`  |  
|  `built_in_tools`  |  `List[dict] | None`  |  The built-in tools to use for the model to augment responses.  |  `None`  |  
|  `truncation`  |  Whether to auto-truncate the input if it exceeds the model's context window.  |  `'disabled'`  |  
|  `user`  |  `str | None`  |  An optional identifier to help track the user's requests for abuse.  |  `None`  |  
|  `strict`  |  `bool`  |  Whether to enforce strict validation of the structured output.  |  `False`  |  
|  `additional_kwargs`  |  `Dict[str, Any]`  |  Add additional parameters to OpenAI request body.  |  `None`  |  
|  `max_retries`  |  How many times to retry the API call if it fails.  |  
|  `timeout`  |  `float`  |  How long to wait, in seconds, for an API call before failing.  |  `60.0`  |  
|  `api_key`  |  `str | None`  |  Your OpenAI api key  |  `None`  |  
|  `api_base`  |  The base URL of the API to call  |  `None`  |  
|  `api_version`  |  the version of the API to call  |  `None`  |  
|  `default_headers`  |  `Dict[str, str] | None`  |  override the default headers for API requests.  |  `None`  |  
|  `http_client`  |  `Optional[Client]`  |  pass in your own httpx.Client instance.  |  `None`  |  
|  `async_http_client`  |  `Optional[AsyncClient]`  |  pass in your own httpx.AsyncClient instance.  |  `None`  |  
|  `top_p`  |  `float`  |  The top-p value to use during generation.  |  `1.0`  |  
|  `call_metadata`  |  `Dict[str, Any] | None`  |  Metadata to include in the API call.  |  `None`  |  
|  `context_window`  |  `int | None`  |  The context window override for the model.  |  `None`  |  
Examples:
`pip install llama-index-llms-openai`

```
fromllama_index.llms.openaiimport OpenAIResponses

llm = OpenAIResponses(model="gpt-4o-mini", api_key="sk-...")

response = llm.complete("Hi, write a short story")
print(response.text)

```

Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/responses.py`  
| 
```
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
```
 | 
```
classOpenAIResponses(FunctionCallingLLM):
"""
    OpenAI Responses LLM.

    Args:
        model: name of the OpenAI model to use.
        temperature: a float from 0 to 1 controlling randomness in generation; higher will lead to more creative, less deterministic responses.
        max_output_tokens: the maximum number of tokens to generate.
        reasoning_options: Optional dictionary to configure reasoning for O1 models.
                    Corresponds to the 'reasoning' parameter in the OpenAI API.
                    Example: {"effort": "low", "summary": "concise"}
        include: Additional output data to include in the model response.
        instructions: Instructions for the model to follow.
        track_previous_responses: Whether to track previous responses. If true, the LLM class will statefully track previous responses.
        store: Whether to store previous responses in OpenAI's storage.
        built_in_tools: The built-in tools to use for the model to augment responses.
        truncation: Whether to auto-truncate the input if it exceeds the model's context window.
        user: An optional identifier to help track the user's requests for abuse.
        strict: Whether to enforce strict validation of the structured output.
        additional_kwargs: Add additional parameters to OpenAI request body.
        max_retries: How many times to retry the API call if it fails.
        timeout: How long to wait, in seconds, for an API call before failing.
        api_key: Your OpenAI api key
        api_base: The base URL of the API to call
        api_version: the version of the API to call
        default_headers: override the default headers for API requests.
        http_client: pass in your own httpx.Client instance.
        async_http_client: pass in your own httpx.AsyncClient instance.

    Examples:
        `pip install llama-index-llms-openai`

        ```python
        from llama_index.llms.openai import OpenAIResponses

        llm = OpenAIResponses(model="gpt-4o-mini", api_key="sk-...")

        response = llm.complete("Hi, write a short story")
        print(response.text)
        ```
    """

    model: str = Field(
        default=DEFAULT_OPENAI_MODEL, description="The OpenAI model to use."
    )
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use during generation.",
        ge=0.0,
        le=2.0,
    )
    top_p: float = Field(
        default=1.0,
        description="The top-p value to use during generation.",
        ge=0.0,
        le=1.0,
    )
    max_output_tokens: Optional[int] = Field(
        description="The maximum number of tokens to generate.",
        gt=0,
    )
    reasoning_options: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional dictionary to configure reasoning for O1 models. Example: {'effort': 'low', 'summary': 'concise'}",
    )
    include: Optional[List[str]] = Field(
        default=None,
        description="Additional output data to include in the model response.",
    )
    instructions: Optional[str] = Field(
        default=None,
        description="Instructions for the model to follow.",
    )
    track_previous_responses: bool = Field(
        default=False,
        description="Whether to track previous responses. If true, the LLM class will statefully track previous responses.",
    )
    store: bool = Field(
        default=False,
        description="Whether to store previous responses in OpenAI's storage.",
    )
    built_in_tools: Optional[List[dict]] = Field(
        default=None,
        description="The built-in tools to use for the model to augment responses.",
    )
    truncation: str = Field(
        default="disabled",
        description="Whether to auto-truncate the input if it exceeds the model's context window.",
    )
    user: Optional[str] = Field(
        default=None,
        description="An optional identifier to help track the user's requests for abuse.",
    )
    call_metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Metadata to include in the API call.",
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional kwargs for the OpenAI API at inference time.",
    )
    max_retries: int = Field(
        default=3,
        description="The maximum number of API retries.",
        ge=0,
    )
    timeout: float = Field(
        default=60.0,
        description="The timeout, in seconds, for API requests.",
        ge=0,
    )
    strict: bool = Field(
        default=False,
        description="Whether to enforce strict validation of the structured output.",
    )
    default_headers: Optional[Dict[str, str]] = Field(
        default=None, description="The default headers for API requests."
    )
    api_key: Optional[str] = Field(default=None, description="The OpenAI API key.")
    api_base: str = Field(description="The base URL for OpenAI API.")
    api_version: str = Field(description="The API version for OpenAI API.")
    context_window: Optional[int] = Field(
        default=None,
        description="The context window override for the model.",
    )

    _client: SyncOpenAI = PrivateAttr()
    _aclient: AsyncOpenAI = PrivateAttr()
    _http_client: Optional[httpx.Client] = PrivateAttr()
    _async_http_client: Optional[httpx.AsyncClient] = PrivateAttr()
    _previous_response_id: Optional[str] = PrivateAttr()

    def__init__(
        self,
        model: str = DEFAULT_OPENAI_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_output_tokens: Optional[int] = None,
        reasoning_options: Optional[Dict[str, Any]] = None,
        include: Optional[List[str]] = None,
        instructions: Optional[str] = None,
        track_previous_responses: bool = False,
        store: bool = False,
        built_in_tools: Optional[List[dict]] = None,
        truncation: str = "disabled",
        user: Optional[str] = None,
        previous_response_id: Optional[str] = None,
        call_metadata: Optional[Dict[str, Any]] = None,
        strict: bool = False,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        timeout: float = 60.0,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        default_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        async_http_client: Optional[httpx.AsyncClient] = None,
        openai_client: Optional[SyncOpenAI] = None,
        async_openai_client: Optional[AsyncOpenAI] = None,
        context_window: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        api_key, api_base, api_version = resolve_openai_credentials(
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
        )

        # TODO: Temp forced to 1.0 for o1
        if model in O1_MODELS:
            temperature = 1.0

        super().__init__(
            model=model,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            reasoning_options=reasoning_options,
            include=include,
            instructions=instructions,
            track_previous_responses=track_previous_responses,
            store=store,
            built_in_tools=built_in_tools,
            truncation=truncation,
            user=user,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            api_key=api_key,
            api_version=api_version,
            api_base=api_base,
            timeout=timeout,
            default_headers=default_headers,
            call_metadata=call_metadata,
            strict=strict,
            context_window=context_window,
            **kwargs,
        )

        self._previous_response_id = previous_response_id

        # store is set to true if track_previous_responses is true
        if self.track_previous_responses:
            self.store = True

        self._http_client = http_client
        self._async_http_client = async_http_client
        self._client = openai_client or SyncOpenAI(**self._get_credential_kwargs())
        self._aclient = async_openai_client or AsyncOpenAI(
            **self._get_credential_kwargs(is_async=True)
        )

    @classmethod
    defclass_name(cls) -> str:
        return "openai_responses_llm"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window
            or openai_modelname_to_contextsize(self._get_model_name()),
            num_output=self.max_output_tokens or -1,
            is_chat_model=True,
            is_function_calling_model=is_function_calling_model(
                model=self._get_model_name()
            ),
            model_name=self.model,
        )

    @property
    def_tokenizer(self) -> Optional[Tokenizer]:
"""
        Get a tokenizer for this model, or None if a tokenizing method is unknown.

        OpenAI can do this using the tiktoken package, subclasses may not have
        this convenience.
        """
        return tiktoken.encoding_for_model(self._get_model_name())

    def_get_model_name(self) -> str:
        model_name = self.model
        if "ft-" in model_name:  # legacy fine-tuning
            model_name = model_name.split(":")[0]
        elif model_name.startswith("ft:"):
            model_name = model_name.split(":")[1]
        return model_name

    def_is_azure_client(self) -> bool:
        return isinstance(self._client, AzureOpenAI)

    def_get_credential_kwargs(self, is_async: bool = False) -> Dict[str, Any]:
        return {
            "api_key": self.api_key,
            "base_url": self.api_base,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "default_headers": self.default_headers,
            "http_client": self._async_http_client if is_async else self._http_client,
        }

    def_get_model_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        initial_tools = self.built_in_tools or []
        model_kwargs = {
            "model": self.model,
            "include": self.include,
            "instructions": self.instructions,
            "max_output_tokens": self.max_output_tokens,
            "metadata": self.call_metadata,
            "previous_response_id": self._previous_response_id,
            "store": self.store,
            "temperature": self.temperature,
            "tools": [*initial_tools, *(kwargs.pop("tools", []) or [])],
            "top_p": self.top_p,
            "truncation": self.truncation,
            "user": self.user,
        }

        if self.model in O1_MODELS and self.reasoning_options is not None:
            model_kwargs["reasoning"] = self.reasoning_options

        if self.reasoning_options is not None or self.model in O1_MODELS:
            params_to_exclude_for_reasoning = {
                "top_p",
                "temperature",
                "presence_penalty",
                "frequency_penalty",
            }
            for param in params_to_exclude_for_reasoning:
                model_kwargs.pop(param, None)

        # priority is class args > additional_kwargs > runtime args
        model_kwargs.update(self.additional_kwargs)

        kwargs = kwargs or {}
        model_kwargs.update(kwargs)

        return model_kwargs

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        return self._chat(messages, **kwargs)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        return self._stream_chat(messages, **kwargs)

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        complete_fn = chat_to_completion_decorator(self._chat)

        return complete_fn(prompt, **kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        stream_complete_fn = stream_chat_to_completion_decorator(self._stream_chat)

        return stream_complete_fn(prompt, **kwargs)

    @staticmethod
    def_parse_response_output(output: List[ResponseOutputItem]) -> ChatResponse:
        message = ChatMessage(role=MessageRole.ASSISTANT, blocks=[])
        additional_kwargs = {"built_in_tool_calls": []}
        blocks: List[ContentBlock] = []
        for item in output:
            if isinstance(item, ResponseOutputMessage):
                for part in item.content:
                    if hasattr(part, "text"):
                        blocks.append(TextBlock(text=part.text))
                    if hasattr(part, "annotations"):
                        additional_kwargs["annotations"] = part.annotations
                    if hasattr(part, "refusal"):
                        additional_kwargs["refusal"] = part.refusal

                message.blocks.extend(blocks)
            elif isinstance(item, ImageGenerationCall):
                # return an ImageBlock if there is image generation
                if item.status != "failed":
                    additional_kwargs["built_in_tool_calls"].append(item)
                    if item.result is not None:
                        image_bytes = base64.b64decode(item.result)
                        blocks.append(ImageBlock(image=image_bytes))
            elif isinstance(item, ResponseCodeInterpreterToolCall):
                additional_kwargs["built_in_tool_calls"].append(item)
            elif isinstance(item, McpCall):
                additional_kwargs["built_in_tool_calls"].append(item)
            elif isinstance(item, ResponseFileSearchToolCall):
                additional_kwargs["built_in_tool_calls"].append(item)
            elif isinstance(item, ResponseFunctionToolCall):
                message.blocks.append(
                    ToolCallBlock(
                        tool_name=item.name,
                        tool_call_id=item.call_id,
                        tool_kwargs=item.arguments,
                    )
                )
            elif isinstance(item, ResponseFunctionWebSearch):
                additional_kwargs["built_in_tool_calls"].append(item)
            elif isinstance(item, ResponseComputerToolCall):
                additional_kwargs["built_in_tool_calls"].append(item)
            elif isinstance(item, ResponseReasoningItem):
                content: Optional[str] = None
                if item.content:
                    content = "\n".join([i.text for i in item.content])
                if item.summary:
                    if content:
                        content += "\n" + "\n".join([i.text for i in item.summary])
                    else:
                        content = "\n".join([i.text for i in item.summary])
                message.blocks.append(
                    ThinkingBlock(
                        content=content,
                        additional_information=item.model_dump(
                            exclude={"content", "summary"}
                        ),
                    )
                )

        return ChatResponse(message=message, additional_kwargs=additional_kwargs)

    @llm_retry_decorator
    def_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        kwargs_dict = self._get_model_kwargs(**kwargs)
        message_dicts = to_openai_message_dicts(
            messages,
            model=self.model,
            is_responses_api=True,
            store=kwargs_dict.get("store"),
        )

        response: Response = self._client.responses.create(
            input=message_dicts,
            stream=False,
            **kwargs_dict,
        )

        if self.track_previous_responses:
            self._previous_response_id = response.id

        chat_response = OpenAIResponses._parse_response_output(response.output)
        chat_response.raw = response
        chat_response.additional_kwargs["usage"] = response.usage
        if hasattr(response.usage.output_tokens_details, "reasoning_tokens"):
            for block in chat_response.message.blocks:
                if isinstance(block, ThinkingBlock):
                    block.num_tokens = (
                        response.usage.output_tokens_details.reasoning_tokens
                    )

        return chat_response

    @staticmethod
    defprocess_response_event(
        event: ResponseStreamEvent,
        built_in_tool_calls: List[Any],
        additional_kwargs: Dict[str, Any],
        current_tool_call: Optional[ResponseFunctionToolCall],
        track_previous_responses: bool,
        previous_response_id: Optional[str] = None,
    ) -> Tuple[
        List[ContentBlock],
        List[Any],
        Dict[str, Any],
        Optional[ResponseFunctionToolCall],
        Optional[str],
        str,
    ]:
"""
        Process a ResponseStreamEvent and update the state accordingly.

        Args:
            event: The response stream event to process
            content: Current accumulated content string
            tool_calls: List of completed tool calls
            built_in_tool_calls: List of built-in tool calls
            additional_kwargs: Additional keyword arguments to include in ChatResponse
            current_tool_call: The currently in-progress tool call, if any
            track_previous_responses: Whether to track previous response IDs
            previous_response_id: Previous response ID if tracking

        Returns:
            A tuple containing the updated state:
            (content, tool_calls, built_in_tool_calls, additional_kwargs, current_tool_call, updated_previous_response_id, delta)
        """
        delta = ""
        updated_previous_response_id = previous_response_id
        # we use blocks instead of content, since now we also support images! :)
        blocks: List[ContentBlock] = []
        if isinstance(event, ResponseCreatedEvent) or isinstance(
            event, ResponseInProgressEvent
        ):
            # Initial events, track the response id
            if track_previous_responses:
                updated_previous_response_id = event.response.id
        elif isinstance(event, ResponseOutputItemAddedEvent):
            # New output item (message, tool call, etc.)
            if isinstance(event.item, ResponseFunctionToolCall):
                current_tool_call = event.item
        elif isinstance(event, ResponseTextDeltaEvent):
            # Text content is being added
            delta = event.delta
            blocks.append(TextBlock(text=delta))
        elif isinstance(event, ResponseImageGenCallPartialImageEvent):
            # Partial image
            if event.partial_image_b64:
                blocks.append(
                    ImageBlock(
                        image=base64.b64decode(event.partial_image_b64),
                        detail=f"id_{event.partial_image_index}",
                    )
                )
        elif isinstance(event, ResponseFunctionCallArgumentsDeltaEvent):
            # Function call arguments are being streamed
            if current_tool_call is not None:
                current_tool_call.arguments += event.delta
        elif isinstance(event, ResponseFunctionCallArgumentsDoneEvent):
            # Function call arguments are complete
            if current_tool_call is not None:
                current_tool_call.arguments = event.arguments
                current_tool_call.status = "completed"
                blocks.append(
                    ToolCallBlock(
                        tool_name=current_tool_call.name,
                        tool_kwargs=current_tool_call.arguments,
                        tool_call_id=current_tool_call.call_id,
                    )
                )

                # clear the current tool call
                current_tool_call = None
        elif isinstance(event, ResponseOutputTextAnnotationAddedEvent):
            # Annotations for the text
            annotations = additional_kwargs.get("annotations", [])
            annotations.append(event.annotation)
            additional_kwargs["annotations"] = annotations
        elif isinstance(event, ResponseFileSearchCallCompletedEvent):
            # File search tool call completed
            built_in_tool_calls.append(event)
        elif isinstance(event, ResponseWebSearchCallCompletedEvent):
            # Web search tool call completed
            built_in_tool_calls.append(event)
        elif isinstance(event, ResponseOutputItemDoneEvent):
            # Reasoning information
            if isinstance(event.item, ResponseReasoningItem):
                content: Optional[str] = None
                if event.item.content:
                    content = "\n".join([i.text for i in event.item.content])
                if event.item.summary:
                    if content:
                        content += "\n" + "\n".join(
                            [i.text for i in event.item.summary]
                        )
                    else:
                        content = "\n".join([i.text for i in event.item.summary])
                blocks.append(
                    ThinkingBlock(
                        content=content,
                        additional_information=event.item.model_dump(
                            exclude={"content", "summary"}
                        ),
                    )
                )
        elif isinstance(event, ResponseCompletedEvent):
            # Response is complete
            if hasattr(event, "response") and hasattr(event.response, "usage"):
                additional_kwargs["usage"] = event.response.usage
            resp = OpenAIResponses._parse_response_output(event.response.output)
            blocks = resp.message.blocks

        return (
            blocks,
            built_in_tool_calls,
            additional_kwargs,
            current_tool_call,
            updated_previous_response_id,
            delta,
        )

    @llm_retry_decorator
    def_stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        message_dicts = to_openai_message_dicts(
            messages,
            model=self.model,
            is_responses_api=True,
        )

        defgen() -> ChatResponseGen:
            built_in_tool_calls = []
            additional_kwargs = {"built_in_tool_calls": []}
            current_tool_call: Optional[ResponseFunctionToolCall] = None
            local_previous_response_id = self._previous_response_id

            for event in self._client.responses.create(
                input=message_dicts,
                stream=True,
                **self._get_model_kwargs(**kwargs),
            ):
                # Process the event and update state
                (
                    blocks,
                    built_in_tool_calls,
                    additional_kwargs,
                    current_tool_call,
                    local_previous_response_id,
                    delta,
                ) = OpenAIResponses.process_response_event(
                    event=event,
                    built_in_tool_calls=built_in_tool_calls,
                    additional_kwargs=additional_kwargs,
                    current_tool_call=current_tool_call,
                    track_previous_responses=self.track_previous_responses,
                    previous_response_id=local_previous_response_id,
                )

                if (
                    self.track_previous_responses
                    and local_previous_response_id != self._previous_response_id
                ):
                    self._previous_response_id = local_previous_response_id

                if built_in_tool_calls:
                    additional_kwargs["built_in_tool_calls"] = built_in_tool_calls

                # For any event, yield a ChatResponse with the current state
                yield ChatResponse(
                    message=ChatMessage(
                        role=MessageRole.ASSISTANT,
                        blocks=blocks,
                    ),
                    delta=delta,
                    raw=event,
                    additional_kwargs=additional_kwargs,
                )

        return gen()

    # ===== Async Endpoints =====
    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        return await self._achat(messages, **kwargs)

    @llm_chat_callback()
    async defastream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        return await self._astream_chat(messages, **kwargs)

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        acomplete_fn = achat_to_completion_decorator(self._achat)

        return await acomplete_fn(prompt, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        astream_complete_fn = astream_chat_to_completion_decorator(self._astream_chat)

        return await astream_complete_fn(prompt, **kwargs)

    @llm_retry_decorator
    async def_achat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        message_dicts = to_openai_message_dicts(
            messages,
            model=self.model,
            is_responses_api=True,
        )

        response: Response = await self._aclient.responses.create(
            input=message_dicts,
            stream=False,
            **self._get_model_kwargs(**kwargs),
        )

        if self.track_previous_responses:
            self._previous_response_id = response.id

        chat_response = OpenAIResponses._parse_response_output(response.output)
        chat_response.raw = response
        chat_response.additional_kwargs["usage"] = response.usage

        return chat_response

    @llm_retry_decorator
    async def_astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        message_dicts = to_openai_message_dicts(
            messages,
            model=self.model,
            is_responses_api=True,
        )

        async defgen() -> ChatResponseAsyncGen:
            built_in_tool_calls = []
            additional_kwargs = {"built_in_tool_calls": []}
            current_tool_call: Optional[ResponseFunctionToolCall] = None
            local_previous_response_id = self._previous_response_id

            response_stream = await self._aclient.responses.create(
                input=message_dicts,
                stream=True,
                **self._get_model_kwargs(**kwargs),
            )

            async for event in response_stream:
                # Process the event and update state
                (
                    blocks,
                    built_in_tool_calls,
                    additional_kwargs,
                    current_tool_call,
                    local_previous_response_id,
                    delta,
                ) = OpenAIResponses.process_response_event(
                    event=event,
                    built_in_tool_calls=built_in_tool_calls,
                    additional_kwargs=additional_kwargs,
                    current_tool_call=current_tool_call,
                    track_previous_responses=self.track_previous_responses,
                    previous_response_id=local_previous_response_id,
                )

                if (
                    self.track_previous_responses
                    and local_previous_response_id != self._previous_response_id
                ):
                    self._previous_response_id = local_previous_response_id

                if built_in_tool_calls:
                    additional_kwargs["built_in_tool_calls"] = built_in_tool_calls

                # For any event, yield a ChatResponse with the current state
                yield ChatResponse(
                    message=ChatMessage(
                        role=MessageRole.ASSISTANT,
                        blocks=blocks,
                    ),
                    delta=delta,
                    raw=event,
                    additional_kwargs=additional_kwargs,
                )

        return gen()

    def_prepare_chat_with_tools(
        self,
        tools: Sequence["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        allow_parallel_tool_calls: bool = True,
        tool_required: bool = False,
        tool_choice: Optional[Union[str, dict]] = None,
        verbose: bool = False,
        strict: Optional[bool] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
"""Predict and call the tool."""

        # openai responses api has a slightly different tool spec format
        tool_specs = [
            {
                "type": "function",
                **tool.metadata.to_openai_tool(skip_length_check=True)["function"],
            }
            for tool in tools
        ]

        if strict is not None:
            strict = strict
        else:
            strict = self.strict

        if strict:
            for tool_spec in tool_specs:
                tool_spec["strict"] = True
                tool_spec["parameters"]["additionalProperties"] = False

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        messages = chat_history or []
        if user_msg:
            messages.append(user_msg)

        return {
            "messages": messages,
            "tools": tool_specs or None,
            "tool_choice": resolve_tool_choice(tool_choice, tool_required)
            if tool_specs
            else None,
            "parallel_tool_calls": allow_parallel_tool_calls,
            **kwargs,
        }

    defget_tool_calls_from_response(
        self,
        response: "ChatResponse",
        error_on_no_tool_call: bool = True,
        **kwargs: Any,
    ) -> List[ToolSelection]:
"""Predict and call the tool."""
        tool_calls: List[ToolCallBlock] = [
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
            # this should handle both complete and partial jsons
            try:
                argument_dict = parse_partial_json(cast(str, tool_call.tool_kwargs))
            except Exception:
                argument_dict = {}

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
"""Structured predict using constrained decoding via responses.parse.

        Uses `text_format` with `tool_choice="none"` to guarantee JSON schema
        adherence at the API level, rather than best-effort function calling.
        """
        messages = prompt.format_messages(**prompt_args)
        message_dicts = to_openai_message_dicts(
            messages, model=self.model, is_responses_api=True
        )
        response = self._client.responses.parse(
            model=self.model,
            input=message_dicts,
            text_format=output_cls,
            tool_choice="none",
            store=self.store,
            **(llm_kwargs or {}),
        )
        if response.output_parsed is not None:
            return response.output_parsed
        raise ValueError("Failed to produce a structured response from the model.")

    @dispatcher.span
    async defastructured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
"""Async structured predict using constrained decoding via responses.parse.

        Uses `text_format` with `tool_choice="none"` to guarantee JSON schema
        adherence at the API level, rather than best-effort function calling.
        """
        messages = prompt.format_messages(**prompt_args)
        message_dicts = to_openai_message_dicts(
            messages, model=self.model, is_responses_api=True
        )
        response = await self._aclient.responses.parse(
            model=self.model,
            input=message_dicts,
            text_format=output_cls,
            tool_choice="none",
            store=self.store,
            **(llm_kwargs or {}),
        )
        if response.output_parsed is not None:
            return response.output_parsed
        raise ValueError("Failed to produce a structured response from the model.")

    @dispatcher.span
    defstream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Generator[Union[Model, FlexibleModel], None, None]:
"""Stream structured predict."""
        llm_kwargs = llm_kwargs or {}

        llm_kwargs["tool_choice"] = (
            "required" if "tool_choice" not in llm_kwargs else llm_kwargs["tool_choice"]
        )
        # by default structured prediction uses function calling to extract structured outputs
        # here we force tool_choice to be required
        return super().stream_structured_predict(
            output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
        )

    @dispatcher.span
    async defastream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> AsyncGenerator[Union[Model, FlexibleModel], None]:
"""Stream structured predict."""
        llm_kwargs = llm_kwargs or {}

        llm_kwargs["tool_choice"] = (
            "required" if "tool_choice" not in llm_kwargs else llm_kwargs["tool_choice"]
        )
        # by default structured prediction uses function calling to extract structured outputs
        # here we force tool_choice to be required
        return await super().astream_structured_predict(
            output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
        )

```
 |  
| --- | --- |  
###  process_response_event `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAIResponses.process_response_event "Permanent link")

```
process_response_event(
    event: ResponseStreamEvent,
    built_in_tool_calls: [],
    additional_kwargs: [, ],
    current_tool_call: Optional[ResponseFunctionToolCall],
    track_previous_responses: ,
    previous_response_id: Optional[] = None,
) -> Tuple[
    [ContentBlock],
    [],
    [, ],
    Optional[ResponseFunctionToolCall],
    Optional[],
    ,
]

```

Process a ResponseStreamEvent and update the state accordingly.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `event`  |  `ResponseStreamEvent`  |  The response stream event to process  |  _required_  |  
|  `content`  |  Current accumulated content string  |  _required_  |  
|  `tool_calls`  |  List of completed tool calls  |  _required_  |  
|  `built_in_tool_calls`  |  `List[Any]`  |  List of built-in tool calls  |  _required_  |  
|  `additional_kwargs`  |  `Dict[str, Any]`  |  Additional keyword arguments to include in ChatResponse  |  _required_  |  
|  `current_tool_call`  |  `Optional[ResponseFunctionToolCall]`  |  The currently in-progress tool call, if any  |  _required_  |  
|  `track_previous_responses`  |  `bool`  |  Whether to track previous response IDs  |  _required_  |  
|  `previous_response_id`  |  `Optional[str]`  |  Previous response ID if tracking  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[ContentBlock]`  |  A tuple containing the updated state:  |  
|  `List[Any]`  |  (content, tool_calls, built_in_tool_calls, additional_kwargs, current_tool_call, updated_previous_response_id, delta)  |  
Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/responses.py`  
| 
```
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
```
 | 
```
@staticmethod
defprocess_response_event(
    event: ResponseStreamEvent,
    built_in_tool_calls: List[Any],
    additional_kwargs: Dict[str, Any],
    current_tool_call: Optional[ResponseFunctionToolCall],
    track_previous_responses: bool,
    previous_response_id: Optional[str] = None,
) -> Tuple[
    List[ContentBlock],
    List[Any],
    Dict[str, Any],
    Optional[ResponseFunctionToolCall],
    Optional[str],
    str,
]:
"""
    Process a ResponseStreamEvent and update the state accordingly.

    Args:
        event: The response stream event to process
        content: Current accumulated content string
        tool_calls: List of completed tool calls
        built_in_tool_calls: List of built-in tool calls
        additional_kwargs: Additional keyword arguments to include in ChatResponse
        current_tool_call: The currently in-progress tool call, if any
        track_previous_responses: Whether to track previous response IDs
        previous_response_id: Previous response ID if tracking

    Returns:
        A tuple containing the updated state:
        (content, tool_calls, built_in_tool_calls, additional_kwargs, current_tool_call, updated_previous_response_id, delta)
    """
    delta = ""
    updated_previous_response_id = previous_response_id
    # we use blocks instead of content, since now we also support images! :)
    blocks: List[ContentBlock] = []
    if isinstance(event, ResponseCreatedEvent) or isinstance(
        event, ResponseInProgressEvent
    ):
        # Initial events, track the response id
        if track_previous_responses:
            updated_previous_response_id = event.response.id
    elif isinstance(event, ResponseOutputItemAddedEvent):
        # New output item (message, tool call, etc.)
        if isinstance(event.item, ResponseFunctionToolCall):
            current_tool_call = event.item
    elif isinstance(event, ResponseTextDeltaEvent):
        # Text content is being added
        delta = event.delta
        blocks.append(TextBlock(text=delta))
    elif isinstance(event, ResponseImageGenCallPartialImageEvent):
        # Partial image
        if event.partial_image_b64:
            blocks.append(
                ImageBlock(
                    image=base64.b64decode(event.partial_image_b64),
                    detail=f"id_{event.partial_image_index}",
                )
            )
    elif isinstance(event, ResponseFunctionCallArgumentsDeltaEvent):
        # Function call arguments are being streamed
        if current_tool_call is not None:
            current_tool_call.arguments += event.delta
    elif isinstance(event, ResponseFunctionCallArgumentsDoneEvent):
        # Function call arguments are complete
        if current_tool_call is not None:
            current_tool_call.arguments = event.arguments
            current_tool_call.status = "completed"
            blocks.append(
                ToolCallBlock(
                    tool_name=current_tool_call.name,
                    tool_kwargs=current_tool_call.arguments,
                    tool_call_id=current_tool_call.call_id,
                )
            )

            # clear the current tool call
            current_tool_call = None
    elif isinstance(event, ResponseOutputTextAnnotationAddedEvent):
        # Annotations for the text
        annotations = additional_kwargs.get("annotations", [])
        annotations.append(event.annotation)
        additional_kwargs["annotations"] = annotations
    elif isinstance(event, ResponseFileSearchCallCompletedEvent):
        # File search tool call completed
        built_in_tool_calls.append(event)
    elif isinstance(event, ResponseWebSearchCallCompletedEvent):
        # Web search tool call completed
        built_in_tool_calls.append(event)
    elif isinstance(event, ResponseOutputItemDoneEvent):
        # Reasoning information
        if isinstance(event.item, ResponseReasoningItem):
            content: Optional[str] = None
            if event.item.content:
                content = "\n".join([i.text for i in event.item.content])
            if event.item.summary:
                if content:
                    content += "\n" + "\n".join(
                        [i.text for i in event.item.summary]
                    )
                else:
                    content = "\n".join([i.text for i in event.item.summary])
            blocks.append(
                ThinkingBlock(
                    content=content,
                    additional_information=event.item.model_dump(
                        exclude={"content", "summary"}
                    ),
                )
            )
    elif isinstance(event, ResponseCompletedEvent):
        # Response is complete
        if hasattr(event, "response") and hasattr(event.response, "usage"):
            additional_kwargs["usage"] = event.response.usage
        resp = OpenAIResponses._parse_response_output(event.response.output)
        blocks = resp.message.blocks

    return (
        blocks,
        built_in_tool_calls,
        additional_kwargs,
        current_tool_call,
        updated_previous_response_id,
        delta,
    )

```
 |  
| --- | --- |  
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAIResponses.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
    **kwargs: 
) -> []

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/responses.py`  
| 
```
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
    tool_calls: List[ToolCallBlock] = [
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
        # this should handle both complete and partial jsons
        try:
            argument_dict = parse_partial_json(cast(str, tool_call.tool_kwargs))
        except Exception:
            argument_dict = {}

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
###  structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAIResponses.structured_predict "Permanent link")

```
structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> 

```

Structured predict using constrained decoding via responses.parse.
Uses `text_format` with `tool_choice="none"` to guarantee JSON schema adherence at the API level, rather than best-effort function calling.
Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/responses.py`  
| 
```
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
"""Structured predict using constrained decoding via responses.parse.

    Uses `text_format` with `tool_choice="none"` to guarantee JSON schema
    adherence at the API level, rather than best-effort function calling.
    """
    messages = prompt.format_messages(**prompt_args)
    message_dicts = to_openai_message_dicts(
        messages, model=self.model, is_responses_api=True
    )
    response = self._client.responses.parse(
        model=self.model,
        input=message_dicts,
        text_format=output_cls,
        tool_choice="none",
        store=self.store,
        **(llm_kwargs or {}),
    )
    if response.output_parsed is not None:
        return response.output_parsed
    raise ValueError("Failed to produce a structured response from the model.")

```
 |  
| --- | --- |  
###  astructured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAIResponses.astructured_predict "Permanent link")

```
astructured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> 

```

Async structured predict using constrained decoding via responses.parse.
Uses `text_format` with `tool_choice="none"` to guarantee JSON schema adherence at the API level, rather than best-effort function calling.
Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/responses.py`  
| 
```
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
"""Async structured predict using constrained decoding via responses.parse.

    Uses `text_format` with `tool_choice="none"` to guarantee JSON schema
    adherence at the API level, rather than best-effort function calling.
    """
    messages = prompt.format_messages(**prompt_args)
    message_dicts = to_openai_message_dicts(
        messages, model=self.model, is_responses_api=True
    )
    response = await self._aclient.responses.parse(
        model=self.model,
        input=message_dicts,
        text_format=output_cls,
        tool_choice="none",
        store=self.store,
        **(llm_kwargs or {}),
    )
    if response.output_parsed is not None:
        return response.output_parsed
    raise ValueError("Failed to produce a structured response from the model.")

```
 |  
| --- | --- |  
###  stream_structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAIResponses.stream_structured_predict "Permanent link")

```
stream_structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> Generator[Union[, FlexibleModel], None, None]

```

Stream structured predict.
Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/responses.py`  
| 
```
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
) -> Generator[Union[Model, FlexibleModel], None, None]:
"""Stream structured predict."""
    llm_kwargs = llm_kwargs or {}

    llm_kwargs["tool_choice"] = (
        "required" if "tool_choice" not in llm_kwargs else llm_kwargs["tool_choice"]
    )
    # by default structured prediction uses function calling to extract structured outputs
    # here we force tool_choice to be required
    return super().stream_structured_predict(
        output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
    )

```
 |  
| --- | --- |  
###  astream_structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai/#llama_index.llms.openai.OpenAIResponses.astream_structured_predict "Permanent link")

```
astream_structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> AsyncGenerator[Union[, FlexibleModel], None]

```

Stream structured predict.
Source code in `llama-index-integrations/llms/llama-index-llms-openai/llama_index/llms/openai/responses.py`  
| 
```
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
) -> AsyncGenerator[Union[Model, FlexibleModel], None]:
"""Stream structured predict."""
    llm_kwargs = llm_kwargs or {}

    llm_kwargs["tool_choice"] = (
        "required" if "tool_choice" not in llm_kwargs else llm_kwargs["tool_choice"]
    )
    # by default structured prediction uses function calling to extract structured outputs
    # here we force tool_choice to be required
    return await super().astream_structured_predict(
        output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
    )

```
 |  
| --- | --- |  
options: members: - OpenAI - OpenAIResponses
