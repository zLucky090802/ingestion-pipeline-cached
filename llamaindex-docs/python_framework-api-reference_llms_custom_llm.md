# Custom llm
Bases: 
Simple abstract base class for custom LLMs.
Subclasses must implement the `__init__`, `_complete`, `_stream_complete`, and `metadata` methods.
Source code in `llama-index-core/llama_index/core/llms/custom.py`  
| 
```
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
```
 | 
```
classCustomLLM(LLM):
"""
    Simple abstract base class for custom LLMs.

    Subclasses must implement the `__init__`, `_complete`,
        `_stream_complete`, and `metadata` methods.
    """

    def__init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        assert self.messages_to_prompt is not None

        prompt = self.messages_to_prompt(messages)
        completion_response = self.complete(prompt, formatted=True, **kwargs)
        return completion_response_to_chat_response(completion_response)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        assert self.messages_to_prompt is not None

        prompt = self.messages_to_prompt(messages)
        completion_response_gen = self.stream_complete(prompt, formatted=True, **kwargs)
        return stream_completion_response_to_chat_response(completion_response_gen)

    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        return self.chat(messages, **kwargs)

    @llm_chat_callback()
    async defastream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        async defgen() -> ChatResponseAsyncGen:
            for message in self.stream_chat(messages, **kwargs):
                yield message

        # NOTE: convert generator to async generator
        return gen()

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        return self.complete(prompt, formatted=formatted, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        async defgen() -> CompletionResponseAsyncGen:
            for message in self.stream_complete(prompt, formatted=formatted, **kwargs):
                yield message

        # NOTE: convert generator to async generator
        return gen()

    @classmethod
    defclass_name(cls) -> str:
        return "custom_llm"

```
 |  
| --- | --- |
