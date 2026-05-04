# Moss
##  MossToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/moss/#llama_index.tools.moss.MossToolSpec "Permanent link")
Bases: 
Moss Tool Spec.
This tool allows agents to interact with the Moss search engine to index documents and query for relevant information.
Source code in `llama-index-integrations/tools/llama-index-tools-moss/llama_index/tools/moss/base.py`  
| 
```
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
```
 | 
```
classMossToolSpec(BaseToolSpec):
"""
    Moss Tool Spec.

    This tool allows agents to interact with the Moss search engine to index documents
    and query for relevant information.
    """

    spec_functions: tuple[str, ...] = ("query", "list_indexes", "delete_index")

    def__init__(
        self,
        client: MossClient,
        index_name: str,
        query_options: Optional[QueryOptions] = None,
    ) -> None:
"""
        Initialize the Moss tool spec.

        Args:
            client (MossClient): The client to interact with the Moss service.
            index_name (str): The name of the index to use.
            query_options (Optional[QueryOptions]): Configuration options for the tool.
                Includes top_k (int), alpha (float), and model_id (str).

        """
        opt = query_options or QueryOptions()

        if not (0.0 <= opt.alpha <= 1.0):
            raise ValueError("alpha must be between 0 and 1")
        if opt.top_k  1:
            raise ValueError("top_k must be greater than 0")

        self.top_k: int = opt.top_k
        self.alpha: float = opt.alpha
        self.model_id: str = opt.model_id
        self.client: MossClient = client
        self.index_name: str = index_name
        self._index_loaded: bool = False

    async defindex_docs(self, docs: List[DocumentInfo]) -> None:
        await self.client.create_index(self.index_name, docs, model_id=self.model_id)
        self._index_loaded = False

    async def_load_index(self) -> None:
"""Load the index if it hasn't been loaded locally yet."""
        await self.client.load_index(self.index_name)
        self._index_loaded = True

    async defquery(self, query: str) -> str:
"""
        Search the Moss knowledge base for information relevant to a specific query.

        This tool performs a hybrid semantic search to find the most relevant
        text snippets from the indexed documents. It is best used for answering
        technical questions, retrieving facts, or finding specific context
        within a large collection of documents.

        Args:
            query (str): The search terms or question to look up in the index.

        Returns:
            str: A formatted report containing the top matching text snippets,
                 their relevance scores, and their source metadata (like filename).

        """
        if not self._index_loaded:
            await self._load_index()

        results = await self.client.query(
            self.index_name, query, MossQueryOptions(top_k=self.top_k, alpha=self.alpha)
        )
        answer = f"Search results for: '{query}'\n\n"

        for i, result in enumerate(results.docs):
            source = (
                result.metadata.get("filename")
                or result.metadata.get("source")
                or "Unknown Source"
            )
            page = result.metadata.get("page", "N/A")

            answer += f"Match {i+1} [Score: {result.score:.2f}]\n"
            answer += f"Source: {source} (Page: {page})\n"
            answer += f"Content: {result.text}\n"
            answer += "-" * 20 + "\n\n"

        return answer

    async deflist_indexes(self) -> str:
"""
        List all available indexes in the Moss project.

        Use this tool to discover what indexes exist before querying or managing them.

        Returns:
            str: A formatted list of all index names in the project.

        """
        indexes = await self.client.list_indexes()
        if not indexes:
            return "No indexes found."

        result = "Available indexes:\n"
        for idx in indexes:
            result += f"  - {idx.name} (docs: {idx.doc_count}, status: {idx.status})\n"
        return result

    async defdelete_index(self, index_name: str) -> str:
"""
        Delete an index from the Moss project.

        Use this tool to remove an index and all its documents when it is no longer needed.

        Args:
            index_name (str): The name of the index to delete.

        Returns:
            str: A confirmation message indicating the index was deleted.

        """
        await self.client.delete_index(index_name)
        if index_name == self.index_name:
            self._index_loaded = False
        return f"Index '{index_name}' has been deleted."

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/moss/#llama_index.tools.moss.MossToolSpec.query "Permanent link")

```
query(query: ) -> 

```

Search the Moss knowledge base for information relevant to a specific query.
This tool performs a hybrid semantic search to find the most relevant text snippets from the indexed documents. It is best used for answering technical questions, retrieving facts, or finding specific context within a large collection of documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The search terms or question to look up in the index.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A formatted report containing the top matching text snippets, their relevance scores, and their source metadata (like filename).  |  
Source code in `llama-index-integrations/tools/llama-index-tools-moss/llama_index/tools/moss/base.py`  
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
```
 | 
```
async defquery(self, query: str) -> str:
"""
    Search the Moss knowledge base for information relevant to a specific query.

    This tool performs a hybrid semantic search to find the most relevant
    text snippets from the indexed documents. It is best used for answering
    technical questions, retrieving facts, or finding specific context
    within a large collection of documents.

    Args:
        query (str): The search terms or question to look up in the index.

    Returns:
        str: A formatted report containing the top matching text snippets,
             their relevance scores, and their source metadata (like filename).

    """
    if not self._index_loaded:
        await self._load_index()

    results = await self.client.query(
        self.index_name, query, MossQueryOptions(top_k=self.top_k, alpha=self.alpha)
    )
    answer = f"Search results for: '{query}'\n\n"

    for i, result in enumerate(results.docs):
        source = (
            result.metadata.get("filename")
            or result.metadata.get("source")
            or "Unknown Source"
        )
        page = result.metadata.get("page", "N/A")

        answer += f"Match {i+1} [Score: {result.score:.2f}]\n"
        answer += f"Source: {source} (Page: {page})\n"
        answer += f"Content: {result.text}\n"
        answer += "-" * 20 + "\n\n"

    return answer

```
 |  
| --- | --- |  
###  list_indexes [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/moss/#llama_index.tools.moss.MossToolSpec.list_indexes "Permanent link")

```
list_indexes() -> 

```

List all available indexes in the Moss project.
Use this tool to discover what indexes exist before querying or managing them.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A formatted list of all index names in the project.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-moss/llama_index/tools/moss/base.py`  
| 
```
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
```
 | 
```
async deflist_indexes(self) -> str:
"""
    List all available indexes in the Moss project.

    Use this tool to discover what indexes exist before querying or managing them.

    Returns:
        str: A formatted list of all index names in the project.

    """
    indexes = await self.client.list_indexes()
    if not indexes:
        return "No indexes found."

    result = "Available indexes:\n"
    for idx in indexes:
        result += f"  - {idx.name} (docs: {idx.doc_count}, status: {idx.status})\n"
    return result

```
 |  
| --- | --- |  
###  delete_index [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/moss/#llama_index.tools.moss.MossToolSpec.delete_index "Permanent link")

```
delete_index(index_name: ) -> 

```

Delete an index from the Moss project.
Use this tool to remove an index and all its documents when it is no longer needed.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index_name`  |  The name of the index to delete.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A confirmation message indicating the index was deleted.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-moss/llama_index/tools/moss/base.py`  
| 
```
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
```
 | 
```
async defdelete_index(self, index_name: str) -> str:
"""
    Delete an index from the Moss project.

    Use this tool to remove an index and all its documents when it is no longer needed.

    Args:
        index_name (str): The name of the index to delete.

    Returns:
        str: A confirmation message indicating the index was deleted.

    """
    await self.client.delete_index(index_name)
    if index_name == self.index_name:
        self._index_loaded = False
    return f"Index '{index_name}' has been deleted."

```
 |  
| --- | --- |  
##  QueryOptions `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/moss/#llama_index.tools.moss.QueryOptions "Permanent link")
Configuration options for Moss search queries.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `top_k`  |  Number of results to return from queries. Defaults to 5.  |  
| `alpha`  |  `float`  |  Hybrid search weight (0.0=keyword, 1.0=semantic). Defaults to 0.5.  |  
| `model_id`  |  The embedding model ID used when creating the index. Defaults to "moss-minilm".  |  
Source code in `llama-index-integrations/tools/llama-index-tools-moss/llama_index/tools/moss/base.py`  
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
```
 | 
```
@dataclass
classQueryOptions:
"""
    Configuration options for Moss search queries.

    Attributes:
        top_k (int): Number of results to return from queries. Defaults to 5.
        alpha (float): Hybrid search weight (0.0=keyword, 1.0=semantic). Defaults to 0.5.
        model_id (str): The embedding model ID used when creating the index. Defaults to "moss-minilm".

    """

    top_k: int = 5
    alpha: float = 0.5
    model_id: str = "moss-minilm"

```
 |  
| --- | --- |  
options: members: - MossToolSpec
