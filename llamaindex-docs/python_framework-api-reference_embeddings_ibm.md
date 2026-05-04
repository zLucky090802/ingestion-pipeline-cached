# Ibm
##  WatsonxEmbeddings [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/ibm/#llama_index.embeddings.ibm.WatsonxEmbeddings "Permanent link")
Bases: 
IBM watsonx.ai embeddings.
Example
`pip install llama-index-embeddings-ibm`

```
fromllama_index.embeddings.ibmimport WatsonxEmbeddings

watsonx_llm = WatsonxEmbeddings(
    model_id="ibm/slate-125m-english-rtrvr-v2",
    url="https://us-south.ml.cloud.ibm.com",
    apikey="*****",
    project_id="*****",
)

```

Source code in `llama-index-integrations/embeddings/llama-index-embeddings-ibm/llama_index/embeddings/ibm/base.py`  
| 
```
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
```
 | 
```
classWatsonxEmbeddings(BaseEmbedding):
"""
    IBM watsonx.ai embeddings.

    Example:
        `pip install llama-index-embeddings-ibm`

        ```python
        from llama_index.embeddings.ibm import WatsonxEmbeddings

        watsonx_llm = WatsonxEmbeddings(
            model_id="ibm/slate-125m-english-rtrvr-v2",
            url="https://us-south.ml.cloud.ibm.com",
            apikey="*****",
            project_id="*****",

        ```

    """

    model_id: str = Field(
        default=DEFAULT_EMBED_MODEL,
        description="Type of model to use.",
        allow_mutation=False,
    )

    truncate_input_tokens: Optional[int] = Field(
        default=None,
        description="Represents the maximum number of input tokens accepted.",
    )

    project_id: Optional[str] = Field(
        default=None,
        description="ID of the Watson Studio project.",
        allow_mutation=False,
    )

    space_id: Optional[str] = Field(
        default=None,
        description="ID of the Watson Studio space.",
        allow_mutation=False,
    )

    url: Optional[SecretStr] = Field(
        default=None,
        description="Url to the IBM watsonx.ai for IBM Cloud or the IBM watsonx.ai software instance.",
        allow_mutation=False,
    )

    apikey: Optional[SecretStr] = Field(
        default=None,
        description="API key to the IBM watsonx.ai for IBM Cloud or the IBM watsonx.ai software instance.",
        allow_mutation=False,
    )

    token: Optional[SecretStr] = Field(
        default=None,
        description="Token to the IBM watsonx.ai software instance.",
        allow_mutation=False,
    )

    password: Optional[SecretStr] = Field(
        default=None,
        description="Password to the IBM watsonx.ai software instance.",
        allow_mutation=False,
    )

    username: Optional[SecretStr] = Field(
        default=None,
        description="Username to the IBM watsonx.ai software instance.",
        allow_mutation=False,
    )

    instance_id: Optional[SecretStr] = Field(
        default=None,
        description="Instance_id of the IBM watsonx.ai software instance.",
        allow_mutation=False,
        deprecated="The `instance_id` parameter is deprecated and will no longer be utilized for logging to the IBM watsonx.ai software instance.",
    )

    version: Optional[SecretStr] = Field(
        default=None,
        description="Version of the IBM watsonx.ai software instance.",
        allow_mutation=False,
    )

    verify: Union[str, bool, None] = Field(
        default=None,
        description="""User can pass as verify one of following:
        the path to a CA_BUNDLE file
        the path of directory with certificates of trusted CAs
        True - default path to truststore will be taken
        False - no verification will be made""",
        allow_mutation=False,
    )

    _embed_model: Embeddings = PrivateAttr()

    def__init__(
        self,
        model_id: str,
        truncate_input_tokens: Optional[int] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        project_id: Optional[str] = None,
        space_id: Optional[str] = None,
        url: Optional[str] = None,
        apikey: Optional[str] = None,
        token: Optional[str] = None,
        password: Optional[str] = None,
        username: Optional[str] = None,
        version: Optional[str] = None,
        verify: Union[str, bool, None] = None,
        api_client: Optional[APIClient] = None,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ):
        callback_manager = callback_manager or CallbackManager([])

        if isinstance(api_client, APIClient):
            project_id = api_client.default_project_id or project_id
            space_id = api_client.default_space_id or space_id
            creds = {}
        else:
            creds = resolve_watsonx_credentials(
                url=url,
                apikey=apikey,
                token=token,
                username=username,
                password=password,
            )

        url = creds.get("url").get_secret_value() if creds.get("url") else None
        apikey = creds.get("apikey").get_secret_value() if creds.get("apikey") else None
        token = creds.get("token").get_secret_value() if creds.get("token") else None
        password = (
            creds.get("password").get_secret_value() if creds.get("password") else None
        )
        username = (
            creds.get("username").get_secret_value() if creds.get("username") else None
        )

        super().__init__(
            model_id=model_id,
            truncate_input_tokens=truncate_input_tokens,
            project_id=project_id,
            space_id=space_id,
            url=url,
            apikey=apikey,
            token=token,
            password=password,
            username=username,
            version=version,
            verify=verify,
            callback_manager=callback_manager,
            embed_batch_size=embed_batch_size,
            **kwargs,
        )

        self._embed_model = Embeddings(
            model_id=model_id,
            params=self.params,
            credentials=(
                Credentials.from_dict(
                    {
                        key: value.get_secret_value() if value else None
                        for key, value in self._get_credential_kwargs().items()
                    },
                    _verify=self.verify,
                )
                if creds
                else None
            ),
            project_id=self.project_id,
            space_id=self.space_id,
            api_client=api_client,
        )

    classConfig:
        validate_assignment = True

    @classmethod
    defclass_name(cls) -> str:
        return "WatsonxEmbedding"

    def_get_credential_kwargs(self) -> Dict[str, SecretStr | None]:
        return {
            "url": self.url,
            "apikey": self.apikey,
            "token": self.token,
            "password": self.password,
            "username": self.username,
            "version": self.version,
        }

    @property
    defparams(self) -> Dict[str, int] | None:
        return (
            {"truncate_input_tokens": self.truncate_input_tokens}
            if self.truncate_input_tokens
            else None
        )

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self._embed_model.embed_query(text=query, params=self.params)

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._get_query_embedding(query=text)

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        return self._embed_model.embed_documents(texts=texts, params=self.params)

    ### Async methods
    # Asynchronous evaluation is not yet supported for watsonx.ai embeddings
    async def_aget_query_embedding(self, query: str) -> List[float]:
"""The asynchronous version of _get_query_embedding."""
        return self._get_query_embedding(query)

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get text embedding."""
        return self._get_text_embedding(text)

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Asynchronously get text embeddings."""
        return self._get_text_embeddings(texts)

```
 |  
| --- | --- |  
options: members: - WatsonxEmbeddings
