# Kibela
##  KibelaReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/kibela/#llama_index.readers.kibela.KibelaReader "Permanent link")
Bases: 
Kibela reader.
Reads pages from Kibela.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `team`  |  Kibela team.  |  _required_  |  
|  `token`  |  Kibela API token.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-kibela/llama_index/readers/kibela/base.py`  
| 
```
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
```
 | 
```
classKibelaReader(BaseReader):
"""
    Kibela reader.

    Reads pages from Kibela.

    Args:
        team (str): Kibela team.
        token (str): Kibela API token.

    """

    def__init__(self, team: str, token: str) -> None:
"""Initialize with parameters."""
        fromgqlimport Client
        fromgql.transport.aiohttpimport AIOHTTPTransport

        self.url = f"https://{team}.kibe.la/api/v1"
        self.headers = {"Authorization": f"Bearer {token}"}
        transport = AIOHTTPTransport(url=self.url, headers=self.headers)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    defrequest(self, query: str, params: dict) -> Dict:
        fromgqlimport gql

        q = gql(query)
        return self.client.execute(q, variable_values=params)

    defload_data(self) -> List[Document]:
"""
        Load data from Kibela.

        Returns:
            List[Document]: List of documents.

        """
        query = """
        query getNotes($after: String) {
          notes(first: 100, after: $after) {
            totalCount
            pageInfo {
              endCursor
              startCursor
              hasNextPage

            edges {
              cursor
              node {


                title
                content




        """
        params = {"after": ""}
        has_next = True
        documents = []
        # Due to the request limit of 10 requests per second on the Kibela API, we do not process in parallel.
        # See https://github.com/kibela/kibela-api-v1-document#1%E7%A7%92%E3%81%82%E3%81%9F%E3%82%8A%E3%81%AE%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%E6%95%B0
        while has_next:
            res = self.request(query, params)
            note_conn = Connection[Note].model_validate(res["notes"])
            for note in note_conn.edges:
                doc = (
                    f"---\nurl: {note.node.url}\ntitle:"
                    f" {note.node.title}\n---\ncontent:\n{note.node.content}\n"
                )
                documents.append(Document(text=doc))
            has_next = note_conn.pageInfo.hasNextPage
            params = {"after": note_conn.pageInfo.endCursor}

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/kibela/#llama_index.readers.kibela.KibelaReader.load_data "Permanent link")

```
load_data() -> []

```

Load data from Kibela.
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-kibela/llama_index/readers/kibela/base.py`  
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
```
 | 
```
defload_data(self) -> List[Document]:
"""
    Load data from Kibela.

    Returns:
        List[Document]: List of documents.

    """
    query = """
    query getNotes($after: String) {
      notes(first: 100, after: $after) {
        totalCount
        pageInfo {
          endCursor
          startCursor
          hasNextPage

        edges {
          cursor
          node {


            title
            content




    """
    params = {"after": ""}
    has_next = True
    documents = []
    # Due to the request limit of 10 requests per second on the Kibela API, we do not process in parallel.
    # See https://github.com/kibela/kibela-api-v1-document#1%E7%A7%92%E3%81%82%E3%81%9F%E3%82%8A%E3%81%AE%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%E6%95%B0
    while has_next:
        res = self.request(query, params)
        note_conn = Connection[Note].model_validate(res["notes"])
        for note in note_conn.edges:
            doc = (
                f"---\nurl: {note.node.url}\ntitle:"
                f" {note.node.title}\n---\ncontent:\n{note.node.content}\n"
            )
            documents.append(Document(text=doc))
        has_next = note_conn.pageInfo.hasNextPage
        params = {"after": note_conn.pageInfo.endCursor}

    return documents

```
 |  
| --- | --- |  
options: members: - KibelaReader
