# Openapi
##  OpenAPIToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/openapi/#llama_index.tools.openapi.OpenAPIToolSpec "Permanent link")
Bases: 
OpenAPI Tool.
This tool can be used to parse an OpenAPI spec for endpoints and operations Use the RequestsToolSpec to automate requests to the openapi server
Source code in `llama-index-integrations/tools/llama-index-tools-openapi/llama_index/tools/openapi/base.py`  
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
```
 | 
```
classOpenAPIToolSpec(BaseToolSpec):
"""
    OpenAPI Tool.

    This tool can be used to parse an OpenAPI spec for endpoints and operations
    Use the RequestsToolSpec to automate requests to the openapi server
    """

    spec_functions = ["load_openapi_spec"]

    def__init__(
        self,
        spec: Optional[dict] = None,
        url: Optional[str] = None,
        operation_id_filter: Callable[[str], bool] = None,
    ):
        importyaml

        if spec and url:
            raise ValueError("Only provide one of OpenAPI dict or url")
        elif spec:
            pass
        elif url:
            response = requests.get(url).text
            spec = yaml.safe_load(response)
        else:
            raise ValueError("You must provide a url or OpenAPI spec as a dict")

        # TODO: if we retrieved spec from URL, the server URL inside the spec may be relative to
        #  the retrieval URL.
        parsed_spec = self.process_api_spec(spec, operation_id_filter)
        self.spec = Document(text=json.dumps(parsed_spec))

    defload_openapi_spec(self) -> List[Document]:
"""
        You are an AI agent specifically designed to retrieve information by making web requests to
        an API based on an OpenAPI specification.

        Here's a step-by-step guide to assist you in answering questions:

        1. Determine the server base URL required for making the request

        2. Identify the relevant endpoint (a HTTP verb plus path template) necessary to address the
        question

        3. Generate the required parameters and/or request body for making the request to the
        endpoint

        4. Perform the necessary requests to obtain the answer

        Returns:
            Document: A List of Document objects that describes the available API.

        """
        return [self.spec]

    defprocess_api_spec(
        self, spec: dict, operation_id_filter: Callable[[str], bool]
    ) -> dict:
"""
        Perform simplification and reduction on an OpenAPI specification.

        The goal is to create a more concise and efficient representation
        for retrieval purposes.
        """

        defreduce_details(details: dict) -> dict:
            reduced = OrderedDict()
            if details.get("description"):
                reduced["description"] = details.get("description")
            elif details.get("summary"):
                reduced["description"] = details.get("summary")
            if details.get("parameters"):
                reduced["parameters"] = details.get("parameters", [])
            if details.get("requestBody"):
                reduced["requestBody"] = details.get("requestBody")
            if "200" in details["responses"]:
                reduced["responses"] = details["responses"]["200"]
            return reduced

        defdereference_openapi(openapi_doc):
"""Dereferences a Swagger/OpenAPI document by resolving all $ref pointers."""
            try:
                importjsonschema
            except ImportError:
                raise ImportError(
                    "The jsonschema library is required to parse OpenAPI documents. "
                    "Please install it with `pip install jsonschema`."
                )

            resolver = jsonschema.RefResolver.from_schema(openapi_doc)

            def_dereference(obj):
                if isinstance(obj, dict):
                    if "$ref" in obj:
                        with resolver.resolving(obj["$ref"]) as resolved:
                            return _dereference(resolved)
                    return {k: _dereference(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [_dereference(item) for item in obj]
                else:
                    return obj

            return _dereference(openapi_doc)

        spec = dereference_openapi(spec)
        endpoints = []
        for path_template, operations in spec["paths"].items():
            for operation, operation_detail in operations.items():
                operation_id = operation_detail.get("operationId")
                if operation_id_filter is None or operation_id_filter(operation_id):
                    if operation in ["get", "post", "patch", "put", "delete"]:
                        # preserve order so the LLM "reads" the description first before all the
                        # schema details
                        details = OrderedDict()
                        details["verb"] = operation.upper()
                        details["path_template"] = path_template
                        details.update(reduce_details(operation_detail))
                        endpoints.append(details)

        return {
            "servers": spec["servers"],
            "description": spec["info"].get("description"),
            "endpoints": endpoints,
        }

```
 |  
| --- | --- |  
###  load_openapi_spec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/openapi/#llama_index.tools.openapi.OpenAPIToolSpec.load_openapi_spec "Permanent link")

```
load_openapi_spec() -> []

```

You are an AI agent specifically designed to retrieve information by making web requests to an API based on an OpenAPI specification.
Here's a step-by-step guide to assist you in answering questions:
  1. Determine the server base URL required for making the request
  2. Identify the relevant endpoint (a HTTP verb plus path template) necessary to address the question
  3. Generate the required parameters and/or request body for making the request to the endpoint
  4. Perform the necessary requests to obtain the answer


Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |   |  A List of Document objects that describes the available API.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-openapi/llama_index/tools/openapi/base.py`  
| 
```
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
```
 | 
```
defload_openapi_spec(self) -> List[Document]:
"""
    You are an AI agent specifically designed to retrieve information by making web requests to
    an API based on an OpenAPI specification.

    Here's a step-by-step guide to assist you in answering questions:

    1. Determine the server base URL required for making the request

    2. Identify the relevant endpoint (a HTTP verb plus path template) necessary to address the
    question

    3. Generate the required parameters and/or request body for making the request to the
    endpoint

    4. Perform the necessary requests to obtain the answer

    Returns:
        Document: A List of Document objects that describes the available API.

    """
    return [self.spec]

```
 |  
| --- | --- |  
###  process_api_spec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/openapi/#llama_index.tools.openapi.OpenAPIToolSpec.process_api_spec "Permanent link")

```
process_api_spec(
    spec: , operation_id_filter: Callable[[], ]
) -> 

```

Perform simplification and reduction on an OpenAPI specification.
The goal is to create a more concise and efficient representation for retrieval purposes.
Source code in `llama-index-integrations/tools/llama-index-tools-openapi/llama_index/tools/openapi/base.py`  
| 
```
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
```
 | 
```
defprocess_api_spec(
    self, spec: dict, operation_id_filter: Callable[[str], bool]
) -> dict:
"""
    Perform simplification and reduction on an OpenAPI specification.

    The goal is to create a more concise and efficient representation
    for retrieval purposes.
    """

    defreduce_details(details: dict) -> dict:
        reduced = OrderedDict()
        if details.get("description"):
            reduced["description"] = details.get("description")
        elif details.get("summary"):
            reduced["description"] = details.get("summary")
        if details.get("parameters"):
            reduced["parameters"] = details.get("parameters", [])
        if details.get("requestBody"):
            reduced["requestBody"] = details.get("requestBody")
        if "200" in details["responses"]:
            reduced["responses"] = details["responses"]["200"]
        return reduced

    defdereference_openapi(openapi_doc):
"""Dereferences a Swagger/OpenAPI document by resolving all $ref pointers."""
        try:
            importjsonschema
        except ImportError:
            raise ImportError(
                "The jsonschema library is required to parse OpenAPI documents. "
                "Please install it with `pip install jsonschema`."
            )

        resolver = jsonschema.RefResolver.from_schema(openapi_doc)

        def_dereference(obj):
            if isinstance(obj, dict):
                if "$ref" in obj:
                    with resolver.resolving(obj["$ref"]) as resolved:
                        return _dereference(resolved)
                return {k: _dereference(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_dereference(item) for item in obj]
            else:
                return obj

        return _dereference(openapi_doc)

    spec = dereference_openapi(spec)
    endpoints = []
    for path_template, operations in spec["paths"].items():
        for operation, operation_detail in operations.items():
            operation_id = operation_detail.get("operationId")
            if operation_id_filter is None or operation_id_filter(operation_id):
                if operation in ["get", "post", "patch", "put", "delete"]:
                    # preserve order so the LLM "reads" the description first before all the
                    # schema details
                    details = OrderedDict()
                    details["verb"] = operation.upper()
                    details["path_template"] = path_template
                    details.update(reduce_details(operation_detail))
                    endpoints.append(details)

    return {
        "servers": spec["servers"],
        "description": spec["info"].get("description"),
        "endpoints": endpoints,
    }

```
 |  
| --- | --- |  
options: members: - OpenAPIToolSpec
