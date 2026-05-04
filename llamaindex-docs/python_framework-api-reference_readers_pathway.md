# Pathway
##  PathwayReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pathway/#llama_index.readers.pathway.PathwayReader "Permanent link")
Bases: 
Pathway reader.
Retrieve documents from Pathway data indexing pipeline.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  The URI where Pathway is currently hosted.  |  `None`  |  
|  `port`  |  `str | int`  |  The port number on which Pathway is listening.  |  `None`  |  
See Also
llamaindex.retriever.pathway.PathwayRetriever and, llamaindex.retriever.pathway.PathwayVectorServer
Source code in `llama-index-integrations/readers/llama-index-readers-pathway/llama_index/readers/pathway/base.py`  
| 
```
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
```
 | 
```
classPathwayReader(BaseReader):
"""
    Pathway reader.

    Retrieve documents from Pathway data indexing pipeline.

    Args:
        host (str): The URI where Pathway is currently hosted.
        port (str | int): The port number on which Pathway is listening.

    See Also:
        llamaindex.retriever.pathway.PathwayRetriever and,
        llamaindex.retriever.pathway.PathwayVectorServer

    """

    def__init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        url: Optional[str] = None,
    ):
"""Initializing the Pathway reader client."""
        self.client = _VectorStoreClient(host, port, url)

    defload_data(
        self,
        query_text: str,
        k: Optional[int] = 4,
        metadata_filter: Optional[str] = None,
    ) -> List[Document]:
"""
        Load data from Pathway.

        Args:
            query_text (str): The text to get the closest neighbors of.
            k (int): Number of results to return.
            metadata_filter (str): Filter to be applied.

        Returns:
            List[Document]: A list of documents.

        """
        results = self.client(query_text, k, metadata_filter)
        documents = []
        for return_elem in results:
            document = Document(
                text=return_elem["text"],
                extra_info=return_elem["metadata"],
            )

            documents.append(document)

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pathway/#llama_index.readers.pathway.PathwayReader.load_data "Permanent link")

```
load_data(
    query_text: ,
    k: Optional[] = 4,
    metadata_filter: Optional[] = None,
) -> []

```

Load data from Pathway.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_text`  |  The text to get the closest neighbors of.  |  _required_  |  
|  Number of results to return.  |  
|  `metadata_filter`  |  Filter to be applied.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-pathway/llama_index/readers/pathway/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    query_text: str,
    k: Optional[int] = 4,
    metadata_filter: Optional[str] = None,
) -> List[Document]:
"""
    Load data from Pathway.

    Args:
        query_text (str): The text to get the closest neighbors of.
        k (int): Number of results to return.
        metadata_filter (str): Filter to be applied.

    Returns:
        List[Document]: A list of documents.

    """
    results = self.client(query_text, k, metadata_filter)
    documents = []
    for return_elem in results:
        document = Document(
            text=return_elem["text"],
            extra_info=return_elem["metadata"],
        )

        documents.append(document)

    return documents

```
 |  
| --- | --- |  
options: members: - PathwayReader
