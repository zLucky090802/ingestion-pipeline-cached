# Wordpress
##  WordpressReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/wordpress/#llama_index.readers.wordpress.WordpressReader "Permanent link")
Bases: 
Wordpress reader. Reads data from a Wordpress workspace.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  Base URL of the WordPress site.  |  _required_  |  
|  `username`  |  `Optional[str]`  |  WordPress username for authentication.  |  `None`  |  
|  `password`  |  `Optional[str]`  |  WordPress password for authentication.  |  `None`  |  
|  `get_pages`  |  `bool`  |  Retrieve static WordPress 'pages'. Default True.  |  `True`  |  
|  `get_posts`  |  `bool`  |  Retrieve WordPress 'posts' (blog entries). Default True.  |  `True`  |  
|  `additional_post_types`  |  `Optional[str]`  |  Comma-separated list of additional post types to retrieve (e.g., 'my-custom-page,webinars'). Default is None.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-wordpress/llama_index/readers/wordpress/base.py`  
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
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
```
 | 
```
classWordpressReader(BaseReader):
"""
    Wordpress reader. Reads data from a Wordpress workspace.

    Args:
        url (str): Base URL of the WordPress site.
        username (Optional[str]): WordPress username for authentication.
        password (Optional[str]): WordPress password for authentication.
        get_pages (bool): Retrieve static WordPress 'pages'. Default True.
        get_posts (bool): Retrieve WordPress 'posts' (blog entries). Default True.
        additional_post_types (Optional[str]): Comma-separated list of additional post types to retrieve
                                               (e.g., 'my-custom-page,webinars'). Default is None.

    """

    def__init__(
        self,
        url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        get_pages: bool = True,
        get_posts: bool = True,
        additional_post_types: Optional[str] = None,
    ) -> None:
"""Initialize Wordpress reader."""
        self.url = url
        self.username = username
        self.password = password

        # Use a set to prevent duplicates
        self.post_types = set()

        # Add default types based on backward-compatible options
        if get_pages:
            self.post_types.add("pages")
        if get_posts:
            self.post_types.add("posts")

        # Add any additional post types specified
        if additional_post_types:
            self.post_types.update(
                post_type.strip() for post_type in additional_post_types.split(",")
            )

        # Convert post_types back to a list
        self.post_types = list(self.post_types)

    defload_data(self) -> List[Document]:
"""
        Load data from the specified post types.

        Returns:
            List[Document]: List of documents.

        """
        frombs4import BeautifulSoup, GuessedAtParserWarning

        #  Suppressing this warning because guessing at the parser is the
        #  desired behavior -- we don't want to force lxml on packages
        #  where it's not installed.
        warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

        results = []
        articles = []

        # Fetch articles for each specified post type
        for post_type in self.post_types:
            articles.extend(self.get_all_posts(post_type))

        # Process each article to extract content and metadata
        for article in articles:
            body = article.get("content", {}).get("rendered", None)
            if body is None:
                body = article.get("content")

            soup = BeautifulSoup(body)
            body = soup.get_text()

            title = article.get("title", {}).get("rendered", None) or article.get(
                "title"
            )

            extra_info = {
                "id": article["id"],
                "title": title,
                "url": article["link"],
                "updated_at": article["modified"],
            }

            results.append(
                Document(
                    text=body,
                    extra_info=extra_info,
                )
            )
        return results

    defget_all_posts(self, post_type: str) -> List[dict]:
"""Retrieve all posts of a specific type, handling pagination."""
        posts = []
        next_page = 1

        while True:
            response = self.get_posts_page(post_type, next_page)
            posts.extend(response["articles"])
            next_page = response["next_page"]

            if next_page is None:
                break

        return posts

    defget_posts_page(self, post_type: str, current_page: int = 1) -> dict:
"""Retrieve a single page of posts for a given post type."""
        importrequests

        url = f"{self.url}/wp-json/wp/v2/{post_type}?per_page=100&page={current_page}"

        # Handle authentication if username and password are provided
        auth = (
            (self.username, self.password) if self.username and self.password else None
        )
        response = requests.get(url, auth=auth)
        response.raise_for_status()  # Raise an error for bad responses

        headers = response.headers
        num_pages = int(headers.get("X-WP-TotalPages", 1))
        next_page = current_page + 1 if num_pages  current_page else None

        articles = response.json()
        return {"articles": articles, "next_page": next_page}

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/wordpress/#llama_index.readers.wordpress.WordpressReader.load_data "Permanent link")

```
load_data() -> []

```

Load data from the specified post types.
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-wordpress/llama_index/readers/wordpress/base.py`  
| 
```
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
 99
100
101
102
103
104
105
```
 | 
```
defload_data(self) -> List[Document]:
"""
    Load data from the specified post types.

    Returns:
        List[Document]: List of documents.

    """
    frombs4import BeautifulSoup, GuessedAtParserWarning

    #  Suppressing this warning because guessing at the parser is the
    #  desired behavior -- we don't want to force lxml on packages
    #  where it's not installed.
    warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

    results = []
    articles = []

    # Fetch articles for each specified post type
    for post_type in self.post_types:
        articles.extend(self.get_all_posts(post_type))

    # Process each article to extract content and metadata
    for article in articles:
        body = article.get("content", {}).get("rendered", None)
        if body is None:
            body = article.get("content")

        soup = BeautifulSoup(body)
        body = soup.get_text()

        title = article.get("title", {}).get("rendered", None) or article.get(
            "title"
        )

        extra_info = {
            "id": article["id"],
            "title": title,
            "url": article["link"],
            "updated_at": article["modified"],
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
###  get_all_posts [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/wordpress/#llama_index.readers.wordpress.WordpressReader.get_all_posts "Permanent link")

```
get_all_posts(post_type: ) -> []

```

Retrieve all posts of a specific type, handling pagination.
Source code in `llama-index-integrations/readers/llama-index-readers-wordpress/llama_index/readers/wordpress/base.py`  
| 
```
107
108
109
110
111
112
113
114
115
116
117
118
119
120
```
 | 
```
defget_all_posts(self, post_type: str) -> List[dict]:
"""Retrieve all posts of a specific type, handling pagination."""
    posts = []
    next_page = 1

    while True:
        response = self.get_posts_page(post_type, next_page)
        posts.extend(response["articles"])
        next_page = response["next_page"]

        if next_page is None:
            break

    return posts

```
 |  
| --- | --- |  
###  get_posts_page [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/wordpress/#llama_index.readers.wordpress.WordpressReader.get_posts_page "Permanent link")

```
get_posts_page(
    post_type: , current_page:  = 1
) -> 

```

Retrieve a single page of posts for a given post type.
Source code in `llama-index-integrations/readers/llama-index-readers-wordpress/llama_index/readers/wordpress/base.py`  
| 
```
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
```
 | 
```
defget_posts_page(self, post_type: str, current_page: int = 1) -> dict:
"""Retrieve a single page of posts for a given post type."""
    importrequests

    url = f"{self.url}/wp-json/wp/v2/{post_type}?per_page=100&page={current_page}"

    # Handle authentication if username and password are provided
    auth = (
        (self.username, self.password) if self.username and self.password else None
    )
    response = requests.get(url, auth=auth)
    response.raise_for_status()  # Raise an error for bad responses

    headers = response.headers
    num_pages = int(headers.get("X-WP-TotalPages", 1))
    next_page = current_page + 1 if num_pages  current_page else None

    articles = response.json()
    return {"articles": articles, "next_page": next_page}

```
 |  
| --- | --- |  
options: members: - WordpressReader
