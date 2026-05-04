# Neo4j
##  Neo4jQueryToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/neo4j/#llama_index.tools.neo4j.Neo4jQueryToolSpec "Permanent link")
Bases: 
This class is responsible for querying a Neo4j graph database based on a provided schema definition.
Source code in `llama-index-integrations/tools/llama-index-tools-neo4j/llama_index/tools/neo4j/base.py`  
| 
```
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
```
 | 
```
classNeo4jQueryToolSpec(BaseToolSpec):
"""
    This class is responsible for querying a Neo4j graph database based on a provided schema definition.
    """

    spec_functions = ["run_request"]

    def__init__(
        self, url, user, password, database, llm: LLM, validate_cypher: bool = False
    ):
"""
        Initializes the Neo4jSchemaWiseQuery object.

        Args:
            url (str): The connection string for the Neo4j database.
            user (str): Username for the Neo4j database.
            password (str): Password for the Neo4j database.
            llm (obj): A language model for generating Cypher queries.
            validate_cypher (bool): Validate relationship directions in
                the generated Cypher statement. Default: False

        """
        if find_spec("neo4j") is None:
            raise ImportError(
                "`neo4j` package not found, please run `pip install neo4j`"
            )

        self.graph_store = Neo4jGraphStore(
            url=url, username=user, password=password, database=database
        )
        self.llm = llm
        self.cypher_query_corrector = None
        if validate_cypher:
            corrector_schema = [
                Schema(el["start"], el["type"], el["end"])
                for el in self.graph_store.structured_schema.get("relationships")
            ]
            self.cypher_query_corrector = CypherQueryCorrector(corrector_schema)

    defget_system_message(self):
"""
        Generates a system message detailing the task and schema.

        Returns:
            str: The system message.

        """
        return f"""
        Task: Generate Cypher queries to query a Neo4j graph database based on the provided schema definition.
        Instructions:
        Use only the provided relationship types and properties.
        Do not use any other relationship types or properties that are not provided.
        If you cannot generate a Cypher statement based on the provided schema, explain the reason to the user.
        Schema:
{self.graph_store.schema}

        Note: Do not include any explanations or apologies in your responses.
        """

    defquery_graph_db(self, neo4j_query, params=None):
"""
        Queries the Neo4j database.

        Args:
            neo4j_query (str): The Cypher query to be executed.
            params (dict, optional): Parameters for the Cypher query. Defaults to None.

        Returns:
            list: The query results.

        """
        if params is None:
            params = {}
        with self.graph_store.client.session() as session:
            result = session.run(neo4j_query, params)
            output = [r.values() for r in result]
            output.insert(0, list(result.keys()))
            return output

    defconstruct_cypher_query(self, question, history=None):
"""
        Constructs a Cypher query based on a given question and history.

        Args:
            question (str): The question to construct the Cypher query for.
            history (list, optional): A list of previous interactions for context. Defaults to None.

        Returns:
            str: The constructed Cypher query.

        """
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=self.get_system_message()),
            ChatMessage(role=MessageRole.USER, content=question),
        ]
        # Used for Cypher healing flows
        if history:
            messages.extend(history)

        completions = self.llm.chat(messages)
        return completions.message.content

    defrun_request(self, question, history=None, retry=True):
"""
        Executes a Cypher query based on a given question.

        Args:
            question (str): The question to execute the Cypher query for.
            history (list, optional): A list of previous interactions for context. Defaults to None.
            retry (bool, optional): Whether to retry in case of a syntax error. Defaults to True.

        Returns:
            list/str: The query results or an error message.

        """
        fromneo4j.exceptionsimport CypherSyntaxError

        # Construct Cypher statement
        cypher = self.construct_cypher_query(question, history)
        # Validate Cypher statement
        if self.cypher_query_corrector:
            cypher = self.cypher_query_corrector(cypher)
        print(cypher)
        try:
            return self.query_graph_db(cypher)
        # Self-healing flow
        except CypherSyntaxError as e:
            # If out of retries
            if not retry:
                return "Invalid Cypher syntax"
            # Self-healing Cypher flow by
            # providing specific error to GPT-4
            print("Retrying")
            return self.run_request(
                question,
                [
                    ChatMessage(role=MessageRole.ASSISTANT, content=cypher),
                    ChatMessage(
                        role=MessageRole.SYSTEM,
                        content=f"This query returns an error: {e!s}\n"
                        "Give me a improved query that works without any explanations or apologies",
                    ),
                ],
                retry=False,
            )

```
 |  
| --- | --- |  
###  get_system_message [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/neo4j/#llama_index.tools.neo4j.Neo4jQueryToolSpec.get_system_message "Permanent link")

```
get_system_message()

```

Generates a system message detailing the task and schema.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The system message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-neo4j/llama_index/tools/neo4j/base.py`  
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
```
 | 
```
defget_system_message(self):
"""
    Generates a system message detailing the task and schema.

    Returns:
        str: The system message.

    """
    return f"""
    Task: Generate Cypher queries to query a Neo4j graph database based on the provided schema definition.
    Instructions:
    Use only the provided relationship types and properties.
    Do not use any other relationship types or properties that are not provided.
    If you cannot generate a Cypher statement based on the provided schema, explain the reason to the user.
    Schema:
{self.graph_store.schema}

    Note: Do not include any explanations or apologies in your responses.
    """

```
 |  
| --- | --- |  
###  query_graph_db [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/neo4j/#llama_index.tools.neo4j.Neo4jQueryToolSpec.query_graph_db "Permanent link")

```
query_graph_db(neo4j_query, params=None)

```

Queries the Neo4j database.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `neo4j_query`  |  The Cypher query to be executed.  |  _required_  |  
|  `params`  |  `dict`  |  Parameters for the Cypher query. Defaults to None.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `list`  |  The query results.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-neo4j/llama_index/tools/neo4j/base.py`  
| 
```
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
```
 | 
```
defquery_graph_db(self, neo4j_query, params=None):
"""
    Queries the Neo4j database.

    Args:
        neo4j_query (str): The Cypher query to be executed.
        params (dict, optional): Parameters for the Cypher query. Defaults to None.

    Returns:
        list: The query results.

    """
    if params is None:
        params = {}
    with self.graph_store.client.session() as session:
        result = session.run(neo4j_query, params)
        output = [r.values() for r in result]
        output.insert(0, list(result.keys()))
        return output

```
 |  
| --- | --- |  
###  construct_cypher_query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/neo4j/#llama_index.tools.neo4j.Neo4jQueryToolSpec.construct_cypher_query "Permanent link")

```
construct_cypher_query(question, history=None)

```

Constructs a Cypher query based on a given question and history.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `question`  |  The question to construct the Cypher query for.  |  _required_  |  
|  `history`  |  `list`  |  A list of previous interactions for context. Defaults to None.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The constructed Cypher query.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-neo4j/llama_index/tools/neo4j/base.py`  
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
```
 | 
```
defconstruct_cypher_query(self, question, history=None):
"""
    Constructs a Cypher query based on a given question and history.

    Args:
        question (str): The question to construct the Cypher query for.
        history (list, optional): A list of previous interactions for context. Defaults to None.

    Returns:
        str: The constructed Cypher query.

    """
    messages = [
        ChatMessage(role=MessageRole.SYSTEM, content=self.get_system_message()),
        ChatMessage(role=MessageRole.USER, content=question),
    ]
    # Used for Cypher healing flows
    if history:
        messages.extend(history)

    completions = self.llm.chat(messages)
    return completions.message.content

```
 |  
| --- | --- |  
###  run_request [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/neo4j/#llama_index.tools.neo4j.Neo4jQueryToolSpec.run_request "Permanent link")

```
run_request(question, history=None, retry=True)

```

Executes a Cypher query based on a given question.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `question`  |  The question to execute the Cypher query for.  |  _required_  |  
|  `history`  |  `list`  |  A list of previous interactions for context. Defaults to None.  |  `None`  |  
|  `retry`  |  `bool`  |  Whether to retry in case of a syntax error. Defaults to True.  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  list/str: The query results or an error message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-neo4j/llama_index/tools/neo4j/base.py`  
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
```
 | 
```
defrun_request(self, question, history=None, retry=True):
"""
    Executes a Cypher query based on a given question.

    Args:
        question (str): The question to execute the Cypher query for.
        history (list, optional): A list of previous interactions for context. Defaults to None.
        retry (bool, optional): Whether to retry in case of a syntax error. Defaults to True.

    Returns:
        list/str: The query results or an error message.

    """
    fromneo4j.exceptionsimport CypherSyntaxError

    # Construct Cypher statement
    cypher = self.construct_cypher_query(question, history)
    # Validate Cypher statement
    if self.cypher_query_corrector:
        cypher = self.cypher_query_corrector(cypher)
    print(cypher)
    try:
        return self.query_graph_db(cypher)
    # Self-healing flow
    except CypherSyntaxError as e:
        # If out of retries
        if not retry:
            return "Invalid Cypher syntax"
        # Self-healing Cypher flow by
        # providing specific error to GPT-4
        print("Retrying")
        return self.run_request(
            question,
            [
                ChatMessage(role=MessageRole.ASSISTANT, content=cypher),
                ChatMessage(
                    role=MessageRole.SYSTEM,
                    content=f"This query returns an error: {e!s}\n"
                    "Give me a improved query that works without any explanations or apologies",
                ),
            ],
            retry=False,
        )

```
 |  
| --- | --- |  
options: members: - Neo4jQueryToolSpec
