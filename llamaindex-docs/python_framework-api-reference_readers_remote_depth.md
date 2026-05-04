# Remote depth
##  RemoteDepthReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/remote_depth/#llama_index.readers.remote_depth.RemoteDepthReader "Permanent link")
Bases: 
Source code in `llama-index-integrations/readers/llama-index-readers-remote-depth/llama_index/readers/remote_depth/base.py`  
| 
```
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
```
 | 
```
classRemoteDepthReader(BaseReader):
    def__init__(
        self,
        *args: Any,
        file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = None,
        depth: int = 1,
        domain_lock: bool = False,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__(*args, **kwargs)
        self.file_extractor = file_extractor
        self.depth = depth
        self.domain_lock = domain_lock

    defload_data(self, url: str) -> List[Document]:
        fromtqdm.autoimport tqdm

"""Parse whatever is at the URL.""" ""
        remote_reader = RemoteReader(file_extractor=self.file_extractor)
        documents = []
        links = self.get_links(url)
        urls = {-1: [url]}  # -1 is the starting point
        links_visited = []
        for i in range(self.depth + 1):
            urls[i] = []
            new_links = []
            print(f"Reading links at depth {i}...")
            for link in tqdm(links):
"""Checking if the link belongs the provided domain."""
                if (self.domain_lock and link.find(url)  -1) or (not self.domain_lock):
                    print("Loading link: " + link)
                    if link in links_visited:
                        continue
                    if link:
                        urls[i].append(link)
                        new_links.extend(self.get_links(link))
                    links_visited.append(link)
                else:
                    print("Link ignored: " + link)
            new_links = list(set(new_links))
            links = new_links
        print(f"Found {len(urls)} links at depth {self.depth}.")
        for depth_i in urls:
            for url in urls[depth_i]:
                try:
                    documents.extend(remote_reader.load_data(url))
                except Exception as e:
                    print(f"Error reading {url} at depth {depth_i}: {e}")
                    continue

        return documents

    @staticmethod
    defis_url(href) -> bool:
"""Check if a link is a URL."""
        return href.startswith("http")

    defget_links(self, url) -> List[str]:
        fromurllib.parseimport urljoin, urlparse, urlunparse

        frombs4import BeautifulSoup

"""Get all links from a page."""
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        links = soup.find_all("a")
        result = []
        for link in links:
            if isinstance(link, str):
                href = link
            else:
                href = link.get("href")
            if href is not None:
                if not self.is_url(href):
                    href = urljoin(url, href)

            url_parsed = urlparse(href)
            url_without_query_string = urlunparse(
                (url_parsed.scheme, url_parsed.netloc, url_parsed.path, "", "", "")
            )

            if (
                url_without_query_string not in result
                and url_without_query_string
                and url_without_query_string.startswith("http")
            ):
                result.append(url_without_query_string)
        return result

```
 |  
| --- | --- |  
###  is_url `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/remote_depth/#llama_index.readers.remote_depth.RemoteDepthReader.is_url "Permanent link")

```
is_url(href) -> 

```

Check if a link is a URL.
Source code in `llama-index-integrations/readers/llama-index-readers-remote-depth/llama_index/readers/remote_depth/base.py`  
| 
```
68
69
70
71
```
 | 
```
@staticmethod
defis_url(href) -> bool:
"""Check if a link is a URL."""
    return href.startswith("http")

```
 |  
| --- | --- |  
options: members: - RemoteDepthReader
