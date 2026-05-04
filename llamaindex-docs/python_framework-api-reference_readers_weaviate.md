# Weaviate
##  WeaviateReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/weaviate/#llama_index.readers.weaviate.WeaviateReader "Permanent link")
Bases: 
Weaviate reader.
Retrieves documents from Weaviate through vector lookup. Allows option to concatenate retrieved documents into one Document, or to return separate Document objects per document.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  host.  |  _required_  |  
|  `auth_client_secret`  |  `Optional[AuthCredentials]`  |  auth_client_secret.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-weaviate/llama_index/readers/weaviate/base.py`  
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
```
 | 
```
classWeaviateReader(BaseReader):
"""
    Weaviate reader.

    Retrieves documents from Weaviate through vector lookup. Allows option
    to concatenate retrieved documents into one Document, or to return
    separate Document objects per document.

    Args:
        host (str): host.
        auth_client_secret (Optional[weaviate.auth.AuthCredentials]):
            auth_client_secret.

    """

    def__init__(
        self,
        host: str,
        auth_client_secret: Optional[Any] = None,
    ) -> None:
"""Initialize with parameters."""
        try:
            importweaviate  # noqa
            fromweaviateimport Client
            fromweaviate.authimport AuthCredentials  # noqa
        except ImportError:
            raise ImportError(
                "`weaviate` package not found, please run `pip install weaviate-client`"
            )

        self.client: Client = Client(host, auth_client_secret=auth_client_secret)

    defload_data(
        self,
        class_name: Optional[str] = None,
        properties: Optional[List[str]] = None,
        graphql_query: Optional[str] = None,
        separate_documents: Optional[bool] = True,
    ) -> List[Document]:
"""
        Load data from Weaviate.

        If `graphql_query` is not found in load_kwargs, we assume that
        `class_name` and `properties` are provided.

        Args:
            class_name (Optional[str]): class_name to retrieve documents from.
            properties (Optional[List[str]]): properties to retrieve from documents.
            graphql_query (Optional[str]): Raw GraphQL Query.
                We assume that the query is a Get query.
            separate_documents (Optional[bool]): Whether to return separate
                documents. Defaults to True.

        Returns:
            List[Document]: A list of documents.

        """
        if class_name is not None and properties is not None:
            props_txt = "\n".join(properties)
            graphql_query = f"""
{{
{{
{class_name}{{
{props_txt}
}}
}}
}}

        elif graphql_query is not None:
            pass
        else:
            raise ValueError(
                "Either `class_name` and `properties` must be specified, "
                "or `graphql_query` must be specified."
            )

        response = self.client.query.raw(graphql_query)
        if "errors" in response:
            raise ValueError("Invalid query, got errors: {}".format(response["errors"]))

        data_response = response["data"]
        if "Get" not in data_response:
            raise ValueError("Invalid query response, must be a Get query.")

        if class_name is None:
            # infer class_name if only graphql_query was provided
            class_name = next(iter(data_response["Get"].keys()))
        entries = data_response["Get"][class_name]
        documents = []
        for entry in entries:
            embedding: Optional[List[float]] = None
            # for each entry, join properties into <property>:<value>
            # separated by newlines
            text_list = []
            for k, v in entry.items():
                if k == "_additional":
                    if "vector" in v:
                        embedding = v["vector"]
                    continue
                text_list.append(f"{k}: {v}")

            text = "\n".join(text_list)
            documents.append(Document(text=text, embedding=embedding))

        if not separate_documents:
            # join all documents into one
            text_list = [doc.get_content() for doc in documents]
            text = "\n\n".join(text_list)
            documents = [Document(text=text)]

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/weaviate/#llama_index.readers.weaviate.WeaviateReader.load_data "Permanent link")

```
load_data(
    class_name: Optional[] = None,
    properties: Optional[[]] = None,
    graphql_query: Optional[] = None,
    separate_documents: Optional[] = True,
) -> []

```

Load data from Weaviate.
If `graphql_query` is not found in load_kwargs, we assume that `class_name` and `properties` are provided.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `class_name`  |  `Optional[str]`  |  class_name to retrieve documents from.  |  `None`  |  
|  `properties`  |  `Optional[List[str]]`  |  properties to retrieve from documents.  |  `None`  |  
|  `graphql_query`  |  `Optional[str]`  |  Raw GraphQL Query. We assume that the query is a Get query.  |  `None`  |  
|  `separate_documents`  |  `Optional[bool]`  |  Whether to return separate documents. Defaults to True.  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-weaviate/llama_index/readers/weaviate/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    class_name: Optional[str] = None,
    properties: Optional[List[str]] = None,
    graphql_query: Optional[str] = None,
    separate_documents: Optional[bool] = True,
) -> List[Document]:
"""
    Load data from Weaviate.

    If `graphql_query` is not found in load_kwargs, we assume that
    `class_name` and `properties` are provided.

    Args:
        class_name (Optional[str]): class_name to retrieve documents from.
        properties (Optional[List[str]]): properties to retrieve from documents.
        graphql_query (Optional[str]): Raw GraphQL Query.
            We assume that the query is a Get query.
        separate_documents (Optional[bool]): Whether to return separate
            documents. Defaults to True.

    Returns:
        List[Document]: A list of documents.

    """
    if class_name is not None and properties is not None:
        props_txt = "\n".join(properties)
        graphql_query = f"""
{{
{{
{class_name}{{
{props_txt}
}}
}}
}}
        """
    elif graphql_query is not None:
        pass
    else:
        raise ValueError(
            "Either `class_name` and `properties` must be specified, "
            "or `graphql_query` must be specified."
        )

    response = self.client.query.raw(graphql_query)
    if "errors" in response:
        raise ValueError("Invalid query, got errors: {}".format(response["errors"]))

    data_response = response["data"]
    if "Get" not in data_response:
        raise ValueError("Invalid query response, must be a Get query.")

    if class_name is None:
        # infer class_name if only graphql_query was provided
        class_name = next(iter(data_response["Get"].keys()))
    entries = data_response["Get"][class_name]
    documents = []
    for entry in entries:
        embedding: Optional[List[float]] = None
        # for each entry, join properties into <property>:<value>
        # separated by newlines
        text_list = []
        for k, v in entry.items():
            if k == "_additional":
                if "vector" in v:
                    embedding = v["vector"]
                continue
            text_list.append(f"{k}: {v}")

        text = "\n".join(text_list)
        documents.append(Document(text=text, embedding=embedding))

    if not separate_documents:
        # join all documents into one
        text_list = [doc.get_content() for doc in documents]
        text = "\n\n".join(text_list)
        documents = [Document(text=text)]

    return documents

```
 |  
| --- | --- |  
options: members: - WeaviateReader
