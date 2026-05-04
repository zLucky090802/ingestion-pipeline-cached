# Llm rails
##  LLMRailsEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/llm_rails/#llama_index.embeddings.llm_rails.LLMRailsEmbedding "Permanent link")
Bases: 
LLMRails embedding models.
This class provides an interface to generate embeddings using a model deployed in an LLMRails cluster. It requires a model_id of the model deployed in the cluster and api key you can obtain from https://console.llmrails.com/api-keys.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-llm-rails/llama_index/embeddings/llm_rails/base.py`  
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
```
 | 
```
classLLMRailsEmbedding(BaseEmbedding):
"""
    LLMRails embedding models.

    This class provides an interface to generate embeddings using a model deployed
    in an LLMRails cluster. It requires a model_id of the model deployed in the cluster and api key you can obtain
    from https://console.llmrails.com/api-keys.

    """

    model_id: str
    api_key: str
    session: requests.Session

    @classmethod
    defclass_name(self) -> str:
        return "LLMRailsEmbedding"

    def__init__(
        self,
        api_key: str,
        model_id: str = "embedding-english-v1",  # or embedding-multi-v1
        **kwargs: Any,
    ):
        retry = Retry(
            total=3,
            connect=3,
            read=2,
            allowed_methods=["POST"],
            backoff_factor=2,
            status_forcelist=[502, 503, 504],
        )
        session = requests.Session()
        session.mount("https://api.llmrails.com", HTTPAdapter(max_retries=retry))
        session.headers = {"X-API-KEY": api_key}
        super().__init__(model_id=model_id, api_key=api_key, session=session, **kwargs)

    def_get_embedding(self, text: str) -> List[float]:
"""
        Generate an embedding for a single query text.

        Args:
            text (str): The query text to generate an embedding for.

        Returns:
            List[float]: The embedding for the input query text.

        """
        try:
            response = self.session.post(
                "https://api.llmrails.com/v1/embeddings",
                json={"input": [text], "model": self.model_id},
            )

            response.raise_for_status()
            return response.json()["data"][0]["embedding"]

        except requests.exceptions.HTTPError as e:
            logger.error(f"Error while embedding text {e}.")
            raise ValueError(f"Unable to embed given text {e}")

    async def_aget_embedding(self, text: str) -> List[float]:
"""
        Generate an embedding for a single query text.

        Args:
            text (str): The query text to generate an embedding for.

        Returns:
            List[float]: The embedding for the input query text.

        """
        try:
            importhttpx
        except ImportError:
            raise ImportError(
                "The httpx library is required to use the async version of "
                "this function. Install it with `pip install httpx`."
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.llmrails.com/v1/embeddings",
                    headers={"X-API-KEY": self.api_key},
                    json={"input": [text], "model": self.model_id},
                )

                response.raise_for_status()

            return response.json()["data"][0]["embedding"]

        except httpx._exceptions.HTTPError as e:
            logger.error(f"Error while embedding text {e}.")
            raise ValueError(f"Unable to embed given text {e}")

    def_get_text_embedding(self, text: str) -> List[float]:
        return self._get_embedding(text)

    def_get_query_embedding(self, query: str) -> List[float]:
        return self._get_embedding(query)

    async def_aget_query_embedding(self, query: str) -> List[float]:
        return await self._aget_embedding(query)

    async def_aget_text_embedding(self, query: str) -> List[float]:
        return await self._aget_embedding(query)

```
 |  
| --- | --- |  
options: members: - LLMRailsEmbedding
