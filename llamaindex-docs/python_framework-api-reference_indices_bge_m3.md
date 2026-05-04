# Bge m3
##  BGEM3Index [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/bge_m3/#llama_index.indices.managed.bge_m3.BGEM3Index "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[IndexDict]`
Store for BGE-M3 with PLAID indexing.
BGE-M3 is a multilingual embedding model with multi-functionality: Dense retrieval, Sparse retrieval and Multi-vector retrieval.
#### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/indices/bge_m3/#llama_index.indices.managed.bge_m3.BGEM3Index--parameters "Permanent link")
index_path: directory containing PLAID index files. model_name: BGE-M3 hugging face model name. Default: "BAAI/bge-m3". show_progress: whether to show progress bar when building index. Default: False. noop for BGE-M3 for now. doc_maxlen: max document length. Default: 120. query_maxlen: max query length. Default: 60.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-bge-m3/llama_index/indices/managed/bge_m3/base.py`  
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
```
 | 
```
classBGEM3Index(BaseIndex[IndexDict]):
"""
    Store for BGE-M3 with PLAID indexing.

    BGE-M3 is a multilingual embedding model with multi-functionality:
    Dense retrieval, Sparse retrieval and Multi-vector retrieval.

    Parameters
    ----------
    index_path: directory containing PLAID index files.
    model_name: BGE-M3 hugging face model name.
        Default: "BAAI/bge-m3".
    show_progress: whether to show progress bar when building index.
        Default: False. noop for BGE-M3 for now.
    doc_maxlen: max document length. Default: 120.
    query_maxlen: max query length. Default: 60.

    """

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[IndexDict] = None,
        storage_context: Optional[StorageContext] = None,
        model_name: str = "BAAI/bge-m3",
        index_name: str = "",
        show_progress: bool = False,
        pooling_method: str = "cls",
        normalize_embeddings: bool = True,
        use_fp16: bool = False,
        batch_size: int = 32,
        doc_maxlen: int = 8192,
        query_maxlen: int = 8192,
        weights_for_different_modes: List[float] = None,
        **kwargs: Any,
    ) -> None:
        self.index_path = "storage/bge_m3_index"
        self.index_name = index_name
        self.batch_size = batch_size
        self.doc_maxlen = doc_maxlen
        self.query_maxlen = query_maxlen
        self.weights_for_different_modes = weights_for_different_modes
        self._multi_embed_store = None
        self._docs_pos_to_node_id: Dict[int, str] = {}
        try:
            fromFlagEmbeddingimport BGEM3FlagModel
        except ImportError as exc:
            raise ImportError(
                "Please install FlagEmbedding to use this feature from the repo:",
                "https://github.com/FlagOpen/FlagEmbedding/tree/master/FlagEmbedding/BGE_M3",
            ) fromexc
        self.model = BGEM3FlagModel(
            model_name,
            pooling_method=pooling_method,
            normalize_embeddings=normalize_embeddings,
            use_fp16=use_fp16,
        )
        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            index_name=index_name,
            storage_context=storage_context,
            show_progress=show_progress,
            objects=objects,
            **kwargs,
        )

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
        raise NotImplementedError("BGEM3Index does not support insertion yet.")

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
        raise NotImplementedError("BGEM3Index does not support deletion yet.")

    defas_retriever(self, **kwargs: Any) -> BaseRetriever:
        from.retrieverimport BGEM3Retriever

        return BGEM3Retriever(index=self, object_map=self._object_map, **kwargs)

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
        raise NotImplementedError("BGEM3Index does not support ref_doc_info.")

    def_build_index_from_nodes(
        self, nodes: Sequence[BaseNode], **kwargs: Any
    ) -> IndexDict:
"""
        Generate a PLAID index from the BGE-M3 checkpoint via its hugging face
        model_name.
        """
        index_struct = IndexDict()

        docs_list = []
        for i, node in enumerate(nodes):
            docs_list.append(node.get_content())
            self._docs_pos_to_node_id[i] = node.node_id
            index_struct.add_node(node, text_id=str(i))

        self._multi_embed_store = self.model.encode(
            docs_list,
            batch_size=self.batch_size,
            max_length=self.doc_maxlen,
            return_dense=True,
            return_sparse=True,
            return_colbert_vecs=True,
        )
        return index_struct

    defpersist(self, persist_dir: str) -> None:
        # Check if the destination directory exists
        if os.path.exists(persist_dir):
            # Remove the existing destination directory
            shutil.rmtree(persist_dir)

        self._storage_context.persist(persist_dir=persist_dir)
        # Save _multi_embed_store
        # Use pickle protocol 4 which supports large objects better
        with open(Path(persist_dir) / "multi_embed_store.pkl", "wb") as f:
            pickler = pickle.Pickler(f, protocol=pickle.HIGHEST_PROTOCOL)
            pickler.dump(self._multi_embed_store)

    @classmethod
    defload_from_disk(
        cls,
        persist_dir: str,
        model_name: str = "BAAI/bge-m3",
        index_name: str = "",
        weights_for_different_modes: List[float] = None,
    ) -> "BGEM3Index":
        sc = StorageContext.from_defaults(persist_dir=persist_dir)
        index = BGEM3Index(
            model_name=model_name,
            index_name=index_name,
            index_struct=sc.index_store.index_structs()[0],
            storage_context=sc,
            weights_for_different_modes=weights_for_different_modes,
        )
        docs_pos_to_node_id = {
            int(k): v for k, v in index.index_struct.nodes_dict.items()
        }
        index._docs_pos_to_node_id = docs_pos_to_node_id
        index._multi_embed_store = pickle.load(
            open(Path(persist_dir) / "multi_embed_store.pkl", "rb")
        )
        return index

    defquery(self, query_str: str, top_k: int = 10) -> List[NodeWithScore]:
"""
        Query the BGE-M3 + Plaid store.

        Returns: list of NodeWithScore.
        """
        query_embed = self.model.encode(
            query_str,
            batch_size=self.batch_size,
            max_length=self.query_maxlen,
            return_dense=True,
            return_sparse=True,
            return_colbert_vecs=True,
        )

        dense_scores = np.matmul(
            query_embed["dense_vecs"], self._multi_embed_store["dense_vecs"].T
        )

        sparse_scores = np.array(
            [
                self.model.compute_lexical_matching_score(
                    query_embed["lexical_weights"], doc_lexical_weights
                )
                for doc_lexical_weights in self._multi_embed_store["lexical_weights"]
            ]
        )

        colbert_scores = np.array(
            [
                self.model.colbert_score(
                    query_embed["colbert_vecs"], doc_colbert_vecs
                ).item()
                for doc_colbert_vecs in self._multi_embed_store["colbert_vecs"]
            ]
        )

        if self.weights_for_different_modes is None:
            weights_for_different_modes = [1.0, 1.0, 1.0]
            weight_sum = 3.0
        else:
            weights_for_different_modes = self.weights_for_different_modes
            weight_sum = sum(weights_for_different_modes)

        combined_scores = (
            dense_scores * weights_for_different_modes[0]
            + sparse_scores * weights_for_different_modes[1]
            + colbert_scores * weights_for_different_modes[2]
        ) / weight_sum

        topk_indices = np.argsort(combined_scores)[::-1][:top_k]
        topk_scores = [combined_scores[idx] for idx in topk_indices]

        node_doc_ids = [self._docs_pos_to_node_id[idx] for idx in topk_indices]
        nodes = self.docstore.get_nodes(node_doc_ids)

        nodes_with_score = []
        for node, score in zip(nodes, topk_scores):
            nodes_with_score.append(NodeWithScore(node=node, score=score))
        return nodes_with_score

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/bge_m3/#llama_index.indices.managed.bge_m3.BGEM3Index.query "Permanent link")

```
query(
    query_str: , top_k:  = 10
) -> []

```

Query the BGE-M3 + Plaid store.
Returns: list of NodeWithScore.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-bge-m3/llama_index/indices/managed/bge_m3/base.py`  
| 
```
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
```
 | 
```
defquery(self, query_str: str, top_k: int = 10) -> List[NodeWithScore]:
"""
    Query the BGE-M3 + Plaid store.

    Returns: list of NodeWithScore.
    """
    query_embed = self.model.encode(
        query_str,
        batch_size=self.batch_size,
        max_length=self.query_maxlen,
        return_dense=True,
        return_sparse=True,
        return_colbert_vecs=True,
    )

    dense_scores = np.matmul(
        query_embed["dense_vecs"], self._multi_embed_store["dense_vecs"].T
    )

    sparse_scores = np.array(
        [
            self.model.compute_lexical_matching_score(
                query_embed["lexical_weights"], doc_lexical_weights
            )
            for doc_lexical_weights in self._multi_embed_store["lexical_weights"]
        ]
    )

    colbert_scores = np.array(
        [
            self.model.colbert_score(
                query_embed["colbert_vecs"], doc_colbert_vecs
            ).item()
            for doc_colbert_vecs in self._multi_embed_store["colbert_vecs"]
        ]
    )

    if self.weights_for_different_modes is None:
        weights_for_different_modes = [1.0, 1.0, 1.0]
        weight_sum = 3.0
    else:
        weights_for_different_modes = self.weights_for_different_modes
        weight_sum = sum(weights_for_different_modes)

    combined_scores = (
        dense_scores * weights_for_different_modes[0]
        + sparse_scores * weights_for_different_modes[1]
        + colbert_scores * weights_for_different_modes[2]
    ) / weight_sum

    topk_indices = np.argsort(combined_scores)[::-1][:top_k]
    topk_scores = [combined_scores[idx] for idx in topk_indices]

    node_doc_ids = [self._docs_pos_to_node_id[idx] for idx in topk_indices]
    nodes = self.docstore.get_nodes(node_doc_ids)

    nodes_with_score = []
    for node, score in zip(nodes, topk_scores):
        nodes_with_score.append(NodeWithScore(node=node, score=score))
    return nodes_with_score

```
 |  
| --- | --- |  
options: members: - BGEM3Index
