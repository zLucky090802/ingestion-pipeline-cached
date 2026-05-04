# Presidio
##  PresidioPIINodePostprocessor [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/presidio/#llama_index.postprocessor.presidio.PresidioPIINodePostprocessor "Permanent link")
Bases: 
presidio PII Node processor. Uses a presidio to analyse PIIs.
Source code in `llama-index-integrations/postprocessor/llama-index-postprocessor-presidio/llama_index/postprocessor/presidio/base.py`  
| 
```
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
```
 | 
```
classPresidioPIINodePostprocessor(BaseNodePostprocessor):
"""
    presidio PII Node processor.
    Uses a presidio to analyse PIIs.
    """

    pii_node_info_key: str = "__pii_node_info__"
    entity_mapping: Dict[str, Dict] = Field(default_factory=dict)
    mapping: Dict[str, str] = Field(default_factory=dict)
    presidio_entities: List = Field(default_factory=list)

    @classmethod
    defclass_name(cls) -> str:
        return "PresidioPIINodePostprocessor"

    defmask_pii(self, text: str) -> Tuple[str, Dict]:
        analyzer = AnalyzerEngine()
        results = analyzer.analyze(
            text=text, language="en", entities=self.presidio_entities
        )
        engine = AnonymizerEngine()
        engine.add_anonymizer(EntityTypeCountAnonymizer)

        new_text = engine.anonymize(
            text=text,
            analyzer_results=results,
            operators={
                "DEFAULT": OperatorConfig(
                    "EntityTypeCountAnonymizer",
                    {
                        "entity_mapping": self.entity_mapping,
                        "deanonymize_mapping": self.mapping,
                    },
                )
            },
        )

        return new_text.text

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""
        # swap out text from nodes, with the original node mappings
        new_nodes = []
        for node_with_score in nodes:
            node = node_with_score.node
            new_text = self.mask_pii(node.get_content(metadata_mode=MetadataMode.LLM))
            new_node = deepcopy(node)
            new_node.excluded_embed_metadata_keys.append(self.pii_node_info_key)
            new_node.excluded_llm_metadata_keys.append(self.pii_node_info_key)
            new_node.metadata[self.pii_node_info_key] = self.mapping
            new_node.set_content(new_text)
            new_nodes.append(NodeWithScore(node=new_node, score=node_with_score.score))

        return new_nodes

```
 |  
| --- | --- |  
options: members: - PresidioPIINodePostprocessor
