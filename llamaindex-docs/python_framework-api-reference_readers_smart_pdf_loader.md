# Smart pdf loader
##  SmartPDFLoader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/smart_pdf_loader/#llama_index.readers.smart_pdf_loader.SmartPDFLoader "Permanent link")
Bases: 
SmartPDFLoader uses nested layout information such as sections, paragraphs, lists and tables to smartly chunk PDFs for optimal usage of LLM context window.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `llmsherpa_api_url`  |  Address of the service hosting llmsherpa PDF parser  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-smart-pdf-loader/llama_index/readers/smart_pdf_loader/base.py`  
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
```
 | 
```
classSmartPDFLoader(BaseReader):
"""
    SmartPDFLoader uses nested layout information such as sections, paragraphs, lists and tables to smartly chunk PDFs for optimal usage of LLM context window.

    Args:
        llmsherpa_api_url (str): Address of the service hosting llmsherpa PDF parser

    """

    def__init__(
        self, *args: Any, llmsherpa_api_url: str = None, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        fromllmsherpa.readersimport LayoutPDFReader

        self.pdf_reader = LayoutPDFReader(llmsherpa_api_url)

    defload_data(
        self, pdf_path_or_url: str, extra_info: Optional[Dict] = None
    ) -> List[Document]:
"""
        Load data and extract table from PDF file.

        Args:
            pdf_path_or_url (str): A url or file path pointing to the PDF

        Returns:
            List[Document]: List of documents.

        """
        results = []
        doc = self.pdf_reader.read_pdf(str(pdf_path_or_url))
        for chunk in doc.chunks():
            document = Document(
                text=chunk.to_context_text(),
                extra_info={**extra_info, "chunk_type": chunk.tag}
                if extra_info
                else {"chunk_type": chunk.tag},
            )
            results.append(document)
        return results

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/smart_pdf_loader/#llama_index.readers.smart_pdf_loader.SmartPDFLoader.load_data "Permanent link")

```
load_data(
    pdf_path_or_url: , extra_info: Optional[] = None
) -> []

```

Load data and extract table from PDF file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `pdf_path_or_url`  |  A url or file path pointing to the PDF  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-smart-pdf-loader/llama_index/readers/smart_pdf_loader/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self, pdf_path_or_url: str, extra_info: Optional[Dict] = None
) -> List[Document]:
"""
    Load data and extract table from PDF file.

    Args:
        pdf_path_or_url (str): A url or file path pointing to the PDF

    Returns:
        List[Document]: List of documents.

    """
    results = []
    doc = self.pdf_reader.read_pdf(str(pdf_path_or_url))
    for chunk in doc.chunks():
        document = Document(
            text=chunk.to_context_text(),
            extra_info={**extra_info, "chunk_type": chunk.tag}
            if extra_info
            else {"chunk_type": chunk.tag},
        )
        results.append(document)
    return results

```
 |  
| --- | --- |  
options: members: - SmartPDFLoader
