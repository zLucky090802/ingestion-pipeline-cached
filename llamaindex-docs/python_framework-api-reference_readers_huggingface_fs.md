# Huggingface fs
Init params.
##  HuggingFaceFSReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/huggingface_fs/#llama_index.readers.huggingface_fs.HuggingFaceFSReader "Permanent link")
Bases: 
Hugging Face File System reader.
Uses the new Filesystem API from the Hugging Face Hub client library.
Source code in `llama-index-integrations/readers/llama-index-readers-huggingface-fs/llama_index/readers/huggingface_fs/base.py`  
| 
```
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
```
 | 
```
classHuggingFaceFSReader(BaseReader):
"""
    Hugging Face File System reader.

    Uses the new Filesystem API from the Hugging Face Hub client library.
    """

    def__init__(self) -> None:
        fromhuggingface_hubimport HfFileSystem

        self.fs = HfFileSystem()

    defload_dicts(self, path: str) -> List[Dict]:
"""Parse file."""
        test_data = self.fs.read_bytes(path)

        path = Path(path)
        if ".gz" in path.suffixes:
            importgzip

            with TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                with open(tmp / "tmp.jsonl.gz", "wb") as fp:
                    fp.write(test_data)

                f = gzip.open(tmp / "tmp.jsonl.gz", "rb")
                raw = f.read()
                data = raw.decode()
        else:
            data = test_data.decode()

        text_lines = data.split("\n")
        json_dicts = []
        for t in text_lines:
            try:
                json_dict = json.loads(t)
            except json.decoder.JSONDecodeError:
                continue
            json_dicts.append(json_dict)
        return json_dicts

    defload_df(self, path: str) -> pd.DataFrame:
"""Load pandas dataframe."""
        return pd.DataFrame(self.load_dicts(path))

    defload_data(self, path: str) -> List[Document]:
"""Load data."""
        json_dicts = self.load_dicts(path)
        docs = []
        for d in json_dicts:
            docs.append(Document(text=str(d)))
        return docs

```
 |  
| --- | --- |  
###  load_dicts [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/huggingface_fs/#llama_index.readers.huggingface_fs.HuggingFaceFSReader.load_dicts "Permanent link")

```
load_dicts(path: ) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-huggingface-fs/llama_index/readers/huggingface_fs/base.py`  
| 
```
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
```
 | 
```
defload_dicts(self, path: str) -> List[Dict]:
"""Parse file."""
    test_data = self.fs.read_bytes(path)

    path = Path(path)
    if ".gz" in path.suffixes:
        importgzip

        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            with open(tmp / "tmp.jsonl.gz", "wb") as fp:
                fp.write(test_data)

            f = gzip.open(tmp / "tmp.jsonl.gz", "rb")
            raw = f.read()
            data = raw.decode()
    else:
        data = test_data.decode()

    text_lines = data.split("\n")
    json_dicts = []
    for t in text_lines:
        try:
            json_dict = json.loads(t)
        except json.decoder.JSONDecodeError:
            continue
        json_dicts.append(json_dict)
    return json_dicts

```
 |  
| --- | --- |  
###  load_df [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/huggingface_fs/#llama_index.readers.huggingface_fs.HuggingFaceFSReader.load_df "Permanent link")

```
load_df(path: ) -> DataFrame

```

Load pandas dataframe.
Source code in `llama-index-integrations/readers/llama-index-readers-huggingface-fs/llama_index/readers/huggingface_fs/base.py`  
| 
```
59
60
61
```
 | 
```
defload_df(self, path: str) -> pd.DataFrame:
"""Load pandas dataframe."""
    return pd.DataFrame(self.load_dicts(path))

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/huggingface_fs/#llama_index.readers.huggingface_fs.HuggingFaceFSReader.load_data "Permanent link")

```
load_data(path: ) -> []

```

Load data.
Source code in `llama-index-integrations/readers/llama-index-readers-huggingface-fs/llama_index/readers/huggingface_fs/base.py`  
| 
```
63
64
65
66
67
68
69
```
 | 
```
defload_data(self, path: str) -> List[Document]:
"""Load data."""
    json_dicts = self.load_dicts(path)
    docs = []
    for d in json_dicts:
        docs.append(Document(text=str(d)))
    return docs

```
 |  
| --- | --- |  
options: members: - HuggingFaceFSReader
