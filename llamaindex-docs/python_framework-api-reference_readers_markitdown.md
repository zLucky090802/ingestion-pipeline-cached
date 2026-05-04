# Markitdown
##  MarkItDownReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/markitdown/#llama_index.readers.markitdown.MarkItDownReader "Permanent link")
Bases: 
MarkItDownReader is a document reader that utilizes the MarkItDown parser to convert files or collections of files into Document objects.
#### Methods[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/markitdown/#llama_index.readers.markitdown.MarkItDownReader--methods "Permanent link")
load_data(file_path: str | Path | Iterable[str] | Iterable[Path]) -> List[Document] Loads and parses a directory (if `file_path` is `str` or `Path`) or a list of files specified by `file_path` using the MarkItDown parser. Returns a list of Document objects, each containing the text content and metadata such as file path, file type, and content length.
Source code in `llama-index-integrations/readers/llama-index-readers-markitdown/llama_index/readers/markitdown/base.py`  
| 
```
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
121
122
123
124
125
126
127
128
129
130
131
```
 | 
```
classMarkItDownReader(BaseReader):
"""
    MarkItDownReader is a document reader that utilizes the MarkItDown parser to convert files or collections of files into Document objects.

    Methods
    -------
    load_data(file_path: str | Path | Iterable[str] | Iterable[Path]) -> List[Document]
        Loads and parses a directory (if `file_path` is `str` or `Path`) or a list of files specified by `file_path` using the MarkItDown parser.
        Returns a list of Document objects, each containing the text content and metadata such as file path, file type, and content length.

    """

    _reader: MarkItDown = MarkItDown()

    @classmethod
    defclass_name(cls) -> str:
"""Get the name identifier of the class."""
        return "MarkItDownReader"

    defload_data(
        self,
        file_path: Union[str, Path, List[str], List[Path]],
        **kwargs,
    ) -> List[Document]:
        docs: List[Document] = []
        fl_pt = ValidFilePath(file_path=file_path)
        fs = fl_pt.file_path

        for f in fs:
            res = self._reader.convert(f)
            docs.append(
                Document(
                    text=res.text_content,
                    metadata={
                        "file_path": f.__str__(),
                        "file_type": os.path.splitext(f)[1],
                        "content_length": len(res.text_content),
                    },
                )
            )

        return docs

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/markitdown/#llama_index.readers.markitdown.MarkItDownReader.class_name "Permanent link")

```
class_name() -> 

```

Get the name identifier of the class.
Source code in `llama-index-integrations/readers/llama-index-readers-markitdown/llama_index/readers/markitdown/base.py`  
| 
```
104
105
106
107
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get the name identifier of the class."""
    return "MarkItDownReader"

```
 |  
| --- | --- |  
options: members: - OpenMap
