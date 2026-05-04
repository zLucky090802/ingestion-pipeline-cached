# Igpt email
##  IGPTEmailToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/igpt_email/#llama_index.tools.igpt_email.IGPTEmailToolSpec "Permanent link")
Bases: 
iGPT Email Intelligence tool spec.
Wraps the iGPT recall.ask() and recall.search() endpoints, giving agents structured, reasoning-ready context from connected email threads.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  iGPT API key. See https://docs.igpt.ai for details.  |  _required_  |  
|  `user`  |  User identifier for the connected mailbox.  |  _required_  |  
Example
.. code-block:: python

```
from llama_index.tools.igpt_email import IGPTEmailToolSpec
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI

tool_spec = IGPTEmailToolSpec(api_key="your-key", user="user-id")

agent = FunctionAgent(
    tools=tool_spec.to_tool_list(),
    llm=OpenAI(model="gpt-4.1"),
)

answer = await agent.run("What tasks were assigned to me this week?")

```
Source code in `llama-index-integrations/tools/llama-index-tools-igpt-email/llama_index/tools/igpt_email/base.py`  
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
```
 | 
```
classIGPTEmailToolSpec(BaseToolSpec):
"""
    iGPT Email Intelligence tool spec.

    Wraps the iGPT recall.ask() and recall.search() endpoints, giving agents
    structured, reasoning-ready context from connected email threads.

    Args:
        api_key (str): iGPT API key. See https://docs.igpt.ai for details.
        user (str): User identifier for the connected mailbox.

    Example:
        .. code-block:: python

            from llama_index.tools.igpt_email import IGPTEmailToolSpec
            from llama_index.core.agent.workflow import FunctionAgent
            from llama_index.llms.openai import OpenAI

            tool_spec = IGPTEmailToolSpec(api_key="your-key", user="user-id")

            agent = FunctionAgent(
                tools=tool_spec.to_tool_list(),
                llm=OpenAI(model="gpt-4.1"),


            answer = await agent.run("What tasks were assigned to me this week?")

    """

    spec_functions = ["ask", "search"]

    def__init__(self, api_key: str, user: str) -> None:
"""Initialize with parameters."""
        self.client = IGPT(api_key=api_key, user=user)

    defask(
        self,
        question: str,
        output_format: str = "json",
    ) -> List[Document]:
"""
        Ask a question about email context using iGPT's reasoning engine.

        Calls recall.ask() and returns structured context extracted from
        connected email threads, including tasks, decisions, owners, sentiment,
        deadlines, and citations.

        Args:
            question (str): The question or prompt to reason over email context.
            output_format (str): Response format — "text" or "json". Default is "json".

        Returns:
            List[Document]: A single Document containing the structured reasoning
                response. Citations are stored in metadata["citations"].

        """
        response = self.client.recall.ask(
            input=question,
            output_format=output_format,
        )

        if isinstance(response, dict) and "error" in response:
            raise ValueError(f"iGPT API error: {response['error']}")

        if isinstance(response, dict):
            text = json.dumps(response)
            citations = response.get("citations", [])
        else:
            text = str(response)
            citations = []

        return [
            Document(
                text=text,
                metadata={
                    "question": question,
                    "citations": citations,
                    "source": "igpt_email_ask",
                },
            )
        ]

    defsearch(
        self,
        query: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        max_results: Optional[int] = 10,
    ) -> List[Document]:
"""
        Search email context for relevant messages and threads.

        Calls recall.search() and returns matching email context as Documents,
        with thread metadata (subject, participants, date, thread ID) preserved
        in metadata for downstream filtering and retrieval.

        Args:
            query (str): Search query to run against connected email data.
            date_from (str, optional): Filter results from this date (YYYY-MM-DD).
            date_to (str, optional): Filter results up to this date (YYYY-MM-DD).
            max_results (int, optional): Maximum number of results to return. Default is 10.

        Returns:
            List[Document]: One Document per email result. Thread metadata is
                stored in metadata (subject, from, to, date, thread_id, id).

        """
        response = self.client.recall.search(
            query=query,
            date_from=date_from,
            date_to=date_to,
            max_results=max_results,
        )

        if isinstance(response, dict) and "error" in response:
            raise ValueError(f"iGPT API error: {response['error']}")

        if not response:
            return []

        results = (
            response if isinstance(response, list) else response.get("results", [])
        )

        documents = []
        for item in results:
            if isinstance(item, dict):
                text = item.get("content", item.get("body", json.dumps(item)))
                metadata = {
                    "source": "igpt_email_search",
                    "subject": item.get("subject"),
                    "from": item.get("from"),
                    "to": item.get("to"),
                    "date": item.get("date"),
                    "thread_id": item.get("thread_id"),
                    "id": item.get("id"),
                }
            else:
                text = str(item)
                metadata = {"source": "igpt_email_search"}

            documents.append(Document(text=text, metadata=metadata))

        return documents

```
 |  
| --- | --- |  
###  ask [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/igpt_email/#llama_index.tools.igpt_email.IGPTEmailToolSpec.ask "Permanent link")

```
ask(
    question: , output_format:  = "json"
) -> []

```

Ask a question about email context using iGPT's reasoning engine.
Calls recall.ask() and returns structured context extracted from connected email threads, including tasks, decisions, owners, sentiment, deadlines, and citations.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `question`  |  The question or prompt to reason over email context.  |  _required_  |  
|  `output_format`  |  Response format — "text" or "json". Default is "json".  |  `'json'`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A single Document containing the structured reasoning response. Citations are stored in metadata["citations"].  |  
Source code in `llama-index-integrations/tools/llama-index-tools-igpt-email/llama_index/tools/igpt_email/base.py`  
| 
```
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
```
 | 
```
defask(
    self,
    question: str,
    output_format: str = "json",
) -> List[Document]:
"""
    Ask a question about email context using iGPT's reasoning engine.

    Calls recall.ask() and returns structured context extracted from
    connected email threads, including tasks, decisions, owners, sentiment,
    deadlines, and citations.

    Args:
        question (str): The question or prompt to reason over email context.
        output_format (str): Response format — "text" or "json". Default is "json".

    Returns:
        List[Document]: A single Document containing the structured reasoning
            response. Citations are stored in metadata["citations"].

    """
    response = self.client.recall.ask(
        input=question,
        output_format=output_format,
    )

    if isinstance(response, dict) and "error" in response:
        raise ValueError(f"iGPT API error: {response['error']}")

    if isinstance(response, dict):
        text = json.dumps(response)
        citations = response.get("citations", [])
    else:
        text = str(response)
        citations = []

    return [
        Document(
            text=text,
            metadata={
                "question": question,
                "citations": citations,
                "source": "igpt_email_ask",
            },
        )
    ]

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/igpt_email/#llama_index.tools.igpt_email.IGPTEmailToolSpec.search "Permanent link")

```
search(
    query: ,
    date_from: Optional[] = None,
    date_to: Optional[] = None,
    max_results: Optional[] = 10,
) -> []

```

Search email context for relevant messages and threads.
Calls recall.search() and returns matching email context as Documents, with thread metadata (subject, participants, date, thread ID) preserved in metadata for downstream filtering and retrieval.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Search query to run against connected email data.  |  _required_  |  
|  `date_from`  |  Filter results from this date (YYYY-MM-DD).  |  `None`  |  
|  `date_to`  |  Filter results up to this date (YYYY-MM-DD).  |  `None`  |  
|  `max_results`  |  Maximum number of results to return. Default is 10.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: One Document per email result. Thread metadata is stored in metadata (subject, from, to, date, thread_id, id).  |  
Source code in `llama-index-integrations/tools/llama-index-tools-igpt-email/llama_index/tools/igpt_email/base.py`  
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
```
 | 
```
defsearch(
    self,
    query: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    max_results: Optional[int] = 10,
) -> List[Document]:
"""
    Search email context for relevant messages and threads.

    Calls recall.search() and returns matching email context as Documents,
    with thread metadata (subject, participants, date, thread ID) preserved
    in metadata for downstream filtering and retrieval.

    Args:
        query (str): Search query to run against connected email data.
        date_from (str, optional): Filter results from this date (YYYY-MM-DD).
        date_to (str, optional): Filter results up to this date (YYYY-MM-DD).
        max_results (int, optional): Maximum number of results to return. Default is 10.

    Returns:
        List[Document]: One Document per email result. Thread metadata is
            stored in metadata (subject, from, to, date, thread_id, id).

    """
    response = self.client.recall.search(
        query=query,
        date_from=date_from,
        date_to=date_to,
        max_results=max_results,
    )

    if isinstance(response, dict) and "error" in response:
        raise ValueError(f"iGPT API error: {response['error']}")

    if not response:
        return []

    results = (
        response if isinstance(response, list) else response.get("results", [])
    )

    documents = []
    for item in results:
        if isinstance(item, dict):
            text = item.get("content", item.get("body", json.dumps(item)))
            metadata = {
                "source": "igpt_email_search",
                "subject": item.get("subject"),
                "from": item.get("from"),
                "to": item.get("to"),
                "date": item.get("date"),
                "thread_id": item.get("thread_id"),
                "id": item.get("id"),
            }
        else:
            text = str(item)
            metadata = {"source": "igpt_email_search"}

        documents.append(Document(text=text, metadata=metadata))

    return documents

```
 |  
| --- | --- |  
options: members: - IGPTEmailToolSpec
