# Graphql
##  GraphQLReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/graphql/#llama_index.readers.graphql.GraphQLReader "Permanent link")
Bases: 
GraphQL reader.
Combines all GraphQL results into the Document used by LlamaIndex.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `uri`  |  GraphQL uri.  |  `None`  |  
|  `headers`  |  `Optional[Dict]`  |  Optional http headers.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-graphql/llama_index/readers/graphql/base.py`  
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
```
 | 
```
classGraphQLReader(BaseReader):
"""
    GraphQL reader.

    Combines all GraphQL results into the Document used by LlamaIndex.

    Args:
        uri (str): GraphQL uri.
        headers (Optional[Dict]): Optional http headers.

    """

    def__init__(
        self,
        uri: Optional[str] = None,
        headers: Optional[Dict] = None,
    ) -> None:
"""Initialize with parameters."""
        try:
            fromgqlimport Client
            fromgql.transport.requestsimport RequestsHTTPTransport

        except ImportError:
            raise ImportError("`gql` package not found, please run `pip install gql`")
        if uri:
            if uri is None:
                raise ValueError("`uri` must be provided.")
            if headers is None:
                headers = {}
            transport = RequestsHTTPTransport(url=uri, headers=headers)
            self.client = Client(transport=transport, fetch_schema_from_transport=True)

    defload_data(self, query: str, variables: Optional[Dict] = None) -> List[Document]:
"""
        Run query with optional variables and turn results into documents.

        Args:
            query (str): GraphQL query string.
            variables (Optional[Dict]): optional query parameters.

        Returns:
            List[Document]: A list of documents.

        """
        try:
            fromgqlimport gql

        except ImportError:
            raise ImportError("`gql` package not found, please run `pip install gql`")
        if variables is None:
            variables = {}

        documents = []

        result = self.client.execute(gql(query), variable_values=variables)

        for key in result:
            entry = result[key]
            if isinstance(entry, list):
                documents.extend([Document(text=yaml.dump(v)) for v in entry])
            else:
                documents.append(Document(text=yaml.dump(entry)))

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/graphql/#llama_index.readers.graphql.GraphQLReader.load_data "Permanent link")

```
load_data(
    query: , variables: Optional[] = None
) -> []

```

Run query with optional variables and turn results into documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  GraphQL query string.  |  _required_  |  
|  `variables`  |  `Optional[Dict]`  |  optional query parameters.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-graphql/llama_index/readers/graphql/base.py`  
| 
```
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
```
 | 
```
defload_data(self, query: str, variables: Optional[Dict] = None) -> List[Document]:
"""
    Run query with optional variables and turn results into documents.

    Args:
        query (str): GraphQL query string.
        variables (Optional[Dict]): optional query parameters.

    Returns:
        List[Document]: A list of documents.

    """
    try:
        fromgqlimport gql

    except ImportError:
        raise ImportError("`gql` package not found, please run `pip install gql`")
    if variables is None:
        variables = {}

    documents = []

    result = self.client.execute(gql(query), variable_values=variables)

    for key in result:
        entry = result[key]
        if isinstance(entry, list):
            documents.extend([Document(text=yaml.dump(v)) for v in entry])
        else:
            documents.append(Document(text=yaml.dump(entry)))

    return documents

```
 |  
| --- | --- |  
options: members: - GraphQLReader
