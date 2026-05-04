# Bagel
##  BagelReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/bagel/#llama_index.readers.bagel.BagelReader "Permanent link")
Bases: 
Reader for Bagel files.
Source code in `llama-index-integrations/readers/llama-index-readers-bagel/llama_index/readers/bagel/base.py`  
| 
```
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
```
 | 
```
classBagelReader(BaseReader):
"""Reader for Bagel files."""

    def__init__(self, collection_name: str) -> None:
"""
        Initialize BagelReader.

        Args: collection_name: Name of the collection to load from.

        Returns: None
        """
        try:
            importbagel
        except ImportError:
            raise ImportError(
                "`bagel` package not found, please run `pip install bagel`"
            )
        frombagel.configimport Settings

        if not collection_name:
            raise ValueError("collection_name cannot be empty")

        self.collection_name = collection_name

        server_settings = Settings(
            bagel_api_impl="rest", bagel_server_host="api.bageldb.ai"
        )

        self.client = bagel.Client(server_settings)

        self._collection = self.client.get_cluster(collection_name)

    defcreate_documents(self, results: Any) -> Any:
"""
        Create documents from the results.

        Args:
            results: Results from the query.

        Returns:
            List of documents.

        """
        documents = []
        # create a list of results
        all_results = list(
            zip(
                results["ids"][0],
                results["documents"][0],
                results["embeddings"][0],
                results["metadatas"][0],
            )
        )
        # iterate through the results
        for result in all_results:
            # create a Llama Document
            document = Document(
                doc_id=result[0],
                text=result[1],
                embedding=result[2],
                metadata=result[3],
            )
            documents.append(document)

        return documents

    defload_data(
        self,
        query_vector: Optional[OneOrMany[Embedding]] = None,
        query_texts: Optional[OneOrMany[Doc]] = None,
        limit: int = 10,
        where: Optional[Where] = None,
        where_document: Optional[WhereDocument] = None,
        include: Include = ["metadatas", "documents", "embeddings", "distances"],
    ) -> Any:
"""
        Get the top n_results documents for provided query_embeddings or query_texts.

        Args:
            query_embeddings: The embeddings to get the closes neighbors of. Optional.
            query_texts: The document texts to get the closes neighbors of. Optional.
            n_results: The number of neighbors to return for each query. Optional.
            where: A Where type dict used to filter results by. Optional.
            where_document: A WhereDocument type dict used to filter. Optional.
            include: A list of what to include in the results. Optional.

        Returns:
            Llama Index Document(s) with the closest embeddings to the
            query_embeddings or query_texts.

        """
        # get the results from the collection
        # If neither query_embeddings nor query_texts are provided,
        # or both are provided, raise an error
        if (query_vector is None and query_texts is None) or (
            query_vector is not None and query_texts is not None
        ):
            raise ValueError(
                "You must provide either embeddings or texts to find, but not both"
            )

        if where is None:
            where = {}

        if where_document is None:
            where_document = {}

        results = self._collection.find(
            query_embeddings=query_vector,
            query_texts=query_texts,
            n_results=limit,
            where=where,
            where_document=where_document,
            include=include,
        )

        # check if there are results
        if not results:
            raise ValueError("No results found")

        # check if there are embeddings or documents
        if not results["embeddings"] and not results["documents"]:
            raise ValueError("No embeddings or documents found")

        # create documents from the results
        return self.create_documents(results)

```
 |  
| --- | --- |  
###  create_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/bagel/#llama_index.readers.bagel.BagelReader.create_documents "Permanent link")

```
create_documents(results: ) -> 

```

Create documents from the results.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `results`  |  Results from the query.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-bagel/llama_index/readers/bagel/base.py`  
| 
```
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
```
 | 
```
defcreate_documents(self, results: Any) -> Any:
"""
    Create documents from the results.

    Args:
        results: Results from the query.

    Returns:
        List of documents.

    """
    documents = []
    # create a list of results
    all_results = list(
        zip(
            results["ids"][0],
            results["documents"][0],
            results["embeddings"][0],
            results["metadatas"][0],
        )
    )
    # iterate through the results
    for result in all_results:
        # create a Llama Document
        document = Document(
            doc_id=result[0],
            text=result[1],
            embedding=result[2],
            metadata=result[3],
        )
        documents.append(document)

    return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/bagel/#llama_index.readers.bagel.BagelReader.load_data "Permanent link")

```
load_data(
    query_vector: Optional[OneOrMany[Embedding]] = None,
    query_texts: Optional[OneOrMany[]] = None,
    limit:  = 10,
    where: Optional[] = None,
    where_document: Optional[WhereDocument] = None,
    include: Include = [
        "metadatas",
        "documents",
        "embeddings",
        "distances",
    ],
) -> 

```

Get the top n_results documents for provided query_embeddings or query_texts.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_embeddings`  |  The embeddings to get the closes neighbors of. Optional.  |  _required_  |  
|  `query_texts`  |  `Optional[OneOrMany[Doc]]`  |  The document texts to get the closes neighbors of. Optional.  |  `None`  |  
|  `n_results`  |  The number of neighbors to return for each query. Optional.  |  _required_  |  
|  `where`  |  `Optional[Where]`  |  A Where type dict used to filter results by. Optional.  |  `None`  |  
|  `where_document`  |  `Optional[WhereDocument]`  |  A WhereDocument type dict used to filter. Optional.  |  `None`  |  
|  `include`  |  `Include`  |  A list of what to include in the results. Optional.  |  `['metadatas', 'documents', 'embeddings', 'distances']`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  Llama Index Document(s) with the closest embeddings to the  |  
|  query_embeddings or query_texts.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-bagel/llama_index/readers/bagel/base.py`  
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
```
 | 
```
defload_data(
    self,
    query_vector: Optional[OneOrMany[Embedding]] = None,
    query_texts: Optional[OneOrMany[Doc]] = None,
    limit: int = 10,
    where: Optional[Where] = None,
    where_document: Optional[WhereDocument] = None,
    include: Include = ["metadatas", "documents", "embeddings", "distances"],
) -> Any:
"""
    Get the top n_results documents for provided query_embeddings or query_texts.

    Args:
        query_embeddings: The embeddings to get the closes neighbors of. Optional.
        query_texts: The document texts to get the closes neighbors of. Optional.
        n_results: The number of neighbors to return for each query. Optional.
        where: A Where type dict used to filter results by. Optional.
        where_document: A WhereDocument type dict used to filter. Optional.
        include: A list of what to include in the results. Optional.

    Returns:
        Llama Index Document(s) with the closest embeddings to the
        query_embeddings or query_texts.

    """
    # get the results from the collection
    # If neither query_embeddings nor query_texts are provided,
    # or both are provided, raise an error
    if (query_vector is None and query_texts is None) or (
        query_vector is not None and query_texts is not None
    ):
        raise ValueError(
            "You must provide either embeddings or texts to find, but not both"
        )

    if where is None:
        where = {}

    if where_document is None:
        where_document = {}

    results = self._collection.find(
        query_embeddings=query_vector,
        query_texts=query_texts,
        n_results=limit,
        where=where,
        where_document=where_document,
        include=include,
    )

    # check if there are results
    if not results:
        raise ValueError("No results found")

    # check if there are embeddings or documents
    if not results["embeddings"] and not results["documents"]:
        raise ValueError("No embeddings or documents found")

    # create documents from the results
    return self.create_documents(results)

```
 |  
| --- | --- |  
options: members: - BagelReader
