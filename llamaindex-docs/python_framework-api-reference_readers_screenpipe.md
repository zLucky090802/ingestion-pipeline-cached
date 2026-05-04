# Screenpipe
##  ScreenpipeReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/screenpipe/#llama_index.readers.screenpipe.ScreenpipeReader "Permanent link")
Bases: 
Screenpipe reader.
Reads screen capture (OCR) and audio transcription data from a local Screenpipe instance via its REST API.
See https://github.com/mediar-ai/screenpipe for details.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `base_url`  |  Base URL of the Screenpipe server. Defaults to `http://localhost:3030`.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-screenpipe/llama_index/readers/screenpipe/base.py`  
| 
```
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
```
 | 
```
classScreenpipeReader(BasePydanticReader):
"""
    Screenpipe reader.

    Reads screen capture (OCR) and audio transcription data from a local
    Screenpipe instance via its REST API.

    See https://github.com/mediar-ai/screenpipe for details.

    Args:
        base_url (str): Base URL of the Screenpipe server.
            Defaults to ``http://localhost:3030``.

    """

    is_remote: bool = True
    base_url: str = "http://localhost:3030"

    @classmethod
    defclass_name(cls) -> str:
        return "ScreenpipeReader"

    @staticmethod
    def_to_utc_isoformat(dt: datetime) -> str:
"""
        Convert a datetime to a UTC ISO 8601 string.

        Screenpipe requires UTC timestamps. Naive datetimes (no tzinfo) are
        assumed to be local time and converted to UTC.
        """
        if dt.tzinfo is None:
            dt = dt.astimezone(timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
"""Execute a search request against the Screenpipe API."""
        url = SEARCH_URL_TMPL.format(base_url=self.base_url.rstrip("/"))
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    defload_data(
        self,
        content_type: str = "all",
        query: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        app_name: Optional[str] = None,
        window_name: Optional[str] = None,
        limit: int = 20,
    ) -> List[Document]:
"""
        Load data from Screenpipe.

        Args:
            content_type: Type of content to retrieve.
                One of ``"all"``, ``"ocr"``, ``"audio"``, ``"ui"``,
                ``"audio+ui"``, ``"ocr+ui"``, ``"audio+ocr"``.
            query: Optional search query for semantic filtering.
            start_time: Filter results after this timestamp.
            end_time: Filter results before this timestamp.
            app_name: Filter by application name.
            window_name: Filter by window name.
            limit: Maximum number of results to return.

        Returns:
            List of documents.

        """
        if content_type not in VALID_CONTENT_TYPES:
            raise ValueError(
                f"Invalid content_type '{content_type}'. "
                f"Must be one of: {sorted(VALID_CONTENT_TYPES)}"
            )

        params: Dict[str, Any] = {
            "content_type": content_type,
            "limit": limit,
        }
        if query is not None:
            params["q"] = query
        if start_time is not None:
            params["start_time"] = self._to_utc_isoformat(start_time)
        if end_time is not None:
            params["end_time"] = self._to_utc_isoformat(end_time)
        if app_name is not None:
            params["app_name"] = app_name
        if window_name is not None:
            params["window_name"] = window_name

        all_items: List[Dict[str, Any]] = []
        offset = 0

        while True:
            params["offset"] = offset
            data = self._search(params)
            items = data.get("data", [])
            if not items:
                break
            all_items.extend(items)
            if len(all_items) >= limit:
                all_items = all_items[:limit]
                break
            pagination = data.get("pagination", {})
            total = pagination.get("total", 0)
            offset += len(items)
            if offset >= total:
                break

        documents = []
        for item in all_items:
            doc = self._item_to_document(item)
            if doc is not None:
                documents.append(doc)

        return documents

    def_item_to_document(self, item: Dict[str, Any]) -> Optional[Document]:
"""Convert a Screenpipe search result item to a Document."""
        item_type = item.get("type", "")
        content = item.get("content", {})

        if item_type == "OCR":
            return self._ocr_to_document(content)
        elif item_type == "Audio":
            return self._audio_to_document(content)
        elif item_type == "UI":
            return self._ui_to_document(content)
        else:
            logger.warning("Unknown item type '%s', skipping.", item_type)
            return None

    def_ocr_to_document(self, content: Dict[str, Any]) -> Document:
"""Convert an OCR content item to a Document."""
        text = content.get("text", "")
        metadata: Dict[str, Any] = {
            "type": "ocr",
            "app_name": content.get("app_name", ""),
            "window_name": content.get("window_name", ""),
            "timestamp": content.get("timestamp", ""),
        }
        if content.get("file_path"):
            metadata["file_path"] = content["file_path"]
        if content.get("browser_url"):
            metadata["browser_url"] = content["browser_url"]
        return Document(text=text, metadata=metadata)

    def_audio_to_document(self, content: Dict[str, Any]) -> Document:
"""Convert an Audio content item to a Document."""
        text = content.get("transcription", "")
        metadata: Dict[str, Any] = {
            "type": "audio",
            "device_name": content.get("device_name", ""),
            "device_type": content.get("device_type", ""),
            "timestamp": content.get("timestamp", ""),
        }
        if content.get("file_path"):
            metadata["file_path"] = content["file_path"]
        speaker = content.get("speaker")
        if speaker:
            metadata["speaker_id"] = speaker.get("id")
            metadata["speaker_name"] = speaker.get("name")
        return Document(text=text, metadata=metadata)

    def_ui_to_document(self, content: Dict[str, Any]) -> Document:
"""Convert a UI content item to a Document."""
        text = content.get("text", "")
        metadata: Dict[str, Any] = {
            "type": "ui",
            "app_name": content.get("app_name", ""),
            "window_name": content.get("window_name", ""),
            "timestamp": content.get("timestamp", ""),
        }
        if content.get("browser_url"):
            metadata["browser_url"] = content["browser_url"]
        return Document(text=text, metadata=metadata)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/screenpipe/#llama_index.readers.screenpipe.ScreenpipeReader.load_data "Permanent link")

```
load_data(
    content_type:  = "all",
    query: Optional[] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    app_name: Optional[] = None,
    window_name: Optional[] = None,
    limit:  = 20,
) -> []

```

Load data from Screenpipe.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `content_type`  |  Type of content to retrieve. One of `"all"`, `"ocr"`, `"audio"`, `"ui"`, `"audio+ui"`, `"ocr+ui"`, `"audio+ocr"`.  |  `'all'`  |  
|  `query`  |  `Optional[str]`  |  Optional search query for semantic filtering.  |  `None`  |  
|  `start_time`  |  `Optional[datetime]`  |  Filter results after this timestamp.  |  `None`  |  
|  `end_time`  |  `Optional[datetime]`  |  Filter results before this timestamp.  |  `None`  |  
|  `app_name`  |  `Optional[str]`  |  Filter by application name.  |  `None`  |  
|  `window_name`  |  `Optional[str]`  |  Filter by window name.  |  `None`  |  
|  `limit`  |  Maximum number of results to return.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-screenpipe/llama_index/readers/screenpipe/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    content_type: str = "all",
    query: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    app_name: Optional[str] = None,
    window_name: Optional[str] = None,
    limit: int = 20,
) -> List[Document]:
"""
    Load data from Screenpipe.

    Args:
        content_type: Type of content to retrieve.
            One of ``"all"``, ``"ocr"``, ``"audio"``, ``"ui"``,
            ``"audio+ui"``, ``"ocr+ui"``, ``"audio+ocr"``.
        query: Optional search query for semantic filtering.
        start_time: Filter results after this timestamp.
        end_time: Filter results before this timestamp.
        app_name: Filter by application name.
        window_name: Filter by window name.
        limit: Maximum number of results to return.

    Returns:
        List of documents.

    """
    if content_type not in VALID_CONTENT_TYPES:
        raise ValueError(
            f"Invalid content_type '{content_type}'. "
            f"Must be one of: {sorted(VALID_CONTENT_TYPES)}"
        )

    params: Dict[str, Any] = {
        "content_type": content_type,
        "limit": limit,
    }
    if query is not None:
        params["q"] = query
    if start_time is not None:
        params["start_time"] = self._to_utc_isoformat(start_time)
    if end_time is not None:
        params["end_time"] = self._to_utc_isoformat(end_time)
    if app_name is not None:
        params["app_name"] = app_name
    if window_name is not None:
        params["window_name"] = window_name

    all_items: List[Dict[str, Any]] = []
    offset = 0

    while True:
        params["offset"] = offset
        data = self._search(params)
        items = data.get("data", [])
        if not items:
            break
        all_items.extend(items)
        if len(all_items) >= limit:
            all_items = all_items[:limit]
            break
        pagination = data.get("pagination", {})
        total = pagination.get("total", 0)
        offset += len(items)
        if offset >= total:
            break

    documents = []
    for item in all_items:
        doc = self._item_to_document(item)
        if doc is not None:
            documents.append(doc)

    return documents

```
 |  
| --- | --- |  
options: members: - ScreenpipeReader
