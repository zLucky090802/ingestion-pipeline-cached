# Graphql
##  GraphQLToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/graphql/#llama_index.tools.graphql.GraphQLToolSpec "Permanent link")
Bases: 
Requests Tool.
Source code in `llama-index-integrations/tools/llama-index-tools-graphql/llama_index/tools/graphql/base.py`  
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
36
37
38
39
40
41
42
```
 | 
```
classGraphQLToolSpec(BaseToolSpec):
"""Requests Tool."""

    spec_functions = ["graphql_request"]

    def__init__(self, url: str, headers: Optional[dict] = {}):
        self.headers = headers
        self.url = url

    defgraphql_request(self, query: str, variables: str, operation_name: str):
r"""
        Use this tool to make a GraphQL query against the server.

        Args:
            query (str): The GraphQL query to execute
            variables (str): The variable values for the query
            operation_name (str): The name for the query

        example input:
            "query":"query Ships {\n  ships {\n    id\n    model\n    name\n    type\n    status\n  }\n}",
            "variables":{},
            "operation_name":"Ships"

        """
        res = requests.post(
            self.url,
            headers=self.headers,
            json={
                "query": query,
                "variables": variables,
                "operationName": operation_name,
            },
        )
        return res.text

```
 |  
| --- | --- |  
###  graphql_request [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/graphql/#llama_index.tools.graphql.GraphQLToolSpec.graphql_request "Permanent link")

```
graphql_request(
    query: , variables: , operation_name: 
)

```

Use this tool to make a GraphQL query against the server.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The GraphQL query to execute  |  _required_  |  
|  `variables`  |  The variable values for the query  |  _required_  |  
|  `operation_name`  |  The name for the query  |  _required_  |  
example input
"query":"query Ships {\n ships {\n id\n model\n name\n type\n status\n }\n}", "variables":{}, "operation_name":"Ships"
Source code in `llama-index-integrations/tools/llama-index-tools-graphql/llama_index/tools/graphql/base.py`  
| 
```
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
```
 | 
```
defgraphql_request(self, query: str, variables: str, operation_name: str):
r"""
    Use this tool to make a GraphQL query against the server.

    Args:
        query (str): The GraphQL query to execute
        variables (str): The variable values for the query
        operation_name (str): The name for the query

    example input:
        "query":"query Ships {\n  ships {\n    id\n    model\n    name\n    type\n    status\n  }\n}",
        "variables":{},
        "operation_name":"Ships"

    """
    res = requests.post(
        self.url,
        headers=self.headers,
        json={
            "query": query,
            "variables": variables,
            "operationName": operation_name,
        },
    )
    return res.text

```
 |  
| --- | --- |  
options: members: - GraphQLToolSpec
