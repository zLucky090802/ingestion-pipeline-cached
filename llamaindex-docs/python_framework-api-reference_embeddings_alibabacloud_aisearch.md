# Alibabacloud aisearch
##  AlibabaCloudAISearchEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/alibabacloud_aisearch/#llama_index.embeddings.alibabacloud_aisearch.AlibabaCloudAISearchEmbedding "Permanent link")
Bases: 
For further details, please visit `https://help.aliyun.com/zh/open-search/search-platform/developer-reference/text-embedding-api-details`.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-alibabacloud-aisearch/llama_index/embeddings/alibabacloud_aisearch/base.py`  
| 
```
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
```
 | 
```
classAlibabaCloudAISearchEmbedding(BaseEmbedding):
"""
    For further details, please visit `https://help.aliyun.com/zh/open-search/search-platform/developer-reference/text-embedding-api-details`.
    """

    _client: Client = PrivateAttr()

    aisearch_api_key: str = Field(default=None, exclude=True)
    endpoint: str = None

    service_id: str = "ops-text-embedding-002"
    workspace_name: str = "default"

    def__init__(
        self, endpoint: str = None, aisearch_api_key: str = None, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.aisearch_api_key = get_from_param_or_env(
            "aisearch_api_key", aisearch_api_key, "AISEARCH_API_KEY"
        )
        self.endpoint = get_from_param_or_env("endpoint", endpoint, "AISEARCH_ENDPOINT")

        config = AISearchConfig(
            bearer_token=self.aisearch_api_key,
            endpoint=self.endpoint,
            protocol="http",
        )

        self._client = Client(config=config)

    @classmethod
    defclass_name(cls) -> str:
        return "AlibabaCloudAISearchEmbedding"

    @retry_decorator
    def_get_embedding(self, text: str, input_type: str) -> List[float]:
        request = GetTextEmbeddingRequest(input=text, input_type=input_type)
        response: GetTextEmbeddingResponse = self._client.get_text_embedding(
            workspace_name=self.workspace_name,
            service_id=self.service_id,
            request=request,
        )
        embeddings = response.body.result.embeddings
        return embeddings[0].embedding

    @aretry_decorator
    async def_aget_embedding(self, text: str, input_type: str) -> List[float]:
        request = GetTextEmbeddingRequest(input=text, input_type=input_type)
        response: GetTextEmbeddingResponse = (
            await self._client.get_text_embedding_async(
                workspace_name=self.workspace_name,
                service_id=self.service_id,
                request=request,
            )
        )
        embeddings = response.body.result.embeddings
        return embeddings[0].embedding

    @retry_decorator
    def_get_embeddings(self, texts: List[str], input_type: str) -> List[List[float]]:
        request = GetTextEmbeddingRequest(input=texts, input_type=input_type)
        response: GetTextEmbeddingResponse = self._client.get_text_embedding(
            workspace_name=self.workspace_name,
            service_id=self.service_id,
            request=request,
        )
        embeddings = response.body.result.embeddings
        return [emb.embedding for emb in embeddings]

    @aretry_decorator
    async def_aget_embeddings(
        self,
        texts: List[str],
        input_type: str,
    ) -> List[List[float]]:
        request = GetTextEmbeddingRequest(input=texts, input_type=input_type)
        response: GetTextEmbeddingResponse = (
            await self._client.get_text_embedding_async(
                workspace_name=self.workspace_name,
                service_id=self.service_id,
                request=request,
            )
        )
        embeddings = response.body.result.embeddings
        return [emb.embedding for emb in embeddings]

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self._get_embedding(
            query,
            input_type="query",
        )

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""The asynchronous version of _get_query_embedding."""
        return await self._aget_embedding(
            query,
            input_type="query",
        )

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._get_embedding(
            text,
            input_type="document",
        )

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""The asynchronous version of _get_text_embedding."""
        return await self._aget_embedding(
            text,
            input_type="document",
        )

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        return self._get_embeddings(
            texts,
            input_type="document",
        )

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""The asynchronous version of _get_text_embeddings."""
        return await self._aget_embeddings(
            texts,
            input_type="document",
        )

```
 |  
| --- | --- |  
options: members: - AlibabaCloudAISearchEmbedding
