# Intercom
##  IntercomReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/intercom/#llama_index.readers.intercom.IntercomReader "Permanent link")
Bases: 
Intercom reader. Reads data from a Intercom workspace.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `personal_access_token`  |  Intercom token.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-intercom/llama_index/readers/intercom/base.py`  
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
```
 | 
```
classIntercomReader(BaseReader):
"""
    Intercom reader. Reads data from a Intercom workspace.

    Args:
        personal_access_token (str): Intercom token.

    """

    def__init__(self, intercom_access_token: str) -> None:
"""Initialize Intercom reader."""
        self.intercom_access_token = intercom_access_token

    defload_data(self) -> List[Document]:
"""
        Load data from the workspace.

        Args:
            workspace_id (str): Workspace ID.


        Returns:
            List[Document]: List of documents.

        """
        frombs4import BeautifulSoup

        results = []

        articles = self.get_all_articles()

        for article in articles:
            body = article["body"]
            soup = BeautifulSoup(body, "html.parser")
            body = soup.get_text()

            extra_info = {
                "id": article["id"],
                "title": article["title"],
                "url": article["url"],
                "updated_at": article["updated_at"],
            }

            results.append(
                Document(
                    text=body,
                    extra_info=extra_info or {},
                )
            )

        return results

    defget_all_articles(self):
        articles = []
        next_page = None

        while True:
            response = self.get_articles_page(next_page)
            articles.extend(response["articles"])
            next_page = response["next_page"]

            if next_page is None:
                break

        return articles

    defget_articles_page(self, next_page: str = None):
        importrequests

        if next_page is None:
            url = "https://api.intercom.io/articles"
        else:
            url = next_page

        headers = {
            "accept": "application/json",
            "Intercom-Version": "2.8",
            "authorization": f"Bearer {self.intercom_access_token}",
        }

        response = requests.get(url, headers=headers)

        response_json = json.loads(response.text)

        next_page = response_json.get("pages", {}).get("next", None)

        articles = response_json.get("data", [])

        return {"articles": articles, "next_page": next_page}

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/intercom/#llama_index.readers.intercom.IntercomReader.load_data "Permanent link")

```
load_data() -> []

```

Load data from the workspace.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `workspace_id`  |  Workspace ID.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-intercom/llama_index/readers/intercom/base.py`  
| 
```
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
defload_data(self) -> List[Document]:
"""
    Load data from the workspace.

    Args:
        workspace_id (str): Workspace ID.


    Returns:
        List[Document]: List of documents.

    """
    frombs4import BeautifulSoup

    results = []

    articles = self.get_all_articles()

    for article in articles:
        body = article["body"]
        soup = BeautifulSoup(body, "html.parser")
        body = soup.get_text()

        extra_info = {
            "id": article["id"],
            "title": article["title"],
            "url": article["url"],
            "updated_at": article["updated_at"],
        }

        results.append(
            Document(
                text=body,
                extra_info=extra_info or {},
            )
        )

    return results

```
 |  
| --- | --- |  
options: members: - IntercomReader
