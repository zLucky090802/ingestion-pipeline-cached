# Valyu
##  ValyuToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/valyu/#llama_index.tools.valyu.ValyuToolSpec "Permanent link")
Bases: 
Valyu tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-valyu/llama_index/tools/valyu/base.py`  
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
```
 | 
```
classValyuToolSpec(BaseToolSpec):
"""Valyu tool spec."""

    spec_functions = [
        "search",
        "get_contents",
    ]

    def__init__(
        self,
        api_key: str,
        verbose: bool = False,
        # Search API parameters
        max_price: Optional[float] = 100,
        relevance_threshold: float = 0.5,
        fast_mode: Optional[bool] = False,
        included_sources: Optional[List[str]] = None,
        excluded_sources: Optional[List[str]] = None,
        response_length: Optional[Union[int, str]] = None,
        country_code: Optional[str] = None,
        # Contents API parameters
        contents_summary: Optional[Union[bool, str, Dict[str, Any]]] = None,
        contents_extract_effort: Optional[str] = "normal",
        contents_response_length: Optional[Union[str, int]] = "short",
    ) -> None:
"""
        Initialize with parameters.

        Args:
            api_key (str): Valyu API key
            verbose (bool): Enable verbose logging. Defaults to False
            max_price (Optional[float]): Maximum cost in dollars for search operations. Defaults to 100
            relevance_threshold (float): Minimum relevance score required for results (0.0-1.0). Defaults to 0.5
            fast_mode (Optional[bool]): Enable fast mode for faster but shorter results. If None, model can decide per search (defaults to False if not specified). Defaults to None
            included_sources (Optional[List[str]]): List of URLs, domains or datasets to only search over and return in results. Defaults to None
            excluded_sources (Optional[List[str]]): List of URLs, domains or datasets to exclude from search results. Defaults to None
            response_length (Optional[Union[int, str]]): Number of characters to return per item or preset values: "short" (25k chars), "medium" (50k chars), "large" (100k chars), "max" (full content). Defaults to None
            country_code (Optional[str]): 2-letter ISO country code (e.g., "GB", "US") to bias search results to a specific country. Defaults to None
            contents_summary (Optional[Union[bool, str, Dict[str, Any]]]): AI summary configuration:
                - False/None: No AI processing (raw content)
                - True: Basic automatic summarization
                - str: Custom instructions (max 500 chars)
                - dict: JSON schema for structured extraction
            contents_extract_effort (Optional[str]): Extraction thoroughness:
                - "normal": Fast extraction (default)
                - "high": More thorough but slower
                - "auto": Automatically determine extraction effort but slowest
            contents_response_length (Optional[Union[str, int]]): Content length per URL:
                - "short": 25,000 characters (default)
                - "medium": 50,000 characters
                - "large": 100,000 characters
                - "max": No limit
                - int: Custom character limit

        """
        fromvalyuimport Valyu

        # Validate parameters
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            raise ValueError("api_key must be a non-empty string")

        if max_price is not None and (
            not isinstance(max_price, (int, float)) or max_price  0
        ):
            raise ValueError("max_price must be a non-negative number or None")

        if (
            not isinstance(relevance_threshold, (int, float))
            or relevance_threshold  0.0
            or relevance_threshold  1.0
        ):
            raise ValueError("relevance_threshold must be a number between 0.0 and 1.0")

        if not isinstance(verbose, bool):
            raise ValueError("verbose must be a boolean")

        if fast_mode is not None and not isinstance(fast_mode, bool):
            raise ValueError("fast_mode must be a boolean or None")

        # Validate search parameters
        if included_sources is not None:
            if not isinstance(included_sources, list) or not all(
                isinstance(s, str) for s in included_sources
            ):
                raise ValueError("included_sources must be a list of strings or None")

        if excluded_sources is not None:
            if not isinstance(excluded_sources, list) or not all(
                isinstance(s, str) for s in excluded_sources
            ):
                raise ValueError("excluded_sources must be a list of strings or None")

        # Validate response_length
        if response_length is not None:
            valid_preset_lengths = ["short", "medium", "large", "max"]
            if isinstance(response_length, str):
                if response_length not in valid_preset_lengths:
                    raise ValueError(
                        f"response_length string must be one of {valid_preset_lengths}"
                    )
            elif isinstance(response_length, int):
                if response_length  1:
                    raise ValueError(
                        "response_length must be a positive integer when using custom length"
                    )
            else:
                raise ValueError(
                    "response_length must be a string preset, positive integer, or None"
                )

        # Validate country_code
        if country_code is not None:
            if (
                not isinstance(country_code, str)
                or len(country_code) != 2
                or not country_code.isalpha()
            ):
                raise ValueError(
                    "country_code must be a 2-letter ISO country code (e.g., 'GB', 'US') or None"
                )

        # Validate contents_summary
        if contents_summary is not None:
            if isinstance(contents_summary, str):
                if len(contents_summary)  500:
                    raise ValueError(
                        f"contents_summary string must be 500 characters or less. "
                        f"Current length: {len(contents_summary)} characters."
                    )
            elif not isinstance(contents_summary, (bool, dict)):
                raise ValueError(
                    "contents_summary must be a boolean, string, dict, or None"
                )

        # Validate contents_extract_effort
        valid_extract_efforts = ["normal", "high", "auto"]
        if (
            contents_extract_effort is not None
            and contents_extract_effort not in valid_extract_efforts
        ):
            raise ValueError(
                f"contents_extract_effort must be one of {valid_extract_efforts}"
            )

        # Validate contents_response_length
        if contents_response_length is not None:
            valid_preset_lengths = ["short", "medium", "large", "max"]
            if isinstance(contents_response_length, str):
                if contents_response_length not in valid_preset_lengths:
                    raise ValueError(
                        f"contents_response_length string must be one of {valid_preset_lengths}"
                    )
            elif isinstance(contents_response_length, int):
                if contents_response_length  1:
                    raise ValueError(
                        "contents_response_length must be a positive integer when using custom length"
                    )
            else:
                raise ValueError(
                    "contents_response_length must be a string preset, positive integer, or None"
                )

        self.client = Valyu(api_key=api_key)
        self._verbose = verbose
        self._max_price = max_price
        self._relevance_threshold = relevance_threshold
        self._fast_mode = fast_mode
        # Search API defaults
        self._included_sources = included_sources
        self._excluded_sources = excluded_sources
        self._response_length = response_length
        self._country_code = country_code
        # Contents API defaults
        self._contents_summary = contents_summary
        self._contents_extract_effort = contents_extract_effort
        self._contents_response_length = contents_response_length

    defsearch(
        self,
        query: str,
        search_type: str = "all",
        max_num_results: int = 5,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fast_mode: Optional[bool] = None,
    ) -> List[Document]:
"""
        Search and retrieve relevant content from proprietary and public sources using Valyu's deep search.

        Args:
            query (str): The input query to be processed
            search_type (str): Type of search - "all" (both proprietary and web), "proprietary" (Valyu indices only), or "web" (web search only). Defaults to "all"
            max_num_results (int): Maximum number of results to return (1-20). Defaults to 5
            start_date (Optional[str]): Start date for time filtering in YYYY-MM-DD format
            end_date (Optional[str]): End date for time filtering in YYYY-MM-DD format
            fast_mode (Optional[bool]): Enable fast mode for faster but shorter results. If None, uses the default set during initialization, or defaults to False if no user default was set

        Returns:
            List[Document]: List of Document objects containing the search results

        Note:
            The following parameters are set during tool initialization and cannot be modified per search:
            - max_price: Maximum cost limit for search operations
            - relevance_threshold: Minimum relevance score required for results
            - included_sources: List of sources to include in search
            - excluded_sources: List of sources to exclude from search
            - response_length: Response length configuration
            - country_code: Country bias for search results

        """
        # Handle fast_mode: if user set a specific value (not None), always use it
        # If user set None, then model can decide, but we need to provide a boolean to the SDK
        if self._fast_mode is not None:
            fast_mode = self._fast_mode  # User controls fast_mode
        elif fast_mode is None:
            # Both user and model didn't specify, use SDK default (False)
            fast_mode = False

        response = self.client.search(
            query=query,
            search_type=search_type,
            max_num_results=max_num_results,
            relevance_threshold=self._relevance_threshold,
            max_price=self._max_price,
            start_date=start_date,
            end_date=end_date,
            included_sources=self._included_sources,
            excluded_sources=self._excluded_sources,
            response_length=self._response_length,
            country_code=self._country_code,
            fast_mode=fast_mode,
        )

        if self._verbose:
            print(f"[Valyu Tool] Response: {response}")

        documents = []
        for result in response.results:
            metadata = {
                "title": result.title,
                "url": result.url,
                "source": result.source,
                "price": result.price,
                "length": result.length,
                "data_type": result.data_type,
                "relevance_score": result.relevance_score,
            }

            documents.append(
                Document(
                    text=result.content,
                    metadata=metadata,
                )
            )

        return documents

    defget_contents(
        self,
        urls: List[str],
    ) -> List[Document]:
"""
        Extract clean, structured content from web pages.

        This method fetches the content from the provided URLs using Valyu's content extraction API.
        The extraction parameters (summary, extract_effort, response_length, max_price) are set
        during tool initialization and cannot be modified by the model - only the URLs can be specified.

        Args:
            urls (List[str]): List of URLs to extract content from (maximum 10 URLs per request)

        Returns:
            List[Document]: List of Document objects containing the extracted content

        """
        response = self.client.contents(
            urls=urls,
            summary=self._contents_summary,
            extract_effort=self._contents_extract_effort,
            response_length=self._contents_response_length,
        )

        if self._verbose:
            print(f"[Valyu Tool] Contents Response: {response}")

        documents = []
        if response and response.results:
            for result in response.results:
                metadata = {
                    "url": result.url,
                    "title": result.title,
                    "source": result.source,
                    "length": result.length,
                    "data_type": result.data_type,
                    "citation": result.citation,
                }

                # Add summary info if available
                if hasattr(result, "summary") and result.summary:
                    metadata["summary"] = result.summary
                if (
                    hasattr(result, "summary_success")
                    and result.summary_success is not None
                ):
                    metadata["summary_success"] = result.summary_success

                # Add image URL if available
                if hasattr(result, "image_url") and result.image_url:
                    metadata["image_url"] = result.image_url

                documents.append(
                    Document(
                        text=str(result.content),
                        metadata=metadata,
                    )
                )

        return documents

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/valyu/#llama_index.tools.valyu.ValyuToolSpec.search "Permanent link")

```
search(
    query: ,
    search_type:  = "all",
    max_num_results:  = 5,
    start_date: Optional[] = None,
    end_date: Optional[] = None,
    fast_mode: Optional[] = None,
) -> []

```

Search and retrieve relevant content from proprietary and public sources using Valyu's deep search.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The input query to be processed  |  _required_  |  
|  `search_type`  |  Type of search - "all" (both proprietary and web), "proprietary" (Valyu indices only), or "web" (web search only). Defaults to "all"  |  `'all'`  |  
|  `max_num_results`  |  Maximum number of results to return (1-20). Defaults to 5  |  
|  `start_date`  |  `Optional[str]`  |  Start date for time filtering in YYYY-MM-DD format  |  `None`  |  
|  `end_date`  |  `Optional[str]`  |  End date for time filtering in YYYY-MM-DD format  |  `None`  |  
|  `fast_mode`  |  `Optional[bool]`  |  Enable fast mode for faster but shorter results. If None, uses the default set during initialization, or defaults to False if no user default was set  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of Document objects containing the search results  |  
Note
The following parameters are set during tool initialization and cannot be modified per search: - max_price: Maximum cost limit for search operations - relevance_threshold: Minimum relevance score required for results - included_sources: List of sources to include in search - excluded_sources: List of sources to exclude from search - response_length: Response length configuration - country_code: Country bias for search results
Source code in `llama-index-integrations/tools/llama-index-tools-valyu/llama_index/tools/valyu/base.py`  
| 
```
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
```
 | 
```
defsearch(
    self,
    query: str,
    search_type: str = "all",
    max_num_results: int = 5,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    fast_mode: Optional[bool] = None,
) -> List[Document]:
"""
    Search and retrieve relevant content from proprietary and public sources using Valyu's deep search.

    Args:
        query (str): The input query to be processed
        search_type (str): Type of search - "all" (both proprietary and web), "proprietary" (Valyu indices only), or "web" (web search only). Defaults to "all"
        max_num_results (int): Maximum number of results to return (1-20). Defaults to 5
        start_date (Optional[str]): Start date for time filtering in YYYY-MM-DD format
        end_date (Optional[str]): End date for time filtering in YYYY-MM-DD format
        fast_mode (Optional[bool]): Enable fast mode for faster but shorter results. If None, uses the default set during initialization, or defaults to False if no user default was set

    Returns:
        List[Document]: List of Document objects containing the search results

    Note:
        The following parameters are set during tool initialization and cannot be modified per search:
        - max_price: Maximum cost limit for search operations
        - relevance_threshold: Minimum relevance score required for results
        - included_sources: List of sources to include in search
        - excluded_sources: List of sources to exclude from search
        - response_length: Response length configuration
        - country_code: Country bias for search results

    """
    # Handle fast_mode: if user set a specific value (not None), always use it
    # If user set None, then model can decide, but we need to provide a boolean to the SDK
    if self._fast_mode is not None:
        fast_mode = self._fast_mode  # User controls fast_mode
    elif fast_mode is None:
        # Both user and model didn't specify, use SDK default (False)
        fast_mode = False

    response = self.client.search(
        query=query,
        search_type=search_type,
        max_num_results=max_num_results,
        relevance_threshold=self._relevance_threshold,
        max_price=self._max_price,
        start_date=start_date,
        end_date=end_date,
        included_sources=self._included_sources,
        excluded_sources=self._excluded_sources,
        response_length=self._response_length,
        country_code=self._country_code,
        fast_mode=fast_mode,
    )

    if self._verbose:
        print(f"[Valyu Tool] Response: {response}")

    documents = []
    for result in response.results:
        metadata = {
            "title": result.title,
            "url": result.url,
            "source": result.source,
            "price": result.price,
            "length": result.length,
            "data_type": result.data_type,
            "relevance_score": result.relevance_score,
        }

        documents.append(
            Document(
                text=result.content,
                metadata=metadata,
            )
        )

    return documents

```
 |  
| --- | --- |  
###  get_contents [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/valyu/#llama_index.tools.valyu.ValyuToolSpec.get_contents "Permanent link")

```
get_contents(urls: []) -> []

```

Extract clean, structured content from web pages.
This method fetches the content from the provided URLs using Valyu's content extraction API. The extraction parameters (summary, extract_effort, response_length, max_price) are set during tool initialization and cannot be modified by the model - only the URLs can be specified.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List of URLs to extract content from (maximum 10 URLs per request)  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of Document objects containing the extracted content  |  
Source code in `llama-index-integrations/tools/llama-index-tools-valyu/llama_index/tools/valyu/base.py`  
| 
```
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
```
 | 
```
defget_contents(
    self,
    urls: List[str],
) -> List[Document]:
"""
    Extract clean, structured content from web pages.

    This method fetches the content from the provided URLs using Valyu's content extraction API.
    The extraction parameters (summary, extract_effort, response_length, max_price) are set
    during tool initialization and cannot be modified by the model - only the URLs can be specified.

    Args:
        urls (List[str]): List of URLs to extract content from (maximum 10 URLs per request)

    Returns:
        List[Document]: List of Document objects containing the extracted content

    """
    response = self.client.contents(
        urls=urls,
        summary=self._contents_summary,
        extract_effort=self._contents_extract_effort,
        response_length=self._contents_response_length,
    )

    if self._verbose:
        print(f"[Valyu Tool] Contents Response: {response}")

    documents = []
    if response and response.results:
        for result in response.results:
            metadata = {
                "url": result.url,
                "title": result.title,
                "source": result.source,
                "length": result.length,
                "data_type": result.data_type,
                "citation": result.citation,
            }

            # Add summary info if available
            if hasattr(result, "summary") and result.summary:
                metadata["summary"] = result.summary
            if (
                hasattr(result, "summary_success")
                and result.summary_success is not None
            ):
                metadata["summary_success"] = result.summary_success

            # Add image URL if available
            if hasattr(result, "image_url") and result.image_url:
                metadata["image_url"] = result.image_url

            documents.append(
                Document(
                    text=str(result.content),
                    metadata=metadata,
                )
            )

    return documents

```
 |  
| --- | --- |  
##  ValyuRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/valyu/#llama_index.tools.valyu.ValyuRetriever "Permanent link")
Bases: 
Valyu retriever for extracting content from URLs.
Source code in `llama-index-integrations/tools/llama-index-tools-valyu/llama_index/tools/valyu/retriever.py`  
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
```
 | 
```
classValyuRetriever(BaseRetriever):
"""Valyu retriever for extracting content from URLs."""

    def__init__(
        self,
        api_key: str,
        verbose: bool = False,
        # Contents API parameters
        contents_summary: Optional[Union[bool, str, Dict[str, Any]]] = None,
        contents_extract_effort: Optional[str] = "normal",
        contents_response_length: Optional[Union[str, int]] = "short",
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
"""
        Initialize Valyu retriever.

        Args:
            api_key (str): Valyu API key
            verbose (bool): Enable verbose logging. Defaults to False
            contents_summary (Optional[Union[bool, str, Dict[str, Any]]]): AI summary configuration:
                - False/None: No AI processing (raw content)
                - True: Basic automatic summarization
                - str: Custom instructions (max 500 chars)
                - dict: JSON schema for structured extraction
            contents_extract_effort (Optional[str]): Extraction thoroughness:
                - "normal": Fast extraction (default)
                - "high": More thorough but slower
                - "auto": Automatically determine extraction effort but slowest
            contents_response_length (Optional[Union[str, int]]): Content length per URL:
                - "short": 25,000 characters (default)
                - "medium": 50,000 characters
                - "large": 100,000 characters
                - "max": No limit
                - int: Custom character limit
            callback_manager (Optional[CallbackManager]): Callback manager for tracking operations

        """
        fromvalyuimport Valyu

        # Validate parameters
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            raise ValueError("api_key must be a non-empty string")

        if not isinstance(verbose, bool):
            raise ValueError("verbose must be a boolean")

        # Validate contents_summary
        if contents_summary is not None:
            if isinstance(contents_summary, str):
                if len(contents_summary)  500:
                    raise ValueError(
                        f"contents_summary string must be 500 characters or less. "
                        f"Current length: {len(contents_summary)} characters."
                    )
            elif not isinstance(contents_summary, (bool, dict)):
                raise ValueError(
                    "contents_summary must be a boolean, string, dict, or None"
                )

        # Validate contents_extract_effort
        valid_extract_efforts = ["normal", "high", "auto"]
        if (
            contents_extract_effort is not None
            and contents_extract_effort not in valid_extract_efforts
        ):
            raise ValueError(
                f"contents_extract_effort must be one of {valid_extract_efforts}"
            )

        # Validate contents_response_length
        if contents_response_length is not None:
            valid_preset_lengths = ["short", "medium", "large", "max"]
            if isinstance(contents_response_length, str):
                if contents_response_length not in valid_preset_lengths:
                    raise ValueError(
                        f"contents_response_length string must be one of {valid_preset_lengths}"
                    )
            elif isinstance(contents_response_length, int):
                if contents_response_length  1:
                    raise ValueError(
                        "contents_response_length must be a positive integer when using custom length"
                    )
            else:
                raise ValueError(
                    "contents_response_length must be a string preset, positive integer, or None"
                )

        self.client = Valyu(api_key=api_key)
        self._verbose = verbose
        self._contents_summary = contents_summary
        self._contents_extract_effort = contents_extract_effort
        self._contents_response_length = contents_response_length

        super().__init__(callback_manager=callback_manager)

    def_retrieve(self, query_bundle) -> List[NodeWithScore]:
"""
        Retrieve content from URLs.

        The query_bundle.query_str should contain URLs (space or comma separated).
        This method extracts content from those URLs and returns them as scored nodes.

        Args:
            query_bundle: Query bundle containing URLs to extract content from

        Returns:
            List[NodeWithScore]: List of nodes with extracted content and relevance scores

        """
        # Parse URLs from query string
        urls = self._parse_urls_from_query(query_bundle.query_str)

        if not urls:
            return []

        # Get content using Valyu API
        response = self.client.contents(
            urls=urls,
            summary=self._contents_summary,
            extract_effort=self._contents_extract_effort,
            response_length=self._contents_response_length,
        )

        if self._verbose:
            print(f"[Valyu Retriever] Contents Response: {response}")

        nodes = []
        if response and response.results:
            for result in response.results:
                metadata = {
                    "url": result.url,
                    "title": result.title,
                    "source": result.source,
                    "length": result.length,
                    "data_type": result.data_type,
                    "citation": result.citation,
                }

                # Add summary info if available
                if hasattr(result, "summary") and result.summary:
                    metadata["summary"] = result.summary
                if (
                    hasattr(result, "summary_success")
                    and result.summary_success is not None
                ):
                    metadata["summary_success"] = result.summary_success

                # Add image URL if available
                if hasattr(result, "image_url") and result.image_url:
                    metadata["image_url"] = result.image_url

                # Create text node
                node = TextNode(
                    text=str(result.content),
                    metadata=metadata,
                )

                # Add as scored node (all retrieved content gets score of 1.0)
                nodes.append(NodeWithScore(node=node, score=1.0))

        return nodes

    def_parse_urls_from_query(self, query_str: str) -> List[str]:
"""
        Parse URLs from query string.

        Args:
            query_str: String containing URLs (space or comma separated)

        Returns:
            List[str]: List of valid URLs

        """
        # Split by common separators
        importre

        # Split by whitespace or commas
        potential_urls = re.split(r"[,\s]+", query_str.strip())

        # Filter for valid URLs
        urls = []
        for url in potential_urls:
            url = url.strip()
            if url and url.startswith(("http://", "https://")):
                urls.append(url)

        return urls[:10]  # Limit to 10 URLs as per API constraint

```
 |  
| --- | --- |  
options: members: - ValyuToolSpec
