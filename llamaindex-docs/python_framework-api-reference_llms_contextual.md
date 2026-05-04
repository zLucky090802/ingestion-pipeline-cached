# Contextual
##  Contextual [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/contextual/#llama_index.llms.contextual.Contextual "Permanent link")
Bases: 
Generate a response using Contextual's Grounded Language Model (GLM), an LLM engineered specifically to prioritize faithfulness to in-context retrievals over parametric knowledge to reduce hallucinations in Retrieval-Augmented Generation.
The total request cannot exceed 32,000 tokens. Email glm-feedback@contextual.ai with any feedback or questions.
Examples:
`pip install llama-index-llms-contextual`

```
fromllama_index.llms.contextualimport Contextual

# Set up the Contextual class with the required model and API key
llm = Contextual(model="contextual-clm", api_key="your_api_key")

# Call the complete method with a query
response = llm.complete("Explain the importance of low latency LLMs")

print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-contextual/llama_index/llms/contextual/base.py`  
| 
```
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
```
 | 
```
classContextual(OpenAILike):
"""
    Generate a response using Contextual's Grounded Language Model (GLM), an LLM engineered specifically to prioritize faithfulness to in-context retrievals over parametric knowledge to reduce hallucinations in Retrieval-Augmented Generation.

    The total request cannot exceed 32,000 tokens. Email glm-feedback@contextual.ai with any feedback or questions.

    Examples:
        `pip install llama-index-llms-contextual`

        ```python
        from llama_index.llms.contextual import Contextual

        # Set up the Contextual class with the required model and API key
        llm = Contextual(model="contextual-clm", api_key="your_api_key")

        # Call the complete method with a query
        response = llm.complete("Explain the importance of low latency LLMs")

        print(response)
        ```

    """

    model: str = Field(
        description="The model to use. Currently only supports `v1`.", default="v1"
    )
    api_key: str = Field(description="The API key to use.", default=None)
    base_url: str = Field(
        description="The base URL to use.",
        default="https://api.contextual.ai/v1/generate",
    )
    avoid_commentary: bool = Field(
        description="Flag to indicate whether the model should avoid providing additional commentary in responses. Commentary is conversational in nature and does not contain verifiable claims; therefore, commentary is not strictly grounded in available context. However, commentary may provide useful context which improves the helpfulness of responses.",
        default=False,
    )
    client: Any = Field(default=None, description="Contextual AI Client")

    def__init__(
        self,
        model: str,
        api_key: str,
        base_url: str = None,
        avoid_commentary: bool = False,
        **openai_llm_kwargs: Any,
    ) -> None:
        super().__init__(
            model=model,
            api_key=api_key,
            api_base=base_url,
            is_chat_model=openai_llm_kwargs.pop("is_chat_model", True),
            **openai_llm_kwargs,
        )

        try:
            self.client = ContextualAI(api_key=api_key, base_url=base_url)
        except Exception as e:
            raise ValueError(f"Error initializing ContextualAI client: {e}")

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "contextual-clm"

    # Synchronous Methods
    @llm_completion_callback()
    defcomplete(
        self, prompt: str, knowledge: Optional[List[str]] = None, **kwargs
    ) -> CompletionResponse:
"""
        Generate completion for the given prompt.

        Args:
            prompt (str): The input prompt to generate completion for.
            **kwargs: Additional keyword arguments for the API request.

        Returns:
            str: The generated text completion.

        """
        messages_list = [{"role": MessageRole.USER, "content": prompt}]
        response = self._generate(
            knowledge=knowledge,
            messages=messages_list,
            model=self.model,
            system_prompt=self.system_prompt,
            **kwargs,
        )
        return CompletionResponse(text=response)

    @llm_chat_callback()
    defchat(self, messages: List[ChatMessage], **kwargs) -> ChatResponse:
"""
        Generate a chat response for the given messages.
        """
        messages_list = [
            {"role": msg.role, "content": msg.blocks[0].text} for msg in messages
        ]
        response = self._generate(
            knowledge=kwargs.get("knowledge_base"),
            messages=messages_list,
            model=self.model,
            system_prompt=self.system_prompt,
            **kwargs,
        )
        return ChatResponse(
            message=ChatMessage(role=MessageRole.ASSISTANT, content=response)
        )

    @llm_chat_callback()
    defstream_chat(self, messages: List[ChatMessage], **kwargs) -> ChatResponseGen:
"""
        Generate a chat response for the given messages.
        """
        raise NotImplementedError("stream methods not implemented in Contextual")

    @llm_completion_callback()
    defstream_complete(self, prompt: str, **kwargs) -> ChatResponseGen:
"""
        Generate a chat response for the given messages.
        """
        raise NotImplementedError("stream methods not implemented in Contextual")

    # ===== Async Endpoints =====
    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        raise NotImplementedError("async methods not implemented in Contextual")

    @llm_chat_callback()
    async defastream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        raise NotImplementedError("async methods not implemented in Contextual")

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        raise NotImplementedError("async methods not implemented in Contextual")

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        raise NotImplementedError("async methods not implemented in Contextual")

    def_generate(
        self, knowledge, messages, system_prompt, **kwargs
    ) -> CompletionResponse:
"""
        Generate completion for the given prompt.
        """
        raw_message = self.client.generate.create(
            messages=messages,
            knowledge=knowledge or [],
            model=self.model,
            system_prompt=system_prompt,
            avoid_commentary=self.avoid_commentary,
            temperature=kwargs.get("temperature", 0.0),
            max_new_tokens=kwargs.get("max_tokens", 1024),
            top_p=kwargs.get("top_p", 1),
        )
        return raw_message.response

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/contextual/#llama_index.llms.contextual.Contextual.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-contextual/llama_index/llms/contextual/base.py`  
| 
```
82
83
84
85
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "contextual-clm"

```
 |  
| --- | --- |  
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/contextual/#llama_index.llms.contextual.Contextual.complete "Permanent link")

```
complete(
    prompt: ,
    knowledge: Optional[[]] = None,
    **kwargs
) -> 

```

Generate completion for the given prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The input prompt to generate completion for.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API request.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |   |  The generated text completion.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-contextual/llama_index/llms/contextual/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defcomplete(
    self, prompt: str, knowledge: Optional[List[str]] = None, **kwargs
) -> CompletionResponse:
"""
    Generate completion for the given prompt.

    Args:
        prompt (str): The input prompt to generate completion for.
        **kwargs: Additional keyword arguments for the API request.

    Returns:
        str: The generated text completion.

    """
    messages_list = [{"role": MessageRole.USER, "content": prompt}]
    response = self._generate(
        knowledge=knowledge,
        messages=messages_list,
        model=self.model,
        system_prompt=self.system_prompt,
        **kwargs,
    )
    return CompletionResponse(text=response)

```
 |  
| --- | --- |  
###  chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/contextual/#llama_index.llms.contextual.Contextual.chat "Permanent link")

```
chat(messages: [], **kwargs) -> 

```

Generate a chat response for the given messages.
Source code in `llama-index-integrations/llms/llama-index-llms-contextual/llama_index/llms/contextual/base.py`  
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
```
 | 
```
@llm_chat_callback()
defchat(self, messages: List[ChatMessage], **kwargs) -> ChatResponse:
"""
    Generate a chat response for the given messages.
    """
    messages_list = [
        {"role": msg.role, "content": msg.blocks[0].text} for msg in messages
    ]
    response = self._generate(
        knowledge=kwargs.get("knowledge_base"),
        messages=messages_list,
        model=self.model,
        system_prompt=self.system_prompt,
        **kwargs,
    )
    return ChatResponse(
        message=ChatMessage(role=MessageRole.ASSISTANT, content=response)
    )

```
 |  
| --- | --- |  
###  stream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/contextual/#llama_index.llms.contextual.Contextual.stream_chat "Permanent link")

```
stream_chat(
    messages: [], **kwargs
) -> ChatResponseGen

```

Generate a chat response for the given messages.
Source code in `llama-index-integrations/llms/llama-index-llms-contextual/llama_index/llms/contextual/base.py`  
| 
```
132
133
134
135
136
137
```
 | 
```
@llm_chat_callback()
defstream_chat(self, messages: List[ChatMessage], **kwargs) -> ChatResponseGen:
"""
    Generate a chat response for the given messages.
    """
    raise NotImplementedError("stream methods not implemented in Contextual")

```
 |  
| --- | --- |  
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/contextual/#llama_index.llms.contextual.Contextual.stream_complete "Permanent link")

```
stream_complete(prompt: , **kwargs) -> ChatResponseGen

```

Generate a chat response for the given messages.
Source code in `llama-index-integrations/llms/llama-index-llms-contextual/llama_index/llms/contextual/base.py`  
| 
```
139
140
141
142
143
144
```
 | 
```
@llm_completion_callback()
defstream_complete(self, prompt: str, **kwargs) -> ChatResponseGen:
"""
    Generate a chat response for the given messages.
    """
    raise NotImplementedError("stream methods not implemented in Contextual")

```
 |  
| --- | --- |  
options: members: - Contextual
