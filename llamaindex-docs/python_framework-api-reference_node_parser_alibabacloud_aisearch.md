# Alibabacloud aisearch
##  AlibabaCloudAISearchNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/alibabacloud_aisearch/#llama_index.node_parser.alibabacloud_aisearch.AlibabaCloudAISearchNodeParser "Permanent link")
Bases: 
For further details, please visit `https://help.aliyun.com/zh/open-search/search-platform/developer-reference/document-split-api-details`.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-alibabacloud-aisearch/llama_index/node_parser/alibabacloud_aisearch/base.py`  
| 
```
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
```
 | 
```
classAlibabaCloudAISearchNodeParser(NodeParser):
"""
    For further details, please visit `https://help.aliyun.com/zh/open-search/search-platform/developer-reference/document-split-api-details`.
    """

    _client: Client = PrivateAttr()
    _split_strategy: GetDocumentSplitRequestStrategy = PrivateAttr()

    image_reader: Optional[BaseReader] = Field(default=None, exclude=True)

    aisearch_api_key: str = Field(default=None, exclude=True)
    endpoint: str = None

    service_id: str = "ops-document-split-001"
    workspace_name: str = "default"
    chunk_size: int = 300
    need_sentence: bool = False
    default_content_encoding: str = "utf8"
    default_content_type: str = "text/plain"
    num_workers: int = 4

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
        self._split_strategy = GetDocumentSplitRequestStrategy(
            max_chunk_size=self.chunk_size, need_sentence=self.need_sentence
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "AlibabaCloudAISearchNodeParser"

    def_parse_nodes(
        self,
        documents: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
        return asyncio.get_event_loop().run_until_complete(
            self._aparse_nodes(documents, show_progress, **kwargs)
        )

    async def_aparse_nodes(
        self,
        documents: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""
        Parse document into nodes.

        Args:
            nodes (Sequence[BaseNode]): nodes to parse

        """
        jobs = [self._aparse_node(d) for d in documents]
        results = await run_jobs(
            jobs,
            workers=self.num_workers,
            desc="Parsing documents into nodes",
            show_progress=show_progress,
        )
        # return flattened results
        return [item for sublist in results for item in sublist]

    @aretry_decorator
    async def_aparse_node(
        self,
        node: BaseNode,
    ) -> List[BaseNode]:
        content_type = getattr(node, "mimetype", self.default_content_type)
        main_type, sub_type = content_type.split("/")
        if main_type != "text":
            raise ValueError(f"Unsupported content type: {content_type}")
        content_encoding = node.metadata.get("encoding", self.default_content_encoding)
        document = GetDocumentSplitRequestDocument(
            content=node.get_content(),
            content_encoding=content_encoding,
            content_type=sub_type,
        )
        request = GetDocumentSplitRequest(
            document=document, strategy=self._split_strategy
        )

        response: GetDocumentSplitResponse = (
            await self._client.get_document_split_async(
                workspace_name=self.workspace_name,
                service_id=self.service_id,
                request=request,
            )
        )
        return await self._handle_response(response, node)

    async def_handle_response(
        self, response: GetDocumentSplitResponse, node: BaseNode
    ) -> List[TextNode]:
        chunks = list(response.body.result.chunks)
        if response.body.result.sentences:
            chunks.extend(response.body.result.sentences)
        chunks.extend(await self._handle_rich_texts(response.body.result.rich_texts))
        return build_nodes_from_splits(
            [chunk.content for chunk in chunks], node, id_func=self.id_func
        )

    async def_handle_rich_texts(self, rich_texts) -> List[str]:
        chunks = []
        if not rich_texts:
            return chunks
        chunks = list(rich_texts)
        for chunk in chunks:
            if chunk.meta.get("type") == "image":
                chunk.content = await self._handle_image(chunk.content)
        return chunks

    async def_handle_image(self, url: str) -> str:
        content = url
        if not self.image_reader:
            return content
        try:
            docs = await self.image_reader.aload_data([url])
            content = docs[0].get_content()
        except Exception as e:
            logger.error(f"Read image {url} error: {e}")
        return content

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/alibabacloud_aisearch/#llama_index.node_parser.alibabacloud_aisearch.AlibabaCloudAISearchNodeParser.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-alibabacloud-aisearch/llama_index/node_parser/alibabacloud_aisearch/base.py`  
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
"""Get class name."""
    return "AlibabaCloudAISearchNodeParser"

```
 |  
| --- | --- |  
options: members: - AlibabaCloudAISearchNodeParser
