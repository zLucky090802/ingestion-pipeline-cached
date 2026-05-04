# Dashvector
##  DashVectorReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/dashvector/#llama_index.readers.dashvector.DashVectorReader "Permanent link")
Bases: 
DashVector reader.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  DashVector API key.  |  _required_  |  
|  `endpoint`  |  DashVector cluster endpoint.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-dashvector/llama_index/readers/dashvector/base.py`  
| 
```
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
```
 | 
```
classDashVectorReader(BaseReader):
"""
    DashVector reader.

    Args:
        api_key (str): DashVector API key.
        endpoint (str): DashVector cluster endpoint.

    """

    def__init__(self, api_key: str, endpoint: str):
"""Initialize with parameters."""
        try:
            importdashvector
        except ImportError:
            raise ImportError(
                "`dashvector` package not found, please run `pip install dashvector`"
            )

        self._client: dashvector.Client = dashvector.Client(
            api_key=api_key, endpoint=endpoint
        )

    defload_data(
        self,
        collection_name: str,
        vector: Optional[List[float]],
        topk: int,
        filter: Optional[str] = None,
        include_vector: bool = True,
        partition: Optional[str] = None,
        output_fields: Optional[List[str]] = None,
        sparse_vector: Optional[Dict[int, float]] = None,
    ) -> List[Document]:
"""
        Load data from DashVector.

        Args:
            collection_name (str): Name of the collection.
            vector (List[float]): Query vector.
            topk (int): Number of results to return.
            filter (Optional[str]): doc fields filter
                conditions that meet the SQL where clause specification.detail in https://help.aliyun.com/document_detail/2513006.html?spm=a2c4g.2510250.0.0.40d25637QMI4eV
            include_vector (bool): Whether to include the embedding in the response.Defaults to True.
            partition (Optional[str]): The partition name
                to query. Defaults to None.
            output_fields (Optional[List[str]]): The fields
                to return. Defaults to None, meaning all fields
            sparse_vector (Optional[Dict[int, float]]): The
                sparse vector to query.Defaults to None.

        Returns:
            List[Document]: A list of documents.

        """
        collection = self._client.get(collection_name)
        if not collection:
            raise ValueError(
                f"Failed to get collection: {collection_name},Error: {collection}"
            )

        ret = collection.query(
            vector=vector,
            topk=topk,
            filter=filter,
            include_vector=include_vector,
            partition=partition,
            output_fields=output_fields,
            sparse_vector=sparse_vector,
        )
        if not ret:
            raise Exception(f"Failed to query document,Error: {ret}")

        doc_metas = ret.output
        documents = []

        for doc_meta in doc_metas:
            node_content = json.loads(doc_meta.fields["_node_content"])
            document = Document(
                id_=doc_meta.id,
                text=node_content["text"],
                metadata=node_content["metadata"],
                embedding=doc_meta.vector,
            )
            documents.append(document)

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/dashvector/#llama_index.readers.dashvector.DashVectorReader.load_data "Permanent link")

```
load_data(
    collection_name: ,
    vector: Optional[[float]],
    topk: ,
    filter: Optional[] = None,
    include_vector:  = True,
    partition: Optional[] = None,
    output_fields: Optional[[]] = None,
    sparse_vector: Optional[[, float]] = None,
) -> []

```

Load data from DashVector.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_name`  |  Name of the collection.  |  _required_  |  
|  `vector`  |  `List[float]`  |  Query vector.  |  _required_  |  
|  `topk`  |  Number of results to return.  |  _required_  |  
|  `filter`  |  `Optional[str]`  |  doc fields filter conditions that meet the SQL where clause specification.detail in https://help.aliyun.com/document_detail/2513006.html?spm=a2c4g.2510250.0.0.40d25637QMI4eV  |  `None`  |  
|  `include_vector`  |  `bool`  |  Whether to include the embedding in the response.Defaults to True.  |  `True`  |  
|  `partition`  |  `Optional[str]`  |  The partition name to query. Defaults to None.  |  `None`  |  
|  `output_fields`  |  `Optional[List[str]]`  |  The fields to return. Defaults to None, meaning all fields  |  `None`  |  
|  `sparse_vector`  |  `Optional[Dict[int, float]]`  |  The sparse vector to query.Defaults to None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-dashvector/llama_index/readers/dashvector/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    collection_name: str,
    vector: Optional[List[float]],
    topk: int,
    filter: Optional[str] = None,
    include_vector: bool = True,
    partition: Optional[str] = None,
    output_fields: Optional[List[str]] = None,
    sparse_vector: Optional[Dict[int, float]] = None,
) -> List[Document]:
"""
    Load data from DashVector.

    Args:
        collection_name (str): Name of the collection.
        vector (List[float]): Query vector.
        topk (int): Number of results to return.
        filter (Optional[str]): doc fields filter
            conditions that meet the SQL where clause specification.detail in https://help.aliyun.com/document_detail/2513006.html?spm=a2c4g.2510250.0.0.40d25637QMI4eV
        include_vector (bool): Whether to include the embedding in the response.Defaults to True.
        partition (Optional[str]): The partition name
            to query. Defaults to None.
        output_fields (Optional[List[str]]): The fields
            to return. Defaults to None, meaning all fields
        sparse_vector (Optional[Dict[int, float]]): The
            sparse vector to query.Defaults to None.

    Returns:
        List[Document]: A list of documents.

    """
    collection = self._client.get(collection_name)
    if not collection:
        raise ValueError(
            f"Failed to get collection: {collection_name},Error: {collection}"
        )

    ret = collection.query(
        vector=vector,
        topk=topk,
        filter=filter,
        include_vector=include_vector,
        partition=partition,
        output_fields=output_fields,
        sparse_vector=sparse_vector,
    )
    if not ret:
        raise Exception(f"Failed to query document,Error: {ret}")

    doc_metas = ret.output
    documents = []

    for doc_meta in doc_metas:
        node_content = json.loads(doc_meta.fields["_node_content"])
        document = Document(
            id_=doc_meta.id,
            text=node_content["text"],
            metadata=node_content["metadata"],
            embedding=doc_meta.vector,
        )
        documents.append(document)

    return documents

```
 |  
| --- | --- |  
options: members: - DashVectorReader
