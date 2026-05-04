# Index
##  SubQuestion [#](https://developers.llamaindex.ai/python/framework-api-reference/question_gen/#llama_index.core.question_gen.types.SubQuestion "Permanent link")
Bases: `BaseModel`
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sub_question`  |  _required_  |  
|  `tool_name`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/question_gen/types.py`  
| 
```
11
12
13
```
 | 
```
classSubQuestion(BaseModel):
    sub_question: str
    tool_name: str

```
 |  
| --- | --- |  
##  SubQuestionList [#](https://developers.llamaindex.ai/python/framework-api-reference/question_gen/#llama_index.core.question_gen.types.SubQuestionList "Permanent link")
Bases: `BaseModel`
A pydantic object wrapping a list of sub-questions.
This is mostly used to make getting a json schema easier.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `items`  |  `List[SubQuestion[](https://developers.llamaindex.ai/python/framework-api-reference/question_gen/#llama_index.core.question_gen.types.SubQuestion "SubQuestion \(llama_index.core.question_gen.types.SubQuestion\)")]`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/question_gen/types.py`  
| 
```
16
17
18
19
20
21
22
23
```
 | 
```
classSubQuestionList(BaseModel):
"""
    A pydantic object wrapping a list of sub-questions.

    This is mostly used to make getting a json schema easier.
    """

    items: List[SubQuestion]

```
 |  
| --- | --- |  
##  BaseQuestionGenerator [#](https://developers.llamaindex.ai/python/framework-api-reference/question_gen/#llama_index.core.question_gen.types.BaseQuestionGenerator "Permanent link")
Bases: `PromptMixin`, `DispatcherSpanMixin`
Source code in `llama-index-core/llama_index/core/question_gen/types.py`  
| 
```
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
```
 | 
```
classBaseQuestionGenerator(PromptMixin, DispatcherSpanMixin):
    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt modules."""
        return {}

    @abstractmethod
    defgenerate(
        self, tools: Sequence[ToolMetadata], query: QueryBundle
    ) -> List[SubQuestion]:
        pass

    @abstractmethod
    async defagenerate(
        self, tools: Sequence[ToolMetadata], query: QueryBundle
    ) -> List[SubQuestion]:
        pass

```
 |  
| --- | --- |  
options: members: - BaseQuestionGenerator - SubQuestionList - SubQuestion
