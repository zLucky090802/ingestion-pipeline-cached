# Openvino
##  OpenVINOLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openvino/#llama_index.llms.openvino.OpenVINOLLM "Permanent link")
Bases: 
OpenVINOLLM LLM.
Examples:
`pip install llama-index-llms-openvino`

```
fromllama_index.llms.openvinoimport OpenVINOLLM

defmessages_to_prompt(messages):
    prompt = ""
    for message in messages:
        if message.role == 'system':
        prompt += f"<|system|>\n{message.content}</s>\n"
        elif message.role == 'user':
        prompt += f"<|user|>\n{message.content}</s>\n"
        elif message.role == 'assistant':
        prompt += f"<|assistant|>\n{message.content}</s>\n"

    # ensure we start with a system prompt, insert blank if needed
    if not prompt.startswith("<|system|>\n"):
        prompt = "<|system|>\n</s>\n" + prompt

    # add final assistant prompt
    prompt = prompt + "<|assistant|>\n"

    return prompt

defcompletion_to_prompt(completion):
    return f"<|system|>\n</s>\n<|user|>\n{completion}</s>\n<|assistant|>\n"

importtorch
fromllama_index.core.promptsimport PromptTemplate
fromllama_index.llms.openvinoimport OpenVINOLLM

ov_config = {
    "PERFORMANCE_HINT": "LATENCY",
    "NUM_STREAMS": "1",
    "CACHE_DIR": "",
}

llm = OpenVINOLLM(
    model_id_or_path="HuggingFaceH4/zephyr-7b-beta",
    tokenizer_name="HuggingFaceH4/zephyr-7b-beta",
    context_window=3900,
    max_new_tokens=256,
    model_kwargs={"ov_config": ov_config},
    generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    device_map="auto",
)

response = llm.complete("What is the meaning of life?")
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-openvino/llama_index/llms/openvino/base.py`  
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
```
 | 
```
classOpenVINOLLM(HuggingFaceLLM):
r"""
    OpenVINOLLM LLM.

    Examples:
        `pip install llama-index-llms-openvino`

        ```python
        from llama_index.llms.openvino import OpenVINOLLM

        def messages_to_prompt(messages):
            prompt = ""
            for message in messages:
                if message.role == 'system':
                prompt += f"<|system|>\n{message.content}</s>\n"
                elif message.role == 'user':
                prompt += f"<|user|>\n{message.content}</s>\n"
                elif message.role == 'assistant':
                prompt += f"<|assistant|>\n{message.content}</s>\n"

            # ensure we start with a system prompt, insert blank if needed
            if not prompt.startswith("<|system|>\n"):
                prompt = "<|system|>\n</s>\n" + prompt

            # add final assistant prompt
            prompt = prompt + "<|assistant|>\n"

            return prompt

        def completion_to_prompt(completion):
            return f"<|system|>\n</s>\n<|user|>\n{completion}</s>\n<|assistant|>\n"

        import torch
        from llama_index.core.prompts import PromptTemplate
        from llama_index.llms.openvino import OpenVINOLLM

        ov_config = {
            "PERFORMANCE_HINT": "LATENCY",
            "NUM_STREAMS": "1",
            "CACHE_DIR": "",


        llm = OpenVINOLLM(
            model_id_or_path="HuggingFaceH4/zephyr-7b-beta",
            tokenizer_name="HuggingFaceH4/zephyr-7b-beta",
            context_window=3900,
            max_new_tokens=256,
            model_kwargs={"ov_config": ov_config},
            generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            device_map="auto",


        response = llm.complete("What is the meaning of life?")
        print(str(response))
        ```

    """

    model_id_or_path: str = Field(
        default=DEFAULT_HUGGINGFACE_MODEL,
        description=(
            "The model name to use from HuggingFace. "
            "Unused if `model` is passed in directly."
        ),
    )

    def__init__(
        self,
        context_window: int = DEFAULT_CONTEXT_WINDOW,
        max_new_tokens: int = DEFAULT_NUM_OUTPUTS,
        query_wrapper_prompt: Union[str, PromptTemplate] = "{query_str}",
        model_id_or_path: str = DEFAULT_HUGGINGFACE_MODEL,
        model: Optional[Any] = None,
        tokenizer: Optional[Any] = None,
        device_map: Optional[str] = "auto",
        stopping_ids: Optional[List[int]] = None,
        tokenizer_kwargs: Optional[dict] = None,
        tokenizer_outputs_to_remove: Optional[list] = None,
        model_kwargs: Optional[dict] = None,
        generate_kwargs: Optional[dict] = None,
        is_chat_model: Optional[bool] = False,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: str = "",
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
"""Initialize params."""
        model_kwargs = model_kwargs or {}

        defrequire_model_export(
            model_id: str, revision: Any = None, subfolder: Any = None
        ) -> bool:
            model_dir = Path(model_id)
            if subfolder is not None:
                model_dir = model_dir / subfolder
            if model_dir.is_dir():
                return (
                    not (model_dir / "openvino_model.xml").exists()
                    or not (model_dir / "openvino_model.bin").exists()
                )
            hf_api = HfApi()
            try:
                model_info = hf_api.model_info(model_id, revision=revision or "main")
                normalized_subfolder = (
                    None if subfolder is None else Path(subfolder).as_posix()
                )
                model_files = [
                    file.rfilename
                    for file in model_info.siblings
                    if normalized_subfolder is None
                    or file.rfilename.startswith(normalized_subfolder)
                ]
                ov_model_path = (
                    "openvino_model.xml"
                    if subfolder is None
                    else f"{normalized_subfolder}/openvino_model.xml"
                )
                return (
                    ov_model_path not in model_files
                    or ov_model_path.replace(".xml", ".bin") not in model_files
                )
            except Exception:
                return True

        if require_model_export(model_id_or_path):
            # use remote model
            ov_model = model or OVModelForCausalLM.from_pretrained(
                model_id_or_path, export=True, device=device_map, **model_kwargs
            )
        else:
            # use local model
            ov_model = model or OVModelForCausalLM.from_pretrained(
                model_id_or_path, device=device_map, **model_kwargs
            )
        super().__init__(
            context_window=context_window,
            max_new_tokens=max_new_tokens,
            query_wrapper_prompt=query_wrapper_prompt,
            tokenizer_name=model_id_or_path,
            model_name=model_id_or_path,
            model=ov_model,
            tokenizer=tokenizer,
            device_map=device_map,
            stopping_ids=stopping_ids or [],
            tokenizer_kwargs=tokenizer_kwargs or {},
            tokenizer_outputs_to_remove=tokenizer_outputs_to_remove or [],
            model_kwargs=model_kwargs or {},
            generate_kwargs=generate_kwargs or {},
            is_chat_model=is_chat_model,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "OpenVINO_LLM"

```
 |  
| --- | --- |  
options: members: - OpenVINOLLM
