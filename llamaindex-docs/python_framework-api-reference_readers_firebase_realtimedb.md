# Firebase realtimedb
##  FirebaseRealtimeDatabaseReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/firebase_realtimedb/#llama_index.readers.firebase_realtimedb.FirebaseRealtimeDatabaseReader "Permanent link")
Bases: 
Firebase Realtime Database reader.
Retrieves data from Firebase Realtime Database and converts it into the Document used by LlamaIndex.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `database_url`  |  Firebase Realtime Database URL.  |  _required_  |  
|  `service_account_key_path`  |  `Optional[str]`  |  Path to the service account key file.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-firebase-realtimedb/llama_index/readers/firebase_realtimedb/base.py`  
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
```
 | 
```
classFirebaseRealtimeDatabaseReader(BaseReader):
"""
    Firebase Realtime Database reader.

    Retrieves data from Firebase Realtime Database and converts it into the Document used by LlamaIndex.

    Args:
        database_url (str): Firebase Realtime Database URL.
        service_account_key_path (Optional[str]): Path to the service account key file.

    """

    def__init__(
        self,
        database_url: str,
        service_account_key_path: Optional[str] = None,
    ) -> None:
"""Initialize with parameters."""
        try:
            importfirebase_admin
            fromfirebase_adminimport credentials
        except ImportError:
            raise ImportError(
                "`firebase_admin` package not found, please run `pip install"
                " firebase-admin`"
            )

        if not firebase_admin._apps:
            if service_account_key_path:
                cred = credentials.Certificate(service_account_key_path)
                firebase_admin.initialize_app(
                    cred, options={"databaseURL": database_url}
                )
            else:
                firebase_admin.initialize_app(options={"databaseURL": database_url})

    defload_data(self, path: str, field: Optional[str] = None) -> List[Document]:
"""
        Load data from Firebase Realtime Database and convert it into documents.

        Args:
            path (str): Path to the data in the Firebase Realtime Database.
            field (str, Optional): Key to pick data from

        Returns:
            List[Document]: A list of documents.

        """
        try:
            fromfirebase_adminimport db
        except ImportError:
            raise ImportError(
                "`firebase_admin` package not found, please run `pip install"
                " firebase-admin`"
            )

        ref = db.reference(path)
        data = ref.get()

        documents = []

        if isinstance(data, Dict):
            for key in data:
                entry = data[key]
                extra_info = {
                    "document_id": key,
                }
                if type(entry) is Dict and field in entry:
                    text = entry[field]
                else:
                    text = str(entry)

                document = Document(text=text, extra_info=extra_info)
                documents.append(document)
        elif isinstance(data, str):
            documents.append(Document(text=data))

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/firebase_realtimedb/#llama_index.readers.firebase_realtimedb.FirebaseRealtimeDatabaseReader.load_data "Permanent link")

```
load_data(
    path: , field: Optional[] = None
) -> []

```

Load data from Firebase Realtime Database and convert it into documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `path`  |  Path to the data in the Firebase Realtime Database.  |  _required_  |  
|  `field`  |  `(str, Optional)`  |  Key to pick data from  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-firebase-realtimedb/llama_index/readers/firebase_realtimedb/base.py`  
| 
```
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
```
 | 
```
defload_data(self, path: str, field: Optional[str] = None) -> List[Document]:
"""
    Load data from Firebase Realtime Database and convert it into documents.

    Args:
        path (str): Path to the data in the Firebase Realtime Database.
        field (str, Optional): Key to pick data from

    Returns:
        List[Document]: A list of documents.

    """
    try:
        fromfirebase_adminimport db
    except ImportError:
        raise ImportError(
            "`firebase_admin` package not found, please run `pip install"
            " firebase-admin`"
        )

    ref = db.reference(path)
    data = ref.get()

    documents = []

    if isinstance(data, Dict):
        for key in data:
            entry = data[key]
            extra_info = {
                "document_id": key,
            }
            if type(entry) is Dict and field in entry:
                text = entry[field]
            else:
                text = str(entry)

            document = Document(text=text, extra_info=extra_info)
            documents.append(document)
    elif isinstance(data, str):
        documents.append(Document(text=data))

    return documents

```
 |  
| --- | --- |  
options: members: - FirebaseRealtimeDatabaseReader
