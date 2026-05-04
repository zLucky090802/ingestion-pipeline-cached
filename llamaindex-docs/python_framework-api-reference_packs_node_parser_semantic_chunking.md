# Node parser semantic chunking
##  SemanticChunkingQueryEnginePack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/node_parser_semantic_chunking/#llama_index.packs.node_parser_semantic_chunking.SemanticChunkingQueryEnginePack "Permanent link")
Bases: 
Semantic Chunking Query Engine Pack.
Takes in a list of documents, parses it with semantic embedding chunker, and runs a query engine on the resulting chunks.
Source code in `llama-index-packs/llama-index-packs-node-parser-semantic-chunking/llama_index/packs/node_parser_semantic_chunking/base.py`  
| 
```
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
```
 | 
```
classSemanticChunkingQueryEnginePack(BaseLlamaPack):
"""
    Semantic Chunking Query Engine Pack.

    Takes in a list of documents, parses it with semantic embedding chunker,
    and runs a query engine on the resulting chunks.

    """

    def__init__(
        self,
        documents: List[Document],
        buffer_size: int = 1,
        breakpoint_percentile_threshold: float = 95.0,
    ) -> None:
"""Init params."""
        self.embed_model = OpenAIEmbedding()
        self.splitter = SemanticChunker(
            buffer_size=buffer_size,
            breakpoint_percentile_threshold=breakpoint_percentile_threshold,
            embed_model=self.embed_model,
        )

        nodes = self.splitter.get_nodes_from_documents(documents)
        self.vector_index = VectorStoreIndex(nodes)
        self.query_engine = self.vector_index.as_query_engine()

    defget_modules(self) -> Dict[str, Any]:
        return {
            "vector_index": self.vector_index,
            "query_engine": self.query_engine,
            "splitter": self.splitter,
            "embed_model": self.embed_model,
        }

    defrun(self, query: str) -> Any:
"""Run the pipeline."""
        return self.query_engine.query(query)

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/node_parser_semantic_chunking/#llama_index.packs.node_parser_semantic_chunking.SemanticChunkingQueryEnginePack.run "Permanent link")

```
run(query: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-node-parser-semantic-chunking/llama_index/packs/node_parser_semantic_chunking/base.py`  
| 
```
240
241
242
```
 | 
```
defrun(self, query: str) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(query)

```
 |  
| --- | --- |  
options: members: - SemanticChunkingQueryEnginePack
