# Jira issue
##  JiraIssueToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira_issue/#llama_index.tools.jira_issue.JiraIssueToolSpec "Permanent link")
Bases: 
Atlassian Jira Issue Tool Spec.
Source code in `llama-index-integrations/tools/llama-index-tools-jira-issue/llama_index/tools/jira_issue/base.py`  
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
```
 | 
```
classJiraIssueToolSpec(BaseToolSpec):
"""Atlassian Jira Issue Tool Spec."""

    spec_functions = [
        "search_issues",
        "create_issue",
        "add_comment_to_issue",
        "update_issue_summary",
        "update_issue_assignee",
        "update_issue_status",
        "update_issue_due_date",
        "delete_issue",
    ]

    def__init__(
        self,
        email: str = os.environ.get("JIRA_ACCOUNT_EMAIL", ""),
        api_key: Optional[str] = os.environ.get("JIRA_API_KEY", ""),
        server_url: Optional[str] = os.environ.get("JIRA_SERVER_URL", ""),
    ) -> None:
        if email and api_key and server_url:
            self.jira = JIRA(
                basic_auth=(email, api_key),
                server=server_url,
            )
        else:
            raise Exception("Please provide Jira credentials to continue.")

    defsearch_issues(self, jql_str: str) -> Dict[str, Any]:
"""
        Search for JIRA issues using JQL.

        Args:
            jql_str (str): JQL query string to search for issues.

        Returns:
            Dict[str, Any]: A dictionary containing the search results or error message.

        """
        try:
            issues = self.jira.search_issues(jql_str)

            if issues:
                return {
                    "error": False,
                    "message": "Issues found",
                    "issues": [
                        {
                            "key": issue.key,
                            "summary": issue.fields.summary,
                            "status": issue.fields.status.name,
                            "assignee": issue.fields.assignee.displayName
                            if issue.fields.assignee
                            else None,
                        }
                        for issue in issues
                    ],
                }
            else:
                return {
                    "error": True,
                    "message": "No issues found.",
                }
        except Exception as e:
            return {
                "error": True,
                "message": f"Failed to search issues: {e!s}",
            }

    defcreate_issue(
        self,
        project_key: str = "KAN",
        summary: str = "New Issue",
        description: Optional[str] = None,
        issue_type: Literal["Task", "Bug", "Epic"] = "Task",
    ) -> Dict[str, Any]:
"""
        Create a new JIRA issue.

        Args:
            project_key (str): The key of the project to create the issue in (default is "KAN").
            summary (str): The summary of the new issue (default is "New Issue").
            description (Optional[str]): The description of the new issue.
            issue_type (str): The type of the issue to create, can be "Task", "Bug", or "Epic" (default is "Task").

        Returns:
            Dict[str, Any]: A dictionary indicating success or failure of the operation.

        """
        try:
            new_issue = self.jira.create_issue(
                project=project_key,
                summary=summary,
                description=description,
                issuetype={"name": issue_type},
            )
            return {
                "error": False,
                "message": f"Issue {new_issue.key} created successfully.",
                "issue_key": new_issue.key,
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"Failed to create new issue: {e!s}",
            }

    defadd_comment_to_issue(self, issue_key: str, comment: str) -> Dict[str, Any]:
"""
        Add a comment to a JIRA issue.

        Args:
            issue_key (str): The key of the JIRA issue to comment on.
            comment (str): The comment text to add.

        Returns:
            Dict[str, Any]: A dictionary indicating success or failure of the operation.

        """
        try:
            issue = self.jira.issue(issue_key)
            self.jira.add_comment(issue, comment)
            return {"error": False, "message": f"Comment added to issue {issue_key}."}
        except Exception as e:
            return {
                "error": True,
                "message": f"Failed to add comment to issue {issue_key}: {e!s}",
            }

    defupdate_issue_summary(
        self, issue_key: str, new_summary: str, notify: bool = False
    ) -> Dict[str, Any]:
"""
        Update the summary of a JIRA issue.

        Args:
            issue_key (str): The key of the JIRA issue to update.
            new_summary (str): The new summary text for the issue.
            notify (bool): Whether to email watchers of the issue about the update.

        Returns:
            Dict[str, Any]: A dictionary indicating success or failure of the operation.

        """
        try:
            issue = self.jira.issue(issue_key)
            issue.update(summary=new_summary, notify=notify)
            return {"error": False, "message": f"Issue {issue_key} summary updated."}
        except Exception as e:
            return {
                "error": True,
                "message": f"Failed to update issue {issue_key}: {e!s}",
            }

    defupdate_issue_assignee(self, issue_key, assignee_full_name):
"""
        Update the assignee of the Jira issue using the assignee's full name.

        Args:
            issue_key (str): The key of the Jira issue to update.
            assignee_full_name (str): The full name of the user to assign the issue to.

        Returns:
            Dict[str, Any]: A dictionary indicating success or failure of the operation.

        """
        try:
            # Search for users by display name
            users = self.jira.search_users(query=assignee_full_name)

            # Find exact match for the full name
            target_user = None
            for user in users:
                if user.displayName.lower() == assignee_full_name.lower():
                    target_user = user
                    break

            if not target_user:
                return {
                    "error": True,
                    "message": f"User with full name '{assignee_full_name}' not found",
                }

            # Get the issue
            issue = self.jira.issue(issue_key)
            issue.update(assignee={"accountId": target_user.accountId})

            return {
                "error": False,
                "message": f"Issue {issue_key} successfully assigned to {assignee_full_name}",
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"An error occurred while updating the assignee: {e!s}",
            }

    defupdate_issue_status(
        self, issue_key: str, new_status: Literal["To Do", "In Progress", "Done"]
    ) -> Dict[str, Any]:
"""
        Update the status of a JIRA issue.

        Args:
            issue_key (str): The key of the JIRA issue to update.
            new_status (str): The new status to set for the issue.

        Returns:
            Dict[str, Any]: A dictionary indicating success or failure of the operation.

        """
        try:
            issue = self.jira.issue(issue_key)
            transitions = self.jira.transitions(issue)
            transition_id = next(
                (t["id"] for t in transitions if t["name"] == new_status), None
            )

            if transition_id:
                self.jira.transition_issue(issue, transition_id)
                return {
                    "error": False,
                    "message": f"Issue {issue_key} status updated to {new_status}.",
                }
            else:
                available_statuses = [t["name"] for t in transitions]
                return {
                    "error": True,
                    "message": f"Status '{new_status}' not available for issue {issue_key}. Available transitions: {available_statuses}",
                }
        except Exception as e:
            return {
                "error": True,
                "message": f"Failed to update status for issue {issue_key}: {e!s}",
            }

    defupdate_issue_due_date(
        self, issue_key: str, due_date: Optional[str] = None
    ) -> Dict[str, Any]:
"""
        Update the due date of a JIRA issue.

        Args:
            issue_key (str): The key of the JIRA issue to update.
            due_date (Optional[str]): The new due date in 'YYYY-MM-DD' format.

        Returns:
            Dict[str, Any]: A dictionary indicating success or failure of the operation.

        """
        if due_date:
            try:
                fromdatetimeimport datetime

                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                return {
                    "error": True,
                    "message": "Invalid date format. Use YYYY-MM-DD.",
                }
        try:
            issue = self.jira.issue(issue_key)
            issue.update(duedate=due_date)
            return {
                "error": False,
                "message": f"Issue {issue_key} due date {'updated'ifdue_dateelse'cleared'}.",
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"Failed to update due date for issue {issue_key}: {e!s}",
            }

    defdelete_issue(self, issue_key: str) -> Dict[str, Any]:
"""
        Delete a JIRA issue.

        Args:
            issue_key (str): The key of the JIRA issue to delete.

        Returns:
            Dict[str, Any]: A dictionary indicating success or failure of the operation.

        """
        try:
            issue = self.jira.issue(issue_key)
            issue.delete()
            return {
                "error": False,
                "message": f"Issue {issue_key} deleted successfully.",
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"Failed to delete issue {issue_key}: {e!s}",
            }

```
 |  
| --- | --- |  
###  search_issues [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira_issue/#llama_index.tools.jira_issue.JiraIssueToolSpec.search_issues "Permanent link")

```
search_issues(jql_str: ) -> [, ]

```

Search for JIRA issues using JQL.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `jql_str`  |  JQL query string to search for issues.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: A dictionary containing the search results or error message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-jira-issue/llama_index/tools/jira_issue/base.py`  
| 
```
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
```
 | 
```
defsearch_issues(self, jql_str: str) -> Dict[str, Any]:
"""
    Search for JIRA issues using JQL.

    Args:
        jql_str (str): JQL query string to search for issues.

    Returns:
        Dict[str, Any]: A dictionary containing the search results or error message.

    """
    try:
        issues = self.jira.search_issues(jql_str)

        if issues:
            return {
                "error": False,
                "message": "Issues found",
                "issues": [
                    {
                        "key": issue.key,
                        "summary": issue.fields.summary,
                        "status": issue.fields.status.name,
                        "assignee": issue.fields.assignee.displayName
                        if issue.fields.assignee
                        else None,
                    }
                    for issue in issues
                ],
            }
        else:
            return {
                "error": True,
                "message": "No issues found.",
            }
    except Exception as e:
        return {
            "error": True,
            "message": f"Failed to search issues: {e!s}",
        }

```
 |  
| --- | --- |  
###  create_issue [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira_issue/#llama_index.tools.jira_issue.JiraIssueToolSpec.create_issue "Permanent link")

```
create_issue(
    project_key:  = "KAN",
    summary:  = "New Issue",
    description: Optional[] = None,
    issue_type: Literal["Task", "Bug", "Epic"] = "Task",
) -> [, ]

```

Create a new JIRA issue.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `project_key`  |  The key of the project to create the issue in (default is "KAN").  |  `'KAN'`  |  
|  `summary`  |  The summary of the new issue (default is "New Issue").  |  `'New Issue'`  |  
|  `description`  |  `Optional[str]`  |  The description of the new issue.  |  `None`  |  
|  `issue_type`  |  The type of the issue to create, can be "Task", "Bug", or "Epic" (default is "Task").  |  `'Task'`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: A dictionary indicating success or failure of the operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-jira-issue/llama_index/tools/jira_issue/base.py`  
| 
```
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
```
 | 
```
defcreate_issue(
    self,
    project_key: str = "KAN",
    summary: str = "New Issue",
    description: Optional[str] = None,
    issue_type: Literal["Task", "Bug", "Epic"] = "Task",
) -> Dict[str, Any]:
"""
    Create a new JIRA issue.

    Args:
        project_key (str): The key of the project to create the issue in (default is "KAN").
        summary (str): The summary of the new issue (default is "New Issue").
        description (Optional[str]): The description of the new issue.
        issue_type (str): The type of the issue to create, can be "Task", "Bug", or "Epic" (default is "Task").

    Returns:
        Dict[str, Any]: A dictionary indicating success or failure of the operation.

    """
    try:
        new_issue = self.jira.create_issue(
            project=project_key,
            summary=summary,
            description=description,
            issuetype={"name": issue_type},
        )
        return {
            "error": False,
            "message": f"Issue {new_issue.key} created successfully.",
            "issue_key": new_issue.key,
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"Failed to create new issue: {e!s}",
        }

```
 |  
| --- | --- |  
###  add_comment_to_issue [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira_issue/#llama_index.tools.jira_issue.JiraIssueToolSpec.add_comment_to_issue "Permanent link")

```
add_comment_to_issue(
    issue_key: , comment: 
) -> [, ]

```

Add a comment to a JIRA issue.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `issue_key`  |  The key of the JIRA issue to comment on.  |  _required_  |  
|  `comment`  |  The comment text to add.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: A dictionary indicating success or failure of the operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-jira-issue/llama_index/tools/jira_issue/base.py`  
| 
```
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
```
 | 
```
defadd_comment_to_issue(self, issue_key: str, comment: str) -> Dict[str, Any]:
"""
    Add a comment to a JIRA issue.

    Args:
        issue_key (str): The key of the JIRA issue to comment on.
        comment (str): The comment text to add.

    Returns:
        Dict[str, Any]: A dictionary indicating success or failure of the operation.

    """
    try:
        issue = self.jira.issue(issue_key)
        self.jira.add_comment(issue, comment)
        return {"error": False, "message": f"Comment added to issue {issue_key}."}
    except Exception as e:
        return {
            "error": True,
            "message": f"Failed to add comment to issue {issue_key}: {e!s}",
        }

```
 |  
| --- | --- |  
###  update_issue_summary [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira_issue/#llama_index.tools.jira_issue.JiraIssueToolSpec.update_issue_summary "Permanent link")

```
update_issue_summary(
    issue_key: , new_summary: , notify:  = False
) -> [, ]

```

Update the summary of a JIRA issue.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `issue_key`  |  The key of the JIRA issue to update.  |  _required_  |  
|  `new_summary`  |  The new summary text for the issue.  |  _required_  |  
|  `notify`  |  `bool`  |  Whether to email watchers of the issue about the update.  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: A dictionary indicating success or failure of the operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-jira-issue/llama_index/tools/jira_issue/base.py`  
| 
```
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
```
 | 
```
defupdate_issue_summary(
    self, issue_key: str, new_summary: str, notify: bool = False
) -> Dict[str, Any]:
"""
    Update the summary of a JIRA issue.

    Args:
        issue_key (str): The key of the JIRA issue to update.
        new_summary (str): The new summary text for the issue.
        notify (bool): Whether to email watchers of the issue about the update.

    Returns:
        Dict[str, Any]: A dictionary indicating success or failure of the operation.

    """
    try:
        issue = self.jira.issue(issue_key)
        issue.update(summary=new_summary, notify=notify)
        return {"error": False, "message": f"Issue {issue_key} summary updated."}
    except Exception as e:
        return {
            "error": True,
            "message": f"Failed to update issue {issue_key}: {e!s}",
        }

```
 |  
| --- | --- |  
###  update_issue_assignee [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira_issue/#llama_index.tools.jira_issue.JiraIssueToolSpec.update_issue_assignee "Permanent link")

```
update_issue_assignee(issue_key, assignee_full_name)

```

Update the assignee of the Jira issue using the assignee's full name.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `issue_key`  |  The key of the Jira issue to update.  |  _required_  |  
|  `assignee_full_name`  |  The full name of the user to assign the issue to.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  Dict[str, Any]: A dictionary indicating success or failure of the operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-jira-issue/llama_index/tools/jira_issue/base.py`  
| 
```
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
```
 | 
```
defupdate_issue_assignee(self, issue_key, assignee_full_name):
"""
    Update the assignee of the Jira issue using the assignee's full name.

    Args:
        issue_key (str): The key of the Jira issue to update.
        assignee_full_name (str): The full name of the user to assign the issue to.

    Returns:
        Dict[str, Any]: A dictionary indicating success or failure of the operation.

    """
    try:
        # Search for users by display name
        users = self.jira.search_users(query=assignee_full_name)

        # Find exact match for the full name
        target_user = None
        for user in users:
            if user.displayName.lower() == assignee_full_name.lower():
                target_user = user
                break

        if not target_user:
            return {
                "error": True,
                "message": f"User with full name '{assignee_full_name}' not found",
            }

        # Get the issue
        issue = self.jira.issue(issue_key)
        issue.update(assignee={"accountId": target_user.accountId})

        return {
            "error": False,
            "message": f"Issue {issue_key} successfully assigned to {assignee_full_name}",
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"An error occurred while updating the assignee: {e!s}",
        }

```
 |  
| --- | --- |  
###  update_issue_status [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira_issue/#llama_index.tools.jira_issue.JiraIssueToolSpec.update_issue_status "Permanent link")

```
update_issue_status(
    issue_key: ,
    new_status: Literal["To Do", "In Progress", "Done"],
) -> [, ]

```

Update the status of a JIRA issue.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `issue_key`  |  The key of the JIRA issue to update.  |  _required_  |  
|  `new_status`  |  The new status to set for the issue.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: A dictionary indicating success or failure of the operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-jira-issue/llama_index/tools/jira_issue/base.py`  
| 
```
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
```
 | 
```
defupdate_issue_status(
    self, issue_key: str, new_status: Literal["To Do", "In Progress", "Done"]
) -> Dict[str, Any]:
"""
    Update the status of a JIRA issue.

    Args:
        issue_key (str): The key of the JIRA issue to update.
        new_status (str): The new status to set for the issue.

    Returns:
        Dict[str, Any]: A dictionary indicating success or failure of the operation.

    """
    try:
        issue = self.jira.issue(issue_key)
        transitions = self.jira.transitions(issue)
        transition_id = next(
            (t["id"] for t in transitions if t["name"] == new_status), None
        )

        if transition_id:
            self.jira.transition_issue(issue, transition_id)
            return {
                "error": False,
                "message": f"Issue {issue_key} status updated to {new_status}.",
            }
        else:
            available_statuses = [t["name"] for t in transitions]
            return {
                "error": True,
                "message": f"Status '{new_status}' not available for issue {issue_key}. Available transitions: {available_statuses}",
            }
    except Exception as e:
        return {
            "error": True,
            "message": f"Failed to update status for issue {issue_key}: {e!s}",
        }

```
 |  
| --- | --- |  
###  update_issue_due_date [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira_issue/#llama_index.tools.jira_issue.JiraIssueToolSpec.update_issue_due_date "Permanent link")

```
update_issue_due_date(
    issue_key: , due_date: Optional[] = None
) -> [, ]

```

Update the due date of a JIRA issue.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `issue_key`  |  The key of the JIRA issue to update.  |  _required_  |  
|  `due_date`  |  `Optional[str]`  |  The new due date in 'YYYY-MM-DD' format.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: A dictionary indicating success or failure of the operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-jira-issue/llama_index/tools/jira_issue/base.py`  
| 
```
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
```
 | 
```
defupdate_issue_due_date(
    self, issue_key: str, due_date: Optional[str] = None
) -> Dict[str, Any]:
"""
    Update the due date of a JIRA issue.

    Args:
        issue_key (str): The key of the JIRA issue to update.
        due_date (Optional[str]): The new due date in 'YYYY-MM-DD' format.

    Returns:
        Dict[str, Any]: A dictionary indicating success or failure of the operation.

    """
    if due_date:
        try:
            fromdatetimeimport datetime

            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return {
                "error": True,
                "message": "Invalid date format. Use YYYY-MM-DD.",
            }
    try:
        issue = self.jira.issue(issue_key)
        issue.update(duedate=due_date)
        return {
            "error": False,
            "message": f"Issue {issue_key} due date {'updated'ifdue_dateelse'cleared'}.",
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"Failed to update due date for issue {issue_key}: {e!s}",
        }

```
 |  
| --- | --- |  
###  delete_issue [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/jira_issue/#llama_index.tools.jira_issue.JiraIssueToolSpec.delete_issue "Permanent link")

```
delete_issue(issue_key: ) -> [, ]

```

Delete a JIRA issue.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `issue_key`  |  The key of the JIRA issue to delete.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  Dict[str, Any]: A dictionary indicating success or failure of the operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-jira-issue/llama_index/tools/jira_issue/base.py`  
| 
```
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
```
 | 
```
defdelete_issue(self, issue_key: str) -> Dict[str, Any]:
"""
    Delete a JIRA issue.

    Args:
        issue_key (str): The key of the JIRA issue to delete.

    Returns:
        Dict[str, Any]: A dictionary indicating success or failure of the operation.

    """
    try:
        issue = self.jira.issue(issue_key)
        issue.delete()
        return {
            "error": False,
            "message": f"Issue {issue_key} deleted successfully.",
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"Failed to delete issue {issue_key}: {e!s}",
        }

```
 |  
| --- | --- |  
options: members: - JiraToolSpec
