# Replicate
##  Replicate [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/replicate/#llama_index.llms.replicate.Replicate "Permanent link")
Bases: `CustomLLM`
Replicate LLM.
Examples:
`pip install llama-index-llms-replicate`

```
fromllama_index.llms.replicateimport Replicate

# Set up the Replicate API token
importos
os.environ["REPLICATE_API_TOKEN"] = "<your API key>"

# Initialize the Replicate class
llm = Replicate(
    model="replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b"
)

# Example of calling the 'complete' method with a prompt
resp = llm.complete("Who is Paul Graham?")

print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-replicate/llama_index/llms/replicate/base.py`  
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
```
 | 
```
classReplicate(CustomLLM):
"""
    Replicate LLM.

    Examples:
        `pip install llama-index-llms-replicate`

        ```python
        from llama_index.llms.replicate import Replicate

        # Set up the Replicate API token
        import os
        os.environ["REPLICATE_API_TOKEN"] = "<your API key>"

        # Initialize the Replicate class
        llm = Replicate(
            model="replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b"


        # Example of calling the 'complete' method with a prompt
        resp = llm.complete("Who is Paul Graham?")

        print(resp)
        ```

    """

    model: str = Field(description="The Replicate model to use.")
    temperature: float = Field(
        default=DEFAULT_REPLICATE_TEMP,
        description="The temperature to use for sampling.",
        ge=0.01,
        le=1.0,
    )
    image: str = Field(
        default="", description="The image file for multimodal model to use. (optional)"
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model.",
        gt=0,
    )
    prompt_key: str = Field(
        default="prompt", description="The key to use for the prompt in API calls."
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the Replicate API."
    )
    is_chat_model: bool = Field(
        default=False, description="Whether the model is a chat model."
    )

    @classmethod
    defclass_name(cls) -> str:
        return "Replicate_llm"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=DEFAULT_NUM_OUTPUTS,
            model_name=self.model,
            is_chat_model=self.is_chat_model,
        )

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs: Dict[str, Any] = {
            "temperature": self.temperature,
            "max_length": self.context_window,
        }
        if self.image != "":
            try:
                base_kwargs["image"] = open(self.image, "rb")
            except FileNotFoundError:
                raise FileNotFoundError(
                    "Could not load image file. Please check whether the file exists"
                )
        return {
            **base_kwargs,
            **self.additional_kwargs,
        }

    def_get_input_dict(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        return {self.prompt_key: prompt, **self._model_kwargs, **kwargs}

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        prompt = self.messages_to_prompt(messages)
        completion_response = self.complete(prompt, formatted=True, **kwargs)
        return completion_response_to_chat_response(completion_response)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        prompt = self.messages_to_prompt(messages)
        completion_response = self.stream_complete(prompt, formatted=True, **kwargs)
        return stream_completion_response_to_chat_response(completion_response)

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        response_gen = self.stream_complete(prompt, formatted=formatted, **kwargs)
        response_list = list(response_gen)
        final_response = response_list[-1]
        final_response.delta = None
        return final_response

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        try:
            importreplicate
        except ImportError:
            raise ImportError(
                "Could not import replicate library."
                "Please install replicate with `pip install replicate`"
            )

        if not formatted:
            prompt = self.completion_to_prompt(prompt)
        input_dict = self._get_input_dict(prompt, **kwargs)
        response_iter = replicate.stream(self.model, input=input_dict)

        defgen() -> CompletionResponseGen:
            text = ""
            for server_event in response_iter:
                delta = str(server_event)
                text += delta
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                )

        return gen()

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/replicate/#llama_index.llms.replicate.Replicate.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
options: members: - Replicate
