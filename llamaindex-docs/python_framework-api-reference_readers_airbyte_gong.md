# Airbyte gong
##  AirbyteGongReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/airbyte_gong/#llama_index.readers.airbyte_gong.AirbyteGongReader "Permanent link")
Bases: 
AirbyteGongReader reader.
Retrieve documents from Gong
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `config`  |  `Mapping[str, Any]`  |  The config object for the gong source.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-airbyte-gong/llama_index/readers/airbyte_gong/base.py`  
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
classAirbyteGongReader(AirbyteCDKReader):
"""
    AirbyteGongReader reader.

    Retrieve documents from Gong

    Args:
        config: The config object for the gong source.

    """

    def__init__(
        self,
        config: Mapping[str, Any],
        record_handler: Optional[RecordHandler] = None,
    ) -> None:
"""Initialize with parameters."""
        importsource_gong

        super().__init__(
            source_class=source_gong.SourceGong,
            config=config,
            record_handler=record_handler,
        )

```
 |  
| --- | --- |  
options: members: - AirbyteGongReader
