# Index
Node parser interface.
##  BaseExtractor [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/#llama_index.core.extractors.interface.BaseExtractor "Permanent link")
Bases: 
Metadata extractor.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `is_text_node_only`  |  `bool`  |  `True`  |  
|  `show_progress`  |  `bool`  |  Whether to show progress.  |  `True`  |  
|  `metadata_mode`  |  `MetadataMode`  |  Metadata mode to use when reading nodes.  |  `<MetadataMode.ALL: 'all'>`  |  
|  `node_text_template`  |  Template to represent how node text is mixed with metadata text.  |  `'[Excerpt from document]\n{metadata_str}\nExcerpt:\n-----\n{content}\n-----\n'`  |  
|  `disable_template_rewrite`  |  `bool`  |  Disable the node template rewrite.  |  `False`  |  
|  `in_place`  |  `bool`  |  Whether to process nodes in place.  |  `True`  |  
|  `num_workers`  |  Number of workers to use for concurrent async processing.  |  
|  `max_retries`  |  Maximum number of retry attempts when aextract() raises an exception. 0 means no retries (fail immediately, preserving current behaviour).  |  
|  `retry_backoff`  |  `float`  |  Base delay in seconds for exponential backoff between retries. Actual delay is retry_backoff * 2^attempt.  |  `1.0`  |  
|  `raise_on_error`  |  `bool`  |  Whether to raise exceptions when extraction fails after all retries. If True, the exception propagates (current behaviour). If False, logs a warning and returns empty metadata dicts.  |  `True`  |  
Source code in `llama-index-core/llama_index/core/extractors/interface.py`  
| 
```
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
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
```
 | 
```
classBaseExtractor(TransformComponent):
"""Metadata extractor."""

    is_text_node_only: bool = True

    show_progress: bool = Field(default=True, description="Whether to show progress.")

    metadata_mode: MetadataMode = Field(
        default=MetadataMode.ALL, description="Metadata mode to use when reading nodes."
    )

    node_text_template: str = Field(
        default=DEFAULT_NODE_TEXT_TEMPLATE,
        description="Template to represent how node text is mixed with metadata text.",
    )
    disable_template_rewrite: bool = Field(
        default=False, description="Disable the node template rewrite."
    )

    in_place: bool = Field(
        default=True, description="Whether to process nodes in place."
    )

    num_workers: int = Field(
        default=4,
        description="Number of workers to use for concurrent async processing.",
    )

    max_retries: int = Field(
        default=0,
        description=(
            "Maximum number of retry attempts when aextract() raises an exception. "
            "0 means no retries (fail immediately, preserving current behaviour)."
        ),
    )

    retry_backoff: float = Field(
        default=1.0,
        description=(
            "Base delay in seconds for exponential backoff between retries. "
            "Actual delay is retry_backoff * 2^attempt."
        ),
    )

    raise_on_error: bool = Field(
        default=True,
        description=(
            "Whether to raise exceptions when extraction fails after all retries. "
            "If True, the exception propagates (current behaviour). "
            "If False, logs a warning and returns empty metadata dicts."
        ),
    )

    @classmethod
    deffrom_dict(cls, data: Dict[str, Any], **kwargs: Any) -> Self:  # type: ignore
        if isinstance(kwargs, dict):
            data.update(kwargs)

        data.pop("class_name", None)

        llm_predictor = data.get("llm_predictor")
        if llm_predictor:
            fromllama_index.core.llm_predictor.loadingimport load_predictor

            llm_predictor = load_predictor(llm_predictor)
            data["llm_predictor"] = llm_predictor

        llm = data.get("llm")
        if llm:
            fromllama_index.core.llms.loadingimport load_llm

            llm = load_llm(llm)
            data["llm"] = llm

        return cls(**data)

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "MetadataExtractor"

    @abstractmethod
    async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
        Extracts metadata for a sequence of nodes, returning a list of
        metadata dictionaries corresponding to each node.

        Args:
            nodes (Sequence[Document]): nodes to extract metadata from

        """

    defextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
        Extracts metadata for a sequence of nodes, returning a list of
        metadata dictionaries corresponding to each node.

        Args:
            nodes (Sequence[Document]): nodes to extract metadata from

        """
        return asyncio_run(self.aextract(nodes))

    async def_aextract_with_retry(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""Call aextract() with optional retry and error-policy logic."""
        last_exception: Optional[Exception] = None
        for attempt in range(1 + self.max_retries):
            try:
                return await self.aextract(nodes)
            except Exception as e:
                last_exception = e
                if attempt  self.max_retries:
                    delay = self.retry_backoff * (2**attempt)
                    logger.warning(
                        "Extraction attempt %d/%d failed (%s), retrying in %.1fs ...",
                        attempt + 1,
                        self.max_retries + 1,
                        e,
                        delay,
                    )
                    await asyncio.sleep(delay)

        # All retries exhausted
        if not self.raise_on_error:
            logger.warning(
                "Extraction failed after %d attempt(s) (%s). "
                "Returning empty metadata for %d node(s).",
                self.max_retries + 1,
                last_exception,
                len(nodes),
            )
            return [{} for _ in nodes]

        raise last_exception  # type: ignore[misc]

    async defaprocess_nodes(
        self,
        nodes: Sequence[BaseNode],
        excluded_embed_metadata_keys: Optional[List[str]] = None,
        excluded_llm_metadata_keys: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""
        Post process nodes parsed from documents.

        Allows extractors to be chained.

        Args:
            nodes (List[BaseNode]): nodes to post-process
            excluded_embed_metadata_keys (Optional[List[str]]):
                keys to exclude from embed metadata
            excluded_llm_metadata_keys (Optional[List[str]]):
                keys to exclude from llm metadata

        """
        if self.in_place:
            new_nodes = nodes
        else:
            new_nodes = [deepcopy(node) for node in nodes]

        cur_metadata_list = await self._aextract_with_retry(new_nodes)
        for idx, node in enumerate(new_nodes):
            node.metadata.update(cur_metadata_list[idx])

        for idx, node in enumerate(new_nodes):
            if excluded_embed_metadata_keys is not None:
                node.excluded_embed_metadata_keys.extend(excluded_embed_metadata_keys)
            if excluded_llm_metadata_keys is not None:
                node.excluded_llm_metadata_keys.extend(excluded_llm_metadata_keys)
            if not self.disable_template_rewrite:
                if isinstance(node, TextNode):
                    cast(TextNode, node).text_template = self.node_text_template

        return new_nodes  # type: ignore

    defprocess_nodes(
        self,
        nodes: Sequence[BaseNode],
        excluded_embed_metadata_keys: Optional[List[str]] = None,
        excluded_llm_metadata_keys: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[BaseNode]:
        return asyncio_run(
            self.aprocess_nodes(
                nodes,
                excluded_embed_metadata_keys=excluded_embed_metadata_keys,
                excluded_llm_metadata_keys=excluded_llm_metadata_keys,
                **kwargs,
            )
        )

    def__call__(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
"""
        Post process nodes parsed from documents.

        Allows extractors to be chained.

        Args:
            nodes (List[BaseNode]): nodes to post-process

        """
        return self.process_nodes(nodes, **kwargs)

    async defacall(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
"""
        Post process nodes parsed from documents.

        Allows extractors to be chained.

        Args:
            nodes (List[BaseNode]): nodes to post-process

        """
        return await self.aprocess_nodes(nodes, **kwargs)

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/#llama_index.core.extractors.interface.BaseExtractor.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/extractors/interface.py`  
| 
```
102
103
104
105
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "MetadataExtractor"

```
 |  
| --- | --- |  
###  aextract `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/#llama_index.core.extractors.interface.BaseExtractor.aextract "Permanent link")

```
aextract(nodes: Sequence[]) -> []

```

Extracts metadata for a sequence of nodes, returning a list of metadata dictionaries corresponding to each node.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Sequence[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]`  |  nodes to extract metadata from  |  _required_  |  
Source code in `llama-index-core/llama_index/core/extractors/interface.py`  
| 
```
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
```
 | 
```
@abstractmethod
async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
    Extracts metadata for a sequence of nodes, returning a list of
    metadata dictionaries corresponding to each node.

    Args:
        nodes (Sequence[Document]): nodes to extract metadata from

    """

```
 |  
| --- | --- |  
###  extract [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/#llama_index.core.extractors.interface.BaseExtractor.extract "Permanent link")

```
extract(nodes: Sequence[]) -> []

```

Extracts metadata for a sequence of nodes, returning a list of metadata dictionaries corresponding to each node.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Sequence[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]`  |  nodes to extract metadata from  |  _required_  |  
Source code in `llama-index-core/llama_index/core/extractors/interface.py`  
| 
```
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
```
 | 
```
defextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
    Extracts metadata for a sequence of nodes, returning a list of
    metadata dictionaries corresponding to each node.

    Args:
        nodes (Sequence[Document]): nodes to extract metadata from

    """
    return asyncio_run(self.aextract(nodes))

```
 |  
| --- | --- |  
###  aprocess_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/#llama_index.core.extractors.interface.BaseExtractor.aprocess_nodes "Permanent link")

```
aprocess_nodes(
    nodes: Sequence[],
    excluded_embed_metadata_keys: Optional[
        []
    ] = None,
    excluded_llm_metadata_keys: Optional[[]] = None,
    **kwargs: 
) -> []

```

Post process nodes parsed from documents.
Allows extractors to be chained.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  nodes to post-process  |  _required_  |  
|  `excluded_embed_metadata_keys`  |  `Optional[List[str]]`  |  keys to exclude from embed metadata  |  `None`  |  
|  `excluded_llm_metadata_keys`  |  `Optional[List[str]]`  |  keys to exclude from llm metadata  |  `None`  |  
Source code in `llama-index-core/llama_index/core/extractors/interface.py`  
| 
```
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
```
 | 
```
async defaprocess_nodes(
    self,
    nodes: Sequence[BaseNode],
    excluded_embed_metadata_keys: Optional[List[str]] = None,
    excluded_llm_metadata_keys: Optional[List[str]] = None,
    **kwargs: Any,
) -> List[BaseNode]:
"""
    Post process nodes parsed from documents.

    Allows extractors to be chained.

    Args:
        nodes (List[BaseNode]): nodes to post-process
        excluded_embed_metadata_keys (Optional[List[str]]):
            keys to exclude from embed metadata
        excluded_llm_metadata_keys (Optional[List[str]]):
            keys to exclude from llm metadata

    """
    if self.in_place:
        new_nodes = nodes
    else:
        new_nodes = [deepcopy(node) for node in nodes]

    cur_metadata_list = await self._aextract_with_retry(new_nodes)
    for idx, node in enumerate(new_nodes):
        node.metadata.update(cur_metadata_list[idx])

    for idx, node in enumerate(new_nodes):
        if excluded_embed_metadata_keys is not None:
            node.excluded_embed_metadata_keys.extend(excluded_embed_metadata_keys)
        if excluded_llm_metadata_keys is not None:
            node.excluded_llm_metadata_keys.extend(excluded_llm_metadata_keys)
        if not self.disable_template_rewrite:
            if isinstance(node, TextNode):
                cast(TextNode, node).text_template = self.node_text_template

    return new_nodes  # type: ignore

```
 |  
| --- | --- |  
###  acall [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/#llama_index.core.extractors.interface.BaseExtractor.acall "Permanent link")

```
acall(
    nodes: Sequence[], **kwargs: 
) -> []

```

Post process nodes parsed from documents.
Allows extractors to be chained.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  nodes to post-process  |  _required_  |  
Source code in `llama-index-core/llama_index/core/extractors/interface.py`  
| 
```
229
230
231
232
233
234
235
236
237
238
239
```
 | 
```
async defacall(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
"""
    Post process nodes parsed from documents.

    Allows extractors to be chained.

    Args:
        nodes (List[BaseNode]): nodes to post-process

    """
    return await self.aprocess_nodes(nodes, **kwargs)

```
 |  
| --- | --- |  
options: members: - BaseExtractor
