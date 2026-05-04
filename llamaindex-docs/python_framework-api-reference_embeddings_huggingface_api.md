# Huggingface api
##  HuggingFaceInferenceAPIEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/huggingface_api/#llama_index.embeddings.huggingface_api.HuggingFaceInferenceAPIEmbedding "Permanent link")
Bases: 
Wrapper on the Hugging Face's Inference API for embeddings.
Overview of the design: - Uses the feature extraction task: https://huggingface.co/tasks/feature-extraction
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-huggingface-api/llama_index/embeddings/huggingface_api/base.py`  
| 
```
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
```
 | 
```
classHuggingFaceInferenceAPIEmbedding(BaseEmbedding):  # type: ignore[misc]
"""
    Wrapper on the Hugging Face's Inference API for embeddings.

    Overview of the design:
    - Uses the feature extraction task: https://huggingface.co/tasks/feature-extraction
    """

    pooling: Optional[Pooling] = Field(
        default=Pooling.CLS,
        description="Pooling strategy. If None, the model's default pooling is used.",
    )
    query_instruction: Optional[str] = Field(
        default=None, description="Instruction to prepend during query embedding."
    )
    text_instruction: Optional[str] = Field(
        default=None, description="Instruction to prepend during text embedding."
    )

    # Corresponds with huggingface_hub.InferenceClient
    model_name: Optional[str] = Field(
        default=None,
        description="Hugging Face model name. If None, the task will be used.",
    )
    token: Union[str, bool, None] = Field(
        default=None,
        description=(
            "Hugging Face token. Will default to the locally saved token. Pass "
            "token=False if you don’t want to send your token to the server."
        ),
    )
    timeout: Optional[float] = Field(
        default=None,
        description=(
            "The maximum number of seconds to wait for a response from the server."
            " Loading a new model in Inference API can take up to several minutes."
            " Defaults to None, meaning it will loop until the server is available."
        ),
    )
    headers: Optional[Dict[str, str]] = Field(
        default=None,
        description=(
            "Additional headers to send to the server. By default only the"
            " authorization and user-agent headers are sent. Values in this dictionary"
            " will override the default values."
        ),
    )
    cookies: Optional[Dict[str, str]] = Field(
        default=None, description="Additional cookies to send to the server."
    )
    task: Optional[str] = Field(
        default=None,
        description=(
            "Optional task to pick Hugging Face's recommended model, used when"
            " model_name is left as default of None."
        ),
    )
    _sync_client: "InferenceClient" = PrivateAttr()
    _async_client: "AsyncInferenceClient" = PrivateAttr()
    _get_model_info: "Callable[..., ModelInfo]" = PrivateAttr()

    def_get_inference_client_kwargs(self) -> Dict[str, Any]:
"""Extract the Hugging Face InferenceClient construction parameters."""
        return {
            "model": self.model_name,
            "token": self.token,
            "timeout": self.timeout,
            "headers": self.headers,
            "cookies": self.cookies,
        }

    def__init__(self, **kwargs: Any) -> None:
"""
        Initialize.

        Args:
            kwargs: See the class-level Fields.

        """
        if kwargs.get("model_name") is None:
            task = kwargs.get("task", "")
            # NOTE: task being None or empty string leads to ValueError,
            # which ensures model is present
            kwargs["model_name"] = InferenceClient.get_recommended_model(task=task)
            logger.debug(
                f"Using Hugging Face's recommended model {kwargs['model_name']}"
                f" given task {task}."
            )
            print(kwargs["model_name"], flush=True)
        super().__init__(**kwargs)  # Populate pydantic Fields
        self._sync_client = InferenceClient(**self._get_inference_client_kwargs())
        self._async_client = AsyncInferenceClient(**self._get_inference_client_kwargs())
        self._get_model_info = model_info

    defvalidate_supported(self, task: str) -> None:
"""
        Confirm the contained model_name is deployed on the Inference API service.

        Args:
            task: Hugging Face task to check within. A list of all tasks can be
                found here: https://huggingface.co/tasks

        """
        all_models = self._sync_client.list_deployed_models(frameworks="all")
        try:
            if self.model_name not in all_models[task]:
                raise ValueError(
                    "The Inference API service doesn't have the model"
                    f" {self.model_name!r} deployed."
                )
        except KeyError as exc:
            raise KeyError(
                f"Input task {task!r} not in possible tasks {list(all_models.keys())}."
            ) fromexc

    defget_model_info(self, **kwargs: Any) -> "ModelInfo":
"""Get metadata on the current model from Hugging Face."""
        return self._get_model_info(self.model_name, **kwargs)

    @classmethod
    defclass_name(cls) -> str:
        return "HuggingFaceInferenceAPIEmbedding"

    async def_async_embed_single(self, text: str) -> Embedding:
        embedding = await self._async_client.feature_extraction(text)
        if len(embedding.shape) == 1:
            return embedding.tolist()
        embedding = embedding.squeeze(axis=0)
        if len(embedding.shape) == 1:  # Some models pool internally
            return embedding.tolist()
        try:
            return self.pooling(embedding).tolist()  # type: ignore[misc]
        except TypeError as exc:
            raise ValueError(
                f"Pooling is required for {self.model_name} because it returned"
                " a > 1-D value, please specify pooling as not None."
            ) fromexc

    async def_async_embed_bulk(self, texts: Sequence[str]) -> List[Embedding]:
"""
        Embed a sequence of text, in parallel and asynchronously.

        NOTE: this uses an externally created asyncio event loop.
        """
        tasks = [self._async_embed_single(text) for text in texts]
        return await asyncio.gather(*tasks)

    def_get_query_embedding(self, query: str) -> Embedding:
"""
        Embed the input query synchronously.

        NOTE: a new asyncio event loop is created internally for this.
        """
        return asyncio.run(self._aget_query_embedding(query))

    def_get_text_embedding(self, text: str) -> Embedding:
"""
        Embed the text query synchronously.

        NOTE: a new asyncio event loop is created internally for this.
        """
        return asyncio.run(self._aget_text_embedding(text))

    def_get_text_embeddings(self, texts: List[str]) -> List[Embedding]:
"""
        Embed the input sequence of text synchronously and in parallel.

        NOTE: a new asyncio event loop is created internally for this.
        """
        loop = asyncio.new_event_loop()
        try:
            tasks = [
                loop.create_task(self._aget_text_embedding(text)) for text in texts
            ]
            loop.run_until_complete(asyncio.wait(tasks))
        finally:
            loop.close()
        return [task.result() for task in tasks]

    async def_aget_query_embedding(self, query: str) -> Embedding:
        return await self._async_embed_single(
            text=format_query(query, self.model_name, self.query_instruction)
        )

    async def_aget_text_embedding(self, text: str) -> Embedding:
        return await self._async_embed_single(
            text=format_text(text, self.model_name, self.text_instruction)
        )

    async def_aget_text_embeddings(self, texts: List[str]) -> List[Embedding]:
        return await self._async_embed_bulk(
            texts=[
                format_text(text, self.model_name, self.text_instruction)
                for text in texts
            ]
        )

```
 |  
| --- | --- |  
###  validate_supported [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/huggingface_api/#llama_index.embeddings.huggingface_api.HuggingFaceInferenceAPIEmbedding.validate_supported "Permanent link")

```
validate_supported(task: ) -> None

```

Confirm the contained model_name is deployed on the Inference API service.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `task`  |  Hugging Face task to check within. A list of all tasks can be found here: https://huggingface.co/tasks  |  _required_  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-huggingface-api/llama_index/embeddings/huggingface_api/base.py`  
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
```
 | 
```
defvalidate_supported(self, task: str) -> None:
"""
    Confirm the contained model_name is deployed on the Inference API service.

    Args:
        task: Hugging Face task to check within. A list of all tasks can be
            found here: https://huggingface.co/tasks

    """
    all_models = self._sync_client.list_deployed_models(frameworks="all")
    try:
        if self.model_name not in all_models[task]:
            raise ValueError(
                "The Inference API service doesn't have the model"
                f" {self.model_name!r} deployed."
            )
    except KeyError as exc:
        raise KeyError(
            f"Input task {task!r} not in possible tasks {list(all_models.keys())}."
        ) fromexc

```
 |  
| --- | --- |  
###  get_model_info [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/huggingface_api/#llama_index.embeddings.huggingface_api.HuggingFaceInferenceAPIEmbedding.get_model_info "Permanent link")

```
get_model_info(**kwargs: ) -> ModelInfo

```

Get metadata on the current model from Hugging Face.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-huggingface-api/llama_index/embeddings/huggingface_api/base.py`  
| 
```
140
141
142
```
 | 
```
defget_model_info(self, **kwargs: Any) -> "ModelInfo":
"""Get metadata on the current model from Hugging Face."""
    return self._get_model_info(self.model_name, **kwargs)

```
 |  
| --- | --- |  
options: members: - HuggingFaceInferenceAPIEmbedding
