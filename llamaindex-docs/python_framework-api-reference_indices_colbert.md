# Colbert
##  ColbertIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/colbert/#llama_index.indices.managed.colbert.ColbertIndex "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[IndexDict]`
Store for ColBERT v2 with PLAID indexing.
ColBERT is a neural retrieval method that tends to work well in a zero-shot setting on out of domain datasets, due to it's use of token-level encodings (rather than sentence or chunk level)
#### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/indices/colbert/#llama_index.indices.managed.colbert.ColbertIndex--parameters "Permanent link")
index_path: directory containing PLAID index files. model_name: ColBERT hugging face model name. Default: "colbert-ir/colbertv2.0". show_progress: whether to show progress bar when building index. Default: False. noop for ColBERT for now. nbits: number of bits to quantize the residual vectors. Default: 2. kmeans_niters: number of kmeans clustering iterations. Default: 1. gpus: number of GPUs to use for indexing. Default: 0. rank: number of ranks to use for indexing. Default: 1. doc_maxlen: max document length. Default: 120. query_maxlen: max query length. Default: 60. kmeans_niters: number of kmeans iterations. Default: 4.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-colbert/llama_index/indices/managed/colbert/base.py`  
| 
```
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
```
 | 
```
classColbertIndex(BaseIndex[IndexDict]):
"""
    Store for ColBERT v2 with PLAID indexing.

    ColBERT is a neural retrieval method that tends to work
    well in a zero-shot setting on out of domain datasets, due
    to it's use of token-level encodings (rather than sentence or
    chunk level)

    Parameters
    ----------
    index_path: directory containing PLAID index files.
    model_name: ColBERT hugging face model name.
        Default: "colbert-ir/colbertv2.0".
    show_progress: whether to show progress bar when building index.
        Default: False. noop for ColBERT for now.
    nbits: number of bits to quantize the residual vectors. Default: 2.
    kmeans_niters: number of kmeans clustering iterations. Default: 1.
    gpus: number of GPUs to use for indexing. Default: 0.
    rank: number of ranks to use for indexing. Default: 1.
    doc_maxlen: max document length. Default: 120.
    query_maxlen: max query length. Default: 60.
    kmeans_niters: number of kmeans iterations. Default: 4.

    """

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[IndexDict] = None,
        storage_context: Optional[StorageContext] = None,
        model_name: str = "colbert-ir/colbertv2.0",
        index_name: str = "",
        show_progress: bool = False,
        nbits: int = 2,
        gpus: int = 0,
        ranks: int = 1,
        doc_maxlen: int = 120,
        query_maxlen: int = 60,
        kmeans_niters: int = 4,
        **kwargs: Any,
    ) -> None:
        self.model_name = model_name
        self.index_path = "storage/colbert_index"
        self.index_name = index_name
        self.nbits = nbits
        self.gpus = gpus
        self.ranks = ranks
        self.doc_maxlen = doc_maxlen
        self.query_maxlen = query_maxlen
        self.kmeans_niters = kmeans_niters
        self._docs_pos_to_node_id: Dict[int, str] = {}
        try:
            pass
        except ImportError as exc:
            raise ImportError(
                "Please install colbert to use this feature from the repo:",
                "https://github.com/stanford-futuredata/ColBERT",
            ) fromexc
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
        raise NotImplementedError("ColbertStoreIndex does not support insertion yet.")

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
        raise NotImplementedError("ColbertStoreIndex does not support deletion yet.")

    defas_retriever(self, **kwargs: Any) -> BaseRetriever:
        from.retrieverimport ColbertRetriever

        return ColbertRetriever(index=self, object_map=self._object_map, **kwargs)

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
        raise NotImplementedError("ColbertStoreIndex does not support ref_doc_info.")

    def_build_index_from_nodes(
        self, nodes: Sequence[BaseNode], **kwargs: Any
    ) -> IndexDict:
"""
        Generate a PLAID index from the ColBERT checkpoint via its hugging face
        model_name.
        """
        fromcolbertimport Indexer, Searcher
        fromcolbert.infraimport ColBERTConfig, Run, RunConfig

        index_struct = IndexDict()

        docs_list = []
        for i, node in enumerate(nodes):
            docs_list.append(node.get_content())
            self._docs_pos_to_node_id[i] = node.node_id
            index_struct.add_node(node, text_id=str(i))

        with Run().context(
            RunConfig(index_root=self.index_path, nranks=self.ranks, gpus=self.gpus)
        ):
            config = ColBERTConfig(
                doc_maxlen=self.doc_maxlen,
                query_maxlen=self.query_maxlen,
                nbits=self.nbits,
                kmeans_niters=self.kmeans_niters,
            )
            indexer = Indexer(checkpoint=self.model_name, config=config)
            indexer.index(name=self.index_name, collection=docs_list, overwrite=True)
            self.store = Searcher(
                index=self.index_name, collection=docs_list, checkpoint=self.model_name
            )
        return index_struct

    # @staticmethod
    # def _normalize_scores(docs: List[Document]) -> None:
    #     "Normalizing the MaxSim scores using softmax."
    #     Z = sum(math.exp(doc.score) for doc in docs)
    #     for doc in docs:
    #         doc.score = math.exp(doc.score) / Z

    defpersist(self, persist_dir: str) -> None:
        # Check if the destination directory exists
        if os.path.exists(persist_dir):
            # Remove the existing destination directory
            shutil.rmtree(persist_dir)

        # Copy PLAID vectors
        shutil.copytree(
            Path(self.index_path) / self.index_name, Path(persist_dir) / self.index_name
        )
        self._storage_context.persist(persist_dir=persist_dir)

    @classmethod
    defload_from_disk(cls, persist_dir: str, index_name: str = "") -> "ColbertIndex":
        fromcolbertimport Searcher
        fromcolbert.infraimport ColBERTConfig

        colbert_config = ColBERTConfig.load_from_index(Path(persist_dir) / index_name)
        searcher = Searcher(
            index=index_name, index_root=persist_dir, config=colbert_config
        )
        sc = StorageContext.from_defaults(persist_dir=persist_dir)
        colbert_index = ColbertIndex(
            index_struct=sc.index_store.index_structs()[0], storage_context=sc
        )
        docs_pos_to_node_id = {
            int(k): v for k, v in colbert_index.index_struct.nodes_dict.items()
        }
        colbert_index._docs_pos_to_node_id = docs_pos_to_node_id
        colbert_index.store = searcher
        return colbert_index

    defquery(self, query_str: str, top_k: int = 10) -> List[NodeWithScore]:
"""
        Query the Colbert v2 + Plaid store.

        Returns: list of NodeWithScore.
        """
        doc_ids, _, scores = self.store.search(text=query_str, k=top_k)

        node_doc_ids = [self._docs_pos_to_node_id[id] for id in doc_ids]
        nodes = self.docstore.get_nodes(node_doc_ids)

        nodes_with_score = []

        for node, score in zip(nodes, scores):
            nodes_with_score.append(NodeWithScore(node=node, score=score))

        return nodes_with_score

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/colbert/#llama_index.indices.managed.colbert.ColbertIndex.query "Permanent link")

```
query(
    query_str: , top_k:  = 10
) -> []

```

Query the Colbert v2 + Plaid store.
Returns: list of NodeWithScore.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-colbert/llama_index/indices/managed/colbert/base.py`  
| 
```
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
```
 | 
```
defquery(self, query_str: str, top_k: int = 10) -> List[NodeWithScore]:
"""
    Query the Colbert v2 + Plaid store.

    Returns: list of NodeWithScore.
    """
    doc_ids, _, scores = self.store.search(text=query_str, k=top_k)

    node_doc_ids = [self._docs_pos_to_node_id[id] for id in doc_ids]
    nodes = self.docstore.get_nodes(node_doc_ids)

    nodes_with_score = []

    for node, score in zip(nodes, scores):
        nodes_with_score.append(NodeWithScore(node=node, score=score))

    return nodes_with_score

```
 |  
| --- | --- |  
options: members: - ColbertIndex
