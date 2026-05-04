# Igpt email
##  IGPTEmailReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/igpt_email/#llama_index.readers.igpt_email.IGPTEmailReader "Permanent link")
Bases: 
iGPT Email Intelligence Reader.
Loads structured, reasoning-ready email context from the iGPT API as LlamaIndex Documents for indexing and retrieval.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  iGPT API key. See https://docs.igpt.ai for details.  |  _required_  |  
|  `user`  |  User identifier for the connected mailbox.  |  _required_  |  
Example
.. code-block:: python

```
from llama_index.readers.igpt_email import IGPTEmailReader
from llama_index.core import VectorStoreIndex

reader = IGPTEmailReader(api_key="your-key", user="user-id")
documents = reader.load_data(
    query="project Alpha", date_from="2025-01-01"
)
index = VectorStoreIndex.from_documents(documents)

```
Source code in `llama-index-integrations/readers/llama-index-readers-igpt-email/llama_index/readers/igpt_email/base.py`  
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
```
 | 
```
classIGPTEmailReader(BaseReader):
"""
    iGPT Email Intelligence Reader.

    Loads structured, reasoning-ready email context from the iGPT API as
    LlamaIndex Documents for indexing and retrieval.

    Args:
        api_key (str): iGPT API key. See https://docs.igpt.ai for details.
        user (str): User identifier for the connected mailbox.

    Example:
        .. code-block:: python

            from llama_index.readers.igpt_email import IGPTEmailReader
            from llama_index.core import VectorStoreIndex

            reader = IGPTEmailReader(api_key="your-key", user="user-id")
            documents = reader.load_data(
                query="project Alpha", date_from="2025-01-01"

            index = VectorStoreIndex.from_documents(documents)

    """

    def__init__(self, api_key: str, user: str) -> None:
"""Initialize with parameters."""
        super().__init__()
        self.client = IGPT(api_key=api_key, user=user)

    defload_data(
        self,
        query: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        max_results: int = 50,
    ) -> List[Document]:
"""
        Load email context as Documents from iGPT recall.search().

        Each result from the iGPT API is returned as a separate Document.
        Thread metadata (subject, participants, date, thread ID) is preserved
        in metadata for filtering and attribution during retrieval.

        Args:
            query (str): Search query to run against connected email data.
            date_from (str, optional): Filter results from this date (YYYY-MM-DD).
            date_to (str, optional): Filter results up to this date (YYYY-MM-DD).
            max_results (int): Maximum number of results to return. Default is 50.

        Returns:
            List[Document]: One Document per email result, ready for indexing.
                Thread metadata is stored in metadata (subject, from, to,
                date, thread_id, id).

        """
        response = self.client.recall.search(
            query=query,
            date_from=date_from,
            date_to=date_to,
            max_results=max_results,
        )

        if isinstance(response, dict) and "error" in response:
            raise ValueError(f"iGPT API error: {response['error']}")

        if not response:
            return []

        results = (
            response if isinstance(response, list) else response.get("results", [])
        )

        documents = []
        for item in results:
            if isinstance(item, dict):
                text = item.get("content", item.get("body", json.dumps(item)))
                metadata = {
                    "source": "igpt_email",
                    "subject": item.get("subject"),
                    "from": item.get("from"),
                    "to": item.get("to"),
                    "date": item.get("date"),
                    "thread_id": item.get("thread_id"),
                    "id": item.get("id"),
                }
            else:
                text = str(item)
                metadata = {"source": "igpt_email"}

            documents.append(Document(text=text, metadata=metadata))

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/igpt_email/#llama_index.readers.igpt_email.IGPTEmailReader.load_data "Permanent link")

```
load_data(
    query: ,
    date_from: Optional[] = None,
    date_to: Optional[] = None,
    max_results:  = 50,
) -> []

```

Load email context as Documents from iGPT recall.search().
Each result from the iGPT API is returned as a separate Document. Thread metadata (subject, participants, date, thread ID) is preserved in metadata for filtering and attribution during retrieval.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Search query to run against connected email data.  |  _required_  |  
|  `date_from`  |  Filter results from this date (YYYY-MM-DD).  |  `None`  |  
|  `date_to`  |  Filter results up to this date (YYYY-MM-DD).  |  `None`  |  
|  `max_results`  |  Maximum number of results to return. Default is 50.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: One Document per email result, ready for indexing. Thread metadata is stored in metadata (subject, from, to, date, thread_id, id).  |  
Source code in `llama-index-integrations/readers/llama-index-readers-igpt-email/llama_index/readers/igpt_email/base.py`  
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
```
 | 
```
defload_data(
    self,
    query: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    max_results: int = 50,
) -> List[Document]:
"""
    Load email context as Documents from iGPT recall.search().

    Each result from the iGPT API is returned as a separate Document.
    Thread metadata (subject, participants, date, thread ID) is preserved
    in metadata for filtering and attribution during retrieval.

    Args:
        query (str): Search query to run against connected email data.
        date_from (str, optional): Filter results from this date (YYYY-MM-DD).
        date_to (str, optional): Filter results up to this date (YYYY-MM-DD).
        max_results (int): Maximum number of results to return. Default is 50.

    Returns:
        List[Document]: One Document per email result, ready for indexing.
            Thread metadata is stored in metadata (subject, from, to,
            date, thread_id, id).

    """
    response = self.client.recall.search(
        query=query,
        date_from=date_from,
        date_to=date_to,
        max_results=max_results,
    )

    if isinstance(response, dict) and "error" in response:
        raise ValueError(f"iGPT API error: {response['error']}")

    if not response:
        return []

    results = (
        response if isinstance(response, list) else response.get("results", [])
    )

    documents = []
    for item in results:
        if isinstance(item, dict):
            text = item.get("content", item.get("body", json.dumps(item)))
            metadata = {
                "source": "igpt_email",
                "subject": item.get("subject"),
                "from": item.get("from"),
                "to": item.get("to"),
                "date": item.get("date"),
                "thread_id": item.get("thread_id"),
                "id": item.get("id"),
            }
        else:
            text = str(item)
            metadata = {"source": "igpt_email"}

        documents.append(Document(text=text, metadata=metadata))

    return documents

```
 |  
| --- | --- |  
options: members: - IGPTEmailReader
