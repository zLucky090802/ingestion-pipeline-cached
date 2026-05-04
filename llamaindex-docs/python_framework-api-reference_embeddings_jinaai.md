# Jinaai
##  JinaEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/jinaai/#llama_index.embeddings.jinaai.JinaEmbedding "Permanent link")
Bases: 
JinaAI class for embeddings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  Model for embedding. Defaults to `jina-embeddings-v3`  |  `'jina-embeddings-v3'`  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-jinaai/llama_index/embeddings/jinaai/base.py`  
| 
```
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
```
 | 
```
classJinaEmbedding(MultiModalEmbedding):
"""
    JinaAI class for embeddings.

    Args:
        model (str): Model for embedding.
            Defaults to `jina-embeddings-v3`

    """

    api_key: Optional[str] = Field(default=None, description="The JinaAI API key.")
    model: str = Field(
        default="jina-embeddings-v3",
        description="The model to use when calling Jina AI API",
    )

    _encoding_queries: str = PrivateAttr()
    _encoding_documents: str = PrivateAttr()
    _task: str = PrivateAttr()
    _api: Any = PrivateAttr()

    def__init__(
        self,
        model: str = "jina-embeddings-v3",
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        api_key: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        encoding_queries: Optional[str] = None,
        encoding_documents: Optional[str] = None,
        task: Optional[str] = None,
        dimensions: Optional[int] = None,
        late_chunking: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            model=model,
            api_key=api_key,
            **kwargs,
        )
        self._encoding_queries = encoding_queries or "float"
        self._encoding_documents = encoding_documents or "float"
        self._task = task
        self._dimensions = dimensions
        self._late_chunking = late_chunking

        assert self._encoding_documents in VALID_ENCODING, (
            f"Encoding Documents parameter {self._encoding_documents} not supported. Please choose one of {VALID_ENCODING}"
        )
        assert self._encoding_queries in VALID_ENCODING, (
            f"Encoding Queries parameter {self._encoding_documents} not supported. Please choose one of {VALID_ENCODING}"
        )

        self._api = _JinaAPICaller(model=model, api_key=api_key)

    @classmethod
    defclass_name(cls) -> str:
        return "JinaAIEmbedding"

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self._api.get_embeddings(
            input=[query],
            encoding_type=self._encoding_queries,
            task=self._task,
            dimensions=self._dimensions,
            late_chunking=self._late_chunking,
        )[0]

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""The asynchronous version of _get_query_embedding."""
        result = await self._api.aget_embeddings(
            input=[query],
            encoding_type=self._encoding_queries,
            task=self._task,
            dimensions=self._dimensions,
            late_chunking=self._late_chunking,
        )
        return result[0]

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._get_text_embeddings([text])[0]

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get text embedding."""
        result = await self._aget_text_embeddings([text])
        return result[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return self._api.get_embeddings(
            input=texts,
            encoding_type=self._encoding_documents,
            task=self._task,
            dimensions=self._dimensions,
            late_chunking=self._late_chunking,
        )

    async def_aget_text_embeddings(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        return await self._api.aget_embeddings(
            input=texts,
            encoding_type=self._encoding_documents,
            task=self._task,
            dimensions=self._dimensions,
            late_chunking=self._late_chunking,
        )

    def_get_image_embedding(self, img_file_path: ImageType) -> List[float]:
        if is_local(img_file_path):
            input = [{"bytes": get_bytes_str(img_file_path)}]
        else:
            input = [{"url": img_file_path}]
        return self._api.get_embeddings(input=input)[0]

    async def_aget_image_embedding(self, img_file_path: ImageType) -> List[float]:
        if is_local(img_file_path):
            input = [{"bytes": get_bytes_str(img_file_path)}]
        else:
            input = [{"url": img_file_path}]
        return await self._api.aget_embeddings(input=input)[0]

    def_get_image_embeddings(
        self, img_file_paths: List[ImageType]
    ) -> List[List[float]]:
        input = []
        for img_file_path in img_file_paths:
            if is_local(img_file_path):
                input.append({"bytes": get_bytes_str(img_file_path)})
            else:
                input.append({"url": img_file_path})
        return self._api.get_embeddings(input=input)

    async def_aget_image_embeddings(
        self, img_file_paths: List[ImageType]
    ) -> List[List[float]]:
        input = []
        for img_file_path in img_file_paths:
            if is_local(img_file_path):
                input.append({"bytes": get_bytes_str(img_file_path)})
            else:
                input.append({"url": img_file_path})
        return await self._api.aget_embeddings(input=input)

```
 |  
| --- | --- |  
options: members: - JinaEmbedding
