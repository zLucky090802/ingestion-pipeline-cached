# Metaphor
##  MetaphorToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/metaphor/#llama_index.tools.metaphor.MetaphorToolSpec "Permanent link")
Bases: 
Metaphor tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-metaphor/llama_index/tools/metaphor/base.py`  
| 
```
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
```
 | 
```
classMetaphorToolSpec(BaseToolSpec):
"""Metaphor tool spec."""

    spec_functions = [
        "search",
        "retrieve_documents",
        "search_and_retrieve_documents",
        "find_similar",
        "current_date",
    ]

    def__init__(self, api_key: str, verbose: bool = True) -> None:
"""Initialize with parameters."""
        frommetaphor_pythonimport Metaphor

        self.client = Metaphor(api_key=api_key, user_agent="llama-index")
        self._verbose = verbose

    defsearch(
        self,
        query: str,
        num_results: Optional[int] = 10,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        start_published_date: Optional[str] = None,
        end_published_date: Optional[str] = None,
    ) -> str:
"""
        Metaphor allows you to use a natural language query to search the internet.

        Args:
            query (str): A natural language query phrased as an answer for what the link provides, ie: "This is the latest news about space:"
            num_results (Optional[int]): Number of results to return. Defaults to 10.
            include_domains (Optional[List(str)]): A list of top level domains like ["wsj.com"] to limit the search to specific sites.
            exclude_domains (Optional[List(str)]): Top level domains to exclude.
            start_published_date (Optional[str]): A date string like "2020-06-15". Get the date from `current_date`
            end_published_date (Optional[str]): End date string

        """
        response = self.client.search(
            query,
            num_results=num_results,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            start_published_date=start_published_date,
            end_published_date=end_published_date,
            use_autoprompt=True,
        )
        if self._verbose:
            print(f"[Metaphor Tool] Autoprompt: {response.autoprompt_string}")
        return [
            {"title": result.title, "url": result.url, "id": result.id}
            for result in response.results
        ]

    defretrieve_documents(self, ids: List[str]) -> List[Document]:
"""
        Retrieve a list of document summaries returned by `metaphor_search`, using the ID field.

        Args:
            ids (List(str)): the ids of the documents to retrieve

        """
        response = self.client.get_contents(ids)
        return [Document(text=con.extract) for con in response.contents]

    deffind_similar(
        self,
        url: str,
        num_results: Optional[int] = 3,
        start_published_date: Optional[str] = None,
        end_published_date: Optional[str] = None,
    ) -> str:
"""
        Retrieve a list of similar documents to a given url.

        Args:
            url (str): The web page to find similar results of
            num_results (Optional[int]): Number of results to return. Default 3.
            start_published_date (Optional[str]): A date string like "2020-06-15"
            end_published_date (Optional[str]): End date string

        """
        response = self.client.find_similar(
            url,
            num_results=num_results,
            start_published_date=start_published_date,
            end_published_date=end_published_date,
        )
        return [
            {"title": result.title, "url": result.url, "id": result.id}
            for result in response.results
        ]

    defsearch_and_retrieve_documents(
        self,
        query: str,
        num_results: Optional[int] = 10,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        start_published_date: Optional[str] = None,
        end_published_date: Optional[str] = None,
    ) -> str:
"""
        Combines the functionality of `search` and `retrieve_documents`.

        Args:
            query (str): the natural language query
            num_results (Optional[int]): Number of results. Defaults to 10.
            include_domains (Optional[List(str)]): A list of top level domains to search, like ["wsj.com"]
            exclude_domains (Optional[List(str)]): Top level domains to exclude.
            start_published_date (Optional[str]): A date string like "2020-06-15".
            end_published_date (Optional[str]): End date string

        """
        response = self.client.search(
            query,
            num_results=num_results,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            start_published_date=start_published_date,
            end_published_date=end_published_date,
            use_autoprompt=True,
        )
        if self._verbose:
            print(f"[Metaphor Tool] Autoprompt: {response.autoprompt_string}")
        ids = [result.id for result in response.results]
        documents = self.client.get_contents(ids)
        return [Document(text=document.extract) for document in documents.contents]

    defcurrent_date(self):
"""
        A function to return todays date.
        Call this before any other functions that take timestamps as an argument.
        """
        return datetime.date.today()

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/metaphor/#llama_index.tools.metaphor.MetaphorToolSpec.search "Permanent link")

```
search(
    query: ,
    num_results: Optional[] = 10,
    include_domains: Optional[[]] = None,
    exclude_domains: Optional[[]] = None,
    start_published_date: Optional[] = None,
    end_published_date: Optional[] = None,
) -> 

```

Metaphor allows you to use a natural language query to search the internet.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  A natural language query phrased as an answer for what the link provides, ie: "This is the latest news about space:"  |  _required_  |  
|  `num_results`  |  `Optional[int]`  |  Number of results to return. Defaults to 10.  |  
|  `include_domains`  |  `Optional[List(str)]`  |  A list of top level domains like ["wsj.com"] to limit the search to specific sites.  |  `None`  |  
|  `exclude_domains`  |  `Optional[List(str)]`  |  Top level domains to exclude.  |  `None`  |  
|  `start_published_date`  |  `Optional[str]`  |  A date string like "2020-06-15". Get the date from `current_date`  |  `None`  |  
|  `end_published_date`  |  `Optional[str]`  |  End date string  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-metaphor/llama_index/tools/metaphor/base.py`  
| 
```
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
```
 | 
```
defsearch(
    self,
    query: str,
    num_results: Optional[int] = 10,
    include_domains: Optional[List[str]] = None,
    exclude_domains: Optional[List[str]] = None,
    start_published_date: Optional[str] = None,
    end_published_date: Optional[str] = None,
) -> str:
"""
    Metaphor allows you to use a natural language query to search the internet.

    Args:
        query (str): A natural language query phrased as an answer for what the link provides, ie: "This is the latest news about space:"
        num_results (Optional[int]): Number of results to return. Defaults to 10.
        include_domains (Optional[List(str)]): A list of top level domains like ["wsj.com"] to limit the search to specific sites.
        exclude_domains (Optional[List(str)]): Top level domains to exclude.
        start_published_date (Optional[str]): A date string like "2020-06-15". Get the date from `current_date`
        end_published_date (Optional[str]): End date string

    """
    response = self.client.search(
        query,
        num_results=num_results,
        include_domains=include_domains,
        exclude_domains=exclude_domains,
        start_published_date=start_published_date,
        end_published_date=end_published_date,
        use_autoprompt=True,
    )
    if self._verbose:
        print(f"[Metaphor Tool] Autoprompt: {response.autoprompt_string}")
    return [
        {"title": result.title, "url": result.url, "id": result.id}
        for result in response.results
    ]

```
 |  
| --- | --- |  
###  retrieve_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/metaphor/#llama_index.tools.metaphor.MetaphorToolSpec.retrieve_documents "Permanent link")

```
retrieve_documents(ids: []) -> []

```

Retrieve a list of document summaries returned by `metaphor_search`, using the ID field.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ids`  |  `List(str)`  |  the ids of the documents to retrieve  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-metaphor/llama_index/tools/metaphor/base.py`  
| 
```
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
```
 | 
```
defretrieve_documents(self, ids: List[str]) -> List[Document]:
"""
    Retrieve a list of document summaries returned by `metaphor_search`, using the ID field.

    Args:
        ids (List(str)): the ids of the documents to retrieve

    """
    response = self.client.get_contents(ids)
    return [Document(text=con.extract) for con in response.contents]

```
 |  
| --- | --- |  
###  find_similar [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/metaphor/#llama_index.tools.metaphor.MetaphorToolSpec.find_similar "Permanent link")

```
find_similar(
    url: ,
    num_results: Optional[] = 3,
    start_published_date: Optional[] = None,
    end_published_date: Optional[] = None,
) -> 

```

Retrieve a list of similar documents to a given url.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  The web page to find similar results of  |  _required_  |  
|  `num_results`  |  `Optional[int]`  |  Number of results to return. Default 3.  |  
|  `start_published_date`  |  `Optional[str]`  |  A date string like "2020-06-15"  |  `None`  |  
|  `end_published_date`  |  `Optional[str]`  |  End date string  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-metaphor/llama_index/tools/metaphor/base.py`  
| 
```
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
```
 | 
```
deffind_similar(
    self,
    url: str,
    num_results: Optional[int] = 3,
    start_published_date: Optional[str] = None,
    end_published_date: Optional[str] = None,
) -> str:
"""
    Retrieve a list of similar documents to a given url.

    Args:
        url (str): The web page to find similar results of
        num_results (Optional[int]): Number of results to return. Default 3.
        start_published_date (Optional[str]): A date string like "2020-06-15"
        end_published_date (Optional[str]): End date string

    """
    response = self.client.find_similar(
        url,
        num_results=num_results,
        start_published_date=start_published_date,
        end_published_date=end_published_date,
    )
    return [
        {"title": result.title, "url": result.url, "id": result.id}
        for result in response.results
    ]

```
 |  
| --- | --- |  
###  search_and_retrieve_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/metaphor/#llama_index.tools.metaphor.MetaphorToolSpec.search_and_retrieve_documents "Permanent link")

```
search_and_retrieve_documents(
    query: ,
    num_results: Optional[] = 10,
    include_domains: Optional[[]] = None,
    exclude_domains: Optional[[]] = None,
    start_published_date: Optional[] = None,
    end_published_date: Optional[] = None,
) -> 

```

Combines the functionality of `search` and `retrieve_documents`.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  the natural language query  |  _required_  |  
|  `num_results`  |  `Optional[int]`  |  Number of results. Defaults to 10.  |  
|  `include_domains`  |  `Optional[List(str)]`  |  A list of top level domains to search, like ["wsj.com"]  |  `None`  |  
|  `exclude_domains`  |  `Optional[List(str)]`  |  Top level domains to exclude.  |  `None`  |  
|  `start_published_date`  |  `Optional[str]`  |  A date string like "2020-06-15".  |  `None`  |  
|  `end_published_date`  |  `Optional[str]`  |  End date string  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-metaphor/llama_index/tools/metaphor/base.py`  
| 
```
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
```
 | 
```
defsearch_and_retrieve_documents(
    self,
    query: str,
    num_results: Optional[int] = 10,
    include_domains: Optional[List[str]] = None,
    exclude_domains: Optional[List[str]] = None,
    start_published_date: Optional[str] = None,
    end_published_date: Optional[str] = None,
) -> str:
"""
    Combines the functionality of `search` and `retrieve_documents`.

    Args:
        query (str): the natural language query
        num_results (Optional[int]): Number of results. Defaults to 10.
        include_domains (Optional[List(str)]): A list of top level domains to search, like ["wsj.com"]
        exclude_domains (Optional[List(str)]): Top level domains to exclude.
        start_published_date (Optional[str]): A date string like "2020-06-15".
        end_published_date (Optional[str]): End date string

    """
    response = self.client.search(
        query,
        num_results=num_results,
        include_domains=include_domains,
        exclude_domains=exclude_domains,
        start_published_date=start_published_date,
        end_published_date=end_published_date,
        use_autoprompt=True,
    )
    if self._verbose:
        print(f"[Metaphor Tool] Autoprompt: {response.autoprompt_string}")
    ids = [result.id for result in response.results]
    documents = self.client.get_contents(ids)
    return [Document(text=document.extract) for document in documents.contents]

```
 |  
| --- | --- |  
###  current_date [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/metaphor/#llama_index.tools.metaphor.MetaphorToolSpec.current_date "Permanent link")

```
current_date()

```

A function to return todays date. Call this before any other functions that take timestamps as an argument.
Source code in `llama-index-integrations/tools/llama-index-tools-metaphor/llama_index/tools/metaphor/base.py`  
| 
```
140
141
142
143
144
145
```
 | 
```
defcurrent_date(self):
"""
    A function to return todays date.
    Call this before any other functions that take timestamps as an argument.
    """
    return datetime.date.today()

```
 |  
| --- | --- |  
options: members: - MetaphorToolSpec
