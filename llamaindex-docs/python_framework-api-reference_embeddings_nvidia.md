# Nvidia
##  NVIDIAEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/nvidia/#llama_index.embeddings.nvidia.NVIDIAEmbedding "Permanent link")
Bases: 
NVIDIA embeddings.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-nvidia/llama_index/embeddings/nvidia/base.py`  
| 
```
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
```
 | 
```
classNVIDIAEmbedding(BaseEmbedding):
"""NVIDIA embeddings."""

    base_url: str = Field(
        default_factory=lambda: os.getenv("NVIDIA_BASE_URL", BASE_URL),
        description="Base url for model listing an invocation",
    )
    model: Optional[str] = Field(
        description="Name of the NVIDIA embedding model to use.\n"
    )

    truncate: Literal["NONE", "START", "END"] = Field(
        default="NONE",
        description=(
            "Truncate input text if it exceeds the model's maximum token length. "
            "Default is 'NONE', which raises an error if an input is too long."
        ),
    )

    timeout: float = Field(
        default=120, description="The timeout for the API request in seconds.", ge=0
    )

    max_retries: int = Field(
        default=5,
        description="The maximum number of retries for the API request.",
        ge=0,
    )

    dimensions: Optional[int] = Field(
        default=None,
        description=(
            "The number of dimensions for the embeddings. This parameter is not "
            "supported by all models."
        ),
    )

    _client: Any = PrivateAttr()
    _aclient: Any = PrivateAttr()
    _is_hosted: bool = PrivateAttr(True)

    def__init__(
        self,
        model: Optional[str] = None,
        timeout: Optional[float] = 120,
        max_retries: Optional[int] = 5,
        dimensions: Optional[int] = 0,
        nvidia_api_key: Optional[str] = None,
        api_key: Optional[str] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,  # This could default to 50
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ):
"""
        Construct an Embedding interface for NVIDIA NIM.

        This constructor initializes an instance of the NVIDIAEmbedding class, which provides
        an interface for embedding text using NVIDIA's NIM service.

        Parameters
        ----------
        - model (str, optional): The name of the model to use for embeddings.
        - timeout (float, optional): The timeout for requests to the NIM service, in seconds. Defaults to 120.
        - max_retries (int, optional): The maximum number of retries for requests to the NIM service. Defaults to 5.
        - dimensions (int, optional): The number of dimensions for the embeddings. This
                              parameter is not supported by all models.
        - nvidia_api_key (str, optional): The API key for the NIM service. This is required if using a hosted NIM.
        - api_key (str, optional): An alternative parameter for providing the API key.
        - base_url (str, optional): The base URL for the NIM service. If not provided, the service will default to a hosted NIM.
        - **kwargs: Additional keyword arguments.

        API Keys:
        - The recommended way to provide the API key is through the `NVIDIA_API_KEY` environment variable.

        Note:
        - Switch from a hosted NIM (default) to an on-premises NIM using the `base_url` parameter. An API key is required for hosted NIM.

        """
        super().__init__(
            model=model,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            dimensions=dimensions,
            **kwargs,
        )
        self.dimensions = dimensions

        if embed_batch_size  259:
            raise ValueError("The batch size should not be larger than 259.")

        api_key = get_from_param_or_env(
            "api_key",
            nvidia_api_key or api_key,
            "NVIDIA_API_KEY",
            "NO_API_KEY_PROVIDED",
        )

        self._is_hosted = self.base_url in KNOWN_URLS

        if self._is_hosted:  # hosted on API Catalog (build.nvidia.com)
            if api_key == "NO_API_KEY_PROVIDED":
                raise ValueError("An API key is required for hosted NIM.")

        self._client = OpenAI(
            api_key=api_key,
            base_url=self.base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self._client._custom_headers = {"User-Agent": "llama-index-embeddings-nvidia"}

        self._aclient = AsyncOpenAI(
            api_key=api_key,
            base_url=self.base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self._aclient._custom_headers = {"User-Agent": "llama-index-embeddings-nvidia"}

        self.model = model
        if not self.model:
            if self._is_hosted:
                self.model = DEFAULT_MODEL
            else:
                self.__get_default_model()

        if not self.model.startswith("nvdev/"):
            self._validate_model(self.model)  ## validate model

    def__get_default_model(self) -> None:
"""Set default model."""
        if not self._is_hosted:
            valid_models = [
                model.id
                for model in self.available_models
                if not model.base_model or model.base_model == model.id
            ]
            self.model = next(iter(valid_models), None)
            if self.model:
                warnings.warn(
                    f"Default model is set as: {self.model}. \n"
                    "Set model using model parameter. \n"
                    "To get available models use available_models property.",
                    UserWarning,
                )
            else:
                raise ValueError("No locally hosted model was found.")
        else:
            self.model = self.model or DEFAULT_MODEL

    def_validate_model(self, model_name: str) -> None:
"""
        Validates compatibility of the hosted model with the client.
        Skipping the client validation for non-catalogue requests.

        Args:
            model_name (str): The name of the model.

        Raises:
            ValueError: If the model is incompatible with the client.

        """
        model = determine_model(model_name)
        if self._is_hosted:
            if not model:
                warnings.warn(f"Unable to determine validity of {model_name}")
            if model and model.endpoint:
                self.base_url = model.endpoint
                # Update client base_url for custom endpoints
                self._client.base_url = self.base_url
                self._aclient.base_url = self.base_url
        # TODO: handle locally hosted models

    @property
    defavailable_models(self) -> List[str]:
"""Get available models."""
        # TODO: hosted now has a model listing, need to merge known and listed models
        if not self._is_hosted:
            return [
                Model(
                    id=model.id,
                    base_model=getattr(model, "params", {}).get("root", None),
                )
                for model in self._client.models.list()
            ]
        else:
            return [Model(id=id) for id in EMBEDDING_MODEL_TABLE]

    @classmethod
    defclass_name(cls) -> str:
        return "NVIDIAEmbedding"

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        extra_body = {"input_type": "passage", "truncate": self.truncate}
        if self.dimensions:
            extra_body["dimensions"] = self.dimensions
        return (
            self._client.embeddings.create(
                input=[query],
                model=self.model,
                extra_body=extra_body,
            )
            .data[0]
            .embedding
        )

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        extra_body = {"input_type": "passage", "truncate": self.truncate}
        if self.dimensions:
            extra_body["dimensions"] = self.dimensions
        return (
            self._client.embeddings.create(
                input=[text],
                model=self.model,
                extra_body=extra_body,
            )
            .data[0]
            .embedding
        )

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        assert len(texts) <= 259, "The batch size should not be larger than 259."
        extra_body = {"input_type": "passage", "truncate": self.truncate}
        if self.dimensions:
            extra_body["dimensions"] = self.dimensions
        data = self._client.embeddings.create(
            input=texts,
            model=self.model,
            extra_body=extra_body,
        ).data
        return [d.embedding for d in data]

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""Asynchronously get query embedding."""
        return (
            (
                await self._aclient.embeddings.create(
                    input=[query],
                    model=self.model,
                    extra_body={"input_type": "query", "truncate": self.truncate},
                )
            )
            .data[0]
            .embedding
        )

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get text embedding."""
        return (
            (
                await self._aclient.embeddings.create(
                    input=[text],
                    model=self.model,
                    extra_body={"input_type": "passage", "truncate": self.truncate},
                )
            )
            .data[0]
            .embedding
        )

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Asynchronously get text embeddings."""
        assert len(texts) <= 259, "The batch size should not be larger than 259."

        data = (
            await self._aclient.embeddings.create(
                input=texts,
                model=self.model,
                extra_body={"input_type": "passage", "truncate": self.truncate},
            )
        ).data
        return [d.embedding for d in data]

```
 |  
| --- | --- |  
###  available_models `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/nvidia/#llama_index.embeddings.nvidia.NVIDIAEmbedding.available_models "Permanent link")

```
available_models: []

```

Get available models.
options: members: - NVIDIA
