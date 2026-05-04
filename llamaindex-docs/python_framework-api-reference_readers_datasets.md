# Datasets
##  DatasetsReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/datasets/#llama_index.readers.datasets.DatasetsReader "Permanent link")
Bases: 
Datasets reader.
Load HuggingFace datasets as documents.
Source code in `llama-index-integrations/readers/llama-index-readers-datasets/llama_index/readers/datasets/base.py`  
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
```
 | 
```
classDatasetsReader(BaseReader):
"""
    Datasets reader.

    Load HuggingFace datasets as documents.

    """

    @staticmethod
    def_make_document(
        sample: Dict[str, Any],
        doc_id_key: Optional[str] = None,
        text_key: Optional[str] = None,
    ) -> Document:
        kwargs = {"metadata": sample}

        if doc_id_key:
            if doc_id_key not in sample:
                msg = f"Document id key '{doc_id_key}' not found."
                raise KeyError(msg)
            kwargs["id_"] = sample[doc_id_key]

        if text_key:
            if text_key not in sample:
                msg = f"Text key '{text_key}' not found."
                raise KeyError(msg)
            kwargs["text"] = sample[text_key]

        return Document(**kwargs)

    defload_data(
        self,
        *args: Any,
        dataset: Optional[Dataset] = None,
        split: Union[Split, str] = Split.TRAIN,
        doc_id_key: Optional[str] = None,
        text_key: Optional[str] = None,
        **load_kwargs: Any,
    ) -> List[Document]:
"""
        Load data from the dataset.

        Args:
            *args: Positional arguments to pass to load_dataset.
            dataset (Optional[Dataset]): The dataset to load. load_dataset is skipped if provided. Optional.
            split (Union[Split, str]): The split to load. Default: Split.TRAIN.
            doc_id_key (Optional[str]): The key of the doc_id in samples. Optional.
            text_key (Optional[str]): The key of the text in samples. Optional.
            **load_kwargs: Keyword arguments to pass to load_dataset.

        Returns:
            List[Document]: A list of documents.

        """
        if dataset is None:
            dataset = load_dataset(*args, **load_kwargs, split=split, streaming=False)

        return [
            self._make_document(sample, doc_id_key=doc_id_key, text_key=text_key)
            for sample in dataset
        ]

    deflazy_load_data(
        self,
        *args: Any,
        dataset: Optional[IterableDataset] = None,
        split: Union[Split, str] = Split.TRAIN,
        doc_id_key: Optional[str] = None,
        text_key: Optional[str] = None,
        **load_kwargs: Any,
    ) -> Iterable[Document]:
"""
        Lazily load data from the dataset.

        Args:
            *args: Positional arguments to pass to load_dataset.
            dataset (Optional[IterableDataset]): The dataset to load. load_dataset is skipped if provided. Optional.
            split (Union[Split, str]): The split to load. Default: Split.TRAIN.
            doc_id_key (Optional[str]): The key of the doc_id in samples. Optional.
            text_key (Optional[str]): The key of the text in samples. Optional.
            **load_kwargs: Keyword arguments to pass to load_dataset.

        Returns:
            List[Document]: A list of documents.

        """
        if dataset is None:
            dataset = load_dataset(*args, **load_kwargs, split=split, streaming=True)

        # Return Document generator
        return (
            self._make_document(sample, doc_id_key=doc_id_key, text_key=text_key)
            for sample in dataset
        )

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/datasets/#llama_index.readers.datasets.DatasetsReader.load_data "Permanent link")

```
load_data(
    *args: ,
    dataset: Optional[Dataset] = None,
    split: Union[Split, ] = TRAIN,
    doc_id_key: Optional[] = None,
    text_key: Optional[] = None,
    **load_kwargs: 
) -> []

```

Load data from the dataset.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `*args`  |  Positional arguments to pass to load_dataset.  |  
|  `dataset`  |  `Optional[Dataset]`  |  The dataset to load. load_dataset is skipped if provided. Optional.  |  `None`  |  
|  `split`  |  `Union[Split, str]`  |  The split to load. Default: Split.TRAIN.  |  `TRAIN`  |  
|  `doc_id_key`  |  `Optional[str]`  |  The key of the doc_id in samples. Optional.  |  `None`  |  
|  `text_key`  |  `Optional[str]`  |  The key of the text in samples. Optional.  |  `None`  |  
|  `**load_kwargs`  |  Keyword arguments to pass to load_dataset.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-datasets/llama_index/readers/datasets/base.py`  
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
```
 | 
```
defload_data(
    self,
    *args: Any,
    dataset: Optional[Dataset] = None,
    split: Union[Split, str] = Split.TRAIN,
    doc_id_key: Optional[str] = None,
    text_key: Optional[str] = None,
    **load_kwargs: Any,
) -> List[Document]:
"""
    Load data from the dataset.

    Args:
        *args: Positional arguments to pass to load_dataset.
        dataset (Optional[Dataset]): The dataset to load. load_dataset is skipped if provided. Optional.
        split (Union[Split, str]): The split to load. Default: Split.TRAIN.
        doc_id_key (Optional[str]): The key of the doc_id in samples. Optional.
        text_key (Optional[str]): The key of the text in samples. Optional.
        **load_kwargs: Keyword arguments to pass to load_dataset.

    Returns:
        List[Document]: A list of documents.

    """
    if dataset is None:
        dataset = load_dataset(*args, **load_kwargs, split=split, streaming=False)

    return [
        self._make_document(sample, doc_id_key=doc_id_key, text_key=text_key)
        for sample in dataset
    ]

```
 |  
| --- | --- |  
###  lazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/datasets/#llama_index.readers.datasets.DatasetsReader.lazy_load_data "Permanent link")

```
lazy_load_data(
    *args: ,
    dataset: Optional[IterableDataset] = None,
    split: Union[Split, ] = TRAIN,
    doc_id_key: Optional[] = None,
    text_key: Optional[] = None,
    **load_kwargs: 
) -> Iterable[]

```

Lazily load data from the dataset.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `*args`  |  Positional arguments to pass to load_dataset.  |  
|  `dataset`  |  `Optional[IterableDataset]`  |  The dataset to load. load_dataset is skipped if provided. Optional.  |  `None`  |  
|  `split`  |  `Union[Split, str]`  |  The split to load. Default: Split.TRAIN.  |  `TRAIN`  |  
|  `doc_id_key`  |  `Optional[str]`  |  The key of the doc_id in samples. Optional.  |  `None`  |  
|  `text_key`  |  `Optional[str]`  |  The key of the text in samples. Optional.  |  `None`  |  
|  `**load_kwargs`  |  Keyword arguments to pass to load_dataset.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Iterable[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]`  |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-datasets/llama_index/readers/datasets/base.py`  
| 
```
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
```
 | 
```
deflazy_load_data(
    self,
    *args: Any,
    dataset: Optional[IterableDataset] = None,
    split: Union[Split, str] = Split.TRAIN,
    doc_id_key: Optional[str] = None,
    text_key: Optional[str] = None,
    **load_kwargs: Any,
) -> Iterable[Document]:
"""
    Lazily load data from the dataset.

    Args:
        *args: Positional arguments to pass to load_dataset.
        dataset (Optional[IterableDataset]): The dataset to load. load_dataset is skipped if provided. Optional.
        split (Union[Split, str]): The split to load. Default: Split.TRAIN.
        doc_id_key (Optional[str]): The key of the doc_id in samples. Optional.
        text_key (Optional[str]): The key of the text in samples. Optional.
        **load_kwargs: Keyword arguments to pass to load_dataset.

    Returns:
        List[Document]: A list of documents.

    """
    if dataset is None:
        dataset = load_dataset(*args, **load_kwargs, split=split, streaming=True)

    # Return Document generator
    return (
        self._make_document(sample, doc_id_key=doc_id_key, text_key=text_key)
        for sample in dataset
    )

```
 |  
| --- | --- |  
options: members: - DatasetsReader
