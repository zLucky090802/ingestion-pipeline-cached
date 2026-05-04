# Unstructured element
Node parsers.
##  HTMLNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.HTMLNodeParser "Permanent link")
Bases: 
HTML node parser.
Splits a document into Nodes using custom HTML splitting logic.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `include_metadata`  |  `bool`  |  whether to include metadata in nodes  |  _required_  |  
|  `include_prev_next_rel`  |  `bool`  |  whether to include prev/next relationships  |  _required_  |  
|  `tags`  |  `List[str]`  |  HTML tags to extract text from.  |  `['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'b', 'i', 'u', 'section']`  |  
Source code in `llama-index-core/llama_index/core/node_parser/file/html.py`  
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
137
138
139
140
141
142
143
```
 | 
```
classHTMLNodeParser(NodeParser):
"""
    HTML node parser.

    Splits a document into Nodes using custom HTML splitting logic.

    Args:
        include_metadata (bool): whether to include metadata in nodes
        include_prev_next_rel (bool): whether to include prev/next relationships

    """

    tags: List[str] = Field(
        default=DEFAULT_TAGS, description="HTML tags to extract text from."
    )

    @classmethod
    deffrom_defaults(
        cls,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        tags: Optional[List[str]] = DEFAULT_TAGS,
    ) -> "HTMLNodeParser":
        callback_manager = callback_manager or CallbackManager([])

        return cls(
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            callback_manager=callback_manager,
            tags=tags,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "HTMLNodeParser"

    def_parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")

        for node in nodes_with_progress:
            nodes = self.get_nodes_from_node(node)
            all_nodes.extend(nodes)

        return all_nodes

    defget_nodes_from_node(self, node: BaseNode) -> List[TextNode]:
"""Get nodes from document."""
        try:
            frombs4import BeautifulSoup, Tag
        except ImportError:
            raise ImportError("bs4 is required to read HTML files.")

        text = node.get_content(metadata_mode=MetadataMode.NONE)
        soup = BeautifulSoup(text, "html.parser")
        html_nodes = []
        last_tag = None
        current_section = ""

        tags = soup.find_all(self.tags)
        for tag in tags:
            tag_text = self._extract_text_from_tag(tag)
            if isinstance(tag, Tag) and (tag.name == last_tag or last_tag is None):
                last_tag = tag.name
                current_section += f"{tag_text.strip()}\n"
            else:
                html_nodes.append(
                    self._build_node_from_split(
                        current_section.strip(), node, {"tag": last_tag}
                    )
                )
                if isinstance(tag, Tag):
                    last_tag = tag.name
                current_section = f"{tag_text}\n"

        if current_section:
            html_nodes.append(
                self._build_node_from_split(
                    current_section.strip(), node, {"tag": last_tag}
                )
            )

        return html_nodes

    def_extract_text_from_tag(
        self, tag: Union["Tag", "NavigableString", "PageElement"]
    ) -> str:
        frombs4import NavigableString, Tag, PageElement

        texts = []
        if isinstance(tag, Tag):
            for elem in tag.children:
                if isinstance(elem, NavigableString):
                    if elem.strip():
                        texts.append(elem.strip())
                elif isinstance(elem, Tag):
                    if elem.name in self.tags:
                        continue
                    else:
                        texts.append(elem.get_text().strip())
                elif isinstance(elem, PageElement):
                    texts.append(elem.get_text().strip())
        else:
            texts.append(tag.get_text().strip())
        return "\n".join(texts)

    def_build_node_from_split(
        self,
        text_split: str,
        node: BaseNode,
        metadata: dict,
    ) -> TextNode:
"""Build node from single text split."""
        node = build_nodes_from_splits([text_split], node, id_func=self.id_func)[0]

        if self.include_metadata:
            node.metadata = {**node.metadata, **metadata}

        return node

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.HTMLNodeParser.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/node_parser/file/html.py`  
| 
```
51
52
53
54
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "HTMLNodeParser"

```
 |  
| --- | --- |  
###  get_nodes_from_node [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.HTMLNodeParser.get_nodes_from_node "Permanent link")

```
get_nodes_from_node(node: ) -> []

```

Get nodes from document.
Source code in `llama-index-core/llama_index/core/node_parser/file/html.py`  
| 
```
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
```
 | 
```
defget_nodes_from_node(self, node: BaseNode) -> List[TextNode]:
"""Get nodes from document."""
    try:
        frombs4import BeautifulSoup, Tag
    except ImportError:
        raise ImportError("bs4 is required to read HTML files.")

    text = node.get_content(metadata_mode=MetadataMode.NONE)
    soup = BeautifulSoup(text, "html.parser")
    html_nodes = []
    last_tag = None
    current_section = ""

    tags = soup.find_all(self.tags)
    for tag in tags:
        tag_text = self._extract_text_from_tag(tag)
        if isinstance(tag, Tag) and (tag.name == last_tag or last_tag is None):
            last_tag = tag.name
            current_section += f"{tag_text.strip()}\n"
        else:
            html_nodes.append(
                self._build_node_from_split(
                    current_section.strip(), node, {"tag": last_tag}
                )
            )
            if isinstance(tag, Tag):
                last_tag = tag.name
            current_section = f"{tag_text}\n"

    if current_section:
        html_nodes.append(
            self._build_node_from_split(
                current_section.strip(), node, {"tag": last_tag}
            )
        )

    return html_nodes

```
 |  
| --- | --- |  
##  JSONNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.JSONNodeParser "Permanent link")
Bases: 
JSON node parser.
Splits a document into Nodes using custom JSON splitting logic.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `include_metadata`  |  `bool`  |  whether to include metadata in nodes  |  _required_  |  
|  `include_prev_next_rel`  |  `bool`  |  whether to include prev/next relationships  |  _required_  |  
Source code in `llama-index-core/llama_index/core/node_parser/file/json.py`  
| 
```
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
```
 | 
```
classJSONNodeParser(NodeParser):
"""
    JSON node parser.

    Splits a document into Nodes using custom JSON splitting logic.

    Args:
        include_metadata (bool): whether to include metadata in nodes
        include_prev_next_rel (bool): whether to include prev/next relationships

    """

    @classmethod
    deffrom_defaults(
        cls,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        callback_manager: Optional[CallbackManager] = None,
    ) -> "JSONNodeParser":
        callback_manager = callback_manager or CallbackManager([])

        return cls(
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            callback_manager=callback_manager,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "JSONNodeParser"

    def_parse_nodes(
        self, nodes: Sequence[BaseNode], show_progress: bool = False, **kwargs: Any
    ) -> List[BaseNode]:
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")

        for node in nodes_with_progress:
            nodes = self.get_nodes_from_node(node)
            all_nodes.extend(nodes)

        return all_nodes

    defget_nodes_from_node(self, node: BaseNode) -> List[TextNode]:
"""Get nodes from document."""
        text = node.get_content(metadata_mode=MetadataMode.NONE)
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # Handle invalid JSON input here
            return []

        json_nodes = []
        if isinstance(data, dict):
            lines = [*self._depth_first_yield(data, 0, [])]
            json_nodes.extend(
                build_nodes_from_splits(["\n".join(lines)], node, id_func=self.id_func)
            )
        elif isinstance(data, list):
            for json_object in data:
                lines = [*self._depth_first_yield(json_object, 0, [])]
                json_nodes.extend(
                    build_nodes_from_splits(
                        ["\n".join(lines)], node, id_func=self.id_func
                    )
                )
        else:
            raise ValueError("JSON is invalid")

        return json_nodes

    def_depth_first_yield(
        self, json_data: Dict, levels_back: int, path: List[str]
    ) -> Generator[str, None, None]:
"""
        Do depth first yield of all of the leaf nodes of a JSON.

        Combines keys in the JSON tree using spaces.

        If levels_back is set to 0, prints all levels.

        """
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                new_path = path[:]
                new_path.append(key)
                yield from self._depth_first_yield(value, levels_back, new_path)
        elif isinstance(json_data, list):
            for _, value in enumerate(json_data):
                yield from self._depth_first_yield(value, levels_back, path)
        else:
            new_path = path[-levels_back:]
            new_path.append(str(json_data))
            yield " ".join(new_path)

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.JSONNodeParser.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/node_parser/file/json.py`  
| 
```
40
41
42
43
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "JSONNodeParser"

```
 |  
| --- | --- |  
###  get_nodes_from_node [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.JSONNodeParser.get_nodes_from_node "Permanent link")

```
get_nodes_from_node(node: ) -> []

```

Get nodes from document.
Source code in `llama-index-core/llama_index/core/node_parser/file/json.py`  
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
```
 | 
```
defget_nodes_from_node(self, node: BaseNode) -> List[TextNode]:
"""Get nodes from document."""
    text = node.get_content(metadata_mode=MetadataMode.NONE)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Handle invalid JSON input here
        return []

    json_nodes = []
    if isinstance(data, dict):
        lines = [*self._depth_first_yield(data, 0, [])]
        json_nodes.extend(
            build_nodes_from_splits(["\n".join(lines)], node, id_func=self.id_func)
        )
    elif isinstance(data, list):
        for json_object in data:
            lines = [*self._depth_first_yield(json_object, 0, [])]
            json_nodes.extend(
                build_nodes_from_splits(
                    ["\n".join(lines)], node, id_func=self.id_func
                )
            )
    else:
        raise ValueError("JSON is invalid")

    return json_nodes

```
 |  
| --- | --- |  
##  MarkdownNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.MarkdownNodeParser "Permanent link")
Bases: 
Markdown node parser.
Splits a document into Nodes using Markdown header-based splitting logic. Each node contains its text content and the path of headers leading to it.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `include_metadata`  |  `bool`  |  whether to include metadata in nodes  |  _required_  |  
|  `include_prev_next_rel`  |  `bool`  |  whether to include prev/next relationships  |  _required_  |  
|  `header_path_separator`  |  separator char used for section header path metadata  |  `'/'`  |  
Source code in `llama-index-core/llama_index/core/node_parser/file/markdown.py`  
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
137
138
139
140
141
```
 | 
```
classMarkdownNodeParser(NodeParser):
"""
    Markdown node parser.

    Splits a document into Nodes using Markdown header-based splitting logic.
    Each node contains its text content and the path of headers leading to it.

    Args:
        include_metadata (bool): whether to include metadata in nodes
        include_prev_next_rel (bool): whether to include prev/next relationships
        header_path_separator (str): separator char used for section header path metadata

    """

    header_path_separator: str = Field(
        default="/", description="Separator char used for section header path metadata."
    )

    @classmethod
    deffrom_defaults(
        cls,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        header_path_separator: str = "/",
        callback_manager: Optional[CallbackManager] = None,
    ) -> "MarkdownNodeParser":
        callback_manager = callback_manager or CallbackManager([])
        return cls(
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            header_path_separator=header_path_separator,
            callback_manager=callback_manager,
        )

    defget_nodes_from_node(self, node: BaseNode) -> List[TextNode]:
"""Get nodes from document by splitting on headers."""
        text = node.get_content(metadata_mode=MetadataMode.NONE)
        markdown_nodes = []
        lines = text.split("\n")
        current_section = ""
        # Keep track of (markdown level, text) for headers
        header_stack: List[tuple[int, str]] = []
        code_block = False

        for line in lines:
            # Track if we're inside a code block to avoid parsing headers in code
            if line.lstrip().startswith("```"):
                code_block = not code_block
                current_section += line + "\n"
                continue

            # Only parse headers if we're not in a code block
            if not code_block:
                header_match = re.match(r"^(#+)\s(.*)", line)
                if header_match:
                    # Save the previous section before starting a new one
                    if current_section.strip():
                        markdown_nodes.append(
                            self._build_node_from_split(
                                current_section.strip(),
                                node,
                                self.header_path_separator.join(
                                    h[1] for h in header_stack[:-1]
                                ),
                            )
                        )

                    header_level = len(header_match.group(1))
                    header_text = header_match.group(2)

                    # Compare against top-of-stack item’s markdown level.
                    # Pop headers of equal or higher markdown level; not necessarily current stack size / depth.
                    # Hierarchy depth gets deeper one level at a time, but markdown headers can jump from H1 to H3, for example.
                    while header_stack and header_stack[-1][0] >= header_level:
                        header_stack.pop()

                    # Add the new header
                    header_stack.append((header_level, header_text))
                    current_section = "#" * header_level + f" {header_text}\n"
                    continue

            current_section += line + "\n"

        # Add the final section
        if current_section.strip():
            markdown_nodes.append(
                self._build_node_from_split(
                    current_section.strip(),
                    node,
                    self.header_path_separator.join(h[1] for h in header_stack[:-1]),
                )
            )

        return markdown_nodes

    def_build_node_from_split(
        self,
        text_split: str,
        node: BaseNode,
        header_path: str,
    ) -> TextNode:
"""Build node from single text split."""
        node = build_nodes_from_splits([text_split], node, id_func=self.id_func)[0]

        if self.include_metadata:
            separator = self.header_path_separator
            node.metadata["header_path"] = (
                # ex: "/header1/header2/" || "/"
                separator + header_path + separator if header_path else separator
            )

        return node

    def_parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""Parse nodes."""
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")

        for node in nodes_with_progress:
            nodes = self.get_nodes_from_node(node)
            all_nodes.extend(nodes)

        return all_nodes

```
 |  
| --- | --- |  
###  get_nodes_from_node [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.MarkdownNodeParser.get_nodes_from_node "Permanent link")

```
get_nodes_from_node(node: ) -> []

```

Get nodes from document by splitting on headers.
Source code in `llama-index-core/llama_index/core/node_parser/file/markdown.py`  
| 
```
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
```
 | 
```
defget_nodes_from_node(self, node: BaseNode) -> List[TextNode]:
"""Get nodes from document by splitting on headers."""
    text = node.get_content(metadata_mode=MetadataMode.NONE)
    markdown_nodes = []
    lines = text.split("\n")
    current_section = ""
    # Keep track of (markdown level, text) for headers
    header_stack: List[tuple[int, str]] = []
    code_block = False

    for line in lines:
        # Track if we're inside a code block to avoid parsing headers in code
        if line.lstrip().startswith("```"):
            code_block = not code_block
            current_section += line + "\n"
            continue

        # Only parse headers if we're not in a code block
        if not code_block:
            header_match = re.match(r"^(#+)\s(.*)", line)
            if header_match:
                # Save the previous section before starting a new one
                if current_section.strip():
                    markdown_nodes.append(
                        self._build_node_from_split(
                            current_section.strip(),
                            node,
                            self.header_path_separator.join(
                                h[1] for h in header_stack[:-1]
                            ),
                        )
                    )

                header_level = len(header_match.group(1))
                header_text = header_match.group(2)

                # Compare against top-of-stack item’s markdown level.
                # Pop headers of equal or higher markdown level; not necessarily current stack size / depth.
                # Hierarchy depth gets deeper one level at a time, but markdown headers can jump from H1 to H3, for example.
                while header_stack and header_stack[-1][0] >= header_level:
                    header_stack.pop()

                # Add the new header
                header_stack.append((header_level, header_text))
                current_section = "#" * header_level + f" {header_text}\n"
                continue

        current_section += line + "\n"

    # Add the final section
    if current_section.strip():
        markdown_nodes.append(
            self._build_node_from_split(
                current_section.strip(),
                node,
                self.header_path_separator.join(h[1] for h in header_stack[:-1]),
            )
        )

    return markdown_nodes

```
 |  
| --- | --- |  
##  SimpleFileNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.SimpleFileNodeParser "Permanent link")
Bases: 
Simple file node parser.
Splits a document loaded from a file into Nodes using logic based on the file type automatically detects the NodeParser to use based on file type
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `include_metadata`  |  `bool`  |  whether to include metadata in nodes  |  _required_  |  
|  `include_prev_next_rel`  |  `bool`  |  whether to include prev/next relationships  |  _required_  |  
Source code in `llama-index-core/llama_index/core/node_parser/file/simple_file.py`  
| 
```
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
```
 | 
```
classSimpleFileNodeParser(NodeParser):
"""
    Simple file node parser.

    Splits a document loaded from a file into Nodes using logic based on the file type
    automatically detects the NodeParser to use based on file type

    Args:
        include_metadata (bool): whether to include metadata in nodes
        include_prev_next_rel (bool): whether to include prev/next relationships

    """

    @classmethod
    deffrom_defaults(
        cls,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        callback_manager: Optional[CallbackManager] = None,
    ) -> "SimpleFileNodeParser":
        callback_manager = callback_manager or CallbackManager([])

        return cls(
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            callback_manager=callback_manager,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "SimpleFileNodeParser"

    def_parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""
        Parse document into nodes.

        Args:
            nodes (Sequence[BaseNode]): nodes to parse

        """
        all_nodes: List[BaseNode] = []
        documents_with_progress = get_tqdm_iterable(
            nodes, show_progress, "Parsing documents into nodes"
        )

        for document in documents_with_progress:
            # Try to get extension from metadata, or extract from file_path
            ext = document.metadata.get("extension")
            if ext is None and "file_path" in document.metadata:
                # Extract extension from file_path
                _, ext = os.path.splitext(document.metadata["file_path"])
                ext = ext.lower()

            if ext and ext in FILE_NODE_PARSERS:
                parser = FILE_NODE_PARSERS[ext](
                    include_metadata=self.include_metadata,
                    include_prev_next_rel=self.include_prev_next_rel,
                    callback_manager=self.callback_manager,
                )

                nodes = parser.get_nodes_from_documents([document], show_progress)
                all_nodes.extend(nodes)
            else:
                # What to do when file type isn't supported yet?
                all_nodes.extend(
                    # build node from document
                    build_nodes_from_splits(
                        [document.get_content(metadata_mode=MetadataMode.NONE)],
                        document,
                        id_func=self.id_func,
                    )
                )

        return all_nodes

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.SimpleFileNodeParser.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/node_parser/file/simple_file.py`  
| 
```
50
51
52
53
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "SimpleFileNodeParser"

```
 |  
| --- | --- |  
##  MetadataAwareTextSplitter [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.MetadataAwareTextSplitter "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/node_parser/interface.py`  
| 
```
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
```
 | 
```
classMetadataAwareTextSplitter(TextSplitter):
    def__init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        super().__init_subclass__(*args, **kwargs)

        # Pydantic v2 keeps the user-defined init on __pydantic_init__
        user_init = getattr(cls, "__pydantic_init__", None)
        if user_init is None:
            return

        # Safety: don't propagate pydantic-generated docs
        if getattr(user_init, "__module__", "").startswith("pydantic"):
            return

        doc = getattr(user_init, "__doc__", None)
        if not doc:
            return

        # Patch the generated __init__ that help() will show
        try:
            cls.__init__.__doc__ = doc
        except (AttributeError, TypeError):
            pass

    @abstractmethod
    defsplit_text_metadata_aware(self, text: str, metadata_str: str) -> List[str]: ...

    defsplit_texts_metadata_aware(
        self, texts: List[str], metadata_strs: List[str]
    ) -> List[str]:
        if len(texts) != len(metadata_strs):
            raise ValueError("Texts and metadata_strs must have the same length")
        nested_texts = [
            self.split_text_metadata_aware(text, metadata)
            for text, metadata in zip(texts, metadata_strs)
        ]
        return [item for sublist in nested_texts for item in sublist]

    def_get_metadata_str(self, node: BaseNode) -> str:
"""Helper function to get the proper metadata str for splitting."""
        embed_metadata_str = node.get_metadata_str(mode=MetadataMode.EMBED)
        llm_metadata_str = node.get_metadata_str(mode=MetadataMode.LLM)

        # use the longest metadata str for splitting
        if len(embed_metadata_str)  len(llm_metadata_str):
            metadata_str = embed_metadata_str
        else:
            metadata_str = llm_metadata_str

        return metadata_str

    def_parse_nodes(
        self, nodes: Sequence[BaseNode], show_progress: bool = False, **kwargs: Any
    ) -> List[BaseNode]:
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")

        for node in nodes_with_progress:
            metadata_str = self._get_metadata_str(node)
            splits = self.split_text_metadata_aware(
                node.get_content(metadata_mode=MetadataMode.NONE),
                metadata_str=metadata_str,
            )
            all_nodes.extend(
                build_nodes_from_splits(splits, node, id_func=self.id_func)
            )

        return all_nodes

```
 |  
| --- | --- |  
##  NodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.NodeParser "Permanent link")
Bases: , 
Base interface for node parser.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `include_metadata`  |  `bool`  |  Whether or not to consider metadata when splitting.  |  `True`  |  
|  `include_prev_next_rel`  |  `bool`  |  Include prev/next node relationships.  |  `True`  |  
|  `callback_manager`  |   |  `<llama_index.core.callbacks.base.CallbackManager object at 0x7f00af2d6270>`  |  
|  `id_func`  |  `Callable`  |  Function to generate node IDs.  |  `<function default_id_func at 0x7f00b0d78bf0>`  |  
Source code in `llama-index-core/llama_index/core/node_parser/interface.py`  
| 
```
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
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
```
 | 
```
classNodeParser(TransformComponent, ABC):
"""Base interface for node parser."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    include_metadata: bool = Field(
        default=True, description="Whether or not to consider metadata when splitting."
    )
    include_prev_next_rel: bool = Field(
        default=True, description="Include prev/next node relationships."
    )
    callback_manager: CallbackManager = Field(
        default_factory=lambda: CallbackManager([]), exclude=True
    )
    id_func: IdFuncCallable = Field(
        default=default_id_func,
        description="Function to generate node IDs.",
    )

    @abstractmethod
    def_parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]: ...

    async def_aparse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
        return self._parse_nodes(nodes, show_progress=show_progress, **kwargs)

    def_postprocess_parsed_nodes(
        self, nodes: List[BaseNode], parent_doc_map: Dict[str, Document]
    ) -> List[BaseNode]:
        # Track search position per document to handle duplicate text correctly
        # Nodes are assumed to be in document order from _parse_nodes
        # We track the START position (not end) to allow for overlapping chunks
        doc_search_positions: Dict[str, int] = {}

        for i, node in enumerate(nodes):
            parent_doc = parent_doc_map.get(node.ref_doc_id or "", None)
            parent_node = node.source_node

            if parent_doc is not None:
                if parent_doc.source_node is not None:
                    node.relationships.update(
                        {
                            NodeRelationship.SOURCE: parent_doc.source_node,
                        }
                    )

                # Get or initialize search position for this document
                doc_id = node.ref_doc_id or ""
                search_start = doc_search_positions.get(doc_id, 0)

                # Search for node content starting from the last found position
                node_content = node.get_content(metadata_mode=MetadataMode.NONE)
                start_char_idx = parent_doc.text.find(node_content, search_start)

                # update start/end char idx
                if start_char_idx >= 0 and isinstance(node, TextNode):
                    node.start_char_idx = start_char_idx
                    node.end_char_idx = start_char_idx + len(node_content)
                    # Update search position to start from next character after this node's START
                    # This allows overlapping chunks to be found correctly
                    doc_search_positions[doc_id] = start_char_idx + 1

                # update metadata
                if self.include_metadata:
                    # Merge parent_doc.metadata into nodes.metadata, giving preference to node's values
                    node.metadata = {**parent_doc.metadata, **node.metadata}

            if parent_node is not None:
                if self.include_metadata:
                    parent_metadata = parent_node.metadata

                    combined_metadata = {**parent_metadata, **node.metadata}

                    # Merge parent_node.metadata into nodes.metadata, giving preference to node's values
                    node.metadata.update(combined_metadata)

            if self.include_prev_next_rel:
                # establish prev/next relationships if nodes share the same source_node
                if (
                    i  0
                    and node.source_node
                    and nodes[i - 1].source_node
                    and nodes[i - 1].source_node.node_id == node.source_node.node_id  # type: ignore
                ):
                    node.relationships[NodeRelationship.PREVIOUS] = nodes[
                        i - 1
                    ].as_related_node_info()
                if (
                    i  len(nodes) - 1
                    and node.source_node
                    and nodes[i + 1].source_node
                    and nodes[i + 1].source_node.node_id == node.source_node.node_id  # type: ignore
                ):
                    node.relationships[NodeRelationship.NEXT] = nodes[
                        i + 1
                    ].as_related_node_info()

        return nodes

    defget_nodes_from_documents(
        self,
        documents: Sequence[Document],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""
        Parse documents into nodes.

        Args:
            documents (Sequence[Document]): documents to parse
            show_progress (bool): whether to show progress bar

        """
        doc_id_to_document = {doc.id_: doc for doc in documents}

        with self.callback_manager.event(
            CBEventType.NODE_PARSING, payload={EventPayload.DOCUMENTS: documents}
        ) as event:
            nodes = self._parse_nodes(documents, show_progress=show_progress, **kwargs)
            nodes = self._postprocess_parsed_nodes(nodes, doc_id_to_document)

            event.on_end({EventPayload.NODES: nodes})

        return nodes

    async defaget_nodes_from_documents(
        self,
        documents: Sequence[Document],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
        doc_id_to_document = {doc.id_: doc for doc in documents}

        with self.callback_manager.event(
            CBEventType.NODE_PARSING, payload={EventPayload.DOCUMENTS: documents}
        ) as event:
            nodes = await self._aparse_nodes(
                documents, show_progress=show_progress, **kwargs
            )
            nodes = self._postprocess_parsed_nodes(nodes, doc_id_to_document)

            event.on_end({EventPayload.NODES: nodes})

        return nodes

    def__call__(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
        return self.get_nodes_from_documents(nodes, **kwargs)  # type: ignore

    async defacall(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
        return await self.aget_nodes_from_documents(nodes, **kwargs)  # type: ignore

```
 |  
| --- | --- |  
###  get_nodes_from_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.NodeParser.get_nodes_from_documents "Permanent link")

```
get_nodes_from_documents(
    documents: Sequence[],
    show_progress:  = False,
    **kwargs: 
) -> []

```

Parse documents into nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `documents`  |  `Sequence[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]`  |  documents to parse  |  _required_  |  
|  `show_progress`  |  `bool`  |  whether to show progress bar  |  `False`  |  
Source code in `llama-index-core/llama_index/core/node_parser/interface.py`  
| 
```
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
```
 | 
```
defget_nodes_from_documents(
    self,
    documents: Sequence[Document],
    show_progress: bool = False,
    **kwargs: Any,
) -> List[BaseNode]:
"""
    Parse documents into nodes.

    Args:
        documents (Sequence[Document]): documents to parse
        show_progress (bool): whether to show progress bar

    """
    doc_id_to_document = {doc.id_: doc for doc in documents}

    with self.callback_manager.event(
        CBEventType.NODE_PARSING, payload={EventPayload.DOCUMENTS: documents}
    ) as event:
        nodes = self._parse_nodes(documents, show_progress=show_progress, **kwargs)
        nodes = self._postprocess_parsed_nodes(nodes, doc_id_to_document)

        event.on_end({EventPayload.NODES: nodes})

    return nodes

```
 |  
| --- | --- |  
##  TextSplitter [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.TextSplitter "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/node_parser/interface.py`  
| 
```
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
```
 | 
```
classTextSplitter(NodeParser):
    @abstractmethod
    defsplit_text(self, text: str) -> List[str]: ...

    defsplit_texts(self, texts: List[str]) -> List[str]:
        nested_texts = [self.split_text(text) for text in texts]
        return [item for sublist in nested_texts for item in sublist]

    def_parse_nodes(
        self, nodes: Sequence[BaseNode], show_progress: bool = False, **kwargs: Any
    ) -> List[BaseNode]:
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")
        for node in nodes_with_progress:
            splits = self.split_text(node.get_content())

            all_nodes.extend(
                build_nodes_from_splits(splits, node, id_func=self.id_func)
            )

        return all_nodes

```
 |  
| --- | --- |  
##  HierarchicalNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.HierarchicalNodeParser "Permanent link")
Bases: 
Hierarchical node parser.
Splits a document into a recursive hierarchy Nodes using a NodeParser.
NOTE: this will return a hierarchy of nodes in a flat list, where there will be overlap between parent nodes (e.g. with a bigger chunk size), and child nodes per parent (e.g. with a smaller chunk size).
For instance, this may return a list of nodes like:
  * list of top-level nodes with chunk size 2048
  * list of second-level nodes, where each node is a child of a top-level node, chunk size 512
  * list of third-level nodes, where each node is a child of a second-level node, chunk size 128


Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `chunk_sizes`  |  `List[int] | None`  |  The chunk sizes to use when splitting documents, in order of level.  |  `None`  |  
|  `node_parser_ids`  |  `List[str]`  |  List of ids for the node parsers to use when splitting documents, in order of level (first id used for first level, etc.).  |  `<dynamic>`  |  
|  `node_parser_map`  |  `Dict[str, NodeParser[](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/#llama_index.core.node_parser.interface.NodeParser "NodeParser \(llama_index.core.node_parser.interface.NodeParser\)")]`  |  Map of node parser id to node parser.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/node_parser/relational/hierarchical.py`  
| 
```
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
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
```
 | 
```
classHierarchicalNodeParser(NodeParser):
"""
    Hierarchical node parser.

    Splits a document into a recursive hierarchy Nodes using a NodeParser.

    NOTE: this will return a hierarchy of nodes in a flat list, where there will be
    overlap between parent nodes (e.g. with a bigger chunk size), and child nodes
    per parent (e.g. with a smaller chunk size).

    For instance, this may return a list of nodes like:

    - list of top-level nodes with chunk size 2048
    - list of second-level nodes, where each node is a child of a top-level node,
      chunk size 512
    - list of third-level nodes, where each node is a child of a second-level node,
      chunk size 128
    """

    chunk_sizes: Optional[List[int]] = Field(
        default=None,
        description=(
            "The chunk sizes to use when splitting documents, in order of level."
        ),
    )
    node_parser_ids: List[str] = Field(
        default_factory=list,
        description=(
            "List of ids for the node parsers to use when splitting documents, "
            + "in order of level (first id used for first level, etc.)."
        ),
    )
    node_parser_map: Dict[str, NodeParser] = Field(
        description="Map of node parser id to node parser.",
    )

    @classmethod
    deffrom_defaults(
        cls,
        chunk_sizes: Optional[List[int]] = None,
        chunk_overlap: int = 20,
        node_parser_ids: Optional[List[str]] = None,
        node_parser_map: Optional[Dict[str, NodeParser]] = None,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        callback_manager: Optional[CallbackManager] = None,
    ) -> "HierarchicalNodeParser":
        callback_manager = callback_manager or CallbackManager([])

        if node_parser_ids is None:
            if chunk_sizes is None:
                chunk_sizes = [2048, 512, 128]

            node_parser_ids = [f"chunk_size_{chunk_size}" for chunk_size in chunk_sizes]
            node_parser_map = {}
            for chunk_size, node_parser_id in zip(chunk_sizes, node_parser_ids):
                node_parser_map[node_parser_id] = SentenceSplitter(
                    chunk_size=chunk_size,
                    callback_manager=callback_manager,
                    chunk_overlap=chunk_overlap,
                    include_metadata=include_metadata,
                    include_prev_next_rel=include_prev_next_rel,
                )
        else:
            if chunk_sizes is not None:
                raise ValueError("Cannot specify both node_parser_ids and chunk_sizes.")
            if node_parser_map is None:
                raise ValueError(
                    "Must specify node_parser_map if using node_parser_ids."
                )

        return cls(
            chunk_sizes=chunk_sizes,
            node_parser_ids=node_parser_ids,
            node_parser_map=node_parser_map,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            callback_manager=callback_manager,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "HierarchicalNodeParser"

    def_recursively_get_nodes_from_nodes(
        self,
        nodes: List[BaseNode],
        level: int,
        show_progress: bool = False,
    ) -> List[BaseNode]:
"""Recursively get nodes from nodes."""
        if level >= len(self.node_parser_ids):
            raise ValueError(
                f"Level {level} is greater than number of text "
                f"splitters ({len(self.node_parser_ids)})."
            )

        # first split current nodes into sub-nodes
        nodes_with_progress = get_tqdm_iterable(
            nodes, show_progress, "Parsing documents into nodes"
        )
        sub_nodes = []
        for node in nodes_with_progress:
            cur_sub_nodes = self.node_parser_map[
                self.node_parser_ids[level]
            ].get_nodes_from_documents([node])
            # add parent relationship from sub node to parent node
            # add child relationship from parent node to sub node
            # NOTE: Only add relationships if level > 0, since we don't want to add
            # relationships for the top-level document objects that we are splitting
            if level  0:
                for sub_node in cur_sub_nodes:
                    _add_parent_child_relationship(
                        parent_node=node,
                        child_node=sub_node,
                    )

            sub_nodes.extend(cur_sub_nodes)

        # now for each sub-node, recursively split into sub-sub-nodes, and add
        if level  len(self.node_parser_ids) - 1:
            sub_sub_nodes = self._recursively_get_nodes_from_nodes(
                sub_nodes,
                level + 1,
                show_progress=show_progress,
            )
        else:
            sub_sub_nodes = []

        return sub_nodes + sub_sub_nodes

    defget_nodes_from_documents(
        self,
        documents: Sequence[Document],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""Parse document into nodes."""
        with self.callback_manager.event(
            CBEventType.NODE_PARSING, payload={EventPayload.DOCUMENTS: documents}
        ) as event:
            all_nodes: List[BaseNode] = []
            documents_with_progress = get_tqdm_iterable(
                documents, show_progress, "Parsing documents into nodes"
            )

            # TODO: a bit of a hack rn for tqdm
            for doc in documents_with_progress:
                nodes_from_doc = self._recursively_get_nodes_from_nodes([doc], 0)
                all_nodes.extend(nodes_from_doc)

            event.on_end(payload={EventPayload.NODES: all_nodes})

        return all_nodes

    # Unused abstract method
    def_parse_nodes(
        self, nodes: Sequence[BaseNode], show_progress: bool = False, **kwargs: Any
    ) -> List[BaseNode]:
        return list(nodes)

```
 |  
| --- | --- |  
###  get_nodes_from_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.HierarchicalNodeParser.get_nodes_from_documents "Permanent link")

```
get_nodes_from_documents(
    documents: Sequence[],
    show_progress:  = False,
    **kwargs: 
) -> []

```

Parse document into nodes.
Source code in `llama-index-core/llama_index/core/node_parser/relational/hierarchical.py`  
| 
```
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
```
 | 
```
defget_nodes_from_documents(
    self,
    documents: Sequence[Document],
    show_progress: bool = False,
    **kwargs: Any,
) -> List[BaseNode]:
"""Parse document into nodes."""
    with self.callback_manager.event(
        CBEventType.NODE_PARSING, payload={EventPayload.DOCUMENTS: documents}
    ) as event:
        all_nodes: List[BaseNode] = []
        documents_with_progress = get_tqdm_iterable(
            documents, show_progress, "Parsing documents into nodes"
        )

        # TODO: a bit of a hack rn for tqdm
        for doc in documents_with_progress:
            nodes_from_doc = self._recursively_get_nodes_from_nodes([doc], 0)
            all_nodes.extend(nodes_from_doc)

        event.on_end(payload={EventPayload.NODES: all_nodes})

    return all_nodes

```
 |  
| --- | --- |  
##  MarkdownElementNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.MarkdownElementNodeParser "Permanent link")
Bases: `BaseElementNodeParser`
Markdown element node parser.
Splits a markdown document into Text Nodes and Index Nodes corresponding to embedded objects (e.g. tables).
Source code in `llama-index-core/llama_index/core/node_parser/relational/markdown_element.py`  
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
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
```
 | 
```
classMarkdownElementNodeParser(BaseElementNodeParser):
"""
    Markdown element node parser.

    Splits a markdown document into Text Nodes and Index Nodes corresponding to embedded objects
    (e.g. tables).

    """

    @classmethod
    defclass_name(cls) -> str:
        return "MarkdownElementNodeParser"

    defget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
        elements = self.extract_elements(
            node.get_content(), table_filters=[self.filter_table], node_id=node.node_id
        )
        elements = self.extract_html_tables(elements)
        # extract summaries over table elements
        # Pass all elements so that extract_table_summaries can access
        # surrounding context (e.g., table titles) for better summarization
        self.extract_table_summaries(elements)
        # convert into nodes
        # will return a list of Nodes and Index Nodes
        nodes = self.get_nodes_from_elements(
            elements, node, ref_doc_text=node.get_content()
        )
        source_document = node.source_node or node.as_related_node_info()
        for n in nodes:
            n.relationships[NodeRelationship.SOURCE] = source_document
            n.metadata.update(node.metadata)
        return nodes

    async defaget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
        elements = self.extract_elements(
            node.get_content(), table_filters=[self.filter_table], node_id=node.node_id
        )
        # extract summaries over table elements
        # Pass all elements so that aextract_table_summaries can access
        # surrounding context (e.g., table titles) for better summarization
        await self.aextract_table_summaries(elements)
        # convert into nodes
        # will return a list of Nodes and Index Nodes
        nodes = self.get_nodes_from_elements(
            elements, node, ref_doc_text=node.get_content()
        )
        source_document = node.source_node or node.as_related_node_info()
        for n in nodes:
            n.relationships[NodeRelationship.SOURCE] = source_document
            n.metadata.update(node.metadata)
        return nodes

    defextract_html_tables(self, elements: List[Element]) -> List[Element]:
"""
        Extract html tables from text.

        Returns:
            List[Element]: text elements split by table_text element

        """
        new_elements = []
        for element in elements:
            if element.type != "text":
                # skip when it is not text
                new_elements.append(element)
                continue
            else:
                text = element.element
                last_pos = 0
                i = 0
                n = len(text)

                while i  n:
                    table_start = text.find("<table>", i)
                    if table_start == -1:
                        break

                    table_end = text.find("</table>", table_start)
                    if table_end - table_start <= 7:
                        # not a valid <table></table>
                        break

                    # extract text before the table
                    pre_text = text[last_pos:table_start].strip()
                    if pre_text:
                        new_elements.append(
                            Element(
                                id=f"{element.id}_{len(new_elements)}",
                                type="text",
                                element=pre_text,
                            )
                        )

                    # extract the html table
                    table_content = text[
                        table_start : table_end + 8
                    ]  # 8 is length of </table>
                    new_elements.append(
                        Element(
                            id=f"{element.id}_{len(new_elements)}",
                            type="table_text",
                            element=table_content,
                        )
                    )

                    last_pos = table_end + 8
                    i = last_pos

                # add the last piece of text
                final_text = text[last_pos:].strip()
                if final_text:
                    new_elements.append(
                        Element(
                            id=f"{element.id}_{len(new_elements)}",
                            type="text",
                            element=final_text,
                        )
                    )

        return new_elements

    defextract_elements(
        self,
        text: str,
        node_id: Optional[str] = None,
        table_filters: Optional[List[Callable]] = None,
        **kwargs: Any,
    ) -> List[Element]:
        # get node id for each node so that we can avoid using the same id for different nodes
"""Extract elements from text."""
        lines = text.split("\n")
        currentElement = None

        elements: List[Element] = []
        # Then parse the lines
        for line in lines:
            if line.startswith("```"):
                # check if this is the end of a code block
                if currentElement is not None and currentElement.type == "code":
                    elements.append(currentElement)
                    currentElement = None
                    # if there is some text after the ``` create a text element with it
                    if len(line)  3:
                        elements.append(
                            Element(
                                id=f"id_{len(elements)}",
                                type="text",
                                element=line.lstrip("```"),
                            )
                        )

                elif line.count("```") == 2 and line[-3] != "`":
                    # check if inline code block (aka have a second ``` in line but not at the end)
                    if currentElement is not None:
                        elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}",
                        type="code",
                        element=line.lstrip("```"),
                    )
                else:
                    # Start of a new code block
                    if currentElement is not None:
                        elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="code", element=""
                    )
            elif currentElement is not None and currentElement.type == "code":
                currentElement.element += "\n" + line

            elif line.startswith("|"):
                if currentElement is not None and currentElement.type != "table":
                    if currentElement is not None:
                        elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="table", element=line
                    )
                elif currentElement is not None:
                    currentElement.element += "\n" + line
                else:
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="table", element=line
                    )
            elif line.startswith("#"):
                if currentElement is not None:
                    elements.append(currentElement)
                currentElement = Element(
                    id=f"id_{len(elements)}",
                    type="title",
                    element=line.lstrip("#"),
                    title_level=len(line) - len(line.lstrip("#")),
                )
            else:
                if currentElement is not None and currentElement.type != "text":
                    elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="text", element=line
                    )
                elif currentElement is not None:
                    currentElement.element += "\n" + line
                else:
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="text", element=line
                    )
        if currentElement is not None:
            elements.append(currentElement)

        for idx, element in enumerate(elements):
            if element.type == "table":
                should_keep = True
                perfect_table = True

                # verify that the table (markdown) have the same number of columns on each rows
                table_lines = element.element.split("\n")
                table_columns = [len(line.split("|")) for line in table_lines]
                if len(set(table_columns))  1:
                    # if the table have different number of columns on each rows, it's not a perfect table
                    # we will store the raw text for such tables instead of converting them to a dataframe
                    perfect_table = False

                # verify that the table (markdown) have at least 2 rows
                if len(table_lines)  2:
                    should_keep = False

                # apply the table filter, now only filter empty tables
                if should_keep and perfect_table and table_filters is not None:
                    should_keep = all(tf(element) for tf in table_filters)

                # if the element is a table, convert it to a dataframe
                if should_keep:
                    if perfect_table:
                        table = md_to_df(element.element)

                        elements[idx] = Element(
                            id=f"id_{node_id}_{idx}" if node_id else f"id_{idx}",
                            type="table",
                            element=element.element,
                            table=table,
                        )
                    else:
                        # for non-perfect tables, we will store the raw text
                        # and give it a different type to differentiate it from perfect tables
                        elements[idx] = Element(
                            id=f"id_{node_id}_{idx}" if node_id else f"id_{idx}",
                            type="table_text",
                            element=element.element,
                            # table=table
                        )
                else:
                    elements[idx] = Element(
                        id=f"id_{node_id}_{idx}" if node_id else f"id_{idx}",
                        type="text",
                        element=element.element,
                    )
            else:
                # if the element is not a table, keep its original type
                elements[idx] = Element(
                    id=f"id_{node_id}_{idx}" if node_id else f"id_{idx}",
                    type=element.type,
                    element=element.element,
                )

        # merge consecutive text elements together for now
        merged_elements: List[Element] = []
        for element in elements:
            if (
                len(merged_elements)  0
                and element.type == "text"
                and merged_elements[-1].type == "text"
            ):
                merged_elements[-1].element += "\n" + element.element
            else:
                merged_elements.append(element)
        elements = merged_elements
        return merged_elements

    deffilter_table(self, table_element: Any) -> bool:
"""Filter tables."""
        table_df = md_to_df(table_element.element)

        # check if table_df is not None, has more than one row, and more than one column
        return table_df is not None and not table_df.empty and len(table_df.columns)  1

```
 |  
| --- | --- |  
###  get_nodes_from_node [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.MarkdownElementNodeParser.get_nodes_from_node "Permanent link")

```
get_nodes_from_node(node: ) -> []

```

Get nodes from node.
Source code in `llama-index-core/llama_index/core/node_parser/relational/markdown_element.py`  
| 
```
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
```
 | 
```
defget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
    elements = self.extract_elements(
        node.get_content(), table_filters=[self.filter_table], node_id=node.node_id
    )
    elements = self.extract_html_tables(elements)
    # extract summaries over table elements
    # Pass all elements so that extract_table_summaries can access
    # surrounding context (e.g., table titles) for better summarization
    self.extract_table_summaries(elements)
    # convert into nodes
    # will return a list of Nodes and Index Nodes
    nodes = self.get_nodes_from_elements(
        elements, node, ref_doc_text=node.get_content()
    )
    source_document = node.source_node or node.as_related_node_info()
    for n in nodes:
        n.relationships[NodeRelationship.SOURCE] = source_document
        n.metadata.update(node.metadata)
    return nodes

```
 |  
| --- | --- |  
###  aget_nodes_from_node [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.MarkdownElementNodeParser.aget_nodes_from_node "Permanent link")

```
aget_nodes_from_node(node: ) -> []

```

Get nodes from node.
Source code in `llama-index-core/llama_index/core/node_parser/relational/markdown_element.py`  
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
```
 | 
```
async defaget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
    elements = self.extract_elements(
        node.get_content(), table_filters=[self.filter_table], node_id=node.node_id
    )
    # extract summaries over table elements
    # Pass all elements so that aextract_table_summaries can access
    # surrounding context (e.g., table titles) for better summarization
    await self.aextract_table_summaries(elements)
    # convert into nodes
    # will return a list of Nodes and Index Nodes
    nodes = self.get_nodes_from_elements(
        elements, node, ref_doc_text=node.get_content()
    )
    source_document = node.source_node or node.as_related_node_info()
    for n in nodes:
        n.relationships[NodeRelationship.SOURCE] = source_document
        n.metadata.update(node.metadata)
    return nodes

```
 |  
| --- | --- |  
###  extract_html_tables [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.MarkdownElementNodeParser.extract_html_tables "Permanent link")

```
extract_html_tables(
    elements: [Element],
) -> [Element]

```

Extract html tables from text.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[Element]`  |  List[Element]: text elements split by table_text element  |  
Source code in `llama-index-core/llama_index/core/node_parser/relational/markdown_element.py`  
| 
```
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
```
 | 
```
defextract_html_tables(self, elements: List[Element]) -> List[Element]:
"""
    Extract html tables from text.

    Returns:
        List[Element]: text elements split by table_text element

    """
    new_elements = []
    for element in elements:
        if element.type != "text":
            # skip when it is not text
            new_elements.append(element)
            continue
        else:
            text = element.element
            last_pos = 0
            i = 0
            n = len(text)

            while i  n:
                table_start = text.find("<table>", i)
                if table_start == -1:
                    break

                table_end = text.find("</table>", table_start)
                if table_end - table_start <= 7:
                    # not a valid <table></table>
                    break

                # extract text before the table
                pre_text = text[last_pos:table_start].strip()
                if pre_text:
                    new_elements.append(
                        Element(
                            id=f"{element.id}_{len(new_elements)}",
                            type="text",
                            element=pre_text,
                        )
                    )

                # extract the html table
                table_content = text[
                    table_start : table_end + 8
                ]  # 8 is length of </table>
                new_elements.append(
                    Element(
                        id=f"{element.id}_{len(new_elements)}",
                        type="table_text",
                        element=table_content,
                    )
                )

                last_pos = table_end + 8
                i = last_pos

            # add the last piece of text
            final_text = text[last_pos:].strip()
            if final_text:
                new_elements.append(
                    Element(
                        id=f"{element.id}_{len(new_elements)}",
                        type="text",
                        element=final_text,
                    )
                )

    return new_elements

```
 |  
| --- | --- |  
###  extract_elements [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.MarkdownElementNodeParser.extract_elements "Permanent link")

```
extract_elements(
    text: ,
    node_id: Optional[] = None,
    table_filters: Optional[[Callable]] = None,
    **kwargs: 
) -> [Element]

```

Extract elements from text.
Source code in `llama-index-core/llama_index/core/node_parser/relational/markdown_element.py`  
| 
```
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
```
 | 
```
defextract_elements(
    self,
    text: str,
    node_id: Optional[str] = None,
    table_filters: Optional[List[Callable]] = None,
    **kwargs: Any,
) -> List[Element]:
    # get node id for each node so that we can avoid using the same id for different nodes
"""Extract elements from text."""
    lines = text.split("\n")
    currentElement = None

    elements: List[Element] = []
    # Then parse the lines
    for line in lines:
        if line.startswith("```"):
            # check if this is the end of a code block
            if currentElement is not None and currentElement.type == "code":
                elements.append(currentElement)
                currentElement = None
                # if there is some text after the ``` create a text element with it
                if len(line)  3:
                    elements.append(
                        Element(
                            id=f"id_{len(elements)}",
                            type="text",
                            element=line.lstrip("```"),
                        )
                    )

            elif line.count("```") == 2 and line[-3] != "`":
                # check if inline code block (aka have a second ``` in line but not at the end)
                if currentElement is not None:
                    elements.append(currentElement)
                currentElement = Element(
                    id=f"id_{len(elements)}",
                    type="code",
                    element=line.lstrip("```"),
                )
            else:
                # Start of a new code block
                if currentElement is not None:
                    elements.append(currentElement)
                currentElement = Element(
                    id=f"id_{len(elements)}", type="code", element=""
                )
        elif currentElement is not None and currentElement.type == "code":
            currentElement.element += "\n" + line

        elif line.startswith("|"):
            if currentElement is not None and currentElement.type != "table":
                if currentElement is not None:
                    elements.append(currentElement)
                currentElement = Element(
                    id=f"id_{len(elements)}", type="table", element=line
                )
            elif currentElement is not None:
                currentElement.element += "\n" + line
            else:
                currentElement = Element(
                    id=f"id_{len(elements)}", type="table", element=line
                )
        elif line.startswith("#"):
            if currentElement is not None:
                elements.append(currentElement)
            currentElement = Element(
                id=f"id_{len(elements)}",
                type="title",
                element=line.lstrip("#"),
                title_level=len(line) - len(line.lstrip("#")),
            )
        else:
            if currentElement is not None and currentElement.type != "text":
                elements.append(currentElement)
                currentElement = Element(
                    id=f"id_{len(elements)}", type="text", element=line
                )
            elif currentElement is not None:
                currentElement.element += "\n" + line
            else:
                currentElement = Element(
                    id=f"id_{len(elements)}", type="text", element=line
                )
    if currentElement is not None:
        elements.append(currentElement)

    for idx, element in enumerate(elements):
        if element.type == "table":
            should_keep = True
            perfect_table = True

            # verify that the table (markdown) have the same number of columns on each rows
            table_lines = element.element.split("\n")
            table_columns = [len(line.split("|")) for line in table_lines]
            if len(set(table_columns))  1:
                # if the table have different number of columns on each rows, it's not a perfect table
                # we will store the raw text for such tables instead of converting them to a dataframe
                perfect_table = False

            # verify that the table (markdown) have at least 2 rows
            if len(table_lines)  2:
                should_keep = False

            # apply the table filter, now only filter empty tables
            if should_keep and perfect_table and table_filters is not None:
                should_keep = all(tf(element) for tf in table_filters)

            # if the element is a table, convert it to a dataframe
            if should_keep:
                if perfect_table:
                    table = md_to_df(element.element)

                    elements[idx] = Element(
                        id=f"id_{node_id}_{idx}" if node_id else f"id_{idx}",
                        type="table",
                        element=element.element,
                        table=table,
                    )
                else:
                    # for non-perfect tables, we will store the raw text
                    # and give it a different type to differentiate it from perfect tables
                    elements[idx] = Element(
                        id=f"id_{node_id}_{idx}" if node_id else f"id_{idx}",
                        type="table_text",
                        element=element.element,
                        # table=table
                    )
            else:
                elements[idx] = Element(
                    id=f"id_{node_id}_{idx}" if node_id else f"id_{idx}",
                    type="text",
                    element=element.element,
                )
        else:
            # if the element is not a table, keep its original type
            elements[idx] = Element(
                id=f"id_{node_id}_{idx}" if node_id else f"id_{idx}",
                type=element.type,
                element=element.element,
            )

    # merge consecutive text elements together for now
    merged_elements: List[Element] = []
    for element in elements:
        if (
            len(merged_elements)  0
            and element.type == "text"
            and merged_elements[-1].type == "text"
        ):
            merged_elements[-1].element += "\n" + element.element
        else:
            merged_elements.append(element)
    elements = merged_elements
    return merged_elements

```
 |  
| --- | --- |  
###  filter_table [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.MarkdownElementNodeParser.filter_table "Permanent link")

```
filter_table(table_element: ) -> 

```

Filter tables.
Source code in `llama-index-core/llama_index/core/node_parser/relational/markdown_element.py`  
| 
```
289
290
291
292
293
294
```
 | 
```
deffilter_table(self, table_element: Any) -> bool:
"""Filter tables."""
    table_df = md_to_df(table_element.element)

    # check if table_df is not None, has more than one row, and more than one column
    return table_df is not None and not table_df.empty and len(table_df.columns)  1

```
 |  
| --- | --- |  
##  UnstructuredElementNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.UnstructuredElementNodeParser "Permanent link")
Bases: `BaseElementNodeParser`
Unstructured element node parser.
Splits a document into Text Nodes and Index Nodes corresponding to embedded objects (e.g. tables).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `partitioning_parameters`  |  `Dict[str, Any] | None`  |  Extra dictionary representing parameters of the partitioning process.  |  
Source code in `llama-index-core/llama_index/core/node_parser/relational/unstructured_element.py`  
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
137
138
139
140
141
142
143
```
 | 
```
classUnstructuredElementNodeParser(BaseElementNodeParser):
"""
    Unstructured element node parser.

    Splits a document into Text Nodes and Index Nodes corresponding to embedded objects
    (e.g. tables).

    """

    partitioning_parameters: Optional[Dict[str, Any]] = Field(
        default={},
        description="Extra dictionary representing parameters of the partitioning process.",
    )

    def__init__(
        self,
        callback_manager: Optional[CallbackManager] = None,
        llm: Optional[Any] = None,
        summary_query_str: str = DEFAULT_SUMMARY_QUERY_STR,
        partitioning_parameters: Optional[Dict[str, Any]] = {},
    ) -> None:
"""Initialize."""
        try:
            importlxml  # noqa  # pants: no-infer-dep
            importunstructured  # noqa  # pants: no-infer-dep
        except ImportError:
            raise ImportError(
                "You must install the `unstructured` and `lxml` "
                "package to use this node parser."
            )
        callback_manager = callback_manager or CallbackManager([])

        return super().__init__(
            callback_manager=callback_manager,
            llm=llm,
            summary_query_str=summary_query_str,
            partitioning_parameters=partitioning_parameters,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "UnstructuredElementNodeParser"

    defget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
        elements = self.extract_elements(
            node.get_content(), table_filters=[self.filter_table]
        )
        # extract summaries over table elements
        # Pass all elements so that extract_table_summaries can access
        # surrounding context (e.g., table titles) for better summarization
        self.extract_table_summaries(elements)
        # convert into nodes
        # will return a list of Nodes and Index Nodes
        nodes = self.get_nodes_from_elements(
            elements, node, ref_doc_text=node.get_content()
        )

        source_document = node.source_node or node.as_related_node_info()
        for n in nodes:
            n.relationships[NodeRelationship.SOURCE] = source_document
            n.metadata.update(node.metadata)
        return nodes

    async defaget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
        elements = self.extract_elements(
            node.get_content(), table_filters=[self.filter_table]
        )
        # extract summaries over table elements
        # Pass all elements so that extract_table_summaries can access
        # surrounding context (e.g., table titles) for better summarization
        await self.aextract_table_summaries(elements)
        # convert into nodes
        # will return a list of Nodes and Index Nodes
        nodes = self.get_nodes_from_elements(
            elements, node, ref_doc_text=node.get_content()
        )

        source_document = node.source_node or node.as_related_node_info()
        for n in nodes:
            n.relationships[NodeRelationship.SOURCE] = source_document
            n.metadata.update(node.metadata)
        return nodes

    defextract_elements(
        self, text: str, table_filters: Optional[List[Callable]] = None, **kwargs: Any
    ) -> List[Element]:
"""Extract elements from text."""
        fromunstructured.partition.htmlimport partition_html  # pants: no-infer-dep

        table_filters = table_filters or []
        partitioning_parameters = self.partitioning_parameters or {}
        elements = partition_html(text=text, **partitioning_parameters)
        output_els = []
        for idx, element in enumerate(elements):
            if "unstructured.documents.elements.Table" in str(type(element)):
                should_keep = all(tf(element) for tf in table_filters)
                if should_keep:
                    table_df = html_to_df(str(element.metadata.text_as_html))
                    output_els.append(
                        Element(
                            id=f"id_{idx}",
                            type="table",
                            element=element,
                            table=table_df,
                        )
                    )
                else:
                    # if not a table, keep it as Text as we don't want to lose context
                    fromunstructured.documents.elementsimport Text

                    new_element = Text(str(element))
                    output_els.append(
                        Element(id=f"id_{idx}", type="text", element=new_element)
                    )
            else:
                output_els.append(Element(id=f"id_{idx}", type="text", element=element))
        return output_els

    deffilter_table(self, table_element: Any) -> bool:
"""Filter tables."""
        table_df = html_to_df(table_element.metadata.text_as_html)

        # check if table_df is not None, has more than one row, and more than one column
        return table_df is not None and not table_df.empty and len(table_df.columns)  1

```
 |  
| --- | --- |  
###  get_nodes_from_node [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.UnstructuredElementNodeParser.get_nodes_from_node "Permanent link")

```
get_nodes_from_node(node: ) -> []

```

Get nodes from node.
Source code in `llama-index-core/llama_index/core/node_parser/relational/unstructured_element.py`  
| 
```
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
```
 | 
```
defget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
    elements = self.extract_elements(
        node.get_content(), table_filters=[self.filter_table]
    )
    # extract summaries over table elements
    # Pass all elements so that extract_table_summaries can access
    # surrounding context (e.g., table titles) for better summarization
    self.extract_table_summaries(elements)
    # convert into nodes
    # will return a list of Nodes and Index Nodes
    nodes = self.get_nodes_from_elements(
        elements, node, ref_doc_text=node.get_content()
    )

    source_document = node.source_node or node.as_related_node_info()
    for n in nodes:
        n.relationships[NodeRelationship.SOURCE] = source_document
        n.metadata.update(node.metadata)
    return nodes

```
 |  
| --- | --- |  
###  aget_nodes_from_node [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.UnstructuredElementNodeParser.aget_nodes_from_node "Permanent link")

```
aget_nodes_from_node(node: ) -> []

```

Get nodes from node.
Source code in `llama-index-core/llama_index/core/node_parser/relational/unstructured_element.py`  
| 
```
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
```
 | 
```
async defaget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
    elements = self.extract_elements(
        node.get_content(), table_filters=[self.filter_table]
    )
    # extract summaries over table elements
    # Pass all elements so that extract_table_summaries can access
    # surrounding context (e.g., table titles) for better summarization
    await self.aextract_table_summaries(elements)
    # convert into nodes
    # will return a list of Nodes and Index Nodes
    nodes = self.get_nodes_from_elements(
        elements, node, ref_doc_text=node.get_content()
    )

    source_document = node.source_node or node.as_related_node_info()
    for n in nodes:
        n.relationships[NodeRelationship.SOURCE] = source_document
        n.metadata.update(node.metadata)
    return nodes

```
 |  
| --- | --- |  
###  extract_elements [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.UnstructuredElementNodeParser.extract_elements "Permanent link")

```
extract_elements(
    text: ,
    table_filters: Optional[[Callable]] = None,
    **kwargs: 
) -> [Element]

```

Extract elements from text.
Source code in `llama-index-core/llama_index/core/node_parser/relational/unstructured_element.py`  
| 
```
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
defextract_elements(
    self, text: str, table_filters: Optional[List[Callable]] = None, **kwargs: Any
) -> List[Element]:
"""Extract elements from text."""
    fromunstructured.partition.htmlimport partition_html  # pants: no-infer-dep

    table_filters = table_filters or []
    partitioning_parameters = self.partitioning_parameters or {}
    elements = partition_html(text=text, **partitioning_parameters)
    output_els = []
    for idx, element in enumerate(elements):
        if "unstructured.documents.elements.Table" in str(type(element)):
            should_keep = all(tf(element) for tf in table_filters)
            if should_keep:
                table_df = html_to_df(str(element.metadata.text_as_html))
                output_els.append(
                    Element(
                        id=f"id_{idx}",
                        type="table",
                        element=element,
                        table=table_df,
                    )
                )
            else:
                # if not a table, keep it as Text as we don't want to lose context
                fromunstructured.documents.elementsimport Text

                new_element = Text(str(element))
                output_els.append(
                    Element(id=f"id_{idx}", type="text", element=new_element)
                )
        else:
            output_els.append(Element(id=f"id_{idx}", type="text", element=element))
    return output_els

```
 |  
| --- | --- |  
###  filter_table [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.UnstructuredElementNodeParser.filter_table "Permanent link")

```
filter_table(table_element: ) -> 

```

Filter tables.
Source code in `llama-index-core/llama_index/core/node_parser/relational/unstructured_element.py`  
| 
```
138
139
140
141
142
143
```
 | 
```
deffilter_table(self, table_element: Any) -> bool:
"""Filter tables."""
    table_df = html_to_df(table_element.metadata.text_as_html)

    # check if table_df is not None, has more than one row, and more than one column
    return table_df is not None and not table_df.empty and len(table_df.columns)  1

```
 |  
| --- | --- |  
##  LlamaParseJsonNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.LlamaParseJsonNodeParser "Permanent link")
Bases: `BaseElementNodeParser`
Llama Parse Json format element node parser.
Splits a json format document from LlamaParse into Text Nodes and Index Nodes corresponding to embedded objects (e.g. tables).
Source code in `llama-index-core/llama_index/core/node_parser/relational/llama_parse_json_element.py`  
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
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
```
 | 
```
classLlamaParseJsonNodeParser(BaseElementNodeParser):
"""
    Llama Parse Json format element node parser.

    Splits a json format document from LlamaParse into Text Nodes and Index Nodes
    corresponding to embedded objects (e.g. tables).

    """

    @classmethod
    defclass_name(cls) -> str:
        return "LlamaParseJsonNodeParser"

    defget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
        elements = self.extract_elements(
            node.get_content(),
            table_filters=[self.filter_table],
            node_id=node.id_,
            node_metadata=node.metadata,
        )
        # extract summaries over table elements
        # Pass all elements so that extract_table_summaries can access
        # surrounding context (e.g., table titles) for better summarization
        self.extract_table_summaries(elements)
        # convert into nodes
        # will return a list of Nodes and Index Nodes
        return self.get_nodes_from_elements(
            elements, node, ref_doc_text=node.get_content()
        )

    async defaget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
        elements = self.extract_elements(
            node.get_content(),
            table_filters=[self.filter_table],
            node_id=node.id_,
            node_metadata=node.metadata,
        )
        # extract summaries over table elements
        # Pass all elements so that extract_table_summaries can access
        # surrounding context (e.g., table titles) for better summarization
        await self.aextract_table_summaries(elements)
        # convert into nodes
        # will return a list of Nodes and Index Nodes
        return self.get_nodes_from_elements(
            elements, node, ref_doc_text=node.get_content()
        )

    defextract_elements(
        self,
        text: str,
        mode: Optional[str] = "json",
        node_id: Optional[str] = None,
        node_metadata: Optional[Dict[str, Any]] = None,
        table_filters: Optional[List[Callable]] = None,
        **kwargs: Any,
    ) -> List[Element]:
        # get node id for each node so that we can avoid using the same id for different nodes
"""
        Extract elements from json based nodes.

        Args:
            text: node's text content
            mode: different modes for returning different types of elements based on the selected mode
            node_id: unique id for the node
            node_metadata: metadata for the node. the json output for the nodes contains a lot of fields for elements

        """
        elements: List[Element] = []
        currentElement = None
        page_number = node_metadata.get("page") if node_metadata is not None else 0

        if mode == "json" and node_metadata is not None:
            json_items = node_metadata.get("items") or []
            for element_idx, json_item in enumerate(json_items):
                ele_type = json_item.get("type")
                if ele_type == "heading":
                    elements.append(
                        Element(
                            id=f"id_page_{page_number}_heading_{element_idx}",
                            type="heading",
                            title_level=json_item.get("lvl"),
                            element=json_item.get("value"),
                            markdown=json_item.get("md"),
                            page_number=page_number,
                        )
                    )
                elif ele_type == "text":
                    elements.append(
                        Element(
                            id=f"id_page_{page_number}_text_{element_idx}",
                            type="text",
                            element=json_item.get("value"),
                            markdown=json_item.get("md"),
                            page_number=page_number,
                        )
                    )
                elif ele_type == "table":
                    elements.append(
                        Element(
                            id=f"id_page_{page_number}_table_{element_idx}",
                            type="table",
                            element=json_item.get("rows"),
                            markdown=json_item.get("md"),
                            page_number=page_number,
                        )
                    )
        elif mode == "images" and node_metadata is not None:
            # only get images from json metadata
            images = node_metadata.get("images") or []
            for idx, image in enumerate(images):
                elements.append(
                    Element(
                        id=f"id_page_{page_number}_image_{idx}",
                        type="image",
                        element=image,
                    )
                )
        else:
            lines = text.split("\n")
            # Then parse the lines from raw text of json
            for line in lines:
                if line.startswith("```"):
                    # check if this is the end of a code block
                    if currentElement is not None and currentElement.type == "code":
                        elements.append(currentElement)
                        currentElement = None
                        # if there is some text after the ``` create a text element with it
                        if len(line)  3:
                            elements.append(
                                Element(
                                    id=f"id_{len(elements)}",
                                    type="text",
                                    element=line.lstrip("```"),
                                )
                            )

                    elif line.count("```") == 2 and line[-3] != "`":
                        # check if inline code block (aka have a second ``` in line but not at the end)
                        if currentElement is not None:
                            elements.append(currentElement)
                        currentElement = Element(
                            id=f"id_{len(elements)}",
                            type="code",
                            element=line.lstrip("```"),
                        )
                    elif currentElement is not None and currentElement.type == "text":
                        currentElement.element += "\n" + line
                    else:
                        if currentElement is not None:
                            elements.append(currentElement)
                        currentElement = Element(
                            id=f"id_{len(elements)}", type="text", element=line
                        )

                elif currentElement is not None and currentElement.type == "code":
                    currentElement.element += "\n" + line

                elif line.startswith("|"):
                    if currentElement is not None and currentElement.type != "table":
                        if currentElement is not None:
                            elements.append(currentElement)
                        currentElement = Element(
                            id=f"id_{len(elements)}", type="table", element=line
                        )
                    elif currentElement is not None:
                        currentElement.element += "\n" + line
                    else:
                        currentElement = Element(
                            id=f"id_{len(elements)}", type="table", element=line
                        )
                elif line.startswith("#"):
                    if currentElement is not None:
                        elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}",
                        type="title",
                        element=line.lstrip("#"),
                        title_level=len(line) - len(line.lstrip("#")),
                    )
                else:
                    if currentElement is not None and currentElement.type != "text":
                        elements.append(currentElement)
                        currentElement = Element(
                            id=f"id_{len(elements)}", type="text", element=line
                        )
                    elif currentElement is not None:
                        currentElement.element += "\n" + line
                    else:
                        currentElement = Element(
                            id=f"id_{len(elements)}", type="text", element=line
                        )
        if currentElement is not None:
            elements.append(currentElement)

        for idx, element in enumerate(elements):
            if element.type == "table":
                assert element.markdown is not None

                should_keep = True
                perfect_table = True

                # verify that the table (markdown) have the same number of columns on each rows
                table_lines = element.markdown.split("\n")
                table_columns = [len(line.split("|")) for line in table_lines]
                if len(set(table_columns))  1:
                    # if the table have different number of columns on each rows, it's not a perfect table
                    # we will store the raw text for such tables instead of converting them to a dataframe
                    perfect_table = False

                # verify that the table (markdown) have at least 2 rows
                if len(table_lines)  2:
                    should_keep = False

                # apply the table filter, now only filter empty tables
                if should_keep and perfect_table and table_filters is not None:
                    should_keep = all(tf(element) for tf in table_filters)

                # if the element is a table, convert it to a dataframe
                if should_keep:
                    if perfect_table:
                        assert element.markdown is not None
                        table = md_to_df(element.markdown)

                        elements[idx] = Element(
                            id=(
                                f"id_page_{page_number}_{node_id}_{idx}"
                                if node_id
                                else f"id_{idx}"
                            ),
                            type="table",
                            element=element,
                            table=table,
                        )
                    else:
                        # for non-perfect tables, we will store the raw text
                        # and give it a different type to differentiate it from perfect tables
                        elements[idx] = Element(
                            id=(
                                f"id_page_{page_number}_{node_id}_{idx}"
                                if node_id
                                else f"id_{idx}"
                            ),
                            type="table_text",
                            element=element.element,
                            # table=table
                        )
                else:
                    elements[idx] = Element(
                        id=(
                            f"id_page_{page_number}_{node_id}_{idx}"
                            if node_id
                            else f"id_page_{page_number}_{idx}"
                        ),
                        type="text",
                        element=element.element,
                    )
            else:
                # if the element is not a table, keep it as to text
                elements[idx] = Element(
                    id=(
                        f"id_page_{page_number}_{node_id}_{idx}"
                        if node_id
                        else f"id_page_{page_number}_{idx}"
                    ),
                    type="text",
                    element=element.element,
                )

        # merge consecutive text elements together for now
        merged_elements: List[Element] = []
        for element in elements:
            if (
                len(merged_elements)  0
                and element.type == "text"
                and merged_elements[-1].type == "text"
            ):
                if isinstance(element.element, list):
                    merged_elements[-1].element += "\n" + " ".join(
                        str(e) for e in element.element
                    )
                else:
                    merged_elements[-1].element += "\n" + element.element
            else:
                merged_elements.append(element)
        elements = merged_elements
        return merged_elements

    deffilter_table(self, table_element: Any) -> bool:
"""Filter tables."""
        # convert markdown of the table to df
        table_df = md_to_df(table_element.markdown)

        # check if table_df is not None, has more than one row, and more than one column
        return table_df is not None and not table_df.empty and len(table_df.columns)  1

```
 |  
| --- | --- |  
###  get_nodes_from_node [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.LlamaParseJsonNodeParser.get_nodes_from_node "Permanent link")

```
get_nodes_from_node(node: ) -> []

```

Get nodes from node.
Source code in `llama-index-core/llama_index/core/node_parser/relational/llama_parse_json_element.py`  
| 
```
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
defget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
    elements = self.extract_elements(
        node.get_content(),
        table_filters=[self.filter_table],
        node_id=node.id_,
        node_metadata=node.metadata,
    )
    # extract summaries over table elements
    # Pass all elements so that extract_table_summaries can access
    # surrounding context (e.g., table titles) for better summarization
    self.extract_table_summaries(elements)
    # convert into nodes
    # will return a list of Nodes and Index Nodes
    return self.get_nodes_from_elements(
        elements, node, ref_doc_text=node.get_content()
    )

```
 |  
| --- | --- |  
###  aget_nodes_from_node [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.LlamaParseJsonNodeParser.aget_nodes_from_node "Permanent link")

```
aget_nodes_from_node(node: ) -> []

```

Get nodes from node.
Source code in `llama-index-core/llama_index/core/node_parser/relational/llama_parse_json_element.py`  
| 
```
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
```
 | 
```
async defaget_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
"""Get nodes from node."""
    elements = self.extract_elements(
        node.get_content(),
        table_filters=[self.filter_table],
        node_id=node.id_,
        node_metadata=node.metadata,
    )
    # extract summaries over table elements
    # Pass all elements so that extract_table_summaries can access
    # surrounding context (e.g., table titles) for better summarization
    await self.aextract_table_summaries(elements)
    # convert into nodes
    # will return a list of Nodes and Index Nodes
    return self.get_nodes_from_elements(
        elements, node, ref_doc_text=node.get_content()
    )

```
 |  
| --- | --- |  
###  extract_elements [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.LlamaParseJsonNodeParser.extract_elements "Permanent link")

```
extract_elements(
    text: ,
    mode: Optional[] = "json",
    node_id: Optional[] = None,
    node_metadata: Optional[[, ]] = None,
    table_filters: Optional[[Callable]] = None,
    **kwargs: 
) -> [Element]

```

Extract elements from json based nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `text`  |  node's text content  |  _required_  |  
|  `mode`  |  `Optional[str]`  |  different modes for returning different types of elements based on the selected mode  |  `'json'`  |  
|  `node_id`  |  `Optional[str]`  |  unique id for the node  |  `None`  |  
|  `node_metadata`  |  `Optional[Dict[str, Any]]`  |  metadata for the node. the json output for the nodes contains a lot of fields for elements  |  `None`  |  
Source code in `llama-index-core/llama_index/core/node_parser/relational/llama_parse_json_element.py`  
| 
```
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
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
```
 | 
```
defextract_elements(
    self,
    text: str,
    mode: Optional[str] = "json",
    node_id: Optional[str] = None,
    node_metadata: Optional[Dict[str, Any]] = None,
    table_filters: Optional[List[Callable]] = None,
    **kwargs: Any,
) -> List[Element]:
    # get node id for each node so that we can avoid using the same id for different nodes
"""
    Extract elements from json based nodes.

    Args:
        text: node's text content
        mode: different modes for returning different types of elements based on the selected mode
        node_id: unique id for the node
        node_metadata: metadata for the node. the json output for the nodes contains a lot of fields for elements

    """
    elements: List[Element] = []
    currentElement = None
    page_number = node_metadata.get("page") if node_metadata is not None else 0

    if mode == "json" and node_metadata is not None:
        json_items = node_metadata.get("items") or []
        for element_idx, json_item in enumerate(json_items):
            ele_type = json_item.get("type")
            if ele_type == "heading":
                elements.append(
                    Element(
                        id=f"id_page_{page_number}_heading_{element_idx}",
                        type="heading",
                        title_level=json_item.get("lvl"),
                        element=json_item.get("value"),
                        markdown=json_item.get("md"),
                        page_number=page_number,
                    )
                )
            elif ele_type == "text":
                elements.append(
                    Element(
                        id=f"id_page_{page_number}_text_{element_idx}",
                        type="text",
                        element=json_item.get("value"),
                        markdown=json_item.get("md"),
                        page_number=page_number,
                    )
                )
            elif ele_type == "table":
                elements.append(
                    Element(
                        id=f"id_page_{page_number}_table_{element_idx}",
                        type="table",
                        element=json_item.get("rows"),
                        markdown=json_item.get("md"),
                        page_number=page_number,
                    )
                )
    elif mode == "images" and node_metadata is not None:
        # only get images from json metadata
        images = node_metadata.get("images") or []
        for idx, image in enumerate(images):
            elements.append(
                Element(
                    id=f"id_page_{page_number}_image_{idx}",
                    type="image",
                    element=image,
                )
            )
    else:
        lines = text.split("\n")
        # Then parse the lines from raw text of json
        for line in lines:
            if line.startswith("```"):
                # check if this is the end of a code block
                if currentElement is not None and currentElement.type == "code":
                    elements.append(currentElement)
                    currentElement = None
                    # if there is some text after the ``` create a text element with it
                    if len(line)  3:
                        elements.append(
                            Element(
                                id=f"id_{len(elements)}",
                                type="text",
                                element=line.lstrip("```"),
                            )
                        )

                elif line.count("```") == 2 and line[-3] != "`":
                    # check if inline code block (aka have a second ``` in line but not at the end)
                    if currentElement is not None:
                        elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}",
                        type="code",
                        element=line.lstrip("```"),
                    )
                elif currentElement is not None and currentElement.type == "text":
                    currentElement.element += "\n" + line
                else:
                    if currentElement is not None:
                        elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="text", element=line
                    )

            elif currentElement is not None and currentElement.type == "code":
                currentElement.element += "\n" + line

            elif line.startswith("|"):
                if currentElement is not None and currentElement.type != "table":
                    if currentElement is not None:
                        elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="table", element=line
                    )
                elif currentElement is not None:
                    currentElement.element += "\n" + line
                else:
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="table", element=line
                    )
            elif line.startswith("#"):
                if currentElement is not None:
                    elements.append(currentElement)
                currentElement = Element(
                    id=f"id_{len(elements)}",
                    type="title",
                    element=line.lstrip("#"),
                    title_level=len(line) - len(line.lstrip("#")),
                )
            else:
                if currentElement is not None and currentElement.type != "text":
                    elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="text", element=line
                    )
                elif currentElement is not None:
                    currentElement.element += "\n" + line
                else:
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="text", element=line
                    )
    if currentElement is not None:
        elements.append(currentElement)

    for idx, element in enumerate(elements):
        if element.type == "table":
            assert element.markdown is not None

            should_keep = True
            perfect_table = True

            # verify that the table (markdown) have the same number of columns on each rows
            table_lines = element.markdown.split("\n")
            table_columns = [len(line.split("|")) for line in table_lines]
            if len(set(table_columns))  1:
                # if the table have different number of columns on each rows, it's not a perfect table
                # we will store the raw text for such tables instead of converting them to a dataframe
                perfect_table = False

            # verify that the table (markdown) have at least 2 rows
            if len(table_lines)  2:
                should_keep = False

            # apply the table filter, now only filter empty tables
            if should_keep and perfect_table and table_filters is not None:
                should_keep = all(tf(element) for tf in table_filters)

            # if the element is a table, convert it to a dataframe
            if should_keep:
                if perfect_table:
                    assert element.markdown is not None
                    table = md_to_df(element.markdown)

                    elements[idx] = Element(
                        id=(
                            f"id_page_{page_number}_{node_id}_{idx}"
                            if node_id
                            else f"id_{idx}"
                        ),
                        type="table",
                        element=element,
                        table=table,
                    )
                else:
                    # for non-perfect tables, we will store the raw text
                    # and give it a different type to differentiate it from perfect tables
                    elements[idx] = Element(
                        id=(
                            f"id_page_{page_number}_{node_id}_{idx}"
                            if node_id
                            else f"id_{idx}"
                        ),
                        type="table_text",
                        element=element.element,
                        # table=table
                    )
            else:
                elements[idx] = Element(
                    id=(
                        f"id_page_{page_number}_{node_id}_{idx}"
                        if node_id
                        else f"id_page_{page_number}_{idx}"
                    ),
                    type="text",
                    element=element.element,
                )
        else:
            # if the element is not a table, keep it as to text
            elements[idx] = Element(
                id=(
                    f"id_page_{page_number}_{node_id}_{idx}"
                    if node_id
                    else f"id_page_{page_number}_{idx}"
                ),
                type="text",
                element=element.element,
            )

    # merge consecutive text elements together for now
    merged_elements: List[Element] = []
    for element in elements:
        if (
            len(merged_elements)  0
            and element.type == "text"
            and merged_elements[-1].type == "text"
        ):
            if isinstance(element.element, list):
                merged_elements[-1].element += "\n" + " ".join(
                    str(e) for e in element.element
                )
            else:
                merged_elements[-1].element += "\n" + element.element
        else:
            merged_elements.append(element)
    elements = merged_elements
    return merged_elements

```
 |  
| --- | --- |  
###  filter_table [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.LlamaParseJsonNodeParser.filter_table "Permanent link")

```
filter_table(table_element: ) -> 

```

Filter tables.
Source code in `llama-index-core/llama_index/core/node_parser/relational/llama_parse_json_element.py`  
| 
```
300
301
302
303
304
305
306
```
 | 
```
deffilter_table(self, table_element: Any) -> bool:
"""Filter tables."""
    # convert markdown of the table to df
    table_df = md_to_df(table_element.markdown)

    # check if table_df is not None, has more than one row, and more than one column
    return table_df is not None and not table_df.empty and len(table_df.columns)  1

```
 |  
| --- | --- |  
##  CodeSplitter [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.CodeSplitter "Permanent link")
Bases: 
Split code using a AST parser.
Thank you to Kevin Lu / SweepAI for suggesting this elegant code splitting solution. https://docs.sweep.dev/blogs/chunking-2m-files
Supports both character-based and token-based chunking modes for more precise control over chunk sizes when working with language models.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `language`  |  The programming language of the code being split.  |  _required_  |  
|  `chunk_lines`  |  The number of lines to include in each chunk.  |  
|  `chunk_lines_overlap`  |  How many lines of code each chunk overlaps with.  |  
|  `max_chars`  |  Maximum number of characters per chunk.  |  `1500`  |  
|  `count_mode`  |  `Literal['token', 'char']`  |  Mode for counting chunk size: 'char' for characters, 'token' for tokens.  |  `'char'`  |  
|  `max_tokens`  |  Maximum number of tokens per chunk (used when count_mode='token').  |  `512`  |  
Source code in `llama-index-core/llama_index/core/node_parser/text/code.py`  
| 
```
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
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
```
 | 
```
classCodeSplitter(TextSplitter):
"""
    Split code using a AST parser.

    Thank you to Kevin Lu / SweepAI for suggesting this elegant code splitting solution.
    https://docs.sweep.dev/blogs/chunking-2m-files

    Supports both character-based and token-based chunking modes for more precise
    control over chunk sizes when working with language models.
    """

    language: str = Field(
        description="The programming language of the code being split."
    )
    chunk_lines: int = Field(
        default=DEFAULT_CHUNK_LINES,
        description="The number of lines to include in each chunk.",
        gt=0,
    )
    chunk_lines_overlap: int = Field(
        default=DEFAULT_LINES_OVERLAP,
        description="How many lines of code each chunk overlaps with.",
        gt=0,
    )
    max_chars: int = Field(
        default=DEFAULT_MAX_CHARS,
        description="Maximum number of characters per chunk.",
        gt=0,
    )
    count_mode: Literal["token", "char"] = Field(
        default="char",
        description="Mode for counting chunk size: 'char' for characters, 'token' for tokens.",
    )
    max_tokens: int = Field(
        default=DEFAULT_MAX_TOKENS,
        description="Maximum number of tokens per chunk (used when count_mode='token').",
        gt=0,
    )
    _parser: Any = PrivateAttr()
    _tokenizer: Callable = PrivateAttr()

    def__init__(
        self,
        language: str,
        chunk_lines: int = DEFAULT_CHUNK_LINES,
        chunk_lines_overlap: int = DEFAULT_LINES_OVERLAP,
        max_chars: int = DEFAULT_MAX_CHARS,
        count_mode: Literal["token", "char"] = "char",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        tokenizer: Optional[Callable] = None,
        parser: Any = None,
        callback_manager: Optional[CallbackManager] = None,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        id_func: Optional[Callable[[int, Document], str]] = None,
    ) -> None:
"""
        Initialize a CodeSplitter.

        Args:
            language: The programming language of the code being split.
            chunk_lines: The number of lines to include in each chunk.
            chunk_lines_overlap: How many lines of code each chunk overlaps with.
            max_chars: Maximum number of characters per chunk.
            count_mode: Mode for counting chunk size: 'char' for characters, 'token' for tokens.
            max_tokens: Maximum number of tokens per chunk (used when count_mode='token').
            tokenizer: Optional tokenizer function for token-based counting.
            parser: Optional tree-sitter Parser object.
            callback_manager: Optional callback manager.
            include_metadata: Whether to include metadata in chunks.
            include_prev_next_rel: Whether to include previous/next relationships.
            id_func: Optional function to generate chunk IDs.

        """
        fromtree_sitterimport Parser  # pants: no-infer-dep

        callback_manager = callback_manager or CallbackManager([])
        id_func = id_func or default_id_func

        super().__init__(
            language=language,
            chunk_lines=chunk_lines,
            chunk_lines_overlap=chunk_lines_overlap,
            max_chars=max_chars,
            count_mode=count_mode,
            max_tokens=max_tokens,
            callback_manager=callback_manager,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            id_func=id_func,
        )

        # Initialize tokenizer if using token mode
        self._tokenizer = tokenizer or get_tokenizer()

        if parser is None:
            try:
                importtree_sitter_language_pack  # pants: no-infer-dep

                parser = tree_sitter_language_pack.get_parser(language)  # type: ignore
            except ImportError:
                raise ImportError(
                    "Please install tree_sitter_language_pack to use CodeSplitter."
                    "Or pass in a parser object."
                )
            except Exception:
                print(
                    f"Could not get parser for language {language}. Check "
                    "https://github.com/Goldziher/tree-sitter-language-pack?tab=readme-ov-file#available-languages "
                    "for a list of valid languages."
                )
                raise
        if not isinstance(parser, Parser):
            raise ValueError("Parser must be a tree-sitter Parser object.")

        self._parser = parser

    @classmethod
    deffrom_defaults(
        cls,
        language: str,
        chunk_lines: int = DEFAULT_CHUNK_LINES,
        chunk_lines_overlap: int = DEFAULT_LINES_OVERLAP,
        max_chars: int = DEFAULT_MAX_CHARS,
        count_mode: Literal["token", "char"] = "char",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        tokenizer: Optional[Callable] = None,
        callback_manager: Optional[CallbackManager] = None,
        parser: Any = None,
    ) -> "CodeSplitter":
"""Create a CodeSplitter with default values."""
        return cls(
            language=language,
            chunk_lines=chunk_lines,
            chunk_lines_overlap=chunk_lines_overlap,
            max_chars=max_chars,
            count_mode=count_mode,
            max_tokens=max_tokens,
            tokenizer=tokenizer,
            callback_manager=callback_manager,
            parser=parser,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "CodeSplitter"

    def_chunk_node(self, node: Any, text_bytes: bytes, last_end: int = 0) -> List[str]:
"""
        Recursively chunk a node into smaller pieces based on character or token limits.

        Args:
            node (Any): The AST node to chunk.
            text_bytes (bytes): The original source code text as bytes.
            last_end (int, optional): The ending position of the last processed chunk. Defaults to 0.

        Returns:
            List[str]: A list of code chunks that respect the size limits.

        """
        new_chunks = []
        current_chunk = ""
        max_size = self.max_chars if self.count_mode == "char" else self.max_tokens

        for child in node.children:
            child_text = text_bytes[child.start_byte : child.end_byte].decode("utf-8")
            child_size = (
                len(child_text)
                if self.count_mode == "char"
                else len(self._tokenizer(child_text))
            )

            if child_size  max_size:
                # Child is too big, recursively chunk the child
                if len(current_chunk)  0:
                    new_chunks.append(current_chunk)
                current_chunk = ""
                new_chunks.extend(self._chunk_node(child, text_bytes, last_end))
            else:
                # Calculate what adding this child would do to current chunk size
                new_chunk_text = current_chunk + text_bytes[
                    last_end : child.end_byte
                ].decode("utf-8")
                new_chunk_size = (
                    len(new_chunk_text)
                    if self.count_mode == "char"
                    else len(self._tokenizer(new_chunk_text))
                )

                if new_chunk_size  max_size:
                    # Child would make the current chunk too big, so start a new chunk
                    if len(current_chunk)  0:
                        new_chunks.append(current_chunk)
                    current_chunk = text_bytes[last_end : child.end_byte].decode(
                        "utf-8"
                    )
                else:
                    current_chunk += text_bytes[last_end : child.end_byte].decode(
                        "utf-8"
                    )
            last_end = child.end_byte

        if len(current_chunk)  0:
            new_chunks.append(current_chunk)
        return new_chunks

    defsplit_text(self, text: str) -> List[str]:
"""
        Split incoming code into chunks using the AST parser.

        This method parses the input code into an AST and then chunks it while preserving
        syntactic structure. Supports both character-based and token-based chunking modes
        for more precise control over chunk sizes.

        Args:
            text (str): The source code text to split.

        Returns:
            List[str]: A list of code chunks that respect size limits based on count_mode.

        Raises:
            ValueError: If the code cannot be parsed for the specified language.

        """
        with self.callback_manager.event(
            CBEventType.CHUNKING, payload={EventPayload.CHUNKS: [text]}
        ) as event:
            text_bytes = bytes(text, "utf-8")
            tree = self._parser.parse(text_bytes)

            if (
                not tree.root_node.children
                or tree.root_node.children[0].type != "ERROR"
            ):
                chunks = [
                    chunk.strip()
                    for chunk in self._chunk_node(tree.root_node, text_bytes)
                ]
                event.on_end(
                    payload={EventPayload.CHUNKS: chunks},
                )

                return chunks
            else:
                raise ValueError(f"Could not parse code with language {self.language}.")

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.CodeSplitter.from_defaults "Permanent link")

```
from_defaults(
    language: ,
    chunk_lines:  = DEFAULT_CHUNK_LINES,
    chunk_lines_overlap:  = DEFAULT_LINES_OVERLAP,
    max_chars:  = DEFAULT_MAX_CHARS,
    count_mode: Literal["token", "char"] = "char",
    max_tokens:  = DEFAULT_MAX_TOKENS,
    tokenizer: Optional[Callable] = None,
    callback_manager: Optional[] = None,
    parser:  = None,
) -> 

```

Create a CodeSplitter with default values.
Source code in `llama-index-core/llama_index/core/node_parser/text/code.py`  
| 
```
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    language: str,
    chunk_lines: int = DEFAULT_CHUNK_LINES,
    chunk_lines_overlap: int = DEFAULT_LINES_OVERLAP,
    max_chars: int = DEFAULT_MAX_CHARS,
    count_mode: Literal["token", "char"] = "char",
    max_tokens: int = DEFAULT_MAX_TOKENS,
    tokenizer: Optional[Callable] = None,
    callback_manager: Optional[CallbackManager] = None,
    parser: Any = None,
) -> "CodeSplitter":
"""Create a CodeSplitter with default values."""
    return cls(
        language=language,
        chunk_lines=chunk_lines,
        chunk_lines_overlap=chunk_lines_overlap,
        max_chars=max_chars,
        count_mode=count_mode,
        max_tokens=max_tokens,
        tokenizer=tokenizer,
        callback_manager=callback_manager,
        parser=parser,
    )

```
 |  
| --- | --- |  
###  split_text [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.CodeSplitter.split_text "Permanent link")

```
split_text(text: ) -> []

```

Split incoming code into chunks using the AST parser.
This method parses the input code into an AST and then chunks it while preserving syntactic structure. Supports both character-based and token-based chunking modes for more precise control over chunk sizes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `text`  |  The source code text to split.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: A list of code chunks that respect size limits based on count_mode.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If the code cannot be parsed for the specified language.  |  
Source code in `llama-index-core/llama_index/core/node_parser/text/code.py`  
| 
```
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
```
 | 
```
defsplit_text(self, text: str) -> List[str]:
"""
    Split incoming code into chunks using the AST parser.

    This method parses the input code into an AST and then chunks it while preserving
    syntactic structure. Supports both character-based and token-based chunking modes
    for more precise control over chunk sizes.

    Args:
        text (str): The source code text to split.

    Returns:
        List[str]: A list of code chunks that respect size limits based on count_mode.

    Raises:
        ValueError: If the code cannot be parsed for the specified language.

    """
    with self.callback_manager.event(
        CBEventType.CHUNKING, payload={EventPayload.CHUNKS: [text]}
    ) as event:
        text_bytes = bytes(text, "utf-8")
        tree = self._parser.parse(text_bytes)

        if (
            not tree.root_node.children
            or tree.root_node.children[0].type != "ERROR"
        ):
            chunks = [
                chunk.strip()
                for chunk in self._chunk_node(tree.root_node, text_bytes)
            ]
            event.on_end(
                payload={EventPayload.CHUNKS: chunks},
            )

            return chunks
        else:
            raise ValueError(f"Could not parse code with language {self.language}.")

```
 |  
| --- | --- |  
##  LangchainNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.LangchainNodeParser "Permanent link")
Bases: 
Basic wrapper around langchain's text splitter.
TODO: Figure out how to make this metadata aware.
Source code in `llama-index-core/llama_index/core/node_parser/text/langchain.py`  
| 
```
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
```
 | 
```
classLangchainNodeParser(TextSplitter):
"""
    Basic wrapper around langchain's text splitter.

    TODO: Figure out how to make this metadata aware.
    """

    _lc_splitter: "LC_TextSplitter" = PrivateAttr()

    def__init__(
        self,
        lc_splitter: "LC_TextSplitter",
        callback_manager: Optional[CallbackManager] = None,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        id_func: Optional[Callable[[int, Document], str]] = None,
    ):
"""Initialize with parameters."""
        id_func = id_func or default_id_func

        super().__init__(
            callback_manager=callback_manager or CallbackManager(),
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            id_func=id_func,
        )
        self._lc_splitter = lc_splitter

    defsplit_text(self, text: str) -> List[str]:
"""Split text into sentences."""
        return self._lc_splitter.split_text(text)

```
 |  
| --- | --- |  
###  split_text [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.LangchainNodeParser.split_text "Permanent link")

```
split_text(text: ) -> []

```

Split text into sentences.
Source code in `llama-index-core/llama_index/core/node_parser/text/langchain.py`  
| 
```
48
49
50
```
 | 
```
defsplit_text(self, text: str) -> List[str]:
"""Split text into sentences."""
    return self._lc_splitter.split_text(text)

```
 |  
| --- | --- |  
##  SemanticSplitterNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.SemanticSplitterNodeParser "Permanent link")
Bases: 
Semantic node parser.
Splits a document into Nodes, with each node being a group of semantically related sentences.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `buffer_size`  |  number of sentences to group together when evaluating semantic similarity  |  
|  `embed_model`  |   |  (BaseEmbedding): embedding model to use  |  _required_  |  
|  `sentence_splitter`  |  `Callable[list, List[str]]`  |  splits text into sentences  |  `<function split_by_sentence_tokenizer.<locals>.<lambda> at 0x7f00a5c7d2d0>`  |  
|  `breakpoint_percentile_threshold`  |  dissimilarity threshold for creating semantic breakpoints, lower value will generate more nodes  |  
|  `include_metadata`  |  `bool`  |  whether to include metadata in nodes  |  _required_  |  
|  `include_prev_next_rel`  |  `bool`  |  whether to include prev/next relationships  |  _required_  |  
Source code in `llama-index-core/llama_index/core/node_parser/text/semantic_splitter.py`  
| 
```
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
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
```
 | 
```
classSemanticSplitterNodeParser(NodeParser):
"""
    Semantic node parser.

    Splits a document into Nodes, with each node being a group of semantically related sentences.

    Args:
        buffer_size (int): number of sentences to group together when evaluating semantic similarity
        embed_model: (BaseEmbedding): embedding model to use
        sentence_splitter (Optional[Callable]): splits text into sentences
        breakpoint_percentile_threshold (int): dissimilarity threshold for creating semantic breakpoints, lower value will generate more nodes
        include_metadata (bool): whether to include metadata in nodes
        include_prev_next_rel (bool): whether to include prev/next relationships

    """

    sentence_splitter: SentenceSplitterCallable = Field(
        default_factory=split_by_sentence_tokenizer,
        description="The text splitter to use when splitting documents.",
        exclude=True,
    )

    embed_model: SerializeAsAny[BaseEmbedding] = Field(
        description="The embedding model to use to for semantic comparison",
    )

    buffer_size: int = Field(
        default=1,
        description=(
            "The number of sentences to group together when evaluating semantic similarity. "
            "Set to 1 to consider each sentence individually. "
            "Set to >1 to group sentences together."
        ),
    )

    breakpoint_percentile_threshold: int = Field(
        default=95,
        description=(
            "The percentile of cosine dissimilarity that must be exceeded between a "
            "group of sentences and the next to form a node.  The smaller this "
            "number is, the more nodes will be generated"
        ),
    )

    @classmethod
    defclass_name(cls) -> str:
        return "SemanticSplitterNodeParser"

    @classmethod
    deffrom_defaults(
        cls,
        embed_model: Optional[BaseEmbedding] = None,
        breakpoint_percentile_threshold: Optional[int] = 95,
        buffer_size: Optional[int] = 1,
        sentence_splitter: Optional[Callable[[str], List[str]]] = None,
        original_text_metadata_key: str = DEFAULT_OG_TEXT_METADATA_KEY,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        id_func: Optional[Callable[[int, Document], str]] = None,
    ) -> "SemanticSplitterNodeParser":
        callback_manager = callback_manager or CallbackManager([])

        sentence_splitter = sentence_splitter or split_by_sentence_tokenizer()
        if embed_model is None:
            try:
                fromllama_index.embeddings.openaiimport (
                    OpenAIEmbedding,
                )  # pants: no-infer-dep

                embed_model = embed_model or OpenAIEmbedding()
            except ImportError:
                raise ImportError(
                    "`llama-index-embeddings-openai` package not found, "
                    "please run `pip install llama-index-embeddings-openai`"
                )

        id_func = id_func or default_id_func

        return cls(
            embed_model=embed_model,
            breakpoint_percentile_threshold=breakpoint_percentile_threshold,
            buffer_size=buffer_size,
            sentence_splitter=sentence_splitter,
            original_text_metadata_key=original_text_metadata_key,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            callback_manager=callback_manager,
            id_func=id_func,
        )

    def_parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""Parse document into nodes."""
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")

        for node in nodes_with_progress:
            nodes = self.build_semantic_nodes_from_documents([node], show_progress)
            all_nodes.extend(nodes)

        return all_nodes

    async def_aparse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""Asynchronously parse document into nodes."""
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")

        for node in nodes_with_progress:
            nodes = await self.abuild_semantic_nodes_from_documents(
                [node], show_progress
            )
            all_nodes.extend(nodes)

        return all_nodes

    defbuild_semantic_nodes_from_documents(
        self,
        documents: Sequence[Document],
        show_progress: bool = False,
    ) -> List[BaseNode]:
"""Build window nodes from documents."""
        all_nodes: List[BaseNode] = []
        for doc in documents:
            text = doc.text
            text_splits = self.sentence_splitter(text)

            sentences = self._build_sentence_groups(text_splits)

            combined_sentence_embeddings = self.embed_model.get_text_embedding_batch(
                [s["combined_sentence"] for s in sentences],
                show_progress=show_progress,
            )

            for i, embedding in enumerate(combined_sentence_embeddings):
                sentences[i]["combined_sentence_embedding"] = embedding

            distances = self._calculate_distances_between_sentence_groups(sentences)

            chunks = self._build_node_chunks(sentences, distances)

            nodes = build_nodes_from_splits(
                chunks,
                doc,
                id_func=self.id_func,
            )

            all_nodes.extend(nodes)

        return all_nodes

    async defabuild_semantic_nodes_from_documents(
        self,
        documents: Sequence[Document],
        show_progress: bool = False,
    ) -> List[BaseNode]:
"""Asynchronously build window nodes from documents."""
        all_nodes: List[BaseNode] = []
        for doc in documents:
            text = doc.text
            text_splits = self.sentence_splitter(text)

            sentences = self._build_sentence_groups(text_splits)

            combined_sentence_embeddings = (
                await self.embed_model.aget_text_embedding_batch(
                    [s["combined_sentence"] for s in sentences],
                    show_progress=show_progress,
                )
            )

            for i, embedding in enumerate(combined_sentence_embeddings):
                sentences[i]["combined_sentence_embedding"] = embedding

            distances = self._calculate_distances_between_sentence_groups(sentences)

            chunks = self._build_node_chunks(sentences, distances)

            nodes = build_nodes_from_splits(
                chunks,
                doc,
                id_func=self.id_func,
            )

            all_nodes.extend(nodes)

        return all_nodes

    def_build_sentence_groups(
        self, text_splits: List[str]
    ) -> List[SentenceCombination]:
        sentences: List[SentenceCombination] = [
            {
                "sentence": x,
                "index": i,
                "combined_sentence": "",
                "combined_sentence_embedding": [],
            }
            for i, x in enumerate(text_splits)
        ]

        # Group sentences and calculate embeddings for sentence groups
        for i in range(len(sentences)):
            combined_sentence = ""

            for j in range(i - self.buffer_size, i):
                if j >= 0:
                    combined_sentence += sentences[j]["sentence"]

            combined_sentence += sentences[i]["sentence"]

            for j in range(i + 1, i + 1 + self.buffer_size):
                if j  len(sentences):
                    combined_sentence += sentences[j]["sentence"]

            sentences[i]["combined_sentence"] = combined_sentence

        return sentences

    def_calculate_distances_between_sentence_groups(
        self, sentences: List[SentenceCombination]
    ) -> List[float]:
        distances = []
        for i in range(len(sentences) - 1):
            embedding_current = sentences[i]["combined_sentence_embedding"]
            embedding_next = sentences[i + 1]["combined_sentence_embedding"]

            similarity = self.embed_model.similarity(embedding_current, embedding_next)

            distance = 1 - similarity

            distances.append(distance)

        return distances

    def_build_node_chunks(
        self, sentences: List[SentenceCombination], distances: List[float]
    ) -> List[str]:
        chunks = []
        if len(distances)  0:
            breakpoint_distance_threshold = np.percentile(
                distances, self.breakpoint_percentile_threshold
            )

            indices_above_threshold = [
                i for i, x in enumerate(distances) if x  breakpoint_distance_threshold
            ]

            # Chunk sentences into semantic groups based on percentile breakpoints
            start_index = 0

            for index in indices_above_threshold:
                group = sentences[start_index : index + 1]
                combined_text = "".join([d["sentence"] for d in group])
                chunks.append(combined_text)

                start_index = index + 1

            if start_index  len(sentences):
                combined_text = "".join(
                    [d["sentence"] for d in sentences[start_index:]]
                )
                chunks.append(combined_text)
        else:
            # If, for some reason we didn't get any distances (i.e. very, very small documents) just
            # treat the whole document as a single node
            chunks = [" ".join([s["sentence"] for s in sentences])]

        return chunks

```
 |  
| --- | --- |  
###  build_semantic_nodes_from_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.SemanticSplitterNodeParser.build_semantic_nodes_from_documents "Permanent link")

```
build_semantic_nodes_from_documents(
    documents: Sequence[],
    show_progress:  = False,
) -> []

```

Build window nodes from documents.
Source code in `llama-index-core/llama_index/core/node_parser/text/semantic_splitter.py`  
| 
```
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
```
 | 
```
defbuild_semantic_nodes_from_documents(
    self,
    documents: Sequence[Document],
    show_progress: bool = False,
) -> List[BaseNode]:
"""Build window nodes from documents."""
    all_nodes: List[BaseNode] = []
    for doc in documents:
        text = doc.text
        text_splits = self.sentence_splitter(text)

        sentences = self._build_sentence_groups(text_splits)

        combined_sentence_embeddings = self.embed_model.get_text_embedding_batch(
            [s["combined_sentence"] for s in sentences],
            show_progress=show_progress,
        )

        for i, embedding in enumerate(combined_sentence_embeddings):
            sentences[i]["combined_sentence_embedding"] = embedding

        distances = self._calculate_distances_between_sentence_groups(sentences)

        chunks = self._build_node_chunks(sentences, distances)

        nodes = build_nodes_from_splits(
            chunks,
            doc,
            id_func=self.id_func,
        )

        all_nodes.extend(nodes)

    return all_nodes

```
 |  
| --- | --- |  
###  abuild_semantic_nodes_from_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.SemanticSplitterNodeParser.abuild_semantic_nodes_from_documents "Permanent link")

```
abuild_semantic_nodes_from_documents(
    documents: Sequence[],
    show_progress:  = False,
) -> []

```

Asynchronously build window nodes from documents.
Source code in `llama-index-core/llama_index/core/node_parser/text/semantic_splitter.py`  
| 
```
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
```
 | 
```
async defabuild_semantic_nodes_from_documents(
    self,
    documents: Sequence[Document],
    show_progress: bool = False,
) -> List[BaseNode]:
"""Asynchronously build window nodes from documents."""
    all_nodes: List[BaseNode] = []
    for doc in documents:
        text = doc.text
        text_splits = self.sentence_splitter(text)

        sentences = self._build_sentence_groups(text_splits)

        combined_sentence_embeddings = (
            await self.embed_model.aget_text_embedding_batch(
                [s["combined_sentence"] for s in sentences],
                show_progress=show_progress,
            )
        )

        for i, embedding in enumerate(combined_sentence_embeddings):
            sentences[i]["combined_sentence_embedding"] = embedding

        distances = self._calculate_distances_between_sentence_groups(sentences)

        chunks = self._build_node_chunks(sentences, distances)

        nodes = build_nodes_from_splits(
            chunks,
            doc,
            id_func=self.id_func,
        )

        all_nodes.extend(nodes)

    return all_nodes

```
 |  
| --- | --- |  
##  SemanticDoubleMergingSplitterNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.SemanticDoubleMergingSplitterNodeParser "Permanent link")
Bases: 
Semantic double merging text splitter.
Splits a document into Nodes, with each node being a group of semantically related sentences. Supports either Spacy (language-specific) or an embedding model (any language, e.g. Hugging Face).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `language_config`  |  `LanguageConfig`  |  language and Spacy model when using Spacy backend (ignored if embed_model is set)  |  `<llama_index.core.node_parser.text.semantic_double_merging_splitter.LanguageConfig object at 0x7f00b0d91fd0>`  |  
|  `embed_model`  |  `Annotated[BaseEmbedding[](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding "BaseEmbedding \(llama_index.core.base.embeddings.base.BaseEmbedding\)"), SerializeAsAny] | None`  |  when set, use this for similarity instead of Spacy (multilingual)  |  `None`  |  
|  `initial_threshold`  |  `float`  |  sets threshold for initializing new chunk  |  `0.6`  |  
|  `appending_threshold`  |  `float`  |  sets threshold for appending new sentences to chunk  |  `0.8`  |  
|  `merging_threshold`  |  `float`  |  sets threshold for merging whole chunks  |  `0.8`  |  
|  `max_chunk_size`  |  maximum size of chunk (in characters)  |  `1000`  |  
|  `merging_range`  |  How many chunks 'ahead' beyond the nearest neighbor to be merged if similar (1 or 2 available)  |  
|  `merging_separator`  |  The separator to use when merging chunks. Defaults to a single space.  |  `' '`  |  
|  `sentence_splitter`  |  `Callable[list, List[str]]`  |  splits text into sentences  |  `<function split_by_sentence_tokenizer.<locals>.<lambda> at 0x7f00a5c7d170>`  |  
Source code in `llama-index-core/llama_index/core/node_parser/text/semantic_double_merging_splitter.py`  
| 
```
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
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
```
 | 
```
classSemanticDoubleMergingSplitterNodeParser(NodeParser):
"""
    Semantic double merging text splitter.

    Splits a document into Nodes, with each node being a group of semantically related sentences.
    Supports either Spacy (language-specific) or an embedding model (any language, e.g. Hugging Face).

    Args:
        language_config (LanguageConfig): language and Spacy model when using Spacy backend (ignored if embed_model is set)
        embed_model (Optional[BaseEmbedding]): when set, use this for similarity instead of Spacy (multilingual)
        initial_threshold (float): sets threshold for initializing new chunk
        appending_threshold (float): sets threshold for appending new sentences to chunk
        merging_threshold (float): sets threshold for merging whole chunks
        max_chunk_size (int): maximum size of chunk (in characters)
        merging_range (int): How many chunks 'ahead' beyond the nearest neighbor to be merged if similar (1 or 2 available)
        merging_separator (str): The separator to use when merging chunks. Defaults to a single space.
        sentence_splitter (Optional[Callable]): splits text into sentences

    """

    language_config: LanguageConfig = Field(
        default=LanguageConfig(),
        description="Config that selects language and spacy model for chunking (used only when embed_model is None)",
    )

    embed_model: Optional[SerializeAsAny[BaseEmbedding]] = Field(
        default=None,
        description="When set, use this embedding model for similarity instead of Spacy (enables any language).",
    )

    initial_threshold: float = Field(
        default=0.6,
        description=(
            "The value of semantic similarity that must be exceeded between two"
            "sentences to create a new chunk.  The bigger this "
            "value is, the more nodes will be generated. Range is from 0 to 1."
        ),
    )

    appending_threshold: float = Field(
        default=0.8,
        description=(
            "The value of semantic similarity that must be exceeded between a "
            "chunk and new sentence to add this sentence to existing chunk.  The bigger this "
            "value is, the more nodes will be generated. Range is from 0 to 1."
        ),
    )

    merging_threshold: float = Field(
        default=0.8,
        description=(
            "The value of semantic similarity that must be exceeded between two chunks "
            "to form a bigger chunk.  The bigger this value is,"
            "the more nodes will be generated. Range is from 0 to 1."
        ),
    )

    max_chunk_size: int = Field(
        default=1000,
        description="Maximum length of chunk that can be subjected to verification (number of characters)",
    )

    merging_range: int = Field(
        default=1,
        description=(
            "How many chunks 'ahead' beyond the nearest neighbor"
            "should the algorithm check during the second pass"
            "(possible options are 1 or 2"
        ),
    )

    merging_separator: str = Field(
        default=" ",
        description="The separator to use when merging chunks. Defaults to a single space.",
    )

    sentence_splitter: Callable[[str], List[str]] = Field(
        default_factory=split_by_sentence_tokenizer,
        description="The text splitter to use when splitting documents.",
        exclude=True,
    )

    @classmethod
    defclass_name(cls) -> str:
        return "SemanticDoubleMergingSplitterNodeParser"

    @classmethod
    deffrom_defaults(
        cls,
        language_config: Optional[LanguageConfig] = None,
        embed_model: Optional[BaseEmbedding] = None,
        initial_threshold: Optional[float] = 0.6,
        appending_threshold: Optional[float] = 0.8,
        merging_threshold: Optional[float] = 0.8,
        max_chunk_size: Optional[int] = 1000,
        merging_range: Optional[int] = 1,
        merging_separator: Optional[str] = " ",
        sentence_splitter: Optional[Callable[[str], List[str]]] = None,
        original_text_metadata_key: str = DEFAULT_OG_TEXT_METADATA_KEY,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        id_func: Optional[Callable[[int, Document], str]] = None,
    ) -> "SemanticDoubleMergingSplitterNodeParser":
        callback_manager = callback_manager or CallbackManager([])
        sentence_splitter = sentence_splitter or split_by_sentence_tokenizer()
        id_func = id_func or default_id_func
        if language_config is None:
            language_config = LanguageConfig()
        return cls(
            language_config=language_config,
            embed_model=embed_model,
            initial_threshold=initial_threshold,
            appending_threshold=appending_threshold,
            merging_threshold=merging_threshold,
            max_chunk_size=max_chunk_size,
            merging_range=merging_range,
            merging_separator=merging_separator,
            sentence_splitter=sentence_splitter,
            original_text_metadata_key=original_text_metadata_key,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            callback_manager=callback_manager,
            id_func=id_func,
        )

    def_similarity(self, text_a: str, text_b: str) -> float:
        if self.embed_model is not None:
            embeddings = self.embed_model.get_text_embedding_batch([text_a, text_b])
            return self.embed_model.similarity(embeddings[0], embeddings[1])
        if self.language_config.nlp is None:
            self.language_config.load_model()
        assert self.language_config.nlp is not None
        clean_a = self._clean_text_advanced(text_a)
        clean_b = self._clean_text_advanced(text_b)
        return self.language_config.nlp(clean_a).similarity(
            self.language_config.nlp(clean_b)
        )

    def_parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""Parse document into nodes."""
        if self.embed_model is None:
            self.language_config.load_model()
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")
        for node in nodes_with_progress:
            nodes = self.build_semantic_nodes_from_nodes([node])
            all_nodes.extend(nodes)
        return all_nodes

    defbuild_semantic_nodes_from_documents(
        self,
        documents: Sequence[Document],
    ) -> List[BaseNode]:
"""Build window nodes from documents."""
        return self.build_semantic_nodes_from_nodes(documents)

    defbuild_semantic_nodes_from_nodes(
        self,
        nodes: Sequence[BaseNode],
    ) -> List[BaseNode]:
"""Build window nodes from nodes."""
        all_nodes: List[BaseNode] = []

        for node in nodes:
            text = node.get_content()
            sentences = self.sentence_splitter(text)
            sentences = [s.strip() for s in sentences]
            initial_chunks = self._create_initial_chunks(sentences)
            chunks = self._merge_initial_chunks(initial_chunks)

            split_nodes = build_nodes_from_splits(
                chunks,
                node,
                id_func=self.id_func,
            )

            previous_node: Optional[BaseNode] = None
            for split_node in split_nodes:
                if previous_node:
                    split_node.relationships[NodeRelationship.PREVIOUS] = (
                        previous_node.as_related_node_info()
                    )
                    previous_node.relationships[NodeRelationship.NEXT] = (
                        split_node.as_related_node_info()
                    )
                previous_node = split_node
            all_nodes.extend(split_nodes)

        return all_nodes

    def_create_initial_chunks(self, sentences: List[str]) -> List[str]:
        initial_chunks: List[str] = []
        chunk = sentences[0]
        new = True
        for sentence in sentences[1:]:
            if new:
                if (
                    self._similarity(chunk, sentence)  self.initial_threshold
                    and len(chunk) + len(sentence) + 1 <= self.max_chunk_size
                ):
                    initial_chunks.append(chunk)
                    chunk = sentence
                    continue
                chunk_sentences = [chunk]
                if len(chunk) + len(sentence) + 1 <= self.max_chunk_size:
                    chunk_sentences.append(sentence)
                    chunk = self.merging_separator.join(chunk_sentences)
                    new = False
                else:
                    new = True
                    initial_chunks.append(chunk)
                    chunk = sentence
                    continue
                last_sentences = self.merging_separator.join(chunk_sentences[-2:])
            elif (
                self._similarity(last_sentences, sentence)  self.appending_threshold
                and len(chunk) + len(sentence) + 1 <= self.max_chunk_size
            ):
                chunk_sentences.append(sentence)
                last_sentences = self.merging_separator.join(chunk_sentences[-2:])
                chunk += self.merging_separator + sentence
            else:
                initial_chunks.append(chunk)
                chunk = sentence
                new = True
        initial_chunks.append(chunk)
        return initial_chunks

    def_merge_initial_chunks(self, initial_chunks: List[str]) -> List[str]:
        chunks: List[str] = []
        skip = 0
        current = initial_chunks[0]
        for i in range(1, len(initial_chunks)):
            if skip  0:
                skip -= 1
                continue
            if len(current) >= self.max_chunk_size:
                chunks.append(current)
                current = initial_chunks[i]
            elif (
                self._similarity(current, initial_chunks[i])  self.merging_threshold
                and len(current) + len(initial_chunks[i]) + 1 <= self.max_chunk_size
            ):
                current += self.merging_separator + initial_chunks[i]
            elif (
                i <= len(initial_chunks) - 2
                and self._similarity(current, initial_chunks[i + 1])
                 self.merging_threshold
                and len(current)
                + len(initial_chunks[i])
                + len(initial_chunks[i + 1])
                + 2
                <= self.max_chunk_size
            ):
                current += (
                    self.merging_separator
                    + initial_chunks[i]
                    + self.merging_separator
                    + initial_chunks[i + 1]
                )
                skip = 1
            elif (
                i  len(initial_chunks) - 2
                and self._similarity(current, initial_chunks[i + 2])
                 self.merging_threshold
                and self.merging_range == 2
                and len(current)
                + len(initial_chunks[i])
                + len(initial_chunks[i + 1])
                + len(initial_chunks[i + 2])
                + 3
                <= self.max_chunk_size
            ):
                current += (
                    self.merging_separator
                    + initial_chunks[i]
                    + self.merging_separator
                    + initial_chunks[i + 1]
                    + self.merging_separator
                    + initial_chunks[i + 2]
                )
                skip = 2
            else:
                chunks.append(current)
                current = initial_chunks[i]
        chunks.append(current)
        return chunks

    def_clean_text_advanced(self, text: str) -> str:
        text = text.lower()
        # Remove urls
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
        # Remove punctuations
        text = text.translate(str.maketrans("", "", string.punctuation))
        # Remove stopwords
        tokens = globals_helper.punkt_tokenizer.tokenize(text)
        filtered_words = [w for w in tokens if w not in self.language_config.stopwords]

        return " ".join(filtered_words)

```
 |  
| --- | --- |  
###  build_semantic_nodes_from_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.SemanticDoubleMergingSplitterNodeParser.build_semantic_nodes_from_documents "Permanent link")

```
build_semantic_nodes_from_documents(
    documents: Sequence[],
) -> []

```

Build window nodes from documents.
Source code in `llama-index-core/llama_index/core/node_parser/text/semantic_double_merging_splitter.py`  
| 
```
216
217
218
219
220
221
```
 | 
```
defbuild_semantic_nodes_from_documents(
    self,
    documents: Sequence[Document],
) -> List[BaseNode]:
"""Build window nodes from documents."""
    return self.build_semantic_nodes_from_nodes(documents)

```
 |  
| --- | --- |  
###  build_semantic_nodes_from_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.SemanticDoubleMergingSplitterNodeParser.build_semantic_nodes_from_nodes "Permanent link")

```
build_semantic_nodes_from_nodes(
    nodes: Sequence[],
) -> []

```

Build window nodes from nodes.
Source code in `llama-index-core/llama_index/core/node_parser/text/semantic_double_merging_splitter.py`  
| 
```
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
```
 | 
```
defbuild_semantic_nodes_from_nodes(
    self,
    nodes: Sequence[BaseNode],
) -> List[BaseNode]:
"""Build window nodes from nodes."""
    all_nodes: List[BaseNode] = []

    for node in nodes:
        text = node.get_content()
        sentences = self.sentence_splitter(text)
        sentences = [s.strip() for s in sentences]
        initial_chunks = self._create_initial_chunks(sentences)
        chunks = self._merge_initial_chunks(initial_chunks)

        split_nodes = build_nodes_from_splits(
            chunks,
            node,
            id_func=self.id_func,
        )

        previous_node: Optional[BaseNode] = None
        for split_node in split_nodes:
            if previous_node:
                split_node.relationships[NodeRelationship.PREVIOUS] = (
                    previous_node.as_related_node_info()
                )
                previous_node.relationships[NodeRelationship.NEXT] = (
                    split_node.as_related_node_info()
                )
            previous_node = split_node
        all_nodes.extend(split_nodes)

    return all_nodes

```
 |  
| --- | --- |  
##  SentenceSplitter [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.SentenceSplitter "Permanent link")
Bases: 
Parse text with a preference for complete sentences.
In general, this class tries to keep sentences and paragraphs together. Therefore compared to the original TokenTextSplitter, there are less likely to be hanging sentences or parts of sentences at the end of the node chunk.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `chunk_size`  |  The token chunk size for each chunk.  |  `1024`  |  
|  `chunk_overlap`  |  The token overlap of each chunk when splitting.  |  `200`  |  
|  `separator`  |  Default separator for splitting into words  |  `' '`  |  
|  `paragraph_separator`  |  Separator between paragraphs.  |  `'\n\n\n'`  |  
|  `secondary_chunking_regex`  |  `str | None`  |  Backup regex for splitting into sentences.  |  `'[^,.;。？！]+[,.;。？！]?|[,.;。？！]'`  |  
Source code in `llama-index-core/llama_index/core/node_parser/text/sentence.py`  
| 
```
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
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
```
 | 
```
classSentenceSplitter(MetadataAwareTextSplitter):
"""
    Parse text with a preference for complete sentences.

    In general, this class tries to keep sentences and paragraphs together. Therefore
    compared to the original TokenTextSplitter, there are less likely to be
    hanging sentences or parts of sentences at the end of the node chunk.
    """

    chunk_size: int = Field(
        default=DEFAULT_CHUNK_SIZE,
        description="The token chunk size for each chunk.",
        gt=0,
    )
    chunk_overlap: int = Field(
        default=SENTENCE_CHUNK_OVERLAP,
        description="The token overlap of each chunk when splitting.",
        ge=0,
    )
    separator: str = Field(
        default=" ", description="Default separator for splitting into words"
    )
    paragraph_separator: str = Field(
        default=DEFAULT_PARAGRAPH_SEP, description="Separator between paragraphs."
    )
    secondary_chunking_regex: Optional[str] = Field(
        default=CHUNKING_REGEX, description="Backup regex for splitting into sentences."
    )

    _chunking_tokenizer_fn: Callable[[str], List[str]] = PrivateAttr()
    _tokenizer: Callable = PrivateAttr()
    _split_fns: List[Callable] = PrivateAttr()
    _sub_sentence_split_fns: List[Callable] = PrivateAttr()

    def__init__(
        self,
        separator: str = " ",
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = SENTENCE_CHUNK_OVERLAP,
        tokenizer: Optional[Callable] = None,
        paragraph_separator: str = DEFAULT_PARAGRAPH_SEP,
        chunking_tokenizer_fn: Optional[Callable[[str], List[str]]] = None,
        secondary_chunking_regex: Optional[str] = CHUNKING_REGEX,
        callback_manager: Optional[CallbackManager] = None,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        id_func: Optional[Callable] = None,
    ):
"""Initialize with parameters."""
        if chunk_overlap  chunk_size:
            raise ValueError(
                f"Got a larger chunk overlap ({chunk_overlap}) than chunk size "
                f"({chunk_size}), should be smaller."
            )
        id_func = id_func or default_id_func
        callback_manager = callback_manager or CallbackManager([])
        super().__init__(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            secondary_chunking_regex=secondary_chunking_regex,
            separator=separator,
            paragraph_separator=paragraph_separator,
            callback_manager=callback_manager,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            id_func=id_func,
        )
        self._chunking_tokenizer_fn = (
            chunking_tokenizer_fn or split_by_sentence_tokenizer()
        )
        self._tokenizer = tokenizer or get_tokenizer()

        self._split_fns = [
            split_by_sep(paragraph_separator),
            self._chunking_tokenizer_fn,
        ]

        if secondary_chunking_regex:
            self._sub_sentence_split_fns = [
                split_by_regex(secondary_chunking_regex),
                split_by_sep(separator),
                split_by_char(),
            ]
        else:
            self._sub_sentence_split_fns = [
                split_by_sep(separator),
                split_by_char(),
            ]

    @classmethod
    deffrom_defaults(
        cls,
        separator: str = " ",
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = SENTENCE_CHUNK_OVERLAP,
        tokenizer: Optional[Callable] = None,
        paragraph_separator: str = DEFAULT_PARAGRAPH_SEP,
        chunking_tokenizer_fn: Optional[Callable[[str], List[str]]] = None,
        secondary_chunking_regex: str = CHUNKING_REGEX,
        callback_manager: Optional[CallbackManager] = None,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
    ) -> "SentenceSplitter":
"""Initialize with parameters."""
        callback_manager = callback_manager or CallbackManager([])
        return cls(
            separator=separator,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            tokenizer=tokenizer,
            paragraph_separator=paragraph_separator,
            chunking_tokenizer_fn=chunking_tokenizer_fn,
            secondary_chunking_regex=secondary_chunking_regex,
            callback_manager=callback_manager,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "SentenceSplitter"

    defsplit_text_metadata_aware(self, text: str, metadata_str: str) -> List[str]:
        metadata_len = len(self._tokenizer(metadata_str))
        effective_chunk_size = self.chunk_size - metadata_len
        if effective_chunk_size <= 0:
            raise ValueError(
                f"Metadata length ({metadata_len}) is longer than chunk size "
                f"({self.chunk_size}). Consider increasing the chunk size or "
                "decreasing the size of your metadata to avoid this."
            )
        elif effective_chunk_size  50:
            print(
                f"Metadata length ({metadata_len}) is close to chunk size "
                f"({self.chunk_size}). Resulting chunks are less than 50 tokens. "
                "Consider increasing the chunk size or decreasing the size of "
                "your metadata to avoid this.",
                flush=True,
            )

        return self._split_text(text, chunk_size=effective_chunk_size)

    defsplit_text(self, text: str) -> List[str]:
        return self._split_text(text, chunk_size=self.chunk_size)

    def_split_text(self, text: str, chunk_size: int) -> List[str]:
"""
        _Split incoming text and return chunks with overlap size.

        Has a preference for complete sentences, phrases, and minimal overlap.
        """
        if text == "":
            return [text]

        with self.callback_manager.event(
            CBEventType.CHUNKING, payload={EventPayload.CHUNKS: [text]}
        ) as event:
            splits = self._split(text, chunk_size)
            chunks = self._merge(splits, chunk_size)

            event.on_end(payload={EventPayload.CHUNKS: chunks})

        return chunks

    def_split(self, text: str, chunk_size: int) -> List[_Split]:
r"""
        Break text into splits that are smaller than chunk size.

        The order of splitting is:
        1. split by paragraph separator
        2. split by chunking tokenizer (default is nltk sentence tokenizer)
        3. split by second chunking regex (default is "[^,\.;]+[,\.;]?")
        4. split by default separator (" ")

        """
        token_size = self._token_size(text)
        if token_size <= chunk_size:
            return [_Split(text, is_sentence=True, token_size=token_size)]

        text_splits_by_fns, is_sentence = self._get_splits_by_fns(text)

        text_splits = []
        for text_split_by_fns in text_splits_by_fns:
            token_size = self._token_size(text_split_by_fns)
            if token_size <= chunk_size:
                text_splits.append(
                    _Split(
                        text_split_by_fns,
                        is_sentence=is_sentence,
                        token_size=token_size,
                    )
                )
            else:
                recursive_text_splits = self._split(
                    text_split_by_fns, chunk_size=chunk_size
                )
                text_splits.extend(recursive_text_splits)
        return text_splits

    def_merge(self, splits: List[_Split], chunk_size: int) -> List[str]:
"""Merge splits into chunks."""
        chunks: List[str] = []
        cur_chunk: List[Tuple[str, int]] = []  # list of (text, length)
        last_chunk: List[Tuple[str, int]] = []
        cur_chunk_len = 0
        new_chunk = True

        defclose_chunk() -> None:
            nonlocal chunks, cur_chunk, last_chunk, cur_chunk_len, new_chunk

            chunks.append("".join([text for text, length in cur_chunk]))
            last_chunk = cur_chunk
            cur_chunk = []
            cur_chunk_len = 0
            new_chunk = True

            # add overlap to the next chunk using the last one first
            if len(last_chunk)  0:
                last_index = len(last_chunk) - 1
                while (
                    last_index >= 0
                    and cur_chunk_len + last_chunk[last_index][1] <= self.chunk_overlap
                ):
                    overlap_text, overlap_length = last_chunk[last_index]
                    cur_chunk_len += overlap_length
                    cur_chunk.insert(0, (overlap_text, overlap_length))
                    last_index -= 1

        split_idx = 0
        while split_idx  len(splits):
            cur_split = splits[split_idx]
            if cur_split.token_size  chunk_size:
                raise ValueError("Single token exceeded chunk size")
            if cur_chunk_len + cur_split.token_size  chunk_size and not new_chunk:
                # if adding split to current chunk exceeds chunk size: close out chunk
                close_chunk()
            else:
                # If this is a new chunk with overlap, and adding the split would
                # exceed chunk_size, remove overlap to make room
                if new_chunk and cur_chunk_len + cur_split.token_size  chunk_size:
                    # Remove overlap from the beginning until split fits
                    while (
                        len(cur_chunk)  0
                        and cur_chunk_len + cur_split.token_size  chunk_size
                    ):
                        _, length = cur_chunk.pop(0)
                        cur_chunk_len -= length

                if (
                    cur_split.is_sentence
                    or cur_chunk_len + cur_split.token_size <= chunk_size
                    or new_chunk  # new chunk, always add at least one split
                ):
                    # add split to chunk
                    cur_chunk_len += cur_split.token_size
                    cur_chunk.append((cur_split.text, cur_split.token_size))
                    split_idx += 1
                    new_chunk = False
                else:
                    # close out chunk
                    close_chunk()

        # handle the last chunk
        if not new_chunk:
            chunk = "".join([text for text, length in cur_chunk])
            chunks.append(chunk)

        # run postprocessing to remove blank spaces
        return self._postprocess_chunks(chunks)

    def_postprocess_chunks(self, chunks: List[str]) -> List[str]:
"""
        Post-process chunks.
        Remove whitespace only chunks and remove leading and trailing whitespace.
        """
        new_chunks = []
        for chunk in chunks:
            stripped_chunk = chunk.strip()
            if stripped_chunk == "":
                continue
            new_chunks.append(stripped_chunk)
        return new_chunks

    def_token_size(self, text: str) -> int:
        return len(self._tokenizer(text))

    def_get_splits_by_fns(self, text: str) -> Tuple[List[str], bool]:
        for split_fn in self._split_fns:
            splits = split_fn(text)
            if len(splits)  1:
                return splits, True

        for split_fn in self._sub_sentence_split_fns:
            splits = split_fn(text)
            if len(splits)  1:
                break

        return splits, False

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.SentenceSplitter.from_defaults "Permanent link")

```
from_defaults(
    separator:  = " ",
    chunk_size:  = DEFAULT_CHUNK_SIZE,
    chunk_overlap:  = SENTENCE_CHUNK_OVERLAP,
    tokenizer: Optional[Callable] = None,
    paragraph_separator:  = DEFAULT_PARAGRAPH_SEP,
    chunking_tokenizer_fn: Optional[
        Callable[[], []]
    ] = None,
    secondary_chunking_regex:  = CHUNKING_REGEX,
    callback_manager: Optional[] = None,
    include_metadata:  = True,
    include_prev_next_rel:  = True,
) -> 

```

Initialize with parameters.
Source code in `llama-index-core/llama_index/core/node_parser/text/sentence.py`  
| 
```
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
137
138
139
140
141
142
143
144
145
146
147
148
149
150
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    separator: str = " ",
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = SENTENCE_CHUNK_OVERLAP,
    tokenizer: Optional[Callable] = None,
    paragraph_separator: str = DEFAULT_PARAGRAPH_SEP,
    chunking_tokenizer_fn: Optional[Callable[[str], List[str]]] = None,
    secondary_chunking_regex: str = CHUNKING_REGEX,
    callback_manager: Optional[CallbackManager] = None,
    include_metadata: bool = True,
    include_prev_next_rel: bool = True,
) -> "SentenceSplitter":
"""Initialize with parameters."""
    callback_manager = callback_manager or CallbackManager([])
    return cls(
        separator=separator,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        tokenizer=tokenizer,
        paragraph_separator=paragraph_separator,
        chunking_tokenizer_fn=chunking_tokenizer_fn,
        secondary_chunking_regex=secondary_chunking_regex,
        callback_manager=callback_manager,
        include_metadata=include_metadata,
        include_prev_next_rel=include_prev_next_rel,
    )

```
 |  
| --- | --- |  
##  SentenceWindowNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.SentenceWindowNodeParser "Permanent link")
Bases: 
Sentence window node parser.
Splits a document into Nodes, with each node being a sentence. Each node contains a window from the surrounding sentences in the metadata.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sentence_splitter`  |  `Callable[list, List[str]]`  |  splits text into sentences  |  `<function split_by_sentence_tokenizer.<locals>.<lambda> at 0x7f00a6822350>`  |  
|  `include_metadata`  |  `bool`  |  whether to include metadata in nodes  |  _required_  |  
|  `include_prev_next_rel`  |  `bool`  |  whether to include prev/next relationships  |  _required_  |  
|  `window_size`  |  The number of sentences on each side of a sentence to capture.  |  
|  `window_metadata_key`  |  The metadata key to store the sentence window under.  |  `'window'`  |  
|  `original_text_metadata_key`  |  The metadata key to store the original sentence in.  |  `'original_text'`  |  
Source code in `llama-index-core/llama_index/core/node_parser/text/sentence_window.py`  
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
137
138
139
140
```
 | 
```
classSentenceWindowNodeParser(NodeParser):
"""
    Sentence window node parser.

    Splits a document into Nodes, with each node being a sentence.
    Each node contains a window from the surrounding sentences in the metadata.

    Args:
        sentence_splitter (Optional[Callable]): splits text into sentences
        include_metadata (bool): whether to include metadata in nodes
        include_prev_next_rel (bool): whether to include prev/next relationships

    """

    sentence_splitter: Callable[[str], List[str]] = Field(
        default_factory=split_by_sentence_tokenizer,
        description="The text splitter to use when splitting documents.",
        exclude=True,
    )
    window_size: int = Field(
        default=DEFAULT_WINDOW_SIZE,
        description="The number of sentences on each side of a sentence to capture.",
        gt=0,
    )
    window_metadata_key: str = Field(
        default=DEFAULT_WINDOW_METADATA_KEY,
        description="The metadata key to store the sentence window under.",
    )
    original_text_metadata_key: str = Field(
        default=DEFAULT_OG_TEXT_METADATA_KEY,
        description="The metadata key to store the original sentence in.",
    )

    @classmethod
    defclass_name(cls) -> str:
        return "SentenceWindowNodeParser"

    @classmethod
    deffrom_defaults(
        cls,
        sentence_splitter: Optional[Callable[[str], List[str]]] = None,
        window_size: int = DEFAULT_WINDOW_SIZE,
        window_metadata_key: str = DEFAULT_WINDOW_METADATA_KEY,
        original_text_metadata_key: str = DEFAULT_OG_TEXT_METADATA_KEY,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        id_func: Optional[Callable[[int, Document], str]] = None,
    ) -> "SentenceWindowNodeParser":
        callback_manager = callback_manager or CallbackManager([])

        sentence_splitter = sentence_splitter or split_by_sentence_tokenizer()

        id_func = id_func or default_id_func

        return cls(
            sentence_splitter=sentence_splitter,
            window_size=window_size,
            window_metadata_key=window_metadata_key,
            original_text_metadata_key=original_text_metadata_key,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            callback_manager=callback_manager,
            id_func=id_func,
        )

    def_parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""Parse document into nodes."""
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")

        for node in nodes_with_progress:
            nodes = self.build_window_nodes_from_documents([node])
            all_nodes.extend(nodes)

        return all_nodes

    defbuild_window_nodes_from_documents(
        self, documents: Sequence[Document]
    ) -> List[BaseNode]:
"""Build window nodes from documents."""
        all_nodes: List[BaseNode] = []
        for doc in documents:
            text = doc.text
            text_splits = self.sentence_splitter(text)
            nodes = build_nodes_from_splits(
                text_splits,
                doc,
                id_func=self.id_func,
            )

            # add window to each node
            for i, node in enumerate(nodes):
                window_nodes = nodes[
                    max(0, i - self.window_size) : min(
                        i + self.window_size + 1, len(nodes)
                    )
                ]

                node.metadata[self.window_metadata_key] = " ".join(
                    [n.text for n in window_nodes]
                )
                node.metadata[self.original_text_metadata_key] = node.text

                # exclude window metadata from embed and llm
                node.excluded_embed_metadata_keys.extend(
                    [self.window_metadata_key, self.original_text_metadata_key]
                )
                node.excluded_llm_metadata_keys.extend(
                    [self.window_metadata_key, self.original_text_metadata_key]
                )

            all_nodes.extend(nodes)

        return all_nodes

```
 |  
| --- | --- |  
###  build_window_nodes_from_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.SentenceWindowNodeParser.build_window_nodes_from_documents "Permanent link")

```
build_window_nodes_from_documents(
    documents: Sequence[],
) -> []

```

Build window nodes from documents.
Source code in `llama-index-core/llama_index/core/node_parser/text/sentence_window.py`  
| 
```
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
137
138
139
140
```
 | 
```
defbuild_window_nodes_from_documents(
    self, documents: Sequence[Document]
) -> List[BaseNode]:
"""Build window nodes from documents."""
    all_nodes: List[BaseNode] = []
    for doc in documents:
        text = doc.text
        text_splits = self.sentence_splitter(text)
        nodes = build_nodes_from_splits(
            text_splits,
            doc,
            id_func=self.id_func,
        )

        # add window to each node
        for i, node in enumerate(nodes):
            window_nodes = nodes[
                max(0, i - self.window_size) : min(
                    i + self.window_size + 1, len(nodes)
                )
            ]

            node.metadata[self.window_metadata_key] = " ".join(
                [n.text for n in window_nodes]
            )
            node.metadata[self.original_text_metadata_key] = node.text

            # exclude window metadata from embed and llm
            node.excluded_embed_metadata_keys.extend(
                [self.window_metadata_key, self.original_text_metadata_key]
            )
            node.excluded_llm_metadata_keys.extend(
                [self.window_metadata_key, self.original_text_metadata_key]
            )

        all_nodes.extend(nodes)

    return all_nodes

```
 |  
| --- | --- |  
##  TokenTextSplitter [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.TokenTextSplitter "Permanent link")
Bases: 
Implementation of splitting text that looks at word tokens.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `chunk_size`  |  The token chunk size for each chunk.  |  `1024`  |  
|  `chunk_overlap`  |  The token overlap of each chunk when splitting.  |  
|  `separator`  |  Default separator for splitting into words  |  `' '`  |  
|  `backup_separators`  |  `List`  |  Additional separators for splitting.  |  `<dynamic>`  |  
|  `keep_whitespaces`  |  `bool`  |  Whether to keep leading/trailing whitespaces in the chunk.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/node_parser/text/token.py`  
| 
```
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
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
```
 | 
```
classTokenTextSplitter(MetadataAwareTextSplitter):
"""Implementation of splitting text that looks at word tokens."""

    chunk_size: int = Field(
        default=DEFAULT_CHUNK_SIZE,
        description="The token chunk size for each chunk.",
        gt=0,
    )
    chunk_overlap: int = Field(
        default=DEFAULT_CHUNK_OVERLAP,
        description="The token overlap of each chunk when splitting.",
        ge=0,
    )
    separator: str = Field(
        default=" ", description="Default separator for splitting into words"
    )
    backup_separators: List = Field(
        default_factory=list, description="Additional separators for splitting."
    )

    keep_whitespaces: bool = Field(
        default=False,
        description="Whether to keep leading/trailing whitespaces in the chunk.",
    )

    _tokenizer: Callable = PrivateAttr()
    _split_fns: List[Callable] = PrivateAttr()

    def__init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
        tokenizer: Optional[Callable] = None,
        callback_manager: Optional[CallbackManager] = None,
        separator: str = " ",
        backup_separators: Optional[List[str]] = ["\n"],
        keep_whitespaces: bool = False,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        id_func: Optional[Callable[[int, Document], str]] = None,
    ):
"""Initialize with parameters."""
        if chunk_overlap  chunk_size:
            raise ValueError(
                f"Got a larger chunk overlap ({chunk_overlap}) than chunk size "
                f"({chunk_size}), should be smaller."
            )
        callback_manager = callback_manager or CallbackManager([])
        id_func = id_func or default_id_func
        super().__init__(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator=separator,
            backup_separators=backup_separators,
            keep_whitespaces=keep_whitespaces,
            callback_manager=callback_manager,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            id_func=id_func,
        )
        self._tokenizer = tokenizer or get_tokenizer()
        all_seps = [separator] + (backup_separators or [])
        self._split_fns = [split_by_sep(sep) for sep in all_seps] + [split_by_char()]

    @classmethod
    deffrom_defaults(
        cls,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
        separator: str = " ",
        backup_separators: Optional[List[str]] = ["\n"],
        callback_manager: Optional[CallbackManager] = None,
        keep_whitespaces: bool = False,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        id_func: Optional[Callable[[int, Document], str]] = None,
    ) -> "TokenTextSplitter":
"""Initialize with default parameters."""
        callback_manager = callback_manager or CallbackManager([])
        return cls(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator=separator,
            backup_separators=backup_separators,
            keep_whitespaces=keep_whitespaces,
            callback_manager=callback_manager,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            id_func=id_func,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "TokenTextSplitter"

    defsplit_text_metadata_aware(self, text: str, metadata_str: str) -> List[str]:
"""Split text into chunks, reserving space required for metadata str."""
        metadata_len = len(self._tokenizer(metadata_str)) + DEFAULT_METADATA_FORMAT_LEN
        effective_chunk_size = self.chunk_size - metadata_len
        if effective_chunk_size <= 0:
            raise ValueError(
                f"Metadata length ({metadata_len}) is longer than chunk size "
                f"({self.chunk_size}). Consider increasing the chunk size or "
                "decreasing the size of your metadata to avoid this."
            )
        elif effective_chunk_size  50:
            print(
                f"Metadata length ({metadata_len}) is close to chunk size "
                f"({self.chunk_size}). Resulting chunks are less than 50 tokens. "
                "Consider increasing the chunk size or decreasing the size of "
                "your metadata to avoid this.",
                flush=True,
            )

        return self._split_text(text, chunk_size=effective_chunk_size)

    defsplit_text(self, text: str) -> List[str]:
"""Split text into chunks."""
        return self._split_text(text, chunk_size=self.chunk_size)

    def_split_text(self, text: str, chunk_size: int) -> List[str]:
"""Split text into chunks up to chunk_size."""
        if text == "":
            return [text]

        with self.callback_manager.event(
            CBEventType.CHUNKING, payload={EventPayload.CHUNKS: [text]}
        ) as event:
            splits = self._split(text, chunk_size)
            chunks = self._merge(splits, chunk_size)

            event.on_end(
                payload={EventPayload.CHUNKS: chunks},
            )

        return chunks

    def_split(self, text: str, chunk_size: int) -> List[str]:
"""
        Break text into splits that are smaller than chunk size.

        The order of splitting is:
        1. split by separator
        2. split by backup separators (if any)
        3. split by characters

        NOTE: the splits contain the separators.
        """
        if len(self._tokenizer(text)) <= chunk_size:
            return [text]

        for split_fn in self._split_fns:
            splits = split_fn(text)
            if len(splits)  1:
                break

        new_splits = []
        for split in splits:
            split_len = len(self._tokenizer(split))
            if split_len <= chunk_size:
                new_splits.append(split)
            else:
                # recursively split
                new_splits.extend(self._split(split, chunk_size=chunk_size))
        return new_splits

    def_merge(self, splits: List[str], chunk_size: int) -> List[str]:
"""
        Merge splits into chunks.

        The high-level idea is to keep adding splits to a chunk until we
        exceed the chunk size, then we start a new chunk with overlap.

        When we start a new chunk, we pop off the first element of the previous
        chunk until the total length is less than the chunk size.
        """
        chunks: List[str] = []

        cur_chunk: List[str] = []
        cur_len = 0
        for split in splits:
            split_len = len(self._tokenizer(split))
            if split_len  chunk_size:
                _logger.warning(
                    f"Got a split of size {split_len}, ",
                    f"larger than chunk size {chunk_size}.",
                )

            # if we exceed the chunk size after adding the new split, then
            # we need to end the current chunk and start a new one
            if cur_len + split_len  chunk_size:
                # end the previous chunk
                chunk = (
                    "".join(cur_chunk)
                    if self.keep_whitespaces
                    else "".join(cur_chunk).strip()
                )
                if chunk:
                    chunks.append(chunk)

                # start a new chunk with overlap
                # keep popping off the first element of the previous chunk until:
                #   1. the current chunk length is less than chunk overlap
                #   2. the total length is less than chunk size
                while cur_len  self.chunk_overlap or cur_len + split_len  chunk_size:
                    # pop off the first element
                    first_chunk = cur_chunk.pop(0)
                    cur_len -= len(self._tokenizer(first_chunk))

            cur_chunk.append(split)
            cur_len += split_len

        # handle the last chunk
        chunk = (
            "".join(cur_chunk) if self.keep_whitespaces else "".join(cur_chunk).strip()
        )
        if chunk:
            chunks.append(chunk)

        return chunks

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.TokenTextSplitter.from_defaults "Permanent link")

```
from_defaults(
    chunk_size:  = DEFAULT_CHUNK_SIZE,
    chunk_overlap:  = DEFAULT_CHUNK_OVERLAP,
    separator:  = " ",
    backup_separators: Optional[[]] = ["\n"],
    callback_manager: Optional[] = None,
    keep_whitespaces:  = False,
    include_metadata:  = True,
    include_prev_next_rel:  = True,
    id_func: Optional[
        Callable[[, ], ]
    ] = None,
) -> 

```

Initialize with default parameters.
Source code in `llama-index-core/llama_index/core/node_parser/text/token.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    separator: str = " ",
    backup_separators: Optional[List[str]] = ["\n"],
    callback_manager: Optional[CallbackManager] = None,
    keep_whitespaces: bool = False,
    include_metadata: bool = True,
    include_prev_next_rel: bool = True,
    id_func: Optional[Callable[[int, Document], str]] = None,
) -> "TokenTextSplitter":
"""Initialize with default parameters."""
    callback_manager = callback_manager or CallbackManager([])
    return cls(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator=separator,
        backup_separators=backup_separators,
        keep_whitespaces=keep_whitespaces,
        callback_manager=callback_manager,
        include_metadata=include_metadata,
        include_prev_next_rel=include_prev_next_rel,
        id_func=id_func,
    )

```
 |  
| --- | --- |  
###  split_text_metadata_aware [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.TokenTextSplitter.split_text_metadata_aware "Permanent link")

```
split_text_metadata_aware(
    text: , metadata_str: 
) -> []

```

Split text into chunks, reserving space required for metadata str.
Source code in `llama-index-core/llama_index/core/node_parser/text/token.py`  
| 
```
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
defsplit_text_metadata_aware(self, text: str, metadata_str: str) -> List[str]:
"""Split text into chunks, reserving space required for metadata str."""
    metadata_len = len(self._tokenizer(metadata_str)) + DEFAULT_METADATA_FORMAT_LEN
    effective_chunk_size = self.chunk_size - metadata_len
    if effective_chunk_size <= 0:
        raise ValueError(
            f"Metadata length ({metadata_len}) is longer than chunk size "
            f"({self.chunk_size}). Consider increasing the chunk size or "
            "decreasing the size of your metadata to avoid this."
        )
    elif effective_chunk_size  50:
        print(
            f"Metadata length ({metadata_len}) is close to chunk size "
            f"({self.chunk_size}). Resulting chunks are less than 50 tokens. "
            "Consider increasing the chunk size or decreasing the size of "
            "your metadata to avoid this.",
            flush=True,
        )

    return self._split_text(text, chunk_size=effective_chunk_size)

```
 |  
| --- | --- |  
###  split_text [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.TokenTextSplitter.split_text "Permanent link")

```
split_text(text: ) -> []

```

Split text into chunks.
Source code in `llama-index-core/llama_index/core/node_parser/text/token.py`  
| 
```
138
139
140
```
 | 
```
defsplit_text(self, text: str) -> List[str]:
"""Split text into chunks."""
    return self._split_text(text, chunk_size=self.chunk_size)

```
 |  
| --- | --- |  
##  get_leaf_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.get_leaf_nodes "Permanent link")

```
get_leaf_nodes(nodes: []) -> []

```

Get leaf nodes.
Source code in `llama-index-core/llama_index/core/node_parser/relational/hierarchical.py`  
| 
```
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
defget_leaf_nodes(nodes: List[BaseNode]) -> List[BaseNode]:
"""Get leaf nodes."""
    leaf_nodes = []
    for node in nodes:
        if NodeRelationship.CHILD not in node.relationships:
            leaf_nodes.append(node)
    return leaf_nodes

```
 |  
| --- | --- |  
##  get_root_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.get_root_nodes "Permanent link")

```
get_root_nodes(nodes: []) -> []

```

Get root nodes.
Source code in `llama-index-core/llama_index/core/node_parser/relational/hierarchical.py`  
| 
```
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
defget_root_nodes(nodes: List[BaseNode]) -> List[BaseNode]:
"""Get root nodes."""
    root_nodes = []
    for node in nodes:
        if NodeRelationship.PARENT not in node.relationships:
            root_nodes.append(node)
    return root_nodes

```
 |  
| --- | --- |  
##  get_child_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.get_child_nodes "Permanent link")

```
get_child_nodes(
    nodes: [], all_nodes: []
) -> []

```

Get child nodes of nodes from given all_nodes.
Source code in `llama-index-core/llama_index/core/node_parser/relational/hierarchical.py`  
| 
```
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
```
 | 
```
defget_child_nodes(nodes: List[BaseNode], all_nodes: List[BaseNode]) -> List[BaseNode]:
"""Get child nodes of nodes from given all_nodes."""
    children_ids = []
    for node in nodes:
        if NodeRelationship.CHILD not in node.relationships:
            continue

        children_ids.extend([r.node_id for r in (node.child_nodes or [])])

    child_nodes = []
    for candidate_node in all_nodes:
        if candidate_node.node_id not in children_ids:
            continue
        child_nodes.append(candidate_node)

    return child_nodes

```
 |  
| --- | --- |  
##  get_deeper_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/unstructured_element/#llama_index.core.node_parser.get_deeper_nodes "Permanent link")

```
get_deeper_nodes(
    nodes: [], depth:  = 1
) -> []

```

Get children of root nodes in given nodes that have given depth.
Source code in `llama-index-core/llama_index/core/node_parser/relational/hierarchical.py`  
| 
```
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
```
 | 
```
defget_deeper_nodes(nodes: List[BaseNode], depth: int = 1) -> List[BaseNode]:
"""Get children of root nodes in given nodes that have given depth."""
    if depth  0:
        raise ValueError("Depth cannot be a negative number!")
    root_nodes = get_root_nodes(nodes)
    if not root_nodes:
        raise ValueError("There is no root nodes in given nodes!")

    deeper_nodes = root_nodes
    for _ in range(depth):
        deeper_nodes = get_child_nodes(deeper_nodes, nodes)

    return deeper_nodes

```
 |  
| --- | --- |  
options: members: - UnstructuredElementNodeParser
