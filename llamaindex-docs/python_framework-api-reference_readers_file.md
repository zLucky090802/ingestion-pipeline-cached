# File
##  DocxReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.DocxReader "Permanent link")
Bases: 
Docx parser.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/docs/base.py`  
| 
```
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
132
133
```
 | 
```
classDocxReader(BaseReader):
"""Docx parser."""

    defload_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""Parse file."""
        if not isinstance(file, Path):
            file = Path(file)

        try:
            importdocx2txt
        except ImportError:
            raise ImportError(
                "docx2txt is required to read Microsoft Word files: "
                "`pip install docx2txt`"
            )

        if fs:
            with fs.open(str(file)) as f:
                text = docx2txt.process(f)
        else:
            text = docx2txt.process(file)
        metadata = {"file_name": file.name}
        if extra_info is not None:
            metadata.update(extra_info)

        return [Document(text=text, metadata=metadata or {})]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.DocxReader.load_data "Permanent link")

```
load_data(
    file: ,
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/docs/base.py`  
| 
```
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
132
133
```
 | 
```
defload_data(
    self,
    file: Path,
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""Parse file."""
    if not isinstance(file, Path):
        file = Path(file)

    try:
        importdocx2txt
    except ImportError:
        raise ImportError(
            "docx2txt is required to read Microsoft Word files: "
            "`pip install docx2txt`"
        )

    if fs:
        with fs.open(str(file)) as f:
            text = docx2txt.process(f)
    else:
        text = docx2txt.process(file)
    metadata = {"file_name": file.name}
    if extra_info is not None:
        metadata.update(extra_info)

    return [Document(text=text, metadata=metadata or {})]

```
 |  
| --- | --- |  
##  HWPReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.HWPReader "Permanent link")
Bases: 
Hwp Parser.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/docs/base.py`  
| 
```
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
```
 | 
```
classHWPReader(BaseReader):
"""Hwp Parser."""

    def__init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.FILE_HEADER_SECTION = "FileHeader"
        self.HWP_SUMMARY_SECTION = "\x05HwpSummaryInformation"
        self.SECTION_NAME_LENGTH = len("Section")
        self.BODYTEXT_SECTION = "BodyText"
        self.HWP_TEXT_TAGS = [67]
        self.text = ""

    defload_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""
        Load data and extract table from Hwp file.

        Args:
            file (Path): Path for the Hwp file.

        Returns:
            List[Document]

        """
        importolefile

        if fs:
            logger.warning(
                "fs was specified but HWPReader doesn't support loading "
                "from fsspec filesystems. Will load from local filesystem instead."
            )

        if not isinstance(file, Path):
            file = Path(file)
        load_file = olefile.OleFileIO(file)
        file_dir = load_file.listdir()
        if self.is_valid(file_dir) is False:
            raise Exception("Not Valid HwpFile")

        result_text = self._get_text(load_file, file_dir)
        result = self._text_to_document(text=result_text, extra_info=extra_info)
        return [result]

    defis_valid(self, dirs: List[str]) -> bool:
        if [self.FILE_HEADER_SECTION] not in dirs:
            return False

        return [self.HWP_SUMMARY_SECTION] in dirs

    defget_body_sections(self, dirs: List[str]) -> List[str]:
        m = []
        for d in dirs:
            if d[0] == self.BODYTEXT_SECTION:
                m.append(int(d[1][self.SECTION_NAME_LENGTH :]))

        return ["BodyText/Section" + str(x) for x in sorted(m)]

    def_text_to_document(
        self, text: str, extra_info: Optional[Dict] = None
    ) -> Document:
        return Document(text=text, extra_info=extra_info or {})

    defget_text(self) -> str:
        return self.text

        # 전체 text 추출

    def_get_text(self, load_file: Any, file_dirs: List[str]) -> str:
        sections = self.get_body_sections(file_dirs)
        text = ""
        for section in sections:
            text += self.get_text_from_section(load_file, section)
            text += "\n"

        self.text = text
        return self.text

    defis_compressed(self, load_file: Any) -> bool:
        header = load_file.openstream("FileHeader")
        header_data = header.read()
        return (header_data[36]  1) == 1

    defget_text_from_section(self, load_file: Any, section: str) -> str:
        bodytext = load_file.openstream(section)
        data = bodytext.read()

        unpacked_data = (
            zlib.decompress(data, -15) if self.is_compressed(load_file) else data
        )
        size = len(unpacked_data)

        i = 0

        text = ""
        while i  size:
            header = struct.unpack_from("<I", unpacked_data, i)[0]
            rec_type = header  0x3FF
            (header  10)  0x3FF
            rec_len = (header  20)  0xFFF

            if rec_type in self.HWP_TEXT_TAGS:
                rec_data = unpacked_data[i + 4 : i + 4 + rec_len]
                text += rec_data.decode("utf-16")
                text += "\n"

            i += 4 + rec_len

        return text

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.HWPReader.load_data "Permanent link")

```
load_data(
    file: ,
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Load data and extract table from Hwp file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file`  |  `Path`  |  Path for the Hwp file.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]  |  
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/docs/base.py`  
| 
```
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
```
 | 
```
defload_data(
    self,
    file: Path,
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""
    Load data and extract table from Hwp file.

    Args:
        file (Path): Path for the Hwp file.

    Returns:
        List[Document]

    """
    importolefile

    if fs:
        logger.warning(
            "fs was specified but HWPReader doesn't support loading "
            "from fsspec filesystems. Will load from local filesystem instead."
        )

    if not isinstance(file, Path):
        file = Path(file)
    load_file = olefile.OleFileIO(file)
    file_dir = load_file.listdir()
    if self.is_valid(file_dir) is False:
        raise Exception("Not Valid HwpFile")

    result_text = self._get_text(load_file, file_dir)
    result = self._text_to_document(text=result_text, extra_info=extra_info)
    return [result]

```
 |  
| --- | --- |  
##  PDFReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PDFReader "Permanent link")
Bases: 
PDF parser.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/docs/base.py`  
| 
```
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
```
 | 
```
classPDFReader(BaseReader):
"""PDF parser."""

    def__init__(self, return_full_document: Optional[bool] = False) -> None:
"""
        Initialize PDFReader.
        """
        self.return_full_document = return_full_document

    @retry(
        stop=stop_after_attempt(RETRY_TIMES),
    )
    defload_data(
        self,
        file: Union[Path, PurePosixPath],
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""Parse file."""
        fs = fs or get_default_fs()
        _Path = Path if is_default_fs(fs) else PurePosixPath
        if not isinstance(file, (Path, PurePosixPath)):
            file = _Path(file)

        try:
            importpypdf
        except ImportError:
            raise ImportError(
                "pypdf is required to read PDF files: `pip install pypdf`"
            )

        with fs.open(str(file), "rb") as fp:
            # Load the file in memory if the filesystem is not the default one to avoid
            # issues with pypdf
            stream = fp if is_default_fs(fs) else io.BytesIO(fp.read())

            # Create a PDF object
            pdf = pypdf.PdfReader(stream)

            # Get the number of pages in the PDF document
            num_pages = len(pdf.pages)

            docs = []

            # This block returns a whole PDF as a single Document
            if self.return_full_document:
                metadata = {"file_name": file.name}
                if extra_info is not None:
                    metadata.update(extra_info)

                # Join text extracted from each page
                text = "\n".join(
                    pdf.pages[page].extract_text() for page in range(num_pages)
                )

                docs.append(Document(text=text, metadata=metadata))

            # This block returns each page of a PDF as its own Document
            else:
                # Iterate over every page

                for page in range(num_pages):
                    # Extract the text from the page
                    page_text = pdf.pages[page].extract_text()
                    page_label = pdf.page_labels[page]

                    metadata = {"page_label": page_label, "file_name": file.name}
                    if extra_info is not None:
                        metadata.update(extra_info)

                    docs.append(Document(text=page_text, metadata=metadata))

            return docs

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PDFReader.load_data "Permanent link")

```
load_data(
    file: Union[, PurePosixPath],
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/docs/base.py`  
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
```
 | 
```
@retry(
    stop=stop_after_attempt(RETRY_TIMES),
)
defload_data(
    self,
    file: Union[Path, PurePosixPath],
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""Parse file."""
    fs = fs or get_default_fs()
    _Path = Path if is_default_fs(fs) else PurePosixPath
    if not isinstance(file, (Path, PurePosixPath)):
        file = _Path(file)

    try:
        importpypdf
    except ImportError:
        raise ImportError(
            "pypdf is required to read PDF files: `pip install pypdf`"
        )

    with fs.open(str(file), "rb") as fp:
        # Load the file in memory if the filesystem is not the default one to avoid
        # issues with pypdf
        stream = fp if is_default_fs(fs) else io.BytesIO(fp.read())

        # Create a PDF object
        pdf = pypdf.PdfReader(stream)

        # Get the number of pages in the PDF document
        num_pages = len(pdf.pages)

        docs = []

        # This block returns a whole PDF as a single Document
        if self.return_full_document:
            metadata = {"file_name": file.name}
            if extra_info is not None:
                metadata.update(extra_info)

            # Join text extracted from each page
            text = "\n".join(
                pdf.pages[page].extract_text() for page in range(num_pages)
            )

            docs.append(Document(text=text, metadata=metadata))

        # This block returns each page of a PDF as its own Document
        else:
            # Iterate over every page

            for page in range(num_pages):
                # Extract the text from the page
                page_text = pdf.pages[page].extract_text()
                page_label = pdf.page_labels[page]

                metadata = {"page_label": page_label, "file_name": file.name}
                if extra_info is not None:
                    metadata.update(extra_info)

                docs.append(Document(text=page_text, metadata=metadata))

        return docs

```
 |  
| --- | --- |  
##  EpubReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.EpubReader "Permanent link")
Bases: 
Epub Parser.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/epub/base.py`  
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
```
 | 
```
classEpubReader(BaseReader):
"""Epub Parser."""

    defload_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""Parse file."""
        try:
            importebooklib
            importhtml2text
            fromebooklibimport epub
        except ImportError:
            raise ImportError(
                "Please install extra dependencies that are required for "
                "the EpubReader: "
                "`pip install EbookLib html2text`"
            )
        if fs:
            logger.warning(
                "fs was specified but EpubReader doesn't support loading "
                "from fsspec filesystems. Will load from local filesystem instead."
            )

        text_list = []
        book = epub.read_epub(file, options={"ignore_ncx": True})

        # Iterate through all chapters.
        for item in book.get_items():
            # Chapters are typically located in epub documents items.
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                text_list.append(
                    html2text.html2text(item.get_content().decode("utf-8"))
                )

        text = "\n".join(text_list)
        return [Document(text=text, metadata=extra_info or {})]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.EpubReader.load_data "Permanent link")

```
load_data(
    file: ,
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/epub/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    file: Path,
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""Parse file."""
    try:
        importebooklib
        importhtml2text
        fromebooklibimport epub
    except ImportError:
        raise ImportError(
            "Please install extra dependencies that are required for "
            "the EpubReader: "
            "`pip install EbookLib html2text`"
        )
    if fs:
        logger.warning(
            "fs was specified but EpubReader doesn't support loading "
            "from fsspec filesystems. Will load from local filesystem instead."
        )

    text_list = []
    book = epub.read_epub(file, options={"ignore_ncx": True})

    # Iterate through all chapters.
    for item in book.get_items():
        # Chapters are typically located in epub documents items.
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text_list.append(
                html2text.html2text(item.get_content().decode("utf-8"))
            )

    text = "\n".join(text_list)
    return [Document(text=text, metadata=extra_info or {})]

```
 |  
| --- | --- |  
##  FlatReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.FlatReader "Permanent link")
Bases: 
Flat reader.
Extract raw text from a file and save the file type in the metadata
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/flat/base.py`  
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
```
 | 
```
classFlatReader(BaseReader):
"""
    Flat reader.

    Extract raw text from a file and save the file type in the metadata
    """

    def__init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__(*args, **kwargs)

    def_get_fs(
        self, file: Path, fs: Optional[AbstractFileSystem] = None
    ) -> AbstractFileSystem:
        if fs is None:
            fs = LocalFileSystem()
        return fs

    defload_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""Parse file into string."""
        fs = self._get_fs(file, fs)
        with fs.open(file, encoding="utf-8") as f:
            content = f.read()
        metadata = {"filename": file.name, "extension": file.suffix}
        if extra_info:
            metadata = {**metadata, **extra_info}

        return [Document(text=content, metadata=metadata)]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.FlatReader.load_data "Permanent link")

```
load_data(
    file: ,
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Parse file into string.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/flat/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    file: Path,
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""Parse file into string."""
    fs = self._get_fs(file, fs)
    with fs.open(file, encoding="utf-8") as f:
        content = f.read()
    metadata = {"filename": file.name, "extension": file.suffix}
    if extra_info:
        metadata = {**metadata, **extra_info}

    return [Document(text=content, metadata=metadata)]

```
 |  
| --- | --- |  
##  HTMLTagReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.HTMLTagReader "Permanent link")
Bases: 
Read HTML files and extract text from a specific tag with BeautifulSoup.
By default, reads the text from the `<section>` tag.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/html/base.py`  
| 
```
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
```
 | 
```
classHTMLTagReader(BaseReader):
"""
    Read HTML files and extract text from a specific tag with BeautifulSoup.

    By default, reads the text from the ``<section>`` tag.
    """

    def__init__(
        self,
        tag: str = "section",
        ignore_no_id: bool = False,
    ) -> None:
        self._tag = tag
        self._ignore_no_id = ignore_no_id

        super().__init__()

    defload_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        try:
            frombs4import BeautifulSoup
        except ImportError:
            raise ImportError("bs4 is required to read HTML files.")

        with open(file, encoding="utf-8") as html_file:
            soup = BeautifulSoup(html_file, "html.parser")

        tags = soup.find_all(self._tag)
        docs = []
        for tag in tags:
            tag_id = tag.get("id")
            tag_text = self._extract_text_from_tag(tag)

            if self._ignore_no_id and not tag_id:
                continue

            metadata = {
                "tag": self._tag,
                "tag_id": tag_id,
                "file_path": str(file),
            }
            metadata.update(extra_info or {})

            doc = Document(
                text=tag_text,
                metadata=metadata,
            )
            docs.append(doc)
        return docs

    def_extract_text_from_tag(self, tag: "Tag") -> str:
        try:
            frombs4import NavigableString
        except ImportError:
            raise ImportError("bs4 is required to read HTML files.")

        texts = []
        for elem in tag.children:
            if isinstance(elem, NavigableString):
                if elem.strip():
                    texts.append(elem.strip())
            elif elem.name == self._tag:
                continue
            else:
                texts.append(elem.get_text().strip())
        return "\n".join(texts)

```
 |  
| --- | --- |  
##  ImageReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.ImageReader "Permanent link")
Bases: 
Image parser.
Extract text from images using DONUT or pytesseract.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/image/base.py`  
| 
```
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
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
```
 | 
```
classImageReader(BaseReader):
"""
    Image parser.

    Extract text from images using DONUT or pytesseract.

    """

    def__init__(
        self,
        parser_config: Optional[Dict] = None,
        keep_image: bool = False,
        parse_text: bool = False,
        text_type: str = "text",
        pytesseract_model_kwargs: Dict[str, Any] = {},
    ):
"""Init parser."""
        self._text_type = text_type
        if parser_config is None and parse_text:
            if text_type == "plain_text":
                try:
                    importpytesseract
                except ImportError:
                    raise ImportError(
                        "Please install extra dependencies that are required for "
                        "the ImageReader when text_type is 'plain_text': "
                        "`pip install pytesseract`"
                    )
                processor = None
                model = pytesseract
            else:
                try:
                    importsentencepiece  # noqa
                    importtorch  # noqa
                    fromPILimport Image  # noqa
                    fromtransformersimport DonutProcessor, VisionEncoderDecoderModel
                except ImportError:
                    raise ImportError(
                        "Please install extra dependencies that are required for "
                        "the ImageCaptionReader: "
                        "`pip install torch transformers sentencepiece Pillow`"
                    )

                processor = DonutProcessor.from_pretrained(
                    "naver-clova-ix/donut-base-finetuned-cord-v2"
                )
                model = VisionEncoderDecoderModel.from_pretrained(
                    "naver-clova-ix/donut-base-finetuned-cord-v2"
                )
            parser_config = {"processor": processor, "model": model}

        self._parser_config = parser_config
        self._keep_image = keep_image
        self._parse_text = parse_text
        self._pytesseract_model_kwargs = pytesseract_model_kwargs

    defload_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""Parse file."""
        fromllama_index.core.img_utilsimport img_2_b64
        fromPILimport Image

        # load document image
        if fs:
            with fs.open(path=file) as f:
                image = Image.open(BytesIO(f.read()))
        else:
            image = Image.open(file)

        if image.mode != "RGB":
            image = image.convert("RGB")

        # Encode image into base64 string and keep in document
        image_str: Optional[str] = None
        if self._keep_image:
            image_str = img_2_b64(image)

        # Parse image into text
        text_str: str = ""
        if self._parse_text:
            assert self._parser_config is not None
            model = self._parser_config["model"]
            processor = self._parser_config["processor"]

            if processor:
                device = infer_torch_device()
                model.to(device)

                # prepare decoder inputs
                task_prompt = "<s_cord-v2>"
                decoder_input_ids = processor.tokenizer(
                    task_prompt, add_special_tokens=False, return_tensors="pt"
                ).input_ids

                pixel_values = processor(image, return_tensors="pt").pixel_values

                outputs = model.generate(
                    pixel_values.to(device),
                    decoder_input_ids=decoder_input_ids.to(device),
                    max_length=model.decoder.config.max_position_embeddings,
                    early_stopping=True,
                    pad_token_id=processor.tokenizer.pad_token_id,
                    eos_token_id=processor.tokenizer.eos_token_id,
                    use_cache=True,
                    num_beams=3,
                    bad_words_ids=[[processor.tokenizer.unk_token_id]],
                    return_dict_in_generate=True,
                )

                sequence = processor.batch_decode(outputs.sequences)[0]
                sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(
                    processor.tokenizer.pad_token, ""
                )
                # remove first task start token
                text_str = re.sub(r"<.*?>", "", sequence, count=1).strip()
            else:
                importpytesseract

                model = cast(pytesseract, self._parser_config["model"])
                text_str = model.image_to_string(
                    image, **self._pytesseract_model_kwargs
                )

        return [
            ImageDocument(
                text=text_str,
                image=image_str,
                image_path=str(file),
                metadata=extra_info or {},
            )
        ]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.ImageReader.load_data "Permanent link")

```
load_data(
    file: ,
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/image/base.py`  
| 
```
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
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
```
 | 
```
defload_data(
    self,
    file: Path,
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""Parse file."""
    fromllama_index.core.img_utilsimport img_2_b64
    fromPILimport Image

    # load document image
    if fs:
        with fs.open(path=file) as f:
            image = Image.open(BytesIO(f.read()))
    else:
        image = Image.open(file)

    if image.mode != "RGB":
        image = image.convert("RGB")

    # Encode image into base64 string and keep in document
    image_str: Optional[str] = None
    if self._keep_image:
        image_str = img_2_b64(image)

    # Parse image into text
    text_str: str = ""
    if self._parse_text:
        assert self._parser_config is not None
        model = self._parser_config["model"]
        processor = self._parser_config["processor"]

        if processor:
            device = infer_torch_device()
            model.to(device)

            # prepare decoder inputs
            task_prompt = "<s_cord-v2>"
            decoder_input_ids = processor.tokenizer(
                task_prompt, add_special_tokens=False, return_tensors="pt"
            ).input_ids

            pixel_values = processor(image, return_tensors="pt").pixel_values

            outputs = model.generate(
                pixel_values.to(device),
                decoder_input_ids=decoder_input_ids.to(device),
                max_length=model.decoder.config.max_position_embeddings,
                early_stopping=True,
                pad_token_id=processor.tokenizer.pad_token_id,
                eos_token_id=processor.tokenizer.eos_token_id,
                use_cache=True,
                num_beams=3,
                bad_words_ids=[[processor.tokenizer.unk_token_id]],
                return_dict_in_generate=True,
            )

            sequence = processor.batch_decode(outputs.sequences)[0]
            sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(
                processor.tokenizer.pad_token, ""
            )
            # remove first task start token
            text_str = re.sub(r"<.*?>", "", sequence, count=1).strip()
        else:
            importpytesseract

            model = cast(pytesseract, self._parser_config["model"])
            text_str = model.image_to_string(
                image, **self._pytesseract_model_kwargs
            )

    return [
        ImageDocument(
            text=text_str,
            image=image_str,
            image_path=str(file),
            metadata=extra_info or {},
        )
    ]

```
 |  
| --- | --- |  
##  ImageCaptionReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.ImageCaptionReader "Permanent link")
Bases: 
Image parser.
Caption image using Blip.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/image_caption/base.py`  
| 
```
 9
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
```
 | 
```
classImageCaptionReader(BaseReader):
"""
    Image parser.

    Caption image using Blip.

    """

    def__init__(
        self,
        parser_config: Optional[Dict] = None,
        keep_image: bool = False,
        prompt: Optional[str] = None,
    ):
"""Init params."""
        if parser_config is None:
"""Init parser."""
            try:
                importsentencepiece  # noqa
                importtorch
                fromPILimport Image  # noqa
                fromtransformersimport BlipForConditionalGeneration, BlipProcessor
            except ImportError:
                raise ImportError(
                    "Please install extra dependencies that are required for "
                    "the ImageCaptionReader: "
                    "`pip install torch transformers sentencepiece Pillow`"
                )

            device = infer_torch_device()
            dtype = torch.float16 if torch.cuda.is_available() else torch.float32

            processor = BlipProcessor.from_pretrained(
                "Salesforce/blip-image-captioning-large"
            )
            model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-large", torch_dtype=dtype
            )

            parser_config = {
                "processor": processor,
                "model": model,
                "device": device,
                "dtype": dtype,
            }

        self._parser_config = parser_config
        self._keep_image = keep_image
        self._prompt = prompt

    defload_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
"""Parse file."""
        fromllama_index.core.img_utilsimport img_2_b64
        fromPILimport Image

        # load document image
        image = Image.open(file)
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Encode image into base64 string and keep in document
        image_str: Optional[str] = None
        if self._keep_image:
            image_str = img_2_b64(image)

        # Parse image into text
        model = self._parser_config["model"]
        processor = self._parser_config["processor"]

        device = self._parser_config["device"]
        dtype = self._parser_config["dtype"]
        model.to(device)

        # unconditional image captioning

        inputs = processor(image, self._prompt, return_tensors="pt").to(device, dtype)

        out = model.generate(**inputs)
        text_str = processor.decode(out[0], skip_special_tokens=True)

        return [
            ImageDocument(
                text=text_str,
                image=image_str,
                image_path=str(file),
                metadata=extra_info or {},
            )
        ]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.ImageCaptionReader.load_data "Permanent link")

```
load_data(
    file: , extra_info: Optional[] = None
) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/image_caption/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self, file: Path, extra_info: Optional[Dict] = None
) -> List[Document]:
"""Parse file."""
    fromllama_index.core.img_utilsimport img_2_b64
    fromPILimport Image

    # load document image
    image = Image.open(file)
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Encode image into base64 string and keep in document
    image_str: Optional[str] = None
    if self._keep_image:
        image_str = img_2_b64(image)

    # Parse image into text
    model = self._parser_config["model"]
    processor = self._parser_config["processor"]

    device = self._parser_config["device"]
    dtype = self._parser_config["dtype"]
    model.to(device)

    # unconditional image captioning

    inputs = processor(image, self._prompt, return_tensors="pt").to(device, dtype)

    out = model.generate(**inputs)
    text_str = processor.decode(out[0], skip_special_tokens=True)

    return [
        ImageDocument(
            text=text_str,
            image=image_str,
            image_path=str(file),
            metadata=extra_info or {},
        )
    ]

```
 |  
| --- | --- |  
##  ImageTabularChartReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.ImageTabularChartReader "Permanent link")
Bases: 
Image parser.
Extract tabular data from a chart or figure.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/image_deplot/base.py`  
| 
```
 8
 9
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
```
 | 
```
classImageTabularChartReader(BaseReader):
"""
    Image parser.

    Extract tabular data from a chart or figure.

    """

    def__init__(
        self,
        parser_config: Optional[Dict] = None,
        keep_image: bool = False,
        max_output_tokens=512,
        prompt: str = "Generate underlying data table of the figure below:",
    ):
"""Init params."""
        if parser_config is None:
            try:
                importtorch
                fromPILimport Image  # noqa: F401
                fromtransformersimport (
                    Pix2StructForConditionalGeneration,
                    Pix2StructProcessor,
                )
            except ImportError:
                raise ImportError(
                    "Please install extra dependencies that are required for "
                    "the ImageCaptionReader: "
                    "`pip install torch transformers Pillow`"
                )

            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            processor = Pix2StructProcessor.from_pretrained("google/deplot")
            model = Pix2StructForConditionalGeneration.from_pretrained(
                "google/deplot", torch_dtype=dtype
            )
            parser_config = {
                "processor": processor,
                "model": model,
                "device": device,
                "dtype": dtype,
            }

        self._parser_config = parser_config
        self._keep_image = keep_image
        self._max_output_tokens = max_output_tokens
        self._prompt = prompt

    defload_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
"""Parse file."""
        fromllama_index.core.img_utilsimport img_2_b64
        fromPILimport Image

        # load document image
        image = Image.open(file)
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Encode image into base64 string and keep in document
        image_str: Optional[str] = None
        if self._keep_image:
            image_str = img_2_b64(image)

        # Parse image into text
        model = self._parser_config["model"]
        processor = self._parser_config["processor"]

        device = self._parser_config["device"]
        dtype = self._parser_config["dtype"]
        model.to(device)

        # unconditional image captioning

        inputs = processor(image, self._prompt, return_tensors="pt").to(device, dtype)

        out = model.generate(**inputs, max_new_tokens=self._max_output_tokens)
        text_str = "Figure or chart with tabular data: " + processor.decode(
            out[0], skip_special_tokens=True
        )

        return [
            ImageDocument(
                text=text_str,
                image=image_str,
                extra_info=extra_info or {},
            )
        ]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.ImageTabularChartReader.load_data "Permanent link")

```
load_data(
    file: , extra_info: Optional[] = None
) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/image_deplot/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self, file: Path, extra_info: Optional[Dict] = None
) -> List[Document]:
"""Parse file."""
    fromllama_index.core.img_utilsimport img_2_b64
    fromPILimport Image

    # load document image
    image = Image.open(file)
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Encode image into base64 string and keep in document
    image_str: Optional[str] = None
    if self._keep_image:
        image_str = img_2_b64(image)

    # Parse image into text
    model = self._parser_config["model"]
    processor = self._parser_config["processor"]

    device = self._parser_config["device"]
    dtype = self._parser_config["dtype"]
    model.to(device)

    # unconditional image captioning

    inputs = processor(image, self._prompt, return_tensors="pt").to(device, dtype)

    out = model.generate(**inputs, max_new_tokens=self._max_output_tokens)
    text_str = "Figure or chart with tabular data: " + processor.decode(
        out[0], skip_special_tokens=True
    )

    return [
        ImageDocument(
            text=text_str,
            image=image_str,
            extra_info=extra_info or {},
        )
    ]

```
 |  
| --- | --- |  
##  ImageVisionLLMReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.ImageVisionLLMReader "Permanent link")
Bases: 
Image parser.
Caption image using Blip2 (a multimodal VisionLLM similar to GPT4).
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/image_vision_llm/base.py`  
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
```
 | 
```
classImageVisionLLMReader(BaseReader):
"""
    Image parser.

    Caption image using Blip2 (a multimodal VisionLLM similar to GPT4).

    """

    def__init__(
        self,
        parser_config: Optional[Dict] = None,
        keep_image: bool = False,
        prompt: str = "Question: describe what you see in this image. Answer:",
    ):
"""Init params."""
        if parser_config is None:
            try:
                importsentencepiece  # noqa
                importtorch
                fromPILimport Image  # noqa
                fromtransformersimport Blip2ForConditionalGeneration, Blip2Processor
            except ImportError:
                raise ImportError(
                    "Please install extra dependencies that are required for "
                    "the ImageCaptionReader: "
                    "`pip install torch transformers sentencepiece Pillow`"
                )

            self._torch = torch
            self._torch_imported = True

            device = infer_torch_device()
            dtype = (
                self._torch.float16
                if self._torch.cuda.is_available()
                else self._torch.float32
            )
            processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
            model = Blip2ForConditionalGeneration.from_pretrained(
                "Salesforce/blip2-opt-2.7b", torch_dtype=dtype
            )
            parser_config = {
                "processor": processor,
                "model": model,
                "device": device,
                "dtype": dtype,
            }

        # Try to import PyTorch in order to run inference efficiently.
        self._import_torch()

        self._parser_config = parser_config
        self._keep_image = keep_image
        self._prompt = prompt

    defload_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
"""Parse file."""
        fromllama_index.core.img_utilsimport img_2_b64
        fromPILimport Image

        # load document image
        image = Image.open(file)
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Encode image into base64 string and keep in document
        image_str: Optional[str] = None
        if self._keep_image:
            image_str = img_2_b64(image)

        # Parse image into text
        model = self._parser_config["model"]
        processor = self._parser_config["processor"]

        device = self._parser_config["device"]
        dtype = self._parser_config["dtype"]
        model.to(device)

        # unconditional image captioning

        inputs = processor(image, self._prompt, return_tensors="pt").to(device, dtype)

        if self._torch_imported:
            # Gradients are not needed during inference. If PyTorch is
            # installed, we can instruct it to not track the gradients.
            # This reduces GPU memory usage and improves inference efficiency.
            with self._torch.no_grad():
                out = model.generate(**inputs)
        else:
            # Fallback to less efficient behavior if PyTorch is not installed.
            out = model.generate(**inputs)

        text_str = processor.decode(out[0], skip_special_tokens=True)

        return [
            ImageDocument(
                text=text_str,
                image=image_str,
                image_path=str(file),
                metadata=extra_info or {},
            )
        ]

    def_import_torch(self) -> None:
        self._torch = None

        try:
            importtorch

            self._torch = torch
            self._torch_imported = True
        except ImportError:
            self._torch_imported = False

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.ImageVisionLLMReader.load_data "Permanent link")

```
load_data(
    file: , extra_info: Optional[] = None
) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/image_vision_llm/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self, file: Path, extra_info: Optional[Dict] = None
) -> List[Document]:
"""Parse file."""
    fromllama_index.core.img_utilsimport img_2_b64
    fromPILimport Image

    # load document image
    image = Image.open(file)
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Encode image into base64 string and keep in document
    image_str: Optional[str] = None
    if self._keep_image:
        image_str = img_2_b64(image)

    # Parse image into text
    model = self._parser_config["model"]
    processor = self._parser_config["processor"]

    device = self._parser_config["device"]
    dtype = self._parser_config["dtype"]
    model.to(device)

    # unconditional image captioning

    inputs = processor(image, self._prompt, return_tensors="pt").to(device, dtype)

    if self._torch_imported:
        # Gradients are not needed during inference. If PyTorch is
        # installed, we can instruct it to not track the gradients.
        # This reduces GPU memory usage and improves inference efficiency.
        with self._torch.no_grad():
            out = model.generate(**inputs)
    else:
        # Fallback to less efficient behavior if PyTorch is not installed.
        out = model.generate(**inputs)

    text_str = processor.decode(out[0], skip_special_tokens=True)

    return [
        ImageDocument(
            text=text_str,
            image=image_str,
            image_path=str(file),
            metadata=extra_info or {},
        )
    ]

```
 |  
| --- | --- |  
##  IPYNBReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.IPYNBReader "Permanent link")
Bases: 
Image parser.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/ipynb/base.py`  
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
```
 | 
```
classIPYNBReader(BaseReader):
"""Image parser."""

    def__init__(
        self,
        parser_config: Optional[Dict] = None,
        concatenate: bool = False,
    ):
"""Init params."""
        self._parser_config = parser_config
        self._concatenate = concatenate

    defload_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""Parse file."""
        if file.name.endswith(".ipynb"):
            try:
                importnbconvert
            except ImportError:
                raise ImportError("Please install nbconvert 'pip install nbconvert' ")
        if fs:
            with fs.open(file, encoding="utf-8") as f:
                string = nbconvert.exporters.ScriptExporter().from_file(f)[0]
        else:
            string = nbconvert.exporters.ScriptExporter().from_file(file)[0]
        # split each In[] cell into a separate string
        splits = re.split(r"In\[\d+\]:", string)
        # remove the first element, which is empty
        splits.pop(0)

        if self._concatenate:
            docs = [Document(text="\n\n".join(splits), metadata=extra_info or {})]
        else:
            docs = [Document(text=s, metadata=extra_info or {}) for s in splits]
        return docs

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.IPYNBReader.load_data "Permanent link")

```
load_data(
    file: ,
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/ipynb/base.py`  
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
```
 | 
```
defload_data(
    self,
    file: Path,
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""Parse file."""
    if file.name.endswith(".ipynb"):
        try:
            importnbconvert
        except ImportError:
            raise ImportError("Please install nbconvert 'pip install nbconvert' ")
    if fs:
        with fs.open(file, encoding="utf-8") as f:
            string = nbconvert.exporters.ScriptExporter().from_file(f)[0]
    else:
        string = nbconvert.exporters.ScriptExporter().from_file(file)[0]
    # split each In[] cell into a separate string
    splits = re.split(r"In\[\d+\]:", string)
    # remove the first element, which is empty
    splits.pop(0)

    if self._concatenate:
        docs = [Document(text="\n\n".join(splits), metadata=extra_info or {})]
    else:
        docs = [Document(text=s, metadata=extra_info or {}) for s in splits]
    return docs

```
 |  
| --- | --- |  
##  MarkdownReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.MarkdownReader "Permanent link")
Bases: 
Markdown parser.
Extract text from markdown files. Returns dictionary with keys as headers and values as the text between headers.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/markdown/base.py`  
| 
```
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
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
```
 | 
```
classMarkdownReader(BaseReader):
"""
    Markdown parser.

    Extract text from markdown files.
    Returns dictionary with keys as headers and values as the text between headers.

    """

    def__init__(
        self,
        *args: Any,
        remove_hyperlinks: bool = True,
        remove_images: bool = True,
        separator: str = " ",
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__(*args, **kwargs)
        self._remove_hyperlinks = remove_hyperlinks
        self._remove_images = remove_images
        self._separator = separator

    defmarkdown_to_tups(self, markdown_text: str) -> List[Tuple[Optional[str], str]]:
"""Convert a markdown file to a list of tuples containing header and text."""
        markdown_tups: List[Tuple[Optional[str], str]] = []
        lines = markdown_text.split("\n")

        current_lines = []
        in_code_block = False
        headers = {}
        for line in lines:
            # Toggle code block state
            if line.startswith("```"):
                in_code_block = not in_code_block

            if in_code_block:
                current_lines.append(line)
                continue
            # Process headers only when not in a code block
            else:
                line = line.strip()
                if not line:
                    continue

                header_match = re.match(r"^(#+)\s+(.*)", line)
                if header_match:
                    if current_lines and not headers:
                        # Add content before first header
                        markdown_tups.append((None, "\n".join(current_lines)))
                        current_lines.clear()
                    # Extract header level and text
                    header_level = len(
                        header_match.group(1)
                    )  # number of '#' indicates level
                    current_header = header_match.group(2)  # the header text
                    if headers.get(header_level):
                        # Add previous section to the list before switching header
                        markdown_tups.append(
                            (
                                self._separator.join(headers.values()),
                                "\n".join(current_lines),
                            )
                        )
                        # remove all headers with level greater than current header
                        headers = {k: v for k, v in headers.items() if k  header_level}
                        current_lines.clear()

                    headers[header_level] = current_header
                else:
                    current_lines.append(line)

        # Append the last section
        if current_lines or headers:
            markdown_tups.append(
                (self._separator.join(headers.values()), "\n".join(current_lines))
            )

        # Postprocess the tuples before returning
        return [
            (
                key.strip() if key else None,  # Clean up header (strip whitespace)
                re.sub(r"<.*?>", "", value),  # Remove HTML tags
            )
            for key, value in markdown_tups
        ]

    defremove_images(self, content: str) -> str:
"""Remove images in markdown content but keep the description."""
        pattern = r"![(.?)](.?)"
        return re.sub(pattern, r"\1", content)

    defremove_hyperlinks(self, content: str) -> str:
"""Remove hyperlinks in markdown content."""
        pattern = r"\[(.*?)\]\((.*?)\)"
        return re.sub(pattern, r"\1", content)

    def_init_parser(self) -> Dict:
"""Initialize the parser with the config."""
        return {}

    defparse_tups(
        self,
        filepath: str,
        errors: str = "ignore",
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Tuple[Optional[str], str]]:
"""Parse file into tuples."""
        fs = fs or LocalFileSystem()
        with fs.open(filepath, encoding="utf-8") as f:
            content = f.read().decode(encoding="utf-8")
        if self._remove_hyperlinks:
            content = self.remove_hyperlinks(content)
        if self._remove_images:
            content = self.remove_images(content)
        return self.markdown_to_tups(content)

    defload_data(
        self,
        file: str,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""Parse file into string."""
        tups = self.parse_tups(file, fs=fs)
        results = []

        for header, text in tups:
            if header is None:
                results.append(Document(text=text, metadata=extra_info or {}))
            else:
                results.append(
                    Document(text=f"\n\n{header}\n{text}", metadata=extra_info or {})
                )
        return results

```
 |  
| --- | --- |  
###  markdown_to_tups [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.MarkdownReader.markdown_to_tups "Permanent link")

```
markdown_to_tups(
    markdown_text: ,
) -> [Tuple[Optional[], ]]

```

Convert a markdown file to a list of tuples containing header and text.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/markdown/base.py`  
| 
```
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
```
 | 
```
defmarkdown_to_tups(self, markdown_text: str) -> List[Tuple[Optional[str], str]]:
"""Convert a markdown file to a list of tuples containing header and text."""
    markdown_tups: List[Tuple[Optional[str], str]] = []
    lines = markdown_text.split("\n")

    current_lines = []
    in_code_block = False
    headers = {}
    for line in lines:
        # Toggle code block state
        if line.startswith("```"):
            in_code_block = not in_code_block

        if in_code_block:
            current_lines.append(line)
            continue
        # Process headers only when not in a code block
        else:
            line = line.strip()
            if not line:
                continue

            header_match = re.match(r"^(#+)\s+(.*)", line)
            if header_match:
                if current_lines and not headers:
                    # Add content before first header
                    markdown_tups.append((None, "\n".join(current_lines)))
                    current_lines.clear()
                # Extract header level and text
                header_level = len(
                    header_match.group(1)
                )  # number of '#' indicates level
                current_header = header_match.group(2)  # the header text
                if headers.get(header_level):
                    # Add previous section to the list before switching header
                    markdown_tups.append(
                        (
                            self._separator.join(headers.values()),
                            "\n".join(current_lines),
                        )
                    )
                    # remove all headers with level greater than current header
                    headers = {k: v for k, v in headers.items() if k  header_level}
                    current_lines.clear()

                headers[header_level] = current_header
            else:
                current_lines.append(line)

    # Append the last section
    if current_lines or headers:
        markdown_tups.append(
            (self._separator.join(headers.values()), "\n".join(current_lines))
        )

    # Postprocess the tuples before returning
    return [
        (
            key.strip() if key else None,  # Clean up header (strip whitespace)
            re.sub(r"<.*?>", "", value),  # Remove HTML tags
        )
        for key, value in markdown_tups
    ]

```
 |  
| --- | --- |  
###  remove_images [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.MarkdownReader.remove_images "Permanent link")

```
remove_images(content: ) -> 

```

Remove images in markdown content but keep the description.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/markdown/base.py`  
| 
```
103
104
105
106
```
 | 
```
defremove_images(self, content: str) -> str:
"""Remove images in markdown content but keep the description."""
    pattern = r"![(.?)](.?)"
    return re.sub(pattern, r"\1", content)

```
 |  
| --- | --- |  
###  remove_hyperlinks [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.MarkdownReader.remove_hyperlinks "Permanent link")

```
remove_hyperlinks(content: ) -> 

```

Remove hyperlinks in markdown content.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/markdown/base.py`  
| 
```
108
109
110
111
```
 | 
```
defremove_hyperlinks(self, content: str) -> str:
"""Remove hyperlinks in markdown content."""
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.sub(pattern, r"\1", content)

```
 |  
| --- | --- |  
###  parse_tups [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.MarkdownReader.parse_tups "Permanent link")

```
parse_tups(
    filepath: ,
    errors:  = "ignore",
    fs: Optional[AbstractFileSystem] = None,
) -> [Tuple[Optional[], ]]

```

Parse file into tuples.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/markdown/base.py`  
| 
```
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
defparse_tups(
    self,
    filepath: str,
    errors: str = "ignore",
    fs: Optional[AbstractFileSystem] = None,
) -> List[Tuple[Optional[str], str]]:
"""Parse file into tuples."""
    fs = fs or LocalFileSystem()
    with fs.open(filepath, encoding="utf-8") as f:
        content = f.read().decode(encoding="utf-8")
    if self._remove_hyperlinks:
        content = self.remove_hyperlinks(content)
    if self._remove_images:
        content = self.remove_images(content)
    return self.markdown_to_tups(content)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.MarkdownReader.load_data "Permanent link")

```
load_data(
    file: ,
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Parse file into string.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/markdown/base.py`  
| 
```
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
```
 | 
```
defload_data(
    self,
    file: str,
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""Parse file into string."""
    tups = self.parse_tups(file, fs=fs)
    results = []

    for header, text in tups:
        if header is None:
            results.append(Document(text=text, metadata=extra_info or {}))
        else:
            results.append(
                Document(text=f"\n\n{header}\n{text}", metadata=extra_info or {})
            )
    return results

```
 |  
| --- | --- |  
##  MboxReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.MboxReader "Permanent link")
Bases: 
Mbox parser.
Extract messages from mailbox files. Returns string including date, subject, sender, receiver and content for each message.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/mbox/base.py`  
| 
```
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
```
 | 
```
classMboxReader(BaseReader):
"""
    Mbox parser.

    Extract messages from mailbox files.
    Returns string including date, subject, sender, receiver and
    content for each message.

    """

    DEFAULT_MESSAGE_FORMAT: str = (
        "Date: {_date}\n"
        "From: {_from}\n"
        "To: {_to}\n"
        "Subject: {_subject}\n"
        "Content: {_content}"
    )

    def__init__(
        self,
        *args: Any,
        max_count: int = 0,
        message_format: str = DEFAULT_MESSAGE_FORMAT,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        try:
            frombs4import BeautifulSoup  # noqa
        except ImportError:
            raise ImportError(
                "`beautifulsoup4` package not found: `pip install beautifulsoup4`"
            )

        super().__init__(*args, **kwargs)
        self.max_count = max_count
        self.message_format = message_format

    defload_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""Parse file into string."""
        # Import required libraries
        importmailbox
        fromemail.parserimport BytesParser
        fromemail.policyimport default

        frombs4import BeautifulSoup

        if fs:
            logger.warning(
                "fs was specified but MboxReader doesn't support loading "
                "from fsspec filesystems. Will load from local filesystem instead."
            )

        i = 0
        results: List[str] = []
        # Load file using mailbox
        bytes_parser = BytesParser(policy=default).parse
        mbox = mailbox.mbox(file, factory=bytes_parser)  # type: ignore

        # Iterate through all messages
        for _, _msg in enumerate(mbox):
            try:
                msg: mailbox.mboxMessage = _msg
                # Parse multipart messages
                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        cdispo = str(part.get("Content-Disposition"))
                        if ctype == "text/plain" and "attachment" not in cdispo:
                            content = part.get_payload(decode=True)  # decode
                            break
                # Get plain message payload for non-multipart messages
                else:
                    content = msg.get_payload(decode=True)

                # Parse message HTML content and remove unneeded whitespace
                soup = BeautifulSoup(content)
                stripped_content = " ".join(soup.get_text().split())
                # Format message to include date, sender, receiver and subject
                msg_string = self.message_format.format(
                    _date=msg["date"],
                    _from=msg["from"],
                    _to=msg["to"],
                    _subject=msg["subject"],
                    _content=stripped_content,
                )
                # Add message string to results
                results.append(msg_string)
            except Exception as e:
                logger.warning(f"Failed to parse message:\n{_msg}\n with exception {e}")

            # Increment counter and return if max count is met
            i += 1
            if self.max_count  0 and i >= self.max_count:
                break

        return [Document(text=result, metadata=extra_info or {}) for result in results]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.MboxReader.load_data "Permanent link")

```
load_data(
    file: ,
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Parse file into string.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/mbox/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    file: Path,
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""Parse file into string."""
    # Import required libraries
    importmailbox
    fromemail.parserimport BytesParser
    fromemail.policyimport default

    frombs4import BeautifulSoup

    if fs:
        logger.warning(
            "fs was specified but MboxReader doesn't support loading "
            "from fsspec filesystems. Will load from local filesystem instead."
        )

    i = 0
    results: List[str] = []
    # Load file using mailbox
    bytes_parser = BytesParser(policy=default).parse
    mbox = mailbox.mbox(file, factory=bytes_parser)  # type: ignore

    # Iterate through all messages
    for _, _msg in enumerate(mbox):
        try:
            msg: mailbox.mboxMessage = _msg
            # Parse multipart messages
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get("Content-Disposition"))
                    if ctype == "text/plain" and "attachment" not in cdispo:
                        content = part.get_payload(decode=True)  # decode
                        break
            # Get plain message payload for non-multipart messages
            else:
                content = msg.get_payload(decode=True)

            # Parse message HTML content and remove unneeded whitespace
            soup = BeautifulSoup(content)
            stripped_content = " ".join(soup.get_text().split())
            # Format message to include date, sender, receiver and subject
            msg_string = self.message_format.format(
                _date=msg["date"],
                _from=msg["from"],
                _to=msg["to"],
                _subject=msg["subject"],
                _content=stripped_content,
            )
            # Add message string to results
            results.append(msg_string)
        except Exception as e:
            logger.warning(f"Failed to parse message:\n{_msg}\n with exception {e}")

        # Increment counter and return if max count is met
        i += 1
        if self.max_count  0 and i >= self.max_count:
            break

    return [Document(text=result, metadata=extra_info or {}) for result in results]

```
 |  
| --- | --- |  
##  PagedCSVReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PagedCSVReader "Permanent link")
Bases: 
Paged CSV parser.
Displayed each row in an LLM-friendly format on a separate document.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `encoding`  |  Encoding used to open the file. utf-8 by default.  |  `'utf-8'`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/paged_csv/base.py`  
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
```
 | 
```
classPagedCSVReader(BaseReader):
"""
    Paged CSV parser.

    Displayed each row in an LLM-friendly format on a separate document.

    Args:
        encoding (str): Encoding used to open the file.
            utf-8 by default.

    """

    def__init__(self, *args: Any, encoding: str = "utf-8", **kwargs: Any) -> None:
"""Init params."""
        super().__init__(*args, **kwargs)
        self._encoding = encoding

    defload_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        delimiter: str = ",",
        quotechar: str = '"',
    ) -> List[Document]:
"""Parse file."""
        importcsv

        docs = []
        with open(file, encoding=self._encoding) as fp:
            csv_reader = csv.DictReader(f=fp, delimiter=delimiter, quotechar=quotechar)  # type: ignore
            for row in csv_reader:
                docs.append(
                    Document(
                        text="\n".join(
                            f"{k.strip()}: {v.strip()}" for k, v in row.items()
                        ),
                        extra_info=extra_info or {},
                    )
                )
        return docs

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PagedCSVReader.load_data "Permanent link")

```
load_data(
    file: ,
    extra_info: Optional[] = None,
    delimiter:  = ",",
    quotechar:  = '"',
) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/paged_csv/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    file: Path,
    extra_info: Optional[Dict] = None,
    delimiter: str = ",",
    quotechar: str = '"',
) -> List[Document]:
"""Parse file."""
    importcsv

    docs = []
    with open(file, encoding=self._encoding) as fp:
        csv_reader = csv.DictReader(f=fp, delimiter=delimiter, quotechar=quotechar)  # type: ignore
        for row in csv_reader:
            docs.append(
                Document(
                    text="\n".join(
                        f"{k.strip()}: {v.strip()}" for k, v in row.items()
                    ),
                    extra_info=extra_info or {},
                )
            )
    return docs

```
 |  
| --- | --- |  
##  PyMuPDFReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PyMuPDFReader "Permanent link")
Bases: 
Read PDF files using PyMuPDF library.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/pymu_pdf/base.py`  
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
```
 | 
```
classPyMuPDFReader(BaseReader):
"""Read PDF files using PyMuPDF library."""

    defload_data(
        self,
        file_path: Union[Path, str],
        metadata: bool = True,
        extra_info: Optional[Dict] = None,
    ) -> List[Document]:
"""Loads list of documents from PDF file and also accepts extra information in dict format."""
        return self.load(file_path, metadata=metadata, extra_info=extra_info)

    defload(
        self,
        file_path: Union[Path, str],
        metadata: bool = True,
        extra_info: Optional[Dict] = None,
    ) -> List[Document]:
"""
        Loads list of documents from PDF file and also accepts extra information in dict format.

        Args:
            file_path (Union[Path, str]): file path of PDF file (accepts string or Path).
            metadata (bool, optional): if metadata to be included or not. Defaults to True.
            extra_info (Optional[Dict], optional): extra information related to each document in dict format. Defaults to None.

        Raises:
            TypeError: if extra_info is not a dictionary.
            TypeError: if file_path is not a string or Path.

        Returns:
            List[Document]: list of documents.

        """
        importfitz

        # check if file_path is a string or Path
        if not isinstance(file_path, str) and not isinstance(file_path, Path):
            raise TypeError("file_path must be a string or Path.")

        # open PDF file
        doc = fitz.open(file_path)

        # if extra_info is not None, check if it is a dictionary
        if extra_info:
            if not isinstance(extra_info, dict):
                raise TypeError("extra_info must be a dictionary.")

        # if metadata is True, add metadata to each document
        if metadata:
            if not extra_info:
                extra_info = {}
            extra_info["total_pages"] = len(doc)
            extra_info["file_path"] = str(file_path)

            # return list of documents
            return [
                Document(
                    text=page.get_text().encode("utf-8"),
                    extra_info=dict(
                        extra_info,
                        **{
                            "source": f"{page.number+1}",
                        },
                    ),
                )
                for page in doc
            ]

        else:
            return [
                Document(
                    text=page.get_text().encode("utf-8"), extra_info=extra_info or {}
                )
                for page in doc
            ]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PyMuPDFReader.load_data "Permanent link")

```
load_data(
    file_path: Union[, ],
    metadata:  = True,
    extra_info: Optional[] = None,
) -> []

```

Loads list of documents from PDF file and also accepts extra information in dict format.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/pymu_pdf/base.py`  
| 
```
13
14
15
16
17
18
19
20
```
 | 
```
defload_data(
    self,
    file_path: Union[Path, str],
    metadata: bool = True,
    extra_info: Optional[Dict] = None,
) -> List[Document]:
"""Loads list of documents from PDF file and also accepts extra information in dict format."""
    return self.load(file_path, metadata=metadata, extra_info=extra_info)

```
 |  
| --- | --- |  
###  load [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PyMuPDFReader.load "Permanent link")

```
load(
    file_path: Union[, ],
    metadata:  = True,
    extra_info: Optional[] = None,
) -> []

```

Loads list of documents from PDF file and also accepts extra information in dict format.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_path`  |  `Union[Path, str]`  |  file path of PDF file (accepts string or Path).  |  _required_  |  
|  `metadata`  |  `bool`  |  if metadata to be included or not. Defaults to True.  |  `True`  |  
|  `extra_info`  |  `Optional[Dict]`  |  extra information related to each document in dict format. Defaults to None.  |  `None`  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `TypeError`  |  if extra_info is not a dictionary.  |  
|  `TypeError`  |  if file_path is not a string or Path.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/pymu_pdf/base.py`  
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
```
 | 
```
defload(
    self,
    file_path: Union[Path, str],
    metadata: bool = True,
    extra_info: Optional[Dict] = None,
) -> List[Document]:
"""
    Loads list of documents from PDF file and also accepts extra information in dict format.

    Args:
        file_path (Union[Path, str]): file path of PDF file (accepts string or Path).
        metadata (bool, optional): if metadata to be included or not. Defaults to True.
        extra_info (Optional[Dict], optional): extra information related to each document in dict format. Defaults to None.

    Raises:
        TypeError: if extra_info is not a dictionary.
        TypeError: if file_path is not a string or Path.

    Returns:
        List[Document]: list of documents.

    """
    importfitz

    # check if file_path is a string or Path
    if not isinstance(file_path, str) and not isinstance(file_path, Path):
        raise TypeError("file_path must be a string or Path.")

    # open PDF file
    doc = fitz.open(file_path)

    # if extra_info is not None, check if it is a dictionary
    if extra_info:
        if not isinstance(extra_info, dict):
            raise TypeError("extra_info must be a dictionary.")

    # if metadata is True, add metadata to each document
    if metadata:
        if not extra_info:
            extra_info = {}
        extra_info["total_pages"] = len(doc)
        extra_info["file_path"] = str(file_path)

        # return list of documents
        return [
            Document(
                text=page.get_text().encode("utf-8"),
                extra_info=dict(
                    extra_info,
                    **{
                        "source": f"{page.number+1}",
                    },
                ),
            )
            for page in doc
        ]

    else:
        return [
            Document(
                text=page.get_text().encode("utf-8"), extra_info=extra_info or {}
            )
            for page in doc
        ]

```
 |  
| --- | --- |  
##  RTFReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.RTFReader "Permanent link")
Bases: 
RTF (Rich Text Format) Reader. Reads rtf file and convert to Document.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/rtf/base.py`  
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
```
 | 
```
classRTFReader(BaseReader):
"""RTF (Rich Text Format) Reader. Reads rtf file and convert to Document."""

    defload_data(
        self,
        input_file: Union[Path, str],
        extra_info: Optional[Dict[str, Any]] = None,
        **load_kwargs: Any,
    ) -> List[Document]:
"""
        Load data from RTF file.

        Args:
            input_file (Path | str): Path for the RTF file.
            extra_info (Dict[str, Any]): Path for the RTF file.

        Returns:
            List[Document]: List of documents.

        """
        try:
            fromstriprtf.striprtfimport rtf_to_text
        except ImportError:
            raise ImportError("striprtf is required to read RTF files.")

        with open(str(input_file)) as f:
            text = rtf_to_text(f.read())
            return [Document(text=text.strip(), metadata=extra_info or {})]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.RTFReader.load_data "Permanent link")

```
load_data(
    input_file: Union[, ],
    extra_info: Optional[[, ]] = None,
    **load_kwargs: 
) -> []

```

Load data from RTF file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `input_file`  |  `Path | str`  |  Path for the RTF file.  |  _required_  |  
|  `extra_info`  |  `Dict[str, Any]`  |  Path for the RTF file.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/rtf/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    input_file: Union[Path, str],
    extra_info: Optional[Dict[str, Any]] = None,
    **load_kwargs: Any,
) -> List[Document]:
"""
    Load data from RTF file.

    Args:
        input_file (Path | str): Path for the RTF file.
        extra_info (Dict[str, Any]): Path for the RTF file.

    Returns:
        List[Document]: List of documents.

    """
    try:
        fromstriprtf.striprtfimport rtf_to_text
    except ImportError:
        raise ImportError("striprtf is required to read RTF files.")

    with open(str(input_file)) as f:
        text = rtf_to_text(f.read())
        return [Document(text=text.strip(), metadata=extra_info or {})]

```
 |  
| --- | --- |  
##  PptxReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PptxReader "Permanent link")
Bases: 
Enhanced PowerPoint parser.
Extract text, tables, charts, speaker notes, and optionally caption images. Supports multithreaded processing and LLM-based content consolidation. Always returns one Document per slide.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/slides/base.py`  
| 
```
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
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
```
 | 
```
classPptxReader(BaseReader):
"""
    Enhanced PowerPoint parser.

    Extract text, tables, charts, speaker notes, and optionally caption images.
    Supports multithreaded processing and LLM-based content consolidation.
    Always returns one Document per slide.
    """

    def__init__(
        self,
        extract_images: bool = False,
        context_consolidation_with_llm: bool = False,
        llm: Optional[BaseLLM] = None,
        batch_size: int = 10,
        num_workers: int = 4,
        raise_on_error: bool = False,
    ) -> None:
"""
        Initialize enhanced PptxReader.

        Args:
            extract_images: Whether to extract and caption images
            context_consolidation_with_llm: Whether to use LLM for contextual content consolidation
            llm: LLM instance for content consolidation (optional)
            batch_size: Number of slides to process in parallel batches
            num_workers: Number of worker threads (0 for sequential processing)

        """
        # Use provided LLM or fall back to global Settings
        if context_consolidation_with_llm and llm is None:
            llm = Settings.llm

        # Store settings
        self.extract_images = extract_images
        self.context_consolidation_with_llm = context_consolidation_with_llm
        self.llm = llm
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.raise_on_error = raise_on_error
        self.content_extractor = SlideContentExtractor(
            llm=self.llm,
            extract_images=self.extract_images,
            context_consolidation_with_llm=self.context_consolidation_with_llm,
        )
        self.raise_on_error = raise_on_error

    defload_data(
        self,
        file: Union[str, Path],
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""
        Parse PowerPoint file with enhanced content extraction.

        Args:
            file: Path to the PowerPoint file
            extra_info: Additional metadata to include
            fs: File system to use for reading

        Returns:
            List of Documents (one per slide)

        """
        logger.debug(f"Loading PPTX file: {file}")
        file_path_str = str(file)

        # Extract content using enhanced extraction
        result = self.extract_with_validation(
            file_path=file_path_str,
            extract_images=self.extract_images,
            context_consolidation_with_llm=self.context_consolidation_with_llm,
            fs=fs,
        )

        if not result["success"] and not self.raise_on_error:
            logger.error(
                f"Failed to extract data from {file_path_str}: {result['errors']}"
            )
            return []
        elif not result["success"] and self.raise_on_error:
            raise ValueError(
                f"Failed to extract data from {file_path_str}: {result['errors']}"
            )

        # Convert to Documents
        docs = []
        for i, slide in enumerate(result["data"]["slides"], start=1):
            # Create rich metadata
            metadata = {
                "file_path": str(file),
                "page_label": i,
                "title": slide.get("title", ""),
                "extraction_errors": slide.get("extraction_errors", []),
                "extraction_warnings": slide.get("extraction_warnings", []),
                "tables": slide.get("tables", []),
                "charts": slide.get("charts", []),
                "notes": slide.get("notes", ""),
                "images": slide.get("images", []),
                "text_sections": slide.get("text_sections", []),
            }
            if extra_info:
                metadata.update(extra_info)

            docs.append(
                Document(
                    text=slide["content"],
                    metadata=metadata,
                    excluded_embed_metadata_keys=list(
                        metadata.keys()
                    ),  # excluding the metadata keys from the embedding since the metadata size can potentially be too large and may cause the embedding to fail
                    excluded_llm_metadata_keys=list(
                        metadata.keys()
                    ),  # excluding the metadata keys from the llm
                )
            )

        logger.debug(f"Successfully loaded {len(docs)} slides from {file}")
        return docs

    defextract_with_validation(
        self,
        file_path: str,
        extract_images: bool = True,
        context_consolidation_with_llm: bool = False,
        fs: Optional[AbstractFileSystem] = None,
    ) -> Dict[str, Any]:
"""Extract content from PowerPoint file with validation and multithreaded processing."""
        result: Dict[str, Any] = {
            "success": False,
            "data": None,
            "errors": [],
            "warnings": [],
            "stats": {},
        }

        # Validate file and get presentation object
        validation = self._validate_file(file_path, fs)
        if not validation.get("valid", False):
            result["errors"] = validation.get("errors", [])
            return result

        # Use the presentation object from validation
        presentation = validation.get("presentation")
        if presentation is None:
            result["errors"].append("Failed to get presentation object from validation")
            return result

        filename = Path(file_path).name
        logger.debug(f"Processing file: {filename}")

        try:
            start_time = datetime.now()
            total_slides = len(presentation.slides)
            logger.debug(f"Processing {total_slides} slides from {filename}")

            # Prepare result structure
            slides_data: list = []

            # Create batches of slide indices
            batches = [
                (i, min(i + self.batch_size, total_slides))
                for i in range(0, total_slides, self.batch_size)
            ]

            # Process in parallel or serial
            if self.num_workers and self.num_workers  0:
                with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                    futures = {
                        executor.submit(
                            self._process_batch,
                            presentation,
                            start,
                            end,
                            filename,
                            extract_images,
                            context_consolidation_with_llm,
                        ): (start, end)
                        for start, end in batches
                    }
                    for fut in as_completed(futures):
                        start, end = futures[fut]
                        try:
                            batch_results = fut.result()
                            slides_data.extend(batch_results)
                        except Exception as e:
                            logger.error(f"Batch {start+1}-{end} failed: {e}")
                            for idx in range(start, end):
                                slides_data.append(
                                    {
                                        "slide_number": idx + 1,
                                        "error": str(e),
                                        "partial_extraction": True,
                                    }
                                )
                        finally:
                            gc.collect()
            else:
                # Serial fallback
                for start, end in batches:
                    slides_data.extend(
                        self._process_batch(
                            presentation,
                            start,
                            end,
                            filename,
                            extract_images,
                            context_consolidation_with_llm,
                        )
                    )
                    gc.collect()

            # Calculate stats and finalize
            processing_time = (datetime.now() - start_time).total_seconds()
            stats = {
                "total_slides": total_slides,
                "processed_slides": len(slides_data),
                "total_errors": sum(
                    1
                    for s in slides_data
                    if s.get("error") or s.get("extraction_errors")
                ),
                "processing_time_seconds": processing_time,
                "file_size_mb": 0 if fs else os.path.getsize(file_path) / (1024 * 1024),
            }

            result.update(
                {
                    "success": True,
                    "data": {
                        "filename": filename,
                        "slides": sorted(
                            slides_data, key=lambda s: s.get("slide_number", 0)
                        ),
                        "metadata": {
                            "total_slides": total_slides,
                            "file_path": file_path,
                            "processing_timestamp": datetime.now().isoformat(),
                            "extract_images": extract_images,
                            "context_consolidation_with_llm": context_consolidation_with_llm,
                        },
                    },
                    "errors": [],
                    "stats": stats,
                }
            )

            logger.debug(
                f"Successfully processed {filename}: {stats['processed_slides']} slides "
                f"in {stats['processing_time_seconds']:.2f}s"
            )

            # Cleanup
            del presentation
            gc.collect()

        except Exception as e:
            error_msg = f"Critical error processing {filename}: {e}"
            logger.error(error_msg)
            result["errors"].append(error_msg)

        return result

    def_process_batch(
        self,
        presentation: Any,
        start: int,
        end: int,
        filename: str,
        extract_images: bool,
        context_consolidation_with_llm: bool,
    ) -> list:
"""
        Process slides in the range [start, end) and return their extracted data.
        Runs in the context of a worker thread.
        """
        thread_name = threading.current_thread().name
        logger.debug(f"[{thread_name}] Starting batch {start+1}-{end}")

        batch_data: list = []
        for idx in range(start, end):
            try:
                slide = presentation.slides[idx]
                slide_data = self.content_extractor.extract_slide_safe(
                    slide=slide,
                    slide_number=idx + 1,
                    filename=Path(filename),
                )
                batch_data.append(slide_data)
                if slide_data.get("extraction_errors"):
                    logger.warning(
                        f"[{thread_name}] Slide {idx+1} had extraction errors: {slide_data.get('extraction_errors')}"
                    )
            except Exception as e:
                logger.warning(f"[{thread_name}] Error on slide {idx+1}: {e}")
                batch_data.append(
                    {
                        "slide_number": idx + 1,
                        "error": str(e),
                        "partial_extraction": True,
                    }
                )
        logger.debug(f"[{thread_name}] Finished batch {start+1}-{end}")
        return batch_data

    def_validate_file(
        self, file_path: str, fs: Optional[AbstractFileSystem] = None
    ) -> Dict[str, Any]:
"""Validate that the file exists, and can be opened. Returns presentation object for reuse."""
        frompptximport Presentation
        importio

        validation: Dict[str, Any] = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "presentation": None,
        }

        # Extension warning
        if not file_path.lower().endswith((".pptx", ".ppt")):
            validation["warnings"].append(
                "File extension not typical for PowerPoint files"
            )

        # File existence (only for local files)
        if not fs:
            if not os.path.exists(file_path):
                validation["valid"] = False
                validation["errors"].append(f"File not found: {file_path}")
                return validation

        # Try opening the presentation
        try:
            if fs:
                with fs.open(file_path) as f:
                    presentation = Presentation(io.BytesIO(f.read()))
            else:
                presentation = Presentation(file_path)

            count = len(presentation.slides)
            if count == 0:
                validation["warnings"].append("Presentation contains no slides")
            elif count  1000:
                validation["warnings"].append(f"Large presentation: {count} slides")

            # Return the presentation object for reuse
            validation["presentation"] = presentation

        except Exception as e:
            validation["valid"] = False
            validation["errors"].append(f"Cannot open as PowerPoint file: {e}")

        return validation

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PptxReader.load_data "Permanent link")

```
load_data(
    file: Union[, ],
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Parse PowerPoint file with enhanced content extraction.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file`  |  `Union[str, Path]`  |  Path to the PowerPoint file  |  _required_  |  
|  `extra_info`  |  `Optional[Dict]`  |  Additional metadata to include  |  `None`  |  
|  `Optional[AbstractFileSystem]`  |  File system to use for reading  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List of Documents (one per slide)  |  
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/slides/base.py`  
| 
```
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
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
```
 | 
```
defload_data(
    self,
    file: Union[str, Path],
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""
    Parse PowerPoint file with enhanced content extraction.

    Args:
        file: Path to the PowerPoint file
        extra_info: Additional metadata to include
        fs: File system to use for reading

    Returns:
        List of Documents (one per slide)

    """
    logger.debug(f"Loading PPTX file: {file}")
    file_path_str = str(file)

    # Extract content using enhanced extraction
    result = self.extract_with_validation(
        file_path=file_path_str,
        extract_images=self.extract_images,
        context_consolidation_with_llm=self.context_consolidation_with_llm,
        fs=fs,
    )

    if not result["success"] and not self.raise_on_error:
        logger.error(
            f"Failed to extract data from {file_path_str}: {result['errors']}"
        )
        return []
    elif not result["success"] and self.raise_on_error:
        raise ValueError(
            f"Failed to extract data from {file_path_str}: {result['errors']}"
        )

    # Convert to Documents
    docs = []
    for i, slide in enumerate(result["data"]["slides"], start=1):
        # Create rich metadata
        metadata = {
            "file_path": str(file),
            "page_label": i,
            "title": slide.get("title", ""),
            "extraction_errors": slide.get("extraction_errors", []),
            "extraction_warnings": slide.get("extraction_warnings", []),
            "tables": slide.get("tables", []),
            "charts": slide.get("charts", []),
            "notes": slide.get("notes", ""),
            "images": slide.get("images", []),
            "text_sections": slide.get("text_sections", []),
        }
        if extra_info:
            metadata.update(extra_info)

        docs.append(
            Document(
                text=slide["content"],
                metadata=metadata,
                excluded_embed_metadata_keys=list(
                    metadata.keys()
                ),  # excluding the metadata keys from the embedding since the metadata size can potentially be too large and may cause the embedding to fail
                excluded_llm_metadata_keys=list(
                    metadata.keys()
                ),  # excluding the metadata keys from the llm
            )
        )

    logger.debug(f"Successfully loaded {len(docs)} slides from {file}")
    return docs

```
 |  
| --- | --- |  
###  extract_with_validation [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PptxReader.extract_with_validation "Permanent link")

```
extract_with_validation(
    file_path: ,
    extract_images:  = True,
    context_consolidation_with_llm:  = False,
    fs: Optional[AbstractFileSystem] = None,
) -> [, ]

```

Extract content from PowerPoint file with validation and multithreaded processing.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/slides/base.py`  
| 
```
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
```
 | 
```
defextract_with_validation(
    self,
    file_path: str,
    extract_images: bool = True,
    context_consolidation_with_llm: bool = False,
    fs: Optional[AbstractFileSystem] = None,
) -> Dict[str, Any]:
"""Extract content from PowerPoint file with validation and multithreaded processing."""
    result: Dict[str, Any] = {
        "success": False,
        "data": None,
        "errors": [],
        "warnings": [],
        "stats": {},
    }

    # Validate file and get presentation object
    validation = self._validate_file(file_path, fs)
    if not validation.get("valid", False):
        result["errors"] = validation.get("errors", [])
        return result

    # Use the presentation object from validation
    presentation = validation.get("presentation")
    if presentation is None:
        result["errors"].append("Failed to get presentation object from validation")
        return result

    filename = Path(file_path).name
    logger.debug(f"Processing file: {filename}")

    try:
        start_time = datetime.now()
        total_slides = len(presentation.slides)
        logger.debug(f"Processing {total_slides} slides from {filename}")

        # Prepare result structure
        slides_data: list = []

        # Create batches of slide indices
        batches = [
            (i, min(i + self.batch_size, total_slides))
            for i in range(0, total_slides, self.batch_size)
        ]

        # Process in parallel or serial
        if self.num_workers and self.num_workers  0:
            with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                futures = {
                    executor.submit(
                        self._process_batch,
                        presentation,
                        start,
                        end,
                        filename,
                        extract_images,
                        context_consolidation_with_llm,
                    ): (start, end)
                    for start, end in batches
                }
                for fut in as_completed(futures):
                    start, end = futures[fut]
                    try:
                        batch_results = fut.result()
                        slides_data.extend(batch_results)
                    except Exception as e:
                        logger.error(f"Batch {start+1}-{end} failed: {e}")
                        for idx in range(start, end):
                            slides_data.append(
                                {
                                    "slide_number": idx + 1,
                                    "error": str(e),
                                    "partial_extraction": True,
                                }
                            )
                    finally:
                        gc.collect()
        else:
            # Serial fallback
            for start, end in batches:
                slides_data.extend(
                    self._process_batch(
                        presentation,
                        start,
                        end,
                        filename,
                        extract_images,
                        context_consolidation_with_llm,
                    )
                )
                gc.collect()

        # Calculate stats and finalize
        processing_time = (datetime.now() - start_time).total_seconds()
        stats = {
            "total_slides": total_slides,
            "processed_slides": len(slides_data),
            "total_errors": sum(
                1
                for s in slides_data
                if s.get("error") or s.get("extraction_errors")
            ),
            "processing_time_seconds": processing_time,
            "file_size_mb": 0 if fs else os.path.getsize(file_path) / (1024 * 1024),
        }

        result.update(
            {
                "success": True,
                "data": {
                    "filename": filename,
                    "slides": sorted(
                        slides_data, key=lambda s: s.get("slide_number", 0)
                    ),
                    "metadata": {
                        "total_slides": total_slides,
                        "file_path": file_path,
                        "processing_timestamp": datetime.now().isoformat(),
                        "extract_images": extract_images,
                        "context_consolidation_with_llm": context_consolidation_with_llm,
                    },
                },
                "errors": [],
                "stats": stats,
            }
        )

        logger.debug(
            f"Successfully processed {filename}: {stats['processed_slides']} slides "
            f"in {stats['processing_time_seconds']:.2f}s"
        )

        # Cleanup
        del presentation
        gc.collect()

    except Exception as e:
        error_msg = f"Critical error processing {filename}: {e}"
        logger.error(error_msg)
        result["errors"].append(error_msg)

    return result

```
 |  
| --- | --- |  
##  CSVReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.CSVReader "Permanent link")
Bases: 
CSV parser.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `concat_rows`  |  `bool`  |  whether to concatenate all rows into one document. If set to False, a Document will be created for each row. True by default.  |  `True`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/tabular/base.py`  
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
```
 | 
```
classCSVReader(BaseReader):
"""
    CSV parser.

    Args:
        concat_rows (bool): whether to concatenate all rows into one document.
            If set to False, a Document will be created for each row.
            True by default.

    """

    def__init__(self, *args: Any, concat_rows: bool = True, **kwargs: Any) -> None:
"""Init params."""
        super().__init__(*args, **kwargs)
        self._concat_rows = concat_rows

    defload_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
"""
        Parse file.

        Returns:
            Union[str, List[str]]: a string or a List of strings.

        """
        try:
            importcsv
        except ImportError:
            raise ImportError("csv module is required to read CSV files.")
        text_list = []
        with open(file) as fp:
            csv_reader = csv.reader(fp)
            for row in csv_reader:
                text_list.append(", ".join(row))

        metadata = {"filename": file.name, "extension": file.suffix}
        if extra_info:
            metadata = {**metadata, **extra_info}

        if self._concat_rows:
            return [Document(text="\n".join(text_list), metadata=metadata)]
        else:
            return [Document(text=text, metadata=metadata) for text in text_list]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.CSVReader.load_data "Permanent link")

```
load_data(
    file: , extra_info: Optional[] = None
) -> []

```

Parse file.
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  Union[str, List[str]]: a string or a List of strings.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/tabular/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self, file: Path, extra_info: Optional[Dict] = None
) -> List[Document]:
"""
    Parse file.

    Returns:
        Union[str, List[str]]: a string or a List of strings.

    """
    try:
        importcsv
    except ImportError:
        raise ImportError("csv module is required to read CSV files.")
    text_list = []
    with open(file) as fp:
        csv_reader = csv.reader(fp)
        for row in csv_reader:
            text_list.append(", ".join(row))

    metadata = {"filename": file.name, "extension": file.suffix}
    if extra_info:
        metadata = {**metadata, **extra_info}

    if self._concat_rows:
        return [Document(text="\n".join(text_list), metadata=metadata)]
    else:
        return [Document(text=text, metadata=metadata) for text in text_list]

```
 |  
| --- | --- |  
##  PandasCSVReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PandasCSVReader "Permanent link")
Bases: 
Pandas-based CSV parser.
Parses CSVs using the separator detection from Pandas `read_csv`function. If special parameters are required, use the `pandas_config` dict.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `concat_rows`  |  `bool`  |  whether to concatenate all rows into one document. If set to False, a Document will be created for each row. True by default.  |  `True`  |  
|  `col_joiner`  |  Separator to use for joining cols per row. Set to ", " by default.  |  `', '`  |  
|  `row_joiner`  |  Separator to use for joining each row. Only used when `concat_rows=True`. Set to "\n" by default.  |  `'\n'`  |  
|  `pandas_config`  |  `dict`  |  Options for the `pandas.read_csv` function call. Refer to https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html for more information. Set to empty dict by default, this means pandas will try to figure out the separators, table head, etc. on its own.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/tabular/base.py`  
| 
```
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
132
133
```
 | 
```
classPandasCSVReader(BaseReader):
r"""
    Pandas-based CSV parser.

    Parses CSVs using the separator detection from Pandas `read_csv`function.
    If special parameters are required, use the `pandas_config` dict.

    Args:
        concat_rows (bool): whether to concatenate all rows into one document.
            If set to False, a Document will be created for each row.
            True by default.

        col_joiner (str): Separator to use for joining cols per row.
            Set to ", " by default.

        row_joiner (str): Separator to use for joining each row.
            Only used when `concat_rows=True`.
            Set to "\n" by default.

        pandas_config (dict): Options for the `pandas.read_csv` function call.
            Refer to https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
            for more information.
            Set to empty dict by default, this means pandas will try to figure
            out the separators, table head, etc. on its own.

    """

    def__init__(
        self,
        *args: Any,
        concat_rows: bool = True,
        col_joiner: str = ", ",
        row_joiner: str = "\n",
        pandas_config: dict = {},
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__(*args, **kwargs)
        self._concat_rows = concat_rows
        self._col_joiner = col_joiner
        self._row_joiner = row_joiner
        self._pandas_config = pandas_config

    defload_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""Parse file."""
        if fs:
            with fs.open(file) as f:
                df = pd.read_csv(f, **self._pandas_config)
        else:
            df = pd.read_csv(file, **self._pandas_config)

        text_list = df.apply(
            lambda row: (self._col_joiner).join(row.astype(str).tolist()), axis=1
        ).tolist()

        if self._concat_rows:
            return [
                Document(
                    text=(self._row_joiner).join(text_list), metadata=extra_info or {}
                )
            ]
        else:
            return [
                Document(text=text, metadata=extra_info or {}) for text in text_list
            ]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PandasCSVReader.load_data "Permanent link")

```
load_data(
    file: ,
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/tabular/base.py`  
| 
```
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
132
133
```
 | 
```
defload_data(
    self,
    file: Path,
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""Parse file."""
    if fs:
        with fs.open(file) as f:
            df = pd.read_csv(f, **self._pandas_config)
    else:
        df = pd.read_csv(file, **self._pandas_config)

    text_list = df.apply(
        lambda row: (self._col_joiner).join(row.astype(str).tolist()), axis=1
    ).tolist()

    if self._concat_rows:
        return [
            Document(
                text=(self._row_joiner).join(text_list), metadata=extra_info or {}
            )
        ]
    else:
        return [
            Document(text=text, metadata=extra_info or {}) for text in text_list
        ]

```
 |  
| --- | --- |  
##  PandasExcelReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PandasExcelReader "Permanent link")
Bases: 
Custom Excel parser that includes header names in each row.
Parses Excel files using Pandas' `read_excel` function, but formats each row to include the header name, for example: "name: joao, position: analyst". The first row (header) is not included in the generated documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `concat_rows`  |  `bool`  |  Determines whether to concatenate all rows into one document. If set to False, one Document is created for each row. Defaults to True.  |  `True`  |  
|  `sheet_name`  |  `str | int | None`  |  Defaults to None, meaning all sheets. Alternatively, pass a string or an integer to specify the sheet to be read.  |  `None`  |  
|  `field_separator`  |  Character or string to separate each field. Default: ", ".  |  `', '`  |  
|  `key_value_separator`  |  Character or string to separate the key from the value. Default: ": ".  |  `': '`  |  
|  `pandas_config`  |  `dict`  |  Options for the `pandas.read_excel` function call. Refer to https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html for more details. Defaults to an empty dictionary.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/tabular/base.py`  
| 
```
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
```
 | 
```
classPandasExcelReader(BaseReader):
"""
    Custom Excel parser that includes header names in each row.

    Parses Excel files using Pandas' `read_excel` function, but formats
    each row to include the header name, for example: "name: joao, position: analyst".
    The first row (header) is not included in the generated documents.

    Args:
        concat_rows (bool): Determines whether to concatenate all rows into one document.
            If set to False, one Document is created for each row.
            Defaults to True.
        sheet_name (str | int | None): Defaults to None, meaning all sheets.
            Alternatively, pass a string or an integer to specify the sheet to be read.
        field_separator (str): Character or string to separate each field. Default: ", ".
        key_value_separator (str): Character or string to separate the key from the value. Default: ": ".
        pandas_config (dict): Options for the `pandas.read_excel` function call.
            Refer to https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
            for more details.
            Defaults to an empty dictionary.

    """

    def__init__(
        self,
        *args: Any,
        concat_rows: bool = True,
        sheet_name=None,
        field_separator: str = ", ",
        key_value_separator: str = ": ",
        pandas_config: dict = {},
        **kwargs: Any,
    ) -> None:
"""Initializes the parameters."""
        super().__init__(*args, **kwargs)
        self._concat_rows = concat_rows
        self._sheet_name = sheet_name
        self._field_separator = field_separator
        self._key_value_separator = key_value_separator
        self._pandas_config = pandas_config

    defload_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""Parses the file."""
        openpyxl_spec = importlib.util.find_spec("openpyxl")
        if openpyxl_spec is not None:
            pass
        else:
            raise ImportError(
                "Please install openpyxl to read Excel files. You can install it with 'pip install openpyxl'"
            )

        # A sheet_name of None means all sheets; otherwise, indexing starts at 0
        if fs:
            with fs.open(file) as f:
                dfs = pd.read_excel(f, self._sheet_name, **self._pandas_config)
        else:
            dfs = pd.read_excel(file, self._sheet_name, **self._pandas_config)

        documents = []

        # Handle the case where only a single DataFrame is returned
        if isinstance(dfs, pd.DataFrame):
            df = dfs.fillna("")
            # Get the headers/column names
            headers = df.columns.tolist()

            # Convert the DataFrame into a list of rows formatted with header names
            text_list = []

            # Start from index 0 to include all data rows
            # The header is already in 'headers', not in the data rows
            for _, row in df.iterrows():
                # Format each row as "header1: value1, header2: value2, ..."
                formatted_row = self._field_separator.join(
                    [
                        f"{header}{self._key_value_separator}{row[header]!s}"
                        for header in headers
                    ]
                )
                text_list.append(formatted_row)

            if self._concat_rows:
                documents.append(
                    Document(text="\n".join(text_list), metadata=extra_info or {})
                )
            else:
                documents.extend(
                    [
                        Document(text=text, metadata=extra_info or {})
                        for text in text_list
                    ]
                )
        else:
            # Handle multiple sheets
            for df in dfs.values():
                df = df.fillna("")
                headers = df.columns.tolist()

                text_list = []
                for _, row in df.iterrows():
                    formatted_row = self._field_separator.join(
                        [
                            f"{header}{self._key_value_separator}{row[header]!s}"
                            for header in headers
                        ]
                    )
                    text_list.append(formatted_row)

                if self._concat_rows:
                    documents.append(
                        Document(text="\n".join(text_list), metadata=extra_info or {})
                    )
                else:
                    documents.extend(
                        [
                            Document(text=text, metadata=extra_info or {})
                            for text in text_list
                        ]
                    )

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.PandasExcelReader.load_data "Permanent link")

```
load_data(
    file: ,
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Parses the file.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/tabular/base.py`  
| 
```
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
```
 | 
```
defload_data(
    self,
    file: Path,
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""Parses the file."""
    openpyxl_spec = importlib.util.find_spec("openpyxl")
    if openpyxl_spec is not None:
        pass
    else:
        raise ImportError(
            "Please install openpyxl to read Excel files. You can install it with 'pip install openpyxl'"
        )

    # A sheet_name of None means all sheets; otherwise, indexing starts at 0
    if fs:
        with fs.open(file) as f:
            dfs = pd.read_excel(f, self._sheet_name, **self._pandas_config)
    else:
        dfs = pd.read_excel(file, self._sheet_name, **self._pandas_config)

    documents = []

    # Handle the case where only a single DataFrame is returned
    if isinstance(dfs, pd.DataFrame):
        df = dfs.fillna("")
        # Get the headers/column names
        headers = df.columns.tolist()

        # Convert the DataFrame into a list of rows formatted with header names
        text_list = []

        # Start from index 0 to include all data rows
        # The header is already in 'headers', not in the data rows
        for _, row in df.iterrows():
            # Format each row as "header1: value1, header2: value2, ..."
            formatted_row = self._field_separator.join(
                [
                    f"{header}{self._key_value_separator}{row[header]!s}"
                    for header in headers
                ]
            )
            text_list.append(formatted_row)

        if self._concat_rows:
            documents.append(
                Document(text="\n".join(text_list), metadata=extra_info or {})
            )
        else:
            documents.extend(
                [
                    Document(text=text, metadata=extra_info or {})
                    for text in text_list
                ]
            )
    else:
        # Handle multiple sheets
        for df in dfs.values():
            df = df.fillna("")
            headers = df.columns.tolist()

            text_list = []
            for _, row in df.iterrows():
                formatted_row = self._field_separator.join(
                    [
                        f"{header}{self._key_value_separator}{row[header]!s}"
                        for header in headers
                    ]
                )
                text_list.append(formatted_row)

            if self._concat_rows:
                documents.append(
                    Document(text="\n".join(text_list), metadata=extra_info or {})
                )
            else:
                documents.extend(
                    [
                        Document(text=text, metadata=extra_info or {})
                        for text in text_list
                    ]
                )

    return documents

```
 |  
| --- | --- |  
##  UnstructuredReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.UnstructuredReader "Permanent link")
Bases: 
General unstructured text reader for a variety of files.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/unstructured/base.py`  
| 
```
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
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
```
 | 
```
classUnstructuredReader(BaseReader):
"""General unstructured text reader for a variety of files."""

    def__init__(
        self,
        *args: Any,
        api_key: str = None,
        url: str = None,
        allowed_metadata_types: Optional[Tuple] = None,
        excluded_metadata_keys: Optional[Set] = None,
    ) -> None:
"""
        Initialize UnstructuredReader.

        Args:
            *args (Any): Additional arguments passed to the BaseReader.
            api_key (str, optional): API key for accessing the Unstructured.io API. If provided, the reader will use the API for parsing files. Defaults to None.
            url (str, optional): URL for the Unstructured.io API. If not provided and an api_key is given, defaults to "http://localhost:8000". Ignored if api_key is not provided. Defaults to None.
            allowed_metadata_types (Optional[Tuple], optional): Tuple of types that are allowed in the metadata. Defaults to (str, int, float, type(None)).
            excluded_metadata_keys (Optional[Set], optional): Set of metadata keys to exclude from the final document. Defaults to {"orig_elements"}.

        Attributes:
            api_key (str or None): Stores the API key.
            use_api (bool): Indicates whether to use the API for parsing files, based on the presence of the api_key.
            url (str or None): URL for the Unstructured.io API if using the API.
            allowed_metadata_types (Tuple): Tuple of types that are allowed in the metadata.
            excluded_metadata_keys (Set): Set of metadata keys to exclude from the final document.

        """
        super().__init__(*args)  # not passing kwargs to parent bc it cannot accept it

        if Element is None:
            raise ImportError(
                "Unstructured is not installed. Please install it using 'pip install -U unstructured'."
            )

        self.api_key = api_key
        self.use_api = bool(api_key)
        self.url = url or "http://localhost:8000" if self.use_api else None
        self.allowed_metadata_types = allowed_metadata_types or (
            str,
            int,
            float,
            type(None),
        )
        self.excluded_metadata_keys = excluded_metadata_keys or {"orig_elements"}

    @classmethod
    deffrom_api(cls, api_key: str, url: str = None):
"""Set the server url and api key."""
        return cls(api_key, url)

    defload_data(
        self,
        file: Optional[Path] = None,
        unstructured_kwargs: Optional[Dict] = None,
        document_kwargs: Optional[Dict] = None,
        extra_info: Optional[Dict] = None,
        split_documents: Optional[bool] = False,
        excluded_metadata_keys: Optional[List[str]] = None,
    ) -> List[Document]:
"""
        Load data using Unstructured.io.

        Depending on the configuration, if url is set or use_api is True,
        it'll parse the file using an API call, otherwise it parses it locally.
        extra_info is extended by the returned metadata if split_documents is True.

        Args:
            file (Optional[Path]): Path to the file to be loaded.
            unstructured_kwargs (Optional[Dict]): Additional arguments for unstructured partitioning.
            document_kwargs (Optional[Dict]): Additional arguments for document creation.
            extra_info (Optional[Dict]): Extra information to add to the document metadata.
            split_documents (Optional[bool]): Whether to split the documents.
            excluded_metadata_keys (Optional[List[str]]): Keys to exclude from the metadata.

        Returns:
            List[Document]: List of parsed documents.

        """
        unstructured_kwargs = unstructured_kwargs.copy() if unstructured_kwargs else {}

        if (
            unstructured_kwargs.get("file") is not None
            and unstructured_kwargs.get("metadata_filename") is None
        ):
            raise ValueError(
                "Please provide a 'metadata_filename' as part of the 'unstructured_kwargs' when loading a file stream."
            )

        elements: List[Element] = self._partition_elements(unstructured_kwargs, file)

        return self._create_documents(
            elements,
            document_kwargs,
            extra_info,
            split_documents,
            excluded_metadata_keys,
        )

    def_partition_elements(
        self, unstructured_kwargs: Dict, file: Optional[Path] = None
    ) -> List[Element]:
"""
        Partition the elements from the file or via API.

        Args:
            file (Optional[Path]): Path to the file to be loaded.
            unstructured_kwargs (Dict): Additional arguments for unstructured partitioning.

        Returns:
            List[Element]: List of partitioned elements.

        """
        if file:
            unstructured_kwargs["filename"] = str(file)

        if self.use_api:
            fromunstructured.partition.apiimport partition_via_api

            return partition_via_api(
                api_key=self.api_key,
                api_url=self.url + "/general/v0/general",
                **unstructured_kwargs,
            )
        else:
            fromunstructured.partition.autoimport partition

            return partition(**unstructured_kwargs)

    def_create_documents(
        self,
        elements: List[Element],
        document_kwargs: Optional[Dict],
        extra_info: Optional[Dict],
        split_documents: Optional[bool],
        excluded_metadata_keys: Optional[List[str]],
    ) -> List[Document]:
"""
        Create documents from partitioned elements.

        Args:
            elements (List): List of partitioned elements.
            document_kwargs (Optional[Dict]): Additional arguments for document creation.
            extra_info (Optional[Dict]): Extra information to add to the document metadata.
            split_documents (Optional[bool]): Whether to split the documents.
            excluded_metadata_keys (Optional[List[str]]): Keys to exclude from the metadata.

        Returns:
            List[Document]: List of parsed documents.

        """
        doc_kwargs = document_kwargs or {}
        doc_extras = extra_info or {}
        excluded_keys = set(excluded_metadata_keys or self.excluded_metadata_keys)
        docs: List[Document] = []

        def_merge_metadata(
            element: Element, sequence_number: Optional[int] = None
        ) -> Dict[str, Any]:
            candidate_metadata = {**element.metadata.to_dict(), **doc_extras}
            metadata = {
                key: (
                    value
                    if isinstance(value, self.allowed_metadata_types)
                    else json.dumps(value)
                )
                for key, value in candidate_metadata.items()
                if key not in excluded_keys
            }
            if sequence_number is not None:
                metadata["sequence_number"] = sequence_number
            return metadata

        if len(elements) == 0:
            return []

        text_chunks = [" ".join(str(el).split()) for el in elements]
        metadata = _merge_metadata(elements[0])
        filename = metadata.get("file_path", None) or metadata["filename"]
        source = Document(
            text="\n\n".join(text_chunks),
            extra_info=metadata,
            doc_id=filename,
            id_=filename,
            **doc_kwargs,
        )

        if split_documents:
            docs = []
            for sequence_number, element in enumerate(elements):
                hash_id = element.id_to_hash(sequence_number)
                node = TextNode(
                    text=element.text,
                    metadata=_merge_metadata(element, sequence_number),
                    doc_id=hash_id,
                    id_=hash_id,
                    **doc_kwargs,
                )
                node.relationships[NodeRelationship.SOURCE] = (
                    source.as_related_node_info()
                )
                docs.append(node)
        else:
            docs = [source]

        return docs

```
 |  
| --- | --- |  
###  from_api `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.UnstructuredReader.from_api "Permanent link")

```
from_api(api_key: , url:  = None)

```

Set the server url and api key.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/unstructured/base.py`  
| 
```
71
72
73
74
```
 | 
```
@classmethod
deffrom_api(cls, api_key: str, url: str = None):
"""Set the server url and api key."""
    return cls(api_key, url)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.UnstructuredReader.load_data "Permanent link")

```
load_data(
    file: Optional[] = None,
    unstructured_kwargs: Optional[] = None,
    document_kwargs: Optional[] = None,
    extra_info: Optional[] = None,
    split_documents: Optional[] = False,
    excluded_metadata_keys: Optional[[]] = None,
) -> []

```

Load data using Unstructured.io.
Depending on the configuration, if url is set or use_api is True, it'll parse the file using an API call, otherwise it parses it locally. extra_info is extended by the returned metadata if split_documents is True.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file`  |  `Optional[Path]`  |  Path to the file to be loaded.  |  `None`  |  
|  `unstructured_kwargs`  |  `Optional[Dict]`  |  Additional arguments for unstructured partitioning.  |  `None`  |  
|  `document_kwargs`  |  `Optional[Dict]`  |  Additional arguments for document creation.  |  `None`  |  
|  `extra_info`  |  `Optional[Dict]`  |  Extra information to add to the document metadata.  |  `None`  |  
|  `split_documents`  |  `Optional[bool]`  |  Whether to split the documents.  |  `False`  |  
|  `excluded_metadata_keys`  |  `Optional[List[str]]`  |  Keys to exclude from the metadata.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of parsed documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/unstructured/base.py`  
| 
```
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
121
122
```
 | 
```
defload_data(
    self,
    file: Optional[Path] = None,
    unstructured_kwargs: Optional[Dict] = None,
    document_kwargs: Optional[Dict] = None,
    extra_info: Optional[Dict] = None,
    split_documents: Optional[bool] = False,
    excluded_metadata_keys: Optional[List[str]] = None,
) -> List[Document]:
"""
    Load data using Unstructured.io.

    Depending on the configuration, if url is set or use_api is True,
    it'll parse the file using an API call, otherwise it parses it locally.
    extra_info is extended by the returned metadata if split_documents is True.

    Args:
        file (Optional[Path]): Path to the file to be loaded.
        unstructured_kwargs (Optional[Dict]): Additional arguments for unstructured partitioning.
        document_kwargs (Optional[Dict]): Additional arguments for document creation.
        extra_info (Optional[Dict]): Extra information to add to the document metadata.
        split_documents (Optional[bool]): Whether to split the documents.
        excluded_metadata_keys (Optional[List[str]]): Keys to exclude from the metadata.

    Returns:
        List[Document]: List of parsed documents.

    """
    unstructured_kwargs = unstructured_kwargs.copy() if unstructured_kwargs else {}

    if (
        unstructured_kwargs.get("file") is not None
        and unstructured_kwargs.get("metadata_filename") is None
    ):
        raise ValueError(
            "Please provide a 'metadata_filename' as part of the 'unstructured_kwargs' when loading a file stream."
        )

    elements: List[Element] = self._partition_elements(unstructured_kwargs, file)

    return self._create_documents(
        elements,
        document_kwargs,
        extra_info,
        split_documents,
        excluded_metadata_keys,
    )

```
 |  
| --- | --- |  
##  VideoAudioReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.VideoAudioReader "Permanent link")
Bases: 
Video audio parser.
Extract text from transcript of video/audio files.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/video_audio/base.py`  
| 
```
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
```
 | 
```
classVideoAudioReader(BaseReader):
"""
    Video audio parser.

    Extract text from transcript of video/audio files.

    """

    def__init__(self, *args: Any, model_version: str = "base", **kwargs: Any) -> None:
"""Init parser."""
        super().__init__(*args, **kwargs)
        self._model_version = model_version

        try:
            importwhisper
        except ImportError:
            raise ImportError(
                "Please install OpenAI whisper model "
                "'pip install git+https://github.com/openai/whisper.git' "
                "to use the model"
            )

        model = whisper.load_model(self._model_version)

        self.parser_config = {"model": model}

    defload_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
"""Parse file."""
        importwhisper

        if file.name.endswith("mp4"):
            try:
                frompydubimport AudioSegment
            except ImportError:
                raise ImportError("Please install pydub 'pip install pydub' ")
            if fs:
                with fs.open(file, "rb") as f:
                    video = AudioSegment.from_file(f, format="mp4")
            else:
                # open file
                video = AudioSegment.from_file(file, format="mp4")

            # Extract audio from video
            audio = video.split_to_mono()[0]

            file_str = str(file)[:-4] + ".mp3"
            # export file
            audio.export(file_str, format="mp3")

        model = cast(whisper.Whisper, self.parser_config["model"])
        result = model.transcribe(str(file))

        transcript = result["text"]

        return [Document(text=transcript, metadata=extra_info or {})]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.VideoAudioReader.load_data "Permanent link")

```
load_data(
    file: ,
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/video_audio/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    file: Path,
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> List[Document]:
"""Parse file."""
    importwhisper

    if file.name.endswith("mp4"):
        try:
            frompydubimport AudioSegment
        except ImportError:
            raise ImportError("Please install pydub 'pip install pydub' ")
        if fs:
            with fs.open(file, "rb") as f:
                video = AudioSegment.from_file(f, format="mp4")
        else:
            # open file
            video = AudioSegment.from_file(file, format="mp4")

        # Extract audio from video
        audio = video.split_to_mono()[0]

        file_str = str(file)[:-4] + ".mp3"
        # export file
        audio.export(file_str, format="mp3")

    model = cast(whisper.Whisper, self.parser_config["model"])
    result = model.transcribe(str(file))

    transcript = result["text"]

    return [Document(text=transcript, metadata=extra_info or {})]

```
 |  
| --- | --- |  
##  XMLReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.XMLReader "Permanent link")
Bases: 
XML reader.
Reads XML documents with options to help suss out relationships between nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `tree_level_split`  |  From which level in the xml tree we split documents,  |  
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/xml/base.py`  
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
```
 | 
```
classXMLReader(BaseReader):
"""
    XML reader.

    Reads XML documents with options to help suss out relationships between nodes.

    Args:
        tree_level_split (int): From which level in the xml tree we split documents,
        the default level is the root which is level 0

    """

    def__init__(self, tree_level_split: Optional[int] = 0) -> None:
"""Initialize with arguments."""
        super().__init__()
        self.tree_level_split = tree_level_split

    def_parse_xmlelt_to_document(
        self, root: _XmlET.Element, extra_info: Optional[Dict] = None
    ) -> List[Document]:
"""
        Parse the xml object into a list of Documents.

        Args:
            root: The XML Element to be converted.
            extra_info (Optional[Dict]): Additional information. Default is None.

        Returns:
            Document: The documents.

        """
        nodes = _get_leaf_nodes_up_to_level(root, self.tree_level_split)
        documents = []
        for node in nodes:
            content = ET.tostring(node, encoding="utf8").decode("utf-8")
            content = re.sub(r"^<\?xml.*", "", content)
            content = content.strip()
            documents.append(Document(text=content, extra_info=extra_info or {}))

        return documents

    defload_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
    ) -> List[Document]:
"""
        Load data from the input file.

        Args:
            file (Path): Path to the input file.
            extra_info (Optional[Dict]): Additional information. Default is None.

        Returns:
            List[Document]: List of documents.

        """
        if not isinstance(file, Path):
            file = Path(file)

        tree = ET.parse(file)
        return self._parse_xmlelt_to_document(tree.getroot(), extra_info)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/file/#llama_index.readers.file.XMLReader.load_data "Permanent link")

```
load_data(
    file: , extra_info: Optional[] = None
) -> []

```

Load data from the input file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file`  |  `Path`  |  Path to the input file.  |  _required_  |  
|  `extra_info`  |  `Optional[Dict]`  |  Additional information. Default is None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/xml/base.py`  
| 
```
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
defload_data(
    self,
    file: Path,
    extra_info: Optional[Dict] = None,
) -> List[Document]:
"""
    Load data from the input file.

    Args:
        file (Path): Path to the input file.
        extra_info (Optional[Dict]): Additional information. Default is None.

    Returns:
        List[Document]: List of documents.

    """
    if not isinstance(file, Path):
        file = Path(file)

    tree = ET.parse(file)
    return self._parse_xmlelt_to_document(tree.getroot(), extra_info)

```
 |  
| --- | --- |  
options: members: - CSVReader - DocxReader - EpubReader - FlatReader - HTMLTagReader - HWPReader - IPYNBReader - ImageCaptionReader - ImageReader - ImageTabularChartReader - ImageVisionLLMReader - MarkdownReader - MboxReader - PDFReader - PagedCSVReader - PandasCSVReader - PandasExcelReader - PptxReader - PyMuPDFReader - RTFReader - UnstructuredReader - VideoAudioReader - XMLReader
