# Koda retriever
##  KodaRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.KodaRetriever "Permanent link")
Bases: 
Custom Hybrid Retriever that dynamically determines the optimal alpha for a given query. An LLM is used to categorize the query and therefore determine the optimal alpha value, as each category has a preset/provided alpha value. It is recommended that you run tests on your corpus of data and queries to determine categories and corresponding alpha values for your use case.
KodaRetriever is built from BaseRetriever, and therefore is a llama-index compatible drop-in replacement for any hybrid retriever.
Auto-routing is NOT enabled without providing an LLM. If no LLM is provided, the default alpha value will be used for all queries and no alpha tuning will be done. Reranking will be done automatically if a reranker is provided. If no matrix is provided, a default matrix is leveraged. (Not recommended for production use)
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index`  |   |  The index to be used for retrieval  |  _required_  |  
|  `llm`  |  The LLM to be used for auto-routing. Defaults to None.  |  `None`  |  
|  `reranker`  |   |  The reranker to be used for postprocessing. Defaults to None.  |  `None`  |  
|  `default_alpha`  |  `float`  |  The default alpha value to be used if no LLM is provided. Defaults to .5.  |  `0.5`  |  
|  `matrix`  |  `dict or AlphaMatrix[](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.AlphaMatrix "AlphaMatrix \(llama_index.packs.koda_retriever.matrix.AlphaMatrix\)")`  |  The matrix to be used for auto-routing. Defaults to AlphaMatrix(data=DEFAULT_CATEGORIES).  |  `DEFAULT_CATEGORIES`  |  
|  `verbose`  |  `bool`  |  Whether to log verbose output. Defaults to False.  |  `False`  |  
|  `**kwargs`  |  Additional arguments for VectorIndexRetriever  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  KodaRetriever  |  
Examples:

```
>>> # Example 1 - provide your own LLM
>>> retriever = KodaRetriever( # woof woof
                    index=vector_index
                    , llm=Settings.llm
                    , verbose=True

>>> results = retriever.retrieve("What is the capital of France?")

```


```
>>> # Example 2 - set custom alpha values
>>> matrix_data = { # this is just dummy data, alpha values were randomly chosen
        "positive sentiment": {
            "alpha": .2
            , "description": "Queries expecting a positive answer"
            , "examples": [
                "I love this product"
                , "This is the best product ever"


        , "negative sentiment": {
            "alpha": .7
            , "description": "Queries expecting a negative answer"
            , "examples": [
                "I hate this product"
                , "This is the worst product ever"




```


```
>>> retriever = KodaRetriever( # woof woof
                    index=vector_index
                    , llm=Settings.llm
                    , matrix=matrix_data
                    , verbose=True

>>> results = retriever.retrieve("What happened on Y2K?")

```

Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/base.py`  
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
```
 | 
```
classKodaRetriever(BaseRetriever):
"""
    Custom Hybrid Retriever that dynamically determines the optimal alpha for a given query.
    An LLM is used to categorize the query and therefore determine the optimal alpha value, as each category has a preset/provided alpha value.
    It is recommended that you run tests on your corpus of data and queries to determine categories and corresponding alpha values for your use case.

    KodaRetriever is built from BaseRetriever, and therefore is a llama-index compatible drop-in replacement for any hybrid retriever.

    Auto-routing is NOT enabled without providing an LLM.
    If no LLM is provided, the default alpha value will be used for all queries and no alpha tuning will be done.
    Reranking will be done automatically if a reranker is provided.
    If no matrix is provided, a default matrix is leveraged. (Not recommended for production use)

    Args:
        index (VectorStoreIndex): The index to be used for retrieval
        llm (LLM, optional): The LLM to be used for auto-routing. Defaults to None.
        reranker (BaseNodePostprocessor, optional): The reranker to be used for postprocessing. Defaults to None.
        default_alpha (float, optional): The default alpha value to be used if no LLM is provided. Defaults to .5.
        matrix (dict or AlphaMatrix, optional): The matrix to be used for auto-routing. Defaults to AlphaMatrix(data=DEFAULT_CATEGORIES).
        verbose (bool, optional): Whether to log verbose output. Defaults to False.
        **kwargs: Additional arguments for VectorIndexRetriever

    Returns:
        KodaRetriever

    Examples:
        >>> # Example 1 - provide your own LLM
        >>> retriever = KodaRetriever( # woof woof
                            index=vector_index
                            , llm=Settings.llm
                            , verbose=True

        >>> results = retriever.retrieve("What is the capital of France?")

        >>> # Example 2 - set custom alpha values
        >>> matrix_data = { # this is just dummy data, alpha values were randomly chosen
                "positive sentiment": {
                    "alpha": .2
                    , "description": "Queries expecting a positive answer"
                    , "examples": [
                        "I love this product"
                        , "This is the best product ever"


                , "negative sentiment": {
                    "alpha": .7
                    , "description": "Queries expecting a negative answer"
                    , "examples": [
                        "I hate this product"
                        , "This is the worst product ever"




        >>> retriever = KodaRetriever( # woof woof
                            index=vector_index
                            , llm=Settings.llm
                            , matrix=matrix_data
                            , verbose=True

        >>> results = retriever.retrieve("What happened on Y2K?")

    """

    def__init__(
        self,
        index: VectorStoreIndex,
        llm: Optional[LLM] = None,  # if I could, I'd default to
        reranker: Optional[BaseNodePostprocessor] = None,
        default_alpha: float = 0.5,
        matrix: dict or AlphaMatrix = DEFAULT_CATEGORIES,  # type: ignore
        verbose: bool = False,
        **kwargs,  # kwargs for VectorIndexRetriever
    ):
        super().__init__()

        self.index = index
        self.retriever = VectorIndexRetriever(
            index=index,
            vector_store_query_mode=VectorStoreQueryMode.HYBRID,
            alpha=default_alpha,
            **kwargs,  # filters, etc, added here
        )
        self.default_alpha = default_alpha
        self.reranker = reranker
        self.llm = llm
        self.verbose = verbose

        if isinstance(matrix, dict):
            matrix = AlphaMatrix(data=matrix)

        self.matrix = matrix

    defcategorize(self, query: str) -> str:
"""Categorizes a query using the provided LLM and matrix. If no LLM is provided, the default alpha value will be used."""
        if not self.llm:
            err = "LLM is required for auto-routing. During instantiation, please provide an LLM or use direct routing."
            raise TypeError(err)

        prompt = CATEGORIZER_PROMPT.format(
            question=query, category_info=self.matrix.get_all_category_info()
        )

        response = str(self.llm.complete(prompt))  # type: ignore

        if response not in self.matrix.get_categories():
            raise ValueError(
                f"LLM classified question in a category that is not registered. {response} not in {self.matrix.get_categories()}"
            )

        return response

    async defa_categorize(self, query: str) -> str:
"""(async) Categorizes a query using the provided LLM and matrix. If no LLM is provided, the default alpha value will be used."""
        if not self.llm:
            err = "LLM is required for auto-routing. During instantiation, please provide an LLM or use direct routing."
            raise TypeError(err)

        prompt = CATEGORIZER_PROMPT.format(
            question=query, category_info=self.matrix.get_all_category_info()
        )

        response = await self.llm.acomplete(prompt)  # type: ignore
        response = str(response)

        if response not in self.matrix.get_categories():
            raise ValueError(
                f"LLM classified question in a category that is not registered. {response!s} not in {self.matrix.get_categories()}"
            )

        return response

    defcategory_retrieve(self, category: str, query: QueryType) -> List[NodeWithScore]:
"""Updates the alpha and retrieves results for a query using the provided category and query. If no LLM is provided, the default alpha value will be used."""
        alpha = self.matrix.get_alpha(category)
        self.retriever._alpha = (
            alpha  # updates alpha according to classification of query
        )

        return self.retriever.retrieve(str_or_query_bundle=query)

    async defa_category_retrieve(
        self, category: str, query: QueryType
    ) -> List[NodeWithScore]:
"""(async) Updates the alpha and retrieves results for a query using the provided category and query. If no LLM is provided, the default alpha value will be used."""
        alpha = self.matrix.get_alpha(category)
        self.retriever._alpha = (
            alpha  # updates alpha according to classification of query
        )

        return await self.retriever.aretrieve(str_or_query_bundle=query)

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""llama-index compatible retrieve method that auto-determines the optimal alpha for a query and then retrieves results for a query."""
        if not self.llm:
            warning = f"LLM is not provided, skipping route categorization. Default alpha of {self.default_alpha} will be used."
            logging.warning(warning)

            results = self.retriever.retrieve(query_bundle)
        else:
            category = self.categorize(query=query_bundle.query_str)  # type: ignore
            results = self.category_retrieve(category, query_bundle)
            if self.verbose:
                logging.info(
                    f"Query categorized as {category} with alpha of {self.matrix.get_alpha(category)}"
                )

        if self.reranker:
            if self.verbose:
                logging.info("Reranking results")
            results = self.reranker.postprocess_nodes(
                nodes=results, query_bundle=query_bundle
            )

        return results

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""(async) llama-index compatible retrieve method that auto-determines the optimal alpha for a query and then retrieves results for a query."""
        if not self.llm:
            warning = f"LLM is not provided, skipping route categorization. Default alpha of {self.default_alpha} will be used."
            logging.warning(warning)

            results = await self.retriever.aretrieve(query_bundle)
        else:
            category = await self.a_categorize(query_bundle.query_str)  # type: ignore
            results = await self.a_category_retrieve(category, query_bundle)
            if self.verbose:
                logging.info(
                    f"Query categorized as {category} with alpha of {self.matrix.get_alpha(category)}"
                )

        if self.reranker:
            if self.verbose:
                logging.info("Reranking results")
            results = self.reranker.postprocess_nodes(
                nodes=results, query_bundle=query_bundle
            )

        return results

```
 |  
| --- | --- |  
###  categorize [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.KodaRetriever.categorize "Permanent link")

```
categorize(query: ) -> 

```

Categorizes a query using the provided LLM and matrix. If no LLM is provided, the default alpha value will be used.
Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/base.py`  
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
```
 | 
```
defcategorize(self, query: str) -> str:
"""Categorizes a query using the provided LLM and matrix. If no LLM is provided, the default alpha value will be used."""
    if not self.llm:
        err = "LLM is required for auto-routing. During instantiation, please provide an LLM or use direct routing."
        raise TypeError(err)

    prompt = CATEGORIZER_PROMPT.format(
        question=query, category_info=self.matrix.get_all_category_info()
    )

    response = str(self.llm.complete(prompt))  # type: ignore

    if response not in self.matrix.get_categories():
        raise ValueError(
            f"LLM classified question in a category that is not registered. {response} not in {self.matrix.get_categories()}"
        )

    return response

```
 |  
| --- | --- |  
###  a_categorize [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.KodaRetriever.a_categorize "Permanent link")

```
a_categorize(query: ) -> 

```

(async) Categorizes a query using the provided LLM and matrix. If no LLM is provided, the default alpha value will be used.
Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/base.py`  
| 
```
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
```
 | 
```
async defa_categorize(self, query: str) -> str:
"""(async) Categorizes a query using the provided LLM and matrix. If no LLM is provided, the default alpha value will be used."""
    if not self.llm:
        err = "LLM is required for auto-routing. During instantiation, please provide an LLM or use direct routing."
        raise TypeError(err)

    prompt = CATEGORIZER_PROMPT.format(
        question=query, category_info=self.matrix.get_all_category_info()
    )

    response = await self.llm.acomplete(prompt)  # type: ignore
    response = str(response)

    if response not in self.matrix.get_categories():
        raise ValueError(
            f"LLM classified question in a category that is not registered. {response!s} not in {self.matrix.get_categories()}"
        )

    return response

```
 |  
| --- | --- |  
###  category_retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.KodaRetriever.category_retrieve "Permanent link")

```
category_retrieve(
    category: , query: QueryType
) -> []

```

Updates the alpha and retrieves results for a query using the provided category and query. If no LLM is provided, the default alpha value will be used.
Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/base.py`  
| 
```
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
defcategory_retrieve(self, category: str, query: QueryType) -> List[NodeWithScore]:
"""Updates the alpha and retrieves results for a query using the provided category and query. If no LLM is provided, the default alpha value will be used."""
    alpha = self.matrix.get_alpha(category)
    self.retriever._alpha = (
        alpha  # updates alpha according to classification of query
    )

    return self.retriever.retrieve(str_or_query_bundle=query)

```
 |  
| --- | --- |  
###  a_category_retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.KodaRetriever.a_category_retrieve "Permanent link")

```
a_category_retrieve(
    category: , query: QueryType
) -> []

```

(async) Updates the alpha and retrieves results for a query using the provided category and query. If no LLM is provided, the default alpha value will be used.
Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/base.py`  
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
```
 | 
```
async defa_category_retrieve(
    self, category: str, query: QueryType
) -> List[NodeWithScore]:
"""(async) Updates the alpha and retrieves results for a query using the provided category and query. If no LLM is provided, the default alpha value will be used."""
    alpha = self.matrix.get_alpha(category)
    self.retriever._alpha = (
        alpha  # updates alpha according to classification of query
    )

    return await self.retriever.aretrieve(str_or_query_bundle=query)

```
 |  
| --- | --- |  
##  AlphaMatrix [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.AlphaMatrix "Permanent link")
Bases: `BaseModel`
This class is not necessary to understand to use a KodaRetriever - as it will be automatically instantiated if a dictionary is provided.
Pydantic class to enforce the required fields for a KodaRetriever Its best to just instantiate this using a dictionary, don't both trying to instantiate by declaring any AlphaCategory objects.
Example
> > > data = { "normal query": { # examples is not required if you aren't using few-shot auto-routing "alpha": .5 , "description": "This is a normal query" # desc is not required if you aren't using few-shot auto-routing , "examples": ["This is a normal query", "Another normal query"] } } matrix = AlphaMatrix(data=data) # arg must be named matrix for the retriever to use it
Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/matrix.py`  
| 
```
 5
 6
 7
 8
 9
10
11
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
```
 | 
```
classAlphaMatrix(BaseModel):
"""
    This class is not necessary to understand to use a KodaRetriever - as it will be automatically instantiated if a dictionary is provided.

    Pydantic class to enforce the required fields for a KodaRetriever
    Its best to just instantiate this using a dictionary, don't both trying to instantiate by declaring any AlphaCategory objects.

    Example:
        >>> data = {
                "normal query": { # examples is not required if you aren't using few-shot auto-routing
                    "alpha": .5
                    , "description": "This is a normal query" # desc is not required if you aren't using few-shot auto-routing
                    , "examples": ["This is a normal query", "Another normal query"]


        >>> matrix = AlphaMatrix(data=data) # arg must be named matrix for the retriever to use it

    """

    classAlphaCategory(BaseModel):
"""
        Subclass to enforce the required fields for a category in the AlphaMatrix - necessary for nesting in the AlphaMatrix class
        You should not have to really touch this, as it is only used for type checking and validation.
        """

        alpha: float
        description: Optional[str] = (
            None  # optional if providing a custom LLM, its presumed this was part of your training data for the custom model
        )
        examples: Optional[List[str]] = (
            None  # if not providing a custom model, this is required
        )

    data: Dict[str, AlphaCategory]

    defget_alpha(self, category: str) -> float:
"""Simple helper function to get the alpha value for a given category."""
        if category not in self.data:
            err = f"Provided category '{category}' cannot be found"
            raise ValueError(err)

        return self.data.get(category).alpha  # type: ignore

    defget_examples(self, category: str) -> List[str]:
"""Simple helper function to get the examples for a given category."""
        if category not in self.data:
            err = f"Provided category '{category}' cannot be found"
            raise ValueError(err)

        return self.data.get(category).examples  # type: ignore

    defget_description(self, category: str) -> str:
"""Simple helper function to get the description for a given category."""
        if category not in self.data:
            err = f"Provided category '{category}' cannot be found"
            raise ValueError(err)

        return self.data.get(category).description  # type: ignore

    defget_categories(self) -> list:
"""Simple helper function to get the categories for a given category."""
        return list(self.data.keys())

    defformat_category(self, category: str) -> str:
"""Simple helper function to format the category information for a given category."""
        if category not in self.data:
            err = f"Provided category '{category}' cannot be found"
            raise ValueError(err)

        description = self.get_description(category)
        examples = self.get_examples(category)

        category_info = f"""
{category}:
            description: {description}
        """.strip()

        if examples:
            examples = "; ".join(examples)
            example_info = f"""
            examples:
{examples}

            category_info = f"{category_info}\n{example_info}"

        return category_info

    defget_all_category_info(self) -> str:
"""Simple helper function to get the category information for all categories."""
        categories = []
        for category in self.get_categories():
            category_info = self.format_category(category)
            categories.append(category_info)
        return "\n".join(categories)

```
 |  
| --- | --- |  
###  AlphaCategory [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.AlphaMatrix.AlphaCategory "Permanent link")
Bases: `BaseModel`
Subclass to enforce the required fields for a category in the AlphaMatrix - necessary for nesting in the AlphaMatrix class You should not have to really touch this, as it is only used for type checking and validation.
Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/matrix.py`  
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
```
 | 
```
classAlphaCategory(BaseModel):
"""
    Subclass to enforce the required fields for a category in the AlphaMatrix - necessary for nesting in the AlphaMatrix class
    You should not have to really touch this, as it is only used for type checking and validation.
    """

    alpha: float
    description: Optional[str] = (
        None  # optional if providing a custom LLM, its presumed this was part of your training data for the custom model
    )
    examples: Optional[List[str]] = (
        None  # if not providing a custom model, this is required
    )

```
 |  
| --- | --- |  
###  get_alpha [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.AlphaMatrix.get_alpha "Permanent link")

```
get_alpha(category: ) -> float

```

Simple helper function to get the alpha value for a given category.
Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/matrix.py`  
| 
```
40
41
42
43
44
45
46
```
 | 
```
defget_alpha(self, category: str) -> float:
"""Simple helper function to get the alpha value for a given category."""
    if category not in self.data:
        err = f"Provided category '{category}' cannot be found"
        raise ValueError(err)

    return self.data.get(category).alpha  # type: ignore

```
 |  
| --- | --- |  
###  get_examples [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.AlphaMatrix.get_examples "Permanent link")

```
get_examples(category: ) -> []

```

Simple helper function to get the examples for a given category.
Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/matrix.py`  
| 
```
48
49
50
51
52
53
54
```
 | 
```
defget_examples(self, category: str) -> List[str]:
"""Simple helper function to get the examples for a given category."""
    if category not in self.data:
        err = f"Provided category '{category}' cannot be found"
        raise ValueError(err)

    return self.data.get(category).examples  # type: ignore

```
 |  
| --- | --- |  
###  get_description [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.AlphaMatrix.get_description "Permanent link")

```
get_description(category: ) -> 

```

Simple helper function to get the description for a given category.
Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/matrix.py`  
| 
```
56
57
58
59
60
61
62
```
 | 
```
defget_description(self, category: str) -> str:
"""Simple helper function to get the description for a given category."""
    if category not in self.data:
        err = f"Provided category '{category}' cannot be found"
        raise ValueError(err)

    return self.data.get(category).description  # type: ignore

```
 |  
| --- | --- |  
###  get_categories [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.AlphaMatrix.get_categories "Permanent link")

```
get_categories() -> 

```

Simple helper function to get the categories for a given category.
Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/matrix.py`  
| 
```
64
65
66
```
 | 
```
defget_categories(self) -> list:
"""Simple helper function to get the categories for a given category."""
    return list(self.data.keys())

```
 |  
| --- | --- |  
###  format_category [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.AlphaMatrix.format_category "Permanent link")

```
format_category(category: ) -> 

```

Simple helper function to format the category information for a given category.
Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/matrix.py`  
| 
```
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
```
 | 
```
defformat_category(self, category: str) -> str:
"""Simple helper function to format the category information for a given category."""
    if category not in self.data:
        err = f"Provided category '{category}' cannot be found"
        raise ValueError(err)

    description = self.get_description(category)
    examples = self.get_examples(category)

    category_info = f"""
{category}:
        description: {description}
    """.strip()

    if examples:
        examples = "; ".join(examples)
        example_info = f"""
        examples:
{examples}
        """
        category_info = f"{category_info}\n{example_info}"

    return category_info

```
 |  
| --- | --- |  
###  get_all_category_info [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/koda_retriever/#llama_index.packs.koda_retriever.AlphaMatrix.get_all_category_info "Permanent link")

```
get_all_category_info() -> 

```

Simple helper function to get the category information for all categories.
Source code in `llama-index-packs/llama-index-packs-koda-retriever/llama_index/packs/koda_retriever/matrix.py`  
| 
```
92
93
94
95
96
97
98
```
 | 
```
defget_all_category_info(self) -> str:
"""Simple helper function to get the category information for all categories."""
    categories = []
    for category in self.get_categories():
        category_info = self.format_category(category)
        categories.append(category_info)
    return "\n".join(categories)

```
 |  
| --- | --- |  
options: members: - KodaRetrieverPack
