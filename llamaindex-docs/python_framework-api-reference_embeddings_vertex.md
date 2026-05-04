# Vertex
##  VertexEmbeddingMode [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/vertex/#llama_index.embeddings.vertex.VertexEmbeddingMode "Permanent link")
Bases: `str`, `Enum`
VertexAI embedding mode.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `DEFAULT_MODE`  |  The default embedding mode, for older models before August 2023, that does not support task_type  |  
| `CLASSIFICATION_MODE`  |  Optimizes embeddings for classification tasks.  |  
| `CLUSTERING_MODE`  |  Optimizes embeddings for clustering tasks.  |  
| `SEMANTIC_SIMILARITY_MODE`  |  Optimizes embeddings for tasks that require assessments of semantic similarity.  |  
| `RETRIEVAL_MODE`  |  Optimizes embeddings for retrieval tasks, including search and document retrieval.  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-vertex/llama_index/embeddings/vertex/base.py`  
| 
```
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
```
 | 
```
@deprecated.deprecated(
    reason=(
        "Should use `llama-index-embeddings-google-genai` instead, using Google's latest unified SDK. "
        "See: https://docs.llamaindex.ai/en/stable/examples/embeddings/google_genai/"
    )
)
classVertexEmbeddingMode(str, Enum):
"""
    VertexAI embedding mode.

    Attributes:
        DEFAULT_MODE (str): The default embedding mode, for older models before August 2023,
                            that does not support task_type
        CLASSIFICATION_MODE (str): Optimizes embeddings for classification tasks.
        CLUSTERING_MODE (str): Optimizes embeddings for clustering tasks.
        SEMANTIC_SIMILARITY_MODE (str): Optimizes embeddings for tasks that require assessments of semantic similarity.
        RETRIEVAL_MODE (str): Optimizes embeddings for retrieval tasks, including search and document retrieval.

    """

    DEFAULT_MODE = "default"
    CLASSIFICATION_MODE = "classification"
    CLUSTERING_MODE = "clustering"
    SEMANTIC_SIMILARITY_MODE = "similarity"
    RETRIEVAL_MODE = "retrieval"

```
 |  
| --- | --- |  
options: members: - VertexMultiModalEmbedding - VertexTextEmbedding
