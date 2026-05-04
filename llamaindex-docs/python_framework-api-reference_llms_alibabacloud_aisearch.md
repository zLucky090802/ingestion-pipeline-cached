# Alibabacloud aisearch
##  AlibabaCloudAISearchLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/alibabacloud_aisearch/#llama_index.llms.alibabacloud_aisearch.AlibabaCloudAISearchLLM "Permanent link")
Bases: `CustomLLM`
For further details, please visit `https://help.aliyun.com/zh/open-search/search-platform/developer-reference/text-generation-api-details`.
Source code in `llama-index-integrations/llms/llama-index-llms-alibabacloud-aisearch/llama_index/llms/alibabacloud_aisearch/base.py`  
| 
```
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
```
 | 
```
classAlibabaCloudAISearchLLM(CustomLLM):
"""
    For further details, please visit `https://help.aliyun.com/zh/open-search/search-platform/developer-reference/text-generation-api-details`.
    """

    _client: Client = PrivateAttr()
    _options: RuntimeOptions = PrivateAttr()

    aisearch_api_key: str = Field(default=None, exclude=True)
    endpoint: str = None

    service_id: str = "ops-qwen-turbo"
    workspace_name: str = "default"

    temperature: float = 0.5
    top_k: float = 1
    additional_kwargs: Dict[str, Any] = Field(default_factory=dict)

    read_timeout: int = 60000
    connection_timeout: int = 5000
    csi_level: str = "strict"

    def__init__(
        self, endpoint: str = None, aisearch_api_key: str = None, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.aisearch_api_key = get_from_param_or_env(
            "aisearch_api_key", aisearch_api_key, "AISEARCH_API_KEY"
        )
        self.endpoint = get_from_param_or_env("endpoint", endpoint, "AISEARCH_ENDPOINT")

        config = AISearchConfig(
            bearer_token=self.aisearch_api_key,
            endpoint=self.endpoint,
            protocol="http",
        )

        self._client = Client(config=config)

        self._options = RuntimeOptions(
            read_timeout=self.read_timeout, connect_timeout=self.connection_timeout
        )

    @property
    defmetadata(self) -> LLMMetadata:
"""Get LLM metadata."""
        return LLMMetadata(model_name=self.service_id, is_chat_model=True)

    @property
    def_default_params(self) -> Dict[str, Any]:
        return {
            "temperature": self.temperature,
            "top_k": self.top_k,
            **self.additional_kwargs,
        }

    @staticmethod
    def_convert_chat_messages(
        messages: Sequence[ChatMessage],
    ) -> List[GetTextGenerationRequestMessages]:
        results = []
        for message in messages:
            message = GetTextGenerationRequestMessages(
                content=message.content, role=message.role
            )
            results.append(message)
        return results

    @retry_decorator
    def_get_text_generation(
        self, messages: List[GetTextGenerationRequestMessages], **kwargs: Any
    ) -> GetTextGenerationResponse:
        parameters: Dict[str, Any] = self._default_params
        parameters.update(kwargs)
        request = GetTextGenerationRequest(
            csi_level=self.csi_level, messages=messages, parameters=parameters
        )

        response: GetTextGenerationResponse = (
            self._client.get_text_generation_with_options(
                workspace_name=self.workspace_name,
                service_id=self.service_id,
                request=request,
                headers={},
                runtime=self._options,
            )
        )
        return response

    @aretry_decorator
    async def_aget_text_generation(
        self, messages: List[GetTextGenerationRequestMessages], **kwargs: Any
    ) -> GetTextGenerationResponse:
        parameters: Dict[str, Any] = self._default_params
        parameters.update(kwargs)
        request = GetTextGenerationRequest(
            csi_level=self.csi_level, messages=messages, parameters=parameters
        )

        response: GetTextGenerationResponse = (
            await self._client.get_text_generation_with_options_async(
                workspace_name=self.workspace_name,
                service_id=self.service_id,
                request=request,
                headers={},
                runtime=self._options,
            )
        )

        return response

    @llm_completion_callback()
    defcomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        messages = [
            GetTextGenerationRequestMessages(content=prompt, role=MessageRole.USER)
        ]
        response: GetTextGenerationResponse = self._get_text_generation(
            messages, **kwargs
        )
        text = response.body.result.text
        return CompletionResponse(text=text, raw=response)

    defstream_complete(self, messages: Any, **kwargs: Any) -> CompletionResponse:
        raise NotImplementedError

    @llm_completion_callback()
    async defacomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        messages = [
            GetTextGenerationRequestMessages(content=prompt, role=MessageRole.USER)
        ]
        response: GetTextGenerationResponse = await self._aget_text_generation(
            messages, **kwargs
        )
        text = response.body.result.text
        return CompletionResponse(text=text, raw=response)

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        messages = self._convert_chat_messages(messages)
        response: GetTextGenerationResponse = self._get_text_generation(
            messages, **kwargs
        )
        text = response.body.result.text
        return ChatResponse(
            message=ChatMessage(role=MessageRole.ASSISTANT, content=text), raw=response
        )

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        messages = self._convert_chat_messages(messages)
        response: GetTextGenerationResponse = await self._aget_text_generation(
            messages, **kwargs
        )
        text = response.body.result.text
        return ChatResponse(
            message=ChatMessage(role=MessageRole.ASSISTANT, content=text), raw=response
        )

    @classmethod
    defclass_name(cls) -> str:
        return "AlibabaCloudAISearchLLM"

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/alibabacloud_aisearch/#llama_index.llms.alibabacloud_aisearch.AlibabaCloudAISearchLLM.metadata "Permanent link")

```
metadata: 

```

Get LLM metadata.
options: members: - AlibabaCloudAISearchLLM
