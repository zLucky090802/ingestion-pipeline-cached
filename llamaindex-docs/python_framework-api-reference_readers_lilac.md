# Lilac
##  LilacReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/lilac/#llama_index.readers.lilac.LilacReader "Permanent link")
Bases: 
Lilac dataset reader.
Source code in `llama-index-integrations/readers/llama-index-readers-lilac/llama_index/readers/lilac/base.py`  
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
```
 | 
```
classLilacReader(BaseReader):
"""
    Lilac dataset reader.
    """

    defload_data(
        self,
        dataset: str,
        text_path: "Path" = "text",
        doc_id_path: Optional["Path"] = "doc_id",
        columns: Optional[List["ColumnId"]] = None,
        filters: Optional[List["FilterLike"]] = None,
        project_dir: Optional[str] = None,
    ) -> List[Document]:
"""
        Load text from relevant posts and top-level comments in subreddit(s), given keyword(s) for search.

        Args:
            project_dir (Optional[str]): The Lilac project dir to read from. If not defined, uses the `LILAC_PROJECT_DIR`
              environment variable.
            text_path: The path to the text field in the dataset. If not defined, uses 'text'.
            columns (Optional[List[ColumnId]]): The columns to load from the dataset. If not defined, loads all columns.
            dataset (str): The dataset to load. Should be formatted like {namespace}/{dataset_name}.
            filters (Optional[Filter]): A filter to apply to the dataset before loading into documents. Useful to filter
              for labeled data.

        """
        try:
            importlilacasll
        except ImportError:
            raise ("`lilac` package not found, please run `pip install lilac`")

        namespace, dataset_name = dataset.split("/")
        lilac_dataset = ll.get_dataset(namespace, dataset_name, project_dir=project_dir)

        # Check to make sure text path, and doc_id path are valid.
        manifest = lilac_dataset.manifest()

        text_path = ll.normalize_path(text_path)
        text_field = manifest.data_schema.get_field(text_path)
        if not text_field:
            raise ValueError(
                f"Could not find text field {text_path} in dataset {dataset}"
            )

        doc_id_path = ll.normalize_path(doc_id_path)
        doc_id_field = manifest.data_schema.get_field(doc_id_path)
        if not doc_id_field:
            raise ValueError(
                f"Could not find doc_id field {doc_id_path} in dataset {dataset}"
            )

        rows = lilac_dataset.select_rows(
            columns=([*columns, text_field, doc_id_path]) if columns else ["*"],
            filters=filters,
            combine_columns=True,
        )

        def_item_from_path(item: ll.Item, path: ll.PathTuple) -> ll.Item:
            if len(path) == 1:
                item = item[path[0]]
                if isinstance(item, dict):
                    return item[ll.VALUE_KEY]
                else:
                    return item
            else:
                return _item_from_path(item[path[0]], path[1:])

        def_remove_item_path(item: ll.Item, path: ll.PathTuple) -> None:
            if len(path) == 0:
                return
            if len(path) == 1:
                if item and path[0] in item:
                    leaf_item = item[path[0]]
                    if isinstance(leaf_item, dict):
                        del item[path[0]][ll.VALUE_KEY]
                    else:
                        del item[path[0]]
                return
            else:
                _remove_item_path(item[path[0]], path[1:])

        documents: List[Document] = []
        for row in rows:
            text = _item_from_path(row, text_path)
            doc_id = _item_from_path(row, doc_id_path)
            _remove_item_path(row, text_path)
            _remove_item_path(row, doc_id_path)
            documents.append(Document(text=text, doc_id=doc_id, extra_info=row or {}))

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/lilac/#llama_index.readers.lilac.LilacReader.load_data "Permanent link")

```
load_data(
    dataset: ,
    text_path:  = "text",
    doc_id_path: Optional[] = "doc_id",
    columns: Optional[[ColumnId]] = None,
    filters: Optional[[FilterLike]] = None,
    project_dir: Optional[] = None,
) -> []

```

Load text from relevant posts and top-level comments in subreddit(s), given keyword(s) for search.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `project_dir`  |  `Optional[str]`  |  The Lilac project dir to read from. If not defined, uses the `LILAC_PROJECT_DIR` environment variable.  |  `None`  |  
|  `text_path`  |  `Path`  |  The path to the text field in the dataset. If not defined, uses 'text'.  |  `'text'`  |  
|  `columns`  |  `Optional[List[ColumnId]]`  |  The columns to load from the dataset. If not defined, loads all columns.  |  `None`  |  
|  `dataset`  |  The dataset to load. Should be formatted like {namespace}/{dataset_name}.  |  _required_  |  
|  `filters`  |  `Optional[Filter]`  |  A filter to apply to the dataset before loading into documents. Useful to filter for labeled data.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-lilac/llama_index/readers/lilac/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    dataset: str,
    text_path: "Path" = "text",
    doc_id_path: Optional["Path"] = "doc_id",
    columns: Optional[List["ColumnId"]] = None,
    filters: Optional[List["FilterLike"]] = None,
    project_dir: Optional[str] = None,
) -> List[Document]:
"""
    Load text from relevant posts and top-level comments in subreddit(s), given keyword(s) for search.

    Args:
        project_dir (Optional[str]): The Lilac project dir to read from. If not defined, uses the `LILAC_PROJECT_DIR`
          environment variable.
        text_path: The path to the text field in the dataset. If not defined, uses 'text'.
        columns (Optional[List[ColumnId]]): The columns to load from the dataset. If not defined, loads all columns.
        dataset (str): The dataset to load. Should be formatted like {namespace}/{dataset_name}.
        filters (Optional[Filter]): A filter to apply to the dataset before loading into documents. Useful to filter
          for labeled data.

    """
    try:
        importlilacasll
    except ImportError:
        raise ("`lilac` package not found, please run `pip install lilac`")

    namespace, dataset_name = dataset.split("/")
    lilac_dataset = ll.get_dataset(namespace, dataset_name, project_dir=project_dir)

    # Check to make sure text path, and doc_id path are valid.
    manifest = lilac_dataset.manifest()

    text_path = ll.normalize_path(text_path)
    text_field = manifest.data_schema.get_field(text_path)
    if not text_field:
        raise ValueError(
            f"Could not find text field {text_path} in dataset {dataset}"
        )

    doc_id_path = ll.normalize_path(doc_id_path)
    doc_id_field = manifest.data_schema.get_field(doc_id_path)
    if not doc_id_field:
        raise ValueError(
            f"Could not find doc_id field {doc_id_path} in dataset {dataset}"
        )

    rows = lilac_dataset.select_rows(
        columns=([*columns, text_field, doc_id_path]) if columns else ["*"],
        filters=filters,
        combine_columns=True,
    )

    def_item_from_path(item: ll.Item, path: ll.PathTuple) -> ll.Item:
        if len(path) == 1:
            item = item[path[0]]
            if isinstance(item, dict):
                return item[ll.VALUE_KEY]
            else:
                return item
        else:
            return _item_from_path(item[path[0]], path[1:])

    def_remove_item_path(item: ll.Item, path: ll.PathTuple) -> None:
        if len(path) == 0:
            return
        if len(path) == 1:
            if item and path[0] in item:
                leaf_item = item[path[0]]
                if isinstance(leaf_item, dict):
                    del item[path[0]][ll.VALUE_KEY]
                else:
                    del item[path[0]]
            return
        else:
            _remove_item_path(item[path[0]], path[1:])

    documents: List[Document] = []
    for row in rows:
        text = _item_from_path(row, text_path)
        doc_id = _item_from_path(row, doc_id_path)
        _remove_item_path(row, text_path)
        _remove_item_path(row, doc_id_path)
        documents.append(Document(text=text, doc_id=doc_id, extra_info=row or {}))

    return documents

```
 |  
| --- | --- |  
options: members: - LilacReader
