# Pdf marker
##  PDFMarkerReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pdf_marker/#llama_index.readers.pdf_marker.PDFMarkerReader "Permanent link")
Bases: 
PDF Marker Reader. Reads a pdf to markdown format and tables with layout.
Source code in `llama-index-integrations/readers/llama-index-readers-pdf-marker/llama_index/readers/pdf_marker/base.py`  
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
```
 | 
```
classPDFMarkerReader(BaseReader):
"""
    PDF Marker Reader. Reads a pdf to markdown format and tables with layout.
    """

    def__init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    defload_data(
        self,
        file: Path,
        max_pages: int = None,
        langs: List[str] = None,
        batch_multiplier: int = 2,
        start_page: int = None,
        extra_info: Optional[Dict] = None,
    ) -> List[Document]:
"""
        Load data from PDF
        Args:
            file (Path): Path for the PDF file.
            max_pages (int): is the maximum number of pages to process. Omit this to convert the entire document.
            langs (List[str]): List of languages to use for OCR. See supported languages : https://github.com/VikParuchuri/surya/blob/master/surya/languages.py
            batch_multiplier (int): is how much to multiply default batch sizes by if you have extra VRAM. Higher numbers will take more VRAM, but process faster. Set to 2 by default. The default batch sizes will take ~3GB of VRAM.
            start_page (int): Start page for conversion.

        Returns:
            List[Document]: List of documents.

        """
        frommarker.convertimport convert_single_pdf
        frommarker.modelsimport load_all_models

        model_lst = load_all_models()
        full_text, images, out_meta = convert_single_pdf(
            str(file),
            model_lst,
            max_pages=max_pages,
            langs=langs,
            batch_multiplier=batch_multiplier,
            start_page=start_page,
        )

        doc = Document(text=full_text, extra_info=extra_info or {})

        return [doc]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pdf_marker/#llama_index.readers.pdf_marker.PDFMarkerReader.load_data "Permanent link")

```
load_data(
    file: ,
    max_pages:  = None,
    langs: [] = None,
    batch_multiplier:  = 2,
    start_page:  = None,
    extra_info: Optional[] = None,
) -> []

```

Load data from PDF Args: file (Path): Path for the PDF file. max_pages (int): is the maximum number of pages to process. Omit this to convert the entire document. langs (List[str]): List of languages to use for OCR. See supported languages : https://github.com/VikParuchuri/surya/blob/master/surya/languages.py batch_multiplier (int): is how much to multiply default batch sizes by if you have extra VRAM. Higher numbers will take more VRAM, but process faster. Set to 2 by default. The default batch sizes will take ~3GB of VRAM. start_page (int): Start page for conversion.
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-pdf-marker/llama_index/readers/pdf_marker/base.py`  
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
```
 | 
```
defload_data(
    self,
    file: Path,
    max_pages: int = None,
    langs: List[str] = None,
    batch_multiplier: int = 2,
    start_page: int = None,
    extra_info: Optional[Dict] = None,
) -> List[Document]:
"""
    Load data from PDF
    Args:
        file (Path): Path for the PDF file.
        max_pages (int): is the maximum number of pages to process. Omit this to convert the entire document.
        langs (List[str]): List of languages to use for OCR. See supported languages : https://github.com/VikParuchuri/surya/blob/master/surya/languages.py
        batch_multiplier (int): is how much to multiply default batch sizes by if you have extra VRAM. Higher numbers will take more VRAM, but process faster. Set to 2 by default. The default batch sizes will take ~3GB of VRAM.
        start_page (int): Start page for conversion.

    Returns:
        List[Document]: List of documents.

    """
    frommarker.convertimport convert_single_pdf
    frommarker.modelsimport load_all_models

    model_lst = load_all_models()
    full_text, images, out_meta = convert_single_pdf(
        str(file),
        model_lst,
        max_pages=max_pages,
        langs=langs,
        batch_multiplier=batch_multiplier,
        start_page=start_page,
    )

    doc = Document(text=full_text, extra_info=extra_info or {})

    return [doc]

```
 |  
| --- | --- |  
options: members: - PDFMarkerReader
