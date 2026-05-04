# Couchdb
##  SimpleCouchDBReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/couchdb/#llama_index.readers.couchdb.SimpleCouchDBReader "Permanent link")
Bases: 
Simple CouchDB reader.
Concatenates each CouchDB doc into Document used by LlamaIndex.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `couchdb_url`  |  CouchDB Full URL.  |  `None`  |  
|  `max_docs`  |  Maximum number of documents to load.  |  `1000`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-couchdb/llama_index/readers/couchdb/base.py`  
| 
```
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
```
 | 
```
classSimpleCouchDBReader(BaseReader):
"""
    Simple CouchDB reader.

    Concatenates each CouchDB doc into Document used by LlamaIndex.

    Args:
        couchdb_url (str): CouchDB Full URL.
        max_docs (int): Maximum number of documents to load.

    """

    def__init__(
        self,
        user: str,
        pwd: str,
        host: str,
        port: int,
        couchdb_url: Optional[Dict] = None,
        max_docs: int = 1000,
    ) -> None:
"""Initialize with parameters."""
        if couchdb_url is not None:
            self.client = couchdb3.Server(couchdb_url)
        else:
            self.client = couchdb3.Server(f"http://{user}:{pwd}@{host}:{port}")
        self.max_docs = max_docs

    defload_data(self, db_name: str, query: Optional[str] = None) -> List[Document]:
"""
        Load data from the input directory.

        Args:
            db_name (str): name of the database.
            query (Optional[str]): query to filter documents.
                Defaults to None

        Returns:
            List[Document]: A list of documents.

        """
        documents = []
        db = self.client.get(db_name)
        if query is None:
            # if no query is specified, return all docs in database
            logging.debug("showing all docs")
            results = db.view("_all_docs", include_docs=True)
        else:
            logging.debug("executing query")
            results = db.find(query)

        if not isinstance(results, dict):
            logging.debug(results.rows)
        else:
            logging.debug(results)

        # check if more than one result
        if (
            not isinstance(results, dict)
            and hasattr(results, "rows")
            and results.rows is not None
        ):
            for row in results.rows:
                # check that the id field exists
                if "id" not in row:
                    raise ValueError("`id` field not found in CouchDB document.")
                documents.append(Document(text=json.dumps(row.doc)))
        else:
            # only one result
            if results.get("docs") is not None:
                for item in results.get("docs"):
                    # check that the _id field exists
                    if "_id" not in item:
                        raise ValueError("`_id` field not found in CouchDB document.")
                    documents.append(Document(text=json.dumps(item)))

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/couchdb/#llama_index.readers.couchdb.SimpleCouchDBReader.load_data "Permanent link")

```
load_data(
    db_name: , query: Optional[] = None
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `db_name`  |  name of the database.  |  _required_  |  
|  `query`  |  `Optional[str]`  |  query to filter documents. Defaults to None  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-couchdb/llama_index/readers/couchdb/base.py`  
| 
```
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
```
 | 
```
defload_data(self, db_name: str, query: Optional[str] = None) -> List[Document]:
"""
    Load data from the input directory.

    Args:
        db_name (str): name of the database.
        query (Optional[str]): query to filter documents.
            Defaults to None

    Returns:
        List[Document]: A list of documents.

    """
    documents = []
    db = self.client.get(db_name)
    if query is None:
        # if no query is specified, return all docs in database
        logging.debug("showing all docs")
        results = db.view("_all_docs", include_docs=True)
    else:
        logging.debug("executing query")
        results = db.find(query)

    if not isinstance(results, dict):
        logging.debug(results.rows)
    else:
        logging.debug(results)

    # check if more than one result
    if (
        not isinstance(results, dict)
        and hasattr(results, "rows")
        and results.rows is not None
    ):
        for row in results.rows:
            # check that the id field exists
            if "id" not in row:
                raise ValueError("`id` field not found in CouchDB document.")
            documents.append(Document(text=json.dumps(row.doc)))
    else:
        # only one result
        if results.get("docs") is not None:
            for item in results.get("docs"):
                # check that the _id field exists
                if "_id" not in item:
                    raise ValueError("`_id` field not found in CouchDB document.")
                documents.append(Document(text=json.dumps(item)))

    return documents

```
 |  
| --- | --- |  
options: members: - SimpleCouchDBReader
