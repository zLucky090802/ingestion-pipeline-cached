# Zephyr query engine
##  ZephyrQueryEnginePack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/zephyr_query_engine/#llama_index.packs.zephyr_query_engine.ZephyrQueryEnginePack "Permanent link")
Bases: 
Source code in `llama-index-packs/llama-index-packs-zephyr-query-engine/llama_index/packs/zephyr_query_engine/base.py`  
| 
```
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
```
 | 
```
classZephyrQueryEnginePack(BaseLlamaPack):
    def__init__(self, documents: List[Document]) -> None:
"""Init params."""
        try:
            importtorch
            fromtransformersimport BitsAndBytesConfig
        except ImportError:
            raise ImportError(
                "Dependencies missing, run "
                "`pip install torch transformers accelerate bitsandbytes`"
            )

        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )

        try:
            llm = HuggingFaceLLM(
                model_name="HuggingFaceH4/zephyr-7b-beta",
                tokenizer_name="HuggingFaceH4/zephyr-7b-beta",
                query_wrapper_prompt=PromptTemplate(
                    "<|system|>\n</s>\n<|user|>\n{query_str}</s>\n<|assistant|>\n"
                ),
                context_window=3900,
                max_new_tokens=256,
                model_kwargs={"quantization_config": quantization_config},
                generate_kwargs={
                    "do_sample": True,
                    "temperature": 0.7,
                    "top_k": 50,
                    "top_p": 0.95,
                },
                device_map="auto",
            )
        except Exception:
            print(
                "Failed to load and quantize model, likely due to CUDA being missing. "
                "Loading full precision model instead."
            )
            llm = HuggingFaceLLM(
                model_name="HuggingFaceH4/zephyr-7b-beta",
                tokenizer_name="HuggingFaceH4/zephyr-7b-beta",
                query_wrapper_prompt=PromptTemplate(
                    "<|system|>\n</s>\n<|user|>\n{query_str}</s>\n<|assistant|>\n"
                ),
                context_window=3900,
                max_new_tokens=256,
                generate_kwargs={
                    "do_sample": True,
                    "temperature": 0.7,
                    "top_k": 50,
                    "top_p": 0.95,
                },
                device_map="auto",
            )

        # set tokenizer for proper token counting
        fromtransformersimport AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-beta")
        set_global_tokenizer(tokenizer.encode)

        Settings.llm = llm
        Settings.embed_model = "local:BAAI/bge-base-en-v1.5"

        self.llm = llm
        self.index = VectorStoreIndex.from_documents(documents)

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {"llm": self.llm, "index": self.index}

    defrun(self, query_str: str, **kwargs: Any) -> Any:
"""Run the pipeline."""
        query_engine = self.index.as_query_engine(**kwargs)
        return query_engine.query(query_str)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/zephyr_query_engine/#llama_index.packs.zephyr_query_engine.ZephyrQueryEnginePack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-zephyr-query-engine/llama_index/packs/zephyr_query_engine/base.py`  
| 
```
83
84
85
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {"llm": self.llm, "index": self.index}

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/zephyr_query_engine/#llama_index.packs.zephyr_query_engine.ZephyrQueryEnginePack.run "Permanent link")

```
run(query_str: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-zephyr-query-engine/llama_index/packs/zephyr_query_engine/base.py`  
| 
```
87
88
89
90
```
 | 
```
defrun(self, query_str: str, **kwargs: Any) -> Any:
"""Run the pipeline."""
    query_engine = self.index.as_query_engine(**kwargs)
    return query_engine.query(query_str)

```
 |  
| --- | --- |  
options: members: - ZephyrQueryEnginePack
