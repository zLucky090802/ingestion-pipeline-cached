# Clip
##  ClipEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/clip/#llama_index.embeddings.clip.ClipEmbedding "Permanent link")
Bases: 
CLIP embedding models for encoding text and image for Multi-Modal purpose.
This class provides an interface to generate embeddings using a model deployed in OpenAI CLIP. At the initialization it requires a model name of CLIP.
Note
Requires `clip` package to be available in the PYTHONPATH. It can be installed with `pip install git+https://github.com/openai/CLIP.git`.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-clip/llama_index/embeddings/clip/base.py`  
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
```
 | 
```
classClipEmbedding(MultiModalEmbedding):
"""
    CLIP embedding models for encoding text and image for Multi-Modal purpose.

    This class provides an interface to generate embeddings using a model
    deployed in OpenAI CLIP. At the initialization it requires a model name
    of CLIP.

    Note:
        Requires `clip` package to be available in the PYTHONPATH. It can be installed with
        `pip install git+https://github.com/openai/CLIP.git`.

    """

    embed_batch_size: int = Field(default=DEFAULT_EMBED_BATCH_SIZE, gt=0)

    _clip: Any = PrivateAttr()
    _model: Any = PrivateAttr()
    _preprocess: Any = PrivateAttr()
    _device: Any = PrivateAttr()

    @classmethod
    defclass_name(cls) -> str:
        return "ClipEmbedding"

    def__init__(
        self,
        *,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        model_name: str = DEFAULT_CLIP_MODEL,
        **kwargs: Any,
    ):
"""
        Initializes the ClipEmbedding class.

        During the initialization the `clip` package is imported.

        Args:
            embed_batch_size (int, optional): The batch size for embedding generation. Defaults to 10,
                must be > 0 and <= 100.
            model_name (str): The model name of Clip model.

        Raises:
            ImportError: If the `clip` package is not available in the PYTHONPATH.
            ValueError: If the model cannot be fetched from Open AI. or if the embed_batch_size
                is not in the range (0, 100].

        """
        if embed_batch_size <= 0:
            raise ValueError(f"Embed batch size {embed_batch_size}  must be > 0.")

        try:
            importclip
            importtorch
        except ImportError:
            raise ImportError(
                "ClipEmbedding requires `pip install git+https://github.com/openai/CLIP.git` and torch."
            )

        super().__init__(
            embed_batch_size=embed_batch_size, model_name=model_name, **kwargs
        )

        try:
            self._device = "cuda" if torch.cuda.is_available() else "cpu"
            self._model, self._preprocess = clip.load(
                self.model_name, device=self._device
            )

        except Exception as e:
            logger.error("Error while loading clip model.")
            raise ValueError("Unable to fetch the requested embeddings model") frome

    # TEXT EMBEDDINGS

    async def_aget_query_embedding(self, query: str) -> Embedding:
        return self._get_query_embedding(query)

    def_get_text_embedding(self, text: str) -> Embedding:
        return self._get_text_embeddings([text])[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[Embedding]:
        results = []
        for text in texts:
            try:
                importclip
            except ImportError:
                raise ImportError(
                    "ClipEmbedding requires `pip install git+https://github.com/openai/CLIP.git` and torch."
                )
            text_embedding = self._model.encode_text(
                clip.tokenize(text).to(self._device)
            )
            results.append(text_embedding.tolist()[0])

        return results

    def_get_query_embedding(self, query: str) -> Embedding:
        return self._get_text_embedding(query)

    # IMAGE EMBEDDINGS

    async def_aget_image_embedding(self, img_file_path: ImageType) -> Embedding:
        return self._get_image_embedding(img_file_path)

    def_get_image_embedding(self, img_file_path: ImageType) -> Embedding:
        importtorch

        with torch.no_grad():
            image = (
                self._preprocess(Image.open(img_file_path))
                .unsqueeze(0)
                .to(self._device)
            )
            return self._model.encode_image(image).tolist()[0]

```
 |  
| --- | --- |  
options: members: - ClipEmbedding
