# Jira
##  JiraReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/jira/#llama_index.readers.jira.JiraReader "Permanent link")
Bases: 
Jira reader. Reads data from Jira issues from passed query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `Optional basic_auth`  |  { "email": "email", "api_token": "token", "server_url": "server_url"  |  _required_  |  
|  `Optional oauth`  |  { "cloud_id": "cloud_id", "api_token": "token"  |  _required_  |  
|  `Optional patauth`  |  { "server_url": "server_url", "api_token": "token"  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-jira/llama_index/readers/jira/base.py`  
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
```
 | 
```
classJiraReader(BaseReader):
"""
    Jira reader. Reads data from Jira issues from passed query.

    Args:
        Optional basic_auth:{
            "email": "email",
            "api_token": "token",
            "server_url": "server_url"

        Optional oauth:{
            "cloud_id": "cloud_id",
            "api_token": "token"

        Optional patauth:{
            "server_url": "server_url",
            "api_token": "token"


    """

    include_epics: bool = True

    def__init__(
        self,
        email: Optional[str] = None,
        api_token: Optional[str] = None,
        server_url: Optional[str] = None,
        BasicAuth: Optional[BasicAuth] = None,
        Oauth2: Optional[Oauth2] = None,
        PATauth: Optional[PATauth] = None,
        include_epics: bool = True,
    ) -> None:
        fromjiraimport JIRA

        if email and api_token and server_url:
            if BasicAuth is None:
                BasicAuth = {}
            BasicAuth["email"] = email
            BasicAuth["api_token"] = api_token
            BasicAuth["server_url"] = server_url

        if Oauth2:
            options = {
                "server": f"https://api.atlassian.com/ex/jira/{Oauth2['cloud_id']}",
                "headers": {"Authorization": f"Bearer {Oauth2['api_token']}"},
            }
            self.jira = JIRA(options=options)
        elif PATauth:
            options = {
                "server": PATauth["server_url"],
                "headers": {"Authorization": f"Bearer {PATauth['api_token']}"},
            }
            self.jira = JIRA(options=options)
        else:
            self.jira = JIRA(
                basic_auth=(BasicAuth["email"], BasicAuth["api_token"]),
                server=f"https://{BasicAuth['server_url']}",
            )

        self.include_epics = include_epics

    defload_data(
        self, query: str, start_at: int = 0, max_results: int = 50
    ) -> List[Document]:
        relevant_issues = self.jira.search_issues(
            query, startAt=start_at, maxResults=max_results
        )

        issues = []

        assignee = ""
        reporter = ""
        epic_key = ""
        epic_summary = ""
        epic_descripton = ""

        for issue in relevant_issues:
            issue_type = issue.fields.issuetype.name
            if issue_type == "Epic" and not self.include_epics:
                continue

            assignee = ""
            reporter = ""
            epic_key = ""
            epic_summary = ""
            epic_descripton = ""

            if issue.fields.assignee:
                assignee = issue.fields.assignee.displayName
            if issue.fields.reporter:
                reporter = issue.fields.reporter.displayName

            if "parent" in issue.raw["fields"]:
                if issue.raw["fields"]["parent"]["key"]:
                    epic_key = issue.raw["fields"]["parent"]["key"]

                if issue.raw["fields"]["parent"]["fields"]["summary"]:
                    epic_summary = issue.raw["fields"]["parent"]["fields"]["summary"]

                if issue.raw["fields"]["parent"]["fields"]["status"]["description"]:
                    epic_descripton = issue.raw["fields"]["parent"]["fields"]["status"][
                        "description"
                    ]

            extra_info = {
                "id": safe_get(issue, "id"),
                "title": safe_get(issue, "fields", "summary"),
                "url": safe_get(issue, "permalink"),
                "created_at": safe_get(issue, "fields", "created"),
                "updated_at": safe_get(issue, "fields", "updated"),
                "labels": safe_get(issue, "fields", "labels"),
                "status": safe_get(issue, "fields", "status", "name"),
                "assignee": assignee,
                "reporter": reporter,
                "project": safe_get(issue, "fields", "project", "name"),
                "issue_type": issue_type,
                "priority": safe_get(issue, "fields", "priority", "name"),
                "epic_key": epic_key,
                "epic_summary": epic_summary,
                "epic_description": epic_descripton,
            }

            issues.append(
                Document(
                    text=f"{issue.fields.summary}\n{issue.fields.description}",
                    doc_id=issue.id,
                    extra_info=extra_info,
                )
            )

        return issues

```
 |  
| --- | --- |  
options: members: - JiraReader
