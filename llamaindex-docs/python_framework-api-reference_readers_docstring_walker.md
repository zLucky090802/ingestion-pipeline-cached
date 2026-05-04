# Docstring walker
Init file.
##  DocstringWalker [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker "Permanent link")
Bases: 
A loader for docstring extraction and building structured documents from them. Recursively walks a directory and extracts docstrings from each Python module - starting from the module itself, then classes, then functions. Builds a graph of dependencies between the extracted docstrings.
Source code in `llama-index-integrations/readers/llama-index-readers-docstring-walker/llama_index/readers/docstring_walker/base.py`  
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
```
 | 
```
classDocstringWalker(BaseReader):
"""
    A loader for docstring extraction and building structured documents from them.
    Recursively walks a directory and extracts docstrings from each Python
    module - starting from the module itself, then classes, then functions.
    Builds a graph of dependencies between the extracted docstrings.
    """

    defload_data(
        self,
        code_dir: str,
        skip_initpy: bool = True,
        fail_on_malformed_files: bool = False,
    ) -> List[Document]:
"""
        Load data from the specified code directory.
        Additionally, after loading the data, build a dependency graph between the loaded documents.
        The graph is stored as an attribute of the class.


        Parameters
        ----------
        code_dir : str
            The directory path to the code files.
        skip_initpy : bool
            Whether to skip the __init__.py files. Defaults to True.
        fail_on_malformed_files : bool
            Whether to fail on malformed files. Defaults to False - in this case,
            the malformed files are skipped and a warning is logged.

        Returns
        -------
        List[Document]
            A list of loaded documents.

        """
        return self.process_directory(code_dir, skip_initpy, fail_on_malformed_files)

    defprocess_directory(
        self,
        code_dir: str,
        skip_initpy: bool = True,
        fail_on_malformed_files: bool = False,
    ) -> List[Document]:
"""
        Process a directory and extract information from Python files.

        Parameters
        ----------
        code_dir : str
            The directory path to the code files.
        skip_initpy : bool
            Whether to skip the __init__.py files. Defaults to True.
        fail_on_malformed_files : bool
            Whether to fail on malformed files. Defaults to False - in this case,
            the malformed files are skipped and a warning is logged.

        Returns
        -------
        List[Document]
            A list of Document objects.

        """
        llama_docs = []
        for root, _, files in os.walk(code_dir):
            for file in files:
                if file.endswith(".py"):
                    if skip_initpy and file == "__init__.py":
                        continue
                    module_name = file.replace(".py", "")
                    module_path = os.path.join(root, file)
                    try:
                        doc = self.parse_module(module_name, module_path)
                        llama_docs.append(doc)
                    except Exception as e:
                        if fail_on_malformed_files:
                            raise e  # noqa: TRY201
                        log.warning(
                            "Failed to parse file %s. Skipping. Error: %s",
                            module_path,
                            e,
                        )
                        continue
        return llama_docs

    defread_module_text(self, path: str) -> str:
"""
        Read the text of a Python module. For tests this function can be mocked.

        Parameters
        ----------
        path : str
            Path to the module.

        Returns
        -------
        str
            The text of the module.

        """
        with open(path, encoding="utf-8") as f:
            return f.read()

    defparse_module(self, module_name: str, path: str) -> Document:
"""
        Function for parsing a single Python module.

        Parameters
        ----------
        module_name : str
            A module name.
        path : str
            Path to the module.

        Returns
        -------
        Document
            A LLama Index Document object with extracted information from the module.

        """
        module_text = self.read_module_text(path)
        module = ast.parse(module_text)
        module_docstring = ast.get_docstring(module)
        module_text = f"Module name: {module_name}\n Docstring: {module_docstring}\n"
        sub_texts = []
        for elem in module.body:
            if type(elem) in TYPES_TO_PROCESS:
                sub_text = self.process_elem(elem, module_name)
                sub_texts.append(sub_text)
        module_text += "\n".join(sub_texts)
        return Document(text=module_text)

    defprocess_class(self, class_node: ast.ClassDef, parent_node: str):
"""
        Process a class node in the AST and add relevant information to the graph.

        Parameters
        ----------
        class_node : ast.ClassDef
            The class node to process. It represents a class definition
            in the abstract syntax tree (AST).
        parent_node : str
            The name of the parent node. It specifies the name of the parent node in the graph.

        Returns
        -------
        str
            A string representation of the processed class node and its sub-elements.
            It provides a textual representation of the processed class node and its sub-elements.

        """
        cls_name = class_node.name
        cls_docstring = ast.get_docstring(class_node)

        text = f"\n Class name: {cls_name}, In: {parent_node}\n Docstring: {cls_docstring}"
        sub_texts = []
        for elem in class_node.body:
            sub_text = self.process_elem(elem, cls_name)
            sub_texts.append(sub_text)
        return text + "\n".join(sub_texts)

    defprocess_function(self, func_node: ast.FunctionDef, parent_node: str) -> str:
"""
        Process a function node in the AST and add it to the graph. Build node text.

        Parameters
        ----------
        func_node : ast.FunctionDef
            The function node to process.
        parent_node : str
            The name of the parent node.

        Returns
        -------
        str
            A string representation of the processed function node with its sub-elements.

        """
        func_name = func_node.name
        func_docstring = ast.get_docstring(func_node)

        text = f"\n Function name: {func_name}, In: {parent_node}\n Docstring: {func_docstring}"
        sub_texts = []
        for elem in func_node.body:
            sub_text = self.process_elem(elem, func_name)
            sub_texts.append(sub_text)
        return text + "\n".join(sub_texts)

    defprocess_elem(self, elem, parent_node: str) -> str:
"""
        Process an element in the abstract syntax tree (AST).

        This is a generic function that delegates the execution to more specific
        functions based on the type of the element.

        Args:
            elem (ast.AST): The element to process.
            parent_node (str): The parent node in the graph.
            graph (nx.Graph): The graph to update.

        Returns:
            str: The result of processing the element.

        """
        if isinstance(elem, ast.FunctionDef):
            return self.process_function(elem, parent_node)
        elif isinstance(elem, ast.ClassDef):
            return self.process_class(elem, parent_node)
        return ""

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.load_data "Permanent link")

```
load_data(
    code_dir: ,
    skip_initpy:  = True,
    fail_on_malformed_files:  = False,
) -> []

```

Load data from the specified code directory. Additionally, after loading the data, build a dependency graph between the loaded documents. The graph is stored as an attribute of the class.
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.load_data--parameters "Permanent link")
code_dir : str The directory path to the code files. skip_initpy : bool Whether to skip the **init**.py files. Defaults to True. fail_on_malformed_files : bool Whether to fail on malformed files. Defaults to False - in this case, the malformed files are skipped and a warning is logged.
##### Returns[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.load_data--returns "Permanent link")
List[Document] A list of loaded documents.
Source code in `llama-index-integrations/readers/llama-index-readers-docstring-walker/llama_index/readers/docstring_walker/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    code_dir: str,
    skip_initpy: bool = True,
    fail_on_malformed_files: bool = False,
) -> List[Document]:
"""
    Load data from the specified code directory.
    Additionally, after loading the data, build a dependency graph between the loaded documents.
    The graph is stored as an attribute of the class.


    Parameters
    ----------
    code_dir : str
        The directory path to the code files.
    skip_initpy : bool
        Whether to skip the __init__.py files. Defaults to True.
    fail_on_malformed_files : bool
        Whether to fail on malformed files. Defaults to False - in this case,
        the malformed files are skipped and a warning is logged.

    Returns
    -------
    List[Document]
        A list of loaded documents.

    """
    return self.process_directory(code_dir, skip_initpy, fail_on_malformed_files)

```
 |  
| --- | --- |  
###  process_directory [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.process_directory "Permanent link")

```
process_directory(
    code_dir: ,
    skip_initpy:  = True,
    fail_on_malformed_files:  = False,
) -> []

```

Process a directory and extract information from Python files.
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.process_directory--parameters "Permanent link")
code_dir : str The directory path to the code files. skip_initpy : bool Whether to skip the **init**.py files. Defaults to True. fail_on_malformed_files : bool Whether to fail on malformed files. Defaults to False - in this case, the malformed files are skipped and a warning is logged.
##### Returns[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.process_directory--returns "Permanent link")
List[Document] A list of Document objects.
Source code in `llama-index-integrations/readers/llama-index-readers-docstring-walker/llama_index/readers/docstring_walker/base.py`  
| 
```
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
```
 | 
```
defprocess_directory(
    self,
    code_dir: str,
    skip_initpy: bool = True,
    fail_on_malformed_files: bool = False,
) -> List[Document]:
"""
    Process a directory and extract information from Python files.

    Parameters
    ----------
    code_dir : str
        The directory path to the code files.
    skip_initpy : bool
        Whether to skip the __init__.py files. Defaults to True.
    fail_on_malformed_files : bool
        Whether to fail on malformed files. Defaults to False - in this case,
        the malformed files are skipped and a warning is logged.

    Returns
    -------
    List[Document]
        A list of Document objects.

    """
    llama_docs = []
    for root, _, files in os.walk(code_dir):
        for file in files:
            if file.endswith(".py"):
                if skip_initpy and file == "__init__.py":
                    continue
                module_name = file.replace(".py", "")
                module_path = os.path.join(root, file)
                try:
                    doc = self.parse_module(module_name, module_path)
                    llama_docs.append(doc)
                except Exception as e:
                    if fail_on_malformed_files:
                        raise e  # noqa: TRY201
                    log.warning(
                        "Failed to parse file %s. Skipping. Error: %s",
                        module_path,
                        e,
                    )
                    continue
    return llama_docs

```
 |  
| --- | --- |  
###  read_module_text [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.read_module_text "Permanent link")

```
read_module_text(path: ) -> 

```

Read the text of a Python module. For tests this function can be mocked.
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.read_module_text--parameters "Permanent link")
path : str Path to the module.
##### Returns[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.read_module_text--returns "Permanent link")
str The text of the module.
Source code in `llama-index-integrations/readers/llama-index-readers-docstring-walker/llama_index/readers/docstring_walker/base.py`  
| 
```
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
```
 | 
```
defread_module_text(self, path: str) -> str:
"""
    Read the text of a Python module. For tests this function can be mocked.

    Parameters
    ----------
    path : str
        Path to the module.

    Returns
    -------
    str
        The text of the module.

    """
    with open(path, encoding="utf-8") as f:
        return f.read()

```
 |  
| --- | --- |  
###  parse_module [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.parse_module "Permanent link")

```
parse_module(module_name: , path: ) -> 

```

Function for parsing a single Python module.
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.parse_module--parameters "Permanent link")
module_name : str A module name. path : str Path to the module.
##### Returns[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.parse_module--returns "Permanent link")
Document A LLama Index Document object with extracted information from the module.
Source code in `llama-index-integrations/readers/llama-index-readers-docstring-walker/llama_index/readers/docstring_walker/base.py`  
| 
```
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
defparse_module(self, module_name: str, path: str) -> Document:
"""
    Function for parsing a single Python module.

    Parameters
    ----------
    module_name : str
        A module name.
    path : str
        Path to the module.

    Returns
    -------
    Document
        A LLama Index Document object with extracted information from the module.

    """
    module_text = self.read_module_text(path)
    module = ast.parse(module_text)
    module_docstring = ast.get_docstring(module)
    module_text = f"Module name: {module_name}\n Docstring: {module_docstring}\n"
    sub_texts = []
    for elem in module.body:
        if type(elem) in TYPES_TO_PROCESS:
            sub_text = self.process_elem(elem, module_name)
            sub_texts.append(sub_text)
    module_text += "\n".join(sub_texts)
    return Document(text=module_text)

```
 |  
| --- | --- |  
###  process_class [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.process_class "Permanent link")

```
process_class(class_node: ClassDef, parent_node: )

```

Process a class node in the AST and add relevant information to the graph.
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.process_class--parameters "Permanent link")
class_node : ast.ClassDef The class node to process. It represents a class definition in the abstract syntax tree (AST). parent_node : str The name of the parent node. It specifies the name of the parent node in the graph.
##### Returns[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.process_class--returns "Permanent link")
str A string representation of the processed class node and its sub-elements. It provides a textual representation of the processed class node and its sub-elements.
Source code in `llama-index-integrations/readers/llama-index-readers-docstring-walker/llama_index/readers/docstring_walker/base.py`  
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
```
 | 
```
defprocess_class(self, class_node: ast.ClassDef, parent_node: str):
"""
    Process a class node in the AST and add relevant information to the graph.

    Parameters
    ----------
    class_node : ast.ClassDef
        The class node to process. It represents a class definition
        in the abstract syntax tree (AST).
    parent_node : str
        The name of the parent node. It specifies the name of the parent node in the graph.

    Returns
    -------
    str
        A string representation of the processed class node and its sub-elements.
        It provides a textual representation of the processed class node and its sub-elements.

    """
    cls_name = class_node.name
    cls_docstring = ast.get_docstring(class_node)

    text = f"\n Class name: {cls_name}, In: {parent_node}\n Docstring: {cls_docstring}"
    sub_texts = []
    for elem in class_node.body:
        sub_text = self.process_elem(elem, cls_name)
        sub_texts.append(sub_text)
    return text + "\n".join(sub_texts)

```
 |  
| --- | --- |  
###  process_function [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.process_function "Permanent link")

```
process_function(
    func_node: FunctionDef, parent_node: 
) -> 

```

Process a function node in the AST and add it to the graph. Build node text.
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.process_function--parameters "Permanent link")
func_node : ast.FunctionDef The function node to process. parent_node : str The name of the parent node.
##### Returns[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.process_function--returns "Permanent link")
str A string representation of the processed function node with its sub-elements.
Source code in `llama-index-integrations/readers/llama-index-readers-docstring-walker/llama_index/readers/docstring_walker/base.py`  
| 
```
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
```
 | 
```
defprocess_function(self, func_node: ast.FunctionDef, parent_node: str) -> str:
"""
    Process a function node in the AST and add it to the graph. Build node text.

    Parameters
    ----------
    func_node : ast.FunctionDef
        The function node to process.
    parent_node : str
        The name of the parent node.

    Returns
    -------
    str
        A string representation of the processed function node with its sub-elements.

    """
    func_name = func_node.name
    func_docstring = ast.get_docstring(func_node)

    text = f"\n Function name: {func_name}, In: {parent_node}\n Docstring: {func_docstring}"
    sub_texts = []
    for elem in func_node.body:
        sub_text = self.process_elem(elem, func_name)
        sub_texts.append(sub_text)
    return text + "\n".join(sub_texts)

```
 |  
| --- | --- |  
###  process_elem [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docstring_walker/#llama_index.readers.docstring_walker.DocstringWalker.process_elem "Permanent link")

```
process_elem(elem, parent_node: ) -> 

```

Process an element in the abstract syntax tree (AST).
This is a generic function that delegates the execution to more specific functions based on the type of the element.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `elem`  |  The element to process.  |  _required_  |  
|  `parent_node`  |  The parent node in the graph.  |  _required_  |  
|  `graph`  |  `Graph`  |  The graph to update.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The result of processing the element.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-docstring-walker/llama_index/readers/docstring_walker/base.py`  
| 
```
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
```
 | 
```
defprocess_elem(self, elem, parent_node: str) -> str:
"""
    Process an element in the abstract syntax tree (AST).

    This is a generic function that delegates the execution to more specific
    functions based on the type of the element.

    Args:
        elem (ast.AST): The element to process.
        parent_node (str): The parent node in the graph.
        graph (nx.Graph): The graph to update.

    Returns:
        str: The result of processing the element.

    """
    if isinstance(elem, ast.FunctionDef):
        return self.process_function(elem, parent_node)
    elif isinstance(elem, ast.ClassDef):
        return self.process_class(elem, parent_node)
    return ""

```
 |  
| --- | --- |  
options: members: - DocstringWalker
