# Index
Node parser interface.
##  NodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/#llama_index.core.node_parser.interface.NodeParser "Permanent link")
Bases: , 
Base interface for node parser.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `include_metadata`  |  `bool`  |  Whether or not to consider metadata when splitting.  |  `True`  |  
|  `include_prev_next_rel`  |  `bool`  |  Include prev/next node relationships.  |  `True`  |  
|  `callback_manager`  |   |  `<llama_index.core.callbacks.base.CallbackManager object at 0x7f00af2d6270>`  |  
|  `id_func`  |  `Callable`  |  Function to generate node IDs.  |  `<function default_id_func at 0x7f00b0d78bf0>`  |  
Source code in `llama-index-core/llama_index/core/node_parser/interface.py`  
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
classNodeParser(TransformComponent, ABC):
"""Base interface for node parser."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    include_metadata: bool = Field(
        default=True, description="Whether or not to consider metadata when splitting."
    )
    include_prev_next_rel: bool = Field(
        default=True, description="Include prev/next node relationships."
    )
    callback_manager: CallbackManager = Field(
        default_factory=lambda: CallbackManager([]), exclude=True
    )
    id_func: IdFuncCallable = Field(
        default=default_id_func,
        description="Function to generate node IDs.",
    )

    @abstractmethod
    def_parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]: ...

    async def_aparse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
        return self._parse_nodes(nodes, show_progress=show_progress, **kwargs)

    def_postprocess_parsed_nodes(
        self, nodes: List[BaseNode], parent_doc_map: Dict[str, Document]
    ) -> List[BaseNode]:
        # Track search position per document to handle duplicate text correctly
        # Nodes are assumed to be in document order from _parse_nodes
        # We track the START position (not end) to allow for overlapping chunks
        doc_search_positions: Dict[str, int] = {}

        for i, node in enumerate(nodes):
            parent_doc = parent_doc_map.get(node.ref_doc_id or "", None)
            parent_node = node.source_node

            if parent_doc is not None:
                if parent_doc.source_node is not None:
                    node.relationships.update(
                        {
                            NodeRelationship.SOURCE: parent_doc.source_node,
                        }
                    )

                # Get or initialize search position for this document
                doc_id = node.ref_doc_id or ""
                search_start = doc_search_positions.get(doc_id, 0)

                # Search for node content starting from the last found position
                node_content = node.get_content(metadata_mode=MetadataMode.NONE)
                start_char_idx = parent_doc.text.find(node_content, search_start)

                # update start/end char idx
                if start_char_idx >= 0 and isinstance(node, TextNode):
                    node.start_char_idx = start_char_idx
                    node.end_char_idx = start_char_idx + len(node_content)
                    # Update search position to start from next character after this node's START
                    # This allows overlapping chunks to be found correctly
                    doc_search_positions[doc_id] = start_char_idx + 1

                # update metadata
                if self.include_metadata:
                    # Merge parent_doc.metadata into nodes.metadata, giving preference to node's values
                    node.metadata = {**parent_doc.metadata, **node.metadata}

            if parent_node is not None:
                if self.include_metadata:
                    parent_metadata = parent_node.metadata

                    combined_metadata = {**parent_metadata, **node.metadata}

                    # Merge parent_node.metadata into nodes.metadata, giving preference to node's values
                    node.metadata.update(combined_metadata)

            if self.include_prev_next_rel:
                # establish prev/next relationships if nodes share the same source_node
                if (
                    i  0
                    and node.source_node
                    and nodes[i - 1].source_node
                    and nodes[i - 1].source_node.node_id == node.source_node.node_id  # type: ignore
                ):
                    node.relationships[NodeRelationship.PREVIOUS] = nodes[
                        i - 1
                    ].as_related_node_info()
                if (
                    i  len(nodes) - 1
                    and node.source_node
                    and nodes[i + 1].source_node
                    and nodes[i + 1].source_node.node_id == node.source_node.node_id  # type: ignore
                ):
                    node.relationships[NodeRelationship.NEXT] = nodes[
                        i + 1
                    ].as_related_node_info()

        return nodes

    defget_nodes_from_documents(
        self,
        documents: Sequence[Document],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""
        Parse documents into nodes.

        Args:
            documents (Sequence[Document]): documents to parse
            show_progress (bool): whether to show progress bar

        """
        doc_id_to_document = {doc.id_: doc for doc in documents}

        with self.callback_manager.event(
            CBEventType.NODE_PARSING, payload={EventPayload.DOCUMENTS: documents}
        ) as event:
            nodes = self._parse_nodes(documents, show_progress=show_progress, **kwargs)
            nodes = self._postprocess_parsed_nodes(nodes, doc_id_to_document)

            event.on_end({EventPayload.NODES: nodes})

        return nodes

    async defaget_nodes_from_documents(
        self,
        documents: Sequence[Document],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
        doc_id_to_document = {doc.id_: doc for doc in documents}

        with self.callback_manager.event(
            CBEventType.NODE_PARSING, payload={EventPayload.DOCUMENTS: documents}
        ) as event:
            nodes = await self._aparse_nodes(
                documents, show_progress=show_progress, **kwargs
            )
            nodes = self._postprocess_parsed_nodes(nodes, doc_id_to_document)

            event.on_end({EventPayload.NODES: nodes})

        return nodes

    def__call__(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
        return self.get_nodes_from_documents(nodes, **kwargs)  # type: ignore

    async defacall(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
        return await self.aget_nodes_from_documents(nodes, **kwargs)  # type: ignore

```
 |  
| --- | --- |  
###  get_nodes_from_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/#llama_index.core.node_parser.interface.NodeParser.get_nodes_from_documents "Permanent link")

```
get_nodes_from_documents(
    documents: Sequence[],
    show_progress:  = False,
    **kwargs: 
) -> []

```

Parse documents into nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `documents`  |  `Sequence[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]`  |  documents to parse  |  _required_  |  
|  `show_progress`  |  `bool`  |  whether to show progress bar  |  `False`  |  
Source code in `llama-index-core/llama_index/core/node_parser/interface.py`  
| 
```
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
```
 | 
```
defget_nodes_from_documents(
    self,
    documents: Sequence[Document],
    show_progress: bool = False,
    **kwargs: Any,
) -> List[BaseNode]:
"""
    Parse documents into nodes.

    Args:
        documents (Sequence[Document]): documents to parse
        show_progress (bool): whether to show progress bar

    """
    doc_id_to_document = {doc.id_: doc for doc in documents}

    with self.callback_manager.event(
        CBEventType.NODE_PARSING, payload={EventPayload.DOCUMENTS: documents}
    ) as event:
        nodes = self._parse_nodes(documents, show_progress=show_progress, **kwargs)
        nodes = self._postprocess_parsed_nodes(nodes, doc_id_to_document)

        event.on_end({EventPayload.NODES: nodes})

    return nodes

```
 |  
| --- | --- |  
##  TextSplitter [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/#llama_index.core.node_parser.interface.TextSplitter "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/node_parser/interface.py`  
| 
```
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
```
 | 
```
classTextSplitter(NodeParser):
    @abstractmethod
    defsplit_text(self, text: str) -> List[str]: ...

    defsplit_texts(self, texts: List[str]) -> List[str]:
        nested_texts = [self.split_text(text) for text in texts]
        return [item for sublist in nested_texts for item in sublist]

    def_parse_nodes(
        self, nodes: Sequence[BaseNode], show_progress: bool = False, **kwargs: Any
    ) -> List[BaseNode]:
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")
        for node in nodes_with_progress:
            splits = self.split_text(node.get_content())

            all_nodes.extend(
                build_nodes_from_splits(splits, node, id_func=self.id_func)
            )

        return all_nodes

```
 |  
| --- | --- |  
##  MetadataAwareTextSplitter [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/#llama_index.core.node_parser.interface.MetadataAwareTextSplitter "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/node_parser/interface.py`  
| 
```
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
```
 | 
```
classMetadataAwareTextSplitter(TextSplitter):
    def__init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        super().__init_subclass__(*args, **kwargs)

        # Pydantic v2 keeps the user-defined init on __pydantic_init__
        user_init = getattr(cls, "__pydantic_init__", None)
        if user_init is None:
            return

        # Safety: don't propagate pydantic-generated docs
        if getattr(user_init, "__module__", "").startswith("pydantic"):
            return

        doc = getattr(user_init, "__doc__", None)
        if not doc:
            return

        # Patch the generated __init__ that help() will show
        try:
            cls.__init__.__doc__ = doc
        except (AttributeError, TypeError):
            pass

    @abstractmethod
    defsplit_text_metadata_aware(self, text: str, metadata_str: str) -> List[str]: ...

    defsplit_texts_metadata_aware(
        self, texts: List[str], metadata_strs: List[str]
    ) -> List[str]:
        if len(texts) != len(metadata_strs):
            raise ValueError("Texts and metadata_strs must have the same length")
        nested_texts = [
            self.split_text_metadata_aware(text, metadata)
            for text, metadata in zip(texts, metadata_strs)
        ]
        return [item for sublist in nested_texts for item in sublist]

    def_get_metadata_str(self, node: BaseNode) -> str:
"""Helper function to get the proper metadata str for splitting."""
        embed_metadata_str = node.get_metadata_str(mode=MetadataMode.EMBED)
        llm_metadata_str = node.get_metadata_str(mode=MetadataMode.LLM)

        # use the longest metadata str for splitting
        if len(embed_metadata_str)  len(llm_metadata_str):
            metadata_str = embed_metadata_str
        else:
            metadata_str = llm_metadata_str

        return metadata_str

    def_parse_nodes(
        self, nodes: Sequence[BaseNode], show_progress: bool = False, **kwargs: Any
    ) -> List[BaseNode]:
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")

        for node in nodes_with_progress:
            metadata_str = self._get_metadata_str(node)
            splits = self.split_text_metadata_aware(
                node.get_content(metadata_mode=MetadataMode.NONE),
                metadata_str=metadata_str,
            )
            all_nodes.extend(
                build_nodes_from_splits(splits, node, id_func=self.id_func)
            )

        return all_nodes

```
 |  
| --- | --- |
