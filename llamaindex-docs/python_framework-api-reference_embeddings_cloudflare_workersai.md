# Cloudflare workersai
##  CloudflareEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/cloudflare_workersai/#llama_index.embeddings.cloudflare_workersai.CloudflareEmbedding "Permanent link")
Bases: 
Cloudflare Workers AI class for generating text embeddings.
This class allows for the generation of text embeddings using Cloudflare Workers AI with the BAAI general embedding models.
Args: account_id (str): The Cloudflare Account ID. auth_token (str, Optional): The Cloudflare Auth Token. Alternatively, set up environment variable `CLOUDFLARE_AUTH_TOKEN`. model (str): The model ID for the embedding service. Cloudflare provides different models for embeddings, check https://developers.cloudflare.com/workers-ai/models/#text-embeddings. Defaults to "@cf/baai/bge-base-en-v1.5". embed_batch_size (int): The batch size for embedding generation. Cloudflare's current limit is 100 at max. Defaults to llama_index's default.
Note: Ensure you have a valid Cloudflare account and have access to the necessary AI services and models. The account ID and authorization token are sensitive details; secure them appropriately.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-cloudflare-workersai/llama_index/embeddings/cloudflare_workersai/base.py`  
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
```
 | 
```
classCloudflareEmbedding(BaseEmbedding):
"""
    Cloudflare Workers AI class for generating text embeddings.

    This class allows for the generation of text embeddings using Cloudflare Workers AI with the BAAI general embedding models.

    Args:
    account_id (str): The Cloudflare Account ID.
    auth_token (str, Optional): The Cloudflare Auth Token. Alternatively, set up environment variable `CLOUDFLARE_AUTH_TOKEN`.
    model (str): The model ID for the embedding service. Cloudflare provides different models for embeddings, check https://developers.cloudflare.com/workers-ai/models/#text-embeddings. Defaults to "@cf/baai/bge-base-en-v1.5".
    embed_batch_size (int): The batch size for embedding generation. Cloudflare's current limit is 100 at max. Defaults to llama_index's default.

    Note:
    Ensure you have a valid Cloudflare account and have access to the necessary AI services and models. The account ID and authorization token are sensitive details; secure them appropriately.

    """

    account_id: str = Field(default=None, description="The Cloudflare Account ID.")
    auth_token: str = Field(default=None, description="The Cloudflare Auth Token.")
    model: str = Field(
        default="@cf/baai/bge-base-en-v1.5",
        description="The model to use when calling Cloudflare AI API",
    )

    _session: Any = PrivateAttr()

    def__init__(
        self,
        account_id: str,
        auth_token: Optional[str] = None,
        model: str = "@cf/baai/bge-base-en-v1.5",
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            model=model,
            **kwargs,
        )
        self.account_id = account_id
        self.auth_token = get_from_param_or_env(
            "auth_token", auth_token, "CLOUDFLARE_AUTH_TOKEN", ""
        )
        self.model = model
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {self.auth_token}"})

    @classmethod
    defclass_name(cls) -> str:
        return "CloudflareEmbedding"

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self._get_text_embedding(query)

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""The asynchronous version of _get_query_embedding."""
        return await self._aget_text_embedding(query)

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._get_text_embeddings([text])[0]

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get text embedding."""
        result = await self._aget_text_embeddings([text])
        return result[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        response = self._session.post(
            API_URL_TEMPLATE.format(self.account_id, self.model), json={"text": texts}
        ).json()

        if "result" not in response:
            print(response)
            raise RuntimeError("Failed to fetch embeddings")

        return response["result"]["data"]

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Asynchronously get text embeddings."""
        importaiohttp

        async with aiohttp.ClientSession(trust_env=True) as session:
            headers = {
                "Authorization": f"Bearer {self.auth_token}",
                "Accept-Encoding": "identity",
            }
            async with session.post(
                API_URL_TEMPLATE.format(self.account_id, self.model),
                json={"text": texts},
                headers=headers,
            ) as response:
                resp = await response.json()
                if "result" not in resp:
                    raise RuntimeError("Failed to fetch embeddings asynchronously")

                return resp["result"]["data"]

```
 |  
| --- | --- |  
options: members: - CloudflareEmbedding
