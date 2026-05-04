# Python file
##  PythonFileToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/python_file/#llama_index.tools.python_file.PythonFileToolSpec "Permanent link")
Bases: 
Source code in `llama-index-integrations/tools/llama-index-tools-python-file/llama_index/tools/python_file/base.py`  
| 
```
 7
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
```
 | 
```
classPythonFileToolSpec(BaseToolSpec):
    spec_functions = ["function_definitions", "get_function", "get_functions"]

    def__init__(self, file_name: str) -> None:
        f = open(file_name).read()
        self.tree = ast.parse(f)

    deffunction_definitions(self, external: Optional[bool] = True) -> str:
"""
        Use this function to get the name and arguments of all function definitions in the python file.

        Args:
            external (Optional[bool]): Defaults to true. If false, this function will also return functions that start with _

        """
        functions = ""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if external and node.name.startswith("_"):
                    continue
                functions += f"""
name: {node.name}
arguments: {ast.dump(node.args)}

        return functions

    defget_function(self, name: str) -> str:
"""
        Use this function to get the name and arguments of a single function definition in the python file.

        Args:
            name (str): The name of the function to retrieve

        """
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == name:
                    return f"""
name: {node.name}
arguments: {ast.dump(node.args)}
docstring: {ast.get_docstring(node)}

        return None

    defget_functions(self, names: List[str]) -> str:
"""
        Use this function to get the name and arguments of a list of function definition in the python file.

        Args:
            name (List[str]): The names of the functions to retrieve

        """
        functions = ""
        for name in names:
            functions += self.get_function(name) + "\n"
        return functions

```
 |  
| --- | --- |  
###  function_definitions [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/python_file/#llama_index.tools.python_file.PythonFileToolSpec.function_definitions "Permanent link")

```
function_definitions(
    external: Optional[] = True,
) -> 

```

Use this function to get the name and arguments of all function definitions in the python file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `external`  |  `Optional[bool]`  |  Defaults to true. If false, this function will also return functions that start with _  |  `True`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-python-file/llama_index/tools/python_file/base.py`  
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
```
 | 
```
    deffunction_definitions(self, external: Optional[bool] = True) -> str:
"""
        Use this function to get the name and arguments of all function definitions in the python file.

        Args:
            external (Optional[bool]): Defaults to true. If false, this function will also return functions that start with _

        """
        functions = ""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if external and node.name.startswith("_"):
                    continue
                functions += f"""
name: {node.name}
arguments: {ast.dump(node.args)}

        return functions

```
 |  
| --- | --- |  
###  get_function [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/python_file/#llama_index.tools.python_file.PythonFileToolSpec.get_function "Permanent link")

```
get_function(name: ) -> 

```

Use this function to get the name and arguments of a single function definition in the python file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  The name of the function to retrieve  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-python-file/llama_index/tools/python_file/base.py`  
| 
```
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
```
 | 
```
    defget_function(self, name: str) -> str:
"""
        Use this function to get the name and arguments of a single function definition in the python file.

        Args:
            name (str): The name of the function to retrieve

        """
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == name:
                    return f"""
name: {node.name}
arguments: {ast.dump(node.args)}
docstring: {ast.get_docstring(node)}

        return None

```
 |  
| --- | --- |  
###  get_functions [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/python_file/#llama_index.tools.python_file.PythonFileToolSpec.get_functions "Permanent link")

```
get_functions(names: []) -> 

```

Use this function to get the name and arguments of a list of function definition in the python file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  `List[str]`  |  The names of the functions to retrieve  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-python-file/llama_index/tools/python_file/base.py`  
| 
```
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
```
 | 
```
defget_functions(self, names: List[str]) -> str:
"""
    Use this function to get the name and arguments of a list of function definition in the python file.

    Args:
        name (List[str]): The names of the functions to retrieve

    """
    functions = ""
    for name in names:
        functions += self.get_function(name) + "\n"
    return functions

```
 |  
| --- | --- |  
options: members: - PythonFileToolSpec
