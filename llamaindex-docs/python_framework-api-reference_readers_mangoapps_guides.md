# Mangoapps guides
##  MangoppsGuidesReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mangoapps_guides/#llama_index.readers.mangoapps_guides.MangoppsGuidesReader "Permanent link")
Bases: 
MangoppsGuides reader. Reads data from a MangoppsGuides workspace.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `domain_url`  |  MangoppsGuides domain url  |  _required_  |  
|  `limir`  |  depth to crawl  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-mangoapps-guides/llama_index/readers/mangoapps_guides/base.py`  
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
141
142
```
 | 
```
classMangoppsGuidesReader(BaseReader):
"""
    MangoppsGuides reader. Reads data from a MangoppsGuides workspace.

    Args:
        domain_url (str): MangoppsGuides domain url
        limir (int): depth to crawl

    """

    def__init__(self) -> None:
"""Initialize MangoppsGuides reader."""

    defload_data(self, domain_url: str, limit: int) -> List[Document]:
"""
        Load data from the workspace.

        Returns:
            List[Document]: List of documents.

        """
        importrequests
        frombs4import BeautifulSoup

        self.domain_url = domain_url
        self.limit = limit
        self.start_url = f"{self.domain_url}/home/"

        fetched_urls = self.crawl_urls()[: self.limit]

        results = []

        guides_pages = {}
        for url in fetched_urls:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")

                page_title = soup.find("title").text

                # Remove the div with aria-label="Table of contents"
                table_of_contents_div = soup.find(
                    "div", {"aria-label": "Table of contents"}
                )
                if table_of_contents_div:
                    table_of_contents_div.decompose()

                # Remove header and footer
                header = soup.find("header")
                if header:
                    header.decompose()
                footer = soup.find("footer")
                if footer:
                    footer.decompose()

                # Exclude links and their text content from the main content
                for link in soup.find_all("a"):
                    link.decompose()

                # Remove empty elements from the main content
                for element in soup.find_all():
                    if element.get_text(strip=True) == "":
                        element.decompose()

                # Find the main element containing the desired content
                main_element = soup.find(
                    "main"
                )  # Replace "main" with the appropriate element tag or CSS class

                # Extract the text content from the main element
                if main_element:
                    text_content = main_element.get_text("\n")
                    # Remove multiple consecutive newlines and keep only one newline
                    text_content = re.sub(r"\n+", "\n", text_content)
                else:
                    text_content = ""

                page_text = text_content

                guides_page = {}
                guides_page["title"] = page_title
                guides_page["text"] = page_text
                guides_pages[url] = guides_page
            except Exception as e:
                print(f"Failed for {url} => {e}")

        for k, v in guides_pages.items():
            extra_info = {"url": k, "title": v["title"]}
            results.append(
                Document(
                    text=v["text"],
                    extra_info=extra_info,
                )
            )

        return results

    defcrawl_urls(self) -> List[str]:
"""Crawls all the urls from given domain."""
        self.visited = []

        fetched_urls = self.fetch_url(self.start_url)
        return list(set(fetched_urls))

    deffetch_url(self, url):
"""Fetch the urls from given domain."""
        importrequests
        frombs4import BeautifulSoup

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        self.visited.append(url)

        newurls = []
        for link in soup.find_all("a"):
            href: str = link.get("href")
            if href and urlparse(href).netloc == self.domain_url:
                newurls.append(href)
            elif href and href.startswith("/"):
                newurls.append(f"{self.domain_url}{href}")

        for newurl in newurls:
            if (
                newurl not in self.visited
                and not newurl.startswith("#")
                and f"https://{urlparse(newurl).netloc}" == self.domain_url
                and len(self.visited) <= self.limit
            ):
                newurls = newurls + self.fetch_url(newurl)

        return list(set(newurls))

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mangoapps_guides/#llama_index.readers.mangoapps_guides.MangoppsGuidesReader.load_data "Permanent link")

```
load_data(domain_url: , limit: ) -> []

```

Load data from the workspace.
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-mangoapps-guides/llama_index/readers/mangoapps_guides/base.py`  
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
```
 | 
```
defload_data(self, domain_url: str, limit: int) -> List[Document]:
"""
    Load data from the workspace.

    Returns:
        List[Document]: List of documents.

    """
    importrequests
    frombs4import BeautifulSoup

    self.domain_url = domain_url
    self.limit = limit
    self.start_url = f"{self.domain_url}/home/"

    fetched_urls = self.crawl_urls()[: self.limit]

    results = []

    guides_pages = {}
    for url in fetched_urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            page_title = soup.find("title").text

            # Remove the div with aria-label="Table of contents"
            table_of_contents_div = soup.find(
                "div", {"aria-label": "Table of contents"}
            )
            if table_of_contents_div:
                table_of_contents_div.decompose()

            # Remove header and footer
            header = soup.find("header")
            if header:
                header.decompose()
            footer = soup.find("footer")
            if footer:
                footer.decompose()

            # Exclude links and their text content from the main content
            for link in soup.find_all("a"):
                link.decompose()

            # Remove empty elements from the main content
            for element in soup.find_all():
                if element.get_text(strip=True) == "":
                    element.decompose()

            # Find the main element containing the desired content
            main_element = soup.find(
                "main"
            )  # Replace "main" with the appropriate element tag or CSS class

            # Extract the text content from the main element
            if main_element:
                text_content = main_element.get_text("\n")
                # Remove multiple consecutive newlines and keep only one newline
                text_content = re.sub(r"\n+", "\n", text_content)
            else:
                text_content = ""

            page_text = text_content

            guides_page = {}
            guides_page["title"] = page_title
            guides_page["text"] = page_text
            guides_pages[url] = guides_page
        except Exception as e:
            print(f"Failed for {url} => {e}")

    for k, v in guides_pages.items():
        extra_info = {"url": k, "title": v["title"]}
        results.append(
            Document(
                text=v["text"],
                extra_info=extra_info,
            )
        )

    return results

```
 |  
| --- | --- |  
###  crawl_urls [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mangoapps_guides/#llama_index.readers.mangoapps_guides.MangoppsGuidesReader.crawl_urls "Permanent link")

```
crawl_urls() -> []

```

Crawls all the urls from given domain.
Source code in `llama-index-integrations/readers/llama-index-readers-mangoapps-guides/llama_index/readers/mangoapps_guides/base.py`  
| 
```
108
109
110
111
112
113
```
 | 
```
defcrawl_urls(self) -> List[str]:
"""Crawls all the urls from given domain."""
    self.visited = []

    fetched_urls = self.fetch_url(self.start_url)
    return list(set(fetched_urls))

```
 |  
| --- | --- |  
###  fetch_url [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mangoapps_guides/#llama_index.readers.mangoapps_guides.MangoppsGuidesReader.fetch_url "Permanent link")

```
fetch_url(url)

```

Fetch the urls from given domain.
Source code in `llama-index-integrations/readers/llama-index-readers-mangoapps-guides/llama_index/readers/mangoapps_guides/base.py`  
| 
```
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
141
142
```
 | 
```
deffetch_url(self, url):
"""Fetch the urls from given domain."""
    importrequests
    frombs4import BeautifulSoup

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    self.visited.append(url)

    newurls = []
    for link in soup.find_all("a"):
        href: str = link.get("href")
        if href and urlparse(href).netloc == self.domain_url:
            newurls.append(href)
        elif href and href.startswith("/"):
            newurls.append(f"{self.domain_url}{href}")

    for newurl in newurls:
        if (
            newurl not in self.visited
            and not newurl.startswith("#")
            and f"https://{urlparse(newurl).netloc}" == self.domain_url
            and len(self.visited) <= self.limit
        ):
            newurls = newurls + self.fetch_url(newurl)

    return list(set(newurls))

```
 |  
| --- | --- |  
options: members: - MangoppsGuidesReader
