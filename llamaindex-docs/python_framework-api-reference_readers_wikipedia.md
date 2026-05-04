# Wikipedia
##  WikipediaReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/wikipedia/#llama_index.readers.wikipedia.WikipediaReader "Permanent link")
Bases: 
Wikipedia reader.
Reads a page.
Source code in `llama-index-integrations/readers/llama-index-readers-wikipedia/llama_index/readers/wikipedia/base.py`  
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
```
 | 
```
classWikipediaReader(BasePydanticReader):
"""
    Wikipedia reader.

    Reads a page.

    """

    is_remote: bool = True

    def__init__(self) -> None:
"""Initialize with parameters."""
        try:
            importwikipedia  # noqa
        except ImportError:
            raise ImportError(
                "`wikipedia` package not found, please run `pip install wikipedia`"
            )

    @classmethod
    defclass_name(cls) -> str:
        return "WikipediaReader"

    defload_data(
        self, pages: List[str], lang_prefix: str = "en", **load_kwargs: Any
    ) -> List[Document]:
"""
        Load data from the input directory.

        Args:
            pages (List[str]): List of pages to read.
            lang_prefix (str): Language prefix for Wikipedia. Defaults to English. Valid Wikipedia language codes
            can be found at https://en.wikipedia.org/wiki/List_of_Wikipedias.

        """
        importwikipedia

        if lang_prefix.lower() != "en":
            if lang_prefix.lower() in wikipedia.languages():
                wikipedia.set_lang(lang_prefix.lower())
            else:
                raise ValueError(
                    f"Language prefix '{lang_prefix}' for Wikipedia is not supported. Check supported languages at https://en.wikipedia.org/wiki/List_of_Wikipedias."
                )

        results = []
        for page in pages:
            wiki_page = wikipedia.page(page, **load_kwargs)
            page_content = wiki_page.content
            page_id = wiki_page.pageid
            results.append(Document(id_=page_id, text=page_content))
        return results

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/wikipedia/#llama_index.readers.wikipedia.WikipediaReader.load_data "Permanent link")

```
load_data(
    pages: [],
    lang_prefix:  = "en",
    **load_kwargs: 
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `pages`  |  `List[str]`  |  List of pages to read.  |  _required_  |  
|  `lang_prefix`  |  Language prefix for Wikipedia. Defaults to English. Valid Wikipedia language codes  |  `'en'`  |  
|  `can be found at https`  |  //en.wikipedia.org/wiki/List_of_Wikipedias.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-wikipedia/llama_index/readers/wikipedia/base.py`  
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
```
 | 
```
defload_data(
    self, pages: List[str], lang_prefix: str = "en", **load_kwargs: Any
) -> List[Document]:
"""
    Load data from the input directory.

    Args:
        pages (List[str]): List of pages to read.
        lang_prefix (str): Language prefix for Wikipedia. Defaults to English. Valid Wikipedia language codes
        can be found at https://en.wikipedia.org/wiki/List_of_Wikipedias.

    """
    importwikipedia

    if lang_prefix.lower() != "en":
        if lang_prefix.lower() in wikipedia.languages():
            wikipedia.set_lang(lang_prefix.lower())
        else:
            raise ValueError(
                f"Language prefix '{lang_prefix}' for Wikipedia is not supported. Check supported languages at https://en.wikipedia.org/wiki/List_of_Wikipedias."
            )

    results = []
    for page in pages:
        wiki_page = wikipedia.page(page, **load_kwargs)
        page_content = wiki_page.content
        page_id = wiki_page.pageid
        results.append(Document(id_=page_id, text=page_content))
    return results

```
 |  
| --- | --- |  
options: members: - WikipediaReader
