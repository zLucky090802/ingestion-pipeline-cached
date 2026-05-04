# Nvidia rerank
##  NVIDIARerank [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/nvidia_rerank/#llama_index.postprocessor.nvidia_rerank.NVIDIARerank "Permanent link")
Bases: 
NVIDIA's API Catalog Reranker Connector.
Source code in `llama-index-integrations/postprocessor/llama-index-postprocessor-nvidia-rerank/llama_index/postprocessor/nvidia_rerank/base.py`  
| 
```
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
```
 | 
```
classNVIDIARerank(BaseNodePostprocessor):
"""NVIDIA's API Catalog Reranker Connector."""

    model_config = ConfigDict(validate_assignment=True)
    model: Optional[str] = Field(
        description="The NVIDIA API Catalog reranker to use.",
    )
    top_n: Optional[int] = Field(
        default=5,
        ge=0,
        description="The number of nodes to return.",
    )
    max_batch_size: Optional[int] = Field(
        default=64,
        ge=1,
        description="The maximum batch size supported by the inference server.",
    )
    truncate: Optional[Literal["NONE", "END"]] = Field(
        description=(
            "Truncate input text if it exceeds the model's maximum token length. "
            "Default is model dependent and is likely to raise error if an "
            "input is too long."
        ),
        default=None,
    )
    _api_key: str = PrivateAttr("NO_API_KEY_PROVIDED")  # TODO: should be SecretStr
    _mode: str = PrivateAttr("nvidia")
    _is_hosted: bool = PrivateAttr(True)
    base_url: Optional[str] = None
    _http_client: Optional[httpx.Client] = PrivateAttr(None)

    def__init__(
        self,
        model: Optional[str] = None,
        nvidia_api_key: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = os.getenv("NVIDIA_BASE_URL", BASE_URL),
        http_client: Optional[httpx.Client] = None,
        **kwargs: Any,
    ):
"""
        Initialize a NVIDIARerank instance.

        This class provides access to a NVIDIA NIM for reranking. By default, it connects to a hosted NIM, but can be configured to connect to an on-premises NIM using the `base_url` parameter. An API key is required for hosted NIM.

        Args:
            model (str): The model to use for reranking.
            nvidia_api_key (str, optional): The NVIDIA API key. Defaults to None.
            api_key (str, optional): The API key. Defaults to None.
            base_url (str, optional): The base URL of the on-premises NIM. Defaults to None.
            http_client (httpx.Client, optional): Custom HTTP client for making requests.
            truncate (str): "NONE", "END", truncate input text if it exceeds
                            the model's context length. Default is model dependent and
                            is likely to raise an error if an input is too long.
            **kwargs: Additional keyword arguments.

        API Key:
        - The recommended way to provide the API key is through the `NVIDIA_API_KEY` environment variable.

        """
        if not base_url or (base_url in KNOWN_URLS and not model):
            model = model or DEFAULT_MODEL
        super().__init__(model=model, **kwargs)

        self._is_hosted = base_url in KNOWN_URLS
        self.base_url = base_url
        self._is_hosted = base_url in KNOWN_URLS
        self.base_url = base_url
        self._api_key = get_from_param_or_env(
            "api_key",
            nvidia_api_key or api_key,
            "NVIDIA_API_KEY",
            "NO_API_KEY_PROVIDED",
        )
        if self._is_hosted:  # hosted on API Catalog (build.nvidia.com)
            if (not self._api_key) or (self._api_key == "NO_API_KEY_PROVIDED"):
                raise ValueError("An API key is required for hosted NIM.")

        self.model = model
        if not self.model:
            if self._is_hosted:
                self.model = DEFAULT_MODEL
            else:
                self.__get_default_model()

        if not self.model.startswith("nvdev/"):
            self._validate_model(self.model)  ## validate model

        self._http_client = http_client

    def__get_default_model(self):
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
            self.model = DEFAULT_MODEL

    @property
    defnormalized_base_url(self) -> str:
"""Return the normalized base URL (without trailing slashes)."""
        return self.base_url.rstrip("/")

    def_get_headers(self, auth_required: bool = False) -> dict:
"""
        Return default headers for HTTP requests.

        If auth_required is True or the client is hosted, includes an Authorization header.
        """
        headers = {"Accept": "application/json"}
        if auth_required or self._is_hosted:
            headers["Authorization"] = f"Bearer {self._api_key}"
        return headers

    def_get_models(self) -> List[Model]:
        client = self.client
        _headers = self._get_headers(
            auth_required=bool(self._api_key != "NO_API_KEY_PROVIDED" and self._api_key)
            or self._is_hosted
        )
        url = (
            "https://integrate.api.nvidia.com/v1/models"
            if self._is_hosted
            else self.normalized_base_url + "/models"
        )
        response = client.get(url, headers=_headers)
        response.raise_for_status()

        assert "data" in response.json(), (
            "Response does not contain expected 'data' key"
        )
        assert isinstance(response.json()["data"], list), (
            "Response 'data' is not a list"
        )
        assert all(isinstance(result, dict) for result in response.json()["data"]), (
            "Response 'data' is not a list of dictionaries"
        )
        assert all("id" in result for result in response.json()["data"]), (
            "Response 'rankings' is not a list of dictionaries with 'id'"
        )

        # TODO: hosted now has a model listing, need to merge known and listed models
        # TODO: parse model config for local models
        if not self._is_hosted:
            return [
                Model(
                    id=model["id"],
                    base_model=getattr(model, "params", {}).get("root", None),
                )
                for model in response.json()["data"]
            ]
        else:
            return RANKING_MODEL_TABLE
        # TODO: hosted now has a model listing, need to merge known and listed models
        # TODO: parse model config for local models
        if not self._is_hosted:
            return [
                Model(
                    id=model["id"],
                    base_model=getattr(model, "params", {}).get("root", None),
                )
                for model in response.json()["data"]
            ]
        else:
            return RANKING_MODEL_TABLE

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
        available_model_ids = [model.id for model in self.available_models]

        if not model:
            if self._is_hosted:
                warnings.warn(f"Unable to determine validity of {model_name}")
            else:
                if model_name not in available_model_ids:
                    raise ValueError(f"No locally hosted {model_name} was found.")

        if self._is_hosted and model and model.endpoint:
            self.base_url = model.endpoint

    @property
    defavailable_models(self) -> List[Model]:
"""Get available models."""
        # all available models are in the map
        ids = RANKING_MODEL_TABLE.keys()
        ids = RANKING_MODEL_TABLE.keys()
        if not self._is_hosted:
            return self._get_models()
        else:
            return [Model(id=id) for id in ids]

    @property
    defclient(self) -> httpx.Client:
"""
        Lazy initialization of the HTTP client.
        """
        if self._http_client is None:
            self._http_client = httpx.Client()
        return self._http_client

    @classmethod
    defclass_name(cls) -> str:
        return "NVIDIARerank"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        dispatcher.event(
            ReRankStartEvent(
                query=query_bundle,
                nodes=nodes,
                top_n=self.top_n,
                model_name=self.model,
            )
        )

        if query_bundle is None:
            raise ValueError(
                "Missing query bundle in extra info. Please do not give empty query!"
            )
        if len(nodes) == 0:
            return []

        url = self.normalized_base_url
        if not url.endswith(("/ranking", "/reranking")):
            url = f"{url}/ranking"

        client = self.client
        _headers = self._get_headers(auth_required=True)

        # TODO: replace with itertools.batched in python 3.12
        defbatched(ls: list, size: int) -> Generator[List[NodeWithScore], None, None]:
            for i in range(0, len(ls), size):
                yield ls[i : i + size]

        with self.callback_manager.event(
            CBEventType.RERANKING,
            payload={
                EventPayload.NODES: nodes,
                EventPayload.MODEL_NAME: self.model,
                EventPayload.QUERY_STR: query_bundle.query_str,
                EventPayload.TOP_K: self.top_n,
            },
        ) as event:
            results = []
            for batch in batched(nodes, self.max_batch_size):
                payloads = {
                    "model": self.model,
                    **({"truncate": self.truncate} if self.truncate else {}),
                    "query": {"text": query_bundle.query_str},
                    "passages": [
                        {"text": n.get_content(metadata_mode=MetadataMode.EMBED)}
                        for n in batch
                    ],
                }

                response = client.post(url, headers=_headers, json=payloads)
                response.raise_for_status()
                # expected response format:
                # {
                #     "rankings": [
                #         {
                #             "index": 0,
                #             "logit": 0.0
                #         },
                #         ...
                #     ]
                # }
                assert "rankings" in response.json(), (
                    "Response does not contain expected 'rankings' key"
                )
                assert isinstance(response.json()["rankings"], list), (
                    "Response 'rankings' is not a list"
                )
                assert all(
                    isinstance(result, dict) for result in response.json()["rankings"]
                ), "Response 'rankings' is not a list of dictionaries"
                assert all(
                    "index" in result and "logit" in result
                    for result in response.json()["rankings"]
                ), (
                    "Response 'rankings' is not a list of dictionaries with 'index' and 'logit' keys"
                )
                for result in response.json()["rankings"][: self.top_n]:
                    results.append(
                        NodeWithScore(
                            node=batch[result["index"]].node, score=result["logit"]
                        )
                    )
            if len(nodes)  self.max_batch_size:
                results.sort(key=lambda x: x.score, reverse=True)
            results = results[: self.top_n]
            event.on_end(payload={EventPayload.NODES: results})

        dispatcher.event(ReRankEndEvent(nodes=results))
        return results

```
 |  
| --- | --- |  
###  normalized_base_url `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/nvidia_rerank/#llama_index.postprocessor.nvidia_rerank.NVIDIARerank.normalized_base_url "Permanent link")

```
normalized_base_url: 

```

Return the normalized base URL (without trailing slashes).
###  available_models `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/nvidia_rerank/#llama_index.postprocessor.nvidia_rerank.NVIDIARerank.available_models "Permanent link")

```
available_models: []

```

Get available models.
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/nvidia_rerank/#llama_index.postprocessor.nvidia_rerank.NVIDIARerank.client "Permanent link")

```
client: Client

```

Lazy initialization of the HTTP client.
options: members: - NVIDIA
