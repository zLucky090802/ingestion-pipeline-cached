# Dashscope
##  DashScopeJsonNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/dashscope/#llama_index.node_parser.dashscope.DashScopeJsonNodeParser "Permanent link")
Bases: `BaseElementNodeParser`
DashScope Json format element node parser.
Splits a json format document from DashScope Parse into Text Nodes and Index Nodes corresponding to embedded objects (e.g. tables).
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-relational-dashscope/llama_index/node_parser/dashscope/base.py`  
| 
```
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
```
 | 
```
classDashScopeJsonNodeParser(BaseElementNodeParser):
"""
    DashScope Json format element node parser.

    Splits a json format document from DashScope Parse into Text Nodes and Index Nodes
    corresponding to embedded objects (e.g. tables).
    """

    try_count_limit: int = Field(
        default=10, description="Maximum number of retry attempts."
    )
    chunk_size: int = Field(default=500, description="Size of each chunk to process.")
    overlap_size: int = Field(
        default=100, description="Overlap size between consecutive chunks."
    )
    separator: str = Field(
        default=" |,|，|。|？|！|\n|\\?|\\!",
        description="Separator characters for splitting texts.",
    )
    input_type: str = Field(default="idp", description="parse format type.")
    language: str = Field(
        default="cn",
        description="language of tokenizor, accept cn, en, any. Notice that <any> mode will be slow.",
    )

    @classmethod
    defclass_name(cls) -> str:
        return "DashScopeJsonNodeParser"

    defget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
        ftype = node.metadata.get("parse_fmt_type", self.input_type)
        assert ftype in [
            "DASHSCOPE_DOCMIND",
            "idp",
        ], f"Unexpected parse_fmt_type: {node.metadata.get('parse_fmt_type','')}"

        ftype_map = {
            "DASHSCOPE_DOCMIND": "idp",
        }

        my_input = {
            "text": json.loads(node.get_content()),
            "file_type": ftype_map.get(ftype, ftype),
            "chunk_size": self.chunk_size,
            "overlap_size": self.overlap_size,
            "language": "cn",
            "separator": self.separator,
        }

        try_count = 0
        response_text = self.post_service(my_input)
        while response_text is None and try_count  self.try_count_limit:
            try_count += 1
            response_text = self.post_service(my_input)
        if response_text is None:
            logging.error("DashScopeJsonNodeParser Failed to get response from service")
            return []

        return self.parse_result(response_text, node)

    defpost_service(self, my_input: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", None)
        if DASHSCOPE_API_KEY is None:
            logging.error("DASHSCOPE_API_KEY is not set")
            raise ValueError("DASHSCOPE_API_KEY is not set")
        headers = {
            "Content-Type": "application/json",
            "Accept-Encoding": "utf-8",
            "Authorization": "Bearer " + DASHSCOPE_API_KEY,
        }
        service_url = (
            os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com")
            + "/api/v1/indices/component/configed_transformations/spliter"
        )
        try:
            response = requests.post(
                service_url, data=json.dumps(my_input), headers=headers
            )
            response_text = response.json()
            if "chunkService" in response_text:
                return response_text["chunkService"]["chunkResult"]
            else:
                logging.error(f"{response_text}, try again.")
                return None
        except Exception as e:
            logging.error(f"{e}, try again.")
            return None

    defparse_result(
        self, content_json: List[Dict[str, Any]], document: TextNode
    ) -> List[BaseNode]:
        nodes = []
        for data in content_json:
            text = "\n".join(
                [data["title"], data.get("hier_title", ""), data["content"]]
            )
            nodes.append(
                TextNode(
                    metadata=document.metadata,
                    text=text,
                    excluded_embed_metadata_keys=document.excluded_embed_metadata_keys,
                    excluded_llm_metadata_keys=document.excluded_llm_metadata_keys,
                )
            )
        return nodes

    defextract_elements(
        self,
        text: str,
        mode: Optional[str] = "json",
        node_id: Optional[str] = None,
        node_metadata: Optional[Dict[str, Any]] = None,
        table_filters: Optional[List[Callable]] = None,
        **kwargs: Any,
    ) -> List[Element]:
        return []

```
 |  
| --- | --- |  
###  get_nodes_from_node [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/dashscope/#llama_index.node_parser.dashscope.DashScopeJsonNodeParser.get_nodes_from_node "Permanent link")

```
get_nodes_from_node(node: ) -> []

```

Get nodes from node.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-relational-dashscope/llama_index/node_parser/dashscope/base.py`  
| 
```
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
defget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
    ftype = node.metadata.get("parse_fmt_type", self.input_type)
    assert ftype in [
        "DASHSCOPE_DOCMIND",
        "idp",
    ], f"Unexpected parse_fmt_type: {node.metadata.get('parse_fmt_type','')}"

    ftype_map = {
        "DASHSCOPE_DOCMIND": "idp",
    }

    my_input = {
        "text": json.loads(node.get_content()),
        "file_type": ftype_map.get(ftype, ftype),
        "chunk_size": self.chunk_size,
        "overlap_size": self.overlap_size,
        "language": "cn",
        "separator": self.separator,
    }

    try_count = 0
    response_text = self.post_service(my_input)
    while response_text is None and try_count  self.try_count_limit:
        try_count += 1
        response_text = self.post_service(my_input)
    if response_text is None:
        logging.error("DashScopeJsonNodeParser Failed to get response from service")
        return []

    return self.parse_result(response_text, node)

```
 |  
| --- | --- |  
options: members: - DashScopeJsonNodeParser
