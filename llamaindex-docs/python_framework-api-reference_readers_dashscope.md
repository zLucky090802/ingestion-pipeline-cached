# Dashscope
##  DashScopeParse [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/dashscope/#llama_index.readers.dashscope.DashScopeParse "Permanent link")
Bases: 
A smart-parser for files.
Source code in `llama-index-integrations/readers/llama-index-readers-dashscope/llama_index/readers/dashscope/base.py`  
| 
```
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
```
 | 
```
classDashScopeParse(BasePydanticReader):
"""A smart-parser for files."""

    api_key: str = Field(
        default="",
        description="The API key for the DashScope API.",
        validate_default=True,
    )
    workspace_id: str = Field(
        default="",
        description="The Workspace  for the DashScope API.If not set, "
        "it will use the default workspace.",
        validate_default=True,
    )
    category_id: str = Field(
        default=DASHSCOPE_DEFAULT_DC_CATEGORY,
        description="The dc category for the DashScope API.If not set, "
        "it will use the default dc category.",
        validate_default=True,
    )
    base_url: str = Field(
        default=DASHSCOPE_DEFAULT_BASE_URL,
        description="The base URL of the DashScope Parsing API.",
        validate_default=True,
    )
    result_type: ResultType = Field(
        default=ResultType.DASHSCOPE_DOCMIND,
        description="The result type for the parser.",
    )
    num_workers: int = Field(
        default=4,
        gt=0,
        lt=10,
        description="The number of workers to use sending API requests for parsing.",
    )
    check_interval: int = Field(
        default=5,
        description="The interval in seconds to check if the parsing is done.",
    )
    max_timeout: int = Field(
        default=3600,
        description="The maximum timeout in seconds to wait for the parsing to finish.",
    )
    verbose: bool = Field(
        default=True, description="Whether to print the progress of the parsing."
    )
    show_progress: bool = Field(
        default=True, description="Show progress when parsing multiple files."
    )
    ignore_errors: bool = Field(
        default=True,
        description="Whether or not to ignore and skip errors raised during parsing.",
    )
    parse_result: bool = Field(
        default=True,
        description="Whether or not to return parsed text content.",
    )

    @field_validator("api_key", mode="before", check_fields=True)
    defvalidate_api_key(cls, v: str) -> str:
"""Validate the API key."""
        if not v:
            importos

            api_key = os.getenv("DASHSCOPE_API_KEY", None)
            if api_key is None:
                raise ValueError("The API key [DASHSCOPE_API_KEY] is required.")
            return api_key

        return v

    @field_validator("workspace_id", mode="before", check_fields=True)
    defvalidate_workspace_id(cls, v: str) -> str:
"""Validate the Workspace."""
        if not v:
            importos

            return os.getenv("DASHSCOPE_WORKSPACE_ID", "")

        return v

    @field_validator("category_id", mode="before", check_fields=True)
    defvalidate_category_id(cls, v: str) -> str:
"""Validate the category."""
        if not v:
            importos

            return os.getenv("DASHSCOPE_CATEGORY_ID", DASHSCOPE_DEFAULT_DC_CATEGORY)
        return v

    @field_validator("base_url", mode="before", check_fields=True)
    defvalidate_base_url(cls, v: str) -> str:
"""Validate the base URL."""
        if v and v != DASHSCOPE_DEFAULT_BASE_URL:
            return v
        else:
            url = (
                os.getenv("DASHSCOPE_BASE_URL", None)
                or "https://dashscope.aliyuncs.com"
            )
            if url and not url.startswith(("http://", "https://")):
                raise ValueError(
                    "The DASHSCOPE_BASE_URL must start with http or https. "
                )
            return url or DASHSCOPE_DEFAULT_BASE_URL

    def_get_dashscope_header(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-WorkSpace": f"{self.workspace_id}",
            "X-DashScope-OpenAPISource": "CloudSDK",
        }

    # upload a document and get back a job_id
    async def_create_job(
        self, file_path: str, extra_info: Optional[dict] = None
    ) -> str:
        file_path = str(file_path)
        UploadFileLeaseResult.is_file_valid(file_path=file_path)

        headers = self._get_dashscope_header()

        # load data
        with open(file_path, "rb") as f:
            upload_file_lease_result = self.__upload_lease(file_path, headers)

            upload_file_lease_result.upload(file_path, f)

            url = f"{self.base_url}/api/v1/datacenter/category/{self.category_id}/add_file"
            async with httpx.AsyncClient(timeout=self.max_timeout) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    json={
                        "lease_id": upload_file_lease_result.lease_id,
                        "parser": ResultType.DASHSCOPE_DOCMIND.value,
                    },
                )
            add_file_result = dashscope_response_handler(
                response, "add_file", AddFileResult, url=url
            )

        return add_file_result.file_id

    @retry(
        stop=stop_after_delay(60),
        wait=wait_exponential(multiplier=5, max=60),
        before_sleep=before_sleep_log(logger, logging.INFO),
        after=after_log(logger, logging.INFO),
        reraise=True,
        retry=retry_if_exception_type(RetryException),
    )
    def__upload_lease(self, file_path, headers):
        url = f"{self.base_url}/api/v1/datacenter/category/{self.category_id}/upload_lease"
        try:
            with httpx.Client(timeout=self.max_timeout) as client:
                response = client.post(
                    url,
                    headers=headers,
                    json={
                        "file_name": os.path.basename(file_path),
                        "size_bytes": os.path.getsize(file_path),
                        "content_md5": get_file_md5(file_path),
                    },
                )
        except httpx.ConnectTimeout:
            raise RetryException("Connect timeout")
        except httpx.ReadTimeout:
            raise RetryException("Read timeout")
        except httpx.NetworkError:
            raise RetryException("Network error")

        upload_file_lease_result = dashscope_response_handler(
            response, "upload_lease", UploadFileLeaseResult, url=url
        )
        logger.info(
            f"{file_path} upload lease result: {upload_file_lease_result.lease_id}"
        )
        return upload_file_lease_result

    async def_get_job_result(
        self, data_id: str, result_type: str, verbose: bool = False
    ) -> dict:
        result_url = f"{self.base_url}/api/v1/datacenter/category/{self.category_id}/file/{data_id}/download_lease"
        status_url = f"{self.base_url}/api/v1/datacenter/category/{self.category_id}/file/{data_id}/query"

        headers = self._get_dashscope_header()

        start = time.time()
        tries = 0
        while True:
            await asyncio.sleep(1)
            tries += 1
            query_file_result = await self._dashscope_query(
                data_id, headers, status_url
            )

            status = query_file_result.status
            if DatahubDataStatusEnum.PARSE_SUCCESS.value == status:
                async with httpx.AsyncClient(timeout=self.max_timeout) as client:
                    response = await client.post(
                        result_url, headers=headers, json={"file_id": data_id}
                    )
                    down_file_lease_result = dashscope_response_handler(
                        response,
                        "download_lease",
                        DownloadFileLeaseResult,
                        url=result_url,
                    )
                    if self.parse_result:
                        return {
                            result_type: down_file_lease_result.download(escape=True),
                            "job_id": data_id,
                        }
                    else:
                        return {result_type: "{}", "job_id": data_id}
            elif (
                DatahubDataStatusEnum.PARSING.value == status
                or DatahubDataStatusEnum.INIT.value == status
            ):
                end = time.time()
                if end - start  self.max_timeout:
                    raise Exception(f"Timeout while parsing the file: {data_id}")
                if verbose and tries % 5 == 0:
                    print(".", end="", flush=True)

                await asyncio.sleep(self.check_interval)

                continue
            else:
                raise Exception(
                    f"Failed to parse the file: {data_id}, status: {status}"
                )

    @retry(
        stop=stop_after_delay(60),
        wait=wait_exponential(multiplier=5, max=60),
        before_sleep=before_sleep_log(logger, logging.INFO),
        after=after_log(logger, logging.INFO),
        reraise=True,
        retry=retry_if_exception_type(RetryException),
    )
    async def_dashscope_query(self, data_id, headers, status_url):
        try:
            async with httpx.AsyncClient(timeout=self.max_timeout) as client:
                response = await client.post(
                    status_url, headers=headers, json={"file_id": data_id}
                )
                return dashscope_response_handler(
                    response, "query", QueryFileResult, url=status_url
                )
        except httpx.ConnectTimeout:
            raise RetryException("Connect timeout")
        except httpx.ReadTimeout:
            raise RetryException("Read timeout")
        except httpx.NetworkError:
            raise RetryException("Network error")

    async def_aload_data(
        self, file_path: str, extra_info: Optional[dict] = None, verbose: bool = False
    ) -> List[Document]:
"""Load data from the input path."""
        try:
            data_id = await self._create_job(file_path, extra_info=extra_info)
            logger.info(f"Started parsing the file [{file_path}] under [{data_id}]")

            result = await self._get_job_result(
                data_id, self.result_type.value, verbose=verbose
            )

            document = Document(
                text=result[self.result_type.value],
                metadata=extra_info or {},
            )
            document.id_ = data_id

            return [document]

        except Exception as e:
            logger.error(f"Error while parsing the file '{file_path}':{e!s}")
            if self.ignore_errors:
                return []
            else:
                raise

    async defaload_data(
        self, file_path: Union[List[str], str], extra_info: Optional[dict] = None
    ) -> List[Document]:
"""Load data from the input path."""
        if isinstance(file_path, (str, Path)):
            return await self._aload_data(
                file_path, extra_info=extra_info, verbose=self.verbose
            )
        elif isinstance(file_path, list):
            jobs = [
                self._aload_data(
                    f,
                    extra_info=extra_info,
                    verbose=self.verbose and not self.show_progress,
                )
                for f in file_path
            ]
            try:
                results = await run_jobs(
                    jobs,
                    workers=self.num_workers,
                    desc="Parsing files",
                    show_progress=self.show_progress,
                )

                # return flattened results
                return [item for sublist in results for item in sublist]
            except RuntimeError as e:
                if nest_asyncio_err in str(e):
                    raise RuntimeError(nest_asyncio_msg)
                else:
                    raise
        else:
            raise ValueError(
                "The input file_path must be a string or a list of strings."
            )

    defload_data(
        self, file_path: Union[List[str], str], extra_info: Optional[dict] = None
    ) -> List[Document]:
        extra_info = {"parse_fmt_type": ResultType.DASHSCOPE_DOCMIND.value}
"""Load data from the input path."""
        try:
            return asyncio.run(self.aload_data(file_path, extra_info))
        except RuntimeError as e:
            if nest_asyncio_err in str(e):
                raise RuntimeError(nest_asyncio_msg)
            else:
                raise

    async def_aget_json(
        self, file_path: str, extra_info: Optional[dict] = None
    ) -> List[dict]:
"""Load data from the input path."""
        try:
            job_id = await self._create_job(file_path, extra_info=extra_info)
            if self.verbose:
                logger.info("Started parsing the file under job_id %s" % job_id)

            result = await self._get_job_result(
                job_id, ResultType.DASHSCOPE_DOCMIND.value
            )
            result["job_id"] = job_id
            result["file_path"] = file_path
            return [result]

        except Exception as e:
            logger.info(f"Error while parsing the file '{file_path}':", e)
            if self.ignore_errors:
                return []
            else:
                raise

    async defaget_json(
        self, file_path: Union[List[str], str], extra_info: Optional[dict] = None
    ) -> List[dict]:
"""Load data from the input path."""
        if isinstance(file_path, (str, Path)):
            return await self._aget_json(file_path, extra_info=extra_info)
        elif isinstance(file_path, list):
            jobs = [self._aget_json(f, extra_info=extra_info) for f in file_path]
            try:
                results = await run_jobs(
                    jobs,
                    workers=self.num_workers,
                    desc="Parsing files",
                    show_progress=self.show_progress,
                )

                # return flattened results
                return [item for sublist in results for item in sublist]
            except RuntimeError as e:
                if nest_asyncio_err in str(e):
                    raise RuntimeError(nest_asyncio_msg)
                else:
                    raise
        else:
            raise ValueError(
                "The input file_path must be a string or a list of strings."
            )

    defget_json_result(
        self, file_path: Union[List[str], str], extra_info: Optional[dict] = None
    ) -> List[dict]:
        extra_info = {"parse_fmt_type": ResultType.DASHSCOPE_DOCMIND.value}
"""Parse the input path."""
        try:
            return asyncio.run(self.aget_json(file_path, extra_info))
        except RuntimeError as e:
            if nest_asyncio_err in str(e):
                raise RuntimeError(nest_asyncio_msg)
            else:
                raise

    defget_images(self, json_result: List[dict], download_path: str) -> List[dict]:
        raise NotImplementedError

```
 |  
| --- | --- |  
###  validate_api_key [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/dashscope/#llama_index.readers.dashscope.DashScopeParse.validate_api_key "Permanent link")

```
validate_api_key(v: ) -> 

```

Validate the API key.
Source code in `llama-index-integrations/readers/llama-index-readers-dashscope/llama_index/readers/dashscope/base.py`  
| 
```
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
```
 | 
```
@field_validator("api_key", mode="before", check_fields=True)
defvalidate_api_key(cls, v: str) -> str:
"""Validate the API key."""
    if not v:
        importos

        api_key = os.getenv("DASHSCOPE_API_KEY", None)
        if api_key is None:
            raise ValueError("The API key [DASHSCOPE_API_KEY] is required.")
        return api_key

    return v

```
 |  
| --- | --- |  
###  validate_workspace_id [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/dashscope/#llama_index.readers.dashscope.DashScopeParse.validate_workspace_id "Permanent link")

```
validate_workspace_id(v: ) -> 

```

Validate the Workspace.
Source code in `llama-index-integrations/readers/llama-index-readers-dashscope/llama_index/readers/dashscope/base.py`  
| 
```
109
110
111
112
113
114
115
116
117
```
 | 
```
@field_validator("workspace_id", mode="before", check_fields=True)
defvalidate_workspace_id(cls, v: str) -> str:
"""Validate the Workspace."""
    if not v:
        importos

        return os.getenv("DASHSCOPE_WORKSPACE_ID", "")

    return v

```
 |  
| --- | --- |  
###  validate_category_id [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/dashscope/#llama_index.readers.dashscope.DashScopeParse.validate_category_id "Permanent link")

```
validate_category_id(v: ) -> 

```

Validate the category.
Source code in `llama-index-integrations/readers/llama-index-readers-dashscope/llama_index/readers/dashscope/base.py`  
| 
```
119
120
121
122
123
124
125
126
```
 | 
```
@field_validator("category_id", mode="before", check_fields=True)
defvalidate_category_id(cls, v: str) -> str:
"""Validate the category."""
    if not v:
        importos

        return os.getenv("DASHSCOPE_CATEGORY_ID", DASHSCOPE_DEFAULT_DC_CATEGORY)
    return v

```
 |  
| --- | --- |  
###  validate_base_url [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/dashscope/#llama_index.readers.dashscope.DashScopeParse.validate_base_url "Permanent link")

```
validate_base_url(v: ) -> 

```

Validate the base URL.
Source code in `llama-index-integrations/readers/llama-index-readers-dashscope/llama_index/readers/dashscope/base.py`  
| 
```
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
```
 | 
```
@field_validator("base_url", mode="before", check_fields=True)
defvalidate_base_url(cls, v: str) -> str:
"""Validate the base URL."""
    if v and v != DASHSCOPE_DEFAULT_BASE_URL:
        return v
    else:
        url = (
            os.getenv("DASHSCOPE_BASE_URL", None)
            or "https://dashscope.aliyuncs.com"
        )
        if url and not url.startswith(("http://", "https://")):
            raise ValueError(
                "The DASHSCOPE_BASE_URL must start with http or https. "
            )
        return url or DASHSCOPE_DEFAULT_BASE_URL

```
 |  
| --- | --- |  
###  aload_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/dashscope/#llama_index.readers.dashscope.DashScopeParse.aload_data "Permanent link")

```
aload_data(
    file_path: Union[[], ],
    extra_info: Optional[] = None,
) -> []

```

Load data from the input path.
Source code in `llama-index-integrations/readers/llama-index-readers-dashscope/llama_index/readers/dashscope/base.py`  
| 
```
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
```
 | 
```
async defaload_data(
    self, file_path: Union[List[str], str], extra_info: Optional[dict] = None
) -> List[Document]:
"""Load data from the input path."""
    if isinstance(file_path, (str, Path)):
        return await self._aload_data(
            file_path, extra_info=extra_info, verbose=self.verbose
        )
    elif isinstance(file_path, list):
        jobs = [
            self._aload_data(
                f,
                extra_info=extra_info,
                verbose=self.verbose and not self.show_progress,
            )
            for f in file_path
        ]
        try:
            results = await run_jobs(
                jobs,
                workers=self.num_workers,
                desc="Parsing files",
                show_progress=self.show_progress,
            )

            # return flattened results
            return [item for sublist in results for item in sublist]
        except RuntimeError as e:
            if nest_asyncio_err in str(e):
                raise RuntimeError(nest_asyncio_msg)
            else:
                raise
    else:
        raise ValueError(
            "The input file_path must be a string or a list of strings."
        )

```
 |  
| --- | --- |  
###  aget_json [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/dashscope/#llama_index.readers.dashscope.DashScopeParse.aget_json "Permanent link")

```
aget_json(
    file_path: Union[[], ],
    extra_info: Optional[] = None,
) -> []

```

Load data from the input path.
Source code in `llama-index-integrations/readers/llama-index-readers-dashscope/llama_index/readers/dashscope/base.py`  
| 
```
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
```
 | 
```
async defaget_json(
    self, file_path: Union[List[str], str], extra_info: Optional[dict] = None
) -> List[dict]:
"""Load data from the input path."""
    if isinstance(file_path, (str, Path)):
        return await self._aget_json(file_path, extra_info=extra_info)
    elif isinstance(file_path, list):
        jobs = [self._aget_json(f, extra_info=extra_info) for f in file_path]
        try:
            results = await run_jobs(
                jobs,
                workers=self.num_workers,
                desc="Parsing files",
                show_progress=self.show_progress,
            )

            # return flattened results
            return [item for sublist in results for item in sublist]
        except RuntimeError as e:
            if nest_asyncio_err in str(e):
                raise RuntimeError(nest_asyncio_msg)
            else:
                raise
    else:
        raise ValueError(
            "The input file_path must be a string or a list of strings."
        )

```
 |  
| --- | --- |  
##  ResultType [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/dashscope/#llama_index.readers.dashscope.ResultType "Permanent link")
Bases: `Enum`
The result type for the parser.
Source code in `llama-index-integrations/readers/llama-index-readers-dashscope/llama_index/readers/dashscope/utils.py`  
| 
```
145
146
147
148
```
 | 
```
classResultType(Enum):
"""The result type for the parser."""

    DASHSCOPE_DOCMIND = "DASHSCOPE_DOCMIND"

```
 |  
| --- | --- |  
options: members: - DashScopeParse
