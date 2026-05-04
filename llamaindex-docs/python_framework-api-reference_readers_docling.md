# Docling
##  DoclingReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docling/#llama_index.readers.docling.DoclingReader "Permanent link")
Bases: 
Docling Reader.
Extracts PDF, DOCX, and other document formats into LlamaIndex Documents as either Markdown or JSON-serialized Docling native format.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `export_type`  |  `Literal[markdown, json]`  |  The type to export to. Defaults to "markdown".  |  _required_  |  
|  `doc_converter`  |  `DocumentConverter`  |  The Docling converter to use. Default factory: `DocumentConverter`.  |  _required_  |  
|  `md_export_kwargs`  |  `Dict[str, Any]`  |  Kwargs to use in case of markdown export. Defaults to `{"image_placeholder": ""}`.  |  _required_  |  
|  `id_func`  |  (DocIDGenCallable, optional): Doc ID generation function to use. Default: `_uuid4_doc_id_gen`  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-docling/llama_index/readers/docling/base.py`  
| 
```
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
```
 | 
```
classDoclingReader(BasePydanticReader):
"""
    Docling Reader.

    Extracts PDF, DOCX, and other document formats into LlamaIndex Documents as either Markdown or JSON-serialized Docling native format.

    Args:
        export_type (Literal["markdown", "json"], optional): The type to export to. Defaults to "markdown".
        doc_converter (DocumentConverter, optional): The Docling converter to use. Default factory: `DocumentConverter`.
        md_export_kwargs (Dict[str, Any], optional): Kwargs to use in case of markdown export. Defaults to `{"image_placeholder": ""}`.
        id_func: (DocIDGenCallable, optional): Doc ID generation function to use. Default: `_uuid4_doc_id_gen`

    """

    classExportType(str, Enum):
        MARKDOWN = "markdown"
        JSON = "json"

    @runtime_checkable
    classDocIDGenCallable(Protocol):
        def__call__(self, doc: DLDocument, file_path: str | Path) -> str: ...

    @staticmethod
    def_uuid4_doc_id_gen(doc: DLDocument, file_path: str | Path) -> str:
        return str(uuid.uuid4())

    export_type: ExportType = ExportType.MARKDOWN
    doc_converter: DocumentConverter = Field(default_factory=DocumentConverter)
    md_export_kwargs: Dict[str, Any] = {"image_placeholder": ""}
    id_func: DocIDGenCallable = _uuid4_doc_id_gen

    deflazy_load_data(
        self,
        file_path: str | Path | Iterable[str] | Iterable[Path],
        extra_info: dict | None = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> Iterable[LIDocument]:
"""
        Lazily load from given source.

        Args:
            file_path (str | Path | Iterable[str] | Iterable[Path]): Document file source as single str (URL or local file) or pathlib.Path — or iterable thereof
            extra_info (dict | None, optional): Any pre-existing metadata to include. Defaults to None.

        Returns:
            Iterable[LIDocument]: Iterable over the created LlamaIndex documents.

        """
        file_paths = (
            file_path
            if isinstance(file_path, Iterable) and not isinstance(file_path, str)
            else [file_path]
        )

        for source in file_paths:
            dl_doc = self.doc_converter.convert(source).document
            text: str
            if self.export_type == self.ExportType.MARKDOWN:
                text = dl_doc.export_to_markdown(**self.md_export_kwargs)
            elif self.export_type == self.ExportType.JSON:
                text = json.dumps(dl_doc.export_to_dict())
            else:
                raise ValueError(f"Unexpected export type: {self.export_type}")
            li_doc = LIDocument(
                doc_id=self.id_func(doc=dl_doc, file_path=source),
                text=text,
            )
            li_doc.metadata = extra_info or {}
            yield li_doc

```
 |  
| --- | --- |  
###  lazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docling/#llama_index.readers.docling.DoclingReader.lazy_load_data "Permanent link")

```
lazy_load_data(
    file_path:  |  | Iterable[] | Iterable[],
    extra_info:  | None = None,
    fs: Optional[AbstractFileSystem] = None,
) -> Iterable[]

```

Lazily load from given source.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_path`  |  `str | Path | Iterable[str] | Iterable[Path]`  |  Document file source as single str (URL or local file) or pathlib.Path — or iterable thereof  |  _required_  |  
|  `extra_info`  |  `dict | None`  |  Any pre-existing metadata to include. Defaults to None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Iterable[Document[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document "Document \(llama_index.core.Document\)")]`  |  Iterable[LIDocument]: Iterable over the created LlamaIndex documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-docling/llama_index/readers/docling/base.py`  
| 
```
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
```
 | 
```
deflazy_load_data(
    self,
    file_path: str | Path | Iterable[str] | Iterable[Path],
    extra_info: dict | None = None,
    fs: Optional[AbstractFileSystem] = None,
) -> Iterable[LIDocument]:
"""
    Lazily load from given source.

    Args:
        file_path (str | Path | Iterable[str] | Iterable[Path]): Document file source as single str (URL or local file) or pathlib.Path — or iterable thereof
        extra_info (dict | None, optional): Any pre-existing metadata to include. Defaults to None.

    Returns:
        Iterable[LIDocument]: Iterable over the created LlamaIndex documents.

    """
    file_paths = (
        file_path
        if isinstance(file_path, Iterable) and not isinstance(file_path, str)
        else [file_path]
    )

    for source in file_paths:
        dl_doc = self.doc_converter.convert(source).document
        text: str
        if self.export_type == self.ExportType.MARKDOWN:
            text = dl_doc.export_to_markdown(**self.md_export_kwargs)
        elif self.export_type == self.ExportType.JSON:
            text = json.dumps(dl_doc.export_to_dict())
        else:
            raise ValueError(f"Unexpected export type: {self.export_type}")
        li_doc = LIDocument(
            doc_id=self.id_func(doc=dl_doc, file_path=source),
            text=text,
        )
        li_doc.metadata = extra_info or {}
        yield li_doc

```
 |  
| --- | --- |  
options: members: - DoclingReader
