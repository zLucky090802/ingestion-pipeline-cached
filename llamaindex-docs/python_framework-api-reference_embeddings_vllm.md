# Vllm
##  VllmEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/vllm/#llama_index.embeddings.vllm.VllmEmbedding "Permanent link")
Bases: 
Vllm LLM.
This class runs a vLLM embedding model locally.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-vllm/llama_index/embeddings/vllm/base.py`  
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
```
 | 
```
classVllmEmbedding(MultiModalEmbedding):
"""
    Vllm LLM.

    This class runs a vLLM embedding model locally.
    """

    tensor_parallel_size: Optional[int] = Field(
        default=1,
        description="The number of GPUs to use for distributed execution with tensor parallelism.",
    )

    trust_remote_code: Optional[bool] = Field(
        default=True,
        description="Trust remote code (e.g., from HuggingFace) when downloading the model and tokenizer.",
    )

    dtype: str = Field(
        default="auto",
        description="The data type for the model weights and activations.",
    )

    download_dir: Optional[str] = Field(
        default=None,
        description="Directory to download and load the weights. (Default to the default cache dir of huggingface)",
    )

    vllm_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Holds any model parameters valid for `vllm.LLM` call not explicitly specified.",
    )

    _client: Any = PrivateAttr()

    _image_token_id: Union[int, None] = PrivateAttr()

    def__init__(
        self,
        model_name: str = "facebook/opt-125m",
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        tensor_parallel_size: int = 1,
        trust_remote_code: bool = False,
        dtype: str = "auto",
        download_dir: Optional[str] = None,
        vllm_kwargs: Dict[str, Any] = {},
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        callback_manager = callback_manager or CallbackManager([])
        super().__init__(
            model_name=model_name,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
        )
        try:
            fromvllmimport LLM as VLLModel
        except ImportError:
            raise ImportError(
                "Could not import vllm python package. "
                "Please install it with `pip install vllm`."
            )
        self._client = VLLModel(
            model=model_name,
            task="embed",
            max_num_seqs=embed_batch_size,
            tensor_parallel_size=tensor_parallel_size,
            trust_remote_code=trust_remote_code,
            dtype=dtype,
            download_dir=download_dir,
            **vllm_kwargs,
        )
        try:
            self._image_token_id = (
                self._client.llm_engine.model_config.hf_config.image_token_id
            )
        except AttributeError:
            self._image_token_id = None

    @classmethod
    defclass_name(cls) -> str:
        return "VllmEmbedding"

    @atexit.register
    defclose():
        importtorch
        importgc

        if torch.cuda.is_available():
            gc.collect()
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    def_embed_with_retry(
        self, inputs: List[Union[str, BytesIO]], embed_type: str = "text"
    ) -> List[List[float]]:
"""
        Generates embeddings with retry mechanism.

        Args:
            inputs: List of texts or images to embed

        Returns:
            List of embedding vectors

        Raises:
            Exception: If embedding fails after retries

        """
        try:
            if embed_type == "image":
                inputs = [
                    {
                        "prompt_token_ids": [self._image_token_id],
                        "multi_modal_data": {"image": x},
                    }
                    for x in inputs
                ]
            emb = self._client.embed(inputs)
            return [x.outputs.embedding for x in emb]
        except Exception as e:
            logger.warning(f"Embedding attempt failed: {e!s}")
            raise

    def_embed(
        self, inputs: List[Union[str, BytesIO]], embed_type: str = "text"
    ) -> List[List[float]]:
"""
        Generates Embeddings with input validation and retry mechanism.

        Args:
            sentences: Texts or Sentences to embed
            prompt_name: The name of the prompt to use for encoding

        Returns:
            List of embedding vectors

        Raises:
            ValueError: If any input text is invalid
            Exception: If embedding fails after retries

        """
        if embed_type not in SUPPORT_EMBED_TYPES:
            raise (ValueError("Not Implemented"))
        return self._embed_with_retry(inputs, embed_type)

    def_get_query_embedding(self, query: str) -> List[float]:
"""
        Generates Embeddings for Query.

        Args:
            query (str): Query text/sentence

        Returns:
            List[float]: numpy array of embeddings

        """
        return self._embed([query])[0]

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""
        Generates Embeddings for Query Asynchronously.

        Args:
            query (str): Query text/sentence

        Returns:
            List[float]: numpy array of embeddings

        """
        return self._get_query_embedding(query)

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""
        Generates Embeddings for text Asynchronously.

        Args:
            text (str): Text/Sentence

        Returns:
            List[float]: numpy array of embeddings

        """
        return self._get_text_embedding(text)

    def_get_text_embedding(self, text: str) -> List[float]:
"""
        Generates Embeddings for text.

        Args:
            text (str): Text/sentences

        Returns:
            List[float]: numpy array of embeddings

        """
        return self._embed([text])[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""
        Generates Embeddings for text.

        Args:
            texts (List[str]): Texts / Sentences

        Returns:
            List[List[float]]: numpy array of embeddings

        """
        return self._embed(texts)

    def_get_image_embedding(self, img_file_path: ImageType) -> List[float]:
"""Generate embedding for an image."""
        image = Image.open(img_file_path)
        return self._embed([image], "image")[0]

    async def_aget_image_embedding(self, img_file_path: ImageType) -> List[float]:
"""Generate embedding for an image asynchronously."""
        return self._get_image_embedding(img_file_path)

    def_get_image_embeddings(
        self, img_file_paths: List[ImageType]
    ) -> List[List[float]]:
        images = [Image.open(x) for x in img_file_paths]
"""Generate embeddings for multiple images."""
        return self._embed(images, "image")

    async def_aget_image_embeddings(
        self, img_file_paths: List[ImageType]
    ) -> List[List[float]]:
"""Generate embeddings for multiple images asynchronously."""
        return self._get_image_embeddings(img_file_paths)

```
 |  
| --- | --- |  
options: members: - VllmEmbedding
