# Yandexgpt
##  YandexGPTEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/yandexgpt/#llama_index.embeddings.yandexgpt.YandexGPTEmbedding "Permanent link")
Bases: 
A class representation for generating embeddings using the Yandex Cloud API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  `Optional[str]`  |  An API key for Yandex Cloud.  |  `None`  |  
|  `model_name`  |  The name of the model to be used for generating embeddings. The class ensures that this model is supported. Defaults to "general:embedding".  |  `'general:embedding'`  |  
|  `embed_batch_size`  |  The batch size for embedding. Defaults to DEFAULT_EMBED_BATCH_SIZE.  |  `DEFAULT_EMBED_BATCH_SIZE`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.CallbackManager\)")]`  |  Callback manager for hooks.  |  `None`  |  
Example
. code-block:: python

```
from llama_index.embeddings.yandexgpt import YandexGPTEmbedding

embeddings = YandexGPTEmbedding(
    api_key="your-api-key",
    folder_id="your-folder-id",
)

```
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-yandexgpt/llama_index/embeddings/yandexgpt/base.py`  
| 
```
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
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
```
 | 
```
classYandexGPTEmbedding(BaseEmbedding):
"""
    A class representation for generating embeddings using the Yandex Cloud API.

    Args:
      api_key (Optional[str]): An API key for Yandex Cloud.
      model_name (str): The name of the model to be used for generating embeddings.
                         The class ensures that this model is supported. Defaults to "general:embedding".
      embed_batch_size (int): The batch size for embedding. Defaults to DEFAULT_EMBED_BATCH_SIZE.
      callback_manager (Optional[CallbackManager]): Callback manager for hooks.

    Example:
        . code-block:: python

            from llama_index.embeddings.yandexgpt import YandexGPTEmbedding

            embeddings = YandexGPTEmbedding(
                api_key="your-api-key",
                folder_id="your-folder-id",


    """

    api_key: str = Field(description="The YandexGPT API key.")
    folder_id: str = Field(description="The folder id for YandexGPT API.")
    retries: int = 6
    sleep_interval: float = 0.1

    def__init__(
        self,
        api_key: Optional[str] = None,
        folder_id: Optional[str] = None,
        model_name: str = "general:embedding",
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
        if not api_key:
            raise ValueError(
                "You must provide an API key or IAM token to use YandexGPT. "
                "You can either pass it in as an argument or set it `YANDEXGPT_API_KEY`."
            )
        if not folder_id:
            raise ValueError(
                "You must provide catalog_id to use YandexGPT. "
                "You can either pass it in as an argument or set it `YANDEXGPT_CATALOG_ID`."
            )

        api_key = get_from_param_or_env("api_key", api_key, "YANDEXGPT_KEY")
        folder_id = get_from_param_or_env(
            "folder_id", folder_id, "YANDEXGPT_CATALOG_ID"
        )

        super().__init__(
            model_name=model_name,
            api_key=api_key,
            folder_id=folder_id,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            **kwargs,
        )

    def_getModelUri(self, is_document: bool = False) -> str:
"""Construct the model URI based on whether the text is a document or a query."""
        return f"emb://{self.folder_id}/text-search-{'doc'ifis_documentelse'query'}/latest"

    @classmethod
    defclass_name(cls) -> str:
"""Return the class name."""
        return "YandexGPTEmbedding"

    def_embed(self, text: str, is_document: bool = False) -> List[float]:
"""
        Embeds text using the YandexGPT Cloud API synchronously.

        Args:
          text: The text to embed.
          is_document: Whether the text is a document (True) or a query (False).

        Returns:
          A list of floats representing the embedding.

        Raises:
          YException: If an error occurs during embedding.

        """
        payload = {"modelUri": self._getModelUri(is_document), "text": text}
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}",
            "x-data-logging-enabled": "false",
        }
        try:
            for attempt in Retrying(
                stop=stop_after_attempt(self.retries),
                wait=wait_fixed(self.sleep_interval),
            ):
                with attempt:
                    response = requests.post(
                        DEFAULT_YANDEXGPT_API_BASE, json=payload, headers=header
                    )
                    response = response.json()
                    if "embedding" in response:
                        return response["embedding"]
                    raise YException(f"No embedding found, result returned: {response}")
        except RetryError:
            raise YException(
                f"Error computing embeddings after {self.retries} retries. Result returned:\n{response}"
            )

    async def_aembed(self, text: str, is_document: bool = False) -> List[float]:
"""
        Embeds text using the YandexGPT Cloud API asynchronously.

        Args:
          text: The text to embed.
          is_document: Whether the text is a document (True) or a query (False).

        Returns:
          A list of floats representing the embedding.

        Raises:
          YException: If an error occurs during embedding.

        """
        payload = {"modelUri": self._getModelUri(is_document), "text": text}
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}",
            "x-data-logging-enabled": "false",
        }
        try:
            for attempt in Retrying(
                stop=stop_after_attempt(self.retries),
                wait=wait_fixed(self.sleep_interval),
            ):
                with attempt:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            DEFAULT_YANDEXGPT_API_BASE, json=payload, headers=header
                        ) as response:
                            result = await response.json()
                            if "embedding" in result:
                                return result["embedding"]
                            raise YException(
                                f"No embedding found, result returned: {result}"
                            )
        except RetryError:
            raise YException(
                f"Error computing embeddings after {self.retries} retries. Result returned:\n{result}"
            )

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding sync."""
        return self._embed(text, is_document=True)

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get list of texts embeddings sync."""
        embeddings = []
        for text in texts:
            embeddings.append(self._embed(text, is_document=True))
            time.sleep(self.sleep_interval)
        return embeddings

    def_get_query_embedding(self, text: str) -> List[float]:
"""Get query embedding sync."""
        return self._embed(text, is_document=False)

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Get query text async."""
        return await self._aembed(text, is_document=True)

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get list of texts embeddings async."""
        embeddings = []
        for text in texts:
            embeddings.append(await self._aembed(text, is_document=True))
            await asyncio.sleep(self.sleep_interval)
        return embeddings

    async def_aget_query_embedding(self, text: str) -> List[float]:
"""Get query embedding async."""
        return await self._aembed(text, is_document=False)

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/yandexgpt/#llama_index.embeddings.yandexgpt.YandexGPTEmbedding.class_name "Permanent link")

```
class_name() -> 

```

Return the class name.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-yandexgpt/llama_index/embeddings/yandexgpt/base.py`  
| 
```
91
92
93
94
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Return the class name."""
    return "YandexGPTEmbedding"

```
 |  
| --- | --- |  
options: members: - YandexGPTEmbedding
