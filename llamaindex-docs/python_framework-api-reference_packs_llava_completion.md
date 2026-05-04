# Llava completion
##  LlavaCompletionPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/llava_completion/#llama_index.packs.llava_completion.LlavaCompletionPack "Permanent link")
Bases: 
Llava Completion pack.
Source code in `llama-index-packs/llama-index-packs-llava-completion/llama_index/packs/llava_completion/base.py`  
| 
```
 9
10
11
12
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
38
39
```
 | 
```
classLlavaCompletionPack(BaseLlamaPack):
"""Llava Completion pack."""

    def__init__(
        self,
        image_url: str,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        importos

        if not os.environ.get("REPLICATE_API_TOKEN", None):
            raise ValueError("Replicate API Token is missing or blank.")

        self.image_url = image_url

        self.llm = Replicate(
            model="yorickvp/llava-13b:2facb4a474a0462c15041b78b1ad70952ea46b5ec6ad29583c0b29dbd4249591",
            image=self.image_url,
        )

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "llm": self.llm,
            "image_url": self.image_url,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self.llm.complete(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/llava_completion/#llama_index.packs.llava_completion.LlavaCompletionPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-llava-completion/llama_index/packs/llava_completion/base.py`  
| 
```
30
31
32
33
34
35
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "llm": self.llm,
        "image_url": self.image_url,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/llava_completion/#llama_index.packs.llava_completion.LlavaCompletionPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-llava-completion/llama_index/packs/llava_completion/base.py`  
| 
```
37
38
39
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.llm.complete(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - LlavaCompletionPack
