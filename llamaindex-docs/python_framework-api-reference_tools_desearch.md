# Desearch
##  DesearchToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/desearch/#llama_index.tools.desearch.DesearchToolSpec "Permanent link")
Bases: 
Desearch tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-desearch/llama_index/tools/desearch/base.py`  
| 
```
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
```
 | 
```
classDesearchToolSpec(BaseToolSpec):
"""Desearch tool spec."""

    spec_functions = [
        "ai_search_tool",
        "twitter_search_tool",
        "web_search_tool",
    ]

    def__init__(self, api_key: str) -> None:
"""Initialize with parameters."""
        self.client = Desearch(api_key=api_key)

    defai_search_tool(
        self,
        prompt: str = Field(description="The search prompt or query."),
        tool: List[
            Literal[
                "web",
                "hackernews",
                "reddit",
                "wikipedia",
                "youtube",
                "twitter",
                "arxiv",
            ]
        ] = Field(description="List of tools to use. Must include at least one tool."),
        model: str = Field(
            default="NOVA",
            description="The model to use for the search. Value should 'NOVA', 'ORBIT' or 'HORIZON'",
        ),
        date_filter: Optional[str] = Field(
            default=None, description="Date filter for the search."
        ),
    ) -> str | dict:
"""
        Perform a search using Desearch.

        Args:
            prompt (str): The search prompt or query.
            tool (List[Literal["web", "hackernews", "reddit", "wikipedia", "youtube", "twitter", "arxiv"]]): List of tools to use. Must include at least one tool.
            model (str, optional): The model to use for the search. Defaults to "NOVA".
            date_filter (Optional[str], optional): Date filter for the search. Defaults to None.

        Returns:
            str | dict: The search result or an error string.

        """
        try:
            return self.client.search(
                prompt,
                tool,
                model,
                date_filter,
            )
        except Exception as e:
            return str(e)

    deftwitter_search_tool(
        self,
        query: str = Field(description="The Twitter search query."),
        sort: str = Field(default="Top", description="Sort order for the results."),
        count: int = Field(default=10, description="Number of results to return."),
    ) -> BasicTwitterSearchResponse:
"""
        Perform a basic Twitter search using the Exa API.

        Args:
            query (str, optional): The Twitter search query. Defaults to None.
            sort (str, optional): Sort order for the results. Defaults to "Top".
            count (int, optional): Number of results to return. Defaults to 10.

        Returns:
            BasicTwitterSearchResponse: The search results.

        Raises:
            Exception: If an error occurs when calling the API.

        """
        try:
            return self.client.basic_twitter_search(query, sort, count)
        except Exception as e:
            return str(e)

    defweb_search_tool(
        self,
        query: str = Field(description="The search query."),
        num: int = Field(default=10, description="Number of results to return."),
        start: int = Field(
            default=1, description="The starting index for the search results."
        ),
    ) -> List[WebSearchResult]:
"""
        Perform a basic web search using the Exa API.

        Args:
            query (str, optional): The search query. Defaults to None.
            num (int, optional): Number of results to return. Defaults to 10.
            start (int, optional): The starting index for the search results. Defaults to 1.

        Returns:
            List[WebSearchResult]: The search results.

        Raises:
            Exception: If an error occurs when calling the API.

        """
        try:
            return self.client.basic_web_search(query, num, start)
        except Exception as e:
            return str(e)

```
 |  
| --- | --- |  
###  ai_search_tool [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/desearch/#llama_index.tools.desearch.DesearchToolSpec.ai_search_tool "Permanent link")

```
ai_search_tool(
    prompt:  = Field(
        description="The search prompt or query."
    ),
    tool: [
        Literal[
            "web",
            "hackernews",
            "reddit",
            "wikipedia",
            "youtube",
            "twitter",
            "arxiv",
        ]
    ] = Field(
        description="List of tools to use. Must include at least one tool."
    ),
    model:  = Field(
        default="NOVA",
        description="The model to use for the search. Value should 'NOVA', 'ORBIT' or 'HORIZON'",
    ),
    date_filter: Optional[] = Field(
        default=None,
        description="Date filter for the search.",
    ),
) ->  | 

```

Perform a search using Desearch.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The search prompt or query.  |  `Field(description='The search prompt or query.')`  |  
|  `tool`  |  `List[Literal['web', 'hackernews', 'reddit', 'wikipedia', 'youtube', 'twitter', 'arxiv']]`  |  List of tools to use. Must include at least one tool.  |  `Field(description='List of tools to use. Must include at least one tool.')`  |  
|  `model`  |  The model to use for the search. Defaults to "NOVA".  |  `Field(default='NOVA', description="The model to use for the search. Value should 'NOVA', 'ORBIT' or 'HORIZON'")`  |  
|  `date_filter`  |  `Optional[str]`  |  Date filter for the search. Defaults to None.  |  `Field(default=None, description='Date filter for the search.')`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `str | dict`  |  str | dict: The search result or an error string.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-desearch/llama_index/tools/desearch/base.py`  
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
```
 | 
```
defai_search_tool(
    self,
    prompt: str = Field(description="The search prompt or query."),
    tool: List[
        Literal[
            "web",
            "hackernews",
            "reddit",
            "wikipedia",
            "youtube",
            "twitter",
            "arxiv",
        ]
    ] = Field(description="List of tools to use. Must include at least one tool."),
    model: str = Field(
        default="NOVA",
        description="The model to use for the search. Value should 'NOVA', 'ORBIT' or 'HORIZON'",
    ),
    date_filter: Optional[str] = Field(
        default=None, description="Date filter for the search."
    ),
) -> str | dict:
"""
    Perform a search using Desearch.

    Args:
        prompt (str): The search prompt or query.
        tool (List[Literal["web", "hackernews", "reddit", "wikipedia", "youtube", "twitter", "arxiv"]]): List of tools to use. Must include at least one tool.
        model (str, optional): The model to use for the search. Defaults to "NOVA".
        date_filter (Optional[str], optional): Date filter for the search. Defaults to None.

    Returns:
        str | dict: The search result or an error string.

    """
    try:
        return self.client.search(
            prompt,
            tool,
            model,
            date_filter,
        )
    except Exception as e:
        return str(e)

```
 |  
| --- | --- |  
###  twitter_search_tool [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/desearch/#llama_index.tools.desearch.DesearchToolSpec.twitter_search_tool "Permanent link")

```
twitter_search_tool(
    query:  = Field(
        description="The Twitter search query."
    ),
    sort:  = Field(
        default="Top",
        description="Sort order for the results.",
    ),
    count:  = Field(
        default=10,
        description="Number of results to return.",
    ),
) -> BasicTwitterSearchResponse

```

Perform a basic Twitter search using the Exa API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The Twitter search query. Defaults to None.  |  `Field(description='The Twitter search query.')`  |  
|  `sort`  |  Sort order for the results. Defaults to "Top".  |  `Field(default='Top', description='Sort order for the results.')`  |  
|  `count`  |  Number of results to return. Defaults to 10.  |  `Field(default=10, description='Number of results to return.')`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `BasicTwitterSearchResponse`  |  `BasicTwitterSearchResponse`  |  The search results.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `Exception`  |  If an error occurs when calling the API.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-desearch/llama_index/tools/desearch/base.py`  
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
```
 | 
```
deftwitter_search_tool(
    self,
    query: str = Field(description="The Twitter search query."),
    sort: str = Field(default="Top", description="Sort order for the results."),
    count: int = Field(default=10, description="Number of results to return."),
) -> BasicTwitterSearchResponse:
"""
    Perform a basic Twitter search using the Exa API.

    Args:
        query (str, optional): The Twitter search query. Defaults to None.
        sort (str, optional): Sort order for the results. Defaults to "Top".
        count (int, optional): Number of results to return. Defaults to 10.

    Returns:
        BasicTwitterSearchResponse: The search results.

    Raises:
        Exception: If an error occurs when calling the API.

    """
    try:
        return self.client.basic_twitter_search(query, sort, count)
    except Exception as e:
        return str(e)

```
 |  
| --- | --- |  
###  web_search_tool [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/desearch/#llama_index.tools.desearch.DesearchToolSpec.web_search_tool "Permanent link")

```
web_search_tool(
    query:  = Field(description="The search query."),
    num:  = Field(
        default=10,
        description="Number of results to return.",
    ),
    start:  = Field(
        default=1,
        description="The starting index for the search results.",
    ),
) -> [WebSearchResult]

```

Perform a basic web search using the Exa API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The search query. Defaults to None.  |  `Field(description='The search query.')`  |  
|  `num`  |  Number of results to return. Defaults to 10.  |  `Field(default=10, description='Number of results to return.')`  |  
|  `start`  |  The starting index for the search results. Defaults to 1.  |  `Field(default=1, description='The starting index for the search results.')`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[WebSearchResult]`  |  List[WebSearchResult]: The search results.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `Exception`  |  If an error occurs when calling the API.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-desearch/llama_index/tools/desearch/base.py`  
| 
```
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
```
 | 
```
defweb_search_tool(
    self,
    query: str = Field(description="The search query."),
    num: int = Field(default=10, description="Number of results to return."),
    start: int = Field(
        default=1, description="The starting index for the search results."
    ),
) -> List[WebSearchResult]:
"""
    Perform a basic web search using the Exa API.

    Args:
        query (str, optional): The search query. Defaults to None.
        num (int, optional): Number of results to return. Defaults to 10.
        start (int, optional): The starting index for the search results. Defaults to 1.

    Returns:
        List[WebSearchResult]: The search results.

    Raises:
        Exception: If an error occurs when calling the API.

    """
    try:
        return self.client.basic_web_search(query, num, start)
    except Exception as e:
        return str(e)

```
 |  
| --- | --- |  
options: members: - DesearchToolSpec
