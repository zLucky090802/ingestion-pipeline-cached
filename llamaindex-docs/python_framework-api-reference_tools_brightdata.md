# Brightdata
##  BrightDataToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/brightdata/#llama_index.tools.brightdata.BrightDataToolSpec "Permanent link")
Bases: 
Bright Data tool spec for web scraping and search capabilities.
Source code in `llama-index-integrations/tools/llama-index-tools-brightdata/llama_index/tools/brightdata/base.py`  
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
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
```
 | 
```
classBrightDataToolSpec(BaseToolSpec):
"""Bright Data tool spec for web scraping and search capabilities."""

    spec_functions = [
        "scrape_as_markdown",
        "get_screenshot",
        "search_engine",
        "web_data_feed",
    ]

    def__init__(
        self,
        api_key: str,
        zone: str = "unblocker",
        verbose: bool = False,
    ) -> None:
"""
        Initialize with API token and default zone.

        Args:
            api_key (str): Your Bright Data API token
            zone (str): Bright Data zone name
            verbose (bool): Print additional information about requests

        """
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        self._api_key = api_key
        self._zone = zone
        self._verbose = verbose
        self._endpoint = "https://api.brightdata.com/request"

    def_make_request(self, payload: Dict) -> str:
"""
        Make a request to Bright Data API.

        Args:
            payload (Dict): Request payload

        Returns:
            str: Response text

        """
        importrequests
        importjson

        if self._verbose:
            print(f"[Bright Data] Request: {payload['url']}")

        response = requests.post(
            self._endpoint, headers=self._headers, data=json.dumps(payload)
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to scrape: {response.status_code}{response.text}"
            )

        return response.text

    defscrape_as_markdown(self, url: str, zone: Optional[str] = None) -> Document:
"""
        Scrape a webpage and return content in Markdown format.

        Args:
            url (str): URL to scrape
            zone (Optional[str]): Override default zone

        Returns:
            Document: Scraped content as Markdown

        """
        payload = {
            "url": url,
            "zone": zone or self._zone,
            "format": "raw",
            "data_format": "markdown",
        }

        content = self._make_request(payload)
        return Document(text=content, metadata={"url": url})

    defget_screenshot(
        self, url: str, output_path: str, zone: Optional[str] = None
    ) -> str:
"""
        Take a screenshot of a webpage.

        Args:
            url (str): URL to screenshot
            output_path (str): Path to save the screenshot
            zone (Optional[str]): Override default zone

        Returns:
            str: Path to saved screenshot

        """
        importrequests
        importjson

        payload = {
            "url": url,
            "zone": zone or self._zone,
            "format": "raw",
            "data_format": "screenshot",
        }

        response = requests.post(
            self._endpoint, headers=self._headers, data=json.dumps(payload)
        )

        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")

        with open(output_path, "wb") as f:
            f.write(response.content)

        return output_path

    defsearch_engine(
        self,
        query: str,
        engine: str = "google",
        zone: Optional[str] = None,
        language: Optional[str] = None,  # hl parameter, e.g., "en"
        country_code: Optional[str] = None,  # gl parameter, e.g., "us"
        search_type: Optional[
            str
        ] = None,  # tbm parameter (images, shopping, news, etc.)
        start: Optional[int] = None,  # pagination start index
        num_results: Optional[int] = 10,  # number of results to return
        location: Optional[str] = None,  # uule parameter for geo-location
        device: Optional[str] = None,  # device type for user-agent
        return_json: bool = False,  # parse results as JSON
        hotel_dates: Optional[str] = None,  # check-in and check-out dates
        hotel_occupancy: Optional[int] = None,  # number of guests
    ) -> Document:
"""
        Search using Google, Bing, or Yandex with advanced parameters and return results in Markdown.

        Args:
            query (str): Search query
            engine (str): Search engine - 'google', 'bing', or 'yandex'
            zone (Optional[str]): Override default zone

            # Google SERP specific parameters
            language (Optional[str]): Two-letter language code (hl parameter)
            country_code (Optional[str]): Two-letter country code (gl parameter)
            search_type (Optional[str]): Type of search (images, shopping, news, etc.)
            start (Optional[int]): Results pagination offset (0=first page, 10=second page)
            num_results (Optional[int]): Number of results to return (default 10)
            location (Optional[str]): Location for search results (uule parameter)
            device (Optional[str]): Device type (mobile, ios, android, ipad, android_tablet)
            return_json (bool): Return parsed JSON instead of HTML/Markdown

            # Hotel search parameters
            hotel_dates (Optional[str]): Check-in and check-out dates (format: YYYY-MM-DD,YYYY-MM-DD)
            hotel_occupancy (Optional[int]): Number of guests (1-4)

        Returns:
            Document: Search results as Markdown or JSON

        """
        encoded_query = self._encode_query(query)

        base_urls = {
            "google": f"https://www.google.com/search?q={encoded_query}",
            "bing": f"https://www.bing.com/search?q={encoded_query}",
            "yandex": f"https://yandex.com/search/?text={encoded_query}",
        }

        if engine not in base_urls:
            raise ValueError(
                f"Unsupported search engine: {engine}. Use 'google', 'bing', or 'yandex'"
            )

        search_url = base_urls[engine]

        if engine == "google":
            params = []

            if language:
                params.append(f"hl={language}")

            if country_code:
                params.append(f"gl={country_code}")

            if search_type:
                if search_type == "jobs":
                    params.append("ibp=htl;jobs")
                else:
                    search_types = {"images": "isch", "shopping": "shop", "news": "nws"}
                    tbm_value = search_types.get(search_type, search_type)
                    params.append(f"tbm={tbm_value}")

            if start is not None:
                params.append(f"start={start}")

            if num_results:
                params.append(f"num={num_results}")

            if location:
                params.append(f"uule={self._encode_query(location)}")

            if device:
                device_value = "1"

                if device in ["ios", "iphone"]:
                    device_value = "ios"
                elif device == "ipad":
                    device_value = "ios_tablet"
                elif device == "android":
                    device_value = "android"
                elif device == "android_tablet":
                    device_value = "android_tablet"

                params.append(f"brd_mobile={device_value}")

            if return_json:
                params.append("brd_json=1")

            if hotel_dates:
                params.append(f"hotel_dates={self._encode_query(hotel_dates)}")

            if hotel_occupancy:
                params.append(f"hotel_occupancy={hotel_occupancy}")

            if params:
                search_url += "&" + "&".join(params)

        payload = {
            "url": search_url,
            "zone": zone or self._zone,
            "format": "raw",
            "data_format": "markdown" if not return_json else "raw",
        }

        content = self._make_request(payload)
        return Document(
            text=content, metadata={"query": query, "engine": engine, "url": search_url}
        )

    defweb_data_feed(
        self,
        source_type: str,
        url: str,
        num_of_reviews: Optional[int] = None,
        timeout: int = 600,
        polling_interval: int = 1,
    ) -> Dict:
"""
        Retrieve structured web data from various sources like LinkedIn, Amazon, Instagram, etc.

        Args:
            source_type (str): Type of data source (e.g., 'linkedin_person_profile', 'amazon_product')
            url (str): URL of the web resource to retrieve data from
            num_of_reviews (Optional[int]): Number of reviews to retrieve (only for facebook_company_reviews)
            timeout (int): Maximum time in seconds to wait for data retrieval
            polling_interval (int): Time in seconds between polling attempts

        Returns:
            Dict: Structured data from the requested source

        """
        importrequests
        importtime

        datasets = {
            "amazon_product": "gd_l7q7dkf244hwjntr0",
            "amazon_product_reviews": "gd_le8e811kzy4ggddlq",
            "linkedin_person_profile": "gd_l1viktl72bvl7bjuj0",
            "linkedin_company_profile": "gd_l1vikfnt1wgvvqz95w",
            "zoominfo_company_profile": "gd_m0ci4a4ivx3j5l6nx",
            "instagram_profiles": "gd_l1vikfch901nx3by4",
            "instagram_posts": "gd_lk5ns7kz21pck8jpis",
            "instagram_reels": "gd_lyclm20il4r5helnj",
            "instagram_comments": "gd_ltppn085pokosxh13",
            "facebook_posts": "gd_lyclm1571iy3mv57zw",
            "facebook_marketplace_listings": "gd_lvt9iwuh6fbcwmx1a",
            "facebook_company_reviews": "gd_m0dtqpiu1mbcyc2g86",
            "x_posts": "gd_lwxkxvnf1cynvib9co",
            "zillow_properties_listing": "gd_lfqkr8wm13ixtbd8f5",
            "booking_hotel_listings": "gd_m5mbdl081229ln6t4a",
            "youtube_videos": "gd_m5mbdl081229ln6t4a",
        }

        if source_type not in datasets:
            valid_sources = ", ".join(datasets.keys())
            raise ValueError(
                f"Invalid source_type: {source_type}. Valid options are: {valid_sources}"
            )

        dataset_id = datasets[source_type]

        request_data = {"url": url}
        if source_type == "facebook_company_reviews" and num_of_reviews is not None:
            request_data["num_of_reviews"] = str(num_of_reviews)

        trigger_response = requests.post(
            "https://api.brightdata.com/datasets/v3/trigger",
            params={"dataset_id": dataset_id, "include_errors": True},
            headers=self._headers,
            json=[request_data],
        )

        trigger_data = trigger_response.json()
        if not trigger_data.get("snapshot_id"):
            raise Exception("No snapshot ID returned from trigger request")

        snapshot_id = trigger_data["snapshot_id"]
        if self._verbose:
            print(
                f"[Bright Data] {source_type} triggered with snapshot ID: {snapshot_id}"
            )

        attempts = 0
        max_attempts = timeout

        while attempts  max_attempts:
            try:
                snapshot_response = requests.get(
                    f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}",
                    params={"format": "json"},
                    headers=self._headers,
                )

                snapshot_data = snapshot_response.json()

                if (
                    isinstance(snapshot_data, dict)
                    and snapshot_data.get("status") == "running"
                ):
                    if self._verbose:
                        print(
                            f"[Bright Data] Snapshot not ready, polling again (attempt {attempts+1}/{max_attempts})"
                        )
                    attempts += 1
                    time.sleep(polling_interval)
                    continue

                if self._verbose:
                    print(f"[Bright Data] Data received after {attempts+1} attempts")

                return snapshot_data

            except Exception as e:
                if self._verbose:
                    print(f"[Bright Data] Polling error: {e!s}")
                attempts += 1
                time.sleep(polling_interval)

        raise TimeoutError(
            f"Timeout after {max_attempts} seconds waiting for {source_type} data"
        )

    @staticmethod
    def_encode_query(query: str) -> str:
"""URL encode a search query."""
        fromurllib.parseimport quote

        return quote(query)

```
 |  
| --- | --- |  
###  scrape_as_markdown [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/brightdata/#llama_index.tools.brightdata.BrightDataToolSpec.scrape_as_markdown "Permanent link")

```
scrape_as_markdown(
    url: , zone: Optional[] = None
) -> 

```

Scrape a webpage and return content in Markdown format.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  URL to scrape  |  _required_  |  
|  `zone`  |  `Optional[str]`  |  Override default zone  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |   |  Scraped content as Markdown  |  
Source code in `llama-index-integrations/tools/llama-index-tools-brightdata/llama_index/tools/brightdata/base.py`  
| 
```
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
```
 | 
```
defscrape_as_markdown(self, url: str, zone: Optional[str] = None) -> Document:
"""
    Scrape a webpage and return content in Markdown format.

    Args:
        url (str): URL to scrape
        zone (Optional[str]): Override default zone

    Returns:
        Document: Scraped content as Markdown

    """
    payload = {
        "url": url,
        "zone": zone or self._zone,
        "format": "raw",
        "data_format": "markdown",
    }

    content = self._make_request(payload)
    return Document(text=content, metadata={"url": url})

```
 |  
| --- | --- |  
###  get_screenshot [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/brightdata/#llama_index.tools.brightdata.BrightDataToolSpec.get_screenshot "Permanent link")

```
get_screenshot(
    url: , output_path: , zone: Optional[] = None
) -> 

```

Take a screenshot of a webpage.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  URL to screenshot  |  _required_  |  
|  `output_path`  |  Path to save the screenshot  |  _required_  |  
|  `zone`  |  `Optional[str]`  |  Override default zone  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Path to saved screenshot  |  
Source code in `llama-index-integrations/tools/llama-index-tools-brightdata/llama_index/tools/brightdata/base.py`  
| 
```
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
```
 | 
```
defget_screenshot(
    self, url: str, output_path: str, zone: Optional[str] = None
) -> str:
"""
    Take a screenshot of a webpage.

    Args:
        url (str): URL to screenshot
        output_path (str): Path to save the screenshot
        zone (Optional[str]): Override default zone

    Returns:
        str: Path to saved screenshot

    """
    importrequests
    importjson

    payload = {
        "url": url,
        "zone": zone or self._zone,
        "format": "raw",
        "data_format": "screenshot",
    }

    response = requests.post(
        self._endpoint, headers=self._headers, data=json.dumps(payload)
    )

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

```
 |  
| --- | --- |  
###  search_engine [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/brightdata/#llama_index.tools.brightdata.BrightDataToolSpec.search_engine "Permanent link")

```
search_engine(
    query: ,
    engine:  = "google",
    zone: Optional[] = None,
    language: Optional[] = None,
    country_code: Optional[] = None,
    search_type: Optional[] = None,
    start: Optional[] = None,
    num_results: Optional[] = 10,
    location: Optional[] = None,
    device: Optional[] = None,
    return_json:  = False,
    hotel_dates: Optional[] = None,
    hotel_occupancy: Optional[] = None,
) -> 

```

Search using Google, Bing, or Yandex with advanced parameters and return results in Markdown.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Search query  |  _required_  |  
|  `engine`  |  Search engine - 'google', 'bing', or 'yandex'  |  `'google'`  |  
|  `zone`  |  `Optional[str]`  |  Override default zone  |  `None`  |  
|  `language`  |  `Optional[str]`  |  Two-letter language code (hl parameter)  |  `None`  |  
|  `country_code`  |  `Optional[str]`  |  Two-letter country code (gl parameter)  |  `None`  |  
|  `search_type`  |  `Optional[str]`  |  Type of search (images, shopping, news, etc.)  |  `None`  |  
|  `start`  |  `Optional[int]`  |  Results pagination offset (0=first page, 10=second page)  |  `None`  |  
|  `num_results`  |  `Optional[int]`  |  Number of results to return (default 10)  |  
|  `location`  |  `Optional[str]`  |  Location for search results (uule parameter)  |  `None`  |  
|  `device`  |  `Optional[str]`  |  Device type (mobile, ios, android, ipad, android_tablet)  |  `None`  |  
|  `return_json`  |  `bool`  |  Return parsed JSON instead of HTML/Markdown  |  `False`  |  
|  `hotel_dates`  |  `Optional[str]`  |  Check-in and check-out dates (format: YYYY-MM-DD,YYYY-MM-DD)  |  `None`  |  
|  `hotel_occupancy`  |  `Optional[int]`  |  Number of guests (1-4)  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |   |  Search results as Markdown or JSON  |  
Source code in `llama-index-integrations/tools/llama-index-tools-brightdata/llama_index/tools/brightdata/base.py`  
| 
```
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
```
 | 
```
defsearch_engine(
    self,
    query: str,
    engine: str = "google",
    zone: Optional[str] = None,
    language: Optional[str] = None,  # hl parameter, e.g., "en"
    country_code: Optional[str] = None,  # gl parameter, e.g., "us"
    search_type: Optional[
        str
    ] = None,  # tbm parameter (images, shopping, news, etc.)
    start: Optional[int] = None,  # pagination start index
    num_results: Optional[int] = 10,  # number of results to return
    location: Optional[str] = None,  # uule parameter for geo-location
    device: Optional[str] = None,  # device type for user-agent
    return_json: bool = False,  # parse results as JSON
    hotel_dates: Optional[str] = None,  # check-in and check-out dates
    hotel_occupancy: Optional[int] = None,  # number of guests
) -> Document:
"""
    Search using Google, Bing, or Yandex with advanced parameters and return results in Markdown.

    Args:
        query (str): Search query
        engine (str): Search engine - 'google', 'bing', or 'yandex'
        zone (Optional[str]): Override default zone

        # Google SERP specific parameters
        language (Optional[str]): Two-letter language code (hl parameter)
        country_code (Optional[str]): Two-letter country code (gl parameter)
        search_type (Optional[str]): Type of search (images, shopping, news, etc.)
        start (Optional[int]): Results pagination offset (0=first page, 10=second page)
        num_results (Optional[int]): Number of results to return (default 10)
        location (Optional[str]): Location for search results (uule parameter)
        device (Optional[str]): Device type (mobile, ios, android, ipad, android_tablet)
        return_json (bool): Return parsed JSON instead of HTML/Markdown

        # Hotel search parameters
        hotel_dates (Optional[str]): Check-in and check-out dates (format: YYYY-MM-DD,YYYY-MM-DD)
        hotel_occupancy (Optional[int]): Number of guests (1-4)

    Returns:
        Document: Search results as Markdown or JSON

    """
    encoded_query = self._encode_query(query)

    base_urls = {
        "google": f"https://www.google.com/search?q={encoded_query}",
        "bing": f"https://www.bing.com/search?q={encoded_query}",
        "yandex": f"https://yandex.com/search/?text={encoded_query}",
    }

    if engine not in base_urls:
        raise ValueError(
            f"Unsupported search engine: {engine}. Use 'google', 'bing', or 'yandex'"
        )

    search_url = base_urls[engine]

    if engine == "google":
        params = []

        if language:
            params.append(f"hl={language}")

        if country_code:
            params.append(f"gl={country_code}")

        if search_type:
            if search_type == "jobs":
                params.append("ibp=htl;jobs")
            else:
                search_types = {"images": "isch", "shopping": "shop", "news": "nws"}
                tbm_value = search_types.get(search_type, search_type)
                params.append(f"tbm={tbm_value}")

        if start is not None:
            params.append(f"start={start}")

        if num_results:
            params.append(f"num={num_results}")

        if location:
            params.append(f"uule={self._encode_query(location)}")

        if device:
            device_value = "1"

            if device in ["ios", "iphone"]:
                device_value = "ios"
            elif device == "ipad":
                device_value = "ios_tablet"
            elif device == "android":
                device_value = "android"
            elif device == "android_tablet":
                device_value = "android_tablet"

            params.append(f"brd_mobile={device_value}")

        if return_json:
            params.append("brd_json=1")

        if hotel_dates:
            params.append(f"hotel_dates={self._encode_query(hotel_dates)}")

        if hotel_occupancy:
            params.append(f"hotel_occupancy={hotel_occupancy}")

        if params:
            search_url += "&" + "&".join(params)

    payload = {
        "url": search_url,
        "zone": zone or self._zone,
        "format": "raw",
        "data_format": "markdown" if not return_json else "raw",
    }

    content = self._make_request(payload)
    return Document(
        text=content, metadata={"query": query, "engine": engine, "url": search_url}
    )

```
 |  
| --- | --- |  
###  web_data_feed [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/brightdata/#llama_index.tools.brightdata.BrightDataToolSpec.web_data_feed "Permanent link")

```
web_data_feed(
    source_type: ,
    url: ,
    num_of_reviews: Optional[] = None,
    timeout:  = 600,
    polling_interval:  = 1,
) -> 

```

Retrieve structured web data from various sources like LinkedIn, Amazon, Instagram, etc.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `source_type`  |  Type of data source (e.g., 'linkedin_person_profile', 'amazon_product')  |  _required_  |  
|  `url`  |  URL of the web resource to retrieve data from  |  _required_  |  
|  `num_of_reviews`  |  `Optional[int]`  |  Number of reviews to retrieve (only for facebook_company_reviews)  |  `None`  |  
|  `timeout`  |  Maximum time in seconds to wait for data retrieval  |  `600`  |  
|  `polling_interval`  |  Time in seconds between polling attempts  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Dict`  |  `Dict`  |  Structured data from the requested source  |  
Source code in `llama-index-integrations/tools/llama-index-tools-brightdata/llama_index/tools/brightdata/base.py`  
| 
```
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
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
```
 | 
```
defweb_data_feed(
    self,
    source_type: str,
    url: str,
    num_of_reviews: Optional[int] = None,
    timeout: int = 600,
    polling_interval: int = 1,
) -> Dict:
"""
    Retrieve structured web data from various sources like LinkedIn, Amazon, Instagram, etc.

    Args:
        source_type (str): Type of data source (e.g., 'linkedin_person_profile', 'amazon_product')
        url (str): URL of the web resource to retrieve data from
        num_of_reviews (Optional[int]): Number of reviews to retrieve (only for facebook_company_reviews)
        timeout (int): Maximum time in seconds to wait for data retrieval
        polling_interval (int): Time in seconds between polling attempts

    Returns:
        Dict: Structured data from the requested source

    """
    importrequests
    importtime

    datasets = {
        "amazon_product": "gd_l7q7dkf244hwjntr0",
        "amazon_product_reviews": "gd_le8e811kzy4ggddlq",
        "linkedin_person_profile": "gd_l1viktl72bvl7bjuj0",
        "linkedin_company_profile": "gd_l1vikfnt1wgvvqz95w",
        "zoominfo_company_profile": "gd_m0ci4a4ivx3j5l6nx",
        "instagram_profiles": "gd_l1vikfch901nx3by4",
        "instagram_posts": "gd_lk5ns7kz21pck8jpis",
        "instagram_reels": "gd_lyclm20il4r5helnj",
        "instagram_comments": "gd_ltppn085pokosxh13",
        "facebook_posts": "gd_lyclm1571iy3mv57zw",
        "facebook_marketplace_listings": "gd_lvt9iwuh6fbcwmx1a",
        "facebook_company_reviews": "gd_m0dtqpiu1mbcyc2g86",
        "x_posts": "gd_lwxkxvnf1cynvib9co",
        "zillow_properties_listing": "gd_lfqkr8wm13ixtbd8f5",
        "booking_hotel_listings": "gd_m5mbdl081229ln6t4a",
        "youtube_videos": "gd_m5mbdl081229ln6t4a",
    }

    if source_type not in datasets:
        valid_sources = ", ".join(datasets.keys())
        raise ValueError(
            f"Invalid source_type: {source_type}. Valid options are: {valid_sources}"
        )

    dataset_id = datasets[source_type]

    request_data = {"url": url}
    if source_type == "facebook_company_reviews" and num_of_reviews is not None:
        request_data["num_of_reviews"] = str(num_of_reviews)

    trigger_response = requests.post(
        "https://api.brightdata.com/datasets/v3/trigger",
        params={"dataset_id": dataset_id, "include_errors": True},
        headers=self._headers,
        json=[request_data],
    )

    trigger_data = trigger_response.json()
    if not trigger_data.get("snapshot_id"):
        raise Exception("No snapshot ID returned from trigger request")

    snapshot_id = trigger_data["snapshot_id"]
    if self._verbose:
        print(
            f"[Bright Data] {source_type} triggered with snapshot ID: {snapshot_id}"
        )

    attempts = 0
    max_attempts = timeout

    while attempts  max_attempts:
        try:
            snapshot_response = requests.get(
                f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}",
                params={"format": "json"},
                headers=self._headers,
            )

            snapshot_data = snapshot_response.json()

            if (
                isinstance(snapshot_data, dict)
                and snapshot_data.get("status") == "running"
            ):
                if self._verbose:
                    print(
                        f"[Bright Data] Snapshot not ready, polling again (attempt {attempts+1}/{max_attempts})"
                    )
                attempts += 1
                time.sleep(polling_interval)
                continue

            if self._verbose:
                print(f"[Bright Data] Data received after {attempts+1} attempts")

            return snapshot_data

        except Exception as e:
            if self._verbose:
                print(f"[Bright Data] Polling error: {e!s}")
            attempts += 1
            time.sleep(polling_interval)

    raise TimeoutError(
        f"Timeout after {max_attempts} seconds waiting for {source_type} data"
    )

```
 |  
| --- | --- |  
options: members: - BrightDataToolSpec
