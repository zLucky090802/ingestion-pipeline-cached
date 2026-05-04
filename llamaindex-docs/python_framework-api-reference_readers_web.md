# Web
Init file.
##  AgentQLWebReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.AgentQLWebReader "Permanent link")
Bases: 
Scrape a URL with or without a agentql query and returns document in json format.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  The AgentQL API key, get one at https://dev.agentql.com  |  _required_  |  
|  `params`  |  `dict`  |  Additional parameters to pass to the AgentQL API. Visit https://docs.agentql.com/rest-api/api-reference for details.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/agentql_web/base.py`  
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
```
 | 
```
classAgentQLWebReader(BasePydanticReader):
"""
    Scrape a URL with or without a agentql query and returns document in json format.

    Args:
        api_key (str): The AgentQL API key, get one at https://dev.agentql.com
        params (dict): Additional parameters to pass to the AgentQL API. Visit https://docs.agentql.com/rest-api/api-reference for details.

    """

    api_key: str
    params: Optional[dict]

    def__init__(
        self,
        api_key: str,
        params: Optional[dict] = None,
    ) -> None:
        super().__init__(api_key=api_key, params=params)

    defload_data(
        self, url: str, query: Optional[str] = None, prompt: Optional[str] = None
    ) -> List[Document]:
"""
        Load data from the input directory.

        Args:
            url (str): URL to scrape or crawl.
            query (Optional[str]): AgentQL query used to specify the scraped data.
            prompt (Optional[str]): Natural language description of the data you want to scrape.
            Either query or prompt must be provided.
            params (Optional[dict]): Additional parameters to pass to the AgentQL API. Visit https://docs.agentql.com/rest-api/api-reference for details.

        Returns:
            List[Document]: List of documents.

        """
        payload = {"url": url, "query": query, "prompt": prompt, "params": self.params}

        headers = {
            "X-API-Key": f"{self.api_key}",
            "Content-Type": "application/json",
            "X-TF-Request-Origin": REQUEST_ORIGIN,
        }

        try:
            response = httpx.post(
                QUERY_DATA_ENDPOINT,
                headers=headers,
                json=payload,
                timeout=API_TIMEOUT_SECONDS,
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            response = e.response
            if response.status_code in [401, 403]:
                raise ValueError(
                    "Please, provide a valid API Key. You can create one at https://dev.agentql.com."
                ) frome
            else:
                try:
                    error_json = response.json()
                    msg = (
                        error_json["error_info"]
                        if "error_info" in error_json
                        else error_json["detail"]
                    )
                except (ValueError, TypeError):
                    msg = f"HTTP {e}."
                raise ValueError(msg) frome
        else:
            json = response.json()

            return [Document(text=str(json["data"]), metadata=json["metadata"])]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.AgentQLWebReader.load_data "Permanent link")

```
load_data(
    url: ,
    query: Optional[] = None,
    prompt: Optional[] = None,
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  URL to scrape or crawl.  |  _required_  |  
|  `query`  |  `Optional[str]`  |  AgentQL query used to specify the scraped data.  |  `None`  |  
|  `prompt`  |  `Optional[str]`  |  Natural language description of the data you want to scrape.  |  `None`  |  
|  `params`  |  `Optional[dict]`  |  Additional parameters to pass to the AgentQL API. Visit https://docs.agentql.com/rest-api/api-reference for details.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/agentql_web/base.py`  
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
```
 | 
```
defload_data(
    self, url: str, query: Optional[str] = None, prompt: Optional[str] = None
) -> List[Document]:
"""
    Load data from the input directory.

    Args:
        url (str): URL to scrape or crawl.
        query (Optional[str]): AgentQL query used to specify the scraped data.
        prompt (Optional[str]): Natural language description of the data you want to scrape.
        Either query or prompt must be provided.
        params (Optional[dict]): Additional parameters to pass to the AgentQL API. Visit https://docs.agentql.com/rest-api/api-reference for details.

    Returns:
        List[Document]: List of documents.

    """
    payload = {"url": url, "query": query, "prompt": prompt, "params": self.params}

    headers = {
        "X-API-Key": f"{self.api_key}",
        "Content-Type": "application/json",
        "X-TF-Request-Origin": REQUEST_ORIGIN,
    }

    try:
        response = httpx.post(
            QUERY_DATA_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=API_TIMEOUT_SECONDS,
        )
        response.raise_for_status()

    except httpx.HTTPStatusError as e:
        response = e.response
        if response.status_code in [401, 403]:
            raise ValueError(
                "Please, provide a valid API Key. You can create one at https://dev.agentql.com."
            ) frome
        else:
            try:
                error_json = response.json()
                msg = (
                    error_json["error_info"]
                    if "error_info" in error_json
                    else error_json["detail"]
                )
            except (ValueError, TypeError):
                msg = f"HTTP {e}."
            raise ValueError(msg) frome
    else:
        json = response.json()

        return [Document(text=str(json["data"]), metadata=json["metadata"])]

```
 |  
| --- | --- |  
##  AsyncWebPageReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.AsyncWebPageReader "Permanent link")
Bases: 
Asynchronous web page reader.
Reads pages from the web asynchronously.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `html_to_text`  |  `bool`  |  Whether to convert HTML to text. Requires `html2text` package.  |  `False`  |  
|  `limit`  |  Maximum number of concurrent requests.  |  
|  `dedupe`  |  `bool`  |  to deduplicate urls if there is exact-match within given list  |  `True`  |  
|  `fail_on_error`  |  `bool`  |  if requested url does not return status code 200 the routine will raise an ValueError  |  `False`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/async_web/base.py`  
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
```
 | 
```
classAsyncWebPageReader(BaseReader):
"""
    Asynchronous web page reader.

    Reads pages from the web asynchronously.

    Args:
        html_to_text (bool): Whether to convert HTML to text.
            Requires `html2text` package.
        limit (int): Maximum number of concurrent requests.
        dedupe (bool): to deduplicate urls if there is exact-match within given list
        fail_on_error (bool): if requested url does not return status code 200 the routine will raise an ValueError

    """

    def__init__(
        self,
        html_to_text: bool = False,
        limit: int = 10,
        dedupe: bool = True,
        fail_on_error: bool = False,
        timeout: Optional[int] = 60,
    ) -> None:
"""Initialize with parameters."""
        try:
            importhtml2text  # noqa: F401
        except ImportError:
            raise ImportError(
                "`html2text` package not found, please run `pip install html2text`"
            )
        try:
            importaiohttp  # noqa: F401
        except ImportError:
            raise ImportError(
                "`aiohttp` package not found, please run `pip install aiohttp`"
            )
        self._limit = limit
        self._html_to_text = html_to_text
        self._dedupe = dedupe
        self._fail_on_error = fail_on_error
        self._timeout = timeout

    async defaload_data(self, urls: List[str]) -> List[Document]:
"""
        Load data from the input urls.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[Document]: List of documents.

        """
        if self._dedupe:
            urls = list(dict.fromkeys(urls))

        importaiohttp

        defchunked_http_client(limit: int):
            semaphore = asyncio.Semaphore(limit)

            async defhttp_get(url: str, session: aiohttp.ClientSession):
                async with semaphore:
                    async with session.get(url) as response:
                        return response, await response.text()

            return http_get

        async deffetch_urls(urls: List[str]):
            http_client = chunked_http_client(self._limit)

            timeout = (
                aiohttp.ClientTimeout(total=self._timeout) if self._timeout else None
            )

            async with aiohttp.ClientSession(timeout=timeout) as session:
                tasks = [http_client(url, session) for url in urls]
                return await asyncio.gather(*tasks, return_exceptions=True)

        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")

        documents = []
        responses = await fetch_urls(urls)

        for i, response_tuple in enumerate(responses):
            if not isinstance(response_tuple, tuple):
                if self._fail_on_error:
                    raise ValueError(f"Error fetching {urls[i]}")
                continue

            response, raw_page = response_tuple

            if response.status != 200:
                logger.warning(f"Error fetching page from {urls[i]}")
                logger.info(response)

                if self._fail_on_error:
                    raise ValueError(
                        f"Error fetching page from {urls[i]}. server returned status:"
                        f" {response.status} and response {raw_page}"
                    )

                continue

            if self._html_to_text:
                importhtml2text

                response_text = html2text.html2text(raw_page)
            else:
                response_text = raw_page

            documents.append(
                Document(text=response_text, extra_info={"Source": str(response.url)})
            )

        return documents

    defload_data(self, urls: List[str]) -> List[Document]:
"""
        Load data from the input urls.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[Document]: List of documents.

        """
        return asyncio.run(self.aload_data(urls))

```
 |  
| --- | --- |  
###  aload_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.AsyncWebPageReader.aload_data "Permanent link")

```
aload_data(urls: []) -> []

```

Load data from the input urls.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List of URLs to scrape.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/async_web/base.py`  
| 
```
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
```
 | 
```
async defaload_data(self, urls: List[str]) -> List[Document]:
"""
    Load data from the input urls.

    Args:
        urls (List[str]): List of URLs to scrape.

    Returns:
        List[Document]: List of documents.

    """
    if self._dedupe:
        urls = list(dict.fromkeys(urls))

    importaiohttp

    defchunked_http_client(limit: int):
        semaphore = asyncio.Semaphore(limit)

        async defhttp_get(url: str, session: aiohttp.ClientSession):
            async with semaphore:
                async with session.get(url) as response:
                    return response, await response.text()

        return http_get

    async deffetch_urls(urls: List[str]):
        http_client = chunked_http_client(self._limit)

        timeout = (
            aiohttp.ClientTimeout(total=self._timeout) if self._timeout else None
        )

        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = [http_client(url, session) for url in urls]
            return await asyncio.gather(*tasks, return_exceptions=True)

    if not isinstance(urls, list):
        raise ValueError("urls must be a list of strings.")

    documents = []
    responses = await fetch_urls(urls)

    for i, response_tuple in enumerate(responses):
        if not isinstance(response_tuple, tuple):
            if self._fail_on_error:
                raise ValueError(f"Error fetching {urls[i]}")
            continue

        response, raw_page = response_tuple

        if response.status != 200:
            logger.warning(f"Error fetching page from {urls[i]}")
            logger.info(response)

            if self._fail_on_error:
                raise ValueError(
                    f"Error fetching page from {urls[i]}. server returned status:"
                    f" {response.status} and response {raw_page}"
                )

            continue

        if self._html_to_text:
            importhtml2text

            response_text = html2text.html2text(raw_page)
        else:
            response_text = raw_page

        documents.append(
            Document(text=response_text, extra_info={"Source": str(response.url)})
        )

    return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.AsyncWebPageReader.load_data "Permanent link")

```
load_data(urls: []) -> []

```

Load data from the input urls.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List of URLs to scrape.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/async_web/base.py`  
| 
```
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
defload_data(self, urls: List[str]) -> List[Document]:
"""
    Load data from the input urls.

    Args:
        urls (List[str]): List of URLs to scrape.

    Returns:
        List[Document]: List of documents.

    """
    return asyncio.run(self.aload_data(urls))

```
 |  
| --- | --- |  
##  BeautifulSoupWebReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.BeautifulSoupWebReader "Permanent link")
Bases: 
BeautifulSoup web page reader.
Reads pages from the web. Requires the `bs4` and `urllib` packages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `website_extractor`  |  `Optional[Dict[str, Callable]]`  |  A mapping of website hostname (e.g. google.com) to a function that specifies how to extract text from the BeautifulSoup obj. See DEFAULT_WEBSITE_EXTRACTOR.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/beautiful_soup_web/base.py`  
| 
```
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
```
 | 
```
classBeautifulSoupWebReader(BasePydanticReader):
"""
    BeautifulSoup web page reader.

    Reads pages from the web.
    Requires the `bs4` and `urllib` packages.

    Args:
        website_extractor (Optional[Dict[str, Callable]]): A mapping of website
            hostname (e.g. google.com) to a function that specifies how to
            extract text from the BeautifulSoup obj. See DEFAULT_WEBSITE_EXTRACTOR.

    """

    is_remote: bool = True
    _website_extractor: Dict[str, Callable] = PrivateAttr()

    def__init__(self, website_extractor: Optional[Dict[str, Callable]] = None) -> None:
        super().__init__()
        self._website_extractor = website_extractor or DEFAULT_WEBSITE_EXTRACTOR

    @classmethod
    defclass_name(cls) -> str:
"""Get the name identifier of the class."""
        return "BeautifulSoupWebReader"

    defload_data(
        self,
        urls: List[str],
        custom_hostname: Optional[str] = None,
        include_url_in_text: Optional[bool] = True,
    ) -> List[Document]:
"""
        Load data from the urls.

        Args:
            urls (List[str]): List of URLs to scrape.
            custom_hostname (Optional[str]): Force a certain hostname in the case
                a website is displayed under custom URLs (e.g. Substack blogs)
            include_url_in_text (Optional[bool]): Include the reference url in the text of the document

        Returns:
            List[Document]: List of documents.

        """
        fromurllib.parseimport urlparse

        importrequests
        frombs4import BeautifulSoup

        documents = []
        for url in urls:
            try:
                page = requests.get(url)
            except Exception:
                raise ValueError(f"One of the inputs is not a valid url: {url}")

            hostname = custom_hostname or urlparse(url).hostname or ""

            soup = BeautifulSoup(page.content, "html.parser")

            data = ""
            extra_info = {"URL": url}
            if hostname in self._website_extractor:
                data, metadata = self._website_extractor[hostname](
                    soup=soup, url=url, include_url_in_text=include_url_in_text
                )
                extra_info.update(metadata)

            else:
                data = soup.getText()

            documents.append(
                Document(text=data, id_=str(uuid.uuid4()), extra_info=extra_info)
            )

        return documents

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.BeautifulSoupWebReader.class_name "Permanent link")

```
class_name() -> 

```

Get the name identifier of the class.
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/beautiful_soup_web/base.py`  
| 
```
157
158
159
160
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get the name identifier of the class."""
    return "BeautifulSoupWebReader"

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.BeautifulSoupWebReader.load_data "Permanent link")

```
load_data(
    urls: [],
    custom_hostname: Optional[] = None,
    include_url_in_text: Optional[] = True,
) -> []

```

Load data from the urls.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List of URLs to scrape.  |  _required_  |  
|  `custom_hostname`  |  `Optional[str]`  |  Force a certain hostname in the case a website is displayed under custom URLs (e.g. Substack blogs)  |  `None`  |  
|  `include_url_in_text`  |  `Optional[bool]`  |  Include the reference url in the text of the document  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/beautiful_soup_web/base.py`  
| 
```
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
```
 | 
```
defload_data(
    self,
    urls: List[str],
    custom_hostname: Optional[str] = None,
    include_url_in_text: Optional[bool] = True,
) -> List[Document]:
"""
    Load data from the urls.

    Args:
        urls (List[str]): List of URLs to scrape.
        custom_hostname (Optional[str]): Force a certain hostname in the case
            a website is displayed under custom URLs (e.g. Substack blogs)
        include_url_in_text (Optional[bool]): Include the reference url in the text of the document

    Returns:
        List[Document]: List of documents.

    """
    fromurllib.parseimport urlparse

    importrequests
    frombs4import BeautifulSoup

    documents = []
    for url in urls:
        try:
            page = requests.get(url)
        except Exception:
            raise ValueError(f"One of the inputs is not a valid url: {url}")

        hostname = custom_hostname or urlparse(url).hostname or ""

        soup = BeautifulSoup(page.content, "html.parser")

        data = ""
        extra_info = {"URL": url}
        if hostname in self._website_extractor:
            data, metadata = self._website_extractor[hostname](
                soup=soup, url=url, include_url_in_text=include_url_in_text
            )
            extra_info.update(metadata)

        else:
            data = soup.getText()

        documents.append(
            Document(text=data, id_=str(uuid.uuid4()), extra_info=extra_info)
        )

    return documents

```
 |  
| --- | --- |  
##  BrowserbaseWebReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.BrowserbaseWebReader "Permanent link")
Bases: 
BrowserbaseWebReader.
Load pre-rendered web pages using a headless browser hosted on Browserbase. Depends on `browserbase` package. Get your API key from https://browserbase.com
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/browserbase_web/base.py`  
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
```
 | 
```
classBrowserbaseWebReader(BaseReader):
"""
    BrowserbaseWebReader.

    Load pre-rendered web pages using a headless browser hosted on Browserbase.
    Depends on `browserbase` package.
    Get your API key from https://browserbase.com
    """

    def__init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> None:
        try:
            frombrowserbaseimport Browserbase
        except ImportError:
            raise ImportError(
                "`browserbase` package not found, please run `pip install browserbase`"
            )

        self.browserbase = Browserbase(api_key, project_id)

    deflazy_load_data(
        self,
        urls: Sequence[str],
        text_content: bool = False,
        session_id: Optional[str] = None,
        proxy: Optional[bool] = None,
    ) -> Iterator[Document]:
"""Load pages from URLs."""
        pages = self.browserbase.load_urls(urls, text_content, session_id, proxy)

        for i, page in enumerate(pages):
            yield Document(
                text=page,
                metadata={
                    "url": urls[i],
                },
            )

```
 |  
| --- | --- |  
###  lazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.BrowserbaseWebReader.lazy_load_data "Permanent link")

```
lazy_load_data(
    urls: Sequence[],
    text_content:  = False,
    session_id: Optional[] = None,
    proxy: Optional[] = None,
) -> Iterator[]

```

Load pages from URLs.
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/browserbase_web/base.py`  
| 
```
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
```
 | 
```
deflazy_load_data(
    self,
    urls: Sequence[str],
    text_content: bool = False,
    session_id: Optional[str] = None,
    proxy: Optional[bool] = None,
) -> Iterator[Document]:
"""Load pages from URLs."""
    pages = self.browserbase.load_urls(urls, text_content, session_id, proxy)

    for i, page in enumerate(pages):
        yield Document(
            text=page,
            metadata={
                "url": urls[i],
            },
        )

```
 |  
| --- | --- |  
##  FireCrawlWebReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.FireCrawlWebReader "Permanent link")
Bases: 
turn a url to llm accessible markdown with `Firecrawl.dev`.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  The Firecrawl API key.  |  _required_  |  
|  `api_url`  |  `Optional[str]`  |  Optional base URL for Firecrawl deployment  |  `None`  |  
|  `mode`  |  `Optional[str]`  |  The mode to run the loader in. Default is "crawl". Options include "scrape" (single url), "crawl" (all accessible sub pages), "map" (map all accessible sub pages), "search" (search for content), and "extract" (extract structured data from URLs using a prompt).  |  `'crawl'`  |  
|  `params`  |  `Optional[dict]`  |  The parameters to pass to the Firecrawl API.  |  `None`  |  
Examples include crawlerOptions. For more details, visit: https://docs.firecrawl.dev/sdks/python
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/firecrawl_web/base.py`  
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
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
```
 | 
```
classFireCrawlWebReader(BasePydanticReader):
"""
    turn a url to llm accessible markdown with `Firecrawl.dev`.

    Args:
        api_key (str): The Firecrawl API key.
        api_url (Optional[str]): Optional base URL for Firecrawl deployment
        mode (Optional[str]):
            The mode to run the loader in. Default is "crawl".
            Options include "scrape" (single url),
            "crawl" (all accessible sub pages),
            "map" (map all accessible sub pages),
            "search" (search for content), and
            "extract" (extract structured data from URLs using a prompt).
        params (Optional[dict]): The parameters to pass to the Firecrawl API.

    Examples include crawlerOptions.
    For more details, visit: https://docs.firecrawl.dev/sdks/python

    """

    firecrawl: Any
    api_key: str
    api_url: Optional[str]
    mode: Optional[str]
    params: Optional[dict]

    _metadata_fn: Optional[Callable[[str], Dict]] = PrivateAttr()

    # --------------------
    # Aux methods (init)
    # --------------------
    def_import_firecrawl(self) -> Any:
        try:
            fromfirecrawlimport Firecrawl  # type: ignore
        except Exception as exc:
            raise ImportError(
                "firecrawl not found, please run `pip install 'firecrawl-py>=4.3.3'`"
            ) fromexc
        return Firecrawl

    def_init_client(self, api_key: str, api_url: Optional[str]) -> Any:
        Firecrawl = self._import_firecrawl()
        client_kwargs: Dict[str, Any] = {"api_key": api_key}
        if api_url is not None:
            client_kwargs["api_url"] = api_url
        return Firecrawl(**client_kwargs)

    def_params_copy(self) -> Dict[str, Any]:
        params: Dict[str, Any] = self.params.copy() if self.params else {}
        return params

    # --------------------
    # Aux helpers (common)
    # --------------------
    def_safe_get_attr(self, obj: Any, *names: str) -> Optional[Any]:
        for name in names:
            try:
                val = getattr(obj, name, None)
            except Exception:
                val = None
            if val:
                return val
        return None

    def_to_dict_best_effort(self, obj: Any) -> Dict[str, Any]:
        # pydantic v2
        if hasattr(obj, "model_dump") and callable(obj.model_dump):
            try:
                return obj.model_dump()  # type: ignore[attr-defined]
            except Exception:
                pass
        # pydantic v1
        if hasattr(obj, "dict") and callable(obj.dict):
            try:
                return obj.dict()  # type: ignore[attr-defined]
            except Exception:
                pass
        # dataclass or simple object
        if hasattr(obj, "__dict__"):
            try:
                return {k: v for k, v in vars(obj).items() if not k.startswith("_")}
            except Exception:
                pass
        # reflect over attributes
        result: Dict[str, Any] = {}
        try:
            for attr in dir(obj):
                if attr.startswith("_"):
                    continue
                try:
                    val = getattr(obj, attr)
                except Exception:
                    continue
                if callable(val):
                    continue
                result[attr] = val
        except Exception:
            pass
        return result

    # --------------------
    # Aux handlers (SCRAPE)
    # --------------------
    def_scrape_get_first(self, data_obj: Dict[str, Any], *keys: str) -> Optional[Any]:
        for k in keys:
            if isinstance(data_obj, dict) and k in data_obj and data_obj.get(k):
                return data_obj.get(k)
        return None

    def_scrape_from_dict(
        self, firecrawl_docs: Dict[str, Any]
    ) -> (str, Dict[str, Any]):
        data_obj = firecrawl_docs.get("data", firecrawl_docs)
        text_value = (
            self._scrape_get_first(
                data_obj,
                "markdown",
                "content",
                "html",
                "raw_html",
                "rawHtml",
                "summary",
            )
            or ""
        )

        meta_obj = data_obj.get("metadata", {}) if isinstance(data_obj, dict) else {}
        metadata_value: Dict[str, Any] = {}

        if isinstance(meta_obj, dict):
            metadata_value = meta_obj
        else:
            try:
                metadata_value = self._to_dict_best_effort(meta_obj)
            except Exception:
                metadata_value = {"metadata": str(meta_obj)}

        if isinstance(data_obj, dict):
            for extra_key in (
                "links",
                "actions",
                "screenshot",
                "warning",
                "changeTracking",
            ):
                if extra_key in data_obj and data_obj.get(extra_key) is not None:
                    metadata_value[extra_key] = data_obj.get(extra_key)

        if "success" in firecrawl_docs:
            metadata_value["success"] = firecrawl_docs.get("success")
        if "warning" in firecrawl_docs and firecrawl_docs.get("warning") is not None:
            metadata_value["warning_top"] = firecrawl_docs.get("warning")

        return text_value, metadata_value

    def_scrape_from_obj(self, firecrawl_docs: Any) -> (str, Dict[str, Any]):
        text_value = (
            self._safe_get_attr(
                firecrawl_docs,
                "markdown",
                "content",
                "html",
                "raw_html",
                "summary",
            )
            or ""
        )

        meta_obj = getattr(firecrawl_docs, "metadata", None)
        metadata_value: Dict[str, Any] = {}
        if meta_obj is not None:
            try:
                metadata_value = self._to_dict_best_effort(meta_obj)
            except Exception:
                metadata_value = {"metadata": str(meta_obj)}

        for extra_attr in (
            "links",
            "actions",
            "screenshot",
            "warning",
            "change_tracking",
        ):
            try:
                extra_val = getattr(firecrawl_docs, extra_attr, None)
            except Exception:
                extra_val = None
            if extra_val is not None:
                metadata_value[extra_attr] = extra_val

        return text_value, metadata_value

    def_handle_scrape_response(self, firecrawl_docs: Any) -> (str, Dict[str, Any]):
        if isinstance(firecrawl_docs, dict):
            return self._scrape_from_dict(firecrawl_docs)
        else:
            return self._scrape_from_obj(firecrawl_docs)

    # --------------------
    # Aux handlers (CRAWL)
    # --------------------
    def_normalize_crawl_response(self, firecrawl_docs: Any) -> List[Dict[str, Any]]:
        return firecrawl_docs.get("data", firecrawl_docs)

    # --------------------
    # Aux handlers (MAP)
    # --------------------
    def_handle_map_error_or_links(self, response: Any, url: str) -> List[Document]:
        docs: List[Document] = []
        if (
            isinstance(response, dict)
            and "error" in response
            and not response.get("success", False)
        ):
            error_message = response.get("error", "Unknown error")
            docs.append(
                Document(
                    text=f"Map request failed: {error_message}",
                    metadata={"source": "map", "url": url, "error": error_message},
                )
            )
            return docs

        links = response.links or []
        for link in links:
            link_url = link.url
            title = link.title
            description = link.description
            text_content = title or description or link_url
            docs.append(
                Document(
                    text=text_content,
                    metadata={
                        "source": "map",
                        "url": link_url,
                        "title": title,
                        "description": description,
                    },
                )
            )
        return docs

    # --------------------
    # Aux handlers (SEARCH)
    # --------------------
    def_process_search_dict(
        self, search_response: Dict[str, Any], query: str
    ) -> List[Document]:
        documents: List[Document] = []
        if search_response.get("success", False):
            search_results = search_response.get("data", [])
            for result in search_results:
                text = result.get("markdown", "")
                if not text:
                    text = result.get("description", "")
                metadata = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "description": result.get("description", ""),
                    "source": "search",
                    "query": query,
                }
                if "metadata" in result and isinstance(result["metadata"], dict):
                    metadata.update(result["metadata"])
                documents.append(Document(text=text, metadata=metadata))
        else:
            warning = search_response.get("warning", "Unknown error")
            print(f"Search was unsuccessful: {warning}")
            documents.append(
                Document(
                    text=f"Search for '{query}' was unsuccessful: {warning}",
                    metadata={"source": "search", "query": query, "error": warning},
                )
            )
        return documents

    def_process_search_items(
        self, result_list: Any, result_type: str, query: str
    ) -> List[Document]:
        docs: List[Document] = []
        if not result_list:
            return docs
        for item in result_list:
            item_url = getattr(item, "url", "")
            item_title = getattr(item, "title", "")
            item_description = getattr(item, "description", "")
            text_content = item_title or item_description or item_url

            metadata = {
                "title": item_title,
                "url": item_url,
                "description": item_description,
                "source": "search",
                "search_type": result_type,
                "query": query,
            }
            base_keys = set(metadata.keys())
            extra_attrs = self._to_dict_best_effort(item)
            for k, v in extra_attrs.items():
                if k not in base_keys:
                    metadata[k] = v
            docs.append(Document(text=text_content, metadata=metadata))
        return docs

    def_process_search_sdk(self, search_response: Any, query: str) -> List[Document]:
        documents: List[Document] = []
        documents += self._process_search_items(
            getattr(search_response, "web", None), "web", query
        )  # type: ignore[attr-defined]
        documents += self._process_search_items(
            getattr(search_response, "news", None), "news", query
        )  # type: ignore[attr-defined]
        documents += self._process_search_items(
            getattr(search_response, "images", None), "images", query
        )  # type: ignore[attr-defined]
        return documents

    # --------------------
    # Aux handlers (EXTRACT)
    # --------------------
    def_format_extract_text(self, extract_data: Dict[str, Any]) -> str:
        text_parts = []
        for key, value in extract_data.items():
            text_parts.append(f"{key}: {value}")
        return "\n".join(text_parts)

    # --------------------
    # __init__ (unchanged behavior)
    # --------------------
    def__init__(
        self,
        api_key: str,
        api_url: Optional[str] = None,
        mode: Optional[str] = "crawl",
        params: Optional[dict] = None,
    ) -> None:
"""Initialize with parameters."""
        # Ensure firecrawl client is installed and instantiate
        try:
            fromfirecrawlimport Firecrawl  # type: ignore
        except Exception as exc:
            raise ImportError(
                "firecrawl not found, please run `pip install 'firecrawl-py>=4.3.3'`"
            ) fromexc

        # Instantiate the new Firecrawl client
        client_kwargs: Dict[str, Any] = {"api_key": api_key}
        if api_url is not None:
            client_kwargs["api_url"] = api_url

        firecrawl = Firecrawl(**client_kwargs)

        params = params or {}
        params["integration"] = "llamaindex"

        super().__init__(
            firecrawl=firecrawl,
            api_key=api_key,
            api_url=api_url,
            mode=mode,
            params=params,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "Firecrawl_reader"

    defload_data(
        self,
        url: Optional[str] = None,
        query: Optional[str] = None,
        urls: Optional[List[str]] = None,
    ) -> List[Document]:
"""
        Load data from the input directory.

        Args:
            url (Optional[str]): URL to scrape or crawl.
            query (Optional[str]): Query to search for.
            urls (Optional[List[str]]): List of URLs for extract mode.

        Returns:
            List[Document]: List of documents.

        Raises:
            ValueError: If invalid combination of parameters is provided.

        """
        if sum(x is not None for x in [url, query, urls]) != 1:
            raise ValueError("Exactly one of url, query, or urls must be provided.")

        documents = []

        if self.mode == "scrape":
            # [SCRAPE] params: https://docs.firecrawl.dev/api-reference/endpoint/scrape
            if url is None:
                raise ValueError("URL must be provided for scrape mode.")
            # Map params to new client call signature
            scrape_params = self._params_copy()
            firecrawl_docs = self.firecrawl.scrape(url, **scrape_params)
            # Support both dict and SDK object responses
            text_value = ""
            metadata_value: Dict[str, Any] = {}

            if isinstance(firecrawl_docs, dict):
                # Newer API may return { success, data: {...} }
                data_obj = firecrawl_docs.get("data", firecrawl_docs)

                def_get_first(*keys: str) -> Optional[Any]:
                    for k in keys:
                        if (
                            isinstance(data_obj, dict)
                            and k in data_obj
                            and data_obj.get(k)
                        ):
                            return data_obj.get(k)
                    return None

                text_value = (
                    _get_first(
                        "markdown", "content", "html", "raw_html", "rawHtml", "summary"
                    )
                    or ""
                )

                meta_obj = (
                    data_obj.get("metadata", {}) if isinstance(data_obj, dict) else {}
                )
                if isinstance(meta_obj, dict):
                    metadata_value = meta_obj
                else:
                    # Convert metadata object to dict if needed
                    try:
                        if hasattr(meta_obj, "model_dump") and callable(
                            meta_obj.model_dump
                        ):
                            metadata_value = meta_obj.model_dump()  # type: ignore[attr-defined]
                        elif hasattr(meta_obj, "dict") and callable(meta_obj.dict):
                            metadata_value = meta_obj.dict()  # type: ignore[attr-defined]
                        elif hasattr(meta_obj, "__dict__"):
                            metadata_value = {
                                k: v
                                for k, v in vars(meta_obj).items()
                                if not k.startswith("_")
                            }
                    except Exception:
                        metadata_value = {"metadata": str(meta_obj)}

                # Capture other helpful fields into metadata
                if isinstance(data_obj, dict):
                    for extra_key in (
                        "links",
                        "actions",
                        "screenshot",
                        "warning",
                        "changeTracking",
                    ):
                        if (
                            extra_key in data_obj
                            and data_obj.get(extra_key) is not None
                        ):
                            metadata_value[extra_key] = data_obj.get(extra_key)
                # Bubble up success/warning if at top-level
                if "success" in firecrawl_docs:
                    metadata_value["success"] = firecrawl_docs.get("success")
                if (
                    "warning" in firecrawl_docs
                    and firecrawl_docs.get("warning") is not None
                ):
                    metadata_value["warning_top"] = firecrawl_docs.get("warning")
            else:
                # SDK object with attributes
                def_safe_get(obj: Any, *names: str) -> Optional[Any]:
                    for name in names:
                        try:
                            val = getattr(obj, name, None)
                        except Exception:
                            val = None
                        if val:
                            return val
                    return None

                text_value = (
                    _safe_get(
                        firecrawl_docs,
                        "markdown",
                        "content",
                        "html",
                        "raw_html",
                        "summary",
                    )
                    or ""
                )

                meta_obj = getattr(firecrawl_docs, "metadata", None)
                if meta_obj is not None:
                    try:
                        if hasattr(meta_obj, "model_dump") and callable(
                            meta_obj.model_dump
                        ):
                            metadata_value = meta_obj.model_dump()  # type: ignore[attr-defined]
                        elif hasattr(meta_obj, "dict") and callable(meta_obj.dict):
                            metadata_value = meta_obj.dict()  # type: ignore[attr-defined]
                        elif hasattr(meta_obj, "__dict__"):
                            metadata_value = {
                                k: v
                                for k, v in vars(meta_obj).items()
                                if not k.startswith("_")
                            }
                        else:
                            metadata_value = {"metadata": str(meta_obj)}
                    except Exception:
                        metadata_value = {"metadata": str(meta_obj)}

                # Attach extra top-level attributes if present on SDK object
                for extra_attr in (
                    "links",
                    "actions",
                    "screenshot",
                    "warning",
                    "change_tracking",
                ):
                    try:
                        extra_val = getattr(firecrawl_docs, extra_attr, None)
                    except Exception:
                        extra_val = None
                    if extra_val is not None:
                        metadata_value[extra_attr] = extra_val

            documents.append(Document(text=text_value or "", metadata=metadata_value))
        elif self.mode == "crawl":
            # [CRAWL] params: https://docs.firecrawl.dev/api-reference/endpoint/crawl-post
            if url is None:
                raise ValueError("URL must be provided for crawl mode.")
            crawl_params = self._params_copy()
            # Remove deprecated/unsupported parameters
            if "maxDepth" in crawl_params:
                crawl_params.pop("maxDepth", None)
            firecrawl_docs = self.firecrawl.crawl(url, **crawl_params)
            # Normalize Crawl response across SDK versions
            items: List[Any] = []
            if isinstance(firecrawl_docs, dict):
                data = firecrawl_docs.get("data", firecrawl_docs)
                if isinstance(data, list):
                    items = data
            else:
                # Try common list-bearing attributes first
                for attr_name in ("data", "results", "documents", "items", "pages"):
                    try:
                        candidate = getattr(firecrawl_docs, attr_name, None)
                    except Exception:
                        candidate = None
                    if isinstance(candidate, list) and candidate:
                        items = candidate
                        break
                # Fallback to model dump reflection
                if not items:
                    try:
                        if hasattr(firecrawl_docs, "model_dump") and callable(
                            firecrawl_docs.model_dump
                        ):
                            dump_obj = firecrawl_docs.model_dump()  # type: ignore[attr-defined]
                        elif hasattr(firecrawl_docs, "dict") and callable(
                            firecrawl_docs.dict
                        ):
                            dump_obj = firecrawl_docs.dict()  # type: ignore[attr-defined]
                        else:
                            dump_obj = {}
                    except Exception:
                        dump_obj = {}
                    if isinstance(dump_obj, dict):
                        data = (
                            dump_obj.get("data")
                            or dump_obj.get("results")
                            or dump_obj.get("documents")
                        )
                        if isinstance(data, list):
                            items = data

            for doc in items:
                if isinstance(doc, dict):
                    text_val = (
                        doc.get("markdown")
                        or doc.get("content")
                        or doc.get("text")
                        or ""
                    )
                    metadata_val = doc.get("metadata", {})
                else:
                    text_val = (
                        self._safe_get_attr(
                            doc,
                            "markdown",
                            "content",
                            "text",
                            "html",
                            "raw_html",
                            "rawHtml",
                            "summary",
                        )
                        or ""
                    )
                    meta_obj = getattr(doc, "metadata", None)
                    if isinstance(meta_obj, dict):
                        metadata_val = meta_obj
                    elif meta_obj is not None:
                        try:
                            metadata_val = self._to_dict_best_effort(meta_obj)
                        except Exception:
                            metadata_val = {"metadata": str(meta_obj)}
                    else:
                        metadata_val = {}
                documents.append(Document(text=text_val, metadata=metadata_val))
        elif self.mode == "map":
            # [MAP] params: https://docs.firecrawl.dev/api-reference/endpoint/map
            # Expected response: { "success": true, "links": [{"url":..., "title":..., "description":...}, ...] }
            if url is None:
                raise ValueError("URL must be provided for map mode.")

            map_params = self._params_copy()
            # Pass through optional parameters like sitemap, includeSubdomains, ignoreQueryParameters, limit, timeout, search
            response = self.firecrawl.map(url, **map_params)  # type: ignore[attr-defined]

            # Handle error response format: { "error": "..." }
            if (
                isinstance(response, dict)
                and "error" in response
                and not response.get("success", False)
            ):
                error_message = response.get("error", "Unknown error")
                documents.append(
                    Document(
                        text=f"Map request failed: {error_message}",
                        metadata={"source": "map", "url": url, "error": error_message},
                    )
                )
                return documents

            # Extract links from success response
            links = response.links or []

            for link in links:
                link_url = link.url
                title = link.title
                description = link.description
                text_content = title or description or link_url
                documents.append(
                    Document(
                        text=text_content,
                        metadata={
                            "source": "map",
                            "url": link_url,
                            "title": title,
                            "description": description,
                        },
                    )
                )
        elif self.mode == "search":
            # [SEARCH] params: https://docs.firecrawl.dev/api-reference/endpoint/search
            if query is None:
                raise ValueError("Query must be provided for search mode.")

            # Remove query from params if it exists to avoid duplicate
            search_params = self._params_copy()
            if "query" in search_params:
                del search_params["query"]

            # Get search results
            search_response = self.firecrawl.search(query, **search_params)

            # Handle the search response format
            if isinstance(search_response, dict):
                # Check for success
                if search_response.get("success", False):
                    # Get the data array
                    search_results = search_response.get("data", [])

                    # Process each search result
                    for result in search_results:
                        # Extract text content (prefer markdown if available)
                        text = result.get("markdown", "")
                        if not text:
                            # Fall back to description if markdown is not available
                            text = result.get("description", "")

                        # Extract metadata
                        metadata = {
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "description": result.get("description", ""),
                            "source": "search",
                            "query": query,
                        }

                        # Add additional metadata if available
                        if "metadata" in result and isinstance(
                            result["metadata"], dict
                        ):
                            metadata.update(result["metadata"])

                        # Create document
                        documents.append(
                            Document(
                                text=text,
                                metadata=metadata,
                            )
                        )
                else:
                    # Handle unsuccessful response
                    warning = search_response.get("warning", "Unknown error")
                    print(f"Search was unsuccessful: {warning}")
                    documents.append(
                        Document(
                            text=f"Search for '{query}' was unsuccessful: {warning}",
                            metadata={
                                "source": "search",
                                "query": query,
                                "error": warning,
                            },
                        )
                    )
            elif (
                hasattr(search_response, "web")
                or hasattr(search_response, "news")
                or hasattr(search_response, "images")
            ):
                # New SDK object response like: web=[SearchResultWeb(...)] news=None images=None
                def_process_results(result_list, result_type: str) -> None:
                    if not result_list:
                        return
                    for item in result_list:
                        # Try to access attributes with safe fallbacks
                        item_url = getattr(item, "url", "")
                        item_title = getattr(item, "title", "")
                        item_description = getattr(item, "description", "")
                        text_content = item_title or item_description or item_url

                        metadata = {
                            "title": item_title,
                            "url": item_url,
                            "description": item_description,
                            "source": "search",
                            "search_type": result_type,
                            "query": query,
                        }

                        # Collect all other attributes dynamically without whitelisting
                        base_keys = set(metadata.keys())

                        def_item_to_dict(obj: Any) -> Dict[str, Any]:
                            # pydantic v2
                            if hasattr(obj, "model_dump") and callable(obj.model_dump):
                                try:
                                    return obj.model_dump()  # type: ignore[attr-defined]
                                except Exception:
                                    pass
                            # pydantic v1
                            if hasattr(obj, "dict") and callable(obj.dict):
                                try:
                                    return obj.dict()  # type: ignore[attr-defined]
                                except Exception:
                                    pass
                            # dataclass or simple object
                            if hasattr(obj, "__dict__"):
                                try:
                                    return {
                                        k: v
                                        for k, v in vars(obj).items()
                                        if not k.startswith("_")
                                    }
                                except Exception:
                                    pass
                            # Fallback: reflect over attributes
                            result: Dict[str, Any] = {}
                            try:
                                for attr in dir(obj):
                                    if attr.startswith("_"):
                                        continue
                                    try:
                                        val = getattr(obj, attr)
                                    except Exception:
                                        continue
                                    if callable(val):
                                        continue
                                    result[attr] = val
                            except Exception:
                                pass
                            return result

                        extra_attrs = _item_to_dict(item)
                        for k, v in extra_attrs.items():
                            if k not in base_keys:
                                metadata[k] = v

                        documents.append(
                            Document(
                                text=text_content,
                                metadata=metadata,
                            )
                        )

                _process_results(getattr(search_response, "web", None), "web")  # type: ignore[attr-defined]
                _process_results(getattr(search_response, "news", None), "news")  # type: ignore[attr-defined]
                _process_results(getattr(search_response, "images", None), "images")  # type: ignore[attr-defined]
            else:
                # Handle unexpected response format
                print(f"Unexpected search response format: {type(search_response)}")
                documents.append(
                    Document(
                        text=str(search_response),
                        metadata={"source": "search", "query": query},
                    )
                )
        elif self.mode == "extract":
            # [EXTRACT] params: https://docs.firecrawl.dev/api-reference/endpoint/extract
            if urls is None:
                # For backward compatibility, convert single URL to list if provided
                if url is not None:
                    urls = [url]
                else:
                    raise ValueError("URLs must be provided for extract mode.")

            # Ensure we have a prompt in params
            extract_params = self._params_copy()
            if "prompt" not in extract_params:
                raise ValueError("A 'prompt' parameter is required for extract mode.")

            # Prepare the payload according to the new API structure
            payload = {"prompt": extract_params.pop("prompt")}
            payload["integration"] = "llamaindex"

            # Call the extract method with the urls and params
            extract_response = self.firecrawl.extract(urls=urls, **payload)

            # Handle the extract response format
            if isinstance(extract_response, dict):
                # Check for success
                if extract_response.get("success", False):
                    # Get the data from the response
                    extract_data = extract_response.get("data", {})

                    # Get the sources if available
                    sources = extract_response.get("sources", {})

                    # Convert the extracted data to text
                    if extract_data:
                        # Convert the data to a formatted string
                        text_parts = []
                        for key, value in extract_data.items():
                            text_parts.append(f"{key}: {value}")

                        text = "\n".join(text_parts)

                        # Create metadata
                        metadata = {
                            "urls": urls,
                            "source": "extract",
                            "status": extract_response.get("status"),
                            "expires_at": extract_response.get("expiresAt"),
                        }

                        # Add sources to metadata if available
                        if sources:
                            metadata["sources"] = sources

                        # Create document
                        documents.append(
                            Document(
                                text=text,
                                metadata=metadata,
                            )
                        )
                    else:
                        # Handle empty data in successful response
                        print("Extract response successful but no data returned")
                        documents.append(
                            Document(
                                text="Extraction was successful but no data was returned",
                                metadata={"urls": urls, "source": "extract"},
                            )
                        )
                else:
                    # Handle unsuccessful response
                    warning = extract_response.get("warning", "Unknown error")
                    print(f"Extraction was unsuccessful: {warning}")
                    documents.append(
                        Document(
                            text=f"Extraction was unsuccessful: {warning}",
                            metadata={
                                "urls": urls,
                                "source": "extract",
                                "error": warning,
                            },
                        )
                    )
            else:
                # Handle unexpected response format
                print(f"Unexpected extract response format: {type(extract_response)}")
                documents.append(
                    Document(
                        text=str(extract_response),
                        metadata={"urls": urls, "source": "extract"},
                    )
                )
        else:
            raise ValueError(
                "Invalid mode. Please choose 'scrape', 'crawl', 'search', or 'extract'."
            )

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.FireCrawlWebReader.load_data "Permanent link")

```
load_data(
    url: Optional[] = None,
    query: Optional[] = None,
    urls: Optional[[]] = None,
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  `Optional[str]`  |  URL to scrape or crawl.  |  `None`  |  
|  `query`  |  `Optional[str]`  |  Query to search for.  |  `None`  |  
|  `urls`  |  `Optional[List[str]]`  |  List of URLs for extract mode.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If invalid combination of parameters is provided.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/firecrawl_web/base.py`  
| 
```
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
```
 | 
```
defload_data(
    self,
    url: Optional[str] = None,
    query: Optional[str] = None,
    urls: Optional[List[str]] = None,
) -> List[Document]:
"""
    Load data from the input directory.

    Args:
        url (Optional[str]): URL to scrape or crawl.
        query (Optional[str]): Query to search for.
        urls (Optional[List[str]]): List of URLs for extract mode.

    Returns:
        List[Document]: List of documents.

    Raises:
        ValueError: If invalid combination of parameters is provided.

    """
    if sum(x is not None for x in [url, query, urls]) != 1:
        raise ValueError("Exactly one of url, query, or urls must be provided.")

    documents = []

    if self.mode == "scrape":
        # [SCRAPE] params: https://docs.firecrawl.dev/api-reference/endpoint/scrape
        if url is None:
            raise ValueError("URL must be provided for scrape mode.")
        # Map params to new client call signature
        scrape_params = self._params_copy()
        firecrawl_docs = self.firecrawl.scrape(url, **scrape_params)
        # Support both dict and SDK object responses
        text_value = ""
        metadata_value: Dict[str, Any] = {}

        if isinstance(firecrawl_docs, dict):
            # Newer API may return { success, data: {...} }
            data_obj = firecrawl_docs.get("data", firecrawl_docs)

            def_get_first(*keys: str) -> Optional[Any]:
                for k in keys:
                    if (
                        isinstance(data_obj, dict)
                        and k in data_obj
                        and data_obj.get(k)
                    ):
                        return data_obj.get(k)
                return None

            text_value = (
                _get_first(
                    "markdown", "content", "html", "raw_html", "rawHtml", "summary"
                )
                or ""
            )

            meta_obj = (
                data_obj.get("metadata", {}) if isinstance(data_obj, dict) else {}
            )
            if isinstance(meta_obj, dict):
                metadata_value = meta_obj
            else:
                # Convert metadata object to dict if needed
                try:
                    if hasattr(meta_obj, "model_dump") and callable(
                        meta_obj.model_dump
                    ):
                        metadata_value = meta_obj.model_dump()  # type: ignore[attr-defined]
                    elif hasattr(meta_obj, "dict") and callable(meta_obj.dict):
                        metadata_value = meta_obj.dict()  # type: ignore[attr-defined]
                    elif hasattr(meta_obj, "__dict__"):
                        metadata_value = {
                            k: v
                            for k, v in vars(meta_obj).items()
                            if not k.startswith("_")
                        }
                except Exception:
                    metadata_value = {"metadata": str(meta_obj)}

            # Capture other helpful fields into metadata
            if isinstance(data_obj, dict):
                for extra_key in (
                    "links",
                    "actions",
                    "screenshot",
                    "warning",
                    "changeTracking",
                ):
                    if (
                        extra_key in data_obj
                        and data_obj.get(extra_key) is not None
                    ):
                        metadata_value[extra_key] = data_obj.get(extra_key)
            # Bubble up success/warning if at top-level
            if "success" in firecrawl_docs:
                metadata_value["success"] = firecrawl_docs.get("success")
            if (
                "warning" in firecrawl_docs
                and firecrawl_docs.get("warning") is not None
            ):
                metadata_value["warning_top"] = firecrawl_docs.get("warning")
        else:
            # SDK object with attributes
            def_safe_get(obj: Any, *names: str) -> Optional[Any]:
                for name in names:
                    try:
                        val = getattr(obj, name, None)
                    except Exception:
                        val = None
                    if val:
                        return val
                return None

            text_value = (
                _safe_get(
                    firecrawl_docs,
                    "markdown",
                    "content",
                    "html",
                    "raw_html",
                    "summary",
                )
                or ""
            )

            meta_obj = getattr(firecrawl_docs, "metadata", None)
            if meta_obj is not None:
                try:
                    if hasattr(meta_obj, "model_dump") and callable(
                        meta_obj.model_dump
                    ):
                        metadata_value = meta_obj.model_dump()  # type: ignore[attr-defined]
                    elif hasattr(meta_obj, "dict") and callable(meta_obj.dict):
                        metadata_value = meta_obj.dict()  # type: ignore[attr-defined]
                    elif hasattr(meta_obj, "__dict__"):
                        metadata_value = {
                            k: v
                            for k, v in vars(meta_obj).items()
                            if not k.startswith("_")
                        }
                    else:
                        metadata_value = {"metadata": str(meta_obj)}
                except Exception:
                    metadata_value = {"metadata": str(meta_obj)}

            # Attach extra top-level attributes if present on SDK object
            for extra_attr in (
                "links",
                "actions",
                "screenshot",
                "warning",
                "change_tracking",
            ):
                try:
                    extra_val = getattr(firecrawl_docs, extra_attr, None)
                except Exception:
                    extra_val = None
                if extra_val is not None:
                    metadata_value[extra_attr] = extra_val

        documents.append(Document(text=text_value or "", metadata=metadata_value))
    elif self.mode == "crawl":
        # [CRAWL] params: https://docs.firecrawl.dev/api-reference/endpoint/crawl-post
        if url is None:
            raise ValueError("URL must be provided for crawl mode.")
        crawl_params = self._params_copy()
        # Remove deprecated/unsupported parameters
        if "maxDepth" in crawl_params:
            crawl_params.pop("maxDepth", None)
        firecrawl_docs = self.firecrawl.crawl(url, **crawl_params)
        # Normalize Crawl response across SDK versions
        items: List[Any] = []
        if isinstance(firecrawl_docs, dict):
            data = firecrawl_docs.get("data", firecrawl_docs)
            if isinstance(data, list):
                items = data
        else:
            # Try common list-bearing attributes first
            for attr_name in ("data", "results", "documents", "items", "pages"):
                try:
                    candidate = getattr(firecrawl_docs, attr_name, None)
                except Exception:
                    candidate = None
                if isinstance(candidate, list) and candidate:
                    items = candidate
                    break
            # Fallback to model dump reflection
            if not items:
                try:
                    if hasattr(firecrawl_docs, "model_dump") and callable(
                        firecrawl_docs.model_dump
                    ):
                        dump_obj = firecrawl_docs.model_dump()  # type: ignore[attr-defined]
                    elif hasattr(firecrawl_docs, "dict") and callable(
                        firecrawl_docs.dict
                    ):
                        dump_obj = firecrawl_docs.dict()  # type: ignore[attr-defined]
                    else:
                        dump_obj = {}
                except Exception:
                    dump_obj = {}
                if isinstance(dump_obj, dict):
                    data = (
                        dump_obj.get("data")
                        or dump_obj.get("results")
                        or dump_obj.get("documents")
                    )
                    if isinstance(data, list):
                        items = data

        for doc in items:
            if isinstance(doc, dict):
                text_val = (
                    doc.get("markdown")
                    or doc.get("content")
                    or doc.get("text")
                    or ""
                )
                metadata_val = doc.get("metadata", {})
            else:
                text_val = (
                    self._safe_get_attr(
                        doc,
                        "markdown",
                        "content",
                        "text",
                        "html",
                        "raw_html",
                        "rawHtml",
                        "summary",
                    )
                    or ""
                )
                meta_obj = getattr(doc, "metadata", None)
                if isinstance(meta_obj, dict):
                    metadata_val = meta_obj
                elif meta_obj is not None:
                    try:
                        metadata_val = self._to_dict_best_effort(meta_obj)
                    except Exception:
                        metadata_val = {"metadata": str(meta_obj)}
                else:
                    metadata_val = {}
            documents.append(Document(text=text_val, metadata=metadata_val))
    elif self.mode == "map":
        # [MAP] params: https://docs.firecrawl.dev/api-reference/endpoint/map
        # Expected response: { "success": true, "links": [{"url":..., "title":..., "description":...}, ...] }
        if url is None:
            raise ValueError("URL must be provided for map mode.")

        map_params = self._params_copy()
        # Pass through optional parameters like sitemap, includeSubdomains, ignoreQueryParameters, limit, timeout, search
        response = self.firecrawl.map(url, **map_params)  # type: ignore[attr-defined]

        # Handle error response format: { "error": "..." }
        if (
            isinstance(response, dict)
            and "error" in response
            and not response.get("success", False)
        ):
            error_message = response.get("error", "Unknown error")
            documents.append(
                Document(
                    text=f"Map request failed: {error_message}",
                    metadata={"source": "map", "url": url, "error": error_message},
                )
            )
            return documents

        # Extract links from success response
        links = response.links or []

        for link in links:
            link_url = link.url
            title = link.title
            description = link.description
            text_content = title or description or link_url
            documents.append(
                Document(
                    text=text_content,
                    metadata={
                        "source": "map",
                        "url": link_url,
                        "title": title,
                        "description": description,
                    },
                )
            )
    elif self.mode == "search":
        # [SEARCH] params: https://docs.firecrawl.dev/api-reference/endpoint/search
        if query is None:
            raise ValueError("Query must be provided for search mode.")

        # Remove query from params if it exists to avoid duplicate
        search_params = self._params_copy()
        if "query" in search_params:
            del search_params["query"]

        # Get search results
        search_response = self.firecrawl.search(query, **search_params)

        # Handle the search response format
        if isinstance(search_response, dict):
            # Check for success
            if search_response.get("success", False):
                # Get the data array
                search_results = search_response.get("data", [])

                # Process each search result
                for result in search_results:
                    # Extract text content (prefer markdown if available)
                    text = result.get("markdown", "")
                    if not text:
                        # Fall back to description if markdown is not available
                        text = result.get("description", "")

                    # Extract metadata
                    metadata = {
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "description": result.get("description", ""),
                        "source": "search",
                        "query": query,
                    }

                    # Add additional metadata if available
                    if "metadata" in result and isinstance(
                        result["metadata"], dict
                    ):
                        metadata.update(result["metadata"])

                    # Create document
                    documents.append(
                        Document(
                            text=text,
                            metadata=metadata,
                        )
                    )
            else:
                # Handle unsuccessful response
                warning = search_response.get("warning", "Unknown error")
                print(f"Search was unsuccessful: {warning}")
                documents.append(
                    Document(
                        text=f"Search for '{query}' was unsuccessful: {warning}",
                        metadata={
                            "source": "search",
                            "query": query,
                            "error": warning,
                        },
                    )
                )
        elif (
            hasattr(search_response, "web")
            or hasattr(search_response, "news")
            or hasattr(search_response, "images")
        ):
            # New SDK object response like: web=[SearchResultWeb(...)] news=None images=None
            def_process_results(result_list, result_type: str) -> None:
                if not result_list:
                    return
                for item in result_list:
                    # Try to access attributes with safe fallbacks
                    item_url = getattr(item, "url", "")
                    item_title = getattr(item, "title", "")
                    item_description = getattr(item, "description", "")
                    text_content = item_title or item_description or item_url

                    metadata = {
                        "title": item_title,
                        "url": item_url,
                        "description": item_description,
                        "source": "search",
                        "search_type": result_type,
                        "query": query,
                    }

                    # Collect all other attributes dynamically without whitelisting
                    base_keys = set(metadata.keys())

                    def_item_to_dict(obj: Any) -> Dict[str, Any]:
                        # pydantic v2
                        if hasattr(obj, "model_dump") and callable(obj.model_dump):
                            try:
                                return obj.model_dump()  # type: ignore[attr-defined]
                            except Exception:
                                pass
                        # pydantic v1
                        if hasattr(obj, "dict") and callable(obj.dict):
                            try:
                                return obj.dict()  # type: ignore[attr-defined]
                            except Exception:
                                pass
                        # dataclass or simple object
                        if hasattr(obj, "__dict__"):
                            try:
                                return {
                                    k: v
                                    for k, v in vars(obj).items()
                                    if not k.startswith("_")
                                }
                            except Exception:
                                pass
                        # Fallback: reflect over attributes
                        result: Dict[str, Any] = {}
                        try:
                            for attr in dir(obj):
                                if attr.startswith("_"):
                                    continue
                                try:
                                    val = getattr(obj, attr)
                                except Exception:
                                    continue
                                if callable(val):
                                    continue
                                result[attr] = val
                        except Exception:
                            pass
                        return result

                    extra_attrs = _item_to_dict(item)
                    for k, v in extra_attrs.items():
                        if k not in base_keys:
                            metadata[k] = v

                    documents.append(
                        Document(
                            text=text_content,
                            metadata=metadata,
                        )
                    )

            _process_results(getattr(search_response, "web", None), "web")  # type: ignore[attr-defined]
            _process_results(getattr(search_response, "news", None), "news")  # type: ignore[attr-defined]
            _process_results(getattr(search_response, "images", None), "images")  # type: ignore[attr-defined]
        else:
            # Handle unexpected response format
            print(f"Unexpected search response format: {type(search_response)}")
            documents.append(
                Document(
                    text=str(search_response),
                    metadata={"source": "search", "query": query},
                )
            )
    elif self.mode == "extract":
        # [EXTRACT] params: https://docs.firecrawl.dev/api-reference/endpoint/extract
        if urls is None:
            # For backward compatibility, convert single URL to list if provided
            if url is not None:
                urls = [url]
            else:
                raise ValueError("URLs must be provided for extract mode.")

        # Ensure we have a prompt in params
        extract_params = self._params_copy()
        if "prompt" not in extract_params:
            raise ValueError("A 'prompt' parameter is required for extract mode.")

        # Prepare the payload according to the new API structure
        payload = {"prompt": extract_params.pop("prompt")}
        payload["integration"] = "llamaindex"

        # Call the extract method with the urls and params
        extract_response = self.firecrawl.extract(urls=urls, **payload)

        # Handle the extract response format
        if isinstance(extract_response, dict):
            # Check for success
            if extract_response.get("success", False):
                # Get the data from the response
                extract_data = extract_response.get("data", {})

                # Get the sources if available
                sources = extract_response.get("sources", {})

                # Convert the extracted data to text
                if extract_data:
                    # Convert the data to a formatted string
                    text_parts = []
                    for key, value in extract_data.items():
                        text_parts.append(f"{key}: {value}")

                    text = "\n".join(text_parts)

                    # Create metadata
                    metadata = {
                        "urls": urls,
                        "source": "extract",
                        "status": extract_response.get("status"),
                        "expires_at": extract_response.get("expiresAt"),
                    }

                    # Add sources to metadata if available
                    if sources:
                        metadata["sources"] = sources

                    # Create document
                    documents.append(
                        Document(
                            text=text,
                            metadata=metadata,
                        )
                    )
                else:
                    # Handle empty data in successful response
                    print("Extract response successful but no data returned")
                    documents.append(
                        Document(
                            text="Extraction was successful but no data was returned",
                            metadata={"urls": urls, "source": "extract"},
                        )
                    )
            else:
                # Handle unsuccessful response
                warning = extract_response.get("warning", "Unknown error")
                print(f"Extraction was unsuccessful: {warning}")
                documents.append(
                    Document(
                        text=f"Extraction was unsuccessful: {warning}",
                        metadata={
                            "urls": urls,
                            "source": "extract",
                            "error": warning,
                        },
                    )
                )
        else:
            # Handle unexpected response format
            print(f"Unexpected extract response format: {type(extract_response)}")
            documents.append(
                Document(
                    text=str(extract_response),
                    metadata={"urls": urls, "source": "extract"},
                )
            )
    else:
        raise ValueError(
            "Invalid mode. Please choose 'scrape', 'crawl', 'search', or 'extract'."
        )

    return documents

```
 |  
| --- | --- |  
##  HyperbrowserWebReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.HyperbrowserWebReader "Permanent link")
Bases: 
Hyperbrowser Web Reader.
Scrape or crawl web pages with optional parameters for configuring content extraction. Requires the `hyperbrowser` package. Get your API Key from https://app.hyperbrowser.ai/
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  `Optional[str]`  |  The Hyperbrowser API key, can be set as an environment variable `HYPERBROWSER_API_KEY` or passed directly  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/hyperbrowser_web/base.py`  
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
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
```
 | 
```
classHyperbrowserWebReader(BaseReader):
"""
    Hyperbrowser Web Reader.

    Scrape or crawl web pages with optional parameters for configuring content extraction.
    Requires the `hyperbrowser` package.
    Get your API Key from https://app.hyperbrowser.ai/

    Args:
        api_key: The Hyperbrowser API key, can be set as an environment variable `HYPERBROWSER_API_KEY` or passed directly

    """

    def__init__(self, api_key: Optional[str] = None):
        api_key = api_key or os.getenv("HYPERBROWSER_API_KEY")
        if not api_key:
            raise ValueError(
                "`api_key` is required, please set the `HYPERBROWSER_API_KEY` environment variable or pass it directly"
            )

        try:
            fromhyperbrowserimport Hyperbrowser, AsyncHyperbrowser
        except ImportError:
            raise ImportError(
                "`hyperbrowser` package not found, please run `pip install hyperbrowser`"
            )

        self.hyperbrowser = Hyperbrowser(api_key=api_key)
        self.async_hyperbrowser = AsyncHyperbrowser(api_key=api_key)

    def_prepare_params(self, params: Dict) -> Dict:
"""Prepare session and scrape options parameters."""
        try:
            fromhyperbrowser.models.sessionimport CreateSessionParams
            fromhyperbrowser.models.scrapeimport ScrapeOptions
        except ImportError:
            raise ImportError(
                "`hyperbrowser` package not found, please run `pip install hyperbrowser`"
            )

        if "scrape_options" in params:
            if "formats" in params["scrape_options"]:
                formats = params["scrape_options"]["formats"]
                if not all(fmt in ["markdown", "html"] for fmt in formats):
                    raise ValueError("formats can only contain 'markdown' or 'html'")

        if "session_options" in params:
            params["session_options"] = CreateSessionParams(**params["session_options"])
        if "scrape_options" in params:
            params["scrape_options"] = ScrapeOptions(**params["scrape_options"])
        return params

    def_create_document(self, content: str, metadata: dict) -> Document:
"""Create a Document with text and metadata."""
        return Document(text=content, metadata=metadata)

    def_extract_content_metadata(self, data: Union[Any, None]):
"""Extract content and metadata from response data."""
        content = ""
        metadata = {}
        if data:
            content = data.markdown or data.html or ""
            if data.metadata:
                metadata = data.metadata
        return content, metadata

    deflazy_load_data(
        self,
        urls: List[str],
        operation: Literal["scrape", "crawl"] = "scrape",
        params: Optional[Dict] = {},
    ) -> Iterable[Document]:
"""
        Lazy load documents.

        Args:
            urls: List of URLs to scrape or crawl
            operation: Operation to perform. Can be "scrape" or "crawl"
            params: Optional params for scrape or crawl. For more information on the supported params, visit https://docs.hyperbrowser.ai/reference/sdks/python/scrape#start-scrape-job-and-wait or https://docs.hyperbrowser.ai/reference/sdks/python/crawl#start-crawl-job-and-wait

        """
        try:
            fromhyperbrowser.models.scrapeimport StartScrapeJobParams
            fromhyperbrowser.models.crawlimport StartCrawlJobParams
        except ImportError:
            raise ImportError(
                "`hyperbrowser` package not found, please run `pip install hyperbrowser`"
            )

        if operation == "crawl" and len(urls)  1:
            raise ValueError("`crawl` operation can only accept a single URL")
        params = self._prepare_params(params)

        if operation == "scrape":
            for url in urls:
                scrape_params = StartScrapeJobParams(url=url, **params)
                try:
                    scrape_resp = self.hyperbrowser.scrape.start_and_wait(scrape_params)
                    content, metadata = self._extract_content_metadata(scrape_resp.data)
                    yield self._create_document(content, metadata)
                except Exception as e:
                    logger.error(f"Error scraping {url}: {e}")
                    yield self._create_document("", {})
        else:
            crawl_params = StartCrawlJobParams(url=urls[0], **params)
            try:
                crawl_resp = self.hyperbrowser.crawl.start_and_wait(crawl_params)
                for page in crawl_resp.data:
                    content = page.markdown or page.html or ""
                    yield self._create_document(content, page.metadata or {})
            except Exception as e:
                logger.error(f"Error crawling {urls[0]}: {e}")
                yield self._create_document("", {})

    async defalazy_load_data(
        self,
        urls: Sequence[str],
        operation: Literal["scrape", "crawl"] = "scrape",
        params: Optional[Dict] = {},
    ) -> AsyncIterable[Document]:
"""
        Async lazy load documents.

        Args:
            urls: List of URLs to scrape or crawl
            operation: Operation to perform. Can be "scrape" or "crawl"
            params: Optional params for scrape or crawl. For more information on the supported params, visit https://docs.hyperbrowser.ai/reference/sdks/python/scrape#start-scrape-job-and-wait or https://docs.hyperbrowser.ai/reference/sdks/python/crawl#start-crawl-job-and-wait

        """
        try:
            fromhyperbrowser.models.scrapeimport StartScrapeJobParams
            fromhyperbrowser.models.crawlimport StartCrawlJobParams
        except ImportError:
            raise ImportError(
                "`hyperbrowser` package not found, please run `pip install hyperbrowser`"
            )

        if operation == "crawl" and len(urls)  1:
            raise ValueError("`crawl` operation can only accept a single URL")
        params = self._prepare_params(params)

        if operation == "scrape":
            for url in urls:
                scrape_params = StartScrapeJobParams(url=url, **params)
                try:
                    scrape_resp = await self.async_hyperbrowser.scrape.start_and_wait(
                        scrape_params
                    )
                    content, metadata = self._extract_content_metadata(scrape_resp.data)
                    yield self._create_document(content, metadata)
                except Exception as e:
                    logger.error(f"Error scraping {url}: {e}")
                    yield self._create_document("", {})
        else:
            crawl_params = StartCrawlJobParams(url=urls[0], **params)
            try:
                crawl_resp = await self.async_hyperbrowser.crawl.start_and_wait(
                    crawl_params
                )
                for page in crawl_resp.data:
                    content = page.markdown or page.html or ""
                    yield self._create_document(content, page.metadata or {})
            except Exception as e:
                logger.error(f"Error crawling {urls[0]}: {e}")
                yield self._create_document("", {})

```
 |  
| --- | --- |  
###  lazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.HyperbrowserWebReader.lazy_load_data "Permanent link")

```
lazy_load_data(
    urls: [],
    operation: Literal["scrape", "crawl"] = "scrape",
    params: Optional[] = {},
) -> Iterable[]

```

Lazy load documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List of URLs to scrape or crawl  |  _required_  |  
|  `operation`  |  `Literal['scrape', 'crawl']`  |  Operation to perform. Can be "scrape" or "crawl"  |  `'scrape'`  |  
|  `params`  |  `Optional[Dict]`  |  Optional params for scrape or crawl. For more information on the supported params, visit https://docs.hyperbrowser.ai/reference/sdks/python/scrape#start-scrape-job-and-wait or https://docs.hyperbrowser.ai/reference/sdks/python/crawl#start-crawl-job-and-wait  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/hyperbrowser_web/base.py`  
| 
```
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
```
 | 
```
deflazy_load_data(
    self,
    urls: List[str],
    operation: Literal["scrape", "crawl"] = "scrape",
    params: Optional[Dict] = {},
) -> Iterable[Document]:
"""
    Lazy load documents.

    Args:
        urls: List of URLs to scrape or crawl
        operation: Operation to perform. Can be "scrape" or "crawl"
        params: Optional params for scrape or crawl. For more information on the supported params, visit https://docs.hyperbrowser.ai/reference/sdks/python/scrape#start-scrape-job-and-wait or https://docs.hyperbrowser.ai/reference/sdks/python/crawl#start-crawl-job-and-wait

    """
    try:
        fromhyperbrowser.models.scrapeimport StartScrapeJobParams
        fromhyperbrowser.models.crawlimport StartCrawlJobParams
    except ImportError:
        raise ImportError(
            "`hyperbrowser` package not found, please run `pip install hyperbrowser`"
        )

    if operation == "crawl" and len(urls)  1:
        raise ValueError("`crawl` operation can only accept a single URL")
    params = self._prepare_params(params)

    if operation == "scrape":
        for url in urls:
            scrape_params = StartScrapeJobParams(url=url, **params)
            try:
                scrape_resp = self.hyperbrowser.scrape.start_and_wait(scrape_params)
                content, metadata = self._extract_content_metadata(scrape_resp.data)
                yield self._create_document(content, metadata)
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                yield self._create_document("", {})
    else:
        crawl_params = StartCrawlJobParams(url=urls[0], **params)
        try:
            crawl_resp = self.hyperbrowser.crawl.start_and_wait(crawl_params)
            for page in crawl_resp.data:
                content = page.markdown or page.html or ""
                yield self._create_document(content, page.metadata or {})
        except Exception as e:
            logger.error(f"Error crawling {urls[0]}: {e}")
            yield self._create_document("", {})

```
 |  
| --- | --- |  
###  alazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.HyperbrowserWebReader.alazy_load_data "Permanent link")

```
alazy_load_data(
    urls: Sequence[],
    operation: Literal["scrape", "crawl"] = "scrape",
    params: Optional[] = {},
) -> AsyncIterable[]

```

Async lazy load documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `Sequence[str]`  |  List of URLs to scrape or crawl  |  _required_  |  
|  `operation`  |  `Literal['scrape', 'crawl']`  |  Operation to perform. Can be "scrape" or "crawl"  |  `'scrape'`  |  
|  `params`  |  `Optional[Dict]`  |  Optional params for scrape or crawl. For more information on the supported params, visit https://docs.hyperbrowser.ai/reference/sdks/python/scrape#start-scrape-job-and-wait or https://docs.hyperbrowser.ai/reference/sdks/python/crawl#start-crawl-job-and-wait  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/hyperbrowser_web/base.py`  
| 
```
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
```
 | 
```
async defalazy_load_data(
    self,
    urls: Sequence[str],
    operation: Literal["scrape", "crawl"] = "scrape",
    params: Optional[Dict] = {},
) -> AsyncIterable[Document]:
"""
    Async lazy load documents.

    Args:
        urls: List of URLs to scrape or crawl
        operation: Operation to perform. Can be "scrape" or "crawl"
        params: Optional params for scrape or crawl. For more information on the supported params, visit https://docs.hyperbrowser.ai/reference/sdks/python/scrape#start-scrape-job-and-wait or https://docs.hyperbrowser.ai/reference/sdks/python/crawl#start-crawl-job-and-wait

    """
    try:
        fromhyperbrowser.models.scrapeimport StartScrapeJobParams
        fromhyperbrowser.models.crawlimport StartCrawlJobParams
    except ImportError:
        raise ImportError(
            "`hyperbrowser` package not found, please run `pip install hyperbrowser`"
        )

    if operation == "crawl" and len(urls)  1:
        raise ValueError("`crawl` operation can only accept a single URL")
    params = self._prepare_params(params)

    if operation == "scrape":
        for url in urls:
            scrape_params = StartScrapeJobParams(url=url, **params)
            try:
                scrape_resp = await self.async_hyperbrowser.scrape.start_and_wait(
                    scrape_params
                )
                content, metadata = self._extract_content_metadata(scrape_resp.data)
                yield self._create_document(content, metadata)
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                yield self._create_document("", {})
    else:
        crawl_params = StartCrawlJobParams(url=urls[0], **params)
        try:
            crawl_resp = await self.async_hyperbrowser.crawl.start_and_wait(
                crawl_params
            )
            for page in crawl_resp.data:
                content = page.markdown or page.html or ""
                yield self._create_document(content, page.metadata or {})
        except Exception as e:
            logger.error(f"Error crawling {urls[0]}: {e}")
            yield self._create_document("", {})

```
 |  
| --- | --- |  
##  KnowledgeBaseWebReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.KnowledgeBaseWebReader "Permanent link")
Bases: 
Knowledge base reader.
Crawls and reads articles from a knowledge base/help center with Playwright. Tested on Zendesk and Intercom CMS, may work on others. Can be run in headless mode but it may be blocked by Cloudflare. Run it headed to be safe. Times out occasionally, just increase the default time out if it does. Requires the `playwright` package.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `root_url`  |  the base url of the knowledge base, with no trailing slash e.g. 'https://support.intercom.com'  |  _required_  |  
|  `link_selectors`  |  `List[str]`  |  list of css selectors to find links to articles while crawling e.g. ['.article-list a', '.article-list a']  |  _required_  |  
|  `article_path`  |  the url path of articles on this domain so the crawler knows when to stop e.g. '/articles'  |  _required_  |  
|  `title_selector`  |  `Optional[str]`  |  css selector to find the title of the article e.g. '.article-title'  |  `None`  |  
|  `subtitle_selector`  |  `Optional[str]`  |  css selector to find the subtitle/description of the article e.g. '.article-subtitle'  |  `None`  |  
|  `body_selector`  |  `Optional[str]`  |  css selector to find the body of the article e.g. '.article-body'  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/knowledge_base/base.py`  
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
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
```
 | 
```
classKnowledgeBaseWebReader(BaseReader):
"""
    Knowledge base reader.

    Crawls and reads articles from a knowledge base/help center with Playwright.
    Tested on Zendesk and Intercom CMS, may work on others.
    Can be run in headless mode but it may be blocked by Cloudflare. Run it headed to be safe.
    Times out occasionally, just increase the default time out if it does.
    Requires the `playwright` package.

    Args:
        root_url (str): the base url of the knowledge base, with no trailing slash
            e.g. 'https://support.intercom.com'
        link_selectors (List[str]): list of css selectors to find links to articles while crawling
            e.g. ['.article-list a', '.article-list a']
        article_path (str): the url path of articles on this domain so the crawler knows when to stop
            e.g. '/articles'
        title_selector (Optional[str]): css selector to find the title of the article
            e.g. '.article-title'
        subtitle_selector (Optional[str]): css selector to find the subtitle/description of the article
            e.g. '.article-subtitle'
        body_selector (Optional[str]): css selector to find the body of the article
            e.g. '.article-body'

    """

    def__init__(
        self,
        root_url: str,
        link_selectors: List[str],
        article_path: str,
        title_selector: Optional[str] = None,
        subtitle_selector: Optional[str] = None,
        body_selector: Optional[str] = None,
        max_depth: int = 100,
    ) -> None:
"""Initialize with parameters."""
        self.root_url = root_url
        self.link_selectors = link_selectors
        self.article_path = article_path
        self.title_selector = title_selector
        self.subtitle_selector = subtitle_selector
        self.body_selector = body_selector
        self.max_depth = max_depth

    defload_data(self) -> List[Document]:
"""Load data from the knowledge base."""
        fromplaywright.sync_apiimport sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)

            # Crawl
            article_urls = self.get_article_urls(
                browser, self.root_url, self.root_url, self.max_depth
            )

            # Scrape
            documents = []
            for url in article_urls:
                article = self.scrape_article(
                    browser,
                    url,
                )
                extra_info = {
                    "title": article["title"],
                    "subtitle": article["subtitle"],
                    "url": article["url"],
                }
                documents.append(Document(text=article["body"], extra_info=extra_info))

            browser.close()

            return documents

    defscrape_article(
        self,
        browser: Any,
        url: str,
    ) -> Dict[str, str]:
"""
        Scrape a single article url.

        Args:
            browser (Any): a Playwright Chromium browser.
            url (str): URL of the article to scrape.

        Returns:
            Dict[str, str]: a mapping of article attributes to their values.

        """
        page = browser.new_page(ignore_https_errors=True)
        page.set_default_timeout(60000)
        page.goto(url, wait_until="domcontentloaded")

        title = (
            (
                page.query_selector(self.title_selector).evaluate(
                    "node => node.innerText"
                )
            )
            if self.title_selector
            else ""
        )
        subtitle = (
            (
                page.query_selector(self.subtitle_selector).evaluate(
                    "node => node.innerText"
                )
            )
            if self.subtitle_selector
            else ""
        )
        body = (
            (page.query_selector(self.body_selector).evaluate("node => node.innerText"))
            if self.body_selector
            else ""
        )

        page.close()
        print("scraped:", url)
        return {"title": title, "subtitle": subtitle, "body": body, "url": url}

    defget_article_urls(
        self,
        browser: Any,
        root_url: str,
        current_url: str,
        max_depth: int = 100,
        depth: int = 0,
    ) -> List[str]:
"""
        Recursively crawl through the knowledge base to find a list of articles.

        Args:
            browser (Any): a Playwright Chromium browser.
            root_url (str): root URL of the knowledge base.
            current_url (str): current URL that is being crawled.
            max_depth (int): maximum recursion level for the crawler
            depth (int): current depth level

        Returns:
            List[str]: a list of URLs of found articles.

        """
        if depth >= max_depth:
            print(f"Reached max depth ({max_depth}): {current_url}")
            return []

        page = browser.new_page(ignore_https_errors=True)
        page.set_default_timeout(60000)
        page.goto(current_url, wait_until="domcontentloaded")

        # If this is a leaf node aka article page, return itself
        if self.article_path in current_url:
            print("Found an article: ", current_url)
            page.close()
            return [current_url]

        # Otherwise crawl this page and find all the articles linked from it
        article_urls = []
        links = []

        for link_selector in self.link_selectors:
            ahrefs = page.query_selector_all(link_selector)
            links.extend(ahrefs)

        for link in links:
            url = root_url + page.evaluate("(node) => node.getAttribute('href')", link)
            article_urls.extend(
                self.get_article_urls(browser, root_url, url, max_depth, depth + 1)
            )

        page.close()

        return article_urls

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.KnowledgeBaseWebReader.load_data "Permanent link")

```
load_data() -> []

```

Load data from the knowledge base.
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/knowledge_base/base.py`  
| 
```
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
```
 | 
```
defload_data(self) -> List[Document]:
"""Load data from the knowledge base."""
    fromplaywright.sync_apiimport sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Crawl
        article_urls = self.get_article_urls(
            browser, self.root_url, self.root_url, self.max_depth
        )

        # Scrape
        documents = []
        for url in article_urls:
            article = self.scrape_article(
                browser,
                url,
            )
            extra_info = {
                "title": article["title"],
                "subtitle": article["subtitle"],
                "url": article["url"],
            }
            documents.append(Document(text=article["body"], extra_info=extra_info))

        browser.close()

        return documents

```
 |  
| --- | --- |  
###  scrape_article [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.KnowledgeBaseWebReader.scrape_article "Permanent link")

```
scrape_article(browser: , url: ) -> [, ]

```

Scrape a single article url.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `browser`  |  a Playwright Chromium browser.  |  _required_  |  
|  `url`  |  URL of the article to scrape.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, str]`  |  Dict[str, str]: a mapping of article attributes to their values.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/knowledge_base/base.py`  
| 
```
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
```
 | 
```
defscrape_article(
    self,
    browser: Any,
    url: str,
) -> Dict[str, str]:
"""
    Scrape a single article url.

    Args:
        browser (Any): a Playwright Chromium browser.
        url (str): URL of the article to scrape.

    Returns:
        Dict[str, str]: a mapping of article attributes to their values.

    """
    page = browser.new_page(ignore_https_errors=True)
    page.set_default_timeout(60000)
    page.goto(url, wait_until="domcontentloaded")

    title = (
        (
            page.query_selector(self.title_selector).evaluate(
                "node => node.innerText"
            )
        )
        if self.title_selector
        else ""
    )
    subtitle = (
        (
            page.query_selector(self.subtitle_selector).evaluate(
                "node => node.innerText"
            )
        )
        if self.subtitle_selector
        else ""
    )
    body = (
        (page.query_selector(self.body_selector).evaluate("node => node.innerText"))
        if self.body_selector
        else ""
    )

    page.close()
    print("scraped:", url)
    return {"title": title, "subtitle": subtitle, "body": body, "url": url}

```
 |  
| --- | --- |  
###  get_article_urls [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.KnowledgeBaseWebReader.get_article_urls "Permanent link")

```
get_article_urls(
    browser: ,
    root_url: ,
    current_url: ,
    max_depth:  = 100,
    depth:  = 0,
) -> []

```

Recursively crawl through the knowledge base to find a list of articles.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `browser`  |  a Playwright Chromium browser.  |  _required_  |  
|  `root_url`  |  root URL of the knowledge base.  |  _required_  |  
|  `current_url`  |  current URL that is being crawled.  |  _required_  |  
|  `max_depth`  |  maximum recursion level for the crawler  |  `100`  |  
|  `depth`  |  current depth level  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: a list of URLs of found articles.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/knowledge_base/base.py`  
| 
```
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
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
```
 | 
```
defget_article_urls(
    self,
    browser: Any,
    root_url: str,
    current_url: str,
    max_depth: int = 100,
    depth: int = 0,
) -> List[str]:
"""
    Recursively crawl through the knowledge base to find a list of articles.

    Args:
        browser (Any): a Playwright Chromium browser.
        root_url (str): root URL of the knowledge base.
        current_url (str): current URL that is being crawled.
        max_depth (int): maximum recursion level for the crawler
        depth (int): current depth level

    Returns:
        List[str]: a list of URLs of found articles.

    """
    if depth >= max_depth:
        print(f"Reached max depth ({max_depth}): {current_url}")
        return []

    page = browser.new_page(ignore_https_errors=True)
    page.set_default_timeout(60000)
    page.goto(current_url, wait_until="domcontentloaded")

    # If this is a leaf node aka article page, return itself
    if self.article_path in current_url:
        print("Found an article: ", current_url)
        page.close()
        return [current_url]

    # Otherwise crawl this page and find all the articles linked from it
    article_urls = []
    links = []

    for link_selector in self.link_selectors:
        ahrefs = page.query_selector_all(link_selector)
        links.extend(ahrefs)

    for link in links:
        url = root_url + page.evaluate("(node) => node.getAttribute('href')", link)
        article_urls.extend(
            self.get_article_urls(browser, root_url, url, max_depth, depth + 1)
        )

    page.close()

    return article_urls

```
 |  
| --- | --- |  
##  MainContentExtractorReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.MainContentExtractorReader "Permanent link")
Bases: 
MainContentExtractor web page reader.
Reads pages from the web.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `text_format`  |  The format of the text. Defaults to "markdown". Requires `MainContentExtractor` package.  |  `'markdown'`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/main_content_extractor/base.py`  
| 
```
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
46
47
48
49
```
 | 
```
classMainContentExtractorReader(BaseReader):
"""
    MainContentExtractor web page reader.

    Reads pages from the web.

    Args:
        text_format (str, optional): The format of the text. Defaults to "markdown".
            Requires `MainContentExtractor` package.

    """

    def__init__(self, text_format: str = "markdown") -> None:
"""Initialize with parameters."""
        self.text_format = text_format

    defload_data(self, urls: List[str]) -> List[Document]:
"""
        Load data from the input directory.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[Document]: List of documents.

        """
        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")

        frommain_content_extractorimport MainContentExtractor

        documents = []
        for url in urls:
            response = requests.get(url).text
            response = MainContentExtractor.extract(
                response, output_format=self.text_format, include_links=False
            )

            documents.append(Document(text=response))

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.MainContentExtractorReader.load_data "Permanent link")

```
load_data(urls: []) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List of URLs to scrape.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/main_content_extractor/base.py`  
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
```
 | 
```
defload_data(self, urls: List[str]) -> List[Document]:
"""
    Load data from the input directory.

    Args:
        urls (List[str]): List of URLs to scrape.

    Returns:
        List[Document]: List of documents.

    """
    if not isinstance(urls, list):
        raise ValueError("urls must be a list of strings.")

    frommain_content_extractorimport MainContentExtractor

    documents = []
    for url in urls:
        response = requests.get(url).text
        response = MainContentExtractor.extract(
            response, output_format=self.text_format, include_links=False
        )

        documents.append(Document(text=response))

    return documents

```
 |  
| --- | --- |  
##  NewsArticleReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.NewsArticleReader "Permanent link")
Bases: 
Simple news article reader.
Reads news articles from the web and parses them using the `newspaper` library.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `text_mode`  |  `bool`  |  Whether to load a text version or HTML version of the content (default=True).  |  `True`  |  
|  `use_nlp`  |  `bool`  |  Whether to use NLP to extract additional summary and keywords (default=True).  |  `True`  |  
|  `newspaper_kwargs`  |  Additional keyword arguments to pass to newspaper.Article. See https://newspaper.readthedocs.io/en/latest/user_guide/quickstart.html#article  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/news/base.py`  
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
```
 | 
```
classNewsArticleReader(BaseReader):
"""
    Simple news article reader.

    Reads news articles from the web and parses them using the `newspaper` library.

    Args:
        text_mode (bool): Whether to load a text version or HTML version of the content (default=True).
        use_nlp (bool): Whether to use NLP to extract additional summary and keywords (default=True).
        newspaper_kwargs: Additional keyword arguments to pass to newspaper.Article. See
            https://newspaper.readthedocs.io/en/latest/user_guide/quickstart.html#article

    """

    def__init__(
        self, text_mode: bool = True, use_nlp: bool = True, **newspaper_kwargs: Any
    ) -> None:
"""Initialize with parameters."""
        if find_spec("newspaper") is None:
            raise ImportError(
                "`newspaper` package not found, please run `pip install newspaper3k`"
            )
        self.load_text = text_mode
        self.use_nlp = use_nlp
        self.newspaper_kwargs = newspaper_kwargs

    defload_data(self, urls: List[str]) -> List[Document]:
"""
        Load data from the list of news article urls.

        Args:
            urls (List[str]): List of URLs to load news articles.

        Returns:
            List[Document]: List of documents.

        """
        if not isinstance(urls, list) and not isinstance(urls, Generator):
            raise ValueError("urls must be a list or generator.")
        documents = []
        for url in urls:
            fromnewspaperimport Article

            try:
                article = Article(url, **self.newspaper_kwargs)
                article.download()
                article.parse()

                if self.use_nlp:
                    article.nlp()

            except Exception as e:
                logger.error(f"Error fetching or processing {url}, exception: {e}")
                continue

            metadata = {
                "title": getattr(article, "title", ""),
                "link": getattr(article, "url", getattr(article, "canonical_link", "")),
                "authors": getattr(article, "authors", []),
                "language": getattr(article, "meta_lang", ""),
                "description": getattr(article, "meta_description", ""),
                "publish_date": getattr(article, "publish_date", ""),
            }

            if self.load_text:
                content = article.text
            else:
                content = article.html

            if self.use_nlp:
                metadata["keywords"] = getattr(article, "keywords", [])
                metadata["summary"] = getattr(article, "summary", "")

            documents.append(Document(text=content, metadata=metadata))

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.NewsArticleReader.load_data "Permanent link")

```
load_data(urls: []) -> []

```

Load data from the list of news article urls.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List of URLs to load news articles.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/news/base.py`  
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
```
 | 
```
defload_data(self, urls: List[str]) -> List[Document]:
"""
    Load data from the list of news article urls.

    Args:
        urls (List[str]): List of URLs to load news articles.

    Returns:
        List[Document]: List of documents.

    """
    if not isinstance(urls, list) and not isinstance(urls, Generator):
        raise ValueError("urls must be a list or generator.")
    documents = []
    for url in urls:
        fromnewspaperimport Article

        try:
            article = Article(url, **self.newspaper_kwargs)
            article.download()
            article.parse()

            if self.use_nlp:
                article.nlp()

        except Exception as e:
            logger.error(f"Error fetching or processing {url}, exception: {e}")
            continue

        metadata = {
            "title": getattr(article, "title", ""),
            "link": getattr(article, "url", getattr(article, "canonical_link", "")),
            "authors": getattr(article, "authors", []),
            "language": getattr(article, "meta_lang", ""),
            "description": getattr(article, "meta_description", ""),
            "publish_date": getattr(article, "publish_date", ""),
        }

        if self.load_text:
            content = article.text
        else:
            content = article.html

        if self.use_nlp:
            metadata["keywords"] = getattr(article, "keywords", [])
            metadata["summary"] = getattr(article, "summary", "")

        documents.append(Document(text=content, metadata=metadata))

    return documents

```
 |  
| --- | --- |  
##  OxylabsWebReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.OxylabsWebReader "Permanent link")
Bases: 
Scrape any website with Oxylabs Web Scraper API and get results in Markdown format.
[See the API documentation](https://developers.oxylabs.io/scraper-apis/web-scraper-api/other-websites)
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `username`  |  Oxylabs API username.  |  _required_  |  
|  `password`  |  Oxylabs API password.  |  _required_  |  
Example
.. code-block:: python from llama_index.readers.web.oxylabs_web.base import OxylabsWebReader

```
reader = OxylabsWebReader(
    username=os.environ["OXYLABS_USERNAME"], password=os.environ["OXYLABS_PASSWORD"]
)

docs = reader.load_data(
    [
        "https://sandbox.oxylabs.io/products/1",
        "https://sandbox.oxylabs.io/products/2"
    ],
    {
        "parse": True,
    }
)

print(docs[0].text)

```
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/oxylabs_web/base.py`  
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
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
```
 | 
```
classOxylabsWebReader(BasePydanticReader):
"""
    Scrape any website with Oxylabs Web Scraper API and get results in Markdown format.

    [See the API documentation](https://developers.oxylabs.io/scraper-apis/web-scraper-api/other-websites)

    Args:
        username: Oxylabs API username.
        password: Oxylabs API password.

    Example:
        .. code-block:: python
            from llama_index.readers.web.oxylabs_web.base import OxylabsWebReader

            reader = OxylabsWebReader(
                username=os.environ["OXYLABS_USERNAME"], password=os.environ["OXYLABS_PASSWORD"]


            docs = reader.load_data(

                    "https://sandbox.oxylabs.io/products/1",
                    "https://sandbox.oxylabs.io/products/2"


                    "parse": True,



            print(docs[0].text)

    """

    timeout_s: int = 100
    oxylabs_scraper_url: str = "https://realtime.oxylabs.io/v1/queries"
    api: "RealtimeAPI"
    async_api: "AsyncAPI"
    default_config: dict[str, Any] = Field(default_factory=get_default_config)

    def__init__(self, username: str, password: str, **kwargs) -> None:
        fromoxylabs.internal.apiimport AsyncAPI, APICredentials, RealtimeAPI

        credentials = APICredentials(username=username, password=password)

        bits, _ = architecture()
        sdk_type = (
            f"oxylabs-llama-index-web-sdk-python/"
            f"{version('llama-index-readers-web')} "
            f"({python_version()}; {bits})"
        )

        api = RealtimeAPI(credentials, sdk_type=sdk_type)
        async_api = AsyncAPI(credentials, sdk_type=sdk_type)

        super().__init__(api=api, async_api=async_api, **kwargs)

    @classmethod
    defclass_name(cls) -> str:
        return "OxylabsWebReader"

    def_get_document_from_response(self, response: dict[str, Any]) -> Document:
        content = response["results"][0]["content"]

        if isinstance(content, (dict, list)):
            text = json_to_markdown(content)
        else:
            striped_html = strip_html(str(content))
            text = markdownify(striped_html)

        return Document(
            metadata={"oxylabs_job": response["job"]},
            text=text,
        )

    async defaload_data(
        self,
        urls: list[str],
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
"""
        Asynchronously load data from urls.

        Args:
            urls: List of URLs to load.
            additional_params: Dictionary of scraper parameters as described
                [here](https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/generic-target#additional)

        """
        if additional_params is None:
            additional_params = {}

        responses = await asyncio.gather(
            *[
                self.async_api.get_response(
                    {**additional_params, "url": url},
                    self.default_config,
                )
                for url in urls
            ]
        )

        return [
            self._get_document_from_response(response)
            for response in responses
            if response
        ]

    defload_data(
        self,
        urls: list[str],
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
"""
        Load data from urls.

        Args:
            urls: List of URLs to load.
            additional_params: Dictionary of scraper parameters as described
                [here](https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/generic-target#additional)

        """
        if additional_params is None:
            additional_params = {}

        responses = [
            self.api.get_response(
                {**additional_params, "url": url},
                self.default_config,
            )
            for url in urls
        ]

        return [
            self._get_document_from_response(response)
            for response in responses
            if response
        ]

```
 |  
| --- | --- |  
###  aload_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.OxylabsWebReader.aload_data "Permanent link")

```
aload_data(
    urls: [],
    additional_params: Optional[[, ]] = None,
) -> []

```

Asynchronously load data from urls.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `list[str]`  |  List of URLs to load.  |  _required_  |  
|  `additional_params`  |  `Optional[Dict[str, Any]]`  |  Dictionary of scraper parameters as described [here](https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/generic-target#additional)  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/oxylabs_web/base.py`  
| 
```
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
```
 | 
```
async defaload_data(
    self,
    urls: list[str],
    additional_params: Optional[Dict[str, Any]] = None,
) -> List[Document]:
"""
    Asynchronously load data from urls.

    Args:
        urls: List of URLs to load.
        additional_params: Dictionary of scraper parameters as described
            [here](https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/generic-target#additional)

    """
    if additional_params is None:
        additional_params = {}

    responses = await asyncio.gather(
        *[
            self.async_api.get_response(
                {**additional_params, "url": url},
                self.default_config,
            )
            for url in urls
        ]
    )

    return [
        self._get_document_from_response(response)
        for response in responses
        if response
    ]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.OxylabsWebReader.load_data "Permanent link")

```
load_data(
    urls: [],
    additional_params: Optional[[, ]] = None,
) -> []

```

Load data from urls.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `list[str]`  |  List of URLs to load.  |  _required_  |  
|  `additional_params`  |  `Optional[Dict[str, Any]]`  |  Dictionary of scraper parameters as described [here](https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/generic-target#additional)  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/oxylabs_web/base.py`  
| 
```
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
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
```
 | 
```
defload_data(
    self,
    urls: list[str],
    additional_params: Optional[Dict[str, Any]] = None,
) -> List[Document]:
"""
    Load data from urls.

    Args:
        urls: List of URLs to load.
        additional_params: Dictionary of scraper parameters as described
            [here](https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/generic-target#additional)

    """
    if additional_params is None:
        additional_params = {}

    responses = [
        self.api.get_response(
            {**additional_params, "url": url},
            self.default_config,
        )
        for url in urls
    ]

    return [
        self._get_document_from_response(response)
        for response in responses
        if response
    ]

```
 |  
| --- | --- |  
##  ReadabilityWebPageReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ReadabilityWebPageReader "Permanent link")
Bases: 
Readability Webpage Loader.
Extracting relevant information from a fully rendered web page. During the processing, it is always assumed that web pages used as data sources contain textual content.
  1. Load the page and wait for it rendered. (playwright)
  2. Inject Readability.js to extract the main content.


Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `proxy`  |  `Optional[str]`  |  Proxy server. Defaults to None.  |  `None`  |  
|  `wait_until`  |  `Optional[Literal['commit', 'domcontentloaded', 'load', 'networkidle']]`  |  Wait until the page is loaded. Defaults to "domcontentloaded".  |  `'domcontentloaded'`  |  
|  `text_splitter`  |   |  Text splitter. Defaults to None.  |  `None`  |  
|  `normalizer`  |  `Optional[Callable[[str], str]]`  |  Text normalizer. Defaults to nfkc_normalize.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/readability_web/base.py`  
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
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
```
 | 
```
classReadabilityWebPageReader(BaseReader):
"""
    Readability Webpage Loader.

    Extracting relevant information from a fully rendered web page.
    During the processing, it is always assumed that web pages used as data sources contain textual content.

    1. Load the page and wait for it rendered. (playwright)
    2. Inject Readability.js to extract the main content.

    Args:
        proxy (Optional[str], optional): Proxy server. Defaults to None.
        wait_until (Optional[Literal["commit", "domcontentloaded", "load", "networkidle"]], optional): Wait until the page is loaded. Defaults to "domcontentloaded".
        text_splitter (TextSplitter, optional): Text splitter. Defaults to None.
        normalizer (Optional[Callable[[str], str]], optional): Text normalizer. Defaults to nfkc_normalize.

    """

    def__init__(
        self,
        proxy: Optional[str] = None,
        wait_until: Optional[
            Literal["commit", "domcontentloaded", "load", "networkidle"]
        ] = "domcontentloaded",
        text_splitter: Optional[TextSplitter] = None,
        normalize: Optional[Callable[[str], str]] = nfkc_normalize,
    ) -> None:
        self._launch_options = {
            "headless": True,
        }
        self._wait_until = wait_until
        if proxy:
            self._launch_options["proxy"] = {
                "server": proxy,
            }
        self._text_splitter = text_splitter
        self._normalize = normalize
        self._readability_js = None

    async defasync_load_data(self, url: str) -> List[Document]:
"""
        Render and load data content from url.

        Args:
            url (str): URL to scrape.

        Returns:
            List[Document]: List of documents.

        """
        fromplaywright.async_apiimport async_playwright

        async with async_playwright() as async_playwright:
            browser = await async_playwright.chromium.launch(**self._launch_options)

            article = await self.scrape_page(
                browser,
                url,
            )
            extra_info = {
                key: article[key]
                for key in [
                    "title",
                    "length",
                    "excerpt",
                    "byline",
                    "dir",
                    "lang",
                    "siteName",
                ]
            }

            if self._normalize is not None:
                article["textContent"] = self._normalize(article["textContent"])
            texts = []
            if self._text_splitter is not None:
                texts = self._text_splitter.split_text(article["textContent"])
            else:
                texts = [article["textContent"]]

            await browser.close()

            return [Document(text=x, extra_info=extra_info) for x in texts]

    defload_data(self, url: str) -> List[Document]:
        return async_to_sync(self.async_load_data(url))

    async defscrape_page(
        self,
        browser: Browser,
        url: str,
    ) -> Dict[str, str]:
"""
        Scrape a single article url.

        Args:
            browser (Any): a Playwright Chromium browser.
            url (str): URL of the article to scrape.

        Returns:
            Ref: https://github.com/mozilla/readability
            title: article title;
            content: HTML string of processed article content;
            textContent: text content of the article, with all the HTML tags removed;
            length: length of an article, in characters;
            excerpt: article description, or short excerpt from the content;
            byline: author metadata;
            dir: content direction;
            siteName: name of the site.
            lang: content language

        """
        if self._readability_js is None:
            with open(path) as f:
                self._readability_js = f.read()

        inject_readability = f"""
            (function(){{
{self._readability_js}
            function executor() {{
                return new Readability({{}}, document).parse();
}}
            return executor();
}}())
        """

        # browser = cast(Browser, browser)
        page = await browser.new_page(ignore_https_errors=True)
        page.set_default_timeout(60000)
        await page.goto(url, wait_until=self._wait_until)

        r = await page.evaluate(inject_readability)

        await page.close()
        print("scraped:", url)

        return r

```
 |  
| --- | --- |  
###  async_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ReadabilityWebPageReader.async_load_data "Permanent link")

```
async_load_data(url: ) -> []

```

Render and load data content from url.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  URL to scrape.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/readability_web/base.py`  
| 
```
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
async defasync_load_data(self, url: str) -> List[Document]:
"""
    Render and load data content from url.

    Args:
        url (str): URL to scrape.

    Returns:
        List[Document]: List of documents.

    """
    fromplaywright.async_apiimport async_playwright

    async with async_playwright() as async_playwright:
        browser = await async_playwright.chromium.launch(**self._launch_options)

        article = await self.scrape_page(
            browser,
            url,
        )
        extra_info = {
            key: article[key]
            for key in [
                "title",
                "length",
                "excerpt",
                "byline",
                "dir",
                "lang",
                "siteName",
            ]
        }

        if self._normalize is not None:
            article["textContent"] = self._normalize(article["textContent"])
        texts = []
        if self._text_splitter is not None:
            texts = self._text_splitter.split_text(article["textContent"])
        else:
            texts = [article["textContent"]]

        await browser.close()

        return [Document(text=x, extra_info=extra_info) for x in texts]

```
 |  
| --- | --- |  
###  scrape_page [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ReadabilityWebPageReader.scrape_page "Permanent link")

```
scrape_page(browser: Browser, url: ) -> [, ]

```

Scrape a single article url.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `browser`  |  a Playwright Chromium browser.  |  _required_  |  
|  `url`  |  URL of the article to scrape.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Ref`  |  `Dict[str, str]`  |  https://github.com/mozilla/readability  |  
| `title`  |  `Dict[str, str]`  |  article title;  |  
| `content`  |  `Dict[str, str]`  |  HTML string of processed article content;  |  
| `textContent`  |  `Dict[str, str]`  |  text content of the article, with all the HTML tags removed;  |  
| `length`  |  `Dict[str, str]`  |  length of an article, in characters;  |  
| `excerpt`  |  `Dict[str, str]`  |  article description, or short excerpt from the content;  |  
| `byline`  |  `Dict[str, str]`  |  author metadata;  |  
| `dir`  |  `Dict[str, str]`  |  content direction;  |  
| `siteName`  |  `Dict[str, str]`  |  name of the site.  |  
| `lang`  |  `Dict[str, str]`  |  content language  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/readability_web/base.py`  
| 
```
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
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
```
 | 
```
async defscrape_page(
    self,
    browser: Browser,
    url: str,
) -> Dict[str, str]:
"""
    Scrape a single article url.

    Args:
        browser (Any): a Playwright Chromium browser.
        url (str): URL of the article to scrape.

    Returns:
        Ref: https://github.com/mozilla/readability
        title: article title;
        content: HTML string of processed article content;
        textContent: text content of the article, with all the HTML tags removed;
        length: length of an article, in characters;
        excerpt: article description, or short excerpt from the content;
        byline: author metadata;
        dir: content direction;
        siteName: name of the site.
        lang: content language

    """
    if self._readability_js is None:
        with open(path) as f:
            self._readability_js = f.read()

    inject_readability = f"""
        (function(){{
{self._readability_js}
        function executor() {{
            return new Readability({{}}, document).parse();
}}
        return executor();
}}())
    """

    # browser = cast(Browser, browser)
    page = await browser.new_page(ignore_https_errors=True)
    page.set_default_timeout(60000)
    await page.goto(url, wait_until=self._wait_until)

    r = await page.evaluate(inject_readability)

    await page.close()
    print("scraped:", url)

    return r

```
 |  
| --- | --- |  
##  RssReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.RssReader "Permanent link")
Bases: 
RSS reader.
Reads content from an RSS feed.
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/rss/base.py`  
| 
```
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
```
 | 
```
classRssReader(BasePydanticReader):
"""
    RSS reader.

    Reads content from an RSS feed.

    """

    is_remote: bool = True
    html_to_text: bool = False
    user_agent: Union[str, None] = None

    def__init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # https://pythonhosted.org/feedparser/http-useragent.html
        self.user_agent = kwargs.get("user_agent")

    @classmethod
    defclass_name(cls) -> str:
        return "RssReader"

    defload_data(self, urls: List[str]) -> List[Document]:
"""
        Load data from RSS feeds.

        Args:
            urls (List[str]): List of RSS URLs to load.

        Returns:
            List[Document]: List of documents.

        """
        importfeedparser

        if self.user_agent:
            feedparser.USER_AGENT = self.user_agent

        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")

        documents = []

        for url in urls:
            parsed = feedparser.parse(url)
            for entry in parsed.entries:
                doc_id = getattr(entry, "id", None) or getattr(entry, "link", None)
                data = entry.get("content", [{}])[0].get(
                    "value", entry.get("description", entry.get("summary", ""))
                )

                if self.html_to_text:
                    importhtml2text

                    data = html2text.html2text(data)

                extra_info = {
                    "title": getattr(entry, "title", None),
                    "link": getattr(entry, "link", None),
                    "date": getattr(entry, "published", None),
                }

                if doc_id:
                    documents.append(
                        Document(text=data, id_=doc_id, extra_info=extra_info)
                    )
                else:
                    documents.append(Document(text=data, extra_info=extra_info))

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.RssReader.load_data "Permanent link")

```
load_data(urls: []) -> []

```

Load data from RSS feeds.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List of RSS URLs to load.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/rss/base.py`  
| 
```
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
```
 | 
```
defload_data(self, urls: List[str]) -> List[Document]:
"""
    Load data from RSS feeds.

    Args:
        urls (List[str]): List of RSS URLs to load.

    Returns:
        List[Document]: List of documents.

    """
    importfeedparser

    if self.user_agent:
        feedparser.USER_AGENT = self.user_agent

    if not isinstance(urls, list):
        raise ValueError("urls must be a list of strings.")

    documents = []

    for url in urls:
        parsed = feedparser.parse(url)
        for entry in parsed.entries:
            doc_id = getattr(entry, "id", None) or getattr(entry, "link", None)
            data = entry.get("content", [{}])[0].get(
                "value", entry.get("description", entry.get("summary", ""))
            )

            if self.html_to_text:
                importhtml2text

                data = html2text.html2text(data)

            extra_info = {
                "title": getattr(entry, "title", None),
                "link": getattr(entry, "link", None),
                "date": getattr(entry, "published", None),
            }

            if doc_id:
                documents.append(
                    Document(text=data, id_=doc_id, extra_info=extra_info)
                )
            else:
                documents.append(Document(text=data, extra_info=extra_info))

    return documents

```
 |  
| --- | --- |  
##  RssNewsReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.RssNewsReader "Permanent link")
Bases: 
RSS news reader.
Reads news content from RSS feeds and parses with NewsArticleReader.
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/rss_news/base.py`  
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
```
 | 
```
classRssNewsReader(BaseReader):
"""
    RSS news reader.

    Reads news content from RSS feeds and parses with NewsArticleReader.

    """

    def__init__(self, **reader_kwargs: Any) -> None:
"""
        Initialize with parameters.

        Args:
            html_to_text (bool): Whether to convert HTML to text.
                Requires `html2text` package.

        """
        try:
            importfeedparser  # noqa: F401
        except ImportError:
            raise ImportError(
                "`feedparser` package not found, please run `pip install feedparser`"
            )

        try:
            importlistparser  # noqa: F401
        except ImportError:
            raise ImportError(
                "`listparser` package not found, please run `pip install listparser`"
            )

        self.reader_kwargs = reader_kwargs

    defload_data(self, urls: List[str] = None, opml: str = None) -> List[Document]:
"""
        Load data from either RSS feeds or OPML.

        Args:
            urls (List[str]): List of RSS URLs to load.
            opml (str): URL to OPML file or string or byte OPML content.

        Returns:
            List[Document]: List of documents.

        """
        if (urls is None) == (
            opml is None
        ):  # This is True if both are None or neither is None
            raise ValueError(
                "Provide either the urls or the opml argument, but not both."
            )

        importfeedparser

        if urls and not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")

        documents = []

        if not urls and opml:
            try:
                importlistparser
            except ImportError as e:
                raise ImportError(
                    "Package listparser must be installed if the opml arg is used. "
                    "Please install with 'pip install listparser' or use the "
                    "urls arg instead."
                ) frome
            rss = listparser.parse(opml)
            urls = [feed.url for feed in rss.feeds]

        for url in urls:
            try:
                feed = feedparser.parse(url)
                for i, entry in enumerate(feed.entries):
                    article = NewsArticleReader(**self.reader_kwargs).load_data(
                        urls=[entry.link],
                    )[0]
                    article.metadata["feed"] = url

                    documents.append(
                        Document(text=article.text, metadata=article.metadata)
                    )

            except Exception as e:
                logger.error(f"Error fetching or processing {url}, exception: {e}")
                continue

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.RssNewsReader.load_data "Permanent link")

```
load_data(
    urls: [] = None, opml:  = None
) -> []

```

Load data from either RSS feeds or OPML.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List of RSS URLs to load.  |  `None`  |  
|  `opml`  |  URL to OPML file or string or byte OPML content.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/rss_news/base.py`  
| 
```
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
```
 | 
```
defload_data(self, urls: List[str] = None, opml: str = None) -> List[Document]:
"""
    Load data from either RSS feeds or OPML.

    Args:
        urls (List[str]): List of RSS URLs to load.
        opml (str): URL to OPML file or string or byte OPML content.

    Returns:
        List[Document]: List of documents.

    """
    if (urls is None) == (
        opml is None
    ):  # This is True if both are None or neither is None
        raise ValueError(
            "Provide either the urls or the opml argument, but not both."
        )

    importfeedparser

    if urls and not isinstance(urls, list):
        raise ValueError("urls must be a list of strings.")

    documents = []

    if not urls and opml:
        try:
            importlistparser
        except ImportError as e:
            raise ImportError(
                "Package listparser must be installed if the opml arg is used. "
                "Please install with 'pip install listparser' or use the "
                "urls arg instead."
            ) frome
        rss = listparser.parse(opml)
        urls = [feed.url for feed in rss.feeds]

    for url in urls:
        try:
            feed = feedparser.parse(url)
            for i, entry in enumerate(feed.entries):
                article = NewsArticleReader(**self.reader_kwargs).load_data(
                    urls=[entry.link],
                )[0]
                article.metadata["feed"] = url

                documents.append(
                    Document(text=article.text, metadata=article.metadata)
                )

        except Exception as e:
            logger.error(f"Error fetching or processing {url}, exception: {e}")
            continue

    return documents

```
 |  
| --- | --- |  
##  ScrapflyReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ScrapflyReader "Permanent link")
Bases: 
Turn a url to llm accessible markdown with `Scrapfly.io`.
Args: api_key: The Scrapfly API key. scrape_config: The Scrapfly ScrapeConfig object. ignore_scrape_failures: Whether to continue on failures. urls: List of urls to scrape. scrape_format: Scrape result format (markdown or text) For further details, visit: https://scrapfly.io/docs/sdk/python
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/scrapfly_web/base.py`  
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
```
 | 
```
classScrapflyReader(BasePydanticReader):
"""
    Turn a url to llm accessible markdown with `Scrapfly.io`.

    Args:
    api_key: The Scrapfly API key.
    scrape_config: The Scrapfly ScrapeConfig object.
    ignore_scrape_failures: Whether to continue on failures.
    urls: List of urls to scrape.
    scrape_format: Scrape result format (markdown or text)
    For further details, visit: https://scrapfly.io/docs/sdk/python

    """

    api_key: str
    ignore_scrape_failures: bool = True
    scrapfly: "ScrapflyClient"

    def__init__(self, api_key: str, ignore_scrape_failures: bool = True) -> None:
"""Initialize client."""
        try:
            fromscrapflyimport ScrapflyClient
        except ImportError:
            raise ImportError(
                "`scrapfly` package not found, please run `pip install scrapfly-sdk`"
            )
        scrapfly = ScrapflyClient(key=api_key)
        super().__init__(
            api_key=api_key,
            ignore_scrape_failures=ignore_scrape_failures,
            scrapfly=scrapfly,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "Scrapfly_reader"

    defload_data(
        self,
        urls: List[str],
        scrape_format: Literal["markdown", "text"] = "markdown",
        scrape_config: Optional[dict] = None,
    ) -> List[Document]:
"""
        Load data from the urls.

        Args:
            urls: List[str]): List of URLs to scrape.
            scrape_config: Optional[dict]: Dictionary of ScrapFly scrape config object.

        Returns:
            List[Document]: List of documents.

        Raises:
            ValueError: If URLs aren't provided.

        """
        fromscrapflyimport ScrapeApiResponse, ScrapeConfig

        if urls is None:
            raise ValueError("URLs must be provided.")
        scrape_config = scrape_config if scrape_config is not None else {}

        documents = []
        for url in urls:
            try:
                response: ScrapeApiResponse = self.scrapfly.scrape(
                    ScrapeConfig(url, format=scrape_format, **scrape_config)
                )
                documents.append(
                    Document(
                        text=response.scrape_result["content"], extra_info={"url": url}
                    )
                )
            except Exception as e:
                if self.ignore_scrape_failures:
                    logger.error(f"Error fetching data from {url}, exception: {e}")
                else:
                    raise e  # noqa: TRY201

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ScrapflyReader.load_data "Permanent link")

```
load_data(
    urls: [],
    scrape_format: Literal["markdown", "text"] = "markdown",
    scrape_config: Optional[] = None,
) -> []

```

Load data from the urls.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List[str]): List of URLs to scrape.  |  _required_  |  
|  `scrape_config`  |  `Optional[dict]`  |  Optional[dict]: Dictionary of ScrapFly scrape config object.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If URLs aren't provided.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/scrapfly_web/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    urls: List[str],
    scrape_format: Literal["markdown", "text"] = "markdown",
    scrape_config: Optional[dict] = None,
) -> List[Document]:
"""
    Load data from the urls.

    Args:
        urls: List[str]): List of URLs to scrape.
        scrape_config: Optional[dict]: Dictionary of ScrapFly scrape config object.

    Returns:
        List[Document]: List of documents.

    Raises:
        ValueError: If URLs aren't provided.

    """
    fromscrapflyimport ScrapeApiResponse, ScrapeConfig

    if urls is None:
        raise ValueError("URLs must be provided.")
    scrape_config = scrape_config if scrape_config is not None else {}

    documents = []
    for url in urls:
        try:
            response: ScrapeApiResponse = self.scrapfly.scrape(
                ScrapeConfig(url, format=scrape_format, **scrape_config)
            )
            documents.append(
                Document(
                    text=response.scrape_result["content"], extra_info={"url": url}
                )
            )
        except Exception as e:
            if self.ignore_scrape_failures:
                logger.error(f"Error fetching data from {url}, exception: {e}")
            else:
                raise e  # noqa: TRY201

    return documents

```
 |  
| --- | --- |  
##  ScrapyWebReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ScrapyWebReader "Permanent link")
Bases: 
Scrapy web page reader.
Reads pages from the web.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `project_path`  |  `Optional[str]`  |  The path to the Scrapy project for loading the project settings (with middlewares and pipelines). The project path should contain the `scrapy.cfg` file. Settings will be set to empty if path not specified or not found. Defaults to "".  |  
|  `metadata_keys`  |  `Optional[List[str]]`  |  List of keys to use as document metadata from the scraped item. Defaults to [].  |  
|  `keep_keys`  |  `bool`  |  Whether to keep metadata keys in items. Defaults to False.  |  `False`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/scrapy_web/base.py`  
| 
```
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
```
 | 
```
classScrapyWebReader(BasePydanticReader):
"""
    Scrapy web page reader.

    Reads pages from the web.

    Args:
        project_path (Optional[str]): The path to the Scrapy project for
            loading the project settings (with middlewares and pipelines).
            The project path should contain the `scrapy.cfg` file.
            Settings will be set to empty if path not specified or not found.
            Defaults to "".

        metadata_keys (Optional[List[str]]): List of keys to use
            as document metadata from the scraped item. Defaults to [].

        keep_keys (bool): Whether to keep metadata keys in items.
            Defaults to False.

    """

    project_path: Optional[str] = ""
    metadata_keys: Optional[List[str]] = []
    keep_keys: bool = False

    def__init__(
        self,
        project_path: Optional[str] = "",
        metadata_keys: Optional[List[str]] = [],
        keep_keys: bool = False,
    ):
        super().__init__(
            project_path=project_path,
            metadata_keys=metadata_keys,
            keep_keys=keep_keys,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "ScrapyWebReader"

    defload_data(self, spider: Union[Spider, str]) -> List[Document]:
"""
        Load data from the input spider.

        Args:
            spider (Union[Spider, str]): The Scrapy spider class or
                the spider name from the project to use for scraping.

        Returns:
            List[Document]: List of documents extracted from the web pages.

        """
        if not self._is_spider_correct_type(spider):
            raise ValueError(
                "Invalid spider type. Provide a Spider class or spider name with project path."
            )

        documents_queue = Queue()

        config = {
            "keep_keys": self.keep_keys,
            "metadata_keys": self.metadata_keys,
            "settings": load_scrapy_settings(self.project_path),
        }

        # Running each spider in a separate process as Scrapy uses
        # twisted reactor which can only be run once in a process
        process = Process(
            target=run_spider_process, args=(spider, documents_queue, config)
        )

        process.start()
        process.join()

        if documents_queue.empty():
            return []

        return documents_queue.get()

    def_is_spider_correct_type(self, spider: Union[Spider, str]) -> bool:
        return not (isinstance(spider, str) and not self.project_path)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ScrapyWebReader.load_data "Permanent link")

```
load_data(spider: Union[Spider, ]) -> []

```

Load data from the input spider.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `spider`  |  `Union[Spider, str]`  |  The Scrapy spider class or the spider name from the project to use for scraping.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents extracted from the web pages.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/scrapy_web/base.py`  
| 
```
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
```
 | 
```
defload_data(self, spider: Union[Spider, str]) -> List[Document]:
"""
    Load data from the input spider.

    Args:
        spider (Union[Spider, str]): The Scrapy spider class or
            the spider name from the project to use for scraping.

    Returns:
        List[Document]: List of documents extracted from the web pages.

    """
    if not self._is_spider_correct_type(spider):
        raise ValueError(
            "Invalid spider type. Provide a Spider class or spider name with project path."
        )

    documents_queue = Queue()

    config = {
        "keep_keys": self.keep_keys,
        "metadata_keys": self.metadata_keys,
        "settings": load_scrapy_settings(self.project_path),
    }

    # Running each spider in a separate process as Scrapy uses
    # twisted reactor which can only be run once in a process
    process = Process(
        target=run_spider_process, args=(spider, documents_queue, config)
    )

    process.start()
    process.join()

    if documents_queue.empty():
        return []

    return documents_queue.get()

```
 |  
| --- | --- |  
##  SimpleWebPageReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.SimpleWebPageReader "Permanent link")
Bases: 
Simple web page reader.
Reads pages from the web.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `html_to_text`  |  `bool`  |  Whether to convert HTML to text. Requires `html2text` package.  |  `False`  |  
|  `metadata_fn`  |  `Optional[Callable[[str], Dict]]`  |  A function that takes in a URL and returns a dictionary of metadata. Default is None.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/simple_web/base.py`  
| 
```
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
```
 | 
```
classSimpleWebPageReader(BasePydanticReader):
"""
    Simple web page reader.

    Reads pages from the web.

    Args:
        html_to_text (bool): Whether to convert HTML to text.
            Requires `html2text` package.
        metadata_fn (Optional[Callable[[str], Dict]]): A function that takes in
            a URL and returns a dictionary of metadata.
            Default is None.

    """

    is_remote: bool = True
    html_to_text: bool

    _metadata_fn: Optional[Callable[[str], Dict]] = PrivateAttr()
    _timeout: Optional[int] = PrivateAttr()
    _fail_on_error: bool = PrivateAttr()

    def__init__(
        self,
        html_to_text: bool = False,
        metadata_fn: Optional[Callable[[str], Dict]] = None,
        timeout: Optional[int] = 60,
        fail_on_error: bool = False,
    ) -> None:
"""Initialize with parameters."""
        try:
            importhtml2text  # noqa
        except ImportError:
            raise ImportError(
                "`html2text` package not found, please run `pip install html2text`"
            )
        super().__init__(html_to_text=html_to_text)
        self._metadata_fn = metadata_fn
        self._timeout = timeout
        self._fail_on_error = fail_on_error

    @classmethod
    defclass_name(cls) -> str:
        return "SimpleWebPageReader"

    defload_data(self, urls: List[str]) -> List[Document]:
"""
        Load data from the input directory.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[Document]: List of documents.

        """
        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")
        documents = []
        for url in urls:
            try:
                response = requests.get(url, headers=None, timeout=self._timeout)
            except Exception:
                if self._fail_on_error:
                    raise
                continue

            response_text = response.text

            if response.status_code != 200 and self._fail_on_error:
                raise ValueError(
                    f"Error fetching page from {url}. server returned status:"
                    f" {response.status_code} and response {response_text}"
                )

            if self.html_to_text:
                importhtml2text

                response_text = html2text.html2text(response_text)

            metadata: Dict = {"url": url}
            if self._metadata_fn is not None:
                metadata = self._metadata_fn(url)
                if "url" not in metadata:
                    metadata["url"] = url

            documents.append(
                Document(text=response_text, id_=str(uuid.uuid4()), metadata=metadata)
            )

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.SimpleWebPageReader.load_data "Permanent link")

```
load_data(urls: []) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List of URLs to scrape.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/simple_web/base.py`  
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
```
 | 
```
defload_data(self, urls: List[str]) -> List[Document]:
"""
    Load data from the input directory.

    Args:
        urls (List[str]): List of URLs to scrape.

    Returns:
        List[Document]: List of documents.

    """
    if not isinstance(urls, list):
        raise ValueError("urls must be a list of strings.")
    documents = []
    for url in urls:
        try:
            response = requests.get(url, headers=None, timeout=self._timeout)
        except Exception:
            if self._fail_on_error:
                raise
            continue

        response_text = response.text

        if response.status_code != 200 and self._fail_on_error:
            raise ValueError(
                f"Error fetching page from {url}. server returned status:"
                f" {response.status_code} and response {response_text}"
            )

        if self.html_to_text:
            importhtml2text

            response_text = html2text.html2text(response_text)

        metadata: Dict = {"url": url}
        if self._metadata_fn is not None:
            metadata = self._metadata_fn(url)
            if "url" not in metadata:
                metadata["url"] = url

        documents.append(
            Document(text=response_text, id_=str(uuid.uuid4()), metadata=metadata)
        )

    return documents

```
 |  
| --- | --- |  
##  SitemapReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.SitemapReader "Permanent link")
Bases: 
Asynchronous sitemap reader for web.
Reads pages from the web based on their sitemap.xml.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sitemap_url`  |  `string`  |  Path to the sitemap.xml. e.g. https://gpt-index.readthedocs.io/sitemap.xml  |  _required_  |  
|  `html_to_text`  |  `bool`  |  Whether to convert HTML to text. Requires `html2text` package.  |  `False`  |  
|  `limit`  |  Maximum number of concurrent requests.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/sitemap/base.py`  
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
```
 | 
```
classSitemapReader(BaseReader):
"""
    Asynchronous sitemap reader for web.

    Reads pages from the web based on their sitemap.xml.

    Args:
        sitemap_url (string): Path to the sitemap.xml. e.g. https://gpt-index.readthedocs.io/sitemap.xml
        html_to_text (bool): Whether to convert HTML to text.
            Requires `html2text` package.
        limit (int): Maximum number of concurrent requests.

    """

    xml_schema_sitemap = "http://www.sitemaps.org/schemas/sitemap/0.9"

    def__init__(self, html_to_text: bool = False, limit: int = 10) -> None:
"""Initialize with parameters."""
        self._async_loader = AsyncWebPageReader(html_to_text=html_to_text, limit=limit)
        self._html_to_text = html_to_text
        self._limit = limit

    def_load_sitemap(self, sitemap_url: str) -> str:
        sitemap_url_request = httpx.get(sitemap_url)

        return sitemap_url_request.content

    def_parse_sitemap(self, raw_sitemap: str, filter_locs: str = None) -> list:
        sitemap = fromstring(raw_sitemap)
        sitemap_urls = []

        for url in sitemap.findall(f"{{{self.xml_schema_sitemap}}}url"):
            location = url.find(f"{{{self.xml_schema_sitemap}}}loc").text

            if filter_locs is None or filter_locs in location:
                sitemap_urls.append(location)

        return sitemap_urls

    defload_data(self, sitemap_url: str, filter: str = None) -> List[Document]:
        sitemap = self._load_sitemap(sitemap_url=sitemap_url)
        sitemap_urls = self._parse_sitemap(sitemap, filter)

        return self._async_loader.load_data(urls=sitemap_urls)

```
 |  
| --- | --- |  
##  SpiderWebReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.SpiderWebReader "Permanent link")
Bases: 
Scrapes a URL for data and returns llm-ready data with `Spider.cloud`.
Must have the Python package `spider-client` installed and a Spider API key. See https://spider.cloud for more.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  The Spider API key, get one at https://spider.cloud  |  `None`  |  
|  `mode`  |  `Mode`  |  "Scrape" the url (default) or "crawl" the url following all subpages.  |  `'scrape'`  |  
|  `params`  |  `dict`  |  Additional parameters to pass to the Spider API.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/spider_web/base.py`  
| 
```
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
```
 | 
```
classSpiderWebReader(BasePydanticReader):
"""
    Scrapes a URL for data and returns llm-ready data with `Spider.cloud`.

    Must have the Python package `spider-client` installed and a Spider API key.
    See https://spider.cloud for more.

    Args:
        api_key (str): The Spider API key, get one at https://spider.cloud
        mode (Mode): "Scrape" the url (default) or "crawl" the url following all subpages.
        params (dict): Additional parameters to pass to the Spider API.

    """

    classConfig:
        use_enum_values = True
        extra = "allow"

    def__init__(
        self,
        *,
        api_key: Optional[str] = None,
        mode: Literal["scrape", "crawl"] = "scrape",
        params: Optional[dict] = None,
    ) -> None:
        super().__init__(api_key=api_key, mode=mode, params=params)

        if params is None:
            params = {"return_format": "markdown", "metadata": True}
        try:
            fromspiderimport Spider
        except ImportError:
            raise ImportError(
                "`spider-client` package not found, please run `pip install spider-client`"
            )
        self.spider = Spider(api_key=api_key)
        self.mode = mode
        self.params = params

    defload_data(self, url: str) -> List[Document]:
        if self.mode != "scrape" and self.mode != "crawl":
            raise ValueError(
                "Unknown mode in `mode` parameter, `scrape` or `crawl` is the allowed modes"
            )
        action = (
            self.spider.scrape_url if self.mode == "scrape" else self.spider.crawl_url
        )
        spider_docs = action(url=url, params=self.params)

        if not spider_docs:
            return [Document(page_content="", metadata={})]

        documents = []
        if isinstance(spider_docs, list):
            for doc in spider_docs:
                text = doc.get("content", "")
                if text is not None:
                    documents.append(
                        Document(
                            text=text,
                            metadata=doc.get("metadata", {}),
                        )
                    )

        return documents

```
 |  
| --- | --- |  
##  TrafilaturaWebReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.TrafilaturaWebReader "Permanent link")
Bases: 
Trafilatura web page reader.
Reads pages from the web. Requires the `trafilatura` package.
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/trafilatura_web/base.py`  
| 
```
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
```
 | 
```
classTrafilaturaWebReader(BasePydanticReader):
"""
    Trafilatura web page reader.

    Reads pages from the web.
    Requires the `trafilatura` package.

    """

    is_remote: bool = True

    @classmethod
    defclass_name(cls) -> str:
"""Get the name identifier of the class."""
        return "TrafilaturaWebReader"

    defload_data(
        self,
        urls: List[str],
        include_comments=True,
        output_format="txt",
        include_tables=True,
        include_images=False,
        include_formatting=False,
        include_links=False,
        show_progress=False,
        no_ssl=False,
        **kwargs,
    ) -> List[Document]:
"""
        Load data from the urls.

        Args:
            urls (List[str]): List of URLs to scrape.
            include_comments (bool, optional): Include comments in the output. Defaults to True.
            output_format (str, optional): Output format. Defaults to 'txt'.
            include_tables (bool, optional): Include tables in the output. Defaults to True.
            include_images (bool, optional): Include images in the output. Defaults to False.
            include_formatting (bool, optional): Include formatting in the output. Defaults to False.
            include_links (bool, optional): Include links in the output. Defaults to False.
            show_progress (bool, optional): Show progress bar. Defaults to False
            no_ssl (bool, optional): Bypass SSL verification. Defaults to False.
            kwargs: Additional keyword arguments for the `trafilatura.extract` function.

        Returns:
            List[Document]: List of documents.

        """
        importtrafilatura

        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")
        documents = []

        if show_progress:
            fromtqdmimport tqdm

            iterator = tqdm(urls, desc="Downloading pages")
        else:
            iterator = urls
        for url in iterator:
            downloaded = trafilatura.fetch_url(url, no_ssl=no_ssl)
            response = trafilatura.extract(
                downloaded,
                include_comments=include_comments,
                output_format=output_format,
                include_tables=include_tables,
                include_images=include_images,
                include_formatting=include_formatting,
                include_links=include_links,
                **kwargs,
            )
            documents.append(
                Document(text=response, id_=str(uuid.uuid4()), metadata={"url": url})
            )

        return documents

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.TrafilaturaWebReader.class_name "Permanent link")

```
class_name() -> 

```

Get the name identifier of the class.
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/trafilatura_web/base.py`  
| 
```
19
20
21
22
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get the name identifier of the class."""
    return "TrafilaturaWebReader"

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.TrafilaturaWebReader.load_data "Permanent link")

```
load_data(
    urls: [],
    include_comments=True,
    output_format="txt",
    include_tables=True,
    include_images=False,
    include_formatting=False,
    include_links=False,
    show_progress=False,
    no_ssl=False,
    **kwargs
) -> []

```

Load data from the urls.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List of URLs to scrape.  |  _required_  |  
|  `include_comments`  |  `bool`  |  Include comments in the output. Defaults to True.  |  `True`  |  
|  `output_format`  |  Output format. Defaults to 'txt'.  |  `'txt'`  |  
|  `include_tables`  |  `bool`  |  Include tables in the output. Defaults to True.  |  `True`  |  
|  `include_images`  |  `bool`  |  Include images in the output. Defaults to False.  |  `False`  |  
|  `include_formatting`  |  `bool`  |  Include formatting in the output. Defaults to False.  |  `False`  |  
|  `include_links`  |  `bool`  |  Include links in the output. Defaults to False.  |  `False`  |  
|  `show_progress`  |  `bool`  |  Show progress bar. Defaults to False  |  `False`  |  
|  `no_ssl`  |  `bool`  |  Bypass SSL verification. Defaults to False.  |  `False`  |  
|  `kwargs`  |  Additional keyword arguments for the `trafilatura.extract` function.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/trafilatura_web/base.py`  
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
```
 | 
```
defload_data(
    self,
    urls: List[str],
    include_comments=True,
    output_format="txt",
    include_tables=True,
    include_images=False,
    include_formatting=False,
    include_links=False,
    show_progress=False,
    no_ssl=False,
    **kwargs,
) -> List[Document]:
"""
    Load data from the urls.

    Args:
        urls (List[str]): List of URLs to scrape.
        include_comments (bool, optional): Include comments in the output. Defaults to True.
        output_format (str, optional): Output format. Defaults to 'txt'.
        include_tables (bool, optional): Include tables in the output. Defaults to True.
        include_images (bool, optional): Include images in the output. Defaults to False.
        include_formatting (bool, optional): Include formatting in the output. Defaults to False.
        include_links (bool, optional): Include links in the output. Defaults to False.
        show_progress (bool, optional): Show progress bar. Defaults to False
        no_ssl (bool, optional): Bypass SSL verification. Defaults to False.
        kwargs: Additional keyword arguments for the `trafilatura.extract` function.

    Returns:
        List[Document]: List of documents.

    """
    importtrafilatura

    if not isinstance(urls, list):
        raise ValueError("urls must be a list of strings.")
    documents = []

    if show_progress:
        fromtqdmimport tqdm

        iterator = tqdm(urls, desc="Downloading pages")
    else:
        iterator = urls
    for url in iterator:
        downloaded = trafilatura.fetch_url(url, no_ssl=no_ssl)
        response = trafilatura.extract(
            downloaded,
            include_comments=include_comments,
            output_format=output_format,
            include_tables=include_tables,
            include_images=include_images,
            include_formatting=include_formatting,
            include_links=include_links,
            **kwargs,
        )
        documents.append(
            Document(text=response, id_=str(uuid.uuid4()), metadata={"url": url})
        )

    return documents

```
 |  
| --- | --- |  
##  UnstructuredURLLoader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.UnstructuredURLLoader "Permanent link")
Bases: 
Loader that uses unstructured to load HTML files.
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/unstructured_web/base.py`  
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
```
 | 
```
classUnstructuredURLLoader(BaseReader):
"""Loader that uses unstructured to load HTML files."""

    def__init__(
        self, urls: List[str], continue_on_failure: bool = True, headers: dict = {}
    ):
"""Initialize with file path."""
        try:
            importunstructured  # noqa:F401
            fromunstructured.__version__import __version__ as __unstructured_version__

            self.__version = __unstructured_version__
        except ImportError:
            raise ValueError(
                "unstructured package not found, please install it with "
                "`pip install unstructured`"
            )

        if not self.__is_headers_available() and len(headers.keys()) != 0:
            logger.warning(
                "You are using old version of unstructured. "
                "The headers parameter is ignored"
            )

        self.urls = urls
        self.continue_on_failure = continue_on_failure
        self.headers = headers

    def__is_headers_available(self) -> bool:
        _unstructured_version = self.__version.split("-")[0]
        unstructured_version = tuple([int(x) for x in _unstructured_version.split(".")])

        return unstructured_version >= (0, 5, 7)

    defload_data(self) -> List[Document]:
"""Load file."""
        fromunstructured.partition.htmlimport partition_html

        docs: List[Document] = []
        for url in self.urls:
            try:
                if self.__is_headers_available():
                    elements = partition_html(url=url, headers=self.headers)
                else:
                    elements = partition_html(url=url)
                text = "\n\n".join([str(el) for el in elements])
                metadata = {"source": url}
                docs.append(Document(text=text, extra_info=metadata))
            except Exception as e:
                if self.continue_on_failure:
                    logger.error(f"Error fetching or processing {url}, exception: {e}")
                else:
                    raise e  # noqa: TRY201
        return docs

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.UnstructuredURLLoader.load_data "Permanent link")

```
load_data() -> []

```

Load file.
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/unstructured_web/base.py`  
| 
```
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
```
 | 
```
defload_data(self) -> List[Document]:
"""Load file."""
    fromunstructured.partition.htmlimport partition_html

    docs: List[Document] = []
    for url in self.urls:
        try:
            if self.__is_headers_available():
                elements = partition_html(url=url, headers=self.headers)
            else:
                elements = partition_html(url=url)
            text = "\n\n".join([str(el) for el in elements])
            metadata = {"source": url}
            docs.append(Document(text=text, extra_info=metadata))
        except Exception as e:
            if self.continue_on_failure:
                logger.error(f"Error fetching or processing {url}, exception: {e}")
            else:
                raise e  # noqa: TRY201
    return docs

```
 |  
| --- | --- |  
##  WholeSiteReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.WholeSiteReader "Permanent link")
Bases: 
BFS Web Scraper for websites.
This class provides functionality to scrape entire websites using a breadth-first search algorithm. It navigates web pages from a given base URL, following links that match a specified prefix.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `prefix`  |  URL prefix to focus the scraping.  |  
| `max_depth`  |  Maximum depth for BFS algorithm.  |  
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prefix`  |  URL prefix for scraping.  |  _required_  |  
|  `max_depth`  |  Maximum depth for BFS. Defaults to 10.  |  
|  `uri_as_id`  |  `bool`  |  Whether to use the URI as the document ID. Defaults to False.  |  `False`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/whole_site/base.py`  
| 
```
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
143
144
145
146
147
148
149
150
151
152
153
```
 | 
```
classWholeSiteReader(BaseReader):
"""
    BFS Web Scraper for websites.

    This class provides functionality to scrape entire websites using a breadth-first search algorithm.
    It navigates web pages from a given base URL, following links that match a specified prefix.

    Attributes:
        prefix (str): URL prefix to focus the scraping.
        max_depth (int): Maximum depth for BFS algorithm.

    Args:
        prefix (str): URL prefix for scraping.
        max_depth (int, optional): Maximum depth for BFS. Defaults to 10.
        uri_as_id (bool, optional): Whether to use the URI as the document ID. Defaults to False.

    """

    def__init__(
        self,
        prefix: str,
        max_depth: int = 10,
        uri_as_id: bool = False,
        driver: Optional[webdriver.Chrome] = None,
    ) -> None:
"""
        Initialize the WholeSiteReader with the provided prefix and maximum depth.
        """
        self.prefix = prefix
        self.max_depth = max_depth
        self.uri_as_id = uri_as_id
        self.driver = driver if driver else self.setup_driver()

    defsetup_driver(self):
"""
        Sets up the Selenium WebDriver for Chrome.

        Returns:
            WebDriver: An instance of Chrome WebDriver.

        """
        try:
            importchromedriver_autoinstaller
        except ImportError:
            raise ImportError("Please install chromedriver_autoinstaller")

        opt = webdriver.ChromeOptions()
        opt.add_argument("--start-maximized")
        chromedriver_autoinstaller.install()
        return webdriver.Chrome(options=opt)

    defclean_url(self, url):
        return url.split("#")[0]

    defrestart_driver(self):
        self.driver.quit()
        self.driver = self.setup_driver()

    defextract_content(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        body_element = self.driver.find_element(By.TAG_NAME, "body")
        return body_element.text.strip()

    defextract_links(self):
        js_script = """
            var links = [];
            var elements = document.getElementsByTagName('a');
            for (var i = 0; i < elements.length; i++) {
                var href = elements[i].href;
                if (href) {
                    links.push(href);


            return links;

        return self.driver.execute_script(js_script)

    defload_data(self, base_url: str) -> List[Document]:
"""
        Load data from the base URL using BFS algorithm.

        Args:
            base_url (str): Base URL to start scraping.


        Returns:
            List[Document]: List of scraped documents.

        """
        added_urls = set()
        urls_to_visit = [(base_url, 0)]
        documents = []

        while urls_to_visit:
            current_url, depth = urls_to_visit.pop(0)
            print(f"Visiting: {current_url}, {len(urls_to_visit)} left")

            try:
                self.driver.get(current_url)
                page_content = self.extract_content()
                added_urls.add(current_url)

                next_depth = depth + 1
                if next_depth <= self.max_depth:
                    # links = self.driver.find_elements(By.TAG_NAME, 'a')
                    links = self.extract_links()
                    # clean all urls
                    links = [self.clean_url(link) for link in links]
                    # extract new links
                    links = [link for link in links if link not in added_urls]
                    print(f"Found {len(links)} new potential links")

                    for href in links:
                        try:
                            if href.startswith(self.prefix) and href not in added_urls:
                                urls_to_visit.append((href, next_depth))
                                added_urls.add(href)
                        except Exception:
                            continue

                doc = Document(text=page_content, extra_info={"URL": current_url})
                if self.uri_as_id:
                    warnings.warn(
                        "Setting the URI as the id of the document might break the code execution downstream and should be avoided."
                    )
                    doc.id_ = current_url
                documents.append(doc)
                time.sleep(1)

            except WebDriverException:
                print("WebDriverException encountered, restarting driver...")
                self.restart_driver()
            except Exception as e:
                print(f"An unexpected exception occurred: {e}, skipping URL...")
                continue

        self.driver.quit()
        return documents

```
 |  
| --- | --- |  
###  setup_driver [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.WholeSiteReader.setup_driver "Permanent link")

```
setup_driver()

```

Sets up the Selenium WebDriver for Chrome.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `WebDriver`  |  An instance of Chrome WebDriver.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/whole_site/base.py`  
| 
```
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
```
 | 
```
defsetup_driver(self):
"""
    Sets up the Selenium WebDriver for Chrome.

    Returns:
        WebDriver: An instance of Chrome WebDriver.

    """
    try:
        importchromedriver_autoinstaller
    except ImportError:
        raise ImportError("Please install chromedriver_autoinstaller")

    opt = webdriver.ChromeOptions()
    opt.add_argument("--start-maximized")
    chromedriver_autoinstaller.install()
    return webdriver.Chrome(options=opt)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.WholeSiteReader.load_data "Permanent link")

```
load_data(base_url: ) -> []

```

Load data from the base URL using BFS algorithm.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `base_url`  |  Base URL to start scraping.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of scraped documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/whole_site/base.py`  
| 
```
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
143
144
145
146
147
148
149
150
151
152
153
```
 | 
```
defload_data(self, base_url: str) -> List[Document]:
"""
    Load data from the base URL using BFS algorithm.

    Args:
        base_url (str): Base URL to start scraping.


    Returns:
        List[Document]: List of scraped documents.

    """
    added_urls = set()
    urls_to_visit = [(base_url, 0)]
    documents = []

    while urls_to_visit:
        current_url, depth = urls_to_visit.pop(0)
        print(f"Visiting: {current_url}, {len(urls_to_visit)} left")

        try:
            self.driver.get(current_url)
            page_content = self.extract_content()
            added_urls.add(current_url)

            next_depth = depth + 1
            if next_depth <= self.max_depth:
                # links = self.driver.find_elements(By.TAG_NAME, 'a')
                links = self.extract_links()
                # clean all urls
                links = [self.clean_url(link) for link in links]
                # extract new links
                links = [link for link in links if link not in added_urls]
                print(f"Found {len(links)} new potential links")

                for href in links:
                    try:
                        if href.startswith(self.prefix) and href not in added_urls:
                            urls_to_visit.append((href, next_depth))
                            added_urls.add(href)
                    except Exception:
                        continue

            doc = Document(text=page_content, extra_info={"URL": current_url})
            if self.uri_as_id:
                warnings.warn(
                    "Setting the URI as the id of the document might break the code execution downstream and should be avoided."
                )
                doc.id_ = current_url
            documents.append(doc)
            time.sleep(1)

        except WebDriverException:
            print("WebDriverException encountered, restarting driver...")
            self.restart_driver()
        except Exception as e:
            print(f"An unexpected exception occurred: {e}, skipping URL...")
            continue

    self.driver.quit()
    return documents

```
 |  
| --- | --- |  
##  ZyteWebReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ZyteWebReader "Permanent link")
Bases: 
Load text from URLs using `Zyte api`.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  Zyte API key.  |  _required_  |  
|  `mode`  |  `Literal['article', 'html', 'html-text']`  |  Determines how the text is extracted for the page content. It can take one of the following values: 'html', 'html-text', 'article'  |  `'article'`  |  
|  `n_conn`  |  It is the maximum number of concurrent requests to use.  |  
|  `**download_kwargs`  |  `Optional[Dict[str, Any]]`  |  Any additional download arguments to pass for download. See: https://docs.zyte.com/zyte-api/usage/reference.html  |  `None`  |  
Example
.. code-block:: python

```
from llama_index.readers.web import ZyteWebReader

reader = ZyteWebReader(
   api_key="ZYTE_API_KEY",
)
docs = reader.load_data(
    urls=["<url-1>", "<url-2>"],
)

```
Zyte-API reference
https://www.zyte.com/zyte-api/
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/zyte_web/base.py`  
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
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
```
 | 
```
classZyteWebReader(BasePydanticReader):
"""
    Load text from URLs using `Zyte api`.

    Args:
        api_key: Zyte API key.
        mode: Determines how the text is extracted for the page content.
            It can take one of the following values: 'html', 'html-text', 'article'
        n_conn: It is the maximum number of concurrent requests to use.
        **download_kwargs: Any additional download arguments to pass for download.
            See: https://docs.zyte.com/zyte-api/usage/reference.html

    Example:
        .. code-block:: python

            from llama_index.readers.web import ZyteWebReader

            reader = ZyteWebReader(
               api_key="ZYTE_API_KEY",

            docs = reader.load_data(
                urls=["<url-1>", "<url-2>"],


    Zyte-API reference:
        https://www.zyte.com/zyte-api/

    """

    client_async: Optional[object] = Field(None)
    api_key: str
    mode: str
    n_conn: int
    download_kwargs: Optional[dict]
    continue_on_failure: bool

    def__init__(
        self,
        api_key: str,
        mode: Literal["article", "html", "html-text"] = "article",
        n_conn: int = 15,
        download_kwargs: Optional[Dict[str, Any]] = None,
        continue_on_failure: bool = True,
    ) -> None:
"""Initialize with file path."""
        super().__init__(
            api_key=api_key,
            mode=mode,
            n_conn=n_conn,
            download_kwargs=download_kwargs,
            continue_on_failure=continue_on_failure,
        )
        try:
            fromzyte_apiimport AsyncZyteAPI
            fromzyte_api.utilsimport USER_AGENT as PYTHON_ZYTE_API_USER_AGENT

        except ImportError:
            raise ImportError(
                "zyte-api package not found, please install it with "
                "`pip install zyte-api`"
            )
        if mode not in ("article", "html", "html-text"):
            raise ValueError(
                f"Unrecognized mode '{mode}'. Expected one of "
                f"'article', 'html', 'html-text'."
            )

        user_agent = f"llama-index-zyte-api/{PYTHON_ZYTE_API_USER_AGENT}"
        self.client_async = AsyncZyteAPI(
            api_key=api_key, user_agent=user_agent, n_conn=n_conn
        )

    @classmethod
    defclass_name(cls) -> str:
        return "ZyteWebReader"

    def_zyte_html_option(self) -> str:
        if self.download_kwargs and "browserHtml" in self.download_kwargs:
            return "browserHtml"
        return "httpResponseBody"

    def_get_article(self, page: Dict) -> str:
        headline = page["article"].get("headline", "")
        article_body = page["article"].get("articleBody", "")
        return headline + "\n\n" + article_body

    def_zyte_request_params(self, url: str) -> dict:
        request_params: Dict[str, Any] = {"url": url}
        if self.mode == "article":
            request_params.update({"article": True})

        if self.mode in ("html", "html-text"):
            request_params.update({self._zyte_html_option(): True})

        if self.download_kwargs:
            request_params.update(self.download_kwargs)
        return request_params

    async deffetch_items(self, urls) -> List:
        results = []
        queries = [self._zyte_request_params(url) for url in urls]
        async with self.client_async.session() as session:
            for i, future in enumerate(session.iter(queries)):
                try:
                    result = await future
                    results.append(result)
                except Exception as e:
                    url = queries[i]["url"]
                    if self.continue_on_failure:
                        logger.warning(
                            f"Error {e} while fetching url {url}, "
                            f"skipping because continue_on_failure is True"
                        )
                        continue
                    else:
                        logger.exception(
                            f"Error fetching {url} and aborting, use "
                            f"continue_on_failure=True to continue loading "
                            f"urls after encountering an error."
                        )
                        raise
        return results

    def_get_content(self, response: Dict) -> str:
        if self.mode == "html-text":
            try:
                fromhtml2textimport html2text

            except ImportError:
                raise ImportError(
                    "html2text package not found, please install it with "
                    "`pip install html2text`"
                )
        if self.mode in ("html", "html-text"):
            content = response[self._zyte_html_option()]

            if self._zyte_html_option() == "httpResponseBody":
                content = b64decode(content).decode()

            if self.mode == "html-text":
                content = html2text(content)
        elif self.mode == "article":
            content = self._get_article(response)
        return content

    defload_data(self, urls) -> List[Document]:
        docs = []
        responses = asyncio.run(self.fetch_items(urls))
        for response in responses:
            content = self._get_content(response)
            doc = Document(text=content, metadata={"url": response["url"]})
            docs.append(doc)
        return docs

```
 |  
| --- | --- |  
##  ZenRowsWebReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ZenRowsWebReader "Permanent link")
Bases: 
ZenRows Web Reader.
Read web pages using ZenRows Universal Scraper API with advanced features like: - JavaScript rendering for dynamic content - Anti-bot bypass - Premium residential proxies with geo-location - Custom headers and session management - Advanced data extraction with CSS selectors - Multiple output formats (HTML, Markdown, Text, PDF) - Screenshot capabilities
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  ZenRows API key. Get one at https://app.zenrows.com/register  |  _required_  |  
|  `js_render`  |  `Optional[bool]`  |  Enable JavaScript rendering with a headless browser. Default False.  |  _required_  |  
|  `js_instructions`  |  `Optional[str]`  |  Execute custom JavaScript on the page to interact with elements.  |  _required_  |  
|  `premium_proxy`  |  `Optional[bool]`  |  Use residential IPs to bypass anti-bot protection. Default False.  |  _required_  |  
|  `proxy_country`  |  `Optional[str]`  |  Set the country of the IP used for the request (requires Premium Proxies).  |  _required_  |  
|  `session_id`  |  `Optional[int]`  |  Maintain the same IP for multiple requests for up to 10 minutes.  |  _required_  |  
|  `custom_headers`  |  `Optional[Dict[str, str]]`  |  Include custom headers in your request to mimic browser behavior.  |  _required_  |  
|  `wait_for`  |  `Optional[str]`  |  Wait for a specific CSS Selector to appear in the DOM before returning content.  |  _required_  |  
|  `wait`  |  `Optional[int]`  |  Wait a fixed amount of milliseconds after page load.  |  _required_  |  
|  `block_resources`  |  `Optional[str]`  |  Block specific resources (images, fonts, etc.) from loading.  |  _required_  |  
|  `response_type`  |  `Optional[Literal['markdown', 'plaintext', 'pdf']]`  |  Convert HTML to other formats.  |  _required_  |  
|  `css_extractor`  |  `Optional[str]`  |  Extract specific elements using CSS selectors (JSON format).  |  _required_  |  
|  `autoparse`  |  `Optional[bool]`  |  Automatically extract structured data from HTML. Default False.  |  _required_  |  
|  `screenshot`  |  `Optional[str]`  |  Capture an above-the-fold screenshot of the page.  |  _required_  |  
|  `screenshot_fullpage`  |  `Optional[str]`  |  Capture a full-page screenshot.  |  _required_  |  
|  `screenshot_selector`  |  `Optional[str]`  |  Capture a screenshot of a specific element using CSS Selector.  |  _required_  |  
|  `original_status`  |  `Optional[bool]`  |  Return the original HTTP status code from the target page. Default False.  |  _required_  |  
|  `allowed_status_codes`  |  `Optional[str]`  |  Returns content even if target page fails with specified status codes.  |  _required_  |  
|  `json_response`  |  `Optional[bool]`  |  Capture network requests in JSON format. Default False.  |  _required_  |  
|  `screenshot_format`  |  `Optional[Literal['png', 'jpeg']]`  |  Choose between png and jpeg formats for screenshots.  |  _required_  |  
|  `screenshot_quality`  |  `Optional[int]`  |  For JPEG format, set quality from 1 to 100.  |  _required_  |  
|  `outputs`  |  `Optional[str]`  |  Specify which data types to extract from the scraped HTML.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/zenrows_web/base.py`  
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
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
```
 | 
```
classZenRowsWebReader(BasePydanticReader):
"""
    ZenRows Web Reader.

    Read web pages using ZenRows Universal Scraper API with advanced features like:
    - JavaScript rendering for dynamic content
    - Anti-bot bypass
    - Premium residential proxies with geo-location
    - Custom headers and session management
    - Advanced data extraction with CSS selectors
    - Multiple output formats (HTML, Markdown, Text, PDF)
    - Screenshot capabilities

    Args:
        api_key (str): ZenRows API key. Get one at https://app.zenrows.com/register
        js_render (Optional[bool]): Enable JavaScript rendering with a headless browser. Default False.
        js_instructions (Optional[str]): Execute custom JavaScript on the page to interact with elements.
        premium_proxy (Optional[bool]): Use residential IPs to bypass anti-bot protection. Default False.
        proxy_country (Optional[str]): Set the country of the IP used for the request (requires Premium Proxies).
        session_id (Optional[int]): Maintain the same IP for multiple requests for up to 10 minutes.
        custom_headers (Optional[Dict[str, str]]): Include custom headers in your request to mimic browser behavior.
        wait_for (Optional[str]): Wait for a specific CSS Selector to appear in the DOM before returning content.
        wait (Optional[int]): Wait a fixed amount of milliseconds after page load.
        block_resources (Optional[str]): Block specific resources (images, fonts, etc.) from loading.
        response_type (Optional[Literal["markdown", "plaintext", "pdf"]]): Convert HTML to other formats.
        css_extractor (Optional[str]): Extract specific elements using CSS selectors (JSON format).
        autoparse (Optional[bool]): Automatically extract structured data from HTML. Default False.
        screenshot (Optional[str]): Capture an above-the-fold screenshot of the page.
        screenshot_fullpage (Optional[str]): Capture a full-page screenshot.
        screenshot_selector (Optional[str]): Capture a screenshot of a specific element using CSS Selector.
        original_status (Optional[bool]): Return the original HTTP status code from the target page. Default False.
        allowed_status_codes (Optional[str]): Returns content even if target page fails with specified status codes.
        json_response (Optional[bool]): Capture network requests in JSON format. Default False.
        screenshot_format (Optional[Literal["png", "jpeg"]]): Choose between png and jpeg formats for screenshots.
        screenshot_quality (Optional[int]): For JPEG format, set quality from 1 to 100.
        outputs (Optional[str]): Specify which data types to extract from the scraped HTML.

    """

    is_remote: bool = True
    api_key: str = Field(description="ZenRows API key")
    js_render: Optional[bool] = Field(
        default=False,
        description="Enable JavaScript rendering with a headless browser. Essential for modern web apps, SPAs, and sites with dynamic content.",
    )
    js_instructions: Optional[str] = Field(
        default=None,
        description="Execute custom JavaScript on the page to interact with elements, scroll, click buttons, or manipulate content.",
    )
    premium_proxy: Optional[bool] = Field(
        default=False,
        description="Use residential IPs to bypass anti-bot protection. Essential for accessing protected sites.",
    )
    proxy_country: Optional[str] = Field(
        default=None,
        description="Set the country of the IP used for the request (requires Premium Proxies). Use for accessing geo-restricted content.",
    )
    session_id: Optional[int] = Field(
        default=None,
        description="Maintain the same IP for multiple requests for up to 10 minutes. Essential for multi-step processes.",
    )
    custom_headers: Optional[Dict[str, str]] = Field(
        default=None,
        description="Include custom headers in your request to mimic browser behavior.",
    )
    wait_for: Optional[str] = Field(
        default=None,
        description="Wait for a specific CSS Selector to appear in the DOM before returning content.",
    )
    wait: Optional[int] = Field(
        default=None, description="Wait a fixed amount of milliseconds after page load."
    )
    block_resources: Optional[str] = Field(
        default=None,
        description="Block specific resources (images, fonts, etc.) from loading to speed up scraping.",
    )
    response_type: Optional[Literal["markdown", "plaintext", "pdf"]] = Field(
        default=None,
        description="Convert HTML to other formats. Options: markdown, plaintext, pdf.",
    )
    css_extractor: Optional[str] = Field(
        default=None,
        description="Extract specific elements using CSS selectors (JSON format).",
    )
    autoparse: Optional[bool] = Field(
        default=False, description="Automatically extract structured data from HTML."
    )
    screenshot: Optional[str] = Field(
        default=None, description="Capture an above-the-fold screenshot of the page."
    )
    screenshot_fullpage: Optional[str] = Field(
        default=None, description="Capture a full-page screenshot."
    )
    screenshot_selector: Optional[str] = Field(
        default=None,
        description="Capture a screenshot of a specific element using CSS Selector.",
    )
    original_status: Optional[bool] = Field(
        default=False,
        description="Return the original HTTP status code from the target page.",
    )
    allowed_status_codes: Optional[str] = Field(
        default=None,
        description="Returns the content even if the target page fails with specified status codes.",
    )
    json_response: Optional[bool] = Field(
        default=False,
        description="Capture network requests in JSON format, including XHR or Fetch data.",
    )
    screenshot_format: Optional[Literal["png", "jpeg"]] = Field(
        default=None,
        description="Choose between png (default) and jpeg formats for screenshots.",
    )
    screenshot_quality: Optional[int] = Field(
        default=None,
        description="For JPEG format, set quality from 1 to 100.",
    )
    outputs: Optional[str] = Field(
        default=None,
        description="Specify which data types to extract from the scraped HTML.",
    )

    _base_url: str = PrivateAttr(default="https://api.zenrows.com/v1/")

    @field_validator("css_extractor")
    @classmethod
    defvalidate_css_extractor(cls, v):
"""Validate that css_extractor is valid JSON if provided."""
        if v is not None:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("css_extractor must be valid JSON")
        return v

    @field_validator("proxy_country")
    @classmethod
    defvalidate_proxy_country(cls, v):
"""Validate that proxy_country is a two-letter country code."""
        if v is not None and len(v) != 2:
            raise ValueError("proxy_country must be a two-letter country code")
        return v

    def__init__(self, **kwargs):
"""Initialize ZenRows Web Reader."""
        super().__init__(**kwargs)
        if not self.api_key:
            raise ValueError(
                "ZenRows API key is required. Get one at https://app.zenrows.com/register"
            )

    @classmethod
    defclass_name(cls) -> str:
"""Get the name identifier of the class."""
        return "ZenRowsWebReader"

    def_prepare_request_params(
        self, url: str, extra_params: Optional[Dict] = None
    ) -> tuple[Dict[str, Any], Optional[Dict[str, str]]]:
"""Prepare request parameters for ZenRows API."""
        params = {"url": url, "apikey": self.api_key}

        # Add all configured parameters
        if self.js_render:
            params["js_render"] = self.js_render
        if self.js_instructions:
            params["js_instructions"] = self.js_instructions
        if self.premium_proxy:
            params["premium_proxy"] = self.premium_proxy
        if self.proxy_country:
            params["proxy_country"] = self.proxy_country
        if self.session_id:
            params["session_id"] = self.session_id
        if self.wait_for:
            params["wait_for"] = self.wait_for
        if self.wait:
            params["wait"] = self.wait
        if self.block_resources:
            params["block_resources"] = self.block_resources
        if self.response_type:
            params["response_type"] = self.response_type
        if self.css_extractor:
            params["css_extractor"] = self.css_extractor
        if self.autoparse:
            params["autoparse"] = self.autoparse
        if self.screenshot:
            params["screenshot"] = self.screenshot
        if self.screenshot_fullpage:
            params["screenshot_fullpage"] = self.screenshot_fullpage
        if self.screenshot_selector:
            params["screenshot_selector"] = self.screenshot_selector
        if self.original_status:
            params["original_status"] = self.original_status
        if self.allowed_status_codes:
            params["allowed_status_codes"] = self.allowed_status_codes
        if self.json_response:
            params["json_response"] = self.json_response
        if self.screenshot_format:
            params["screenshot_format"] = self.screenshot_format
        if self.screenshot_quality:
            params["screenshot_quality"] = self.screenshot_quality
        if self.outputs:
            params["outputs"] = self.outputs

        # Add any extra parameters for this specific request
        if extra_params:
            params.update(extra_params)

        # Auto-enable js_render for parameters that require JavaScript rendering
        js_required_params = [
            "screenshot",
            "screenshot_fullpage",
            "screenshot_selector",
            "js_instructions",
            "json_response",
            "wait",
            "wait_for",
        ]
        js_required = any(params.get(param) for param in js_required_params)

        if js_required:
            params["js_render"] = True

        # Special handling for screenshot variants
        screenshot_variants = ["screenshot_fullpage", "screenshot_selector"]
        if any(params.get(param) for param in screenshot_variants):
            params["screenshot"] = "true"

        # Auto-enable premium_proxy when proxy_country is specified
        if params.get("proxy_country"):
            params["premium_proxy"] = True

        # Handle custom headers
        request_headers = None
        if "custom_headers" in params and params["custom_headers"]:
            # Store the headers dictionary for the request
            request_headers = params["custom_headers"]
            # Set custom_headers to "true" to enable custom header support in the API
            params["custom_headers"] = "true"
        elif self.custom_headers:
            request_headers = self.custom_headers
            params["custom_headers"] = "true"
        else:
            # Remove custom_headers if not provided or empty
            params.pop("custom_headers", None)

        # Remove None values to avoid sending unnecessary parameters
        params = {k: v for k, v in params.items() if v is not None}

        return params, request_headers

    def_make_request(
        self, url: str, extra_params: Optional[Dict] = None
    ) -> requests.Response:
"""Make request to ZenRows API."""
        params, request_headers = self._prepare_request_params(url, extra_params)

        response = requests.get(
            self._base_url,
            params=params,
            headers=request_headers,
        )
        response.raise_for_status()
        return response

    def_extract_metadata(
        self, response: requests.Response, url: str
    ) -> Dict[str, Any]:
"""Extract metadata from ZenRows response."""
        metadata = {
            "source_url": url,
            "scraped_at": time.time(),
        }

        # Extract ZenRows specific headers
        if "X-Request-Cost" in response.headers:
            metadata["request_cost"] = float(response.headers["X-Request-Cost"])
        if "X-Request-Id" in response.headers:
            metadata["request_id"] = response.headers["X-Request-Id"]
        if "Zr-Final-Url" in response.headers:
            metadata["final_url"] = response.headers["Zr-Final-Url"]
        if "Concurrency-Remaining" in response.headers:
            metadata["concurrency_remaining"] = int(
                response.headers["Concurrency-Remaining"]
            )
        if "Concurrency-Limit" in response.headers:
            metadata["concurrency_limit"] = int(response.headers["Concurrency-Limit"])

        # Add response info
        metadata["status_code"] = response.status_code
        metadata["content_type"] = response.headers.get("Content-Type", "")
        metadata["content_length"] = len(response.content)

        # Add scraping configuration used
        metadata["zenrows_config"] = {
            "js_render": self.js_render,
            "premium_proxy": self.premium_proxy,
            "proxy_country": self.proxy_country,
            "session_id": self.session_id,
            "response_type": self.response_type,
        }

        return metadata

    def_process_response_content(self, response: requests.Response) -> str:
"""Process response content based on whether it's a screenshot or not."""
        # Handle screenshot responses
        screenshot_params = ["screenshot", "screenshot_fullpage", "screenshot_selector"]
        if any(getattr(self, param, None) for param in screenshot_params):
            return response.content

        # For all other responses, return text
        return response.text

    defload_data(
        self, urls: Union[str, List[str]], extra_params: Optional[Dict] = None, **kwargs
    ) -> List[Document]:
"""
        Load data from URLs using ZenRows API.

        Args:
            urls: Single URL string or list of URLs to scrape
            extra_params: Additional parameters for this specific request
            **kwargs: Additional keyword arguments (for compatibility)

        Returns:
            List of Document objects containing scraped content and metadata

        """
        if isinstance(urls, str):
            urls = [urls]

        documents = []

        for url in urls:
            try:
                response = self._make_request(url, extra_params)
                content = self._process_response_content(response)
                metadata = self._extract_metadata(response, url)

                # Create document
                document = Document(
                    text=content,
                    metadata=metadata,
                )
                documents.append(document)

            except Exception as e:
                # Create error document for failed URLs
                error_metadata = {
                    "source_url": url,
                    "error": str(e),
                    "scraped_at": time.time(),
                    "status": "failed",
                }
                error_document = Document(
                    text=f"Error scraping {url}: {e!s}",
                    metadata=error_metadata,
                )
                documents.append(error_document)

        return documents

```
 |  
| --- | --- |  
###  validate_css_extractor `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ZenRowsWebReader.validate_css_extractor "Permanent link")

```
validate_css_extractor(v)

```

Validate that css_extractor is valid JSON if provided.
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/zenrows_web/base.py`  
| 
```
137
138
139
140
141
142
143
144
145
146
```
 | 
```
@field_validator("css_extractor")
@classmethod
defvalidate_css_extractor(cls, v):
"""Validate that css_extractor is valid JSON if provided."""
    if v is not None:
        try:
            json.loads(v)
        except json.JSONDecodeError:
            raise ValueError("css_extractor must be valid JSON")
    return v

```
 |  
| --- | --- |  
###  validate_proxy_country `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ZenRowsWebReader.validate_proxy_country "Permanent link")

```
validate_proxy_country(v)

```

Validate that proxy_country is a two-letter country code.
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/zenrows_web/base.py`  
| 
```
148
149
150
151
152
153
154
```
 | 
```
@field_validator("proxy_country")
@classmethod
defvalidate_proxy_country(cls, v):
"""Validate that proxy_country is a two-letter country code."""
    if v is not None and len(v) != 2:
        raise ValueError("proxy_country must be a two-letter country code")
    return v

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ZenRowsWebReader.class_name "Permanent link")

```
class_name() -> 

```

Get the name identifier of the class.
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/zenrows_web/base.py`  
| 
```
164
165
166
167
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get the name identifier of the class."""
    return "ZenRowsWebReader"

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/web/#llama_index.readers.web.ZenRowsWebReader.load_data "Permanent link")

```
load_data(
    urls: Union[, []],
    extra_params: Optional[] = None,
    **kwargs
) -> []

```

Load data from URLs using ZenRows API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `Union[str, List[str]]`  |  Single URL string or list of URLs to scrape  |  _required_  |  
|  `extra_params`  |  `Optional[Dict]`  |  Additional parameters for this specific request  |  `None`  |  
|  `**kwargs`  |  Additional keyword arguments (for compatibility)  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List of Document objects containing scraped content and metadata  |  
Source code in `llama-index-integrations/readers/llama-index-readers-web/llama_index/readers/web/zenrows_web/base.py`  
| 
```
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
```
 | 
```
defload_data(
    self, urls: Union[str, List[str]], extra_params: Optional[Dict] = None, **kwargs
) -> List[Document]:
"""
    Load data from URLs using ZenRows API.

    Args:
        urls: Single URL string or list of URLs to scrape
        extra_params: Additional parameters for this specific request
        **kwargs: Additional keyword arguments (for compatibility)

    Returns:
        List of Document objects containing scraped content and metadata

    """
    if isinstance(urls, str):
        urls = [urls]

    documents = []

    for url in urls:
        try:
            response = self._make_request(url, extra_params)
            content = self._process_response_content(response)
            metadata = self._extract_metadata(response, url)

            # Create document
            document = Document(
                text=content,
                metadata=metadata,
            )
            documents.append(document)

        except Exception as e:
            # Create error document for failed URLs
            error_metadata = {
                "source_url": url,
                "error": str(e),
                "scraped_at": time.time(),
                "status": "failed",
            }
            error_document = Document(
                text=f"Error scraping {url}: {e!s}",
                metadata=error_metadata,
            )
            documents.append(error_document)

    return documents

```
 |  
| --- | --- |  
options: members: - AgentQLWebReader - AsyncWebPageReader - BeautifulSoupWebReader - BrowserbaseWebReader - FireCrawlWebReader - HyperbrowserWebReader - KnowledgeBaseWebReader - MainContentExtractorReader - NewsArticleReader - OlostepWebReader - OxylabsWebReader - ReadabilityWebPageReader - RssNewsReader - RssReader - ScrapflyReader - ScrapyWebReader - SimpleWebPageReader - SitemapReader - SpiderReader - TrafilaturaWebReader - UnstructuredURLLoader - WholeSiteReader - ZenRowsWebReader
