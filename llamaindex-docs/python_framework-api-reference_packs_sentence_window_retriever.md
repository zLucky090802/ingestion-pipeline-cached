# Sentence window retriever
##  SentenceWindowRetrieverPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/sentence_window_retriever/#llama_index.packs.sentence_window_retriever.SentenceWindowRetrieverPack "Permanent link")
Bases: 
Sentence Window Retriever pack.
Build input nodes from a text file by inserting metadata, build a vector index over the input nodes, then after retrieval insert the text into the output nodes before synthesis.
Source code in `llama-index-packs/llama-index-packs-sentence-window-retriever/llama_index/packs/sentence_window_retriever/base.py`  
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
```
 | 
```
classSentenceWindowRetrieverPack(BaseLlamaPack):
"""
    Sentence Window Retriever pack.

    Build input nodes from a text file by inserting metadata,
    build a vector index over the input nodes,
    then after retrieval insert the text into the output nodes
    before synthesis.

    """

    def__init__(
        self,
        docs: List[Document] = None,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        # create the sentence window node parser w/ default settings
        self.node_parser = SentenceWindowNodeParser.from_defaults(
            window_size=3,
            window_metadata_key="window",
            original_text_metadata_key="original_text",
        )

        self.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
        self.embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-mpnet-base-v2", max_length=512
        )
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model

        # extract nodes
        nodes = self.node_parser.get_nodes_from_documents(docs)
        self.sentence_index = VectorStoreIndex(nodes)
        self.postprocessor = MetadataReplacementPostProcessor(
            target_metadata_key="window"
        )
        self.query_engine = self.sentence_index.as_query_engine(
            similarity_top_k=2,
            # the target key defaults to `window` to match the node_parser's default
            node_postprocessors=[self.postprocessor],
        )

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "sentence_index": self.sentence_index,
            "node_parser": self.node_parser,
            "postprocessor": self.postprocessor,
            "llm": self.llm,
            "embed_model": self.embed_model,
            "query_engine": self.query_engine,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/sentence_window_retriever/#llama_index.packs.sentence_window_retriever.SentenceWindowRetrieverPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-sentence-window-retriever/llama_index/packs/sentence_window_retriever/base.py`  
| 
```
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
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "sentence_index": self.sentence_index,
        "node_parser": self.node_parser,
        "postprocessor": self.postprocessor,
        "llm": self.llm,
        "embed_model": self.embed_model,
        "query_engine": self.query_engine,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/sentence_window_retriever/#llama_index.packs.sentence_window_retriever.SentenceWindowRetrieverPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-sentence-window-retriever/llama_index/packs/sentence_window_retriever/base.py`  
| 
```
70
71
72
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - SentenceWindowRetrieverPack
