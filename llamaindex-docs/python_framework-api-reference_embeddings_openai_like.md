# Openai like
##  OpenAILikeEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/openai_like/#llama_index.embeddings.openai_like.OpenAILikeEmbedding "Permanent link")
Bases: 
OpenAI-Like class for embeddings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_name`  |  Model for embedding.  |  _required_  |  
|  `api_key`  |  The API key (if any) to use for the embedding API.  |  `'fake'`  |  
|  `api_base`  |  The base URL for the embedding API.  |  `None`  |  
|  `api_version`  |  The version for the embedding API.  |  `None`  |  
|  `max_retries`  |  The maximum number of retries for the embedding API.  |  
|  `timeout`  |  `float`  |  The timeout for the embedding API.  |  `60.0`  |  
|  `reuse_client`  |  `bool`  |  Whether to reuse the client for the embedding API.  |  `True`  |  
|  `callback_manager`  |   |  The callback manager for the embedding API.  |  `None`  |  
|  `default_headers`  |  `Dict[str, str]`  |  The default headers for the embedding API.  |  `None`  |  
|  `additional_kwargs`  |  `Dict[str, Any]`  |  Additional kwargs for the embedding API.  |  `None`  |  
|  `dimensions`  |  The number of dimensions for the embedding API.  |  `None`  |  
Example

```
pipinstallllama-index-embeddings-openai-like

```


```
fromllama_index.embeddings.openai_likeimport OpenAILikeEmbedding

embedding = OpenAILikeEmbedding(
    model_name="my-model-name",
    api_base="http://localhost:1234/v1",
    api_key="fake",
    embed_batch_size=10,
)

```

Source code in `llama-index-integrations/embeddings/llama-index-embeddings-openai-like/llama_index/embeddings/openai_like/base.py`  
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
```
 | 
```
classOpenAILikeEmbedding(OpenAIEmbedding):
"""
    OpenAI-Like class for embeddings.

    Args:
        model_name (str):
            Model for embedding.
        api_key (str):
            The API key (if any) to use for the embedding API.
        api_base (str):
            The base URL for the embedding API.
        api_version (str):
            The version for the embedding API.
        max_retries (int):
            The maximum number of retries for the embedding API.
        timeout (float):
            The timeout for the embedding API.
        reuse_client (bool):
            Whether to reuse the client for the embedding API.
        callback_manager (CallbackManager):
            The callback manager for the embedding API.
        default_headers (Dict[str, str]):
            The default headers for the embedding API.
        additional_kwargs (Dict[str, Any]):
            Additional kwargs for the embedding API.
        dimensions (int):
            The number of dimensions for the embedding API.

    Example:
        ```bash
        pip install llama-index-embeddings-openai-like
        ```

        ```python
        from llama_index.embeddings.openai_like import OpenAILikeEmbedding

        embedding = OpenAILikeEmbedding(
            model_name="my-model-name",
            api_base="http://localhost:1234/v1",
            api_key="fake",
            embed_batch_size=10,

        ```

    """

    def__init__(
        self,
        model_name: str,
        embed_batch_size: int = 10,
        dimensions: Optional[int] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        api_key: str = "fake",
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        max_retries: int = 10,
        timeout: float = 60.0,
        reuse_client: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        default_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        async_http_client: Optional[httpx.AsyncClient] = None,
        num_workers: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        # ensure model is not passed in kwargs, will cause error in parent class
        if "model" in kwargs:
            raise ValueError(
                "Use `model_name` instead of `model` to initialize OpenAILikeEmbedding"
            )

        super().__init__(
            model_name=model_name,
            embed_batch_size=embed_batch_size,
            dimensions=dimensions,
            callback_manager=callback_manager,
            additional_kwargs=additional_kwargs,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            max_retries=max_retries,
            reuse_client=reuse_client,
            timeout=timeout,
            default_headers=default_headers,
            http_client=http_client,
            async_http_client=async_http_client,
            num_workers=num_workers,
            **kwargs,
        )

```
 |  
| --- | --- |  
options: members: - OpenAILikeEmbedding
