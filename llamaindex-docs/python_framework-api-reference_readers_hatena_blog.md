# Hatena blog
##  HatenaBlogReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/hatena_blog/#llama_index.readers.hatena_blog.HatenaBlogReader "Permanent link")
Bases: 
Hatena Blog reader.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `root_endpoint`  |  AtomPub root endpoint.  |  _required_  |  
|  `api_key`  |  AtomPub API Key  |  _required_  |  
|  `username`  |  Hatena ID  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-hatena-blog/llama_index/readers/hatena_blog/base.py`  
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
```
 | 
```
classHatenaBlogReader(BaseReader):
"""
    Hatena Blog reader.

    Args:
        root_endpoint (str): AtomPub root endpoint.
        api_key (str): AtomPub API Key
        username (str): Hatena ID

    """

    def__init__(self, root_endpoint: str, api_key: str, username: str) -> None:
"""Initialize Hatena Blog reader."""
        self.root_endpoint = root_endpoint
        self.api_key = api_key
        self.username = username

    defload_data(self) -> List[Document]:
        results = []
        articles = self.get_all_articles()
        for a in articles:
            results.append(
                Document(
                    text=a.content,
                    extra_info={
                        "title": a.title,
                        "published": a.published,
                        "url": a.url,
                    },
                )
            )

        return results

    defget_all_articles(self) -> List[Article]:
        articles: List[Article] = []
        page_url = ATOM_PUB_ENTRY_URL.format(root_endpoint=self.root_endpoint)

        while True:
            res = self.get_articles(page_url)
            articles += res.get("articles")
            page_url = res.get("next_page")
            if page_url is None:
                break

        return articles

    defget_articles(self, url: str) -> Dict:
        importrequests
        frombs4import BeautifulSoup
        fromrequests.authimport HTTPBasicAuth

        articles: List[Article] = []
        next_page = None

        res = requests.get(url, auth=HTTPBasicAuth(self.username, self.api_key))
        soup = BeautifulSoup(res.text, "xml")
        for entry in soup.find_all("entry"):
            if entry.find("app:control").find("app:draft").string == "yes":
                continue
            article = Article()
            article.title = entry.find("title").string
            article.published = entry.find("published").string
            article.url = entry.find("link", rel="alternate")["href"]
            content = entry.find("content")
            if content.get("type") == "text/html":
                article.content = (
                    BeautifulSoup(entry.find("content").string, "html.parser")
                    .get_text()
                    .strip()
                )
            else:
                article.content = entry.find("content").string.strip()
            articles.append(article)

        next = soup.find("link", attrs={"rel": "next"})
        if next:
            next_page = next.get("href")

        return {"articles": articles, "next_page": next_page}

```
 |  
| --- | --- |  
options: members: - HatenaBlogReader
