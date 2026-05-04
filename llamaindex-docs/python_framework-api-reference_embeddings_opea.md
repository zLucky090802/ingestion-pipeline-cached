# Opea
##  OPEAEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/opea/#llama_index.embeddings.opea.OPEAEmbedding "Permanent link")
Bases: 
OPEA class for embeddings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  Model for embedding.  |  _required_  |  
|  `api_base`  |  The base URL for OPEA Embeddings microservice.  |  _required_  |  
|  `additional_kwargs`  |  `Dict[str, Any]`  |  Additional kwargs for the OpenAI API.  |  `None`  |  
Examples:
`pip install llama-index-embeddings-opea`

```
fromllama_index.embeddings.opeaimport OPEAEmbedding

embed_model = OPEAEmbedding(
    model_name="...",
    api_base="http://localhost:8080",
)

```

Source code in `llama-index-integrations/embeddings/llama-index-embeddings-opea/llama_index/embeddings/opea/base.py`  
| 
```
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
```
 | 
```
classOPEAEmbedding(OpenAIEmbedding):
"""
    OPEA class for embeddings.

    Args:
        model (str): Model for embedding.
        api_base (str): The base URL for OPEA Embeddings microservice.
        additional_kwargs (Dict[str, Any]): Additional kwargs for the OpenAI API.

    Examples:
        `pip install llama-index-embeddings-opea`

        ```python
        from llama_index.embeddings.opea import OPEAEmbedding

        embed_model = OPEAEmbedding(
            model_name="...",
            api_base="http://localhost:8080",

        ```

    """

    def__init__(
        self,
        model_name: str,
        api_base: str,
        dimensions: Optional[int] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 10,
        timeout: float = 60.0,
        reuse_client: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        default_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        api_key: Optional[str] = "fake",
        **kwargs: Any,
    ) -> None:
        super().__init__(
            model_name=model_name,
            dimensions=dimensions,
            embed_batch_size=embed_batch_size,
            additional_kwargs=additional_kwargs,
            api_key=api_key,
            api_base=api_base,
            max_retries=max_retries,
            timeout=timeout,
            reuse_client=reuse_client,
            callback_manager=callback_manager,
            default_headers=default_headers,
            http_client=http_client,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "OPEAEmbedding"

```
 |  
| --- | --- |  
options: members: - OPEAEmbedding
