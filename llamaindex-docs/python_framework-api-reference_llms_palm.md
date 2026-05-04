# Palm
##  PaLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/palm/#llama_index.llms.palm.PaLM "Permanent link")
Bases: `CustomLLM`
PaLM LLM.
Examples:
`pip install llama-index-llms-palm`

```
importgoogle.generativeaiaspalm

# API key for PaLM
palm_api_key = "YOUR_API_KEY_HERE"

# List all models that support text generation
models = [
    m
    for m in palm.list_models()
    if "generateText" in m.supported_generation_methods
]
model = models[0].name
print(model)

# Start using our PaLM LLM abstraction
fromllama_index.llms.palmimport PaLM

# Create an instance of the PaLM class with the API key
llm = PaLM(model_name=model, api_key=palm_api_key)

# Use the complete method to generate text based on a prompt
response = llm.complete("Your prompt text here.")
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-palm/llama_index/llms/palm/base.py`  
| 
```
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
```
 | 
```
classPaLM(CustomLLM):
"""
    PaLM LLM.

    Examples:
        `pip install llama-index-llms-palm`

        ```python
        import google.generativeai as palm

        # API key for PaLM
        palm_api_key = "YOUR_API_KEY_HERE"

        # List all models that support text generation
        models = [

            for m in palm.list_models()
            if "generateText" in m.supported_generation_methods

        model = models[0].name
        print(model)

        # Start using our PaLM LLM abstraction
        from llama_index.llms.palm import PaLM

        # Create an instance of the PaLM class with the API key
        llm = PaLM(model_name=model, api_key=palm_api_key)

        # Use the complete method to generate text based on a prompt
        response = llm.complete("Your prompt text here.")
        print(str(response))
        ```

    """

    model_name: str = Field(
        default=DEFAULT_PALM_MODEL, description="The PaLM model to use."
    )
    num_output: int = Field(
        default=DEFAULT_NUM_OUTPUTS,
        description="The number of tokens to generate.",
        gt=0,
    )
    generate_kwargs: dict = Field(
        default_factory=dict, description="Kwargs for generation."
    )

    _model: Any = PrivateAttr()

    def__init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = DEFAULT_PALM_MODEL,
        num_output: Optional[int] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        **generate_kwargs: Any,
    ) -> None:
"""Initialize params."""
        api_key = api_key or os.environ.get("PALM_API_KEY")
        palm.configure(api_key=api_key)

        models = palm.list_models()
        models_dict = {m.name: m for m in models}
        if model_name not in models_dict:
            raise ValueError(
                f"Model name {model_name} not found in {models_dict.keys()}"
            )

        model_name = model_name
        model = models_dict[model_name]

        # get num_output
        num_output = num_output or model.output_token_limit

        generate_kwargs = generate_kwargs or {}
        super().__init__(
            model_name=model_name,
            num_output=num_output,
            generate_kwargs=generate_kwargs,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )
        self._model = model

    @classmethod
    defclass_name(cls) -> str:
        return "PaLM_llm"

    @property
    defmetadata(self) -> LLMMetadata:
"""Get LLM metadata."""
        # TODO: google palm actually separates input and output token limits
        total_tokens = self._model.input_token_limit + self.num_output
        return LLMMetadata(
            context_window=total_tokens,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
"""
        Predict the answer to a query.

        Args:
            prompt (str): Prompt to use for prediction.

        Returns:
            Tuple[str, str]: Tuple of the predicted answer and the formatted prompt.

        """
        completion = palm.generate_text(
            model=self.model_name,
            prompt=prompt,
            **kwargs,
        )
        return CompletionResponse(text=completion.result, raw=completion.candidates[0])

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
"""
        Stream the answer to a query.

        NOTE: this is a beta feature. Will try to build or use
        better abstractions about response handling.

        Args:
            prompt (str): Prompt to use for prediction.

        Returns:
            str: The predicted answer.

        """
        raise NotImplementedError(
            "PaLM does not support streaming completion in LlamaIndex currently."
        )

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/palm/#llama_index.llms.palm.PaLM.metadata "Permanent link")

```
metadata: 

```

Get LLM metadata.
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/palm/#llama_index.llms.palm.PaLM.complete "Permanent link")

```
complete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Predict the answer to a query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  Prompt to use for prediction.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  Tuple[str, str]: Tuple of the predicted answer and the formatted prompt.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-palm/llama_index/llms/palm/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defcomplete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponse:
"""
    Predict the answer to a query.

    Args:
        prompt (str): Prompt to use for prediction.

    Returns:
        Tuple[str, str]: Tuple of the predicted answer and the formatted prompt.

    """
    completion = palm.generate_text(
        model=self.model_name,
        prompt=prompt,
        **kwargs,
    )
    return CompletionResponse(text=completion.result, raw=completion.candidates[0])

```
 |  
| --- | --- |  
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/palm/#llama_index.llms.palm.PaLM.stream_complete "Permanent link")

```
stream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseGen

```

Stream the answer to a query.
NOTE: this is a beta feature. Will try to build or use better abstractions about response handling.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  Prompt to use for prediction.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  `CompletionResponseGen`  |  The predicted answer.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-palm/llama_index/llms/palm/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defstream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseGen:
"""
    Stream the answer to a query.

    NOTE: this is a beta feature. Will try to build or use
    better abstractions about response handling.

    Args:
        prompt (str): Prompt to use for prediction.

    Returns:
        str: The predicted answer.

    """
    raise NotImplementedError(
        "PaLM does not support streaming completion in LlamaIndex currently."
    )

```
 |  
| --- | --- |  
options: members: - PaLM
