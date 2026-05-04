# Alibabacloud aisearch
##  AlibabaCloudAISearchDocumentReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/alibabacloud_aisearch/#llama_index.readers.alibabacloud_aisearch.AlibabaCloudAISearchDocumentReader "Permanent link")
Bases: 
Supported file types include PPT/PPTX, DOC/DOCX, PDF, and more. For further details, please visit `https://help.aliyun.com/zh/open-search/search-platform/developer-reference/api-details`.
Source code in `llama-index-integrations/readers/llama-index-readers-alibabacloud-aisearch/llama_index/readers/alibabacloud_aisearch/base.py`  
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
```
 | 
```
classAlibabaCloudAISearchDocumentReader(BasePydanticReader):
"""
    Supported file types include PPT/PPTX, DOC/DOCX, PDF, and more.
    For further details, please visit `https://help.aliyun.com/zh/open-search/search-platform/developer-reference/api-details`.
    """

    _client: Client = PrivateAttr()

    aisearch_api_key: str = Field(default=None, exclude=True)
    endpoint: str = None

    service_id: str = "ops-document-analyze-001"
    workspace_name: str = "default"

    check_interval: int = 3
    num_workers: int = 4
    show_progress: bool = False

    def__init__(
        self, endpoint: str = None, aisearch_api_key: str = None, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.aisearch_api_key = get_from_param_or_env(
            "aisearch_api_key", aisearch_api_key, "AISEARCH_API_KEY"
        )
        self.endpoint = get_from_param_or_env("endpoint", endpoint, "AISEARCH_ENDPOINT")

        config = AISearchConfig(
            bearer_token=self.aisearch_api_key,
            endpoint=self.endpoint,
            protocol="http",
        )

        self._client = Client(config=config)

    # upload a document and get back a task_id
    @aretry_decorator
    async def_create_task(
        self,
        file_path: str,
        file_type: str,
        **load_kwargs: Any,
    ) -> str:
        if file_path.startswith("http"):
            file_name = os.path.basename(file_path.split("?")[0].split("#")[0])
            if not file_type:
                file_type = os.path.splitext(file_name)[1][1:]
            document = CreateDocumentAnalyzeTaskRequestDocument(
                url=file_path,
                file_name=file_name,
                file_type=file_type,
            )
        else:
            file_name = os.path.basename(file_path)
            if not file_type:
                file_type = os.path.splitext(file_name)[1][1:]
            document = CreateDocumentAnalyzeTaskRequestDocument(
                content=base64.b64encode(open(file_path, "rb").read()).decode(),
                file_name=file_name,
                file_type=file_type,
            )
        if not file_type:
            raise ValueError(
                "The file_type cannot be determined based on the file extension. Please specify it manually."
            )
        output = CreateDocumentAnalyzeTaskRequestOutput(
            image_storage=load_kwargs.get("image_storage", "url")
        )
        request = CreateDocumentAnalyzeTaskRequest(document=document, output=output)
        response: CreateDocumentAnalyzeTaskResponse = (
            await self._client.create_document_analyze_task_async(
                self.workspace_name, self.service_id, request
            )
        )
        return response.body.result.task_id

    async def_get_task_result(self, task_id: str) -> Document:
        request = GetDocumentAnalyzeTaskStatusRequest(task_id=task_id)
        while True:
            response: GetDocumentAnalyzeTaskStatusResponse = (
                await self._client.get_document_analyze_task_status_async(
                    self.workspace_name, self.service_id, request
                )
            )
            status = response.body.result.status
            if status == "PENDING":
                await asyncio.sleep(self.check_interval)
            elif status == "SUCCESS":
                data = response.body.result.data
                return Document(
                    text=data.content,
                    mimetype=f"text/{data.content_type}",
                )
            else:
                raise RuntimeError(
                    f"Failed to parse the file, error: {response.body.result.error}, task id: {task_id}"
                )

    async def_aload_data(
        self,
        file_path: str,
        file_type: str = None,
        **load_kwargs: Any,
    ) -> Document:
"""Load data from the input path."""
        task_id = await self._create_task(file_path, file_type, **load_kwargs)
        return await self._get_task_result(task_id)

    async defaload_data(
        self,
        file_path: Union[List[FilePath], FilePath],
        file_type: Union[List[FilePath], FilePath] = None,
        **load_kwargs: Any,
    ) -> List[Document]:
"""Load data from the input path."""
        if isinstance(file_path, (str, Path)):
            doc = await self._aload_data(str(file_path), file_type, **load_kwargs)
            return [doc]
        elif isinstance(file_path, list):
            if isinstance(file_type, list) and len(file_type) != len(file_path):
                raise ValueError(
                    "The length of file_type must be the same as file_path."
                )
            else:
                file_type = [file_type] * len(file_path)
            jobs = [
                self._aload_data(
                    str(f),
                    t,
                    **load_kwargs,
                )
                for f, t in zip(file_path, file_type)
            ]
            return await run_jobs(
                jobs,
                workers=self.num_workers,
                desc="Parsing files",
                show_progress=self.show_progress,
            )
        else:
            raise ValueError(
                "The input file_path must be a string or a list of strings."
            )

    defload_data(
        self,
        file_path: Union[List[FilePath], FilePath],
        **load_kwargs: Any,
    ) -> List[Document]:
"""Load data from the input path."""
        return asyncio.get_event_loop().run_until_complete(
            self.aload_data(file_path, **load_kwargs)
        )

```
 |  
| --- | --- |  
###  aload_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/alibabacloud_aisearch/#llama_index.readers.alibabacloud_aisearch.AlibabaCloudAISearchDocumentReader.aload_data "Permanent link")

```
aload_data(
    file_path: Union[[FilePath], FilePath],
    file_type: Union[[FilePath], FilePath] = None,
    **load_kwargs: 
) -> []

```

Load data from the input path.
Source code in `llama-index-integrations/readers/llama-index-readers-alibabacloud-aisearch/llama_index/readers/alibabacloud_aisearch/base.py`  
| 
```
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
```
 | 
```
async defaload_data(
    self,
    file_path: Union[List[FilePath], FilePath],
    file_type: Union[List[FilePath], FilePath] = None,
    **load_kwargs: Any,
) -> List[Document]:
"""Load data from the input path."""
    if isinstance(file_path, (str, Path)):
        doc = await self._aload_data(str(file_path), file_type, **load_kwargs)
        return [doc]
    elif isinstance(file_path, list):
        if isinstance(file_type, list) and len(file_type) != len(file_path):
            raise ValueError(
                "The length of file_type must be the same as file_path."
            )
        else:
            file_type = [file_type] * len(file_path)
        jobs = [
            self._aload_data(
                str(f),
                t,
                **load_kwargs,
            )
            for f, t in zip(file_path, file_type)
        ]
        return await run_jobs(
            jobs,
            workers=self.num_workers,
            desc="Parsing files",
            show_progress=self.show_progress,
        )
    else:
        raise ValueError(
            "The input file_path must be a string or a list of strings."
        )

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/alibabacloud_aisearch/#llama_index.readers.alibabacloud_aisearch.AlibabaCloudAISearchDocumentReader.load_data "Permanent link")

```
load_data(
    file_path: Union[[FilePath], FilePath],
    **load_kwargs: 
) -> []

```

Load data from the input path.
Source code in `llama-index-integrations/readers/llama-index-readers-alibabacloud-aisearch/llama_index/readers/alibabacloud_aisearch/base.py`  
| 
```
214
215
216
217
218
219
220
221
222
```
 | 
```
defload_data(
    self,
    file_path: Union[List[FilePath], FilePath],
    **load_kwargs: Any,
) -> List[Document]:
"""Load data from the input path."""
    return asyncio.get_event_loop().run_until_complete(
        self.aload_data(file_path, **load_kwargs)
    )

```
 |  
| --- | --- |  
##  AlibabaCloudAISearchImageReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/alibabacloud_aisearch/#llama_index.readers.alibabacloud_aisearch.AlibabaCloudAISearchImageReader "Permanent link")
Bases: `AlibabaCloudAISearchDocumentReader[](https://developers.llamaindex.ai/python/framework-api-reference/readers/alibabacloud_aisearch/#llama_index.readers.alibabacloud_aisearch.AlibabaCloudAISearchDocumentReader "AlibabaCloudAISearchDocumentReader \(llama_index.readers.alibabacloud_aisearch.base.AlibabaCloudAISearchDocumentReader\)")`
For further details, please visit `https://help.aliyun.com/zh/open-search/search-platform/developer-reference/opensearch-api-details`.
Source code in `llama-index-integrations/readers/llama-index-readers-alibabacloud-aisearch/llama_index/readers/alibabacloud_aisearch/base.py`  
| 
```
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
```
 | 
```
classAlibabaCloudAISearchImageReader(AlibabaCloudAISearchDocumentReader):
"""
    For further details, please visit `https://help.aliyun.com/zh/open-search/search-platform/developer-reference/opensearch-api-details`.
    """

    service_id: str = "ops-image-analyze-ocr-001"

    # upload a document and get back a task_id
    @aretry_decorator
    async def_create_task(
        self,
        file_path: str,
        file_type: str,
        **load_kwargs: Any,
    ) -> str:
        if file_path.startswith("data:"):
            prefix, content = file_path.split(",")
            if not file_type:
                m = re.match(r"^data:image/(\w+);base64$", prefix)
                file_type = m.group(1)
            file_name = f"image.{file_type}"
            document = CreateImageAnalyzeTaskRequestDocument(
                content=content,
                file_name=file_name,
                file_type=file_type,
            )
        elif file_path.startswith("http"):
            file_name = os.path.basename(file_path.split("?")[0].split("#")[0])
            if not file_type:
                file_type = os.path.splitext(file_name)[1][1:]
            document = CreateImageAnalyzeTaskRequestDocument(
                url=file_path,
                file_name=file_name,
                file_type=file_type,
            )
        else:
            file_name = os.path.basename(file_path)
            if not file_type:
                file_type = os.path.splitext(file_name)[1][1:]
            document = CreateImageAnalyzeTaskRequestDocument(
                content=base64.b64encode(open(file_path, "rb").read()).decode(),
                file_name=file_name,
                file_type=file_type,
            )
        if not file_type:
            raise ValueError(
                "The file_type cannot be determined based on the file extension. Please specify it manually."
            )
        request = CreateImageAnalyzeTaskRequest(document=document)
        response: CreateImageAnalyzeTaskResponse = (
            await self._client.create_image_analyze_task_async(
                self.workspace_name, self.service_id, request
            )
        )
        return response.body.result.task_id

    async def_get_task_result(self, task_id: str) -> Document:
        request = GetImageAnalyzeTaskStatusRequest(task_id=task_id)
        while True:
            response: GetImageAnalyzeTaskStatusResponse = (
                await self._client.get_image_analyze_task_status_async(
                    self.workspace_name, self.service_id, request
                )
            )
            status = response.body.result.status
            if status == "PENDING":
                await asyncio.sleep(self.check_interval)
            elif status == "SUCCESS":
                data = response.body.result.data
                return Document(
                    text=data.content,
                    mimetype=f"text/{data.content_type}",
                )
            else:
                raise RuntimeError(
                    f"Failed to parse the file, error: {response.body.result.error}, task id: {task_id}"
                )

```
 |  
| --- | --- |  
options: members: - AlibabaCloudAISearchDocumentReader - AlibabaCloudAISearchImageReader
