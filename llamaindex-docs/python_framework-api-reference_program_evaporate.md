# Evaporate
##  BaseEvaporateProgram [#](https://developers.llamaindex.ai/python/framework-api-reference/program/evaporate/#llama_index.program.evaporate.BaseEvaporateProgram "Permanent link")
Bases: , `Generic[Model]`
BaseEvaporate program.
You should provide the fields you want to extract. Then when you call the program you should pass in a list of training_data nodes and a list of infer_data nodes. The program will call the EvaporateExtractor to synthesize a python function from the training data and then apply the function to the infer_data.
Source code in `llama-index-integrations/program/llama-index-program-evaporate/llama_index/program/evaporate/base.py`  
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
```
 | 
```
classBaseEvaporateProgram(BasePydanticProgram, Generic[Model]):
"""
    BaseEvaporate program.

    You should provide the fields you want to extract.
    Then when you call the program you should pass in a list of training_data nodes
    and a list of infer_data nodes. The program will call the EvaporateExtractor
    to synthesize a python function from the training data and then apply the function
    to the infer_data.
    """

    def__init__(
        self,
        extractor: EvaporateExtractor,
        fields_to_extract: Optional[List[str]] = None,
        fields_context: Optional[Dict[str, Any]] = None,
        nodes_to_fit: Optional[List[BaseNode]] = None,
        verbose: bool = False,
    ) -> None:
"""Init params."""
        self._extractor = extractor
        self._fields = fields_to_extract or []
        self._fields_context = fields_context or {}
        # NOTE: this will change with each call to `fit`
        self._field_fns: Dict[str, str] = {}
        self._verbose = verbose

        # if nodes_to_fit is not None, then fit extractor
        if nodes_to_fit is not None:
            self._field_fns = self.fit_fields(nodes_to_fit)

    @classmethod
    deffrom_defaults(
        cls,
        fields_to_extract: Optional[List[str]] = None,
        fields_context: Optional[Dict[str, Any]] = None,
        llm: Optional[LLM] = None,
        schema_id_prompt: Optional[SchemaIDPrompt] = None,
        fn_generate_prompt: Optional[FnGeneratePrompt] = None,
        field_extract_query_tmpl: str = DEFAULT_FIELD_EXTRACT_QUERY_TMPL,
        nodes_to_fit: Optional[List[BaseNode]] = None,
        verbose: bool = False,
    ) -> "BaseEvaporateProgram":
"""Evaporate program."""
        extractor = EvaporateExtractor(
            llm=llm,
            schema_id_prompt=schema_id_prompt,
            fn_generate_prompt=fn_generate_prompt,
            field_extract_query_tmpl=field_extract_query_tmpl,
        )
        return cls(
            extractor,
            fields_to_extract=fields_to_extract,
            fields_context=fields_context,
            nodes_to_fit=nodes_to_fit,
            verbose=verbose,
        )

    @property
    defextractor(self) -> EvaporateExtractor:
"""Extractor."""
        return self._extractor

    defget_function_str(self, field: str) -> str:
"""Get function string."""
        return self._field_fns[field]

    defset_fields_to_extract(self, fields: List[str]) -> None:
"""Set fields to extract."""
        self._fields = fields

    deffit_fields(
        self,
        nodes: List[BaseNode],
        inplace: bool = True,
    ) -> Dict[str, str]:
"""Fit on all fields."""
        if len(self._fields) == 0:
            raise ValueError("Must provide at least one field to extract.")

        field_fns = {}
        for field in self._fields:
            field_context = self._fields_context.get(field, None)
            field_fns[field] = self.fit(
                nodes, field, field_context=field_context, inplace=inplace
            )
        return field_fns

    @abstractmethod
    deffit(
        self,
        nodes: List[BaseNode],
        field: str,
        field_context: Optional[Any] = None,
        expected_output: Optional[Any] = None,
        inplace: bool = True,
    ) -> str:
"""Given the input Nodes and fields, synthesize the python code."""

```
 |  
| --- | --- |  
###  extractor `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/program/evaporate/#llama_index.program.evaporate.BaseEvaporateProgram.extractor "Permanent link")

```
extractor: EvaporateExtractor

```

Extractor.
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/program/evaporate/#llama_index.program.evaporate.BaseEvaporateProgram.from_defaults "Permanent link")

```
from_defaults(
    fields_to_extract: Optional[[]] = None,
    fields_context: Optional[[, ]] = None,
    llm: Optional[] = None,
    schema_id_prompt: Optional[SchemaIDPrompt] = None,
    fn_generate_prompt: Optional[FnGeneratePrompt] = None,
    field_extract_query_tmpl:  = DEFAULT_FIELD_EXTRACT_QUERY_TMPL,
    nodes_to_fit: Optional[[]] = None,
    verbose:  = False,
) -> 

```

Evaporate program.
Source code in `llama-index-integrations/program/llama-index-program-evaporate/llama_index/program/evaporate/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    fields_to_extract: Optional[List[str]] = None,
    fields_context: Optional[Dict[str, Any]] = None,
    llm: Optional[LLM] = None,
    schema_id_prompt: Optional[SchemaIDPrompt] = None,
    fn_generate_prompt: Optional[FnGeneratePrompt] = None,
    field_extract_query_tmpl: str = DEFAULT_FIELD_EXTRACT_QUERY_TMPL,
    nodes_to_fit: Optional[List[BaseNode]] = None,
    verbose: bool = False,
) -> "BaseEvaporateProgram":
"""Evaporate program."""
    extractor = EvaporateExtractor(
        llm=llm,
        schema_id_prompt=schema_id_prompt,
        fn_generate_prompt=fn_generate_prompt,
        field_extract_query_tmpl=field_extract_query_tmpl,
    )
    return cls(
        extractor,
        fields_to_extract=fields_to_extract,
        fields_context=fields_context,
        nodes_to_fit=nodes_to_fit,
        verbose=verbose,
    )

```
 |  
| --- | --- |  
###  get_function_str [#](https://developers.llamaindex.ai/python/framework-api-reference/program/evaporate/#llama_index.program.evaporate.BaseEvaporateProgram.get_function_str "Permanent link")

```
get_function_str(field: ) -> 

```

Get function string.
Source code in `llama-index-integrations/program/llama-index-program-evaporate/llama_index/program/evaporate/base.py`  
| 
```
89
90
91
```
 | 
```
defget_function_str(self, field: str) -> str:
"""Get function string."""
    return self._field_fns[field]

```
 |  
| --- | --- |  
###  set_fields_to_extract [#](https://developers.llamaindex.ai/python/framework-api-reference/program/evaporate/#llama_index.program.evaporate.BaseEvaporateProgram.set_fields_to_extract "Permanent link")

```
set_fields_to_extract(fields: []) -> None

```

Set fields to extract.
Source code in `llama-index-integrations/program/llama-index-program-evaporate/llama_index/program/evaporate/base.py`  
| 
```
93
94
95
```
 | 
```
defset_fields_to_extract(self, fields: List[str]) -> None:
"""Set fields to extract."""
    self._fields = fields

```
 |  
| --- | --- |  
###  fit_fields [#](https://developers.llamaindex.ai/python/framework-api-reference/program/evaporate/#llama_index.program.evaporate.BaseEvaporateProgram.fit_fields "Permanent link")

```
fit_fields(
    nodes: [], inplace:  = True
) -> [, ]

```

Fit on all fields.
Source code in `llama-index-integrations/program/llama-index-program-evaporate/llama_index/program/evaporate/base.py`  
| 
```
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
```
 | 
```
deffit_fields(
    self,
    nodes: List[BaseNode],
    inplace: bool = True,
) -> Dict[str, str]:
"""Fit on all fields."""
    if len(self._fields) == 0:
        raise ValueError("Must provide at least one field to extract.")

    field_fns = {}
    for field in self._fields:
        field_context = self._fields_context.get(field, None)
        field_fns[field] = self.fit(
            nodes, field, field_context=field_context, inplace=inplace
        )
    return field_fns

```
 |  
| --- | --- |  
###  fit `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/program/evaporate/#llama_index.program.evaporate.BaseEvaporateProgram.fit "Permanent link")

```
fit(
    nodes: [],
    field: ,
    field_context: Optional[] = None,
    expected_output: Optional[] = None,
    inplace:  = True,
) -> 

```

Given the input Nodes and fields, synthesize the python code.
Source code in `llama-index-integrations/program/llama-index-program-evaporate/llama_index/program/evaporate/base.py`  
| 
```
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
```
 | 
```
@abstractmethod
deffit(
    self,
    nodes: List[BaseNode],
    field: str,
    field_context: Optional[Any] = None,
    expected_output: Optional[Any] = None,
    inplace: bool = True,
) -> str:
"""Given the input Nodes and fields, synthesize the python code."""

```
 |  
| --- | --- |  
##  DFEvaporateProgram [#](https://developers.llamaindex.ai/python/framework-api-reference/program/evaporate/#llama_index.program.evaporate.DFEvaporateProgram "Permanent link")
Bases: `BaseEvaporateProgram[](https://developers.llamaindex.ai/python/framework-api-reference/program/evaporate/#llama_index.program.evaporate.BaseEvaporateProgram "BaseEvaporateProgram \(llama_index.program.evaporate.base.BaseEvaporateProgram\)")[DataFrameRowsOnly]`
Evaporate DF program.
Given a set of fields, extracts a dataframe from a set of nodes. Each node corresponds to a row in the dataframe - each value in the row corresponds to a field value.
Source code in `llama-index-integrations/program/llama-index-program-evaporate/llama_index/program/evaporate/base.py`  
| 
```
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
```
 | 
```
classDFEvaporateProgram(BaseEvaporateProgram[DataFrameRowsOnly]):
"""
    Evaporate DF program.

    Given a set of fields, extracts a dataframe from a set of nodes.
    Each node corresponds to a row in the dataframe - each value in the row
    corresponds to a field value.

    """

    deffit(
        self,
        nodes: List[BaseNode],
        field: str,
        field_context: Optional[Any] = None,
        expected_output: Optional[Any] = None,
        inplace: bool = True,
    ) -> str:
"""Given the input Nodes and fields, synthesize the python code."""
        fn = self._extractor.extract_fn_from_nodes(nodes, field)
        logger.debug(f"Extracted function: {fn}")
        if inplace:
            self._field_fns[field] = fn
        return fn

    def_inference(
        self, nodes: List[BaseNode], fn_str: str, field_name: str
    ) -> List[Any]:
"""Given the input, call the python code and return the result."""
        results = self._extractor.run_fn_on_nodes(nodes, fn_str, field_name)
        logger.debug(f"Results: {results}")
        return results

    @property
    defoutput_cls(self) -> Type[DataFrameRowsOnly]:
"""Output class."""
        return DataFrameRowsOnly

    def__call__(self, *args: Any, **kwds: Any) -> DataFrameRowsOnly:
"""Call evaporate on inference data."""
        # TODO: either specify `nodes` or `texts` in kwds
        if "nodes" in kwds:
            nodes = kwds["nodes"]
        elif "texts" in kwds:
            nodes = [TextNode(text=t) for t in kwds["texts"]]
        else:
            raise ValueError("Must provide either `nodes` or `texts`.")

        col_dict = {}
        for field in self._fields:
            col_dict[field] = self._inference(nodes, self._field_fns[field], field)

        df = pd.DataFrame(col_dict, columns=self._fields)

        # convert pd.DataFrame to DataFrameRowsOnly
        df_row_objs = []
        for row_arr in df.values:
            df_row_objs.append(DataFrameRow(row_values=list(row_arr)))
        return DataFrameRowsOnly(rows=df_row_objs)

```
 |  
| --- | --- |  
###  output_cls `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/program/evaporate/#llama_index.program.evaporate.DFEvaporateProgram.output_cls "Permanent link")

```
output_cls: [DataFrameRowsOnly]

```

Output class.
###  fit [#](https://developers.llamaindex.ai/python/framework-api-reference/program/evaporate/#llama_index.program.evaporate.DFEvaporateProgram.fit "Permanent link")

```
fit(
    nodes: [],
    field: ,
    field_context: Optional[] = None,
    expected_output: Optional[] = None,
    inplace:  = True,
) -> 

```

Given the input Nodes and fields, synthesize the python code.
Source code in `llama-index-integrations/program/llama-index-program-evaporate/llama_index/program/evaporate/base.py`  
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
```
 | 
```
deffit(
    self,
    nodes: List[BaseNode],
    field: str,
    field_context: Optional[Any] = None,
    expected_output: Optional[Any] = None,
    inplace: bool = True,
) -> str:
"""Given the input Nodes and fields, synthesize the python code."""
    fn = self._extractor.extract_fn_from_nodes(nodes, field)
    logger.debug(f"Extracted function: {fn}")
    if inplace:
        self._field_fns[field] = fn
    return fn

```
 |  
| --- | --- |  
options: members: - DFEvaporateProgram
