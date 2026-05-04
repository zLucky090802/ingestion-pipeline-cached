# Notion
Notion tool spec.
##  NotionToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/notion/#llama_index.tools.notion.NotionToolSpec "Permanent link")
Bases: 
Notion tool spec.
Currently a simple wrapper around the data loader. TODO: add more methods to the Notion spec.
Source code in `llama-index-integrations/tools/llama-index-tools-notion/llama_index/tools/notion/base.py`  
| 
```
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
```
 | 
```
classNotionToolSpec(BaseToolSpec):
"""
    Notion tool spec.

    Currently a simple wrapper around the data loader.
    TODO: add more methods to the Notion spec.

    """

    spec_functions = ["load_data", "search_data"]

    def__init__(self, integration_token: Optional[str] = None) -> None:
"""Initialize with parameters."""
        self.reader = NotionPageReader(integration_token=integration_token)

    defget_fn_schema_from_fn_name(
        self, fn_name: str, spec_functions: Optional[List[SPEC_FUNCTION_TYPE]] = None
    ) -> Optional[Type[BaseModel]]:
"""Return map from function name."""
        if fn_name == "load_data":
            return NotionLoadDataSchema
        elif fn_name == "search_data":
            return NotionSearchDataSchema
        else:
            raise ValueError(f"Invalid function name: {fn_name}")

    defload_data(
        self,
        page_ids: Optional[List[str]] = None,
        database_ids: Optional[List[str]] = None,
    ) -> str:
"""
        Loads content from a set of page ids or database ids.

        Don't use this endpoint if you don't know the page ids or database ids.

        """
        page_ids = page_ids or []
        docs = self.reader.load_data(page_ids=page_ids, database_ids=database_ids)
        return "\n".join([doc.get_content() for doc in docs])

    defsearch_data(
        self,
        query: str,
        direction: Optional[str] = None,
        timestamp: Optional[str] = None,
        value: Optional[str] = None,
        property: Optional[str] = None,
        page_size: int = 100,
    ) -> List[Dict[str, Any]]:
"""
        Search a list of relevant pages.

        Contains metadata for each page (but not the page content).
        params:
           query: the title of the page or database to search for, which is fuzzy matched.
        """
        payload: Dict[str, Any] = {
            "query": query,
            "page_size": page_size,
        }
        if direction is not None or timestamp is not None:
            payload["sort"] = {}
            if direction is not None:
                payload["sort"]["direction"] = direction
            if timestamp is not None:
                payload["sort"]["timestamp"] = timestamp

        if value is not None or property is not None:
            payload["filter"] = {}
            if value is not None:
                payload["filter"]["value"] = value
            if property is not None:
                payload["filter"]["property"] = property

        response = requests.post(SEARCH_URL, json=payload, headers=self.reader.headers)
        response_json = response.json()
        return response_json["results"]

```
 |  
| --- | --- |  
###  get_fn_schema_from_fn_name [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/notion/#llama_index.tools.notion.NotionToolSpec.get_fn_schema_from_fn_name "Permanent link")

```
get_fn_schema_from_fn_name(
    fn_name: ,
    spec_functions: Optional[
        [SPEC_FUNCTION_TYPE]
    ] = None,
) -> Optional[[BaseModel]]

```

Return map from function name.
Source code in `llama-index-integrations/tools/llama-index-tools-notion/llama_index/tools/notion/base.py`  
| 
```
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
```
 | 
```
defget_fn_schema_from_fn_name(
    self, fn_name: str, spec_functions: Optional[List[SPEC_FUNCTION_TYPE]] = None
) -> Optional[Type[BaseModel]]:
"""Return map from function name."""
    if fn_name == "load_data":
        return NotionLoadDataSchema
    elif fn_name == "search_data":
        return NotionSearchDataSchema
    else:
        raise ValueError(f"Invalid function name: {fn_name}")

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/notion/#llama_index.tools.notion.NotionToolSpec.load_data "Permanent link")

```
load_data(
    page_ids: Optional[[]] = None,
    database_ids: Optional[[]] = None,
) -> 

```

Loads content from a set of page ids or database ids.
Don't use this endpoint if you don't know the page ids or database ids.
Source code in `llama-index-integrations/tools/llama-index-tools-notion/llama_index/tools/notion/base.py`  
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
```
 | 
```
defload_data(
    self,
    page_ids: Optional[List[str]] = None,
    database_ids: Optional[List[str]] = None,
) -> str:
"""
    Loads content from a set of page ids or database ids.

    Don't use this endpoint if you don't know the page ids or database ids.

    """
    page_ids = page_ids or []
    docs = self.reader.load_data(page_ids=page_ids, database_ids=database_ids)
    return "\n".join([doc.get_content() for doc in docs])

```
 |  
| --- | --- |  
###  search_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/notion/#llama_index.tools.notion.NotionToolSpec.search_data "Permanent link")

```
search_data(
    query: ,
    direction: Optional[] = None,
    timestamp: Optional[] = None,
    value: Optional[] = None,
    property: Optional[] = None,
    page_size:  = 100,
) -> [[, ]]

```

Search a list of relevant pages.
Contains metadata for each page (but not the page content). params: query: the title of the page or database to search for, which is fuzzy matched.
Source code in `llama-index-integrations/tools/llama-index-tools-notion/llama_index/tools/notion/base.py`  
| 
```
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
```
 | 
```
defsearch_data(
    self,
    query: str,
    direction: Optional[str] = None,
    timestamp: Optional[str] = None,
    value: Optional[str] = None,
    property: Optional[str] = None,
    page_size: int = 100,
) -> List[Dict[str, Any]]:
"""
    Search a list of relevant pages.

    Contains metadata for each page (but not the page content).
    params:
       query: the title of the page or database to search for, which is fuzzy matched.
    """
    payload: Dict[str, Any] = {
        "query": query,
        "page_size": page_size,
    }
    if direction is not None or timestamp is not None:
        payload["sort"] = {}
        if direction is not None:
            payload["sort"]["direction"] = direction
        if timestamp is not None:
            payload["sort"]["timestamp"] = timestamp

    if value is not None or property is not None:
        payload["filter"] = {}
        if value is not None:
            payload["filter"]["value"] = value
        if property is not None:
            payload["filter"]["property"] = property

    response = requests.post(SEARCH_URL, json=payload, headers=self.reader.headers)
    response_json = response.json()
    return response_json["results"]

```
 |  
| --- | --- |  
options: members: - NotionToolSpec
