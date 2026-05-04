# Cleanlab
##  CleanlabTLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cleanlab/#llama_index.llms.cleanlab.CleanlabTLM "Permanent link")
Bases: `CustomLLM`
Cleanlab TLM.
Examples:
`pip install llama-index-llms-cleanlab`

```
fromllama_index.llms.cleanlabimport CleanlabTLM

llm = CleanlabTLM(api_key=api_key, quality_preset="best", options={"log": ["explanation"]})
resp = llm.complete("Who is Paul Graham?")
print(resp)

```

Arguments: `quality_preset` and `options` are configuration settings you can optionally specify to improve latency or accuracy.
More information can be found here
https://help.cleanlab.ai/tlm/
Source code in `llama-index-integrations/llms/llama-index-llms-cleanlab/llama_index/llms/cleanlab/base.py`  
| 
```
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
```
 | 
```
classCleanlabTLM(CustomLLM):
"""
    Cleanlab TLM.

    Examples:
        `pip install llama-index-llms-cleanlab`

        ```python
        from llama_index.llms.cleanlab import CleanlabTLM

        llm = CleanlabTLM(api_key=api_key, quality_preset="best", options={"log": ["explanation"]})
        resp = llm.complete("Who is Paul Graham?")
        print(resp)
        ```

    Arguments:
    `quality_preset` and `options` are configuration settings you can optionally specify to improve latency or accuracy.

    More information can be found here:
        https://help.cleanlab.ai/tlm/

    """

    model: str = Field(
        default=DEFAULT_MODEL,
        description="Base LLM to use with TLM.",
    )
    max_tokens: int = Field(
        default=DEFAULT_MAX_TOKENS,
        description="The maximum number of tokens to generate in TLM response.",
    )
    _client: Any = PrivateAttr()

    def__init__(
        self,
        api_key: Optional[str] = None,
        quality_preset: Optional[str] = DEFAULT_QUALITY_PRESET,
        options: Optional[Dict] = None,
        callback_manager: Optional[CallbackManager] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            additional_kwargs=additional_kwargs or {},
            callback_manager=callback_manager,
        )

        self.max_tokens = (
            options.get("max_tokens")
            if options and "max_tokens" in options
            else DEFAULT_MAX_TOKENS
        )

        api_key = get_from_param_or_env("api_key", api_key, "CLEANLAB_API_KEY")

        self._client = TLM(
            api_key=api_key, quality_preset=quality_preset, options=options
        )
        self.model = self._client.get_model_name()

    @classmethod
    defclass_name(cls) -> str:
        return "CleanlabTLM"

    @property
    defmetadata(self) -> LLMMetadata:
"""Get LLM metadata."""
        return LLMMetadata(
            context_window=get_default_context_limit(),
            num_output=self.max_tokens,
            model_name=self.model,
        )

    def_parse_response(self, response: Dict) -> CompletionResponse:
"""Parse the response from TLM and return a CompletionResponse object."""
        try:
            text = response["response"]
            trust_score = response["trustworthiness_score"]
        except KeyError as e:
            raise ValueError(f"Missing expected key in response: {e}")

        additional_data = {"trustworthiness_score": trust_score}
        if "log" in response and "explanation" in response["log"]:
            additional_data["explanation"] = response["log"]["explanation"]

        return CompletionResponse(text=text, additional_kwargs=additional_data)

    @llm_completion_callback()
    defcomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        response = self._client.prompt(prompt)
        return self._parse_response(response)

    @llm_completion_callback()
    defstream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        # Raise implementation error since TLM doesn't support native streaming
        raise NotImplementedError(
            "Streaming is not supported in TLM. Instead stream in the response from the LLM and subsequently use TLM to score its trustworthiness."
        )

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cleanlab/#llama_index.llms.cleanlab.CleanlabTLM.metadata "Permanent link")

```
metadata: 

```

Get LLM metadata.
options: members: - CleanlabTLM
