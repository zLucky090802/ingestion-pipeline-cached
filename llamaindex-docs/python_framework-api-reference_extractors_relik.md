# Relik
##  RelikPathExtractor [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/relik/#llama_index.extractors.relik.RelikPathExtractor "Permanent link")
Bases: 
A transformer class for converting documents into graph structures. Uses the Relik library and models. This class leverages relik models for extracting relationships and nodes from text documents and converting them into a graph format. The relationships are filtered based on a specified confidence threshold. For more details on the Relik library, visit their GitHub repository: https://github.com/SapienzaNLP/relik Args: model (str): The name of the pretrained Relik model to use. Default is "relik-ie/relik-relation-extraction-small-wikipedia". relationship_confidence_threshold (float): The confidence threshold for filtering relationships. Default is 0.1. skip_errors (bool): Whether to skip errors during extraction. Defaults to False.
Source code in `llama-index-integrations/extractors/llama-index-extractors-relik/llama_index/extractors/relik/base.py`  
| 
```
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
```
 | 
```
classRelikPathExtractor(TransformComponent):
"""
    A transformer class for converting documents into graph structures.
    Uses the Relik library and models.
    This class leverages relik models for extracting relationships
    and nodes from text documents and converting them into a graph format.
    The relationships are filtered based on a specified confidence threshold.
    For more details on the Relik library, visit their GitHub repository:
      https://github.com/SapienzaNLP/relik
    Args:
        model (str): The name of the pretrained Relik model to use.
          Default is "relik-ie/relik-relation-extraction-small-wikipedia".
        relationship_confidence_threshold (float): The confidence threshold for
          filtering relationships. Default is 0.1.
        skip_errors (bool): Whether to skip errors during extraction. Defaults to False.
    """

    relik_model: Any
    relationship_confidence_threshold: float
    num_workers: int
    skip_errors: bool
    ignore_self_loops: bool

    def__init__(
        self,
        model: str = "relik-ie/relik-relation-extraction-small",
        relationship_confidence_threshold: float = 0.1,
        skip_errors: bool = False,
        num_workers: int = 4,
        model_config: Dict[str, Any] = {},
        ignore_self_loops: bool = True,
    ) -> None:
"""Init params."""
        try:
            importrelik  # type: ignore

            # Remove default INFO logging
            logging.getLogger("relik").setLevel(logging.WARNING)
        except ImportError:
            raise ImportError(
                "Could not import relik python package. "
                "Please install it with `pip install relik`."
            )

        relik_model = relik.Relik.from_pretrained(model, **model_config)

        super().__init__(
            relik_model=relik_model,
            relationship_confidence_threshold=relationship_confidence_threshold,
            num_workers=num_workers,
            skip_errors=skip_errors,
            ignore_self_loops=ignore_self_loops,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "RelikPathExtractor"

    def__call__(
        self, nodes: List[BaseNode], show_progress: bool = False, **kwargs: Any
    ) -> List[BaseNode]:
"""Extract triples from nodes."""
        result_nodes = []
        for node in tqdm.tqdm(
            nodes, desc="Extracting triples", disable=not show_progress
        ):
            result_nodes.append(self._extract(node))

        return result_nodes

    def_extract(self, node: BaseNode) -> BaseNode:
"""Extract triples from a node."""
        assert hasattr(node, "text")

        text = node.get_content(metadata_mode="llm")
        try:
            relik_out = self.relik_model(text)
        except Exception as e:
            if self.skip_errors:
                node.metadata[KG_NODES_KEY] = node.metadata.get(KG_NODES_KEY, [])
                node.metadata[KG_RELATIONS_KEY] = node.metadata.get(
                    KG_RELATIONS_KEY, []
                )
                return node
            raise ValueError(f"Failed to extract triples from text: {e}")

        existing_nodes = node.metadata.pop(KG_NODES_KEY, [])
        existing_relations = node.metadata.pop(KG_RELATIONS_KEY, [])

        metadata = node.metadata.copy()
        # Extract nodes
        for n in relik_out.spans:
            existing_nodes.append(
                EntityNode(
                    name=n.text,
                    label=DEFAULT_NODE_TYPE
                    if n.label.strip() == "--NME--"
                    else n.label.strip(),
                    properties=metadata,
                )
            )
        # Extract relationships
        for triple in relik_out.triplets:
            # Ignore relationship if below confidence threshold
            if triple.confidence  self.relationship_confidence_threshold:
                continue
            # Ignore self loops
            if self.ignore_self_loops and triple.subject.text == triple.object.text:
                continue
            rel_node = Relation(
                label=triple.label.replace(" ", "_").upper(),
                source_id=triple.subject.text,
                target_id=triple.object.text,
                properties=metadata,
            )

            existing_relations.append(rel_node)

        node.metadata[KG_NODES_KEY] = existing_nodes
        node.metadata[KG_RELATIONS_KEY] = existing_relations

        return node

    async defacall(
        self, nodes: List[BaseNode], show_progress: bool = False, **kwargs: Any
    ) -> List[BaseNode]:
"""Extract triples from nodes async."""
        return self.__call__(nodes, show_progress=show_progress, **kwargs)

```
 |  
| --- | --- |  
###  acall [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/relik/#llama_index.extractors.relik.RelikPathExtractor.acall "Permanent link")

```
acall(
    nodes: [],
    show_progress:  = False,
    **kwargs: 
) -> []

```

Extract triples from nodes async.
Source code in `llama-index-integrations/extractors/llama-index-extractors-relik/llama_index/extractors/relik/base.py`  
| 
```
139
140
141
142
143
```
 | 
```
async defacall(
    self, nodes: List[BaseNode], show_progress: bool = False, **kwargs: Any
) -> List[BaseNode]:
"""Extract triples from nodes async."""
    return self.__call__(nodes, show_progress=show_progress, **kwargs)

```
 |  
| --- | --- |  
options: members: - RelikPathExtractor
