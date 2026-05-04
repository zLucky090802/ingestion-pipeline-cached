# Requests
##  RequestsToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/requests/#llama_index.tools.requests.RequestsToolSpec "Permanent link")
Bases: 
Requests Tool.
Source code in `llama-index-integrations/tools/llama-index-tools-requests/llama_index/tools/requests/base.py`  
| 
```
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
```
 | 
```
classRequestsToolSpec(BaseToolSpec):
"""Requests Tool."""

    spec_functions = [
        "get_request",
        "post_request",
        "patch_request",
        "put_request",
        "delete_request",
    ]

    def__init__(self, domain_headers: Optional[dict] = None, timeout_seconds=None):
        self.domain_headers = {} if domain_headers is None else domain_headers
        self.timeout_seconds = timeout_seconds

    # Using dict[str, str] instead of tuple[str, str] for query_params because the way Pydantic
    # converts it into a JSON schema is incompatible with OpenAPI.
    defget_request(
        self,
        url_template: str,
        path_params: dict[str, str] = None,
        query_params: dict[str, str] = None,
    ):
"""
        Use this to GET content from a website.

        Args:
            url_template ([str]): The url to make the request against, potentially includes curly
                braces {} to mark a section of a URL path as replaceable using path parameters.
            path_params (dict[str, str]): path parameters for use in the url_template
            query_params (dict[str, str]): query parameters

        """
        if query_params is None:
            query_params = {}
        if not self._valid_url(url_template):
            return INVALID_URL_PROMPT

        path_params = {} if path_params is None else path_params
        url = self._replace_path_params(url_template, path_params)
        res = requests.get(
            url,
            headers=self._get_headers_for_url(url_template),
            params=query_params,
            timeout=self.timeout_seconds,
        )
        return res.json()

    defpost_request(
        self,
        url_template: str,
        path_params: dict[str, str] = None,
        query_params: dict[str, str] = None,
        body: Optional[dict] = None,
    ):
"""
        Use this to POST content to a website.

        Args:
            url_template ([str]): The url to make the request against, potentially includes curly
                braces {} to mark a section of a URL path as replaceable using path parameters.
            path_params (dict[str, str]): path parameters for use in the url_template
            query_params (dict[str, str]): query parameters
            body (Optional[dict]): the body of the request, sent as JSON

        """
        if not self._valid_url(url_template):
            return INVALID_URL_PROMPT

        url = self._replace_path_params(url_template, path_params)
        res = requests.post(
            url,
            headers=self._get_headers_for_url(url_template),
            params=query_params,
            json=body,
            timeout=self.timeout_seconds,
        )
        return res.json()

    defpatch_request(
        self,
        url_template: str,
        path_params: dict[str, str] = None,
        query_params: dict[str, str] = None,
        body: Optional[dict] = None,
    ):
"""
        Use this to PATCH content to a website.

        Args:
            url_template ([str]): The url to make the request against, potentially includes curly
                braces {} to mark a section of a URL path as replaceable using path parameters.
            path_params (dict[str, str]): path parameters for use in the url_template
            query_params (dict[str, str]): query parameters
            body (Optional[dict]): the body of the request, sent as JSON

        """
        if not self._valid_url(url_template):
            return INVALID_URL_PROMPT

        url = self._replace_path_params(url_template, path_params)
        res = requests.patch(
            url,
            headers=self._get_headers_for_url(url_template),
            params=query_params,
            json=body,
            timeout=self.timeout_seconds,
        )
        return res.json()

    defput_request(
        self,
        url_template: str,
        path_params: dict[str, str] = None,
        query_params: dict[str, str] = None,
        body: Optional[dict] = None,
    ):
"""
        Use this to PUT content to a website.

        Args:
            url_template ([str]): The url to make the request against, potentially includes curly
                braces {} to mark a section of a URL path as replaceable using path parameters.
            path_params (dict[str, str]): path parameters for use in the url_template
            query_params (dict[str, str]): query parameters
            body (Optional[dict]): the body of the request, sent as JSON

        """
        if not self._valid_url(url_template):
            return INVALID_URL_PROMPT

        url = self._replace_path_params(url_template, path_params)
        res = requests.put(
            url,
            headers=self._get_headers_for_url(url_template),
            params=query_params,
            json=body,
            timeout=self.timeout_seconds,
        )
        return res.json()

    defdelete_request(
        self,
        url_template: str,
        path_params: dict[str, str] = None,
        query_params: dict[str, str] = None,
        body: Optional[dict] = None,
    ):
"""
        Use this to DELETE content from a website.

        Args:
            url_template ([str]): The url to make the request against, potentially includes
                curly braces {} to mark a section of a URL path as replaceable using path
                parameters.
            path_params (dict[str, str]): path parameters for use in the url_template
            query_params (dict[str, str]): query parameters
            body (Optional[dict]): the body of the request, sent as JSON (not typically used)

        """
        if not self._valid_url(url_template):
            return INVALID_URL_PROMPT

        url = self._replace_path_params(url_template, path_params)
        res = requests.delete(
            url,
            headers=self._get_headers_for_url(url_template),
            params=query_params,
            json=body,
            timeout=self.timeout_seconds,
        )
        return res.json()

    def_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.scheme and parsed.hostname

    def_get_domain(self, url: str) -> str:
        return urlparse(url).hostname

    def_get_headers_for_url(self, url: str) -> dict:
        return self.domain_headers.get(self._get_domain(url), {})

    @staticmethod
    def_replace_path_params(url_template: str, params: dict) -> str:
        if not params:
            return url_template

        parsed = urlparse(url_template)
        path = parsed.path
        for key, value in params.items():
            path = path.replace("{" + key + "}", str(value))
        parsed = parsed._replace(path=path)
        return str(urlunparse(parsed))

```
 |  
| --- | --- |  
###  get_request [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/requests/#llama_index.tools.requests.RequestsToolSpec.get_request "Permanent link")

```
get_request(
    url_template: ,
    path_params: [, ] = None,
    query_params: [, ] = None,
)

```

Use this to GET content from a website.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url_template`  |  `[str]`  |  The url to make the request against, potentially includes curly braces {} to mark a section of a URL path as replaceable using path parameters.  |  _required_  |  
|  `path_params`  |  `dict[str, str]`  |  path parameters for use in the url_template  |  `None`  |  
|  `query_params`  |  `dict[str, str]`  |  query parameters  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-requests/llama_index/tools/requests/base.py`  
| 
```
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
```
 | 
```
defget_request(
    self,
    url_template: str,
    path_params: dict[str, str] = None,
    query_params: dict[str, str] = None,
):
"""
    Use this to GET content from a website.

    Args:
        url_template ([str]): The url to make the request against, potentially includes curly
            braces {} to mark a section of a URL path as replaceable using path parameters.
        path_params (dict[str, str]): path parameters for use in the url_template
        query_params (dict[str, str]): query parameters

    """
    if query_params is None:
        query_params = {}
    if not self._valid_url(url_template):
        return INVALID_URL_PROMPT

    path_params = {} if path_params is None else path_params
    url = self._replace_path_params(url_template, path_params)
    res = requests.get(
        url,
        headers=self._get_headers_for_url(url_template),
        params=query_params,
        timeout=self.timeout_seconds,
    )
    return res.json()

```
 |  
| --- | --- |  
###  post_request [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/requests/#llama_index.tools.requests.RequestsToolSpec.post_request "Permanent link")

```
post_request(
    url_template: ,
    path_params: [, ] = None,
    query_params: [, ] = None,
    body: Optional[] = None,
)

```

Use this to POST content to a website.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url_template`  |  `[str]`  |  The url to make the request against, potentially includes curly braces {} to mark a section of a URL path as replaceable using path parameters.  |  _required_  |  
|  `path_params`  |  `dict[str, str]`  |  path parameters for use in the url_template  |  `None`  |  
|  `query_params`  |  `dict[str, str]`  |  query parameters  |  `None`  |  
|  `body`  |  `Optional[dict]`  |  the body of the request, sent as JSON  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-requests/llama_index/tools/requests/base.py`  
| 
```
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
```
 | 
```
defpost_request(
    self,
    url_template: str,
    path_params: dict[str, str] = None,
    query_params: dict[str, str] = None,
    body: Optional[dict] = None,
):
"""
    Use this to POST content to a website.

    Args:
        url_template ([str]): The url to make the request against, potentially includes curly
            braces {} to mark a section of a URL path as replaceable using path parameters.
        path_params (dict[str, str]): path parameters for use in the url_template
        query_params (dict[str, str]): query parameters
        body (Optional[dict]): the body of the request, sent as JSON

    """
    if not self._valid_url(url_template):
        return INVALID_URL_PROMPT

    url = self._replace_path_params(url_template, path_params)
    res = requests.post(
        url,
        headers=self._get_headers_for_url(url_template),
        params=query_params,
        json=body,
        timeout=self.timeout_seconds,
    )
    return res.json()

```
 |  
| --- | --- |  
###  patch_request [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/requests/#llama_index.tools.requests.RequestsToolSpec.patch_request "Permanent link")

```
patch_request(
    url_template: ,
    path_params: [, ] = None,
    query_params: [, ] = None,
    body: Optional[] = None,
)

```

Use this to PATCH content to a website.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url_template`  |  `[str]`  |  The url to make the request against, potentially includes curly braces {} to mark a section of a URL path as replaceable using path parameters.  |  _required_  |  
|  `path_params`  |  `dict[str, str]`  |  path parameters for use in the url_template  |  `None`  |  
|  `query_params`  |  `dict[str, str]`  |  query parameters  |  `None`  |  
|  `body`  |  `Optional[dict]`  |  the body of the request, sent as JSON  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-requests/llama_index/tools/requests/base.py`  
| 
```
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
```
 | 
```
defpatch_request(
    self,
    url_template: str,
    path_params: dict[str, str] = None,
    query_params: dict[str, str] = None,
    body: Optional[dict] = None,
):
"""
    Use this to PATCH content to a website.

    Args:
        url_template ([str]): The url to make the request against, potentially includes curly
            braces {} to mark a section of a URL path as replaceable using path parameters.
        path_params (dict[str, str]): path parameters for use in the url_template
        query_params (dict[str, str]): query parameters
        body (Optional[dict]): the body of the request, sent as JSON

    """
    if not self._valid_url(url_template):
        return INVALID_URL_PROMPT

    url = self._replace_path_params(url_template, path_params)
    res = requests.patch(
        url,
        headers=self._get_headers_for_url(url_template),
        params=query_params,
        json=body,
        timeout=self.timeout_seconds,
    )
    return res.json()

```
 |  
| --- | --- |  
###  put_request [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/requests/#llama_index.tools.requests.RequestsToolSpec.put_request "Permanent link")

```
put_request(
    url_template: ,
    path_params: [, ] = None,
    query_params: [, ] = None,
    body: Optional[] = None,
)

```

Use this to PUT content to a website.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url_template`  |  `[str]`  |  The url to make the request against, potentially includes curly braces {} to mark a section of a URL path as replaceable using path parameters.  |  _required_  |  
|  `path_params`  |  `dict[str, str]`  |  path parameters for use in the url_template  |  `None`  |  
|  `query_params`  |  `dict[str, str]`  |  query parameters  |  `None`  |  
|  `body`  |  `Optional[dict]`  |  the body of the request, sent as JSON  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-requests/llama_index/tools/requests/base.py`  
| 
```
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
```
 | 
```
defput_request(
    self,
    url_template: str,
    path_params: dict[str, str] = None,
    query_params: dict[str, str] = None,
    body: Optional[dict] = None,
):
"""
    Use this to PUT content to a website.

    Args:
        url_template ([str]): The url to make the request against, potentially includes curly
            braces {} to mark a section of a URL path as replaceable using path parameters.
        path_params (dict[str, str]): path parameters for use in the url_template
        query_params (dict[str, str]): query parameters
        body (Optional[dict]): the body of the request, sent as JSON

    """
    if not self._valid_url(url_template):
        return INVALID_URL_PROMPT

    url = self._replace_path_params(url_template, path_params)
    res = requests.put(
        url,
        headers=self._get_headers_for_url(url_template),
        params=query_params,
        json=body,
        timeout=self.timeout_seconds,
    )
    return res.json()

```
 |  
| --- | --- |  
###  delete_request [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/requests/#llama_index.tools.requests.RequestsToolSpec.delete_request "Permanent link")

```
delete_request(
    url_template: ,
    path_params: [, ] = None,
    query_params: [, ] = None,
    body: Optional[] = None,
)

```

Use this to DELETE content from a website.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url_template`  |  `[str]`  |  The url to make the request against, potentially includes curly braces {} to mark a section of a URL path as replaceable using path parameters.  |  _required_  |  
|  `path_params`  |  `dict[str, str]`  |  path parameters for use in the url_template  |  `None`  |  
|  `query_params`  |  `dict[str, str]`  |  query parameters  |  `None`  |  
|  `body`  |  `Optional[dict]`  |  the body of the request, sent as JSON (not typically used)  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-requests/llama_index/tools/requests/base.py`  
| 
```
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
```
 | 
```
defdelete_request(
    self,
    url_template: str,
    path_params: dict[str, str] = None,
    query_params: dict[str, str] = None,
    body: Optional[dict] = None,
):
"""
    Use this to DELETE content from a website.

    Args:
        url_template ([str]): The url to make the request against, potentially includes
            curly braces {} to mark a section of a URL path as replaceable using path
            parameters.
        path_params (dict[str, str]): path parameters for use in the url_template
        query_params (dict[str, str]): query parameters
        body (Optional[dict]): the body of the request, sent as JSON (not typically used)

    """
    if not self._valid_url(url_template):
        return INVALID_URL_PROMPT

    url = self._replace_path_params(url_template, path_params)
    res = requests.delete(
        url,
        headers=self._get_headers_for_url(url_template),
        params=query_params,
        json=body,
        timeout=self.timeout_seconds,
    )
    return res.json()

```
 |  
| --- | --- |  
options: members: - RequestsToolSpec
