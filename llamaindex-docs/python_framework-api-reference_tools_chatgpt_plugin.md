# Chatgpt plugin
init.py.
##  ChatGPTPluginToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/chatgpt_plugin/#llama_index.tools.chatgpt_plugin.ChatGPTPluginToolSpec "Permanent link")
Bases: 
ChatGPT Plugin Tool.
This tool leverages the OpenAPI tool spec to automatically load ChatGPT plugins from a manifest file. You should also provide the Requests tool spec to allow the Agent to make calls to the OpenAPI endpoints To use endpoints with authorization, use the Requests tool spec with the authorization headers
Source code in `llama-index-integrations/tools/llama-index-tools-chatgpt-plugin/llama_index/tools/chatgpt_plugin/base.py`  
| 
```
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
```
 | 
```
classChatGPTPluginToolSpec(BaseToolSpec):
"""
    ChatGPT Plugin Tool.

    This tool leverages the OpenAPI tool spec to automatically load ChatGPT
    plugins from a manifest file.
    You should also provide the Requests tool spec to allow the Agent to make calls to the OpenAPI endpoints
    To use endpoints with authorization, use the Requests tool spec with the authorization headers
    """

    spec_functions = ["load_openapi_spec", "describe_plugin"]

    def__init__(
        self, manifest: Optional[dict] = None, manifest_url: Optional[str] = None
    ):
        importyaml

        if manifest and manifest_url:
            raise ValueError("You cannot provide both a manifest and a manifest_url")
        elif manifest:
            pass
        elif manifest_url:
            response = requests.get(manifest_url).text
            manifest = yaml.safe_load(response)
        else:
            raise ValueError("You must provide either a manifest or a manifest_url")

        if manifest["api"]["type"] != "openapi":
            raise ValueError(
                f'API type must be "openapi", not "{manifest["api"]["type"]}"'
            )

        if manifest["auth"]["type"] != "none":
            raise ValueError("Authentication cannot be supported for ChatGPT plugins")

        self.openapi = OpenAPIToolSpec(url=manifest["api"]["url"])

        self.plugin_description = f"""
            'human_description': {manifest["description_for_human"]}
            'model_description': {manifest["description_for_model"]}
        """

    defload_openapi_spec(self) -> List[Document]:
"""
        You are an AI agent specifically designed to retrieve information by making web requests to an API based on an OpenAPI specification.

        Here's a step-by-step guide to assist you in answering questions:

        1. Determine the base URL required for making the request

        2. Identify the relevant paths necessary to address the question

        3. Find the required parameters for making the request

        4. Perform the necessary requests to obtain the answer

        Returns:
            Document: A List of Document objects describing the OpenAPI spec

        """
        return self.openapi.load_openapi_spec()

    defdescribe_plugin(self) -> List[Document]:
        return self.plugin_description

```
 |  
| --- | --- |  
###  load_openapi_spec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/chatgpt_plugin/#llama_index.tools.chatgpt_plugin.ChatGPTPluginToolSpec.load_openapi_spec "Permanent link")

```
load_openapi_spec() -> []

```

You are an AI agent specifically designed to retrieve information by making web requests to an API based on an OpenAPI specification.
Here's a step-by-step guide to assist you in answering questions:
  1. Determine the base URL required for making the request
  2. Identify the relevant paths necessary to address the question
  3. Find the required parameters for making the request
  4. Perform the necessary requests to obtain the answer


Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |   |  A List of Document objects describing the OpenAPI spec  |  
Source code in `llama-index-integrations/tools/llama-index-tools-chatgpt-plugin/llama_index/tools/chatgpt_plugin/base.py`  
| 
```
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
defload_openapi_spec(self) -> List[Document]:
"""
    You are an AI agent specifically designed to retrieve information by making web requests to an API based on an OpenAPI specification.

    Here's a step-by-step guide to assist you in answering questions:

    1. Determine the base URL required for making the request

    2. Identify the relevant paths necessary to address the question

    3. Find the required parameters for making the request

    4. Perform the necessary requests to obtain the answer

    Returns:
        Document: A List of Document objects describing the OpenAPI spec

    """
    return self.openapi.load_openapi_spec()

```
 |  
| --- | --- |  
options: members: - ChatGPTPluginToolSpec
