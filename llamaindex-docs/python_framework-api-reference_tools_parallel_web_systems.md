# Parallel web systems
##  ParallelWebSystemsToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/parallel_web_systems/#llama_index.tools.parallel_web_systems.ParallelWebSystemsToolSpec "Permanent link")
Bases: 
Parallel AI tool spec
This tool provides access to Parallel Web Systems Search and Extract APIs, enabling LLM agents to perform web research and content extraction.
The Search API returns structured, compressed excerpts from web search results optimized for LLM consumption.
The Extract API converts public URLs into clean, LLM-optimized markdown, including JavaScript-heavy pages and PDFs.
Source code in `llama-index-integrations/tools/llama-index-tools-parallel-web-systems/llama_index/tools/parallel_web_systems/base.py`  
| 
```
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
```
 | 
```
classParallelWebSystemsToolSpec(BaseToolSpec):
"""
    Parallel AI tool spec

    This tool provides access to Parallel Web Systems Search and Extract
    APIs, enabling LLM agents to perform web research and content extraction.

    The Search API returns structured, compressed excerpts from web search
    results optimized for LLM consumption.

    The Extract API converts public URLs into clean, LLM-optimized markdown,
    including JavaScript-heavy pages and PDFs.
    """

    spec_functions = [
        "search",
        "extract",
    ]

    def__init__(self, api_key: str, base_url: Optional[str] = None) -> None:
"""
        Initialize with parameters

        Args:
            api_key: Your Parallel AI API key from https://platform.parallel.ai/
            base_url: Optional custom base URL for the API

        """
        self.api_key = api_key
        self.base_url = base_url or "https://api.parallel.ai"

    async defsearch(
        self,
        objective: Optional[str] = None,
        search_queries: Optional[List[str]] = None,
        max_results: int = 10,
        mode: Optional[str] = None,
        excerpts: Optional[Dict[str, Any]] = None,
        source_policy: Optional[Dict[str, Any]] = None,
        fetch_policy: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
"""
        Search the web using Parallel Search API

        Returns structured, compressed excerpts optimized for LLM consumption.
        At least one of `objective` or `search_queries` must be provided.

        Args:
            objective: Natural-language description of what the web search is
                trying to find. This can include guidance about preferred sources
                or freshness.
            search_queries: Optional list of traditional keyword search queries
                to guide the search. May contain search operators. Max 5 queries,
                200 chars each.
            max_results: Upper bound on the number of results to return (1-40).
                The default is 10
            mode: Search mode preset. 'one-shot' returns more comprehensive results
                and longer excerpts for single response answers. 'agentic' returns
                more concise, token-efficient results for use in an agentic loop.
            excerpts: Optional settings to configure excerpt generation.
                Example: {'max_chars_per_result': 1500}
            source_policy: Optional source policy governing domain and date
                preferences in search results.
            fetch_policy: Policy for cached vs live content.
                Example: {'max_age_seconds': 86400, 'timeout_seconds': 60}

        Returns:
            A list of Document objects containing search results with excerpts
            and metadata including url, title, and publish_date.

        """
        if not objective and not search_queries:
            raise ValueError(
                "At least one of 'objective' or 'search_queries' must be provided"
            )

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "parallel-beta": "search-extract-2025-10-10",
        }

        payload: Dict[str, Any] = {
            "max_results": max_results,
        }

        if objective:
            payload["objective"] = objective
        if search_queries:
            payload["search_queries"] = search_queries
        if mode:
            payload["mode"] = mode
        if excerpts:
            payload["excerpts"] = excerpts
        if source_policy:
            payload["source_policy"] = source_policy
        if fetch_policy:
            payload["fetch_policy"] = fetch_policy

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1beta/search",
                    headers=headers,
                    json=payload,
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()

            documents = []
            for result in data.get("results", []):
                # combine excerpts into the document text
                excerpts_list = result.get("excerpts", [])
                text = "\n\n".join(excerpts_list) if excerpts_list else ""

                doc = Document(
                    text=text,
                    metadata={
                        "url": result.get("url"),
                        "title": result.get("title"),
                        "publish_date": result.get("publish_date"),
                        "search_id": data.get("search_id"),
                    },
                )
                documents.append(doc)

            return documents

        except Exception as e:
            print(f"Error calling Parallel AI Search API: {e}")
            return []

    async defextract(
        self,
        urls: List[str],
        objective: Optional[str] = None,
        search_queries: Optional[List[str]] = None,
        excerpts: Union[bool, Dict[str, Any]] = True,
        full_content: Union[bool, Dict[str, Any]] = False,
        fetch_policy: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
"""
        Extract clean, structured content from web pages using Parallel AI's Extract API.

        Converts public URLs into clean, LLM-optimized markdown including
        JavaScript-heavy pages and PDFs

        Args:
            urls: List of URLs to extract content from.
            objective: Natural language objective to focus extraction on specific
                topics. The returned excerpts will be relevant to this objective.
            search_queries: Specific keyword queries to focus extraction.
            excerpts: Include relevant excerpts. Can be True/False or a dict with
                settings like {'max_chars_per_result': 2000}. Excerpts are focused
                on objective/queries if provided.
            full_content: Include full page content. Can be True/False or a dict
                with settings like {'max_chars_per_result': 3000}.
            fetch_policy: Cache vs live content policy.
                Example: {'max_age_seconds': 86400, 'timeout_seconds': 60,
                         'disable_cache_fallback': False}

        Returns:
            A list of Document objects containing extracted content with metadata
            including url, title, publish_date, and excerpts

        """
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "parallel-beta": "search-extract-2025-10-10",
        }

        payload: Dict[str, Any] = {
            "urls": urls,
            "excerpts": excerpts,
            "full_content": full_content,
        }

        if objective:
            payload["objective"] = objective
        if search_queries:
            payload["search_queries"] = search_queries
        if fetch_policy:
            payload["fetch_policy"] = fetch_policy

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1beta/extract",
                    headers=headers,
                    json=payload,
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()

            documents = []
            for result in data.get("results", []):
                # Use full_content if available, otherwise combine excerpts
                full_text = result.get("full_content")
                excerpts_list = result.get("excerpts", [])

                if full_text:
                    text = full_text
                elif excerpts_list:
                    text = "\n\n".join(excerpts_list)
                else:
                    text = ""

                doc = Document(
                    text=text,
                    metadata={
                        "url": result.get("url"),
                        "title": result.get("title"),
                        "publish_date": result.get("publish_date"),
                        "extract_id": data.get("extract_id"),
                        "excerpts": excerpts_list,
                    },
                )
                documents.append(doc)

            # handle any errors in response
            for error in data.get("errors", []):
                doc = Document(
                    text=f"Error extracting content: {error.get('content','Unknown error')}",
                    metadata={
                        "url": error.get("url"),
                        "error_type": error.get("error_type"),
                        "extract_id": data.get("extract_id"),
                    },
                )
                documents.append(doc)

            return documents

        except Exception as e:
            print(f"Error calling Parallel AI Extract API: {e}")
            return []

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/parallel_web_systems/#llama_index.tools.parallel_web_systems.ParallelWebSystemsToolSpec.search "Permanent link")

```
search(
    objective: Optional[] = None,
    search_queries: Optional[[]] = None,
    max_results:  = 10,
    mode: Optional[] = None,
    excerpts: Optional[[, ]] = None,
    source_policy: Optional[[, ]] = None,
    fetch_policy: Optional[[, ]] = None,
) -> []

```

Search the web using Parallel Search API
Returns structured, compressed excerpts optimized for LLM consumption. At least one of `objective` or `search_queries` must be provided.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `objective`  |  `Optional[str]`  |  Natural-language description of what the web search is trying to find. This can include guidance about preferred sources or freshness.  |  `None`  |  
|  `search_queries`  |  `Optional[List[str]]`  |  Optional list of traditional keyword search queries to guide the search. May contain search operators. Max 5 queries, 200 chars each.  |  `None`  |  
|  `max_results`  |  Upper bound on the number of results to return (1-40). The default is 10  |  
|  `mode`  |  `Optional[str]`  |  Search mode preset. 'one-shot' returns more comprehensive results and longer excerpts for single response answers. 'agentic' returns more concise, token-efficient results for use in an agentic loop.  |  `None`  |  
|  `excerpts`  |  `Optional[Dict[str, Any]]`  |  Optional settings to configure excerpt generation. Example: {'max_chars_per_result': 1500}  |  `None`  |  
|  `source_policy`  |  `Optional[Dict[str, Any]]`  |  Optional source policy governing domain and date preferences in search results.  |  `None`  |  
|  `fetch_policy`  |  `Optional[Dict[str, Any]]`  |  Policy for cached vs live content. Example: {'max_age_seconds': 86400, 'timeout_seconds': 60}  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  A list of Document objects containing search results with excerpts  |  
|   |  and metadata including url, title, and publish_date.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-parallel-web-systems/llama_index/tools/parallel_web_systems/base.py`  
| 
```
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
```
 | 
```
async defsearch(
    self,
    objective: Optional[str] = None,
    search_queries: Optional[List[str]] = None,
    max_results: int = 10,
    mode: Optional[str] = None,
    excerpts: Optional[Dict[str, Any]] = None,
    source_policy: Optional[Dict[str, Any]] = None,
    fetch_policy: Optional[Dict[str, Any]] = None,
) -> List[Document]:
"""
    Search the web using Parallel Search API

    Returns structured, compressed excerpts optimized for LLM consumption.
    At least one of `objective` or `search_queries` must be provided.

    Args:
        objective: Natural-language description of what the web search is
            trying to find. This can include guidance about preferred sources
            or freshness.
        search_queries: Optional list of traditional keyword search queries
            to guide the search. May contain search operators. Max 5 queries,
            200 chars each.
        max_results: Upper bound on the number of results to return (1-40).
            The default is 10
        mode: Search mode preset. 'one-shot' returns more comprehensive results
            and longer excerpts for single response answers. 'agentic' returns
            more concise, token-efficient results for use in an agentic loop.
        excerpts: Optional settings to configure excerpt generation.
            Example: {'max_chars_per_result': 1500}
        source_policy: Optional source policy governing domain and date
            preferences in search results.
        fetch_policy: Policy for cached vs live content.
            Example: {'max_age_seconds': 86400, 'timeout_seconds': 60}

    Returns:
        A list of Document objects containing search results with excerpts
        and metadata including url, title, and publish_date.

    """
    if not objective and not search_queries:
        raise ValueError(
            "At least one of 'objective' or 'search_queries' must be provided"
        )

    headers = {
        "x-api-key": self.api_key,
        "Content-Type": "application/json",
        "parallel-beta": "search-extract-2025-10-10",
    }

    payload: Dict[str, Any] = {
        "max_results": max_results,
    }

    if objective:
        payload["objective"] = objective
    if search_queries:
        payload["search_queries"] = search_queries
    if mode:
        payload["mode"] = mode
    if excerpts:
        payload["excerpts"] = excerpts
    if source_policy:
        payload["source_policy"] = source_policy
    if fetch_policy:
        payload["fetch_policy"] = fetch_policy

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1beta/search",
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()

        documents = []
        for result in data.get("results", []):
            # combine excerpts into the document text
            excerpts_list = result.get("excerpts", [])
            text = "\n\n".join(excerpts_list) if excerpts_list else ""

            doc = Document(
                text=text,
                metadata={
                    "url": result.get("url"),
                    "title": result.get("title"),
                    "publish_date": result.get("publish_date"),
                    "search_id": data.get("search_id"),
                },
            )
            documents.append(doc)

        return documents

    except Exception as e:
        print(f"Error calling Parallel AI Search API: {e}")
        return []

```
 |  
| --- | --- |  
###  extract [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/parallel_web_systems/#llama_index.tools.parallel_web_systems.ParallelWebSystemsToolSpec.extract "Permanent link")

```
extract(
    urls: [],
    objective: Optional[] = None,
    search_queries: Optional[[]] = None,
    excerpts: Union[, [, ]] = True,
    full_content: Union[, [, ]] = False,
    fetch_policy: Optional[[, ]] = None,
) -> []

```

Extract clean, structured content from web pages using Parallel AI's Extract API.
Converts public URLs into clean, LLM-optimized markdown including JavaScript-heavy pages and PDFs
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  `List[str]`  |  List of URLs to extract content from.  |  _required_  |  
|  `objective`  |  `Optional[str]`  |  Natural language objective to focus extraction on specific topics. The returned excerpts will be relevant to this objective.  |  `None`  |  
|  `search_queries`  |  `Optional[List[str]]`  |  Specific keyword queries to focus extraction.  |  `None`  |  
|  `excerpts`  |  `Union[bool, Dict[str, Any]]`  |  Include relevant excerpts. Can be True/False or a dict with settings like {'max_chars_per_result': 2000}. Excerpts are focused on objective/queries if provided.  |  `True`  |  
|  `full_content`  |  `Union[bool, Dict[str, Any]]`  |  Include full page content. Can be True/False or a dict with settings like {'max_chars_per_result': 3000}.  |  `False`  |  
|  `fetch_policy`  |  `Optional[Dict[str, Any]]`  |  Cache vs live content policy. Example: {'max_age_seconds': 86400, 'timeout_seconds': 60, 'disable_cache_fallback': False}  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  A list of Document objects containing extracted content with metadata  |  
|   |  including url, title, publish_date, and excerpts  |  
Source code in `llama-index-integrations/tools/llama-index-tools-parallel-web-systems/llama_index/tools/parallel_web_systems/base.py`  
| 
```
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
```
 | 
```
async defextract(
    self,
    urls: List[str],
    objective: Optional[str] = None,
    search_queries: Optional[List[str]] = None,
    excerpts: Union[bool, Dict[str, Any]] = True,
    full_content: Union[bool, Dict[str, Any]] = False,
    fetch_policy: Optional[Dict[str, Any]] = None,
) -> List[Document]:
"""
    Extract clean, structured content from web pages using Parallel AI's Extract API.

    Converts public URLs into clean, LLM-optimized markdown including
    JavaScript-heavy pages and PDFs

    Args:
        urls: List of URLs to extract content from.
        objective: Natural language objective to focus extraction on specific
            topics. The returned excerpts will be relevant to this objective.
        search_queries: Specific keyword queries to focus extraction.
        excerpts: Include relevant excerpts. Can be True/False or a dict with
            settings like {'max_chars_per_result': 2000}. Excerpts are focused
            on objective/queries if provided.
        full_content: Include full page content. Can be True/False or a dict
            with settings like {'max_chars_per_result': 3000}.
        fetch_policy: Cache vs live content policy.
            Example: {'max_age_seconds': 86400, 'timeout_seconds': 60,
                     'disable_cache_fallback': False}

    Returns:
        A list of Document objects containing extracted content with metadata
        including url, title, publish_date, and excerpts

    """
    headers = {
        "x-api-key": self.api_key,
        "Content-Type": "application/json",
        "parallel-beta": "search-extract-2025-10-10",
    }

    payload: Dict[str, Any] = {
        "urls": urls,
        "excerpts": excerpts,
        "full_content": full_content,
    }

    if objective:
        payload["objective"] = objective
    if search_queries:
        payload["search_queries"] = search_queries
    if fetch_policy:
        payload["fetch_policy"] = fetch_policy

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1beta/extract",
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()

        documents = []
        for result in data.get("results", []):
            # Use full_content if available, otherwise combine excerpts
            full_text = result.get("full_content")
            excerpts_list = result.get("excerpts", [])

            if full_text:
                text = full_text
            elif excerpts_list:
                text = "\n\n".join(excerpts_list)
            else:
                text = ""

            doc = Document(
                text=text,
                metadata={
                    "url": result.get("url"),
                    "title": result.get("title"),
                    "publish_date": result.get("publish_date"),
                    "extract_id": data.get("extract_id"),
                    "excerpts": excerpts_list,
                },
            )
            documents.append(doc)

        # handle any errors in response
        for error in data.get("errors", []):
            doc = Document(
                text=f"Error extracting content: {error.get('content','Unknown error')}",
                metadata={
                    "url": error.get("url"),
                    "error_type": error.get("error_type"),
                    "extract_id": data.get("extract_id"),
                },
            )
            documents.append(doc)

        return documents

    except Exception as e:
        print(f"Error calling Parallel AI Extract API: {e}")
        return []

```
 |  
| --- | --- |  
options: members: - ParallelWebSystemsToolSpec
