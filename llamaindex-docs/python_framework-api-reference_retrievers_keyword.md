# Keyword
Query for KeywordTableIndex.
##  BaseKeywordTableRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/keyword/#llama_index.core.indices.keyword_table.retrievers.BaseKeywordTableRetriever "Permanent link")
Bases: 
Base Keyword Table Retriever.
Arguments are shared among subclasses.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `keyword_extract_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Keyword Extraction Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `query_keyword_extract_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Query Keyword Extraction Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `refine_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Refinement Prompt (see :ref:`Prompt-Templates`).  |  _required_  |  
|  `text_qa_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Question Answering Prompt (see :ref:`Prompt-Templates`).  |  _required_  |  
|  `max_keywords_per_query`  |  Maximum number of keywords to extract from query.  |  
|  `num_chunks_per_query`  |  Maximum number of text chunks to query.  |  
Source code in `llama-index-core/llama_index/core/indices/keyword_table/retrievers.py`  
| 
```
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
```
 | 
```
classBaseKeywordTableRetriever(BaseRetriever):
"""
    Base Keyword Table Retriever.

    Arguments are shared among subclasses.

    Args:
        keyword_extract_template (Optional[BasePromptTemplate]): A Keyword
            Extraction Prompt
            (see :ref:`Prompt-Templates`).
        query_keyword_extract_template (Optional[BasePromptTemplate]): A Query
            Keyword Extraction
            Prompt (see :ref:`Prompt-Templates`).
        refine_template (Optional[BasePromptTemplate]): A Refinement Prompt
            (see :ref:`Prompt-Templates`).
        text_qa_template (Optional[BasePromptTemplate]): A Question Answering Prompt
            (see :ref:`Prompt-Templates`).
        max_keywords_per_query (int): Maximum number of keywords to extract from query.
        num_chunks_per_query (int): Maximum number of text chunks to query.

    """

    def__init__(
        self,
        index: BaseKeywordTableIndex,
        keyword_extract_template: Optional[BasePromptTemplate] = None,
        query_keyword_extract_template: Optional[BasePromptTemplate] = None,
        max_keywords_per_query: int = 10,
        num_chunks_per_query: int = 10,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._index = index
        self._index_struct = index.index_struct
        self._docstore = index.docstore

        self.max_keywords_per_query = max_keywords_per_query
        self.num_chunks_per_query = num_chunks_per_query
        self.keyword_extract_template = (
            keyword_extract_template or DEFAULT_KEYWORD_EXTRACT_TEMPLATE
        )
        self.query_keyword_extract_template = query_keyword_extract_template or DQKET
        super().__init__(
            callback_manager=callback_manager or Settings.callback_manager,
            object_map=object_map,
            verbose=verbose,
        )

    @abstractmethod
    def_get_keywords(self, query_str: str) -> List[str]:
"""Extract keywords."""

    def_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""Get nodes for response."""
        logger.info(f"> Starting query: {query_bundle.query_str}")
        keywords = self._get_keywords(query_bundle.query_str)
        logger.info(f"query keywords: {keywords}")

        # go through text chunks in order of most matching keywords
        chunk_indices_count: Dict[str, int] = defaultdict(int)
        keywords = [k for k in keywords if k in self._index_struct.keywords]
        logger.info(f"> Extracted keywords: {keywords}")
        for k in keywords:
            for node_id in self._index_struct.table[k]:
                chunk_indices_count[node_id] += 1
        sorted_chunk_indices = sorted(
            chunk_indices_count.keys(),
            key=lambda x: chunk_indices_count[x],
            reverse=True,
        )
        sorted_chunk_indices = sorted_chunk_indices[: self.num_chunks_per_query]
        sorted_nodes = self._docstore.get_nodes(sorted_chunk_indices)

        if logging.getLogger(__name__).getEffectiveLevel() == logging.DEBUG:
            for chunk_idx, node in zip(sorted_chunk_indices, sorted_nodes):
                logger.debug(
                    f"> Querying with idx: {chunk_idx}: "
                    f"{truncate_text(node.get_content(),50)}"
                )
        return [NodeWithScore(node=node) for node in sorted_nodes]

```
 |  
| --- | --- |  
##  KeywordTableGPTRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/keyword/#llama_index.core.indices.keyword_table.retrievers.KeywordTableGPTRetriever "Permanent link")
Bases: 
Keyword Table Index GPT Retriever.
Extracts keywords using GPT. Set when using `retriever_mode="default"`.
See BaseGPTKeywordTableQuery for arguments.
Source code in `llama-index-core/llama_index/core/indices/keyword_table/retrievers.py`  
| 
```
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
```
 | 
```
classKeywordTableGPTRetriever(BaseKeywordTableRetriever):
"""
    Keyword Table Index GPT Retriever.

    Extracts keywords using GPT. Set when using `retriever_mode="default"`.

    See BaseGPTKeywordTableQuery for arguments.

    """

    def__init__(
        self,
        index: BaseKeywordTableIndex,
        keyword_extract_template: Optional[BasePromptTemplate] = None,
        query_keyword_extract_template: Optional[BasePromptTemplate] = None,
        max_keywords_per_query: int = 10,
        num_chunks_per_query: int = 10,
        llm: Optional[LLM] = None,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[dict] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._llm = llm or Settings.llm

        super().__init__(
            index=index,
            keyword_extract_template=keyword_extract_template,
            query_keyword_extract_template=query_keyword_extract_template,
            max_keywords_per_query=max_keywords_per_query,
            num_chunks_per_query=num_chunks_per_query,
            callback_manager=callback_manager or Settings.callback_manager,
            object_map=object_map,
            verbose=verbose,
        )

    def_get_keywords(self, query_str: str) -> List[str]:
"""Extract keywords."""
        response = self._llm.predict(
            self.query_keyword_extract_template,
            max_keywords=self.max_keywords_per_query,
            question=query_str,
        )
        keywords = extract_keywords_given_response(response, start_token="KEYWORDS:")
        return list(keywords)

```
 |  
| --- | --- |  
##  KeywordTableSimpleRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/keyword/#llama_index.core.indices.keyword_table.retrievers.KeywordTableSimpleRetriever "Permanent link")
Bases: 
Keyword Table Index Simple Retriever.
Extracts keywords using simple regex-based keyword extractor. Set when `retriever_mode="simple"`.
See BaseGPTKeywordTableQuery for arguments.
Source code in `llama-index-core/llama_index/core/indices/keyword_table/retrievers.py`  
| 
```
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
classKeywordTableSimpleRetriever(BaseKeywordTableRetriever):
"""
    Keyword Table Index Simple Retriever.

    Extracts keywords using simple regex-based keyword extractor.
    Set when `retriever_mode="simple"`.

    See BaseGPTKeywordTableQuery for arguments.

    """

    def_get_keywords(self, query_str: str) -> List[str]:
"""Extract keywords."""
        return list(
            simple_extract_keywords(query_str, max_keywords=self.max_keywords_per_query)
        )

```
 |  
| --- | --- |  
##  KeywordTableRAKERetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/keyword/#llama_index.core.indices.keyword_table.retrievers.KeywordTableRAKERetriever "Permanent link")
Bases: 
Keyword Table Index RAKE Retriever.
Extracts keywords using RAKE keyword extractor. Set when `retriever_mode="rake"`.
See BaseGPTKeywordTableQuery for arguments.
Source code in `llama-index-core/llama_index/core/indices/keyword_table/retrievers.py`  
| 
```
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
classKeywordTableRAKERetriever(BaseKeywordTableRetriever):
"""
    Keyword Table Index RAKE Retriever.

    Extracts keywords using RAKE keyword extractor.
    Set when `retriever_mode="rake"`.

    See BaseGPTKeywordTableQuery for arguments.

    """

    def_get_keywords(self, query_str: str) -> List[str]:
"""Extract keywords."""
        return list(
            rake_extract_keywords(query_str, max_keywords=self.max_keywords_per_query)
        )

```
 |  
| --- | --- |  
options: members: - BaseKeywordTableRetriever - KeywordTableGPTRetriever - KeywordTableSimpleRetriever - KeywordTableRAKERetriever
