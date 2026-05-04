# Baseten
##  BasetenEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/baseten/#llama_index.embeddings.baseten.BasetenEmbedding "Permanent link")
Bases: 
Baseten class for embeddings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_id`  |  The Baseten model ID (e.g., "03y7n6e3").  |  _required_  |  
|  `api_key`  |  `Optional[str]`  |  The Baseten API key.  |  `None`  |  
|  `embed_batch_size`  |  The batch size for embedding calls.  |  `DEFAULT_EMBED_BATCH_SIZE`  |  
|  `additional_kwargs`  |  `Optional[Dict[str, Any]]`  |  Additional kwargs for the API.  |  `None`  |  
|  `max_retries`  |  The maximum number of retries to make.  |  
|  `timeout`  |  `float`  |  Timeout for each request.  |  `60.0`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.CallbackManager\)")]`  |  Callback manager for logging.  |  `None`  |  
|  `default_headers`  |  `Optional[Dict[str, str]]`  |  Default headers for API requests.  |  `None`  |  
Examples:

```
fromllama_index.embeddings.basetenimport BasetenEmbedding

# Using dedicated endpoint
# You can find the model_id by in the Baseten dashboard here: https://app.baseten.co/overview
embed_model = BasetenEmbedding(
    model_id="MODEL_ID,
    api_key="YOUR_API_KEY",
)

# Single embedding
embedding = embed_model.get_text_embedding("Hello, world!")

# Batch embeddings
embeddings = embed_model.get_text_embedding_batch([
    "Hello, world!",
    "Goodbye, world!"
])

```

Source code in `llama-index-integrations/embeddings/llama-index-embeddings-baseten/llama_index/embeddings/baseten/base.py`  
| 
```
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
 99
100
```
 | 
```
classBasetenEmbedding(OpenAIEmbedding):
"""
    Baseten class for embeddings.

    Args:
        model_id (str): The Baseten model ID (e.g., "03y7n6e3").
        api_key (Optional[str]): The Baseten API key.
        embed_batch_size (int): The batch size for embedding calls.
        additional_kwargs (Optional[Dict[str, Any]]): Additional kwargs for the API.
        max_retries (int): The maximum number of retries to make.
        timeout (float): Timeout for each request.
        callback_manager (Optional[CallbackManager]): Callback manager for logging.
        default_headers (Optional[Dict[str, str]]): Default headers for API requests.

    Examples:
        ```python
        from llama_index.embeddings.baseten import BasetenEmbedding

        # Using dedicated endpoint
        # You can find the model_id by in the Baseten dashboard here: https://app.baseten.co/overview
        embed_model = BasetenEmbedding(
            model_id="MODEL_ID,
            api_key="YOUR_API_KEY",


        # Single embedding
        embedding = embed_model.get_text_embedding("Hello, world!")

        # Batch embeddings
        embeddings = embed_model.get_text_embedding_batch([
            "Hello, world!",
            "Goodbye, world!"

        ```

    """

    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the OpenAI API."
    )

    api_key: str = Field(description="The Baseten API key.")
    api_base: str = Field(default="", description="The base URL for Baseten API.")
    api_version: str = Field(default="", description="The version for OpenAI API.")

    def__init__(
        self,
        model_id: str,
        dimensions: Optional[int] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        max_retries: int = 10,
        timeout: float = 60.0,
        reuse_client: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        default_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        **kwargs: Any,
    ) -> None:
        # Use the dedicated endpoint URL format
        api_base = DEFAULT_API_BASE.format(model_id=model_id)
        api_key = get_from_param_or_env("api_key", api_key, "BASETEN_API_KEY")

        super().__init__(
            model_name=model_id,
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
        return "BasetenEmbedding"

```
 |  
| --- | --- |  
options: members: - BasetenEmbedding
