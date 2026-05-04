# Feedly rss
##  FeedlyRssReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/feedly_rss/#llama_index.readers.feedly_rss.FeedlyRssReader "Permanent link")
Bases: 
Feedly Rss Reader.
Get entries from Feedly Rss Reader
Uses Feedly Official python-api-client: https://github.com/feedly/python-api-client
Source code in `llama-index-integrations/readers/llama-index-readers-feedly-rss/llama_index/readers/feedly_rss/base.py`  
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
```
 | 
```
classFeedlyRssReader(BaseReader):
"""
    Feedly Rss Reader.

    Get entries from Feedly Rss Reader

    Uses Feedly Official python-api-client: https://github.com/feedly/python-api-client
    """

    def__init__(self, bearer_token: str) -> None:
"""Initialize with parameters."""
        super().__init__()
        self.bearer_token = bearer_token

    defsetup_auth(
        self, directory: Path = Path.home() / ".config/feedly", overwrite: bool = False
    ):
"""
        Modified from python-api-client/feedly/api_client/utils.py
        Instead promopting for user input, we take the token as an argument.
        """
        directory.mkdir(exist_ok=True, parents=True)

        auth_file = directory / "access.token"

        if not auth_file.exists() or overwrite:
            auth = self.bearer_token
            auth_file.write_text(auth.strip())

    defload_data(self, category_name, max_count=100):
"""Get the entries from a feedly category."""
        fromfeedly.api_client.sessionimport FeedlySession
        fromfeedly.api_client.streamimport StreamOptions

        self.setup_auth(overwrite=True)
        sess = FeedlySession()
        category = sess.user.user_categories.get(category_name)

        documents = []
        for article in category.stream_contents(
            options=StreamOptions(max_count=max_count)
        ):
            # doc for available fields: https://developer.feedly.com/v3/streams/
            entry = {
                "title": article["title"],
                "published": article["published"],
                "summary": article["summary"],
                "author": article["author"],
                "content": article["content"],
                "keywords": article["keywords"],
                "commonTopics": article["commonTopics"],
            }

            text = json.dumps(entry, ensure_ascii=False)

            documents.append(Document(text=text))
        return documents

```
 |  
| --- | --- |  
###  setup_auth [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/feedly_rss/#llama_index.readers.feedly_rss.FeedlyRssReader.setup_auth "Permanent link")

```
setup_auth(
    directory:  = () / ".config/feedly",
    overwrite:  = False,
)

```

Modified from python-api-client/feedly/api_client/utils.py Instead promopting for user input, we take the token as an argument.
Source code in `llama-index-integrations/readers/llama-index-readers-feedly-rss/llama_index/readers/feedly_rss/base.py`  
| 
```
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
```
 | 
```
defsetup_auth(
    self, directory: Path = Path.home() / ".config/feedly", overwrite: bool = False
):
"""
    Modified from python-api-client/feedly/api_client/utils.py
    Instead promopting for user input, we take the token as an argument.
    """
    directory.mkdir(exist_ok=True, parents=True)

    auth_file = directory / "access.token"

    if not auth_file.exists() or overwrite:
        auth = self.bearer_token
        auth_file.write_text(auth.strip())

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/feedly_rss/#llama_index.readers.feedly_rss.FeedlyRssReader.load_data "Permanent link")

```
load_data(category_name, max_count=100)

```

Get the entries from a feedly category.
Source code in `llama-index-integrations/readers/llama-index-readers-feedly-rss/llama_index/readers/feedly_rss/base.py`  
| 
```
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
```
 | 
```
defload_data(self, category_name, max_count=100):
"""Get the entries from a feedly category."""
    fromfeedly.api_client.sessionimport FeedlySession
    fromfeedly.api_client.streamimport StreamOptions

    self.setup_auth(overwrite=True)
    sess = FeedlySession()
    category = sess.user.user_categories.get(category_name)

    documents = []
    for article in category.stream_contents(
        options=StreamOptions(max_count=max_count)
    ):
        # doc for available fields: https://developer.feedly.com/v3/streams/
        entry = {
            "title": article["title"],
            "published": article["published"],
            "summary": article["summary"],
            "author": article["author"],
            "content": article["content"],
            "keywords": article["keywords"],
            "commonTopics": article["commonTopics"],
        }

        text = json.dumps(entry, ensure_ascii=False)

        documents.append(Document(text=text))
    return documents

```
 |  
| --- | --- |  
options: members: - FeedlyRssReader
