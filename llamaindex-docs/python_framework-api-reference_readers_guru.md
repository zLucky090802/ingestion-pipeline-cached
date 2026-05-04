# Guru
##  GuruReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/guru/#llama_index.readers.guru.GuruReader "Permanent link")
Bases: 
Guru cards / collections reader.
Source code in `llama-index-integrations/readers/llama-index-readers-guru/llama_index/readers/guru/base.py`  
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
```
 | 
```
classGuruReader(BaseReader):
"""Guru cards / collections reader."""

    def__init__(self, guru_username: str, api_token: str) -> None:
"""
        Initialize GuruReader.

        Args:
            guru_username: Guru username.
            api_token: Guru API token. This can be personal API keys or collection based API keys. Note this is not the same as your password.

        """
        self.guru_username = guru_username
        self.api_token = api_token
        self.guru_auth = HTTPBasicAuth(guru_username, api_token)

    defload_data(
        self,
        collection_ids: Optional[List[str]] = None,
        card_ids: Optional[List[str]] = None,
    ) -> List[Document]:
"""
        Load data from Guru.

        Args:
            collection_ids: List of collection ids to load from. Only pass in card_ids or collection_ids, not both.
            card_ids: List of card ids to load from. Only pass in card_ids or collection_ids, not both.

        Returns:
            List[Document]: List of documents.

        """
        assert (collection_ids is None) or (card_ids is None), (
            "Only pass in card_ids or collection_ids, not both."
        )
        assert (collection_ids is not None) or (card_ids is not None), (
            "Pass in card_ids or collection_ids."
        )

        if collection_ids is not None:
            card_ids = self._get_card_ids_from_collection_ids(collection_ids)

        return [self._get_card_info(card_id) for card_id in card_ids]

    def_get_card_ids_from_collection_ids(self, collection_ids: List[str]) -> List[str]:
"""Get card ids from collection ids."""
        all_ids = []
        for collection_id in collection_ids:
            card_ids = self._get_card_ids_from_collection_id(collection_id)
            all_ids.extend(card_ids)
        return all_ids

    def_get_card_ids_from_collection_id(self, collection_id: str) -> List[str]:
        records = []
        next_page = True
        initial_url = "https://api.getguru.com/api/v1/search/cardmgr?queryType=cards"

        response = requests.get(initial_url, auth=self.guru_auth)
        records.extend(response.json())

        while next_page:
            try:
                url = response.headers["Link"]
                url_pattern = r"<(.*?)>"
                url_match = re.search(url_pattern, url)
                url = url_match.group(1)
            except Exception:
                next_page = False
                break

            response = requests.get(url, auth=self.guru_auth)
            records.extend(response.json())

        cards = pd.DataFrame.from_records(records)
        df_normalized = pd.json_normalize(cards["collection"])
        df_normalized.columns = ["collection_" + col for col in df_normalized.columns]
        df = pd.concat([cards, df_normalized], axis=1)
        df = df[df.collection_id == collection_id]
        return list(df["id"])

    def_get_card_info(self, card_id: str) -> Any:
"""
        Get card info.

        Args:
            card_id: Card id.

        Returns:
            Document: Document.

        """
        url = f"https://api.getguru.com/api/v1/cards/{card_id}/extended"
        headers = {"accept": "application/json"}
        response = requests.get(url, auth=self.guru_auth, headers=headers)

        if response.status_code == 200:
            title = response.json()["preferredPhrase"]
            html = response.json()["content"]  # i think this needs to be loaded
            content = self._clean_html(html)
            collection = response.json()["collection"]["name"]

            metadata = {
                "title": title,
                "collection": collection,
                "card_id": card_id,
                "guru_link": self._get_guru_link(card_id),
            }

            return Document(text=content, extra_info=metadata)
        else:
            logger.warning(f"Could not get card info for {card_id}.")
            return None

    @staticmethod
    def_clean_html(text: str) -> str:
"""
        Cleans HTML content by fetching its text representation using BeautifulSoup.
        """
        if text is None:
            return ""

        if isinstance(text, str):
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                soup = BeautifulSoup(text, "html.parser")
                return soup.get_text()

        return str(text)

    def_get_guru_link(self, card_id) -> str:
"""
        Takes a guru "ExternalId" from meta data and returns the link to the guru card.
        """
        url = f"https://api.getguru.com/api/v1/cards/{card_id}/extended"
        headers = {
            "accept": "application/json",
        }
        response = requests.get(url, headers=headers, auth=self.guru_auth)
        if response.status_code == 200:
            slug = response.json()["slug"]
        else:
            raise RuntimeError(f"Guru link doesn't exist: {response.status_code}")

        return f"https://app.getguru.com/card/{slug}"

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/guru/#llama_index.readers.guru.GuruReader.load_data "Permanent link")

```
load_data(
    collection_ids: Optional[[]] = None,
    card_ids: Optional[[]] = None,
) -> []

```

Load data from Guru.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_ids`  |  `Optional[List[str]]`  |  List of collection ids to load from. Only pass in card_ids or collection_ids, not both.  |  `None`  |  
|  `card_ids`  |  `Optional[List[str]]`  |  List of card ids to load from. Only pass in card_ids or collection_ids, not both.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-guru/llama_index/readers/guru/base.py`  
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
```
 | 
```
defload_data(
    self,
    collection_ids: Optional[List[str]] = None,
    card_ids: Optional[List[str]] = None,
) -> List[Document]:
"""
    Load data from Guru.

    Args:
        collection_ids: List of collection ids to load from. Only pass in card_ids or collection_ids, not both.
        card_ids: List of card ids to load from. Only pass in card_ids or collection_ids, not both.

    Returns:
        List[Document]: List of documents.

    """
    assert (collection_ids is None) or (card_ids is None), (
        "Only pass in card_ids or collection_ids, not both."
    )
    assert (collection_ids is not None) or (card_ids is not None), (
        "Pass in card_ids or collection_ids."
    )

    if collection_ids is not None:
        card_ids = self._get_card_ids_from_collection_ids(collection_ids)

    return [self._get_card_info(card_id) for card_id in card_ids]

```
 |  
| --- | --- |  
options: members: - GuruReader
