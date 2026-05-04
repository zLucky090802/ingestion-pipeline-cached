# Gpt repo
Init file.
##  GPTRepoReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gpt_repo/#llama_index.readers.gpt_repo.GPTRepoReader "Permanent link")
Bases: 
GPTRepoReader.
Reads a github repo in a prompt-friendly format.
Source code in `llama-index-integrations/readers/llama-index-readers-gpt-repo/llama_index/readers/gpt_repo/base.py`  
| 
```
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
```
 | 
```
classGPTRepoReader(BaseReader):
"""
    GPTRepoReader.

    Reads a github repo in a prompt-friendly format.

    """

    def__init__(self, concatenate: bool = False) -> None:
"""Initialize."""
        self.concatenate = concatenate

    defload_data(
        self,
        repo_path: str,
        preamble_str: Optional[str] = None,
        extensions: Optional[List[str]] = None,
        encoding: Optional[str] = "utf-8",
    ) -> List[Document]:
"""
        Load data from the input directory.

        Args:
            pages (List[str]): List of pages to read.

        """
        ignore_file_path = os.path.join(repo_path, ".gptignore")

        if os.path.exists(ignore_file_path):
            ignore_list = get_ignore_list(ignore_file_path)
        else:
            ignore_list = []

        output_text = ""
        if preamble_str:
            output_text += f"{preamble_str}\n"
        elif self.concatenate:
            output_text += (
                "The following text is a Git repository with code. "
                "The structure of the text are sections that begin with ----, "
                "followed by a single line containing the file path and file "
                "name, followed by a variable amount of lines containing the "
                "file contents. The text representing the Git repository ends "
                "when the symbols --END-- are encountered. Any further text beyond "
                "--END-- are meant to be interpreted as instructions using the "
                "aforementioned Git repository as context.\n"
            )
        else:
            # self.concatenate is False
            output_text += (
                "The following text is a file in a Git repository. "
                "The structure of the text are sections that begin with ----, "
                "followed by a single line containing the file path and file "
                "name, followed by a variable amount of lines containing the "
                "file contents. The text representing the file ends "
                "when the symbols --END-- are encountered. Any further text beyond "
                "--END-- are meant to be interpreted as instructions using the "
                "aforementioned file as context.\n"
            )
        text_list = process_repository(
            repo_path,
            ignore_list,
            concatenate=self.concatenate,
            extensions=extensions,
            encoding=encoding,
        )
        docs = []
        for text in text_list:
            doc_text = output_text + text + "\n--END--\n"
            docs.append(Document(text=doc_text))

        return docs

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gpt_repo/#llama_index.readers.gpt_repo.GPTRepoReader.load_data "Permanent link")

```
load_data(
    repo_path: ,
    preamble_str: Optional[] = None,
    extensions: Optional[[]] = None,
    encoding: Optional[] = "utf-8",
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `pages`  |  `List[str]`  |  List of pages to read.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gpt-repo/llama_index/readers/gpt_repo/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    repo_path: str,
    preamble_str: Optional[str] = None,
    extensions: Optional[List[str]] = None,
    encoding: Optional[str] = "utf-8",
) -> List[Document]:
"""
    Load data from the input directory.

    Args:
        pages (List[str]): List of pages to read.

    """
    ignore_file_path = os.path.join(repo_path, ".gptignore")

    if os.path.exists(ignore_file_path):
        ignore_list = get_ignore_list(ignore_file_path)
    else:
        ignore_list = []

    output_text = ""
    if preamble_str:
        output_text += f"{preamble_str}\n"
    elif self.concatenate:
        output_text += (
            "The following text is a Git repository with code. "
            "The structure of the text are sections that begin with ----, "
            "followed by a single line containing the file path and file "
            "name, followed by a variable amount of lines containing the "
            "file contents. The text representing the Git repository ends "
            "when the symbols --END-- are encountered. Any further text beyond "
            "--END-- are meant to be interpreted as instructions using the "
            "aforementioned Git repository as context.\n"
        )
    else:
        # self.concatenate is False
        output_text += (
            "The following text is a file in a Git repository. "
            "The structure of the text are sections that begin with ----, "
            "followed by a single line containing the file path and file "
            "name, followed by a variable amount of lines containing the "
            "file contents. The text representing the file ends "
            "when the symbols --END-- are encountered. Any further text beyond "
            "--END-- are meant to be interpreted as instructions using the "
            "aforementioned file as context.\n"
        )
    text_list = process_repository(
        repo_path,
        ignore_list,
        concatenate=self.concatenate,
        extensions=extensions,
        encoding=encoding,
    )
    docs = []
    for text in text_list:
        doc_text = output_text + text + "\n--END--\n"
        docs.append(Document(text=doc_text))

    return docs

```
 |  
| --- | --- |  
##  process_repository [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gpt_repo/#llama_index.readers.gpt_repo.process_repository "Permanent link")

```
process_repository(
    repo_path,
    ignore_list,
    concatenate:  = False,
    extensions: Optional[[]] = None,
    encoding: Optional[] = "utf-8",
) -> []

```

Process repository.
Source code in `llama-index-integrations/readers/llama-index-readers-gpt-repo/llama_index/readers/gpt_repo/base.py`  
| 
```
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
```
 | 
```
defprocess_repository(
    repo_path,
    ignore_list,
    concatenate: bool = False,
    extensions: Optional[List[str]] = None,
    encoding: Optional[str] = "utf-8",
) -> List[str]:
"""Process repository."""
    result_texts = []
    result_text = ""
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, repo_path)

            _, file_ext = os.path.splitext(file_path)
            is_correct_extension = extensions is None or file_ext in extensions

            if (
                not should_ignore(relative_file_path, ignore_list)
                and is_correct_extension
            ):
                with open(file_path, errors="ignore", encoding=encoding) as file:
                    contents = file.read()
                result_text += "-" * 4 + "\n"
                result_text += f"{relative_file_path}\n"
                result_text += f"{contents}\n"
                if not concatenate:
                    result_texts.append(result_text)
                    result_text = ""

    if concatenate:
        result_texts.append(result_text)

    return result_texts

```
 |  
| --- | --- |  
options: members: - GPTRepoReader
