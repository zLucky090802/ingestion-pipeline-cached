# Resume screener
##  ResumeScreenerPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/resume_screener/#llama_index.packs.resume_screener.ResumeScreenerPack "Permanent link")
Bases: 
Source code in `llama-index-packs/llama-index-packs-resume-screener/llama_index/packs/resume_screener/base.py`  
| 
```
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
```
 | 
```
classResumeScreenerPack(BaseLlamaPack):
    def__init__(
        self, job_description: str, criteria: List[str], llm: Optional[LLM] = None
    ) -> None:
        self.reader = PDFReader()
        llm = llm or OpenAI(model="gpt-4")
        Settings.llm = llm
        self.synthesizer = TreeSummarize(output_cls=ResumeScreenerDecision)
        criteria_str = _format_criteria_str(criteria)
        self.query = QUERY_TEMPLATE.format(
            job_description=job_description, criteria_str=criteria_str
        )

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {"reader": self.reader, "synthesizer": self.synthesizer}

    defrun(self, resume_path: str, *args: Any, **kwargs: Any) -> Any:
"""Run pack."""
        docs = self.reader.load_data(Path(resume_path))
        output = self.synthesizer.synthesize(
            query=self.query,
            nodes=[NodeWithScore(node=doc, score=1.0) for doc in docs],
        )
        return output.response

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/resume_screener/#llama_index.packs.resume_screener.ResumeScreenerPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-resume-screener/llama_index/packs/resume_screener/base.py`  
| 
```
71
72
73
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {"reader": self.reader, "synthesizer": self.synthesizer}

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/resume_screener/#llama_index.packs.resume_screener.ResumeScreenerPack.run "Permanent link")

```
run(resume_path: , *args: , **kwargs: ) -> 

```

Run pack.
Source code in `llama-index-packs/llama-index-packs-resume-screener/llama_index/packs/resume_screener/base.py`  
| 
```
75
76
77
78
79
80
81
82
```
 | 
```
defrun(self, resume_path: str, *args: Any, **kwargs: Any) -> Any:
"""Run pack."""
    docs = self.reader.load_data(Path(resume_path))
    output = self.synthesizer.synthesize(
        query=self.query,
        nodes=[NodeWithScore(node=doc, score=1.0) for doc in docs],
    )
    return output.response

```
 |  
| --- | --- |  
options: members: - ResumeScreenerPack
