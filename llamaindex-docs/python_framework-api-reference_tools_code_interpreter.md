# Code interpreter
init.py.
##  CodeInterpreterToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/code_interpreter/#llama_index.tools.code_interpreter.CodeInterpreterToolSpec "Permanent link")
Bases: 
Code Interpreter tool spec.
WARNING: This tool provides the Agent access to the `subprocess.run` command. Arbitrary code execution is possible on the machine running this tool. This tool is not recommended to be used in a production setting, and would require heavy sandboxing or virtual machines
Source code in `llama-index-integrations/tools/llama-index-tools-code-interpreter/llama_index/tools/code_interpreter/base.py`  
| 
```
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
```
 | 
```
classCodeInterpreterToolSpec(BaseToolSpec):
"""
    Code Interpreter tool spec.

    WARNING: This tool provides the Agent access to the `subprocess.run` command.
    Arbitrary code execution is possible on the machine running this tool.
    This tool is not recommended to be used in a production setting, and would require heavy sandboxing or virtual machines

    """

    spec_functions = ["code_interpreter"]

    defcode_interpreter(self, code: str):
"""
        A function to execute python code, and return the stdout and stderr.

        You should import any libraries that you wish to use. You have access to any libraries the user has installed.

        The code passed to this function is executed in isolation. It should be complete at the time it is passed to this function.

        You should interpret the output and errors returned from this function, and attempt to fix any problems.
        If you cannot fix the error, show the code to the user and ask for help

        It is not possible to return graphics or other complicated data from this function. If the user cannot see the output, save it to a file and tell the user.
        """
        result = subprocess.run([sys.executable, "-c", code], capture_output=True)
        return f"StdOut:\n{result.stdout}\nStdErr:\n{result.stderr}"

```
 |  
| --- | --- |  
###  code_interpreter [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/code_interpreter/#llama_index.tools.code_interpreter.CodeInterpreterToolSpec.code_interpreter "Permanent link")

```
code_interpreter(code: )

```

A function to execute python code, and return the stdout and stderr.
You should import any libraries that you wish to use. You have access to any libraries the user has installed.
The code passed to this function is executed in isolation. It should be complete at the time it is passed to this function.
You should interpret the output and errors returned from this function, and attempt to fix any problems. If you cannot fix the error, show the code to the user and ask for help
It is not possible to return graphics or other complicated data from this function. If the user cannot see the output, save it to a file and tell the user.
Source code in `llama-index-integrations/tools/llama-index-tools-code-interpreter/llama_index/tools/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defcode_interpreter(self, code: str):
"""
    A function to execute python code, and return the stdout and stderr.

    You should import any libraries that you wish to use. You have access to any libraries the user has installed.

    The code passed to this function is executed in isolation. It should be complete at the time it is passed to this function.

    You should interpret the output and errors returned from this function, and attempt to fix any problems.
    If you cannot fix the error, show the code to the user and ask for help

    It is not possible to return graphics or other complicated data from this function. If the user cannot see the output, save it to a file and tell the user.
    """
    result = subprocess.run([sys.executable, "-c", code], capture_output=True)
    return f"StdOut:\n{result.stdout}\nStdErr:\n{result.stderr}"

```
 |  
| --- | --- |  
options: members: - CodeInterpreterToolSpec
