# Siliconflow
##  SiliconFlowEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/siliconflow/#llama_index.embeddings.siliconflow.SiliconFlowEmbedding "Permanent link")
Bases: 
SiliconFlow class for embeddings.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-siliconflow/llama_index/embeddings/siliconflow/base.py`  
| 
```
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
```
 | 
```
classSiliconFlowEmbedding(BaseEmbedding):
"""SiliconFlow class for embeddings."""

    model: str = Field(
        default="BAAI/bge-m3",
        description="""\
            The name of the embedding model to use.
            512 tokens for all models input except `bge-m3` which is 8192.
        """,
    )
    api_key: Optional[str] = Field(
        default=None,
        description="The SiliconFlow API key.",
    )
    base_url: str = Field(
        default=DEFAULT_SILICONFLOW_API_URL,
        description="The base URL for the SiliconFlow API.",
    )
    encoding_format: str = Field(
        default="float",
        description="The format to return the embeddings in. Can be either float or base64.",
    )  # TODO: Consider whether to fix the encoding format as float.
    max_retries: int = Field(
        default=3,
        description="The maximum number of API retries.",
        ge=0,
    )

    _headers: Any = PrivateAttr()

    def__init__(
        self,
        model: str = "BAAI/bge-m3",
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_SILICONFLOW_API_URL,
        encoding_format: Optional[str] = "float",
        max_retries: int = 3,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            model=model,
            api_key=api_key,
            base_url=base_url,
            encoding_format=encoding_format,
            max_retries=max_retries,
            callback_manager=callback_manager,
            **kwargs,
        )
        assert self.encoding_format in VALID_ENCODING, f"""\
            Encoding_format parameter {self.encoding_format} not supported.
            Please choose one of {VALID_ENCODING}".
        """

        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    @classmethod
    defclass_name(cls) -> str:
        return "SiliconFlowEmbedding"

    def_data_formatting(self, response: list) -> List[List[float]]:
        results = sorted(response["data"], key=lambda e: e["index"])
        if self.encoding_format == "base64":
            return [base64_to_float_list(data["embedding"]) for data in results]
        else:
            return [data["embedding"] for data in results]

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self._get_text_embeddings([query])[0]

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""The asynchronous version of _get_query_embedding."""
        result = await self._aget_text_embeddings([query])
        return result[0]

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._get_text_embeddings([text])[0]

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get text embedding."""
        result = await self._aget_text_embeddings([text])
        return result[0]

    @embedding_retry_decorator
    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        with requests.Session() as session:
            input_json = {
                "model": self.model,
                "input": texts,
                "encoding_format": self.encoding_format,
            }
            response = session.post(
                self.base_url, json=input_json, headers=self._headers
            ).json()
            if "data" not in response:
                raise RuntimeError(response)
            return self._data_formatting(response)

    @embedding_retry_decorator
    async def_aget_text_embeddings(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        async with aiohttp.ClientSession() as session:
            input_json = {
                "input": texts,
                "model": self.model,
                "encoding_format": self.encoding_format,
            }

            async with session.post(
                self.base_url, json=input_json, headers=self._headers
            ) as response:
                response_json = await response.json()
                response.raise_for_status()
                return self._data_formatting(response_json)

```
 |  
| --- | --- |  
options: members: - SiliconFlowEmbedding
