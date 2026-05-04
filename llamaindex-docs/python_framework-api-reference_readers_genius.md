# Genius
##  GeniusReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/genius/#llama_index.readers.genius.GeniusReader "Permanent link")
Bases: 
GeniusReader for various operations with lyricsgenius.
Source code in `llama-index-integrations/readers/llama-index-readers-genius/llama_index/readers/genius/base.py`  
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
```
 | 
```
classGeniusReader(BaseReader):
"""GeniusReader for various operations with lyricsgenius."""

    def__init__(self, access_token: str):
"""Initialize the GeniusReader with an access token."""
        try:
            importlyricsgenius
        except ImportError:
            raise ImportError(
                "Please install lyricsgenius via 'pip install lyricsgenius'"
            )
        self.genius = lyricsgenius.Genius(access_token)

    defload_artist_songs(
        self, artist_name: str, max_songs: Optional[int] = None
    ) -> List[Document]:
"""Load all or a specified number of songs by an artist."""
        artist = self.genius.search_artist(artist_name, max_songs=max_songs)
        return [Document(text=song.lyrics) for song in artist.songs] if artist else []

    defload_all_artist_songs(self, artist_name: str) -> List[Document]:
        artist = self.genius.search_artist(artist_name)
        artist.save_lyrics()
        return [Document(text=song.lyrics) for song in artist.songs]

    defload_artist_songs_with_filters(
        self,
        artist_name: str,
        most_popular: bool = True,
        max_songs: Optional[int] = None,
        max_pages: int = 50,
    ) -> Document:
"""
        Load the most or least popular song of an artist.

        Args:
            artist_name (str): The artist's name.
            most_popular (bool): True for most popular, False for least popular song.
            max_songs (Optional[int]): Maximum number of songs to consider for popularity.
            max_pages (int): Maximum number of pages to fetch.

        Returns:
            Document: A document containing lyrics of the most/least popular song.

        """
        artist = self.genius.search_artist(artist_name, max_songs=1)
        if not artist:
            return None

        songs_fetched = 0
        page = 1
        songs = []
        while (
            page
            and page <= max_pages
            and (max_songs is None or songs_fetched  max_songs)
        ):
            request = self.genius.artist_songs(
                artist.id, sort="popularity", per_page=50, page=page
            )
            songs.extend(request["songs"])
            songs_fetched += len(request["songs"])
            page = (
                request["next_page"]
                if (max_songs is None or songs_fetched  max_songs)
                else None
            )

        target_song = songs[0] if most_popular else songs[-1]
        song_details = self.genius.search_song(target_song["title"], artist.name)
        return Document(text=song_details.lyrics) if song_details else None

    defload_song_by_url_or_id(
        self, song_url: Optional[str] = None, song_id: Optional[int] = None
    ) -> List[Document]:
"""Load song by URL or ID."""
        if song_url:
            song = self.genius.song(url=song_url)
        elif song_id:
            song = self.genius.song(song_id)
        else:
            return []

        return [Document(text=song.lyrics)] if song else []

    defsearch_songs_by_lyrics(self, lyrics: str) -> List[Document]:
"""
        Search for songs by a snippet of lyrics.

        Args:
            lyrics (str): The lyric snippet you're looking for.

        Returns:
            List[Document]: A list of documents containing songs with those lyrics.

        """
        search_results = self.genius.search_songs(lyrics)
        songs = search_results["hits"] if search_results else []

        results = []
        for hit in songs:
            song_url = hit["result"]["url"]
            song_lyrics = self.genius.lyrics(song_url=song_url)
            results.append(Document(text=song_lyrics))

        return results

    defload_songs_by_tag(
        self, tag: str, max_songs: Optional[int] = None, max_pages: int = 50
    ) -> List[Document]:
"""
        Load songs by a specific tag.

        Args:
            tag (str): The tag or genre to load songs for.
            max_songs (Optional[int]): Maximum number of songs to fetch. If None, no specific limit.
            max_pages (int): Maximum number of pages to fetch.

        Returns:
            List[Document]: A list of documents containing song lyrics.

        """
        lyrics = []
        total_songs_fetched = 0
        page = 1

        while (
            page
            and page <= max_pages
            and (max_songs is None or total_songs_fetched  max_songs)
        ):
            res = self.genius.tag(tag, page=page)
            for hit in res["hits"]:
                if max_songs is None or total_songs_fetched  max_songs:
                    song_lyrics = self.genius.lyrics(song_url=hit["url"])
                    lyrics.append(Document(text=song_lyrics))
                    total_songs_fetched += 1
                else:
                    break
            page = (
                res["next_page"]
                if max_songs is None or total_songs_fetched  max_songs
                else None
            )

        return lyrics

```
 |  
| --- | --- |  
###  load_artist_songs [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/genius/#llama_index.readers.genius.GeniusReader.load_artist_songs "Permanent link")

```
load_artist_songs(
    artist_name: , max_songs: Optional[] = None
) -> []

```

Load all or a specified number of songs by an artist.
Source code in `llama-index-integrations/readers/llama-index-readers-genius/llama_index/readers/genius/base.py`  
| 
```
22
23
24
25
26
27
```
 | 
```
defload_artist_songs(
    self, artist_name: str, max_songs: Optional[int] = None
) -> List[Document]:
"""Load all or a specified number of songs by an artist."""
    artist = self.genius.search_artist(artist_name, max_songs=max_songs)
    return [Document(text=song.lyrics) for song in artist.songs] if artist else []

```
 |  
| --- | --- |  
###  load_artist_songs_with_filters [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/genius/#llama_index.readers.genius.GeniusReader.load_artist_songs_with_filters "Permanent link")

```
load_artist_songs_with_filters(
    artist_name: ,
    most_popular:  = True,
    max_songs: Optional[] = None,
    max_pages:  = 50,
) -> 

```

Load the most or least popular song of an artist.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `artist_name`  |  The artist's name.  |  _required_  |  
|  `most_popular`  |  `bool`  |  True for most popular, False for least popular song.  |  `True`  |  
|  `max_songs`  |  `Optional[int]`  |  Maximum number of songs to consider for popularity.  |  `None`  |  
|  `max_pages`  |  Maximum number of pages to fetch.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |   |  A document containing lyrics of the most/least popular song.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-genius/llama_index/readers/genius/base.py`  
| 
```
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
```
 | 
```
defload_artist_songs_with_filters(
    self,
    artist_name: str,
    most_popular: bool = True,
    max_songs: Optional[int] = None,
    max_pages: int = 50,
) -> Document:
"""
    Load the most or least popular song of an artist.

    Args:
        artist_name (str): The artist's name.
        most_popular (bool): True for most popular, False for least popular song.
        max_songs (Optional[int]): Maximum number of songs to consider for popularity.
        max_pages (int): Maximum number of pages to fetch.

    Returns:
        Document: A document containing lyrics of the most/least popular song.

    """
    artist = self.genius.search_artist(artist_name, max_songs=1)
    if not artist:
        return None

    songs_fetched = 0
    page = 1
    songs = []
    while (
        page
        and page <= max_pages
        and (max_songs is None or songs_fetched  max_songs)
    ):
        request = self.genius.artist_songs(
            artist.id, sort="popularity", per_page=50, page=page
        )
        songs.extend(request["songs"])
        songs_fetched += len(request["songs"])
        page = (
            request["next_page"]
            if (max_songs is None or songs_fetched  max_songs)
            else None
        )

    target_song = songs[0] if most_popular else songs[-1]
    song_details = self.genius.search_song(target_song["title"], artist.name)
    return Document(text=song_details.lyrics) if song_details else None

```
 |  
| --- | --- |  
###  load_song_by_url_or_id [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/genius/#llama_index.readers.genius.GeniusReader.load_song_by_url_or_id "Permanent link")

```
load_song_by_url_or_id(
    song_url: Optional[] = None,
    song_id: Optional[] = None,
) -> []

```

Load song by URL or ID.
Source code in `llama-index-integrations/readers/llama-index-readers-genius/llama_index/readers/genius/base.py`  
| 
```
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
```
 | 
```
defload_song_by_url_or_id(
    self, song_url: Optional[str] = None, song_id: Optional[int] = None
) -> List[Document]:
"""Load song by URL or ID."""
    if song_url:
        song = self.genius.song(url=song_url)
    elif song_id:
        song = self.genius.song(song_id)
    else:
        return []

    return [Document(text=song.lyrics)] if song else []

```
 |  
| --- | --- |  
###  search_songs_by_lyrics [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/genius/#llama_index.readers.genius.GeniusReader.search_songs_by_lyrics "Permanent link")

```
search_songs_by_lyrics(lyrics: ) -> []

```

Search for songs by a snippet of lyrics.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `lyrics`  |  The lyric snippet you're looking for.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents containing songs with those lyrics.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-genius/llama_index/readers/genius/base.py`  
| 
```
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
```
 | 
```
defsearch_songs_by_lyrics(self, lyrics: str) -> List[Document]:
"""
    Search for songs by a snippet of lyrics.

    Args:
        lyrics (str): The lyric snippet you're looking for.

    Returns:
        List[Document]: A list of documents containing songs with those lyrics.

    """
    search_results = self.genius.search_songs(lyrics)
    songs = search_results["hits"] if search_results else []

    results = []
    for hit in songs:
        song_url = hit["result"]["url"]
        song_lyrics = self.genius.lyrics(song_url=song_url)
        results.append(Document(text=song_lyrics))

    return results

```
 |  
| --- | --- |  
###  load_songs_by_tag [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/genius/#llama_index.readers.genius.GeniusReader.load_songs_by_tag "Permanent link")

```
load_songs_by_tag(
    tag: ,
    max_songs: Optional[] = None,
    max_pages:  = 50,
) -> []

```

Load songs by a specific tag.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `tag`  |  The tag or genre to load songs for.  |  _required_  |  
|  `max_songs`  |  `Optional[int]`  |  Maximum number of songs to fetch. If None, no specific limit.  |  `None`  |  
|  `max_pages`  |  Maximum number of pages to fetch.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents containing song lyrics.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-genius/llama_index/readers/genius/base.py`  
| 
```
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
```
 | 
```
defload_songs_by_tag(
    self, tag: str, max_songs: Optional[int] = None, max_pages: int = 50
) -> List[Document]:
"""
    Load songs by a specific tag.

    Args:
        tag (str): The tag or genre to load songs for.
        max_songs (Optional[int]): Maximum number of songs to fetch. If None, no specific limit.
        max_pages (int): Maximum number of pages to fetch.

    Returns:
        List[Document]: A list of documents containing song lyrics.

    """
    lyrics = []
    total_songs_fetched = 0
    page = 1

    while (
        page
        and page <= max_pages
        and (max_songs is None or total_songs_fetched  max_songs)
    ):
        res = self.genius.tag(tag, page=page)
        for hit in res["hits"]:
            if max_songs is None or total_songs_fetched  max_songs:
                song_lyrics = self.genius.lyrics(song_url=hit["url"])
                lyrics.append(Document(text=song_lyrics))
                total_songs_fetched += 1
            else:
                break
        page = (
            res["next_page"]
            if max_songs is None or total_songs_fetched  max_songs
            else None
        )

    return lyrics

```
 |  
| --- | --- |  
options: members: - GeniusReader
