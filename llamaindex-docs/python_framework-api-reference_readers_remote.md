# Remote
Init file.
##  RemoteReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/remote/#llama_index.readers.remote.RemoteReader "Permanent link")
Bases: 
General reader for any remote page or file.
Source code in `llama-index-integrations/readers/llama-index-readers-remote/llama_index/readers/remote/base.py`  
| 
```
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
```
 | 
```
classRemoteReader(BaseReader):
"""General reader for any remote page or file."""

    def__init__(
        self,
        *args: Any,
        file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = None,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__(*args, **kwargs)

        self.file_extractor = file_extractor

    @staticmethod
    def_is_youtube_video(url: str) -> bool:
        # TODO create more global method for detecting all types
"""
        Returns True if the given URL is a video on YouTube, False otherwise.
        """
        # Regular expression pattern to match YouTube video URLs
        youtube_pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([^\s&]+)"

        # Match the pattern against the URL
        match = re.match(youtube_pattern, url)

        # If there's a match, it's a YouTube video URL
        return match is not None

    defload_data(self, url: str) -> List[Document]:
"""Parse whatever is at the URL."""
        importtempfile
        fromurllib.parseimport urlparse
        fromurllib.requestimport Request, urlopen

        # check the URL
        parsed_url = urlparse(url)

        # Check if the scheme is http or https
        if parsed_url.scheme not in (
            "http",
            "https",
            "ftp",
            "ws",
            "wss",
            "sftp",
            "ftps",
            "s3",
        ):
            raise ValueError(
                "Invalid URL scheme. Only http, https, ftp, ftps, sftp, ws, wss, and s3 are allowed."
            )

        extra_info = {"Source": url}

        req = Request(url, headers={"User-Agent": "Magic Browser"})
        result = urlopen(req)
        url_type = result.info().get_content_type()
        documents = []
        if url_type == "text/html" or url_type == "text/plain":
            text = "\n\n".join([str(el.decode("utf-8-sig")) for el in result])
            documents = [Document(text=text, extra_info=extra_info)]
        elif self._is_youtube_video(url):
            youtube_reader = YoutubeTranscriptReader()
            # TODO should we have another language, like english / french?
            documents = youtube_reader.load_data([url])
        else:
            suffix = Path(urlparse(url).path).suffix
            with tempfile.TemporaryDirectory() as temp_dir:
                filepath = f"{temp_dir}/temp{suffix}"
                with open(filepath, "wb") as output:
                    output.write(result.read())
                loader = SimpleDirectoryReader(
                    temp_dir,
                    file_metadata=(lambda _: extra_info),
                    file_extractor=self.file_extractor,
                )
                documents = loader.load_data()
        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/remote/#llama_index.readers.remote.RemoteReader.load_data "Permanent link")

```
load_data(url: ) -> []

```

Parse whatever is at the URL.
Source code in `llama-index-integrations/readers/llama-index-readers-remote/llama_index/readers/remote/base.py`  
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
```
 | 
```
defload_data(self, url: str) -> List[Document]:
"""Parse whatever is at the URL."""
    importtempfile
    fromurllib.parseimport urlparse
    fromurllib.requestimport Request, urlopen

    # check the URL
    parsed_url = urlparse(url)

    # Check if the scheme is http or https
    if parsed_url.scheme not in (
        "http",
        "https",
        "ftp",
        "ws",
        "wss",
        "sftp",
        "ftps",
        "s3",
    ):
        raise ValueError(
            "Invalid URL scheme. Only http, https, ftp, ftps, sftp, ws, wss, and s3 are allowed."
        )

    extra_info = {"Source": url}

    req = Request(url, headers={"User-Agent": "Magic Browser"})
    result = urlopen(req)
    url_type = result.info().get_content_type()
    documents = []
    if url_type == "text/html" or url_type == "text/plain":
        text = "\n\n".join([str(el.decode("utf-8-sig")) for el in result])
        documents = [Document(text=text, extra_info=extra_info)]
    elif self._is_youtube_video(url):
        youtube_reader = YoutubeTranscriptReader()
        # TODO should we have another language, like english / french?
        documents = youtube_reader.load_data([url])
    else:
        suffix = Path(urlparse(url).path).suffix
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = f"{temp_dir}/temp{suffix}"
            with open(filepath, "wb") as output:
                output.write(result.read())
            loader = SimpleDirectoryReader(
                temp_dir,
                file_metadata=(lambda _: extra_info),
                file_extractor=self.file_extractor,
            )
            documents = loader.load_data()
    return documents

```
 |  
| --- | --- |  
options: members: - RemoteReader
