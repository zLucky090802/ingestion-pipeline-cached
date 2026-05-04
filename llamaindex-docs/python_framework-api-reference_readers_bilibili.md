# Bilibili
##  BilibiliTranscriptReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/bilibili/#llama_index.readers.bilibili.BilibiliTranscriptReader "Permanent link")
Bases: 
Bilibili Transcript and video info reader.
Source code in `llama-index-integrations/readers/llama-index-readers-bilibili/llama_index/readers/bilibili/base.py`  
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
```
 | 
```
classBilibiliTranscriptReader(BaseReader):
"""Bilibili Transcript and video info reader."""

    @staticmethod
    defget_bilibili_info_and_subs(bili_url):
        importjson
        importre

        importrequests
        frombilibili_apiimport sync, video

        bvid = re.search(r"BV\w+", bili_url).group()
        # Create credential object
        v = video.Video(bvid=bvid)
        # Get video info and basic info
        video_info = sync(v.get_info())
        title = video_info["title"]
        desc = video_info["desc"]

        # Get subtitle url
        sub_list = video_info["subtitle"]["list"]
        if sub_list:
            sub_url = sub_list[0]["subtitle_url"]
            result = requests.get(sub_url)
            raw_sub_titles = json.loads(result.content)["body"]
            raw_transcript = " ".join([c["content"] for c in raw_sub_titles])
            # Add basic video info to transcript
            return (
                f"Video Title: {title}, description: {desc}\nTranscript:"
                f" {raw_transcript}"
            )
        else:
            raw_transcript = ""
            warnings.warn(
                f"No subtitles found for video: {bili_url}. Return Empty transcript."
            )
            return raw_transcript

    defload_data(self, video_urls: List[str], **load_kwargs: Any) -> List[Document]:
"""
        Load auto generated Video Transcripts from Bilibili, including additional metadata.

        Args:
            video_urls (List[str]): List of Bilibili links for which transcripts are to be read.

        Returns:
            List[Document]: A list of Document objects, each containing the transcript for a Bilibili video.

        """
        results = []
        for bili_url in video_urls:
            try:
                transcript = self.get_bilibili_info_and_subs(bili_url)
                results.append(Document(text=transcript))
            except Exception as e:
                warnings.warn(
                    f"Error loading transcript for video {bili_url}: {e!s}. Skipping"
                    " video."
                )
        return results

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/bilibili/#llama_index.readers.bilibili.BilibiliTranscriptReader.load_data "Permanent link")

```
load_data(
    video_urls: [], **load_kwargs: 
) -> []

```

Load auto generated Video Transcripts from Bilibili, including additional metadata.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `video_urls`  |  `List[str]`  |  List of Bilibili links for which transcripts are to be read.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects, each containing the transcript for a Bilibili video.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-bilibili/llama_index/readers/bilibili/base.py`  
| 
```
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
```
 | 
```
defload_data(self, video_urls: List[str], **load_kwargs: Any) -> List[Document]:
"""
    Load auto generated Video Transcripts from Bilibili, including additional metadata.

    Args:
        video_urls (List[str]): List of Bilibili links for which transcripts are to be read.

    Returns:
        List[Document]: A list of Document objects, each containing the transcript for a Bilibili video.

    """
    results = []
    for bili_url in video_urls:
        try:
            transcript = self.get_bilibili_info_and_subs(bili_url)
            results.append(Document(text=transcript))
        except Exception as e:
            warnings.warn(
                f"Error loading transcript for video {bili_url}: {e!s}. Skipping"
                " video."
            )
    return results

```
 |  
| --- | --- |  
options: members: - BilibiliTranscriptReader
