# Self discover
##  SelfDiscoverPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/self_discover/#llama_index.packs.self_discover.SelfDiscoverPack "Permanent link")
Bases: 
Self-Discover Pack.
Source code in `llama-index-packs/llama-index-packs-self-discover/llama_index/packs/self_discover/base.py`  
| 
```
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
192
193
194
195
196
197
```
 | 
```
classSelfDiscoverPack(BaseLlamaPack):
"""Self-Discover Pack."""

    def__init__(
        self,
        llm: Optional[Any] = None,
        verbose: bool = True,
    ) -> None:
"""Init params."""
        self.llm = llm or OpenAI(model="gpt-3.5-turbo")
        self.reasoning_modules = _REASONING_MODULES
        self.verbose = verbose

        self.workflow = SelfDiscoverWorkflow(verbose=verbose)

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "llm": self.llm,
            "reasoning_modules": self.reasoning_modules,
            "workflow": self.workflow,
        }

    defrun(self, task):
"""Runs the configured pipeline for a specified task and reasoning modules."""
        return asyncio_run(self.workflow.run(task=task, llm=self.llm))

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/self_discover/#llama_index.packs.self_discover.SelfDiscoverPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-self-discover/llama_index/packs/self_discover/base.py`  
| 
```
187
188
189
190
191
192
193
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "llm": self.llm,
        "reasoning_modules": self.reasoning_modules,
        "workflow": self.workflow,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/self_discover/#llama_index.packs.self_discover.SelfDiscoverPack.run "Permanent link")

```
run(task)

```

Runs the configured pipeline for a specified task and reasoning modules.
Source code in `llama-index-packs/llama-index-packs-self-discover/llama_index/packs/self_discover/base.py`  
| 
```
195
196
197
```
 | 
```
defrun(self, task):
"""Runs the configured pipeline for a specified task and reasoning modules."""
    return asyncio_run(self.workflow.run(task=task, llm=self.llm))

```
 |  
| --- | --- |  
options: members: - SelfDiscoverPack
