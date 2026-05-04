# Linear
##  LinearReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/linear/#llama_index.readers.linear.LinearReader "Permanent link")
Bases: 
Linear reader. Reads data from Linear issues for the passed query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  Personal API token.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-linear/llama_index/readers/linear/base.py`  
| 
```
 8
 9
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
```
 | 
```
classLinearReader(BaseReader):
"""
    Linear reader. Reads data from Linear issues for the passed query.

    Args:
        api_key (str): Personal API token.

    """

    def__init__(self, api_key: str) -> None:
        self.api_key = api_key

    defload_data(self, query: str) -> List[Document]:
        # Define the GraphQL query
        graphql_endpoint = "https://api.linear.app/graphql"
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {"query": query}

        # Make the GraphQL request
        response = requests.post(graphql_endpoint, json=payload, headers=headers)
        data = response.json()

        # Extract relevant information
        issues = []
        team_data = data.get("data", {}).get("team", {})
        for issue in team_data.get("issues", {}).get("nodes", []):
            assignee = issue.get("assignee", {}).get("name", "")
            labels = [
                label_node["name"]
                for label_node in issue.get("labels", {}).get("nodes", [])
            ]
            project = issue.get("project", {}).get("name", "")
            state = issue.get("state", {}).get("name", "")
            creator = issue.get("creator", {}).get("name", "")

            issues.append(
                Document(
                    text=f"{issue['title']}\n{issue['description']}",
                    extra_info={
                        "id": issue["id"],
                        "title": issue["title"],
                        "created_at": issue["createdAt"],
                        "archived_at": issue["archivedAt"],
                        "auto_archived_at": issue["autoArchivedAt"],
                        "auto_closed_at": issue["autoClosedAt"],
                        "branch_name": issue["branchName"],
                        "canceled_at": issue["canceledAt"],
                        "completed_at": issue["completedAt"],
                        "creator": creator,
                        "due_date": issue["dueDate"],
                        "estimate": issue["estimate"],
                        "labels": labels,
                        "project": project,
                        "state": state,
                        "updated_at": issue["updatedAt"],
                        "assignee": assignee,
                    },
                )
            )

        return issues

```
 |  
| --- | --- |  
options: members: - LinearReader
