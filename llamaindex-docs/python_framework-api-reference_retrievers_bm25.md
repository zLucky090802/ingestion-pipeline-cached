# Bm25
##  BM25Retriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/bm25/#llama_index.retrievers.bm25.BM25Retriever "Permanent link")
Bases: 
A BM25 retriever that uses the BM25 algorithm to retrieve nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  The nodes to index. If not provided, an existing BM25 object must be passed.  |  `None`  |  
|  `stemmer`  |  `Stemmer`  |  The stemmer to use. Defaults to an english stemmer.  |  `None`  |  
|  `language`  |  The language to use for stopword removal. Defaults to "en".  |  `'en'`  |  
|  `existing_bm25`  |  `BM25`  |  An existing BM25 object to use. If not provided, nodes must be passed.  |  `None`  |  
|  `similarity_top_k`  |  The number of results to return. Defaults to DEFAULT_SIMILARITY_TOP_K.  |  `DEFAULT_SIMILARITY_TOP_K`  |  
|  `callback_manager`  |   |  The callback manager to use. Defaults to None.  |  `None`  |  
|  `objects`  |  `List[IndexNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.IndexNode "IndexNode \(llama_index.core.schema.IndexNode\)")]`  |  The objects to retrieve. Defaults to None.  |  `None`  |  
|  `object_map`  |  `dict`  |  A map of object IDs to nodes. Defaults to None.  |  `None`  |  
|  `token_pattern`  |  The token pattern to use. Defaults to (?u)\b\w\w+\b.  |  `'(?u)\\b\\w\\w+\\b'`  |  
|  `skip_stemming`  |  `bool`  |  Whether to skip stemming. Defaults to False.  |  `False`  |  
|  `verbose`  |  `bool`  |  Whether to show progress. Defaults to False.  |  `False`  |  
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-bm25/llama_index/retrievers/bm25/base.py`  
| 
```
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
```
 | 
```
classBM25Retriever(BaseRetriever):
r"""
    A BM25 retriever that uses the BM25 algorithm to retrieve nodes.

    Args:
        nodes (List[BaseNode], optional):
            The nodes to index. If not provided, an existing BM25 object must be passed.
        stemmer (Stemmer.Stemmer, optional):
            The stemmer to use. Defaults to an english stemmer.
        language (str, optional):
            The language to use for stopword removal. Defaults to "en".
        existing_bm25 (bm25s.BM25, optional):
            An existing BM25 object to use. If not provided, nodes must be passed.
        similarity_top_k (int, optional):
            The number of results to return. Defaults to DEFAULT_SIMILARITY_TOP_K.
        callback_manager (CallbackManager, optional):
            The callback manager to use. Defaults to None.
        objects (List[IndexNode], optional):
            The objects to retrieve. Defaults to None.
        object_map (dict, optional):
            A map of object IDs to nodes. Defaults to None.
        token_pattern (str, optional):
            The token pattern to use. Defaults to (?u)\\b\\w\\w+\\b.
        skip_stemming (bool, optional):
            Whether to skip stemming. Defaults to False.
        verbose (bool, optional):
            Whether to show progress. Defaults to False.

    """

    def__init__(
        self,
        nodes: Optional[List[BaseNode]] = None,
        stemmer: Optional[Stemmer.Stemmer] = None,
        language: str = "en",
        existing_bm25: Optional[bm25s.BM25] = None,
        similarity_top_k: int = DEFAULT_SIMILARITY_TOP_K,
        callback_manager: Optional[CallbackManager] = None,
        objects: Optional[List[IndexNode]] = None,
        object_map: Optional[dict] = None,
        verbose: bool = False,
        skip_stemming: bool = False,
        token_pattern: str = r"(?u)\b\w\w+\b",
        filters: Optional[MetadataFilters] = None,
        corpus_weight_mask: Optional[List[int]] = None,
    ) -> None:
        self.stemmer = stemmer or Stemmer.Stemmer("english")
        self.similarity_top_k = similarity_top_k
        self.token_pattern = token_pattern
        self.skip_stemming = skip_stemming

        if existing_bm25 is not None:
            self.bm25 = existing_bm25
            self.corpus = existing_bm25.corpus
        else:
            if nodes is None:
                raise ValueError("Please pass nodes or an existing BM25 object.")

            self.corpus = [
                node_to_metadata_dict(node) | {"node_id": node.node_id}
                for node in nodes
            ]

            corpus_tokens = bm25s.tokenize(
                [node.get_content(metadata_mode=MetadataMode.EMBED) for node in nodes],
                stopwords=language,
                stemmer=self.stemmer if not skip_stemming else None,
                token_pattern=self.token_pattern,
                show_progress=verbose,
            )
            self.bm25 = bm25s.BM25()
            self.bm25.index(corpus_tokens, show_progress=verbose)

        if (
            self.bm25.scores.get("num_docs")
            and int(self.bm25.scores["num_docs"])  self.similarity_top_k
        ):
            if int(self.bm25.scores["num_docs"]) == 0:
                raise ValueError(
                    "No nodes added to the retriever kindly add more data."
                )

            logger.warning(
                "As bm25s.BM25 requires k less than or equal to number of nodes added. Overriding the value of similarity_top_k to number of nodes added."
            )
            self.similarity_top_k = int(self.bm25.scores["num_docs"])

        self.corpus_weight_mask = corpus_weight_mask or None
        if filters and self.corpus:
            # Build a weight mask for each corpus to filter out only relevant nodes
            _corpus_dict = {
                corpus_token["node_id"]: corpus_token for corpus_token in self.corpus
            }
            _query_filter_fn = build_metadata_filter_fn(
                lambda node_id: _corpus_dict[node_id], filters
            )
            self.corpus_weight_mask = [
                int(_query_filter_fn(corpus_token["node_id"]))
                for corpus_token in self.corpus
            ]

            # Check if all nodes were filtered out
            if not any(self.corpus_weight_mask):
                raise ValueError(
                    "All nodes were filtered out by the metadata filters. "
                    "Please adjust your filters or add more data."
                )

        super().__init__(
            callback_manager=callback_manager,
            object_map=object_map,
            objects=objects,
            verbose=verbose,
        )

    @classmethod
    deffrom_defaults(
        cls,
        index: Optional[VectorStoreIndex] = None,
        nodes: Optional[List[BaseNode]] = None,
        docstore: Optional[BaseDocumentStore] = None,
        stemmer: Optional[Stemmer.Stemmer] = None,
        language: str = "en",
        similarity_top_k: int = DEFAULT_SIMILARITY_TOP_K,
        verbose: bool = False,
        skip_stemming: bool = False,
        token_pattern: str = r"(?u)\b\w\w+\b",
        filters: Optional[MetadataFilters] = None,
        # deprecated
        tokenizer: Optional[Callable[[str], List[str]]] = None,
    ) -> "BM25Retriever":
        if tokenizer is not None:
            logger.warning(
                "The tokenizer parameter is deprecated and will be removed in a future release. "
                "Use a stemmer from PyStemmer instead."
            )

        # ensure only one of index, nodes, or docstore is passed
        if sum(bool(val) for val in [index, nodes, docstore]) != 1:
            raise ValueError("Please pass exactly one of index, nodes, or docstore.")

        if index is not None:
            docstore = index.docstore

        if docstore is not None:
            nodes = cast(List[BaseNode], list(docstore.docs.values()))

        assert nodes is not None, (
            "Please pass exactly one of index, nodes, or docstore."
        )

        return cls(
            nodes=nodes,
            stemmer=stemmer,
            language=language,
            similarity_top_k=similarity_top_k,
            verbose=verbose,
            skip_stemming=skip_stemming,
            token_pattern=token_pattern,
            filters=filters,
        )

    defget_persist_args(self) -> Dict[str, Any]:
"""Get Persist Args Dict to Save."""
        return {
            DEFAULT_PERSIST_ARGS[key]: getattr(self, key)
            for key in DEFAULT_PERSIST_ARGS
            if hasattr(self, key)
        }

    defpersist(self, path: str, encoding: str = "utf-8", **kwargs: Any) -> None:
"""Persist the retriever to a directory."""
        self.bm25.save(path, corpus=self.corpus, **kwargs)
        with open(
            os.path.join(path, DEFAULT_PERSIST_FILENAME), "w", encoding=encoding
        ) as f:
            json.dump(self.get_persist_args(), f, indent=2)

    @classmethod
    deffrom_persist_dir(
        cls, path: str, encoding: str = "utf-8", **kwargs: Any
    ) -> "BM25Retriever":
"""Load the retriever from a directory."""
        bm25 = bm25s.BM25.load(path, load_corpus=True, **kwargs)
        with open(os.path.join(path, DEFAULT_PERSIST_FILENAME), encoding=encoding) as f:
            retriever_data = json.load(f)
        return cls(existing_bm25=bm25, **retriever_data)

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        query = query_bundle.query_str
        tokenized_query = bm25s.tokenize(
            query,
            stemmer=self.stemmer if not self.skip_stemming else None,
            token_pattern=self.token_pattern,
            show_progress=self._verbose,
        )
        indexes, scores = self.bm25.retrieve(
            tokenized_query,
            k=self.similarity_top_k,
            show_progress=self._verbose,
            weight_mask=np.array(self.corpus_weight_mask)
            if self.corpus_weight_mask
            else None,
        )

        # batched, but only one query
        indexes = indexes[0]
        scores = scores[0]

        nodes: List[NodeWithScore] = []
        for idx, score in zip(indexes, scores):
            # idx can be an int or a dict of the node
            if isinstance(idx, dict):
                node = metadata_dict_to_node(idx)
            else:
                node_dict = self.corpus[int(idx)]
                node = metadata_dict_to_node(node_dict)
            nodes.append(NodeWithScore(node=node, score=float(score)))

        return nodes

```
 |  
| --- | --- |  
###  get_persist_args [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/bm25/#llama_index.retrievers.bm25.BM25Retriever.get_persist_args "Permanent link")

```
get_persist_args() -> [, ]

```

Get Persist Args Dict to Save.
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-bm25/llama_index/retrievers/bm25/base.py`  
| 
```
203
204
205
206
207
208
209
```
 | 
```
defget_persist_args(self) -> Dict[str, Any]:
"""Get Persist Args Dict to Save."""
    return {
        DEFAULT_PERSIST_ARGS[key]: getattr(self, key)
        for key in DEFAULT_PERSIST_ARGS
        if hasattr(self, key)
    }

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/bm25/#llama_index.retrievers.bm25.BM25Retriever.persist "Permanent link")

```
persist(
    path: , encoding:  = "utf-8", **kwargs: 
) -> None

```

Persist the retriever to a directory.
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-bm25/llama_index/retrievers/bm25/base.py`  
| 
```
211
212
213
214
215
216
217
```
 | 
```
defpersist(self, path: str, encoding: str = "utf-8", **kwargs: Any) -> None:
"""Persist the retriever to a directory."""
    self.bm25.save(path, corpus=self.corpus, **kwargs)
    with open(
        os.path.join(path, DEFAULT_PERSIST_FILENAME), "w", encoding=encoding
    ) as f:
        json.dump(self.get_persist_args(), f, indent=2)

```
 |  
| --- | --- |  
###  from_persist_dir `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/bm25/#llama_index.retrievers.bm25.BM25Retriever.from_persist_dir "Permanent link")

```
from_persist_dir(
    path: , encoding:  = "utf-8", **kwargs: 
) -> 

```

Load the retriever from a directory.
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-bm25/llama_index/retrievers/bm25/base.py`  
| 
```
219
220
221
222
223
224
225
226
227
```
 | 
```
@classmethod
deffrom_persist_dir(
    cls, path: str, encoding: str = "utf-8", **kwargs: Any
) -> "BM25Retriever":
"""Load the retriever from a directory."""
    bm25 = bm25s.BM25.load(path, load_corpus=True, **kwargs)
    with open(os.path.join(path, DEFAULT_PERSIST_FILENAME), encoding=encoding) as f:
        retriever_data = json.load(f)
    return cls(existing_bm25=bm25, **retriever_data)

```
 |  
| --- | --- |  
options: members: - BM25Retriever
