# Mangadex
Init file.
##  MangaDexReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mangadex/#llama_index.readers.mangadex.MangaDexReader "Permanent link")
Bases: 
Source code in `llama-index-integrations/readers/llama-index-readers-mangadex/llama_index/readers/mangadex/base.py`  
| 
```
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
```
 | 
```
classMangaDexReader(BaseReader):
    def__init__(self) -> None:
        self.base_url = "https://api.mangadex.org"

    def_get_manga_info(self, title: str):
        try:
            manga_response = requests.get(
                f"{self.base_url}/manga", params={"title": title}
            )
            manga_response.raise_for_status()
            manga_data = manga_response.json()["data"]

            if len(manga_data):
                return manga_data[0]
            else:
                logger.warning(f"No match found for title '{title}'")
                return None
        except requests.exceptions.HTTPError as http_error:
            logger.error(f"HTTP error: {http_error}")
        except requests.exceptions.RequestException as req_error:
            logger.error(f"Request Error: {req_error}")
        return None

    # Authors and artists are combined
    def_get_manga_author(self, id: str):
        try:
            author_response = requests.get(
                f"{self.base_url}/author", params={"ids[]": [id]}
            )
            author_response.raise_for_status()
            return author_response.json()["data"][0]
        except requests.exceptions.HTTPError as http_error:
            logger.error(f"HTTP error: {http_error}")
        except requests.exceptions.RequestException as req_error:
            logger.error(f"Request Error: {req_error}")
        return None

    def_get_manga_chapters(self, manga_id: str, lang: str):
        try:
            chapter_response = requests.get(
                f"{self.base_url}/manga/{manga_id}/feed",
                params={
                    "translatedLanguage[]": [lang],
                    "order[chapter]": "asc",
                },
            )
            chapter_response.raise_for_status()
            return chapter_response.json()
        except requests.exceptions.HTTPError as http_error:
            logger.error(f"HTTP error: {http_error}")
        except requests.exceptions.RequestException as req_error:
            logger.error(f"Request Error: {req_error}")
        return None

    defload_data(self, titles: List[str], lang: str = "en") -> List[Document]:
"""
        Load data from the MangaDex API.

        Args:
            title (List[str]): List of manga titles
            lang (str, optional): ISO 639-1 language code. Defaults to 'en'.


        Returns:
            List[Document]: A list of Documents.

        """
        result = []
        for title in titles:
            manga = self._get_manga_info(title)
            if not manga:
                continue

            author_name, artist_name = None, None
            for r in manga["relationships"]:
                if r["type"] == "author":
                    author = self._get_manga_author(r["id"])
                    author_name = author["attributes"]["name"]
                if r["type"] == "artist":
                    artist = self._get_manga_author(r["id"])
                    artist_name = artist["attributes"]["name"]

            chapters = self._get_manga_chapters(manga["id"], lang)
            chapter_count = chapters.get("total", None)
            latest_chapter_published_at = None
            if len(chapters["data"]):
                latest_chapter = chapters["data"][-1]
                latest_chapter_published_at = latest_chapter["attributes"]["publishAt"]

            # Get tags for the selected language
            tags = []
            for tag in manga["attributes"]["tags"]:
                tag_name_dict = tag["attributes"]["name"]
                if lang in tag_name_dict:
                    tags.append(tag_name_dict[lang])

            doc = Document(
                text=manga["attributes"]["title"].get(lang, title),
                extra_info={
                    "id": manga["id"],
                    "author": author_name,
                    "artist": artist_name,
                    "description": manga["attributes"]["description"].get(lang, None),
                    "original_language": manga["attributes"]["originalLanguage"],
                    "tags": tags,
                    "chapter_count": chapter_count,
                    "latest_chapter_published_at": latest_chapter_published_at,
                },
            )
            result.append(doc)

        return result

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mangadex/#llama_index.readers.mangadex.MangaDexReader.load_data "Permanent link")

```
load_data(
    titles: [], lang:  = "en"
) -> []

```

Load data from the MangaDex API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `title`  |  `List[str]`  |  List of manga titles  |  _required_  |  
|  `lang`  |  ISO 639-1 language code. Defaults to 'en'.  |  `'en'`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-mangadex/llama_index/readers/mangadex/base.py`  
| 
```
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
```
 | 
```
defload_data(self, titles: List[str], lang: str = "en") -> List[Document]:
"""
    Load data from the MangaDex API.

    Args:
        title (List[str]): List of manga titles
        lang (str, optional): ISO 639-1 language code. Defaults to 'en'.


    Returns:
        List[Document]: A list of Documents.

    """
    result = []
    for title in titles:
        manga = self._get_manga_info(title)
        if not manga:
            continue

        author_name, artist_name = None, None
        for r in manga["relationships"]:
            if r["type"] == "author":
                author = self._get_manga_author(r["id"])
                author_name = author["attributes"]["name"]
            if r["type"] == "artist":
                artist = self._get_manga_author(r["id"])
                artist_name = artist["attributes"]["name"]

        chapters = self._get_manga_chapters(manga["id"], lang)
        chapter_count = chapters.get("total", None)
        latest_chapter_published_at = None
        if len(chapters["data"]):
            latest_chapter = chapters["data"][-1]
            latest_chapter_published_at = latest_chapter["attributes"]["publishAt"]

        # Get tags for the selected language
        tags = []
        for tag in manga["attributes"]["tags"]:
            tag_name_dict = tag["attributes"]["name"]
            if lang in tag_name_dict:
                tags.append(tag_name_dict[lang])

        doc = Document(
            text=manga["attributes"]["title"].get(lang, title),
            extra_info={
                "id": manga["id"],
                "author": author_name,
                "artist": artist_name,
                "description": manga["attributes"]["description"].get(lang, None),
                "original_language": manga["attributes"]["originalLanguage"],
                "tags": tags,
                "chapter_count": chapter_count,
                "latest_chapter_published_at": latest_chapter_published_at,
            },
        )
        result.append(doc)

    return result

```
 |  
| --- | --- |  
options: members: - MangaDexReader
