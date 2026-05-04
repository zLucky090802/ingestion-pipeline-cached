# Azure openai
##  AzureOpenAI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/azure_openai/#llama_index.llms.azure_openai.AzureOpenAI "Permanent link")
Bases: 
Azure OpenAI.
To use this, you must first deploy a model on Azure OpenAI. Unlike OpenAI, you need to specify a `engine` parameter to identify your deployment (called "model deployment name" in Azure portal).
  * model: Name of the model (e.g. `text-davinci-003`) This in only used to decide completion vs. chat endpoint.
  * engine: This will correspond to the custom name you chose for your deployment when you deployed a model.


You must have the following environment variables set:
  * `OPENAI_API_VERSION`: set this to `2023-07-01-preview` or newer. This may change in the future.
  * `AZURE_OPENAI_ENDPOINT`: your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
  * `AZURE_OPENAI_API_KEY`: your API key if the api type is `azure`| Or pass through `AZURE_AD_TOKEN_PROVIDER` and set `use_azure_ad = True` to use managed identity with Azure Entra ID

More information can be found here
https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quickstart?tabs=command-line&pivots=programming-language-python
Examples:
`pip install llama-index-llms-azure-openai`

```
fromllama_index.llms.azure_openaiimport AzureOpenAI

aoai_api_key = "YOUR_AZURE_OPENAI_API_KEY"
aoai_endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"
aoai_api_version = "2023-07-01-preview"

llm = AzureOpenAI(
    engine="AZURE_AZURE_OPENAI_DEPLOYMENT_NAME",
    model="YOUR_AZURE_OPENAI_COMPLETION_MODEL_NAME",
    api_key=aoai_api_key,
    azure_endpoint=aoai_endpoint,
    api_version=aoai_api_version,
)

```

Using managed identity (passing a token provider instead of an API key):
```python from llama_index.llms.azure_openai import AzureOpenAI
aoai_endpoint = "YOUR_AZURE_OPENAI_ENDPOINT" aoai_api_version = "2023-07-01-preview"
credential = DefaultAzureCredential() token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
llm = AzureOpenAI( engine = llm_deployment model="YOUR_AZURE_OPENAI_COMPLETION_MODEL_NAME", azure_ad_token_provider=token_provider, use_azure_ad=True, azure_endpoint=aoai_endpoint, api_version=aoai_api_version, ) ```
Source code in `llama-index-integrations/llms/llama-index-llms-azure-openai/llama_index/llms/azure_openai/base.py`  
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
```
 | 
```
classAzureOpenAI(OpenAI):
"""
    Azure OpenAI.

    To use this, you must first deploy a model on Azure OpenAI.
    Unlike OpenAI, you need to specify a `engine` parameter to identify
    your deployment (called "model deployment name" in Azure portal).

    - model: Name of the model (e.g. `text-davinci-003`)
        This in only used to decide completion vs. chat endpoint.
    - engine: This will correspond to the custom name you chose
        for your deployment when you deployed a model.

    You must have the following environment variables set:

    - `OPENAI_API_VERSION`: set this to `2023-07-01-preview` or newer.
        This may change in the future.
    - `AZURE_OPENAI_ENDPOINT`: your endpoint should look like the following
        https://YOUR_RESOURCE_NAME.openai.azure.com/
    - `AZURE_OPENAI_API_KEY`: your API key if the api type is `azure`| Or pass through `AZURE_AD_TOKEN_PROVIDER`
        and set `use_azure_ad = True` to use managed identity with Azure Entra ID

    More information can be found here:
        https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quickstart?tabs=command-line&pivots=programming-language-python

    Examples:
        `pip install llama-index-llms-azure-openai`

        ```python
        from llama_index.llms.azure_openai import AzureOpenAI

        aoai_api_key = "YOUR_AZURE_OPENAI_API_KEY"
        aoai_endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"
        aoai_api_version = "2023-07-01-preview"

        llm = AzureOpenAI(
            engine="AZURE_AZURE_OPENAI_DEPLOYMENT_NAME",
            model="YOUR_AZURE_OPENAI_COMPLETION_MODEL_NAME",
            api_key=aoai_api_key,
            azure_endpoint=aoai_endpoint,
            api_version=aoai_api_version,

        ```

        Using managed identity (passing a token provider instead of an API key):

         ```python
        from llama_index.llms.azure_openai import AzureOpenAI

        aoai_endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"
        aoai_api_version = "2023-07-01-preview"

        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

        llm = AzureOpenAI(
            engine = llm_deployment
            model="YOUR_AZURE_OPENAI_COMPLETION_MODEL_NAME",
            azure_ad_token_provider=token_provider,
            use_azure_ad=True,
            azure_endpoint=aoai_endpoint,
            api_version=aoai_api_version,

        ```

    """

    engine: str = Field(description="The name of the deployed azure engine.")
    azure_endpoint: Optional[str] = Field(
        default=None, description="The Azure endpoint to use."
    )
    azure_deployment: Optional[str] = Field(
        default=None, description="The Azure deployment to use."
    )
    use_azure_ad: bool = Field(
        description="Indicates if Microsoft Entra ID (former Azure AD) is used for token authentication"
    )
    azure_ad_token_provider: Optional[AzureADTokenProvider] = Field(
        default=None, description="Callback function to provide Azure Entra ID token."
    )
    api_base: Optional[str] = Field(
        default=None,
        description="The Azure Base URL to use. Useful for proxies on top of Azure OpenAI.",
    )

    _azure_ad_token: Any = PrivateAttr(default=None)
    _client: SyncAzureOpenAI = PrivateAttr()
    _aclient: AsyncAzureOpenAI = PrivateAttr()

    def__init__(
        self,
        model: str = "gpt-35-turbo",
        engine: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        timeout: float = 60.0,
        reuse_client: bool = True,
        api_key: Optional[str] = None,
        api_version: Optional[str] = None,
        api_base: Optional[str] = None,
        # azure specific
        azure_endpoint: Optional[str] = None,
        azure_deployment: Optional[str] = None,
        azure_ad_token_provider: Optional[AzureADTokenProvider] = None,
        use_azure_ad: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        # aliases for engine
        deployment_name: Optional[str] = None,
        deployment_id: Optional[str] = None,
        deployment: Optional[str] = None,
        # custom httpx client
        http_client: Optional[httpx.Client] = None,
        async_http_client: Optional[httpx.AsyncClient] = None,
        # base class
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        **kwargs: Any,
    ) -> None:
        engine = resolve_from_aliases(
            engine, deployment_name, deployment_id, deployment, azure_deployment
        )

        if engine is None:
            raise ValueError("You must specify an `engine` parameter.")

        if api_base is None:
            azure_endpoint = get_from_param_or_env(
                "azure_endpoint", azure_endpoint, "AZURE_OPENAI_ENDPOINT", ""
            )

        super().__init__(
            engine=engine,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            timeout=timeout,
            reuse_client=reuse_client,
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            api_base=api_base,
            azure_ad_token_provider=azure_ad_token_provider,
            use_azure_ad=use_azure_ad,
            api_version=api_version,
            callback_manager=callback_manager,
            http_client=http_client,
            async_http_client=async_http_client,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            **kwargs,
        )

        # reset api_base to None if it is the default
        if self.api_base == DEFAULT_OPENAI_API_BASE or self.azure_endpoint:
            self.api_base = None

    @model_validator(mode="before")
    defvalidate_env(cls, values: Dict[str, Any]) -> Dict[str, Any]:
"""Validate necessary credentials are set."""
        if (
            values["api_base"] == "https://api.openai.com/v1"
            and values["azure_endpoint"] is None
        ):
            raise ValueError(
                "You must set OPENAI_API_BASE to your Azure endpoint. "
                "It should look like https://YOUR_RESOURCE_NAME.openai.azure.com/"
            )
        if values["api_version"] is None:
            raise ValueError("You must set OPENAI_API_VERSION for Azure OpenAI.")

        return values

    def_get_client(self) -> SyncAzureOpenAI:
        if not self.reuse_client:
            return SyncAzureOpenAI(**self._get_credential_kwargs())

        if self._client is None:
            self._client = SyncAzureOpenAI(
                **self._get_credential_kwargs(),
            )
        return self._client

    def_get_aclient(self) -> AsyncAzureOpenAI:
        if not self.reuse_client:
            return AsyncAzureOpenAI(**self._get_credential_kwargs(is_async=True))

        if self._aclient is None:
            self._aclient = AsyncAzureOpenAI(
                **self._get_credential_kwargs(is_async=True),
            )
        return self._aclient

    def_get_credential_kwargs(
        self, is_async: bool = False, **kwargs: Any
    ) -> Dict[str, Any]:
        if self.use_azure_ad:
            if self.azure_ad_token_provider:
                self.api_key = self.azure_ad_token_provider()
            else:
                self._azure_ad_token = refresh_openai_azuread_token(
                    self._azure_ad_token
                )
                self.api_key = self._azure_ad_token.token
        else:
            importos

            self.api_key = self.api_key or os.getenv("AZURE_OPENAI_API_KEY")

        if self.api_key is None:
            raise ValueError(
                "You must set an `api_key` parameter. "
                "Alternatively, you can set the AZURE_OPENAI_API_KEY env var OR set `use_azure_ad=True`."
            )

        return {
            "api_key": self.api_key,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "azure_endpoint": self.azure_endpoint,
            "azure_deployment": self.azure_deployment,
            "base_url": self.api_base,
            "azure_ad_token_provider": self.azure_ad_token_provider,
            "api_version": self.api_version,
            "default_headers": self.default_headers,
            "http_client": self._async_http_client if is_async else self._http_client,
            **kwargs,
        }

    def_get_model_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        model_kwargs = super()._get_model_kwargs(**kwargs)
        model_kwargs["model"] = self.engine
        return model_kwargs

    @classmethod
    defclass_name(cls) -> str:
        return "azure_openai_llm"

```
 |  
| --- | --- |  
###  validate_env [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/azure_openai/#llama_index.llms.azure_openai.AzureOpenAI.validate_env "Permanent link")

```
validate_env(values: [, ]) -> [, ]

```

Validate necessary credentials are set.
Source code in `llama-index-integrations/llms/llama-index-llms-azure-openai/llama_index/llms/azure_openai/base.py`  
| 
```
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
```
 | 
```
@model_validator(mode="before")
defvalidate_env(cls, values: Dict[str, Any]) -> Dict[str, Any]:
"""Validate necessary credentials are set."""
    if (
        values["api_base"] == "https://api.openai.com/v1"
        and values["azure_endpoint"] is None
    ):
        raise ValueError(
            "You must set OPENAI_API_BASE to your Azure endpoint. "
            "It should look like https://YOUR_RESOURCE_NAME.openai.azure.com/"
        )
    if values["api_version"] is None:
        raise ValueError("You must set OPENAI_API_VERSION for Azure OpenAI.")

    return values

```
 |  
| --- | --- |  
##  AzureOpenAIResponses [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/azure_openai/#llama_index.llms.azure_openai.AzureOpenAIResponses "Permanent link")
Bases: 
Azure OpenAI Responses API.
To use this, you must first deploy a model on Azure OpenAI. Unlike OpenAI, you need to specify a `engine` parameter to identify your deployment (called "model deployment name" in Azure portal).
  * model: Name of the model (e.g. `gpt-4o`)
  * engine: This will correspond to the custom name you chose for your deployment when you deployed a model.


You must have the following environment variables set:
  * `OPENAI_API_VERSION`: set this to `2025-03-01-preview` or newer. This may change in the future.
  * `AZURE_OPENAI_ENDPOINT`: your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
  * `AZURE_OPENAI_API_KEY`: your API key if the api type is `azure`

More information can be found here
https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quickstart?tabs=command-line&pivots=programming-language-python
Examples:
`pip install llama-index-llms-azure-openai`

```
fromllama_index.llms.azure_openaiimport AzureOpenAIResponses

aoai_api_key = "YOUR_AZURE_OPENAI_API_KEY"
aoai_endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"
aoai_api_version = "2025-03-01-preview"

llm = AzureOpenAIResponses(
    engine="AZURE_OPENAI_DEPLOYMENT_NAME",
    model="YOUR_AZURE_OPENAI_MODEL_NAME",
    api_key=aoai_api_key,
    azure_endpoint=aoai_endpoint,
    api_version=aoai_api_version,
)

```

Source code in `llama-index-integrations/llms/llama-index-llms-azure-openai/llama_index/llms/azure_openai/responses.py`  
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
```
 | 
```
classAzureOpenAIResponses(OpenAIResponses):
"""
    Azure OpenAI Responses API.

    To use this, you must first deploy a model on Azure OpenAI.
    Unlike OpenAI, you need to specify a `engine` parameter to identify
    your deployment (called "model deployment name" in Azure portal).

    - model: Name of the model (e.g. `gpt-4o`)
    - engine: This will correspond to the custom name you chose
        for your deployment when you deployed a model.

    You must have the following environment variables set:

    - `OPENAI_API_VERSION`: set this to `2025-03-01-preview` or newer.
        This may change in the future.
    - `AZURE_OPENAI_ENDPOINT`: your endpoint should look like the following
        https://YOUR_RESOURCE_NAME.openai.azure.com/
    - `AZURE_OPENAI_API_KEY`: your API key if the api type is `azure`

    More information can be found here:
        https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quickstart?tabs=command-line&pivots=programming-language-python

    Examples:
        `pip install llama-index-llms-azure-openai`

        ```python
        from llama_index.llms.azure_openai import AzureOpenAIResponses

        aoai_api_key = "YOUR_AZURE_OPENAI_API_KEY"
        aoai_endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"
        aoai_api_version = "2025-03-01-preview"

        llm = AzureOpenAIResponses(
            engine="AZURE_OPENAI_DEPLOYMENT_NAME",
            model="YOUR_AZURE_OPENAI_MODEL_NAME",
            api_key=aoai_api_key,
            azure_endpoint=aoai_endpoint,
            api_version=aoai_api_version,

        ```

    """

    engine: str = Field(description="The name of the deployed azure engine.")
    azure_endpoint: Optional[str] = Field(
        default=None, description="The Azure endpoint to use."
    )
    azure_deployment: Optional[str] = Field(
        default=None, description="The Azure deployment to use."
    )
    use_azure_ad: bool = Field(
        default=False,
        description="Indicates if Microsoft Entra ID (former Azure AD) is used for token authentication",
    )
    azure_ad_token_provider: Optional[AzureADTokenProvider] = Field(
        default=None, description="Callback function to provide Azure Entra ID token."
    )

    _azure_ad_token: Any = PrivateAttr(default=None)
    _client: SyncAzureOpenAI = PrivateAttr()
    _aclient: AsyncAzureOpenAI = PrivateAttr()

    def__init__(
        self,
        model: str = "gpt-4o",
        engine: Optional[str] = None,
        temperature: float = 0.1,
        max_output_tokens: Optional[int] = None,
        reasoning_options: Optional[Dict[str, Any]] = None,
        include: Optional[List[str]] = None,
        instructions: Optional[str] = None,
        track_previous_responses: bool = False,
        store: bool = False,
        built_in_tools: Optional[List[dict]] = None,
        truncation: str = "disabled",
        user: Optional[str] = None,
        previous_response_id: Optional[str] = None,
        call_metadata: Optional[Dict[str, Any]] = None,
        strict: bool = False,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        timeout: float = 60.0,
        api_key: Optional[str] = None,
        api_version: Optional[str] = None,
        api_base: Optional[str] = None,
        # azure specific
        azure_endpoint: Optional[str] = None,
        azure_deployment: Optional[str] = None,
        azure_ad_token_provider: Optional[AzureADTokenProvider] = None,
        use_azure_ad: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        # aliases for engine
        deployment_name: Optional[str] = None,
        deployment_id: Optional[str] = None,
        deployment: Optional[str] = None,
        # custom httpx client
        http_client: Optional[httpx.Client] = None,
        async_http_client: Optional[httpx.AsyncClient] = None,
        default_headers: Optional[Dict[str, str]] = None,
        context_window: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        engine = resolve_from_aliases(
            engine, deployment_name, deployment_id, deployment, azure_deployment
        )

        if engine is None:
            raise ValueError("You must specify an `engine` parameter.")

        if api_base is None:
            azure_endpoint = get_from_param_or_env(
                "azure_endpoint", azure_endpoint, "AZURE_OPENAI_ENDPOINT", ""
            )

        # Resolve the API key before building clients
        if use_azure_ad:
            if azure_ad_token_provider:
                api_key = azure_ad_token_provider()
            else:
                self._azure_ad_token = refresh_openai_azuread_token(None)
                api_key = self._azure_ad_token.token
        else:
            api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")

        if api_key is None:
            raise ValueError(
                "You must set an `api_key` parameter. "
                "Alternatively, you can set the AZURE_OPENAI_API_KEY env var OR set `use_azure_ad=True`."
            )

        # Build Azure clients before calling super().__init__() to avoid the
        # parent trying to create plain OpenAI clients with Azure-specific kwargs.
        credential_kwargs = {
            "api_key": api_key,
            "max_retries": max_retries,
            "timeout": timeout,
            "azure_endpoint": azure_endpoint,
            "azure_deployment": azure_deployment,
            "base_url": api_base if api_base else None,
            "azure_ad_token_provider": azure_ad_token_provider,
            "api_version": api_version,
            "default_headers": default_headers,
        }

        sync_client = SyncAzureOpenAI(**credential_kwargs, http_client=http_client)
        async_client = AsyncAzureOpenAI(
            **credential_kwargs, http_client=async_http_client
        )

        super().__init__(
            engine=engine,
            model=model,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            reasoning_options=reasoning_options,
            include=include,
            instructions=instructions,
            track_previous_responses=track_previous_responses,
            store=store,
            built_in_tools=built_in_tools,
            truncation=truncation,
            user=user,
            previous_response_id=previous_response_id,
            call_metadata=call_metadata,
            strict=strict,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            timeout=timeout,
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            api_base=api_base,
            azure_ad_token_provider=azure_ad_token_provider,
            use_azure_ad=use_azure_ad,
            api_version=api_version,
            callback_manager=callback_manager,
            http_client=http_client,
            async_http_client=async_http_client,
            default_headers=default_headers,
            context_window=context_window,
            openai_client=sync_client,
            async_openai_client=async_client,
            **kwargs,
        )

        self._http_client = http_client
        self._async_http_client = async_http_client

    def_get_credential_kwargs(
        self, is_async: bool = False, **kwargs: Any
    ) -> Dict[str, Any]:
        if self.use_azure_ad:
            if self.azure_ad_token_provider:
                self.api_key = self.azure_ad_token_provider()
            else:
                self._azure_ad_token = refresh_openai_azuread_token(
                    self._azure_ad_token
                )
                self.api_key = self._azure_ad_token.token
        else:
            self.api_key = self.api_key or os.getenv("AZURE_OPENAI_API_KEY")

        if self.api_key is None:
            raise ValueError(
                "You must set an `api_key` parameter. "
                "Alternatively, you can set the AZURE_OPENAI_API_KEY env var OR set `use_azure_ad=True`."
            )

        return {
            "api_key": self.api_key,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "azure_endpoint": self.azure_endpoint,
            "azure_deployment": self.azure_deployment,
            "base_url": self.api_base if self.api_base else None,
            "azure_ad_token_provider": self.azure_ad_token_provider,
            "api_version": self.api_version,
            "default_headers": self.default_headers,
            "http_client": self._async_http_client if is_async else self._http_client,
            **kwargs,
        }

    def_get_model_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        model_kwargs = super()._get_model_kwargs(**kwargs)
        model_kwargs["model"] = self.engine
        return model_kwargs

    def_is_azure_client(self) -> bool:
        return True

    @classmethod
    defclass_name(cls) -> str:
        return "azure_openai_responses_llm"

```
 |  
| --- | --- |  
options: members: - AsyncAzureOpenAI - AzureOpenAI - AzureOpenAIResponses - SyncAzureOpenAI
