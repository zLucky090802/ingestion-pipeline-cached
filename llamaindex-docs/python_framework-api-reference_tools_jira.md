# Jira
##  JiraToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira/#llama_index.tools.jira.JiraToolSpec "Permanent link")
Bases: 
Atlassian Jira Tool Spec.
Source code in `llama-index-integrations/tools/llama-index-tools-jira/llama_index/tools/jira/base.py`  
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
```
 | 
```
classJiraToolSpec(BaseToolSpec):
"""Atlassian Jira Tool Spec."""

    spec_functions = [
        "jira_issues_query",
        "jira_issue_query",
        "jira_comments_query",
        "jira_all_projects",
    ]

    def__init__(
        self,
        email: Optional[str] = None,
        api_token: Optional[str] = None,
        server_url: Optional[str] = None,
    ) -> None:
"""Initialize the Atlassian Jira tool spec."""
        fromjiraimport JIRA

        if email and api_token and server_url:
            self.jira = JIRA(
                basic_auth=(email, api_token),
                server=server_url,
            )
        else:
            raise Exception("Error: Please provide Jira api credentials to continue")

    defjira_all_projects(self) -> dict:
"""
        Retrieve all projects from the Atlassian Jira account.

        This method fetches a list of projects from Jira and returns them in a structured
        format, including the project ID, key, and name. If an error occurs during
        retrieval, an error message is returned.

        Returns:
            dict: A dictionary containing:
                - 'error' (bool): Indicates whether the request was successful.
                - 'message' (str): A description of the result.
                - 'projects' (list, optional): A list of projects with their details
                  (ID, key, name) if retrieval is successful.

        """
        try:
            projects = self.jira.projects()

            if projects:
                return {
                    "error": False,
                    "message": "All Projects from the account",
                    "projects": [
                        {"id": project.id, "key": project.key, "name": project.name}
                        for project in projects
                    ],
                }
        except Exception:
            pass

        return {"error": True, "message": "Unable to fetch projects"}

    defjira_comments_query(
        self, issue_key: str, author_email: Optional[str] = None
    ) -> dict:
"""
        Retrieve all comments for a given Jira issue, optionally filtering by the author's email.

        This function fetches comments from a specified Jira issue and returns them as a structured
        JSON response. If an `author_email` is provided, only comments from that specific author
        will be included.

        Args:
            issue_key (str): The Jira issue key for which to retrieve comments.
            author_email (str, Optional): filters comments by the author's email.

        Returns:
            dict: A dictionary containing:
                - 'error' (bool): Indicates whether the request was successful.
                - 'message' (str): A descriptive message about the result.
                - 'comments' (list, optional): A list of comments, where each comment includes:
                    - 'id' (str): The unique identifier of the comment.
                    - 'author' (str): The display name of the comment's author.
                    - 'author_email' (str): The author's email address.
                    - 'body' (str): The content of the comment.
                    - 'created_at' (str): The timestamp when the comment was created.
                    - 'updated_at' (str): The timestamp when the comment was last updated.

        """
        error = False

        try:
            issue = self.jira.issue(issue_key)

            all_comments = list(issue.fields.comment.comments)
            filtered_results = []

            for comment in all_comments:
                if (
                    author_email is not None
                    and author_email not in comment.author.emailAddress
                ):
                    continue

                filtered_results.append(
                    {
                        "id": comment.id,
                        "author": comment.author.displayName,
                        "author_email": comment.author.emailAddress,
                        "body": comment.body,
                        "created_at": comment.created,
                        "updated_at": comment.updated,
                    }
                )

            message = f'All the comments in the issue key "{issue_key}"'
        except Exception:
            error = True
            message = "Unable to fetch comments due to some error"

        response = {"error": error, "message": message}

        if error is False:
            response["comments"] = filtered_results

        return response

    defjira_issue_query(
        self, issue_key: str, just_payload: bool = False
    ) -> Union[None, dict]:
"""
        Retrieves detailed information about a specific Jira issue.

        This method fetches issue details such as summary, description, type, project, priority, status,
        reporter, assignee, labels, and timestamps. The response structure can be adjusted using the
        `just_payload` flag.

        Args:
            issue_key (str): The unique key or ticket number of the Jira issue.
            just_payload (bool, optional): If True, returns only the issue payload without the response
                                           metadata. Defaults to False.

        Returns:
            Union[None, dict]: A dictionary containing issue details if found, or an error response if the issue
                               cannot be retrieved.

        Example:
            > jira_client.load_issue("JIRA-123", just_payload=True)

                'key': 'JIRA-123',
                'summary': 'Fix login bug',
                'description': 'Users unable to log in under certain conditions...',
                'type': 'Bug',
                'project_name': 'Web App',
                'priority': 'High',
                'status': 'In Progress',
                'reporter': 'John Doe',
                'reporter_email': 'john.doe@example.com',
                'labels': ['authentication', 'urgent'],
                'created_at': '2024-02-01T10:15:30.000Z',
                'updated_at': '2024-02-02T12:20:45.000Z',
                'assignee': 'Jane Smith',
                'assignee_email': 'jane.smith@example.com'


        """
        error = False
        try:
            issue = self.jira.issue(issue_key)

            payload = {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description,
                "type": issue.fields.issuetype.name,
                "project_name": issue.fields.project.name,
                "priority": issue.fields.priority.name,
                "status": issue.fields.status.name,
                "reporter": issue.fields.reporter.displayName
                if issue.fields.reporter
                else None,
                "reporter_email": issue.fields.reporter.emailAddress
                if issue.fields.reporter
                else None,
                "labels": issue.fields.labels,
                "created_at": issue.fields.created,
                "updated_at": issue.fields.updated,
                "assignee": issue.fields.assignee.displayName
                if issue.fields.assignee
                else None,
                "assignee_email": issue.fields.assignee.emailAddress
                if issue.fields.assignee
                else None,
            }

            message = f"Details of the issue: {issue.key}"

        except Exception:
            error = True
            message = "Unable to fetch issue due to some error"

        if error is False and just_payload:
            return payload

        response = {"error": error, "message": message}

        if error is False:
            response["result"] = payload

        return response

    defjira_issues_query(self, keyword: str, max_results: int = 10) -> dict:
"""
        Search for Jira issues containing a specific keyword.

        This function searches for Jira issues where the specified `keyword` appears in the summary, description, or comments.
        The results are sorted by creation date in descending order.

        Args:
            keyword (str): The keyword to search for within issue summaries, descriptions, or comments.
            max_results (int, optional): The maximum number of issues to return. Defaults to 10. If set higher than 100, it will be limited to 100.

        Returns:
            dict: A dictionary with the following structure:
                - 'error' (bool): Indicates if an error occurred during the fetch operation.
                - 'message' (str): Describes the outcome of the operation.
                - 'results' (list, optional): A list of issues matching the search criteria, present only if no error occurred.

        """
        error = False

        max_results = min(max_results, 100)

        # if custom_query is not None:
        #     jql = custom_query
        # else:
        jql = f'summary ~ "{keyword}" or description ~ "{keyword}" or text ~ "{keyword}" order by created desc'

        try:
            issues = [
                self.jira_issue_query(issue.key, just_payload=True)
                for issue in self.jira.search_issues(jql, maxResults=max_results)
            ]

            message = "All the issues with specific matching conditions"
        except Exception:
            error = True
            message = "Unable to fetch issue due to some error"

        response = {"error": error, "message": message}

        if error is False:
            response["results"] = issues

        return response

```
 |  
| --- | --- |  
###  jira_all_projects [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira/#llama_index.tools.jira.JiraToolSpec.jira_all_projects "Permanent link")

```
jira_all_projects() -> 

```

Retrieve all projects from the Atlassian Jira account.
This method fetches a list of projects from Jira and returns them in a structured format, including the project ID, key, and name. If an error occurs during retrieval, an error message is returned.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `dict`  |  `dict`  |  A dictionary containing: - 'error' (bool): Indicates whether the request was successful. - 'message' (str): A description of the result. - 'projects' (list, optional): A list of projects with their details (ID, key, name) if retrieval is successful.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-jira/llama_index/tools/jira/base.py`  
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
```
 | 
```
defjira_all_projects(self) -> dict:
"""
    Retrieve all projects from the Atlassian Jira account.

    This method fetches a list of projects from Jira and returns them in a structured
    format, including the project ID, key, and name. If an error occurs during
    retrieval, an error message is returned.

    Returns:
        dict: A dictionary containing:
            - 'error' (bool): Indicates whether the request was successful.
            - 'message' (str): A description of the result.
            - 'projects' (list, optional): A list of projects with their details
              (ID, key, name) if retrieval is successful.

    """
    try:
        projects = self.jira.projects()

        if projects:
            return {
                "error": False,
                "message": "All Projects from the account",
                "projects": [
                    {"id": project.id, "key": project.key, "name": project.name}
                    for project in projects
                ],
            }
    except Exception:
        pass

    return {"error": True, "message": "Unable to fetch projects"}

```
 |  
| --- | --- |  
###  jira_comments_query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira/#llama_index.tools.jira.JiraToolSpec.jira_comments_query "Permanent link")

```
jira_comments_query(
    issue_key: , author_email: Optional[] = None
) -> 

```

Retrieve all comments for a given Jira issue, optionally filtering by the author's email.
This function fetches comments from a specified Jira issue and returns them as a structured JSON response. If an `author_email` is provided, only comments from that specific author will be included.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `issue_key`  |  The Jira issue key for which to retrieve comments.  |  _required_  |  
|  `author_email`  |  `(str, Optional)`  |  filters comments by the author's email.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `dict`  |  `dict`  |  A dictionary containing: - 'error' (bool): Indicates whether the request was successful. - 'message' (str): A descriptive message about the result. - 'comments' (list, optional): A list of comments, where each comment includes: - 'id' (str): The unique identifier of the comment. - 'author' (str): The display name of the comment's author. - 'author_email' (str): The author's email address. - 'body' (str): The content of the comment. - 'created_at' (str): The timestamp when the comment was created. - 'updated_at' (str): The timestamp when the comment was last updated.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-jira/llama_index/tools/jira/base.py`  
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
```
 | 
```
defjira_comments_query(
    self, issue_key: str, author_email: Optional[str] = None
) -> dict:
"""
    Retrieve all comments for a given Jira issue, optionally filtering by the author's email.

    This function fetches comments from a specified Jira issue and returns them as a structured
    JSON response. If an `author_email` is provided, only comments from that specific author
    will be included.

    Args:
        issue_key (str): The Jira issue key for which to retrieve comments.
        author_email (str, Optional): filters comments by the author's email.

    Returns:
        dict: A dictionary containing:
            - 'error' (bool): Indicates whether the request was successful.
            - 'message' (str): A descriptive message about the result.
            - 'comments' (list, optional): A list of comments, where each comment includes:
                - 'id' (str): The unique identifier of the comment.
                - 'author' (str): The display name of the comment's author.
                - 'author_email' (str): The author's email address.
                - 'body' (str): The content of the comment.
                - 'created_at' (str): The timestamp when the comment was created.
                - 'updated_at' (str): The timestamp when the comment was last updated.

    """
    error = False

    try:
        issue = self.jira.issue(issue_key)

        all_comments = list(issue.fields.comment.comments)
        filtered_results = []

        for comment in all_comments:
            if (
                author_email is not None
                and author_email not in comment.author.emailAddress
            ):
                continue

            filtered_results.append(
                {
                    "id": comment.id,
                    "author": comment.author.displayName,
                    "author_email": comment.author.emailAddress,
                    "body": comment.body,
                    "created_at": comment.created,
                    "updated_at": comment.updated,
                }
            )

        message = f'All the comments in the issue key "{issue_key}"'
    except Exception:
        error = True
        message = "Unable to fetch comments due to some error"

    response = {"error": error, "message": message}

    if error is False:
        response["comments"] = filtered_results

    return response

```
 |  
| --- | --- |  
###  jira_issue_query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira/#llama_index.tools.jira.JiraToolSpec.jira_issue_query "Permanent link")

```
jira_issue_query(
    issue_key: , just_payload:  = False
) -> Union[None, ]

```

Retrieves detailed information about a specific Jira issue.
This method fetches issue details such as summary, description, type, project, priority, status, reporter, assignee, labels, and timestamps. The response structure can be adjusted using the `just_payload` flag.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `issue_key`  |  The unique key or ticket number of the Jira issue.  |  _required_  |  
|  `just_payload`  |  `bool`  |  If True, returns only the issue payload without the response metadata. Defaults to False.  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Union[None, dict]`  |  Union[None, dict]: A dictionary containing issue details if found, or an error response if the issue cannot be retrieved.  |  
Example
> jira_client.load_issue("JIRA-123", just_payload=True) { 'key': 'JIRA-123', 'summary': 'Fix login bug', 'description': 'Users unable to log in under certain conditions...', 'type': 'Bug', 'project_name': 'Web App', 'priority': 'High', 'status': 'In Progress', 'reporter': 'John Doe', 'reporter_email': 'john.doe@example.com', 'labels': ['authentication', 'urgent'], 'created_at': '2024-02-01T10:15:30.000Z', 'updated_at': '2024-02-02T12:20:45.000Z', 'assignee': 'Jane Smith', 'assignee_email': 'jane.smith@example.com' }
Source code in `llama-index-integrations/tools/llama-index-tools-jira/llama_index/tools/jira/base.py`  
| 
```
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
```
 | 
```
defjira_issue_query(
    self, issue_key: str, just_payload: bool = False
) -> Union[None, dict]:
"""
    Retrieves detailed information about a specific Jira issue.

    This method fetches issue details such as summary, description, type, project, priority, status,
    reporter, assignee, labels, and timestamps. The response structure can be adjusted using the
    `just_payload` flag.

    Args:
        issue_key (str): The unique key or ticket number of the Jira issue.
        just_payload (bool, optional): If True, returns only the issue payload without the response
                                       metadata. Defaults to False.

    Returns:
        Union[None, dict]: A dictionary containing issue details if found, or an error response if the issue
                           cannot be retrieved.

    Example:
        > jira_client.load_issue("JIRA-123", just_payload=True)

            'key': 'JIRA-123',
            'summary': 'Fix login bug',
            'description': 'Users unable to log in under certain conditions...',
            'type': 'Bug',
            'project_name': 'Web App',
            'priority': 'High',
            'status': 'In Progress',
            'reporter': 'John Doe',
            'reporter_email': 'john.doe@example.com',
            'labels': ['authentication', 'urgent'],
            'created_at': '2024-02-01T10:15:30.000Z',
            'updated_at': '2024-02-02T12:20:45.000Z',
            'assignee': 'Jane Smith',
            'assignee_email': 'jane.smith@example.com'


    """
    error = False
    try:
        issue = self.jira.issue(issue_key)

        payload = {
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "type": issue.fields.issuetype.name,
            "project_name": issue.fields.project.name,
            "priority": issue.fields.priority.name,
            "status": issue.fields.status.name,
            "reporter": issue.fields.reporter.displayName
            if issue.fields.reporter
            else None,
            "reporter_email": issue.fields.reporter.emailAddress
            if issue.fields.reporter
            else None,
            "labels": issue.fields.labels,
            "created_at": issue.fields.created,
            "updated_at": issue.fields.updated,
            "assignee": issue.fields.assignee.displayName
            if issue.fields.assignee
            else None,
            "assignee_email": issue.fields.assignee.emailAddress
            if issue.fields.assignee
            else None,
        }

        message = f"Details of the issue: {issue.key}"

    except Exception:
        error = True
        message = "Unable to fetch issue due to some error"

    if error is False and just_payload:
        return payload

    response = {"error": error, "message": message}

    if error is False:
        response["result"] = payload

    return response

```
 |  
| --- | --- |  
###  jira_issues_query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira/#llama_index.tools.jira.JiraToolSpec.jira_issues_query "Permanent link")

```
jira_issues_query(
    keyword: , max_results:  = 10
) -> 

```

Search for Jira issues containing a specific keyword.
This function searches for Jira issues where the specified `keyword` appears in the summary, description, or comments. The results are sorted by creation date in descending order.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `keyword`  |  The keyword to search for within issue summaries, descriptions, or comments.  |  _required_  |  
|  `max_results`  |  The maximum number of issues to return. Defaults to 10. If set higher than 100, it will be limited to 100.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `dict`  |  `dict`  |  A dictionary with the following structure: - 'error' (bool): Indicates if an error occurred during the fetch operation. - 'message' (str): Describes the outcome of the operation. - 'results' (list, optional): A list of issues matching the search criteria, present only if no error occurred.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-jira/llama_index/tools/jira/base.py`  
| 
```
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
```
 | 
```
defjira_issues_query(self, keyword: str, max_results: int = 10) -> dict:
"""
    Search for Jira issues containing a specific keyword.

    This function searches for Jira issues where the specified `keyword` appears in the summary, description, or comments.
    The results are sorted by creation date in descending order.

    Args:
        keyword (str): The keyword to search for within issue summaries, descriptions, or comments.
        max_results (int, optional): The maximum number of issues to return. Defaults to 10. If set higher than 100, it will be limited to 100.

    Returns:
        dict: A dictionary with the following structure:
            - 'error' (bool): Indicates if an error occurred during the fetch operation.
            - 'message' (str): Describes the outcome of the operation.
            - 'results' (list, optional): A list of issues matching the search criteria, present only if no error occurred.

    """
    error = False

    max_results = min(max_results, 100)

    # if custom_query is not None:
    #     jql = custom_query
    # else:
    jql = f'summary ~ "{keyword}" or description ~ "{keyword}" or text ~ "{keyword}" order by created desc'

    try:
        issues = [
            self.jira_issue_query(issue.key, just_payload=True)
            for issue in self.jira.search_issues(jql, maxResults=max_results)
        ]

        message = "All the issues with specific matching conditions"
    except Exception:
        error = True
        message = "Unable to fetch issue due to some error"

    response = {"error": error, "message": message}

    if error is False:
        response["results"] = issues

    return response

```
 |  
| --- | --- |  
options: members: - JiraToolSpec
