# Notdiamond
##  NotDiamondSelector [#](https://developers.llamaindex.ai/python/framework-api-reference/selectors/notdiamond/#llama_index.selectors.notdiamond.NotDiamondSelector "Permanent link")
Bases: `LLMSingleSelector`
Source code in `llama-index-integrations/selectors/llama-index-selectors-notdiamond/llama_index/selectors/notdiamond/base.py`  
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
```
 | 
```
classNotDiamondSelector(LLMSingleSelector):
    def__init__(
        self,
        client: NotDiamond,
        metric: Metric = None,
        timeout: int = 10,
        api_key: str = None,
        *args,
        **kwargs,
    ):
"""
        Initialize a NotDiamondSelector. Users should instantiate and configure a NotDiamond client as needed before
        creating this selector. The constructor will raise errors re: required client fields.
        """
        # Not needed - we will route using our own client based on the query prompt
        # Add @property for _llm here
        _encap_selector = LLMSingleSelector.from_defaults(llm=MockLLM())
        self._llm = None
        self._prompt = _encap_selector._prompt

        if not getattr(client, "llm_configs", None):
            raise ValueError(
                "NotDiamond client must have llm_configs before creating a NotDiamondSelector."
            )

        if metric and not isinstance(metric, Metric):
            raise ValueError(f"Invalid metric - needed type Metric but got {metric}")
        self._metric = metric or Metric("accuracy")

        self._client = client
        self._llms = [
            self._llm_config_to_client(llm_config)
            for llm_config in self._client.llm_configs
        ]
        self._timeout = timeout
        super().__init__(_encap_selector._llm, _encap_selector._prompt, *args, **kwargs)

    def_llm_config_to_client(self, llm_config: LLMConfig | str) -> LLM:
"""
        For the selected LLMConfig dynamically create an LLM instance. NotDiamondSelector will
        assign this to self._llm to help select the best index.
        """
        if isinstance(llm_config, str):
            llm_config = LLMConfig.from_string(llm_config)
        provider, model = llm_config.provider, llm_config.model

        output = None
        if provider == "openai":
            fromllama_index.llms.openaiimport OpenAI

            output = OpenAI(model=model, api_key=os.getenv("OPENAI_API_KEY"))
        elif provider == "anthropic":
            fromllama_index.llms.anthropicimport Anthropic

            output = Anthropic(model=model, api_key=os.getenv("ANTHROPIC_API_KEY"))
        elif provider == "cohere":
            fromllama_index.llms.cohereimport Cohere

            output = Cohere(model=model, api_key=os.getenv("COHERE_API_KEY"))
        elif provider == "mistral":
            fromllama_index.llms.mistralaiimport MistralAI

            output = MistralAI(model=model, api_key=os.getenv("MISTRALAI_API_KEY"))
        elif provider == "togetherai":
            fromllama_index.llms.togetherimport TogetherLLM

            output = TogetherLLM(model=model, api_key=os.getenv("TOGETHERAI_API_KEY"))
        else:
            raise ValueError(f"Unsupported provider for NotDiamondSelector: {provider}")

        return output

    def_select(
        self, choices: Sequence[ToolMetadata], query: QueryBundle, timeout: int = None
    ) -> SelectorResult:
"""
        Call Not Diamond to select the best LLM for the given prompt, then have the LLM select the best tool.
        """
        messages = [
            {"role": "system", "content": self._format_prompt(choices, query)},
            {"role": "user", "content": query.query_str},
        ]

        session_id, best_llm = self._client.model_select(
            messages=messages,
            llm_configs=self._client.llm_configs,
            metric=self._metric,
            notdiamond_api_key=self._client.api_key,
            max_model_depth=self._client.max_model_depth,
            hash_content=self._client.hash_content,
            tradeoff=self._client.tradeoff,
            preference_id=self._client.preference_id,
            tools=self._client.tools,
            timeout=timeout or self._timeout,
        )

        self._llm = self._llm_config_to_client(best_llm)

        return NotDiamondSelectorResult.from_selector_result(
            super()._select(choices, query), session_id, best_llm
        )

    async def_aselect(
        self, choices: Sequence[ToolMetadata], query: QueryBundle, timeout: int = None
    ) -> SelectorResult:
"""
        Call Not Diamond asynchronously to select the best LLM for the given prompt, then have the LLM select the best tool.
        """
        messages = [
            {"role": "system", "content": self._format_prompt(choices, query)},
            {"role": "user", "content": query.query_str},
        ]

        session_id, best_llm = await self._client.amodel_select(
            messages=messages,
            llm_configs=self._client.llm_configs,
            metric=self._metric,
            notdiamond_api_key=self._client.api_key,
            max_model_depth=self._client.max_model_depth,
            hash_content=self._client.hash_content,
            tradeoff=self._client.tradeoff,
            preference_id=self._client.preference_id,
            tools=self._client.tools,
            timeout=timeout or self._timeout,
        )

        self._llm = self._llm_config_to_client(best_llm)

        return NotDiamondSelectorResult.from_selector_result(
            await super()._aselect(choices, query), session_id, best_llm
        )

    def_format_prompt(
        self, choices: Sequence[ToolMetadata], query: QueryBundle
    ) -> str:
"""
        A system prompt for selection is created when instantiating the parent LLMSingleSelector class.
        This method formats the prompt into a str so that it can be serialized for the NotDiamond API.
        """
        context_list = _build_choices_text(choices)
        return self._prompt.format(
            num_choices=len(choices),
            context_list=context_list,
            query_str=query.query_str,
        )

```
 |  
| --- | --- |  
options: members: - NotDiamondSelector
