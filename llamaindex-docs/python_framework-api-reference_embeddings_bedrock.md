# Bedrock
##  BedrockEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/bedrock/#llama_index.embeddings.bedrock.BedrockEmbedding "Permanent link")
Bases: 
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-bedrock/llama_index/embeddings/bedrock/base.py`  
| 
```
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
```
 | 
```
classBedrockEmbedding(BaseEmbedding):
    model_name: str = Field(description="The modelId of the Bedrock model to use.")
    profile_name: Optional[str] = Field(
        default=None,
        description="The name of aws profile to use. If not given, then the default profile is used.",
    )
    aws_access_key_id: Optional[str] = Field(
        default=None, description="AWS Access Key ID to use"
    )
    aws_secret_access_key: Optional[str] = Field(
        default=None, description="AWS Secret Access Key to use"
    )
    aws_session_token: Optional[str] = Field(
        default=None, description="AWS Session Token to use"
    )
    region_name: Optional[str] = Field(
        default=None,
        description="AWS region name to use. Uses region configured in AWS CLI if not passed",
    )
    botocore_session: Optional[Any] = Field(
        default=None,
        description="Use this Botocore session instead of creating a new default one.",
        exclude=True,
    )
    botocore_config: Optional[Any] = Field(
        default=None,
        description="Custom configuration object to use instead of the default generated one.",
        exclude=True,
    )
    max_retries: int = Field(
        default=10, description="The maximum number of API retries.", gt=0
    )
    timeout: float = Field(
        default=60.0,
        description="The timeout for the Bedrock API request in seconds. It will be used for both connect and read timeouts.",
    )
    application_inference_profile_arn: Optional[str] = Field(
        description="The ARN of an application inference profile to use when calling Bedrock. If provided, make sure that the model_name argument refers to the same model of the application inference profile."
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the bedrock client."
    )

    _config: Any = PrivateAttr()
    _client: Any = PrivateAttr()
    _asession: Any = PrivateAttr()

    def__init__(
        self,
        model_name: str = Models.TITAN_EMBEDDING,
        profile_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        region_name: Optional[str] = None,
        client: Optional[Any] = None,
        botocore_session: Optional[Any] = None,
        botocore_config: Optional[Any] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 10,
        timeout: float = 60.0,
        application_inference_profile_arn: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        # base class
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        **kwargs: Any,
    ):
        if "model" in kwargs:
            raise ValueError(
                "The 'model' parameter is not supported. "
                "Please use 'model_name' instead to specify the Bedrock model ID."
            )

        additional_kwargs = additional_kwargs or {}

        session_kwargs = {
            "profile_name": profile_name,
            "region_name": region_name,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "aws_session_token": aws_session_token,
            "botocore_session": botocore_session,
        }

        super().__init__(
            model_name=model_name,
            max_retries=max_retries,
            timeout=timeout,
            application_inference_profile_arn=application_inference_profile_arn,
            botocore_config=botocore_config,
            profile_name=profile_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name,
            botocore_session=botocore_session,
            additional_kwargs=additional_kwargs,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            **kwargs,
        )

        try:
            importaioboto3
            importboto3
            frombotocore.configimport Config

            self._config = (
                Config(
                    retries={"max_attempts": max_retries, "mode": "standard"},
                    connect_timeout=timeout,
                    read_timeout=timeout,
                    user_agent_extra="x-client-framework:llama_index",
                )
                if botocore_config is None
                else botocore_config
            )
            session = boto3.Session(**session_kwargs)
            self._asession = aioboto3.Session(**session_kwargs)
        except ImportError:
            raise ImportError(
                "boto3 and/or aioboto3 package not found, install with'pip install boto3 aioboto3"
            )

        # Prior to general availability, custom boto3 wheel files were
        # distributed that used the bedrock service to invokeModel.
        # This check prevents any services still using those wheel files
        # from breaking
        if client is not None:
            self._client = client
        elif "bedrock-runtime" in session.get_available_services():
            self._client = session.client("bedrock-runtime", config=self._config)
        else:
            self._client = session.client("bedrock", config=self._config)

    @staticmethod
    deflist_supported_models() -> Dict[str, List[str]]:
        list_models = {}
        for provider in PROVIDERS:
            list_models[provider.value] = [
                m.value for m in Models if provider.value in m.value
            ]
        return list_models

    @classmethod
    defclass_name(cls) -> str:
        return "BedrockEmbedding"

    @deprecated(
        version="0.9.48",
        reason=(
            "Use the provided kwargs in the constructor, set_credentials will be removed in future releases."
        ),
        action="once",
    )
    defset_credentials(
        self,
        aws_region: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        aws_profile: Optional[str] = None,
    ) -> None:
        aws_region = aws_region or os.getenv("AWS_REGION")
        aws_access_key_id = aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = aws_secret_access_key or os.getenv(
            "AWS_SECRET_ACCESS_KEY"
        )
        aws_session_token = aws_session_token or os.getenv("AWS_SESSION_TOKEN")

        if aws_region is None:
            warnings.warn(
                "AWS_REGION not found. Set environment variable AWS_REGION or set aws_region"
            )

        if aws_access_key_id is None:
            warnings.warn(
                "AWS_ACCESS_KEY_ID not found. Set environment variable AWS_ACCESS_KEY_ID or set aws_access_key_id"
            )
            assert aws_access_key_id is not None

        if aws_secret_access_key is None:
            warnings.warn(
                "AWS_SECRET_ACCESS_KEY not found. Set environment variable AWS_SECRET_ACCESS_KEY or set aws_secret_access_key"
            )
            assert aws_secret_access_key is not None

        if aws_session_token is None:
            warnings.warn(
                "AWS_SESSION_TOKEN not found. Set environment variable AWS_SESSION_TOKEN or set aws_session_token"
            )
            assert aws_session_token is not None

        session_kwargs = {
            "profile_name": aws_profile,
            "region_name": aws_region,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "aws_session_token": aws_session_token,
        }

        try:
            importboto3
            frombotocore.configimport Config

            session = boto3.Session(**session_kwargs)
        except ImportError:
            raise ImportError(
                "boto3 package not found, install with'pip install boto3'"
            )

        if "bedrock-runtime" in session.get_available_services():
            config = Config(user_agent_extra="x-client-framework:llama_index")
            self._client = session.client("bedrock-runtime", config=config)
        else:
            self._client = session.client("bedrock")

    @classmethod
    @deprecated(
        version="0.9.48",
        reason=(
            "Use the provided kwargs in the constructor, set_credentials will be removed in future releases."
        ),
        action="once",
    )
    deffrom_credentials(
        cls,
        model_name: str = Models.TITAN_EMBEDDING,
        aws_region: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        aws_profile: Optional[str] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
        verbose: bool = False,
    ) -> "BedrockEmbedding":
"""
        Instantiate using AWS credentials.

        Args:
            model_name (str) : Name of the model
            aws_access_key_id (str): AWS access key ID
            aws_secret_access_key (str): AWS secret access key
            aws_session_token (str): AWS session token
            aws_region (str): AWS region where the service is located
            aws_profile (str): AWS profile, when None, default profile is chosen automatically

        Example:
                .. code-block:: python

                    from llama_index.embeddings import BedrockEmbedding

                    # Define the model name
                    model_name = "your_model_name"

                    embeddings = BedrockEmbedding.from_credentials(
                        model_name,
                        aws_access_key_id,
                        aws_secret_access_key,
                        aws_session_token,
                        aws_region,
                        aws_profile,


        """
        session_kwargs = {
            "profile_name": aws_profile,
            "region_name": aws_region,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "aws_session_token": aws_session_token,
        }

        try:
            importboto3
            frombotocore.configimport Config

            session = boto3.Session(**session_kwargs)
        except ImportError:
            raise ImportError(
                "boto3 package not found, install with'pip install boto3'"
            )

        if "bedrock-runtime" in session.get_available_services():
            config = Config(user_agent_extra="x-client-framework:llama_index")
            client = session.client("bedrock-runtime", config=config)
        else:
            client = session.client("bedrock")
        return cls(
            client=client,
            model=model_name,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            verbose=verbose,
        )

    def_get_provider(self) -> str:
"""
        Extract the provider name from the model_name.

        Bedrock model names follow different formats:
        - 2-part format: "provider.model" (e.g., "amazon.titan-embed-text-v1")
        - 3-part format: "region.provider.model" (e.g., "us.amazon.titan-embed-text-v1")
          where region can be "us", "eu", "global", etc.

        Returns:
            str: The provider name (e.g., "amazon", "cohere")

        Raises:
            ValueError: If the model_name format is unexpected (not 2 or 3 parts)

        """
        model_identifier = self.model_name.split("/")[-1]
        model_parts = model_identifier.split(".")
        if len(model_parts) == 2:
            return model_parts[0]
        elif len(model_parts) == 3:
            return model_parts[1]
        else:
            raise ValueError(
                f"Unexpected number of parts in model_name: {model_identifier}"
            )

    def_get_embedding(
        self, payload: Union[str, List[str]], type: Literal["text", "query"]
    ) -> Union[Embedding, List[Embedding]]:
"""
        Get the embedding for the given payload.

        Args:
            payload (Union[str, List[str]]): The text or list of texts for which the embeddings are to be obtained.
            type (Literal[&quot;text&quot;, &quot;query&quot;]): The type of the payload. It can be either "text" or "query".

        Returns:
            Union[Embedding, List[Embedding]]: The embedding or list of embeddings for the given payload. If the payload is a list of strings, then the response will be a list of embeddings.

        """
        if self._client is None:
            self.set_credentials()

        if self._client is None:
            raise ValueError("Client not set")

        provider = self._get_provider()
        request_body = self._get_request_body(provider, payload, type)

        response = self._client.invoke_model(
            body=request_body,
            modelId=self.application_inference_profile_arn or self.model_name,
            accept="application/json",
            contentType="application/json",
        )

        resp = json.loads(response.get("body").read().decode("utf-8"))
        identifiers = PROVIDER_SPECIFIC_IDENTIFIERS.get(provider)
        if identifiers is None:
            raise ValueError("Provider not supported")
        return identifiers["get_embeddings_func"](resp, isinstance(payload, list))

    def_get_query_embedding(self, query: str) -> Embedding:
        return self._get_embedding(query, "query")

    def_get_text_embedding(self, text: str) -> Embedding:
        return self._get_embedding(text, "text")

    def_get_text_embeddings(self, texts: List[str]) -> List[Embedding]:
        provider = self._get_provider()
        if provider == PROVIDERS.COHERE:
            return self._get_embedding(texts, "text")
        return super()._get_text_embeddings(texts)

    def_get_request_body(
        self,
        provider: str,
        payload: Union[str, List[str]],
        input_type: Literal["text", "query"],
    ) -> Any:
"""
        Build the request body as per the provider.
        Currently supported providers are amazon, cohere.

        amazon:
            Sample Payload of type str
            "Hello World!"

        cohere:
            Sample Payload of type dict of following format

                'texts': ["This is a test document", "This is another document"],
                'input_type': 'search_document'


        """
        if provider == PROVIDERS.AMAZON:
            if isinstance(payload, list):
                raise ValueError("Amazon provider does not support list of texts")

            titan_body_request = {"inputText": payload}

            # Titan Embedding V2.0 has additional body parameters to check.
            if "dimensions" in self.additional_kwargs:
                if self.model_name == Models.TITAN_EMBEDDING_V2_0:
                    titan_body_request["dimensions"] = self.additional_kwargs[
                        "dimensions"
                    ]
                else:
                    raise ValueError(
                        "'dimensions' param not supported outside of 'titan-embed-text-v2:0' model."
                    )
            if "normalize" in self.additional_kwargs:
                if self.model_name == Models.TITAN_EMBEDDING_V2_0:
                    titan_body_request["normalize"] = self.additional_kwargs[
                        "normalize"
                    ]
                else:
                    raise ValueError(
                        "'normalize' param not supported outside of 'titan-embed-text-v2:0' model."
                    )

            request_body = json.dumps(titan_body_request)

        elif provider == PROVIDERS.COHERE:
            input_types = {
                "text": "search_document",
                "query": "search_query",
            }
            payload = [payload] if isinstance(payload, str) else payload
            payload = [p[:2048] if len(p)  2048 else p for p in payload]
            request_body = json.dumps(
                {
                    "texts": payload,
                    "input_type": input_types[input_type],
                }
            )
        else:
            raise ValueError("Provider not supported")
        return request_body

    async def_aget_embedding(
        self, payload: Union[str, List[str]], type: Literal["text", "query"]
    ) -> Union[Embedding, List[Embedding]]:
"""
        Get the embedding asynchronously for the given payload.

        Args:
            payload (Union[str, List[str]]): The text or list of texts for which the embeddings are to be obtained.
            type (Literal[&quot;text&quot;, &quot;query&quot;]): The type of the payload. It can be either "text" or "query".

        Returns:
            Union[Embedding, List[Embedding]]: The embedding or list of embeddings for the given payload. If the payload is a list of strings, then the response will be a list of embeddings.

        """
        if self._asession is None:
            raise ValueError("Client not set")

        provider = self._get_provider()
        request_body = self._get_request_body(provider, payload, type)

        async with self._asession.client(
            "bedrock-runtime", config=self._config
        ) as client:
            response = await client.invoke_model(
                body=request_body,
                modelId=self.application_inference_profile_arn or self.model_name,
                accept="application/json",
                contentType="application/json",
            )
            streaming_body = await response.get("body").read()
            resp = json.loads(streaming_body.decode("utf-8"))

        identifiers = PROVIDER_SPECIFIC_IDENTIFIERS.get(provider)
        if identifiers is None:
            raise ValueError("Provider not supported")
        return identifiers["get_embeddings_func"](resp, isinstance(payload, list))

    async def_aget_query_embedding(self, query: str) -> Embedding:
        return await self._aget_embedding(query, "query")

    async def_aget_text_embedding(self, text: str) -> Embedding:
        return await self._aget_embedding(text, "text")

```
 |  
| --- | --- |  
###  from_credentials `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/bedrock/#llama_index.embeddings.bedrock.BedrockEmbedding.from_credentials "Permanent link")

```
from_credentials(
    model_name:  = TITAN_EMBEDDING,
    aws_region: Optional[] = None,
    aws_access_key_id: Optional[] = None,
    aws_secret_access_key: Optional[] = None,
    aws_session_token: Optional[] = None,
    aws_profile: Optional[] = None,
    embed_batch_size:  = DEFAULT_EMBED_BATCH_SIZE,
    callback_manager: Optional[] = None,
    verbose:  = False,
) -> 

```

Instantiate using AWS credentials.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_name (str) `  |  Name of the model  |  _required_  |  
|  `aws_access_key_id`  |  AWS access key ID  |  `None`  |  
|  `aws_secret_access_key`  |  AWS secret access key  |  `None`  |  
|  `aws_session_token`  |  AWS session token  |  `None`  |  
|  `aws_region`  |  AWS region where the service is located  |  `None`  |  
|  `aws_profile`  |  AWS profile, when None, default profile is chosen automatically  |  `None`  |  
Example
.. code-block:: python

```
from llama_index.embeddings import BedrockEmbedding

# Define the model name
model_name = "your_model_name"

embeddings = BedrockEmbedding.from_credentials(
    model_name,
    aws_access_key_id,
    aws_secret_access_key,
    aws_session_token,
    aws_region,
    aws_profile,
)

```
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-bedrock/llama_index/embeddings/bedrock/base.py`  
| 
```
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
```
 | 
```
@classmethod
@deprecated(
    version="0.9.48",
    reason=(
        "Use the provided kwargs in the constructor, set_credentials will be removed in future releases."
    ),
    action="once",
)
deffrom_credentials(
    cls,
    model_name: str = Models.TITAN_EMBEDDING,
    aws_region: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
    aws_profile: Optional[str] = None,
    embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
    callback_manager: Optional[CallbackManager] = None,
    verbose: bool = False,
) -> "BedrockEmbedding":
"""
    Instantiate using AWS credentials.

    Args:
        model_name (str) : Name of the model
        aws_access_key_id (str): AWS access key ID
        aws_secret_access_key (str): AWS secret access key
        aws_session_token (str): AWS session token
        aws_region (str): AWS region where the service is located
        aws_profile (str): AWS profile, when None, default profile is chosen automatically

    Example:
            .. code-block:: python

                from llama_index.embeddings import BedrockEmbedding

                # Define the model name
                model_name = "your_model_name"

                embeddings = BedrockEmbedding.from_credentials(
                    model_name,
                    aws_access_key_id,
                    aws_secret_access_key,
                    aws_session_token,
                    aws_region,
                    aws_profile,


    """
    session_kwargs = {
        "profile_name": aws_profile,
        "region_name": aws_region,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "aws_session_token": aws_session_token,
    }

    try:
        importboto3
        frombotocore.configimport Config

        session = boto3.Session(**session_kwargs)
    except ImportError:
        raise ImportError(
            "boto3 package not found, install with'pip install boto3'"
        )

    if "bedrock-runtime" in session.get_available_services():
        config = Config(user_agent_extra="x-client-framework:llama_index")
        client = session.client("bedrock-runtime", config=config)
    else:
        client = session.client("bedrock")
    return cls(
        client=client,
        model=model_name,
        embed_batch_size=embed_batch_size,
        callback_manager=callback_manager,
        verbose=verbose,
    )

```
 |  
| --- | --- |  
options: members: - BedrockEmbedding
