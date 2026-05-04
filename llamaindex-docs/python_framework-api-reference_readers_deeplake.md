# Deeplake
##  DeepLakeReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/deeplake/#llama_index.readers.deeplake.DeepLakeReader "Permanent link")
Bases: 
DeepLake reader.
Retrieve documents from existing DeepLake datasets.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `dataset_name`  |  Name of the deeplake dataset.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-deeplake/llama_index/readers/deeplake/base.py`  
| 
```
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
```
 | 
```
classDeepLakeReader(BaseReader):
"""
    DeepLake reader.

    Retrieve documents from existing DeepLake datasets.

    Args:
        dataset_name: Name of the deeplake dataset.

    """

    def__init__(
        self,
        token: Optional[str] = None,
    ):
"""Initializing the deepLake reader."""
        import_err_msg = (
            "`deeplake` package not found, please run `pip install deeplake`"
        )
        try:
            importdeeplake  # noqa
        except ImportError:
            raise ImportError(import_err_msg)
        self.token = token

    defload_data(
        self,
        query_vector: List[float],
        dataset_path: str,
        limit: int = 4,
        distance_metric: str = "l2",
    ) -> List[Document]:
"""
        Load data from DeepLake.

        Args:
            dataset_name (str): Name of the DeepLake dataset.
            query_vector (List[float]): Query vector.
            limit (int): Number of results to return.

        Returns:
            List[Document]: A list of documents.

        """
        importdeeplake
        fromdeeplake.util.exceptionsimport TensorDoesNotExistError

        dataset = deeplake.load(dataset_path, token=self.token)

        try:
            embeddings = dataset.embedding.numpy(fetch_chunks=True)
        except Exception:
            raise TensorDoesNotExistError("embedding")

        indices = vector_search(
            query_vector, embeddings, distance_metric=distance_metric, limit=limit
        )

        documents = []
        for idx in indices:
            document = Document(
                text=str(dataset[idx].text.numpy().tolist()[0]),
                id_=dataset[idx].ids.numpy().tolist()[0],
            )

            documents.append(document)

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/deeplake/#llama_index.readers.deeplake.DeepLakeReader.load_data "Permanent link")

```
load_data(
    query_vector: [float],
    dataset_path: ,
    limit:  = 4,
    distance_metric:  = "l2",
) -> []

```

Load data from DeepLake.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `dataset_name`  |  Name of the DeepLake dataset.  |  _required_  |  
|  `query_vector`  |  `List[float]`  |  Query vector.  |  _required_  |  
|  `limit`  |  Number of results to return.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-deeplake/llama_index/readers/deeplake/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    query_vector: List[float],
    dataset_path: str,
    limit: int = 4,
    distance_metric: str = "l2",
) -> List[Document]:
"""
    Load data from DeepLake.

    Args:
        dataset_name (str): Name of the DeepLake dataset.
        query_vector (List[float]): Query vector.
        limit (int): Number of results to return.

    Returns:
        List[Document]: A list of documents.

    """
    importdeeplake
    fromdeeplake.util.exceptionsimport TensorDoesNotExistError

    dataset = deeplake.load(dataset_path, token=self.token)

    try:
        embeddings = dataset.embedding.numpy(fetch_chunks=True)
    except Exception:
        raise TensorDoesNotExistError("embedding")

    indices = vector_search(
        query_vector, embeddings, distance_metric=distance_metric, limit=limit
    )

    documents = []
    for idx in indices:
        document = Document(
            text=str(dataset[idx].text.numpy().tolist()[0]),
            id_=dataset[idx].ids.numpy().tolist()[0],
        )

        documents.append(document)

    return documents

```
 |  
| --- | --- |  
options: members: - DeepLakeReader
