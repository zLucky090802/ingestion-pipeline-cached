# Firestore
##  FirestoreReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/firestore/#llama_index.readers.firestore.FirestoreReader "Permanent link")
Bases: 
Simple Firestore reader.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `project_id`  |  The Google Cloud Project ID.  |  _required_  |  
|  `*args`  |  `Optional[Any]`  |  Additional arguments.  |  
|  `**kwargs`  |  `Optional[Any]`  |  Additional keyword arguments.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `FirestoreReader`  |  A FirestoreReader object.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-firestore/llama_index/readers/firestore/base.py`  
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
```
 | 
```
classFirestoreReader(BaseReader):
"""
    Simple Firestore reader.

    Args:
        project_id (str): The Google Cloud Project ID.
        *args (Optional[Any]): Additional arguments.
        **kwargs (Optional[Any]): Additional keyword arguments.

    Returns:
        FirestoreReader: A FirestoreReader object.

    """

    def__init__(
        self,
        project_id: str,
        database_id: str = DEFAULT_FIRESTORE_DATABASE,
        *args: Optional[Any],
        **kwargs: Optional[Any],
    ) -> None:
"""Initialize with parameters."""
        try:
            fromgoogle.cloudimport firestore
            fromgoogle.cloud.firestore_v1.services.firestore.transports.baseimport (
                DEFAULT_CLIENT_INFO,
            )
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        client_info = DEFAULT_CLIENT_INFO
        client_info.user_agent = USER_AGENT
        self.db = firestore.Client(
            project=project_id, database=database_id, client_info=client_info
        )

    defload_data(self, collection: str) -> List[Document]:
"""
        Load data from a Firestore collection, returning a list of Documents.

        Args:
            collection (str): The name of the Firestore collection to read from.

        Returns:
            List[Document]: A list of Document objects.

        """
        documents = []
        col_ref = self.db.collection(collection)
        for doc in col_ref.stream():
            doc_str = ", ".join([f"{k}: {v}" for k, v in doc.to_dict().items()])
            documents.append(Document(text=doc_str))
        return documents

    defload_document(self, document_url: str) -> Document:
"""
        Load a single document from Firestore.

        Args:
            document_url (str): The absolute path to the Firestore document to read.

        Returns:
            Document: A Document object.

        """
        parts = document_url.split("/")
        if len(parts) % 2 != 0:
            raise ValueError(f"Invalid document URL: {document_url}")

        ref = self.db.collection(parts[0])
        for i in range(1, len(parts)):
            if i % 2 == 0:
                ref = ref.collection(parts[i])
            else:
                ref = ref.document(parts[i])

        doc = ref.get()
        if not doc.exists:
            raise ValueError(f"No such document: {document_url}")
        doc_str = ", ".join([f"{k}: {v}" for k, v in doc.to_dict().items()])
        return Document(text=doc_str)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/firestore/#llama_index.readers.firestore.FirestoreReader.load_data "Permanent link")

```
load_data(collection: ) -> []

```

Load data from a Firestore collection, returning a list of Documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection`  |  The name of the Firestore collection to read from.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-firestore/llama_index/readers/firestore/base.py`  
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
```
 | 
```
defload_data(self, collection: str) -> List[Document]:
"""
    Load data from a Firestore collection, returning a list of Documents.

    Args:
        collection (str): The name of the Firestore collection to read from.

    Returns:
        List[Document]: A list of Document objects.

    """
    documents = []
    col_ref = self.db.collection(collection)
    for doc in col_ref.stream():
        doc_str = ", ".join([f"{k}: {v}" for k, v in doc.to_dict().items()])
        documents.append(Document(text=doc_str))
    return documents

```
 |  
| --- | --- |  
###  load_document [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/firestore/#llama_index.readers.firestore.FirestoreReader.load_document "Permanent link")

```
load_document(document_url: ) -> 

```

Load a single document from Firestore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `document_url`  |  The absolute path to the Firestore document to read.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |   |  A Document object.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-firestore/llama_index/readers/firestore/base.py`  
| 
```
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
defload_document(self, document_url: str) -> Document:
"""
    Load a single document from Firestore.

    Args:
        document_url (str): The absolute path to the Firestore document to read.

    Returns:
        Document: A Document object.

    """
    parts = document_url.split("/")
    if len(parts) % 2 != 0:
        raise ValueError(f"Invalid document URL: {document_url}")

    ref = self.db.collection(parts[0])
    for i in range(1, len(parts)):
        if i % 2 == 0:
            ref = ref.collection(parts[i])
        else:
            ref = ref.document(parts[i])

    doc = ref.get()
    if not doc.exists:
        raise ValueError(f"No such document: {document_url}")
    doc_str = ", ".join([f"{k}: {v}" for k, v in doc.to_dict().items()])
    return Document(text=doc_str)

```
 |  
| --- | --- |  
options: members: - FirestoreReader
