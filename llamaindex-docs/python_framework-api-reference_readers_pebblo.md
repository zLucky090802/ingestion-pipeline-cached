# Pebblo
##  PebbloSafeReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pebblo/#llama_index.readers.pebblo.PebbloSafeReader "Permanent link")
Bases: 
Pebblo Safe Loader class is a wrapper around document loaders enabling the data to be scrutinized.
Source code in `llama-index-integrations/readers/llama-index-readers-pebblo/llama_index/readers/pebblo/base.py`  
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
```
 | 
```
classPebbloSafeReader(BaseReader):
"""
    Pebblo Safe Loader class is a wrapper around document loaders enabling the data
    to be scrutinized.
    """

    _discover_sent: bool = False
    _loader_sent: bool = False

    def__init__(
        self,
        llama_reader: BaseReader,
        name: str,
        owner: str = "",
        description: str = "",
    ):
        if not name or not isinstance(name, str):
            raise NameError("Must specify a valid name.")
        self.app_name = name
        self.load_id = str(uuid.uuid4())
        self.reader = llama_reader
        self.owner = owner
        self.description = description
        self.reader_name = str(type(self.reader)).split(".")[-1].split("'")[0]
        self.source_type = get_reader_type(self.reader_name)
        self.docs: List[Document] = []
        self.source_aggr_size = 0
        # generate app
        self.app = self._get_app_details()
        self._send_discover()

    defload_data(self, **kwargs) -> List[Document]:
"""
        Load Documents.

        Returns:
            list: Documents fetched from load method of the wrapped `reader`.

        """
        self.docs = self.reader.load_data(**kwargs)
        self._send_reader_doc(loading_end=True, **kwargs)
        return self.docs

    @classmethod
    defset_discover_sent(cls) -> None:
        cls._discover_sent = True

    @classmethod
    defset_reader_sent(cls) -> None:
        cls._reader_sent = True

    def_set_reader_details(self, **kwargs) -> None:
        self.source_path = get_reader_full_path(self.reader, self.reader_name, **kwargs)
        self.source_owner = PebbloSafeReader.get_file_owner_from_path(self.source_path)
        self.source_path_size = self.get_source_size(self.source_path)
        self.reader_details = {
            "loader": self.reader_name,
            "source_path": self.source_path,
            "source_type": self.source_type,
            **(
                {"source_path_size": str(self.source_path_size)}
                if self.source_path_size  0
                else {}
            ),
        }

    def_send_reader_doc(self, loading_end: bool = False, **kwargs) -> None:
"""
        Send documents fetched from reader to pebblo-server. Internal method.

        Args:
            loading_end (bool, optional): Flag indicating the halt of data
                                        loading by reader. Defaults to False.

        """
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        docs = []
        self._set_reader_details(**kwargs)
        for doc in self.docs:
            page_content = str(doc.get_content(metadata_mode=MetadataMode.NONE))
            page_content_size = self.calculate_content_size(page_content)
            self.source_aggr_size += page_content_size
            docs.append(
                {
                    "doc": page_content,
                    "source_path": self.source_path,
                    "last_modified": doc.metadata.get("last_modified", None),
                    "file_owner": self.source_owner,
                    **(
                        {"source_path_size": self.source_path_size}
                        if self.source_path_size is not None
                        else {}
                    ),
                }
            )
        payload: Dict[str, Any] = {
            "name": self.app_name,
            "owner": self.owner,
            "docs": docs,
            "plugin_version": PLUGIN_VERSION,
            "load_id": self.load_id,
            "loader_details": self.reader_details,
            "loading_end": "false",
            "source_owner": self.source_owner,
        }
        if loading_end is True:
            payload["loading_end"] = "true"
            if "loader_details" in payload:
                payload["loader_details"]["source_aggr_size"] = self.source_aggr_size
        payload = Doc(**payload).dict(exclude_unset=True)
        load_doc_url = f"{CLASSIFIER_URL}/v1/loader/doc"
        try:
            resp = requests.post(
                load_doc_url, headers=headers, json=payload, timeout=20
            )
            if resp.status_code not in [HTTPStatus.OK, HTTPStatus.BAD_GATEWAY]:
                logger.warning(
                    f"Received unexpected HTTP response code: {resp.status_code}"
                )
            logger.debug(
                f"send_loader_doc: request \
{resp.request.url}, \
                    body {str(resp.request.body)[:999]}\
{len(resp.request.bodyifresp.request.bodyelse[])}\
                    response status{resp.status_code} body {resp.json()}"
            )
        except requests.exceptions.RequestException:
            logger.warning("Unable to reach pebblo server.")
        except Exception:
            logger.warning("An Exception caught in _send_loader_doc.")
        if loading_end is True:
            PebbloSafeReader.set_reader_sent()

    @staticmethod
    defcalculate_content_size(page_content: str) -> int:
"""
        Calculate the content size in bytes:
        - Encode the string to bytes using a specific encoding (e.g., UTF-8)
        - Get the length of the encoded bytes.

        Args:
            page_content (str): Data string.

        Returns:
            int: Size of string in bytes.

        """
        # Encode the content to bytes using UTF-8
        encoded_content = page_content.encode("utf-8")
        return len(encoded_content)

    def_send_discover(self) -> None:
"""Send app discovery payload to pebblo-server. Internal method."""
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        payload = self.app.dict(exclude_unset=True)
        app_discover_url = f"{CLASSIFIER_URL}/v1/app/discover"
        try:
            resp = requests.post(
                app_discover_url, headers=headers, json=payload, timeout=20
            )
            logger.debug(
                f"send_discover: request \
{resp.request.url}, \
                    headers {resp.request.headers}, \
                    body {str(resp.request.body)[:999]}\
{len(resp.request.bodyifresp.request.bodyelse[])}\
                    response status{resp.status_code} body {resp.json()}"
            )
            if resp.status_code in [HTTPStatus.OK, HTTPStatus.BAD_GATEWAY]:
                PebbloSafeReader.set_discover_sent()
            else:
                logger.warning(
                    f"Received unexpected HTTP response code: {resp.status_code}"
                )
        except requests.exceptions.RequestException:
            logger.warning("Unable to reach pebblo server.")
        except Exception:
            logger.warning("An Exception caught in _send_discover.")

    def_get_app_details(self) -> App:
"""
        Fetch app details. Internal method.

        Returns:
            App: App details.

        """
        framework, runtime = get_runtime()
        return App(
            name=self.app_name,
            owner=self.owner,
            description=self.description,
            load_id=self.load_id,
            runtime=runtime,
            framework=framework,
            plugin_version=PLUGIN_VERSION,
        )

    @staticmethod
    defget_file_owner_from_path(file_path: str) -> str:
"""
        Fetch owner of local file path.

        Args:
            file_path (str): Local file path.

        Returns:
            str: Name of owner.

        """
        try:
            importpwd

            file_owner_uid = os.stat(file_path).st_uid
            file_owner_name = pwd.getpwuid(file_owner_uid).pw_name
        except Exception:
            file_owner_name = "unknown"
        return file_owner_name

    defget_source_size(self, source_path: str) -> int:
"""
        Fetch size of source path. Source can be a directory or a file.

        Args:
            source_path (str): Local path of data source.

        Returns:
            int: Source size in bytes.

        """
        if not source_path:
            return 0
        size = 0
        if os.path.isfile(source_path):
            size = os.path.getsize(source_path)
        elif os.path.isdir(source_path):
            total_size = 0
            for dirpath, _, filenames in os.walk(source_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
            size = total_size
        return size

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pebblo/#llama_index.readers.pebblo.PebbloSafeReader.load_data "Permanent link")

```
load_data(**kwargs) -> []

```

Load Documents.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `list`  |   |  Documents fetched from load method of the wrapped `reader`.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-pebblo/llama_index/readers/pebblo/base.py`  
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
```
 | 
```
defload_data(self, **kwargs) -> List[Document]:
"""
    Load Documents.

    Returns:
        list: Documents fetched from load method of the wrapped `reader`.

    """
    self.docs = self.reader.load_data(**kwargs)
    self._send_reader_doc(loading_end=True, **kwargs)
    return self.docs

```
 |  
| --- | --- |  
###  calculate_content_size `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pebblo/#llama_index.readers.pebblo.PebbloSafeReader.calculate_content_size "Permanent link")

```
calculate_content_size(page_content: ) -> 

```

Calculate the content size in bytes: - Encode the string to bytes using a specific encoding (e.g., UTF-8) - Get the length of the encoded bytes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `page_content`  |  Data string.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `int`  |  Size of string in bytes.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-pebblo/llama_index/readers/pebblo/base.py`  
| 
```
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
```
 | 
```
@staticmethod
defcalculate_content_size(page_content: str) -> int:
"""
    Calculate the content size in bytes:
    - Encode the string to bytes using a specific encoding (e.g., UTF-8)
    - Get the length of the encoded bytes.

    Args:
        page_content (str): Data string.

    Returns:
        int: Size of string in bytes.

    """
    # Encode the content to bytes using UTF-8
    encoded_content = page_content.encode("utf-8")
    return len(encoded_content)

```
 |  
| --- | --- |  
###  get_file_owner_from_path `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pebblo/#llama_index.readers.pebblo.PebbloSafeReader.get_file_owner_from_path "Permanent link")

```
get_file_owner_from_path(file_path: ) -> 

```

Fetch owner of local file path.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_path`  |  Local file path.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Name of owner.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-pebblo/llama_index/readers/pebblo/base.py`  
| 
```
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
```
 | 
```
@staticmethod
defget_file_owner_from_path(file_path: str) -> str:
"""
    Fetch owner of local file path.

    Args:
        file_path (str): Local file path.

    Returns:
        str: Name of owner.

    """
    try:
        importpwd

        file_owner_uid = os.stat(file_path).st_uid
        file_owner_name = pwd.getpwuid(file_owner_uid).pw_name
    except Exception:
        file_owner_name = "unknown"
    return file_owner_name

```
 |  
| --- | --- |  
###  get_source_size [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pebblo/#llama_index.readers.pebblo.PebbloSafeReader.get_source_size "Permanent link")

```
get_source_size(source_path: ) -> 

```

Fetch size of source path. Source can be a directory or a file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `source_path`  |  Local path of data source.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `int`  |  Source size in bytes.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-pebblo/llama_index/readers/pebblo/base.py`  
| 
```
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
```
 | 
```
defget_source_size(self, source_path: str) -> int:
"""
    Fetch size of source path. Source can be a directory or a file.

    Args:
        source_path (str): Local path of data source.

    Returns:
        int: Source size in bytes.

    """
    if not source_path:
        return 0
    size = 0
    if os.path.isfile(source_path):
        size = os.path.getsize(source_path)
    elif os.path.isdir(source_path):
        total_size = 0
        for dirpath, _, filenames in os.walk(source_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        size = total_size
    return size

```
 |  
| --- | --- |  
options: members: - PebbloReader
