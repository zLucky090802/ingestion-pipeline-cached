# Multion
##  MultionToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/multion/#llama_index.tools.multion.MultionToolSpec "Permanent link")
Bases: 
Multion tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-multion/llama_index/tools/multion/base.py`  
| 
```
 6
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
```
 | 
```
classMultionToolSpec(BaseToolSpec):
"""Multion tool spec."""

    spec_functions = ["browse"]

    def__init__(self, api_key: str) -> None:
"""Initialize with parameters."""
        frommultion.clientimport MultiOn

        self.multion = MultiOn(api_key=api_key)

    defbrowse(self, cmd: str):
"""
        Browse the web using Multion
        Multion gives the ability for LLMs to control web browsers using natural language instructions.

        You may have to repeat the instruction through multiple steps or update your instruction to get to
        the final desired state. If the status is 'CONTINUE', reissue the same instruction to continue execution

        Args:
            cmd (str): The detailed and specific natural language instructrion for web browsing

        """
        return self.multion.browse(cmd=cmd, local=True)

```
 |  
| --- | --- |  
###  browse [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/multion/#llama_index.tools.multion.MultionToolSpec.browse "Permanent link")

```
browse(cmd: )

```

Browse the web using Multion Multion gives the ability for LLMs to control web browsers using natural language instructions.
You may have to repeat the instruction through multiple steps or update your instruction to get to the final desired state. If the status is 'CONTINUE', reissue the same instruction to continue execution
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `cmd`  |  The detailed and specific natural language instructrion for web browsing  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-multion/llama_index/tools/multion/base.py`  
| 
```
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
```
 | 
```
defbrowse(self, cmd: str):
"""
    Browse the web using Multion
    Multion gives the ability for LLMs to control web browsers using natural language instructions.

    You may have to repeat the instruction through multiple steps or update your instruction to get to
    the final desired state. If the status is 'CONTINUE', reissue the same instruction to continue execution

    Args:
        cmd (str): The detailed and specific natural language instructrion for web browsing

    """
    return self.multion.browse(cmd=cmd, local=True)

```
 |  
| --- | --- |  
options: members: - MultionToolSpec
