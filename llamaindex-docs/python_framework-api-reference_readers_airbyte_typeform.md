# Airbyte typeform
##  AirbyteTypeformReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/airbyte_typeform/#llama_index.readers.airbyte_typeform.AirbyteTypeformReader "Permanent link")
Bases: 
AirbyteTypeformReader reader.
Retrieve documents from Typeform
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `config`  |  `Mapping[str, Any]`  |  The config object for the typeform source.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-airbyte-typeform/llama_index/readers/airbyte_typeform/base.py`  
| 
```
 6
 7
 8
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
```
 | 
```
classAirbyteTypeformReader(AirbyteCDKReader):
"""
    AirbyteTypeformReader reader.

    Retrieve documents from Typeform

    Args:
        config: The config object for the typeform source.

    """

    def__init__(
        self,
        config: Mapping[str, Any],
        record_handler: Optional[RecordHandler] = None,
    ) -> None:
"""Initialize with parameters."""
        importsource_typeform

        super().__init__(
            source_class=source_typeform.SourceTypeform,
            config=config,
            record_handler=record_handler,
        )

```
 |  
| --- | --- |  
options: members: - AirbyteTypeformReader
