# Textembed
##  TextEmbedEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/textembed/#llama_index.embeddings.textembed.TextEmbedEmbedding "Permanent link")
Bases: 
TextEmbedEmbedding is a class for interfacing with the TextEmbed: embedding inference server.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-textembed/llama_index/embeddings/textembed/base.py`  
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
208
209
210
211
212
213
```
 | 
```
classTextEmbedEmbedding(BaseEmbedding):
"""TextEmbedEmbedding is a class for interfacing with the TextEmbed: embedding inference server."""

    base_url: str = Field(
        default=DEFAULT_URL,
        description="Base URL for the text embeddings service.",
    )
    timeout: float = Field(
        default=60.0,
        description="Timeout in seconds for the request.",
    )
    auth_token: Optional[Union[str, Callable[[str], str]]] = Field(
        default=None,
        description="Authentication token or authentication token generating function for authenticated requests",
    )

    def__init__(
        self,
        model_name: str,
        base_url: str = DEFAULT_URL,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        timeout: float = 60.0,
        callback_manager: Optional[CallbackManager] = None,
        auth_token: Optional[Union[str, Callable[[str], str]]] = None,
    ):
"""
        Initializes the TextEmbedEmbedding object with specified parameters.

        Args:
            model_name (str): The name of the model to be used for embeddings.
            base_url (str): The base URL of the embedding service.
            embed_batch_size (int): The batch size for embedding requests.
            timeout (float): Timeout for requests.
            callback_manager (Optional[CallbackManager]): Manager for handling callbacks.
            auth_token (Optional[Union[str, Callable[[str], str]]]): Authentication token or function for generating it.

        """
        super().__init__(
            base_url=base_url,
            model_name=model_name,
            embed_batch_size=embed_batch_size,
            timeout=timeout,
            callback_manager=callback_manager,
            auth_token=auth_token,
        )

    def_call_api(self, texts: List[str]) -> List[List[float]]:
"""
        Calls the TextEmbed API to get embeddings for a list of texts.

        Args:
            texts (List[str]): A list of texts to get embeddings for.

        Returns:
            List[List[float]]: A list of embeddings for the input texts.

        Raises:
            Exception: If the API responds with a status code other than 200.

        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}" if self.auth_token else None,
        }
        json_data = {"input": texts, "model": self.model_name}
        with requests.post(
            f"{self.base_url}/embedding",
            headers=headers,
            json=json_data,
            timeout=self.timeout,
        ) as response:
            if response.status_code != 200:
                raise Exception(
                    f"TextEmbed responded with an unexpected status message "
                    f"{response.status_code}: {response.text}"
                )
            return [e["embedding"] for e in response.json()["data"]]

    async def_acall_api(self, texts: List[str]) -> List[List[float]]:
"""
        Asynchronously calls the TextEmbed API to get embeddings for a list of texts.

        Args:
            texts (List[str]): A list of texts to get embeddings for.

        Returns:
            List[List[float]]: A list of embeddings for the input texts.

        Raises:
            Exception: If the API responds with a status code other than 200.

        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}" if self.auth_token else None,
        }
        json_data = {"input": texts, "model": self.model_name}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/embedding",
                headers=headers,
                json=json_data,
                timeout=self.timeout,
            ) as response:
                if response.status != 200:
                    raise Exception(
                        f"TextEmbed responded with an unexpected status message "
                        f"{response.status}: {response.text}"
                    )
                data = await response.json()
                return [e["embedding"] for e in data["data"]]

    def_get_query_embedding(self, query: str) -> List[float]:
"""
        Gets the embedding for a single query.

        Args:
            query (str): The query to get the embedding for.

        Returns:
            List[float]: The embedding for the query.

        """
        return self._call_api([query])[0]

    def_get_text_embedding(self, text: str) -> List[float]:
"""
        Gets the embedding for a single text.

        Args:
            text (str): The text to get the embedding for.

        Returns:
            List[float]: The embedding for the text.

        """
        return self._call_api([text])[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""
        Gets the embeddings for a list of texts.

        Args:
            texts (List[str]): The texts to get the embeddings for.

        Returns:
            List[List[float]]: A list of embeddings for the input texts.

        """
        return self._call_api(texts)

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""
        Asynchronously gets the embedding for a single query.

        Args:
            query (str): The query to get the embedding for.

        Returns:
            List[float]: The embedding for the query.

        """
        return (await self._acall_api([query]))[0]

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""
        Asynchronously gets the embedding for a single text.

        Args:
            text (str): The text to get the embedding for.

        Returns:
            List[float]: The embedding for the text.

        """
        return (await self._acall_api([text]))[0]

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""
        Asynchronously gets the embeddings for a list of texts.

        Args:
            texts (List[str]): The texts to get the embeddings for.

        Returns:
            List[List[float]]: A list of embeddings for the input texts.

        """
        return await self._acall_api(texts)

```
 |  
| --- | --- |  
options: members: - TextEmbed
