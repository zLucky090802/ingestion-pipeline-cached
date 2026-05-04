# Bitbucket
##  BitbucketReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/bitbucket/#llama_index.readers.bitbucket.BitbucketReader "Permanent link")
Bases: 
Bitbucket reader.
Reads the content of files in Bitbucket repositories.
Source code in `llama-index-integrations/readers/llama-index-readers-bitbucket/llama_index/readers/bitbucket/base.py`  
| 
```
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
```
 | 
```
classBitbucketReader(BaseReader):
"""
    Bitbucket reader.

    Reads the content of files in Bitbucket repositories.

    """

    def__init__(
        self,
        base_url: Optional[str] = None,
        project_key: Optional[str] = None,
        branch: Optional[str] = "refs/heads/develop",
        repository: Optional[str] = None,
        extensions_to_skip: Optional[List] = [],
    ) -> None:
"""Initialize with parameters."""
        if os.getenv("BITBUCKET_USERNAME") is None:
            raise ValueError("Could not find a Bitbucket username.")
        if os.getenv("BITBUCKET_API_KEY") is None:
            raise ValueError("Could not find a Bitbucket api key.")
        if base_url is None:
            raise ValueError("You must provide a base url for Bitbucket.")
        if project_key is None:
            raise ValueError("You must provide a project key for Bitbucket repository.")
        self.base_url = base_url
        self.project_key = project_key
        self.branch = branch
        self.extensions_to_skip = extensions_to_skip
        self.repository = repository

    defget_headers(self):
        username = os.getenv("BITBUCKET_USERNAME")
        api_token = os.getenv("BITBUCKET_API_KEY")
        auth = base64.b64encode(f"{username}:{api_token}".encode()).decode()
        return {"Authorization": f"Basic {auth}"}

    defget_slugs(self) -> List:
"""
        Get slugs of the specific project.
        """
        slugs = []
        if self.repository is None:
            repos_url = (
                f"{self.base_url}/rest/api/latest/projects/{self.project_key}/repos/"
            )
            headers = self.get_headers()

            response = requests.get(repos_url, headers=headers)

            if response.status_code == 200:
                repositories = response.json()["values"]
                for repo in repositories:
                    repo_slug = repo["slug"]
                    slugs.append(repo_slug)
        slugs.append(self.repository)
        return slugs

    defload_all_file_paths(self, slug, branch, directory_path="", paths=None):
"""
        Go inside every file that is present in the repository and get the paths for each file.
        """
        if paths is None:
            paths = []
        content_url = f"{self.base_url}/rest/api/latest/projects/{self.project_key}/repos/{slug}/browse/{directory_path}"

        query_params = {
            "at": branch,
        }
        headers = self.get_headers()
        response = requests.get(content_url, headers=headers, params=query_params)
        response = response.json()
        if "errors" in response:
            raise ValueError(response["errors"])
        children = response["children"]
        for value in children["values"]:
            if value["type"] == "FILE":
                if value["path"]["extension"] not in self.extensions_to_skip:
                    paths.append(
                        {
                            "slug": slug,
                            "path": f"{directory_path}/{value['path']['toString']}",
                        }
                    )
            elif value["type"] == "DIRECTORY":
                self.load_all_file_paths(
                    slug=slug,
                    branch=branch,
                    directory_path=f"{directory_path}/{value['path']['toString']}",
                    paths=paths,
                )

    defload_text_by_paths(self, slug, file_path, branch) -> List:
"""
        Go inside every file that is present in the repository and get the paths for each file.
        """
        content_url = f"{self.base_url}/rest/api/latest/projects/{self.project_key}/repos/{slug}/browse{file_path}"

        query_params = {
            "at": branch,
        }
        headers = self.get_headers()
        response = requests.get(content_url, headers=headers, params=query_params)
        children = response.json()
        if "errors" in children:
            raise ValueError(children["errors"])
        if "lines" in children:
            return children["lines"]
        return []

    defload_text(self, paths) -> List:
        text_dict = []
        for path in paths:
            lines_list = self.load_text_by_paths(
                slug=path["slug"], file_path=path["path"], branch=self.branch
            )
            concatenated_string = ""

            for line_dict in lines_list:
                text = line_dict.get("text", "")
                concatenated_string = concatenated_string + " " + text

            text_dict.append(concatenated_string)
        return text_dict

    defload_data(self) -> List[Document]:
"""Return a list of Document made of each file in Bitbucket."""
        slugs = self.get_slugs()
        paths = []
        for slug in slugs:
            self.load_all_file_paths(
                slug=slug, branch=self.branch, directory_path="", paths=paths
            )
        texts = self.load_text(paths)
        return [Document(text=text) for text in texts]

```
 |  
| --- | --- |  
###  get_slugs [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/bitbucket/#llama_index.readers.bitbucket.BitbucketReader.get_slugs "Permanent link")

```
get_slugs() -> 

```

Get slugs of the specific project.
Source code in `llama-index-integrations/readers/llama-index-readers-bitbucket/llama_index/readers/bitbucket/base.py`  
| 
```
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
```
 | 
```
defget_slugs(self) -> List:
"""
    Get slugs of the specific project.
    """
    slugs = []
    if self.repository is None:
        repos_url = (
            f"{self.base_url}/rest/api/latest/projects/{self.project_key}/repos/"
        )
        headers = self.get_headers()

        response = requests.get(repos_url, headers=headers)

        if response.status_code == 200:
            repositories = response.json()["values"]
            for repo in repositories:
                repo_slug = repo["slug"]
                slugs.append(repo_slug)
    slugs.append(self.repository)
    return slugs

```
 |  
| --- | --- |  
###  load_all_file_paths [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/bitbucket/#llama_index.readers.bitbucket.BitbucketReader.load_all_file_paths "Permanent link")

```
load_all_file_paths(
    slug, branch, directory_path="", paths=None
)

```

Go inside every file that is present in the repository and get the paths for each file.
Source code in `llama-index-integrations/readers/llama-index-readers-bitbucket/llama_index/readers/bitbucket/base.py`  
| 
```
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
```
 | 
```
defload_all_file_paths(self, slug, branch, directory_path="", paths=None):
"""
    Go inside every file that is present in the repository and get the paths for each file.
    """
    if paths is None:
        paths = []
    content_url = f"{self.base_url}/rest/api/latest/projects/{self.project_key}/repos/{slug}/browse/{directory_path}"

    query_params = {
        "at": branch,
    }
    headers = self.get_headers()
    response = requests.get(content_url, headers=headers, params=query_params)
    response = response.json()
    if "errors" in response:
        raise ValueError(response["errors"])
    children = response["children"]
    for value in children["values"]:
        if value["type"] == "FILE":
            if value["path"]["extension"] not in self.extensions_to_skip:
                paths.append(
                    {
                        "slug": slug,
                        "path": f"{directory_path}/{value['path']['toString']}",
                    }
                )
        elif value["type"] == "DIRECTORY":
            self.load_all_file_paths(
                slug=slug,
                branch=branch,
                directory_path=f"{directory_path}/{value['path']['toString']}",
                paths=paths,
            )

```
 |  
| --- | --- |  
###  load_text_by_paths [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/bitbucket/#llama_index.readers.bitbucket.BitbucketReader.load_text_by_paths "Permanent link")

```
load_text_by_paths(slug, file_path, branch) -> 

```

Go inside every file that is present in the repository and get the paths for each file.
Source code in `llama-index-integrations/readers/llama-index-readers-bitbucket/llama_index/readers/bitbucket/base.py`  
| 
```
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
```
 | 
```
defload_text_by_paths(self, slug, file_path, branch) -> List:
"""
    Go inside every file that is present in the repository and get the paths for each file.
    """
    content_url = f"{self.base_url}/rest/api/latest/projects/{self.project_key}/repos/{slug}/browse{file_path}"

    query_params = {
        "at": branch,
    }
    headers = self.get_headers()
    response = requests.get(content_url, headers=headers, params=query_params)
    children = response.json()
    if "errors" in children:
        raise ValueError(children["errors"])
    if "lines" in children:
        return children["lines"]
    return []

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/bitbucket/#llama_index.readers.bitbucket.BitbucketReader.load_data "Permanent link")

```
load_data() -> []

```

Return a list of Document made of each file in Bitbucket.
Source code in `llama-index-integrations/readers/llama-index-readers-bitbucket/llama_index/readers/bitbucket/base.py`  
| 
```
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
```
 | 
```
defload_data(self) -> List[Document]:
"""Return a list of Document made of each file in Bitbucket."""
    slugs = self.get_slugs()
    paths = []
    for slug in slugs:
        self.load_all_file_paths(
            slug=slug, branch=self.branch, directory_path="", paths=paths
        )
    texts = self.load_text(paths)
    return [Document(text=text) for text in texts]

```
 |  
| --- | --- |  
options: members: - BitbucketReader
