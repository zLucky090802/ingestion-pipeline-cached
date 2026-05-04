# Pandas
##  PandasQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/pandas/#llama_index.experimental.query_engine.PandasQueryEngine "Permanent link")
Bases: 
Pandas query engine.
Convert natural language to Pandas python code.
WARNING: This tool provides the Agent access to the `eval` function. Arbitrary code execution is possible on the machine running this tool. This tool is not recommended to be used in a production setting, and would require heavy sandboxing or virtual machines
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `DataFrame`  |  Pandas dataframe to use.  |  _required_  |  
|  `instruction_str`  |  `Optional[str]`  |  Instruction string to use.  |  `None`  |  
|  `instruction_parser`  |  `Optional[PandasInstructionParser[](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/pandas/#llama_index.experimental.query_engine.PandasInstructionParser "PandasInstructionParser \(llama_index.experimental.query_engine.pandas.output_parser.PandasInstructionParser\)")]`  |  The output parser that takes the pandas query output string and returns a string. It defaults to PandasInstructionParser and takes pandas DataFrame, and any output kwargs as parameters. eg.kwargs["max_colwidth"] = [int] is used to set the length of text that each column can display during str(df). Set it to a higher number if there is possibly long text in the dataframe.  |  `None`  |  
|  `pandas_prompt`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  Pandas prompt to use.  |  `None`  |  
|  `output_kwargs`  |  `dict`  |  Additional output processor kwargs for the PandasInstructionParser.  |  `None`  |  
|  `head`  |  Number of rows to show in the table context.  |  
|  `verbose`  |  `bool`  |  Whether to print verbose output.  |  `False`  |  
|  `llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.llm.LLM\)")]`  |  Language model to use.  |  `None`  |  
|  `synthesize_response`  |  `bool`  |  Whether to synthesize a response from the query results. Defaults to False.  |  `False`  |  
|  `response_synthesis_prompt`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Response Synthesis BasePromptTemplate to use for the query. Defaults to DEFAULT_RESPONSE_SYNTHESIS_PROMPT.  |  `None`  |  
Examples:
`pip install llama-index-experimental`

```
importpandasaspd
fromllama_index.experimental.query_engine.pandasimport PandasQueryEngine

df = pd.DataFrame(
    {
        "city": ["Toronto", "Tokyo", "Berlin"],
        "population": [2930000, 13960000, 3645000]
    }
)

query_engine = PandasQueryEngine(df=df, verbose=True)

response = query_engine.query("What is the population of Tokyo?")

```

Source code in `llama-index-experimental/llama_index/experimental/query_engine/pandas/pandas_query_engine.py`  
| 
```
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
```
 | 
```
classPandasQueryEngine(BaseQueryEngine):
"""
    Pandas query engine.

    Convert natural language to Pandas python code.

    WARNING: This tool provides the Agent access to the `eval` function.
    Arbitrary code execution is possible on the machine running this tool.
    This tool is not recommended to be used in a production setting, and would
    require heavy sandboxing or virtual machines


    Args:
        df (pd.DataFrame): Pandas dataframe to use.
        instruction_str (Optional[str]): Instruction string to use.
        instruction_parser (Optional[PandasInstructionParser]): The output parser
            that takes the pandas query output string and returns a string.
            It defaults to PandasInstructionParser and takes pandas DataFrame,
            and any output kwargs as parameters.
            eg.kwargs["max_colwidth"] = [int] is used to set the length of text
            that each column can display during str(df). Set it to a higher number
            if there is possibly long text in the dataframe.
        pandas_prompt (Optional[BasePromptTemplate]): Pandas prompt to use.
        output_kwargs (dict): Additional output processor kwargs for the
            PandasInstructionParser.
        head (int): Number of rows to show in the table context.
        verbose (bool): Whether to print verbose output.
        llm (Optional[LLM]): Language model to use.
        synthesize_response (bool): Whether to synthesize a response from the
            query results. Defaults to False.
        response_synthesis_prompt (Optional[BasePromptTemplate]): A
            Response Synthesis BasePromptTemplate to use for the query. Defaults to
            DEFAULT_RESPONSE_SYNTHESIS_PROMPT.

    Examples:
        `pip install llama-index-experimental`

        ```python
        import pandas as pd
        from llama_index.experimental.query_engine.pandas import PandasQueryEngine

        df = pd.DataFrame(

                "city": ["Toronto", "Tokyo", "Berlin"],
                "population": [2930000, 13960000, 3645000]



        query_engine = PandasQueryEngine(df=df, verbose=True)

        response = query_engine.query("What is the population of Tokyo?")
        ```

    """

    def__init__(
        self,
        df: pd.DataFrame,
        instruction_str: Optional[str] = None,
        instruction_parser: Optional[PandasInstructionParser] = None,
        pandas_prompt: Optional[BasePromptTemplate] = None,
        output_kwargs: Optional[dict] = None,
        head: int = 5,
        verbose: bool = False,
        llm: Optional[LLM] = None,
        synthesize_response: bool = False,
        response_synthesis_prompt: Optional[BasePromptTemplate] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._df = df

        self._head = head
        self._pandas_prompt = pandas_prompt or DEFAULT_PANDAS_PROMPT
        self._instruction_str = instruction_str or DEFAULT_INSTRUCTION_STR
        self._instruction_parser = instruction_parser or PandasInstructionParser(
            df, output_kwargs or {}
        )
        self._verbose = verbose

        self._llm = llm or Settings.llm
        self._synthesize_response = synthesize_response
        self._response_synthesis_prompt = (
            response_synthesis_prompt or DEFAULT_RESPONSE_SYNTHESIS_PROMPT
        )

        super().__init__(callback_manager=Settings.callback_manager)

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {}

    def_get_prompts(self) -> Dict[str, Any]:
"""Get prompts."""
        return {
            "pandas_prompt": self._pandas_prompt,
            "response_synthesis_prompt": self._response_synthesis_prompt,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "pandas_prompt" in prompts:
            self._pandas_prompt = prompts["pandas_prompt"]
        if "response_synthesis_prompt" in prompts:
            self._response_synthesis_prompt = prompts["response_synthesis_prompt"]

    @classmethod
    deffrom_index(cls, index: PandasIndex, **kwargs: Any) -> "PandasQueryEngine":
        logger.warning(
            "PandasIndex is deprecated. "
            "Directly construct PandasQueryEngine with df instead."
        )
        return cls(df=index.df, **kwargs)

    def_get_table_context(self) -> str:
"""Get table context."""
        pd.set_option("display.max_colwidth", None)
        pd.set_option("display.max_columns", None)
        # since head() is only used.
        pd.set_option("display.max_rows", self._head)
        pd.set_option("display.width", None)
        return str(self._df.head(self._head))

    def_query(self, query_bundle: QueryBundle) -> Response:
"""Answer a query."""
        context = self._get_table_context()

        pandas_response_str = self._llm.predict(
            self._pandas_prompt,
            df_str=context,
            query_str=query_bundle.query_str,
            instruction_str=self._instruction_str,
        )

        if self._verbose:
            print_text(f"> Pandas Instructions:\n```\n{pandas_response_str}\n```\n")
        pandas_output = self._instruction_parser.parse(pandas_response_str)
        if self._verbose:
            print_text(f"> Pandas Output: {pandas_output}\n")

        response_metadata = {
            "pandas_instruction_str": pandas_response_str,
            "raw_pandas_output": pandas_output,
        }
        if self._synthesize_response:
            response_str = str(
                self._llm.predict(
                    self._response_synthesis_prompt,
                    query_str=query_bundle.query_str,
                    pandas_instructions=pandas_response_str,
                    pandas_output=pandas_output,
                )
            )
        else:
            response_str = str(pandas_output)

        return Response(response=response_str, metadata=response_metadata)

    async def_aquery(self, query_bundle: QueryBundle) -> Response:
"""Answer a query asynchronously."""
        context = self._get_table_context()

        pandas_response_str = await self._llm.apredict(
            self._pandas_prompt,
            df_str=context,
            query_str=query_bundle.query_str,
            instruction_str=self._instruction_str,
        )

        if self._verbose:
            print_text(f"> Pandas Instructions:\n```\n{pandas_response_str}\n```\n")
        pandas_output = self._instruction_parser.parse(pandas_response_str)
        if self._verbose:
            print_text(f"> Pandas Output: {pandas_output}\n")

        response_metadata = {
            "pandas_instruction_str": pandas_response_str,
            "raw_pandas_output": pandas_output,
        }
        if self._synthesize_response:
            response_str = str(
                await self._llm.apredict(
                    self._response_synthesis_prompt,
                    query_str=query_bundle.query_str,
                    pandas_instructions=pandas_response_str,
                    pandas_output=pandas_output,
                )
            )
        else:
            response_str = str(pandas_output)

        return Response(response=response_str, metadata=response_metadata)

```
 |  
| --- | --- |  
##  PandasInstructionParser [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/pandas/#llama_index.experimental.query_engine.PandasInstructionParser "Permanent link")
Bases: 
Pandas instruction parser.
This 'output parser' takes in pandas instructions (in Python code) and executes them to return an output.
Source code in `llama-index-experimental/llama_index/experimental/query_engine/pandas/output_parser.py`  
| 
```
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
```
 | 
```
classPandasInstructionParser(BaseOutputParser):
"""
    Pandas instruction parser.

    This 'output parser' takes in pandas instructions (in Python code) and
    executes them to return an output.

    """

    def__init__(
        self, df: pd.DataFrame, output_kwargs: Optional[Dict[str, Any]] = None
    ) -> None:
"""Initialize params."""
        self.df = df
        self.output_kwargs = output_kwargs or {}

    defparse(self, output: str) -> Any:
"""Parse, validate, and correct errors programmatically."""
        return default_output_processor(output, self.df, **self.output_kwargs)

```
 |  
| --- | --- |  
###  parse [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/pandas/#llama_index.experimental.query_engine.PandasInstructionParser.parse "Permanent link")

```
parse(output: ) -> 

```

Parse, validate, and correct errors programmatically.
Source code in `llama-index-experimental/llama_index/experimental/query_engine/pandas/output_parser.py`  
| 
```
94
95
96
```
 | 
```
defparse(self, output: str) -> Any:
"""Parse, validate, and correct errors programmatically."""
    return default_output_processor(output, self.df, **self.output_kwargs)

```
 |  
| --- | --- |  
##  PolarsQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/pandas/#llama_index.experimental.query_engine.PolarsQueryEngine "Permanent link")
Bases: 
Polars query engine.
Convert natural language to Polars python code.
WARNING: This tool provides the Agent access to the `eval` function. Arbitrary code execution is possible on the machine running this tool. This tool is not recommended to be used in a production setting, and would require heavy sandboxing or virtual machines
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `DataFrame`  |  Polars dataframe to use.  |  _required_  |  
|  `instruction_str`  |  `Optional[str]`  |  Instruction string to use.  |  `None`  |  
|  `instruction_parser`  |  `Optional[PolarsInstructionParser[](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/pandas/#llama_index.experimental.query_engine.PolarsInstructionParser "PolarsInstructionParser \(llama_index.experimental.query_engine.polars.output_parser.PolarsInstructionParser\)")]`  |  The output parser that takes the polars query output string and returns a string. It defaults to PolarsInstructionParser and takes polars DataFrame, and any output kwargs as parameters.  |  `None`  |  
|  `polars_prompt`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  Polars prompt to use.  |  `None`  |  
|  `output_kwargs`  |  `dict`  |  Additional output processor kwargs for the PolarsInstructionParser.  |  `None`  |  
|  `head`  |  Number of rows to show in the table context.  |  
|  `verbose`  |  `bool`  |  Whether to print verbose output.  |  `False`  |  
|  `llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.llm.LLM\)")]`  |  Language model to use.  |  `None`  |  
|  `synthesize_response`  |  `bool`  |  Whether to synthesize a response from the query results. Defaults to False.  |  `False`  |  
|  `response_synthesis_prompt`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Response Synthesis BasePromptTemplate to use for the query. Defaults to DEFAULT_RESPONSE_SYNTHESIS_PROMPT.  |  `None`  |  
Examples:
`pip install llama-index-experimental polars`

```
importpolarsaspl
fromllama_index.experimental.query_engine.polarsimport PolarsQueryEngine

df = pl.DataFrame(
    {
        "city": ["Toronto", "Tokyo", "Berlin"],
        "population": [2930000, 13960000, 3645000]
    }
)

query_engine = PolarsQueryEngine(df=df, verbose=True)

response = query_engine.query("What is the population of Tokyo?")

```

Source code in `llama-index-experimental/llama_index/experimental/query_engine/polars/polars_query_engine.py`  
| 
```
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
```
 | 
```
classPolarsQueryEngine(BaseQueryEngine):
"""
    Polars query engine.

    Convert natural language to Polars python code.

    WARNING: This tool provides the Agent access to the `eval` function.
    Arbitrary code execution is possible on the machine running this tool.
    This tool is not recommended to be used in a production setting, and would
    require heavy sandboxing or virtual machines


    Args:
        df (pl.DataFrame): Polars dataframe to use.
        instruction_str (Optional[str]): Instruction string to use.
        instruction_parser (Optional[PolarsInstructionParser]): The output parser
            that takes the polars query output string and returns a string.
            It defaults to PolarsInstructionParser and takes polars DataFrame,
            and any output kwargs as parameters.
        polars_prompt (Optional[BasePromptTemplate]): Polars prompt to use.
        output_kwargs (dict): Additional output processor kwargs for the
            PolarsInstructionParser.
        head (int): Number of rows to show in the table context.
        verbose (bool): Whether to print verbose output.
        llm (Optional[LLM]): Language model to use.
        synthesize_response (bool): Whether to synthesize a response from the
            query results. Defaults to False.
        response_synthesis_prompt (Optional[BasePromptTemplate]): A
            Response Synthesis BasePromptTemplate to use for the query. Defaults to
            DEFAULT_RESPONSE_SYNTHESIS_PROMPT.

    Examples:
        `pip install llama-index-experimental polars`

        ```python
        import polars as pl
        from llama_index.experimental.query_engine.polars import PolarsQueryEngine

        df = pl.DataFrame(

                "city": ["Toronto", "Tokyo", "Berlin"],
                "population": [2930000, 13960000, 3645000]



        query_engine = PolarsQueryEngine(df=df, verbose=True)

        response = query_engine.query("What is the population of Tokyo?")
        ```

    """

    def__init__(
        self,
        df: pl.DataFrame,
        instruction_str: Optional[str] = None,
        instruction_parser: Optional[PolarsInstructionParser] = None,
        polars_prompt: Optional[BasePromptTemplate] = None,
        output_kwargs: Optional[dict] = None,
        head: int = 5,
        verbose: bool = False,
        llm: Optional[LLM] = None,
        synthesize_response: bool = False,
        response_synthesis_prompt: Optional[BasePromptTemplate] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._df = df

        self._head = head
        self._polars_prompt = polars_prompt or DEFAULT_POLARS_PROMPT
        self._instruction_str = instruction_str or DEFAULT_INSTRUCTION_STR
        self._instruction_parser = instruction_parser or PolarsInstructionParser(
            df, output_kwargs or {}
        )
        self._verbose = verbose

        self._llm = llm or Settings.llm
        self._synthesize_response = synthesize_response
        self._response_synthesis_prompt = (
            response_synthesis_prompt or DEFAULT_RESPONSE_SYNTHESIS_PROMPT
        )

        super().__init__(callback_manager=Settings.callback_manager)

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {}

    def_get_prompts(self) -> Dict[str, Any]:
"""Get prompts."""
        return {
            "polars_prompt": self._polars_prompt,
            "response_synthesis_prompt": self._response_synthesis_prompt,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "polars_prompt" in prompts:
            self._polars_prompt = prompts["polars_prompt"]
        if "response_synthesis_prompt" in prompts:
            self._response_synthesis_prompt = prompts["response_synthesis_prompt"]

    def_get_table_context(self) -> str:
"""Get table context."""
        return str(self._df.head(self._head))

    def_query(self, query_bundle: QueryBundle) -> Response:
"""Answer a query."""
        context = self._get_table_context()

        polars_response_str = self._llm.predict(
            self._polars_prompt,
            df_str=context,
            query_str=query_bundle.query_str,
            instruction_str=self._instruction_str,
        )

        if self._verbose:
            print_text(f"> Polars Instructions:\n```\n{polars_response_str}\n```\n")
        polars_output = self._instruction_parser.parse(polars_response_str)
        if self._verbose:
            print_text(f"> Polars Output: {polars_output}\n")

        response_metadata = {
            "polars_instruction_str": polars_response_str,
            "raw_polars_output": polars_output,
        }
        if self._synthesize_response:
            response_str = str(
                self._llm.predict(
                    self._response_synthesis_prompt,
                    query_str=query_bundle.query_str,
                    polars_instructions=polars_response_str,
                    polars_output=polars_output,
                )
            )
        else:
            response_str = str(polars_output)

        return Response(response=response_str, metadata=response_metadata)

    async def_aquery(self, query_bundle: QueryBundle) -> Response:
"""Answer a query asynchronously."""
        context = self._get_table_context()

        polars_response_str = await self._llm.apredict(
            self._polars_prompt,
            df_str=context,
            query_str=query_bundle.query_str,
            instruction_str=self._instruction_str,
        )

        if self._verbose:
            print_text(f"> Polars Instructions:\n```\n{polars_response_str}\n```\n")
        polars_output = self._instruction_parser.parse(polars_response_str)
        if self._verbose:
            print_text(f"> Polars Output: {polars_output}\n")

        response_metadata = {
            "polars_instruction_str": polars_response_str,
            "raw_polars_output": polars_output,
        }
        if self._synthesize_response:
            response_str = str(
                await self._llm.apredict(
                    self._response_synthesis_prompt,
                    query_str=query_bundle.query_str,
                    polars_instructions=polars_response_str,
                    polars_output=polars_output,
                )
            )
        else:
            response_str = str(polars_output)

        return Response(response=response_str, metadata=response_metadata)

```
 |  
| --- | --- |  
##  PolarsInstructionParser [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/pandas/#llama_index.experimental.query_engine.PolarsInstructionParser "Permanent link")
Bases: 
Polars instruction parser.
This 'output parser' takes in polars instructions (in Python code) and executes them to return an output.
Source code in `llama-index-experimental/llama_index/experimental/query_engine/polars/output_parser.py`  
| 
```
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
```
 | 
```
classPolarsInstructionParser(BaseOutputParser):
"""
    Polars instruction parser.

    This 'output parser' takes in polars instructions (in Python code) and
    executes them to return an output.

    """

    def__init__(
        self, df: pl.DataFrame, output_kwargs: Optional[Dict[str, Any]] = None
    ) -> None:
"""Initialize params."""
        self.df = df
        self.output_kwargs = output_kwargs or {}

    defparse(self, output: str) -> Any:
"""Parse, validate, and correct errors programmatically."""
        return default_output_processor(output, self.df, **self.output_kwargs)

```
 |  
| --- | --- |  
###  parse [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/pandas/#llama_index.experimental.query_engine.PolarsInstructionParser.parse "Permanent link")

```
parse(output: ) -> 

```

Parse, validate, and correct errors programmatically.
Source code in `llama-index-experimental/llama_index/experimental/query_engine/polars/output_parser.py`  
| 
```
104
105
106
```
 | 
```
defparse(self, output: str) -> Any:
"""Parse, validate, and correct errors programmatically."""
    return default_output_processor(output, self.df, **self.output_kwargs)

```
 |  
| --- | --- |  
##  JSONalyzeQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/pandas/#llama_index.experimental.query_engine.JSONalyzeQueryEngine "Permanent link")
Bases: 
JSON List Shape Data Analysis Query Engine.
Converts natural language statasical queries to SQL within in-mem SQLite queries.
list_of_dict(List[Dict[str, Any]]): List of dictionaries to query. jsonalyze_prompt (BasePromptTemplate): The JSONalyze prompt to use. use_async (bool): Whether to use async. analyzer (Callable): The analyzer that executes the query. sql_parser (BaseSQLParser): The SQL parser that ensures valid SQL being parsed from llm output. synthesize_response (bool): Whether to synthesize a response. response_synthesis_prompt (BasePromptTemplate): The response synthesis prompt to use. table_name (str): The table name to use. verbose (bool): Whether to print verbose output.
Source code in `llama-index-experimental/llama_index/experimental/query_engine/jsonalyze/jsonalyze_query_engine.py`  
| 
```
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
```
 | 
```
classJSONalyzeQueryEngine(BaseQueryEngine):
"""
    JSON List Shape Data Analysis Query Engine.

    Converts natural language statasical queries to SQL within in-mem SQLite queries.

    list_of_dict(List[Dict[str, Any]]): List of dictionaries to query.
    jsonalyze_prompt (BasePromptTemplate): The JSONalyze prompt to use.
    use_async (bool): Whether to use async.
    analyzer (Callable): The analyzer that executes the query.
    sql_parser (BaseSQLParser): The SQL parser that ensures valid SQL being parsed
        from llm output.
    synthesize_response (bool): Whether to synthesize a response.
    response_synthesis_prompt (BasePromptTemplate): The response synthesis prompt
        to use.
    table_name (str): The table name to use.
    verbose (bool): Whether to print verbose output.
    """

    def__init__(
        self,
        list_of_dict: List[Dict[str, Any]],
        llm: Optional[LLM] = None,
        jsonalyze_prompt: Optional[BasePromptTemplate] = None,
        use_async: bool = False,
        analyzer: Optional[Callable] = None,
        sql_parser: Optional[BaseSQLParser] = None,
        synthesize_response: bool = True,
        response_synthesis_prompt: Optional[BasePromptTemplate] = None,
        table_name: str = DEFAULT_TABLE_NAME,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._list_of_dict = list_of_dict
        self._llm = llm or Settings.llm
        self._jsonalyze_prompt = jsonalyze_prompt or DEFAULT_JSONALYZE_PROMPT
        self._use_async = use_async
        self._analyzer = load_jsonalyzer(use_async, analyzer)
        self._sql_parser = sql_parser or DefaultSQLParser()
        self._synthesize_response = synthesize_response
        self._response_synthesis_prompt = (
            response_synthesis_prompt or DEFAULT_RESPONSE_SYNTHESIS_PROMPT
        )
        self._table_name = table_name
        self._verbose = verbose

        super().__init__(callback_manager=Settings.callback_manager)

    def_get_prompts(self) -> Dict[str, Any]:
"""Get prompts."""
        return {
            "jsonalyze_prompt": self._jsonalyze_prompt,
            "response_synthesis_prompt": self._response_synthesis_prompt,
        }

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "jsonalyze_prompt" in prompts:
            self._jsonalyze_prompt = prompts["jsonalyze_prompt"]
        if "response_synthesis_prompt" in prompts:
            self._response_synthesis_prompt = prompts["response_synthesis_prompt"]

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {}

    def_query(self, query_bundle: QueryBundle) -> Response:
"""Answer an analytical query on the JSON List."""
        query = query_bundle.query_str
        if self._verbose:
            print_text(f"Query: {query}\n", color="green")

        # Perform the analysis
        sql_query, table_schema, results = self._analyzer(
            self._list_of_dict,
            query_bundle,
            self._llm,
            table_name=self._table_name,
            prompt=self._jsonalyze_prompt,
            sql_parser=self._sql_parser,
        )
        if self._verbose:
            print_text(f"SQL Query: {sql_query}\n", color="blue")
            print_text(f"Table Schema: {table_schema}\n", color="cyan")
            print_text(f"SQL Response: {results}\n", color="yellow")

        if self._synthesize_response:
            response_str = self._llm.predict(
                self._response_synthesis_prompt,
                sql_query=sql_query,
                table_schema=table_schema,
                sql_response=results,
                query_str=query_bundle.query_str,
            )
            if self._verbose:
                print_text(f"Response: {response_str}", color="magenta")
        else:
            response_str = str(results)
        response_metadata = {"sql_query": sql_query, "table_schema": str(table_schema)}

        return Response(response=response_str, metadata=response_metadata)

    async def_aquery(self, query_bundle: QueryBundle) -> Response:
"""Answer an analytical query on the JSON List."""
        query = query_bundle.query_str
        if self._verbose:
            print_text(f"Query: {query}", color="green")

        # Perform the analysis
        sql_query, table_schema, results = self._analyzer(
            self._list_of_dict,
            query,
            self._llm,
            table_name=self._table_name,
            prompt=self._jsonalyze_prompt,
        )
        if self._verbose:
            print_text(f"SQL Query: {sql_query}\n", color="blue")
            print_text(f"Table Schema: {table_schema}\n", color="cyan")
            print_text(f"SQL Response: {results}\n", color="yellow")

        if self._synthesize_response:
            response_str = await self._llm.apredict(
                self._response_synthesis_prompt,
                sql_query=sql_query,
                table_schema=table_schema,
                sql_response=results,
                query_str=query_bundle.query_str,
            )
            if self._verbose:
                print_text(f"Response: {response_str}", color="magenta")
        else:
            response_str = json.dumps(
                {
                    "sql_query": sql_query,
                    "table_schema": table_schema,
                    "sql_response": results,
                }
            )
        response_metadata = {"sql_query": sql_query, "table_schema": str(table_schema)}

        return Response(response=response_str, metadata=response_metadata)

```
 |  
| --- | --- |  
options: members: - PandasQueryEngine
