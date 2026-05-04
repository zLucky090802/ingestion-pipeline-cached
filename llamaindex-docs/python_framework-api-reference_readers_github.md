# Github
##  GitHubRepositoryCollaboratorsReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubRepositoryCollaboratorsReader "Permanent link")
Bases: 
GitHub repository collaborators reader.
Retrieves the list of collaborators of a GitHub repository and returns a list of documents.
Examples:

```
>>> reader = GitHubRepositoryCollaboratorsReader("owner", "repo")
>>> colabs = reader.load_data()
>>> print(colabs)

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/collaborators/base.py`  
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
```
 | 
```
classGitHubRepositoryCollaboratorsReader(BaseReader):
"""
    GitHub repository collaborators reader.

    Retrieves the list of collaborators of a GitHub repository and returns a list of documents.

    Examples:
        >>> reader = GitHubRepositoryCollaboratorsReader("owner", "repo")
        >>> colabs = reader.load_data()
        >>> print(colabs)

    """

    classFilterType(enum.Enum):
"""
        Filter type.

        Used to determine whether the filter is inclusive or exclusive.
        """

        EXCLUDE = enum.auto()
        INCLUDE = enum.auto()

    def__init__(
        self,
        github_client: BaseGitHubCollaboratorsClient,
        owner: str,
        repo: str,
        verbose: bool = False,
    ):
"""
        Initialize params.

        Args:
            - github_client (BaseGitHubCollaboratorsClient): GitHub client.
            - owner (str): Owner of the repository.
            - repo (str): Name of the repository.
            - verbose (bool): Whether to print verbose messages.

        Raises:
            - `ValueError`: If the github_token is not provided and
                the GITHUB_TOKEN environment variable is not set.

        """
        super().__init__()

        self._owner = owner
        self._repo = repo
        self._verbose = verbose
        self._github_client = github_client

    defload_data(
        self,
    ) -> List[Document]:
"""
        GitHub repository collaborators reader.

        Retrieves the list of collaborators in a GitHub repository and converts them to documents.

        Each collaborator is converted to a document by doing the following:

            - The text of the document is the login.
            - The title of the document is also the login.
            - The extra_info of the document is a dictionary with the following keys:
                - login: str, the login of the user
                - type: str, the type of user e.g. "User"
                - site_admin: bool, whether the user has admin permissions
                - role_name: str, e.g. "admin"
                - name: str, the name of the user, if available
                - email: str, the email of the user, if available
                - permissions: str, the permissions of the user, if available


        :return: list of documents
        """
        documents = []
        page = 1
        # Loop until there are no more collaborators
        while True:
            collaborators: Dict = asyncio_run(
                self._github_client.get_collaborators(
                    self._owner, self._repo, page=page
                )
            )

            if len(collaborators) == 0:
                print_if_verbose(self._verbose, "No more collaborators found, stopping")

                break
            print_if_verbose(
                self._verbose,
                f"Found {len(collaborators)} collaborators in the repo page {page}",
            )
            page += 1
            for collab in collaborators:
                extra_info = {
                    "login": collab["login"],
                    "type": collab["type"],
                    "site_admin": collab["site_admin"],
                    "role_name": collab["role_name"],
                }
                if collab.get("name") is not None:
                    extra_info["name"] = collab["name"]
                if collab.get("email") is not None:
                    extra_info["email"] = collab["email"]
                if collab.get("permissions") is not None:
                    extra_info["permissions"] = collab["permissions"]
                document = Document(
                    doc_id=str(collab["login"]),
                    text=str(collab["login"]),  # unsure for this
                    extra_info=extra_info,
                )
                documents.append(document)

            print_if_verbose(self._verbose, f"Resulted in {len(documents)} documents")

        return documents

```
 |  
| --- | --- |  
###  FilterType [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubRepositoryCollaboratorsReader.FilterType "Permanent link")
Bases: `Enum`
Filter type.
Used to determine whether the filter is inclusive or exclusive.
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/collaborators/base.py`  
| 
```
55
56
57
58
59
60
61
62
63
```
 | 
```
classFilterType(enum.Enum):
"""
    Filter type.

    Used to determine whether the filter is inclusive or exclusive.
    """

    EXCLUDE = enum.auto()
    INCLUDE = enum.auto()

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubRepositoryCollaboratorsReader.load_data "Permanent link")

```
load_data() -> []

```

GitHub repository collaborators reader.
Retrieves the list of collaborators in a GitHub repository and converts them to documents.
Each collaborator is converted to a document by doing the following:

```
- The text of the document is the login.
- The title of the document is also the login.
- The extra_info of the document is a dictionary with the following keys:
    - login: str, the login of the user
    - type: str, the type of user e.g. "User"
    - site_admin: bool, whether the user has admin permissions
    - role_name: str, e.g. "admin"
    - name: str, the name of the user, if available
    - email: str, the email of the user, if available
    - permissions: str, the permissions of the user, if available

```

:return: list of documents
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/collaborators/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
) -> List[Document]:
"""
    GitHub repository collaborators reader.

    Retrieves the list of collaborators in a GitHub repository and converts them to documents.

    Each collaborator is converted to a document by doing the following:

        - The text of the document is the login.
        - The title of the document is also the login.
        - The extra_info of the document is a dictionary with the following keys:
            - login: str, the login of the user
            - type: str, the type of user e.g. "User"
            - site_admin: bool, whether the user has admin permissions
            - role_name: str, e.g. "admin"
            - name: str, the name of the user, if available
            - email: str, the email of the user, if available
            - permissions: str, the permissions of the user, if available


    :return: list of documents
    """
    documents = []
    page = 1
    # Loop until there are no more collaborators
    while True:
        collaborators: Dict = asyncio_run(
            self._github_client.get_collaborators(
                self._owner, self._repo, page=page
            )
        )

        if len(collaborators) == 0:
            print_if_verbose(self._verbose, "No more collaborators found, stopping")

            break
        print_if_verbose(
            self._verbose,
            f"Found {len(collaborators)} collaborators in the repo page {page}",
        )
        page += 1
        for collab in collaborators:
            extra_info = {
                "login": collab["login"],
                "type": collab["type"],
                "site_admin": collab["site_admin"],
                "role_name": collab["role_name"],
            }
            if collab.get("name") is not None:
                extra_info["name"] = collab["name"]
            if collab.get("email") is not None:
                extra_info["email"] = collab["email"]
            if collab.get("permissions") is not None:
                extra_info["permissions"] = collab["permissions"]
            document = Document(
                doc_id=str(collab["login"]),
                text=str(collab["login"]),  # unsure for this
                extra_info=extra_info,
            )
            documents.append(document)

        print_if_verbose(self._verbose, f"Resulted in {len(documents)} documents")

    return documents

```
 |  
| --- | --- |  
##  GitHubCollaboratorsClient [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubCollaboratorsClient "Permanent link")
An asynchronous client for interacting with the GitHub API for collaborators.
The client supports two authentication methods: 1. Personal Access Token (PAT) - passed as github_token or via GITHUB_TOKEN env var 2. GitHub App - passed as github_app_auth parameter
Examples:

```
>>> # Using Personal Access Token
>>> client = GitHubCollaboratorsClient("my_github_token")
>>> collaborators = client.get_collaborators("owner", "repo")
>>>
>>> # Using GitHub App
>>> fromllama_index.readers.github.github_app_authimport GitHubAppAuth
>>> app_auth = GitHubAppAuth(app_id="123", private_key=key, installation_id="456")
>>> client = GitHubCollaboratorsClient(github_app_auth=app_auth)

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/collaborators/github_client.py`  
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
```
 | 
```
classGitHubCollaboratorsClient:
"""
    An asynchronous client for interacting with the GitHub API for collaborators.

    The client supports two authentication methods:
    1. Personal Access Token (PAT) - passed as github_token or via GITHUB_TOKEN env var
    2. GitHub App - passed as github_app_auth parameter

    Examples:
        >>> # Using Personal Access Token
        >>> client = GitHubCollaboratorsClient("my_github_token")
        >>> collaborators = client.get_collaborators("owner", "repo")

        >>> # Using GitHub App
        >>> from llama_index.readers.github.github_app_auth import GitHubAppAuth
        >>> app_auth = GitHubAppAuth(app_id="123", private_key=key, installation_id="456")
        >>> client = GitHubCollaboratorsClient(github_app_auth=app_auth)

    """

    DEFAULT_BASE_URL = "https://api.github.com"
    DEFAULT_API_VERSION = "2022-11-28"

    def__init__(
        self,
        github_token: Optional[str] = None,
        github_app_auth: Optional[Union["GitHubAppAuth", Any]] = None,
        base_url: str = DEFAULT_BASE_URL,
        api_version: str = DEFAULT_API_VERSION,
        verbose: bool = False,
    ) -> None:
"""
        Initialize the GitHubCollaboratorsClient.

        Args:
            - github_token (str, optional): GitHub token for authentication.
                If not provided, the client will try to get it from
                the GITHUB_TOKEN environment variable. Mutually exclusive with github_app_auth.
            - github_app_auth (GitHubAppAuth, optional): GitHub App authentication handler.
                Mutually exclusive with github_token.
            - base_url (str): Base URL for the GitHub API
                (defaults to "https://api.github.com").
            - api_version (str): GitHub API version (defaults to "2022-11-28").
            - verbose (bool): Whether to print verbose output (defaults to False).

        Raises:
            ValueError: If neither github_token nor github_app_auth is provided,
                       or if both are provided.

        """
        # Validate authentication parameters
        if github_token is not None and github_app_auth is not None:
            raise ValueError(
                "Cannot provide both github_token and github_app_auth. "
                "Please use only one authentication method."
            )

        self._base_url = base_url
        self._api_version = api_version
        self._verbose = verbose
        self._github_app_auth = github_app_auth
        self._github_token = None

        # Set up authentication
        if github_app_auth is not None:
            self._use_github_app = True
        else:
            self._use_github_app = False
            if github_token is None:
                github_token = os.getenv("GITHUB_TOKEN")
                if github_token is None:
                    raise ValueError(
                        "Please provide a GitHub token or GitHub App authentication. "
                        + "You can pass github_token as an argument, "
                        + "set the GITHUB_TOKEN environment variable, "
                        + "or pass github_app_auth for GitHub App authentication."
                    )
            self._github_token = github_token

        self._endpoints = {
            "getCollaborators": "/repos/{owner}/{repo}/collaborators",
        }

        # Base headers (Authorization header will be added per-request)
        self._base_headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": f"{self._api_version}",
        }

        # For backward compatibility, keep _headers with PAT token
        if not self._use_github_app:
            self._headers = {
                **self._base_headers,
                "Authorization": f"Bearer {self._github_token}",
            }
        else:
            self._headers = self._base_headers.copy()

    defget_all_endpoints(self) -> Dict[str, str]:
"""Get all available endpoints."""
        return {**self._endpoints}

    async def_get_auth_headers(self) -> Dict[str, str]:
"""Get authentication headers."""
        if self._use_github_app:
            token = await self._github_app_auth.get_installation_token()
            return {
                **self._base_headers,
                "Authorization": f"Bearer {token}",
            }
        else:
            return self._headers

    async defrequest(
        self,
        endpoint: str,
        method: str,
        headers: Dict[str, Any] = {},
        params: Dict[str, Any] = {},
        **kwargs: Any,
    ) -> Any:
"""
        Makes an API request to the GitHub API.

        Args:
            - `endpoint (str)`: Name of the endpoint to make the request to.
            - `method (str)`: HTTP method to use for the request.
            - `headers (dict)`: HTTP headers to include in the request.
            - `**kwargs`: Keyword arguments to pass to the endpoint URL.

        Returns:
            - `response (httpx.Response)`: Response from the API request.

        Raises:
            - ImportError: If the `httpx` library is not installed.
            - httpx.HTTPError: If the API request fails.

        Examples:
            >>> response = client.request("getCollaborators", "GET",
                                owner="owner", repo="repo", state="all")

        """
        try:
            importhttpx
        except ImportError:
            raise ImportError(
                "`https` package not found, please run `pip install httpx`"
            )

        # Get authentication headers (may fetch fresh token for GitHub App)
        auth_headers = await self._get_auth_headers()
        _headers = {**auth_headers, **headers}

        _client: httpx.AsyncClient
        async with httpx.AsyncClient(
            headers=_headers, base_url=self._base_url, params=params
        ) as _client:
            try:
                response = await _client.request(
                    method, url=self._endpoints[endpoint].format(**kwargs)
                )
                response.raise_for_status()
            except httpx.HTTPError as excp:
                print(f"HTTP Exception for {excp.request.url}{excp}")
                raise excp  # noqa: TRY201
            return response

    async defget_collaborators(
        self,
        owner: str,
        repo: str,
        page: int = 1,
    ) -> Dict:
"""
        List collaborators in a repository.

        Args:
            - `owner (str)`: Owner of the repository.
            - `repo (str)`: Name of the repository.

        Returns:
            - See https://docs.github.com/en/rest/collaborators/collaborators?apiVersion=2022-11-28#list-repository-collaborators

        Examples:
            >>> repo_collaborators = client.get_collaborators("owner", "repo")

        """
        return (
            await self.request(
                endpoint="getCollaborators",
                method="GET",
                params={
                    "per_page": 100,
                    "page": page,
                },
                owner=owner,
                repo=repo,
            )
        ).json()

```
 |  
| --- | --- |  
###  get_all_endpoints [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubCollaboratorsClient.get_all_endpoints "Permanent link")

```
get_all_endpoints() -> [, ]

```

Get all available endpoints.
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/collaborators/github_client.py`  
| 
```
132
133
134
```
 | 
```
defget_all_endpoints(self) -> Dict[str, str]:
"""Get all available endpoints."""
    return {**self._endpoints}

```
 |  
| --- | --- |  
###  request [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubCollaboratorsClient.request "Permanent link")

```
request(
    endpoint: ,
    method: ,
    headers: [, ] = {},
    params: [, ] = {},
    **kwargs: 
) -> 

```

Makes an API request to the GitHub API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `- `endpoint (str)``  |  Name of the endpoint to make the request to.  |  _required_  |  
|  `- `method (str)``  |  HTTP method to use for the request.  |  _required_  |  
|  `- `headers (dict)``  |  HTTP headers to include in the request.  |  _required_  |  
|  `- `**kwargs``  |  Keyword arguments to pass to the endpoint URL.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
| 
  * `response (httpx.Response)`: Response from the API request.

 |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `-ImportError`  |  If the `httpx` library is not installed.  |  
|  `-HTTPError`  |  If the API request fails.  |  
Examples:

```
>>> response = client.request("getCollaborators", "GET",
                    owner="owner", repo="repo", state="all")

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/collaborators/github_client.py`  
| 
```
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
```
 | 
```
async defrequest(
    self,
    endpoint: str,
    method: str,
    headers: Dict[str, Any] = {},
    params: Dict[str, Any] = {},
    **kwargs: Any,
) -> Any:
"""
    Makes an API request to the GitHub API.

    Args:
        - `endpoint (str)`: Name of the endpoint to make the request to.
        - `method (str)`: HTTP method to use for the request.
        - `headers (dict)`: HTTP headers to include in the request.
        - `**kwargs`: Keyword arguments to pass to the endpoint URL.

    Returns:
        - `response (httpx.Response)`: Response from the API request.

    Raises:
        - ImportError: If the `httpx` library is not installed.
        - httpx.HTTPError: If the API request fails.

    Examples:
        >>> response = client.request("getCollaborators", "GET",
                            owner="owner", repo="repo", state="all")

    """
    try:
        importhttpx
    except ImportError:
        raise ImportError(
            "`https` package not found, please run `pip install httpx`"
        )

    # Get authentication headers (may fetch fresh token for GitHub App)
    auth_headers = await self._get_auth_headers()
    _headers = {**auth_headers, **headers}

    _client: httpx.AsyncClient
    async with httpx.AsyncClient(
        headers=_headers, base_url=self._base_url, params=params
    ) as _client:
        try:
            response = await _client.request(
                method, url=self._endpoints[endpoint].format(**kwargs)
            )
            response.raise_for_status()
        except httpx.HTTPError as excp:
            print(f"HTTP Exception for {excp.request.url}{excp}")
            raise excp  # noqa: TRY201
        return response

```
 |  
| --- | --- |  
###  get_collaborators [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubCollaboratorsClient.get_collaborators "Permanent link")

```
get_collaborators(
    owner: , repo: , page:  = 1
) -> 

```

List collaborators in a repository.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `- `owner (str)``  |  Owner of the repository.  |  _required_  |  
|  `- `repo (str)``  |  Name of the repository.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict`  | 
  * See https://docs.github.com/en/rest/collaborators/collaborators?apiVersion=2022-11-28#list-repository-collaborators

 |  
Examples:

```
>>> repo_collaborators = client.get_collaborators("owner", "repo")

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/collaborators/github_client.py`  
| 
```
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
```
 | 
```
async defget_collaborators(
    self,
    owner: str,
    repo: str,
    page: int = 1,
) -> Dict:
"""
    List collaborators in a repository.

    Args:
        - `owner (str)`: Owner of the repository.
        - `repo (str)`: Name of the repository.

    Returns:
        - See https://docs.github.com/en/rest/collaborators/collaborators?apiVersion=2022-11-28#list-repository-collaborators

    Examples:
        >>> repo_collaborators = client.get_collaborators("owner", "repo")

    """
    return (
        await self.request(
            endpoint="getCollaborators",
            method="GET",
            params={
                "per_page": 100,
                "page": page,
            },
            owner=owner,
            repo=repo,
        )
    ).json()

```
 |  
| --- | --- |  
##  GitHubIssuesClient [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubIssuesClient "Permanent link")
An asynchronous client for interacting with the GitHub API for issues.
The client supports two authentication methods: 1. Personal Access Token (PAT) - passed as github_token or via GITHUB_TOKEN env var 2. GitHub App - passed as github_app_auth parameter
Examples:

```
>>> # Using Personal Access Token
>>> client = GitHubIssuesClient("my_github_token")
>>> issues = client.get_issues("owner", "repo")
>>>
>>> # Using GitHub App
>>> fromllama_index.readers.github.github_app_authimport GitHubAppAuth
>>> app_auth = GitHubAppAuth(app_id="123", private_key=key, installation_id="456")
>>> client = GitHubIssuesClient(github_app_auth=app_auth)

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/issues/github_client.py`  
| 
```
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
classGitHubIssuesClient:
"""
    An asynchronous client for interacting with the GitHub API for issues.

    The client supports two authentication methods:
    1. Personal Access Token (PAT) - passed as github_token or via GITHUB_TOKEN env var
    2. GitHub App - passed as github_app_auth parameter

    Examples:
        >>> # Using Personal Access Token
        >>> client = GitHubIssuesClient("my_github_token")
        >>> issues = client.get_issues("owner", "repo")

        >>> # Using GitHub App
        >>> from llama_index.readers.github.github_app_auth import GitHubAppAuth
        >>> app_auth = GitHubAppAuth(app_id="123", private_key=key, installation_id="456")
        >>> client = GitHubIssuesClient(github_app_auth=app_auth)

    """

    DEFAULT_BASE_URL = "https://api.github.com"
    DEFAULT_API_VERSION = "2022-11-28"

    def__init__(
        self,
        github_token: Optional[str] = None,
        github_app_auth: Optional[Union["GitHubAppAuth", Any]] = None,
        base_url: str = DEFAULT_BASE_URL,
        api_version: str = DEFAULT_API_VERSION,
        verbose: bool = False,
    ) -> None:
"""
        Initialize the GitHubIssuesClient.

        Args:
            - github_token (str, optional): GitHub token for authentication.
                If not provided, the client will try to get it from
                the GITHUB_TOKEN environment variable. Mutually exclusive with github_app_auth.
            - github_app_auth (GitHubAppAuth, optional): GitHub App authentication handler.
                Mutually exclusive with github_token.
            - base_url (str): Base URL for the GitHub API
                (defaults to "https://api.github.com").
            - api_version (str): GitHub API version (defaults to "2022-11-28").
            - verbose (bool): Whether to print verbose output (defaults to False).

        Raises:
            ValueError: If neither github_token nor github_app_auth is provided,
                       or if both are provided.

        """
        # Validate authentication parameters
        if github_token is not None and github_app_auth is not None:
            raise ValueError(
                "Cannot provide both github_token and github_app_auth. "
                "Please use only one authentication method."
            )

        self._base_url = base_url
        self._api_version = api_version
        self._verbose = verbose
        self._github_app_auth = github_app_auth
        self._github_token = None

        # Set up authentication
        if github_app_auth is not None:
            self._use_github_app = True
        else:
            self._use_github_app = False
            if github_token is None:
                github_token = os.getenv("GITHUB_TOKEN")
                if github_token is None:
                    raise ValueError(
                        "Please provide a GitHub token or GitHub App authentication. "
                        + "You can pass github_token as an argument, "
                        + "set the GITHUB_TOKEN environment variable, "
                        + "or pass github_app_auth for GitHub App authentication."
                    )
            self._github_token = github_token

        self._endpoints = {
            "getIssues": "/repos/{owner}/{repo}/issues",
        }

        # Base headers (Authorization header will be added per-request)
        self._base_headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": f"{self._api_version}",
        }

        # For backward compatibility, keep _headers with PAT token
        if not self._use_github_app:
            self._headers = {
                **self._base_headers,
                "Authorization": f"Bearer {self._github_token}",
            }
        else:
            self._headers = self._base_headers.copy()

    defget_all_endpoints(self) -> Dict[str, str]:
"""Get all available endpoints."""
        return {**self._endpoints}

    async def_get_auth_headers(self) -> Dict[str, str]:
"""Get authentication headers."""
        if self._use_github_app:
            token = await self._github_app_auth.get_installation_token()
            return {
                **self._base_headers,
                "Authorization": f"Bearer {token}",
            }
        else:
            return self._headers

    async defrequest(
        self,
        endpoint: str,
        method: str,
        headers: Dict[str, Any] = {},
        params: Dict[str, Any] = {},
        **kwargs: Any,
    ) -> Any:
"""
        Makes an API request to the GitHub API.

        Args:
            - `endpoint (str)`: Name of the endpoint to make the request to.
            - `method (str)`: HTTP method to use for the request.
            - `headers (dict)`: HTTP headers to include in the request.
            - `**kwargs`: Keyword arguments to pass to the endpoint URL.

        Returns:
            - `response (httpx.Response)`: Response from the API request.

        Raises:
            - ImportError: If the `httpx` library is not installed.
            - httpx.HTTPError: If the API request fails.

        Examples:
            >>> response = client.request("getIssues", "GET",
                                owner="owner", repo="repo", state="all")

        """
        try:
            importhttpx
        except ImportError:
            raise ImportError(
                "`https` package not found, please run `pip install httpx`"
            )

        # Get authentication headers (may fetch fresh token for GitHub App)
        auth_headers = await self._get_auth_headers()
        _headers = {**auth_headers, **headers}

        _client: httpx.AsyncClient
        async with httpx.AsyncClient(
            headers=_headers,
            base_url=self._base_url,
            params=params,
            follow_redirects=True,
        ) as _client:
            try:
                response = await _client.request(
                    method, url=self._endpoints[endpoint].format(**kwargs)
                )
                response.raise_for_status()
            except httpx.HTTPError as excp:
                print(f"HTTP Exception for {excp.request.url}{excp}")
                raise excp  # noqa: TRY201
            return response

    async defget_issues(
        self,
        owner: str,
        repo: str,
        state: str = "open",
        page: int = 1,
    ) -> Dict:
"""
        List issues in a repository.

        Note: GitHub's REST API considers every pull request an issue, but not every issue is a pull request.
        For this reason, "Issues" endpoints may return both issues and pull requests in the response.
        You can identify pull requests by the pull_request key.
        Be aware that the id of a pull request returned from "Issues" endpoints will be an issue id.
        To find out the pull request id, use the "List pull requests" endpoint.

        Args:
            - `owner (str)`: Owner of the repository.
            - `repo (str)`: Name of the repository.
            - `state (str)`: Indicates the state of the issues to return.
                Default: open
                Can be one of: open, closed, all.

        Returns:
            - See https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues

        Examples:
            >>> repo_issues = client.get_issues("owner", "repo")

        """
        return (
            await self.request(
                endpoint="getIssues",
                method="GET",
                params={
                    "state": state,
                    "per_page": 100,
                    "sort": "updated",
                    "direction": "desc",
                    "page": page,
                },
                owner=owner,
                repo=repo,
            )
        ).json()

```
 |  
| --- | --- |  
###  get_all_endpoints [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubIssuesClient.get_all_endpoints "Permanent link")

```
get_all_endpoints() -> [, ]

```

Get all available endpoints.
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/issues/github_client.py`  
| 
```
133
134
135
```
 | 
```
defget_all_endpoints(self) -> Dict[str, str]:
"""Get all available endpoints."""
    return {**self._endpoints}

```
 |  
| --- | --- |  
###  request [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubIssuesClient.request "Permanent link")

```
request(
    endpoint: ,
    method: ,
    headers: [, ] = {},
    params: [, ] = {},
    **kwargs: 
) -> 

```

Makes an API request to the GitHub API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `- `endpoint (str)``  |  Name of the endpoint to make the request to.  |  _required_  |  
|  `- `method (str)``  |  HTTP method to use for the request.  |  _required_  |  
|  `- `headers (dict)``  |  HTTP headers to include in the request.  |  _required_  |  
|  `- `**kwargs``  |  Keyword arguments to pass to the endpoint URL.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
| 
  * `response (httpx.Response)`: Response from the API request.

 |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `-ImportError`  |  If the `httpx` library is not installed.  |  
|  `-HTTPError`  |  If the API request fails.  |  
Examples:

```
>>> response = client.request("getIssues", "GET",
                    owner="owner", repo="repo", state="all")

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/issues/github_client.py`  
| 
```
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
```
 | 
```
async defrequest(
    self,
    endpoint: str,
    method: str,
    headers: Dict[str, Any] = {},
    params: Dict[str, Any] = {},
    **kwargs: Any,
) -> Any:
"""
    Makes an API request to the GitHub API.

    Args:
        - `endpoint (str)`: Name of the endpoint to make the request to.
        - `method (str)`: HTTP method to use for the request.
        - `headers (dict)`: HTTP headers to include in the request.
        - `**kwargs`: Keyword arguments to pass to the endpoint URL.

    Returns:
        - `response (httpx.Response)`: Response from the API request.

    Raises:
        - ImportError: If the `httpx` library is not installed.
        - httpx.HTTPError: If the API request fails.

    Examples:
        >>> response = client.request("getIssues", "GET",
                            owner="owner", repo="repo", state="all")

    """
    try:
        importhttpx
    except ImportError:
        raise ImportError(
            "`https` package not found, please run `pip install httpx`"
        )

    # Get authentication headers (may fetch fresh token for GitHub App)
    auth_headers = await self._get_auth_headers()
    _headers = {**auth_headers, **headers}

    _client: httpx.AsyncClient
    async with httpx.AsyncClient(
        headers=_headers,
        base_url=self._base_url,
        params=params,
        follow_redirects=True,
    ) as _client:
        try:
            response = await _client.request(
                method, url=self._endpoints[endpoint].format(**kwargs)
            )
            response.raise_for_status()
        except httpx.HTTPError as excp:
            print(f"HTTP Exception for {excp.request.url}{excp}")
            raise excp  # noqa: TRY201
        return response

```
 |  
| --- | --- |  
###  get_issues [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubIssuesClient.get_issues "Permanent link")

```
get_issues(
    owner: ,
    repo: ,
    state:  = "open",
    page:  = 1,
) -> 

```

List issues in a repository.
Note: GitHub's REST API considers every pull request an issue, but not every issue is a pull request. For this reason, "Issues" endpoints may return both issues and pull requests in the response. You can identify pull requests by the pull_request key. Be aware that the id of a pull request returned from "Issues" endpoints will be an issue id. To find out the pull request id, use the "List pull requests" endpoint.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `- `owner (str)``  |  Owner of the repository.  |  _required_  |  
|  `- `repo (str)``  |  Name of the repository.  |  _required_  |  
|  `- `state (str)``  |  Indicates the state of the issues to return. Default: open Can be one of: open, closed, all.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict`  | 
  * See https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues

 |  
Examples:

```
>>> repo_issues = client.get_issues("owner", "repo")

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/issues/github_client.py`  
| 
```
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
async defget_issues(
    self,
    owner: str,
    repo: str,
    state: str = "open",
    page: int = 1,
) -> Dict:
"""
    List issues in a repository.

    Note: GitHub's REST API considers every pull request an issue, but not every issue is a pull request.
    For this reason, "Issues" endpoints may return both issues and pull requests in the response.
    You can identify pull requests by the pull_request key.
    Be aware that the id of a pull request returned from "Issues" endpoints will be an issue id.
    To find out the pull request id, use the "List pull requests" endpoint.

    Args:
        - `owner (str)`: Owner of the repository.
        - `repo (str)`: Name of the repository.
        - `state (str)`: Indicates the state of the issues to return.
            Default: open
            Can be one of: open, closed, all.

    Returns:
        - See https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues

    Examples:
        >>> repo_issues = client.get_issues("owner", "repo")

    """
    return (
        await self.request(
            endpoint="getIssues",
            method="GET",
            params={
                "state": state,
                "per_page": 100,
                "sort": "updated",
                "direction": "desc",
                "page": page,
            },
            owner=owner,
            repo=repo,
        )
    ).json()

```
 |  
| --- | --- |  
##  GitHubRepositoryIssuesReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubRepositoryIssuesReader "Permanent link")
Bases: 
GitHub repository issues reader.
Retrieves the list of issues of a GitHub repository and returns a list of documents.
Examples:

```
>>> reader = GitHubRepositoryIssuesReader("owner", "repo")
>>> issues = reader.load_data()
>>> print(issues)

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/issues/base.py`  
| 
```
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
```
 | 
```
classGitHubRepositoryIssuesReader(BaseReader):
"""
    GitHub repository issues reader.

    Retrieves the list of issues of a GitHub repository and returns a list of documents.

    Examples:
        >>> reader = GitHubRepositoryIssuesReader("owner", "repo")
        >>> issues = reader.load_data()
        >>> print(issues)

    """

    classIssueState(enum.Enum):
"""
        Issue type.

        Used to decide what issues to retrieve.

        Attributes:
            - OPEN: Just open issues. This is the default.
            - CLOSED: Just closed issues.
            - ALL: All issues, open and closed.

        """

        OPEN = "open"
        CLOSED = "closed"
        ALL = "all"

    classFilterType(enum.Enum):
"""
        Filter type.

        Used to determine whether the filter is inclusive or exclusive.
        """

        EXCLUDE = enum.auto()
        INCLUDE = enum.auto()

    def__init__(
        self,
        github_client: BaseGitHubIssuesClient,
        owner: str,
        repo: str,
        verbose: bool = False,
    ):
"""
        Initialize params.

        Args:
            - github_client (BaseGitHubIssuesClient): GitHub client.
            - owner (str): Owner of the repository.
            - repo (str): Name of the repository.
            - verbose (bool): Whether to print verbose messages.

        Raises:
            - `ValueError`: If the github_token is not provided and
                the GITHUB_TOKEN environment variable is not set.

        """
        super().__init__()

        self._owner = owner
        self._repo = repo
        self._verbose = verbose
        self._github_client = github_client

    defload_data(
        self,
        state: Optional[IssueState] = IssueState.OPEN,
        labelFilters: Optional[List[Tuple[str, FilterType]]] = None,
    ) -> List[Document]:
"""
        Load issues from a repository and converts them to documents.

        Each issue is converted to a document by doing the following:

        - The text of the document is the concatenation of the title and the body of the issue.
        - The title of the document is the title of the issue.
        - The doc_id of the document is the issue number.
        - The extra_info of the document is a dictionary with the following keys:
            - state: State of the issue.
            - created_at: Date when the issue was created.
            - closed_at: Date when the issue was closed. Only present if the issue is closed.
            - url: URL of the issue.
            - assignee: Login of the user assigned to the issue. Only present if the issue is assigned.
        - The embedding of the document is None.
        - The doc_hash of the document is None.

        Args:
            - state (IssueState): State of the issues to retrieve. Default is IssueState.OPEN.
            - labelFilters: an optional list of filters to apply to the issue list based on labels.

        :return: list of documents

        """
        documents = []
        page = 1
        # Loop until there are no more issues
        while True:
            issues: Dict = asyncio_run(
                self._github_client.get_issues(
                    self._owner, self._repo, state=state.value, page=page
                )
            )

            if len(issues) == 0:
                print_if_verbose(self._verbose, "No more issues found, stopping")

                break
            print_if_verbose(
                self._verbose, f"Found {len(issues)} issues in the repo page {page}"
            )
            page += 1
            filterCount = 0
            for issue in issues:
                if not self._must_include(labelFilters, issue):
                    filterCount += 1
                    continue
                title = issue["title"]
                body = issue["body"]
                document = Document(
                    doc_id=str(issue["number"]),
                    text=f"{title}\n{body}",
                )
                extra_info = {
                    "state": issue["state"],
                    "created_at": issue["created_at"],
                    # url is the API URL
                    "url": issue["url"],
                    # source is the HTML URL, more convenient for humans
                    "source": issue["html_url"],
                }
                if issue["closed_at"] is not None:
                    extra_info["closed_at"] = issue["closed_at"]
                if issue["assignee"] is not None:
                    extra_info["assignee"] = issue["assignee"]["login"]
                if issue["labels"] is not None:
                    extra_info["labels"] = [label["name"] for label in issue["labels"]]
                document.extra_info = extra_info
                documents.append(document)

            print_if_verbose(self._verbose, f"Resulted in {len(documents)} documents")
            if labelFilters is not None:
                print_if_verbose(self._verbose, f"Filtered out {filterCount} issues")

        return documents

    def_must_include(self, labelFilters, issue):
        if labelFilters is None:
            return True
        labels = [label["name"] for label in issue["labels"]]
        for labelFilter in labelFilters:
            label = labelFilter[0]
            filterType = labelFilter[1]
            # Only include issues with the label and value
            if filterType == self.FilterType.INCLUDE:
                return label in labels
            elif filterType == self.FilterType.EXCLUDE:
                return label not in labels

        return True

```
 |  
| --- | --- |  
###  IssueState [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubRepositoryIssuesReader.IssueState "Permanent link")
Bases: `Enum`
Issue type.
Used to decide what issues to retrieve.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
|  Just open issues. This is the default.  |  
|  `CLOSED`  |  Just closed issues.  |  
|  All issues, open and closed.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/issues/base.py`  
| 
```
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
```
 | 
```
classIssueState(enum.Enum):
"""
    Issue type.

    Used to decide what issues to retrieve.

    Attributes:
        - OPEN: Just open issues. This is the default.
        - CLOSED: Just closed issues.
        - ALL: All issues, open and closed.

    """

    OPEN = "open"
    CLOSED = "closed"
    ALL = "all"

```
 |  
| --- | --- |  
###  FilterType [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubRepositoryIssuesReader.FilterType "Permanent link")
Bases: `Enum`
Filter type.
Used to determine whether the filter is inclusive or exclusive.
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/issues/base.py`  
| 
```
73
74
75
76
77
78
79
80
81
```
 | 
```
classFilterType(enum.Enum):
"""
    Filter type.

    Used to determine whether the filter is inclusive or exclusive.
    """

    EXCLUDE = enum.auto()
    INCLUDE = enum.auto()

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubRepositoryIssuesReader.load_data "Permanent link")

```
load_data(
    state: Optional[] = ,
    labelFilters: Optional[
        [Tuple[, ]]
    ] = None,
) -> []

```

Load issues from a repository and converts them to documents.
Each issue is converted to a document by doing the following:
  * The text of the document is the concatenation of the title and the body of the issue.
  * The title of the document is the title of the issue.
  * The doc_id of the document is the issue number.
  * The extra_info of the document is a dictionary with the following keys:
    * state: State of the issue.
    * created_at: Date when the issue was created.
    * closed_at: Date when the issue was closed. Only present if the issue is closed.
    * url: URL of the issue.
    * assignee: Login of the user assigned to the issue. Only present if the issue is assigned.
  * The embedding of the document is None.
  * The doc_hash of the document is None.


Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `- state`  |   |  State of the issues to retrieve. Default is IssueState.OPEN.  |  _required_  |  
|  `- labelFilters`  |  an optional list of filters to apply to the issue list based on labels.  |  _required_  |  
:return: list of documents
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/issues/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    state: Optional[IssueState] = IssueState.OPEN,
    labelFilters: Optional[List[Tuple[str, FilterType]]] = None,
) -> List[Document]:
"""
    Load issues from a repository and converts them to documents.

    Each issue is converted to a document by doing the following:

    - The text of the document is the concatenation of the title and the body of the issue.
    - The title of the document is the title of the issue.
    - The doc_id of the document is the issue number.
    - The extra_info of the document is a dictionary with the following keys:
        - state: State of the issue.
        - created_at: Date when the issue was created.
        - closed_at: Date when the issue was closed. Only present if the issue is closed.
        - url: URL of the issue.
        - assignee: Login of the user assigned to the issue. Only present if the issue is assigned.
    - The embedding of the document is None.
    - The doc_hash of the document is None.

    Args:
        - state (IssueState): State of the issues to retrieve. Default is IssueState.OPEN.
        - labelFilters: an optional list of filters to apply to the issue list based on labels.

    :return: list of documents

    """
    documents = []
    page = 1
    # Loop until there are no more issues
    while True:
        issues: Dict = asyncio_run(
            self._github_client.get_issues(
                self._owner, self._repo, state=state.value, page=page
            )
        )

        if len(issues) == 0:
            print_if_verbose(self._verbose, "No more issues found, stopping")

            break
        print_if_verbose(
            self._verbose, f"Found {len(issues)} issues in the repo page {page}"
        )
        page += 1
        filterCount = 0
        for issue in issues:
            if not self._must_include(labelFilters, issue):
                filterCount += 1
                continue
            title = issue["title"]
            body = issue["body"]
            document = Document(
                doc_id=str(issue["number"]),
                text=f"{title}\n{body}",
            )
            extra_info = {
                "state": issue["state"],
                "created_at": issue["created_at"],
                # url is the API URL
                "url": issue["url"],
                # source is the HTML URL, more convenient for humans
                "source": issue["html_url"],
            }
            if issue["closed_at"] is not None:
                extra_info["closed_at"] = issue["closed_at"]
            if issue["assignee"] is not None:
                extra_info["assignee"] = issue["assignee"]["login"]
            if issue["labels"] is not None:
                extra_info["labels"] = [label["name"] for label in issue["labels"]]
            document.extra_info = extra_info
            documents.append(document)

        print_if_verbose(self._verbose, f"Resulted in {len(documents)} documents")
        if labelFilters is not None:
            print_if_verbose(self._verbose, f"Filtered out {filterCount} issues")

    return documents

```
 |  
| --- | --- |  
##  GithubClient [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GithubClient "Permanent link")
An asynchronous client for interacting with the Github API.
This client is used for making API requests to Github. It provides methods for accessing the Github API endpoints. The client supports two authentication methods: 1. Personal Access Token (PAT) - passed as github_token or via GITHUB_TOKEN env var 2. GitHub App - passed as github_app_auth parameter
Examples:

```
>>> # Using Personal Access Token
>>> client = GithubClient("my_github_token")
>>> branch_info = client.get_branch("owner", "repo", "branch")
>>>
>>> # Using GitHub App
>>> fromllama_index.readers.github.github_app_authimport GitHubAppAuth
>>> with open("private-key.pem", "r") as f:
...     private_key = f.read()
>>> app_auth = GitHubAppAuth(
...     app_id="123456",
...     private_key=private_key,
...     installation_id="789012"
... )
>>> client = GithubClient(github_app_auth=app_auth)

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/repository/github_client.py`  
| 
```
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
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
```
 | 
```
classGithubClient:
"""
    An asynchronous client for interacting with the Github API.

    This client is used for making API requests to Github.
    It provides methods for accessing the Github API endpoints.
    The client supports two authentication methods:
    1. Personal Access Token (PAT) - passed as github_token or via GITHUB_TOKEN env var
    2. GitHub App - passed as github_app_auth parameter

    Examples:
        >>> # Using Personal Access Token
        >>> client = GithubClient("my_github_token")
        >>> branch_info = client.get_branch("owner", "repo", "branch")

        >>> # Using GitHub App
        >>> from llama_index.readers.github.github_app_auth import GitHubAppAuth
        >>> with open("private-key.pem", "r") as f:
        ...     private_key = f.read()
        >>> app_auth = GitHubAppAuth(
        ...     app_id="123456",
        ...     private_key=private_key,
        ...     installation_id="789012"
        ... )
        >>> client = GithubClient(github_app_auth=app_auth)

    """

    DEFAULT_BASE_URL = "https://api.github.com"
    DEFAULT_API_VERSION = "2022-11-28"

    def__init__(
        self,
        github_token: Optional[str] = None,
        github_app_auth: Optional[Union["GitHubAppAuth", Any]] = None,
        base_url: str = DEFAULT_BASE_URL,
        api_version: str = DEFAULT_API_VERSION,
        verbose: bool = False,
        fail_on_http_error: bool = True,
    ) -> None:
"""
        Initialize the GithubClient.

        Args:
            - github_token (str, optional): Github token for authentication.
                If not provided, the client will try to get it from
                the GITHUB_TOKEN environment variable. Mutually exclusive with github_app_auth.
            - github_app_auth (GitHubAppAuth, optional): GitHub App authentication handler.
                Mutually exclusive with github_token.
            - base_url (str): Base URL for the Github API
                (defaults to "https://api.github.com").
            - api_version (str): Github API version (defaults to "2022-11-28").
            - verbose (bool): Whether to print verbose output (defaults to False).
            - fail_on_http_error (bool): Whether to raise an exception on HTTP errors (defaults to True).

        Raises:
            ValueError: If neither github_token nor github_app_auth is provided,
                       or if both are provided.

        """
        # Validate authentication parameters
        if github_token is not None and github_app_auth is not None:
            raise ValueError(
                "Cannot provide both github_token and github_app_auth. "
                "Please use only one authentication method."
            )

        self._base_url = base_url
        self._api_version = api_version
        self._verbose = verbose
        self._fail_on_http_error = fail_on_http_error
        self._github_app_auth = github_app_auth
        self._github_token = None

        # Set up authentication
        if github_app_auth is not None:
            # Using GitHub App authentication
            self._use_github_app = True
        else:
            # Using PAT authentication
            self._use_github_app = False
            if github_token is None:
                github_token = os.getenv("GITHUB_TOKEN")
                if github_token is None:
                    raise ValueError(
                        "Please provide a Github token or GitHub App authentication. "
                        + "You can pass github_token as an argument, "
                        + "set the GITHUB_TOKEN environment variable, "
                        + "or pass github_app_auth for GitHub App authentication."
                    )
            self._github_token = github_token

        self._endpoints = {
            "getTree": "/repos/{owner}/{repo}/git/trees/{tree_sha}",
            "getBranch": "/repos/{owner}/{repo}/branches/{branch}",
            "getBlob": "/repos/{owner}/{repo}/git/blobs/{file_sha}",
            "getCommit": "/repos/{owner}/{repo}/commits/{commit_sha}",
            "getContent": "/repos/{owner}/{repo}/contents/{path}",
        }

        # Base headers (Authorization header will be added per-request)
        self._base_headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": f"{self._api_version}",
        }

        # For backward compatibility, keep _headers with PAT token
        if not self._use_github_app:
            self._headers = {
                **self._base_headers,
                "Authorization": f"Bearer {self._github_token}",
            }
        else:
            # Headers will be generated per-request for GitHub App
            self._headers = self._base_headers.copy()

    defget_all_endpoints(self) -> Dict[str, str]:
"""Get all available endpoints."""
        return {**self._endpoints}

    async def_get_auth_headers(self) -> Dict[str, str]:
"""
        Get authentication headers.

        For PAT authentication, returns cached headers.
        For GitHub App authentication, fetches a fresh installation token if needed.

        Returns:
            Dictionary containing authentication headers.

        """
        if self._use_github_app:
            # Get fresh token from GitHub App auth
            token = await self._github_app_auth.get_installation_token()
            return {
                **self._base_headers,
                "Authorization": f"Bearer {token}",
            }
        else:
            # Return cached headers with PAT
            return self._headers

    async defrequest(
        self,
        endpoint: str,
        method: str,
        headers: Dict[str, Any] = {},
        timeout: Optional[int] = 5,
        retries: int = 0,
        **kwargs: Any,
    ) -> Any:
"""
        Make an API request to the Github API.

        This method is used for making API requests to the Github API.
        It is used internally by the other methods in the client.

        Args:
            - `endpoint (str)`: Name of the endpoint to make the request to.
            - `method (str)`: HTTP method to use for the request.
            - `headers (dict)`: HTTP headers to include in the request.
            - `timeout (int or None)`: Timeout for the request in seconds. Default is 5.
            - `retries (int)`: Number of retries for the request. Default is 0.
            - `**kwargs`: Keyword arguments to pass to the endpoint URL.

        Returns:
            - `response (httpx.Response)`: Response from the API request.

        Raises:
            - ImportError: If the `httpx` library is not installed.
            - httpx.HTTPError: If the API request fails and fail_on_http_error is True.

        Examples:
            >>> response = client.request("getTree", "GET",
                                owner="owner", repo="repo",
                                tree_sha="tree_sha", timeout=5, retries=0)

        """
        try:
            importhttpx
        except ImportError:
            raise ImportError(
                "Please install httpx to use the GithubRepositoryReader. "
                "You can do so by running `pip install httpx`."
            )

        # Get authentication headers (may fetch fresh token for GitHub App)
        auth_headers = await self._get_auth_headers()
        _headers = {**auth_headers, **headers}

        _client: httpx.AsyncClient
        async with httpx.AsyncClient(
            headers=_headers,
            base_url=self._base_url,
            timeout=timeout,
            transport=httpx.AsyncHTTPTransport(retries=retries),
        ) as _client:
            try:
                response = await _client.request(
                    method, url=self._endpoints[endpoint].format(**kwargs)
                )
            except httpx.HTTPError as excp:
                print(f"HTTP Exception for {excp.request.url}{excp}")
                raise excp  # noqa: TRY201
            return response

    async defget_branch(
        self,
        owner: str,
        repo: str,
        branch: Optional[str] = None,
        branch_name: Optional[str] = None,
        timeout: Optional[int] = 5,
        retries: int = 0,
    ) -> GitBranchResponseModel:
"""
        Get information about a branch. (Github API endpoint: getBranch).

        Args:
            - `owner (str)`: Owner of the repository.
            - `repo (str)`: Name of the repository.
            - `branch (str)`: Name of the branch.
            - `branch_name (str)`: Name of the branch (alternative to `branch`).
            - `timeout (int or None)`: Timeout for the request in seconds. Default is 5.
            - `retries (int)`: Number of retries for the request. Default is 0.

        Returns:
            - `branch_info (GitBranchResponseModel)`: Information about the branch.

        Examples:
            >>> branch_info = client.get_branch("owner", "repo", "branch")

        """
        if branch is None:
            if branch_name is None:
                raise ValueError("Either branch or branch_name must be provided.")
            branch = branch_name

        return GitBranchResponseModel.from_json(
            (
                await self.request(
                    "getBranch",
                    "GET",
                    owner=owner,
                    repo=repo,
                    branch=branch,
                    timeout=timeout,
                    retries=retries,
                )
            ).text
        )

    async defget_tree(
        self,
        owner: str,
        repo: str,
        tree_sha: str,
        timeout: Optional[int] = 5,
        retries: int = 0,
    ) -> GitTreeResponseModel:
"""
        Get information about a tree. (Github API endpoint: getTree).

        Args:
            - `owner (str)`: Owner of the repository.
            - `repo (str)`: Name of the repository.
            - `tree_sha (str)`: SHA of the tree.
            - `timeout (int or None)`: Timeout for the request in seconds. Default is 5.
            - `retries (int)`: Number of retries for the request. Default is 0.

        Returns:
            - `tree_info (GitTreeResponseModel)`: Information about the tree.

        Examples:
            >>> tree_info = client.get_tree("owner", "repo", "tree_sha")

        """
        return GitTreeResponseModel.from_json(
            (
                await self.request(
                    "getTree",
                    "GET",
                    owner=owner,
                    repo=repo,
                    tree_sha=tree_sha,
                    timeout=timeout,
                    retries=retries,
                )
            ).text
        )

    async defget_blob(
        self,
        owner: str,
        repo: str,
        file_sha: str,
        timeout: Optional[int] = 5,
        retries: int = 0,
    ) -> Optional[GitBlobResponseModel]:
"""
        Get information about a blob. (Github API endpoint: getBlob).

        Args:
            - `owner (str)`: Owner of the repository.
            - `repo (str)`: Name of the repository.
            - `file_sha (str)`: SHA of the file.
            - `timeout (int or None)`: Timeout for the request in seconds. Default is 5.
            - `retries (int)`: Number of retries for the request. Default is 0.

        Returns:
            - `blob_info (GitBlobResponseModel)`: Information about the blob.

        Examples:
            >>> blob_info = client.get_blob("owner", "repo", "file_sha")

        """
        try:
            return GitBlobResponseModel.from_json(
                (
                    await self.request(
                        "getBlob",
                        "GET",
                        owner=owner,
                        repo=repo,
                        file_sha=file_sha,
                        timeout=timeout,
                        retries=retries,
                    )
                ).text
            )
        except KeyError:
            print(f"Failed to get blob for {owner}/{repo}/{file_sha}")
            return None
        except HTTPError as excp:
            print(f"HTTP Exception for {excp.request.url}{excp}")
            if self._fail_on_http_error:
                raise
            else:
                return None

    async defget_commit(
        self,
        owner: str,
        repo: str,
        commit_sha: str,
        timeout: Optional[int] = 5,
        retries: int = 0,
    ) -> GitCommitResponseModel:
"""
        Get information about a commit. (Github API endpoint: getCommit).

        Args:
            - `owner (str)`: Owner of the repository.
            - `repo (str)`: Name of the repository.
            - `commit_sha (str)`: SHA of the commit.
            - `timeout (int or None)`: Timeout for the request in seconds. Default is 5.
            - `retries (int)`: Number of retries for the request. Default is 0.

        Returns:
            - `commit_info (GitCommitResponseModel)`: Information about the commit.

        Examples:
            >>> commit_info = client.get_commit("owner", "repo", "commit_sha")

        """
        return GitCommitResponseModel.from_json(
            (
                await self.request(
                    "getCommit",
                    "GET",
                    owner=owner,
                    repo=repo,
                    commit_sha=commit_sha,
                    timeout=timeout,
                    retries=retries,
                )
            ).text
        )

    async defget_content(
        self,
        owner: str,
        repo: str,
        path: str,
        ref: Optional[str] = None,
        timeout: Optional[int] = 5,
        retries: int = 0,
    ) -> GitContentResponseModel:
"""
        Get information about a file content. (Github API endpoint: getContent).

        Args:
            - `owner (str)`: Owner of the repository.
            - `repo (str)`: Name of the repository.
            - `path (str)`: Path to the file.
            - `ref (str)`: The name of the commit/branch/tag.
            - `timeout (int or None)`: Timeout for the request in seconds. Default is 5.
            - `retries (int)`: Number of retries for the request. Default is 0.

        Returns:
            - `content_info (GitContentResponseModel)`: Information about the content.

        Examples:
            >>> content_info = client.get_content("owner", "repo", "path/to/file")

        """
        kwargs = {
            "owner": owner,
            "repo": repo,
            "path": path,
        }
        if ref:
            kwargs["ref"] = ref

        # Handle ref query param
        req_kwargs = {"params": {"ref": ref}} if ref else {}

        return GitContentResponseModel.from_json(
            (
                await self.request(
                    "getContent",
                    "GET",
                    timeout=timeout,
                    retries=retries,
                    **kwargs,
                    **req_kwargs,
                )
            ).text
        )

```
 |  
| --- | --- |  
###  get_all_endpoints [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GithubClient.get_all_endpoints "Permanent link")

```
get_all_endpoints() -> [, ]

```

Get all available endpoints.
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/repository/github_client.py`  
| 
```
363
364
365
```
 | 
```
defget_all_endpoints(self) -> Dict[str, str]:
"""Get all available endpoints."""
    return {**self._endpoints}

```
 |  
| --- | --- |  
###  request [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GithubClient.request "Permanent link")

```
request(
    endpoint: ,
    method: ,
    headers: [, ] = {},
    timeout: Optional[] = 5,
    retries:  = 0,
    **kwargs: 
) -> 

```

Make an API request to the Github API.
This method is used for making API requests to the Github API. It is used internally by the other methods in the client.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `- `endpoint (str)``  |  Name of the endpoint to make the request to.  |  _required_  |  
|  `- `method (str)``  |  HTTP method to use for the request.  |  _required_  |  
|  `- `headers (dict)``  |  HTTP headers to include in the request.  |  _required_  |  
|  `- `timeout (int or None)``  |  Timeout for the request in seconds. Default is 5.  |  _required_  |  
|  `- `retries (int)``  |  Number of retries for the request. Default is 0.  |  _required_  |  
|  `- `**kwargs``  |  Keyword arguments to pass to the endpoint URL.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
| 
  * `response (httpx.Response)`: Response from the API request.

 |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `-ImportError`  |  If the `httpx` library is not installed.  |  
|  `-HTTPError`  |  If the API request fails and fail_on_http_error is True.  |  
Examples:

```
>>> response = client.request("getTree", "GET",
                    owner="owner", repo="repo",
                    tree_sha="tree_sha", timeout=5, retries=0)

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/repository/github_client.py`  
| 
```
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
```
 | 
```
async defrequest(
    self,
    endpoint: str,
    method: str,
    headers: Dict[str, Any] = {},
    timeout: Optional[int] = 5,
    retries: int = 0,
    **kwargs: Any,
) -> Any:
"""
    Make an API request to the Github API.

    This method is used for making API requests to the Github API.
    It is used internally by the other methods in the client.

    Args:
        - `endpoint (str)`: Name of the endpoint to make the request to.
        - `method (str)`: HTTP method to use for the request.
        - `headers (dict)`: HTTP headers to include in the request.
        - `timeout (int or None)`: Timeout for the request in seconds. Default is 5.
        - `retries (int)`: Number of retries for the request. Default is 0.
        - `**kwargs`: Keyword arguments to pass to the endpoint URL.

    Returns:
        - `response (httpx.Response)`: Response from the API request.

    Raises:
        - ImportError: If the `httpx` library is not installed.
        - httpx.HTTPError: If the API request fails and fail_on_http_error is True.

    Examples:
        >>> response = client.request("getTree", "GET",
                            owner="owner", repo="repo",
                            tree_sha="tree_sha", timeout=5, retries=0)

    """
    try:
        importhttpx
    except ImportError:
        raise ImportError(
            "Please install httpx to use the GithubRepositoryReader. "
            "You can do so by running `pip install httpx`."
        )

    # Get authentication headers (may fetch fresh token for GitHub App)
    auth_headers = await self._get_auth_headers()
    _headers = {**auth_headers, **headers}

    _client: httpx.AsyncClient
    async with httpx.AsyncClient(
        headers=_headers,
        base_url=self._base_url,
        timeout=timeout,
        transport=httpx.AsyncHTTPTransport(retries=retries),
    ) as _client:
        try:
            response = await _client.request(
                method, url=self._endpoints[endpoint].format(**kwargs)
            )
        except httpx.HTTPError as excp:
            print(f"HTTP Exception for {excp.request.url}{excp}")
            raise excp  # noqa: TRY201
        return response

```
 |  
| --- | --- |  
###  get_branch [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GithubClient.get_branch "Permanent link")

```
get_branch(
    owner: ,
    repo: ,
    branch: Optional[] = None,
    branch_name: Optional[] = None,
    timeout: Optional[] = 5,
    retries:  = 0,
) -> GitBranchResponseModel

```

Get information about a branch. (Github API endpoint: getBranch).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `- `owner (str)``  |  Owner of the repository.  |  _required_  |  
|  `- `repo (str)``  |  Name of the repository.  |  _required_  |  
|  `- `branch (str)``  |  Name of the branch.  |  _required_  |  
|  `- `branch_name (str)``  |  Name of the branch (alternative to `branch`).  |  _required_  |  
|  `- `timeout (int or None)``  |  Timeout for the request in seconds. Default is 5.  |  _required_  |  
|  `- `retries (int)``  |  Number of retries for the request. Default is 0.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `GitBranchResponseModel`  | 
  * `branch_info (GitBranchResponseModel)`: Information about the branch.

 |  
Examples:

```
>>> branch_info = client.get_branch("owner", "repo", "branch")

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/repository/github_client.py`  
| 
```
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
```
 | 
```
async defget_branch(
    self,
    owner: str,
    repo: str,
    branch: Optional[str] = None,
    branch_name: Optional[str] = None,
    timeout: Optional[int] = 5,
    retries: int = 0,
) -> GitBranchResponseModel:
"""
    Get information about a branch. (Github API endpoint: getBranch).

    Args:
        - `owner (str)`: Owner of the repository.
        - `repo (str)`: Name of the repository.
        - `branch (str)`: Name of the branch.
        - `branch_name (str)`: Name of the branch (alternative to `branch`).
        - `timeout (int or None)`: Timeout for the request in seconds. Default is 5.
        - `retries (int)`: Number of retries for the request. Default is 0.

    Returns:
        - `branch_info (GitBranchResponseModel)`: Information about the branch.

    Examples:
        >>> branch_info = client.get_branch("owner", "repo", "branch")

    """
    if branch is None:
        if branch_name is None:
            raise ValueError("Either branch or branch_name must be provided.")
        branch = branch_name

    return GitBranchResponseModel.from_json(
        (
            await self.request(
                "getBranch",
                "GET",
                owner=owner,
                repo=repo,
                branch=branch,
                timeout=timeout,
                retries=retries,
            )
        ).text
    )

```
 |  
| --- | --- |  
###  get_tree [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GithubClient.get_tree "Permanent link")

```
get_tree(
    owner: ,
    repo: ,
    tree_sha: ,
    timeout: Optional[] = 5,
    retries:  = 0,
) -> GitTreeResponseModel

```

Get information about a tree. (Github API endpoint: getTree).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `- `owner (str)``  |  Owner of the repository.  |  _required_  |  
|  `- `repo (str)``  |  Name of the repository.  |  _required_  |  
|  `- `tree_sha (str)``  |  SHA of the tree.  |  _required_  |  
|  `- `timeout (int or None)``  |  Timeout for the request in seconds. Default is 5.  |  _required_  |  
|  `- `retries (int)``  |  Number of retries for the request. Default is 0.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `GitTreeResponseModel`  | 
  * `tree_info (GitTreeResponseModel)`: Information about the tree.

 |  
Examples:

```
>>> tree_info = client.get_tree("owner", "repo", "tree_sha")

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/repository/github_client.py`  
| 
```
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
```
 | 
```
async defget_tree(
    self,
    owner: str,
    repo: str,
    tree_sha: str,
    timeout: Optional[int] = 5,
    retries: int = 0,
) -> GitTreeResponseModel:
"""
    Get information about a tree. (Github API endpoint: getTree).

    Args:
        - `owner (str)`: Owner of the repository.
        - `repo (str)`: Name of the repository.
        - `tree_sha (str)`: SHA of the tree.
        - `timeout (int or None)`: Timeout for the request in seconds. Default is 5.
        - `retries (int)`: Number of retries for the request. Default is 0.

    Returns:
        - `tree_info (GitTreeResponseModel)`: Information about the tree.

    Examples:
        >>> tree_info = client.get_tree("owner", "repo", "tree_sha")

    """
    return GitTreeResponseModel.from_json(
        (
            await self.request(
                "getTree",
                "GET",
                owner=owner,
                repo=repo,
                tree_sha=tree_sha,
                timeout=timeout,
                retries=retries,
            )
        ).text
    )

```
 |  
| --- | --- |  
###  get_blob [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GithubClient.get_blob "Permanent link")

```
get_blob(
    owner: ,
    repo: ,
    file_sha: ,
    timeout: Optional[] = 5,
    retries:  = 0,
) -> Optional[GitBlobResponseModel]

```

Get information about a blob. (Github API endpoint: getBlob).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `- `owner (str)``  |  Owner of the repository.  |  _required_  |  
|  `- `repo (str)``  |  Name of the repository.  |  _required_  |  
|  `- `file_sha (str)``  |  SHA of the file.  |  _required_  |  
|  `- `timeout (int or None)``  |  Timeout for the request in seconds. Default is 5.  |  _required_  |  
|  `- `retries (int)``  |  Number of retries for the request. Default is 0.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[GitBlobResponseModel]`  | 
  * `blob_info (GitBlobResponseModel)`: Information about the blob.

 |  
Examples:

```
>>> blob_info = client.get_blob("owner", "repo", "file_sha")

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/repository/github_client.py`  
| 
```
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
```
 | 
```
async defget_blob(
    self,
    owner: str,
    repo: str,
    file_sha: str,
    timeout: Optional[int] = 5,
    retries: int = 0,
) -> Optional[GitBlobResponseModel]:
"""
    Get information about a blob. (Github API endpoint: getBlob).

    Args:
        - `owner (str)`: Owner of the repository.
        - `repo (str)`: Name of the repository.
        - `file_sha (str)`: SHA of the file.
        - `timeout (int or None)`: Timeout for the request in seconds. Default is 5.
        - `retries (int)`: Number of retries for the request. Default is 0.

    Returns:
        - `blob_info (GitBlobResponseModel)`: Information about the blob.

    Examples:
        >>> blob_info = client.get_blob("owner", "repo", "file_sha")

    """
    try:
        return GitBlobResponseModel.from_json(
            (
                await self.request(
                    "getBlob",
                    "GET",
                    owner=owner,
                    repo=repo,
                    file_sha=file_sha,
                    timeout=timeout,
                    retries=retries,
                )
            ).text
        )
    except KeyError:
        print(f"Failed to get blob for {owner}/{repo}/{file_sha}")
        return None
    except HTTPError as excp:
        print(f"HTTP Exception for {excp.request.url}{excp}")
        if self._fail_on_http_error:
            raise
        else:
            return None

```
 |  
| --- | --- |  
###  get_commit [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GithubClient.get_commit "Permanent link")

```
get_commit(
    owner: ,
    repo: ,
    commit_sha: ,
    timeout: Optional[] = 5,
    retries:  = 0,
) -> GitCommitResponseModel

```

Get information about a commit. (Github API endpoint: getCommit).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `- `owner (str)``  |  Owner of the repository.  |  _required_  |  
|  `- `repo (str)``  |  Name of the repository.  |  _required_  |  
|  `- `commit_sha (str)``  |  SHA of the commit.  |  _required_  |  
|  `- `timeout (int or None)``  |  Timeout for the request in seconds. Default is 5.  |  _required_  |  
|  `- `retries (int)``  |  Number of retries for the request. Default is 0.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `GitCommitResponseModel`  | 
  * `commit_info (GitCommitResponseModel)`: Information about the commit.

 |  
Examples:

```
>>> commit_info = client.get_commit("owner", "repo", "commit_sha")

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/repository/github_client.py`  
| 
```
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
```
 | 
```
async defget_commit(
    self,
    owner: str,
    repo: str,
    commit_sha: str,
    timeout: Optional[int] = 5,
    retries: int = 0,
) -> GitCommitResponseModel:
"""
    Get information about a commit. (Github API endpoint: getCommit).

    Args:
        - `owner (str)`: Owner of the repository.
        - `repo (str)`: Name of the repository.
        - `commit_sha (str)`: SHA of the commit.
        - `timeout (int or None)`: Timeout for the request in seconds. Default is 5.
        - `retries (int)`: Number of retries for the request. Default is 0.

    Returns:
        - `commit_info (GitCommitResponseModel)`: Information about the commit.

    Examples:
        >>> commit_info = client.get_commit("owner", "repo", "commit_sha")

    """
    return GitCommitResponseModel.from_json(
        (
            await self.request(
                "getCommit",
                "GET",
                owner=owner,
                repo=repo,
                commit_sha=commit_sha,
                timeout=timeout,
                retries=retries,
            )
        ).text
    )

```
 |  
| --- | --- |  
###  get_content [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GithubClient.get_content "Permanent link")

```
get_content(
    owner: ,
    repo: ,
    path: ,
    ref: Optional[] = None,
    timeout: Optional[] = 5,
    retries:  = 0,
) -> GitContentResponseModel

```

Get information about a file content. (Github API endpoint: getContent).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `- `owner (str)``  |  Owner of the repository.  |  _required_  |  
|  `- `repo (str)``  |  Name of the repository.  |  _required_  |  
|  `- `path (str)``  |  Path to the file.  |  _required_  |  
|  `- `ref (str)``  |  The name of the commit/branch/tag.  |  _required_  |  
|  `- `timeout (int or None)``  |  Timeout for the request in seconds. Default is 5.  |  _required_  |  
|  `- `retries (int)``  |  Number of retries for the request. Default is 0.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `GitContentResponseModel`  | 
  * `content_info (GitContentResponseModel)`: Information about the content.

 |  
Examples:

```
>>> content_info = client.get_content("owner", "repo", "path/to/file")

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/repository/github_client.py`  
| 
```
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
```
 | 
```
async defget_content(
    self,
    owner: str,
    repo: str,
    path: str,
    ref: Optional[str] = None,
    timeout: Optional[int] = 5,
    retries: int = 0,
) -> GitContentResponseModel:
"""
    Get information about a file content. (Github API endpoint: getContent).

    Args:
        - `owner (str)`: Owner of the repository.
        - `repo (str)`: Name of the repository.
        - `path (str)`: Path to the file.
        - `ref (str)`: The name of the commit/branch/tag.
        - `timeout (int or None)`: Timeout for the request in seconds. Default is 5.
        - `retries (int)`: Number of retries for the request. Default is 0.

    Returns:
        - `content_info (GitContentResponseModel)`: Information about the content.

    Examples:
        >>> content_info = client.get_content("owner", "repo", "path/to/file")

    """
    kwargs = {
        "owner": owner,
        "repo": repo,
        "path": path,
    }
    if ref:
        kwargs["ref"] = ref

    # Handle ref query param
    req_kwargs = {"params": {"ref": ref}} if ref else {}

    return GitContentResponseModel.from_json(
        (
            await self.request(
                "getContent",
                "GET",
                timeout=timeout,
                retries=retries,
                **kwargs,
                **req_kwargs,
            )
        ).text
    )

```
 |  
| --- | --- |  
##  GithubRepositoryReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GithubRepositoryReader "Permanent link")
Bases: 
Github repository reader.
Retrieves the contents of a Github repository and returns a list of documents. The documents are either the contents of the files in the repository or the text extracted from the files using the parser.
Examples:

```
>>> fromllama_index.core.instrumentationimport get_dispatcher
>>> fromllama_index.core.instrumentation.event_handlersimport BaseEventHandler
>>>
>>> # Set up event handler
>>> classGitHubEventHandler(BaseEventHandler):
...     defhandle(self, event):
...         if isinstance(event, GitHubFileProcessedEvent):
...             print(f"Processed file: {event.file_path}")
...
>>> dispatcher = get_dispatcher()
>>> handler = GitHubEventHandler()
>>> dispatcher.add_event_handler(handler)
>>>
>>> client = github_client = GithubClient(
...    github_token=os.environ["GITHUB_TOKEN"],
...    verbose=True
... )
>>> reader = GithubRepositoryReader(
...    github_client=github_client,
...    owner="run-llama",
...    repo="llama_index",
... )
>>> # Load all files from a branch
>>> branch_documents = reader.load_data(branch="main")
>>> # Load all files from a commit
>>> commit_documents = reader.load_data(commit_sha="commit_sha")

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/repository/base.py`  
| 
```
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
 371
 372
 373
 374
 375
 376
 377
 378
 379
 380
 381
 382
 383
 384
 385
 386
 387
 388
 389
 390
 391
 392
 393
 394
 395
 396
 397
 398
 399
 400
 401
 402
 403
 404
 405
 406
 407
 408
 409
 410
 411
 412
 413
 414
 415
 416
 417
 418
 419
 420
 421
 422
 423
 424
 425
 426
 427
 428
 429
 430
 431
 432
 433
 434
 435
 436
 437
 438
 439
 440
 441
 442
 443
 444
 445
 446
 447
 448
 449
 450
 451
 452
 453
 454
 455
 456
 457
 458
 459
 460
 461
 462
 463
 464
 465
 466
 467
 468
 469
 470
 471
 472
 473
 474
 475
 476
 477
 478
 479
 480
 481
 482
 483
 484
 485
 486
 487
 488
 489
 490
 491
 492
 493
 494
 495
 496
 497
 498
 499
 500
 501
 502
 503
 504
 505
 506
 507
 508
 509
 510
 511
 512
 513
 514
 515
 516
 517
 518
 519
 520
 521
 522
 523
 524
 525
 526
 527
 528
 529
 530
 531
 532
 533
 534
 535
 536
 537
 538
 539
 540
 541
 542
 543
 544
 545
 546
 547
 548
 549
 550
 551
 552
 553
 554
 555
 556
 557
 558
 559
 560
 561
 562
 563
 564
 565
 566
 567
 568
 569
 570
 571
 572
 573
 574
 575
 576
 577
 578
 579
 580
 581
 582
 583
 584
 585
 586
 587
 588
 589
 590
 591
 592
 593
 594
 595
 596
 597
 598
 599
 600
 601
 602
 603
 604
 605
 606
 607
 608
 609
 610
 611
 612
 613
 614
 615
 616
 617
 618
 619
 620
 621
 622
 623
 624
 625
 626
 627
 628
 629
 630
 631
 632
 633
 634
 635
 636
 637
 638
 639
 640
 641
 642
 643
 644
 645
 646
 647
 648
 649
 650
 651
 652
 653
 654
 655
 656
 657
 658
 659
 660
 661
 662
 663
 664
 665
 666
 667
 668
 669
 670
 671
 672
 673
 674
 675
 676
 677
 678
 679
 680
 681
 682
 683
 684
 685
 686
 687
 688
 689
 690
 691
 692
 693
 694
 695
 696
 697
 698
 699
 700
 701
 702
 703
 704
 705
 706
 707
 708
 709
 710
 711
 712
 713
 714
 715
 716
 717
 718
 719
 720
 721
 722
 723
 724
 725
 726
 727
 728
 729
 730
 731
 732
 733
 734
 735
 736
 737
 738
 739
 740
 741
 742
 743
 744
 745
 746
 747
 748
 749
 750
 751
 752
 753
 754
 755
 756
 757
 758
 759
 760
 761
 762
 763
 764
 765
 766
 767
 768
 769
 770
 771
 772
 773
 774
 775
 776
 777
 778
 779
 780
 781
 782
 783
 784
 785
 786
 787
 788
 789
 790
 791
 792
 793
 794
 795
 796
 797
 798
 799
 800
 801
 802
 803
 804
 805
 806
 807
 808
 809
 810
 811
 812
 813
 814
 815
 816
 817
 818
 819
 820
 821
 822
 823
 824
 825
 826
 827
 828
 829
 830
 831
 832
 833
 834
 835
 836
 837
 838
 839
 840
 841
 842
 843
 844
 845
 846
 847
 848
 849
 850
 851
 852
 853
 854
 855
 856
 857
 858
 859
 860
 861
 862
 863
 864
 865
 866
 867
 868
 869
 870
 871
 872
 873
 874
 875
 876
 877
 878
 879
 880
 881
 882
 883
 884
 885
 886
 887
 888
 889
 890
 891
 892
 893
 894
 895
 896
 897
 898
 899
 900
 901
 902
 903
 904
 905
 906
 907
 908
 909
 910
 911
 912
 913
 914
 915
 916
 917
 918
 919
 920
 921
 922
 923
 924
 925
 926
 927
 928
 929
 930
 931
 932
 933
 934
 935
 936
 937
 938
 939
 940
 941
 942
 943
 944
 945
 946
 947
 948
 949
 950
 951
 952
 953
 954
 955
 956
 957
 958
 959
 960
 961
 962
 963
 964
 965
 966
 967
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
```
 | 
```
classGithubRepositoryReader(BaseReader):
"""
    Github repository reader.

    Retrieves the contents of a Github repository and returns a list of documents.
    The documents are either the contents of the files in the repository or the text
    extracted from the files using the parser.

    Examples:
        >>> from llama_index.core.instrumentation import get_dispatcher
        >>> from llama_index.core.instrumentation.event_handlers import BaseEventHandler

        >>> # Set up event handler
        >>> class GitHubEventHandler(BaseEventHandler):
        ...     def handle(self, event):
        ...         if isinstance(event, GitHubFileProcessedEvent):
        ...             print(f"Processed file: {event.file_path}")
        ...
        >>> dispatcher = get_dispatcher()
        >>> handler = GitHubEventHandler()
        >>> dispatcher.add_event_handler(handler)

        >>> client = github_client = GithubClient(
        ...    github_token=os.environ["GITHUB_TOKEN"],
        ...    verbose=True
        ... )
        >>> reader = GithubRepositoryReader(
        ...    github_client=github_client,
        ...    owner="run-llama",
        ...    repo="llama_index",
        ... )
        >>> # Load all files from a branch
        >>> branch_documents = reader.load_data(branch="main")
        >>> # Load all files from a commit
        >>> commit_documents = reader.load_data(commit_sha="commit_sha")

    """

    classFilterType(enum.Enum):
"""
        Filter type.

        Used to determine whether the filter is inclusive or exclusive.

        Attributes:
            - EXCLUDE: Exclude the files in the directories or with the extensions.
            - INCLUDE: Include only the files in the directories or with the extensions.

        """

        EXCLUDE = enum.auto()
        INCLUDE = enum.auto()

    def__init__(
        self,
        github_client: BaseGithubClient,
        owner: str,
        repo: str,
        use_parser: bool = False,
        verbose: bool = False,
        concurrent_requests: int = 5,
        timeout: Optional[int] = 5,
        retries: int = 0,
        filter_directories: Optional[Tuple[List[str], FilterType]] = None,
        filter_file_extensions: Optional[Tuple[List[str], FilterType]] = None,
        filter_file_paths: Optional[Tuple[List[str], FilterType]] = None,
        custom_parsers: Optional[Dict[str, BaseReader]] = None,
        process_file_callback: Optional[Callable[[str, int], tuple[bool, str]]] = None,
        custom_folder: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        fail_on_error: bool = True,
    ):
"""
        Initialize params.

        Args:
            - github_client (BaseGithubClient): Github client.
            - owner (str): Owner of the repository.
            - repo (str): Name of the repository.
            - use_parser (bool): Whether to use the parser to extract
                the text from the files.
            - verbose (bool): Whether to print verbose messages.
            - concurrent_requests (int): Number of concurrent requests to
                make to the Github API.
            - timeout (int or None): Timeout for the requests to the Github API. Default is 5.
            - retries (int): Number of retries for requests made to the Github API. Default is 0.
              This limit applies individually to each request made by this class.
            - filter_directories (Optional[Tuple[List[str], FilterType]]): Tuple
                containing a list of directories and a FilterType. If the FilterType
                is INCLUDE, only the files in the directories in the list will be
                included. If the FilterType is EXCLUDE, the files in the directories
                in the list will be excluded.
            - filter_file_extensions (Optional[Tuple[List[str], FilterType]]): Tuple
                containing a list of file extensions and a FilterType. If the
                FilterType is INCLUDE, only the files with the extensions in the list
                will be included. If the FilterType is EXCLUDE, the files with the
                extensions in the list will be excluded.
            - custom_parsers (Optional[Dict[str, BaseReader]]): Dictionary mapping
                file types to custom parsers for processing specific file extensions.
            - process_file_callback (Optional[Callable[[str, int], tuple[bool, str]]]): Callback function
                to determine if a file should be processed. Takes file_path and file_size
                Returns a tuple of (should_process: bool, reason: str).
            - custom_folder (Optional[str]): Custom folder path for temporary file storage in custom parsers.
                Defaults to current working directory.
            - logger (Optional[logging.Logger]): Custom logger instance.
            - fail_on_error (bool): Whether to raise exceptions on processing errors.
                If False, errors are logged and processing continues.

        Note:
            The reader uses LlamaIndex's instrumentation system for event notifications.
            Events are automatically dispatched to any registered event handlers via the global dispatcher.
            Available events include:
            - GitHubRepositoryProcessingStartedEvent
            - GitHubRepositoryProcessingCompletedEvent
            - GitHubTotalFilesToProcessEvent
            - GitHubFileProcessingStartedEvent
            - GitHubFileProcessedEvent
            - GitHubFileSkippedEvent
            - GitHubFileFailedEvent

        Raises:
            - `ValueError`: If the github_token is not provided and
                the GITHUB_TOKEN environment variable is not set.

        """
        super().__init__()

        self._owner = owner
        self._repo = repo
        self._use_parser = use_parser
        self._verbose = verbose
        self._concurrent_requests = concurrent_requests
        self._timeout = timeout
        self._retries = retries
        self._filter_directories = filter_directories
        self._filter_file_extensions = filter_file_extensions
        self._filter_file_paths = filter_file_paths
        self.custom_folder = custom_folder or os.getcwd()
        self.logger = logger or logging.getLogger(__name__)
        self._process_file_callback = process_file_callback
        self.fail_on_error = fail_on_error
        self._github_client = github_client
        self._file_readers: Dict[str, BaseReader] = custom_parsers or {}
        self._supported_suffix = list(DEFAULT_FILE_READER_CLS.keys())
        self.dispatcher = get_dispatcher()

    def_check_filter_directories(self, tree_obj_path: str) -> bool:
"""
        Check if a tree object should be allowed based on the directories.

        :param `tree_obj_path`: path of the tree object i.e. 'llama_index/readers'

        :return: True if the tree object should be allowed, False otherwise
        """
        if self._filter_directories is None:
            return True
        filter_directories, filter_type = self._filter_directories
        print_if_verbose(
            self._verbose,
            f"Checking {tree_obj_path} whether to {filter_type} it"
            + f" based on the filter directories: {filter_directories}",
        )

        if filter_type == self.FilterType.EXCLUDE:
            print_if_verbose(
                self._verbose,
                f"Checking if {tree_obj_path} is not a subdirectory of any of the"
                " filter directories",
            )
            return not any(
                tree_obj_path.startswith(directory) for directory in filter_directories
            )
        if filter_type == self.FilterType.INCLUDE:
            print_if_verbose(
                self._verbose,
                f"Checking if {tree_obj_path} is a subdirectory of any of the filter"
                " directories",
            )
            return any(
                tree_obj_path.startswith(directory)
                or directory.startswith(tree_obj_path)
                for directory in filter_directories
            )
        raise ValueError(
            f"Unknown filter type: {filter_type}. "
            "Please use either 'INCLUDE' or 'EXCLUDE'."
        )

    def_check_filter_file_paths(self, tree_obj_path: str) -> bool:
"""
        Check if a tree object should be allowed based on the file paths.

        :param `tree_obj_path`: path of the tree object i.e. 'llama_index/readers'

        :return: True if the tree object should be allowed, False otherwise
        """
        if self._filter_file_paths is None:
            return True
        filter_file_paths, filter_type = self._filter_file_paths
        print_if_verbose(
            self._verbose,
            f"Checking {tree_obj_path} whether to {filter_type} it"
            + f" based on the filter file paths: {filter_file_paths}",
        )

        if filter_type == self.FilterType.EXCLUDE:
            to_exclude = tree_obj_path not in filter_file_paths
            file_extension = get_file_extension(tree_obj_path)
            reason = "File in Exclude List"
            if to_exclude:
                self.logger.info(f"Skipping file {tree_obj_path}: {reason}")
                self.dispatcher.event(
                    GitHubFileSkippedEvent(
                        file_path=tree_obj_path,
                        file_type=file_extension,
                        reason=reason,
                    )
                )
            return to_exclude
        if filter_type == self.FilterType.INCLUDE:
            return tree_obj_path in filter_file_paths
        raise ValueError(
            f"Unknown filter type: {filter_type}. "
            "Please use either 'INCLUDE' or 'EXCLUDE'."
        )

    def_check_user_callback(self, full_path: str, file_size: int) -> bool:
"""
        Determine if a file should be processed based on the callback function.

        :param full_path: Full path to the file
        :param file_size: Size of the file in bytes
        :return: True if file should be processed, False otherwise
        """
        if not self._process_file_callback:
            return True

        file_extension = get_file_extension(full_path)

        try:
            should_process, reason = self._process_file_callback(full_path, file_size)
        except Exception as e:
            self.logger.error(f"Error in process_file_callback for {full_path}: {e}")
            if self.fail_on_error:
                raise
            # If fail_on_error is False, skip the file
            reason = f"Callback error: {e!s}"
            should_process = False

        if not should_process:
            self.logger.info(f"Skipping file {full_path}: {reason}")
            self.dispatcher.event(
                GitHubFileSkippedEvent(
                    file_path=full_path,
                    file_type=file_extension,
                    reason=reason,
                )
            )
        return should_process

    def_check_filter_file_extensions(self, tree_obj_path: str) -> bool:
"""
        Check if a tree object should be allowed based on the file extensions.

        :param `tree_obj_path`: path of the tree object i.e. 'llama_index/indices'

        :return: True if the tree object should be allowed, False otherwise
        """
        if self._filter_file_extensions is None:
            return True
        filter_file_extensions, filter_type = self._filter_file_extensions
        print_if_verbose(
            self._verbose,
            f"Checking {tree_obj_path} whether to {filter_type} it"
            + f" based on the filter file extensions: {filter_file_extensions}",
        )

        if filter_type == self.FilterType.EXCLUDE:
            return get_file_extension(tree_obj_path) not in filter_file_extensions
        if filter_type == self.FilterType.INCLUDE:
            return get_file_extension(tree_obj_path) in filter_file_extensions
        raise ValueError(
            f"Unknown filter type: {filter_type}. "
            "Please use either 'INCLUDE' or 'EXCLUDE'."
        )

    def_allow_tree_obj(
        self, tree_obj_path: str, tree_obj_type: str, file_size: int = None
    ) -> bool:
"""
        Check if a tree object should be allowed.

        :param `tree_obj_path`: path of the tree object

        :return: True if the tree object should be allowed, False otherwise

        """
        if self._filter_directories is not None and tree_obj_type == "tree":
            return self._check_filter_directories(tree_obj_path)

        if self._filter_file_extensions is not None and tree_obj_type == "blob":
            return self._check_filter_directories(
                tree_obj_path
            ) and self._check_filter_file_extensions(tree_obj_path)

        if self._filter_file_paths is not None and tree_obj_type == "blob":
            return self._check_filter_file_paths(
                tree_obj_path
            ) and self._check_filter_directories(tree_obj_path)

        if file_size:
            return self._check_user_callback(tree_obj_path, file_size)

        return True

    async def_load_files_by_path(
        self,
        ref: str,
        file_paths: List[str],
        file_exists_callback: Optional[Callable[[str], bool]] = None,
    ) -> List[Document]:
"""
        Load specific files by path.
        """
        documents = []

        sem = asyncio.Semaphore(self._concurrent_requests)

        async deffetch_and_process(path: str) -> Optional[Document]:
            async with sem:
                try:
                    content_data = await self._github_client.get_content(
                        self._owner,
                        self._repo,
                        path,
                        ref=ref,
                        timeout=self._timeout,
                        retries=self._retries,
                    )
                except Exception as e:
                    if self.fail_on_error:
                        raise
                    self.logger.warning(f"Failed to fetch {path}: {e}")
                    return None

            if file_exists_callback and file_exists_callback(content_data.sha):
                return None

            return self._create_and_process_document(
                full_path=path,
                sha=content_data.sha,
                content=content_data.content,
                encoding=content_data.encoding,
                url=content_data.html_url,  # Use html_url for consistency
            )

        # Using asyncio.gather to fetch files concurrently
        tasks = [fetch_and_process(path) for path in file_paths]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                documents.append(result)

        return documents

    def_create_and_process_document(
        self,
        full_path: str,
        sha: str,
        content: str,
        encoding: str,
        url: str,
    ) -> Optional[Document]:
"""
        Helper to decode content and create a Document.
        """
        assert encoding == "base64", f"blob encoding {encoding} not supported"

        file_extension = get_file_extension(full_path)

        # Notify file processing started
        self.dispatcher.event(
            GitHubFileProcessingStartedEvent(
                file_path=full_path, file_type=file_extension
            )
        )

        decoded_bytes = None
        try:
            decoded_bytes = base64.b64decode(content)
        except binascii.Error:
            print_if_verbose(self._verbose, f"could not decode {full_path} as base64")
            self.dispatcher.event(
                GitHubFileFailedEvent(
                    file_path=full_path,
                    file_type=file_extension,
                    error="Could not decode as base64",
                )
            )
            return None

        try:
            if self._use_parser or file_extension in self._file_readers:
                document = self._parse_supported_file(
                    file_path=full_path,
                    file_content=decoded_bytes,
                    tree_sha=sha,
                    tree_path=full_path,
                )
                if document is not None:
                    self.dispatcher.event(
                        GitHubFileProcessedEvent(
                            file_path=full_path,
                            file_type=file_extension,
                            file_size=len(decoded_bytes) if decoded_bytes else 0,
                            document=document,
                        )
                    )
                    return document
                print_if_verbose(
                    self._verbose,
                    f"could not parse {full_path} as a supported file type"
                    + " - falling back to decoding as utf-8 raw text",
                )
        except Exception as e:
            self.logger.error(f"Error processing file {full_path}: {e}")
            self.dispatcher.event(
                GitHubFileFailedEvent(
                    file_path=full_path,
                    file_type=file_extension,
                    error=str(e),
                )
            )
            if self.fail_on_error:
                raise
            else:
                self.logger.warning(
                    f"Failed to process file {full_path}: {e}. Skipping this file."
                )
                return None

        try:
            if decoded_bytes is None:
                raise ValueError("decoded_bytes is None")
            decoded_text = decoded_bytes.decode("utf-8")
        except UnicodeDecodeError:
            print_if_verbose(self._verbose, f"could not decode {full_path} as utf-8")
            self.dispatcher.event(
                GitHubFileFailedEvent(
                    file_path=full_path,
                    file_type=file_extension,
                    error="Could not decode as UTF-8",
                )
            )
            return None

        print_if_verbose(
            self._verbose,
            f"got {len(decoded_text)} characters - adding to documents - {full_path}",
        )

        document = Document(
            text=decoded_text,
            doc_id=sha,
            metadata={
                "file_path": full_path,
                "file_name": full_path.split("/")[-1],
                "url": url,
            },
        )
        self.dispatcher.event(
            GitHubFileProcessedEvent(
                file_path=full_path,
                file_type=file_extension,
                file_size=len(decoded_text.encode("utf-8")),
                document=document,
            )
        )
        return document

        return documents

    def_load_data_from_commit(
        self,
        commit_sha: str,
        file_path: Optional[str] = None,
        file_paths: Optional[List[str]] = None,
        ignore_file_paths: Optional[List[str]] = None,
        file_exists_callback: Optional[Callable[[str], bool]] = None,
    ) -> List[Document]:
"""
        Load data from a commit.

        Loads github repository data from a specific commit sha.

        :param `commit`: commit sha

        :return: list of documents
        """
        repo_name = f"{self._owner}/{self._repo}"

        if file_paths is None and file_path is not None:
            file_paths = [file_path]

        if file_paths is not None:
            return asyncio_run(
                self._load_files_by_path(
                    ref=commit_sha,
                    file_paths=file_paths,
                    file_exists_callback=file_exists_callback,
                )
            )

        # Notify repository processing started
        self.dispatcher.event(
            GitHubRepositoryProcessingStartedEvent(
                repository_name=repo_name, branch_or_commit=commit_sha
            )
        )

        commit_response: GitCommitResponseModel = asyncio_run(
            self._github_client.get_commit(
                self._owner,
                self._repo,
                commit_sha,
                timeout=self._timeout,
                retries=self._retries,
            )
        )

        tree_sha = commit_response.commit.tree.sha
        blobs_and_paths = asyncio_run(self._recurse_tree(tree_sha))

        # Filter ignoring file paths
        if ignore_file_paths:
            blobs_and_paths = [
                (blob, path)
                for blob, path in blobs_and_paths
                if path not in ignore_file_paths
            ]

        # Filter based on file_exists_callback
        if file_exists_callback:
            blobs_and_paths = [
                (blob, path)
                for blob, path in blobs_and_paths
                if not file_exists_callback(blob.sha)
            ]

        print_if_verbose(self._verbose, f"got {len(blobs_and_paths)} blobs")

        # Notify total files to process
        self.dispatcher.event(
            GitHubTotalFilesToProcessEvent(
                repository_name=repo_name,
                branch_or_commit=commit_sha,
                total_files=len(blobs_and_paths),
            )
        )

        documents = asyncio_run(
            self._generate_documents(
                blobs_and_paths=blobs_and_paths,
                id=commit_sha,
            )
        )

        # Notify repository processing completed
        self.dispatcher.event(
            GitHubRepositoryProcessingCompletedEvent(
                repository_name=repo_name,
                branch_or_commit=commit_sha,
                total_documents=len(documents),
            )
        )

        return documents

    def_load_data_from_branch(
        self,
        branch: str,
        file_path: Optional[str] = None,
        file_paths: Optional[List[str]] = None,
        ignore_file_paths: Optional[List[str]] = None,
        file_exists_callback: Optional[Callable[[str], bool]] = None,
    ) -> List[Document]:
"""
        Load data from a branch.

        Loads github repository data from a specific branch.

        :param `branch`: branch name
        :param `file_path`: the full path to a specific file in the repo

        :return: list of documents
        """
        repo_name = f"{self._owner}/{self._repo}"

        if file_paths is None and file_path is not None:
            file_paths = [file_path]

        if file_paths is not None:
            return asyncio_run(
                self._load_files_by_path(
                    ref=branch,
                    file_paths=file_paths,
                    file_exists_callback=file_exists_callback,
                )
            )

        # Notify repository processing started
        self.dispatcher.event(
            GitHubRepositoryProcessingStartedEvent(
                repository_name=repo_name, branch_or_commit=branch
            )
        )

        branch_data: GitBranchResponseModel = asyncio_run(
            self._github_client.get_branch(
                self._owner,
                self._repo,
                branch,
                timeout=self._timeout,
                retries=self._retries,
            )
        )

        tree_sha = branch_data.commit.commit.tree.sha
        blobs_and_paths = asyncio_run(self._recurse_tree(tree_sha))

        # Filter ignoring file paths
        if ignore_file_paths:
            blobs_and_paths = [
                (blob, path)
                for blob, path in blobs_and_paths
                if path not in ignore_file_paths
            ]

        # Filter based on file_exists_callback
        if file_exists_callback:
            blobs_and_paths = [
                (blob, path)
                for blob, path in blobs_and_paths
                if not file_exists_callback(blob.sha)
            ]

        print_if_verbose(self._verbose, f"got {len(blobs_and_paths)} blobs")

        # Notify total files to process
        self.dispatcher.event(
            GitHubTotalFilesToProcessEvent(
                repository_name=repo_name,
                branch_or_commit=branch,
                total_files=len(blobs_and_paths),
            )
        )

        documents = asyncio_run(
            self._generate_documents(
                blobs_and_paths=blobs_and_paths,
                id=branch,
            )
        )

        # Notify repository processing completed
        self.dispatcher.event(
            GitHubRepositoryProcessingCompletedEvent(
                repository_name=repo_name,
                branch_or_commit=branch,
                total_documents=len(documents),
            )
        )

        return documents

    defload_data(
        self,
        commit_sha: Optional[str] = None,
        branch: Optional[str] = None,
        file_path: Optional[str] = None,
        file_paths: Optional[List[str]] = None,
        ignore_file_paths: Optional[List[str]] = None,
        file_exists_callback: Optional[Callable[[str], bool]] = None,
    ) -> List[Document]:
"""
        Load data from a commit or a branch.

        Loads github repository data from a specific commit sha or a branch.

        :param `commit_sha`: commit sha
        :param `branch`: branch name
        :param `file_path`: the full path to a specific file in the repo
        :param `file_paths`: list of full paths to specific files in the repo
        :param `ignore_file_paths`: list of full paths to ignore
        :param `file_exists_callback`: callback to check if a file exists (by SHA)

        :return: list of documents
        """
        if commit_sha is not None and branch is not None:
            raise ValueError("You can only specify one of commit or branch.")

        if commit_sha is None and branch is None:
            raise ValueError("You must specify one of commit or branch.")

        if commit_sha is not None:
            return self._load_data_from_commit(
                commit_sha,
                file_path=file_path,
                file_paths=file_paths,
                ignore_file_paths=ignore_file_paths,
                file_exists_callback=file_exists_callback,
            )

        if branch is not None:
            return self._load_data_from_branch(
                branch,
                file_path=file_path,
                file_paths=file_paths,
                ignore_file_paths=ignore_file_paths,
                file_exists_callback=file_exists_callback,
            )

        raise ValueError("You must specify one of commit or branch.")

    async def_recurse_tree(
        self,
        tree_sha: str,
        current_path: str = "",
        current_depth: int = 0,
        max_depth: int = -1,
    ) -> Any:
"""
        Recursively get all blob tree objects in a tree.

        And construct their full path relative to the root of the repository.
        (see GitTreeResponseModel.GitTreeObject in
            github_api_client.py for more information)

        :param `tree_sha`: sha of the tree to recurse
        :param `current_path`: current path of the tree
        :param `current_depth`: current depth of the tree
        :return: list of tuples of
            (tree object, file's full path relative to the root of the repo)
        """
        if max_depth != -1 and current_depth  max_depth:
            return []

        blobs_and_full_paths: List[Tuple[GitTreeResponseModel.GitTreeObject, str]] = []
        print_if_verbose(
            self._verbose,
            "\t" * current_depth + f"current path: {current_path}",
        )

        tree_data: GitTreeResponseModel = await self._github_client.get_tree(
            self._owner,
            self._repo,
            tree_sha,
            timeout=self._timeout,
            retries=self._retries,
        )
        print_if_verbose(
            self._verbose, "\t" * current_depth + f"tree data: {tree_data}"
        )
        print_if_verbose(
            self._verbose, "\t" * current_depth + f"processing tree {tree_sha}"
        )
        for tree_obj in tree_data.tree:
            file_path = os.path.join(current_path, tree_obj.path)
            file_size = None
            if tree_obj.type == "blob":
                file_size = tree_obj.size
            if not self._allow_tree_obj(file_path, tree_obj.type, file_size):
                print_if_verbose(
                    self._verbose,
                    "\t" * current_depth + f"ignoring {tree_obj.path} due to filter",
                )
                continue

            print_if_verbose(
                self._verbose,
                "\t" * current_depth + f"tree object: {tree_obj}",
            )

            if tree_obj.type == "tree":
                print_if_verbose(
                    self._verbose,
                    "\t" * current_depth + f"recursing into {tree_obj.path}",
                )

                blobs_and_full_paths.extend(
                    await self._recurse_tree(
                        tree_obj.sha, file_path, current_depth + 1, max_depth
                    )
                )
            elif tree_obj.type == "blob":
                print_if_verbose(
                    self._verbose,
                    "\t" * current_depth + f"found blob {tree_obj.path}",
                )

                blobs_and_full_paths.append((tree_obj, file_path))

            print_if_verbose(
                self._verbose,
                "\t" * current_depth + f"blob and full paths: {blobs_and_full_paths}",
            )
        return blobs_and_full_paths

    def_get_base_url(self, blob_url):
        match = re.match(r"(https://[^/]+\.com/)", blob_url)
        if match:
            return match.group(1)
        else:
            return "https://github.com/"

    async def_generate_documents(
        self,
        blobs_and_paths: List[Tuple[GitTreeResponseModel.GitTreeObject, str]],
        id: str = "",
    ) -> List[Document]:
"""
        Generate documents from a list of blobs and their full paths.

        :param `blobs_and_paths`: list of tuples of
            (tree object, file's full path in the repo relative to the root of the repo)
        :param `id`: the branch name or commit sha used when loading the repo
        :return: list of documents
        """
        buffered_iterator = BufferedGitBlobDataIterator(
            blobs_and_paths=blobs_and_paths,
            github_client=self._github_client,
            owner=self._owner,
            repo=self._repo,
            buffer_size=self._concurrent_requests,  # TODO: make this configurable
            verbose=self._verbose,
            timeout=self._timeout,
            retries=self._retries,
        )

        documents = []
        async for blob_data, full_path in buffered_iterator:
            print_if_verbose(self._verbose, f"generating document for {full_path}")

            # Construct URL for the document (mimicking what was there before)
            # The original code constructed URL manually at the end.
            # My helper _create_and_process_document takes a URL.
            # blob_data.url is the API URL. The original code constructed a blob URL.

            # Original URL construction:
            # url = os.path.join(self._get_base_url(blob_data.url), self._owner, self._repo, "blob/", id, full_path)

            url = os.path.join(
                self._get_base_url(blob_data.url),
                self._owner,
                self._repo,
                "blob/",
                id,
                full_path,
            )

            document = self._create_and_process_document(
                full_path=full_path,
                sha=blob_data.sha,
                content=blob_data.content,
                encoding=blob_data.encoding,
                url=url,
            )

            if document:
                documents.append(document)

        return documents

    def_parse_supported_file(
        self,
        file_path: str,
        file_content: bytes,
        tree_sha: str,
        tree_path: str,
    ) -> Optional[Document]:
"""
        Parse a file if it is supported by a parser.

        :param `file_path`: path of the file in the repo
        :param `file_content`: content of the file
        :return: Document if the file is supported by a parser, None otherwise
        """
        file_extension = get_file_extension(file_path)
        if file_extension not in self._supported_suffix:
            # skip
            return None

        if file_extension not in self._file_readers:
            # initialize reader
            cls_ = DEFAULT_FILE_READER_CLS[file_extension]
            self._file_readers[file_extension] = cls_()

        reader = self._file_readers[file_extension]

        print_if_verbose(
            self._verbose,
            f"parsing {file_path}"
            + f"as {file_extension} with "
            + f"{reader.__class__.__name__}",
        )

        if self.custom_folder:
            with tempfile.NamedTemporaryFile(
                dir=self.custom_folder,
                suffix=f".{file_extension}",
                mode="w+b",
                delete=False,
            ) as tmpfile:
                parsed_file = self._start_parsing(
                    tmpfile, file_path, file_content, reader
                )
        else:
            with tempfile.TemporaryDirectory() as tmpdirname:
                with tempfile.NamedTemporaryFile(
                    dir=tmpdirname,
                    suffix=f".{file_extension}",
                    mode="w+b",
                    delete=False,
                ) as tmpfile:
                    parsed_file = self._start_parsing(
                        tmpfile, file_path, file_content, reader
                    )

        if parsed_file is None:
            return None
        return Document(
            text=parsed_file,
            doc_id=tree_sha,
            metadata={
                "file_path": file_path,
                "file_name": tree_path,
            },
        )

    def_start_parsing(
        self,
        tmpfile: tempfile.NamedTemporaryFile,
        file_path: str,
        file_content: bytes,
        reader: BaseReader,
    ):
        print_if_verbose(
            self._verbose,
            "created a temporary file" + f"{tmpfile.name} for parsing {file_path}",
        )
        tmpfile.write(file_content)
        tmpfile.flush()
        tmpfile.close()
        try:
            docs = reader.load_data(pathlib.Path(tmpfile.name))
            parsed_file = "\n\n".join([doc.get_text() for doc in docs])
        except Exception as e:
            print_if_verbose(self._verbose, f"error while parsing {file_path}")
            self.logger.error(
                "Error while parsing "
                + f"{file_path} with "
                + f"{reader.__class__.__name__}:\n{e}"
            )
            parsed_file = None
        finally:
            os.remove(tmpfile.name)
        return parsed_file

```
 |  
| --- | --- |  
###  FilterType [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GithubRepositoryReader.FilterType "Permanent link")
Bases: `Enum`
Filter type.
Used to determine whether the filter is inclusive or exclusive.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
|  `EXCLUDE`  |  Exclude the files in the directories or with the extensions.  |  
|  `INCLUDE`  |  Include only the files in the directories or with the extensions.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/repository/base.py`  
| 
```
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
```
 | 
```
classFilterType(enum.Enum):
"""
    Filter type.

    Used to determine whether the filter is inclusive or exclusive.

    Attributes:
        - EXCLUDE: Exclude the files in the directories or with the extensions.
        - INCLUDE: Include only the files in the directories or with the extensions.

    """

    EXCLUDE = enum.auto()
    INCLUDE = enum.auto()

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GithubRepositoryReader.load_data "Permanent link")

```
load_data(
    commit_sha: Optional[] = None,
    branch: Optional[] = None,
    file_path: Optional[] = None,
    file_paths: Optional[[]] = None,
    ignore_file_paths: Optional[[]] = None,
    file_exists_callback: Optional[
        Callable[[], ]
    ] = None,
) -> []

```

Load data from a commit or a branch.
Loads github repository data from a specific commit sha or a branch.
:param `commit_sha`: commit sha :param `branch`: branch name :param `file_path`: the full path to a specific file in the repo :param `file_paths`: list of full paths to specific files in the repo :param `ignore_file_paths`: list of full paths to ignore :param `file_exists_callback`: callback to check if a file exists (by SHA)
:return: list of documents
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/repository/base.py`  
| 
```
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
```
 | 
```
defload_data(
    self,
    commit_sha: Optional[str] = None,
    branch: Optional[str] = None,
    file_path: Optional[str] = None,
    file_paths: Optional[List[str]] = None,
    ignore_file_paths: Optional[List[str]] = None,
    file_exists_callback: Optional[Callable[[str], bool]] = None,
) -> List[Document]:
"""
    Load data from a commit or a branch.

    Loads github repository data from a specific commit sha or a branch.

    :param `commit_sha`: commit sha
    :param `branch`: branch name
    :param `file_path`: the full path to a specific file in the repo
    :param `file_paths`: list of full paths to specific files in the repo
    :param `ignore_file_paths`: list of full paths to ignore
    :param `file_exists_callback`: callback to check if a file exists (by SHA)

    :return: list of documents
    """
    if commit_sha is not None and branch is not None:
        raise ValueError("You can only specify one of commit or branch.")

    if commit_sha is None and branch is None:
        raise ValueError("You must specify one of commit or branch.")

    if commit_sha is not None:
        return self._load_data_from_commit(
            commit_sha,
            file_path=file_path,
            file_paths=file_paths,
            ignore_file_paths=ignore_file_paths,
            file_exists_callback=file_exists_callback,
        )

    if branch is not None:
        return self._load_data_from_branch(
            branch,
            file_path=file_path,
            file_paths=file_paths,
            ignore_file_paths=ignore_file_paths,
            file_exists_callback=file_exists_callback,
        )

    raise ValueError("You must specify one of commit or branch.")

```
 |  
| --- | --- |  
##  GitHubAppAuth [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubAppAuth "Permanent link")
GitHub App authentication handler.
This class manages authentication for GitHub Apps by generating JWTs and obtaining/caching installation access tokens. Tokens are automatically refreshed when they expire.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `app_id`  |  The GitHub App ID.  |  
| `private_key`  |  The private key for the GitHub App (PEM format).  |  
| `installation_id`  |  The installation ID for the GitHub App.  |  
Examples:

```
>>> # Read private key from file
>>> with open("private-key.pem", "r") as f:
...     private_key = f.read()
>>>
>>> # Create auth handler
>>> auth = GitHubAppAuth(
...     app_id="123456",
...     private_key=private_key,
...     installation_id="789012"
... )
>>>
>>> # Get installation token (cached and auto-refreshed)
>>> importasyncio
>>> token = asyncio.run(auth.get_installation_token())

```

Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/github_app_auth.py`  
| 
```
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
```
 | 
```
classGitHubAppAuth:
"""
    GitHub App authentication handler.

    This class manages authentication for GitHub Apps by generating JWTs and
    obtaining/caching installation access tokens. Tokens are automatically
    refreshed when they expire.

    Attributes:
        app_id (str): The GitHub App ID.
        private_key (str): The private key for the GitHub App (PEM format).
        installation_id (str): The installation ID for the GitHub App.

    Examples:
        >>> # Read private key from file
        >>> with open("private-key.pem", "r") as f:
        ...     private_key = f.read()

        >>> # Create auth handler
        >>> auth = GitHubAppAuth(
        ...     app_id="123456",
        ...     private_key=private_key,
        ...     installation_id="789012"
        ... )

        >>> # Get installation token (cached and auto-refreshed)
        >>> import asyncio
        >>> token = asyncio.run(auth.get_installation_token())

    """

    # Token expiry buffer in seconds (refresh 5 minutes before expiry)
    TOKEN_EXPIRY_BUFFER = 300
    # JWT expiry time in seconds (10 minutes, max allowed by GitHub)
    JWT_EXPIRY_SECONDS = 600
    # Installation token expiry time in seconds (1 hour, GitHub default)
    INSTALLATION_TOKEN_EXPIRY_SECONDS = 3600

    def__init__(
        self,
        app_id: str,
        private_key: str,
        installation_id: str,
        base_url: str = "https://api.github.com",
    ) -> None:
"""
        Initialize GitHubAppAuth.

        Args:
            app_id: The GitHub App ID.
            private_key: The private key for the GitHub App in PEM format.
            installation_id: The installation ID for the GitHub App.
            base_url: Base URL for GitHub API (default: "https://api.github.com").

        Raises:
            ImportError: If PyJWT is not installed.
            GitHubAppAuthenticationError: If initialization fails.

        """
        if jwt is None:
            raise ImportError(
                "PyJWT is required for GitHub App authentication. "
                "Install it with: pip install 'PyJWT[crypto]>=2.8.0'"
            )

        if not app_id:
            raise GitHubAppAuthenticationError("app_id is required")
        if not private_key:
            raise GitHubAppAuthenticationError("private_key is required")
        if not installation_id:
            raise GitHubAppAuthenticationError("installation_id is required")

        self.app_id = app_id
        self.private_key = private_key
        self.installation_id = installation_id
        self.base_url = base_url.rstrip("/")

        # Token cache
        self._token_cache: Optional[str] = None
        self._token_expires_at: float = 0

    def_generate_jwt(self) -> str:
"""
        Generate JWT for GitHub App authentication.

        The JWT is used to authenticate as the GitHub App itself, before
        obtaining an installation access token.

        Returns:
            The generated JWT token.

        Raises:
            GitHubAppAuthenticationError: If JWT generation fails.

        """
        try:
            now = int(time.time())
            payload = {
                "iat": now - 60,  # Issued at (with 60s buffer for clock skew)
                "exp": now + self.JWT_EXPIRY_SECONDS,  # Expires in 10 minutes
                "iss": self.app_id,  # Issuer is the app ID
            }

            return jwt.encode(payload, self.private_key, algorithm="RS256")
        except Exception as e:
            raise GitHubAppAuthenticationError(f"Failed to generate JWT: {e!s}") frome

    async defget_installation_token(self, force_refresh: bool = False) -> str:
"""
        Get or refresh installation access token.

        This method returns a cached token if it's still valid, or requests
        a new token from GitHub if the cached token is expired or about to expire.

        Args:
            force_refresh: If True, forces a token refresh even if cached token
                         is still valid.

        Returns:
            A valid installation access token.

        Raises:
            GitHubAppAuthenticationError: If token retrieval fails.
            ImportError: If httpx is not installed.

        """
        # Check if cached token is still valid (with buffer)
        if not force_refresh and self._is_token_valid():
            return self._token_cache  # type: ignore

        # Generate new token
        try:
            importhttpx
        except ImportError:
            raise ImportError(
                "httpx is required for GitHub App authentication. "
                "Install it with: pip install httpx>=0.26.0"
            )

        jwt_token = self._generate_jwt()

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {jwt_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        url = f"{self.base_url}/app/installations/{self.installation_id}/access_tokens"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, timeout=10.0)
                response.raise_for_status()
                data = response.json()

                self._token_cache = data["token"]
                # Token typically expires in 1 hour
                self._token_expires_at = (
                    time.time() + self.INSTALLATION_TOKEN_EXPIRY_SECONDS
                )

                return self._token_cache
        except httpx.HTTPStatusError as e:
            raise GitHubAppAuthenticationError(
                f"Failed to get installation token: {e.response.status_code}{e.response.text}"
            ) frome
        except Exception as e:
            raise GitHubAppAuthenticationError(
                f"Failed to get installation token: {e!s}"
            ) frome

    def_is_token_valid(self) -> bool:
"""
        Check if the cached token is still valid.

        Returns:
            True if token exists and is not expired (accounting for buffer).

        """
        if not self._token_cache:
            return False

        # Check if token will expire within the buffer period
        time_until_expiry = self._token_expires_at - time.time()
        return time_until_expiry  self.TOKEN_EXPIRY_BUFFER

    definvalidate_token(self) -> None:
"""
        Invalidate the cached token.

        This forces the next call to get_installation_token() to fetch a new token.
        Useful if you know the token has been revoked or is no longer valid.

        """
        self._token_cache = None
        self._token_expires_at = 0

```
 |  
| --- | --- |  
###  get_installation_token [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubAppAuth.get_installation_token "Permanent link")

```
get_installation_token(force_refresh:  = False) -> 

```

Get or refresh installation access token.
This method returns a cached token if it's still valid, or requests a new token from GitHub if the cached token is expired or about to expire.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `force_refresh`  |  `bool`  |  If True, forces a token refresh even if cached token is still valid.  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  A valid installation access token.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|   |  If token retrieval fails.  |  
|  `ImportError`  |  If httpx is not installed.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/github_app_auth.py`  
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
```
 | 
```
async defget_installation_token(self, force_refresh: bool = False) -> str:
"""
    Get or refresh installation access token.

    This method returns a cached token if it's still valid, or requests
    a new token from GitHub if the cached token is expired or about to expire.

    Args:
        force_refresh: If True, forces a token refresh even if cached token
                     is still valid.

    Returns:
        A valid installation access token.

    Raises:
        GitHubAppAuthenticationError: If token retrieval fails.
        ImportError: If httpx is not installed.

    """
    # Check if cached token is still valid (with buffer)
    if not force_refresh and self._is_token_valid():
        return self._token_cache  # type: ignore

    # Generate new token
    try:
        importhttpx
    except ImportError:
        raise ImportError(
            "httpx is required for GitHub App authentication. "
            "Install it with: pip install httpx>=0.26.0"
        )

    jwt_token = self._generate_jwt()

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {jwt_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    url = f"{self.base_url}/app/installations/{self.installation_id}/access_tokens"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            self._token_cache = data["token"]
            # Token typically expires in 1 hour
            self._token_expires_at = (
                time.time() + self.INSTALLATION_TOKEN_EXPIRY_SECONDS
            )

            return self._token_cache
    except httpx.HTTPStatusError as e:
        raise GitHubAppAuthenticationError(
            f"Failed to get installation token: {e.response.status_code}{e.response.text}"
        ) frome
    except Exception as e:
        raise GitHubAppAuthenticationError(
            f"Failed to get installation token: {e!s}"
        ) frome

```
 |  
| --- | --- |  
###  invalidate_token [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubAppAuth.invalidate_token "Permanent link")

```
invalidate_token() -> None

```

Invalidate the cached token.
This forces the next call to get_installation_token() to fetch a new token. Useful if you know the token has been revoked or is no longer valid.
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/github_app_auth.py`  
| 
```
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
```
 | 
```
definvalidate_token(self) -> None:
"""
    Invalidate the cached token.

    This forces the next call to get_installation_token() to fetch a new token.
    Useful if you know the token has been revoked or is no longer valid.

    """
    self._token_cache = None
    self._token_expires_at = 0

```
 |  
| --- | --- |  
##  GitHubAppAuthenticationError [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/github/#llama_index.readers.github.GitHubAppAuthenticationError "Permanent link")
Bases: `Exception`
Raised when GitHub App authentication fails.
Source code in `llama-index-integrations/readers/llama-index-readers-github/llama_index/readers/github/github_app_auth.py`  
| 
```
classGitHubAppAuthenticationError(Exception):
"""Raised when GitHub App authentication fails."""

```
 |  
| --- |  
options: members: - GitHubRepositoryCollaboratorsReader - GitHubRepositoryIssuesReader - GithubRepositoryReader
