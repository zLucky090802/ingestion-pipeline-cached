# Waii
##  WaiiToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/waii/#llama_index.tools.waii.WaiiToolSpec "Permanent link")
Bases: , 
Source code in `llama-index-integrations/tools/llama-index-tools-waii/llama_index/tools/waii/base.py`  
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
```
 | 
```
classWaiiToolSpec(BaseToolSpec, BaseReader):
    spec_functions = [
        "get_answer",
        "describe_query",
        "performance_analyze",
        "diff_query",
        "describe_dataset",
        "transcode",
        "get_semantic_contexts",
        "generate_query_only",
        "run_query",
    ]

    def__init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        database_key: Optional[str] = None,
        verbose: Optional[bool] = False,
    ) -> None:
        fromwaii_sdk_pyimport WAII

        WAII.initialize(url=url, api_key=api_key)
        WAII.Database.activate_connection(key=database_key)
        self.verbose = verbose

    def_try_display(self, obj) -> None:
        # only display when verbose is True, we don't want to display too much information by default.
        if self.verbose:
            try:
                fromIPython.displayimport display

                # display df if the function `display` is available (display only available when running with IPYTHON),
                # if it is not available, just ignore the exception.
                display(obj)
            except ImportError:
                # Handle the case where IPython is not available.
                pass

    def_run_query(self, sql: str, return_summary: bool) -> List[Document]:
        fromwaii_sdk_pyimport WAII
        fromwaii_sdk_py.queryimport RunQueryRequest

        run_result = WAII.Query.run(RunQueryRequest(query=sql))

        self._try_display(run_result.to_pandas_df())

        # create documents based on returned rows
        documents = [Document(text=str(doc)) for doc in run_result.rows]

        if return_summary:
            return self._get_summarization(
                "Summarize the result in text, don't miss any detail.", documents
            )

        return documents

    defload_data(self, ask: str) -> List[Document]:
"""
        Query using natural language and load data from the Database, returning a list of Documents.

        Args:
            ask: a natural language question.

        Returns:
            List[Document]: A list of Document objects.

        """
        query = self.generate_query_only(ask)

        return self._run_query(query, False)

    def_get_summarization(self, original_ask: str, documents) -> Any:
        texts = []

        n_chars = 0
        for i in range(len(documents)):
            t = str(documents[i].text)
            if len(t) + n_chars  8192:
                texts.append(f"... {len(documents)-i} more results")
                break
            texts.append(t)
            n_chars += len(t)

        summarizer = TreeSummarize()
        return summarizer.get_response(original_ask, texts)

    defget_answer(self, ask: str) -> List[Document]:
"""
        Generate a SQL query and run it against the database, returning the summarization of the answer
        Args:
            ask: a natural language question.

        Returns:
            str: A string containing the summarization of the answer.

        """
        query = self.generate_query_only(ask)

        return self._run_query(query, True)

    defgenerate_query_only(self, ask: str) -> str:
"""
        Generate a SQL query and NOT run it, returning the query. If you need to get answer, you should use get_answer instead.

        Args:
            ask: a natural language question.

        Returns:
            str: A string containing the query.

        """
        fromwaii_sdk_pyimport WAII
        fromwaii_sdk_py.queryimport QueryGenerationRequest

        query = WAII.Query.generate(QueryGenerationRequest(ask=ask)).query

        self._try_display(query)

        return query

    defrun_query(self, sql: str) -> List[Document]:
        return self._run_query(sql, False)

    defdescribe_query(self, question: str, query: str) -> str:
"""
        Describe a sql query, returning the summarization of the answer.

        Args:
            question: a natural language question which the people want to ask.
            query: a sql query.

        Returns:
            str: A string containing the summarization of the answer.

        """
        fromwaii_sdk_pyimport WAII
        fromwaii_sdk_py.queryimport DescribeQueryRequest

        result = WAII.Query.describe(DescribeQueryRequest(query=query))
        result = json.dumps(result.dict(), indent=2)
        self._try_display(result)

        return self._get_summarization(question, [Document(text=result)])

    defperformance_analyze(self, query_uuid: str) -> str:
"""
        Analyze the performance of a query, returning the summarization of the answer.

        Args:
            query_uuid: a query uuid, e.g. xxxxxxxxxxxxx...

        Returns:
            str: A string containing the summarization of the answer.

        """
        fromwaii_sdk_pyimport WAII
        fromwaii_sdk_py.queryimport QueryPerformanceRequest

        result = WAII.Query.analyze_performance(
            QueryPerformanceRequest(query_id=query_uuid)
        )
        return json.dumps(result.dict(), indent=2)

    defdiff_query(self, previous_query: str, current_query: str) -> str:
"""
        Diff two sql queries, returning the summarization of the answer.

        Args:
            previous_query: previous sql query.
            current_query: current sql query.

        Returns:
            str: A string containing the summarization of the answer.

        """
        fromwaii_sdk_pyimport WAII
        fromwaii_sdk_py.queryimport DiffQueryRequest

        result = WAII.Query.diff(
            DiffQueryRequest(query=current_query, previous_query=previous_query)
        )
        result = json.dumps(result.dict(), indent=2)
        return self._get_summarization("get diff summary", [Document(text=result)])

    defdescribe_dataset(
        self,
        ask: str,
        schema_name: Optional[str] = None,
        table_name: Optional[str] = None,
    ) -> str:
"""
        Describe a dataset (no matter if it is a table or schema), returning the summarization of the answer.
        Example questions like: "describe the dataset", "what the schema is about", "example question for the table xxx", etc.
        When both schema and table are None, describe the whole database.

        Args:
            ask: a natural language question (how you want to describe the dataset).
            schema_name: a schema name (shouldn't include the database name or the table name).
            table_name: a table name. (shouldn't include the database name or the schema name).

        Returns:
            str: A string containing the summarization of the answer.

        """
        fromwaii_sdk_pyimport WAII

        catalog = WAII.Database.get_catalogs()

        # filter by schema / table
        schemas = {}
        tables = {}

        for c in catalog.catalogs:
            for s in c.schemas:
                for t in s.tables:
                    if (
                        schema_name is not None
                        and schema_name.lower() != t.name.schema_name.lower()
                    ):
                        continue
                    if table_name is not None:
                        if table_name.lower() != t.name.table_name.lower():
                            continue
                        tables[str(t.name)] = t
                    schemas[str(s.name)] = s

        # remove tables ref from schemas
        for schema in schemas:
            schemas[schema].tables = None

        # generate response
        return self._get_summarization(
            ask + ", use the provided information to get comprehensive summarization",
            [Document(text=str(schemas[schema])) for schema in schemas]
            + [Document(text=str(tables[table])) for table in tables],
        )

    deftranscode(
        self,
        instruction: Optional[str] = "",
        source_dialect: Optional[str] = None,
        source_query: Optional[str] = None,
        target_dialect: Optional[str] = None,
    ) -> str:
"""
        Transcode a sql query from one dialect to another, returning generated query.

        Args:
            instruction: instruction in natural language.
            source_dialect: the source dialect of the query.
            source_query: the source query.
            target_dialect: the target dialect of the query.

        Returns:
            str: A string containing the generated query.

        """
        fromwaii_sdk_pyimport WAII
        fromwaii_sdk_py.queryimport TranscodeQueryRequest

        result = WAII.Query.transcode(
            TranscodeQueryRequest(
                ask=instruction,
                source_dialect=source_dialect,
                source_query=source_query,
                target_dialect=target_dialect,
            )
        )
        return result.query

    defget_semantic_contexts(self) -> Any:
"""Get all pre-defined semantic contexts."""
        fromwaii_sdk_pyimport WAII

        return WAII.SemanticContext.get_semantic_context().semantic_context

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/waii/#llama_index.tools.waii.WaiiToolSpec.load_data "Permanent link")

```
load_data(ask: ) -> []

```

Query using natural language and load data from the Database, returning a list of Documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ask`  |  a natural language question.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-waii/llama_index/tools/waii/base.py`  
| 
```
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
defload_data(self, ask: str) -> List[Document]:
"""
    Query using natural language and load data from the Database, returning a list of Documents.

    Args:
        ask: a natural language question.

    Returns:
        List[Document]: A list of Document objects.

    """
    query = self.generate_query_only(ask)

    return self._run_query(query, False)

```
 |  
| --- | --- |  
###  get_answer [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/waii/#llama_index.tools.waii.WaiiToolSpec.get_answer "Permanent link")

```
get_answer(ask: ) -> []

```

Generate a SQL query and run it against the database, returning the summarization of the answer Args: ask: a natural language question.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |   |  A string containing the summarization of the answer.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-waii/llama_index/tools/waii/base.py`  
| 
```
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
```
 | 
```
defget_answer(self, ask: str) -> List[Document]:
"""
    Generate a SQL query and run it against the database, returning the summarization of the answer
    Args:
        ask: a natural language question.

    Returns:
        str: A string containing the summarization of the answer.

    """
    query = self.generate_query_only(ask)

    return self._run_query(query, True)

```
 |  
| --- | --- |  
###  generate_query_only [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/waii/#llama_index.tools.waii.WaiiToolSpec.generate_query_only "Permanent link")

```
generate_query_only(ask: ) -> 

```

Generate a SQL query and NOT run it, returning the query. If you need to get answer, you should use get_answer instead.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ask`  |  a natural language question.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A string containing the query.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-waii/llama_index/tools/waii/base.py`  
| 
```
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
```
 | 
```
defgenerate_query_only(self, ask: str) -> str:
"""
    Generate a SQL query and NOT run it, returning the query. If you need to get answer, you should use get_answer instead.

    Args:
        ask: a natural language question.

    Returns:
        str: A string containing the query.

    """
    fromwaii_sdk_pyimport WAII
    fromwaii_sdk_py.queryimport QueryGenerationRequest

    query = WAII.Query.generate(QueryGenerationRequest(ask=ask)).query

    self._try_display(query)

    return query

```
 |  
| --- | --- |  
###  describe_query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/waii/#llama_index.tools.waii.WaiiToolSpec.describe_query "Permanent link")

```
describe_query(question: , query: ) -> 

```

Describe a sql query, returning the summarization of the answer.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `question`  |  a natural language question which the people want to ask.  |  _required_  |  
|  `query`  |  a sql query.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A string containing the summarization of the answer.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-waii/llama_index/tools/waii/base.py`  
| 
```
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
```
 | 
```
defdescribe_query(self, question: str, query: str) -> str:
"""
    Describe a sql query, returning the summarization of the answer.

    Args:
        question: a natural language question which the people want to ask.
        query: a sql query.

    Returns:
        str: A string containing the summarization of the answer.

    """
    fromwaii_sdk_pyimport WAII
    fromwaii_sdk_py.queryimport DescribeQueryRequest

    result = WAII.Query.describe(DescribeQueryRequest(query=query))
    result = json.dumps(result.dict(), indent=2)
    self._try_display(result)

    return self._get_summarization(question, [Document(text=result)])

```
 |  
| --- | --- |  
###  performance_analyze [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/waii/#llama_index.tools.waii.WaiiToolSpec.performance_analyze "Permanent link")

```
performance_analyze(query_uuid: ) -> 

```

Analyze the performance of a query, returning the summarization of the answer.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_uuid`  |  a query uuid, e.g. xxxxxxxxxxxxx...  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A string containing the summarization of the answer.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-waii/llama_index/tools/waii/base.py`  
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
```
 | 
```
defperformance_analyze(self, query_uuid: str) -> str:
"""
    Analyze the performance of a query, returning the summarization of the answer.

    Args:
        query_uuid: a query uuid, e.g. xxxxxxxxxxxxx...

    Returns:
        str: A string containing the summarization of the answer.

    """
    fromwaii_sdk_pyimport WAII
    fromwaii_sdk_py.queryimport QueryPerformanceRequest

    result = WAII.Query.analyze_performance(
        QueryPerformanceRequest(query_id=query_uuid)
    )
    return json.dumps(result.dict(), indent=2)

```
 |  
| --- | --- |  
###  diff_query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/waii/#llama_index.tools.waii.WaiiToolSpec.diff_query "Permanent link")

```
diff_query(previous_query: , current_query: ) -> 

```

Diff two sql queries, returning the summarization of the answer.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `previous_query`  |  previous sql query.  |  _required_  |  
|  `current_query`  |  current sql query.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A string containing the summarization of the answer.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-waii/llama_index/tools/waii/base.py`  
| 
```
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
```
 | 
```
defdiff_query(self, previous_query: str, current_query: str) -> str:
"""
    Diff two sql queries, returning the summarization of the answer.

    Args:
        previous_query: previous sql query.
        current_query: current sql query.

    Returns:
        str: A string containing the summarization of the answer.

    """
    fromwaii_sdk_pyimport WAII
    fromwaii_sdk_py.queryimport DiffQueryRequest

    result = WAII.Query.diff(
        DiffQueryRequest(query=current_query, previous_query=previous_query)
    )
    result = json.dumps(result.dict(), indent=2)
    return self._get_summarization("get diff summary", [Document(text=result)])

```
 |  
| --- | --- |  
###  describe_dataset [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/waii/#llama_index.tools.waii.WaiiToolSpec.describe_dataset "Permanent link")

```
describe_dataset(
    ask: ,
    schema_name: Optional[] = None,
    table_name: Optional[] = None,
) -> 

```

Describe a dataset (no matter if it is a table or schema), returning the summarization of the answer. Example questions like: "describe the dataset", "what the schema is about", "example question for the table xxx", etc. When both schema and table are None, describe the whole database.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ask`  |  a natural language question (how you want to describe the dataset).  |  _required_  |  
|  `schema_name`  |  `Optional[str]`  |  a schema name (shouldn't include the database name or the table name).  |  `None`  |  
|  `table_name`  |  `Optional[str]`  |  a table name. (shouldn't include the database name or the schema name).  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A string containing the summarization of the answer.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-waii/llama_index/tools/waii/base.py`  
| 
```
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
```
 | 
```
defdescribe_dataset(
    self,
    ask: str,
    schema_name: Optional[str] = None,
    table_name: Optional[str] = None,
) -> str:
"""
    Describe a dataset (no matter if it is a table or schema), returning the summarization of the answer.
    Example questions like: "describe the dataset", "what the schema is about", "example question for the table xxx", etc.
    When both schema and table are None, describe the whole database.

    Args:
        ask: a natural language question (how you want to describe the dataset).
        schema_name: a schema name (shouldn't include the database name or the table name).
        table_name: a table name. (shouldn't include the database name or the schema name).

    Returns:
        str: A string containing the summarization of the answer.

    """
    fromwaii_sdk_pyimport WAII

    catalog = WAII.Database.get_catalogs()

    # filter by schema / table
    schemas = {}
    tables = {}

    for c in catalog.catalogs:
        for s in c.schemas:
            for t in s.tables:
                if (
                    schema_name is not None
                    and schema_name.lower() != t.name.schema_name.lower()
                ):
                    continue
                if table_name is not None:
                    if table_name.lower() != t.name.table_name.lower():
                        continue
                    tables[str(t.name)] = t
                schemas[str(s.name)] = s

    # remove tables ref from schemas
    for schema in schemas:
        schemas[schema].tables = None

    # generate response
    return self._get_summarization(
        ask + ", use the provided information to get comprehensive summarization",
        [Document(text=str(schemas[schema])) for schema in schemas]
        + [Document(text=str(tables[table])) for table in tables],
    )

```
 |  
| --- | --- |  
###  transcode [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/waii/#llama_index.tools.waii.WaiiToolSpec.transcode "Permanent link")

```
transcode(
    instruction: Optional[] = "",
    source_dialect: Optional[] = None,
    source_query: Optional[] = None,
    target_dialect: Optional[] = None,
) -> 

```

Transcode a sql query from one dialect to another, returning generated query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `instruction`  |  `Optional[str]`  |  instruction in natural language.  |  
|  `source_dialect`  |  `Optional[str]`  |  the source dialect of the query.  |  `None`  |  
|  `source_query`  |  `Optional[str]`  |  the source query.  |  `None`  |  
|  `target_dialect`  |  `Optional[str]`  |  the target dialect of the query.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A string containing the generated query.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-waii/llama_index/tools/waii/base.py`  
| 
```
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
```
 | 
```
deftranscode(
    self,
    instruction: Optional[str] = "",
    source_dialect: Optional[str] = None,
    source_query: Optional[str] = None,
    target_dialect: Optional[str] = None,
) -> str:
"""
    Transcode a sql query from one dialect to another, returning generated query.

    Args:
        instruction: instruction in natural language.
        source_dialect: the source dialect of the query.
        source_query: the source query.
        target_dialect: the target dialect of the query.

    Returns:
        str: A string containing the generated query.

    """
    fromwaii_sdk_pyimport WAII
    fromwaii_sdk_py.queryimport TranscodeQueryRequest

    result = WAII.Query.transcode(
        TranscodeQueryRequest(
            ask=instruction,
            source_dialect=source_dialect,
            source_query=source_query,
            target_dialect=target_dialect,
        )
    )
    return result.query

```
 |  
| --- | --- |  
###  get_semantic_contexts [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/waii/#llama_index.tools.waii.WaiiToolSpec.get_semantic_contexts "Permanent link")

```
get_semantic_contexts() -> 

```

Get all pre-defined semantic contexts.
Source code in `llama-index-integrations/tools/llama-index-tools-waii/llama_index/tools/waii/base.py`  
| 
```
283
284
285
286
287
```
 | 
```
defget_semantic_contexts(self) -> Any:
"""Get all pre-defined semantic contexts."""
    fromwaii_sdk_pyimport WAII

    return WAII.SemanticContext.get_semantic_context().semantic_context

```
 |  
| --- | --- |  
options: members: - WaiiToolSpec
