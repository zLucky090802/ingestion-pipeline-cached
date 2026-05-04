# Notion
##  NotionPageReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/notion/#llama_index.readers.notion.NotionPageReader "Permanent link")
Bases: 
Notion Page reader.
Reads a set of Notion pages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `integration_token`  |  Notion integration token.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-notion/llama_index/readers/notion/base.py`  
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
```
 | 
```
classNotionPageReader(BasePydanticReader):
"""
    Notion Page reader.

    Reads a set of Notion pages.

    Args:
        integration_token (str): Notion integration token.

    """

    is_remote: bool = True
    token: str
    headers: Dict[str, str]

    def__init__(self, integration_token: Optional[str] = None) -> None:
"""Initialize with parameters."""
        if integration_token is None:
            integration_token = os.getenv(INTEGRATION_TOKEN_NAME)
            if integration_token is None:
                raise ValueError(
                    "Must specify `integration_token` or set environment "
                    "variable `NOTION_INTEGRATION_TOKEN`."
                )

        token = integration_token
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        super().__init__(token=token, headers=headers)

    @classmethod
    defclass_name(cls) -> str:
"""Get the name identifier of the class."""
        return "NotionPageReader"

    def_read_block(self, block_id: str, num_tabs: int = 0) -> str:
"""Read a block."""
        done = False
        result_lines_arr = []
        cur_block_id = block_id
        while not done:
            block_url = BLOCK_CHILD_URL_TMPL.format(block_id=cur_block_id)
            query_dict: Dict[str, Any] = {}

            res = self._request_with_retry(
                "GET", block_url, headers=self.headers, json=query_dict
            )
            data = res.json()

            for result in data["results"]:
                result_type = result["type"]
                result_obj = result[result_type]

                cur_result_text_arr = []
                if "rich_text" in result_obj:
                    for rich_text in result_obj["rich_text"]:
                        # skip if doesn't have text object
                        if "text" in rich_text:
                            text = rich_text["text"]["content"]
                            prefix = "\t" * num_tabs
                            cur_result_text_arr.append(prefix + text)

                result_block_id = result["id"]
                has_children = result["has_children"]
                if has_children:
                    children_text = self._read_block(
                        result_block_id, num_tabs=num_tabs + 1
                    )
                    cur_result_text_arr.append(children_text)

                cur_result_text = "\n".join(cur_result_text_arr)
                result_lines_arr.append(cur_result_text)

            if data["next_cursor"] is None:
                done = True
                break
            else:
                cur_block_id = data["next_cursor"]

        return "\n".join(result_lines_arr)

    def_request_with_retry(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        json: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
"""Make a request with retry and rate limit handling."""
        max_retries = 5
        backoff_factor = 1

        for attempt in range(max_retries):
            try:
                response = requests.request(method, url, headers=headers, json=json)
                response.raise_for_status()
                return response
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

    defread_page(self, page_id: str) -> str:
"""Read a page."""
        return self._read_block(page_id)

    defquery_database(
        self, database_id: str, query_dict: Dict[str, Any] = {"page_size": 100}
    ) -> List[str]:
"""Get all the pages from a Notion database."""
        pages = []

        res = self._request_with_retry(
            "POST",
            DATABASE_URL_TMPL.format(database_id=database_id),
            headers=self.headers,
            json=query_dict,
        )
        res.raise_for_status()
        data = res.json()

        pages.extend(data.get("results"))

        while data.get("has_more"):
            query_dict["start_cursor"] = data.get("next_cursor")
            res = self._request_with_retry(
                "POST",
                DATABASE_URL_TMPL.format(database_id=database_id),
                headers=self.headers,
                json=query_dict,
            )
            res.raise_for_status()
            data = res.json()
            pages.extend(data.get("results"))

        return [page["id"] for page in pages]

    defsearch(self, query: str) -> List[str]:
"""Search Notion page given a text query."""
        done = False
        next_cursor: Optional[str] = None
        page_ids = []
        while not done:
            query_dict = {
                "query": query,
            }
            if next_cursor is not None:
                query_dict["start_cursor"] = next_cursor
            res = self._request_with_retry(
                "POST", SEARCH_URL, headers=self.headers, json=query_dict
            )
            data = res.json()
            for result in data["results"]:
                page_id = result["id"]
                page_ids.append(page_id)

            if data["next_cursor"] is None:
                done = True
                break
            else:
                next_cursor = data["next_cursor"]
        return page_ids

    defload_data(
        self,
        page_ids: List[str] = [],
        database_ids: Optional[List[str]] = None,
        load_all_if_empty: bool = False,
    ) -> List[Document]:
"""
        Load data from the input directory.

        Args:
            page_ids (List[str]): List of page ids to load.
            database_ids Optional (List[str]): List database ids from which to load page ids.
            load_all_if_empty (bool): If True, load all pages and dbs if no page_ids or database_ids are provided.

        Returns:
            List[Document]: List of documents.

        """
        if not page_ids and not database_ids:
            if not load_all_if_empty:
                raise ValueError(
                    "Must specify either `page_ids` or `database_ids` if "
                    "`load_all_if_empty` is False."
                )
            else:
                database_ids = self.list_databases()
                page_ids = self.list_pages()

        docs = []
        all_page_ids = set(page_ids) if page_ids is not None else set()
        # TODO: in the future add special logic for database_ids
        if database_ids is not None:
            for database_id in database_ids:
                # get all the pages in the database
                db_page_ids = self.query_database(database_id)
                all_page_ids.update(db_page_ids)

        for page_id in all_page_ids:
            page_text = self.read_page(page_id)
            docs.append(
                Document(text=page_text, id_=page_id, extra_info={"page_id": page_id})
            )

        return docs

    deflist_databases(self) -> List[str]:
"""List all databases in the Notion workspace."""
        query_dict = {"filter": {"property": "object", "value": "database"}}
        res = self._request_with_retry(
            "POST", SEARCH_URL, headers=self.headers, json=query_dict
        )
        res.raise_for_status()
        data = res.json()
        return [db["id"] for db in data["results"]]

    deflist_pages(self) -> List[str]:
"""List all pages in the Notion workspace."""
        query_dict = {"filter": {"property": "object", "value": "page"}}
        res = self._request_with_retry(
            "POST", SEARCH_URL, headers=self.headers, json=query_dict
        )
        res.raise_for_status()
        data = res.json()
        return [page["id"] for page in data["results"]]

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/notion/#llama_index.readers.notion.NotionPageReader.class_name "Permanent link")

```
class_name() -> 

```

Get the name identifier of the class.
Source code in `llama-index-integrations/readers/llama-index-readers-notion/llama_index/readers/notion/base.py`  
| 
```
52
53
54
55
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get the name identifier of the class."""
    return "NotionPageReader"

```
 |  
| --- | --- |  
###  read_page [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/notion/#llama_index.readers.notion.NotionPageReader.read_page "Permanent link")

```
read_page(page_id: ) -> 

```

Read a page.
Source code in `llama-index-integrations/readers/llama-index-readers-notion/llama_index/readers/notion/base.py`  
| 
```
132
133
134
```
 | 
```
defread_page(self, page_id: str) -> str:
"""Read a page."""
    return self._read_block(page_id)

```
 |  
| --- | --- |  
###  query_database [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/notion/#llama_index.readers.notion.NotionPageReader.query_database "Permanent link")

```
query_database(
    database_id: ,
    query_dict: [, ] = {"page_size": 100},
) -> []

```

Get all the pages from a Notion database.
Source code in `llama-index-integrations/readers/llama-index-readers-notion/llama_index/readers/notion/base.py`  
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
```
 | 
```
defquery_database(
    self, database_id: str, query_dict: Dict[str, Any] = {"page_size": 100}
) -> List[str]:
"""Get all the pages from a Notion database."""
    pages = []

    res = self._request_with_retry(
        "POST",
        DATABASE_URL_TMPL.format(database_id=database_id),
        headers=self.headers,
        json=query_dict,
    )
    res.raise_for_status()
    data = res.json()

    pages.extend(data.get("results"))

    while data.get("has_more"):
        query_dict["start_cursor"] = data.get("next_cursor")
        res = self._request_with_retry(
            "POST",
            DATABASE_URL_TMPL.format(database_id=database_id),
            headers=self.headers,
            json=query_dict,
        )
        res.raise_for_status()
        data = res.json()
        pages.extend(data.get("results"))

    return [page["id"] for page in pages]

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/notion/#llama_index.readers.notion.NotionPageReader.search "Permanent link")

```
search(query: ) -> []

```

Search Notion page given a text query.
Source code in `llama-index-integrations/readers/llama-index-readers-notion/llama_index/readers/notion/base.py`  
| 
```
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
```
 | 
```
defsearch(self, query: str) -> List[str]:
"""Search Notion page given a text query."""
    done = False
    next_cursor: Optional[str] = None
    page_ids = []
    while not done:
        query_dict = {
            "query": query,
        }
        if next_cursor is not None:
            query_dict["start_cursor"] = next_cursor
        res = self._request_with_retry(
            "POST", SEARCH_URL, headers=self.headers, json=query_dict
        )
        data = res.json()
        for result in data["results"]:
            page_id = result["id"]
            page_ids.append(page_id)

        if data["next_cursor"] is None:
            done = True
            break
        else:
            next_cursor = data["next_cursor"]
    return page_ids

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/notion/#llama_index.readers.notion.NotionPageReader.load_data "Permanent link")

```
load_data(
    page_ids: [] = [],
    database_ids: Optional[[]] = None,
    load_all_if_empty:  = False,
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `page_ids`  |  `List[str]`  |  List of page ids to load.  |  
|  `database_ids Optional`  |  `List[str]`  |  List database ids from which to load page ids.  |  _required_  |  
|  `load_all_if_empty`  |  `bool`  |  If True, load all pages and dbs if no page_ids or database_ids are provided.  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-notion/llama_index/readers/notion/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    page_ids: List[str] = [],
    database_ids: Optional[List[str]] = None,
    load_all_if_empty: bool = False,
) -> List[Document]:
"""
    Load data from the input directory.

    Args:
        page_ids (List[str]): List of page ids to load.
        database_ids Optional (List[str]): List database ids from which to load page ids.
        load_all_if_empty (bool): If True, load all pages and dbs if no page_ids or database_ids are provided.

    Returns:
        List[Document]: List of documents.

    """
    if not page_ids and not database_ids:
        if not load_all_if_empty:
            raise ValueError(
                "Must specify either `page_ids` or `database_ids` if "
                "`load_all_if_empty` is False."
            )
        else:
            database_ids = self.list_databases()
            page_ids = self.list_pages()

    docs = []
    all_page_ids = set(page_ids) if page_ids is not None else set()
    # TODO: in the future add special logic for database_ids
    if database_ids is not None:
        for database_id in database_ids:
            # get all the pages in the database
            db_page_ids = self.query_database(database_id)
            all_page_ids.update(db_page_ids)

    for page_id in all_page_ids:
        page_text = self.read_page(page_id)
        docs.append(
            Document(text=page_text, id_=page_id, extra_info={"page_id": page_id})
        )

    return docs

```
 |  
| --- | --- |  
###  list_databases [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/notion/#llama_index.readers.notion.NotionPageReader.list_databases "Permanent link")

```
list_databases() -> []

```

List all databases in the Notion workspace.
Source code in `llama-index-integrations/readers/llama-index-readers-notion/llama_index/readers/notion/base.py`  
| 
```
238
239
240
241
242
243
244
245
246
```
 | 
```
deflist_databases(self) -> List[str]:
"""List all databases in the Notion workspace."""
    query_dict = {"filter": {"property": "object", "value": "database"}}
    res = self._request_with_retry(
        "POST", SEARCH_URL, headers=self.headers, json=query_dict
    )
    res.raise_for_status()
    data = res.json()
    return [db["id"] for db in data["results"]]

```
 |  
| --- | --- |  
###  list_pages [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/notion/#llama_index.readers.notion.NotionPageReader.list_pages "Permanent link")

```
list_pages() -> []

```

List all pages in the Notion workspace.
Source code in `llama-index-integrations/readers/llama-index-readers-notion/llama_index/readers/notion/base.py`  
| 
```
248
249
250
251
252
253
254
255
256
```
 | 
```
deflist_pages(self) -> List[str]:
"""List all pages in the Notion workspace."""
    query_dict = {"filter": {"property": "object", "value": "page"}}
    res = self._request_with_retry(
        "POST", SEARCH_URL, headers=self.headers, json=query_dict
    )
    res.raise_for_status()
    data = res.json()
    return [page["id"] for page in data["results"]]

```
 |  
| --- | --- |  
options: members: - NotionPageReader
