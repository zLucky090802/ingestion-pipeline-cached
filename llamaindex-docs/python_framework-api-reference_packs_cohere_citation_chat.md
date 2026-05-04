# Cohere citation chat
##  CohereCitationChatEnginePack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/cohere_citation_chat/#llama_index.packs.cohere_citation_chat.CohereCitationChatEnginePack "Permanent link")
Bases: 
Source code in `llama-index-packs/llama-index-packs-cohere-citation-chat/llama_index/packs/cohere_citation_chat/base.py`  
| 
```
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
```
 | 
```
classCohereCitationChatEnginePack(BaseLlamaPack):
    def__init__(self, documents: List[Document], cohere_api_key: str = None) -> None:
"""Init params."""
        try:
            fromllama_index.llms.cohereimport Cohere
            fromllama_index.embeddings.cohereimport CohereEmbedding
        except ImportError:
            raise ImportError(
                "Please run `pip install llama-index-llms-cohere llama-index-embeddings-cohere` "
                "to use the Cohere."
            )
        self.api_key = cohere_api_key or os.environ.get("COHERE_API_KEY")
        self.llm = Cohere(
            "command",
            api_key=self.api_key,
            temperature=0.5,
            additional_kwargs={"prompt_truncation": "AUTO"},
        )

        self.embed_model_document = CohereEmbedding(
            api_key=self.api_key,
            model_name="embed-english-v3.0",
            input_type="search_document",
        )

        self.index = VectorStoreIndexWithCitationsChat.from_documents(
            documents, llm=self.llm, embed_model=self.embed_model_document
        )

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "vector_index": self.index,
            "llm": self.llm,
        }

    defrun(self, **kwargs: Any) -> BaseChatEngine:
"""Run the pipeline."""
        # Change Cohere embed input type. See the documentation here https://docs.cohere.com/reference/embed
        self.index.set_embed_model_input_type("search_query")
        return self.index.as_chat_engine(llm=self.llm)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/cohere_citation_chat/#llama_index.packs.cohere_citation_chat.CohereCitationChatEnginePack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-cohere-citation-chat/llama_index/packs/cohere_citation_chat/base.py`  
| 
```
39
40
41
42
43
44
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "vector_index": self.index,
        "llm": self.llm,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/cohere_citation_chat/#llama_index.packs.cohere_citation_chat.CohereCitationChatEnginePack.run "Permanent link")

```
run(**kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-cohere-citation-chat/llama_index/packs/cohere_citation_chat/base.py`  
| 
```
46
47
48
49
50
```
 | 
```
defrun(self, **kwargs: Any) -> BaseChatEngine:
"""Run the pipeline."""
    # Change Cohere embed input type. See the documentation here https://docs.cohere.com/reference/embed
    self.index.set_embed_model_input_type("search_query")
    return self.index.as_chat_engine(llm=self.llm)

```
 |  
| --- | --- |  
options: members: - CohereCitationChatEnginePack
