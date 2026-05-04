# Quip
##  QuipReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/quip/#llama_index.readers.quip.QuipReader "Permanent link")
Bases: 
Source code in `llama-index-integrations/readers/llama-index-readers-quip/llama_index/readers/quip/base.py`  
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
```
 | 
```
classQuipReader(BasePydanticReader):
    access_token: str = Field(description="Quip API access token")
    request_timeout: Optional[float] = Field(
        default=None, description="Request timeout in seconds"
    )
    headers: Dict[str, str] = Field(
        default=None, description="Headers to be sent with the request"
    )

    def__init__(
        self,
        access_token: str,
        request_timeout: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        headers = headers or {}
        if "Authorization" not in headers:
            headers["Authorization"] = "Bearer " + access_token
        super().__init__(
            access_token=access_token,
            request_timeout=request_timeout,
            headers=headers,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "QuipReader"

    defload_data(self, thread_ids: List[str]) -> List[Document]:
"""Load data from Quip."""
        documents = []
        thread_contents = self._get_threads(thread_ids)
        for i, content in enumerate(thread_contents):
            doc = Document(
                text=content, id_=thread_ids[i], extra_info={"thread_id": thread_ids[i]}
            )
            documents.append(doc)
        return documents

    def_get_threads(self, ids: List[str]) -> List[str]:
"""Returns a dictionary of threads for the given IDs."""
        threads = []
        for id in ids:
            thread_content = self._get_thread(id)
            threads.append(thread_content)
        return threads

    def_get_thread(self, id) -> str:
"""Returns the thread with the given ID."""
        url = BASE_URL + "/2/" + "threads/" + id + "/html"
        return self._request_with_retry("GET", url, headers=self.headers).get(
            "html", ""
        )

    def_request_with_retry(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
"""Make a request with retry and rate limit handling."""
        max_retries = 5
        backoff_factor = 1

        for attempt in range(max_retries):
            try:
                response = requests.request(method, url, headers=headers, json=json)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError:
                if response.status_code == 429:
                    # Rate limit exceeded
                    retry_after = int(response.headers.get("Retry-After", 1))
                    time.sleep(backoff_factor * (2**attempt) + retry_after)
                else:
                    raise requests.exceptions.HTTPError(
                        f"Request failed: {response.text}"
                    )
            except requests.exceptions.RequestException as err:
                raise requests.exceptions.RequestException(f"Request failed: {err}")
        raise Exception("Maximum retries exceeded")

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/quip/#llama_index.readers.quip.QuipReader.load_data "Permanent link")

```
load_data(thread_ids: []) -> []

```

Load data from Quip.
Source code in `llama-index-integrations/readers/llama-index-readers-quip/llama_index/readers/quip/base.py`  
| 
```
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
```
 | 
```
defload_data(self, thread_ids: List[str]) -> List[Document]:
"""Load data from Quip."""
    documents = []
    thread_contents = self._get_threads(thread_ids)
    for i, content in enumerate(thread_contents):
        doc = Document(
            text=content, id_=thread_ids[i], extra_info={"thread_id": thread_ids[i]}
        )
        documents.append(doc)
    return documents

```
 |  
| --- | --- |  
options: members: - QuipReader
