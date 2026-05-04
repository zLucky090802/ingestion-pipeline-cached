# Ragatouille retriever
##  RAGatouilleRetrieverPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/ragatouille_retriever/#llama_index.packs.ragatouille_retriever.RAGatouilleRetrieverPack "Permanent link")
Bases: 
RAGatouille Retriever pack.
Source code in `llama-index-packs/llama-index-packs-ragatouille-retriever/llama_index/packs/ragatouille_retriever/base.py`  
| 
```
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
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
```
 | 
```
classRAGatouilleRetrieverPack(BaseLlamaPack):
"""RAGatouille Retriever pack."""

    def__init__(
        self,
        documents: List[Document],
        model_name: str = "colbert-ir/colbertv2.0",
        index_name: str = "my_index",
        llm: Optional[LLM] = None,
        index_path: Optional[str] = None,
        top_k: int = 10,
    ) -> None:
"""Init params."""
        self._model_name = model_name
        try:
            importragatouille  # noqa
            fromragatouilleimport RAGPretrainedModel
        except ImportError:
            raise ValueError(
                "RAGatouille is not installed. Please install it with `pip install ragatouille`."
            )

        doc_txts = [doc.get_content() for doc in documents]
        doc_ids = [doc.doc_id for doc in documents]
        doc_metadatas = [doc.metadata for doc in documents]

        # index the documents
        if index_path is None:
            RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
            index_path = RAG.index(
                index_name=index_name,
                collection=doc_txts,
                document_ids=doc_ids,
                document_metadatas=doc_metadatas,
            )
        else:
            RAG = RAGPretrainedModel.from_index(index_path)

        self.index_path = index_path

        self.custom_retriever = CustomRetriever(RAG, index_name=index_name, top_k=top_k)

        self.RAG = RAG
        self.documents = documents

        self.llm = llm or OpenAI(model="gpt-3.5-turbo")
        Settings.llm = self.llm
        self.query_engine = RetrieverQueryEngine.from_args(self.custom_retriever)

    defadd_documents(self, documents: List[Document]) -> None:
"""Add documents."""
        doc_txts = [doc.get_content() for doc in documents]
        doc_ids = [doc.doc_id for doc in documents]
        doc_metadatas = [doc.metadata for doc in documents]

        self.RAG.add_to_index(
            new_collection=doc_txts,
            new_document_ids=doc_ids,
            new_document_metadatas=doc_metadatas,
        )

    defdelete_documents(self, documents: List[Document]) -> None:
"""Delete documents."""
        doc_ids = [doc.doc_id for doc in documents]

        self.RAG.delete_from_index(document_ids=doc_ids)

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "RAG": self.RAG,
            "documents": self.documents,
            "retriever": self.custom_retriever,
            "llm": self.llm,
            "query_engine": self.query_engine,
            "index_path": self.index_path,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  add_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/ragatouille_retriever/#llama_index.packs.ragatouille_retriever.RAGatouilleRetrieverPack.add_documents "Permanent link")

```
add_documents(documents: []) -> None

```

Add documents.
Source code in `llama-index-packs/llama-index-packs-ragatouille-retriever/llama_index/packs/ragatouille_retriever/base.py`  
| 
```
 96
 97
 98
 99
100
101
102
103
104
105
106
```
 | 
```
defadd_documents(self, documents: List[Document]) -> None:
"""Add documents."""
    doc_txts = [doc.get_content() for doc in documents]
    doc_ids = [doc.doc_id for doc in documents]
    doc_metadatas = [doc.metadata for doc in documents]

    self.RAG.add_to_index(
        new_collection=doc_txts,
        new_document_ids=doc_ids,
        new_document_metadatas=doc_metadatas,
    )

```
 |  
| --- | --- |  
###  delete_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/ragatouille_retriever/#llama_index.packs.ragatouille_retriever.RAGatouilleRetrieverPack.delete_documents "Permanent link")

```
delete_documents(documents: []) -> None

```

Delete documents.
Source code in `llama-index-packs/llama-index-packs-ragatouille-retriever/llama_index/packs/ragatouille_retriever/base.py`  
| 
```
108
109
110
111
112
```
 | 
```
defdelete_documents(self, documents: List[Document]) -> None:
"""Delete documents."""
    doc_ids = [doc.doc_id for doc in documents]

    self.RAG.delete_from_index(document_ids=doc_ids)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/ragatouille_retriever/#llama_index.packs.ragatouille_retriever.RAGatouilleRetrieverPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-ragatouille-retriever/llama_index/packs/ragatouille_retriever/base.py`  
| 
```
114
115
116
117
118
119
120
121
122
123
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "RAG": self.RAG,
        "documents": self.documents,
        "retriever": self.custom_retriever,
        "llm": self.llm,
        "query_engine": self.query_engine,
        "index_path": self.index_path,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/ragatouille_retriever/#llama_index.packs.ragatouille_retriever.RAGatouilleRetrieverPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-ragatouille-retriever/llama_index/packs/ragatouille_retriever/base.py`  
| 
```
125
126
127
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - RAGatouilleRetrieverPack
