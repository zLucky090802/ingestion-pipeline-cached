# Pdf table
##  PDFTableReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pdf_table/#llama_index.readers.pdf_table.PDFTableReader "Permanent link")
Bases: 
PDF Table Reader. Reads table from PDF.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `row_separator`  |  Row separator used to join rows of a DataFrame.  |  `'\n'`  |  
|  `col_separator`  |  Col separator used to join columns of a DataFrame.  |  `', '`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-pdf-table/llama_index/readers/pdf_table/base.py`  
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
```
 | 
```
classPDFTableReader(BaseReader):
"""
    PDF Table Reader. Reads table from PDF.

    Args:
        row_separator (str): Row separator used to join rows of a DataFrame.
        col_separator (str): Col separator used to join columns of a DataFrame.

    """

    def__init__(
        self,
        *args: Any,
        row_separator: str = "\n",
        col_separator: str = ", ",
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._row_separator = row_separator
        self._col_separator = col_separator

    defload_data(
        self, file: Path, pages: str = "1", extra_info: Optional[Dict] = None
    ) -> List[Document]:
"""
        Load data and extract table from PDF file.

        Args:
            file (Path): Path for the PDF file.
            pages (str): Pages to read tables from.
            extra_info (Optional[Dict]): Extra information.

        Returns:
            List[Document]: List of documents.

        """
        importcamelot

        results = []
        tables = camelot.read_pdf(filepath=str(file), pages=pages)

        for table in tables:
            document = self._dataframe_to_document(df=table.df, extra_info=extra_info)
            results.append(document)

        return results

    def_dataframe_to_document(
        self, df: pd.DataFrame, extra_info: Optional[Dict] = None
    ) -> Document:
        df_list = df.apply(
            lambda row: (self._col_separator).join(row.astype(str).tolist()), axis=1
        ).tolist()

        return Document(
            text=self._row_separator.join(df_list), extra_info=extra_info or {}
        )

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pdf_table/#llama_index.readers.pdf_table.PDFTableReader.load_data "Permanent link")

```
load_data(
    file: ,
    pages:  = "1",
    extra_info: Optional[] = None,
) -> []

```

Load data and extract table from PDF file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file`  |  `Path`  |  Path for the PDF file.  |  _required_  |  
|  `pages`  |  Pages to read tables from.  |  `'1'`  |  
|  `extra_info`  |  `Optional[Dict]`  |  Extra information.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-pdf-table/llama_index/readers/pdf_table/base.py`  
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
```
 | 
```
defload_data(
    self, file: Path, pages: str = "1", extra_info: Optional[Dict] = None
) -> List[Document]:
"""
    Load data and extract table from PDF file.

    Args:
        file (Path): Path for the PDF file.
        pages (str): Pages to read tables from.
        extra_info (Optional[Dict]): Extra information.

    Returns:
        List[Document]: List of documents.

    """
    importcamelot

    results = []
    tables = camelot.read_pdf(filepath=str(file), pages=pages)

    for table in tables:
        document = self._dataframe_to_document(df=table.df, extra_info=extra_info)
        results.append(document)

    return results

```
 |  
| --- | --- |  
options: members: - PDFTableReader
