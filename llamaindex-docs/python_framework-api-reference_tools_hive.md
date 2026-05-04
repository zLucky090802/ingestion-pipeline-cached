# Hive
##  HiveToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/hive/#llama_index.tools.hive.HiveToolSpec "Permanent link")
Bases: 
Hive Search tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-hive/llama_index/tools/hive/base.py`  
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
```
 | 
```
classHiveToolSpec(BaseToolSpec):
"""Hive Search tool spec."""

    spec_functions = ["search"]

    def__init__(
        self,
        api_key: str,
        temperature: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
    ) -> None:
        self.client = HiveSearchClient(api_key=api_key)
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p

    defsearch(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List[HiveSearchMessage]] = None,
        include_data_sources: bool = False,
    ) -> HiveSearchResponse:
"""
        Executes a Hive search request via prompt or chat-style messages.
        """
        req_args = {
            "prompt": prompt,
            "messages": messages,
            "include_data_sources": include_data_sources,
        }

        # Only add parameters if they are not None
        if self.temperature is not None:
            req_args["temperature"] = self.temperature
        if self.top_k is not None:
            req_args["top_k"] = self.top_k
        if self.top_p is not None:
            req_args["top_p"] = self.top_p

        req = HiveSearchRequest(**req_args)
        try:
            response = self.client.search(req)
        except HiveSearchAPIError as e:
            raise RuntimeError(f"{e}") frome

        # Return the Hive search response
        return response

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/hive/#llama_index.tools.hive.HiveToolSpec.search "Permanent link")

```
search(
    prompt: Optional[] = None,
    messages: Optional[[HiveSearchMessage]] = None,
    include_data_sources:  = False,
) -> HiveSearchResponse

```

Executes a Hive search request via prompt or chat-style messages.
Source code in `llama-index-integrations/tools/llama-index-tools-hive/llama_index/tools/hive/base.py`  
| 
```
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
```
 | 
```
defsearch(
    self,
    prompt: Optional[str] = None,
    messages: Optional[List[HiveSearchMessage]] = None,
    include_data_sources: bool = False,
) -> HiveSearchResponse:
"""
    Executes a Hive search request via prompt or chat-style messages.
    """
    req_args = {
        "prompt": prompt,
        "messages": messages,
        "include_data_sources": include_data_sources,
    }

    # Only add parameters if they are not None
    if self.temperature is not None:
        req_args["temperature"] = self.temperature
    if self.top_k is not None:
        req_args["top_k"] = self.top_k
    if self.top_p is not None:
        req_args["top_p"] = self.top_p

    req = HiveSearchRequest(**req_args)
    try:
        response = self.client.search(req)
    except HiveSearchAPIError as e:
        raise RuntimeError(f"{e}") frome

    # Return the Hive search response
    return response

```
 |  
| --- | --- |  
options: members: - HiveToolSpec
