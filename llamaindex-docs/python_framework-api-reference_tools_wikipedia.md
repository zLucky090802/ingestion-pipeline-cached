# Wikipedia
##  WikipediaToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/wikipedia/#llama_index.tools.wikipedia.WikipediaToolSpec "Permanent link")
Bases: 
Specifies two tools for querying information from Wikipedia.
Source code in `llama-index-integrations/tools/llama-index-tools-wikipedia/llama_index/tools/wikipedia/base.py`  
| 
```
 6
 7
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
```
 | 
```
classWikipediaToolSpec(BaseToolSpec):
"""
    Specifies two tools for querying information from Wikipedia.
    """

    spec_functions = ["load_data", "search_data"]

    defload_data(self, page: str, lang: str = "en") -> str:
"""
        Retrieve a Wikipedia page. Useful for learning about a particular concept that isn't private information.

        Args:
            page (str): Title of the page to read.
            lang (str): Language of Wikipedia to read. (default: English)

        """
        importwikipedia

        wikipedia.set_lang(lang)
        try:
            wikipedia_page = wikipedia.page(page, auto_suggest=False)
        except wikipedia.PageError:
            return "Unable to load page. Try searching instead."
        return wikipedia_page.content

    defsearch_data(self, query: str, lang: str = "en") -> str:
"""
        Search Wikipedia for a page related to the given query.
        Use this tool when `load_data` returns no results.

        Args:
            query (str): the string to search for

        """
        importwikipedia

        pages = wikipedia.search(query)
        if len(pages) == 0:
            return "No search results."
        return self.load_data(pages[0], lang)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/wikipedia/#llama_index.tools.wikipedia.WikipediaToolSpec.load_data "Permanent link")

```
load_data(page: , lang:  = 'en') -> 

```

Retrieve a Wikipedia page. Useful for learning about a particular concept that isn't private information.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `page`  |  Title of the page to read.  |  _required_  |  
|  `lang`  |  Language of Wikipedia to read. (default: English)  |  `'en'`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-wikipedia/llama_index/tools/wikipedia/base.py`  
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
```
 | 
```
defload_data(self, page: str, lang: str = "en") -> str:
"""
    Retrieve a Wikipedia page. Useful for learning about a particular concept that isn't private information.

    Args:
        page (str): Title of the page to read.
        lang (str): Language of Wikipedia to read. (default: English)

    """
    importwikipedia

    wikipedia.set_lang(lang)
    try:
        wikipedia_page = wikipedia.page(page, auto_suggest=False)
    except wikipedia.PageError:
        return "Unable to load page. Try searching instead."
    return wikipedia_page.content

```
 |  
| --- | --- |  
###  search_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/wikipedia/#llama_index.tools.wikipedia.WikipediaToolSpec.search_data "Permanent link")

```
search_data(query: , lang:  = 'en') -> 

```

Search Wikipedia for a page related to the given query. Use this tool when `load_data` returns no results.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  the string to search for  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-wikipedia/llama_index/tools/wikipedia/base.py`  
| 
```
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
```
 | 
```
defsearch_data(self, query: str, lang: str = "en") -> str:
"""
    Search Wikipedia for a page related to the given query.
    Use this tool when `load_data` returns no results.

    Args:
        query (str): the string to search for

    """
    importwikipedia

    pages = wikipedia.search(query)
    if len(pages) == 0:
        return "No search results."
    return self.load_data(pages[0], lang)

```
 |  
| --- | --- |  
options: members: - WikipediaToolSpec
