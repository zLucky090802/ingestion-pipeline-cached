# Oci data science
##  OCIDataScienceEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/oci_data_science/#llama_index.embeddings.oci_data_science.OCIDataScienceEmbedding "Permanent link")
Bases: 
Embedding class for OCI Data Science models.
This class provides methods to generate embeddings using models deployed on Oracle Cloud Infrastructure (OCI) Data Science. It supports both synchronous and asynchronous requests and handles authentication, batching, and other configurations.
Setup
Install the required packages: 

```
pipinstall-Uoracle-adsllama-index-embeddings-oci-data-science

```

Configure authentication using `ads.set_auth()`. For example, to use OCI Resource Principal for authentication: 

```
importads
ads.set_auth("resource_principal")

```

For more details on authentication, see: https://accelerated-data-science.readthedocs.io/en/latest/user_guide/cli/authentication.html
Ensure you have the required policies to access the OCI Data Science Model Deployment endpoint: https://docs.oracle.com/en-us/iaas/data-science/using/model-dep-policies-auth.htm
To learn more about deploying LLM models in OCI Data Science, see: https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions-model-deploy.htm
Examples:
Basic Usage: 

```
importads
fromllama_index.embeddings.oci_data_scienceimport OCIDataScienceEmbedding

ads.set_auth(auth="security_token", profile="OC1")

embeddings = OCIDataScienceEmbedding(
    endpoint="https://<MD_OCID>/predict",
)

e1 = embeddings.get_text_embedding("This is a test document")
print(e1)

e2 = embeddings.get_text_embedding_batch([
    "This is a test document",
    "This is another test document"
])
print(e2)

```

Asynchronous Usage: 

```
importads
importasyncio
fromllama_index.embeddings.oci_data_scienceimport OCIDataScienceEmbedding

ads.set_auth(auth="security_token", profile="OC1")

embeddings = OCIDataScienceEmbedding(
    endpoint="https://<MD_OCID>/predict",
)

async defasync_embedding():
    e1 = await embeddings.aget_query_embedding("This is a test document")
    print(e1)

asyncio.run(async_embedding())

```

Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `endpoint`  |  The URI of the endpoint from the deployed model.  |  
|  `Dict[str, Any]`  |  The authentication dictionary used for OCI API requests.  |  
| `model_name`  |  The name of the OCI Data Science embedding model.  |  
| `embed_batch_size`  |  The batch size for embedding calls.  |  
| `additional_kwargs`  |  `Dict[str, Any]`  |  Additional keyword arguments for the OCI Data Science AI request.  |  
| `default_headers`  |  `Dict[str, str]`  |  The default headers for API requests.  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-oci-data-science/llama_index/embeddings/oci_data_science/base.py`  
| 
```
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
```
 | 
```
classOCIDataScienceEmbedding(BaseEmbedding):
"""
    Embedding class for OCI Data Science models.

    This class provides methods to generate embeddings using models deployed on
    Oracle Cloud Infrastructure (OCI) Data Science. It supports both synchronous
    and asynchronous requests and handles authentication, batching, and other
    configurations.

    Setup:
        Install the required packages:
        ```bash
        pip install -U oracle-ads llama-index-embeddings-oci-data-science
        ```

        Configure authentication using `ads.set_auth()`. For example, to use OCI
        Resource Principal for authentication:
        ```python
        import ads
        ads.set_auth("resource_principal")
        ```

        For more details on authentication, see:
        https://accelerated-data-science.readthedocs.io/en/latest/user_guide/cli/authentication.html

        Ensure you have the required policies to access the OCI Data Science Model
        Deployment endpoint:
        https://docs.oracle.com/en-us/iaas/data-science/using/model-dep-policies-auth.htm

        To learn more about deploying LLM models in OCI Data Science, see:
        https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions-model-deploy.htm

    Examples:
        Basic Usage:
        ```python
        import ads
        from llama_index.embeddings.oci_data_science import OCIDataScienceEmbedding

        ads.set_auth(auth="security_token", profile="OC1")

        embeddings = OCIDataScienceEmbedding(
            endpoint="https://<MD_OCID>/predict",


        e1 = embeddings.get_text_embedding("This is a test document")
        print(e1)

        e2 = embeddings.get_text_embedding_batch([
            "This is a test document",
            "This is another test document"

        print(e2)
        ```

        Asynchronous Usage:
        ```python
        import ads
        import asyncio
        from llama_index.embeddings.oci_data_science import OCIDataScienceEmbedding

        ads.set_auth(auth="security_token", profile="OC1")

        embeddings = OCIDataScienceEmbedding(
            endpoint="https://<MD_OCID>/predict",


        async def async_embedding():
            e1 = await embeddings.aget_query_embedding("This is a test document")
            print(e1)

        asyncio.run(async_embedding())
        ```

    Attributes:
        endpoint (str): The URI of the endpoint from the deployed model.
        auth (Dict[str, Any]): The authentication dictionary used for OCI API requests.
        model_name (str): The name of the OCI Data Science embedding model.
        embed_batch_size (int): The batch size for embedding calls.
        additional_kwargs (Dict[str, Any]): Additional keyword arguments for the OCI Data Science AI request.
        default_headers (Dict[str, str]): The default headers for API requests.

    """

    endpoint: str = Field(
        default=None, description="The URI of the endpoint from the deployed model."
    )

    auth: Union[Dict[str, Any], None] = Field(
        default_factory=dict,
        exclude=True,
        description=(
            "The authentication dictionary used for OCI API requests. "
            "If not provided, it will be autogenerated based on environment variables."
        ),
    )
    model_name: Optional[str] = Field(
        default=DEFAULT_MODEL,
        description="The name of the OCI Data Science embedding model to use.",
    )

    embed_batch_size: int = Field(
        default=DEFAULT_EMBED_BATCH_SIZE,
        description="The batch size for embedding calls.",
        gt=0,
        le=2048,
    )

    max_retries: int = Field(
        default=DEFAULT_MAX_RETRIES,
        description="The maximum number of API retries.",
        ge=0,
    )

    timeout: float = Field(
        default=DEFAULT_TIMEOUT, description="The timeout to use in seconds.", ge=0
    )

    additional_kwargs: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional keyword arguments for the OCI Data Science AI request.",
    )

    default_headers: Optional[Dict[str, str]] = Field(
        default_factory=dict, description="The default headers for API requests."
    )

    _client: Client = PrivateAttr()
    _async_client: AsyncClient = PrivateAttr()

    def__init__(
        self,
        endpoint: str,
        model_name: Optional[str] = DEFAULT_MODEL,
        auth: Dict[str, Any] = None,
        timeout: Optional[float] = DEFAULT_TIMEOUT,
        max_retries: Optional[int] = DEFAULT_MAX_RETRIES,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        default_headers: Optional[Dict[str, str]] = None,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
"""
        Initialize the OCIDataScienceEmbedding instance.

        Args:
            endpoint (str): The URI of the endpoint from the deployed model.
            model_name (Optional[str]): The name of the OCI Data Science embedding model to use. Defaults to "odsc-embeddings".
            auth (Optional[Dict[str, Any]]): The authentication dictionary for OCI API requests. Defaults to None.
            timeout (Optional[float]): The timeout setting for the HTTP request in seconds. Defaults to 120.
            max_retries (Optional[int]): The maximum number of retry attempts for the request. Defaults to 5.
            embed_batch_size (int): The batch size for embedding calls. Defaults to DEFAULT_EMBED_BATCH_SIZE.
            additional_kwargs (Optional[Dict[str, Any]]): Additional arguments for the OCI Data Science AI request. Defaults to None.
            default_headers (Optional[Dict[str, str]]): The default headers for API requests. Defaults to None.
            callback_manager (Optional[CallbackManager]): A callback manager for handling events during embedding operations. Defaults to None.
            **kwargs: Additional keyword arguments.

        """
        super().__init__(
            model_name=model_name,
            endpoint=endpoint,
            auth=auth,
            embed_batch_size=embed_batch_size,
            timeout=timeout,
            max_retries=max_retries,
            additional_kwargs=additional_kwargs or {},
            default_headers=default_headers or {},
            callback_manager=callback_manager,
            **kwargs,
        )

    @model_validator(mode="before")
    # @_validate_dependency
    defvalidate_env(cls, values: Dict[str, Any]) -> Dict[str, Any]:
"""
        Validate the environment and dependencies before initialization.

        Args:
            values (Dict[str, Any]): The values passed to the model.

        Returns:
            Dict[str, Any]: The validated values.

        Raises:
            ImportError: If required dependencies are missing.

        """
        return values

    @property
    defclient(self) -> Client:
"""
        Return the synchronous client instance.

        Returns:
            Client: The synchronous client for interacting with the OCI Data Science Model Deployment endpoint.

        """
        if not hasattr(self, "_client") or self._client is None:
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
        Return the asynchronous client instance.

        Returns:
            AsyncClient: The asynchronous client for interacting with the OCI Data Science Model Deployment endpoint.

        """
        if not hasattr(self, "_async_client") or self._async_client is None:
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
        Get the class name.

        Returns:
            str: The name of the class.

        """
        return "OCIDataScienceEmbedding"

    def_get_query_embedding(self, query: str) -> List[float]:
"""
        Generate an embedding for a query string.

        Args:
            query (str): The query string for which to generate an embedding.

        Returns:
            List[float]: The embedding vector for the query.

        """
        return self.client.embeddings(
            input=query, payload=self.additional_kwargs, headers=self.default_headers
        )["data"][0]["embedding"]

    def_get_text_embedding(self, text: str) -> List[float]:
"""
        Generate an embedding for a text string.

        Args:
            text (str): The text string for which to generate an embedding.

        Returns:
            List[float]: The embedding vector for the text.

        """
        return self.client.embeddings(
            input=text, payload=self.additional_kwargs, headers=self.default_headers
        )["data"][0]["embedding"]

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""
        Asynchronously generate an embedding for a text string.

        Args:
            text (str): The text string for which to generate an embedding.

        Returns:
            List[float]: The embedding vector for the text.

        """
        response = await self.async_client.embeddings(
            input=text, payload=self.additional_kwargs, headers=self.default_headers
        )
        return response["data"][0]["embedding"]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""
        Generate embeddings for a list of text strings.

        Args:
            texts (List[str]): A list of text strings for which to generate embeddings.

        Returns:
            List[List[float]]: A list of embedding vectors corresponding to the input texts.

        """
        response = self.client.embeddings(
            input=texts, payload=self.additional_kwargs, headers=self.default_headers
        )
        return [raw["embedding"] for raw in response["data"]]

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""
        Asynchronously generate an embedding for a query string.

        Args:
            query (str): The query string for which to generate an embedding.

        Returns:
            List[float]: The embedding vector for the query.

        """
        response = await self.async_client.embeddings(
            input=query, payload=self.additional_kwargs, headers=self.default_headers
        )
        return response["data"][0]["embedding"]

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""
        Asynchronously generate embeddings for a list of text strings.

        Args:
            texts (List[str]): A list of text strings for which to generate embeddings.

        Returns:
            List[List[float]]: A list of embedding vectors corresponding to the input texts.

        """
        response = await self.async_client.embeddings(
            input=texts, payload=self.additional_kwargs, headers=self.default_headers
        )
        return [raw["embedding"] for raw in response["data"]]

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/oci_data_science/#llama_index.embeddings.oci_data_science.OCIDataScienceEmbedding.client "Permanent link")

```
client: Client

```

Return the synchronous client instance.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Client`  |  `Client`  |  The synchronous client for interacting with the OCI Data Science Model Deployment endpoint.  |  
###  async_client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/oci_data_science/#llama_index.embeddings.oci_data_science.OCIDataScienceEmbedding.async_client "Permanent link")

```
async_client: AsyncClient

```

Return the asynchronous client instance.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `AsyncClient`  |  `AsyncClient`  |  The asynchronous client for interacting with the OCI Data Science Model Deployment endpoint.  |  
###  validate_env [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/oci_data_science/#llama_index.embeddings.oci_data_science.OCIDataScienceEmbedding.validate_env "Permanent link")

```
validate_env(values: [, ]) -> [, ]

```

Validate the environment and dependencies before initialization.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `values`  |  `Dict[str, Any]`  |  The values passed to the model.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: The validated values.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ImportError`  |  If required dependencies are missing.  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-oci-data-science/llama_index/embeddings/oci_data_science/base.py`  
| 
```
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
```
 | 
```
@model_validator(mode="before")
# @_validate_dependency
defvalidate_env(cls, values: Dict[str, Any]) -> Dict[str, Any]:
"""
    Validate the environment and dependencies before initialization.

    Args:
        values (Dict[str, Any]): The values passed to the model.

    Returns:
        Dict[str, Any]: The validated values.

    Raises:
        ImportError: If required dependencies are missing.

    """
    return values

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/oci_data_science/#llama_index.embeddings.oci_data_science.OCIDataScienceEmbedding.class_name "Permanent link")

```
class_name() -> 

```

Get the class name.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The name of the class.  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-oci-data-science/llama_index/embeddings/oci_data_science/base.py`  
| 
```
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
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""
    Get the class name.

    Returns:
        str: The name of the class.

    """
    return "OCIDataScienceEmbedding"

```
 |  
| --- | --- |  
options: members: - OCIDataScienceEmbedding
