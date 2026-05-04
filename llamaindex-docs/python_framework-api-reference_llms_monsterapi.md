# Monsterapi
##  MonsterLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/monsterapi/#llama_index.llms.monsterapi.MonsterLLM "Permanent link")
Bases: 
Source code in `llama-index-integrations/llms/llama-index-llms-monsterapi/llama_index/llms/monsterapi/base.py`  
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
```
 | 
```
classMonsterLLM(OpenAI):
    model_info: dict = Field(
        description="Model info field with pricing and other llm model information in json structure.",
        default={},
    )

"""MonsterAPI LLM.

    Monster Deploy enables you to host any vLLM supported large language model (LLM) like Tinyllama, Mixtral, Phi-2 etc as a rest API endpoint on MonsterAPI's cost optimised GPU cloud.

    With MonsterAPI's integration in Llama index, you can use your deployed LLM API endpoints to create RAG system or RAG bot for use cases such as:
    - Answering questions on your documents
    - Improving the content of your documents
    - Finding context of importance in your documents


    Once deployment is launched use the base_url and api_auth_token once deployment is live and use them below.

    Note: When using LLama index to access Monster Deploy LLMs, you need to create a prompt with required template and send compiled prompt as input.
    See `LLama Index Prompt Template Usage example` section for more details.

    see (https://developer.monsterapi.ai/docs/monster-deploy-beta) for more details

    Once deployment is launched use the base_url and api_auth_token once deployment is live and use them below.

    Note: When using LLama index to access Monster Deploy LLMs, you need to create a prompt with reqhired template and send compiled prompt as input. see section `LLama Index Prompt Template
    Usage example` for more details.

    Examples:
        `pip install llama-index-llms-monsterapi`

        1. MonsterAPI Private LLM Deployment use case
        ```python
        from llama_index.llms.monsterapi import MonsterLLM
        # User monsterAPI Deploy service to launch a deployment
        # then get api_endpoint and api_auth_token and use them as api_base and api_key respectively.
        llm = MonsterLLM(
            model = "whatever is the basemodel used to deploy the llm",
            api_base="https://ecc7deb6-26e0-419b-a7f2-0deb934af29a.monsterapi.ai",
            api_key="a0f8a6ba-c32f-4407-af0c-169f1915490c",
            temperature=0.75,


        response = llm.complete("What is the capital of France?")
        ```

        2. Monster API General Available LLMs
        ```python3
        from llama_index.llms.monsterapi import MonsterLLM
        llm = MonsterLLM(
            model="microsoft/Phi-3-mini-4k-instruct"


        response = llm.complete("What is the capital of France?")
        print(str(response))
        ```
    """

    def__init__(
        self,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_NUM_OUTPUTS,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 10,
        api_base: Optional[str] = DEFAULT_API_BASE,
        api_key: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
        additional_kwargs = additional_kwargs or {}
        callback_manager = callback_manager or CallbackManager([])

        api_base = get_from_param_or_env("api_base", api_base, "MONSTER_API_BASE")
        api_key = get_from_param_or_env("api_key", api_key, "MONSTER_API_KEY")

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_base=api_base,
            api_key=api_key,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )

        self.model_info = self._fetch_model_details(api_base, api_key)

    @classmethod
    defclass_name(cls) -> str:
        return "MonsterAPI LLMs"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self._modelname_to_contextsize(self.model),
            num_output=self.max_tokens,
            is_chat_model=True,
            model_name=self.model,
            is_function_calling_model=False,
        )

    @property
    def_is_chat_model(self) -> bool:
        return True

    def_fetch_model_details(self, api_base: str, api_key: str):
        headers = {"Authorization": f"Bearer {api_key}", "accept": "application/json"}
        response = requests.get(f"{api_base}/models/info", headers=headers)
        response.raise_for_status()

        details = response.json()
        return details["maximum_context_length"]

    def_modelname_to_contextsize(self, model_name):
        return self.model_info.get(model_name)

```
 |  
| --- | --- |  
###  model_info `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/monsterapi/#llama_index.llms.monsterapi.MonsterLLM.model_info "Permanent link")

```
model_info:  = _fetch_model_details(api_base, api_key)

```

MonsterAPI LLM.
Monster Deploy enables you to host any vLLM supported large language model (LLM) like Tinyllama, Mixtral, Phi-2 etc as a rest API endpoint on MonsterAPI's cost optimised GPU cloud.
With MonsterAPI's integration in Llama index, you can use your deployed LLM API endpoints to create RAG system or RAG bot for use cases such as: - Answering questions on your documents - Improving the content of your documents - Finding context of importance in your documents
Once deployment is launched use the base_url and api_auth_token once deployment is live and use them below.
Note: When using LLama index to access Monster Deploy LLMs, you need to create a prompt with required template and send compiled prompt as input. See `LLama Index Prompt Template Usage example` section for more details.
see (https://developer.monsterapi.ai/docs/monster-deploy-beta) for more details
Once deployment is launched use the base_url and api_auth_token once deployment is live and use them below.
Note: When using LLama index to access Monster Deploy LLMs, you need to create a prompt with reqhired template and send compiled prompt as input. see section `LLama Index Prompt Template Usage example` for more details.
Examples:
`pip install llama-index-llms-monsterapi`
  1. MonsterAPI Private LLM Deployment use case 

```
fromllama_index.llms.monsterapiimport MonsterLLM
# User monsterAPI Deploy service to launch a deployment
# then get api_endpoint and api_auth_token and use them as api_base and api_key respectively.
llm = MonsterLLM(
    model = "whatever is the basemodel used to deploy the llm",
    api_base="https://ecc7deb6-26e0-419b-a7f2-0deb934af29a.monsterapi.ai",
    api_key="a0f8a6ba-c32f-4407-af0c-169f1915490c",
    temperature=0.75,
)

response = llm.complete("What is the capital of France?")

```

  2. Monster API General Available LLMs 

```
fromllama_index.llms.monsterapiimport MonsterLLM
llm = MonsterLLM(
    model="microsoft/Phi-3-mini-4k-instruct"
)

response = llm.complete("What is the capital of France?")
print(str(response))

```



options: members: - MonsterLLM
