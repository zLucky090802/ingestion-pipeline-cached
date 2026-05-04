# Marvin
##  MarvinMetadataExtractor [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/marvin/#llama_index.extractors.marvin.MarvinMetadataExtractor "Permanent link")
Bases: 
Source code in `llama-index-integrations/extractors/llama-index-extractors-marvin/llama_index/extractors/marvin/base.py`  
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
```
 | 
```
classMarvinMetadataExtractor(BaseExtractor):
    # Forward reference to handle circular imports
    marvin_model: Type[BaseModel] = Field(
        description="The target pydantic model to cast the metadata into."
    )

"""Metadata extractor for custom metadata using Marvin.
    Node-level extractor. Extracts
    `marvin_metadata` metadata field.
    Args:
        marvin_model: The target pydantic model to cast the metadata into.
    Usage:
        #create extractor list
        extractors = [
            TitleExtractor(nodes=1, llm=llm),
            MarvinMetadataExtractor(marvin_model=YourMetadataModel),


        #create node parser to parse nodes from document
        node_parser = SentenceSplitter(
            text_splitter=text_splitter


        #use node_parser to get nodes from documents
        from llama_index.ingestion import run_transformations
        nodes = run_transformations(documents, [node_parser] + extractors)
        print(nodes)
    """

    def__init__(
        self,
        marvin_model: Type[BaseModel],
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__(marvin_model=marvin_model, **kwargs)

    @classmethod
    defclass_name(cls) -> str:
        return "MarvinEntityExtractor"

    async defaextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
        frommarvinimport cast_async

        metadata_list: List[Dict] = []

        nodes_queue: Iterable[BaseNode] = get_tqdm_iterable(
            nodes, self.show_progress, "Extracting marvin metadata"
        )
        for node in nodes_queue:
            if self.is_text_node_only and not isinstance(node, TextNode):
                metadata_list.append({})
                continue

            metadata = await cast_async(node.get_content(), target=self.marvin_model)

            metadata_list.append({"marvin_metadata": metadata.model_dump()})
        return metadata_list

```
 |  
| --- | --- |  
###  marvin_model `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/marvin/#llama_index.extractors.marvin.MarvinMetadataExtractor.marvin_model "Permanent link")

```
marvin_model: [BaseModel] = Field(
    description="The target pydantic model to cast the metadata into."
)

```

Metadata extractor for custom metadata using Marvin. Node-level extractor. Extracts `marvin_metadata` metadata field. Args: marvin_model: The target pydantic model to cast the metadata into. Usage: #create extractor list extractors = [ TitleExtractor(nodes=1, llm=llm), MarvinMetadataExtractor(marvin_model=YourMetadataModel), ]

```
#create node parser to parse nodes from document
node_parser = SentenceSplitter(
    text_splitter=text_splitter
)

#use node_parser to get nodes from documents
from llama_index.ingestion import run_transformations
nodes = run_transformations(documents, [node_parser] + extractors)
print(nodes)

```

options: members: - MarvinMetadataExtractor
