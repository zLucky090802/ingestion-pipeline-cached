# Mbox
##  MboxReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mbox/#llama_index.readers.mbox.MboxReader "Permanent link")
Bases: 
Mbox e-mail reader.
Reads a set of e-mails saved in the mbox format.
Source code in `llama-index-integrations/readers/llama-index-readers-mbox/llama_index/readers/mbox/base.py`  
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
```
 | 
```
classMboxReader(BaseReader):
"""
    Mbox e-mail reader.

    Reads a set of e-mails saved in the mbox format.
    """

    def__init__(self) -> None:
"""Initialize."""

    defload_data(self, input_dir: str, **load_kwargs: Any) -> List[Document]:
"""
        Load data from the input directory.

        load_kwargs:
            max_count (int): Maximum amount of messages to read.
            message_format (str): Message format overriding default.
        """
        docs: List[Document] = []
        for dirpath, dirnames, filenames in os.walk(input_dir):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for filename in filenames:
                if filename.endswith(".mbox"):
                    filepath = os.path.join(dirpath, filename)
                    file_docs = MboxFileReader(**load_kwargs).load_data(Path(filepath))
                    docs.extend(file_docs)
        return docs

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mbox/#llama_index.readers.mbox.MboxReader.load_data "Permanent link")

```
load_data(
    input_dir: , **load_kwargs: 
) -> []

```

Load data from the input directory.
load_kwargs
max_count (int): Maximum amount of messages to read. message_format (str): Message format overriding default.
Source code in `llama-index-integrations/readers/llama-index-readers-mbox/llama_index/readers/mbox/base.py`  
| 
```
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
```
 | 
```
defload_data(self, input_dir: str, **load_kwargs: Any) -> List[Document]:
"""
    Load data from the input directory.

    load_kwargs:
        max_count (int): Maximum amount of messages to read.
        message_format (str): Message format overriding default.
    """
    docs: List[Document] = []
    for dirpath, dirnames, filenames in os.walk(input_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for filename in filenames:
            if filename.endswith(".mbox"):
                filepath = os.path.join(dirpath, filename)
                file_docs = MboxFileReader(**load_kwargs).load_data(Path(filepath))
                docs.extend(file_docs)
    return docs

```
 |  
| --- | --- |  
options: members: - MboxReader
