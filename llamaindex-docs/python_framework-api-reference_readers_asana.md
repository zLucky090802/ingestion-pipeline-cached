# Asana
##  AsanaReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/asana/#llama_index.readers.asana.AsanaReader "Permanent link")
Bases: 
Asana reader. Reads data from an Asana workspace.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `asana_token`  |  Asana token.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-asana/llama_index/readers/asana/base.py`  
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
```
 | 
```
classAsanaReader(BaseReader):
"""
    Asana reader. Reads data from an Asana workspace.

    Args:
        asana_token (str): Asana token.

    """

    def__init__(self, asana_token: str) -> None:
"""Initialize Asana reader."""
        self.client = asana.Client.access_token(asana_token)

    defload_data(
        self, workspace_id: Optional[str] = None, project_id: Optional[str] = None
    ) -> List[Document]:
"""
        Load data from the workspace.

        Args:
            workspace_id (Optional[str], optional): Workspace ID. Defaults to None.
            project_id (Optional[str], optional): Project ID. Defaults to None.


        Returns:
            List[Document]: List of documents.

        """
        if workspace_id is None and project_id is None:
            raise ValueError("Either workspace_id or project_id must be provided")

        if workspace_id is not None and project_id is not None:
            raise ValueError(
                "Only one of workspace_id or project_id should be provided"
            )

        results = []

        if workspace_id is not None:
            workspace_name = self.client.workspaces.find_by_id(workspace_id)["name"]
            projects = self.client.projects.find_all({"workspace": workspace_id})

        # Case: Only project_id is provided
        else:  # since we've handled the other cases, this means project_id is not None
            projects = [self.client.projects.find_by_id(project_id)]
            workspace_name = projects[0]["workspace"]["name"]

        for project in projects:
            tasks = self.client.tasks.find_all(
                {
                    "project": project["gid"],
                    "opt_fields": "name,notes,completed,completed_at,completed_by,assignee,followers,custom_fields",
                }
            )
            for task in tasks:
                stories = self.client.tasks.stories(task["gid"], opt_fields="type,text")
                comments = "\n".join(
                    [
                        story["text"]
                        for story in stories
                        if story.get("type") == "comment" and "text" in story
                    ]
                )

                task_metadata = {
                    "task_id": task.get("gid", ""),
                    "name": task.get("name", ""),
                    "assignee": (task.get("assignee") or {}).get("name", ""),
                    "completed_on": task.get("completed_at", ""),
                    "completed_by": (task.get("completed_by") or {}).get("name", ""),
                    "project_name": project.get("name", ""),
                    "custom_fields": [
                        i["display_value"]
                        for i in task.get("custom_fields")
                        if task.get("custom_fields") is not None
                    ],
                    "workspace_name": workspace_name,
                    "url": f"https://app.asana.com/0/{project['gid']}/{task['gid']}",
                }

                if task.get("followers") is not None:
                    task_metadata["followers"] = [
                        i.get("name") for i in task.get("followers") if "name" in i
                    ]
                else:
                    task_metadata["followers"] = []

                results.append(
                    Document(
                        text=task.get("name", "")
                        + " "
                        + task.get("notes", "")
                        + " "
                        + comments,
                        extra_info=task_metadata,
                    )
                )

        return results

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/asana/#llama_index.readers.asana.AsanaReader.load_data "Permanent link")

```
load_data(
    workspace_id: Optional[] = None,
    project_id: Optional[] = None,
) -> []

```

Load data from the workspace.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `workspace_id`  |  `Optional[str]`  |  Workspace ID. Defaults to None.  |  `None`  |  
|  `project_id`  |  `Optional[str]`  |  Project ID. Defaults to None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-asana/llama_index/readers/asana/base.py`  
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
```
 | 
```
defload_data(
    self, workspace_id: Optional[str] = None, project_id: Optional[str] = None
) -> List[Document]:
"""
    Load data from the workspace.

    Args:
        workspace_id (Optional[str], optional): Workspace ID. Defaults to None.
        project_id (Optional[str], optional): Project ID. Defaults to None.


    Returns:
        List[Document]: List of documents.

    """
    if workspace_id is None and project_id is None:
        raise ValueError("Either workspace_id or project_id must be provided")

    if workspace_id is not None and project_id is not None:
        raise ValueError(
            "Only one of workspace_id or project_id should be provided"
        )

    results = []

    if workspace_id is not None:
        workspace_name = self.client.workspaces.find_by_id(workspace_id)["name"]
        projects = self.client.projects.find_all({"workspace": workspace_id})

    # Case: Only project_id is provided
    else:  # since we've handled the other cases, this means project_id is not None
        projects = [self.client.projects.find_by_id(project_id)]
        workspace_name = projects[0]["workspace"]["name"]

    for project in projects:
        tasks = self.client.tasks.find_all(
            {
                "project": project["gid"],
                "opt_fields": "name,notes,completed,completed_at,completed_by,assignee,followers,custom_fields",
            }
        )
        for task in tasks:
            stories = self.client.tasks.stories(task["gid"], opt_fields="type,text")
            comments = "\n".join(
                [
                    story["text"]
                    for story in stories
                    if story.get("type") == "comment" and "text" in story
                ]
            )

            task_metadata = {
                "task_id": task.get("gid", ""),
                "name": task.get("name", ""),
                "assignee": (task.get("assignee") or {}).get("name", ""),
                "completed_on": task.get("completed_at", ""),
                "completed_by": (task.get("completed_by") or {}).get("name", ""),
                "project_name": project.get("name", ""),
                "custom_fields": [
                    i["display_value"]
                    for i in task.get("custom_fields")
                    if task.get("custom_fields") is not None
                ],
                "workspace_name": workspace_name,
                "url": f"https://app.asana.com/0/{project['gid']}/{task['gid']}",
            }

            if task.get("followers") is not None:
                task_metadata["followers"] = [
                    i.get("name") for i in task.get("followers") if "name" in i
                ]
            else:
                task_metadata["followers"] = []

            results.append(
                Document(
                    text=task.get("name", "")
                    + " "
                    + task.get("notes", "")
                    + " "
                    + comments,
                    extra_info=task_metadata,
                )
            )

    return results

```
 |  
| --- | --- |  
options: members: - AsanaReader
