# Fireworks
##  FireworksEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/fireworks/#llama_index.embeddings.fireworks.FireworksEmbedding "Permanent link")
Bases: 
Fireworks class for embeddings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  Model for embedding. Defaults to "nomic-ai/nomic-embed-text-v1.5"  |  _required_  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-fireworks/llama_index/embeddings/fireworks/base.py`  
| 
```
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
```
 | 
```
classFireworksEmbedding(OpenAIEmbedding):
"""
    Fireworks class for embeddings.

    Args:
        model (str): Model for embedding.
            Defaults to "nomic-ai/nomic-embed-text-v1.5"

    """

    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the Fireworks API."
    )

    api_key: str = Field(description="The Fireworks API key.")
    api_base: str = Field(description="The base URL for Fireworks API.")
    api_version: str = Field(description="The version for Fireworks API.")

    def__init__(
        self,
        model_name: str = DEFAULT_MODEL,
        dimensions: Optional[int] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = DEFAULT_API_BASE,
        api_version: Optional[str] = None,
        max_retries: int = 10,
        timeout: float = 60.0,
        reuse_client: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        default_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        **kwargs: Any,
    ) -> None:
        api_key, api_base, api_version = resolve_fireworks_credentials(
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
        )

        super().__init__(
            model_name=model_name,
            dimensions=dimensions,
            embed_batch_size=embed_batch_size,
            additional_kwargs=additional_kwargs,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
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
        return "FireworksEmbedding"

```
 |  
| --- | --- |  
options: members: - FireworksEmbedding
