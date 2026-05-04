# Linkup research
##  LinkupToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/linkup_research/#llama_index.tools.linkup_research.LinkupToolSpec "Permanent link")
Bases: 
Linkup tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-linkup-research/llama_index/tools/linkup_research/base.py`  
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
```
 | 
```
classLinkupToolSpec(BaseToolSpec):
"""Linkup tool spec."""

    spec_functions = [
        "search",
    ]

    def__init__(self, api_key: str, depth: str, output_type: str) -> None:
"""Initialize with parameters."""
        fromlinkupimport LinkupClient

        self.client = LinkupClient(api_key=api_key)
        self.depth = depth
        self.output_type = output_type

    defsearch(self, query: str):
"""
        Run query through Linkup Search and return metadata.

        Args:
            query: The query to search for.

        """
        api_params = {
            "query": query,
            "depth": self.depth,
            "output_type": self.output_type,
        }
        if self.output_type == "structured":
            if not self.structured_output_schema:
                raise ValueError(
                    "structured_output_schema must be provided when output_type is 'structured'."
                )
            api_params["structured_output_schema"] = self.structured_output_schema
        return self.client.search(**api_params)

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/linkup_research/#llama_index.tools.linkup_research.LinkupToolSpec.search "Permanent link")

```
search(query: )

```

Run query through Linkup Search and return metadata.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to search for.  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-linkup-research/llama_index/tools/linkup_research/base.py`  
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
36
37
38
39
40
```
 | 
```
defsearch(self, query: str):
"""
    Run query through Linkup Search and return metadata.

    Args:
        query: The query to search for.

    """
    api_params = {
        "query": query,
        "depth": self.depth,
        "output_type": self.output_type,
    }
    if self.output_type == "structured":
        if not self.structured_output_schema:
            raise ValueError(
                "structured_output_schema must be provided when output_type is 'structured'."
            )
        api_params["structured_output_schema"] = self.structured_output_schema
    return self.client.search(**api_params)

```
 |  
| --- | --- |  
options: members: - LinkupToolSpec
