# Gitlab
##  GitLabIssuesReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gitlab/#llama_index.readers.gitlab.GitLabIssuesReader "Permanent link")
Bases: 
GitLab issues reader.
Source code in `llama-index-integrations/readers/llama-index-readers-gitlab/llama_index/readers/gitlab/issues/base.py`  
| 
```
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
```
 | 
```
classGitLabIssuesReader(BaseReader):
"""
    GitLab issues reader.
    """

    classIssueState(enum.Enum):
"""
        Issue type.

        Used to decide what issues to retrieve.

        Attributes:
            - OPEN: Issues that are open.
            - CLOSED: Issues that are closed.
            - ALL: All issues, open and closed.

        """

        OPEN = "opened"
        CLOSED = "closed"
        ALL = "all"

    classIssueType(enum.Enum):
"""
        Issue type.

        Used to decide what issues to retrieve.

        Attributes:
            - ISSUE: Issues.
            - INCIDENT: Incident.
            - TEST_CASE: Test case.
            - TASK: Task.

        """

        ISSUE = "issue"
        INCIDENT = "incident"
        TEST_CASE = "test_case"
        TASK = "task"

    classScope(enum.Enum):
"""
        Scope.

        Used to determine the scope of the issue.

        Attributes:
            - CREATED_BY_ME: Issues created by the authenticated user.
            - ASSIGNED_TO_ME: Issues assigned to the authenticated user.
            - ALL: All issues.

        """

        CREATED_BY_ME = "created_by_me"
        ASSIGNED_TO_ME = "assigned_to_me"
        ALL = "all"

    def__init__(
        self,
        gitlab_client: gitlab.Gitlab,
        project_id: Optional[int] = None,
        group_id: Optional[int] = None,
        verbose: bool = False,
    ):
        super().__init__()

        self._gl = gitlab_client
        self._project_id = project_id
        self._group_id = group_id
        self._verbose = verbose

    def_build_document_from_issue(self, issue: GitLabIssue) -> Document:
        issue_dict = issue.asdict()
        title = issue_dict["title"]
        description = issue_dict["description"]
        document = Document(
            doc_id=str(issue_dict["iid"]),
            text=f"{title}\n{description}",
        )
        extra_info = {
            "state": issue_dict["state"],
            "labels": issue_dict["labels"],
            "created_at": issue_dict["created_at"],
            "closed_at": issue_dict["closed_at"],
            "url": issue_dict["_links"]["self"],  # API URL
            "source": issue_dict["web_url"],  # HTML URL, more convenient for humans
        }
        if issue_dict["assignee"]:
            extra_info["assignee"] = issue_dict["assignee"]["username"]
        if issue_dict["author"]:
            extra_info["author"] = issue_dict["author"]["username"]
        document.extra_info = extra_info
        return document

    def_get_project_issues(self, **kwargs):
        project = self._gl.projects.get(self._project_id)
        return project.issues.list(**kwargs)

    def_get_group_issues(self, **kwargs):
        group = self._gl.groups.get(self._group_id)
        return group.issues.list(**kwargs)

    def_to_gitlab_datetime_format(self, dt: Optional[datetime]) -> str:
        return dt.strftime("%Y-%m-%dT%H:%M:%S") if dt else None

    defload_data(
        self,
        assignee: Optional[Union[str, int]] = None,
        author: Optional[Union[str, int]] = None,
        confidential: Optional[bool] = None,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        iids: Optional[List[int]] = None,
        issue_type: Optional[IssueType] = None,
        labels: Optional[List[str]] = None,
        milestone: Optional[str] = None,
        non_archived: Optional[bool] = None,
        scope: Optional[Scope] = None,
        search: Optional[str] = None,
        state: Optional[IssueState] = IssueState.OPEN,
        updated_after: Optional[datetime] = None,
        updated_before: Optional[datetime] = None,
        get_all: bool = False,
        **kwargs: Any,
    ) -> List[Document]:
"""
        Load group or project issues and converts them to documents. Please refer to the GitLab API documentation for the full list of parameters.

        Each issue is converted to a document by doing the following:

            - The doc_id of the document is the issue number.
            - The text of the document is the concatenation of the title and the description of the issue.
            - The extra_info of the document is a dictionary with the following keys:
                - state: State of the issue.
                - labels: List of labels of the issue.
                - created_at: Date when the issue was created.
                - closed_at: Date when the issue was closed. Only present if the issue is closed.
                - url: URL of the issue.
                - source: URL of the issue. More convenient for humans.
                - assignee: username of the user assigned to the issue. Only present if the issue is assigned.

        Args:
            - assignee: Username or ID of the user assigned to the issue.
            - author: Username or ID of the user that created the issue.
            - confidential: Filter confidential issues.
            - created_after: Filter issues created after the specified date.
            - created_before: Filter issues created before the specified date.
            - iids: Return only the issues having the given iid.
            - issue_type: Filter issues by type.
            - labels: List of label names, issues must have all labels to be returned.
            - milestone: The milestone title.
            - non_archived: Return issues from non archived projects.
            - scope: Return issues for the given scope.
            - search: Search issues against their title and description.
            - state: State of the issues to retrieve.
            - updated_after: Filter issues updated after the specified date.
            - updated_before: Filter issues updated before the specified date.
            - get_all: Get all the items without pagination (for a long lists).


        Returns:
            List[Document]: List of documents.

        """
        to_gitlab_datetime_format = self._to_gitlab_datetime_format
        params = {
            "confidential": confidential,
            "created_after": to_gitlab_datetime_format(created_after),
            "created_before": to_gitlab_datetime_format(created_before),
            "iids": iids,
            "issue_type": issue_type.value if issue_type else None,
            "labels": labels,
            "milestone": milestone,
            "non_archived": non_archived,
            "scope": scope.value if scope else None,
            "search": search,
            "state": state.value if state else None,
            "updated_after": to_gitlab_datetime_format(updated_after),
            "updated_before": to_gitlab_datetime_format(updated_before),
            "get_all": get_all,
        }

        if isinstance(assignee, str):
            params["assignee_username"] = assignee
        elif isinstance(assignee, int):
            params["assignee_id"] = assignee

        if isinstance(author, str):
            params["author_username"] = author
        elif isinstance(author, int):
            params["author_id"] = author

        filtered_params = {k: v for k, v in params.items() if v is not None}

        filtered_params.update(kwargs)

        issues = []

        if self._project_id:
            issues = self._get_project_issues(**filtered_params)
        if self._group_id:
            issues = self._get_group_issues(**filtered_params)

        return [self._build_document_from_issue(issue) for issue in issues]

```
 |  
| --- | --- |  
###  IssueState [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gitlab/#llama_index.readers.gitlab.GitLabIssuesReader.IssueState "Permanent link")
Bases: `Enum`
Issue type.
Used to decide what issues to retrieve.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
|  Issues that are open.  |  
|  `CLOSED`  |  Issues that are closed.  |  
|  All issues, open and closed.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gitlab/llama_index/readers/gitlab/issues/base.py`  
| 
```
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
```
 | 
```
classIssueState(enum.Enum):
"""
    Issue type.

    Used to decide what issues to retrieve.

    Attributes:
        - OPEN: Issues that are open.
        - CLOSED: Issues that are closed.
        - ALL: All issues, open and closed.

    """

    OPEN = "opened"
    CLOSED = "closed"
    ALL = "all"

```
 |  
| --- | --- |  
###  IssueType [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gitlab/#llama_index.readers.gitlab.GitLabIssuesReader.IssueType "Permanent link")
Bases: `Enum`
Issue type.
Used to decide what issues to retrieve.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
|  `ISSUE`  |  Issues.  |  
|  `INCIDENT`  |  Incident.  |  
|  `TEST_CASE`  |  Test case.  |  
|  Task.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gitlab/llama_index/readers/gitlab/issues/base.py`  
| 
```
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
```
 | 
```
classIssueType(enum.Enum):
"""
    Issue type.

    Used to decide what issues to retrieve.

    Attributes:
        - ISSUE: Issues.
        - INCIDENT: Incident.
        - TEST_CASE: Test case.
        - TASK: Task.

    """

    ISSUE = "issue"
    INCIDENT = "incident"
    TEST_CASE = "test_case"
    TASK = "task"

```
 |  
| --- | --- |  
###  Scope [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gitlab/#llama_index.readers.gitlab.GitLabIssuesReader.Scope "Permanent link")
Bases: `Enum`
Scope.
Used to determine the scope of the issue.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
|  `CREATED_BY_ME`  |  Issues created by the authenticated user.  |  
|  `ASSIGNED_TO_ME`  |  Issues assigned to the authenticated user.  |  
|  All issues.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gitlab/llama_index/readers/gitlab/issues/base.py`  
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
64
65
66
67
68
69
70
```
 | 
```
classScope(enum.Enum):
"""
    Scope.

    Used to determine the scope of the issue.

    Attributes:
        - CREATED_BY_ME: Issues created by the authenticated user.
        - ASSIGNED_TO_ME: Issues assigned to the authenticated user.
        - ALL: All issues.

    """

    CREATED_BY_ME = "created_by_me"
    ASSIGNED_TO_ME = "assigned_to_me"
    ALL = "all"

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gitlab/#llama_index.readers.gitlab.GitLabIssuesReader.load_data "Permanent link")

```
load_data(
    assignee: Optional[Union[, ]] = None,
    author: Optional[Union[, ]] = None,
    confidential: Optional[] = None,
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None,
    iids: Optional[[]] = None,
    issue_type: Optional[] = None,
    labels: Optional[[]] = None,
    milestone: Optional[] = None,
    non_archived: Optional[] = None,
    scope: Optional[] = None,
    search: Optional[] = None,
    state: Optional[] = ,
    updated_after: Optional[datetime] = None,
    updated_before: Optional[datetime] = None,
    get_all:  = False,
    **kwargs: 
) -> []

```

Load group or project issues and converts them to documents. Please refer to the GitLab API documentation for the full list of parameters.
Each issue is converted to a document by doing the following:

```
- The doc_id of the document is the issue number.
- The text of the document is the concatenation of the title and the description of the issue.
- The extra_info of the document is a dictionary with the following keys:
    - state: State of the issue.
    - labels: List of labels of the issue.
    - created_at: Date when the issue was created.
    - closed_at: Date when the issue was closed. Only present if the issue is closed.
    - url: URL of the issue.
    - source: URL of the issue. More convenient for humans.
    - assignee: username of the user assigned to the issue. Only present if the issue is assigned.

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `- assignee`  |  Username or ID of the user assigned to the issue.  |  _required_  |  
|  `- author`  |  Username or ID of the user that created the issue.  |  _required_  |  
|  `- confidential`  |  Filter confidential issues.  |  _required_  |  
|  `- created_after`  |  Filter issues created after the specified date.  |  _required_  |  
|  `- created_before`  |  Filter issues created before the specified date.  |  _required_  |  
|  `- iids`  |  Return only the issues having the given iid.  |  _required_  |  
|  `- issue_type`  |  Filter issues by type.  |  _required_  |  
|  `- labels`  |  List of label names, issues must have all labels to be returned.  |  _required_  |  
|  `- milestone`  |  The milestone title.  |  _required_  |  
|  `- non_archived`  |  Return issues from non archived projects.  |  _required_  |  
|  `- scope`  |  Return issues for the given scope.  |  _required_  |  
|  `- search`  |  Search issues against their title and description.  |  _required_  |  
|  `- state`  |  State of the issues to retrieve.  |  _required_  |  
|  `- updated_after`  |  Filter issues updated after the specified date.  |  _required_  |  
|  `- updated_before`  |  Filter issues updated before the specified date.  |  _required_  |  
|  `- get_all`  |  Get all the items without pagination (for a long lists).  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gitlab/llama_index/readers/gitlab/issues/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    assignee: Optional[Union[str, int]] = None,
    author: Optional[Union[str, int]] = None,
    confidential: Optional[bool] = None,
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None,
    iids: Optional[List[int]] = None,
    issue_type: Optional[IssueType] = None,
    labels: Optional[List[str]] = None,
    milestone: Optional[str] = None,
    non_archived: Optional[bool] = None,
    scope: Optional[Scope] = None,
    search: Optional[str] = None,
    state: Optional[IssueState] = IssueState.OPEN,
    updated_after: Optional[datetime] = None,
    updated_before: Optional[datetime] = None,
    get_all: bool = False,
    **kwargs: Any,
) -> List[Document]:
"""
    Load group or project issues and converts them to documents. Please refer to the GitLab API documentation for the full list of parameters.

    Each issue is converted to a document by doing the following:

        - The doc_id of the document is the issue number.
        - The text of the document is the concatenation of the title and the description of the issue.
        - The extra_info of the document is a dictionary with the following keys:
            - state: State of the issue.
            - labels: List of labels of the issue.
            - created_at: Date when the issue was created.
            - closed_at: Date when the issue was closed. Only present if the issue is closed.
            - url: URL of the issue.
            - source: URL of the issue. More convenient for humans.
            - assignee: username of the user assigned to the issue. Only present if the issue is assigned.

    Args:
        - assignee: Username or ID of the user assigned to the issue.
        - author: Username or ID of the user that created the issue.
        - confidential: Filter confidential issues.
        - created_after: Filter issues created after the specified date.
        - created_before: Filter issues created before the specified date.
        - iids: Return only the issues having the given iid.
        - issue_type: Filter issues by type.
        - labels: List of label names, issues must have all labels to be returned.
        - milestone: The milestone title.
        - non_archived: Return issues from non archived projects.
        - scope: Return issues for the given scope.
        - search: Search issues against their title and description.
        - state: State of the issues to retrieve.
        - updated_after: Filter issues updated after the specified date.
        - updated_before: Filter issues updated before the specified date.
        - get_all: Get all the items without pagination (for a long lists).


    Returns:
        List[Document]: List of documents.

    """
    to_gitlab_datetime_format = self._to_gitlab_datetime_format
    params = {
        "confidential": confidential,
        "created_after": to_gitlab_datetime_format(created_after),
        "created_before": to_gitlab_datetime_format(created_before),
        "iids": iids,
        "issue_type": issue_type.value if issue_type else None,
        "labels": labels,
        "milestone": milestone,
        "non_archived": non_archived,
        "scope": scope.value if scope else None,
        "search": search,
        "state": state.value if state else None,
        "updated_after": to_gitlab_datetime_format(updated_after),
        "updated_before": to_gitlab_datetime_format(updated_before),
        "get_all": get_all,
    }

    if isinstance(assignee, str):
        params["assignee_username"] = assignee
    elif isinstance(assignee, int):
        params["assignee_id"] = assignee

    if isinstance(author, str):
        params["author_username"] = author
    elif isinstance(author, int):
        params["author_id"] = author

    filtered_params = {k: v for k, v in params.items() if v is not None}

    filtered_params.update(kwargs)

    issues = []

    if self._project_id:
        issues = self._get_project_issues(**filtered_params)
    if self._group_id:
        issues = self._get_group_issues(**filtered_params)

    return [self._build_document_from_issue(issue) for issue in issues]

```
 |  
| --- | --- |  
##  GitLabRepositoryReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gitlab/#llama_index.readers.gitlab.GitLabRepositoryReader "Permanent link")
Bases: 
Source code in `llama-index-integrations/readers/llama-index-readers-gitlab/llama_index/readers/gitlab/repository/base.py`  
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
```
 | 
```
classGitLabRepositoryReader(BaseReader):
    def__init__(
        self,
        gitlab_client: gitlab.Gitlab,
        project_id: int,
        use_parser: bool = False,
        verbose: bool = False,
    ):
        super().__init__()

        self._gl = gitlab_client
        self._use_parser = use_parser
        self._verbose = verbose
        self._project_url = f"{gitlab_client.api_url}/projects/{project_id}"

        self._project = gitlab_client.projects.get(project_id)

    def_parse_file_content(self, file_properties: dict, file_content: str) -> Document:
        raise NotImplementedError

    def_load_single_file(self, file_path: str, ref: Optional[str] = None) -> Document:
        file = self._project.files.get(file_path=file_path, ref=ref)
        file_properties = file.asdict()
        file_content = file.decode()

        if self._use_parser:
            return self._parse_file_content(file_properties, file_content)

        return Document(
            doc_id=file_properties["blob_id"],
            text=file_content,
            extra_info={
                "file_path": file_properties["file_path"],
                "file_name": file_properties["file_name"],
                "size": file_properties["size"],
                "url": f"{self._project_url}/projects/repository/files/{file_properties['file_path']}/raw",
            },
        )

    defload_data(
        self,
        ref: str,
        file_path: Optional[str] = None,
        path: Optional[str] = None,
        recursive: bool = False,
        iterator: bool = False,
    ) -> List[Document]:
"""
        Load data from a GitLab repository.

        Args:
            ref: The name of a repository branch or commit id
            file_path: Path to the file to load.
            path: Path to the directory to load.
            recursive: Whether to load files recursively.
            iterator: Return a generator handling API pagination automatically

        Returns:
            List[Document]: List of documents loaded from the repository

        """
        if file_path:
            return [self._load_single_file(file_path, ref)]

        project = self._project

        params = {
            "ref": ref,
            "path": path,
            "recursive": recursive,
            "iterator": iterator,
        }

        filtered_params = {k: v for k, v in params.items() if v is not None}

        repo_items = project.repository_tree(**filtered_params)

        documents = []

        for item in repo_items:
            if item["type"] == "blob":
                documents.append(self._load_single_file(item["path"], ref))

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gitlab/#llama_index.readers.gitlab.GitLabRepositoryReader.load_data "Permanent link")

```
load_data(
    ref: ,
    file_path: Optional[] = None,
    path: Optional[] = None,
    recursive:  = False,
    iterator:  = False,
) -> []

```

Load data from a GitLab repository.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref`  |  The name of a repository branch or commit id  |  _required_  |  
|  `file_path`  |  `Optional[str]`  |  Path to the file to load.  |  `None`  |  
|  `path`  |  `Optional[str]`  |  Path to the directory to load.  |  `None`  |  
|  `recursive`  |  `bool`  |  Whether to load files recursively.  |  `False`  |  
|  `iterator`  |  `bool`  |  Return a generator handling API pagination automatically  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents loaded from the repository  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gitlab/llama_index/readers/gitlab/repository/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    ref: str,
    file_path: Optional[str] = None,
    path: Optional[str] = None,
    recursive: bool = False,
    iterator: bool = False,
) -> List[Document]:
"""
    Load data from a GitLab repository.

    Args:
        ref: The name of a repository branch or commit id
        file_path: Path to the file to load.
        path: Path to the directory to load.
        recursive: Whether to load files recursively.
        iterator: Return a generator handling API pagination automatically

    Returns:
        List[Document]: List of documents loaded from the repository

    """
    if file_path:
        return [self._load_single_file(file_path, ref)]

    project = self._project

    params = {
        "ref": ref,
        "path": path,
        "recursive": recursive,
        "iterator": iterator,
    }

    filtered_params = {k: v for k, v in params.items() if v is not None}

    repo_items = project.repository_tree(**filtered_params)

    documents = []

    for item in repo_items:
        if item["type"] == "blob":
            documents.append(self._load_single_file(item["path"], ref))

    return documents

```
 |  
| --- | --- |  
options: members: - GitLabIssuesReader - GitLabRepositoryReader
