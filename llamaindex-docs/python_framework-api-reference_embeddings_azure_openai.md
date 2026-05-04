# Azure openai
##  AzureOpenAIEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/azure_openai/#llama_index.embeddings.azure_openai.AzureOpenAIEmbedding "Permanent link")
Bases: 
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-azure-openai/llama_index/embeddings/azure_openai/base.py`  
| 
```
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
```
 | 
```
classAzureOpenAIEmbedding(OpenAIEmbedding):
    azure_endpoint: Optional[str] = Field(
        default=None, description="The Azure endpoint to use.", validate_default=True
    )
    azure_deployment: Optional[str] = Field(
        default=None, description="The Azure deployment to use.", validate_default=True
    )

    api_base: str = Field(
        default="",
        description="The base URL for Azure deployment.",
        validate_default=True,
    )
    api_version: str = Field(
        default="",
        description="The version for Azure OpenAI API.",
        validate_default=True,
    )

    azure_ad_token_provider: Optional[AnnotatedProvider] = Field(
        default=None,
        description="Callback function to provide Azure AD token.",
        exclude=True,
    )
    use_azure_ad: bool = Field(
        description="Indicates if Microsoft Entra ID (former Azure AD) is used for token authentication"
    )
    _azure_ad_token: Any = PrivateAttr(default=None)

    _client: AzureOpenAI = PrivateAttr()
    _aclient: AsyncAzureOpenAI = PrivateAttr()

    def__init__(
        self,
        mode: str = OpenAIEmbeddingMode.TEXT_SEARCH_MODE,
        model: str = OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        dimensions: Optional[int] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
        api_version: Optional[str] = None,
        api_base: Optional[str] = None,
        # azure specific
        azure_endpoint: Optional[str] = None,
        azure_deployment: Optional[str] = None,
        azure_ad_token_provider: Optional[AzureADTokenProvider] = None,
        use_azure_ad: bool = False,
        deployment_name: Optional[str] = None,
        max_retries: int = 10,
        reuse_client: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        num_workers: Optional[int] = None,
        # custom httpx client
        http_client: Optional[httpx.Client] = None,
        async_http_client: Optional[httpx.AsyncClient] = None,
        **kwargs: Any,
    ):
        # OpenAI base_url (api_base) and azure_endpoint are mutually exclusive
        if api_base is None:
            azure_endpoint = get_from_param_or_env(
                "azure_endpoint", azure_endpoint, "AZURE_OPENAI_ENDPOINT", None
            )

        if not use_azure_ad:
            api_key = get_from_param_or_env(
                "api_key", api_key, "AZURE_OPENAI_API_KEY", None
            )

        azure_deployment = resolve_from_aliases(
            azure_deployment,
            deployment_name,
        )

        super().__init__(
            mode=mode,
            model=model,
            embed_batch_size=embed_batch_size,
            dimensions=dimensions,
            additional_kwargs=additional_kwargs,
            api_key=api_key,
            api_version=api_version,
            api_base=api_base,
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            azure_ad_token_provider=azure_ad_token_provider,
            use_azure_ad=use_azure_ad,
            max_retries=max_retries,
            reuse_client=reuse_client,
            callback_manager=callback_manager,
            http_client=http_client,
            async_http_client=async_http_client,
            num_workers=num_workers,
            **kwargs,
        )

        # reset api_base to None if it is the default
        if self.api_base == DEFAULT_OPENAI_API_BASE or self.azure_endpoint:
            self.api_base = None

    @model_validator(mode="before")
    @classmethod
    defvalidate_env(cls, values: Dict[str, Any]) -> Dict[str, Any]:
"""Validate necessary credentials are set."""
        if (
            values.get("api_base") == "https://api.openai.com/v1"
            and values.get("azure_endpoint") is None
        ):
            raise ValueError(
                "You must set OPENAI_API_BASE to your Azure endpoint. "
                "It should look like https://YOUR_RESOURCE_NAME.openai.azure.com/"
            )
        if values.get("api_version") is None:
            raise ValueError("You must set OPENAI_API_VERSION for Azure OpenAI.")

        return values

    def_get_client(self) -> AzureOpenAI:
        if not self.reuse_client:
            return AzureOpenAI(**self._get_credential_kwargs())

        if self._client is None:
            self._client = AzureOpenAI(**self._get_credential_kwargs())
        return self._client

    def_get_aclient(self) -> AsyncAzureOpenAI:
        if not self.reuse_client:
            return AsyncAzureOpenAI(**self._get_credential_kwargs(is_async=True))

        if self._aclient is None:
            self._aclient = AsyncAzureOpenAI(
                **self._get_credential_kwargs(is_async=True)
            )
        return self._aclient

    def_get_credential_kwargs(self, is_async: bool = False) -> Dict[str, Any]:
        if self.use_azure_ad:
            if self.azure_ad_token_provider:
                self.api_key = self.azure_ad_token_provider()
            else:
                self._azure_ad_token = refresh_openai_azuread_token(
                    self._azure_ad_token
                )
                self.api_key = self._azure_ad_token.token
        else:
            self.api_key = get_from_param_or_env(
                "api_key", self.api_key, "AZURE_OPENAI_API_KEY"
            )
        return {
            "api_key": self.api_key,
            "azure_ad_token_provider": self.azure_ad_token_provider,
            "azure_endpoint": self.azure_endpoint,
            "azure_deployment": self.azure_deployment,
            "base_url": self.api_base,
            "api_version": self.api_version,
            "default_headers": self.default_headers,
            "http_client": self._async_http_client if is_async else self._http_client,
        }

    @classmethod
    defclass_name(cls) -> str:
        return "AzureOpenAIEmbedding"

```
 |  
| --- | --- |  
###  validate_env `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/azure_openai/#llama_index.embeddings.azure_openai.AzureOpenAIEmbedding.validate_env "Permanent link")

```
validate_env(values: [, ]) -> [, ]

```

Validate necessary credentials are set.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-azure-openai/llama_index/embeddings/azure_openai/base.py`  
| 
```
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
```
 | 
```
@model_validator(mode="before")
@classmethod
defvalidate_env(cls, values: Dict[str, Any]) -> Dict[str, Any]:
"""Validate necessary credentials are set."""
    if (
        values.get("api_base") == "https://api.openai.com/v1"
        and values.get("azure_endpoint") is None
    ):
        raise ValueError(
            "You must set OPENAI_API_BASE to your Azure endpoint. "
            "It should look like https://YOUR_RESOURCE_NAME.openai.azure.com/"
        )
    if values.get("api_version") is None:
        raise ValueError("You must set OPENAI_API_VERSION for Azure OpenAI.")

    return values

```
 |  
| --- | --- |  
options: members: - AzureOpenAIEmbedding
