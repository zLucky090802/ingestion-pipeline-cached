# Vector
LlamaIndex data structures.
##  ComposableGraph [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.ComposableGraph "Permanent link")
Composable graph.
Source code in `llama-index-core/llama_index/core/indices/composability/graph.py`  
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
```
 | 
```
classComposableGraph:
"""Composable graph."""

    def__init__(
        self,
        all_indices: Dict[str, BaseIndex],
        root_id: str,
        storage_context: Optional[StorageContext] = None,
    ) -> None:
"""Init params."""
        self._all_indices = all_indices
        self._root_id = root_id
        self.storage_context = storage_context

    @property
    defroot_id(self) -> str:
        return self._root_id

    @property
    defall_indices(self) -> Dict[str, BaseIndex]:
        return self._all_indices

    @property
    defroot_index(self) -> BaseIndex:
        return self._all_indices[self._root_id]

    @property
    defindex_struct(self) -> IndexStruct:
        return self._all_indices[self._root_id].index_struct

    @classmethod
    deffrom_indices(
        cls,
        root_index_cls: Type[BaseIndex],
        children_indices: Sequence[BaseIndex],
        index_summaries: Optional[Sequence[str]] = None,
        storage_context: Optional[StorageContext] = None,
        **kwargs: Any,
    ) -> "ComposableGraph":  # type: ignore
"""Create composable graph using this index class as the root."""
        fromllama_index.coreimport Settings

        with Settings.callback_manager.as_trace("graph_construction"):
            if index_summaries is None:
                for index in children_indices:
                    if index.index_struct.summary is None:
                        raise ValueError(
                            "Summary must be set for children indices. "
                            "If the index does a summary "
                            "(through index.index_struct.summary), then "
                            "it must be specified with then `index_summaries` "
                            "argument in this function. We will support "
                            "automatically setting the summary in the future."
                        )
                index_summaries = [
                    index.index_struct.summary for index in children_indices
                ]
            else:
                # set summaries for each index
                for index, summary in zip(children_indices, index_summaries):
                    index.index_struct.summary = summary

            if len(children_indices) != len(index_summaries):
                raise ValueError("indices and index_summaries must have same length!")

            # construct index nodes
            index_nodes = []
            for index, summary in zip(children_indices, index_summaries):
                assert isinstance(index.index_struct, IndexStruct)
                index_node = IndexNode(
                    text=summary,
                    index_id=index.index_id,
                    relationships={
                        NodeRelationship.SOURCE: RelatedNodeInfo(
                            node_id=index.index_id, node_type=ObjectType.INDEX
                        )
                    },
                )
                index_nodes.append(index_node)

            # construct root index
            root_index = root_index_cls(
                nodes=index_nodes,
                storage_context=storage_context,
                **kwargs,
            )
            # type: ignore
            all_indices: List[BaseIndex] = [
                *cast(List[BaseIndex], children_indices),
                root_index,
            ]

            return cls(
                all_indices={index.index_id: index for index in all_indices},
                root_id=root_index.index_id,
                storage_context=storage_context,
            )

    defget_index(self, index_struct_id: Optional[str] = None) -> BaseIndex:
"""Get index from index struct id."""
        if index_struct_id is None:
            index_struct_id = self._root_id
        return self._all_indices[index_struct_id]

    defas_query_engine(self, **kwargs: Any) -> BaseQueryEngine:
        # NOTE: lazy import
        fromllama_index.core.query_engine.graph_query_engineimport (
            ComposableGraphQueryEngine,
        )

        return ComposableGraphQueryEngine(self, **kwargs)

```
 |  
| --- | --- |  
###  from_indices `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.ComposableGraph.from_indices "Permanent link")

```
from_indices(
    root_index_cls: [],
    children_indices: Sequence[],
    index_summaries: Optional[Sequence[]] = None,
    storage_context: Optional[] = None,
    **kwargs: 
) -> 

```

Create composable graph using this index class as the root.
Source code in `llama-index-core/llama_index/core/indices/composability/graph.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_indices(
    cls,
    root_index_cls: Type[BaseIndex],
    children_indices: Sequence[BaseIndex],
    index_summaries: Optional[Sequence[str]] = None,
    storage_context: Optional[StorageContext] = None,
    **kwargs: Any,
) -> "ComposableGraph":  # type: ignore
"""Create composable graph using this index class as the root."""
    fromllama_index.coreimport Settings

    with Settings.callback_manager.as_trace("graph_construction"):
        if index_summaries is None:
            for index in children_indices:
                if index.index_struct.summary is None:
                    raise ValueError(
                        "Summary must be set for children indices. "
                        "If the index does a summary "
                        "(through index.index_struct.summary), then "
                        "it must be specified with then `index_summaries` "
                        "argument in this function. We will support "
                        "automatically setting the summary in the future."
                    )
            index_summaries = [
                index.index_struct.summary for index in children_indices
            ]
        else:
            # set summaries for each index
            for index, summary in zip(children_indices, index_summaries):
                index.index_struct.summary = summary

        if len(children_indices) != len(index_summaries):
            raise ValueError("indices and index_summaries must have same length!")

        # construct index nodes
        index_nodes = []
        for index, summary in zip(children_indices, index_summaries):
            assert isinstance(index.index_struct, IndexStruct)
            index_node = IndexNode(
                text=summary,
                index_id=index.index_id,
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(
                        node_id=index.index_id, node_type=ObjectType.INDEX
                    )
                },
            )
            index_nodes.append(index_node)

        # construct root index
        root_index = root_index_cls(
            nodes=index_nodes,
            storage_context=storage_context,
            **kwargs,
        )
        # type: ignore
        all_indices: List[BaseIndex] = [
            *cast(List[BaseIndex], children_indices),
            root_index,
        ]

        return cls(
            all_indices={index.index_id: index for index in all_indices},
            root_id=root_index.index_id,
            storage_context=storage_context,
        )

```
 |  
| --- | --- |  
###  get_index [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.ComposableGraph.get_index "Permanent link")

```
get_index(
    index_struct_id: Optional[] = None,
) -> 

```

Get index from index struct id.
Source code in `llama-index-core/llama_index/core/indices/composability/graph.py`  
| 
```
115
116
117
118
119
```
 | 
```
defget_index(self, index_struct_id: Optional[str] = None) -> BaseIndex:
"""Get index from index struct id."""
    if index_struct_id is None:
        index_struct_id = self._root_id
    return self._all_indices[index_struct_id]

```
 |  
| --- | --- |  
##  DocumentSummaryIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.DocumentSummaryIndex "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[IndexDocumentSummary]`
Document Summary Index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `response_synthesizer`  |   |  A response synthesizer for generating summaries.  |  `None`  |  
|  `summary_query`  |  The query to use to generate the summary for each document.  |  `DEFAULT_SUMMARY_QUERY`  |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
|  `embed_summaries`  |  `bool`  |  Whether to embed the summaries. This is required for running the default embedding-based retriever. Defaults to True.  |  `True`  |  
Source code in `llama-index-core/llama_index/core/indices/document_summary/base.py`  
| 
```
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
300
301
302
303
304
305
306
307
308
309
310
311
312
313
```
 | 
```
classDocumentSummaryIndex(BaseIndex[IndexDocumentSummary]):
"""
    Document Summary Index.

    Args:
        response_synthesizer (BaseSynthesizer): A response synthesizer for generating
            summaries.
        summary_query (str): The query to use to generate the summary for each document.
        show_progress (bool): Whether to show tqdm progress bars.
            Defaults to False.
        embed_summaries (bool): Whether to embed the summaries.
            This is required for running the default embedding-based retriever.
            Defaults to True.

    """

    index_struct_cls = IndexDocumentSummary

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[IndexDocumentSummary] = None,
        llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        storage_context: Optional[StorageContext] = None,
        response_synthesizer: Optional[BaseSynthesizer] = None,
        summary_query: str = DEFAULT_SUMMARY_QUERY,
        show_progress: bool = False,
        embed_summaries: bool = True,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._llm = llm or Settings.llm
        self._embed_model = embed_model or Settings.embed_model
        self._response_synthesizer = response_synthesizer or get_response_synthesizer(
            llm=self._llm, response_mode=ResponseMode.TREE_SUMMARIZE
        )
        self._summary_query = summary_query
        self._embed_summaries = embed_summaries

        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            storage_context=storage_context,
            show_progress=show_progress,
            objects=objects,
            **kwargs,
        )

    @property
    defvector_store(self) -> BasePydanticVectorStore:
        return self._vector_store

    defas_retriever(
        self,
        retriever_mode: Union[str, _RetrieverMode] = _RetrieverMode.EMBEDDING,
        **kwargs: Any,
    ) -> BaseRetriever:
"""
        Get retriever.

        Args:
            retriever_mode (Union[str, DocumentSummaryRetrieverMode]): A retriever mode.
                Defaults to DocumentSummaryRetrieverMode.EMBEDDING.

        """
        fromllama_index.core.indices.document_summary.retrieversimport (
            DocumentSummaryIndexEmbeddingRetriever,
            DocumentSummaryIndexLLMRetriever,
        )

        LLMRetriever = DocumentSummaryIndexLLMRetriever
        EmbeddingRetriever = DocumentSummaryIndexEmbeddingRetriever

        if retriever_mode == _RetrieverMode.EMBEDDING:
            if not self._embed_summaries:
                raise ValueError(
                    "Cannot use embedding retriever if embed_summaries is False"
                )

            return EmbeddingRetriever(
                self,
                object_map=self._object_map,
                embed_model=self._embed_model,
                **kwargs,
            )
        if retriever_mode == _RetrieverMode.LLM:
            return LLMRetriever(
                self, object_map=self._object_map, llm=self._llm, **kwargs
            )
        else:
            raise ValueError(f"Unknown retriever mode: {retriever_mode}")

    defget_document_summary(self, doc_id: str) -> str:
"""
        Get document summary by doc id.

        Args:
            doc_id (str): A document id.

        """
        if doc_id not in self._index_struct.doc_id_to_summary_id:
            raise ValueError(f"doc_id {doc_id} not in index")
        summary_id = self._index_struct.doc_id_to_summary_id[doc_id]
        return self.docstore.get_node(summary_id).get_content()

    def_add_nodes_to_index(
        self,
        index_struct: IndexDocumentSummary,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
    ) -> None:
"""Add nodes to index."""
        doc_id_to_nodes = defaultdict(list)
        for node in nodes:
            if node.ref_doc_id is None:
                raise ValueError(
                    "ref_doc_id of node cannot be None when building a document "
                    "summary index"
                )
            doc_id_to_nodes[node.ref_doc_id].append(node)

        summary_node_dict = {}
        items = doc_id_to_nodes.items()
        iterable_with_progress = get_tqdm_iterable(
            items, show_progress, "Summarizing documents"
        )

        for doc_id, nodes in iterable_with_progress:
            print(f"current doc id: {doc_id}")
            nodes_with_scores = [NodeWithScore(node=n) for n in nodes]
            # get the summary for each doc_id
            summary_response = self._response_synthesizer.synthesize(
                query=self._summary_query,
                nodes=nodes_with_scores,
            )
            summary_response = cast(Response, summary_response)
            docid_first_node = doc_id_to_nodes.get(doc_id, [TextNode()])[0]
            summary_node_dict[doc_id] = TextNode(
                text=summary_response.response,
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(node_id=doc_id)
                },
                metadata=docid_first_node.metadata,
                excluded_embed_metadata_keys=docid_first_node.excluded_embed_metadata_keys,
                excluded_llm_metadata_keys=docid_first_node.excluded_llm_metadata_keys,
            )
            self.docstore.add_documents([summary_node_dict[doc_id]])
            logger.info(
                f"> Generated summary for doc {doc_id}: {summary_response.response}"
            )

        for doc_id, nodes in doc_id_to_nodes.items():
            index_struct.add_summary_and_nodes(summary_node_dict[doc_id], nodes)

        if self._embed_summaries:
            summary_nodes = list(summary_node_dict.values())
            id_to_embed_map = embed_nodes(
                summary_nodes, self._embed_model, show_progress=show_progress
            )

            summary_nodes_with_embedding = []
            for node in summary_nodes:
                node_with_embedding = node.model_copy()
                node_with_embedding.embedding = id_to_embed_map[node.node_id]
                summary_nodes_with_embedding.append(node_with_embedding)
            self._vector_store.add(summary_nodes_with_embedding)

    def_build_index_from_nodes(
        self,
        nodes: Sequence[BaseNode],
        **build_kwargs: Any,
    ) -> IndexDocumentSummary:
"""Build index from nodes."""
        # first get doc_id to nodes_dict, generate a summary for each doc_id,
        # then build the index struct
        index_struct = IndexDocumentSummary()
        self._add_nodes_to_index(index_struct, nodes, self._show_progress)
        return index_struct

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a document."""
        self._add_nodes_to_index(self._index_struct, nodes)

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
        pass

    defdelete_nodes(
        self,
        node_ids: List[str],
        delete_from_docstore: bool = False,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete a list of nodes from the index.

        Args:
            node_ids (List[str]): A list of node_ids from the nodes to delete

        """
        index_nodes = self._index_struct.node_id_to_summary_id.keys()
        for node in node_ids:
            if node not in index_nodes:
                logger.warning(f"node_id {node} not found, will not be deleted.")
                node_ids.remove(node)

        self._index_struct.delete_nodes(node_ids)

        remove_summary_ids = [
            summary_id
            for summary_id in self._index_struct.summary_id_to_node_ids
            if len(self._index_struct.summary_id_to_node_ids[summary_id]) == 0
        ]

        remove_docs = [
            doc_id
            for doc_id in self._index_struct.doc_id_to_summary_id
            if self._index_struct.doc_id_to_summary_id[doc_id] in remove_summary_ids
        ]

        for doc_id in remove_docs:
            self.delete_ref_doc(doc_id)

    defdelete_ref_doc(
        self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
    ) -> None:
"""
        Delete a document from the index.
        All nodes in the index related to the document will be deleted.
        """
        ref_doc_info = self.docstore.get_ref_doc_info(ref_doc_id)
        if ref_doc_info is None:
            logger.warning(f"ref_doc_id {ref_doc_id} not found, nothing deleted.")
            return
        self._index_struct.delete(ref_doc_id)
        self._vector_store.delete(ref_doc_id)

        if delete_from_docstore:
            self.docstore.delete_ref_doc(ref_doc_id, raise_error=False)

        self._storage_context.index_store.add_index_struct(self._index_struct)

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        ref_doc_ids = list(self._index_struct.doc_id_to_summary_id.keys())

        all_ref_doc_info = {}
        for ref_doc_id in ref_doc_ids:
            ref_doc_info = self.docstore.get_ref_doc_info(ref_doc_id)
            if not ref_doc_info:
                continue

            all_ref_doc_info[ref_doc_id] = ref_doc_info
        return all_ref_doc_info

```
 |  
| --- | --- |  
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.DocumentSummaryIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
###  as_retriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.DocumentSummaryIndex.as_retriever "Permanent link")

```
as_retriever(
    retriever_mode: Union[, _RetrieverMode] = EMBEDDING,
    **kwargs: 
) -> 

```

Get retriever.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `retriever_mode`  |  `Union[str, DocumentSummaryRetrieverMode]`  |  A retriever mode. Defaults to DocumentSummaryRetrieverMode.EMBEDDING.  |  `EMBEDDING`  |  
Source code in `llama-index-core/llama_index/core/indices/document_summary/base.py`  
| 
```
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
```
 | 
```
defas_retriever(
    self,
    retriever_mode: Union[str, _RetrieverMode] = _RetrieverMode.EMBEDDING,
    **kwargs: Any,
) -> BaseRetriever:
"""
    Get retriever.

    Args:
        retriever_mode (Union[str, DocumentSummaryRetrieverMode]): A retriever mode.
            Defaults to DocumentSummaryRetrieverMode.EMBEDDING.

    """
    fromllama_index.core.indices.document_summary.retrieversimport (
        DocumentSummaryIndexEmbeddingRetriever,
        DocumentSummaryIndexLLMRetriever,
    )

    LLMRetriever = DocumentSummaryIndexLLMRetriever
    EmbeddingRetriever = DocumentSummaryIndexEmbeddingRetriever

    if retriever_mode == _RetrieverMode.EMBEDDING:
        if not self._embed_summaries:
            raise ValueError(
                "Cannot use embedding retriever if embed_summaries is False"
            )

        return EmbeddingRetriever(
            self,
            object_map=self._object_map,
            embed_model=self._embed_model,
            **kwargs,
        )
    if retriever_mode == _RetrieverMode.LLM:
        return LLMRetriever(
            self, object_map=self._object_map, llm=self._llm, **kwargs
        )
    else:
        raise ValueError(f"Unknown retriever mode: {retriever_mode}")

```
 |  
| --- | --- |  
###  get_document_summary [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.DocumentSummaryIndex.get_document_summary "Permanent link")

```
get_document_summary(doc_id: ) -> 

```

Get document summary by doc id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `doc_id`  |  A document id.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/document_summary/base.py`  
| 
```
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
```
 | 
```
defget_document_summary(self, doc_id: str) -> str:
"""
    Get document summary by doc id.

    Args:
        doc_id (str): A document id.

    """
    if doc_id not in self._index_struct.doc_id_to_summary_id:
        raise ValueError(f"doc_id {doc_id} not in index")
    summary_id = self._index_struct.doc_id_to_summary_id[doc_id]
    return self.docstore.get_node(summary_id).get_content()

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.DocumentSummaryIndex.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: [],
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a list of nodes from the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `List[str]`  |  A list of node_ids from the nodes to delete  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/document_summary/base.py`  
| 
```
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
```
 | 
```
defdelete_nodes(
    self,
    node_ids: List[str],
    delete_from_docstore: bool = False,
    **delete_kwargs: Any,
) -> None:
"""
    Delete a list of nodes from the index.

    Args:
        node_ids (List[str]): A list of node_ids from the nodes to delete

    """
    index_nodes = self._index_struct.node_id_to_summary_id.keys()
    for node in node_ids:
        if node not in index_nodes:
            logger.warning(f"node_id {node} not found, will not be deleted.")
            node_ids.remove(node)

    self._index_struct.delete_nodes(node_ids)

    remove_summary_ids = [
        summary_id
        for summary_id in self._index_struct.summary_id_to_node_ids
        if len(self._index_struct.summary_id_to_node_ids[summary_id]) == 0
    ]

    remove_docs = [
        doc_id
        for doc_id in self._index_struct.doc_id_to_summary_id
        if self._index_struct.doc_id_to_summary_id[doc_id] in remove_summary_ids
    ]

    for doc_id in remove_docs:
        self.delete_ref_doc(doc_id)

```
 |  
| --- | --- |  
###  delete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.DocumentSummaryIndex.delete_ref_doc "Permanent link")

```
delete_ref_doc(
    ref_doc_id: ,
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a document from the index. All nodes in the index related to the document will be deleted.
Source code in `llama-index-core/llama_index/core/indices/document_summary/base.py`  
| 
```
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
defdelete_ref_doc(
    self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
) -> None:
"""
    Delete a document from the index.
    All nodes in the index related to the document will be deleted.
    """
    ref_doc_info = self.docstore.get_ref_doc_info(ref_doc_id)
    if ref_doc_info is None:
        logger.warning(f"ref_doc_id {ref_doc_id} not found, nothing deleted.")
        return
    self._index_struct.delete(ref_doc_id)
    self._vector_store.delete(ref_doc_id)

    if delete_from_docstore:
        self.docstore.delete_ref_doc(ref_doc_id, raise_error=False)

    self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
##  EmptyIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.EmptyIndex "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[EmptyIndexStruct]`
Empty Index.
An index that doesn't contain any documents. Used for pure LLM calls. NOTE: this exists because an empty index it allows certain properties, such as the ability to be composed with other indices + token counting + others.
Source code in `llama-index-core/llama_index/core/indices/empty/base.py`  
| 
```
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
```
 | 
```
classEmptyIndex(BaseIndex[EmptyIndexStruct]):
"""
    Empty Index.

    An index that doesn't contain any documents. Used for
    pure LLM calls.
    NOTE: this exists because an empty index it allows certain properties,
    such as the ability to be composed with other indices + token
    counting + others.

    """

    index_struct_cls = EmptyIndexStruct

    def__init__(
        self,
        index_struct: Optional[EmptyIndexStruct] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        super().__init__(
            nodes=None,
            index_struct=index_struct or EmptyIndexStruct(),
            **kwargs,
        )

    defas_retriever(self, **kwargs: Any) -> BaseRetriever:
        # NOTE: lazy import
        fromllama_index.core.indices.empty.retrieversimport EmptyIndexRetriever

        return EmptyIndexRetriever(self)

    defas_query_engine(
        self, llm: Optional[LLMType] = None, **kwargs: Any
    ) -> BaseQueryEngine:
        if "response_mode" not in kwargs:
            kwargs["response_mode"] = "generation"
        else:
            if kwargs["response_mode"] != "generation":
                raise ValueError("EmptyIndex only supports response_mode=generation.")

        return super().as_query_engine(llm=llm, **kwargs)

    def_build_index_from_nodes(
        self, nodes: Sequence[BaseNode], **build_kwargs: Any
    ) -> EmptyIndexStruct:
"""
        Build the index from documents.

        Args:
            documents (List[BaseDocument]): A list of documents.

        Returns:
            IndexList: The created summary index.

        """
        del nodes  # Unused
        return EmptyIndexStruct()

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a document."""
        del nodes  # Unused
        raise NotImplementedError("Cannot insert into an empty index.")

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
"""Delete a node."""
        raise NotImplementedError("Cannot delete from an empty index.")

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        raise NotImplementedError("ref_doc_info not supported for an empty index.")

```
 |  
| --- | --- |  
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.EmptyIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
##  KeywordTableIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.KeywordTableIndex "Permanent link")
Bases: `BaseKeywordTableIndex`
Keyword Table Index.
This index uses a GPT model to extract keywords from the text.
Source code in `llama-index-core/llama_index/core/indices/keyword_table/base.py`  
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
```
 | 
```
classKeywordTableIndex(BaseKeywordTableIndex):
"""
    Keyword Table Index.

    This index uses a GPT model to extract keywords from the text.

    """

    def_extract_keywords(self, text: str) -> Set[str]:
"""Extract keywords from text."""
        response = self._llm.predict(
            self.keyword_extract_template,
            text=text,
        )
        return extract_keywords_given_response(response, start_token="KEYWORDS:")

    async def_async_extract_keywords(self, text: str) -> Set[str]:
"""Extract keywords from text."""
        response = await self._llm.apredict(
            self.keyword_extract_template,
            text=text,
        )
        return extract_keywords_given_response(response, start_token="KEYWORDS:")

```
 |  
| --- | --- |  
##  RAKEKeywordTableIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.RAKEKeywordTableIndex "Permanent link")
Bases: `BaseKeywordTableIndex`
RAKE Keyword Table Index.
This index uses a RAKE keyword extractor to extract keywords from the text.
Source code in `llama-index-core/llama_index/core/indices/keyword_table/rake_base.py`  
| 
```
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
```
 | 
```
classRAKEKeywordTableIndex(BaseKeywordTableIndex):
"""
    RAKE Keyword Table Index.

    This index uses a RAKE keyword extractor to extract keywords from the text.

    """

    def_extract_keywords(self, text: str) -> Set[str]:
"""Extract keywords from text."""
        return rake_extract_keywords(text, max_keywords=self.max_keywords_per_chunk)

    defas_retriever(
        self,
        retriever_mode: Union[
            str, KeywordTableRetrieverMode
        ] = KeywordTableRetrieverMode.RAKE,
        **kwargs: Any,
    ) -> BaseRetriever:
        return super().as_retriever(retriever_mode=retriever_mode, **kwargs)

```
 |  
| --- | --- |  
##  SimpleKeywordTableIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.SimpleKeywordTableIndex "Permanent link")
Bases: `BaseKeywordTableIndex`
Simple Keyword Table Index.
This index uses a simple regex extractor to extract keywords from the text.
Source code in `llama-index-core/llama_index/core/indices/keyword_table/simple_base.py`  
| 
```
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
```
 | 
```
classSimpleKeywordTableIndex(BaseKeywordTableIndex):
"""
    Simple Keyword Table Index.

    This index uses a simple regex extractor to extract keywords from the text.

    """

    def_extract_keywords(self, text: str) -> Set[str]:
"""Extract keywords from text."""
        return simple_extract_keywords(text, self.max_keywords_per_chunk)

    defas_retriever(
        self,
        retriever_mode: Union[
            str, KeywordTableRetrieverMode
        ] = KeywordTableRetrieverMode.SIMPLE,
        **kwargs: Any,
    ) -> BaseRetriever:
        return super().as_retriever(retriever_mode=retriever_mode, **kwargs)

```
 |  
| --- | --- |  
##  KnowledgeGraphIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.KnowledgeGraphIndex "Permanent link")
Bases: 
Knowledge Graph Index.
Build a KG by extracting triplets, and leveraging the KG during query-time.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `kg_triplet_extract_template`  |   |  The prompt to use for extracting triplets.  |  `None`  |  
|  `max_triplets_per_chunk`  |  The maximum number of triplets to extract.  |  
|  `storage_context`  |  `Optional[StorageContext[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.storage.storage_context.StorageContext "StorageContext


  
      dataclass
   \(llama_index.core.storage.storage_context.StorageContext\)")]`  |  The storage context to use.  |  `None`  |  
|  `graph_store`  |  `Optional[GraphStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore "GraphStore \(llama_index.core.graph_stores.types.GraphStore\)")]`  |  The graph store to use.  |  _required_  |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
|  `include_embeddings`  |  `bool`  |  Whether to include embeddings in the index. Defaults to False.  |  `False`  |  
|  `max_object_length`  |  The maximum length of the object in a triplet. Defaults to 128.  |  `128`  |  
|  `kg_triplet_extract_fn`  |  `Optional[Callable]`  |  The function to use for extracting triplets. Defaults to None.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/indices/knowledge_graph/base.py`  
| 
```
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
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
```
 | 
```
@deprecated.deprecated(
    version="0.10.53",
    reason=(
        "The KnowledgeGraphIndex class has been deprecated. "
        "Please use the new PropertyGraphIndex class instead. "
        "If a certain graph store integration is missing in the new class, "
        "please open an issue on the GitHub repository or contribute it!"
    ),
)
classKnowledgeGraphIndex(BaseIndex[KG]):
"""
    Knowledge Graph Index.

    Build a KG by extracting triplets, and leveraging the KG during query-time.

    Args:
        kg_triplet_extract_template (BasePromptTemplate): The prompt to use for
            extracting triplets.
        max_triplets_per_chunk (int): The maximum number of triplets to extract.
        storage_context (Optional[StorageContext]): The storage context to use.
        graph_store (Optional[GraphStore]): The graph store to use.
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
        include_embeddings (bool): Whether to include embeddings in the index.
            Defaults to False.
        max_object_length (int): The maximum length of the object in a triplet.
            Defaults to 128.
        kg_triplet_extract_fn (Optional[Callable]): The function to use for
            extracting triplets. Defaults to None.

    """

    index_struct_cls = KG

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[KG] = None,
        llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        storage_context: Optional[StorageContext] = None,
        kg_triplet_extract_template: Optional[BasePromptTemplate] = None,
        max_triplets_per_chunk: int = 10,
        include_embeddings: bool = False,
        show_progress: bool = False,
        max_object_length: int = 128,
        kg_triplet_extract_fn: Optional[Callable] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        # need to set parameters before building index in base class.
        self.include_embeddings = include_embeddings
        self.max_triplets_per_chunk = max_triplets_per_chunk
        self.kg_triplet_extract_template = (
            kg_triplet_extract_template or DEFAULT_KG_TRIPLET_EXTRACT_PROMPT
        )
        # NOTE: Partially format keyword extract template here.
        self.kg_triplet_extract_template = (
            self.kg_triplet_extract_template.partial_format(
                max_knowledge_triplets=self.max_triplets_per_chunk
            )
        )
        self._max_object_length = max_object_length
        self._kg_triplet_extract_fn = kg_triplet_extract_fn

        self._llm = llm or Settings.llm
        self._embed_model = embed_model or Settings.embed_model

        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            storage_context=storage_context,
            show_progress=show_progress,
            objects=objects,
            **kwargs,
        )

        # TODO: legacy conversion - remove in next release
        if (
            len(self.index_struct.table)  0
            and isinstance(self.graph_store, SimpleGraphStore)
            and len(self.graph_store._data.graph_dict) == 0
        ):
            logger.warning("Upgrading previously saved KG index to new storage format.")
            self.graph_store._data.graph_dict = self.index_struct.rel_map

    @property
    defgraph_store(self) -> GraphStore:
        return self._graph_store

    defas_retriever(
        self,
        retriever_mode: Optional[str] = None,
        embed_model: Optional[BaseEmbedding] = None,
        **kwargs: Any,
    ) -> BaseRetriever:
        fromllama_index.core.indices.knowledge_graph.retrieversimport (
            KGRetrieverMode,
            KGTableRetriever,
        )

        if len(self.index_struct.embedding_dict)  0 and retriever_mode is None:
            retriever_mode = KGRetrieverMode.HYBRID
        elif retriever_mode is None:
            retriever_mode = KGRetrieverMode.KEYWORD
        elif isinstance(retriever_mode, str):
            retriever_mode = KGRetrieverMode(retriever_mode)
        else:
            retriever_mode = retriever_mode

        return KGTableRetriever(
            self,
            object_map=self._object_map,
            llm=self._llm,
            embed_model=embed_model or self._embed_model,
            retriever_mode=retriever_mode,
            **kwargs,
        )

    def_extract_triplets(self, text: str) -> List[Tuple[str, str, str]]:
        if self._kg_triplet_extract_fn is not None:
            return self._kg_triplet_extract_fn(text)
        else:
            return self._llm_extract_triplets(text)

    def_llm_extract_triplets(self, text: str) -> List[Tuple[str, str, str]]:
"""Extract keywords from text."""
        response = self._llm.predict(
            self.kg_triplet_extract_template,
            text=text,
        )
        return self._parse_triplet_response(
            response, max_length=self._max_object_length
        )

    @staticmethod
    def_parse_triplet_response(
        response: str, max_length: int = 128
    ) -> List[Tuple[str, str, str]]:
        knowledge_strs = response.strip().split("\n")
        results = []
        for text in knowledge_strs:
            if "(" not in text or ")" not in text or text.index(")")  text.index("("):
                # skip empty lines and non-triplets
                continue
            triplet_part = text[text.index("(") + 1 : text.index(")")]
            tokens = triplet_part.split(",")
            if len(tokens) != 3:
                continue

            if any(len(s.encode("utf-8"))  max_length for s in tokens):
                # We count byte-length instead of len() for UTF-8 chars,
                # will skip if any of the tokens are too long.
                # This is normally due to a poorly formatted triplet
                # extraction, in more serious KG building cases
                # we'll need NLP models to better extract triplets.
                continue

            subj, pred, obj = map(str.strip, tokens)
            if not subj or not pred or not obj:
                # skip partial triplets
                continue

            # Strip double quotes and Capitalize triplets for disambiguation
            subj, pred, obj = (
                entity.strip('"').capitalize() for entity in [subj, pred, obj]
            )

            results.append((subj, pred, obj))
        return results

    def_build_index_from_nodes(
        self, nodes: Sequence[BaseNode], **build_kwargs: Any
    ) -> KG:
"""Build the index from nodes."""
        # do simple concatenation
        index_struct = self.index_struct_cls()
        nodes_with_progress = get_tqdm_iterable(
            nodes, self._show_progress, "Processing nodes"
        )
        for n in nodes_with_progress:
            triplets = self._extract_triplets(
                n.get_content(metadata_mode=MetadataMode.LLM)
            )
            logger.debug(f"> Extracted triplets: {triplets}")
            for triplet in triplets:
                subj, _, obj = triplet
                self.upsert_triplet(triplet)
                index_struct.add_node([subj, obj], n)

            if self.include_embeddings:
                triplet_texts = [str(t) for t in triplets]

                embed_outputs = self._embed_model.get_text_embedding_batch(
                    triplet_texts, show_progress=self._show_progress
                )
                for rel_text, rel_embed in zip(triplet_texts, embed_outputs):
                    index_struct.add_to_embedding_dict(rel_text, rel_embed)

        return index_struct

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a document."""
        for n in nodes:
            triplets = self._extract_triplets(
                n.get_content(metadata_mode=MetadataMode.LLM)
            )
            logger.debug(f"Extracted triplets: {triplets}")
            for triplet in triplets:
                subj, _, obj = triplet
                triplet_str = str(triplet)
                self.upsert_triplet(triplet)
                self._index_struct.add_node([subj, obj], n)
                if (
                    self.include_embeddings
                    and triplet_str not in self._index_struct.embedding_dict
                ):
                    rel_embedding = self._embed_model.get_text_embedding(triplet_str)
                    self._index_struct.add_to_embedding_dict(triplet_str, rel_embedding)

        # Update the storage context's index_store
        self._storage_context.index_store.add_index_struct(self._index_struct)

    defupsert_triplet(
        self, triplet: Tuple[str, str, str], include_embeddings: bool = False
    ) -> None:
"""
        Insert triplets and optionally embeddings.

        Used for manual insertion of KG triplets (in the form
        of (subject, relationship, object)).

        Args:
            triplet (tuple): Knowledge triplet
            embedding (Any, optional): Embedding option for the triplet. Defaults to None.

        """
        self._graph_store.upsert_triplet(*triplet)
        triplet_str = str(triplet)
        if include_embeddings:
            set_embedding = self._embed_model.get_text_embedding(triplet_str)
            self._index_struct.add_to_embedding_dict(str(triplet), set_embedding)
            self._storage_context.index_store.add_index_struct(self._index_struct)

    defadd_node(self, keywords: List[str], node: BaseNode) -> None:
"""
        Add node.

        Used for manual insertion of nodes (keyed by keywords).

        Args:
            keywords (List[str]): Keywords to index the node.
            node (Node): Node to be indexed.

        """
        self._index_struct.add_node(keywords, node)
        self._docstore.add_documents([node], allow_update=True)

    defupsert_triplet_and_node(
        self,
        triplet: Tuple[str, str, str],
        node: BaseNode,
        include_embeddings: bool = False,
    ) -> None:
"""
        Upsert KG triplet and node.

        Calls both upsert_triplet and add_node.
        Behavior is idempotent; if Node already exists,
        only triplet will be added.

        Args:
            keywords (List[str]): Keywords to index the node.
            node (Node): Node to be indexed.
            include_embeddings (bool): Option to add embeddings for triplets. Defaults to False

        """
        subj, _, obj = triplet
        self.upsert_triplet(triplet)
        self.add_node([subj, obj], node)
        triplet_str = str(triplet)
        if include_embeddings:
            set_embedding = self._embed_model.get_text_embedding(triplet_str)
            self._index_struct.add_to_embedding_dict(str(triplet), set_embedding)
            self._storage_context.index_store.add_index_struct(self._index_struct)

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
"""Delete a node."""
        raise NotImplementedError("Delete is not supported for KG index yet.")

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        node_doc_ids_sets = list(self._index_struct.table.values())
        node_doc_ids = list(set().union(*node_doc_ids_sets))
        nodes = self.docstore.get_nodes(node_doc_ids)

        all_ref_doc_info = {}
        for node in nodes:
            ref_node = node.source_node
            if not ref_node:
                continue

            ref_doc_info = self.docstore.get_ref_doc_info(ref_node.node_id)
            if not ref_doc_info:
                continue

            all_ref_doc_info[ref_node.node_id] = ref_doc_info
        return all_ref_doc_info

    defget_networkx_graph(self, limit: int = 100) -> Any:
"""
        Get networkx representation of the graph structure.

        Args:
            limit (int): Number of starting nodes to be included in the graph.

        NOTE: This function requires networkx to be installed.
        NOTE: This is a beta feature.

        """
        try:
            importnetworkxasnx
        except ImportError:
            raise ImportError(
                "Please install networkx to visualize the graph: `pip install networkx`"
            )

        g = nx.Graph()
        subjs = list(self.index_struct.table.keys())

        # add edges
        rel_map = self._graph_store.get_rel_map(subjs=subjs, depth=1, limit=limit)

        added_nodes = set()
        for keyword in rel_map:
            for path in rel_map[keyword]:
                subj = keyword
                for i in range(0, len(path), 2):
                    if i + 2 >= len(path):
                        break

                    if subj not in added_nodes:
                        g.add_node(subj)
                        added_nodes.add(subj)

                    rel = path[i + 1]
                    obj = path[i + 2]

                    g.add_edge(subj, obj, label=rel, title=rel)
                    subj = obj
        return g

    @property
    defquery_context(self) -> Dict[str, Any]:
        return {GRAPH_STORE_KEY: self._graph_store}

```
 |  
| --- | --- |  
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.KnowledgeGraphIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
###  upsert_triplet [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.KnowledgeGraphIndex.upsert_triplet "Permanent link")

```
upsert_triplet(
    triplet: Tuple[, , ],
    include_embeddings:  = False,
) -> None

```

Insert triplets and optionally embeddings.
Used for manual insertion of KG triplets (in the form of (subject, relationship, object)).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `triplet`  |  `tuple`  |  Knowledge triplet  |  _required_  |  
|  `embedding`  |  Embedding option for the triplet. Defaults to None.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/knowledge_graph/base.py`  
| 
```
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
```
 | 
```
defupsert_triplet(
    self, triplet: Tuple[str, str, str], include_embeddings: bool = False
) -> None:
"""
    Insert triplets and optionally embeddings.

    Used for manual insertion of KG triplets (in the form
    of (subject, relationship, object)).

    Args:
        triplet (tuple): Knowledge triplet
        embedding (Any, optional): Embedding option for the triplet. Defaults to None.

    """
    self._graph_store.upsert_triplet(*triplet)
    triplet_str = str(triplet)
    if include_embeddings:
        set_embedding = self._embed_model.get_text_embedding(triplet_str)
        self._index_struct.add_to_embedding_dict(str(triplet), set_embedding)
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  add_node [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.KnowledgeGraphIndex.add_node "Permanent link")

```
add_node(keywords: [], node: ) -> None

```

Add node.
Used for manual insertion of nodes (keyed by keywords).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `keywords`  |  `List[str]`  |  Keywords to index the node.  |  _required_  |  
|  `node`  |  `Node`  |  Node to be indexed.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/knowledge_graph/base.py`  
| 
```
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
```
 | 
```
defadd_node(self, keywords: List[str], node: BaseNode) -> None:
"""
    Add node.

    Used for manual insertion of nodes (keyed by keywords).

    Args:
        keywords (List[str]): Keywords to index the node.
        node (Node): Node to be indexed.

    """
    self._index_struct.add_node(keywords, node)
    self._docstore.add_documents([node], allow_update=True)

```
 |  
| --- | --- |  
###  upsert_triplet_and_node [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.KnowledgeGraphIndex.upsert_triplet_and_node "Permanent link")

```
upsert_triplet_and_node(
    triplet: Tuple[, , ],
    node: ,
    include_embeddings:  = False,
) -> None

```

Upsert KG triplet and node.
Calls both upsert_triplet and add_node. Behavior is idempotent; if Node already exists, only triplet will be added.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `keywords`  |  `List[str]`  |  Keywords to index the node.  |  _required_  |  
|  `node`  |  `Node`  |  Node to be indexed.  |  _required_  |  
|  `include_embeddings`  |  `bool`  |  Option to add embeddings for triplets. Defaults to False  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/knowledge_graph/base.py`  
| 
```
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
```
 | 
```
defupsert_triplet_and_node(
    self,
    triplet: Tuple[str, str, str],
    node: BaseNode,
    include_embeddings: bool = False,
) -> None:
"""
    Upsert KG triplet and node.

    Calls both upsert_triplet and add_node.
    Behavior is idempotent; if Node already exists,
    only triplet will be added.

    Args:
        keywords (List[str]): Keywords to index the node.
        node (Node): Node to be indexed.
        include_embeddings (bool): Option to add embeddings for triplets. Defaults to False

    """
    subj, _, obj = triplet
    self.upsert_triplet(triplet)
    self.add_node([subj, obj], node)
    triplet_str = str(triplet)
    if include_embeddings:
        set_embedding = self._embed_model.get_text_embedding(triplet_str)
        self._index_struct.add_to_embedding_dict(str(triplet), set_embedding)
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  get_networkx_graph [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.KnowledgeGraphIndex.get_networkx_graph "Permanent link")

```
get_networkx_graph(limit:  = 100) -> 

```

Get networkx representation of the graph structure.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `limit`  |  Number of starting nodes to be included in the graph.  |  `100`  |  
NOTE: This function requires networkx to be installed. NOTE: This is a beta feature.
Source code in `llama-index-core/llama_index/core/indices/knowledge_graph/base.py`  
| 
```
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
```
 | 
```
defget_networkx_graph(self, limit: int = 100) -> Any:
"""
    Get networkx representation of the graph structure.

    Args:
        limit (int): Number of starting nodes to be included in the graph.

    NOTE: This function requires networkx to be installed.
    NOTE: This is a beta feature.

    """
    try:
        importnetworkxasnx
    except ImportError:
        raise ImportError(
            "Please install networkx to visualize the graph: `pip install networkx`"
        )

    g = nx.Graph()
    subjs = list(self.index_struct.table.keys())

    # add edges
    rel_map = self._graph_store.get_rel_map(subjs=subjs, depth=1, limit=limit)

    added_nodes = set()
    for keyword in rel_map:
        for path in rel_map[keyword]:
            subj = keyword
            for i in range(0, len(path), 2):
                if i + 2 >= len(path):
                    break

                if subj not in added_nodes:
                    g.add_node(subj)
                    added_nodes.add(subj)

                rel = path[i + 1]
                obj = path[i + 2]

                g.add_edge(subj, obj, label=rel, title=rel)
                subj = obj
    return g

```
 |  
| --- | --- |  
##  SummaryIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.SummaryIndex "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[IndexList]`
Summary Index.
The summary index is a simple data structure where nodes are stored in a sequence. During index construction, the document texts are chunked up, converted to nodes, and stored in a list.
During query time, the summary index iterates through the nodes with some optional filter parameters, and synthesizes an answer from all the nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `text_qa_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Question-Answer Prompt (see :ref:`Prompt-Templates`). NOTE: this is a deprecated field.  |  _required_  |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/list/base.py`  
| 
```
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
```
 | 
```
classSummaryIndex(BaseIndex[IndexList]):
"""
    Summary Index.

    The summary index is a simple data structure where nodes are stored in
    a sequence. During index construction, the document texts are
    chunked up, converted to nodes, and stored in a list.

    During query time, the summary index iterates through the nodes
    with some optional filter parameters, and synthesizes an
    answer from all the nodes.

    Args:
        text_qa_template (Optional[BasePromptTemplate]): A Question-Answer Prompt
            (see :ref:`Prompt-Templates`).
            NOTE: this is a deprecated field.
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.

    """

    index_struct_cls = IndexList

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[IndexList] = None,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            show_progress=show_progress,
            objects=objects,
            **kwargs,
        )

    defas_retriever(
        self,
        retriever_mode: Union[str, ListRetrieverMode] = ListRetrieverMode.DEFAULT,
        llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        **kwargs: Any,
    ) -> BaseRetriever:
        fromllama_index.core.indices.list.retrieversimport (
            SummaryIndexEmbeddingRetriever,
            SummaryIndexLLMRetriever,
            SummaryIndexRetriever,
        )

        if retriever_mode == ListRetrieverMode.DEFAULT:
            return SummaryIndexRetriever(self, object_map=self._object_map, **kwargs)
        elif retriever_mode == ListRetrieverMode.EMBEDDING:
            embed_model = embed_model or Settings.embed_model
            return SummaryIndexEmbeddingRetriever(
                self, object_map=self._object_map, embed_model=embed_model, **kwargs
            )
        elif retriever_mode == ListRetrieverMode.LLM:
            llm = llm or Settings.llm
            return SummaryIndexLLMRetriever(
                self, object_map=self._object_map, llm=llm, **kwargs
            )
        else:
            raise ValueError(f"Unknown retriever mode: {retriever_mode}")

    def_build_index_from_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **build_kwargs: Any,
    ) -> IndexList:
"""
        Build the index from documents.

        Args:
            documents (List[BaseDocument]): A list of documents.

        Returns:
            IndexList: The created summary index.

        """
        index_struct = IndexList()
        nodes_with_progress = get_tqdm_iterable(
            nodes, show_progress, "Processing nodes"
        )
        for n in nodes_with_progress:
            index_struct.add_node(n)
        return index_struct

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a document."""
        for n in nodes:
            self._index_struct.add_node(n)

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
"""Delete a node."""
        cur_node_ids = self._index_struct.nodes
        cur_nodes = self._docstore.get_nodes(cur_node_ids)
        nodes_to_keep = [n for n in cur_nodes if n.node_id != node_id]
        self._index_struct.nodes = [n.node_id for n in nodes_to_keep]

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        node_doc_ids = self._index_struct.nodes
        nodes = self.docstore.get_nodes(node_doc_ids)

        all_ref_doc_info = {}
        for node in nodes:
            ref_node = node.source_node
            if not ref_node:
                continue

            ref_doc_info = self.docstore.get_ref_doc_info(ref_node.node_id)
            if not ref_doc_info:
                continue

            all_ref_doc_info[ref_node.node_id] = ref_doc_info
        return all_ref_doc_info

```
 |  
| --- | --- |  
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.SummaryIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
##  MultiModalVectorStoreIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.MultiModalVectorStoreIndex "Permanent link")
Bases: 
Multi-Modal Vector Store Index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `use_async`  |  `bool`  |  Whether to use asynchronous calls. Defaults to False.  |  `False`  |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
|  `store_nodes_override`  |  `bool`  |  set to True to always store Node objects in index store and document store even if vector store keeps text. Defaults to False  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/multi_modal/base.py`  
| 
```
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
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
```
 | 
```
classMultiModalVectorStoreIndex(VectorStoreIndex):
"""
    Multi-Modal Vector Store Index.

    Args:
        use_async (bool): Whether to use asynchronous calls. Defaults to False.
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
        store_nodes_override (bool): set to True to always store Node objects in index
            store and document store even if vector store keeps text. Defaults to False

    """

    image_namespace = "image"
    index_struct_cls = MultiModelIndexDict

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        index_struct: Optional[MultiModelIndexDict] = None,
        embed_model: Optional[BaseEmbedding] = None,
        storage_context: Optional[StorageContext] = None,
        use_async: bool = False,
        store_nodes_override: bool = False,
        show_progress: bool = False,
        # Image-related kwargs
        # image_vector_store going to be deprecated. image_store can be passed from storage_context
        # keep image_vector_store here for backward compatibility
        image_vector_store: Optional[BasePydanticVectorStore] = None,
        image_embed_model: EmbedType = "clip:ViT-B/32",
        is_image_to_text: bool = False,
        # is_image_vector_store_empty is used to indicate whether image_vector_store is empty
        # those flags are used for cases when only one vector store is used
        is_image_vector_store_empty: bool = False,
        is_text_vector_store_empty: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        image_embed_model = resolve_embed_model(
            image_embed_model, callback_manager=kwargs.get("callback_manager")
        )
        assert isinstance(image_embed_model, MultiModalEmbedding)
        self._image_embed_model = image_embed_model
        self._is_image_to_text = is_image_to_text
        self._is_image_vector_store_empty = is_image_vector_store_empty
        self._is_text_vector_store_empty = is_text_vector_store_empty
        storage_context = storage_context or StorageContext.from_defaults()

        if image_vector_store is not None:
            if self.image_namespace not in storage_context.vector_stores:
                storage_context.add_vector_store(
                    image_vector_store, self.image_namespace
                )
            else:
                # overwrite image_store from storage_context
                storage_context.vector_stores[self.image_namespace] = image_vector_store

        if self.image_namespace not in storage_context.vector_stores:
            storage_context.add_vector_store(SimpleVectorStore(), self.image_namespace)

        self._image_vector_store = storage_context.vector_stores[self.image_namespace]

        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            embed_model=embed_model,
            storage_context=storage_context,
            show_progress=show_progress,
            use_async=use_async,
            store_nodes_override=store_nodes_override,
            **kwargs,
        )

    @property
    defimage_vector_store(self) -> BasePydanticVectorStore:
        return self._image_vector_store

    @property
    defimage_embed_model(self) -> MultiModalEmbedding:
        return self._image_embed_model

    @property
    defis_image_vector_store_empty(self) -> bool:
        return self._is_image_vector_store_empty

    @property
    defis_text_vector_store_empty(self) -> bool:
        return self._is_text_vector_store_empty

    defas_retriever(self, **kwargs: Any) -> MultiModalVectorIndexRetriever:
        return MultiModalVectorIndexRetriever(
            self,
            node_ids=list(self.index_struct.nodes_dict.values()),
            **kwargs,
        )

    defas_query_engine(
        self,
        llm: Optional[LLMType] = None,
        **kwargs: Any,
    ) -> SimpleMultiModalQueryEngine:
        retriever = cast(MultiModalVectorIndexRetriever, self.as_retriever(**kwargs))

        llm = llm or Settings.llm
        assert isinstance(llm, (BaseLLM, MultiModalLLM))
        class_name = llm.class_name()
        if "multi" not in class_name:
            logger.warning(
                f"Warning: {class_name} does not appear to be a multi-modal LLM. This may not work as expected."
            )

        return SimpleMultiModalQueryEngine(
            retriever,
            multi_modal_llm=llm,  # type: ignore
            **kwargs,
        )

    defas_chat_engine(
        self,
        chat_mode: ChatMode = ChatMode.BEST,
        llm: Optional[LLMType] = None,
        **kwargs: Any,
    ) -> BaseChatEngine:
        llm = llm or Settings.llm
        assert isinstance(llm, (BaseLLM, MultiModalLLM))
        llm = cast(LLM, llm)  # kludge. They don't actually inherit from these types.
        class_name = llm.class_name()
        if "multi" not in class_name:
            logger.warning(
                f"Warning: {class_name} does not appear to be a multi-modal LLM. This may not work as expected."
            )

        if chat_mode == ChatMode.CONTEXT:
            fromllama_index.core.chat_engine.multi_modal_contextimport (
                MultiModalContextChatEngine,
            )

            return MultiModalContextChatEngine.from_defaults(
                retriever=self.as_retriever(**kwargs),
                multi_modal_llm=llm,
                **kwargs,
            )

        if chat_mode == ChatMode.CONDENSE_PLUS_CONTEXT:
            fromllama_index.core.chat_engine.multi_modal_condense_plus_contextimport (
                MultiModalCondensePlusContextChatEngine,
            )

            return MultiModalCondensePlusContextChatEngine.from_defaults(
                retriever=self.as_retriever(**kwargs),
                multi_modal_llm=llm,
                **kwargs,
            )

        return super().as_chat_engine(chat_mode, llm, **kwargs)

    @classmethod
    deffrom_vector_store(
        cls,
        vector_store: BasePydanticVectorStore,
        embed_model: Optional[EmbedType] = None,
        # Image-related kwargs
        image_vector_store: Optional[BasePydanticVectorStore] = None,
        image_embed_model: EmbedType = "clip",
        **kwargs: Any,
    ) -> "MultiModalVectorStoreIndex":
        if not vector_store.stores_text:
            raise ValueError(
                "Cannot initialize from a vector store that does not store text."
            )

        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return cls(
            nodes=[],
            storage_context=storage_context,
            image_vector_store=image_vector_store,
            image_embed_model=image_embed_model,
            embed_model=(
                resolve_embed_model(
                    embed_model, callback_manager=kwargs.get("callback_manager")
                )
                if embed_model
                else Settings.embed_model
            ),
            **kwargs,
        )

    def_get_node_with_embedding(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        is_image: bool = False,
    ) -> List[BaseNode]:
"""
        Get tuples of id, node, and embedding.

        Allows us to store these nodes in a vector store.
        Embeddings are called in batches.

        """
        id_to_text_embed_map = None

        if is_image:
            assert all(isinstance(node, ImageNode) for node in nodes)
            id_to_embed_map = embed_image_nodes(
                nodes,  # type: ignore
                embed_model=self._image_embed_model,
                show_progress=show_progress,
            )

            # text field is populate, so embed them
            if self._is_image_to_text:
                id_to_text_embed_map = embed_nodes(
                    nodes,
                    embed_model=self._embed_model,
                    show_progress=show_progress,
                )
                # TODO: refactor this change of image embed model to same as text
                self._image_embed_model = self._embed_model  # type: ignore

        else:
            id_to_embed_map = embed_nodes(
                nodes,
                embed_model=self._embed_model,
                show_progress=show_progress,
            )

        results = []
        for node in nodes:
            embedding = id_to_embed_map[node.node_id]
            result = node.model_copy()
            result.embedding = embedding
            if is_image and id_to_text_embed_map:
                assert isinstance(result, ImageNode)
                text_embedding = id_to_text_embed_map[node.node_id]
                result.text_embedding = text_embedding
                result.embedding = (
                    text_embedding  # TODO: re-factor to make use of both embeddings
                )
            results.append(result)
        return results

    async def_aget_node_with_embedding(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        is_image: bool = False,
    ) -> List[BaseNode]:
"""
        Asynchronously get tuples of id, node, and embedding.

        Allows us to store these nodes in a vector store.
        Embeddings are called in batches.

        """
        id_to_text_embed_map = None

        if is_image:
            assert all(isinstance(node, ImageNode) for node in nodes)
            id_to_embed_map = await async_embed_image_nodes(
                nodes,  # type: ignore
                embed_model=self._image_embed_model,
                show_progress=show_progress,
            )

            if self._is_image_to_text:
                id_to_text_embed_map = await async_embed_nodes(
                    nodes,
                    embed_model=self._embed_model,
                    show_progress=show_progress,
                )
                # TODO: refactor this change of image embed model to same as text
                self._image_embed_model = self._embed_model  # type: ignore

        else:
            id_to_embed_map = await async_embed_nodes(
                nodes,
                embed_model=self._embed_model,
                show_progress=show_progress,
            )

        results = []
        for node in nodes:
            embedding = id_to_embed_map[node.node_id]
            result = node.model_copy()
            result.embedding = embedding
            if is_image and id_to_text_embed_map:
                assert isinstance(result, ImageNode)
                text_embedding = id_to_text_embed_map[node.node_id]
                result.text_embedding = text_embedding
                result.embedding = (
                    text_embedding  # TODO: re-factor to make use of both embeddings
                )
            results.append(result)
        return results

    async def_async_add_nodes_to_index(
        self,
        index_struct: IndexDict,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **insert_kwargs: Any,
    ) -> None:
"""Asynchronously add nodes to index."""
        if not nodes:
            return

        image_nodes: List[ImageNode] = []
        text_nodes: List[BaseNode] = []
        new_text_ids: List[str] = []
        new_img_ids: List[str] = []

        for node in nodes:
            if isinstance(node, ImageNode):
                image_nodes.append(node)
            if isinstance(node, TextNode) and node.text:
                text_nodes.append(node)

        if len(text_nodes)  0:
            # embed all nodes as text - include image nodes that have text attached
            text_nodes = await self._aget_node_with_embedding(
                text_nodes, show_progress, is_image=False
            )
            new_text_ids = await self.storage_context.vector_stores[
                DEFAULT_VECTOR_STORE
            ].async_add(text_nodes, **insert_kwargs)
        else:
            self._is_text_vector_store_empty = True

        if len(image_nodes)  0:
            # embed image nodes as images directly
            image_nodes = await self._aget_node_with_embedding(  # type: ignore
                image_nodes,
                show_progress,
                is_image=True,
            )
            new_img_ids = await self.storage_context.vector_stores[
                self.image_namespace
            ].async_add(image_nodes, **insert_kwargs)
        else:
            self._is_image_vector_store_empty = True

        # if the vector store doesn't store text, we need to add the nodes to the
        # index struct and document store
        all_nodes = text_nodes + image_nodes
        all_new_ids = new_text_ids + new_img_ids
        if not self._vector_store.stores_text or self._store_nodes_override:
            for node, new_id in zip(all_nodes, all_new_ids):
                # NOTE: remove embedding from node to avoid duplication
                node_without_embedding = node.model_copy()
                node_without_embedding.embedding = None

                index_struct.add_node(node_without_embedding, text_id=new_id)
                self._docstore.add_documents(
                    [node_without_embedding], allow_update=True
                )

    def_add_nodes_to_index(
        self,
        index_struct: IndexDict,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **insert_kwargs: Any,
    ) -> None:
"""Add document to index."""
        if not nodes:
            return

        image_nodes: List[ImageNode] = []
        text_nodes: List[TextNode] = []
        new_text_ids: List[str] = []
        new_img_ids: List[str] = []

        for node in nodes:
            if isinstance(node, ImageNode):
                image_nodes.append(node)
            if isinstance(node, TextNode) and node.text:
                text_nodes.append(node)

        if len(text_nodes)  0:
            # embed all nodes as text - include image nodes that have text attached
            text_nodes = self._get_node_with_embedding(  # type: ignore
                text_nodes, show_progress, is_image=False
            )
            new_text_ids = self.storage_context.vector_stores[DEFAULT_VECTOR_STORE].add(
                text_nodes, **insert_kwargs
            )
        else:
            self._is_text_vector_store_empty = True

        if len(image_nodes)  0:
            # embed image nodes as images directly
            # check if we should use text embedding for images instead of default
            image_nodes = self._get_node_with_embedding(  # type: ignore
                image_nodes,
                show_progress,
                is_image=True,
            )
            new_img_ids = self.storage_context.vector_stores[self.image_namespace].add(
                image_nodes, **insert_kwargs
            )
        else:
            self._is_image_vector_store_empty = True

        # if the vector store doesn't store text, we need to add the nodes to the
        # index struct and document store
        all_nodes = text_nodes + image_nodes
        all_new_ids = new_text_ids + new_img_ids
        if not self._vector_store.stores_text or self._store_nodes_override:
            for node, new_id in zip(all_nodes, all_new_ids):
                # NOTE: remove embedding from node to avoid duplication
                node_without_embedding = node.model_copy()
                node_without_embedding.embedding = None

                index_struct.add_node(node_without_embedding, text_id=new_id)
                self._docstore.add_documents(
                    [node_without_embedding], allow_update=True
                )

    defdelete_ref_doc(
        self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
    ) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
        # delete from all vector stores

        for vector_store in self._storage_context.vector_stores.values():
            vector_store.delete(ref_doc_id)

            if self._store_nodes_override or self._vector_store.stores_text:
                ref_doc_info = self._docstore.get_ref_doc_info(ref_doc_id)
                if ref_doc_info is not None:
                    for node_id in ref_doc_info.node_ids:
                        self._index_struct.delete(node_id)
                        self._vector_store.delete(node_id)

        if delete_from_docstore:
            self._docstore.delete_ref_doc(ref_doc_id, raise_error=False)

        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  delete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.MultiModalVectorStoreIndex.delete_ref_doc "Permanent link")

```
delete_ref_doc(
    ref_doc_id: ,
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a document and it's nodes by using ref_doc_id.
Source code in `llama-index-core/llama_index/core/indices/multi_modal/base.py`  
| 
```
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
```
 | 
```
defdelete_ref_doc(
    self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
    # delete from all vector stores

    for vector_store in self._storage_context.vector_stores.values():
        vector_store.delete(ref_doc_id)

        if self._store_nodes_override or self._vector_store.stores_text:
            ref_doc_info = self._docstore.get_ref_doc_info(ref_doc_id)
            if ref_doc_info is not None:
                for node_id in ref_doc_info.node_ids:
                    self._index_struct.delete(node_id)
                    self._vector_store.delete(node_id)

    if delete_from_docstore:
        self._docstore.delete_ref_doc(ref_doc_id, raise_error=False)

    self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
##  SQLStructStoreIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.SQLStructStoreIndex "Permanent link")
Bases: `BaseStructStoreIndex[SQLStructTable]`
SQL Struct Store Index.
The SQLStructStoreIndex is an index that uses a SQL database under the hood. During index construction, the data can be inferred from unstructured documents given a schema extract prompt, or it can be pre-loaded in the database.
During query time, the user can either specify a raw SQL query or a natural language query to retrieve their data.
NOTE: this is deprecated.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `documents`  |  `Optional[Sequence[DOCUMENTS_INPUT]]`  |  Documents to index. NOTE: in the SQL index, this is an optional field.  |  _required_  |  
|  `sql_database`  |  `Optional[SQLDatabase[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase "SQLDatabase \(llama_index.core.utilities.sql_wrapper.SQLDatabase\)")]`  |  SQL database to use, including table names to specify. See :ref:`Ref-Struct-Store` for more details.  |  `None`  |  
|  `table_name`  |  `Optional[str]`  |  Name of the table to use for extracting data. Either table_name or table must be specified.  |  `None`  |  
|  `table`  |  `Optional[Table]`  |  SQLAlchemy Table object to use. Specifying the Table object explicitly, instead of the table name, allows you to pass in a view. Either table_name or table must be specified.  |  `None`  |  
|  `sql_context_container`  |  `Optional[SQLContextContainer]`  |  SQL context container. an be generated from a SQLContextContainerBuilder. See :ref:`Ref-Struct-Store` for more details.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/indices/struct_store/sql.py`  
| 
```
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
```
 | 
```
classSQLStructStoreIndex(BaseStructStoreIndex[SQLStructTable]):
"""
    SQL Struct Store Index.

    The SQLStructStoreIndex is an index that uses a SQL database
    under the hood. During index construction, the data can be inferred
    from unstructured documents given a schema extract prompt,
    or it can be pre-loaded in the database.

    During query time, the user can either specify a raw SQL query
    or a natural language query to retrieve their data.

    NOTE: this is deprecated.

    Args:
        documents (Optional[Sequence[DOCUMENTS_INPUT]]): Documents to index.
            NOTE: in the SQL index, this is an optional field.
        sql_database (Optional[SQLDatabase]): SQL database to use,
            including table names to specify.
            See :ref:`Ref-Struct-Store` for more details.
        table_name (Optional[str]): Name of the table to use
            for extracting data.
            Either table_name or table must be specified.
        table (Optional[Table]): SQLAlchemy Table object to use.
            Specifying the Table object explicitly, instead of
            the table name, allows you to pass in a view.
            Either table_name or table must be specified.
        sql_context_container (Optional[SQLContextContainer]): SQL context container.
            an be generated from a SQLContextContainerBuilder.
            See :ref:`Ref-Struct-Store` for more details.

    """

    index_struct_cls = SQLStructTable

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        index_struct: Optional[SQLStructTable] = None,
        sql_database: Optional[SQLDatabase] = None,
        table_name: Optional[str] = None,
        table: Optional[Table] = None,
        ref_doc_id_column: Optional[str] = None,
        sql_context_container: Optional[SQLContextContainer] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        if sql_database is None:
            raise ValueError("sql_database must be specified")
        self.sql_database = sql_database
        # needed here for data extractor
        self._ref_doc_id_column = ref_doc_id_column
        self._table_name = table_name
        self._table = table

        # if documents aren't specified, pass in a blank []
        if index_struct is None:
            nodes = nodes or []

        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            **kwargs,
        )

        # TODO: index_struct context_dict is deprecated,
        # we're migrating storage of information to here.
        if sql_context_container is None:
            container_builder = SQLContextContainerBuilder(sql_database)
            sql_context_container = container_builder.build_context_container()
        self.sql_context_container = sql_context_container

    @property
    defref_doc_id_column(self) -> Optional[str]:
        return self._ref_doc_id_column

    def_build_index_from_nodes(
        self, nodes: Sequence[BaseNode], **build_kwargs: Any
    ) -> SQLStructTable:
"""Build index from nodes."""
        index_struct = self.index_struct_cls()
        if len(nodes) == 0:
            return index_struct
        else:
            data_extractor = SQLStructDatapointExtractor(
                Settings.llm,
                self.schema_extract_prompt,
                self.output_parser,
                self.sql_database,
                table_name=self._table_name,
                table=self._table,
                ref_doc_id_column=self._ref_doc_id_column,
            )
            # group nodes by ids
            source_to_node = defaultdict(list)
            for node in nodes:
                source_to_node[node.ref_doc_id].append(node)

            for node_set in source_to_node.values():
                data_extractor.insert_datapoint_from_nodes(node_set)
        return index_struct

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a document."""
        data_extractor = SQLStructDatapointExtractor(
            Settings.llm,
            self.schema_extract_prompt,
            self.output_parser,
            self.sql_database,
            table_name=self._table_name,
            table=self._table,
            ref_doc_id_column=self._ref_doc_id_column,
        )
        data_extractor.insert_datapoint_from_nodes(nodes)

    defas_retriever(self, **kwargs: Any) -> BaseRetriever:
        raise NotImplementedError("Not supported")

    defas_query_engine(
        self,
        llm: Optional[LLMType] = None,
        query_mode: Union[str, SQLQueryMode] = SQLQueryMode.NL,
        **kwargs: Any,
    ) -> BaseQueryEngine:
        # NOTE: lazy import
        fromllama_index.core.indices.struct_store.sql_queryimport (
            NLStructStoreQueryEngine,
            SQLStructStoreQueryEngine,
        )

        if query_mode == SQLQueryMode.NL:
            return NLStructStoreQueryEngine(self, **kwargs)
        elif query_mode == SQLQueryMode.SQL:
            return SQLStructStoreQueryEngine(self, **kwargs)
        else:
            raise ValueError(f"Unknown query mode: {query_mode}")

```
 |  
| --- | --- |  
##  TreeIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.TreeIndex "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[IndexGraph]`
Tree Index.
The tree index is a tree-structured index, where each node is a summary of the children nodes. During index construction, the tree is constructed in a bottoms-up fashion until we end up with a set of root_nodes.
There are a few different options during query time (see :ref:`Ref-Query`). The main option is to traverse down the tree from the root nodes. A secondary answer is to directly synthesize the answer from the root nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `summary_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Summarization Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `insert_prompt`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  An Tree Insertion Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `num_children`  |  The number of children each node should have.  |  
|  `build_tree`  |  `bool`  |  Whether to build the tree during index construction.  |  `True`  |  
|  `show_progress`  |  `bool`  |  Whether to show progress bars. Defaults to False.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/tree/base.py`  
| 
```
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
```
 | 
```
classTreeIndex(BaseIndex[IndexGraph]):
"""
    Tree Index.

    The tree index is a tree-structured index, where each node is a summary of
    the children nodes. During index construction, the tree is constructed
    in a bottoms-up fashion until we end up with a set of root_nodes.

    There are a few different options during query time (see :ref:`Ref-Query`).
    The main option is to traverse down the tree from the root nodes.
    A secondary answer is to directly synthesize the answer from the root nodes.

    Args:
        summary_template (Optional[BasePromptTemplate]): A Summarization Prompt
            (see :ref:`Prompt-Templates`).
        insert_prompt (Optional[BasePromptTemplate]): An Tree Insertion Prompt
            (see :ref:`Prompt-Templates`).
        num_children (int): The number of children each node should have.
        build_tree (bool): Whether to build the tree during index construction.
        show_progress (bool): Whether to show progress bars. Defaults to False.

    """

    index_struct_cls = IndexGraph

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[IndexGraph] = None,
        llm: Optional[LLM] = None,
        summary_template: Optional[BasePromptTemplate] = None,
        insert_prompt: Optional[BasePromptTemplate] = None,
        num_children: int = 10,
        build_tree: bool = True,
        use_async: bool = False,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        # need to set parameters before building index in base class.
        self.num_children = num_children
        self.summary_template = summary_template or DEFAULT_SUMMARY_PROMPT
        self.insert_prompt: BasePromptTemplate = insert_prompt or DEFAULT_INSERT_PROMPT
        self.build_tree = build_tree
        self._use_async = use_async
        self._llm = llm or Settings.llm
        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            show_progress=show_progress,
            objects=objects,
            **kwargs,
        )

    defas_retriever(
        self,
        retriever_mode: Union[str, TreeRetrieverMode] = TreeRetrieverMode.SELECT_LEAF,
        embed_model: Optional[BaseEmbedding] = None,
        **kwargs: Any,
    ) -> BaseRetriever:
        # NOTE: lazy import
        fromllama_index.core.indices.tree.all_leaf_retrieverimport (
            TreeAllLeafRetriever,
        )
        fromllama_index.core.indices.tree.select_leaf_embedding_retrieverimport (
            TreeSelectLeafEmbeddingRetriever,
        )
        fromllama_index.core.indices.tree.select_leaf_retrieverimport (
            TreeSelectLeafRetriever,
        )
        fromllama_index.core.indices.tree.tree_root_retrieverimport (
            TreeRootRetriever,
        )

        self._validate_build_tree_required(TreeRetrieverMode(retriever_mode))

        if retriever_mode == TreeRetrieverMode.SELECT_LEAF:
            return TreeSelectLeafRetriever(self, object_map=self._object_map, **kwargs)
        elif retriever_mode == TreeRetrieverMode.SELECT_LEAF_EMBEDDING:
            embed_model = embed_model or Settings.embed_model
            return TreeSelectLeafEmbeddingRetriever(
                self, embed_model=embed_model, object_map=self._object_map, **kwargs
            )
        elif retriever_mode == TreeRetrieverMode.ROOT:
            return TreeRootRetriever(self, object_map=self._object_map, **kwargs)
        elif retriever_mode == TreeRetrieverMode.ALL_LEAF:
            return TreeAllLeafRetriever(self, object_map=self._object_map, **kwargs)
        else:
            raise ValueError(f"Unknown retriever mode: {retriever_mode}")

    def_validate_build_tree_required(self, retriever_mode: TreeRetrieverMode) -> None:
"""Check if index supports modes that require trees."""
        if retriever_mode in REQUIRE_TREE_MODES and not self.build_tree:
            raise ValueError(
                "Index was constructed without building trees, "
                f"but retriever mode {retriever_mode} requires trees."
            )

    def_build_index_from_nodes(
        self, nodes: Sequence[BaseNode], **build_kwargs: Any
    ) -> IndexGraph:
"""Build the index from nodes."""
        index_builder = GPTTreeIndexBuilder(
            self.num_children,
            self.summary_template,
            llm=self._llm,
            use_async=self._use_async,
            show_progress=self._show_progress,
            docstore=self._docstore,
        )
        return index_builder.build_from_nodes(nodes, build_tree=self.build_tree)

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a document."""
        # TODO: allow to customize insert prompt
        inserter = TreeIndexInserter(
            self.index_struct,
            llm=self._llm,
            num_children=self.num_children,
            insert_prompt=self.insert_prompt,
            summary_prompt=self.summary_template,
            docstore=self._docstore,
        )
        inserter.insert(nodes)

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
"""Delete a node."""
        raise NotImplementedError("Delete not implemented for tree index.")

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        node_doc_ids = list(self.index_struct.all_nodes.values())
        nodes = self.docstore.get_nodes(node_doc_ids)

        all_ref_doc_info = {}
        for node in nodes:
            ref_node = node.source_node
            if not ref_node:
                continue

            ref_doc_info = self.docstore.get_ref_doc_info(ref_node.node_id)
            if not ref_doc_info:
                continue

            all_ref_doc_info[ref_node.node_id] = ref_doc_info
        return all_ref_doc_info

```
 |  
| --- | --- |  
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.TreeIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
##  VectorStoreIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.VectorStoreIndex "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[IndexDict]`
Vector Store Index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `use_async`  |  `bool`  |  Whether to use asynchronous calls. Defaults to False.  |  `False`  |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
|  `store_nodes_override`  |  `bool`  |  set to True to always store Node objects in index store and document store even if vector store keeps text. Defaults to False  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
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
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
```
 | 
```
classVectorStoreIndex(BaseIndex[IndexDict]):
"""
    Vector Store Index.

    Args:
        use_async (bool): Whether to use asynchronous calls. Defaults to False.
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
        store_nodes_override (bool): set to True to always store Node objects in index
            store and document store even if vector store keeps text. Defaults to False

    """

    index_struct_cls = IndexDict

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        # vector store index params
        use_async: bool = False,
        store_nodes_override: bool = False,
        embed_model: Optional[EmbedType] = None,
        insert_batch_size: int = 2048,
        # parent class params
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[IndexDict] = None,
        storage_context: Optional[StorageContext] = None,
        callback_manager: Optional[CallbackManager] = None,
        transformations: Optional[List[TransformComponent]] = None,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._use_async = use_async
        self._store_nodes_override = store_nodes_override
        self._embed_model = resolve_embed_model(
            embed_model or Settings.embed_model, callback_manager=callback_manager
        )

        self._insert_batch_size = insert_batch_size
        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            storage_context=storage_context,
            show_progress=show_progress,
            objects=objects,
            callback_manager=callback_manager,
            transformations=transformations,
            **kwargs,
        )

    @classmethod
    deffrom_vector_store(
        cls,
        vector_store: BasePydanticVectorStore,
        embed_model: Optional[EmbedType] = None,
        **kwargs: Any,
    ) -> "VectorStoreIndex":
        if not vector_store.stores_text:
            raise ValueError(
                "Cannot initialize from a vector store that does not store text."
            )

        kwargs.pop("storage_context", None)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        return cls(
            nodes=[],
            embed_model=embed_model,
            storage_context=storage_context,
            **kwargs,
        )

    @property
    defvector_store(self) -> BasePydanticVectorStore:
        return self._vector_store

    defas_retriever(self, **kwargs: Any) -> BaseRetriever:
        # NOTE: lazy import
        fromllama_index.core.indices.vector_store.retrieversimport (
            VectorIndexRetriever,
        )

        return VectorIndexRetriever(
            self,
            node_ids=list(self.index_struct.nodes_dict.values()),
            callback_manager=self._callback_manager,
            object_map=self._object_map,
            **kwargs,
        )

    def_get_node_with_embedding(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
    ) -> List[BaseNode]:
"""
        Get tuples of id, node, and embedding.

        Allows us to store these nodes in a vector store.
        Embeddings are called in batches.

        """
        id_to_embed_map = embed_nodes(
            nodes, self._embed_model, show_progress=show_progress
        )

        results = []
        for node in nodes:
            embedding = id_to_embed_map[node.node_id]
            result = node.model_copy()
            result.embedding = embedding
            results.append(result)
        return results

    async def_aget_node_with_embedding(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
    ) -> List[BaseNode]:
"""
        Asynchronously get tuples of id, node, and embedding.

        Allows us to store these nodes in a vector store.
        Embeddings are called in batches.

        """
        id_to_embed_map = await async_embed_nodes(
            nodes=nodes,
            embed_model=self._embed_model,
            show_progress=show_progress,
        )

        results = []
        for node in nodes:
            embedding = id_to_embed_map[node.node_id]
            result = node.model_copy()
            result.embedding = embedding
            results.append(result)
        return results

    async def_async_add_nodes_to_index(
        self,
        index_struct: IndexDict,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **insert_kwargs: Any,
    ) -> None:
"""Asynchronously add nodes to index."""
        if not nodes:
            return

        for nodes_batch in iter_batch(nodes, self._insert_batch_size):
            nodes_batch = await self._aget_node_with_embedding(
                nodes_batch, show_progress
            )
            new_ids = await self._vector_store.async_add(nodes_batch, **insert_kwargs)

            # if the vector store doesn't store text, we need to add the nodes to the
            # index struct and document store
            if not self._vector_store.stores_text or self._store_nodes_override:
                for node, new_id in zip(nodes_batch, new_ids):
                    # NOTE: remove embedding from node to avoid duplication
                    node_without_embedding = node.model_copy()
                    node_without_embedding.embedding = None

                    index_struct.add_node(node_without_embedding, text_id=new_id)
                    await self._docstore.async_add_documents(
                        [node_without_embedding], allow_update=True
                    )
            else:
                # NOTE: if the vector store keeps text,
                # we only need to add image and index nodes
                for node, new_id in zip(nodes_batch, new_ids):
                    if isinstance(node, (ImageNode, IndexNode)):
                        # NOTE: remove embedding from node to avoid duplication
                        node_without_embedding = node.model_copy()
                        node_without_embedding.embedding = None

                        index_struct.add_node(node_without_embedding, text_id=new_id)
                        await self._docstore.async_add_documents(
                            [node_without_embedding], allow_update=True
                        )

    def_add_nodes_to_index(
        self,
        index_struct: IndexDict,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **insert_kwargs: Any,
    ) -> None:
"""Add document to index."""
        if not nodes:
            return

        for nodes_batch in iter_batch(nodes, self._insert_batch_size):
            nodes_batch = self._get_node_with_embedding(nodes_batch, show_progress)
            new_ids = self._vector_store.add(nodes_batch, **insert_kwargs)

            if not self._vector_store.stores_text or self._store_nodes_override:
                # NOTE: if the vector store doesn't store text,
                # we need to add the nodes to the index struct and document store
                for node, new_id in zip(nodes_batch, new_ids):
                    # NOTE: remove embedding from node to avoid duplication
                    node_without_embedding = node.model_copy()
                    node_without_embedding.embedding = None

                    index_struct.add_node(node_without_embedding, text_id=new_id)
                    self._docstore.add_documents(
                        [node_without_embedding], allow_update=True
                    )
            else:
                # NOTE: if the vector store keeps text,
                # we only need to add image and index nodes
                for node, new_id in zip(nodes_batch, new_ids):
                    if isinstance(node, (ImageNode, IndexNode)):
                        # NOTE: remove embedding from node to avoid duplication
                        node_without_embedding = node.model_copy()
                        node_without_embedding.embedding = None

                        index_struct.add_node(node_without_embedding, text_id=new_id)
                        self._docstore.add_documents(
                            [node_without_embedding], allow_update=True
                        )

    def_build_index_from_nodes(
        self,
        nodes: Sequence[BaseNode],
        **insert_kwargs: Any,
    ) -> IndexDict:
"""Build index from nodes."""
        index_struct = self.index_struct_cls()
        if self._use_async:
            tasks = [
                self._async_add_nodes_to_index(
                    index_struct,
                    nodes,
                    show_progress=self._show_progress,
                    **insert_kwargs,
                )
            ]
            run_async_tasks(tasks)
        else:
            self._add_nodes_to_index(
                index_struct,
                nodes,
                show_progress=self._show_progress,
                **insert_kwargs,
            )
        return index_struct

    defbuild_index_from_nodes(
        self,
        nodes: Sequence[BaseNode],
        **insert_kwargs: Any,
    ) -> IndexDict:
"""
        Build the index from nodes.

        NOTE: Overrides BaseIndex.build_index_from_nodes.
            VectorStoreIndex only stores nodes in document store
            if vector store does not store text
        """
        # Filter out the nodes that don't have content
        content_nodes = [
            node
            for node in nodes
            if node.get_content(metadata_mode=MetadataMode.EMBED) != ""
        ]

        # Report if some nodes are missing content
        if len(content_nodes) != len(nodes):
            print("Some nodes are missing content, skipping them...")

        return self._build_index_from_nodes(content_nodes, **insert_kwargs)

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a document."""
        self._add_nodes_to_index(self._index_struct, nodes, **insert_kwargs)

    def_validate_serializable(self, nodes: Sequence[BaseNode]) -> None:
"""Validate that the nodes are serializable."""
        for node in nodes:
            if isinstance(node, IndexNode):
                try:
                    node.dict()
                except ValueError:
                    self._object_map[node.index_id] = node.obj
                    node.obj = None

    async defainsert_nodes(
        self, nodes: Sequence[BaseNode], **insert_kwargs: Any
    ) -> None:
"""
        Insert nodes.

        NOTE: overrides BaseIndex.ainsert_nodes.
            VectorStoreIndex only stores nodes in document store
            if vector store does not store text
        """
        self._validate_serializable(nodes)

        with self._callback_manager.as_trace("insert_nodes"):
            await self._async_add_nodes_to_index(
                self._index_struct, nodes, **insert_kwargs
            )
            self._storage_context.index_store.add_index_struct(self._index_struct)

    definsert_nodes(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""
        Insert nodes.

        NOTE: overrides BaseIndex.insert_nodes.
            VectorStoreIndex only stores nodes in document store
            if vector store does not store text
        """
        self._validate_serializable(nodes)

        with self._callback_manager.as_trace("insert_nodes"):
            self._insert(nodes, **insert_kwargs)
            self._storage_context.index_store.add_index_struct(self._index_struct)

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
        pass

    async defadelete_nodes(
        self,
        node_ids: List[str],
        delete_from_docstore: bool = False,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete a list of nodes from the index.

        Args:
            node_ids (List[str]): A list of node_ids from the nodes to delete

        """
        # delete nodes from vector store
        await self._vector_store.adelete_nodes(node_ids, **delete_kwargs)

        # delete from docstore only if needed
        if (
            not self._vector_store.stores_text or self._store_nodes_override
        ) and delete_from_docstore:
            for node_id in node_ids:
                self._index_struct.delete(node_id)
                await self._docstore.adelete_document(node_id, raise_error=False)
            self._storage_context.index_store.add_index_struct(self._index_struct)

    defdelete_nodes(
        self,
        node_ids: List[str],
        delete_from_docstore: bool = False,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete a list of nodes from the index.

        Args:
            node_ids (List[str]): A list of node_ids from the nodes to delete

        """
        # delete nodes from vector store
        self._vector_store.delete_nodes(node_ids, **delete_kwargs)

        # delete from docstore only if needed
        if (
            not self._vector_store.stores_text or self._store_nodes_override
        ) and delete_from_docstore:
            for node_id in node_ids:
                self._index_struct.delete(node_id)
                self._docstore.delete_document(node_id, raise_error=False)
            self._storage_context.index_store.add_index_struct(self._index_struct)

    def_delete_from_index_struct(self, ref_doc_id: str) -> None:
        # delete from index_struct only if needed
        if not self._vector_store.stores_text or self._store_nodes_override:
            ref_doc_info = self._docstore.get_ref_doc_info(ref_doc_id)
            if ref_doc_info is not None:
                for node_id in ref_doc_info.node_ids:
                    self._index_struct.delete(node_id)

    def_delete_from_docstore(self, ref_doc_id: str) -> None:
        # delete from docstore only if needed
        if not self._vector_store.stores_text or self._store_nodes_override:
            self._docstore.delete_ref_doc(ref_doc_id, raise_error=False)

    defdelete_ref_doc(
        self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
    ) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
        self._vector_store.delete(ref_doc_id, **delete_kwargs)
        self._delete_from_index_struct(ref_doc_id)
        if delete_from_docstore:
            self._delete_from_docstore(ref_doc_id)
        self._storage_context.index_store.add_index_struct(self._index_struct)

    async def_adelete_from_index_struct(self, ref_doc_id: str) -> None:
"""Delete from index_struct only if needed."""
        if not self._vector_store.stores_text or self._store_nodes_override:
            ref_doc_info = await self._docstore.aget_ref_doc_info(ref_doc_id)
            if ref_doc_info is not None:
                for node_id in ref_doc_info.node_ids:
                    self._index_struct.delete(node_id)

    async def_adelete_from_docstore(self, ref_doc_id: str) -> None:
"""Delete from docstore only if needed."""
        if not self._vector_store.stores_text or self._store_nodes_override:
            await self._docstore.adelete_ref_doc(ref_doc_id, raise_error=False)

    async defadelete_ref_doc(
        self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
    ) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
        tasks = [
            self._vector_store.adelete(ref_doc_id, **delete_kwargs),
            self._adelete_from_index_struct(ref_doc_id),
        ]
        if delete_from_docstore:
            tasks.append(self._adelete_from_docstore(ref_doc_id))

        await asyncio.gather(*tasks)

        self._storage_context.index_store.add_index_struct(self._index_struct)

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        if not self._vector_store.stores_text or self._store_nodes_override:
            node_doc_ids = list(self.index_struct.nodes_dict.values())
            nodes = self.docstore.get_nodes(node_doc_ids)

            all_ref_doc_info = {}
            for node in nodes:
                ref_node = node.source_node
                if not ref_node:
                    continue

                ref_doc_info = self.docstore.get_ref_doc_info(ref_node.node_id)
                if not ref_doc_info:
                    continue

                all_ref_doc_info[ref_node.node_id] = ref_doc_info
            return all_ref_doc_info
        else:
            raise NotImplementedError(
                "Vector store integrations that store text in the vector store are "
                "not supported by ref_doc_info yet."
            )

```
 |  
| --- | --- |  
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.VectorStoreIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
###  build_index_from_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.VectorStoreIndex.build_index_from_nodes "Permanent link")

```
build_index_from_nodes(
    nodes: Sequence[], **insert_kwargs: 
) -> IndexDict

```

Build the index from nodes.
Overrides BaseIndex.build_index_from_nodes.
VectorStoreIndex only stores nodes in document store if vector store does not store text
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
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
300
301
302
303
304
305
306
307
308
309
```
 | 
```
defbuild_index_from_nodes(
    self,
    nodes: Sequence[BaseNode],
    **insert_kwargs: Any,
) -> IndexDict:
"""
    Build the index from nodes.

    NOTE: Overrides BaseIndex.build_index_from_nodes.
        VectorStoreIndex only stores nodes in document store
        if vector store does not store text
    """
    # Filter out the nodes that don't have content
    content_nodes = [
        node
        for node in nodes
        if node.get_content(metadata_mode=MetadataMode.EMBED) != ""
    ]

    # Report if some nodes are missing content
    if len(content_nodes) != len(nodes):
        print("Some nodes are missing content, skipping them...")

    return self._build_index_from_nodes(content_nodes, **insert_kwargs)

```
 |  
| --- | --- |  
###  ainsert_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.VectorStoreIndex.ainsert_nodes "Permanent link")

```
ainsert_nodes(
    nodes: Sequence[], **insert_kwargs: 
) -> None

```

Insert nodes.
overrides BaseIndex.ainsert_nodes.
VectorStoreIndex only stores nodes in document store if vector store does not store text
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
```
 | 
```
async defainsert_nodes(
    self, nodes: Sequence[BaseNode], **insert_kwargs: Any
) -> None:
"""
    Insert nodes.

    NOTE: overrides BaseIndex.ainsert_nodes.
        VectorStoreIndex only stores nodes in document store
        if vector store does not store text
    """
    self._validate_serializable(nodes)

    with self._callback_manager.as_trace("insert_nodes"):
        await self._async_add_nodes_to_index(
            self._index_struct, nodes, **insert_kwargs
        )
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  insert_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.VectorStoreIndex.insert_nodes "Permanent link")

```
insert_nodes(
    nodes: Sequence[], **insert_kwargs: 
) -> None

```

Insert nodes.
overrides BaseIndex.insert_nodes.
VectorStoreIndex only stores nodes in document store if vector store does not store text
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
343
344
345
346
347
348
349
350
351
352
353
354
355
```
 | 
```
definsert_nodes(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""
    Insert nodes.

    NOTE: overrides BaseIndex.insert_nodes.
        VectorStoreIndex only stores nodes in document store
        if vector store does not store text
    """
    self._validate_serializable(nodes)

    with self._callback_manager.as_trace("insert_nodes"):
        self._insert(nodes, **insert_kwargs)
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.VectorStoreIndex.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: [],
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a list of nodes from the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `List[str]`  |  A list of node_ids from the nodes to delete  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: List[str],
    delete_from_docstore: bool = False,
    **delete_kwargs: Any,
) -> None:
"""
    Delete a list of nodes from the index.

    Args:
        node_ids (List[str]): A list of node_ids from the nodes to delete

    """
    # delete nodes from vector store
    await self._vector_store.adelete_nodes(node_ids, **delete_kwargs)

    # delete from docstore only if needed
    if (
        not self._vector_store.stores_text or self._store_nodes_override
    ) and delete_from_docstore:
        for node_id in node_ids:
            self._index_struct.delete(node_id)
            await self._docstore.adelete_document(node_id, raise_error=False)
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.VectorStoreIndex.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: [],
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a list of nodes from the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `List[str]`  |  A list of node_ids from the nodes to delete  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
```
 | 
```
defdelete_nodes(
    self,
    node_ids: List[str],
    delete_from_docstore: bool = False,
    **delete_kwargs: Any,
) -> None:
"""
    Delete a list of nodes from the index.

    Args:
        node_ids (List[str]): A list of node_ids from the nodes to delete

    """
    # delete nodes from vector store
    self._vector_store.delete_nodes(node_ids, **delete_kwargs)

    # delete from docstore only if needed
    if (
        not self._vector_store.stores_text or self._store_nodes_override
    ) and delete_from_docstore:
        for node_id in node_ids:
            self._index_struct.delete(node_id)
            self._docstore.delete_document(node_id, raise_error=False)
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  delete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.VectorStoreIndex.delete_ref_doc "Permanent link")

```
delete_ref_doc(
    ref_doc_id: ,
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a document and it's nodes by using ref_doc_id.
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
423
424
425
426
427
428
429
430
431
```
 | 
```
defdelete_ref_doc(
    self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
    self._vector_store.delete(ref_doc_id, **delete_kwargs)
    self._delete_from_index_struct(ref_doc_id)
    if delete_from_docstore:
        self._delete_from_docstore(ref_doc_id)
    self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  adelete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.VectorStoreIndex.adelete_ref_doc "Permanent link")

```
adelete_ref_doc(
    ref_doc_id: ,
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a document and it's nodes by using ref_doc_id.
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
446
447
448
449
450
451
452
453
454
455
456
457
458
459
```
 | 
```
async defadelete_ref_doc(
    self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
    tasks = [
        self._vector_store.adelete(ref_doc_id, **delete_kwargs),
        self._adelete_from_index_struct(ref_doc_id),
    ]
    if delete_from_docstore:
        tasks.append(self._adelete_from_docstore(ref_doc_id))

    await asyncio.gather(*tasks)

    self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
##  PropertyGraphIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.PropertyGraphIndex "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[IndexLPG]`
An index for a property graph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Optional[Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]]`  |  A list of nodes to insert into the index.  |  `None`  |  
|  `llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.LLM\)")]`  |  The language model to use for extracting triplets. Defaults to `Settings.llm`.  |  `None`  |  
|  `kg_extractors`  |  `Optional[List[TransformComponent[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TransformComponent "TransformComponent \(llama_index.core.schema.TransformComponent\)")]]`  |  A list of transformations to apply to the nodes to extract triplets. Defaults to `[SimpleLLMPathExtractor(llm=llm), ImplicitEdgeExtractor()]`.  |  `None`  |  
|  `property_graph_store`  |  `Optional[PropertyGraphStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore "PropertyGraphStore \(llama_index.core.graph_stores.types.PropertyGraphStore\)")]`  |  The property graph store to use. If not provided, a new `SimplePropertyGraphStore` will be created.  |  `None`  |  
|  `vector_store`  |  `Optional[BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)")]`  |  The vector store index to use, if the graph store does not support vector queries.  |  `None`  |  
|  `use_async`  |  `bool`  |  Whether to use async for transformations. Defaults to `True`.  |  `True`  |  
|  `embed_model`  |  `Optional[EmbedType]`  |  The embedding model to use for embedding nodes. If not provided, `Settings.embed_model` will be used if `embed_kg_nodes=True`.  |  `None`  |  
|  `embed_kg_nodes`  |  `bool`  |  Whether to embed the KG nodes. Defaults to `True`.  |  `True`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.CallbackManager\)")]`  |  The callback manager to use.  |  `None`  |  
|  `transformations`  |  `Optional[List[TransformComponent[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TransformComponent "TransformComponent \(llama_index.core.schema.TransformComponent\)")]]`  |  A list of transformations to apply to the nodes before inserting them into the index. These are applied prior to the `kg_extractors`.  |  `None`  |  
|  `storage_context`  |  `Optional[StorageContext[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.storage.storage_context.StorageContext "StorageContext


  
      dataclass
   \(llama_index.core.storage.storage_context.StorageContext\)")]`  |  The storage context to use.  |  `None`  |  
|  `show_progress`  |  `bool`  |  Whether to show progress bars for transformations. Defaults to `False`.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/base.py`  
| 
```
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
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
```
 | 
```
classPropertyGraphIndex(BaseIndex[IndexLPG]):
"""
    An index for a property graph.

    Args:
        nodes (Optional[Sequence[BaseNode]]):
            A list of nodes to insert into the index.
        llm (Optional[LLM]):
            The language model to use for extracting triplets. Defaults to `Settings.llm`.
        kg_extractors (Optional[List[TransformComponent]]):
            A list of transformations to apply to the nodes to extract triplets.
            Defaults to `[SimpleLLMPathExtractor(llm=llm), ImplicitEdgeExtractor()]`.
        property_graph_store (Optional[PropertyGraphStore]):
            The property graph store to use. If not provided, a new `SimplePropertyGraphStore` will be created.
        vector_store (Optional[BasePydanticVectorStore]):
            The vector store index to use, if the graph store does not support vector queries.
        use_async (bool):
            Whether to use async for transformations. Defaults to `True`.
        embed_model (Optional[EmbedType]):
            The embedding model to use for embedding nodes.
            If not provided, `Settings.embed_model` will be used if `embed_kg_nodes=True`.
        embed_kg_nodes (bool):
            Whether to embed the KG nodes. Defaults to `True`.
        callback_manager (Optional[CallbackManager]):
            The callback manager to use.
        transformations (Optional[List[TransformComponent]]):
            A list of transformations to apply to the nodes before inserting them into the index.
            These are applied prior to the `kg_extractors`.
        storage_context (Optional[StorageContext]):
            The storage context to use.
        show_progress (bool):
            Whether to show progress bars for transformations. Defaults to `False`.

    """

    index_struct_cls = IndexLPG

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        llm: Optional[LLM] = None,
        kg_extractors: Optional[List[TransformComponent]] = None,
        property_graph_store: Optional[PropertyGraphStore] = None,
        # vector related params
        vector_store: Optional[BasePydanticVectorStore] = None,
        use_async: bool = True,
        embed_model: Optional[EmbedType] = None,
        embed_kg_nodes: bool = True,
        # parent class params
        callback_manager: Optional[CallbackManager] = None,
        transformations: Optional[List[TransformComponent]] = None,
        storage_context: Optional[StorageContext] = None,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        storage_context = storage_context or StorageContext.from_defaults(
            property_graph_store=property_graph_store
        )

        # lazily initialize the graph store on the storage context
        if property_graph_store is not None:
            storage_context.property_graph_store = property_graph_store
        elif storage_context.property_graph_store is None:
            storage_context.property_graph_store = SimplePropertyGraphStore()

        if vector_store is not None:
            storage_context.vector_stores[DEFAULT_VECTOR_STORE] = vector_store

        if embed_kg_nodes and (
            storage_context.property_graph_store.supports_vector_queries
            or embed_kg_nodes
        ):
            self._embed_model = (
                resolve_embed_model(embed_model)
                if embed_model
                else Settings.embed_model
            )
        else:
            self._embed_model = None  # type: ignore

        self._kg_extractors = kg_extractors or [
            SimpleLLMPathExtractor(llm=llm or Settings.llm),
            ImplicitPathExtractor(),
        ]
        self._use_async = use_async
        self._llm = llm
        self._embed_kg_nodes = embed_kg_nodes
        self._override_vector_store = (
            vector_store is not None
            or not storage_context.property_graph_store.supports_vector_queries
        )

        super().__init__(
            nodes=nodes,
            callback_manager=callback_manager,
            storage_context=storage_context,
            transformations=transformations,
            show_progress=show_progress,
            **kwargs,
        )

    @classmethod
    deffrom_existing(
        cls: Type["PropertyGraphIndex"],
        property_graph_store: PropertyGraphStore,
        vector_store: Optional[BasePydanticVectorStore] = None,
        # general params
        llm: Optional[LLM] = None,
        kg_extractors: Optional[List[TransformComponent]] = None,
        # vector related params
        use_async: bool = True,
        embed_model: Optional[EmbedType] = None,
        embed_kg_nodes: bool = True,
        # parent class params
        callback_manager: Optional[CallbackManager] = None,
        transformations: Optional[List[TransformComponent]] = None,
        storage_context: Optional[StorageContext] = None,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> "PropertyGraphIndex":
"""Create an index from an existing property graph store (and optional vector store)."""
        return cls(
            nodes=[],  # no nodes to insert
            property_graph_store=property_graph_store,
            vector_store=vector_store,
            llm=llm,
            kg_extractors=kg_extractors,
            use_async=use_async,
            embed_model=embed_model,
            embed_kg_nodes=embed_kg_nodes,
            callback_manager=callback_manager,
            transformations=transformations,
            storage_context=storage_context,
            show_progress=show_progress,
            **kwargs,
        )

    @property
    defproperty_graph_store(self) -> PropertyGraphStore:
"""Get the labelled property graph store."""
        assert self.storage_context.property_graph_store is not None

        return self.storage_context.property_graph_store

    @property
    defvector_store(self) -> Optional[BasePydanticVectorStore]:
        if self._embed_kg_nodes and self._override_vector_store:
            return self.storage_context.vector_store
        else:
            return None

    def_insert_nodes(self, nodes: Sequence[BaseNode]) -> Sequence[BaseNode]:
"""Insert nodes to the index struct."""
        if len(nodes) == 0:
            return nodes

        # run transformations on nodes to extract triplets
        if self._use_async:
            nodes = asyncio.run(
                arun_transformations(
                    nodes, self._kg_extractors, show_progress=self._show_progress
                )
            )
        else:
            nodes = run_transformations(
                nodes, self._kg_extractors, show_progress=self._show_progress
            )

        # ensure all nodes have nodes and/or relations in metadata
        assert all(
            node.metadata.get(KG_NODES_KEY) is not None
            or node.metadata.get(KG_RELATIONS_KEY) is not None
            for node in nodes
        )

        kg_nodes_to_insert: List[LabelledNode] = []
        kg_rels_to_insert: List[Relation] = []
        for node in nodes:
            # remove nodes and relations from metadata
            kg_nodes = node.metadata.pop(KG_NODES_KEY, [])
            kg_rels = node.metadata.pop(KG_RELATIONS_KEY, [])

            # add source id to properties
            for kg_node in kg_nodes:
                kg_node.properties[TRIPLET_SOURCE_KEY] = node.id_
            for kg_rel in kg_rels:
                kg_rel.properties[TRIPLET_SOURCE_KEY] = node.id_

            # add nodes and relations to insert lists
            kg_nodes_to_insert.extend(kg_nodes)
            kg_rels_to_insert.extend(kg_rels)

        # filter out duplicate kg nodes
        kg_node_ids = {node.id for node in kg_nodes_to_insert}
        existing_kg_nodes = self.property_graph_store.get(ids=list(kg_node_ids))
        existing_kg_node_ids = {node.id for node in existing_kg_nodes}
        kg_nodes_to_insert = [
            node for node in kg_nodes_to_insert if node.id not in existing_kg_node_ids
        ]

        # filter out duplicate llama nodes
        existing_nodes = self.property_graph_store.get_llama_nodes(
            [node.id_ for node in nodes]
        )
        existing_node_hashes = {node.hash for node in existing_nodes}
        nodes = [node for node in nodes if node.hash not in existing_node_hashes]

        # embed nodes (if needed)
        if self._embed_kg_nodes:
            # embed llama-index nodes
            node_texts = [
                node.get_content(metadata_mode=MetadataMode.EMBED) for node in nodes
            ]

            if self._use_async:
                embeddings = asyncio.run(
                    self._embed_model.aget_text_embedding_batch(
                        node_texts, show_progress=self._show_progress
                    )
                )
            else:
                embeddings = self._embed_model.get_text_embedding_batch(
                    node_texts, show_progress=self._show_progress
                )

            for node, embedding in zip(nodes, embeddings):
                node.embedding = embedding

            # embed kg nodes
            kg_node_texts = [str(kg_node) for kg_node in kg_nodes_to_insert]

            if self._use_async:
                kg_embeddings = asyncio.run(
                    self._embed_model.aget_text_embedding_batch(
                        kg_node_texts, show_progress=self._show_progress
                    )
                )
            else:
                kg_embeddings = self._embed_model.get_text_embedding_batch(
                    kg_node_texts,
                    show_progress=self._show_progress,
                )

            for kg_node, embedding in zip(kg_nodes_to_insert, kg_embeddings):
                kg_node.embedding = embedding

        # if graph store doesn't support vectors, or the vector index was provided, use it
        if self.vector_store is not None and len(kg_nodes_to_insert)  0:
            self._insert_nodes_to_vector_index(kg_nodes_to_insert)

        if len(nodes)  0:
            self.property_graph_store.upsert_llama_nodes(nodes)

        if len(kg_nodes_to_insert)  0:
            self.property_graph_store.upsert_nodes(kg_nodes_to_insert)

        # important: upsert relations after nodes
        if len(kg_rels_to_insert)  0:
            self.property_graph_store.upsert_relations(kg_rels_to_insert)

        # refresh schema if needed
        if self.property_graph_store.supports_structured_queries:
            self.property_graph_store.get_schema(refresh=True)

        return nodes

    def_insert_nodes_to_vector_index(self, nodes: List[LabelledNode]) -> None:
"""Insert vector nodes."""
        assert self.vector_store is not None

        llama_nodes: List[TextNode] = []
        for node in nodes:
            if node.embedding is not None:
                llama_nodes.append(
                    TextNode(
                        text=str(node),
                        metadata={VECTOR_SOURCE_KEY: node.id, **node.properties},
                        embedding=[*node.embedding],
                    )
                )
                if not self.vector_store.stores_text:
                    llama_nodes[-1].id_ = node.id

            # clear the embedding to save memory, its not used now
            node.embedding = None

        self.vector_store.add(llama_nodes)

    def_build_index_from_nodes(
        self, nodes: Optional[Sequence[BaseNode]], **build_kwargs: Any
    ) -> IndexLPG:
"""Build index from nodes."""
        nodes = self._insert_nodes(nodes or [])

        # this isn't really used or needed
        return IndexLPG()

    defas_retriever(
        self,
        sub_retrievers: Optional[List["BasePGRetriever"]] = None,
        include_text: bool = True,
        **kwargs: Any,
    ) -> BaseRetriever:
"""
        Return a retriever for the index.

        Args:
            sub_retrievers (Optional[List[BasePGRetriever]]):
                A list of sub-retrievers to use. If not provided, a default list will be used:
                `[LLMSynonymRetriever, VectorContextRetriever]` if the graph store supports vector queries.
            include_text (bool):
                Whether to include source-text in the retriever results.
            **kwargs:
                Additional kwargs to pass to the retriever.

        """
        fromllama_index.core.indices.property_graph.retrieverimport (
            PGRetriever,
        )
        fromllama_index.core.indices.property_graph.sub_retrievers.vectorimport (
            VectorContextRetriever,
        )
        fromllama_index.core.indices.property_graph.sub_retrievers.llm_synonymimport (
            LLMSynonymRetriever,
        )

        if sub_retrievers is None:
            sub_retrievers = [
                LLMSynonymRetriever(
                    graph_store=self.property_graph_store,
                    include_text=include_text,
                    llm=self._llm,
                    **kwargs,
                ),
            ]

            if self._embed_model and (
                self.property_graph_store.supports_vector_queries or self.vector_store
            ):
                sub_retrievers.append(
                    VectorContextRetriever(
                        graph_store=self.property_graph_store,
                        vector_store=self.vector_store,
                        include_text=include_text,
                        embed_model=self._embed_model,
                        **kwargs,
                    )
                )

        return PGRetriever(sub_retrievers, use_async=self._use_async, **kwargs)

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
"""Delete a node."""
        self.property_graph_store.delete(ids=[node_id])

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Index-specific logic for inserting nodes to the index struct."""
        self._insert_nodes(nodes)

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        raise NotImplementedError(
            "Ref doc info not implemented for PropertyGraphIndex. "
            "All inserts are already upserts."
        )

```
 |  
| --- | --- |  
###  property_graph_store `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.PropertyGraphIndex.property_graph_store "Permanent link")

```
property_graph_store: 

```

Get the labelled property graph store.
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.PropertyGraphIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
###  from_existing `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.PropertyGraphIndex.from_existing "Permanent link")

```
from_existing(
    property_graph_store: ,
    vector_store: Optional[] = None,
    llm: Optional[] = None,
    kg_extractors: Optional[
        []
    ] = None,
    use_async:  = True,
    embed_model: Optional[EmbedType] = None,
    embed_kg_nodes:  = True,
    callback_manager: Optional[] = None,
    transformations: Optional[
        []
    ] = None,
    storage_context: Optional[] = None,
    show_progress:  = False,
    **kwargs: 
) -> 

```

Create an index from an existing property graph store (and optional vector store).
Source code in `llama-index-core/llama_index/core/indices/property_graph/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_existing(
    cls: Type["PropertyGraphIndex"],
    property_graph_store: PropertyGraphStore,
    vector_store: Optional[BasePydanticVectorStore] = None,
    # general params
    llm: Optional[LLM] = None,
    kg_extractors: Optional[List[TransformComponent]] = None,
    # vector related params
    use_async: bool = True,
    embed_model: Optional[EmbedType] = None,
    embed_kg_nodes: bool = True,
    # parent class params
    callback_manager: Optional[CallbackManager] = None,
    transformations: Optional[List[TransformComponent]] = None,
    storage_context: Optional[StorageContext] = None,
    show_progress: bool = False,
    **kwargs: Any,
) -> "PropertyGraphIndex":
"""Create an index from an existing property graph store (and optional vector store)."""
    return cls(
        nodes=[],  # no nodes to insert
        property_graph_store=property_graph_store,
        vector_store=vector_store,
        llm=llm,
        kg_extractors=kg_extractors,
        use_async=use_async,
        embed_model=embed_model,
        embed_kg_nodes=embed_kg_nodes,
        callback_manager=callback_manager,
        transformations=transformations,
        storage_context=storage_context,
        show_progress=show_progress,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  as_retriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.PropertyGraphIndex.as_retriever "Permanent link")

```
as_retriever(
    sub_retrievers: Optional[[]] = None,
    include_text:  = True,
    **kwargs: 
) -> 

```

Return a retriever for the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sub_retrievers`  |  `Optional[List[BasePGRetriever[](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/auto_merging/#llama_index.core.retrievers.BasePGRetriever "BasePGRetriever \(llama_index.core.indices.property_graph.sub_retrievers.base.BasePGRetriever\)")]]`  |  A list of sub-retrievers to use. If not provided, a default list will be used: `[LLMSynonymRetriever, VectorContextRetriever]` if the graph store supports vector queries.  |  `None`  |  
|  `include_text`  |  `bool`  |  Whether to include source-text in the retriever results.  |  `True`  |  
|  `**kwargs`  |  Additional kwargs to pass to the retriever.  |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/base.py`  
| 
```
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
```
 | 
```
defas_retriever(
    self,
    sub_retrievers: Optional[List["BasePGRetriever"]] = None,
    include_text: bool = True,
    **kwargs: Any,
) -> BaseRetriever:
"""
    Return a retriever for the index.

    Args:
        sub_retrievers (Optional[List[BasePGRetriever]]):
            A list of sub-retrievers to use. If not provided, a default list will be used:
            `[LLMSynonymRetriever, VectorContextRetriever]` if the graph store supports vector queries.
        include_text (bool):
            Whether to include source-text in the retriever results.
        **kwargs:
            Additional kwargs to pass to the retriever.

    """
    fromllama_index.core.indices.property_graph.retrieverimport (
        PGRetriever,
    )
    fromllama_index.core.indices.property_graph.sub_retrievers.vectorimport (
        VectorContextRetriever,
    )
    fromllama_index.core.indices.property_graph.sub_retrievers.llm_synonymimport (
        LLMSynonymRetriever,
    )

    if sub_retrievers is None:
        sub_retrievers = [
            LLMSynonymRetriever(
                graph_store=self.property_graph_store,
                include_text=include_text,
                llm=self._llm,
                **kwargs,
            ),
        ]

        if self._embed_model and (
            self.property_graph_store.supports_vector_queries or self.vector_store
        ):
            sub_retrievers.append(
                VectorContextRetriever(
                    graph_store=self.property_graph_store,
                    vector_store=self.vector_store,
                    include_text=include_text,
                    embed_model=self._embed_model,
                    **kwargs,
                )
            )

    return PGRetriever(sub_retrievers, use_async=self._use_async, **kwargs)

```
 |  
| --- | --- |  
##  load_graph_from_storage [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.load_graph_from_storage "Permanent link")

```
load_graph_from_storage(
    storage_context: ,
    root_id: ,
    **kwargs: 
) -> 

```

Load composable graph from storage context.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `storage_context`  |   |  storage context containing docstore, index store and vector store.  |  _required_  |  
|  `root_id`  |  ID of the root index of the graph.  |  _required_  |  
|  `**kwargs`  |  Additional keyword args to pass to the index constructors.  |  
Source code in `llama-index-core/llama_index/core/indices/loading.py`  
| 
```
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
```
 | 
```
defload_graph_from_storage(
    storage_context: StorageContext,
    root_id: str,
    **kwargs: Any,
) -> ComposableGraph:
"""
    Load composable graph from storage context.

    Args:
        storage_context (StorageContext): storage context containing
            docstore, index store and vector store.
        root_id (str): ID of the root index of the graph.
        **kwargs: Additional keyword args to pass to the index constructors.

    """
    indices = load_indices_from_storage(storage_context, index_ids=None, **kwargs)
    all_indices = {index.index_id: index for index in indices}
    return ComposableGraph(all_indices=all_indices, root_id=root_id)

```
 |  
| --- | --- |  
##  load_index_from_storage [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.load_index_from_storage "Permanent link")

```
load_index_from_storage(
    storage_context: ,
    index_id: Optional[] = None,
    **kwargs: 
) -> 

```

Load index from storage context.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `storage_context`  |   |  storage context containing docstore, index store and vector store.  |  _required_  |  
|  `index_id`  |  `Optional[str]`  |  ID of the index to load. Defaults to None, which assumes there's only a single index in the index store and load it.  |  `None`  |  
|  `**kwargs`  |  Additional keyword args to pass to the index constructors.  |  
Source code in `llama-index-core/llama_index/core/indices/loading.py`  
| 
```
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
```
 | 
```
defload_index_from_storage(
    storage_context: StorageContext,
    index_id: Optional[str] = None,
    **kwargs: Any,
) -> BaseIndex:
"""
    Load index from storage context.

    Args:
        storage_context (StorageContext): storage context containing
            docstore, index store and vector store.
        index_id (Optional[str]): ID of the index to load.
            Defaults to None, which assumes there's only a single index
            in the index store and load it.
        **kwargs: Additional keyword args to pass to the index constructors.

    """
    index_ids: Optional[Sequence[str]]
    if index_id is None:
        index_ids = None
    else:
        index_ids = [index_id]

    indices = load_indices_from_storage(storage_context, index_ids=index_ids, **kwargs)

    if len(indices) == 0:
        raise ValueError(
            "No index in storage context, check if you specified the right persist_dir."
        )
    elif len(indices)  1:
        raise ValueError(
            f"Expected to load a single index, but got {len(indices)} instead. "
            "Please specify index_id."
        )

    return indices[0]

```
 |  
| --- | --- |  
##  load_indices_from_storage [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vector/#llama_index.core.indices.load_indices_from_storage "Permanent link")

```
load_indices_from_storage(
    storage_context: ,
    index_ids: Optional[Sequence[]] = None,
    **kwargs: 
) -> []

```

Load multiple indices from storage context.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `storage_context`  |   |  storage context containing docstore, index store and vector store.  |  _required_  |  
|  `index_id`  |  `Optional[Sequence[str]]`  |  IDs of the indices to load. Defaults to None, which loads all indices in the index store.  |  _required_  |  
|  `**kwargs`  |  Additional keyword args to pass to the index constructors.  |  
Source code in `llama-index-core/llama_index/core/indices/loading.py`  
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
```
 | 
```
defload_indices_from_storage(
    storage_context: StorageContext,
    index_ids: Optional[Sequence[str]] = None,
    **kwargs: Any,
) -> List[BaseIndex]:
"""
    Load multiple indices from storage context.

    Args:
        storage_context (StorageContext): storage context containing
            docstore, index store and vector store.
        index_id (Optional[Sequence[str]]): IDs of the indices to load.
            Defaults to None, which loads all indices in the index store.
        **kwargs: Additional keyword args to pass to the index constructors.

    """
    if index_ids is None:
        logger.info("Loading all indices.")
        index_structs = storage_context.index_store.index_structs()
    else:
        logger.info(f"Loading indices with ids: {index_ids}")
        index_structs = []
        for index_id in index_ids:
            index_struct = storage_context.index_store.get_index_struct(index_id)
            if index_struct is None:
                raise ValueError(f"Failed to load index with ID {index_id}")
            index_structs.append(index_struct)

    indices = []
    for index_struct in index_structs:
        type_ = index_struct.get_type()
        index_cls = INDEX_STRUCT_TYPE_TO_INDEX_CLASS[type_]
        index = index_cls(
            index_struct=index_struct, storage_context=storage_context, **kwargs
        )
        indices.append(index)
    return indices

```
 |  
| --- | --- |  
options: members: - VectorStoreIndex
