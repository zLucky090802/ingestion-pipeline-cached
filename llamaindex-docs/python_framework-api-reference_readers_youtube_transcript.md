# Youtube transcript
##  YoutubeTranscriptReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/youtube_transcript/#llama_index.readers.youtube_transcript.YoutubeTranscriptReader "Permanent link")
Bases: 
Youtube Transcript reader.
Source code in `llama-index-integrations/readers/llama-index-readers-youtube-transcript/llama_index/readers/youtube_transcript/base.py`  
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
```
 | 
```
classYoutubeTranscriptReader(BasePydanticReader):
"""Youtube Transcript reader."""

    is_remote: bool = True

    @classmethod
    defclass_name(cls) -> str:
"""Get the name identifier of the class."""
        return "YoutubeTranscriptReader"

    defload_data(
        self,
        ytlinks: List[str],
        languages: Optional[List[str]] = ["en"],
        **load_kwargs: Any,
    ) -> List[Document]:
"""
        Load data from the input directory.

        Args:
            pages (List[str]): List of youtube links \
                for which transcripts are to be read.

        """
        results = []
        for link in ytlinks:
            video_id = self._extract_video_id(link)
            if not video_id:
                raise ValueError(
                    f"Supplied url {link} is not a supported youtube URL."
                    "Supported formats include:"
                    "  youtube.com/watch?v=\\{video_id\\} "
                    "(with or without 'www.')\n"
                    "  youtube.com/embed?v=\\{video_id\\} "
                    "(with or without 'www.')\n"
                    "  youtu.be/{video_id\\} (never includes www subdomain)"
                )
            transcript_chunks = YouTubeTranscriptApi.get_transcript(
                video_id, languages=languages
            )
            chunk_text = [chunk["text"] for chunk in transcript_chunks]
            transcript = "\n".join(chunk_text)
            results.append(
                Document(
                    text=transcript, id_=video_id, extra_info={"video_id": video_id}
                )
            )
        return results

    @staticmethod
    def_extract_video_id(yt_link) -> Optional[str]:
        for pattern in YOUTUBE_URL_PATTERNS:
            match = re.search(pattern, yt_link)
            if match:
                return match.group(1)

        # return None if no match is found
        return None

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/youtube_transcript/#llama_index.readers.youtube_transcript.YoutubeTranscriptReader.class_name "Permanent link")

```
class_name() -> 

```

Get the name identifier of the class.
Source code in `llama-index-integrations/readers/llama-index-readers-youtube-transcript/llama_index/readers/youtube_transcript/base.py`  
| 
```
18
19
20
21
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get the name identifier of the class."""
    return "YoutubeTranscriptReader"

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/youtube_transcript/#llama_index.readers.youtube_transcript.YoutubeTranscriptReader.load_data "Permanent link")

```
load_data(
    ytlinks: [],
    languages: Optional[[]] = ["en"],
    **load_kwargs: 
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `pages`  |  `List[str]`  |  List of youtube links for which transcripts are to be read.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-youtube-transcript/llama_index/readers/youtube_transcript/base.py`  
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
defload_data(
    self,
    ytlinks: List[str],
    languages: Optional[List[str]] = ["en"],
    **load_kwargs: Any,
) -> List[Document]:
"""
    Load data from the input directory.

    Args:
        pages (List[str]): List of youtube links \
            for which transcripts are to be read.

    """
    results = []
    for link in ytlinks:
        video_id = self._extract_video_id(link)
        if not video_id:
            raise ValueError(
                f"Supplied url {link} is not a supported youtube URL."
                "Supported formats include:"
                "  youtube.com/watch?v=\\{video_id\\} "
                "(with or without 'www.')\n"
                "  youtube.com/embed?v=\\{video_id\\} "
                "(with or without 'www.')\n"
                "  youtu.be/{video_id\\} (never includes www subdomain)"
            )
        transcript_chunks = YouTubeTranscriptApi.get_transcript(
            video_id, languages=languages
        )
        chunk_text = [chunk["text"] for chunk in transcript_chunks]
        transcript = "\n".join(chunk_text)
        results.append(
            Document(
                text=transcript, id_=video_id, extra_info={"video_id": video_id}
            )
        )
    return results

```
 |  
| --- | --- |  
options: members: - YoutubeTranscriptReader
