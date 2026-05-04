# Index
Vector store index types.
##  VectorStoreQueryResult `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStoreQueryResult "Permanent link")
Vector store query result.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")] | None`  |  `None`  |  
|  `similarities`  |  `List[float] | None`  |  `None`  |  
|  `ids`  |  `List[str] | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
36
37
38
39
40
41
42
```
 | 
```
@dataclass
classVectorStoreQueryResult:
"""Vector store query result."""

    nodes: Optional[Sequence[BaseNode]] = None
    similarities: Optional[List[float]] = None
    ids: Optional[List[str]] = None

```
 |  
| --- | --- |  
##  VectorStoreQueryMode [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStoreQueryMode "Permanent link")
Bases: `str`, `Enum`
Vector store query mode.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
classVectorStoreQueryMode(str, Enum):
"""Vector store query mode."""

    DEFAULT = "default"
    SPARSE = "sparse"
    HYBRID = "hybrid"
    TEXT_SEARCH = "text_search"
    SEMANTIC_HYBRID = "semantic_hybrid"

    # fit learners
    SVM = "svm"
    LOGISTIC_REGRESSION = "logistic_regression"
    LINEAR_REGRESSION = "linear_regression"

    # maximum marginal relevance
    MMR = "mmr"

```
 |  
| --- | --- |  
##  FilterOperator [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.FilterOperator "Permanent link")
Bases: `str`, `Enum`
Vector store filter operator.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
classFilterOperator(str, Enum):
"""Vector store filter operator."""

    # TODO add more operators
    EQ = "=="  # default operator (string, int, float)
    GT = ">"  # greater than (int, float)
    LT = "<"  # less than (int, float)
    NE = "!="  # not equal to (string, int, float)
    GTE = ">="  # greater than or equal to (int, float)
    LTE = "<="  # less than or equal to (int, float)
    IN = "in"  # In array (string or number)
    NIN = "nin"  # Not in array (string or number)
    ANY = "any"  # Contains any (array of strings)
    ALL = "all"  # Contains all (array of strings)
    TEXT_MATCH = "text_match"  # full text match (allows you to search for a specific substring, token or phrase within the text field)
    TEXT_MATCH_INSENSITIVE = (
        "text_match_insensitive"  # full text match (case insensitive)
    )
    CONTAINS = "contains"  # metadata array contains value (string or number)
    IS_EMPTY = "is_empty"  # the field is not exist or empty (null or empty array)

```
 |  
| --- | --- |  
##  FilterCondition [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.FilterCondition "Permanent link")
Bases: `str`, `Enum`
Vector store filter conditions to combine different filters.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
classFilterCondition(str, Enum):
"""Vector store filter conditions to combine different filters."""

    # TODO add more conditions
    AND = "and"
    OR = "or"
    NOT = "not"  # negates the filter condition

```
 |  
| --- | --- |  
##  MetadataFilter [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilter "Permanent link")
Bases: `BaseModel`
Comprehensive metadata filter for vector stores to support more operators.
Value uses Strict types, as int, float and str are compatible types and were all converted to string before.
See: https://docs.pydantic.dev/latest/usage/types/#strict-types
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `value`  |  `Annotated[int, Strict] | Annotated[float, Strict] | Annotated[str, Strict] | List[Annotated[str, Strict]] | List[Annotated[float, Strict]] | List[Annotated[int, Strict]] | None`  |  _required_  |  
|  `operator`  |   |  `<FilterOperator.EQ: '=='>`  |  
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
classMetadataFilter(BaseModel):
r"""
    Comprehensive metadata filter for vector stores to support more operators.

    Value uses Strict types, as int, float and str are compatible types and were all
    converted to string before.

    See: https://docs.pydantic.dev/latest/usage/types/#strict-types
    """

    key: str
    value: Optional[
        Union[
            StrictInt,
            StrictFloat,
            StrictStr,
            List[StrictStr],
            List[StrictFloat],
            List[StrictInt],
        ]
    ]
    operator: FilterOperator = FilterOperator.EQ

    @classmethod
    deffrom_dict(
        cls,
        filter_dict: Dict,
    ) -> "MetadataFilter":
"""
        Create MetadataFilter from dictionary.

        Args:
            filter_dict: Dict with key, value and operator.

        """
        return MetadataFilter.model_validate(filter_dict)

```
 |  
| --- | --- |  
###  from_dict `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilter.from_dict "Permanent link")

```
from_dict(filter_dict: ) -> 

```

Create MetadataFilter from dictionary.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `filter_dict`  |  `Dict`  |  Dict with key, value and operator.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_dict(
    cls,
    filter_dict: Dict,
) -> "MetadataFilter":
"""
    Create MetadataFilter from dictionary.

    Args:
        filter_dict: Dict with key, value and operator.

    """
    return MetadataFilter.model_validate(filter_dict)

```
 |  
| --- | --- |  
##  MetadataFilters [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "Permanent link")
Bases: `BaseModel`
Metadata filters for vector stores.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `filters`  |  `List[MetadataFilter[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilter "MetadataFilter \(llama_index.core.vector_stores.types.MetadataFilter\)") | MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  _required_  |  
|  `condition`  |  `FilterCondition[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.FilterCondition "FilterCondition \(llama_index.core.vector_stores.types.FilterCondition\)") | None`  |  `<FilterCondition.AND: 'and'>`  |  
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
classMetadataFilters(BaseModel):
"""Metadata filters for vector stores."""

    # Exact match filters and Advanced filters with operators like >, <, >=, <=, !=, etc.
    filters: List[Union[MetadataFilter, ExactMatchFilter, "MetadataFilters"]]
    # and/or such conditions for combining different filters
    condition: Optional[FilterCondition] = FilterCondition.AND

    @classmethod
    @deprecated(
        "`from_dict()` is deprecated. "
        "Please use `MetadataFilters(filters=.., condition='and')` directly instead."
    )
    deffrom_dict(cls, filter_dict: Dict) -> "MetadataFilters":
"""Create MetadataFilters from json."""
        filters = []
        for k, v in filter_dict.items():
            filter = MetadataFilter(key=k, value=v, operator=FilterOperator.EQ)
            filters.append(filter)
        return cls(filters=filters)

    @classmethod
    deffrom_dicts(
        cls,
        filter_dicts: List[Dict],
        condition: Optional[FilterCondition] = FilterCondition.AND,
    ) -> "MetadataFilters":
"""
        Create MetadataFilters from dicts.

        This takes in a list of individual MetadataFilter objects, along
        with the condition.

        Args:
            filter_dicts: List of dicts, each dict is a MetadataFilter.
            condition: FilterCondition to combine different filters.

        """
        return cls(
            filters=[
                MetadataFilter.from_dict(filter_dict) for filter_dict in filter_dicts
            ],
            condition=condition,
        )

    deflegacy_filters(self) -> List[ExactMatchFilter]:
"""Convert MetadataFilters to legacy ExactMatchFilters."""
        filters = []
        for filter in self.filters:
            if (
                isinstance(filter, MetadataFilters)
                or filter.operator != FilterOperator.EQ
            ):
                raise ValueError(
                    "Vector Store only supports exact match filters. "
                    "Please use ExactMatchFilter or FilterOperator.EQ instead."
                )
            filters.append(ExactMatchFilter(key=filter.key, value=filter.value))
        return filters

```
 |  
| --- | --- |  
###  from_dict `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters.from_dict "Permanent link")

```
from_dict(filter_dict: ) -> 

```

Create MetadataFilters from json.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
@classmethod
@deprecated(
    "`from_dict()` is deprecated. "
    "Please use `MetadataFilters(filters=.., condition='and')` directly instead."
)
deffrom_dict(cls, filter_dict: Dict) -> "MetadataFilters":
"""Create MetadataFilters from json."""
    filters = []
    for k, v in filter_dict.items():
        filter = MetadataFilter(key=k, value=v, operator=FilterOperator.EQ)
        filters.append(filter)
    return cls(filters=filters)

```
 |  
| --- | --- |  
###  from_dicts `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters.from_dicts "Permanent link")

```
from_dicts(
    filter_dicts: [],
    condition: Optional[] = ,
) -> 

```

Create MetadataFilters from dicts.
This takes in a list of individual MetadataFilter objects, along with the condition.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `filter_dicts`  |  `List[Dict]`  |  List of dicts, each dict is a MetadataFilter.  |  _required_  |  
|  `condition`  |  `Optional[FilterCondition[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.FilterCondition "FilterCondition \(llama_index.core.vector_stores.types.FilterCondition\)")]`  |  FilterCondition to combine different filters.  |  
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_dicts(
    cls,
    filter_dicts: List[Dict],
    condition: Optional[FilterCondition] = FilterCondition.AND,
) -> "MetadataFilters":
"""
    Create MetadataFilters from dicts.

    This takes in a list of individual MetadataFilter objects, along
    with the condition.

    Args:
        filter_dicts: List of dicts, each dict is a MetadataFilter.
        condition: FilterCondition to combine different filters.

    """
    return cls(
        filters=[
            MetadataFilter.from_dict(filter_dict) for filter_dict in filter_dicts
        ],
        condition=condition,
    )

```
 |  
| --- | --- |  
###  legacy_filters [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters.legacy_filters "Permanent link")

```
legacy_filters() -> [ExactMatchFilter]

```

Convert MetadataFilters to legacy ExactMatchFilters.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
deflegacy_filters(self) -> List[ExactMatchFilter]:
"""Convert MetadataFilters to legacy ExactMatchFilters."""
    filters = []
    for filter in self.filters:
        if (
            isinstance(filter, MetadataFilters)
            or filter.operator != FilterOperator.EQ
        ):
            raise ValueError(
                "Vector Store only supports exact match filters. "
                "Please use ExactMatchFilter or FilterOperator.EQ instead."
            )
        filters.append(ExactMatchFilter(key=filter.key, value=filter.value))
    return filters

```
 |  
| --- | --- |  
##  VectorStoreQuerySpec [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStoreQuerySpec "Permanent link")
Bases: `BaseModel`
Schema for a structured request for vector store (i.e. to be converted to a VectorStoreQuery).
Currently only used by VectorIndexAutoRetriever.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  _required_  |  
|  `filters`  |  `List[MetadataFilter[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilter "MetadataFilter \(llama_index.core.vector_stores.types.MetadataFilter\)")]`  |  _required_  |  
|  `top_k`  |  `int | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
classVectorStoreQuerySpec(BaseModel):
"""
    Schema for a structured request for vector store
    (i.e. to be converted to a VectorStoreQuery).

    Currently only used by VectorIndexAutoRetriever.
    """

    query: str
    filters: List[MetadataFilter]
    top_k: Optional[int] = None

```
 |  
| --- | --- |  
##  MetadataInfo [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataInfo "Permanent link")
Bases: `BaseModel`
Information about a metadata filter supported by a vector store.
Currently only used by VectorIndexAutoRetriever.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  _required_  |  
|  `type`  |  _required_  |  
|  `description`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
classMetadataInfo(BaseModel):
"""
    Information about a metadata filter supported by a vector store.

    Currently only used by VectorIndexAutoRetriever.
    """

    name: str
    type: str
    description: str

```
 |  
| --- | --- |  
##  VectorStoreInfo [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStoreInfo "Permanent link")
Bases: `BaseModel`
Information about a vector store (content and supported metadata filters).
Currently only used by VectorIndexAutoRetriever.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `metadata_info`  |  `List[MetadataInfo[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataInfo "MetadataInfo \(llama_index.core.vector_stores.types.MetadataInfo\)")]`  |  _required_  |  
|  `content_info`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
228
229
230
231
232
233
234
235
236
```
 | 
```
classVectorStoreInfo(BaseModel):
"""
    Information about a vector store (content and supported metadata filters).

    Currently only used by VectorIndexAutoRetriever.
    """

    metadata_info: List[MetadataInfo]
    content_info: str

```
 |  
| --- | --- |  
##  VectorStoreQuery `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStoreQuery "Permanent link")
Vector store query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_embedding`  |  `List[float] | None`  |  `None`  |  
|  `similarity_top_k`  |  
|  `doc_ids`  |  `List[str] | None`  |  `None`  |  
|  `node_ids`  |  `List[str] | None`  |  `None`  |  
|  `query_str`  |  `str | None`  |  `None`  |  
|  `output_fields`  |  `List[str] | None`  |  `None`  |  
|  `embedding_field`  |  `str | None`  |  `None`  |  
|  `mode`  |   |  `<VectorStoreQueryMode.DEFAULT: 'default'>`  |  
|  `alpha`  |  `float | None`  |  `None`  |  
|  `filters`  |  `MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)") | None`  |  `None`  |  
|  `mmr_threshold`  |  `float | None`  |  `None`  |  
|  `sparse_top_k`  |  `int | None`  |  `None`  |  
|  `hybrid_top_k`  |  `int | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
@dataclass
classVectorStoreQuery:
"""Vector store query."""

    query_embedding: Optional[List[float]] = None
    similarity_top_k: int = 1
    doc_ids: Optional[List[str]] = None
    node_ids: Optional[List[str]] = None
    query_str: Optional[str] = None
    output_fields: Optional[List[str]] = None
    embedding_field: Optional[str] = None

    mode: VectorStoreQueryMode = VectorStoreQueryMode.DEFAULT

    # NOTE: only for hybrid search (0 for bm25, 1 for vector search)
    alpha: Optional[float] = None

    # metadata filters
    filters: Optional[MetadataFilters] = None

    # only for mmr
    mmr_threshold: Optional[float] = None

    # NOTE: currently only used by postgres hybrid search
    sparse_top_k: Optional[int] = None
    # NOTE: return top k results from hybrid search. similarity_top_k is used for dense search top k
    hybrid_top_k: Optional[int] = None

```
 |  
| --- | --- |  
##  VectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStore "Permanent link")
Bases: `Protocol`
Abstract vector store protocol.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
@runtime_checkable
classVectorStore(Protocol):
"""Abstract vector store protocol."""

    stores_text: bool
    is_embedding_query: bool = True

    @property
    defclient(self) -> Any:
"""Get client."""
        ...

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""Add nodes with embedding to vector store."""
        ...

    async defasync_add(
        self,
        nodes: List[BaseNode],
        **kwargs: Any,
    ) -> List[str]:
"""
        Asynchronously add nodes with embedding to vector store.
        NOTE: this is not implemented for all vector stores. If not implemented,
        it will just call add synchronously.
        """
        return self.add(nodes)

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id."""
        ...

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.
        NOTE: this is not implemented for all vector stores. If not implemented,
        it will just call delete synchronously.
        """
        self.delete(ref_doc_id, **delete_kwargs)

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query vector store."""
        ...

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Asynchronously query vector store.
        NOTE: this is not implemented for all vector stores. If not implemented,
        it will just call query synchronously.
        """
        return self.query(query, **kwargs)

    defpersist(
        self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
    ) -> None:
        return None

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStore.client "Permanent link")

```
client: 

```

Get client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes with embedding to vector store.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
280
281
282
283
284
285
286
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""Add nodes with embedding to vector store."""
    ...

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStore.async_add "Permanent link")

```
async_add(
    nodes: [], **kwargs: 
) -> []

```

Asynchronously add nodes with embedding to vector store. NOTE: this is not implemented for all vector stores. If not implemented, it will just call add synchronously.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
async defasync_add(
    self,
    nodes: List[BaseNode],
    **kwargs: Any,
) -> List[str]:
"""
    Asynchronously add nodes with embedding to vector store.
    NOTE: this is not implemented for all vector stores. If not implemented,
    it will just call add synchronously.
    """
    return self.add(nodes)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
300
301
302
303
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id."""
    ...

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id. NOTE: this is not implemented for all vector stores. If not implemented, it will just call delete synchronously.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
305
306
307
308
309
310
311
```
 | 
```
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.
    NOTE: this is not implemented for all vector stores. If not implemented,
    it will just call delete synchronously.
    """
    self.delete(ref_doc_id, **delete_kwargs)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query vector store.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
313
314
315
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query vector store."""
    ...

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Asynchronously query vector store. NOTE: this is not implemented for all vector stores. If not implemented, it will just call query synchronously.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
317
318
319
320
321
322
323
324
325
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:
"""
    Asynchronously query vector store.
    NOTE: this is not implemented for all vector stores. If not implemented,
    it will just call query synchronously.
    """
    return self.query(query, **kwargs)

```
 |  
| --- | --- |  
##  BasePydanticVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "Permanent link")
Bases: , 
Abstract vector store protocol.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `stores_text`  |  `bool`  |  _required_  |  
|  `is_embedding_query`  |  `bool`  |  `True`  |  
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
classBasePydanticVectorStore(BaseComponent, ABC):
"""Abstract vector store protocol."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    stores_text: bool
    is_embedding_query: bool = True

    @property
    @abstractmethod
    defclient(self) -> Any:
"""Get client."""

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""Get nodes from vector store."""
        raise NotImplementedError("get_nodes not implemented")

    async defaget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""Asynchronously get nodes from vector store."""
        return self.get_nodes(node_ids, filters)

    @abstractmethod
    defadd(
        self,
        nodes: Sequence[BaseNode],
        **kwargs: Any,
    ) -> List[str]:
"""Add nodes to vector store."""

    async defasync_add(
        self,
        nodes: Sequence[BaseNode],
        **kwargs: Any,
    ) -> List[str]:
"""
        Asynchronously add nodes to vector store.
        NOTE: this is not implemented for all vector stores. If not implemented,
        it will just call add synchronously.
        """
        return self.add(nodes, **kwargs)

    @abstractmethod
    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id."""

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.
        NOTE: this is not implemented for all vector stores. If not implemented,
        it will just call delete synchronously.
        """
        self.delete(ref_doc_id, **delete_kwargs)

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""Delete nodes from vector store."""
        raise NotImplementedError("delete_nodes not implemented")

    async defadelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""Asynchronously delete nodes from vector store."""
        self.delete_nodes(node_ids, filters)

    defclear(self) -> None:
"""Clear all nodes from configured vector store."""
        raise NotImplementedError("clear not implemented")

    async defaclear(self) -> None:
"""Asynchronously clear all nodes from configured vector store."""
        self.clear()

    @abstractmethod
    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query vector store."""

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Asynchronously query vector store.
        NOTE: this is not implemented for all vector stores. If not implemented,
        it will just call query synchronously.
        """
        return self.query(query, **kwargs)

    defpersist(
        self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
    ) -> None:
        return None

```
 |  
| --- | --- |  
###  client `abstractmethod` `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.client "Permanent link")

```
client: 

```

Get client.
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes from vector store.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
346
347
348
349
350
351
352
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""Get nodes from vector store."""
    raise NotImplementedError("get_nodes not implemented")

```
 |  
| --- | --- |  
###  aget_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.aget_nodes "Permanent link")

```
aget_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Asynchronously get nodes from vector store.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
354
355
356
357
358
359
360
```
 | 
```
async defaget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""Asynchronously get nodes from vector store."""
    return self.get_nodes(node_ids, filters)

```
 |  
| --- | --- |  
###  add `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.add "Permanent link")

```
add(nodes: Sequence[], **kwargs: ) -> []

```

Add nodes to vector store.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
362
363
364
365
366
367
368
```
 | 
```
@abstractmethod
defadd(
    self,
    nodes: Sequence[BaseNode],
    **kwargs: Any,
) -> List[str]:
"""Add nodes to vector store."""

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.async_add "Permanent link")

```
async_add(
    nodes: Sequence[], **kwargs: 
) -> []

```

Asynchronously add nodes to vector store. NOTE: this is not implemented for all vector stores. If not implemented, it will just call add synchronously.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
```
 | 
```
async defasync_add(
    self,
    nodes: Sequence[BaseNode],
    **kwargs: Any,
) -> List[str]:
"""
    Asynchronously add nodes to vector store.
    NOTE: this is not implemented for all vector stores. If not implemented,
    it will just call add synchronously.
    """
    return self.add(nodes, **kwargs)

```
 |  
| --- | --- |  
###  delete `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
382
383
384
385
```
 | 
```
@abstractmethod
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id."""

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id. NOTE: this is not implemented for all vector stores. If not implemented, it will just call delete synchronously.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
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
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.
    NOTE: this is not implemented for all vector stores. If not implemented,
    it will just call delete synchronously.
    """
    self.delete(ref_doc_id, **delete_kwargs)

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes from vector store.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
395
396
397
398
399
400
401
402
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""Delete nodes from vector store."""
    raise NotImplementedError("delete_nodes not implemented")

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Asynchronously delete nodes from vector store.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
404
405
406
407
408
409
410
411
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""Asynchronously delete nodes from vector store."""
    self.delete_nodes(node_ids, filters)

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.clear "Permanent link")

```
clear() -> None

```

Clear all nodes from configured vector store.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
413
414
415
```
 | 
```
defclear(self) -> None:
"""Clear all nodes from configured vector store."""
    raise NotImplementedError("clear not implemented")

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.aclear "Permanent link")

```
aclear() -> None

```

Asynchronously clear all nodes from configured vector store.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
417
418
419
```
 | 
```
async defaclear(self) -> None:
"""Asynchronously clear all nodes from configured vector store."""
    self.clear()

```
 |  
| --- | --- |  
###  query `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query vector store.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
421
422
423
```
 | 
```
@abstractmethod
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query vector store."""

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Asynchronously query vector store. NOTE: this is not implemented for all vector stores. If not implemented, it will just call query synchronously.
Source code in `llama-index-core/llama_index/core/vector_stores/types.py`  
| 
```
425
426
427
428
429
430
431
432
433
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:
"""
    Asynchronously query vector store.
    NOTE: this is not implemented for all vector stores. If not implemented,
    it will just call query synchronously.
    """
    return self.query(query, **kwargs)

```
 |  
| --- | --- |
