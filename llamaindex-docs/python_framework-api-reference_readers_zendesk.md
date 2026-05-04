# Zendesk
##  ZendeskReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/zendesk/#llama_index.readers.zendesk.ZendeskReader "Permanent link")
Bases: 
Zendesk reader. Reads data from a Zendesk workspace.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `zendesk_subdomain`  |  Zendesk subdomain  |  _required_  |  
|  `locale`  |  Locale of articles  |  `'en-us'`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-zendesk/llama_index/readers/zendesk/base.py`  
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
```
 | 
```
classZendeskReader(BaseReader):
"""
    Zendesk reader. Reads data from a Zendesk workspace.

    Args:
        zendesk_subdomain (str): Zendesk subdomain
        locale (str): Locale of articles

    """

    def__init__(self, zendesk_subdomain: str, locale: str = "en-us") -> None:
"""Initialize Zendesk reader."""
        self.zendesk_subdomain = zendesk_subdomain
        self.locale = locale

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
            if body is None:
                continue
            soup = BeautifulSoup(body, "html.parser")
            body = soup.get_text()
            extra_info = {
                "id": article["id"],
                "title": article["title"],
                "url": article["html_url"],
                "updated_at": article["updated_at"],
            }

            results.append(
                Document(
                    text=body,
                    extra_info=extra_info,
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
            url = f"https://{self.zendesk_subdomain}.zendesk.com/api/v2/help_center/{self.locale}/articles?per_page=100"
        else:
            url = next_page

        response = requests.get(url)

        response_json = json.loads(response.text)

        next_page = response_json.get("next_page", None)

        articles = response_json.get("articles", [])

        return {"articles": articles, "next_page": next_page}

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/zendesk/#llama_index.readers.zendesk.ZendeskReader.load_data "Permanent link")

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
Source code in `llama-index-integrations/readers/llama-index-readers-zendesk/llama_index/readers/zendesk/base.py`  
| 
```
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
        if body is None:
            continue
        soup = BeautifulSoup(body, "html.parser")
        body = soup.get_text()
        extra_info = {
            "id": article["id"],
            "title": article["title"],
            "url": article["html_url"],
            "updated_at": article["updated_at"],
        }

        results.append(
            Document(
                text=body,
                extra_info=extra_info,
            )
        )

    return results

```
 |  
| --- | --- |  
options: members: - ZendeskReader
