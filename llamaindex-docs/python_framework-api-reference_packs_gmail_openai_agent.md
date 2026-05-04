# Gmail openai agent
##  GmailOpenAIAgentPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/gmail_openai_agent/#llama_index.packs.gmail_openai_agent.GmailOpenAIAgentPack "Permanent link")
Bases: 
Source code in `llama-index-packs/llama-index-packs-gmail-openai-agent/llama_index/packs/gmail_openai_agent/base.py`  
| 
```
13
14
15
16
17
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
```
 | 
```
classGmailOpenAIAgentPack(BaseLlamaPack):
    def__init__(self, gmail_tool_kwargs: Dict[str, Any]) -> None:
"""Init params."""
        try:
            fromllama_index.tools.googleimport GmailToolSpec
        except ImportError:
            raise ImportError("llama_hub not installed.")

        self.tool_spec = GmailToolSpec(**gmail_tool_kwargs)
        self.agent = FunctionAgent(
            tools=self.tool_spec.to_tool_list(),
            llm=OpenAI(model="gpt-4.1"),
        )

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {"gmail_tool": self.tool_spec, "agent": self.agent}

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return asyncio_run(self.arun(*args, **kwargs))

    async defarun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline asynchronously."""
        return await self.agent.run(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/gmail_openai_agent/#llama_index.packs.gmail_openai_agent.GmailOpenAIAgentPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-gmail-openai-agent/llama_index/packs/gmail_openai_agent/base.py`  
| 
```
27
28
29
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {"gmail_tool": self.tool_spec, "agent": self.agent}

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/gmail_openai_agent/#llama_index.packs.gmail_openai_agent.GmailOpenAIAgentPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-gmail-openai-agent/llama_index/packs/gmail_openai_agent/base.py`  
| 
```
31
32
33
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return asyncio_run(self.arun(*args, **kwargs))

```
 |  
| --- | --- |  
###  arun [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/gmail_openai_agent/#llama_index.packs.gmail_openai_agent.GmailOpenAIAgentPack.arun "Permanent link")

```
arun(*args: , **kwargs: ) -> 

```

Run the pipeline asynchronously.
Source code in `llama-index-packs/llama-index-packs-gmail-openai-agent/llama_index/packs/gmail_openai_agent/base.py`  
| 
```
35
36
37
```
 | 
```
async defarun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline asynchronously."""
    return await self.agent.run(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - GmailOpenAIAgentPack
