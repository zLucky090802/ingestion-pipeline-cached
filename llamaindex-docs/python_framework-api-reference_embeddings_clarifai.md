# Clarifai
##  ClarifaiEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/clarifai/#llama_index.embeddings.clarifai.ClarifaiEmbedding "Permanent link")
Bases: 
Clarifai embeddings class.
Clarifai uses Personal Access Tokens(PAT) to validate requests. You can create and manage PATs under your Clarifai account security settings. Export your PAT as an environment variable by running `export CLARIFAI_PAT={PAT}`
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-clarifai/llama_index/embeddings/clarifai/base.py`  
| 
```
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
128
129
130
131
132
133
134
135
136
137
138
139
```
 | 
```
classClarifaiEmbedding(BaseEmbedding):
"""
    Clarifai embeddings class.

    Clarifai uses Personal Access Tokens(PAT) to validate requests.
    You can create and manage PATs under your Clarifai account security settings.
    Export your PAT as an environment variable by running `export CLARIFAI_PAT={PAT}`
    """

    model_url: Optional[str] = Field(
        description=f"Full URL of the model. e.g. `{EXAMPLE_URL}`"
    )
    model_id: Optional[str] = Field(description="Model ID.")
    model_version_id: Optional[str] = Field(description="Model Version ID.")
    app_id: Optional[str] = Field(description="Clarifai application ID of the model.")
    user_id: Optional[str] = Field(description="Clarifai user ID of the model.")
    pat: Optional[str] = Field(
        description="Personal Access Tokens(PAT) to validate requests."
    )

    _model: Any = PrivateAttr()

    def__init__(
        self,
        model_name: Optional[str] = None,
        model_url: Optional[str] = None,
        model_version_id: Optional[str] = "",
        app_id: Optional[str] = None,
        user_id: Optional[str] = None,
        pat: Optional[str] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
    ):
        embed_batch_size = min(128, embed_batch_size)

        if pat is None and os.environ.get("CLARIFAI_PAT") is not None:
            pat = os.environ.get("CLARIFAI_PAT")

        if not pat and os.environ.get("CLARIFAI_PAT") is None:
            raise ValueError(
                "Set `CLARIFAI_PAT` as env variable or pass `pat` as constructor argument"
            )

        if model_url is not None and model_name is not None:
            raise ValueError("You can only specify one of model_url or model_name.")
        if model_url is None and model_name is None:
            raise ValueError("You must specify one of model_url or model_name.")

        if model_name is not None:
            if app_id is None or user_id is None:
                raise ValueError(
                    f"Missing one app ID or user ID of the model: {app_id=}, {user_id=}"
                )
            else:
                model = Model(
                    user_id=user_id,
                    app_id=app_id,
                    model_id=model_name,
                    model_version={"id": model_version_id},
                    pat=pat,
                )

        if model_url is not None:
            model = Model(model_url, pat=pat)
            model_name = model.id

        super().__init__(
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            model_name=model_name,
        )
        self._model = model

    @classmethod
    defclass_name(cls) -> str:
        return "ClarifaiEmbedding"

    def_embed(self, sentences: List[str]) -> List[List[float]]:
"""Embed sentences."""
        try:
            fromclarifai.client.inputimport Inputs
        except ImportError:
            raise ImportError("ClarifaiEmbedding requires `pip install clarifai`.")

        embeddings = []
        try:
            for i in range(0, len(sentences), self.embed_batch_size):
                batch = sentences[i : i + self.embed_batch_size]
                input_batch = [
                    Inputs.get_text_input(input_id=str(id), raw_text=inp)
                    for id, inp in enumerate(batch)
                ]
                predict_response = self._model.predict(input_batch)
                embeddings.extend(
                    [
                        list(output.data.embeddings[0].vector)
                        for output in predict_response.outputs
                    ]
                )
        except Exception as e:
            logger.error(f"Predict failed, exception: {e}")

        return embeddings

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self._embed([query])[0]

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""Get query embedding async."""
        return self._get_query_embedding(query)

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Get text embedding async."""
        return self._get_text_embedding(text)

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._embed([text])[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        return self._embed(texts)

```
 |  
| --- | --- |  
options: members: - ClarifaiEmbedding
