# Premai
##  PremAIEmbeddings [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/premai/#llama_index.embeddings.premai.PremAIEmbeddings "Permanent link")
Bases: 
Class for PremAI embeddings.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-premai/llama_index/embeddings/premai/base.py`  
| 
```
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
```
 | 
```
classPremAIEmbeddings(BaseEmbedding):
"""Class for PremAI embeddings."""

    project_id: int = Field(
        description=(
            "The project ID in which the experiments or deployments are carried out. can find all your projects here: https://app.premai.io/projects/"
        )
    )
    premai_api_key: Optional[str] = Field(
        description="Prem AI API Key. Get it here: https://app.premai.io/api_keys/"
    )

    model_name: str = Field(
        description=("The Embedding model to choose from"),
    )

    # Instance variables initialized via Pydantic's mechanism
    _premai_client: "Prem" = PrivateAttr()

    def__init__(
        self,
        project_id: int,
        model_name: str,
        premai_api_key: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ):
        api_key = get_from_param_or_env("api_key", premai_api_key, "PREMAI_API_KEY", "")

        if not api_key:
            raise ValueError(
                "You must provide an API key to use PremAI. "
                "You can either pass it in as an argument or set it `PREMAI_API_KEY`."
            )
        super().__init__(
            project_id=project_id,
            model_name=model_name,
            callback_manager=callback_manager,
            **kwargs,
        )

        self._premai_client = Prem(api_key=api_key)

    @classmethod
    defclass_name(cls) -> str:
        return "PremAIEmbeddings"

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        embedding_response = self._premai_client.embeddings.create(
            project_id=self.project_id, model=self.model_name, input=query
        )
        return embedding_response.data[0].embedding

    async def_aget_query_embedding(self, query: str) -> List[float]:
        raise NotImplementedError("Async calls are not available in this version.")

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        embedding_response = self._premai_client.embeddings.create(
            project_id=self.project_id, model=self.model_name, input=[text]
        )
        return embedding_response.data[0].embedding

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        embeddings = self._premai_client.embeddings.create(
            model=self.model_name, project_id=self.project_id, input=texts
        ).data
        return [embedding.embedding for embedding in embeddings]

```
 |  
| --- | --- |  
options: members: - PremAIEmbeddings
