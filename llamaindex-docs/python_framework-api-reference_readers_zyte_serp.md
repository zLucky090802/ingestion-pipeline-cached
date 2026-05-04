# Zyte serp
##  ZyteSerpReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/zyte_serp/#llama_index.readers.zyte_serp.ZyteSerpReader "Permanent link")
Bases: 
Get google search results URLs for a search query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  Zyte API key.  |  _required_  |  
|  `extract_from`  |  `Optional[str]`  |  Determines the mode while extracting the search results. It can take one of the following values: 'httpResponseBody', 'browserHtml'  |  `None`  |  
Example
.. code-block:: python

```
from llama_index.readers.zyte_serp import ZyteSerpReader

reader = ZyteSerpReader(
   api_key="ZYTE_API_KEY",
)
docs = reader.load_data(
    "search query",
)

```
Zyte-API reference
https://docs.zyte.com/zyte-api/get-started.html
Source code in `llama-index-integrations/readers/llama-index-readers-zyte-serp/llama_index/readers/zyte_serp/base.py`  
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
```
 | 
```
classZyteSerpReader(BasePydanticReader):
"""
    Get google search results URLs for a search query.

    Args:
        api_key: Zyte API key.
        extract_from: Determines the mode while extracting the search results.
            It can take one of the following values: 'httpResponseBody', 'browserHtml'

    Example:
        .. code-block:: python

            from llama_index.readers.zyte_serp import ZyteSerpReader

            reader = ZyteSerpReader(
               api_key="ZYTE_API_KEY",

            docs = reader.load_data(
                "search query",


    Zyte-API reference:
        https://docs.zyte.com/zyte-api/get-started.html

    """

    client: ZyteAPI
    api_key: str
    extract_from: Optional[str]

    def__init__(
        self,
        api_key: str,
        extract_from: Optional[str] = None,
    ) -> None:
"""Initialize with file path."""
        user_agent = f"llama-index-zyte-api/{PYTHON_ZYTE_API_USER_AGENT}"

        client = ZyteAPI(
            api_key=api_key,
            user_agent=user_agent,
        )

        super().__init__(
            api_key=api_key,
            extract_from=extract_from,
            client=client,
        )

    def_serp_url(self, query: str):
        fromurllib.parseimport quote_plus

        base_url = "https://www.google.com/search?q="
        return base_url + quote_plus(query)

    defload_data(self, query: str):
        serp_url = self._serp_url(query)
        serp_request = {
            "url": serp_url,
            "serp": True,
        }
        if self.extract_from:
            serp_request.update({"serpOptions": {"extractFrom": self.extract_from}})
        results = self.client.get(serp_request)
        docs = []
        for result in results["serp"]["organicResults"]:
            doc = Document(
                text=result["url"],
                metadata={"name": result["name"], "rank": result["rank"]},
            )
            docs.append(doc)
        return docs

```
 |  
| --- | --- |  
options: members: - ZyteSerpReader
