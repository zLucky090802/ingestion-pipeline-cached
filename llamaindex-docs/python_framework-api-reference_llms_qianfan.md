# Qianfan
##  Qianfan [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan "Permanent link")
Bases: `CustomLLM`
The LLM supported by Baidu Intelligent Cloud's QIANFAN LLM Platform.
Source code in `llama-index-integrations/llms/llama-index-llms-qianfan/llama_index/llms/qianfan/base.py`  
| 
```
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
```
 | 
```
classQianfan(CustomLLM):
"""
    The LLM supported by Baidu Intelligent Cloud's QIANFAN LLM Platform.
    """

    access_key: str = Field(
        description="The Access Key obtained from the Security Authentication Center of Baidu Intelligent Cloud Console."
    )

    secret_key: str = Field(description="The Secret Key paired with the Access Key.")

    model_name: str = Field(description="The name of the model service.")

    endpoint_url: str = Field(description="The chat endpoint URL of the model service.")

    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW, description="The context window size."
    )

    llm_type: APIType = Field(default="chat", description="The LLM type.")

    _client = PrivateAttr()

    def__init__(
        self,
        access_key: str,
        secret_key: str,
        model_name: str,
        endpoint_url: str,
        context_window: int,
        llm_type: APIType = "chat",
    ) -> None:
"""
        Initialize a Qianfan LLM instance.

        :param access_key: The Access Key obtained from the Security Authentication Center
            of Baidu Intelligent Cloud Console.
        :param secret_key: The Secret Key paired with the Access Key.
        :param model_name: The name of the model service. For example: ERNIE-4.0-8K.
        :param endpoint_url: The chat endpoint URL of the model service.
            For example: https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro .
        :param context_windows: The context window size. for example: 8192.
        :param llm_type: The LLM type. Currently, only the chat type is supported.
        """
        if llm_type != "chat":
            raise NotImplementedError("Only the chat type is supported.")

        super().__init__(
            model_name=model_name,
            endpoint_url=endpoint_url,
            context_window=context_window,
            access_key=access_key,
            secret_key=secret_key,
            llm_type=llm_type,
        )
        self._client = Client(access_key, secret_key)

    @classmethod
    deffrom_model_name(
        cls,
        access_key: str,
        secret_key: str,
        model_name: str,
        context_window: int,
    ):
"""
        Initialize a Qianfan LLM instance. Then query more parameters based on the model name.

        :param access_key: The Access Key obtained from the Security Authentication Center
            of Baidu Intelligent Cloud Console.
        :param secret_key: The Secret Key paired with the Access Key.
        :param model_name: The name of the model service. For example: ERNIE-4.0-8K.
        :param context_windows: The context window size. for example: 8192.
        """
        service_list = get_service_list(access_key, secret_key, ["chat"])
        try:
            service = next(
                service for service in service_list if service.name == model_name
            )
        except StopIteration:
            raise NameError(f"not found {model_name}")

        return cls(
            access_key=access_key,
            secret_key=secret_key,
            model_name=model_name,
            endpoint_url=service.url,
            context_window=context_window,
            llm_type=service.api_type,
        )

    @classmethod
    async defafrom_model_name(
        cls,
        access_key: str,
        secret_key: str,
        model_name: str,
        context_window: int,
    ):
"""
        Initialize a Qianfan LLM instance. Then asynchronously query more parameters based on the model name.

        :param access_key: The Access Key obtained from the Security Authentication Center of
            Baidu Intelligent Cloud Console.
        :param secret_key: The Secret Key paired with the Access Key.
        :param model_name: The name of the model service. For example: ERNIE-4.0-8K.
        :param context_windows: The context window size. for example: 8192.
            The LLMs developed by Baidu all carry context window size in their names.
        """
        service_list = await aget_service_list(access_key, secret_key, ["chat"])
        try:
            service = next(
                service for service in service_list if service.name == model_name
            )
        except StopIteration:
            raise NameError(f"not found {model_name}")

        return cls(
            access_key=access_key,
            secret_key=secret_key,
            model_name=model_name,
            endpoint_url=service.url,
            context_window=context_window,
            llm_type=service.api_type,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "Qianfan_LLM"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            is_chat_model=self.llm_type == "chat",
            model_name=self.model_name,
        )

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
"""
        Request a chat.

        :param messages: The chat message list. The last message is the current request,
            and the previous messages are the historical chat information. The number of
            members must be odd, and the role value of the odd-numbered messages must be
            "user", while the role value of the even-numbered messages must be "assistant".
        :return: The ChatResponse object.
        """
        request = build_chat_request(stream=False, messages=messages, **kwargs)
        resp_dict = self._client.post(self.endpoint_url, json=request.dict())
        return parse_chat_response(resp_dict)

    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
"""
        Asynchronous request for a chat.

        :param messages: The chat message list. The last message is the current request,
            and the previous messages are the historical chat information. The number of
            members must be odd, and the role value of the odd-numbered messages must be
            "user", while the role value of the even-numbered messages must be "assistant".
        :return: The ChatResponse object.
        """
        request = build_chat_request(stream=False, messages=messages, **kwargs)
        resp_dict = await self._client.apost(self.endpoint_url, json=request.dict())
        return parse_chat_response(resp_dict)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
"""
        Request a chat, and the response is returned in a stream.

        :param messages: The chat message list. The last message is the current request,
            and the previous messages are the historical chat information. The number of
            members must be odd, and the role value of the odd-numbered messages must be
            "user", while the role value of the even-numbered messages must be "assistant".
        :return: A ChatResponseGen object, which is a generator of ChatResponse.
        """
        request = build_chat_request(stream=True, messages=messages, **kwargs)

        defgen():
            resp_dict_iter = self._client.post_reply_stream(
                self.endpoint_url, json=request.dict()
            )
            yield from parse_stream_chat_response(resp_dict_iter)

        return gen()

    @llm_chat_callback()
    async defastream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
"""
        Asynchronous request a chat, and the response is returned in a stream.

        :param messages: The chat message list. The last message is the current request,
            and the previous messages are the historical chat information. The number of
            members must be odd, and the role value of the odd-numbered messages must be
            "user", while the role value of the even-numbered messages must be "assistant".
        :return: A ChatResponseAsyncGen object, which is a asynchronous generator of ChatResponse.
        """
        request = build_chat_request(stream=True, messages=messages, **kwargs)

        async defgen():
            resp_dict_iter = self._client.apost_reply_stream(
                self.endpoint_url, json=request.dict()
            )
            async for part in aparse_stream_chat_response(resp_dict_iter):
                yield part

        return gen()

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
"""
        Request to complete a message that begins with the specified prompt.
        The LLM developed by Baidu does not support the complete function.
        Here use a converter to convert the chat function to a complete function.

        :param prompt: The prompt message at the beginning of the completed content.
        :return: CompletionResponse.
        """
        complete_fn = chat_to_completion_decorator(self.chat)
        return complete_fn(prompt, **kwargs)

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
"""
        Asynchronous request to complete a message that begins with the specified prompt.
        The LLM developed by Baidu does not support the complete function.
        Here use a converter to convert the chat function to a complete function.

        :param prompt: The prompt message at the beginning of the completed content.
        :return: A CompletionResponse object.
        """
        complete_fn = achat_to_completion_decorator(self.achat)
        return await complete_fn(prompt, **kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
"""
        Request to complete a message that begins with the specified prompt,
        and the response is returned in a stream.
        The LLM developed by Baidu does not support the complete function.
        Here use a converter to convert the chat function to a complete function.

        :param prompt: The prompt message at the beginning of the completed content.
        :return: A CompletionResponseGen object.
        """
        complete_fn = stream_chat_to_completion_decorator(self.stream_chat)
        return complete_fn(prompt, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
"""
        Asynchronous request to complete a message that begins with the specified prompt,
        and the response is returned in a stream.
        The LLM developed by Baidu does not support the complete function.
        Here use a converter to convert the chat function to a complete function.

        :param prompt: The prompt message at the beginning of the completed content.
        :return: A CompletionResponseAsyncGen object.
        """
        complete_fn = astream_chat_to_completion_decorator(self.astream_chat)
        return await complete_fn(prompt, **kwargs)

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
###  from_model_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan.from_model_name "Permanent link")

```
from_model_name(
    access_key: ,
    secret_key: ,
    model_name: ,
    context_window: ,
)

```

Initialize a Qianfan LLM instance. Then query more parameters based on the model name.
:param access_key: The Access Key obtained from the Security Authentication Center of Baidu Intelligent Cloud Console. :param secret_key: The Secret Key paired with the Access Key. :param model_name: The name of the model service. For example: ERNIE-4.0-8K. :param context_windows: The context window size. for example: 8192.
Source code in `llama-index-integrations/llms/llama-index-llms-qianfan/llama_index/llms/qianfan/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_model_name(
    cls,
    access_key: str,
    secret_key: str,
    model_name: str,
    context_window: int,
):
"""
    Initialize a Qianfan LLM instance. Then query more parameters based on the model name.

    :param access_key: The Access Key obtained from the Security Authentication Center
        of Baidu Intelligent Cloud Console.
    :param secret_key: The Secret Key paired with the Access Key.
    :param model_name: The name of the model service. For example: ERNIE-4.0-8K.
    :param context_windows: The context window size. for example: 8192.
    """
    service_list = get_service_list(access_key, secret_key, ["chat"])
    try:
        service = next(
            service for service in service_list if service.name == model_name
        )
    except StopIteration:
        raise NameError(f"not found {model_name}")

    return cls(
        access_key=access_key,
        secret_key=secret_key,
        model_name=model_name,
        endpoint_url=service.url,
        context_window=context_window,
        llm_type=service.api_type,
    )

```
 |  
| --- | --- |  
###  afrom_model_name `async` `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan.afrom_model_name "Permanent link")

```
afrom_model_name(
    access_key: ,
    secret_key: ,
    model_name: ,
    context_window: ,
)

```

Initialize a Qianfan LLM instance. Then asynchronously query more parameters based on the model name.
:param access_key: The Access Key obtained from the Security Authentication Center of Baidu Intelligent Cloud Console. :param secret_key: The Secret Key paired with the Access Key. :param model_name: The name of the model service. For example: ERNIE-4.0-8K. :param context_windows: The context window size. for example: 8192. The LLMs developed by Baidu all carry context window size in their names.
Source code in `llama-index-integrations/llms/llama-index-llms-qianfan/llama_index/llms/qianfan/base.py`  
| 
```
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
```
 | 
```
@classmethod
async defafrom_model_name(
    cls,
    access_key: str,
    secret_key: str,
    model_name: str,
    context_window: int,
):
"""
    Initialize a Qianfan LLM instance. Then asynchronously query more parameters based on the model name.

    :param access_key: The Access Key obtained from the Security Authentication Center of
        Baidu Intelligent Cloud Console.
    :param secret_key: The Secret Key paired with the Access Key.
    :param model_name: The name of the model service. For example: ERNIE-4.0-8K.
    :param context_windows: The context window size. for example: 8192.
        The LLMs developed by Baidu all carry context window size in their names.
    """
    service_list = await aget_service_list(access_key, secret_key, ["chat"])
    try:
        service = next(
            service for service in service_list if service.name == model_name
        )
    except StopIteration:
        raise NameError(f"not found {model_name}")

    return cls(
        access_key=access_key,
        secret_key=secret_key,
        model_name=model_name,
        endpoint_url=service.url,
        context_window=context_window,
        llm_type=service.api_type,
    )

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-qianfan/llama_index/llms/qianfan/base.py`  
| 
```
274
275
276
277
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "Qianfan_LLM"

```
 |  
| --- | --- |  
###  chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan.chat "Permanent link")

```
chat(
    messages: Sequence[], **kwargs: 
) -> 

```

Request a chat.
:param messages: The chat message list. The last message is the current request, and the previous messages are the historical chat information. The number of members must be odd, and the role value of the odd-numbered messages must be "user", while the role value of the even-numbered messages must be "assistant". :return: The ChatResponse object.
Source code in `llama-index-integrations/llms/llama-index-llms-qianfan/llama_index/llms/qianfan/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
"""
    Request a chat.

    :param messages: The chat message list. The last message is the current request,
        and the previous messages are the historical chat information. The number of
        members must be odd, and the role value of the odd-numbered messages must be
        "user", while the role value of the even-numbered messages must be "assistant".
    :return: The ChatResponse object.
    """
    request = build_chat_request(stream=False, messages=messages, **kwargs)
    resp_dict = self._client.post(self.endpoint_url, json=request.dict())
    return parse_chat_response(resp_dict)

```
 |  
| --- | --- |  
###  achat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan.achat "Permanent link")

```
achat(
    messages: Sequence[], **kwargs: 
) -> 

```

Asynchronous request for a chat.
:param messages: The chat message list. The last message is the current request, and the previous messages are the historical chat information. The number of members must be odd, and the role value of the odd-numbered messages must be "user", while the role value of the even-numbered messages must be "assistant". :return: The ChatResponse object.
Source code in `llama-index-integrations/llms/llama-index-llms-qianfan/llama_index/llms/qianfan/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
async defachat(
    self,
    messages: Sequence[ChatMessage],
    **kwargs: Any,
) -> ChatResponse:
"""
    Asynchronous request for a chat.

    :param messages: The chat message list. The last message is the current request,
        and the previous messages are the historical chat information. The number of
        members must be odd, and the role value of the odd-numbered messages must be
        "user", while the role value of the even-numbered messages must be "assistant".
    :return: The ChatResponse object.
    """
    request = build_chat_request(stream=False, messages=messages, **kwargs)
    resp_dict = await self._client.apost(self.endpoint_url, json=request.dict())
    return parse_chat_response(resp_dict)

```
 |  
| --- | --- |  
###  stream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan.stream_chat "Permanent link")

```
stream_chat(
    messages: Sequence[], **kwargs: 
) -> ChatResponseGen

```

Request a chat, and the response is returned in a stream.
:param messages: The chat message list. The last message is the current request, and the previous messages are the historical chat information. The number of members must be odd, and the role value of the odd-numbered messages must be "user", while the role value of the even-numbered messages must be "assistant". :return: A ChatResponseGen object, which is a generator of ChatResponse.
Source code in `llama-index-integrations/llms/llama-index-llms-qianfan/llama_index/llms/qianfan/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
defstream_chat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponseGen:
"""
    Request a chat, and the response is returned in a stream.

    :param messages: The chat message list. The last message is the current request,
        and the previous messages are the historical chat information. The number of
        members must be odd, and the role value of the odd-numbered messages must be
        "user", while the role value of the even-numbered messages must be "assistant".
    :return: A ChatResponseGen object, which is a generator of ChatResponse.
    """
    request = build_chat_request(stream=True, messages=messages, **kwargs)

    defgen():
        resp_dict_iter = self._client.post_reply_stream(
            self.endpoint_url, json=request.dict()
        )
        yield from parse_stream_chat_response(resp_dict_iter)

    return gen()

```
 |  
| --- | --- |  
###  astream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan.astream_chat "Permanent link")

```
astream_chat(
    messages: Sequence[], **kwargs: 
) -> ChatResponseAsyncGen

```

Asynchronous request a chat, and the response is returned in a stream.
:param messages: The chat message list. The last message is the current request, and the previous messages are the historical chat information. The number of members must be odd, and the role value of the odd-numbered messages must be "user", while the role value of the even-numbered messages must be "assistant". :return: A ChatResponseAsyncGen object, which is a asynchronous generator of ChatResponse.
Source code in `llama-index-integrations/llms/llama-index-llms-qianfan/llama_index/llms/qianfan/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
async defastream_chat(
    self,
    messages: Sequence[ChatMessage],
    **kwargs: Any,
) -> ChatResponseAsyncGen:
"""
    Asynchronous request a chat, and the response is returned in a stream.

    :param messages: The chat message list. The last message is the current request,
        and the previous messages are the historical chat information. The number of
        members must be odd, and the role value of the odd-numbered messages must be
        "user", while the role value of the even-numbered messages must be "assistant".
    :return: A ChatResponseAsyncGen object, which is a asynchronous generator of ChatResponse.
    """
    request = build_chat_request(stream=True, messages=messages, **kwargs)

    async defgen():
        resp_dict_iter = self._client.apost_reply_stream(
            self.endpoint_url, json=request.dict()
        )
        async for part in aparse_stream_chat_response(resp_dict_iter):
            yield part

    return gen()

```
 |  
| --- | --- |  
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan.complete "Permanent link")

```
complete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Request to complete a message that begins with the specified prompt. The LLM developed by Baidu does not support the complete function. Here use a converter to convert the chat function to a complete function.
:param prompt: The prompt message at the beginning of the completed content. :return: CompletionResponse.
Source code in `llama-index-integrations/llms/llama-index-llms-qianfan/llama_index/llms/qianfan/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defcomplete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponse:
"""
    Request to complete a message that begins with the specified prompt.
    The LLM developed by Baidu does not support the complete function.
    Here use a converter to convert the chat function to a complete function.

    :param prompt: The prompt message at the beginning of the completed content.
    :return: CompletionResponse.
    """
    complete_fn = chat_to_completion_decorator(self.chat)
    return complete_fn(prompt, **kwargs)

```
 |  
| --- | --- |  
###  acomplete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan.acomplete "Permanent link")

```
acomplete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Asynchronous request to complete a message that begins with the specified prompt. The LLM developed by Baidu does not support the complete function. Here use a converter to convert the chat function to a complete function.
:param prompt: The prompt message at the beginning of the completed content. :return: A CompletionResponse object.
Source code in `llama-index-integrations/llms/llama-index-llms-qianfan/llama_index/llms/qianfan/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defacomplete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponse:
"""
    Asynchronous request to complete a message that begins with the specified prompt.
    The LLM developed by Baidu does not support the complete function.
    Here use a converter to convert the chat function to a complete function.

    :param prompt: The prompt message at the beginning of the completed content.
    :return: A CompletionResponse object.
    """
    complete_fn = achat_to_completion_decorator(self.achat)
    return await complete_fn(prompt, **kwargs)

```
 |  
| --- | --- |  
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan.stream_complete "Permanent link")

```
stream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseGen

```

Request to complete a message that begins with the specified prompt, and the response is returned in a stream. The LLM developed by Baidu does not support the complete function. Here use a converter to convert the chat function to a complete function.
:param prompt: The prompt message at the beginning of the completed content. :return: A CompletionResponseGen object.
Source code in `llama-index-integrations/llms/llama-index-llms-qianfan/llama_index/llms/qianfan/base.py`  
| 
```
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
@llm_completion_callback()
defstream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseGen:
"""
    Request to complete a message that begins with the specified prompt,
    and the response is returned in a stream.
    The LLM developed by Baidu does not support the complete function.
    Here use a converter to convert the chat function to a complete function.

    :param prompt: The prompt message at the beginning of the completed content.
    :return: A CompletionResponseGen object.
    """
    complete_fn = stream_chat_to_completion_decorator(self.stream_chat)
    return complete_fn(prompt, **kwargs)

```
 |  
| --- | --- |  
###  astream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/qianfan/#llama_index.llms.qianfan.Qianfan.astream_complete "Permanent link")

```
astream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseAsyncGen

```

Asynchronous request to complete a message that begins with the specified prompt, and the response is returned in a stream. The LLM developed by Baidu does not support the complete function. Here use a converter to convert the chat function to a complete function.
:param prompt: The prompt message at the beginning of the completed content. :return: A CompletionResponseAsyncGen object.
Source code in `llama-index-integrations/llms/llama-index-llms-qianfan/llama_index/llms/qianfan/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defastream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseAsyncGen:
"""
    Asynchronous request to complete a message that begins with the specified prompt,
    and the response is returned in a stream.
    The LLM developed by Baidu does not support the complete function.
    Here use a converter to convert the chat function to a complete function.

    :param prompt: The prompt message at the beginning of the completed content.
    :return: A CompletionResponseAsyncGen object.
    """
    complete_fn = astream_chat_to_completion_decorator(self.astream_chat)
    return await complete_fn(prompt, **kwargs)

```
 |  
| --- | --- |  
options: members: - Qianfan
