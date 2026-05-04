# Airbyte cdk
##  AirbyteCDKReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/airbyte_cdk/#llama_index.readers.airbyte_cdk.AirbyteCDKReader "Permanent link")
Bases: 
AirbyteCDKReader reader.
Retrieve documents from an Airbyte source implemented using the CDK.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `source_class`  |  The Airbyte source class.  |  _required_  |  
|  `config`  |  `Mapping[str, Any]`  |  The config object for the Airbyte source.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-airbyte-cdk/llama_index/readers/airbyte_cdk/base.py`  
| 
```
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
classAirbyteCDKReader(BaseReader):
"""
    AirbyteCDKReader reader.

    Retrieve documents from an Airbyte source implemented using the CDK.

    Args:
        source_class: The Airbyte source class.
        config: The config object for the Airbyte source.

    """

    def__init__(
        self,
        source_class: Any,
        config: Mapping[str, Any],
        record_handler: Optional[RecordHandler] = None,
    ) -> None:
"""Initialize with parameters."""
        fromairbyte_cdk.models.airbyte_protocolimport AirbyteRecordMessage
        fromairbyte_cdk.sources.embedded.base_integrationimport (
            BaseEmbeddedIntegration,
        )
        fromairbyte_cdk.sources.embedded.runnerimport CDKRunner

        classCDKIntegration(BaseEmbeddedIntegration):
            def_handle_record(
                self, record: AirbyteRecordMessage, id: Optional[str]
            ) -> Document:
                if record_handler:
                    return record_handler(record, id)
                return Document(
                    doc_id=id, text=json.dumps(record.data), extra_info=record.data
                )

        self._integration = CDKIntegration(
            config=config,
            runner=CDKRunner(source=source_class(), name=source_class.__name__),
        )

    defload_data(self, *args: Any, **kwargs: Any) -> List[Document]:
        return list(self.lazy_load_data(*args, **kwargs))

    deflazy_load_data(self, *args: Any, **kwargs: Any) -> Iterator[Document]:
        return self._integration._load_data(*args, **kwargs)

    @property
    deflast_state(self):
        return self._integration.last_state

```
 |  
| --- | --- |  
options: members: - AirbyteCDKReader
