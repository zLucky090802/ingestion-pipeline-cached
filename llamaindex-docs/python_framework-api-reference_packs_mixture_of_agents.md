# Mixture of agents
##  MixtureOfAgentsPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/mixture_of_agents/#llama_index.packs.mixture_of_agents.MixtureOfAgentsPack "Permanent link")
Bases: 
Source code in `llama-index-packs/llama-index-packs-mixture-of-agents/llama_index/packs/mixture_of_agents/base.py`  
| 
```
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
```
 | 
```
classMixtureOfAgentsPack(BaseLlamaPack):
    def__init__(
        self,
        llm: LLM,
        reference_llms: List[LLM],
        num_layers: int = 3,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        timeout: int = 200,
    ) -> None:
        self._wf = MixtureOfAgentWorkflow(
            llm, reference_llms, num_layers, max_tokens, temperature, timeout=timeout
        )

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "llm": self._wf.main_llm,
            "reference_llms": self._wf.reference_llms,
            "num_layers": self._wf.num_layers,
            "temperature": self._wf.temperature,
            "max_tokens": self._wf.max_tokens,
        }

    defrun(self, query_str: str, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return asyncio_run(self._wf.run(query_str=query_str))

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/mixture_of_agents/#llama_index.packs.mixture_of_agents.MixtureOfAgentsPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-mixture-of-agents/llama_index/packs/mixture_of_agents/base.py`  
| 
```
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
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "llm": self._wf.main_llm,
        "reference_llms": self._wf.reference_llms,
        "num_layers": self._wf.num_layers,
        "temperature": self._wf.temperature,
        "max_tokens": self._wf.max_tokens,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/mixture_of_agents/#llama_index.packs.mixture_of_agents.MixtureOfAgentsPack.run "Permanent link")

```
run(query_str: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-mixture-of-agents/llama_index/packs/mixture_of_agents/base.py`  
| 
```
180
181
182
```
 | 
```
defrun(self, query_str: str, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return asyncio_run(self._wf.run(query_str=query_str))

```
 |  
| --- | --- |  
options: members: - MixtureOfAgentsPack
