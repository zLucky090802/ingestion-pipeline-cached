# Memos
Init file.
##  MemosReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/memos/#llama_index.readers.memos.MemosReader "Permanent link")
Bases: 
Memos reader.
Reads content from an Memos.
Source code in `llama-index-integrations/readers/llama-index-readers-memos/llama_index/readers/memos/base.py`  
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
```
 | 
```
classMemosReader(BaseReader):
"""
    Memos reader.

    Reads content from an Memos.

    """

    def__init__(self, host: str = "https://demo.usememos.com/") -> None:
"""Init params."""
        self._memoUrl = urljoin(host, "api/memo")

    defload_data(self, params: Dict = {}) -> List[Document]:
"""
        Load data from RSS feeds.

        Args:
            params (Dict): Filtering parameters.

        Returns:
            List[Document]: List of documents.

        """
        importrequests

        documents = []
        realUrl = self._memoUrl

        if not params:
            realUrl = urljoin(self._memoUrl, "all", False)

        try:
            req = requests.get(realUrl, params)
            res = req.json()
        except ValueError:
            raise ValueError("Your Memo URL is not valid")

        if "data" not in res:
            raise ValueError("Invalid Memo response")

        memos = res["data"]
        for memo in memos:
            content = memo["content"]
            extra_info = {
                "creator": memo["creator"],
                "resource_list": memo["resourceList"],
                id: memo["id"],
            }
            documents.append(Document(text=content, extra_info=extra_info))

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/memos/#llama_index.readers.memos.MemosReader.load_data "Permanent link")

```
load_data(params:  = {}) -> []

```

Load data from RSS feeds.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `params`  |  `Dict`  |  Filtering parameters.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-memos/llama_index/readers/memos/base.py`  
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
```
 | 
```
defload_data(self, params: Dict = {}) -> List[Document]:
"""
    Load data from RSS feeds.

    Args:
        params (Dict): Filtering parameters.

    Returns:
        List[Document]: List of documents.

    """
    importrequests

    documents = []
    realUrl = self._memoUrl

    if not params:
        realUrl = urljoin(self._memoUrl, "all", False)

    try:
        req = requests.get(realUrl, params)
        res = req.json()
    except ValueError:
        raise ValueError("Your Memo URL is not valid")

    if "data" not in res:
        raise ValueError("Invalid Memo response")

    memos = res["data"]
    for memo in memos:
        content = memo["content"]
        extra_info = {
            "creator": memo["creator"],
            "resource_list": memo["resourceList"],
            id: memo["id"],
        }
        documents.append(Document(text=content, extra_info=extra_info))

    return documents

```
 |  
| --- | --- |  
options: members: - MemosReader
